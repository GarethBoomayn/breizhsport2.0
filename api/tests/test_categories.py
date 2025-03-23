import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.config import Base
from app.dependencies import get_db

# Configuration de la base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def sample_category():
    return {
        "name": "Test Category",
        "description": "Test Description"
    }

def test_create_category(client, sample_category):
    response = client.post("/categories/", json=sample_category)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_category["name"]
    assert data["description"] == sample_category["description"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_create_duplicate_category(client, sample_category):
    # Première création
    client.post("/categories/", json=sample_category)
    # Tentative de création avec le même nom
    response = client.post("/categories/", json=sample_category)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_read_categories(client, sample_category):
    # Créer quelques catégories
    client.post("/categories/", json=sample_category)
    client.post("/categories/", json={
        "name": "Another Category",
        "description": "Another Description"
    })
    
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == sample_category["name"]

def test_read_category(client, sample_category):
    # Créer une catégorie
    create_response = client.post("/categories/", json=sample_category)
    category_id = create_response.json()["id"]
    
    # Lire la catégorie
    response = client.get(f"/categories/{category_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_category["name"]
    assert data["description"] == sample_category["description"]

def test_read_nonexistent_category(client):
    response = client.get("/categories/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_update_category(client, sample_category):
    # Créer une catégorie
    create_response = client.post("/categories/", json=sample_category)
    category_id = create_response.json()["id"]
    
    # Mettre à jour la catégorie
    updated_data = {
        "name": "Updated Category",
        "description": "Updated Description"
    }
    response = client.put(f"/categories/{category_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["description"] == updated_data["description"]

def test_update_nonexistent_category(client, sample_category):
    response = client.put("/categories/999", json=sample_category)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_delete_category(client, sample_category):
    # Créer une catégorie
    create_response = client.post("/categories/", json=sample_category)
    category_id = create_response.json()["id"]
    
    # Supprimer la catégorie
    response = client.delete(f"/categories/{category_id}")
    assert response.status_code == 200
    
    # Vérifier que la catégorie n'existe plus
    get_response = client.get(f"/categories/{category_id}")
    assert get_response.status_code == 404

def test_delete_nonexistent_category(client):
    response = client.delete("/categories/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
