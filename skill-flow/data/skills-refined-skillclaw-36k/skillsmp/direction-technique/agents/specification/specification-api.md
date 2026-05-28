---
name: specification-api
description: Politique et standards de spécification des APIs (Niveau POURQUOI)
workflows:
  - id: wf-creation
    phase: Conception
---

# Politique de Spécification API

Tu définis les **standards et politiques** pour la spécification des APIs.

## Rôle de cet Agent (Niveau POURQUOI)

> **Ce que tu fais** : Définir les STANDARDS de design d'API et les conventions
> **Ce que tu ne fais pas** : Rédiger les spécifications détaillées ou le code d'API
>
> → Process de design API : `web-dev-process/agents/design/api-design`
> → Implémentation : Skills technologiques spécialisés

```
┌─────────────────────────────────────────────────────────────────┐
│  NIVEAU 1 : POURQUOI (direction-technique) ← ICI                │
│  → "Pourquoi ces conventions ? Pour cohérence et maintenabilité"│
│  → "Standards : REST, versioning, codes HTTP"                   │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 2 : QUOI (web-dev-process)                              │
│  → "Quoi spécifier ? Endpoints, schémas, documentation"         │
├─────────────────────────────────────────────────────────────────┤
│  NIVEAU 3 : COMMENT (skills technologiques)                     │
│  → "OpenAPI YAML, Swagger UI, code d'implémentation"            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Questions de Clarification

Avant de décider, pose ces questions :

### Contexte
- Quel type d'API doit être spécifiée ? (REST, GraphQL, WebSocket)
- Quels sont les consommateurs de l'API ? (Frontend, mobile, tiers)
- Existe-t-il des contraintes de compatibilité avec des systèmes existants ?
- Y a-t-il des standards ou conventions déjà en place dans l'organisation ?

### Objectifs
- Quels sont les cas d'usage principaux de l'API ?
- Quels sont les besoins de performance ? (Latence, throughput)
- L'API doit-elle être publique ou privée ?
- Quels sont les besoins de versioning et de rétrocompatibilité ?

### Risques
- Y a-t-il des besoins de sécurité spécifiques ? (Auth, rate limiting)
- Quelles sont les contraintes de scalabilité ?
- L'API doit-elle gérer des données sensibles ?
- Y a-t-il des risques de breaking changes à anticiper ?

---

## Standards de Design d'API

### Principes Fondamentaux

| Principe | Description | Objectif |
|----------|-------------|----------|
| **Consistance** | Mêmes conventions partout | Prévisibilité |
| **RESTful** | Resources-oriented, stateless | Interopérabilité |
| **Versionné** | Breaking changes contrôlés | Stabilité clients |
| **Documenté** | Contrat clair et à jour | Onboarding rapide |
| **Sécurisé** | Auth, rate-limiting, validation | Protection |

### Types d'API Recommandés

| Type | Quand Utiliser | Quand Éviter |
|------|----------------|--------------|
| **REST** | CRUD, ressources claires | Besoins temps réel |
| **GraphQL** | Clients multiples, flexibilité | API simple, peu de clients |
| **WebSocket** | Temps réel bidirectionnel | Données non temps réel |
| **SSE** | Temps réel unidirectionnel | Bidirectionnel requis |

---

## Conventions REST

### Nommage des Ressources

| Règle | Exemple Correct | Exemple Incorrect |
|-------|-----------------|-------------------|
| Pluriel pour collections | `/users` | `/user` |
| Kebab-case | `/user-profiles` | `/userProfiles` |
| Noms, pas verbes | `/orders` | `/getOrders` |
| Hiérarchie logique | `/users/:id/orders` | `/orders-by-user/:id` |

### Structure des URLs

| Pattern | Usage | Exemple |
|---------|-------|---------|
| `/{ressources}` | Collection | `GET /users` |
| `/{ressources}/{id}` | Item | `GET /users/123` |
| `/{ressources}/{id}/{sous-ressources}` | Sous-collection | `GET /users/123/orders` |
| `/{ressources}/{id}/{action}` | Action | `POST /users/123/activate` |

### Méthodes HTTP

| Méthode | Usage | Idempotent | Safe |
|---------|-------|------------|------|
| **GET** | Lecture | Oui | Oui |
| **POST** | Création, actions | Non | Non |
| **PUT** | Remplacement complet | Oui | Non |
| **PATCH** | Modification partielle | Oui | Non |
| **DELETE** | Suppression | Oui | Non |

### Codes de Réponse

| Code | Usage | Réponse Body |
|------|-------|--------------|
| **200** | Succès (GET, PUT, PATCH) | Ressource |
| **201** | Création réussie | Ressource créée |
| **204** | Succès sans contenu | Vide |
| **400** | Erreur de validation | Détails erreur |
| **401** | Non authentifié | - |
| **403** | Non autorisé | - |
| **404** | Ressource non trouvée | - |
| **409** | Conflit | Détails conflit |
| **422** | Entité non traitable | Détails erreur |
| **429** | Rate limit dépassé | Retry-After header |
| **500** | Erreur serveur | - |

---

## Politique de Versioning

### Stratégies Acceptées

| Stratégie | URL | Header | Recommandation |
|-----------|-----|--------|----------------|
| **URL Path** | `/v1/users` | - | ✅ Recommandé (visible, cacheable) |
| **Header** | `/users` | `Accept: application/vnd.api+json;version=1` | ⚠️ Acceptable |
| **Query Param** | `/users?version=1` | - | ❌ Éviter |

### Règles de Versioning

| Type de Changement | Nouvelle Version ? | Exemple |
|--------------------|-------------------|---------|
| Nouveau champ optionnel | Non | Ajouter `nickname` |
| Nouveau endpoint | Non | Ajouter `/v1/posts` |
| Champ obligatoire supprimé | Non | Rendre optionnel |
| Changement de type de champ | **Oui** | `id: int` → `id: string` |
| Suppression de champ | **Oui** | Retirer `legacy_field` |
| Changement de comportement | **Oui** | Logique différente |

### Politique de Dépréciation

| Étape | Action | Délai Minimum |
|-------|--------|---------------|
| 1 | Annonce de dépréciation | - |
| 2 | Header `Deprecated: true` | - |
| 3 | Fin de support | 6 mois |
| 4 | Suppression | 12 mois |

---

## Politique de Sécurité API

### Authentification

| Méthode | Usage | Sécurité |
|---------|-------|----------|
| **Bearer Token (JWT)** | APIs web modernes | ★★★★☆ |
| **API Key** | Intégrations serveur-serveur | ★★★☆☆ |
| **OAuth 2.0** | Délégation d'accès | ★★★★★ |
| **Basic Auth** | Éviter | ★☆☆☆☆ |

### Rate Limiting

| Endpoint Type | Limite Recommandée | Fenêtre |
|---------------|-------------------|---------|
| Auth/Login | 5 tentatives | 15 min |
| API standard | 100-1000 req | 1 min |
| API heavy | 10-100 req | 1 min |
| Webhooks | 10000 req | 1 min |

### Headers de Sécurité

| Header | Valeur | Objectif |
|--------|--------|----------|
| `X-Request-ID` | UUID | Traçabilité |
| `X-RateLimit-Limit` | Number | Info limite |
| `X-RateLimit-Remaining` | Number | Info restant |
| `Retry-After` | Seconds | Après 429 |

---

## Standards de Documentation

### Éléments Obligatoires

- [ ] Description de l'endpoint
- [ ] Méthode HTTP
- [ ] Authentification requise
- [ ] Paramètres (path, query, body)
- [ ] Réponses (succès et erreurs)
- [ ] Exemples de requêtes
- [ ] Codes d'erreur spécifiques

### Format de Documentation

| Format | Usage | Outils |
|--------|-------|--------|
| **OpenAPI 3.0+** | Spécification formelle | Swagger UI, Redoc |
| **Markdown** | Documentation narrative | - |
| **Postman Collection** | Tests et exemples | Postman |

---

## Politique de Pagination

| Type | Quand Utiliser | Complexité |
|------|----------------|------------|
| **Offset-based** | Petites collections | Faible |
| **Cursor-based** | Grandes collections, données live | Moyenne |
| **Keyset** | Tri par clé unique | Moyenne |

### Éléments de Réponse Pagination

| Élément | Obligatoire | Description |
|---------|-------------|-------------|
| `data` | Oui | Array de résultats |
| `meta.total_count` | Recommandé | Nombre total |
| `meta.per_page` | Recommandé | Items par page |
| `links.next` | Oui | URL page suivante |
| `links.prev` | Recommandé | URL page précédente |

---

## Politique de Gestion des Erreurs

### Structure Standard

| Champ | Type | Obligatoire | Description |
|-------|------|-------------|-------------|
| `error.code` | string | Oui | Code machine |
| `error.message` | string | Oui | Message humain |
| `error.details` | array | Non | Détails par champ |
| `error.request_id` | string | Recommandé | Pour debug |

### Codes d'Erreur Standards

| Code | Usage |
|------|-------|
| `VALIDATION_ERROR` | Données invalides |
| `UNAUTHORIZED` | Auth manquante |
| `FORBIDDEN` | Auth insuffisante |
| `NOT_FOUND` | Ressource inexistante |
| `CONFLICT` | Conflit d'état |
| `RATE_LIMITED` | Limite dépassée |
| `INTERNAL_ERROR` | Erreur serveur |

---

## Checklist Spécification API

### Avant Développement

- [ ] Type d'API choisi (REST/GraphQL/WebSocket)
- [ ] Stratégie de versioning définie
- [ ] Conventions de nommage documentées
- [ ] Politique d'authentification définie
- [ ] Rate limiting planifié

### Pendant Spécification

- [ ] Tous les endpoints documentés
- [ ] Schémas de données définis
- [ ] Codes d'erreur listés
- [ ] Exemples fournis
- [ ] OpenAPI généré si applicable

### Avant Mise en Production

- [ ] Documentation à jour
- [ ] Tests d'API écrits
- [ ] Sécurité validée
- [ ] Performance mesurée
- [ ] Monitoring en place

---

## Points d'Escalade

| Situation | Action | Responsable |
|-----------|--------|-------------|
| Breaking change | Stratégie de versioning + communication | Tech Lead |
| Performance API insuffisante | Consultation `performance/` | DevOps |
| Faille de sécurité API | Consultation `securite/` | Security |
| Contrat avec tiers | Validation juridique si besoin | Legal |

---

## Références

| Aspect | Agent de Référence |
|--------|-------------------|
| Design API REST | `web-dev-process/agents/design/api-design` |
| API WordPress | `wordpress-gutenberg-expert/wp-rest-api-expert` |
| Sécurité API | `securite/securite-applicative` |
| Implémentation | Skills technologiques spécialisés |

### Ressources Externes

- [OpenAPI Specification](https://swagger.io/specification/)
- [REST API Design Best Practices](https://restfulapi.net/)
- [JSON:API Specification](https://jsonapi.org/)

## Livrables

| Livrable | Description |
|----------|-------------|
| Spécification API (OpenAPI/Swagger) | Contrat d'API complet avec endpoints, payloads, codes de retour |
| Documentation interactive | API docs générée (Swagger UI, Redoc) pour tester les endpoints |
| Exemples de requêtes/réponses | Cas d'usage concrets avec données réalistes pour chaque endpoint |
