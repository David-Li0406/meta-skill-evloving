---
name: Skill Building
description: How to create Claude Code skill documents with YAML frontmatter, instructions, examples, and reference material
---

# Skill Building

## Instructions

When creating a new skill document:

1. **Location**: Create a folder in `.claude/skills/{Skill Name}/` with a `SKILL.md` file inside

2. **YAML Frontmatter**: Start with:
   ```yaml
   ---
   name: Skill Name
   description: One-line description for the skill picker
   ---
   ```

3. **Structure**: Follow this order:
   - `# Skill Name` - Main header matching the name
   - `## Instructions` - Numbered guidelines for Claude to follow
   - `## Examples` - Example dialogues showing usage
   - `---` - Horizontal rule separator
   - `# Reference` - Detailed reference material, code samples, tables

4. **Instructions Section**: Write as imperatives - "When helping users...", "Always include...", "Use X for Y"

5. **Examples Section**: Use this format:
   ```
   ### Example 1: Brief Title
   ```
   User: What the user asks

   Claude: What Claude should do/say
   [Actions in brackets]
   ```
   ```

6. **Reference Section**: Include:
   - Code samples that work
   - Useful commands
   - Tables of common values
   - File locations
   - Patterns to follow

7. **Supporting Files**: Put reference implementations, templates, or data files in the same folder as SKILL.md

8. **Keep It Practical**: Focus on what Claude needs to do the job. Skip theory, include commands and code.

## Examples

### Example 1: Creating a Database Skill
```
User: Create a skill for working with our PostgreSQL database

Claude: I'll create a skill document:
1. Create folder: .claude/skills/Database Access/
2. Write SKILL.md with:
   - YAML header with name and description
   - Instructions for connection patterns, parameter styles
   - Examples of common queries
   - Reference section with connection strings, table schemas
3. Optionally add reference files (config templates, helper code)
```

### Example 2: Creating a Tool-Based Skill
```
User: Make a skill for our ONI calculator

Claude: I'll create a skill that teaches future Claude sessions:
1. Where the database and source files are
2. How to query the database
3. How to fix the extraction when data is missing
4. Common calculations and reference values

The skill becomes the bootstrap for continuity across sessions.
```

### Example 3: When to Create a Skill
```
User: I keep having to explain how our logging works

Claude: That's a good candidate for a skill. I'll document:
- The logging pattern we use
- How to set it up in new projects
- Common issues and fixes
- Reference implementation to copy

Now future sessions can just load the skill instead of you explaining it.
```

---

# Reference

## File Structure

```
.claude/
└── skills/
    └── My Skill/
        ├── SKILL.md          # Required - the skill document
        ├── helper.cs         # Optional - reference implementation
        ├── template.json     # Optional - config templates
        └── README.md         # Optional - additional docs
```

## YAML Frontmatter

Required fields:
```yaml
---
name: Skill Name
description: Brief description shown in skill picker (one line)
---
```

## Document Template

```markdown
---
name: Skill Name
description: One-line description
---

# Skill Name

## Instructions

When helping users with [topic]:

1. **First Guideline**: Details...
2. **Second Guideline**: Details...
3. **Third Guideline**: Details...

## Examples

### Example 1: Common Task
```
User: How do I...

Claude: I'll help by:
- Step one
- Step two
[Provides implementation]
```

### Example 2: Edge Case
```
User: What if...

Claude: In that case:
[Explains approach]
```

---

# Reference

## Useful Commands

```bash
command --with --options
```

## Key Values

| Item | Value | Notes |
|------|-------|-------|
| ... | ... | ... |

## Code Patterns

```language
// Reference implementation
```
```

## When to Create a Skill

Create a skill when:
- You've explained the same thing multiple times
- A workflow requires knowing file locations, commands, or patterns
- Context would be lost between sessions
- The knowledge is project-specific, not general

Don't create a skill for:
- General programming knowledge
- One-off tasks
- Things that change frequently (put those in config instead)

## Skill Maintenance

- Update skills when patterns change
- Add new examples when edge cases are discovered
- Keep reference material current with actual code
- Remove obsolete information
