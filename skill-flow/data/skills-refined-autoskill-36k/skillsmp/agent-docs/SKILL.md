---
name: agent-docs
description: This skill should be used when the user asks to "audit AGENTS.md", "check agent docs", "verify documentation accuracy", "maintain agent instructions", "check for drift", or mentions documentation needs updating based on code changes.
---

# agent-docs-audit

systematic methodology for auditing and maintaining AGENTS.md documentation. ensures docs stay synchronized with code structure and prevents drift.

## philosophy

| principle | application |
|-----------|-------------|
| docs as contracts | AGENTS.md is a promise to AI agents about codebase behavior |
| drift is debt | stale docs mislead agents, causing wrong assumptions |
| verify before trust | every claim in docs must be checkable |
| minimal viable docs | document what agents need, not everything |
| symlinks for consistency | CLAUDE.md always symlinks to AGENTS.md |

## when to use

| use | skip |
|-----|------|
| pre-commit audit after structural changes | cosmetic/copy changes |
| periodic health checks (weekly) | single-file edits |
| after refactoring or renaming | README updates |
| new directory reaches 3+ files | external documentation |
| drift suspected (agent confusion) | config-only changes |

## decision tree: audit scope

```
What scope should this audit cover?
├── User mentions specific file/directory?
│   └── targeted audit (single AGENTS.md)
├── User mentions "full audit" or "everything"?
│   └── comprehensive audit (all AGENTS.md files)
├── Recent commit/PR context?
│   └── changed-files audit (affected directories only)
├── Periodic/scheduled audit?
│   └── comprehensive + staleness check
└── Drift suspected (agent made wrong assumption)?
    └── forensic audit (trace claim to code)
```

## decision tree: audit depth

```
How deep should verification go?
├── Quick check (< 2 min)?
│   ├── file counts match?
│   ├── key exports exist?
│   └── symlinks valid?
├── Standard check (2-10 min)?
│   ├── all file counts
│   ├── all documented patterns exist
│   ├── all types/functions findable
│   └── recent changes covered
└── Deep check (10+ min)?
    ├── pattern usage counts
    ├── cross-reference accuracy
    ├── example code correctness
    └── missing documentation discovery
```

## decision tree: what to update

```
What action should I take for each finding?
├── File count mismatch?
│   └── update count immediately (low risk)
├── Documented export not found?
│   ├── recently deleted? → remove from docs
│   ├── renamed? → update name in docs
│   └── moved? → update path in docs
├── Undocumented significant code?
│   ├── 3+ files in directory? → create AGENTS.md
│   ├── complex pattern? → document pattern
│   └── critical for agents? → add to parent AGENTS.md
├── CLAUDE.md is regular file?
│   └── convert to symlink → AGENTS.md
├── Stale example code?
│   ├── example still valid pattern? → update syntax
│   └── pattern deprecated? → remove example
└── Missing warning for footgun?
    └── add IMPORTANT/WARNING section
```

## decision tree: documentation needed

```
Does this directory need AGENTS.md?
├── Contains 3+ source files?
│   └── likely yes (document structure)
├── Represents distinct pattern/feature?
│   └── yes (document pattern)
├── Has complex interdependencies?
│   └── yes (document relationships)
├── Agents frequently confused here?
│   └── yes (document gotchas)
├── Just utils/helpers?
│   └── maybe (document only if non-obvious)
└── Leaf node with single responsibility?
    └── no (parent docs sufficient)
```

## decision tree: symlink handling

```
How should I handle CLAUDE.md files?
├── CLAUDE.md is symlink → AGENTS.md?
│   └── ✓ correct, verify target exists
├── CLAUDE.md is symlink → wrong target?
│   └── fix: rm && ln -s AGENTS.md CLAUDE.md
├── CLAUDE.md is regular file?
│   ├── content matches AGENTS.md? → convert to symlink
│   └── content differs? → merge to AGENTS.md, then symlink
├── CLAUDE.md missing but AGENTS.md exists?
│   └── create symlink: ln -s AGENTS.md CLAUDE.md
└── Neither exists?
    └── check if directory needs docs (see above tree)
```

### cross-platform symlink notes

| platform | symlink command | notes |
|----------|-----------------|-------|
| macOS/Linux | `ln -s AGENTS.md CLAUDE.md` | POSIX standard, always works |
| Windows (Git Bash) | `ln -s AGENTS.md CLAUDE.md` | requires `core.symlinks=true` in git config |
| Windows (CMD) | `mklink CLAUDE.md AGENTS.md` | requires admin or developer mode |
| Windows (PowerShell) | `New-Item -ItemType SymbolicLink -Path CLAUDE.md -Target AGENTS.md` | requires admin or developer mode |

