"""
TDD Integration Test Template for career_ios_backend

Use this template when creating new API tests.
"""
import pytest
from httpx import AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_example_create_success(auth_headers):
    """Test creating new resource - happy path"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/examples",
            headers=auth_headers,
            json={"name": "Test Example", "description": "Example description"},
        )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Example"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_example_get_success(auth_headers, created_example):
    """Test retrieving resource by ID"""
    example_id = created_example["id"]

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            f"/api/v1/examples/{example_id}", headers=auth_headers
        )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == example_id


@pytest.mark.asyncio
async def test_example_list_success(auth_headers):
    """Test listing resources"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/examples", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_example_update_success(auth_headers, created_example):
    """Test updating resource"""
    example_id = created_example["id"]

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put(
            f"/api/v1/examples/{example_id}",
            headers=auth_headers,
            json={"name": "Updated Name"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"


@pytest.mark.asyncio
async def test_example_delete_success(auth_headers, created_example):
    """Test deleting resource"""
    example_id = created_example["id"]

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete(
            f"/api/v1/examples/{example_id}", headers=auth_headers
        )

    assert response.status_code == 204

    # Verify deletion
    get_response = await client.get(
        f"/api/v1/examples/{example_id}", headers=auth_headers
    )
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_example_unauthorized():
    """Test endpoint requires authentication"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/examples")

    assert response.status_code == 401


# Fixtures example (add to conftest.py if needed)
"""
@pytest.fixture
async def created_example(auth_headers):
    '''Create a test example resource'''
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/examples",
            headers=auth_headers,
            json={"name": "Test", "description": "Test"}
        )
    return response.json()
"""
