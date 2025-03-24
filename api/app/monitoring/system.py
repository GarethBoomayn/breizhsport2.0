import os
import psutil
import threading
import time
from prometheus_client import Gauge
from .logger import app_logger

# Métriques système
cpu_usage = Gauge(
    "system_cpu_usage_percent", 
    "CPU usage in percent"
)

memory_usage = Gauge(
    "system_memory_usage_bytes", 
    "Memory usage in bytes"
)

memory_total = Gauge(
    "system_memory_total_bytes", 
    "Total memory in bytes"
)

memory_percent = Gauge(
    "system_memory_usage_percent", 
    "Memory usage in percent"
)

disk_usage = Gauge(
    "system_disk_usage_bytes", 
    "Disk usage in bytes", 
    ["mountpoint"]
)

disk_total = Gauge(
    "system_disk_total_bytes", 
    "Total disk space in bytes", 
    ["mountpoint"]
)

disk_percent = Gauge(
    "system_disk_usage_percent", 
    "Disk usage in percent", 
    ["mountpoint"]
)

open_files = Gauge(
    "system_open_files", 
    "Number of open files"
)

# Métriques de l'application
api_uptime = Gauge(
    "api_uptime_seconds", 
    "API uptime in seconds"
)

process_threads = Gauge(
    "process_threads_count", 
    "Number of threads in the process"
)

process_memory = Gauge(
    "process_memory_bytes", 
    "Memory used by the process in bytes"
)

process_connections = Gauge(
    "process_connections_count", 
    "Number of network connections"
)


class SystemMetricsCollector:
    """
    Collecteur de métriques système qui s'exécute en arrière-plan
    """
    
    def __init__(self, interval=15):
        """
        Initialise le collecteur de métriques système
        
        Args:
            interval: Intervalle en secondes entre les collectes de métriques
        """
        self.interval = interval
        self.thread = None
        self.stop_event = threading.Event()
        self.start_time = time.time()

    def start(self):
        """Démarre la collecte de métriques système en arrière-plan"""
        if self.thread is not None:
            return
        
        app_logger.info("Démarrage de la collecte de métriques système")
        self.thread = threading.Thread(target=self._collect_metrics_loop, daemon=True)
        self.thread.start()
        
    def stop(self):
        """Arrête la collecte de métriques système"""
        if self.thread is None:
            return
        
        app_logger.info("Arrêt de la collecte de métriques système")
        self.stop_event.set()
        self.thread.join(timeout=5)
        self.thread = None
    
    def _collect_metrics_loop(self):
        """Boucle de collecte de métriques système"""
        while not self.stop_event.is_set():
            try:
                self._collect_metrics()
            except Exception as e:
                app_logger.error(f"Erreur lors de la collecte des métriques système: {str(e)}")
            
            # Attendre l'intervalle spécifié ou jusqu'à ce que l'événement d'arrêt soit défini
            self.stop_event.wait(timeout=self.interval)
    
    def _collect_metrics(self):
        """Collecte les métriques système et les enregistre dans Prometheus"""
        # Métriques CPU
        cpu_usage.set(psutil.cpu_percent(interval=1))
        
        # Métriques mémoire
        memory = psutil.virtual_memory()
        memory_usage.set(memory.used)
        memory_total.set(memory.total)
        memory_percent.set(memory.percent)
        
        # Métriques disque
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage.labels(mountpoint=partition.mountpoint).set(usage.used)
                disk_total.labels(mountpoint=partition.mountpoint).set(usage.total)
                disk_percent.labels(mountpoint=partition.mountpoint).set(usage.percent)
            except (PermissionError, FileNotFoundError):
                # Ignorer les partitions inaccessibles
                pass
        
        # Métriques de fichiers ouverts
        open_files.set(len(psutil.Process().open_files()))
        
        # Métriques de l'application
        process = psutil.Process(os.getpid())
        api_uptime.set(time.time() - self.start_time)
        process_threads.set(process.num_threads())
        process_memory.set(process.memory_info().rss)
        process_connections.set(len(process.connections()))


# Singleton pour l'utilisation dans l'application
system_metrics_collector = SystemMetricsCollector()
