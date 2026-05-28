---
name: creating-agentic-skills
description: Create Agent Skills that extend AI agent capabilities with specialized knowledge, workflows, and tools. Use when creating new skills, updating existing skills, converting repeated patterns into skills, documenting domain-specific workflows, or when user mentions skills, SKILL.md files, skill development, or skill documentation.
---

# Create Agent Skills

Create skills as folders of instructions, scripts, and resources that agents discover and load dynamically. Skills transform general-purpose agents into specialized tools by packaging procedural knowledge into composable, reusable capabilities.

## Directory Structure

```
skill-name/
├── SKILL.md              # Required: instructions + metadata
├── scripts/              # Optional: executable code
├── references/           # Optional: documentation loaded as needed
└── assets/               # Optional: templates, resources for output
```

Place skills in `.opencode/skill/{name}/SKILL.md` for project-local skills or `~/.config/opencode/skill/{name}/SKILL.md` for global skills.

### Directory Contents

**SKILL.md** (required)

- YAML frontmatter with `name` and `description`
- Markdown instructions and guidance
- Keep under 500 lines; split into references/ when approaching this limit

**scripts/** (optional)

- Executable code for deterministic operations
- Token efficient: executed without loading into context
- Test scripts before including them

**references/** (optional)

- Documentation loaded into context as needed
- Keep files focused and under 100 lines each
- Include table of contents for longer files

**assets/** (optional)

- Files used in output (templates, images, boilerplate)
- Not loaded into context; copied or modified during execution

## SKILL.md Format

### Frontmatter (Required)

```yaml
---
name: skill-name
description: What this skill does and when to use it.
---
```

**name** requirements:

- 1-64 characters
- Lowercase letters, numbers, and hyphens only
- No leading/trailing hyphens, no consecutive hyphens
- Must match the parent directory name

**description** requirements:

- 1-1024 characters (aim for ~200)
- Include what the skill does AND when to use it
- Include trigger keywords users would naturally say
- Write in third person ("Creates..." not "I can help...")

### Writing Effective Descriptions

The description is the primary triggering mechanism. Agents read only the name and description at startup to decide when to load the full skill.

**Formula:**

```
[What the skill does]. Use when [trigger contexts] or when user mentions [keywords].
```

**Effective example:**

```yaml
description: Create Laravel Action classes for business logic operations following domain-driven design. Use when creating Actions, implementing business logic, handling user operations, or when user mentions Action classes, domain operations, business rules, or service classes.
```

**Ineffective examples:**

```yaml
description: Helps with actions  # Too vague, no triggers
description: Action classes for Laravel  # No "use when" triggers
description: I help you create Actions  # Wrong person (use third person)
```

**Key triggers to include:**

1. Action verbs: "Create", "Write", "Build", "Configure"
2. Task contexts: "when creating...", "when implementing..."
3. Natural keywords: phrases users would actually say
4. File types: ".md files", "SKILL.md", relevant extensions

### Body Content

Write instructions in imperative form ("Create..." not "Creating..."). Structure the body with:

1. **Brief overview** - What the skill enables (2-3 sentences max)
2. **Core workflow** - Essential steps to accomplish the task
3. **Key conventions** - Critical patterns with concise code examples
4. **References** - Links to detailed documentation in references/

Do NOT include:

- "When to Use This Skill" sections (this belongs in description)
- Verbose explanations of concepts the agent already knows
- Duplicate information (put it in SKILL.md OR references/, not both)
- README, CHANGELOG, or other auxiliary documentation

## Progressive Disclosure

Skills use three-level loading to manage context efficiently:

| Level        | When Loaded      | Token Cost  | Content                        |
| ------------ | ---------------- | ----------- | ------------------------------ |
| Metadata     | Always (startup) | ~100 tokens | `name` and `description`       |
| Instructions | When triggered   | <5k tokens  | SKILL.md body                  |
| Resources    | As needed        | Unlimited   | references/, scripts/, assets/ |

### When to Split Content

Move content to references/ when:

- SKILL.md approaches 500 lines
- Content is needed only for specific scenarios
- Multiple frameworks/variants exist (one file per variant)
- Detailed examples would bloat the main file

**Pattern: High-level guide with references**

```markdown
## Quick start

[Essential code example]

## Advanced features

- **Form filling**: See [references/forms.md](references/forms.md)
- **API reference**: See [references/api.md](references/api.md)
```

**Pattern: Domain-specific organization**

```
bigquery-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

When user asks about sales, agent reads only sales.md.

### Reference Guidelines

- Keep references one level deep from SKILL.md (no nested references)
- Include table of contents for files over 100 lines
- Use relative paths: `[forms.md](references/forms.md)`
- Describe clearly when to read each reference file

## Creating a Skill

### Step 1: Identify Concrete Examples

Before writing, identify 3-5 concrete examples of how the skill will be used:

- What would a user say to trigger this skill?
- What steps would you follow to complete the task?
- What context does the agent need that it doesn't already have?

### Step 2: Plan Reusable Resources

For each example, identify:

- **Scripts**: Code rewritten repeatedly or needing deterministic reliability
- **References**: Documentation needed while working (schemas, APIs, policies)
- **Assets**: Files used in output (templates, boilerplate)

### Step 3: Write the Skill

1. Create the directory: `.opencode/skill/{skill-name}/`
2. Write SKILL.md with frontmatter and instructions
3. Add scripts/, references/, assets/ as identified
4. Test scripts to ensure they work

### Step 4: Iterate Based on Usage

After using the skill on real tasks:

1. Notice where the agent struggles or makes mistakes
2. Identify what context was missing or unclear
3. Update SKILL.md or resources accordingly
4. Keep refining until results are consistent

## Splitting Large Skills

When an existing skill exceeds 500 lines or becomes unwieldy:

1. **Identify separable content**: Look for variant-specific details, extensive examples, or reference material
2. **Create references/ files**: Move detailed content, keeping only essential workflow in SKILL.md
3. **Add navigation**: Link to references from SKILL.md with clear descriptions of when to read each
4. **Avoid duplication**: Content lives in ONE place only

**Before (monolithic):**

```markdown
# Creating Components

[500+ lines of everything]
```

**After (progressive disclosure):**

```markdown
# Creating Components

[Core workflow ~150 lines]

## References

- [references/patterns.md](references/patterns.md) - Component patterns and variants
- [references/examples.md](references/examples.md) - Complete working examples
```

## Anti-Patterns

### Avoid These Mistakes

```yaml
# Vague description without triggers
description: Helps with PDF files

# "When to Use" in body instead of description
## When to Use This Skill
Use when creating PDFs...  # This should be in description!

# Verbose explanations
PDF (Portable Document Format) is a file format...  # Agent knows this

# Deeply nested references
See [advanced.md] which links to [details.md] which links to...

# Duplicate content
[Same information in SKILL.md AND references/guide.md]

# Extraneous files
README.md, INSTALLATION_GUIDE.md, CHANGELOG.md  # Don't create these
```

### Do This Instead

```yaml
# Specific description with triggers
description: Extract text from PDFs, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.

# All trigger info in description, body has only instructions
## Quick Start
[Immediate actionable content]

# Concise, actionable content
Use pdfplumber to extract text:
[code example]

# One level deep references
See [references/forms.md](references/forms.md) for form filling.

# Single source of truth
[Information in exactly one place]
```

## Quality Standards

Before finalizing a skill, verify:

- [ ] Name is lowercase, hyphenated, matches directory
- [ ] Description includes what + when + keywords
- [ ] Description under 200 chars (up to 1024 if needed)
- [ ] SKILL.md under 500 lines
- [ ] No "When to Use" section in body
- [ ] References are one level deep
- [ ] No duplicate content between files
- [ ] Scripts are tested and working
- [ ] Content is concise (only what agent doesn't know)

See [references/checklist.md](references/checklist.md) for the complete quality checklist.
See [references/examples.md](references/examples.md) for full skill examples.
See [assets/template.md](assets/template.md) for a starter template.
