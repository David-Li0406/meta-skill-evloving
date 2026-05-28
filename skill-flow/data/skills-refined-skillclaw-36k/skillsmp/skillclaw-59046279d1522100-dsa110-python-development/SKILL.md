---
name: dsa110-python-development
description: Use this skill for developing the DSA-110 radio astronomy pipeline with Python 3.11+, integrating Dagster workflows, CASA, FastAPI, and GraphQL/Strawberry, while adhering to scientific computing best practices.
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
export DSA110_CASA_PROCESS_ISOLATION=True
```