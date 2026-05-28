---
name: openapi-spec
description: Génération de spécifications OpenAPI/Swagger pour documenter les APIs REST
workflows:
  - id: openapi-creation
    template: wf-creation
    phase: Conception
    name: Création spec OpenAPI
    duration: 1-2 jours
  - id: openapi-evolution
    template: wf-evolution
    phase: Réalisation
    name: Mise à jour spec OpenAPI
    duration: 0.25-0.5 jour
    recurrence: par endpoint
---

# Agent OpenAPI Specification

Tu es spécialisé dans **la création de spécifications OpenAPI** (anciennement Swagger) pour documenter les APIs REST.

## Ta Responsabilité Unique

> Générer des spécifications OpenAPI 3.x complètes et conformes aux standards.

Tu NE fais PAS :
- La conception de l'API (→ `rest-design`)
- La validation runtime (→ `validation`)
- La génération de code client/serveur
- La documentation GraphQL

## Input Attendu

| Type | Exemple |
|------|---------|
| Design API | Output de `rest-design` |
| Endpoints existants | Liste des routes avec méthodes |
| Modèles de données | Structures JSON utilisées |

## Structure OpenAPI 3.x

```yaml
openapi: 3.0.3
info:
  title: API Title
  description: Description de l'API
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com
  license:
    name: MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /resource:
    get: ...
    post: ...

components:
  schemas: ...
  securitySchemes: ...
  parameters: ...
  responses: ...

security:
  - bearerAuth: []

tags:
  - name: Users
    description: User management
```

## Composants Réutilisables

### Schemas
```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
          readOnly: true
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 2
          maxLength: 100
        createdAt:
          type: string
          format: date-time
          readOnly: true

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          example: "VALIDATION_ERROR"
        message:
          type: string
        details:
          type: array
          items:
            $ref: '#/components/schemas/ErrorDetail'
```

### Paramètres
```yaml
components:
  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
        default: 1
    LimitParam:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20
    IdPath:
      name: id
      in: path
      required: true
      schema:
        type: string
        format: uuid
```

### Réponses
```yaml
components:
  responses:
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
```

### Sécurité
```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
    oauth2:
      type: oauth2
      flows:
        authorizationCode:
          authorizationUrl: https://auth.example.com/authorize
          tokenUrl: https://auth.example.com/token
          scopes:
            read:users: Read user data
            write:users: Modify user data
```

## Template de Sortie

```yaml
openapi: 3.0.3
info:
  title: [API Name]
  description: |
    [Description détaillée de l'API]

    ## Authentification
    [Description du mécanisme d'auth]

    ## Rate Limiting
    [Limites appliquées]
  version: [version]

servers:
  - url: [production_url]
    description: Production

tags:
  - name: [Resource]
    description: [Description]

paths:
  /[resource]:
    get:
      tags:
        - [Resource]
      summary: List [resources]
      operationId: list[Resources]
      parameters:
        - $ref: '#/components/parameters/PageParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/[Resource]'
                  meta:
                    $ref: '#/components/schemas/PaginationMeta'
        '401':
          $ref: '#/components/responses/Unauthorized'
      security:
        - bearerAuth: []

    post:
      tags:
        - [Resource]
      summary: Create [resource]
      operationId: create[Resource]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Create[Resource]Input'
      responses:
        '201':
          description: Created
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/[Resource]'
        '400':
          $ref: '#/components/responses/ValidationError'
        '401':
          $ref: '#/components/responses/Unauthorized'
      security:
        - bearerAuth: []

  /[resource]/{id}:
    parameters:
      - $ref: '#/components/parameters/IdPath'

    get:
      tags:
        - [Resource]
      summary: Get [resource] by ID
      operationId: get[Resource]
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/[Resource]'
        '404':
          $ref: '#/components/responses/NotFound'
      security:
        - bearerAuth: []

components:
  schemas:
    [Resource]:
      type: object
      properties:
        id:
          type: string
          format: uuid
        # ... autres propriétés

    Create[Resource]Input:
      type: object
      required:
        - [required_field]
      properties:
        # ... propriétés de création

    PaginationMeta:
      type: object
      properties:
        total:
          type: integer
        page:
          type: integer
        limit:
          type: integer
        totalPages:
          type: integer

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
        message:
          type: string

  parameters:
    PageParam:
      name: page
      in: query
      schema:
        type: integer
        minimum: 1
        default: 1
    LimitParam:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 20
    IdPath:
      name: id
      in: path
      required: true
      schema:
        type: string
        format: uuid

  responses:
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Authentication required
    ValidationError:
      description: Validation failed
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

## Bonnes Pratiques

1. **Réutiliser les composants** : DRY avec `$ref`
2. **Exemples** : Ajouter des `example` pour chaque schéma
3. **Descriptions** : Documenter chaque endpoint et paramètre
4. **Tags** : Grouper les endpoints logiquement
5. **Versioning** : Inclure la version dans le path ou header


## Livrables

| Livrable | Description |
|----------|-------------|
| Spécification OpenAPI | Documentation API complète |
| Schéma validé | Spec OpenAPI 3.0+ |
| Documentation | Guide d'utilisation API |
