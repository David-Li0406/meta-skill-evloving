---
id: integration-testing
name: "Integration Testing"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Integration Testing

## Overview

Integration testing verifies that multiple components work correctly together, including databases, APIs, message queues, and external services. Unlike unit tests, integration tests use real dependencies or realistic test doubles.

## When to Use

- Testing database interactions (ORM, queries, transactions)
- Testing API endpoints with real request/response cycles
- Verifying message queue producers and consumers
- Testing service-to-service communication
- Validating authentication and authorization flows

## Key Principles

- **Test real integrations**: Use actual databases, not mocks
- **Isolated test data**: Each test controls its own data
- **Clean up after tests**: Restore system to known state
- **Acceptable speed**: Seconds, not milliseconds
- **Test boundaries**: Focus on component interactions

## Best Practices

### Database Integration Tests

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

# Fixture: Real PostgreSQL in Docker
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def engine(postgres_container):
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def db_session(engine):
    """Create a fresh session for each test with automatic rollback."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# Tests
class TestUserRepository:

    def test_create_user(self, db_session):
        repo = UserRepository(db_session)

        user = repo.create(User(
            email="test@example.com",
            name="Test User"
        ))

        assert user.id is not None
        assert user.email == "test@example.com"

    def test_find_by_email(self, db_session):
        repo = UserRepository(db_session)
        repo.create(User(email="find@example.com", name="Find Me"))

        result = repo.find_by_email("find@example.com")

        assert result is not None
        assert result.name == "Find Me"

    def test_find_nonexistent_returns_none(self, db_session):
        repo = UserRepository(db_session)

        result = repo.find_by_email("nonexistent@example.com")

        assert result is None

    def test_transaction_rollback_on_error(self, db_session):
        repo = UserRepository(db_session)

        with pytest.raises(IntegrityError):
            # Try to create user with duplicate email
            repo.create(User(email="dup@example.com", name="First"))
            repo.create(User(email="dup@example.com", name="Second"))

        # Transaction should be rolled back
        result = repo.find_by_email("dup@example.com")
        assert result is None
```

### FastAPI Integration Tests

```python
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest_asyncio

# Synchronous testing
@pytest.fixture
def client(db_session):
    """Create test client with database session."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

