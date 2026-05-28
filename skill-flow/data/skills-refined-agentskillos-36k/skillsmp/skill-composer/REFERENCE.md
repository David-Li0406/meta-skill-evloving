# Skill Maintainer Reference

Technical specifications and field requirements for Claude Code Skills.

## YAML Frontmatter Specification

### Required Fields

```yaml
---
name: "skill-name"
description: "What it does and when to use it"
---
```

### Field Requirements

| Field | Type | Constraints | Example |
|-------|------|-------------|---------|
| `name` | string | Lowercase letters, numbers, hyphens only. Max 64 characters. No spaces or underscores. | `"commit-helper"` |
| `description` | string | Max 1024 characters. MUST include what skill does AND when to use it. | `"Generate commit messages. Use when committing or asked for commit help."` |

### Optional Fields

```yaml
---
name: "skill-name"
description: "Description here"
allowed-tools: Read, Grep, Glob
---
```

| Field | Type | Purpose | Example |
|-------|------|---------|---------|
| `allowed-tools` | comma-separated list | Restricts which tools Claude can use when skill is active | `Read, Grep, Glob` |

## Available Tools for Restriction

When using `allowed-tools`, you can specify any combination of:

- **Read** - Read files from filesystem
- **Write** - Write new files
- **Edit** - Edit existing files
- **Bash** - Execute shell commands
- **Grep** - Search file contents with patterns
- **Glob** - Find files by pattern matching
- **WebFetch** - Fetch content from URLs
- **WebSearch** - Search the web
- **Task** - Launch specialized sub-agents
- **TodoWrite** - Manage task lists
- **Skill** - Load other skills
- **SlashCommand** - Execute slash commands
- **AskUserQuestion** - Prompt user for input

### Common Tool Restriction Patterns

**Read-only analysis**:
```yaml
allowed-tools: Read, Grep, Glob
```
Use for: Code review, security audits, documentation analysis

**Research only**:
```yaml
allowed-tools: Read, WebFetch, WebSearch, Grep, Glob
```
Use for: Information gathering, documentation lookup

**Safe file operations**:
```yaml
allowed-tools: Read, Write, Bash
```
Use for: File generation, report creation (no destructive edits)

**Full access** (default):
```yaml
# Omit allowed-tools field
```
Use for: Complex workflows requiring multiple tools

## Directory Structure Patterns

### Minimal Skill (Single File)

```
skill-name/
└── SKILL.md
```

All instructions in SKILL.md. No supporting files.

### Simple Skill with Reference

```
skill-name/
├── SKILL.md
└── REFERENCE.md
```

SKILL.md contains workflow. REFERENCE.md contains technical details/API docs.

### Complex Skill with Scripts

```
skill-name/
├── SKILL.md
├── REFERENCE.md
├── EXAMPLES.md
└── scripts/
    ├── helper.py
    └── validate.sh
```

Multiple supporting files. Scripts for utilities. Progressive disclosure.

### Full-Featured Skill

```
skill-name/
├── SKILL.md
├── REFERENCE.md
├── EXAMPLES.md
├── scripts/
│   ├── process.py
│   └── validate.sh
└── templates/
    ├── config.json
    └── output.txt
```

Maximum organization. Templates for file generation.

## Supporting File Naming Conventions

Claude Code recognizes these common patterns:

- `REFERENCE.md` - Technical specifications, API documentation
- `EXAMPLES.md` - Code samples, usage patterns
- `scripts/` - Executable utilities (Python, Bash, etc.)
- `templates/` - File templates for generation

Other markdown files work but these are conventional.

## Progressive Disclosure Behavior

Claude loads files **on-demand** based on context:

1. **Always loads**: SKILL.md (required starting point)
2. **Loads when relevant**: Supporting files mentioned or contextually needed
3. **Doesn't load**: Files not referenced or relevant to current task

**Example**:
```
pdf-processing/
├── SKILL.md       # Always loaded
├── FORMS.md       # Loaded only when dealing with forms
└── REFERENCE.md   # Loaded only when API details needed
```

This keeps context efficient while supporting complex capabilities.

## File Path Conventions

### In SKILL.md

Reference supporting files with relative paths:

```markdown
For detailed API reference, see [REFERENCE.md](REFERENCE.md).
For examples, see [EXAMPLES.md](EXAMPLES.md).
```

Reference scripts:

```markdown
Run the validation script:
```bash
python scripts/validate.py
```
```

### In Scripts

Always use **forward slashes** (Unix-style):

