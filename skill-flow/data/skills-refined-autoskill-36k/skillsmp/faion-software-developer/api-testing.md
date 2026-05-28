# API Testing

**ID:** api-testing

## Problem

APIs without tests break silently. Need comprehensive testing strategy.

## Framework

**Testing Pyramid:**

```
          /\
         /  \      E2E Tests (few)
        /----\     Integration Tests (some)
       /      \    Contract Tests (more)
      /--------\   Unit Tests (many)
     /__________\
```

## Contract Testing with Pact

**Consumer Side (Frontend):**

```javascript
const { Pact } = require('@pact-foundation/pact');

const provider = new Pact({
  consumer: 'Frontend',
  provider: 'UserAPI',
  port: 8080
});

describe('User API', () => {
  beforeAll(() => provider.setup());
  afterAll(() => provider.finalize());

  it('should get user by id', async () => {
    await provider.addInteraction({
      state: 'user exists',
      uponReceiving: 'a request for user 123',
      withRequest: {
        method: 'GET',
        path: '/users/123',
        headers: { Authorization: 'Bearer token' }
      },
      willRespondWith: {
        status: 200,
        body: {
          id: '123',
          name: Matchers.string('John'),
          email: Matchers.email()
        }
      }
    });

    const response = await userClient.getUser('123');
    expect(response.id).toBe('123');
  });
});
```

**Provider Side (Backend):**

```python
from pactman import verify_pacts

def test_provider():
    verify_pacts(
        pact_broker_url="https://pact-broker.example.com",
        provider="UserAPI",
        provider_base_url="http://localhost:8000",
        provider_states_url="http://localhost:8000/_pact/states"
    )
```

## Integration Testing

```python
import pytest
from fastapi.testclient import TestClient
from app import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

class TestUsers:
    def test_create_user(self, client, auth_headers):
        response = client.post(
            "/users",
            json={"name": "New User", "email": "new@example.com"},
            headers=auth_headers
        )
        assert response.status_code == 201
        assert response.json()["name"] == "New User"

    def test_get_user_not_found(self, client, auth_headers):
        response = client.get("/users/nonexistent", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["type"].endswith("/not-found")

    def test_validation_error(self, client, auth_headers):
        response = client.post(
            "/users",
            json={"name": "", "email": "invalid"},
            headers=auth_headers
        )
        assert response.status_code == 400
        errors = response.json()["errors"]
        assert any(e["field"] == "email" for e in errors)
```

## OpenAPI Validation

```python
from openapi_core import OpenAPI
from openapi_core.testing.mock import MockRequest, MockResponse

spec = OpenAPI.from_file_path("openapi.yaml")

def test_response_matches_spec():
    response = client.get("/users")

    mock_request = MockRequest("http://localhost", "GET", "/users")
    mock_response = MockResponse(
        data=response.content,
        status_code=response.status_code
    )

    result = spec.validate_response(mock_request, mock_response)
    assert not result.errors
```

## Postman Collection

```json
{
  "info": {
    "name": "User API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Create User",
      "request": {
        "method": "POST",
        "header": [
          {"key": "Authorization", "value": "Bearer {{token}}"}
        ],
        "body": {
          "mode": "raw",
          "raw": "{\"name\": \"Test\", \"email\": \"test@example.com\"}"
        },
        "url": "{{baseUrl}}/users"
      },
      "event": [
        {
          "listen": "test",
          "script": {
            "exec": [
              "pm.test('Status is 201', () => pm.response.to.have.status(201));",
              "pm.test('Has user ID', () => pm.expect(pm.response.json().id).to.exist);"
            ]
          }
        }
      ]
    }
  ]
}
```

## Best Practices

- Test happy path and error scenarios
- Use contract tests for consumer-provider relationships
- Validate responses against OpenAPI spec
- Run tests in CI/CD pipeline
- Mock external dependencies
- Test rate limiting behavior
- Include security tests (auth, injection)

## Agent

faion-api-agent
