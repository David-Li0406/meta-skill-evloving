# Essential Plugins Reference

This reference lists recommended plugins for Claude Code with their context window impact.

## Core Principle

> **Context Window Budget**: Plugins add tools just like MCPs.
> Keep total tools (MCPs + plugins) under 80.

---

## Quick Reference Table

| Plugin | Tools | Purpose | Priority |
|--------|-------|---------|----------|
| hookify | ~3 | Create hooks conversationally | High |
| typescript-lsp | ~8 | TypeScript intelligence | Medium (TS projects) |
| pyright-lsp | ~8 | Python type checking | Medium (Python projects) |
| mgrep | ~2 | Better search | Low |

---

## High Priority Plugins

### hookify - Conversational Hook Creation

**Purpose**: Create Claude Code hooks through conversation instead of editing JSON.

**Context Impact**: ~3 tools (low)

**When to use**: Any project - makes hook configuration much easier.

**Example usage**:
```
User: /hookify
Claude: What kind of hook would you like to create?
User: Format my TypeScript files after editing
Claude: [Creates PostToolUse hook for biome/prettier]
```

**Why recommended**: Hooks are powerful but JSON configuration is error-prone. This plugin dramatically simplifies the process.

---

## Medium Priority Plugins

### typescript-lsp - TypeScript Language Server

**Purpose**: Provides TypeScript intelligence to Claude - better completions, type information, error detection.

**Context Impact**: ~8 tools (medium)

**When to use**: TypeScript projects where type accuracy is critical.

**Benefits**:
- Real-time type checking
- Better code suggestions
- Import assistance
- Refactoring support

**Trade-off**: Adds tools to context. Only enable for TypeScript-heavy work.

---

### pyright-lsp - Python Type Checking

**Purpose**: Provides Python type intelligence to Claude.

**Context Impact**: ~8 tools (medium)

**When to use**: Python projects with type hints.

**Benefits**:
- Type error detection
- Better completions
- Import resolution

**Trade-off**: Similar to typescript-lsp, adds context overhead.

---

## Low Priority Plugins

### mgrep - Enhanced Search

**Purpose**: More powerful search than built-in grep.

**Context Impact**: ~2 tools (low)

**When to use**: Large codebases where search performance matters.

**Alternative**: Built-in Grep tool works well for most cases.

---

## Context Window Impact Analysis

### Minimal Setup (Recommended)

```
Plugins: hookify (~3)
Total plugin tools: 3
```

### TypeScript Project

```
Plugins: hookify (~3) + typescript-lsp (~8)
Total plugin tools: 11
```

### Python Project

```
Plugins: hookify (~3) + pyright-lsp (~8)
Total plugin tools: 11
```

### Full Setup (Caution)

```
Plugins: hookify (~3) + typescript-lsp (~8) + mgrep (~2)
Total plugin tools: 13
```

---

## Installation Patterns

### Check Current Plugins

```bash
# List installed plugins (method varies by setup)
claude plugins list
```

### Install Plugin

```bash
# General pattern
claude plugins install <plugin-name>
```

### Disable Plugin (Keep Installed)

Similar to MCPs, you can disable without uninstalling.

---

## Decision Framework

### Should I Install This Plugin?

Ask these questions:

1. **Do I need this functionality daily?**
   - Yes → Consider installing
   - Occasionally → Use alternative or enable temporarily

2. **Is there a built-in alternative?**
   - Yes → Prefer built-in (no context cost)
   - No → Consider plugin

3. **What's my current tool count?**
   - Under 60 → Safe to add
   - 60-80 → Consider carefully
   - Over 80 → Remove something first

### Plugin Priority by Project Type

**Frontend (TypeScript)**:
1. hookify (essential)
2. typescript-lsp (if complex types)

**Backend (Python)**:
1. hookify (essential)
2. pyright-lsp (if using type hints)

**General**:
1. hookify (essential)
2. Others as needed

---

## Combining with MCPs

### Safe Combination

```
MCPs:
- context7 (~5)
- shadcn (~3)

Plugins:
- hookify (~3)
- typescript-lsp (~8)

Total: ~19 + base(25) = ~44 tools ✓
```

### Risky Combination

```
MCPs:
- context7 (~5)
- shadcn (~3)
- github (~20)
- supabase (~15)

Plugins:
- hookify (~3)
- typescript-lsp (~8)
- pyright-lsp (~8)
- mgrep (~2)

Total: ~64 + base(25) = ~89 tools ⚠
```

---

## Alternatives to Plugins

Before installing a plugin, consider:

| Need | Plugin | Alternative |
|------|--------|-------------|
| Create hooks | hookify | Edit settings.json manually |
| TypeScript help | typescript-lsp | Read tsconfig, run tsc |
| Python types | pyright-lsp | Run mypy/pyright CLI |
| Better search | mgrep | Built-in Grep tool |

---

## Recommendations by Experience Level

### Beginner
- hookify only
- Keep it simple, learn the basics

### Intermediate
- hookify
- LSP for your primary language

### Advanced
- Minimal plugins
- Prefer CLI tools
- Enable plugins temporarily when needed

---

## Plugin Maintenance

### Regular Audit

Monthly, review your plugins:

1. List all installed plugins
2. Check usage frequency
3. Disable unused plugins
4. Update frequently used plugins

### Temporary Enable Pattern

For occasionally-needed plugins:

1. Install but keep disabled
2. Enable when needed: `claude plugins enable <name>`
3. Disable after: `claude plugins disable <name>`

This preserves context window for daily work while keeping capabilities available.
