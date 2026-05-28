# Embedding Philosophy

## Core Principle: Complete Fidelity

**Embedded commands MUST maintain 100% feature parity with plugin commands.**

The `/cartographer:embed` command exports commands for plugin-free operation. These embedded versions should work identically to their plugin counterparts.

## Dynamic Generation

Embedded commands are **generated at runtime** from plugin source files. No separate template files are maintained - the plugin commands ARE the source of truth.

### Benefits of Dynamic Generation

1. **Single source of truth** - No templates to maintain separately
2. **Always in sync** - Embedding always reflects current plugin state
3. **Reduced maintenance** - ~21 fewer files to maintain
4. **Consistency guaranteed** - Transformation rules applied uniformly

## What Gets Transformed

Only these elements are transformed during embed:

| Pattern | Replacement | Example |
|---------|-------------|---------|
| `/cartographer:X` | `/X` | `/cartographer:chart` → `/chart` |
| `/navigator:X` | `/spec-X` | `/navigator:plan` → `/spec-plan` |
| `agents/review/X.md` | `agents/X.md` | Agent path flattening |

## What Does NOT Get Transformed

Everything else is copied verbatim:

- Workflow steps
- Validation logic
- Error handling
- Output formats
- Tool permissions
- Agent definitions (content unchanged, only paths adjusted)

## Embedded Structure

### Standalone Embedding (Default)

Commands are self-contained files that work without the plugin:

```
.claude/commands/
├── chart.md
├── rechart.md
├── health.md
├── explore.md
├── where.md
├── capture.md
├── spec-plan.md
├── spec-build.md
├── spec-review.md
└── agents/
    ├── surveyor.md
    ├── auditor.md
    ├── import-analyzer.md
    ├── pattern-enforcer.md
    ├── architecture-auditor.md
    ├── anti-pattern-detector.md
    ├── convention-checker.md
    └── atlas-validator.md
```

### Agent Export (`--agents`)

When `--agents` flag is used, agent definitions are exported to an `agents/` subdirectory. Commands reference these via relative paths.

## Why Full Fidelity Matters

1. **Reliability**: Embedded commands behave exactly like plugin commands
2. **Maintainability**: One source of truth - update source, re-embed
3. **Debugging**: Issues in embedded mode reproduce in plugin mode
4. **Trust**: Users know what they're getting

## Command Mapping

| Plugin Command | Embedded Command | Purpose |
|----------------|------------------|---------|
| `/cartographer:chart` | `/chart` | Generate atlas |
| `/cartographer:rechart` | `/rechart` | Update atlas |
| `/cartographer:health` | `/health` | Health check (drift + structure + quality) |
| `/cartographer:explore` | `/explore` | Deep domain analysis |
| `/cartographer:where` | `/where` | Quick path lookup |
| `/cartographer:capture` | `/capture` | Capture patterns |
| `/navigator:plan` | `/spec-plan` | Create implementation spec |
| `/navigator:build` | `/spec-build` | Execute spec |
| `/navigator:review` | `/spec-review` | Review implementation |

## Agent Mapping

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

## Validation

After embedding, verify:

1. All commands are present in output directory
2. All agent files are present (if `--agents` used)
3. Command references use embedded paths
4. Agent paths are flattened correctly
