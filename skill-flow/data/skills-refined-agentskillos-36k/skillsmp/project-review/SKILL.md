---
name: project-review
description: This skill should be used for reviewing current project against mature project patterns, tool capabilities, and org standards. Triggers include "review this project", "what am I missing", "align with standards", "check tool usage", "compare to arbor/koto", or proactively at session start in unfamiliar projects. Surfaces gaps in patterns, underutilized tools, and org standard deviations.
---

# project-review

context-aware project analysis against mature patterns, tool capabilities, and org standards. surfaces gaps proactively.

## philosophy

> "tell me what I'm missing before I miss it"

| principle | application |
|-----------|-------------|
| proactive surfacing | don't wait for user to ask - surface gaps |
| context-aware | different projects need different patterns |
| actionable gaps | every gap has a specific recommendation |
| non-blocking | audit informs, doesn't block work |
| cumulative | learnings feed back to improve standards |

## modes

| mode | trigger | behavior |
|------|---------|----------|
| **patterns** | "what patterns am I missing" | compare to arbor/koto/kumori |
| **tools** | "am I using tools well" | check outline/layer/etc. usage |
| **standards** | "align with my standards" | check AGENTS.md/CLAUDE.md adherence |
| **full** | "audit this project" | all of the above |

## when to use

| use | skip |
|-----|------|
| starting in unfamiliar repo | deep in a focused fix |
| "audit this project" | user asked for implementation |
| before major refactor | single-file tweak |
| comparing against arbor/koto/kumori | greenfield spike |
| checking tool usage or standards | time-boxed hotfix |

## decision tree: mode selection

```
What audit mode?
├── User asks about patterns/mature projects?
│   └── mode: patterns
├── User asks about tools/CLI usage?
│   └── mode: tools
├── User asks about standards/principles?
│   └── mode: standards
├── Starting work in unfamiliar project?
│   └── mode: full (proactive)
├── Explicit "audit" or "what am I missing"?
│   └── mode: full
└── Default
    └── mode: full
```

## decision tree: audit scope

```
How deep should the audit go?
├── Fresh repo or major refactor?
│   └── full (patterns + tools + standards)
├── User asked "what am I missing"?
│   └── full
├── Tool usage question only?
│   └── tools-only
├── Standards compliance question?
│   └── standards-only
└── Time-boxed (<15 min)?
    └── quick audit (top 3 gaps only)
```

## concrete values (from references)

| metric | value | source |
|--------|-------|--------|
| outline token savings | 10-50x | `references/tool-capabilities.md` |
| exploration-first order | layer → outline → Read | `references/org-standards.md` |
| passing standards score | 7+/10 | `references/org-standards.md` |
| audit scoring scale | 0-2 per standard | `references/org-standards.md` |
| test naming | `*.test.ts`, `*.integration.test.ts`, `*.e2e.ts` | `references/mature-patterns.md` |

## workflow

### phase 1: project detection

```bash
# detect project type and context
PROJECT_TYPE="unknown"
PROJECT_NAME=$(basename $(pwd))

# convex stack
[ -d "convex" ] && PROJECT_TYPE="convex"

# xcode
{ ls -d *.xcodeproj *.xcworkspace 2>/dev/null | head -1 >/dev/null; } && PROJECT_TYPE="xcode"

# node
[ -f "package.json" ] && PROJECT_TYPE="node"

# turborepo
[ -f "turbo.json" ] && PROJECT_TYPE="turborepo"

# known project detection
case "$(pwd)" in
  */arbor/*) KNOWN_PROJECT="arbor" ;;
  */koto/*) KNOWN_PROJECT="koto" ;;
  */kumori/*) KNOWN_PROJECT="kumori" ;;
  */sine/*) KNOWN_PROJECT="sine" ;;
  */webs/*) KNOWN_PROJECT="webs" ;;
  */zo/*) KNOWN_PROJECT="zo" ;;
  *) KNOWN_PROJECT="unknown" ;;
esac
```

### phase 2: pattern audit

