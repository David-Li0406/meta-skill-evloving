---
name: testing
description: Test development with pytest, fixtures, and integration testing. Use for writing tests, test patterns, coverage, parametrization, and debugging test failures.
context: fork
---

# Testing Skill

Quick reference for writing tests. For full methodology and philosophy, see [Testing Methodology](https://github.com/krazyuniks/guitar-tone-shootout/wiki/Testing-Methodology) in the wiki.

**Philosophy:** Test real services, mock only external network APIs. See `.claude/rules/integration-testing.md`.

## Test Type Taxonomy

| Test Type | What It Tests | Location |
|-----------|---------------|----------|
| **Unit Tests** | Single function/class in isolation | `tests/unit/backend/` |
| **Backend-Integration Tests** | Service orchestration, real DB/Redis | `tests/integration/backend/` |
| **E2E Tests** | Browser + DB verification | `tests/e2e/python/` |
| **Smoke Tests** | Critical path quick validation | Marker-based (`-m smoke`) |

## Running Tests

```bash
# All quality gates
just check

# Backend tests with coverage
docker compose exec backend pytest /tests/unit/backend/ /tests/integration/backend/ \
    --cov=app --cov-report=term-missing

# Specific test file
docker compose exec backend pytest /tests/integration/backend/api/test_signal_chains.py -v

# E2E tests (runs on HOST)
just test-e2e-quick      # Quick E2E (< 1 min, for commits)
just test-e2e-full       # Full E2E (for pre-PR)
pytest -m e2e tests/e2e/python/  # All E2E
```

### Marker-Based Selection

```bash
pytest -m smoke          # Fast critical path (< 3 min)
pytest -m unit           # Unit tests only
pytest -m integration    # Backend-Integration tests
pytest -m e2e_quick      # Quick E2E tests (< 1 min)
pytest -m e2e_full       # Full E2E tests
pytest -m "not slow"     # Exclude slow tests
```

## Test Structure

```
tests/
├── conftest.py              # Root config: markers, pytest_plugins
├── fixtures/                # Shared fixtures
│   ├── database.py          # DB session with transaction rollback
│   ├── auth.py              # JWT tokens, auth headers
│   └── factories.py         # Test data factories
├── unit/backend/            # Pure logic, no external deps
├── integration/backend/     # Real DB/Redis tests
└── e2e/
    ├── python/              # E2E tests (pytest + Playwright)
    │   ├── conftest.py      # Browser fixtures, auth, DB access
    │   └── tests/           # Test files
    └── smoke/               # Infrastructure smoke tests
```

## Key Fixtures

### Database Session (Transaction Rollback)

```python
@pytest.fixture(scope="function")
async def db_session(db_engine) -> AsyncGenerator[AsyncSession, None]:
    """Real database with transaction rollback."""
    connection = await db_engine.connect()
    transaction = await connection.begin()

    async_session_factory = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    session = async_session_factory()

    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()
        await connection.close()
```

### Factory Fixture Pattern

```python
@pytest.fixture(scope="function")
def make_signal_chain(db_session: AsyncSession, test_user):
    """Factory for creating signal chains."""
    async def _make_signal_chain(name: str = "Test Chain", **kwargs):
        chain = SignalChain(
            id=uuid4(),
            user_id=test_user.id,
            name=name,
            **kwargs,
        )
        db_session.add(chain)
        await db_session.flush()
        await db_session.refresh(chain)
        return chain

    return _make_signal_chain
```

### Authentication

```python
@pytest.fixture(scope="function")
def auth_headers(auth_token: str) -> dict[str, str]:
    """Authorization headers for authenticated requests."""
    return {"Authorization": f"Bearer {auth_token}"}
```

## Test Patterns

### Backend-Integration Test (Preferred)

```python
@pytest.mark.asyncio
async def test_create_signal_chain(client, auth_headers, test_user):
    """Test creating a signal chain via API."""
    response = await client.post(
        "/api/v1/signal-chains",
        json={"name": "Test Chain", "platform": "nam"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "Test Chain"
```

### Unit Test (Pure Logic)

```python
def test_signal_chain_validates_name():
    """Test domain validation without database."""
    with pytest.raises(ValueError, match="Name cannot be empty"):
        SignalChainCreate(name="", platform="nam")
```

### E2E Test (Python Playwright)

```python
@pytest.mark.asyncio
@pytest.mark.e2e
@pytest.mark.e2e_quick
async def test_creates_signal_chain(page: Page, db_session, frontend_url: str):
    """Three-layer validation: UI action → DOM update → database state."""

    # LAYER 1: UI Action - Navigate and interact
    await page.goto(f"{frontend_url}/builder")
    await page.fill('[name="chain-name"]', 'My Chain')
    await page.click('button:has-text("Save")')

    # LAYER 2: DOM Update - Verify UI response
    await expect(page.locator('[data-testid="chain-card"]')).to_be_visible()

    # LAYER 3: Database State - Verify persistence
    result = await db_session.execute(
        text("SELECT id FROM signal_chains WHERE name = :name"),
        {"name": "My Chain"}
    )
    assert result.fetchone() is not None
```

### Mocking External APIs Only

```python
@pytest.mark.asyncio
async def test_t3k_sync_handles_error(db_session, test_user):
    """Mock EXTERNAL API only - never mock internal services."""
    with patch("app.services.t3k_client.fetch_tones") as mock:
        mock.side_effect = ExternalAPIError("T3K down")
        service = T3KSyncService(db_session)
        result = await service.sync_user_tones(test_user.id)
        assert result.status == "failed"
```

## Pytest Markers

| Marker | Description | Auto-Applied |
|--------|-------------|--------------|
| `unit` | No external dependencies | `tests/unit/` |
| `integration` | Real DB/Redis required | `tests/integration/` |
| `e2e` | E2E tests (browser + DB) | `tests/e2e/` |
| `e2e_quick` | Quick E2E (< 1 min, for commits) | Manual |
| `e2e_full` | Full E2E (for pre-PR) | Manual |
| `smoke` | Critical path tests (< 3 min total) | `tests/e2e/smoke/` |
| `slow` | Tests > 10 seconds | Manual |
| `t3k_integration` | Real Tone3000 API | Manual |

## Coverage

Target: 80%+

```bash
docker compose exec backend pytest /tests/unit/backend/ /tests/integration/backend/ \
    --cov=app --cov-fail-under=80 --cov-report=html
```

## Related

- [Testing Methodology](https://github.com/krazyuniks/guitar-tone-shootout/wiki/Testing-Methodology) - Full methodology (GitHub Wiki)
- `.claude/rules/integration-testing.md` - Testing rules
