# audit timing guidelines

budget guidelines for different audit scopes.

## quick audit (< 2 min)

**when**: pre-commit sanity check, single directory

**checks**:
- file counts match documented values
- key exports exist (spot check 2-3)
- symlinks valid

**skip**:
- pattern usage counts
- example code verification
- missing documentation scan

## standard audit (2-10 min)

**when**: weekly health check, after refactoring

**checks**:
- all file counts
- all documented patterns exist
- all types/functions findable
- recent changes covered (7 day window)
- symlink integrity

**skip**:
- cross-reference accuracy
- example code execution
- deep pattern analysis

## deep audit (10+ min)

**when**: drift suspected, periodic comprehensive review

**checks**:
- everything in standard
- pattern usage counts
- cross-reference accuracy
- example code correctness (import paths work)
- missing documentation discovery
- staleness analysis (files changed but docs not)

## time allocation

| task | quick | standard | deep |
|------|-------|----------|------|
| discovery | 15s | 30s | 1min |
| symlink check | 15s | 30s | 1min |
| file counts | 30s | 2min | 3min |
| pattern verify | - | 3min | 5min |
| change detection | - | 2min | 3min |
| missing scan | - | - | 5min |
| reporting | 30s | 1min | 2min |
| **total** | ~1.5min | ~9min | ~20min |

## parallelization

for large codebases, run these in parallel:
- symlink verification
- file count verification
- pattern verification

```bash
# parallel execution example
{
  fd "^CLAUDE\.md$" . --type l --exec readlink {} &
  fd -e ts -e tsx . src | wc -l &
  rg "export function" src --type ts --count &
} | wait
```
