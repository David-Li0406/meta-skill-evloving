---
name: cc-pai-optimiser
context: fork
description: Review and optimize PAI (Personal AI Infrastructure) codebases as Claude Code evolves. Use when analyzing PAI repositories against 12-factor agent principles, checking for Claude Code feature compatibility, auditing context management patterns, or generating upgrade recommendations. Triggers on requests involving PAI optimization, Claude Code feature adoption, agent architecture review, or context engineering improvements.
---

# CC-PAI Optimizer (v2.1.12)

Review and optimize PAI codebases by tracking Claude Code evolution and applying 12-factor agent principles.

## Core Workflow

### 1. Gather Latest Claude Code Features

Before any optimization, fetch current CC capabilities from trusted sources:

```bash
# Check current version
claude --version

# Trusted sources
CC_SOURCES=(
  "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md"
  "https://github.com/anthropics/claude-code/releases"
  "https://docs.anthropic.com/en/docs/claude-code"
  "https://github.com/marckrenn/claude-code-changelog/blob/main/cc-prompt.md"
)
```

Reference `references/cc-trusted-sources.md` for complete source list and update frequency recommendations.

### 2. Load PAI Repository

```bash
# Discover PAI structure
ls -la "$PAI_DIR/.claude/"
```

### 3. Run Analysis Pipeline

Execute analysis in this order:

1. **Structure Analysis** - Directory layout and required files
2. **Skills System Audit** - SKILL.md format, context types, invocability
3. **Hooks Configuration** - settings.json hooks, lifecycle events
4. **Context Engineering Audit** - UFC patterns, progressive disclosure
5. **Delegation Patterns** - Multi-agent workflows
6. **12-Factor Compliance** - Agent principles audit
7. **Upgrade Plan Generation** - Prioritized recommendations

## Analysis Modules

### Structure Analysis

Expected PAI v2.x structure:

```
.claude/
├── context/           # Context files (CLAUDE.md)
├── skills/            # Skill definitions (replaces rules/)
│   └── */SKILL.md    # Each skill with frontmatter
├── agents/            # Agent configurations
├── commands/          # Reusable workflows
├── hooks/             # Hook scripts
├── state/             # State persistence
└── settings.json      # CC configuration with hooks
```

### Skills System Analysis

Check for proper SKILL.md format:

```yaml
---
name: skill-name
context: fork|same
description: What this skill does
---
```

Key checks:
- All skills have SKILL.md with frontmatter
- `context: fork` for isolated execution (subagent)
- `context: same` for main conversation
- references/, scripts/, workflows/ subdirectories

### Hooks Configuration (CC 2.1.x)

Hooks are now in settings.json:

```json
{
  "hooks": {
    "PreToolUse": [...],
    "PostToolUse": [...],
    "SessionStart": [...],
    "SessionEnd": [...],
    "UserPromptSubmit": [...],
    "Stop": [...],
    "SubagentStop": [...]
  }
}
```

### Feature Gap Analysis

Compare PAI implementation against CC capabilities:

| CC Feature | Min Version | Check Location | Optimization Signal |
|------------|-------------|----------------|---------------------|
| Subagents | 1.0.80 | `.claude/agents/` | Missing parallel execution |
| Checkpoints | 2.0.0 | `/rewind` usage | No rollback safety |
| Hooks | 2.1.0 | `settings.json` | Missing automation |
| Skills | 2.0.40 | `.claude/skills/` | No reusable capabilities |
| Plan Mode | 2.0.50 | Commands | Missing planning phase |
| Model routing | 2.1.0 | Task tool usage | No per-task model selection |
| Status line | 2.1.0 | `settings.json` | No custom status |
| Context % | 2.1.6 | Status line | Not using native percentage |
| additionalContext | 2.1.9 | PreToolUse hooks | No context injection to model |
| plansDirectory | 2.1.9 | `settings.json` | Using default plans location |
| Session ID | 2.1.9 | Skills | No session tracking in skills |

