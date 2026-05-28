---
name: dsa110-python-development
description: DSA-110 radio astronomy pipeline development with Python 3.11+, Dagster workflows, CASA integration, FastAPI, GraphQL/Strawberry, and scientific computing best practices. Use for any work on the dsa110-contimg codebase.
license: MIT
---

# DSA-110 Python Development

Modern Python development patterns for the DSA-110 continuum imaging pipeline.

## Project Structure

```
backend/src/dsa110_contimg/
├── api/             # FastAPI routes and schemas
├── calibration/     # CASA calibration service
├── dagster/         # Workflow assets and resources
├── graphql/         # Strawberry GraphQL schema
├── pipeline/        # Stage-based execution
├── unified_config.py  # Pydantic configuration
└── public_api.py    # External interface
```

## Configuration (Pydantic Settings)

Use `UnifiedPipelineConfig` for all configuration:

```python
from dsa110_contimg.unified_config import (
    UnifiedPipelineConfig,
    PathsConfig,
    ConversionConfig,
    CalibrationConfig,
    ImagingConfig,
)

# Load from YAML (default: backend/config/pipeline_config.yaml)
config = UnifiedPipelineConfig.from_yaml("pipeline_config.yaml")

# Or with environment variable overrides
# CONTIMG_CONVERSION__MAX_WORKERS=12 → config.conversion.max_workers = 12
config = UnifiedPipelineConfig()

# Access nested config
max_workers = config.conversion.max_workers
input_dir = config.paths.input_dir
```

### Config Precedence
1. Explicit arguments (highest)
2. YAML file
3. Environment variables (`CONTIMG_*`)
4. Code defaults (lowest)

## CASA Integration

Use `CASAService` for all CASA operations (handles log isolation):

```python
from dsa110_contimg.calibration.casa_service import CASAService

# Initialize (checks DSA110_CASA_PROCESS_ISOLATION env var)
casa = CASAService()

# Recommended for production: process isolation
casa = CASAService(use_process_isolation=True)

# Run tasks (all methods available)
casa.gaincal(vis="data.ms", caltable="cal.G", ...)
casa.bandpass(vis="data.ms", caltable="cal.BP", ...)
casa.tclean(vis="data.ms", imagename="output", ...)
casa.applycal(vis="data.ms", gaintable=["cal.G", "cal.BP"])

# Available methods:
# gaincal, bandpass, smoothcal, setjy, fluxscale, applycal,
# flagdata, tclean, ft, flagmanager, concat, initweights,
# phaseshift, gencal, clearcal, exportfits, split, mstransform
```

### Process Isolation
CASA has thread-safety issues with `casalog.log`. Enable isolation:
```bash
export DSA110_CASA_PROCESS_ISOLATION=true
```

## Dagster Assets

Define assets in `dsa110_contimg.dagster`:

```python
from dagster import asset, Output, AssetIn, DailyPartitionsDefinition

from dsa110_contimg.dagster.configs import ConversionRunConfig
from dsa110_contimg.pipeline.stages import ConversionStage
from dsa110_contimg.pipeline.context import PipelineContext

daily_partitions = DailyPartitionsDefinition(
    start_date="2024-01-01",
    timezone="UTC",
)

@asset(
    compute_kind="python",
    group_name="conversion",
    partitions_def=daily_partitions,
    description="Convert UVH5 to Measurement Sets",
    required_resource_keys={"dsa110_pipeline"},
)
def measurement_sets(
    context,
    config: ConversionRunConfig,
) -> Output[list[dict]]:
    """Convert UVH5 files to MS."""
    pipeline = context.resources.dsa110_pipeline
    pipeline_config = pipeline.get_config()
    
    # Apply run-specific overrides
    pipeline_config.conversion.max_workers = config.max_workers
    
    # Create and execute stage
    stage = ConversionStage(pipeline_config)
    pipeline_context = PipelineContext(
        config=pipeline_config,
        inputs={"start_time": start_date.isoformat()},
    )
    
    is_valid, error = stage.validate(pipeline_context)
    if not is_valid:
        return Output([], metadata={"error": error})
    
    result = stage.execute(pipeline_context)
    return Output(
        result.outputs.get("ms_paths", []),
        metadata={"num_converted": len(result.outputs.get("ms_paths", []))},
    )
```

### Asset Groups
- `conversion`: UVH5 → MS
- `calibration`: Solve/apply calibration
- `imaging`: Create FITS images
- `qa`: Quality validation
- `products`: Mosaics and photometry