```python
# Good
with open("templates/config.json") as f:

# Bad (Windows-style)
with open("templates\\config.json") as f:
```

## Script Requirements

### Execute Permissions

Scripts must be executable:

```bash
chmod +x scripts/helper.py
chmod +x scripts/*.sh
```

### Dependencies

Document required packages in skill description:

```yaml
description: "Process PDFs. Use when working with PDF files. Requires pypdf and pdfplumber packages."
```

Pre-install dependencies in environment before Claude uses the skill.

### Shebang Lines

Include shebang for script type:

```python
#!/usr/bin/env python3
```

```bash
#!/usr/bin/env bash
```

## Troubleshooting Reference

### YAML Validation

Valid YAML structure:

```yaml
---
name: "skill-name"
description: "Description here"
---
```

Requirements:
- Opening `---` on line 1
- Closing `---` before content
- Spaces for indentation (NOT tabs)
- Quoted strings with special characters

Common errors:

```yaml
# Missing closing delimiter
---
name: "skill-name"
description: "Description"

# Tabs instead of spaces
---
name:	"skill-name"

# Unquoted string with special characters
---
description: Use "quotes" for values
```

### File Location Verification

Check skill exists:

```bash
# Project/Local skills
ls -la .claude/skills/*/SKILL.md

# Global skills
ls -la /Users/Shared/data/claude/ccc-files/skills/*/SKILL.md
```

Check specific skill structure:

```bash
tree .claude/skills/skill-name
```

### Debug Mode

Run Claude Code with debug flag:

```bash
claude --debug
```

Look for:
- YAML parsing errors
- File loading messages
- Skill activation logs

## Skills vs Slash Commands

| Aspect | Skills | Slash Commands |
|--------|--------|----------------|
| **Invocation** | Automatic (model-invoked) | Manual (user types /command) |
| **Complexity** | Complex capabilities with structure | Simple prompts |
| **Files** | Directory with SKILL.md + supporting files | Single markdown file |
| **Discovery** | Based on description matching | Explicit user command |
| **Use case** | Claude should discover automatically | User wants explicit control |

**Choose Skills when**:
- Claude should activate based on context
- Complex workflows with multiple steps
- Multiple files or scripts needed
- Team needs standardized guidance

**Choose Slash Commands when**:
- User needs explicit invocation control
- Simple, single-file prompt
- Repeated identical instructions

## Plugin Distribution

### Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
├── commands/
├── agents/
└── skills/
    └── my-skill/
        └── SKILL.md
```

Skills in `skills/` directory become available automatically when plugin installed.

### No Manifest Configuration

Unlike commands/agents, skills don't require plugin.json entries. They're discovered automatically from directory structure.

## Version History Format

Recommended format:

```markdown
## Version History

