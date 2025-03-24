from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database.config import get_db
from ..monitoring import app_logger, create_span

router = APIRouter(
    prefix="/health",
    tags=["health"]
)

@router.get("")
async def health_check(db: Session = Depends(get_db)):
    """
    Endpoint de vérification de la santé de l'API
    Vérifie la connectivité avec la base de données
    """
    with create_span("health_check"):
        try:
            # Utiliser text() pour la requête SQL textuelle
            db.execute(text("SELECT 1"))
            db_status = "connected"
            app_logger.info("Health check réussi - Base de données connectée")
        except Exception as e:
            db_status = "disconnected"
            app_logger.error(f"Health check échoué - Problème de base de données: {str(e)}")
            
        return {
            "status": "healthy",
            "database": db_status,
            "version": "1.0.0"
        }
