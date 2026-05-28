---
model: sonnet
allowed-tools: Read, Write, Glob, Bash(test:*), Bash(mkdir:*), Bash(find:*), AskUserQuestion
argument-hint: [--cartographer | --navigator | --agents | --all] [--output <dir>]
description: Export commands for plugin-free operation (dynamic generation)
---

## Context

Arguments: `/cartographer:embed [OPTIONS]`
- **--cartographer** - Export cartographer commands only
- **--navigator** - Export navigator commands only
- **--agents** - Include agent definitions (required for chart/review to work standalone)
- **--all** - Export everything (cartographer + navigator + agents)
- **--output <dir>** - Custom output directory (default: `.claude/commands/`)
- **(empty)** - Same as --all

Current directory: !`pwd`

## Dynamic Generation

This command generates embedded commands **at runtime** from the plugin source files. No separate template files are maintained - the plugin commands ARE the source of truth.

### Transformation Rules

When embedding, apply these transformations:

| Pattern | Replacement | Example |
|---------|-------------|---------|
| `/cartographer:X` | `/X` | `/cartographer:chart` → `/chart` |
| `/navigator:X` | `/spec-X` | `/navigator:plan` → `/spec-plan` |
| `agents/X.md` | `agents/X.md` | (unchanged, relative paths work) |
| `Run \`/cartographer:` | `Run \`/` | Error message updates |

### Command Mapping

| Plugin Command | Embedded Name | Model |
|----------------|---------------|-------|
| `/cartographer:chart` | `/chart` | sonnet |
| `/cartographer:rechart` | `/rechart` | sonnet |
| `/cartographer:health` | `/health` | sonnet |
| `/cartographer:explore` | `/explore` | sonnet |
| `/cartographer:where` | `/where` | haiku |
| `/cartographer:capture` | `/capture` | haiku |
| `/navigator:plan` | `/spec-plan` | sonnet |
| `/navigator:build` | `/spec-build` | sonnet |
| `/navigator:review` | `/spec-review` | sonnet |

### Agent Mapping

| Plugin Agent | Embedded Path |
|--------------|---------------|
| `agents/surveyor.md` | `agents/surveyor.md` |
| `agents/auditor.md` | `agents/auditor.md` |
| `agents/import-analyzer.md` | `agents/import-analyzer.md` |
| `agents/review/pattern-enforcer.md` | `agents/pattern-enforcer.md` |
| `agents/review/architecture-auditor.md` | `agents/architecture-auditor.md` |
| `agents/review/anti-pattern-detector.md` | `agents/anti-pattern-detector.md` |
| `agents/review/convention-checker.md` | `agents/convention-checker.md` |
| `agents/review/atlas-validator.md` | `agents/atlas-validator.md` |

## Workflow

### 1. Discover Plugin Source

Locate the cartographer plugin source. Search in order:

```
~/.claude/plugins/*/cartographer/
~/.claude/plugins/marketplaces/*/cartographer/
.claude/plugins/*/cartographer/
```

Use Glob to find `commands/cartographer/*.md` files. Store path as `{plugin_dir}`.

**If not found:**
```
❌ Could not locate cartographer plugin source.

Searched:
- ~/.claude/plugins/*/cartographer/
- ~/.claude/plugins/marketplaces/*/cartographer/
- .claude/plugins/*/cartographer/

Ensure the cartographer plugin is installed.
```

### 2. Check Output Directory

```bash
test -d "{output_dir}" && echo "EXISTS" || echo "NOT_FOUND"
```

**If exists with conflicts, use AskUserQuestion:**
- Overwrite all
- Skip existing
- Choose different directory
- Abort

### 3. Create Output Directory

```bash
mkdir -p {output_dir}
mkdir -p {output_dir}/agents  # if --agents or --all
```

### 4. Export Cartographer Commands (if enabled)

For each command in `commands/cartographer/`:

1. **Read** source file content
2. **Transform** command references:
   - Replace `/cartographer:chart` with `/chart`
   - Replace `/cartographer:rechart` with `/rechart`
   - Replace `/cartographer:health` with `/health`
   - Replace `/cartographer:explore` with `/explore`
   - Replace `/cartographer:where` with `/where`
   - Replace `/cartographer:capture` with `/capture`
   - Replace `/cartographer:orient` with `/orient`
   - Replace `/cartographer:embed` with `/embed`
   - Replace `/cartographer:help` with `/help`
3. **Transform** navigator references:
   - Replace `/navigator:plan` with `/spec-plan`
   - Replace `/navigator:build` with `/spec-build`
   - Replace `/navigator:review` with `/spec-review`
4. **Write** to output directory with embedded name

**File naming:**
- `chart.md` → `chart.md`
- `rechart.md` → `rechart.md`
- `health.md` → `health.md`
- `explore.md` → `explore.md`
- `where.md` → `where.md`
- `capture.md` → `capture.md`