**git configuration for cross-platform**:

```bash
# enable symlinks in git (required for Windows)
git config --global core.symlinks true

# verify symlink is tracked correctly
git ls-files -s CLAUDE.md  # should show mode 120000 for symlink
```

**fallback for environments without symlink support**:

If symlinks fail (some CI environments, Windows without dev mode), use a copy with a comment marker:

```markdown
<!-- AUTO-GENERATED: Copy of AGENTS.md - do not edit directly -->
<!-- To update: copy content from AGENTS.md -->
```

**verification that accounts for platform differences**:

```bash
# check if file is symlink (works on all POSIX)
[ -L "CLAUDE.md" ] && echo "symlink" || echo "regular file"

# check symlink target portably
readlink CLAUDE.md 2>/dev/null || ls -la CLAUDE.md | awk '{print $NF}'
```

## concrete values

| value | meaning | source |
|-------|---------|--------|
| file threshold | 3+ files → needs AGENTS.md | heuristic: below this, parent docs suffice |
| staleness window | 30 days since last verify | heuristic: monthly audit cadence |
| quick audit budget | 2 min max | `references/audit-timing.md` |
| standard audit budget | 10 min max | `references/audit-timing.md` |
| count tolerance | ±0 (exact match required) | docs are contracts, not estimates |
| symlink target | always "AGENTS.md" | convention: relative symlink |

## tool integration

| tool | command | purpose |
|------|---------|---------|
| fd | `fd "^AGENTS\.md$" . --type f` | find documentation files |
| rg | `rg "export (function|const)" --type ts` | verify documented exports |
| readlink | `readlink CLAUDE.md` | verify symlink targets |
| git | `git log --since="7 days ago" --name-only` | detect changed directories |
| trails | `trails trail record` | audit history persistence |

### trails integration

persist audit results for trend analysis:

```bash
# record audit start
TRACE=$(trails trail record --agent claude --new-trace --action started \
  --task "agent-docs-audit: $PROJECT" --json -q | jq -r '.trace_id')

# record completion with findings
trails trail record --agent claude --trace-id $TRACE \
  --action completed --task "audited $COUNT files, $ISSUES issues found" \
  --confidence $CONFIDENCE --json -q
```

**trails enables**:
- tracking documentation drift over time
- correlating audit findings with code changes
- measuring documentation debt

### tool fallbacks

### fd fallback examples

```bash
# fd "^AGENTS\.md$" . --type f | grep -v node_modules
# fallback:
find . -name "AGENTS.md" -type f | grep -v node_modules | sort

# fd "^CLAUDE\.md$" . --type l
# fallback:
find . -name "CLAUDE.md" -type l | grep -v node_modules

# fd -e ts -e tsx . directory | wc -l
# fallback:
find directory -name "*.ts" -o -name "*.tsx" | wc -l

# fd -t d . --max-depth 3 | grep -v node_modules
# fallback:
find . -maxdepth 3 -type d | grep -v node_modules
```

**note**: `fd` is preferred for speed but all workflows should work with POSIX `find` + `grep`.

## workflow

### phase 1: discovery

```bash
# find all AGENTS.md files
fd "^AGENTS\.md$" . --type f | grep -v node_modules | sort

# find all CLAUDE.md files
fd "^CLAUDE\.md$" . --type f | grep -v node_modules | sort

# count totals
echo "AGENTS.md: $(fd '^AGENTS\.md$' . --type f | grep -v node_modules | wc -l | tr -d ' ')"
echo "CLAUDE.md: $(fd '^CLAUDE\.md$' . --type f | grep -v node_modules | wc -l | tr -d ' ')"
```

### phase 2: symlink verification

```bash
# check each CLAUDE.md is proper symlink
fd "^CLAUDE\.md$" . --type l --exec sh -c '
  target=$(readlink "$1")
  if [ "$target" = "AGENTS.md" ]; then
    echo "✓ $1 → AGENTS.md"
  else
    echo "✗ $1 → $target (should be AGENTS.md)"
  fi
' _ {}

# find CLAUDE.md regular files (should be symlinks)
fd "^CLAUDE\.md$" . --type f | grep -v node_modules | while read f; do
  echo "✗ $f is regular file, should be symlink"
done
```

### phase 3: file count verification

for each AGENTS.md that claims file counts:

```bash
# extract claimed count from docs
grep -E "^\d+ (files|components|modules)" path/to/AGENTS.md

# verify actual count
fd -e ts -e tsx . directory | wc -l

# separate source from tests
total=$(fd -e ts -e tsx . directory | wc -l | tr -d ' ')
tests=$(fd -e test.ts -e test.tsx -e spec.ts -e spec.tsx . directory | wc -l | tr -d ' ')
source=$((total - tests))
echo "Total: $total, Tests: $tests, Source: $source"
```

### phase 4: pattern verification

```bash
# verify documented exports exist
rg "export (function|const|class) FunctionName" directory --type ts

# verify documented types exist
rg "export (type|interface) TypeName" directory --type ts

# verify pattern usage
rg "patternName" directory --type ts --count
```

### phase 5: change detection

```bash
# files changed in last 7 days
git log --since="7 days ago" --name-only --pretty=format: | sort -u | grep -E '\.(ts|tsx)$'

# check if affected directories have up-to-date docs
for file in $(git log --since="7 days ago" --name-only --pretty=format: | sort -u | grep -E '\.(ts|tsx)$'); do
  dir=$(dirname "$file")
  if [ -f "$dir/AGENTS.md" ]; then
    echo "check: $dir/AGENTS.md (file changed: $file)"
  fi
done
```

### phase 6: missing documentation scan

```bash
# find directories with 3+ files but no AGENTS.md
for dir in $(fd -t d . --max-depth 3 | grep -v node_modules); do
  count=$(fd -e ts -e tsx . "$dir" -d 1 2>/dev/null | wc -l | tr -d ' ')
  if [ "$count" -ge 3 ] && [ ! -f "$dir/AGENTS.md" ]; then
    echo "missing: $dir ($count files)"
  fi
done
```

## output format

present findings in structured sections:

```markdown
## audit results: {scope}

### ✓ verified accurate
- `path/AGENTS.md`: all claims verified

### ⚠️ needs update
- `path/AGENTS.md`: claims 56 files, actually 54
- `path/AGENTS.md`: documents `buildFoo()` but not found

### ✗ missing documentation
- `dir/`: 4 files, no AGENTS.md

### 🔗 symlink issues
- `path/CLAUDE.md`: regular file, should be symlink
```

## documentation standards

### structure

| section | purpose | required |
|---------|---------|----------|
| purpose | what this directory does | yes |
| key components | main exports with descriptions | yes |
| patterns | recurring patterns to follow | if applicable |
| important | warnings, gotchas, footguns | if applicable |
| examples | concrete usage with correct imports | recommended |

### voice

- third-person for descriptions ("This directory contains...")
- imperative for instructions ("Use X for Y", "Call Z with...")
- direct warnings ("NEVER do X", "IMPORTANT: Y")

### verification checklist

- [ ] all file counts are exact
- [ ] all documented exports exist
- [ ] all examples use correct import paths
- [ ] all patterns are findable in code
- [ ] CLAUDE.md is symlink to AGENTS.md

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| estimated counts | "~50 files" misleads agents | use exact: `fd -e ts . dir \| wc -l` |
| documenting internals | agents don't need private details | focus on public API and patterns |
| stale examples | wrong imports cause errors | verify examples compile |
| missing warnings | agents hit footguns | add IMPORTANT sections for gotchas |
| CLAUDE.md as copy | diverges from AGENTS.md | always use symlink |
| undocumented patterns | agents reinvent or conflict | document recurring patterns |
| over-documentation | noise obscures signal | document only what agents need |
| no verification | drift accumulates | run audit after structural changes |

## output contract

when agent-docs-audit completes, produce:

```json
{
  "mode": "review",
  "status": "success | partial | blocked",
  "summary": "audited 12 AGENTS.md files, 3 need updates, 2 missing",
  "confidence": 8,
  "artifacts": [
    { "type": "finding", "path": "src/AGENTS.md", "issue": "count mismatch", "severity": "warn" },
    { "type": "finding", "path": "lib/CLAUDE.md", "issue": "regular file", "severity": "error" }
  ],
  "sources": {
    "prompts": [],
    "files_read": ["src/AGENTS.md", "lib/AGENTS.md"]
  },
  "verification": {
    "files_audited": 12,
    "issues_found": 5,
    "symlinks_valid": true
  }
}
```

## references

- [references/patterns.md](references/patterns.md) - documentation patterns and anti-patterns
- [references/verification-methods.md](references/verification-methods.md) - advanced verification techniques
- [references/audit-timing.md](references/audit-timing.md) - audit budget guidelines
