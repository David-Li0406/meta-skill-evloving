# CC-PAI Optimizer Skill (v2.1.5)

A Claude skill for reviewing and optimizing Personal AI Infrastructure (PAI) codebases as Claude Code evolves.

## Problem Solved

Keeping PAI systems up-to-date with Claude Code improvements is challenging because:
1. CC releases frequently (weekly/bi-weekly)
2. New features can significantly improve PAI workflows
3. 12-factor agent principles evolve with the ecosystem
4. Context engineering best practices continue to mature

This skill provides a systematic approach to track CC updates and apply them to PAI codebases.

## Trusted Sources for Claude Code Updates

### Primary Sources (Official - Check Weekly)

| Source | URL | Content |
|--------|-----|---------|
| **GitHub CHANGELOG** | https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md | Detailed version history |
| **GitHub Releases** | https://github.com/anthropics/claude-code/releases | Tagged releases with notes |
| **Anthropic Docs** | https://docs.anthropic.com/en/docs/claude-code | Official documentation |
| **NPM Package** | https://www.npmjs.com/package/@anthropic-ai/claude-code | Package versions |

### Secondary Sources (Community - Verify Against Official)

| Source | URL | Content |
|--------|-----|---------|
| marckrenn changelog | https://github.com/marckrenn/claude-code-changelog | System prompt history |
| ClaudeLog | https://claudelog.com/claude-code-changelog/ | Aggregated changelog |
| DeepWiki | https://deepwiki.com/anthropics/claude-code/ | Feature architecture docs |
| Discord | https://humanlayer.dev/discord | Community discussions |

### Related Resources

| Source | URL | Relevance |
|--------|-----|-----------|
| 12-Factor Agents | https://github.com/humanlayer/12-factor-agents | Agent design principles |
| Claude Agent SDK | https://docs.anthropic.com/en/docs/agent-sdk | Custom agent building |

## Skill Structure

```
cc-pai-optimiser/
├── SKILL.md                              # Main skill file
├── Readme.md                             # This file
├── references/
│   ├── cc-trusted-sources.md            # Trusted sources detail
│   └── 12-factor-checklist.md           # Compliance audit criteria
└── scripts/
    ├── cc-version-check.js              # Version compatibility checker
    └── analyse-pai.js                   # PAI analysis tool
```

## Usage

### Quick Version Check

```bash
# Check CC version compatibility with your PAI
cd ${PAI_DIR}/skills/cc-pai-optimiser
bun run scripts/cc-version-check.js ${PAI_PATH}
```

### Full PAI Analysis

```bash
# Run comprehensive PAI audit
cd ${PAI_DIR}/skills/cc-pai-optimiser
bun run scripts/analyse-pai.js ${PAI_DIR}/..
```

### Manual Workflow

1. **Gather CC Updates**
    - Check GitHub CHANGELOG for new features
    - Note version requirements for each feature

2. **Audit PAI Structure**
    - Run analysis scripts
    - Check 12-factor compliance

3. **Generate Upgrade Plan**
    - Prioritize by impact and effort
    - Create implementation snippets

## Key Claude Code Features to Track

### CC 2.1.x (Current - 2026)

| Feature | Min Version | PAI Impact |
|---------|-------------|------------|
| Model routing | 2.1.0 | Per-task model selection (haiku/sonnet/opus) |
| Skill invocation | 2.1.0 | Skill tool for user-defined skills |
| Background tasks | 2.1.0 | Async agent execution with run_in_background |
| Task resume | 2.1.0 | Resume agents via agent ID |
| Status line | 2.1.0 | Custom status line in settings.json |
| Enhanced hooks | 2.1.0 | Hooks in settings.json (replaces hooks.json) |
| WebSearch | 2.1.0 | Built-in web search capability |
| AskUserQuestion | 2.1.0 | Interactive questions with options |

### CC 2.0.x (Foundational)

| Feature | Min Version | PAI Impact |
|---------|-------------|------------|
| Subagents | 1.0.80 | Parallel task delegation |
| Checkpoints | 2.0.0 | Code state rollback with /rewind |
| Hooks | 1.0.85 | Event automation |
| Skills | 2.0.40 | Reusable capabilities in .claude/skills/ |
| Plan Mode | 2.0.50 | Structured execution |
| LSP | 2.0.74 | Code intelligence |
| Chrome Integration | 2.0.72 | Browser control |

## Analysis Modules

The PAI analyzer checks:

1. **Structure** - Directory layout (.claude/, context/, skills/, etc.)
2. **Context Management** - UFC patterns, file sizes, progressive disclosure
3. **Skills System** - SKILL.md format, context types (fork/same), invocability
4. **Hooks Configuration** - settings.json hooks, lifecycle events
5. **Agent Configuration** - Specialized agents, Factor 10 compliance
6. **Tool Integration** - MCP servers, tool documentation
7. **Workflow Patterns** - Commands, control flow, state management
8. **Delegation Patterns** - Multi-agent workflows, parallel execution

## 12-Factor Agent Principles for PAI

The skill audits against these factors (see `references/12-factor-checklist.md`):

1. **Natural Language to Tool Calls** - Schema definitions
2. **Own Your Prompts** - Version-controlled prompts
3. **Own Your Context Window** - UFC implementation ⭐
4. **Tools Are Structured Outputs** - JSON schemas
5. **Unify Execution State** - Centralized state
6. **Launch/Pause/Resume** - Checkpoint support
7. **Contact Humans with Tools** - HITL patterns
8. **Own Your Control Flow** - Custom logic ⭐
9. **Compact Errors** - Error summarization
10. **Small Focused Agents** - Single-purpose ⭐
11. **Trigger from Anywhere** - Multi-channel
12. **Stateless Reducer** - External state

⭐ = High-impact factors for PAI optimization

## Output Example

When running the skill, expect reports like:

```
╔══════════════════════════════════════════════════════════════╗
║              PAI OPTIMIZATION ANALYSIS                       ║
╚══════════════════════════════════════════════════════════════╝

📅 Generated: 2025-01-09T10:30:00Z
📁 PAI Path: /home/user/.claude
📊 Overall Score: 85/125 (68%)

Progress: [█████████████░░░░░░░] 68%

─── STRUCTURE (10/10) ───
  ✅ .claude exists
  ✅ .claude/context exists
  ✅ .claude/skills exists
  ✅ .claude/hooks exists

─── SKILLSSYSTEM (20/25) ───
  ✅ Skills directory exists
  📦 Found 16 skill(s)
  ✅ All skills have proper SKILL.md format
  ✅ Has fork-context skills (isolated execution)

─── HOOKSCONFIGURATION (20/20) ───
  ✅ Hooks configured in settings.json
  ✅ All recommended hook events configured
  ✅ Status line configured

─── RECOMMENDATIONS ───
📌 delegationPatterns:
   • Document parallel agent execution patterns
```

## Integration with Existing PAI

When using this skill to optimize an existing PAI:

1. **Preserve** - Don't break existing context loading (Layers 1-4)
2. **Enhance** - Add new CC features incrementally
3. **Validate** - Test context hydration after changes
4. **Document** - Update CLAUDE.md files with changes

## Installation

Installation is implicit, ~/.claude/skills is symlinked
