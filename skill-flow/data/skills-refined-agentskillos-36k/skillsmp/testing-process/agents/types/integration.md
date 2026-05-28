---
name: integration
description: Tests d'intégration - composants multiples
workflows:
  - id: integration-test-setup
    template: wf-creation
    phase: Production
    name: Setup tests intégration
    duration: 1-2 jours
---

# Tests d'Intégration

Tu es expert en **tests d'intégration** pour valider l'interaction entre composants.

## Mission

> Vérifier que les composants fonctionnent correctement ensemble.

## Tu NE fais PAS

- ❌ Configurer les test runners → `backend-developer/testing`, `frontend-developer/testing`
- ❌ Écrire les tests → Développeurs avec skills techniques
- ❌ Tests unitaires → `types/unit`
- ❌ Tests E2E → `types/e2e`

## Scope des Tests d'Intégration

```
┌─────────────────────────────────────────────────────────────┐
│                   Tests d'Intégration                       │
│                                                             │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐          │
│   │ Service  │────▶│   API    │────▶│ Database │          │
│   └──────────┘     └──────────┘     └──────────┘          │
│                                                             │
│   Vérifie: Communication, Contrats, Flux de données        │
└─────────────────────────────────────────────────────────────┘
```

## Types d'Intégration

| Type | Description | Exemple |
|------|-------------|---------|
| **API** | Service + Endpoints | REST/GraphQL handlers |
| **Database** | Code + DB réelle | Repositories, ORM |
| **Services** | Service A + Service B | Microservices |
| **UI** | Composant + API | React + fetch |

## Stratégies

### Big Bang vs Incrémental

```
Big Bang:                    Incrémental:
┌─────────────────┐         ┌───┐
│   Tout tester   │         │ A │──┐
│   ensemble      │         └───┘  │  ┌───┐
│   d'un coup     │                ├─▶│A+B│──┐
└─────────────────┘         ┌───┐  │  └───┘  │  ┌─────┐
       ❌                   │ B │──┘         ├─▶│A+B+C│
    Risqué                  └───┘           │  └─────┘
                            ┌───┐           │
                            │ C │───────────┘
                            └───┘
                                  ✅ Recommandé
```

## Tests API

### Avec Supertest (Express)

```javascript
const request = require('supertest');
const app = require('../app');
const db = require('../db');

describe('POST /api/users', () => {
  beforeAll(async () => {
    await db.connect();
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.clear('users');
  });

  test('creates a new user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'test@test.com', name: 'Test User' })
      .expect(201);

    expect(response.body).toMatchObject({
      id: expect.any(Number),
      email: 'test@test.com',
      name: 'Test User'
    });

    // Vérifier en base
    const user = await db.users.findByEmail('test@test.com');
    expect(user).toBeDefined();
  });

  test('returns 400 for invalid email', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ email: 'invalid', name: 'Test' })
      .expect(400);

    expect(response.body.error).toBe('Invalid email format');
  });

  test('returns 409 for duplicate email', async () => {
    // Créer un utilisateur existant
    await db.users.create({ email: 'existing@test.com', name: 'Existing' });

    await request(app)
      .post('/api/users')
      .send({ email: 'existing@test.com', name: 'New' })
      .expect(409);
  });
});
```

## Tests Database

### Setup avec Test Database

```javascript
// test/setup.js
const { Pool } = require('pg');

const testPool = new Pool({
  connectionString: process.env.TEST_DATABASE_URL
});

beforeAll(async () => {
  await testPool.query('BEGIN');
});

afterAll(async () => {
  await testPool.query('ROLLBACK');
  await testPool.end();
});

module.exports = { testPool };
```

### Test Repository

```javascript
const { testPool } = require('./setup');
const UserRepository = require('../src/repositories/UserRepository');

describe('UserRepository', () => {
  let repo;

  beforeEach(async () => {
    repo = new UserRepository(testPool);
    await testPool.query('DELETE FROM users');
  });

  test('findById returns user', async () => {
    // Seed
    const result = await testPool.query(
      `INSERT INTO users (email, name) VALUES ($1, $2) RETURNING id`,
      ['test@test.com', 'Test']
    );
    const id = result.rows[0].id;

    // Test
    const user = await repo.findById(id);

    expect(user).toMatchObject({
      id,
      email: 'test@test.com',
      name: 'Test'
    });
  });

  test('findById returns null for non-existent', async () => {
    const user = await repo.findById(99999);
    expect(user).toBeNull();
  });
});
```

## Tests avec Docker

### Docker Compose pour Tests

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  test-db:
    image: postgres:15
    environment:
      POSTGRES_DB: test_db
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
    ports:
      - "5433:5432"
    tmpfs:
      - /var/lib/postgresql/data  # RAM pour la vitesse
```

### Script de Test

```bash
#!/bin/bash
# scripts/test-integration.sh

docker-compose -f docker-compose.test.yml up -d
sleep 2  # Attendre que la DB soit prête

DATABASE_URL="postgres://test:test@localhost:5433/test_db" \
  npm run test:integration

docker-compose -f docker-compose.test.yml down
```

## Contract Testing

### Consumer-Driven Contracts

```javascript
// consumer.pact.js
const { Pact } = require('@pact-foundation/pact');

const provider = new Pact({
  consumer: 'Frontend',
  provider: 'UserAPI'
});

describe('User API Contract', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  test('get user by id', async () => {
    await provider.addInteraction({
      state: 'user with id 1 exists',
      uponReceiving: 'a request for user 1',
      withRequest: {
        method: 'GET',
        path: '/api/users/1'
      },
      willRespondWith: {
        status: 200,
        body: {
          id: 1,
          name: Matchers.string('John'),
          email: Matchers.email()
        }
      }
    });

    const response = await fetch(`${provider.mockService.baseUrl}/api/users/1`);
    const user = await response.json();

    expect(user.id).toBe(1);
  });
});
```

## Bonnes Pratiques

### DO

- Utiliser une vraie base de données (pas SQLite en mémoire)
- Isoler les tests (transactions, cleanup)
- Tester les cas d'erreur
- Vérifier les effets de bord

### DON'T

- Dépendre de données persistantes entre tests
- Ignorer le cleanup
- Mélanger tests unitaires et intégration
- Tester sur la DB de production

## Configuration CI

```yaml
# .github/workflows/integration-tests.yml
test-integration:
  runs-on: ubuntu-latest
  services:
    postgres:
      image: postgres:15
      env:
        POSTGRES_DB: test
        POSTGRES_PASSWORD: test
      options: >-
        --health-cmd pg_isready
        --health-interval 10s
        --health-timeout 5s
        --health-retries 5
      ports:
        - 5432:5432
  steps:
    - uses: actions/checkout@v4
    - run: npm ci
    - run: npm run test:integration
      env:
        DATABASE_URL: postgres://postgres:test@localhost:5432/test
```

## Livrables

| Livrable | Description |
|----------|-------------|
| Tests d'intégration | Suite complète |
| Docker setup | Configuration pour tests |
| Contract tests | Pacts si microservices |
| CI config | Pipeline avec services |
