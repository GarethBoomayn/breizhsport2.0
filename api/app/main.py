from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from .database.config import engine, Base, get_db
from .models import models
from .routes import products, categories, auth

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BreizhSport API",
    description="API pour l'application e-commerce BreizhSport",
    version="2.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À remplacer par les domaines autorisés en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)

@app.get("/")
async def root():
    return {"message": "Bienvenue sur l'API Breizhsport 2.0"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Vérifier la connexion à la base de données
        db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status
    }
