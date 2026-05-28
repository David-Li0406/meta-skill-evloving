---
name: update-docs
description: Use when implementing new features, changing behavior, or modifying CLI options. Documents changes in README, related docs, and --help output. Determines appropriate documentation scope based on change type.
allowed-tools: [Read, Edit, Grep, Glob, Bash]
---

# Documentation Update Skill

## Purpose

Ensure that user-facing changes are properly documented across all relevant locations. This skill determines the appropriate scope of documentation updates based on the type and impact of the change.

## Trigger Conditions

Use this skill when:
- Adding new CLI options or commands
- Changing existing behavior or API
- Adding new features or capabilities
- Modifying configuration options
- Making breaking changes

## Documentation Locations

| Location | Purpose | Update Criteria |
|----------|---------|-----------------|
| `README.md` | Quick reference | Major features, CLI syntax changes |
| `README.ja.md` | Japanese reference | Same as README.md |
| `--help` output | CLI help | All CLI option changes |
| `agents/README.md` | Agent-specific docs | Agent behavior changes |
| `docs/` | Detailed guides | Complex features, tutorials |
| `CLAUDE.md` | Development guidelines | Internal workflow changes |

## Decision Matrix

### What to Document Where

```
Change Type → Documentation Scope
├── New CLI option
│   ├── --help (REQUIRED): Option description, usage
│   ├── README: If commonly used or important
│   └── docs/: If needs detailed explanation
├── New feature
│   ├── README: Brief mention with example
│   ├── docs/: Detailed usage guide (if complex)
│   └── --help: If has CLI interface
├── Behavior change
│   ├── README: Update existing description
│   ├── CHANGELOG: Note the change
│   └── Migration guide: If breaking
├── Config option
│   ├── Schema file: Type and description
│   ├── README/docs: Usage example
│   └── --help: If CLI-related
└── Internal change
    └── CLAUDE.md or agents/CLAUDE.md: If affects development
```

## Process

### Step 1: Identify Change Scope

```bash
# List recently changed files
git diff --name-only HEAD~1

# Or check staged changes
git diff --cached --name-only
```

### Step 2: Categorize the Change

Ask yourself:
1. Does this add a new user-facing feature? → README, --help
2. Does this change existing behavior? → README, CHANGELOG
3. Does this add/modify CLI options? → --help (REQUIRED)
4. Does this affect agent execution? → agents/README.md
5. Is this a breaking change? → Migration guide in docs/

### Step 3: Update Documentation

#### For CLI Options (src/cli/*)

1. Check `--help` output:
```bash
deno run -A mod.ts --help
deno run -A mod.ts <command> --help
```

2. Update help strings in code if needed

3. Update README if option is commonly used:
```markdown
| Option | Short | Description |
|--------|-------|-------------|
| `--new-option` | `-n` | New option description |
```

#### For Features

1. Add brief description in README.md
2. Create or update detailed guide in docs/ if complex
3. Add code examples

#### For Config/Schema Changes

1. Update JSON Schema description
2. Add example in README or relevant docs
3. Update type definitions documentation if public API

### Step 4: Verify Consistency

```bash
# Check README versions are in sync
diff README.md README.ja.md | head -50

# Verify --help matches documentation
deno run -A mod.ts --help 2>&1 | grep -i "<feature>"
```

## Documentation Guidelines

### Style

- **Concise**: One sentence per feature in README
- **Example-first**: Show usage before explaining
- **Searchable**: Include keywords users would search for

### Format

```markdown
## Feature Name

Brief description in one sentence.

**Example:**
\`\`\`bash
command --option value
\`\`\`
```

### What NOT to Document

- Internal implementation details (unless in CLAUDE.md)
- Temporary workarounds
- Debug-only options
- Deprecated features (mark as deprecated instead)

## Quick Reference

```
New CLI option:
  1. Update help string in code
  2. Test: deno run -A mod.ts --help
  3. Add to README if user-facing

New feature:
  1. Add 1-2 sentences in README
  2. Include usage example
  3. Create docs/ page if complex

Behavior change:
  1. Update existing README section
  2. Add to CHANGELOG (separate skill)
  3. Migration guide if breaking

Agent change:
  1. Update agents/README.md
  2. Update agent.json schema docs
  3. Update builder guide if config-related
```

## Examples

### Example 1: New CLI Option

Change: Added `--verbose` flag

Documentation:
- `--help`: "Enable verbose output for debugging"
- README.md: Add to Key Options table
- CHANGELOG: "Added: `--verbose` flag for debugging"

### Example 2: New Agent Feature

Change: Added `askUserAutoResponse` config

Documentation:
- agents/README.md: Add to behavior config section
- agent.schema.json: Add description (already in schema)
- CHANGELOG: "Added: Autonomous execution mode with `askUserAutoResponse`"

### Example 3: Internal Change

Change: Refactored prompt resolver

Documentation:
- CLAUDE.md or agents/CLAUDE.md: Note architectural change (if affects development)
- No user-facing docs needed
