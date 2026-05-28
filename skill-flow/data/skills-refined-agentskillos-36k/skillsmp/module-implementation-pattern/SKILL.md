---
name: module-implementation-pattern
description: Standard pattern for GUTTERS modules. Use when creating calculation, tracking, or intelligence modules to ensure production-quality implementation with database configs and event integration.
---

# Module Implementation Pattern

Complete pattern for GUTTERS modules. Every module: inherits `BaseModule`, loads config from database, publishes events, contributes to synthesis.

## Directory Structure
```
modules/{layer}/{module_name}/
├── __init__.py
├── module.py          # Main class (inherits BaseModule)
├── schemas.py         # Pydantic validation
├── service.py         # Business logic
├── models.py          # SQLAlchemy (only if module needs tables)
├── crud.py            # FastCRUD (only if has models)
├── tasks.py           # ARQ jobs (only for tracking modules)
└── tests/
    └── test_{module_name}.py
```

## module.py Template
```python
from app.modules.base import BaseModule
from typing import Dict, Any
from uuid import UUID
from sqlalchemy import select

class {ModuleName}Module(BaseModule):
    name = "{module_name}"
    layer = "{calculation|tracking|intelligence}"
    version = "1.0.0"
    description = "Brief description"
    
    async def initialize(self) -> None:
        """Load config from DB, subscribe to events."""
        await super().initialize()
        
        # REQUIRED: Load config from database
        async for db in async_get_db():
            result = await db.execute(
                select(SystemConfiguration).where(
                    SystemConfiguration.module_name == self.name,
                    SystemConfiguration.is_active == True
                )
            )
            config = result.scalar_one_or_none()
            self.config = config.config if config else self.default_config()
            break
        
        # Subscribe to events if needed
        # event_bus.subscribe("event.name", self.handler)
        
        self.initialized = True
    
    async def contribute_to_synthesis(self, user_id: UUID) -> Dict[str, Any]:
        """Return data for master synthesis."""
        profile = await self.get_profile(user_id)
        return {
            "module": self.name,
            "layer": self.layer,
            "data": profile,
            "insights": self.extract_insights(profile),
            "metadata": {"confidence": 1.0}
        }
    
    async def get_profile(self, user_id: UUID) -> Dict[str, Any]:
        """Get/calculate user profile."""
        # Implementation
        pass
    
    def default_config(self) -> Dict[str, Any]:
        """Fallback if no DB config."""
        return {}  # Module-specific defaults
    
    def extract_insights(self, profile: Dict) -> List[str]:
        """Key insights as strings."""
        return []  # Module-specific
```

## schemas.py Pattern
```python
from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class {ModuleName}Data(BaseModel):
    """Typed output (NOT generic dict)."""
    # Specific fields, fully typed
    field1: str
    field2: float
    field3: int

class {ModuleName}Read(BaseModel):
    """API response schema."""
    id: int
    user_id: UUID
    data: {ModuleName}Data
    created_at: datetime
    
    class Config:
        from_attributes = True
```

## service.py Pattern
```python
from typing import Dict, Any

async def calculate_{function}(
    param: Type,
    config: Dict[str, Any]  # From database
) -> {ModuleName}Data:
    """
    Calculate {what}.
    
    Args:
        param: Description
        config: Database config (NEVER hardcoded)
    
    Returns:
        Fully typed result
    """
    # Use config values (from database)
    threshold = config.get("threshold", 10)  # NEVER hardcode
    
    # Calculation logic
    result = perform_calculation(param, threshold)
    
    # Return typed schema
    return {ModuleName}Data(**result)
```

## Testing Pattern
```python
import pytest
from uuid import uuid4

@pytest.mark.asyncio
async def test_module_loads_config_from_db(mock_db):
    """Verify config loaded from database."""
    module = {ModuleName}Module()
    await module.initialize()
    
    assert module.config is not None
    assert "key_setting" in module.config  # From DB

@pytest.mark.asyncio
async def test_calculation_against_known_data():
    """Test against VERIFIED data."""
    result = await calculate_{function}(
        known_input,
        config={"threshold": 8}
    )
    assert result.field == expected_value

@pytest.mark.asyncio
async def test_synthesis_contribution(module):
    """Test synthesis output structure."""
    contribution = await module.contribute_to_synthesis(uuid4())
    
    assert contribution["module"] == module.name
    assert "data" in contribution
    assert "insights" in contribution
    assert len(contribution["insights"]) > 0
```

## Critical Checklist

- [ ] Inherits from `BaseModule`
- [ ] Loads config from `system_configurations` table
- [ ] NO hardcoded thresholds/parameters
- [ ] Full type hints (no `any`)
- [ ] Pydantic schemas for all data
- [ ] Tests with >80% coverage
- [ ] Migration created if models added
- [ ] Registered in `modules/__init__.py`

## Common Mistakes

❌ `threshold = 8  # WRONG - hardcoded`  
✅ `threshold = config.get("threshold", 8)  # RIGHT - from DB`

❌ `def calculate(data):  # WRONG - no types`  
✅ `def calculate(data: InputData) -> OutputData:  # RIGHT`

❌ Skip tests  
✅ Test initialization, calculation, synthesis

See `references/` for detailed examples per module type.