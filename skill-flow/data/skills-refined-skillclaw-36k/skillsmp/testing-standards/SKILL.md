---
name: testing-standards
description: Testing standards for GUTTERS. Use when writing tests for modules, calculations, or integrations. Ensures 80%+ coverage with validated test data.
---

# Testing Standards

Pytest async testing for GUTTERS. All calculations tested against known data, 80% minimum coverage.

## Test Structure
```
tests/
├── conftest.py              # Shared fixtures (DB, Redis, Singleton resets)
├── test_active_memory.py    # Core systems
├── test_synthesis.py
└── modules/
    ├── test_astrology.py
    └── test_numerology.py
```

## Required Test Types

**1. Initialization Test**
```python
@pytest.mark.asyncio
async def test_module_initializes():
    module = AstrologyModule()
    await module.initialize()
    
    assert module.initialized == True
    assert module.config is not None
```

**2. Calculation Against Known Data**
```python
@pytest.mark.asyncio
async def test_natal_chart_steve_jobs():
    """Test against verified birth chart."""
    # Steve Jobs: Feb 24, 1955, 7:15 PM PST, San Francisco
    chart = await calculate_natal_chart(
        datetime(1955, 2, 24, 19, 15, tzinfo=ZoneInfo("America/Los_Angeles")),
        lat=37.7749,
        lon=-122.4194
    )
    
    # Known placements (verified against astro.com)
    assert chart.sun.sign == "Pisces"
    assert abs(chart.sun.degree - 5.5) < 1.0
    assert chart.rising_sign == "Virgo"
```

**3. Synthesis Contribution**
```python
@pytest.mark.asyncio
async def test_synthesis_contribution():
    module = AstrologyModule()
    contribution = await module.contribute_to_synthesis(user_id)
    
    assert contribution["module"] == "astrology"
    assert "data" in contribution
    assert "insights" in contribution
    assert len(contribution["insights"]) > 0
```

**4. High-Fidelity Service Integration**
```python
# Verify the actual persistence in Redis/PostgreSQL. See high-fidelity-testing skill.
```

## Fixtures (conftest.py)

```python
@pytest_asyncio.fixture
async def seeded_user(test_user):
    """
    Deterministic seeding pattern. Populates DB with pattern-rich test data.
    """
    from tests.fixtures.seed_data import SeedDataGenerator
    from src.app.core.db.database import local_session
    
    async with local_session() as db:
        # Seed exact patterns for intelligence modules
        # e.g., anxiety on Sundays, headaches on high-solar days
        SeedDataGenerator.seed_historical_patterns(test_user.id, db)
        await db.commit()
    return test_user.id
```

## Critical Rules (MANDATORY)

- **NO MOCKS for Core Logic:** See `high-fidelity-testing` skill.
- **Service Integration:** Tests must use real Redis and PostgreSQL (Port 5432).
- **Persistence Verification:** Verify data exists in DB/Cache after operation.
- **Deterministic Seeding:** Use real data patterns, not random noise via `SeedDataGenerator`.
- **High Coverage:** 80% overall, 100% for calculation functions.
- **Session Passing:** Always pass the `db` session to modules to avoid isolation conflicts.
- **Aware Datetimes:** Always use `dt.datetime.now(dt.timezone.utc)` for comparisons and storage. NEVER use `dt.datetime.utcnow()`.
- **Async Singleton Initialization:** Integration tests MUST explicitly `await` initialization of `EventBus` and `ActiveMemory`.
- **PYTHONPATH:** Run tests from project root with `PYTHONPATH=src`.