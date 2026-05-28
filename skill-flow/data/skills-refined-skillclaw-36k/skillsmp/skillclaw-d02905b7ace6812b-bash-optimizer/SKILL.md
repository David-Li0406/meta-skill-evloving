---
name: bash-optimizer
description: Use this skill when optimizing shell scripts for performance, enforcing coding standards, and preparing scripts for production.
---

# Bash Script Optimizer

Analyze and optimize bash scripts according to strict standards: performance, modern tooling, and consolidation patterns.

## Quick Start

**Analyze a script:**
```bash
python3 scripts/analyze.py path/to/script.sh
```

**Optimize workflow:**
1. Run the analyzer on target script(s).
2. Review issues by priority: critical → performance → optimization → standards.
3. Apply fixes systematically.
4. Validate with shellcheck.
5. Test functionality.
6. Measure improvement.

## Core Standards

Scripts must include:
```bash
#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob globstar
IFS=$'\n\t'
export LC_ALL=C LANG=C
```

**Style:** 2-space indent, minimal blank lines, short CLI args, quoted variables.

**Native bash:** Use arrays, `[[ ]]` tests, parameter expansion, and process substitution.

**Modern tools (prefer → fallback):**
- fd/fdfind → find
- rg → grep
- sd → sed
- fzf/sk for interactive
- jaq → jq
- choose → cut/awk
- rust-parallel → parallel → xargs -P

See `references/standards.md` for complete specifications.

## Analysis Categories

**Critical:** Must fix (security, correctness)
- Parsing `ls` output
- Unquoted variables
- `eval` usage
- Wrong shebang

**Performance:** Significant impact
- Unnecessary `cat` pipes
- Excessive subshells/forks
- Sequential vs parallel opportunities
- Uncached expensive operations

**Optimization:** Modern alternatives
- `find` → `fd` (3-5x faster)
- `grep` → `rg` (10x+ faster)
- `sed` → `sd` (cleaner syntax)
- Legacy tool replacement opportunities

**Standards:** Code quality
- Use `[[ ]]` instead of `[ ]`
- Prefer `printf` over `echo`
- Maintain 2-space indentation
- Use `fn(){}` for function syntax

## Consolidation Patterns

**When to consolidate multiple scripts:**
- Shared validation/setup logic
- Common function libraries
- Similar workflows with parameter variations
- Reduce maintenance burden

**Unified entry point pattern:**
```bash
mode=${1:-}
case $mode in
  action1) shift; action1_fn "$@";;
  action2) shift; action2_fn "$@";;
  *) die "Usage: $0 {action1|action2}";;
esac
```