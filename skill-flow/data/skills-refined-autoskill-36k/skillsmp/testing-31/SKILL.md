---
name: testing
description: Test patterns and commands for LogiAccounting Pro. Use when writing tests, running test suites, or debugging test failures.
tools:
  - read
  - write
  - bash
metadata:
  version: "1.0"
  category: quality
  frameworks: pytest, jest
---

# Testing Skill

This skill provides testing patterns and commands.

## Quick Commands

### Backend (pytest)

```bash
cd backend

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_login_success

# Run with coverage
pytest --cov=app --cov-report=html

# Stop on first failure
pytest -x

# Run tests matching pattern
pytest -k "login"
```

### Frontend (Jest)

```bash
cd frontend

# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific file
npm test -- Login.test.jsx

# Watch mode
npm test -- --watch
```

## API Testing with curl

### Get Auth Token

```bash
# Login as admin
TOKEN=$(curl -s -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@logiaccounting.demo","password":"Demo2024!Admin"}' \
  | jq -r '.token')

echo $TOKEN
```

### Test Endpoints

```bash
# GET request
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5000/api/v1/inventory/materials

# POST request
curl -X POST http://localhost:5000/api/v1/inventory/materials \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Material","reference":"TM-001","quantity":100}'

# PUT request
curl -X PUT http://localhost:5000/api/v1/inventory/materials/ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Name"}'

# DELETE request
curl -X DELETE http://localhost:5000/api/v1/inventory/materials/ID \
  -H "Authorization: Bearer $TOKEN"
```

## Test File Template

### Backend Test (pytest)

```python
# tests/test_example.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@logiaccounting.demo",
        "password": "Demo2024!Admin"
    })
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}

class TestExample:
    def test_get_all(self, client, auth_headers):
        response = client.get("/api/v1/example", headers=auth_headers)
        assert response.status_code == 200
        assert "items" in response.json()

    def test_create(self, client, auth_headers):
        response = client.post(
            "/api/v1/example",
            json={"name": "Test", "value": 100},
            headers=auth_headers
        )
        assert response.status_code == 201

    def test_unauthorized(self, client):
        response = client.get("/api/v1/example")
        assert response.status_code == 401
```

### Frontend Test (Jest + RTL)

```jsx
// __tests__/Example.test.jsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Example from '../pages/Example';

describe('Example Page', () => {
  test('renders loading state', () => {
    render(<Example />);
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
  });

  test('displays data after load', async () => {
    render(<Example />);
    await waitFor(() => {
      expect(screen.getByText(/item name/i)).toBeInTheDocument();
    });
  });

  test('opens modal on button click', async () => {
    render(<Example />);
    await userEvent.click(screen.getByText(/new item/i));
    expect(screen.getByRole('dialog')).toBeInTheDocument();
  });
});
```

## Coverage Goals

| Component | Target |
|-----------|--------|
| Auth | 90%+ |
| API Routes | 80%+ |
| React Pages | 70%+ |
| Utils | 90%+ |

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Backend Tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest --cov=app
      - name: Frontend Tests
        run: |
          cd frontend
          npm install
          npm test -- --coverage
```