### 5. Export Navigator Commands (if enabled)

For each command in `commands/navigator/`:

1. **Read** source file content
2. **Apply same transformations** as cartographer commands
3. **Write** to output directory with `spec-` prefix

**File naming:**
- `plan.md` → `spec-plan.md`
- `build.md` → `spec-build.md`
- `review.md` → `spec-review.md`

### 6. Export Agents (if --agents or --all)

For each agent file:

1. **Read** source agent file
2. **Transform** any plugin command references
3. **Flatten** review agents (remove `review/` subdirectory)
4. **Write** to `{output_dir}/agents/`

**Agent flattening:**
- `agents/surveyor.md` → `agents/surveyor.md`
- `agents/auditor.md` → `agents/auditor.md`
- `agents/import-analyzer.md` → `agents/import-analyzer.md`
- `agents/review/pattern-enforcer.md` → `agents/pattern-enforcer.md`
- `agents/review/architecture-auditor.md` → `agents/architecture-auditor.md`
- `agents/review/anti-pattern-detector.md` → `agents/anti-pattern-detector.md`
- `agents/review/convention-checker.md` → `agents/convention-checker.md`
- `agents/review/atlas-validator.md` → `agents/atlas-validator.md`

**Update agent paths in commands:**
- `agents/review/X.md` → `agents/X.md`

### 7. Report Results

```markdown
## Commands Embedded

**Output:** `{output_dir}`
**Source:** `{plugin_dir}`

### Cartographer Commands
| Command | Purpose |
|---------|---------|
| `/chart` | Generate atlas (initial) |
| `/rechart` | Update atlas (regeneration) |
| `/health` | Check atlas health (drift + structure + quality) |
| `/explore` | Deep domain analysis |
| `/where` | Quick path lookup |
| `/capture` | Capture new patterns |

### Navigator Commands
| Command | Purpose |
|---------|---------|
| `/spec-plan` | Create implementation spec |
| `/spec-build` | Execute spec |
| `/spec-review` | Review implementation |

{IF agents exported:}
### Agent Definitions
Exported to `{output_dir}/agents/`:
| Agent | Purpose |
|-------|---------|
| `surveyor.md` | Codebase analysis |
| `auditor.md` | Drift detection |
| `import-analyzer.md` | Import pattern analysis |
| `atlas-validator.md` | Atlas structure validation |
| `pattern-enforcer.md` | Pattern compliance |
| `architecture-auditor.md` | Layer boundaries |
| `anti-pattern-detector.md` | Anti-pattern detection |
| `convention-checker.md` | Naming conventions |

### Transformation Applied
- Plugin command references updated for standalone use
- Agent paths flattened (review/ subdirectory removed)
- All links resolve to embedded files

**Next steps:**
- Commands are ready to use without the plugin
- Re-run `/cartographer:embed` to update from plugin changes
```

## Transformation Implementation

### Text Replacement Function

For each file content, apply replacements in this order (order matters for overlapping patterns):

```
1. /cartographer:calibrate-parallel → /calibrate-parallel  # (deprecated, skip)
2. /cartographer:calibrate → /calibrate  # (deprecated, skip)
3. /cartographer:validate → /validate  # (deprecated, skip)
4. /cartographer:review → /atlas-review  # (deprecated, skip)
5. /cartographer:chart → /chart
6. /cartographer:rechart → /rechart
7. /cartographer:health → /health
8. /cartographer:explore → /explore
9. /cartographer:where → /where
10. /cartographer:capture → /capture
11. /cartographer:orient → /orient
12. /cartographer:embed → /embed
13. /cartographer:help → /help
14. /navigator:iterate → /spec-iterate  # (deprecated, skip)
15. /navigator:plan → /spec-plan
16. /navigator:build → /spec-build
17. /navigator:review → /spec-review
18. agents/review/ → agents/  # Flatten agent paths
```

### Commands to Embed

**Cartographer (6 commands):**
- chart.md
- rechart.md
- health.md
- explore.md
- where.md
- capture.md

**Navigator (3 commands):**
- plan.md
- build.md
- review.md

**Agents (8 agents):**
- surveyor.md
- auditor.md
- import-analyzer.md
- pattern-enforcer.md (from review/)
- architecture-auditor.md (from review/)
- anti-pattern-detector.md (from review/)
- convention-checker.md (from review/)
- atlas-validator.md (from review/)

## Error Handling

| Error | Action |
|-------|--------|
| Plugin not found | Report search paths, suggest reinstall |
| Permission denied | Report error, suggest different path |
| Partial export | Report what succeeded, what failed |
| Source file missing | Skip with warning, continue with others |

## Responsibilities

**YOU (handler):**
- Locate plugin source directory
- Read source command and agent files
- Apply text transformations
- Write transformed files to output
- Report results

**You generate embedded commands dynamically. No separate templates to maintain.**
