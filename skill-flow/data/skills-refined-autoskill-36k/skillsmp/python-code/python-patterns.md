# Python Code Patterns

Common patterns for Python code in the statement-extractor library.

## Pydantic Model Patterns

### Basic Model

```python
from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime

class PipelineStatement(BaseModel):
    # Required fields
    subject: ExtractedEntity
    predicate: str
    object: ExtractedEntity
    source_text: str

    # Optional with defaults
    predicate_category: Optional[str] = None
    confidence_score: float = 0.0
    extraction_method: str = "unknown"

    # Collections (use default_factory, NOT Optional)
    metadata: dict[str, Any] = Field(default_factory=dict)
```

### Model with Properties

```python
class TaxonomyResult(BaseModel):
    taxonomy_name: str
    category: str
    label: str
    confidence: float = 1.0

    @property
    def full_label(self) -> str:
        """Return category:label format."""
        return f"{self.category}:{self.label}"
```

### Field Validation

```python
from pydantic import BaseModel, field_validator

class ExtractedEntity(BaseModel):
    text: str
    type: EntityType
    confidence: float = 1.0

    @field_validator('confidence')
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        if not 0.0 <= v <= 1.0:
            raise ValueError(f"Confidence must be 0-1: {v}")
        return v
```

## Functional Patterns

### List Comprehensions (Preferred)

```python
# Extract texts
texts = [stmt.source_text for stmt in statements if stmt.source_text]

# Create lookup
lookup = {entity.entity_ref: entity for entity in entities}

# Get unique values
categories = {result.category for result in results if result.category}
```

### Pure Functions

```python
def calibrate_score(raw_similarity: float, threshold: float = 0.65) -> float:
    """Pure function: same inputs = same output, no side effects."""
    if not -1.0 <= raw_similarity <= 1.0:
        raise ValueError(f"Invalid similarity: {raw_similarity}")
    normalized = (raw_similarity + 1) / 2
    return 1.0 / (1.0 + np.exp(-25.0 * (normalized - threshold)))
```

## Error Handling

### Custom Exceptions

```python
class ExtractorError(Exception):
    """Base for all extractor exceptions."""
    pass

class ModelNotFoundError(ExtractorError):
    """Model file not found."""
    def __init__(self, model_path: str):
        self.model_path = model_path
        super().__init__(f"Model not found: {model_path}")
```

### Validation Pattern

```python
def validate_text_length(text: str, min_length: int = 10) -> None:
    """Validate text length or raise ValueError."""
    if not text:
        raise ValueError("Text is required")
    if len(text) < min_length:
        raise ValueError(f"Text too short: {len(text)} < {min_length}")

def extract_statements(text: str) -> list[Statement]:
    """Extract statements from text."""
    validate_text_length(text)
    return perform_extraction(text)
```

### Logging Pattern

```python
import logging

logger = logging.getLogger(__name__)

def process_triple(raw: RawTriple) -> Optional[PipelineStatement]:
    """Process a raw triple."""
    logger.debug(f"Processing: {raw.subject_text} -> {raw.predicate_text}")

    try:
        result = do_processing(raw)
        logger.info(f"Processed: {result.subject.text}")
        return result
    except Exception as e:
        logger.warning(f"Failed to process triple: {e}")
        return None  # Or raise depending on fail-fast policy
```

## Plugin Patterns

### Base Plugin Implementation

```python
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """Base class for all plugins."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique plugin name."""
        ...

    @property
    def priority(self) -> int:
        """Lower = higher priority."""
        return 100

    @property
    def capabilities(self) -> PluginCapability:
        """Plugin capabilities."""
        return PluginCapability.NONE
```

### Lazy Model Loading

```python
class GLiNER2Extractor(BaseExtractorPlugin):
    def __init__(self):
        self._model = None

    def _get_model(self):
        """Lazy-load the GLiNER2 model."""
        if self._model is None:
            try:
                from gliner2 import GLiNER2
                logger.info("Loading GLiNER2 model...")
                self._model = GLiNER2.from_pretrained("fastino/gliner2-base-v1")
            except ImportError:
                logger.warning("GLiNER2 not installed")
                self._model = None
        return self._model
```

## Configuration Pattern

```python
from typing import Final

# Constants
MIN_CONFIDENCE: Final[float] = 0.3
MAX_CATEGORIES: Final[int] = 3
DEFAULT_MODEL: Final[str] = "all-MiniLM-L6-v2"

# Usage
if confidence < MIN_CONFIDENCE:
    return []
```

## Context Manager Pattern

```python
from contextlib import contextmanager
from typing import Generator
import time

@contextmanager
def timed_operation(name: str) -> Generator[None, None, None]:
    """Context manager for timing operations."""
    start = time.perf_counter()
    logger.info(f"Starting {name}")

    try:
        yield
    except Exception as e:
        logger.error(f"{name} failed: {e}")
        raise
    finally:
        duration = time.perf_counter() - start
        logger.info(f"Completed {name} in {duration:.2f}s")

# Usage
with timed_operation("taxonomy classification"):
    results = classifier.classify(text)
```

## State Machine Pattern

```python
from enum import Enum
from pydantic import BaseModel, ConfigDict

class PipelineStage(str, Enum):
    SPLITTING = "splitting"
    EXTRACTION = "extraction"
    QUALIFICATION = "qualification"
    CANONICALIZATION = "canonicalization"
    LABELING = "labeling"
    TAXONOMY = "taxonomy"

STAGE_ORDER = [
    PipelineStage.SPLITTING,
    PipelineStage.EXTRACTION,
    PipelineStage.QUALIFICATION,
    PipelineStage.CANONICALIZATION,
    PipelineStage.LABELING,
    PipelineStage.TAXONOMY,
]
```

## Import Anti-Patterns

### DON'T: Re-export in __init__.py

```python
# BAD - causes circular imports
# __init__.py
from .module import MyClass
__all__ = ["MyClass"]
```

### DO: Import directly from modules

```python
# GOOD
from statement_extractor.models.base import PipelineStatement
from statement_extractor.pipeline.context import PipelineContext
```

---

(c) Statement Extractor Project
