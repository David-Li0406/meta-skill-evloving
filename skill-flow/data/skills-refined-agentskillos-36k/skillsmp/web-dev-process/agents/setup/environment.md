---
name: environment-orchestrator
description: Orchestrateur pour la configuration des environnements
workflows:
  - id: wdp-setup-environment
    template: wf-creation
    phase: Brief
    name: Configuration des environnements
    duration: 0.5 jour
---

# Orchestrateur Environnements

Ce module coordonne la configuration des environnements de développement et production.

## Agents Spécialisés

| Agent | Responsabilité |
|-------|----------------|
| `env-variables.md` | Variables d'environnement, .env, validation Zod |
| `docker.md` | Dockerfile, docker-compose, conteneurisation |
| `secrets-management.md` | Gestion sécurisée des secrets |

## Tu NE fais PAS

- ❌ Provisionner l'infrastructure → devops
- ❌ Configurer les serveurs → devops
- ❌ Gérer les secrets en production → devops
- ❌ Écrire le code applicatif → frontend-developer, backend-developer

## Contextualisation ADR-005

### Couche Métier (Global)
> Pratique standard de l'industrie pour la gestion d'environnements.

Les environnements standards (local, dev, staging, production) avec variables d'environnement (.env, .env.example), conteneurisation Docker pour la reproductibilité, séparation des secrets du code, et validation des variables (Zod, dotenv-safe) sont des pratiques universelles. Le principe "12-factor app" est un standard reconnu.

### Couche Agence (Spécifique)
> Adaptations selon l'infrastructure et outils agence.

**Questions à poser :**
- Quels environnements sont standards ? (local, dev, staging, prod, ou autres)
- Quel outil de gestion de secrets ? (Vault, AWS Secrets Manager, 1Password)
- Docker est-il systématique ? (docker-compose pour dev local)
- Y a-t-il un template .env.example agence ? (variables communes)
- Comment sont validées les variables ? (Zod, dotenv-safe, scripts custom)

### Couche Projet (Exception)
> Exceptions selon besoins et contraintes projet.

**Questions à poser :**
- Y a-t-il des environnements spécifiques ? (pré-prod, demo, UAT)
- Des contraintes de sécurité particulières ? (secteur régulé, données sensibles)
- Faut-il supporter plusieurs régions ? (multi-cloud, geo-distribution)
- Y a-t-il des services externes à intégrer ? (APIs tierces, legacy systems)
- Des outils de développement imposés ? (IDE, versions spécifiques)

## Environnements Standards

```
┌─────────────────────────────────────────────────────────────┐
│                     ENVIRONNEMENTS                          │
├─────────────┬─────────────┬─────────────┬─────────────────┤
│    LOCAL    │     DEV     │   STAGING   │   PRODUCTION    │
├─────────────┼─────────────┼─────────────┼─────────────────┤
│ Machine dev │ Serveur dev │ Pré-prod    │ Prod            │
│ Données     │ Données     │ Données     │ Données         │
│ fictives    │ de test     │ anonymisées │ réelles         │
│             │             │             │                 │
│ Debug ON    │ Debug ON    │ Debug OFF   │ Debug OFF       │
└─────────────┴─────────────┴─────────────┴─────────────────┘
```

## Setup Rapide

```bash
# 1. Copier le template
cp .env.example .env.local

# 2. Éditer les variables
code .env.local

# 3. Lancer les services
docker-compose up -d

# 4. Démarrer l'app
npm run dev
```

## Fichiers Clés

| Fichier | Description | Commité |
|---------|-------------|---------|
| `.env.example` | Template des variables | ✅ Oui |
| `.env.local` | Variables locales | ❌ Non |
| `docker-compose.yml` | Services de dev | ✅ Oui |
| `Dockerfile` | Image de production | ✅ Oui |

## Exemples de Configuration

### .env.example

```bash
# .env.example - Template à copier en .env.local

# Application
NODE_ENV=development
APP_URL=http://localhost:3000
API_URL=http://localhost:4000

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myapp_dev

# Auth
JWT_SECRET=your-secret-here-change-in-production
SESSION_SECRET=another-secret-change-this

# External APIs
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Feature Flags
FEATURE_NEW_DASHBOARD=false
```

### Validation avec Zod

```typescript
// src/env.ts
import { z } from 'zod';

const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'staging', 'production']),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  STRIPE_SECRET_KEY: z.string().startsWith('sk_'),
});

// Valider au démarrage
export const env = envSchema.parse(process.env);
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: myapp_dev
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - '5432:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:alpine
    ports:
      - '6379:6379'

  mailhog:
    image: mailhog/mailhog
    ports:
      - '1025:1025'  # SMTP
      - '8025:8025'  # Web UI

volumes:
  postgres_data:
```

## Bonnes Pratiques

| Pratique | Raison |
|----------|--------|
| Valider les variables au démarrage | Fail fast si config manquante |
| Utiliser des valeurs par défaut sûres | Éviter erreurs de prod en dev |
| Séparer les secrets | Ne jamais commiter de secrets |
| Documenter chaque variable | Faciliter l'onboarding |
| Utiliser des préfixes cohérents | `DB_`, `API_`, `FEATURE_` |

## Erreurs Courantes

| Erreur | Solution |
|--------|----------|
| Secrets committé par erreur | Utiliser `git-secrets` ou pre-commit hooks |
| Variables manquantes en prod | Valider avec Zod/dotenv-safe au démarrage |
| .env.local non ignoré | Vérifier `.gitignore` |
| Config différente dev/prod | Utiliser `.env.development`, `.env.production` |

## Agents à Consulter

- Pour les variables d'environnement → `env-variables.md`
- Pour Docker et conteneurisation → `docker.md`
- Pour la gestion des secrets → `secrets-management.md`

## Livrables

| Livrable | Description |
|----------|-------------|
| Environment Setup Guide | Guide complet de configuration des environnements (local, dev, staging, prod) |
| Docker Compose Configuration | Configuration docker-compose pour services locaux |
| Environment Documentation | Documentation des différences entre environnements |
| Env Validation Schema | Schéma Zod pour valider les variables d'environnement |
