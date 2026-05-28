---
name: data-io-management
description: Data ingestion, staging, metadata, storage layout, HDF5 lifecycle, and product I/O. Use when moving data through the pipeline, inspecting datasets, or managing storage/metadata integrity.
---

# Data I/O Management

## Workflow

1) Define the dataset scope
- Identify dataset IDs, time ranges, and storage locations.
- Confirm expected inputs/outputs (raw, staged, products).

2) Inspect existing layout and metadata
- Prefer read-only inspection before any migration or cleanup.
- Record current state for provenance.

3) Perform ingestion or lifecycle steps
- Use documented scripts and procedures.
- Validate integrity after each step.

4) Validate outputs and storage health
- Check metadata completeness and expected file counts.

## Repo Pointers

- `docs/how-to/ingestion.md`
- `docs/reference/storage.md`
- `docs/reference/configuration/`
- `docs/hdf5-lifecycle-management.md`
- `docs/HDF5_LIFECYCLE_QUICKSTART.md`
- `docs/tutorials/01_discovery.md` (tutorial; verify before use)
- `docs/tutorials/01_data_discovery_and_conversion.ipynb` (tutorial; verify before use)
- `scripts/validation/`
- `scripts/utils/`
- `products/`
- `stage/`
- `state/`

## References

- Read `references/data-io.md` for ingestion/lifecycle checkpoints and known safe operations.

## Output Expectations

- Provide dataset inventory and paths touched.
- Provide validation results and any anomalies.

## Guardrails

- Avoid destructive cleanup without explicit confirmation.
- Preserve provenance and checksums when possible.
- Treat tutorials as advisory; validate against verified docs and code.
