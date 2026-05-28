# Getting Started with Backend Development

Guide pratique pour démarrer un projet backend avec les agents spécialisés.

## Choisir son Architecture

### Arbre de Décision

```
Quel type de projet ?
│
├── MVP / Startup early-stage
│   └── Monolithe modulaire
│       → architecture/monolith + architecture/patterns
│
├── Application métier complexe
│   └── Domain-Driven Design
│       → architecture/ddd + architecture/patterns
│
├── Système distribué / Scale
│   └── Microservices
│       → architecture/microservices + architecture/event-driven
│
└── Real-time / Event-heavy
    └── Event-Driven Architecture
        → architecture/event-driven + performance/concurrency
```

## Workflow Recommandé

### Phase 1 : Design de l'API

```
Étape 1 : Définir les ressources
────────────────────────────────
"Je veux créer une API pour gérer des utilisateurs et leurs commandes"

→ api/rest-design
  Output: Endpoints CRUD, conventions de nommage, structure des URLs

Étape 2 : Documenter l'API
──────────────────────────
"Génère la spec OpenAPI pour ces endpoints"

→ api/openapi-spec
  Output: Fichier openapi.yaml complet

Étape 3 : Définir la validation
───────────────────────────────
"Quelles validations pour le payload de création d'utilisateur ?"

→ api/validation
  Output: Schémas Zod/Joi avec contraintes
```

### Phase 2 : Base de Données

```
Étape 4 : Modéliser les données
───────────────────────────────
"Modélise le schéma pour users et orders avec relations"

→ database/modeling
  Output: Schéma SQL/Prisma avec relations et contraintes

Étape 5 : Créer les migrations
──────────────────────────────
"Génère les migrations pour ce schéma"

→ database/migrations
  Output: Fichiers de migration versionnés

Étape 6 : Écrire les requêtes
─────────────────────────────
"Requête pour les commandes d'un utilisateur avec pagination"

→ database/queries
  Output: SQL optimisé + code ORM
```

### Phase 3 : Sécurité

```
Étape 7 : Authentification
──────────────────────────
"Implémente JWT avec refresh tokens"

→ auth-security/authentication
  Output: Flow complet avec code

Étape 8 : Autorisation
──────────────────────
"RBAC avec rôles admin/user/guest"

→ auth-security/authorization
  Output: Middleware et policies
```

### Phase 4 : Tests & Performance

```
Étape 9 : Tests unitaires
─────────────────────────
"Tests pour le service UserService"

→ testing/unit
  Output: Tests avec mocks

Étape 10 : Tests API
────────────────────
"Tests d'intégration pour POST /users"

→ testing/api
  Output: Tests supertest/pytest

Étape 11 : Optimisation
───────────────────────
"Mes requêtes sont lentes"

→ performance/caching + database/optimization
  Output: Stratégie de cache + index
```

### Phase 5 : Déploiement

```
Étape 12 : Containerisation
───────────────────────────
"Dockerfile multi-stage pour Node.js"

→ devops/containers
  Output: Dockerfile optimisé

Étape 13 : CI/CD
────────────────
"Pipeline GitHub Actions avec tests et deploy"

→ devops/cicd
  Output: Workflow complet

Étape 14 : Monitoring
─────────────────────
"Métriques et alerting pour la production"

→ devops/monitoring
  Output: Configuration observabilité
```

## Exemples Concrets

### Exemple 1 : API REST E-commerce

**Contexte** : Créer une API pour gérer produits, panier et commandes.

```
1. "Conçois les endpoints REST pour un e-commerce"
   → api/rest-design

   Résultat:
   GET    /products          # Liste produits
   GET    /products/:id      # Détail produit
   POST   /cart/items        # Ajouter au panier
   DELETE /cart/items/:id    # Retirer du panier
   POST   /orders            # Créer commande
   GET    /orders/:id        # Détail commande

2. "Modèle de données pour products, cart, orders"
   → database/modeling

   Résultat: Schéma avec relations et indexes

3. "Sécurise les endpoints orders avec JWT"
   → auth-security/authentication

   Résultat: Middleware auth + refresh flow
```

