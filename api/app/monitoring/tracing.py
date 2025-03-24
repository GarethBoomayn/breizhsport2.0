from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import os
from tenacity import retry, stop_after_attempt, wait_exponential

# Configuration de l'environnement
SERVICE = "breizhsport-api"
OTLP_ENDPOINT = os.getenv("OTLP_ENDPOINT", "http://jaeger:4318/v1/traces")

def setup_tracing(app=None):
    """
    Configure le tracing OpenTelemetry pour l'application
    
    Args:
        app: Instance de l'application FastAPI
    """
    # Créer un resource avec les métadonnées du service
    resource = Resource(attributes={
        SERVICE_NAME: SERVICE
    })
    
    # Configurer le TracerProvider avec ce resource
    provider = TracerProvider(resource=resource)
    
    # Créer un exporteur OTLP avec retry en cas d'échec
    @retry(
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True
    )
    def create_otlp_exporter():
        return OTLPSpanExporter(endpoint=OTLP_ENDPOINT)
    
    try:
        otlp_exporter = create_otlp_exporter()
        processor = BatchSpanProcessor(otlp_exporter)
        provider.add_span_processor(processor)
        
        # Définir le provider global
        trace.set_tracer_provider(provider)
        
        # Si une app FastAPI est fournie, l'instrumenter
        if app:
            FastAPIInstrumentor.instrument_app(app)
            
        return True
    except Exception as e:
        # Si l'initialisation du tracing échoue, logger l'erreur
        # mais continuer l'exécution de l'application
        print(f"Erreur lors de l'initialisation du tracing: {str(e)}")
        return False

def get_tracer():
    """
    Récupère un tracer pour créer des spans personnalisés
    
    Returns:
        Une instance de Tracer
    """
    return trace.get_tracer(SERVICE)

# Fonction utilitaire pour créer un span personnalisé
def create_span(name, parent_span=None):
    tracer = get_tracer()
    return tracer.start_as_current_span(name, context=parent_span)
