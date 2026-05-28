---
name: mxl-laser-driven
description: This skill should be used when users need MaxwellLink laser-driven (prescribed-field) simulations, including pulse setup and coupling-axis conventions.
---

# Laser-driven workflows (prescribed field)

## Use when field is prescribed
- Use `mxl.LaserDrivenSimulation` when no EM back-action is required and the electric field is supplied directly.

## Configure
- Set `dt_au`, `coupling_axis`, and a `drive` (callable or float).
- Reuse pulse helpers from `maxwelllink.tools` (`gaussian_pulse`, `gaussian_enveloped_cosine`, `cosine_drive`) when appropriate.

## Prefer templates
- Template: `skills/mxl-project-scaffold/assets/templates/laser-tls-embedded`

## References
- Recipes: `skills/mxl-laser-driven/references/laser_run_recipes.md`
- Docs: `docs/source/em_solvers/laser_driven.rst`