compare against mature project patterns from `~/.loop/patterns/`:

```bash
# check if patterns exist
if [ -d ~/.loop/patterns ]; then
  echo "=== Pattern Audit ==="

  # file structure comparison
  if [ -f ~/.loop/patterns/file-structure.md ]; then
    echo "Checking file structure against mature patterns..."
    # compare current structure to patterns
  fi

  # test patterns comparison
  if [ -f ~/.loop/patterns/test-patterns.md ]; then
    CURRENT_TEST_COUNT=$(find . -name "*.test.*" -o -name "*.spec.*" | wc -l)
    echo "Test files found: $CURRENT_TEST_COUNT"
    # compare to mature project test coverage
  fi

  # convex schema comparison (if convex project)
  if [ -f ~/.loop/patterns/convex-schema.md ] && [ -d "convex" ]; then
    echo "Checking convex schema patterns..."
  fi
else
  echo "No patterns cached. Run loop's pattern-discovery first."
  echo "  cd ~/Developer/skills/skills/loop/scripts"
  echo "  ./discover-projects.sh && ./extract-patterns.sh"
fi
```

**pattern gaps to check:**

| pattern | source | check |
|---------|--------|-------|
| test colocation | arbor | `*.test.ts` next to source? |
| convex validators | arbor | using zod/valibot? |
| turborepo structure | arbor | apps/packages split? |
| env handling | koto | `.env.example` exists? |
| error boundaries | kumori | error handling in place? |

### phase 3: tool audit

check usage of available CLI tools:

```bash
echo "=== Tool Audit ==="

# outline usage
if command -v outline &>/dev/null; then
  echo "outline: available"

  # check if using advanced features
  # --callers, --callees, --unused, --diff, --pr
  echo "  Features to use:"
  echo "  - outline --callers=X → trace who calls function"
  echo "  - outline --unused → find dead code"
  echo "  - outline --diff=HEAD~1 → structural changes"
  echo "  - outline --pr=123 → PR review"
else
  echo "outline: NOT INSTALLED (recommend: cargo install outline)"
fi

# layer usage
if command -v layer &>/dev/null; then
  echo "layer: available"
  echo "  Features to use:"
  echo "  - layer --check-cycles → detect dependency cycles"
  echo "  - layer --focus=pkg → analyze specific package"
else
  echo "layer: NOT INSTALLED"
fi

# verify usage
if command -v verify &>/dev/null; then
  echo "verify: available"
else
  echo "verify: NOT INSTALLED (use for unified test running)"
fi

# linear usage
if command -v linear &>/dev/null; then
  echo "linear: available"
  # check workspace config
else
  echo "linear: NOT INSTALLED"
fi
```

**tool capability matrix:**

| tool | feature | use case | check |
|------|---------|----------|-------|
| outline | --callers | trace function usage | before refactoring |
| outline | --unused | find dead code | cleanup sessions |
| outline | --diff | structural changes | PR review |
| outline | --pr | PR analysis | before merge |
| layer | --check-cycles | dependency health | architecture review |
| layer | --focus | package analysis | understanding deps |
| verify | --changed | test affected files | fast CI |

### phase 4: standards audit

check alignment with org standards from AGENTS.md:

```bash
echo "=== Standards Audit ==="

# exploration-first principle
echo "Checking: exploration-first (layer → outline → Read)"
# verify recent git history shows exploration before changes

# commit message style
echo "Checking: commit message style"
# verify commits follow pattern: feat(ISSUE-123): description

# test-first development
echo "Checking: TDD patterns"
# check if tests exist and were written before implementation

# voice/style
echo "Checking: voice (lowercase, no corporate speak)"
# verify docs follow style guide
```

**standards checklist:**

| standard | source | verification |
|----------|--------|--------------|
| exploration-first | AGENTS.md | layer/outline in recent commands |
| issue references | AGENTS.md | commits reference LINEAR issues |
| TDD workflow | testing.md | test files exist before impl |
| lowercase voice | AGENTS.md | docs avoid corporate speak |
| backtick paths | AGENTS.md | file paths in backticks |

