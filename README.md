# Breizhsport 2.0

Application e-commerce moderne pour Breizhsport, développée avec FastAPI et Docker.

## Architecture

- Backend: FastAPI (Python 3.11)
- Cache: Redis
- Base de données: PostgreSQL
- Reverse Proxy: Nginx
- Conteneurisation: Docker & Docker Compose

## État d'avancement

### Fonctionnalités implémentées

- **Architecture**
  - Configuration complète de l'environnement Docker
  - Mise en place du reverse proxy Nginx
  - Configuration de la base de données PostgreSQL
  - Configuration du cache Redis

- **API**
  - Configuration FastAPI avec dernières versions (SQLAlchemy 2.0, Pydantic 2.0)
  - Gestion complète des catégories (CRUD)
  - Tests unitaires avec pytest
  - Gestion des erreurs HTTP
  - Configuration CORS

- **Modèles de données**
  - Utilisateurs
  - Catégories
  - Produits
  - Commandes
  - Articles de commande

### En cours de développement

- Authentification utilisateur
- Gestion des produits
- Système de panier avec Redis
- Gestion des commandes
- Pipeline CI/CD
- Monitoring et logging
- Tests de performance

## Prérequis

- Docker
- Docker Compose
- Python 3.11+

## Installation

1. Cloner le repository
```bash
git clone [url-du-repo]
cd breizhsport2.0
```

2. Créer un fichier .env dans le dossier api/ avec les variables suivantes :
```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/breizhsport
REDIS_URL=redis://cache:6379/0
```

3. Lancer l'application avec Docker Compose
```bash
docker-compose up --build
```

L'API sera accessible à l'adresse : http://localhost:80

## Structure du Projet

```
breizhsport2.0/
├── api/                      # Service API principal
│   ├── app/                 # Code source de l'API
│   │   ├── crud/           # Opérations CRUD
│   │   │   └── category.py # Opérations CRUD pour les catégories
│   │   ├── database/       # Configuration base de données
│   │   ├── models/         # Modèles SQLAlchemy
│   │   ├── routes/         # Routes API
│   │   ├── schemas/        # Schémas Pydantic
│   │   ├── scripts/        # Scripts utilitaires
│   │   ├── dependencies.py # Dépendances FastAPI
│   │   └── main.py        # Point d'entrée de l'application
│   ├── tests/             # Tests unitaires et d'intégration
│   ├── alembic/           # Migrations de base de données
│   ├── alembic.ini        # Configuration Alembic
│   ├── Dockerfile         # Dockerfile pour l'API
│   └── requirements.txt   # Dépendances Python
├── nginx/                 # Configuration Nginx
│   └── nginx.conf        # Configuration du reverse proxy
├── docker-compose.yml     # Configuration Docker Compose
└── README.md             # Documentation
```

## API Endpoints

### Catégories

- `GET /categories/` - Liste toutes les catégories
- `GET /categories/{id}` - Récupère une catégorie par son ID
- `POST /categories/` - Crée une nouvelle catégorie
- `PUT /categories/{id}` - Met à jour une catégorie
- `DELETE /categories/{id}` - Supprime une catégorie

## Tests

Pour exécuter les tests :

```bash
# Dans le conteneur API
docker exec breizhsport20_api_1 sh -c 'cd /app && PYTHONPATH=/app pytest -v'
```

## Technologies utilisées

- **FastAPI**: Framework API moderne et performant
- **SQLAlchemy**: ORM SQL avec support asynchrone
- **Pydantic**: Validation de données et sérialisation
- **Pytest**: Framework de test
- **Alembic**: Gestion des migrations de base de données
- **PostgreSQL**: Base de données relationnelle
- **Redis**: Cache et stockage de sessions
- **Nginx**: Reverse proxy et serveur web
- **Docker**: Conteneurisation
- **Docker Compose**: Orchestration de conteneurs
