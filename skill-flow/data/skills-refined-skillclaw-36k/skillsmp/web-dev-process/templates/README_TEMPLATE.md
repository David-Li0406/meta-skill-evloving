# Nom du Projet

<!-- Badges -->
[![CI](https://github.com/ORG/REPO/actions/workflows/ci.yml/badge.svg)](https://github.com/ORG/REPO/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/ORG/REPO/branch/main/graph/badge.svg)](https://codecov.io/gh/ORG/REPO)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Description courte du projet en une ou deux phrases.

## Table des Matières

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Développement](#développement)
- [Tests](#tests)
- [Déploiement](#déploiement)
- [Architecture](#architecture)
- [Contribution](#contribution)
- [License](#license)

## Fonctionnalités

- ✅ Fonctionnalité 1
- ✅ Fonctionnalité 2
- ✅ Fonctionnalité 3
- 🚧 Fonctionnalité en cours de développement
- 📋 Fonctionnalité planifiée

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- [Node.js](https://nodejs.org/) >= 20.x
- [pnpm](https://pnpm.io/) >= 8.x (ou npm/yarn)
- [Docker](https://www.docker.com/) (optionnel, pour le développement local)

## Installation

```bash
# Cloner le repository
git clone https://github.com/ORG/REPO.git
cd REPO

# Installer les dépendances
pnpm install

# Copier le fichier d'environnement
cp .env.example .env.local

# Lancer les services locaux (si Docker)
docker-compose up -d

# Lancer les migrations
pnpm db:migrate

# Lancer l'application
pnpm dev
```

L'application est accessible sur [http://localhost:3000](http://localhost:3000).

## Configuration

### Variables d'Environnement

| Variable | Description | Défaut | Requis |
|----------|-------------|--------|--------|
| `NODE_ENV` | Environnement (development/staging/production) | `development` | ✅ |
| `DATABASE_URL` | URL de connexion à la base de données | - | ✅ |
| `API_SECRET` | Secret pour signer les tokens | - | ✅ |
| `SMTP_HOST` | Serveur SMTP pour les emails | - | ❌ |

Voir [.env.example](.env.example) pour la liste complète.

## Utilisation

### Commandes Disponibles

```bash
# Développement
pnpm dev          # Lancer en mode développement
pnpm build        # Compiler pour la production
pnpm start        # Lancer en mode production

# Tests
pnpm test         # Lancer les tests unitaires
pnpm test:e2e     # Lancer les tests E2E
pnpm test:cov     # Générer le rapport de couverture

# Qualité
pnpm lint         # Vérifier le linting
pnpm lint:fix     # Corriger automatiquement
pnpm typecheck    # Vérifier les types TypeScript
pnpm format       # Formater le code

# Base de données
pnpm db:migrate   # Appliquer les migrations
pnpm db:seed      # Peupler avec des données de test
pnpm db:reset     # Réinitialiser la base
```

### Exemples d'API

```bash
# Créer un utilisateur
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John Doe"}'

# Récupérer les utilisateurs
curl http://localhost:3000/api/users
```

## Développement

### Structure du Projet

```
├── src/
│   ├── components/     # Composants UI réutilisables
│   ├── pages/          # Pages / Routes
│   ├── services/       # Logique métier
│   ├── hooks/          # Custom hooks
│   ├── utils/          # Utilitaires
│   └── types/          # Types TypeScript
├── tests/
│   ├── unit/           # Tests unitaires
│   ├── integration/    # Tests d'intégration
│   └── e2e/            # Tests end-to-end
├── docs/               # Documentation
│   └── adr/            # Architecture Decision Records
└── scripts/            # Scripts utilitaires
```

### Workflow Git

1. Créer une branche depuis `main` : `git checkout -b feat/ma-feature`
2. Développer avec des commits conventionnels : `feat: add login page`
3. Pousser et créer une PR
4. Attendre la review et les checks CI
5. Merger une fois approuvé

Voir [CONTRIBUTING.md](CONTRIBUTING.md) pour plus de détails.

### Conventions de Code

- Commits : [Conventional Commits](https://www.conventionalcommits.org/)
- Style : ESLint + Prettier (appliqués automatiquement via pre-commit hooks)
- Nommage : camelCase pour les variables, PascalCase pour les composants

## Tests

```bash
# Tests unitaires
pnpm test

# Tests avec watch mode
pnpm test:watch

# Tests E2E
pnpm test:e2e

# Couverture
pnpm test:cov
```

### Objectifs de Couverture

| Type de code | Objectif |
|--------------|----------|
| Logique métier | > 90% |
| API / Services | > 80% |
| Composants UI | > 60% |

## Déploiement

### Environnements

| Environnement | URL | Branche | Déploiement |
|---------------|-----|---------|-------------|
| Development | dev.example.com | `develop` | Automatique |
| Staging | staging.example.com | `main` | Automatique |
| Production | example.com | tag `v*` | Manuel |

### Procédure de Release

1. Mettre à jour le CHANGELOG
2. Créer un tag : `git tag v1.2.3`
3. Pousser le tag : `git push origin v1.2.3`
4. Le pipeline de déploiement se déclenche automatiquement

## Architecture

### Diagramme

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   API       │────▶│   Database  │
│   (React)   │     │   (Node.js) │     │ (PostgreSQL)│
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Cache     │
                    │   (Redis)   │
                    └─────────────┘
```

### Décisions d'Architecture

Les décisions d'architecture sont documentées dans [docs/adr/](docs/adr/).

- [ADR-001: Choix du framework frontend](docs/adr/001-frontend-framework.md)
- [ADR-002: Stratégie d'authentification](docs/adr/002-authentication.md)

## Contribution

Les contributions sont les bienvenues ! Consultez [CONTRIBUTING.md](CONTRIBUTING.md) pour :

- Le processus de contribution
- Les conventions de code
- Comment soumettre une PR

## Équipe

| Nom | Rôle | Contact |
|-----|------|---------|
| @person1 | Tech Lead | email@example.com |
| @person2 | Backend | email@example.com |
| @person3 | Frontend | email@example.com |

## License

Ce projet est sous licence [MIT](LICENSE).

---

<p align="center">
  Fait avec ❤️ par l'équipe
</p>
