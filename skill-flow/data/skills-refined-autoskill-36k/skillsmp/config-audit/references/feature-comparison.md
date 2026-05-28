# Claude Code vs Cursor: Feature Comparison

This document provides a detailed comparison of features between Claude Code and Cursor IDE to help understand how they differ and where gaps exist.

## Feature Overview

### Claude Code Features

1. **Slash Commands** - User-invoked text commands
2. **Skills** - Model-invoked modular capabilities
3. **Agents (Sub-agents)** - Specialized AI assistants
4. **Hooks** - Event-triggered shell commands
5. **CLAUDE.md** - Project/user-level instructions
6. **Plugins** - Distribution mechanism for bundled resources

### Cursor Features

1. **Cursor Rules (.mdc)** - AI instruction files with attachment control
2. **Commands** - Text-based prompts (not executable)
3. **.cursorrules** - Deprecated project instruction format
4. **AGENT.md** - Agent-specific instructions (if used)

## Detailed Feature Comparison

### Commands

#### Claude Code Commands

**Location**: `.claude/commands/` (project) or `~/.claude/commands/` (user)

**Format**: Markdown files with YAML frontmatter

**Invocation**: User-invoked via `/command-name`

**Capabilities**:

- Execute with tool permissions via `allowed-tools` field
- Dynamic parameter substitution (`$ARGUMENTS`, `$1`, `$2`, etc.)
- Bash command execution (`` !`command` ``)
- File reference inclusion (`@file/path`)
- Model selection override

**Example frontmatter**:

```yaml
---
description: Commit staged changes
allowed-tools: Bash(git add:*), Bash(git commit:*)
argument-hint: [message]
model: claude-3-5-haiku-20241022
---
```

**Key characteristics**:

- Single file per command
- Can execute code via tool permissions
- Lightweight and easy to create
- Best for frequently-used prompts

#### Cursor Commands

**Location**: Custom directory (e.g., `cursor/commands/`)

**Format**: Markdown files (text only)

**Invocation**: Unknown - appears to be text-based prompt templates

**Capabilities**:

- Text-based instructions only
- No tool execution capabilities
- No dynamic parameter substitution

**Key characteristics**:

- Pure text prompts
- Cannot execute code
- Less powerful than Claude Code commands
- May be invoked differently in Cursor (documentation unclear)

**Equivalent**: Cursor commands are closer to simple prompt templates, while Claude Code commands can be executable with tool permissions.

### Skills vs Cursor Rules

#### Claude Code Skills

**Location**: `.claude/skills/` (project) or `~/.claude/skills/` (user)

**Format**: Directory containing SKILL.md + optional resources

**Invocation**: Model-invoked (Claude decides when to use based on context)

**Structure**:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description)
│   └── Markdown instructions
├── references/ (optional)
│   └── Documentation loaded into context as needed
└── assets/ (optional)
    └── Files used in output (templates, images, etc.)
