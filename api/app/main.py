import uvicorn
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from prometheus_client import make_asgi_app, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

from .database.config import engine, Base, get_db
from .models import models
from .routes import products, categories, auth, health
from .monitoring import app_logger, setup_tracing, system_metrics_collector
from .monitoring.metrics import http_requests_total, http_request_duration_seconds

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BreizhSport API",
    description="API pour l'application e-commerce BreizhSport",
    version="2.0.0"
)

# Initialisation du tracing
setup_tracing(app)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À remplacer par les domaines autorisés en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware pour collecter les métriques
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Traitement de la requête
    response = await call_next(request)
    
    # Collecte des métriques
    duration = time.time() - start_time
    status_code = response.status_code
    endpoint = request.url.path
    method = request.method
    
    # Enregistrement des métriques
    http_requests_total.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code
    ).inc()
    
    http_request_duration_seconds.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)
    
    return response

# Endpoint pour les métriques Prometheus
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# Démarrer le collecteur de métriques système
@app.on_event("startup")
async def startup_event():
    system_metrics_collector.start()
    app_logger.info("Démarrage de l'application BreizhSport API")

# Arrêter le collecteur de métriques système à l'arrêt de l'application
@app.on_event("shutdown")
async def shutdown_event():
    system_metrics_collector.stop()
    app_logger.info("Arrêt de l'application BreizhSport API")

# Inclure les routes
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(health.router)

@app.get("/")
async def root():
    app_logger.info("Accès à la racine de l'API")
    return {"message": "Bienvenue sur l'API Breizhsport 2.0"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Vérifier la connexion à la base de données
        db.execute(text("SELECT 1"))
        db_status = "healthy"
        app_logger.info("Health check réussi")
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
        app_logger.error(f"Health check échoué: {str(e)}")
    
    return {
        "status": "healthy",
        "database": db_status
    }
