# Reference Documentation Index

Guide to all reference documentation in this skill.

## Quick Navigation

### 📘 Start Here

**[COMPONENTS.md](COMPONENTS.md)** - ⭐ **Recommended starting point**

Complete templates for all component types with:
- Strict and flexible template styles
- Real-world input/output examples
- Validation checklists for each component type

### 📖 Component-Specific Guides

Once you understand the basics from COMPONENTS.md, dive deeper:

- **[COMMANDS.md](COMMANDS.md)** - Advanced command patterns, argument handling, error strategies
- **[AGENTS.md](AGENTS.md)** - Agent types, color coding, tool selection, system prompts
- **[SKILLS.md](SKILLS.md)** - Progressive disclosure, organization patterns, content guidelines
- **[HOOKS.md](HOOKS.md)** - All 9 hook event types, event-specific patterns, performance

### 🏗️ Architecture & Integration

- **[PATTERNS.md](PATTERNS.md)** - Common plugin architecture patterns (Command+Agent, Skill+Command, etc.)
- **[MCP.md](MCP.md)** - MCP server integration (SSE, STDIO, HTTP, WebSocket)
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Debug guide for common issues

---

## Which Reference Should I Use?

### Creating Your First Component?

1. **[COMPONENTS.md](COMPONENTS.md)** - Get the template
2. Implement your component
3. Use the validation checklist
4. **Need more detail?** → Jump to component-specific guide below

### Need Advanced Patterns?

- **Commands** → [COMMANDS.md](COMMANDS.md)
  - Complex argument handling
  - Command + Agent pattern
  - Error handling strategies
  - Confirmation workflows

- **Agents** → [AGENTS.md](AGENTS.md)
  - Color coding (blue/green/purple/etc.)
  - Tool selection guide
  - Phased workflow design
  - Agent types (analysis, refactoring, testing, docs)

- **Skills** → [SKILLS.md](SKILLS.md)
  - Progressive disclosure (keep SKILL.md lean)
  - Organization patterns (by domain, complexity, variant)
  - Token optimization strategies
  - Content guidelines (what to include/exclude)

- **Hooks** → [HOOKS.md](HOOKS.md)
  - All 9 hook events explained
  - Event-specific patterns
  - Side effects documentation
  - Performance considerations

### Designing Plugin Architecture?

**[PATTERNS.md](PATTERNS.md)** - Complete patterns library:
- Command + Agent (complex tasks)
- Skill + Command (knowledge invocation)
- Hook + Validation (automatic enforcement)
- Multi-component plugins
- Configuration patterns
- Progressive disclosure

### Integrating External Services?

**[MCP.md](MCP.md)**:
- Server types: SSE, STDIO, HTTP, WebSocket
- Configuration examples
- Security best practices
- Testing strategies

### Debugging Issues?

**[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**:
- Plugin not loading
- Command/agent/hook not working
- YAML errors
- Performance issues
- Quick diagnostic checklist

---

## Recommended Reading Order

### First-Time Plugin Developer

1. **[COMPONENTS.md](COMPONENTS.md)** - Learn template structure
2. Create your first component using the templates
3. **[PATTERNS.md](PATTERNS.md)** - Understand common patterns
4. Component-specific guides when you need more depth

### Experienced Developer

1. **[COMPONENTS.md](COMPONENTS.md)** - Quick template reference
2. Jump to specific component guides:
   - Commands → [COMMANDS.md](COMMANDS.md)
   - Agents → [AGENTS.md](AGENTS.md)
   - Skills → [SKILLS.md](SKILLS.md)
   - Hooks → [HOOKS.md](HOOKS.md)
3. **[PATTERNS.md](PATTERNS.md)** - Architecture patterns

### Advanced Integration

1. **[COMPONENTS.md](COMPONENTS.md)** - Template reference
2. **[PATTERNS.md](PATTERNS.md)** - Architecture patterns
3. **[MCP.md](MCP.md)** - External integrations
4. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Debug when needed

---

## Document Relationships

```
SKILL.md (main guide)
    │
    ├── COMPONENTS.md (templates) ← START HERE
    │       ├── Uses examples from COMMANDS.md
    │       ├── Uses examples from AGENTS.md
    │       ├── Uses examples from SKILLS.md
    │       └── Uses examples from HOOKS.md
    │
    ├── PATTERNS.md (architecture)
    │   └── References all component types
    │
    ├── MCP.md (integration)
    └── TROUBLESHOOTING.md (debugging)
        └── Covers all components
```

---

## File Sizes

- **COMPONENTS.md**: ~13KB - Complete templates (strict/flexible)
- **COMMANDS.md**: ~4KB - Command-specific guide
- **AGENTS.md**: ~6KB - Agent-specific guide
- **SKILLS.md**: ~7KB - Skill-specific guide
- **HOOKS.md**: ~10KB - Hook-specific guide
- **PATTERNS.md**: ~10KB - Architecture patterns
- **MCP.md**: ~5KB - MCP integration
- **TROUBLESHOOTING.md**: ~7KB - Debug guide

---

## Tips

- **Quick templates?** → COMPONENTS.md
- **Best practices?** → Specific component guide
- **Architecture help?** → PATTERNS.md
- **Debugging issues?** → TROUBLESHOOTING.md
- **External APIs?** → MCP.md

All files use progressive disclosure - load only what you need!