```

**Capabilities**:

- Progressive loading (metadata → SKILL.md → resources as needed)
- Helper commands (TypeScript code integrated into `ai` CLI)
- Reference documentation (loaded on demand)
- Asset files (templates, boilerplate, etc.)
- Auto-activation based on description match

**Key characteristics**:

- Comprehensive, structured workflows
- Can include executable helper commands
- Token-efficient through progressive loading
- Best for complex, multi-step processes

#### Cursor Rules

**Location**: `.cursor/rules/` (typically in subdirectories)

**Format**: Single `.mdc` file with YAML frontmatter

**Invocation**: Four modes:

1. **Always** - Always included (`alwaysApply: true`)
2. **Auto Attached** - Included when globs match file patterns
3. **Agent Requested** - AI decides based on description
4. **Manual** - User invokes with `@ruleName`

**Frontmatter**:

```yaml
---
description: Brief explanation of rule's purpose
globs: ["**/*.ts", "**/*.tsx"] # or without brackets
alwaysApply: false
---
```

**Capabilities**:

- Glob pattern matching for auto-attachment
- Four different attachment modes
- Single-file structure (recommended <500 lines)
- File reference with `@filename` syntax

**Key characteristics**:

- Single file (must decompose if >500 lines)
- Sophisticated attachment control via globs
- No executable components (pure instructions)
- Token budget aware through attachment modes

**Equivalent**: Both provide AI instructions, but:

- Skills are directory-based with multiple files vs single .mdc file
- Skills can include executable helpers vs pure instructions
- Skills use description-based matching vs Cursor's multi-mode attachment
- Skills support progressive loading vs Rules' all-or-nothing loading

### Agents

#### Claude Code Agents (Sub-agents)

**Location**: `.claude/agents/` (project) or `~/.claude/agents/` (user)

**Format**: Markdown file with YAML frontmatter

**Invocation**:

- Auto-delegated by Claude based on task
- Manually invoked with explicit instruction

**Frontmatter**:

```yaml
---
name: identifier-name
description: When and why to use this agent
tools: optional,tool,list # omit for all tools
model: sonnet # or 'inherit'
---
System prompt defining the agent's role and approach
```

**Capabilities**:

- Own context window (separate from main conversation)
- Custom system prompt
- Configurable tool access
- Focused expertise for specific domains

**Key characteristics**:

- Prevents context clutter in main conversation
- Specialized for specific tasks
- Can have restricted tool permissions
- Independent operation

#### Cursor Equivalent

**No direct equivalent** - Cursor doesn't have a sub-agent system.

**Closest analog**: Agent Requested rules that activate based on task description, but these don't have:

- Separate context windows
- Independent tool permissions
- Custom system prompts

### Hooks

#### Claude Code Hooks

**Location**: Configured in settings (`.claude/settings.json`)

**Format**: Shell commands triggered by events

**Events**:

- Tool call events
- User prompt submit
- Other workflow events

**Capabilities**:

- Execute shell commands on events
- Can provide feedback to Claude
- Enable workflow automation

**Key characteristics**:

- Event-driven automation
- Shell-based execution
- Can block or modify tool calls

#### Cursor Equivalent

**No direct equivalent** - Cursor doesn't have an event-driven hook system.

### Project Instructions

#### Claude Code: CLAUDE.md

**Location**:

- `.claude/CLAUDE.md` (project)
- `~/.claude/CLAUDE.md` (user)

**Format**: Markdown with optional XML tags for sections

**Capabilities**:

- Project-level instructions always in context
- User-level instructions merged with project instructions
- XML tag-based merging for conflict-free updates
- Can reference other files with `@filename`

**Key characteristics**:

- Always loaded in context
- Hierarchical (user + project)
- XML tags enable safe merging

#### Cursor: .cursorrules

**Location**: `.cursorrules` (project root)

**Format**: Plain text

**Status**: **Deprecated** in favor of Cursor Rules with `alwaysApply: true`

**Modern equivalent**: Create `.cursor/rules/project-standards.mdc` with:

```yaml
---
description: Core project standards
alwaysApply: true
---
```

**Key characteristics**:

- Deprecated format
- Being replaced by Always rules
- Less sophisticated than CLAUDE.md

### Distribution

#### Claude Code: Plugins

**Location**: Distributed via plugin system

**Capabilities**:

- Bundle commands, skills, agents, resources
- Easy installation and updates
- Namespace isolation
- Shareable across projects

**Key characteristics**:

- First-class distribution mechanism
- Plugin registry
- Version management

#### Cursor: No Plugin System

**Distribution**: Manual copying of files

**Method**:

- Copy `.cursor/` directory to projects
- Share via git
- No official distribution mechanism

**Key characteristics**:

- Manual file management
- No versioning
- No centralized registry

## Functional Equivalencies

### Similar Capabilities

| Functionality              | Claude Code              | Cursor                   |
| -------------------------- | ------------------------ | ------------------------ |
| Always-loaded instructions | CLAUDE.md                | Always rules             |
| Context-aware instructions | Skills (auto-invoked)    | Agent Requested rules    |
| File-pattern instructions  | N/A                      | Auto Attached rules      |
| On-demand instructions     | Skills (via description) | Manual rules (@ruleName) |
| Shareable configs          | Plugins                  | Manual file sharing      |

### Unique to Claude Code

1. **Executable Commands** - Commands with tool permissions
2. **Sub-agents** - Separate context windows
3. **Hooks** - Event-driven automation
4. **Helper Commands** - TypeScript code in skills
5. **Progressive Loading** - Skills load resources as needed
6. **Plugin System** - Official distribution mechanism

### Unique to Cursor

1. **Glob Pattern Matching** - Auto-attach based on file patterns
2. **Multi-mode Attachment** - Always/Auto/Agent/Manual
3. **@filename References** - Direct file references in rules
4. **.mdc Format** - Standardized rule format

## When to Use Each Feature

### Use Claude Code Commands When:

- Need to execute code (git, build, tests)
- Want user-invoked shortcuts
- Require dynamic parameters
- Need tool permission control

### Use Cursor Commands When:

- Need simple prompt templates
- Working exclusively in Cursor
- Don't need code execution

### Use Claude Code Skills When:

- Building complex workflows
- Need bundled resources (templates, docs)
- Want helper commands for repetitive tasks
- Need progressive resource loading

### Use Cursor Rules When:

- Want file-pattern-based activation
- Need always-loaded standards
- Working exclusively in Cursor
- Want lightweight single-file structure

### Use Claude Code Agents When:

- Need specialized expertise
- Want separate context windows
- Require task delegation
- Need custom tool permissions

### Use Claude Code Hooks When:

- Need event-driven automation
- Want to intercept tool calls
- Building custom workflows

## Gaps and Opportunities

### Claude Code Missing:

- **File pattern matching** - Cursor's globs feature for auto-attachment
- **Manual invocation syntax** - Cursor's @ruleName pattern

### Cursor Missing:

- **Executable commands** - Can't run code from commands
- **Sub-agents** - No separate context windows
- **Hooks** - No event-driven automation
- **Helper commands** - No executable utilities in rules
- **Plugin system** - No official distribution
- **Progressive loading** - Rules load entirely or not at all

## Migration Considerations

### Claude Code → Cursor

**Commands**:

- Convert to text-only prompts
- Remove `allowed-tools` (not supported)
- Create as .md files

**Skills**:

- Convert SKILL.md to .mdc rule
- Extract core instructions only (no helper commands)
- Choose appropriate rule type (Always/Auto/Agent/Manual)
- Split if >500 lines

**Agents**:

- Convert to Agent Requested rules
- No separate context (merged into main)
- No custom tool permissions

### Cursor → Claude Code

**Always Rules**:

- Add to CLAUDE.md
- Or create as skill if complex

**Auto Attached Rules**:

- Create as skill with description mentioning file types
- No direct glob equivalent

**Manual Rules**:

- Convert to slash command
- Keep invocation pattern

**Agent Requested Rules**:

- Convert to skill with clear description
- Add helper commands if needed
