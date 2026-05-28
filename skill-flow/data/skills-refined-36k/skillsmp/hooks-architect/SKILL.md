---
name: hooks-architect
description: "Configure and audit project guardrails in .claude/ configuration. Helps create component-scoped hooks in skill frontmatter or global hooks in .claude/hooks.json. Routes to hooks-knowledge for patterns and templates. Does not contain active hooks."
disable-model-invocation: true
---

## 🚨 MANDATORY: Read BEFORE Routing

**CRITICAL**: You MUST read and understand these URLs:

### Primary Documentation (MUST READ)
- **[MUST READ] Hooks Guide**: https://code.claude.com/docs/en/hooks
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **Content**: Event automation, hook types, configuration
  - **Cache**: 15 minutes minimum

- **[MUST READ] Project Configuration**: https://code.claude.com/docs/en/plugins
  - **Tool**: `mcp__simplewebfetch__simpleWebFetch`
  - **Content**: .claude/ structure, component organization
  - **Cache**: 15 minutes minimum

### ⚠️ BLOCKING RULES
- **DO NOT proceed** until you've fetched and reviewed Primary Documentation
- **MUST validate** all URLs are accessible before routing
- **REQUIRED** to understand project-scoped configuration before routing

---

# Hooks Architect

Project configuration router for creating and auditing guardrails in your `.claude/` directory. Helps scaffold hooks templates and validate security patterns.

## Core Philosophy

**Project-First Approach**:
- Creates guardrails in YOUR project, not in toolkit
- Prefers component-scoped hooks over global hooks
- Generates scripts in `.claude/scripts/` directory
- Routes to hooks-knowledge for detailed patterns
- Does NOT contain active hooks itself

## Actions

### add-guard
**Adds component-scoped guardrail** to a skill in your project

**Router Logic**:
1. Discover: List existing skills in `.claude/skills/`
2. Select: Which skill needs the guardrail
3. Determine: Event type (PreToolUse, Stop, etc.)
4. Generate: Hook configuration for skill frontmatter
5. Create: Validation script in `.claude/scripts/`
6. Inject: Hook into skill frontmatter

**Output Contract**:
```
## Guardrail Added: {script_name}

### Skill Modified
- Path: .claude/skills/{skill-name}/SKILL.md
- Event: {event-type}
- Script: .claude/scripts/{script-name}.sh

### Guardrail Type
- Blocking: Uses exit 2
- Validation: {purpose}
- Security: {level}

### Template Created
- Script location: .claude/scripts/{script-name}.sh
- Hook added to: skill frontmatter
```

### init-project-hooks
**Initializes global hooks** in your project's `.claude/hooks.json`

**Router Logic**:
1. Check: Does `.claude/` directory exist?
2. Create: `.claude/hooks.json` with template
3. Generate: Common guardrail scripts in `.claude/scripts/`
4. Configure: Basic PreToolUse validation
5. Document: What each guardrail does

**Output Contract**:
```
## Project Hooks Initialized

### Created Files
- .claude/hooks.json (global configuration)
- .claude/scripts/guard-paths.sh (path safety)
- .claude/scripts/guard-commands.sh (command validation)

### Hooks Configured
- PreToolUse: Write|Edit → guard-paths.sh
- PreToolUse: Bash → guard-commands.sh

### Next Steps
1. Review .claude/scripts/*.sh scripts
2. Customize patterns for your project
3. Test guardrails with dangerous operations
```

### audit-safety
**Audits security** of hooks in your project

**Router Logic**:
1. Scan: Find all hooks in `.claude/hooks.json`
2. Scan: Find component-scoped hooks in `.claude/skills/*/SKILL.md`
3. Check: Security patterns (exit 2, input validation)
4. Validate: Scripts exist in `.claude/scripts/`
5. Test: Run security test suite

**Output Contract**:
```
## Security Audit Report

### Hooks Found
- Global hooks: {count}
- Component-scoped hooks: {count}
- Total scripts: {count}

### Security Assessment
- Path safety: {score}/10
- Command validation: {score}/10
- Input sanitization: {score}/10
- Exit code usage: {score}/10

### Issues Found
- {count} critical issues
- {count} warnings
- {count} recommendations

### Recommendations
1. {recommendation-1}
2. {recommendation-2}
```

## Hook Types

**Session Hooks**:
- SessionStart - Initialize session state
- SessionEnd - Cleanup resources

**Tool Hooks**:
- PreToolUse - Validate before execution
- PostToolUse - Process results

**Permission Hooks**:
- PermissionRequest - Handle permission prompts
- UserPromptSubmit - Process user submissions

**Agent Hooks**:
- SubagentStop - Handle subagent completion
- Stop - Handle session stop events

**System Hooks**:
- Notification - Handle system notifications
- PreCompact - Pre-context compact
- Setup - Hook system initialization

**Validation Hooks**:
- PreWrite - Validate file operations
- PreEdit - Validate modifications

**Infrastructure Hooks**:
- MCP configuration
- LSP setup
- Environment preparation

## Implementation Guidance

**For detailed implementation patterns**: Load: hooks-knowledge

**Security Best Practices**:
- Input validation and sanitization
- Event pattern matching safety
- Error handling and recovery
- Performance impact monitoring

### Session Persistence Protocol

**Purpose**: Memory persistence for plugin development workflow

**State File**: `.claude/TOOLKIT_STATE.md`

**Use When**:
- Creating hooks for session state persistence
- Implementing SessionStart/Stop/PreCompact hooks
- Extracting plugin development decisions from transcripts

**Implementation**: Load: hooks-knowledge → references/session-persistence.md

## Routing Criteria

**Direct scaffolding (add-guard)** when:
- Adding guardrail to existing skill
- Creating component-scoped hook
- Generating validation script

**Scaffold project (init-project-hooks)** when:
- Setting up global guardrails for project
- Creating initial .claude/hooks.json
- Generating common security scripts

**Load: hooks-knowledge** when:
- Need detailed patterns (command-hooks.md, prompt-hooks.md)
- Need security patterns (security-patterns.md)
- Need lifecycle guidance (lifecycle.md)
- Need comprehensive examples
- Need troubleshooting help
