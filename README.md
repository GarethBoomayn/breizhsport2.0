# Breizhsport 2.0

Application e-commerce moderne pour Breizhsport, développée avec FastAPI, Vue.js et Docker.

## Architecture

- Frontend: Vue.js 3 avec TypeScript et Tailwind CSS
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
  - Intégration du frontend Vue.js avec le backend

- **API**
  - Configuration FastAPI avec dernières versions (SQLAlchemy 2.0, Pydantic 2.0)
  - Gestion complète des catégories (CRUD)
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

### En cours de développement

- Gestion des produits
- Système de panier avec Redis
- Gestion des commandes
- Pipeline CI/CD
- Monitoring et logging
- Tests de performance

## Prérequis

- Docker
- Docker Compose
- Python 3.11+ (pour le développement local)
- Node.js 22+ (pour le développement local)

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

L'application sera accessible à l'adresse : http://localhost:80
- Frontend: http://localhost:80
- API: http://localhost:80/api
- API directe: http://localhost:8000
- Frontend dev server: http://localhost:5173

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
│   │   │   ├── init_db.py        # Initialisation de la base de données
│   │   │   └── init_test_data.py # Script d'initialisation des données de test
│   │   ├── dependencies.py # Dépendances FastAPI
│   │   └── main.py        # Point d'entrée de l'application
│   ├── tests/             # Tests unitaires et d'intégration
│   ├── alembic/           # Migrations de base de données
│   ├── alembic.ini        # Configuration Alembic
│   ├── Dockerfile         # Dockerfile pour l'API
│   └── requirements.txt   # Dépendances Python
├── frontend/              # Application frontend Vue.js
│   ├── src/              # Code source du frontend
│   │   ├── assets/      # Ressources statiques (CSS, images)
│   │   ├── components/  # Composants Vue réutilisables
│   │   ├── router/      # Configuration des routes
│   │   ├── stores/      # Stores Pinia pour la gestion d'état
│   │   ├── views/       # Composants de pages
│   │   ├── App.vue      # Composant racine
│   │   └── main.ts      # Point d'entrée de l'application
│   ├── public/          # Fichiers statiques publics
│   ├── tests/           # Tests unitaires et E2E
│   ├── Dockerfile       # Dockerfile pour le frontend
│   └── package.json     # Dépendances Node.js
├── nginx/                 # Configuration Nginx
│   └── nginx.conf        # Configuration du reverse proxy
├── docker-compose.yml     # Configuration Docker Compose
└── README.md             # Documentation
```

## API Endpoints

### Authentification

- `POST /api/auth/register` - Inscription d'un nouvel utilisateur
- `POST /api/auth/token` - Connexion et génération de token JWT

### Catégories

- `GET /api/categories/` - Liste toutes les catégories
- `GET /api/categories/{id}` - Récupère une catégorie par son ID
- `POST /api/categories/` - Crée une nouvelle catégorie
- `PUT /api/categories/{id}` - Met à jour une catégorie
- `DELETE /api/categories/{id}` - Supprime une catégorie

## Tests

### Tests Backend

Pour exécuter les tests de l'API :

```bash
# Dans le conteneur API
docker exec breizhsport20_api_1 sh -c 'cd /app && PYTHONPATH=/app pytest -v'
```

### Tests Frontend

Pour exécuter les tests unitaires du frontend :

```bash
# Dans le conteneur Frontend
docker exec breizhsport20_frontend_1 sh -c 'cd /app && npm run test:unit'
```

Pour exécuter les tests E2E du frontend :

```bash
# Dans le conteneur Frontend
docker exec breizhsport20_frontend_1 sh -c 'cd /app && npm run test:e2e'
```

## Développement local

### Backend

```bash
cd api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Technologies utilisées

- **Vue.js**: Framework JavaScript progressif pour les interfaces utilisateur
- **TypeScript**: Typage statique pour JavaScript
- **Tailwind CSS**: Framework CSS utilitaire
- **Vite**: Outil de build ultra-rapide
- **Pinia**: Bibliothèque de gestion d'état pour Vue
- **Vue Router**: Routeur officiel pour Vue.js
- **Vitest**: Framework de test unitaire pour Vite
- **Nightwatch**: Framework de test E2E
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
