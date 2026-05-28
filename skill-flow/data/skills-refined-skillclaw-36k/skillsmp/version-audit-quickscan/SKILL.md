---
name: version-audit-quickscan
description: Quick scan for version strings across common files (README, pyproject, requirements, package manifests) to avoid release blockers from inconsistent versions. Use before tagging or publishing.
---

# Skill Instructions

## Inputs

- `ROOT` (string, optional): directory to scan (default: `.`)
- `EXTRA_PATTERNS` (string, optional): additional grep regex patterns (pipe-separated)

## Procedure

```bash
set -euo pipefail

root="${ROOT:-.}"

# Common version patterns across ecosystems.
# NOTE: keep it broad; the goal is to surface candidates for human review.
base_patterns='(version\s*[=:]\s*["\x27]?[0-9]+\.[0-9]+\.[0-9]+|__version__\s*=\s*["\x27][0-9]+\.[0-9]+\.[0-9]+|v[0-9]+\.[0-9]+\.[0-9]+)'
extra_patterns="${EXTRA_PATTERNS:-}"

pattern="$base_patterns"
if [ -n "$extra_patterns" ]; then
  pattern="$pattern|$extra_patterns"
fi

# Focus on likely files; avoid huge vendor dirs.
# If needed, expand includes for your repo.
find "$root" \
  -type f \
  \( \
    -name 'README.md' -o -name 'CHANGELOG.md' -o \
    -name 'pyproject.toml' -o -name 'setup.py' -o -name 'setup.cfg' -o \
    -name 'requirements*.txt' -o -name 'package.json' -o -name 'Cargo.toml' -o \
    -name '*.yml' -o -name '*.yaml' \
  \) \
  -not -path '*/.venv/*' \
  -not -path '*/venv/*' \
  -not -path '*/venv_host/*' \
  -not -path '*/node_modules/*' \
  -not -path '*/.git/*' \
  -print0 \
| xargs -0 -r grep -nE -- "$pattern" \
| sed -n '1,200p'
```

## Acceptance Criteria

- You get a short list of candidate version strings to verify/update (not necessarily zero matches).
- Any release/version decision is cross-checked against the authoritative roadmap/plan/release artifacts.

## Notes

- This is a *discovery* tool; it may include false positives.
- For large repos, consider narrowing file globs.
