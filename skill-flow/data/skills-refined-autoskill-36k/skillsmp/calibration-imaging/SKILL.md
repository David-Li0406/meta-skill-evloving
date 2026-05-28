---
name: calibration-imaging
description: Calibration, flagging, imaging, mosaicking, and continuum-specific processing workflows. Use when working on calibration recipes, imaging parameters, flagging strategies, beam/mask usage, or generating science-quality images.
---

# Calibration + Imaging

## Workflow

1) Identify the data product and outcome
- Clarify target field, time range, and expected image products.
- Determine whether this is calibration, imaging, self-cal, or mosaicking.

2) Find the closest verified recipe
- Prefer `docs/how-to/*` and `docs/reference/*` guides.
- Treat tutorials as advisory and validate against tested docs or code.

3) Run a scoped test
- Use a small subset or reduced resolution to validate parameters.
- Inspect intermediate artifacts before full-scale runs.

4) Execute full run and validate outputs
- Capture parameters, provenance, and QC notes for reproducibility.

## Repo Pointers

- `docs/how-to/calibration.md`
- `docs/how-to/imaging.md`
- `docs/how-to/mosaicking.md`
- `docs/how-to/self-calibration.md`
- `docs/how-to/recipe-batch-calibration.md`
- `docs/how-to/recipe-calibrator-conversion.md`
- `docs/how-to/recipe-calibrator-transits.md`
- `docs/reference/beam-model-usage.md`
- `docs/reference/mask-usage.md`
- `docs/reference/coordinates.md`
- `docs/tutorials/02_calibration_and_imaging.ipynb` (tutorial; verify before use)
- `docs/tutorials/02_manual_processing.md` (tutorial; verify before use)
- `scripts/analysis/`
- `scripts/visualization/`

## References

- Read `references/calibration-imaging.md` for vetted workflows, parameter defaults, and safety checks.

## Output Expectations

- Provide the parameter set and any modified defaults.
- Provide paths to generated products and validation notes.

## Guardrails

- Avoid full-scale reruns without confirming storage/compute impact.
- Record calibration versions and inputs for traceability.
- Treat tutorials as advisory; validate against verified docs and code.
