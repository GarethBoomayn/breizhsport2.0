from prometheus_client import Counter, Histogram, Gauge, Summary
import time
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
from starlette.types import ASGIApp

# Métriques standard pour l'API
# Compteurs
http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status_code"]
)

db_queries_total = Counter(
    "db_queries_total",
    "Total number of database queries",
    ["operation", "table"]
)

auth_success_total = Counter(
    "auth_success_total",
    "Total number of successful authentications",
    ["method"]  # 'login', 'token_refresh', etc.
)

auth_failure_total = Counter(
    "auth_failure_total",
    "Total number of failed authentications",
    ["method", "reason"]  # 'wrong_password', 'user_not_found', etc.
)

# Histogrammes pour mesurer la latence
http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)
)

db_query_duration_seconds = Histogram(
    "db_query_duration_seconds",
    "Database query duration in seconds",
    ["operation", "table"],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0)
)

# Jauges pour mesurer les valeurs qui montent et descendent
active_users_count = Gauge(
    "active_users_count",
    "Number of currently active users"
)

db_connection_pool_size = Gauge(
    "db_connection_pool_size",
    "Size of the database connection pool"
)

# Résumés pour les statistiques
response_size_bytes = Summary(
    "response_size_bytes",
    "Response size in bytes",
    ["endpoint"]
)

class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware pour collecter des métriques HTTP
    """
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
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
        
        # Si la taille de la réponse est disponible
        if hasattr(response, "content_length") and response.content_length:
            response_size_bytes.labels(endpoint=endpoint).observe(response.content_length)
        
        return response
