import logging
import json
import os
import sys
from pythonjsonlogger import jsonlogger

# Configuration de l'environnement
ENV = os.getenv("ENVIRONMENT", "development")
SERVICE_NAME = "breizhsport-api"

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """
    Formateur personnalisé pour les logs au format JSON.
    """
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["service"] = SERVICE_NAME
        log_record["env"] = ENV
        log_record["level"] = record.levelname
        log_record["timestamp"] = self.formatTime(record, self.datefmt)
        
        # Ajout d'informations de traçage si disponibles
        if hasattr(record, "trace_id"):
            log_record["trace_id"] = record.trace_id
        if hasattr(record, "span_id"):
            log_record["span_id"] = record.span_id

def get_logger(name: str) -> logging.Logger:
    """
    Crée et configure un logger avec le nom spécifié.
    
    Args:
        name: Le nom du logger, généralement __name__
        
    Returns:
        Un logger configuré
    """
    logger = logging.getLogger(name)
    
    # Éviter la duplication des handlers en cas de plusieurs appels
    if logger.handlers:
        return logger
    
    # Configurer le niveau de log selon l'environnement
    if ENV.lower() == "production":
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.DEBUG)
    
    # Créer un handler pour stdout
    handler = logging.StreamHandler(sys.stdout)
    
    # Utiliser le formateur JSON
    formatter = CustomJsonFormatter(
        "%(timestamp)s %(level)s %(name)s %(message)s"
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    return logger

# Logger par défaut pour l'application
app_logger = get_logger("breizhsport")
