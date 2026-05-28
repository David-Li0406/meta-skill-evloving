---
name: swe-onboard-quick
version: 1.0.0
description: Fast feature setup without swarm analysis. Use for quick feature registration when full DAA analysis is not needed.
workflow:
  aware: true
  callable_from:
    - WF_ONBOARD
    - WF_START
  default_return: WF_START
  supports_standalone: true
  auto_transition: true
---

# Onboard Quick Skill

Fast feature registration without swarm analysis (~30 seconds).

## When to Use

- Small features or modules
- When swarm MCPs are unavailable
- Quick prototyping
- When full analysis is overkill

## Process

### Step 1: Basic Info Collection
```
Feature Key: [e.g., AUTH, API, UTILS]
Feature Name: [e.g., "Authentication Module"]
Root Path: [e.g., "src/auth/"]
```

### Step 2: Quick Detection
- Scan root path for file types
- Detect primary language from extensions
- Identify framework from config files (package.json, composer.json, etc.)

### Step 3: Minimal Memory Creation

Create `FEATURE_[KEY]` with:
- Name, type, language, framework
- Root path
- Basic layer detection (if obvious from directory structure)

**Skip**:
- Full DOM_* domain memories
- Full SYS_* system memories
- Detailed architecture analysis

### Step 4: Index Update
- Add feature to INDEX_FEATURES
- Link in ARCH_INDEX if exists

## Skill Return Format

```markdown
## Skill Return
- **Skill**: swe-onboard-quick
- **Status**: [success|needs_clarification]
- **Feature Key**: [KEY]
- **Memories Created**: FEATURE_[KEY]
- **Next Step Hint**: WF_START
```

## Exit

`> **Skill /swe-onboard-quick complete** - Feature [KEY] registered (quick mode)`

## Comparison with /swe-onboard-feature

| Aspect | swe-onboard-quick | swe-onboard-feature |
|--------|---------------|-----------------|
| Time | ~30 sec | 2-5 min |
| Swarm | No | Optional (10 agents) |
| DOM_* | No | Yes |
| SYS_* | No | Yes |
| Layers | Basic | Detailed |
| Best for | Small features | Large codebases |
