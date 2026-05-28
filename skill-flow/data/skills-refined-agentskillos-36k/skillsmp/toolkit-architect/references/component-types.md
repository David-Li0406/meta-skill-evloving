# Component Types

## Table of Contents

- [skill](#skill)
- [command](#command)
- [subagent](#subagent)
- [hook](#hook)
- [mcp](#mcp)
- [Component Type Selection Guide](#component-type-selection-guide)

## skill

**Self-sufficient building blocks** with progressive disclosure

**Knowledge Base**: `/skills-knowledge`
**Patterns**: Auto-discovery, autonomous workflows, progressive disclosure
**Files**: `.claude/skills/skill-name/SKILL.md`

**Structure**:
```
skills/skill-name/
├── SKILL.md              # Core skill definition
├── references/           # Supporting documentation
└── scripts/             # Execution scripts (optional)
```

**Key Features**:
- YAML frontmatter (name, description)
- Progressive disclosure (Tier 1/2/3)
- URL fetching sections
- Best practices enforcement
- Auto-discovery optimization

## command

**Minimal wrappers** with precise workflows

**Knowledge Base**: `/commands-knowledge`
**Patterns**: Dynamic context injection (!command, @file)
**Files**: `.claude/commands/command-name.md`

**Structure**:
```
.claude/commands/
├── command-name.md       # Command definition
└── scripts/             # Supporting scripts (optional)
```

**Key Features**:
- Markdown format
- Dynamic context injection
- Tool specification
- Workflow clarity
- User control

## subagent

**Specialized autonomous workers** for isolation/parallelism

**Knowledge Base**: `/subagents-knowledge`
**Patterns**: Context: fork, coordination patterns
**Files**: Custom agents or Task tool invocations

**Structure**:
```
agents/
└── agent-name.md        # Agent definition
```

**Key Features**:
- Context isolation
- Parallel execution
- State management
- Coordination patterns
- Specialized expertise

## hook

**Event-driven automation** for infrastructure integration

**Knowledge Base**: `/hooks-knowledge`
**Patterns**: Event handlers, validation, security
**Files**: `hooks/hooks.json` or inline in plugin.json

**Structure**:
```
hooks/
└── hooks.json           # Hook configuration
```

**Key Features**:
- Event type specification
- Validation logic
- Security checks
- Automatic execution
- Infrastructure integration

## mcp

**External service integration** via Model Context Protocol

**Knowledge Base**: `/mcp-knowledge`
**Patterns**: Tools, resources, prompts, transport
**Files**: `.mcp.json` or MCP server configurations

**Structure**:
```
mcp/
└── server-config.json   # MCP server configuration
```

**Key Features**:
- Protocol standards
- Transport mechanisms
- External tool integration
- Resource management
- Service connectivity

## Component Type Selection Guide

### Decision Matrix

| Need | Choose | Reason |
|------|--------|--------|
| Domain expertise | **Skill** | Self-sufficient, discoverable |
| User-controlled workflow | **Command** | Explicit invocation |
| Isolation/parallelism | **Subagent** | Separate context |
| Event automation | **Hook** | Infrastructure integration |
| External services | **MCP** | Protocol-based integration |

### Complexity Assessment

**Simple Task** → Skill (regular)
- Direct execution
- Clear success criteria
- Minimal user interaction

**Complex Workflow** → Skill (context: fork)
- Multiple stages
- High-volume output
- Noisy exploration
- Isolated processing

**Explicit Control** → Command
- User determines timing
- Multi-step approval
- Tool constraints
- Specific validation

**Rare/Advanced** → Subagent
- Isolation needed
- Parallel execution
- Context separation
- Specialized coordination