## GraphQL with Strawberry

**CRITICAL**: Always use `@enforced_field` or explicit `name=` for camelCase:

```python
import strawberry
from dsa110_contimg.graphql.schema_utils import enforced_field, validate_schema_class

@strawberry.type
class Query:
    # ✅ CORRECT: Uses enforced_field (auto-converts to camelCase)
    @enforced_field
    def fits_image_metadata(self, path: str) -> FitsImageMetadata:
        return load_fits_metadata(path)
    
    # ✅ CORRECT: Explicit name parameter
    @strawberry.field(name="msFiles")
    def ms_files(self, limit: int = 10) -> list[MSFile]:
        return query_ms_files(limit)
    
    # ❌ WRONG: Will expose as snake_case
    @strawberry.field
    def calibration_tables(self, ms_path: str) -> list[str]:
        ...

# Validate at module load
validate_schema_class(Query)
```

## Public API

Use `public_api` for external integrations:

```python
from dsa110_contimg.public_api import (
    PipelineConfig,
    ConversionRequest,
    convert_uvh5_to_ms,
    calibrate_ms,
    image_ms,
)

# Configure
config = PipelineConfig()

# Convert UVH5 → MS
request = ConversionRequest(input_dir="/data/uvh5", output_dir="/data/ms")
result = convert_uvh5_to_ms(request)
if result.success:
    print(f"Created: {result.ms_path}")

# Calibrate MS
cal_result = calibrate_ms(
    result.ms_path,
    calibrator_field="3C286",
    do_bandpass=True,
    do_delay=False,
)

# Image calibrated MS
img_result = image_ms(
    result.ms_path,
    imsize=2048,
    cell_arcsec=0.5,
    niter=5000,
)
```

## Type Hints

Use Python 3.11+ union syntax:

```python
# ✅ Modern syntax
def process(
    data: str | None = None,
    items: list[str] = [],
) -> dict[str, Any]:
    ...

# ❌ Avoid legacy
from typing import Optional, List, Dict
def process(data: Optional[str] = None) -> Dict[str, Any]:
    ...
```

## Async Patterns

Use async for I/O-bound operations:

```python
import asyncio
from collections.abc import AsyncIterator

async def stream_fits_data(path: str) -> AsyncIterator[bytes]:
    """Stream FITS file in chunks."""
    async with aiofiles.open(path, "rb") as f:
        async for chunk in f:
            yield chunk

async def fetch_calibrator_info(sources: list[str]) -> list[dict]:
    """Fetch calibrator info concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_source(session, src) for src in sources]
        return await asyncio.gather(*tasks)
```

## Testing

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.fixture
def mock_casa_service():
    """Mock CASA service for unit tests."""
    service = AsyncMock()
    service.gaincal.return_value = {"success": True}
    return service

@pytest.mark.asyncio
async def test_calibration(mock_casa_service):
    with patch("dsa110_contimg.calibration.casa_service.CASAService", return_value=mock_casa_service):
        result = await run_calibration("test.ms")
        assert result["success"]
        mock_casa_service.gaincal.assert_called_once()

# Contract tests for real data
@pytest.mark.contract
def test_conversion_with_real_data():
    """Test with actual UVH5 files."""
    ...
```

### Test Commands
```bash
# Fast unit tests
pytest tests/unit/ -q

# Contract tests (real data)
pytest tests/contract/ -v -m contract

# All tests parallel
pytest tests/unit/ -n 4 -q
```

## Best Practices

### Code Style
- Use `ruff` for linting (configured in `pyproject.toml`)
- NumPy-style docstrings (enforced by pydocstyle)
- Ban relative imports (`from ..module import x` → explicit paths)

### Configuration
- Prefer YAML for reproducible pipeline runs
- Use env vars for deployment-specific settings
- Validate early with Pydantic

### CASA Operations
- Always use `CASAService`, never raw CASA imports
- Enable process isolation for production
- Log all CASA commands for debugging

### Dagster Assets
- Use `compute_kind` for UI display ("python", "casa", "wsclean")
- Group related assets with `group_name`
- Return `Output` with metadata for observability
- Use run configs for Launchpad parameter overrides

### GraphQL
- Always validate snake_case → camelCase conversion
- Use `@enforced_field` decorator
- Run `validate_schema_class(Query)` at module load
