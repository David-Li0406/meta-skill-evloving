---
name: mxl-nl2sim-eval
description: Use this skill to build and evaluate NL-to-MaxwellLink agent workflows (benchmarks, validators, closed-loop retries) with research-grade metrics.
---

# NL-to-simulation benchmark and closed-loop evaluation

## Scope
- Use when creating/expanding NL intent benchmarks, attaching physics validators, and running agent loops that scaffold, check, run, and self-critique MaxwellLink jobs.
- Treat this as the research harness: edit the levers below to move from “demo” to publishable results.

## Directory layout (template to clone/modify)
- Put benchmark tasks under `benchmarks/nl2sim/<task-name>/`:
  - `intent.md`: natural-language request.
  - `gold/config.json`: expected MaxwellLink config (project-style).
  - `gold/notes.md`: acceptance criteria (e.g., target signals/fields, tolerances, runtime caps).
  - `checks.yaml`: semantic checks (units, stability, geometry plausibility).
- Run-time projects stay under `projects/YYYY-MM-DD-NAME/` per `AGENTS.md`.

## Build/extend tasks (research lever 1: coverage/difficulty)
- Seed 20–50 tasks spanning solvers/drivers: Meep TLS (embedded/socket), SingleMode, LaserDriven, Psi4 RT-TDDFT/RT-Ehrenfest, ASE/LAMMPS charges.
- Provide short-run variants (small `until`, coarse grids) for fast evaluation and longer variants for “paper-grade” fidelity.
- In `gold/notes.md`, define physics-grounded accept criteria (e.g., max field-energy error ≤5%; population decay trend; no Courant violations).

## Validator hooks (research lever 2: rigor of semantic checks)
- Schema: `python skills/mxl-project-scaffold/scripts/mxl_validate_project.py projects/YYYY-MM-DD-NAME`
- Physics: add Python validators in `benchmarks/nl2sim/validators/` and reference them from `checks.yaml`.
  - Typical checks: `time_units_fs` vs `resolution` (Courant), dipole `orientation` vs source polarization, `pml_thickness` vs wavelength, charge consistency for ASE/LAMMPS, Psi4 grid/basis sanity.
- Emit pass/fail plus messages an LLM can self-critique against.

## Agent loop recipe (working example to start from)
1. Scaffold: `python skills/mxl-project-scaffold/scripts/mxl_scaffold_project.py --template meep-tls-embedded --name nl2sim-demo`
2. Agent fills `projects/YYYY-MM-DD-nl2sim-demo/config.json` from `benchmarks/nl2sim/<task-name>/intent.md` (use the template structure above).
3. Schema check: `python skills/mxl-project-scaffold/scripts/mxl_validate_project.py projects/YYYY-MM-DD-nl2sim-demo`
4. Short sanity run: use the template’s `run_local.sh` or `python em.py` after trimming `until` for speed; capture outputs (e.g., `tls_history.csv`).
5. Physics check: run validators listed in `checks.yaml`; compare to `gold/notes.md`.
6. Self-critique/retry: feed failures back to the LLM, revise `config.json`, and re-run steps 3–5. Log retries and final status.

## Metrics to log (research lever 3: what makes it paper-worthy)
- Task success rate (schema + physics) vs. human baseline.
- Average retries/time/compute per success; token cost if using APIs.
- Quality deltas: spectral peaks, dipole trajectories, energy conservation vs. gold.
- Robustness: transfer to unseen tasks/solvers, ablations of validators or prompts.

## Customize for publication
- Expand `benchmarks/nl2sim/` with harder/novel tasks (multi-molecule sockets, SLURM TCP handoff, long-context KV-cache stress).
- Harden `checks.yaml` and validator functions to catch subtle instabilities (e.g., PML reflections, Psi4 memory/thread mismatches, ASE charge drift).
- Add a comparison harness to run the same task with/without the agent loop and report failure modes; this differentiation is often a high-impact story.