- v2.0.0 (2025-11-15): Breaking change - new API format
- v1.1.0 (2025-11-10): Added feature X
- v1.0.1 (2025-11-05): Fixed bug Y
- v1.0.0 (2025-11-03): Initial version
```

Use semantic versioning:
- **Major** (v2.0.0): Breaking changes
- **Minor** (v1.1.0): New features, backward compatible
- **Patch** (v1.0.1): Bug fixes

## Quality Criteria Details

From official documentation:

- **Discoverable**: Description enables Claude to find skill when relevant
- **Focused**: Single capability, not multiple unrelated features
- **Specific**: File types, formats, use cases in description
- **Documented**: Clear instructions and examples
- **Testable**: Can verify activation with test queries
- **Maintainable**: Version history tracks evolution
- **Secure**: Tool restrictions where appropriate
- **Shared**: Team access via git (project skills) or plugins

## Skill Examples

Six real-world examples from official repositories demonstrating different skill patterns.

### Available Examples

#### [Test-Driven Development](examples/tdd.md)
**Source**: obra/superpowers
**Pattern**: Strict methodology enforcement with rationalization pre-emption
**Features**: Iron Law, rationalization tables, Good/Bad tags, Graphviz diagram, verification checklist

#### [Systematic Debugging](examples/systematic-debugging.md)
**Source**: obra/superpowers
**Pattern**: Four-phase framework with stopping rules
**Features**: Three-fix rule, multi-component diagnostics, sub-skill integration, human partner signals

#### [Web App Testing](examples/webapp-testing.md)
**Source**: anthropics/skills (official)
**Pattern**: Concise skill with helper scripts and decision tree
**Features**: Black box philosophy, --help first, 96 lines total, reconnaissance-then-action

#### [MCP Builder](examples/mcp-builder.md)
**Source**: anthropics/skills (official)
**Pattern**: Comprehensive four-phase framework with external references
**Features**: Quoted design principles, WebFetch integration, 10 evaluation questions, progressive reference loading

#### [XLSX Spreadsheets](examples/xlsx.md)
**Source**: anthropics/skills (official)
**Pattern**: Production standards with zero-tolerance quality policy
**Features**: Zero formula errors policy, color coding standards, recalc.py validation, formula vs hardcode emphasis

#### [DOCX Documents](examples/docx.md)
**Source**: anthropics/skills (official)
**Pattern**: Multi-file with decision tree and external references
**Features**: Workflow decision tree, MANDATORY file reads, batching strategy (3-10 changes), minimal edits principle

#### [Git Worktrees](examples/git-worktrees.md)
**Source**: obra/superpowers
**Pattern**: Workflow automation with safety verification
**Features**: 3-step priority order, .gitignore safety verification, auto-detection, baseline testing

### Pattern Comparison

| Example | Lines | Pattern | Key Feature |
|---------|-------|---------|-------------|
| **TDD** | ~365 | Discipline enforcement | Rationalization tables |
| **Systematic Debugging** | ~296 | Four-phase methodology | Three-fix rule |
| **Web App Testing** | ~96 | Helper scripts | Black box philosophy |
| **MCP Builder** | ~329 | Comprehensive framework | WebFetch integration |
| **XLSX** | ~289 | Production standards | Zero formula errors |
| **DOCX** | ~197 | Decision tree + externals | MANDATORY file reads |
| **Git Worktrees** | ~214 | Safety workflow | .gitignore verification |

### Pattern Selection Guide

#### Discipline Enforcement (TDD)
**Use when**: Need to enforce strict methodology
**Techniques**:
- Iron Laws (unbreakable rules)
- Rationalization tables (pre-empt excuses)
- Verification checklists
- Red flags for self-monitoring

#### Four-Phase Methodology (Systematic Debugging)
**Use when**: Complex process with clear stages
**Techniques**:
- Phase gates (must complete each)
- Stopping rules (three-fix rule)
- Sub-skill integration
- Meta-cognitive monitoring

#### Helper Scripts (Web App Testing)
**Use when**: Complex setup better handled by code
**Techniques**:
- Black box philosophy (don't pollute context)
- --help first (self-documenting)
- Decision trees (guide approach)
- Extreme conciseness (96 lines)

#### Comprehensive Framework (MCP Builder)
**Use when**: Building complex systems with multiple phases
**Techniques**:
- Quoted design principles
- WebFetch for external docs
- Progressive reference loading
- Evaluation framework

#### Production Standards (XLSX)
**Use when**: Domain-specific quality requirements
**Techniques**:
- Zero-tolerance policies
- Industry conventions (color coding)
- Automated validation (recalc.py)
- Verification checklists

#### Decision Tree + Externals (DOCX)
**Use when**: Multiple workflows based on use case
**Techniques**:
- Decision tree upfront
- External documentation (MANDATORY reads)
- Batching strategy (3-10 items)
- Minimal edits principle

#### Safety Workflow (Git Worktrees)
**Use when**: Automation with safety requirements
**Techniques**:
- Priority order (existing > config > ask)
- Safety verification (.gitignore)
- Auto-detection
- Baseline verification

### Common Patterns Across All Examples

1. **Clear structure**: All have well-defined sections
2. **Explicit principles**: Core principles stated upfront
3. **Concrete examples**: Code snippets, commands, workflows
4. **Tables for reference**: Quick reference, comparisons, checklists
5. **Red flags/warnings**: What NOT to do
6. **Integration guidance**: How skills relate to each other

### Key Insights

#### From Community (obra/superpowers)
- **Rationalization pre-emption** (TDD)
- **Stopping rules** (Systematic Debugging)
- **Safety verification** (Git Worktrees)
- **Sub-skill integration**
- **Human partner signals**

#### From Official (anthropics/skills)
- **Extreme conciseness** (Web App Testing: 96 lines)
- **Black box philosophy** (helper scripts)
- **WebFetch integration** (MCP Builder)
- **Zero-tolerance policies** (XLSX)
- **MANDATORY reads** (DOCX)
- **Progressive reference loading**

### Anti-Patterns

What these examples DON'T do:

- No vague descriptions
- No multiple unrelated capabilities
- No ambiguous instructions
- No verification steps skipped
- No version history missing
- No assuming context without checking
- No skipping safety verification
- No polluting context with large files
