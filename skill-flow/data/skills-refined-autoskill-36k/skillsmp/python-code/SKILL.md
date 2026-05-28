---
name: python-code
description: Expert Python code creation and management for the statement-extractor library. Use when creating new Python modules, implementing pipeline plugins, or following project-specific Python patterns. Specializes in NLP pipelines, Pydantic models, and plugin architecture.
---

# Python Code Skill

Expert assistant for creating and managing Python code in the statement-extractor library (`statement-extractor-lib/`).

## Core Philosophy

**Lean and Simple**: Avoid over-engineering, keep abstractions minimal
**Fail-Fast**: Raise exceptions immediately, never silently degrade
**Strong Typing**: Type annotations everywhere, prefer Pydantic over dicts
**Plugin Architecture**: All pipeline functionality through registered plugins

## Quick Reference

### Import Pattern (stdlib → third-party → local)

```python
import logging
from pathlib import Path
from typing import Optional

import numpy as np
from pydantic import BaseModel, Field

from ..base import BasePlugin, PluginCapability
from ...pipeline.context import PipelineContext
from ...pipeline.registry import PluginRegistry
from ...models import PipelineStatement, EntityType
```

### Plugin Registration Pattern

```python
from ...pipeline.registry import PluginRegistry

@PluginRegistry.qualifier  # or @PluginRegistry.labeler, @PluginRegistry.taxonomy, etc.
class MyPlugin(BaseQualifierPlugin):
    """Plugin docstring."""

    @property
    def name(self) -> str:
        return "my_plugin"

    @property
    def priority(self) -> int:
        return 100  # Lower = higher priority
```

### Pydantic Models (NOT dicts)

```python
class TaxonomyResult(BaseModel):
    taxonomy_name: str
    category: str
    label: str
    label_id: Optional[int] = None
    confidence: float = 1.0
    classifier: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @property
    def full_label(self) -> str:
        return f"{self.category}:{self.label}"
```

### Validation (fail-fast at boundaries)

```python
def process_entity(entity_id: str) -> EntityModel:
    if not entity_id:
        raise ValueError("entity_id is required")
    if not entity_id.startswith("entity_"):
        raise ValueError(f"Invalid entity_id format: {entity_id}")
    # ... process
```

### Logging Pattern

```python
import logging

logger = logging.getLogger(__name__)

def process_data(text: str) -> Result:
    logger.info(f"Processing {len(text)} characters")

    try:
        result = do_processing(text)
        logger.debug(f"Processed successfully: {result}")
        return result
    except Exception as e:
        logger.warning(f"Processing failed: {e}")
        raise  # Re-raise after logging
```

## Critical Rules

✅ **DO**:
- Import from modules: `from ...models import EntityType`
- Use Pydantic for structured data
- Validate inputs at function boundaries
- Let exceptions propagate
- Register plugins with decorators
- Keep files under 400 lines
- Use `Optional[T]` for nullable values
- Use `Field(default_factory=list)` for mutable defaults

❌ **DON'T**:
- Re-export in `__init__.py` (causes circular imports)
- Use dicts for business logic (use Pydantic)
- Swallow exceptions silently
- Use `hasattr`/`getattr` for known attributes
- Make List/Dict fields Optional (use `default_factory=`)
- Create plugins without registration

## Project Structure

```
statement-extractor-lib/
  pyproject.toml
  src/statement_extractor/
    __init__.py              # Public API exports
    cli.py                   # CLI entry point
    models/                  # Pydantic models
      __init__.py
      base.py               # RawTriple, PipelineStatement, etc.
      entities.py           # Entity models
      labels.py             # Label and taxonomy models
    pipeline/               # Pipeline infrastructure
      __init__.py
      context.py            # PipelineContext
      config.py             # PipelineConfig
      orchestrator.py       # ExtractionPipeline
      registry.py           # PluginRegistry
    plugins/                # Pipeline plugins
      __init__.py
      base.py               # Base plugin classes
      splitters/            # Stage 1 plugins
      extractors/           # Stage 2 plugins
      qualifiers/           # Stage 3 plugins
      canonicalizers/       # Stage 4 plugins
      labelers/             # Stage 5 plugins
      taxonomy/             # Stage 6 plugins
    data/                   # Data files
      statement_taxonomy.json
```

## Key Patterns

### Pipeline Plugin Pattern

```python
from ..base import BaseTaxonomyPlugin, TaxonomySchema, PluginCapability
from ...pipeline.registry import PluginRegistry
from ...models import TaxonomyResult

@PluginRegistry.taxonomy
class MyTaxonomyPlugin(BaseTaxonomyPlugin):
    """Classify statements against my taxonomy."""

    def __init__(self, min_confidence: float = 0.3):
        self._min_confidence = min_confidence
        self._model = None

    @property
    def name(self) -> str:
        return "my_taxonomy_classifier"

    @property
    def priority(self) -> int:
        return 50

    @property
    def capabilities(self) -> PluginCapability:
        return PluginCapability.LLM_REQUIRED

    @property
    def taxonomy_name(self) -> str:
        return "my_taxonomy"

    def classify(
        self,
        statement: PipelineStatement,
        subject_canonical: CanonicalEntity,
        object_canonical: CanonicalEntity,
        context: PipelineContext,
    ) -> list[TaxonomyResult]:
        # Classification logic here
        return results
```

### Lazy Model Loading

```python
class MyPlugin:
    def __init__(self):
        self._model = None

    def _get_model(self):
        """Lazy-load model on first use."""
        if self._model is None:
            logger.info("Loading model...")
            self._model = load_expensive_model()
        return self._model
```

### Entity Types

```python
from enum import Enum

class EntityType(str, Enum):
    PERSON = "PERSON"
    ORG = "ORG"
    GPE = "GPE"
    LOC = "LOC"
    PRODUCT = "PRODUCT"
    EVENT = "EVENT"
    DATE = "DATE"
    MONEY = "MONEY"
    UNKNOWN = "UNKNOWN"
```

## Supporting Documentation

- **[python-patterns.md](python-patterns.md)**: Pydantic, functional programming, error handling
- **[Plugin Architecture](../../../statement-extractor-lib/README.md)**: 6-stage pipeline documentation

## Related Skills

- **python-code**: General Python patterns
- **doc**: Documentation updates
