# Dependencies

This file is an example placeholder referenced by the Skill Creator skill.

## Upgrade Policy

- **Cadence**: [weekly/monthly]
- **Risk levels**: patch/minor/major
- **Ownership**: who approves and merges upgrades

## Upgrade Workflow

1. Identify target version and changelog highlights
2. Check compatibility notes (peer deps, runtime requirements)
3. Update dependency constraints
4. Fix compile/typecheck/build errors
5. Run tests and verify key flows
6. Monitor after release

## Breaking Changes

- List common break categories: API changes, config changes, transitive dependency shifts
- Preferred mitigation patterns: adapters, shims, incremental migration

## Lockfile & Reproducibility

- Keep lockfiles updated and consistent
- Document how CI installs dependencies

## Security

- How to handle critical CVEs
- How to record/justify exceptions
