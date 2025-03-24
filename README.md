# Breizhsport 2.0

Application e-commerce moderne pour Breizhsport, développée avec FastAPI, Vue.js et Docker.

## Architecture

- **Frontend**: Vue.js 3 avec TypeScript et Tailwind CSS
- **Backend**: FastAPI (Python 3.11)
- **Cache**: Redis
- **Base de données**: PostgreSQL
- **Reverse Proxy**: Nginx
- **Monitoring**: Prometheus, Grafana, Jaeger (OpenTelemetry)
- **Conteneurisation**: Docker & Docker Compose

## État d'avancement

### Fonctionnalités implémentées

- **Architecture**
  - Configuration complète de l'environnement Docker
  - Mise en place du reverse proxy Nginx
  - Configuration de la base de données PostgreSQL
  - Configuration du cache Redis
  - Intégration du frontend Vue.js avec le backend

- **API**
  - Configuration FastAPI avec dernières versions (SQLAlchemy 2.0, Pydantic 2.0)
  - Gestion complète des catégories (CRUD)
  - Gestion des produits (CRUD)
  - Tests unitaires avec pytest
  - Gestion des erreurs HTTP
  - Configuration CORS
  - Système d'authentification avec JWT

- **Frontend**
  - Interface utilisateur moderne avec Vue 3 et Composition API
  - Styling avec Tailwind CSS 4.0
  - Routing avec Vue Router
  - Gestion d'état avec Pinia
  - Support TypeScript complet
  - Tests unitaires avec Vitest
  - Tests E2E avec Nightwatch

- **Modèles de données**
  - Utilisateurs
  - Catégories
  - Produits
  - Commandes
  - Articles de commande

- **Monitoring et Observabilité**
  - Logs structurés en JSON
  - Métriques Prometheus pour les requêtes HTTP et la base de données
  - Métriques système (CPU, mémoire, disque)
  - Tracing distribué avec OpenTelemetry et Jaeger
  - Dashboards Grafana préconfigurés
  - Endpoint de health check pour surveiller l'état de l'application

### En cours de développement

- Système de panier avec Redis
- Gestion des commandes
- Pipeline CI/CD
- Tests de performance

## Prérequis

- Docker
- Docker Compose
- Python 3.11+ (pour le développement local)
- Node.js 22+ (pour le développement local)

## Installation

1. Cloner le repository
```bash
git clone https://github.com/GarethBoomayn/breizhsport2.0.git
cd breizhsport2.0
```

2. Créer un fichier .env dans le dossier api/ avec les variables suivantes :
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/breizhsport
REDIS_URL=redis://cache:6379/0
ENVIRONMENT=development
OTLP_ENDPOINT=http://jaeger:4318/v1/traces
```

3. Lancer l'application avec Docker Compose
```bash
docker-compose up --build
```

4. (Optionnel) Configurer l'infrastructure de monitoring
```bash
chmod +x setup-monitoring.sh
./setup-monitoring.sh
```

L'application sera accessible à l'adresse : http://localhost:80
- Frontend: http://localhost:80
- API: http://localhost:80/api
- API directe: http://localhost:8000
- Frontend dev server: http://localhost:5173
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/admin)
- Jaeger: http://localhost:16686

## Structure du Projet

```
breizhsport2.0/
├── api/                      # Service API principal
│   ├── app/                 # Code source de l'API
│   │   ├── auth/           # Authentification et sécurité
│   │   ├── crud/           # Opérations CRUD
│   │   ├── database/       # Configuration base de données
│   │   ├── models/         # Modèles SQLAlchemy
│   │   ├── monitoring/     # Monitoring et observabilité
│   │   │   ├── logger.py   # Logs structurés en JSON
│   │   │   ├── metrics.py  # Métriques Prometheus
│   │   │   ├── system.py   # Métriques système
│   │   │   └── tracing.py  # Tracing distribué (OpenTelemetry)
│   │   ├── routes/         # Routes API
│   │   │   ├── auth.py     # Endpoints d'authentification
│   │   │   ├── categories.py # Gestion des catégories
│   │   │   ├── health.py   # Health check
│   │   │   └── products.py # Gestion des produits
│   │   └── schemas/        # Schémas Pydantic
│   ├── tests/              # Tests unitaires et d'intégration
│   └── Dockerfile          # Configuration Docker pour l'API
├── frontend/               # Application frontend Vue.js
│   ├── src/                # Code source du frontend
│   │   ├── assets/         # Ressources statiques
│   │   ├── components/     # Composants Vue
│   │   ├── router/         # Configuration des routes
│   │   ├── stores/         # Stores Pinia
│   │   └── views/          # Vues de l'application
│   └── Dockerfile          # Configuration Docker pour le frontend
├── monitoring/             # Configuration des outils de monitoring
│   ├── grafana/            # Configuration Grafana
│   │   ├── dashboards/     # Dashboards préconfigurés
│   │   └── provisioning/   # Configuration des sources de données
│   └── prometheus/         # Configuration Prometheus
│       └── prometheus.yml  # Configuration des cibles à scraper
├── nginx/                  # Configuration du reverse proxy
│   └── nginx.conf          # Configuration Nginx
├── doc/                    # Documentation du projet
├── docker-compose.yml      # Configuration Docker Compose
└── setup-monitoring.sh     # Script de configuration du monitoring
```

## Tests

### Tests Backend

Pour exécuter les tests de l'API :

```bash
cd api
pytest
```

### Tests Frontend

Pour exécuter les tests unitaires du frontend :

```bash
cd frontend
npm run test:unit
```

Pour exécuter les tests E2E du frontend :

```bash
cd frontend
npm run test:e2e
```

## Monitoring et Observabilité

### Logs structurés

Les logs sont formatés en JSON et incluent des métadonnées comme le service, l'environnement et les identifiants de trace.

### Métriques

Les métriques suivantes sont collectées et exposées via Prometheus :

- Métriques HTTP : nombre de requêtes, temps de réponse, statuts
- Métriques de base de données : nombre de requêtes, temps d'exécution
- Métriques système : utilisation CPU, mémoire, disque

### Tracing distribué

Le tracing distribué est implémenté avec OpenTelemetry et permet de suivre le parcours d'une requête à travers les différents services.

### Dashboards

Des dashboards Grafana préconfigurés sont disponibles pour visualiser les métriques de l'application.

## Contribution

1. Forker le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Committer vos changements (`git commit -m 'Add some amazing feature'`)
4. Pousser sur la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.
