#!/bin/bash

# Script de déploiement de l'infrastructure de monitoring pour Breizhsport 2.0
echo "Configuration de l'infrastructure de monitoring pour Breizhsport 2.0"

# Vérification que Docker et Docker Compose sont installés
if ! command -v docker &> /dev/null || ! command -v docker-compose &> /dev/null; then
    echo "Docker et/ou Docker Compose ne sont pas installés."
    echo "Veuillez les installer avant de continuer."
    exit 1
fi

# Création des répertoires de configuration s'ils n'existent pas
mkdir -p monitoring/prometheus
mkdir -p monitoring/grafana/provisioning/datasources
mkdir -p monitoring/grafana/dashboards

# Vérification que les fichiers de configuration existent
if [ ! -f monitoring/prometheus/prometheus.yml ]; then
    echo "Le fichier de configuration Prometheus est manquant."
    exit 1
fi

if [ ! -f monitoring/grafana/provisioning/datasources/prometheus.yml ]; then
    echo "Le fichier de configuration de la source de données Grafana est manquant."
    exit 1
fi

if [ ! -f monitoring/grafana/provisioning/dashboards/dashboards.yml ]; then
    echo "Le fichier de configuration des dashboards Grafana est manquant."
    exit 1
fi

# Démarrage des services
echo "Démarrage des services de monitoring..."
docker-compose up -d prometheus grafana jaeger

# Attendre que les services soient démarrés
echo "Attente du démarrage des services..."
sleep 10

# Vérification que les services sont bien démarrés
echo "Vérification des services:"
echo "- Prometheus: http://localhost:9090"
echo "- Grafana: http://localhost:3000 (utilisateur: admin, mot de passe: admin)"
echo "- Jaeger: http://localhost:16686"

echo ""
echo "Configuration terminée avec succès!"
echo "Vous pouvez maintenant accéder aux tableaux de bord pour surveiller votre application."
echo ""
echo "Notes importantes:"
echo "1. Les métriques sont disponibles à l'adresse: http://localhost:8000/metrics"
echo "2. Les logs sont formatés en JSON pour une meilleure intégration avec des outils comme ELK"
echo "3. Le tracing distribué est configuré pour envoyer des données à Jaeger"
