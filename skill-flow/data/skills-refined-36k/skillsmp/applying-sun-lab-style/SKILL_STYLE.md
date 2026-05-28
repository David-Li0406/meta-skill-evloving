# Claude Skill Style Guide

Conventions for Claude Code skill files and CLAUDE.md project instructions in Sun Lab projects.

---

## File Types

This guide covers two types of Claude instruction files:

| File Type   | Location            | Purpose                                        |
|-------------|---------------------|------------------------------------------------|
| SKILL.md    | `.claude/skills/*/` | Skill-specific instructions loaded on demand   |
| CLAUDE.md   | Project root        | Project-wide instructions loaded every session |

---

## Skill File Conventions

Claude Code skill files (`.md` files in `.claude/skills/`) follow specific formatting conventions.

### Line Length

All skill and asset Markdown files must adhere to the **120 character line limit**. This matches the Python code
formatting standard.

- Wrap prose text at 120 characters
- Break long sentences at natural boundaries (after punctuation, between clauses)
- Code blocks may exceed 120 characters only when necessary for readability
- Tables may exceed 120 characters when proper column alignment aids clarity

### YAML Frontmatter

Every SKILL.md requires YAML frontmatter with `name` and `description`:

```yaml
---
name: exploring-codebase
description: >-
  Performs in-depth codebase exploration at the start of a coding session. Builds comprehensive
  understanding of project structure, architecture, key components, and patterns. Use at session
  start or when the user asks to understand the codebase.
---
```

**Name**: Use gerund form (verb + -ing), lowercase with hyphens. Examples: `exploring-codebase`,
`applying-sun-lab-style`, `designing-experiments`.

**Description**: Write in third person. Include both what the skill does and when to use it.

### Table Formatting

Use **pretty table formatting** with proper column alignment:

**Good:**

```markdown
| Field              | Type        | Required | Description                              |
|--------------------|-------------|----------|------------------------------------------|
| `name`             | str         | Yes      | Visual identifier (e.g., 'A', 'Gray')    |
| `code`             | int         | Yes      | Unique uint8 code for MQTT communication |
```

**Avoid:**

```markdown
| Field | Type | Required | Description |
|---|---|---|---|
| `name` | str | Yes | Visual identifier |
```

### Table Formatting Rules

1. Align all `|` characters vertically
2. Use dashes (`-`) that span the full column width
3. Pad cells to consistent widths within each column
4. Use backticks for field names, types, and values

### Section Organization

```markdown
# Skill Name

Brief description of the skill's purpose.

---

## When to Use

- Bullet points describing use cases

---

## Main Content Section

### Subsection

Content with tables, code blocks, and explanations.
```

### Code Blocks

Use fenced code blocks with language identifiers:

````markdown
```yaml
cues:
  - name: "A"
    code: 1
```

```python
def process_data() -> None:
    pass
```
````

### Voice and Directional Language

Skill files use two voice styles:

- **Descriptive content**: Third person imperative. Example: "Extracts zone positions from configuration files."
- **Agent directives**: Second person with "You MUST", "You should". Example: "You MUST use the Task tool."

### Progressive Disclosure

Keep SKILL.md under 500 lines. Split content into separate files when needed:

```
skill-name/
├── SKILL.md              # Main instructions (loaded when triggered)
├── REFERENCE.md          # Detailed reference (loaded as needed)
└── EXAMPLES.md           # Usage examples (loaded as needed)
```

Reference files using standard Markdown links: `[REFERENCE.md](REFERENCE.md)`

---

## CLAUDE.md Conventions

The `CLAUDE.md` file at the project root provides project-wide instructions loaded at the start of every Claude session.

### Structure

CLAUDE.md files use the following section order:

1. **Title**: `# Claude Code Instructions`
2. **Session Start Behavior**: What Claude should do at session start
3. **Style Guide Compliance**: Required style conventions
4. **Cross-Referenced Library Verification**: Dependencies and version checking (if applicable)
5. **Available Skills**: List of project skills with descriptions
6. **MCP Server**: MCP server documentation (if applicable)
7. **Downstream Library Integration**: Related libraries and coordination (if applicable)
8. **Project Context**: Architecture, key areas, patterns, and standards

### Formatting Rules

CLAUDE.md follows the same formatting conventions as skill files:

- **Line length**: 120 characters maximum
- **Tables**: Pretty formatting with aligned columns
- **Code blocks**: Include language identifiers
- **Section separators**: Use `##` headings (no horizontal rules between sections)

### Voice

- **Descriptive content**: Third person. Example: "This library provides shared assets..."
- **Agent directives**: Second person with emphasis. Example: "You MUST invoke the `/sun-lab-style` skill..."

### Content Guidelines

- Keep CLAUDE.md focused on project-specific instructions
- Reference skills rather than duplicating their content
- Include workflow guidance for common tasks (e.g., adding new components)
- Document integration points with other libraries

---

## Verification Checklist

**You MUST verify your edits against this checklist before submitting any changes to skill or CLAUDE.md files.**

### Skill Files (SKILL.md)

```
- [ ] YAML frontmatter with `name` and `description`
- [ ] Name uses gerund form (verb + -ing), lowercase with hyphens
- [ ] Description in third person, includes what AND when to use
- [ ] All lines ≤ 120 characters (tables/code blocks may exceed for clarity)
- [ ] Tables use pretty formatting with aligned columns
- [ ] Major sections separated with horizontal rules (`---`)
- [ ] Code blocks include language identifiers
- [ ] Third person imperative for descriptions
- [ ] Second person for agent directives ("You MUST...")
- [ ] Sentence case for section headers
- [ ] SKILL.md under 500 lines (split to reference files if needed)
- [ ] References one level deep from SKILL.md
```

### Project Instructions (CLAUDE.md)

```
- [ ] Title is `# Claude Code Instructions`
- [ ] All lines ≤ 120 characters (tables/code blocks may exceed for clarity)
- [ ] Tables use pretty formatting with aligned columns
- [ ] Code blocks include language identifiers
- [ ] Third person for descriptive content
- [ ] Second person with emphasis for directives ("You MUST...")
- [ ] Sections follow recommended order (Session Start, Style Guide, Skills, etc.)
- [ ] Workflow guidance included for common extension tasks
- [ ] Technical claims cross-referenced against codebase
```