class TestUserAPI:

    def test_create_user_success(self, client):
        response = client.post("/api/users", json={
            "email": "new@example.com",
            "name": "New User",
            "password": "securepass123"
        })

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert "id" in data
        assert "password" not in data  # Password should not be returned

    def test_create_user_duplicate_email(self, client, db_session):
        # Create existing user
        repo = UserRepository(db_session)
        repo.create(User(email="exists@example.com", name="Existing"))
        db_session.commit()

        response = client.post("/api/users", json={
            "email": "exists@example.com",
            "name": "Duplicate",
            "password": "pass123"
        })

        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    def test_get_user_authenticated(self, client, db_session, auth_headers):
        # Setup user
        user = create_test_user(db_session)

        response = client.get(
            f"/api/users/{user.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        assert response.json()["id"] == str(user.id)

    def test_get_user_unauthorized(self, client, db_session):
        user = create_test_user(db_session)

        response = client.get(f"/api/users/{user.id}")

        assert response.status_code == 401

# Async testing
@pytest_asyncio.fixture
async def async_client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_async_endpoint(async_client):
    response = await async_client.get("/api/health")
    assert response.status_code == 200
```

### Authentication Testing

```python
import pytest
from jose import jwt

@pytest.fixture
def auth_headers(test_user):
    """Generate valid auth headers for test user."""
    token = create_access_token(
        data={"sub": test_user.id},
        expires_delta=timedelta(hours=1)
    )
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_headers(admin_user):
    """Generate auth headers for admin user."""
    token = create_access_token(
        data={"sub": admin_user.id, "role": "admin"},
        expires_delta=timedelta(hours=1)
    )
    return {"Authorization": f"Bearer {token}"}

class TestAuthentication:

    def test_login_success(self, client, test_user):
        response = client.post("/api/auth/login", data={
            "username": test_user.email,
            "password": "testpassword"
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        response = client.post("/api/auth/login", data={
            "username": "wrong@example.com",
            "password": "wrongpass"
        })

        assert response.status_code == 401

    def test_protected_route_with_valid_token(self, client, auth_headers):
        response = client.get("/api/protected", headers=auth_headers)
        assert response.status_code == 200

    def test_protected_route_with_expired_token(self, client, test_user):
        # Create expired token
        token = create_access_token(
            data={"sub": test_user.id},
            expires_delta=timedelta(seconds=-1)
        )

        response = client.get(
            "/api/protected",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 401

    def test_admin_route_with_user_token(self, client, auth_headers):
        response = client.get("/api/admin/users", headers=auth_headers)
        assert response.status_code == 403

    def test_admin_route_with_admin_token(self, client, admin_headers):
        response = client.get("/api/admin/users", headers=admin_headers)
        assert response.status_code == 200
```

### Message Queue Integration Tests

```python
import pytest
from testcontainers.rabbitmq import RabbitMqContainer
import pika
import json
import time

@pytest.fixture(scope="session")
def rabbitmq_container():
    with RabbitMqContainer("rabbitmq:3-management") as rabbitmq:
        yield rabbitmq

@pytest.fixture
def rabbitmq_connection(rabbitmq_container):
    params = pika.ConnectionParameters(
        host=rabbitmq_container.get_container_host_ip(),
        port=rabbitmq_container.get_exposed_port(5672)
    )
    connection = pika.BlockingConnection(params)
    yield connection
    connection.close()

@pytest.fixture
def rabbitmq_channel(rabbitmq_connection):
    channel = rabbitmq_connection.channel()
    channel.queue_declare(queue='test_queue', durable=True)
    yield channel
    channel.queue_delete(queue='test_queue')

class TestMessageProducer:

    def test_publish_message(self, rabbitmq_channel):
        producer = MessageProducer(rabbitmq_channel)

        producer.publish('test_queue', {'order_id': '123'})

        # Verify message was published
        method, properties, body = rabbitmq_channel.basic_get('test_queue')
        assert method is not None
        assert json.loads(body) == {'order_id': '123'}

    def test_message_persistence(self, rabbitmq_channel):
        producer = MessageProducer(rabbitmq_channel)

        producer.publish('test_queue', {'data': 'test'}, persistent=True)

        method, properties, body = rabbitmq_channel.basic_get('test_queue')
        assert properties.delivery_mode == 2  # Persistent

class TestMessageConsumer:

    def test_consume_and_process(self, rabbitmq_channel):
        processed = []

        def handler(message):
            processed.append(message)
            return True

        consumer = MessageConsumer(rabbitmq_channel, handler)

        # Publish test message
        rabbitmq_channel.basic_publish(
            exchange='',
            routing_key='test_queue',
            body=json.dumps({'order_id': '456'})
        )

        # Consume one message
        consumer.consume_one('test_queue')

        assert len(processed) == 1
        assert processed[0]['order_id'] == '456'
```

### External Service Integration (with WireMock)

```python
import pytest
import requests
from testcontainers.core.container import DockerContainer

@pytest.fixture(scope="session")
def wiremock_container():
    container = DockerContainer("wiremock/wiremock:3.3.1")
    container.with_exposed_ports(8080)
    container.start()

    # Wait for WireMock to be ready
    base_url = f"http://{container.get_container_host_ip()}:{container.get_exposed_port(8080)}"
    for _ in range(30):
        try:
            requests.get(f"{base_url}/__admin/mappings")
            break
        except:
            time.sleep(0.5)

    yield base_url
    container.stop()

@pytest.fixture
def mock_payment_gateway(wiremock_container):
    """Setup mock payment gateway responses."""
    # Register stub for successful payment
    requests.post(f"{wiremock_container}/__admin/mappings", json={
        "request": {
            "method": "POST",
            "urlPath": "/api/charge",
            "bodyPatterns": [{"contains": "amount"}]
        },
        "response": {
            "status": 200,
            "jsonBody": {"payment_id": "pay_123", "status": "success"},
            "headers": {"Content-Type": "application/json"}
        }
    })

    yield wiremock_container

    # Clean up mappings
    requests.delete(f"{wiremock_container}/__admin/mappings")

class TestPaymentIntegration:

    def test_process_payment_success(self, mock_payment_gateway):
        gateway = PaymentGateway(base_url=mock_payment_gateway)

        result = gateway.charge(amount=100, card_token="tok_123")

        assert result["status"] == "success"
        assert result["payment_id"] == "pay_123"
```

### TypeScript/Supertest Integration Tests

```typescript
import request from 'supertest';
import { createApp } from '../src/app';
import { setupTestDatabase, teardownTestDatabase } from './helpers/db';
import { createTestUser, generateAuthToken } from './helpers/auth';

describe('User API Integration', () => {
  let app: Express.Application;
  let authToken: string;
  let testUserId: string;

  beforeAll(async () => {
    await setupTestDatabase();
    app = createApp();
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  beforeEach(async () => {
    const user = await createTestUser({
      email: 'test@example.com',
      password: 'password123',
    });
    testUserId = user.id;
    authToken = generateAuthToken(user);
  });

  describe('GET /api/users/:id', () => {
    it('should return user when authenticated', async () => {
      const response = await request(app)
        .get(`/api/users/${testUserId}`)
        .set('Authorization', `Bearer ${authToken}`)
        .expect(200);

      expect(response.body.id).toBe(testUserId);
      expect(response.body.email).toBe('test@example.com');
      expect(response.body).not.toHaveProperty('password');
    });

    it('should return 401 without auth token', async () => {
      await request(app)
        .get(`/api/users/${testUserId}`)
        .expect(401);
    });

    it('should return 404 for non-existent user', async () => {
      await request(app)
        .get('/api/users/non-existent-id')
        .set('Authorization', `Bearer ${authToken}`)
        .expect(404);
    });
  });

  describe('POST /api/users', () => {
    it('should create user with valid data', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'new@example.com',
          password: 'newpassword123',
          name: 'New User',
        })
        .expect(201);

      expect(response.body.email).toBe('new@example.com');
      expect(response.body).toHaveProperty('id');
    });

    it('should return 400 for invalid email', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'invalid-email',
          password: 'password123',
        })
        .expect(400);

      expect(response.body.errors).toContainEqual(
        expect.objectContaining({ field: 'email' })
      );
    });
  });
});
```

## Anti-patterns

- **Testing against production**: Always use isolated test environments
- **Shared test data**: Tests affecting each other through shared state
- **Not cleaning up**: Test data accumulating between runs
- **Slow tests**: Integration tests should complete in seconds
- **Mocking integrations**: Defeats the purpose of integration testing
- **Ignoring edge cases**: Network failures, timeouts, partial failures

## References

- [testcontainers-python](https://testcontainers-python.readthedocs.io/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Supertest Documentation](https://github.com/ladjs/supertest)
- [WireMock Documentation](https://wiremock.org/docs/)
