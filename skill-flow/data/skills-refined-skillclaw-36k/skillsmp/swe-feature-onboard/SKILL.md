---
name: swe-feature-onboard
version: 2.0.0
description: Feature onboarding wizard with optional quick mode
workflow:
  aware: true
  callable_from:
    - WF_ONBOARD
    - WF_START
  default_return: WF_START
  supports_standalone: true
  auto_transition: true
args:
  - name: key
    description: Feature key (optional, will prompt if not provided)
  - name: quick
    description: Skip swarm analysis, minimal memory creation
    type: boolean
    default: false
---

## ⚠️ WORKFLOW INITIALIZATION

**If starting a new session**, first read workflow initialization:
```
mcp__plugin_swe_serena__read_memory("WF_INIT")
```
Follow WF_INIT instructions before executing this skill.

---

# /swe-feature-onboard [KEY] [--quick]

Interactive wizard for registering features in the workflow system.

## Usage

```bash
/swe-feature-onboard              # Full interactive wizard
/swe-feature-onboard MYAPP        # Start with key pre-filled
/swe-feature-onboard MYAPP --quick # Quick mode (30 sec, minimal)
```

## Quick Mode vs Full Mode

| Aspect | Quick Mode | Full Mode |
|--------|------------|-----------|
| Time | ~30 sec | 2-5 min |
| Swarm analysis | No | Optional (10 agents) |
| DOM_* memories | No | Yes (if domains found) |
| SYS_* memories | No | Yes (if systems found) |
| Layer detection | Basic | Detailed |
| Best for | Small features, prototyping | Large codebases |

---

## Stage 1: Basic Info

Ask the user (skip if provided via args):

```
What feature are you onboarding?

1. **Feature Key**: Short identifier used in memory names
   Examples: BACKEND, AUTH, BLOCKS, THEME_DISTRICT

2. **Feature Name**: Human-readable name
   Examples: "Backend API", "Authentication Module"

3. **Root Path(s)**: Where is the code?
   Examples: "src/", "wp-content/themes/district/"
```

**Validation:**
- Key: UPPERCASE, underscores allowed, 2-20 chars
- Path: Must exist in project

---

## Stage 2: Tech Stack

```
What technology does this feature use?

1. **Type**: web_app | library | api | cli | cms | wordpress_theme | wordpress_plugin
2. **Primary Language**: php | typescript | python | go | rust | etc.
3. **Framework** (optional): react | nextjs | laravel | django | wordpress | etc.
```

**Auto-detection:** Scan root path for:
- `package.json` → Node/TypeScript
- `composer.json` → PHP
- `Cargo.toml` → Rust
- `go.mod` → Go
- `style.css` with `Theme Name:` → WordPress theme

---

## Stage 3: Analysis Mode

**Skip in quick mode** - go directly to Stage 5.

```
How should I analyze the codebase?

[A] Full DAA Swarm Analysis (Recommended for large codebases)
    - 10 specialized agents analyze in parallel
    - Creates detailed DOM_*, SYS_* memories
    - Time: 2-5 minutes

[B] Quick Scan
    - Basic directory structure
    - Primary layer detection
    - Time: ~30 seconds

[C] Manual Configuration
    - You describe the architecture
    - I create memories from your input
```

### If [A] Full DAA Swarm:

```javascript
mcp__ruv-swarm__daa_init({ enableLearning: true })

mcp__ruv-swarm__task_orchestrate({
  task: "Analyze feature architecture",
  agents: [
    "config-analyzer",    // Parse config files
    "architecture-mapper", // Detect layers
    "pattern-detector",   // Find conventions
    "domain-extractor",   // Extract domains
    "system-finder",      // Identify systems
    "test-analyzer",      // Test patterns
    "import-tracer",      // Dependency graph
    "convention-learner", // Style detection
    "file-indexer",       // File inventory
    "synthesizer"         // Compile results
  ],
  context: { featureKey: "[KEY]", rootPath: "[PATH]" }
})
```

---

## Stage 4: Architecture Confirmation

**Skip in quick mode.**

Present detected architecture for confirmation:

```
I detected the following architecture for [FEATURE_NAME]:

**Layers:**
| Layer | Purpose | Directory |
|-------|---------|-----------|
| Presentation | Views/Templates | templates/ |
| Business | Controllers/Services | src/controllers/ |
| Data | Models/Repositories | src/models/ |

**Data Flow:**
Request → Controller → Service → Repository → Database

**Dependencies:**
- Internal: [other features this depends on]
- External: [packages/libraries]

Is this correct? [Y/n]
```

If user says no, gather corrections manually.

---

## Stage 5: Memory Creation

### Create FEATURE_[KEY].md

```markdown
# FEATURE_[KEY] - [Name]

## Feature Overview

| Property | Value |
|----------|-------|
| **Name** | [Feature Name] |
| **Key** | [KEY] |
| **Type** | [type] |
| **Language** | [language] |
| **Framework** | [framework or "none"] |

## Scope Definition

### Primary Directories

| Directory | Purpose |
|-----------|---------|
| [dir] | [purpose] |

## Architecture Layers

[ASCII diagram or table of layers]

## Key Files

| File | Purpose |
|------|---------|
| [file] | [purpose] |

## Related Memories

| Memory | Content |
|--------|---------|
| DOM_[KEY]_* | Domain behaviors |
| SYS_[KEY]_* | System references |
| INDEX_[KEY]_* | Indexes |

## Testing

| Suite | File | Focus |
|-------|------|-------|
| [suite] | [file] | [focus] |
```

### Create via Serena:

```javascript
mcp__plugin_swe_serena__write_memory("FEATURE_[KEY]", "<content>")
```

### Additional memories (full mode only):

If domains detected:
```javascript
mcp__plugin_swe_serena__write_memory("DOM_[KEY]_[DOMAIN]", "<content>")
```

If systems detected:
```javascript
mcp__plugin_swe_serena__write_memory("SYS_[KEY]_[SYSTEM]", "<content>")
```

---

## Stage 6: Index Update

Update INDEX_FEATURES.md:

```javascript
mcp__plugin_swe_serena__edit_memory(
  "INDEX_FEATURES",
  "## Registered Features",
  "## Registered Features\n\n| [KEY] | [Name] | [Type] | [Language] | Active |",
  "literal"
)
```

---

## Skill Return

```markdown
## Skill Return
- **Skill**: swe-feature-onboard
- **Status**: success
- **Feature Key**: [KEY]
- **Mode**: [full|quick]
- **Memories Created**: FEATURE_[KEY], [DOM_*, SYS_* if applicable]
- **Next Step Hint**: WF_START
```

---

## Exit

```
> **Skill /swe-feature-onboard complete** - Feature [KEY] registered
```

---

## Troubleshooting

### Swarm MCP unavailable
Fall back to quick mode or manual configuration.

### Path doesn't exist
```bash
ls -la [path]
```
Ask user to correct.

### INDEX_FEATURES.md missing
Create it first:
```javascript
mcp__plugin_swe_serena__write_memory("INDEX_FEATURES", "# INDEX_FEATURES\n\n## Registered Features\n\n| Key | Name | Type | Language | Status |\n|-----|------|------|----------|--------|\n")
```