### 12-Factor Compliance Check

Reference `references/12-factor-checklist.md` for complete audit criteria.

Key factors to validate:

1. **Factor 3 - Own Context Window**: Is context hydration explicit and controlled?
2. **Factor 8 - Own Control Flow**: Is agent loop logic in application code?
3. **Factor 10 - Small Focused Agents**: Are agents single-purpose?
4. **Factor 12 - Stateless Reducer**: Is state externalized?

## Output Format

Generate report as:

```markdown
# PAI Optimization Report

## Executive Summary
[1-2 sentence overall assessment]

## CC Feature Adoption
| Feature | Status | Priority | Effort |
|---------|--------|----------|--------|

## Skills System
[SKILL.md format compliance, context types]

## Hooks Configuration
[settings.json hooks audit]

## 12-Factor Compliance
[Factor-by-factor status]

## Context Engineering
[UFC audit results]

## Recommended Upgrades
1. [High Priority] ...
2. [Medium Priority] ...

## Implementation Snippets
[Ready-to-use code for top recommendations]
```

## Quick Commands

### Full Audit
```bash
cd ${PAI_DIR}/skills/cc-pai-optimiser
bun run scripts/analyse-pai.js ${PAI_DIR}/..
```

### Version Check
```bash
cd ${PAI_DIR}/skills/cc-pai-optimiser
bun run scripts/cc-version-check.js ${PAI_DIR}/..
```

## Version Tracking

Track CC versions against PAI compatibility:

```javascript
// Key CC 2.1.x features
const CC_2_1_FEATURES = {
  // 2.1.0
  modelRouting: "2.1.0",      // Per-task model selection
  skillInvocation: "2.1.0",   // Skill tool
  backgroundTasks: "2.1.0",   // run_in_background
  taskResume: "2.1.0",        // Resume via agent ID
  statusLine: "2.1.0",        // Custom status line
  settingsJsonHooks: "2.1.0", // Hooks in settings.json
  webSearch: "2.1.0",         // Built-in WebSearch
  askUserQuestion: "2.1.0",   // Interactive questions
  // 2.1.3
  mergedSkillsCommands: "2.1.3", // Unified slash commands and skills
  releaseChannelToggle: "2.1.3", // stable/latest in /config
  enhancedDoctor: "2.1.3",       // /doctor detects unreachable rules
  extendedHookTimeout: "2.1.3",  // Hook timeout: 60s → 10 min
  // 2.1.4
  disableBackgroundTasks: "2.1.4", // CLAUDE_CODE_DISABLE_BACKGROUND_TASKS env var
  // 2.1.5
  tmpDirOverride: "2.1.5",     // CLAUDE_CODE_TMPDIR env var
  // 2.1.6
  configSearch: "2.1.6",       // Search in /config command
  statsDateFiltering: "2.1.6", // /stats date range filtering
  nestedSkillDiscovery: "2.1.6", // Auto-discovery from nested .claude/skills
  contextWindowPercentage: "2.1.6", // used_percentage in status line input
  // 2.1.7
  turnDurationToggle: "2.1.7", // showTurnDuration setting
  permissionFeedback: "2.1.7", // Feedback on permission prompts
  mcpToolSearchAuto: "2.1.7",  // Auto-defer MCP tools >10% context
  // 2.1.9
  additionalContext: "2.1.9",  // PreToolUse hooks return context to model
  plansDirectory: "2.1.9",     // Custom plan file location
  sessionIdSubstitution: "2.1.9", // ${CLAUDE_SESSION_ID} in skills
  mcpAutoThreshold: "2.1.9",   // auto:N syntax for MCP tool threshold
  // 2.1.10
  // (no new features - bug fixes only)
  // 2.1.11
  mcpConnectionFix: "2.1.11",  // Fixed excessive HTTP/SSE MCP reconnection
  // 2.1.12
  messageRenderingFix: "2.1.12", // Fixed message rendering bug
};
```

See `scripts/cc-version-check.js` for automated compatibility checking.
