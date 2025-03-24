import pytest
import uuid
from datetime import datetime
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
def sample_user():
    # Utilisation d'un identifiant unique pour éviter les conflits
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"test_{unique_id}@example.com",
        "username": f"testuser_{unique_id}",
        "password": "testpassword",
        "full_name": "Test User"
    }

@pytest.fixture
def sample_admin_user():
    # Utilisation d'un identifiant unique pour éviter les conflits
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"admin_{unique_id}@example.com",
        "username": f"adminuser_{unique_id}",
        "password": "adminpassword",
        "full_name": "Admin User",
        "is_admin": True
    }

def test_create_user(client, sample_user):
    response = client.post("/auth/register", json=sample_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user["email"]
    assert data["username"] == sample_user["username"]
    assert data["full_name"] == sample_user["full_name"]
    assert "password" not in data
    assert "hashed_password" not in data

def test_create_duplicate_email(client, sample_user):
    # Créer le premier utilisateur
    response = client.post("/auth/register", json=sample_user)
    assert response.status_code == 200
    
    # Tenter de créer un utilisateur avec le même email
    duplicate_user = sample_user.copy()
    duplicate_user["username"] = f"another_user_{str(uuid.uuid4())[:8]}"
    response = client.post("/auth/register", json=duplicate_user)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_create_duplicate_username(client, sample_user):
    # Créer le premier utilisateur
    response = client.post("/auth/register", json=sample_user)
    assert response.status_code == 200
    
    # Tenter de créer un utilisateur avec le même username
    duplicate_user = sample_user.copy()
    duplicate_user["email"] = f"another_{str(uuid.uuid4())[:8]}@example.com"
    response = client.post("/auth/register", json=duplicate_user)
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

def test_login_success(client, sample_user):
    # Créer l'utilisateur
    client.post("/auth/register", json=sample_user)
    
    # Tenter de se connecter
    login_data = {
        "username": sample_user["email"],  # Le username est l'email pour le login
        "password": sample_user["password"]
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, sample_user):
    # Créer l'utilisateur
    client.post("/auth/register", json=sample_user)
    
    # Tenter de se connecter avec un mauvais mot de passe
    login_data = {
        "username": sample_user["email"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/token", data=login_data)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

def test_get_current_user(client, sample_user):
    # Créer l'utilisateur
    client.post("/auth/register", json=sample_user)
    
    # Se connecter pour obtenir le token
    login_data = {
        "username": sample_user["email"],
        "password": sample_user["password"]
    }
    response = client.post("/auth/token", data=login_data)
    token = response.json()["access_token"]
    
    # Récupérer les informations de l'utilisateur connecté
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user["email"]
    assert data["username"] == sample_user["username"]

def test_get_current_user_invalid_token(client):
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]

def test_get_current_user_no_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

def test_admin_flag_is_false_by_default(client, sample_admin_user):
    # Créer l'utilisateur avec le flag is_admin=True dans la requête
    response = client.post("/auth/register", json=sample_admin_user)
    assert response.status_code == 200
    
    # Se connecter pour obtenir le token
    login_data = {
        "username": sample_admin_user["email"],
        "password": sample_admin_user["password"]
    }
    response = client.post("/auth/token", data=login_data)
    token = response.json()["access_token"]
    
    # Vérifier que l'utilisateur n'est PAS admin malgré la demande
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["is_admin"] is False  # Vérifie que is_admin est False par défaut