### Exemple 2 : Microservice Notifications

**Contexte** : Service de notifications (email, push, SMS).

```
1. "Architecture event-driven pour notifications"
   → architecture/event-driven

   Résultat:
   - Events: UserCreated, OrderCompleted, PaymentFailed
   - Consumers: EmailNotifier, PushNotifier, SMSNotifier
   - Queue: RabbitMQ/SQS configuration

2. "Tests pour le consumer EmailNotifier"
   → testing/unit + testing/integration

   Résultat: Tests avec mocks de la queue

3. "Monitoring pour le service notifications"
   → devops/monitoring

   Résultat: Métriques (queue depth, latency, errors)
```

### Exemple 3 : Optimisation Performance

**Contexte** : Dashboard avec requêtes lentes.

```
1. "Cette requête prend 5s, comment l'optimiser ?"
   → database/optimization

   Input: Query SQL + EXPLAIN output
   Résultat: Index recommandés + query réécrite

2. "Stratégie de cache pour les données dashboard"
   → performance/caching

   Résultat:
   - Cache Redis pour aggregations
   - TTL adapté par type de données
   - Invalidation strategy

3. "Le endpoint /stats est appelé 1000x/min"
   → api/rate-limiting

   Résultat: Configuration rate limiting
```

## Composition d'Agents

### Patterns Courants

| Besoin | Agents à Combiner |
|--------|-------------------|
| Nouvelle API | rest-design → openapi-spec → validation |
| Nouvelle table | modeling → migrations → queries |
| Sécuriser endpoint | authentication → authorization → audit |
| Optimiser perf | optimization → caching → profiling |
| Déployer | containers → cicd → kubernetes → monitoring |

### Anti-patterns

```
❌ Commencer par l'optimisation avant d'avoir des métriques
   → Utiliser profiling d'abord

❌ Implémenter microservices pour un MVP
   → Commencer par monolith, extraire ensuite

❌ Ignorer les tests pour "aller plus vite"
   → Tests API minimum pour les endpoints critiques

❌ Sécurité en dernier
   → Intégrer auth-security dès la phase 2
```

## Checklist Projet

### Avant de coder

- [ ] Endpoints REST définis (api/rest-design)
- [ ] Schéma de données modélisé (database/modeling)
- [ ] Authentification choisie (auth-security/authentication)
- [ ] Stack technique validée

### Avant de déployer

- [ ] Tests API passent (testing/api)
- [ ] Migrations testées (database/migrations)
- [ ] Dockerfile optimisé (devops/containers)
- [ ] CI/CD configuré (devops/cicd)
- [ ] Monitoring prêt (devops/monitoring)

### En production

- [ ] Rate limiting actif (api/rate-limiting)
- [ ] Audit logs configurés (auth-security/audit)
- [ ] Alerting configuré (devops/monitoring)
- [ ] Backup DB automatisé (devops/infrastructure)

## Stack Recommandées

### Node.js/TypeScript

```
Framework  : NestJS ou Express + TypeScript
ORM        : Prisma
Validation : Zod
Auth       : Passport + JWT
Tests      : Jest + Supertest
CI/CD      : GitHub Actions
Container  : Docker multi-stage
Monitoring : Prometheus + Grafana
```

### Python

```
Framework  : FastAPI
ORM        : SQLAlchemy + Alembic
Validation : Pydantic
Auth       : python-jose
Tests      : Pytest + httpx
CI/CD      : GitHub Actions
Container  : Docker multi-stage
Monitoring : Prometheus + Grafana
```

### Go

```
Framework  : Gin ou Echo
ORM        : GORM ou sqlx
Validation : go-playground/validator
Auth       : golang-jwt
Tests      : testing + testify
CI/CD      : GitHub Actions
Container  : Docker scratch
Monitoring : Prometheus + Grafana
```

## Ressources

- [README principal](../README.md) - Vue d'ensemble des agents
- [CHANGELOG](../CHANGELOG.md) - Historique des versions
- [Tests](../tests/) - Validation de la structure