### phase 5: gap report

generate actionable gap report:

```markdown
# Project Audit: {project_name}
**Date:** YYYY-MM-DD
**Type:** {project_type}

## Pattern Gaps

| gap | recommendation | effort |
|-----|----------------|--------|
| missing test colocation | move tests next to source | medium |
| no convex validators | add zod schemas | low |

## Tool Gaps

| tool | feature | recommendation |
|------|---------|----------------|
| outline | --unused not used | run: `outline --unused src/` |
| layer | --check-cycles | run: `layer --check-cycles` |

## Standards Gaps

| standard | deviation | fix |
|----------|-----------|-----|
| commit messages | missing issue refs | use `feat(ARB-123):` format |
| exploration-first | reading before exploring | use layer → outline → Read |

## Audit Score

Score: X/10 (pass >= 7)

## Telemetry Snapshot

| metric | value |
|--------|-------|
| tests found | N |
| outline features used | callers, diff |
| layer checks run | check-cycles |
| verify usage | changed, summary |
| commit refs | 8/10 with issue ids |

## Recommendations

### Immediate (do now)
1. {specific action}

### Soon (this session)
1. {specific action}

### Backlog (future)
1. {specific action}
```

## audit scoring

score standards using 0-2 per dimension (max 10):

| standard | 0 | 1 | 2 |
|----------|---|---|---|
| exploration-first | never | sometimes | always |
| commit messages | no refs | some refs | all refs |
| TDD | no tests | tests exist | tests first |
| voice | corporate | mixed | correct |
| issue integration | none | partial | full |

**pass:** 7+/10. below 7 becomes an immediate gap.

## telemetry snapshot

capture light-weight metrics for longitudinal comparison:

| metric | example |
|--------|---------|
| tests found | 42 |
| outline features used | callers, diff |
| layer checks run | check-cycles |
| verify usage | changed, summary |
| commit refs | 8/10 with issue ids |

## integration with loop

add to loop Phase 0 (optional, non-blocking):

```bash
# in loop bootstrap, after project detection
if [ "$SKIP_AUDIT" != "true" ]; then
  echo "=== Quick Project Audit ==="
  # run lightweight pattern check
  # run tool availability check
  # surface top 3 gaps only (don't overwhelm)
fi
```

## proactive triggers

surface audit automatically when:

| trigger | action |
|---------|--------|
| session start in unfamiliar project | run full audit, surface top 3 |
| before major refactor | run pattern audit |
| before PR | run tool audit (suggest outline --pr) |
| loop Phase 0 | run quick audit |

## tool integration

| tool | command | purpose |
|------|---------|---------|
| layer | `layer .`, `layer --check-cycles` | architecture understanding, cycle detection |
| outline | `outline --unused`, `outline --callers=X` | dead code, usage tracing |
| verify | `verify --format=summary` | test coverage verification |
| git | `git log --oneline -10` | commit history, trajectory |
| linear | `linear issue list` | work tracking context |
| trails | `trails trail record` | audit history persistence |

### trails integration

persist audit results for trend analysis:

```bash
# record audit completion
trails trail record --agent claude --action completed \
  --task "project-review: $PROJECT - score $SCORE/10" \
  --confidence $SCORE --json -q
```

**trails enables**:
- tracking audit scores over time
- correlating gaps with code changes
- measuring standard compliance trends

## references

- [references/tool-capabilities.md](references/tool-capabilities.md) - full tool feature matrix
- [references/mature-patterns.md](references/mature-patterns.md) - patterns from arbor/koto/kumori
- [references/org-standards.md](references/org-standards.md) - standards from AGENTS.md
- `~/.loop/patterns/` - cached patterns from pattern-discovery

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| blocking on audit | delays work | audit is informational only |
| overwhelming gaps | paralyzes action | surface top 3, prioritize |
| stale patterns | outdated comparison | refresh patterns monthly |
| ignoring tool features | underutilizing capabilities | check tool --help periodically |
| skipping standards check | drift from org principles | include in session start |
