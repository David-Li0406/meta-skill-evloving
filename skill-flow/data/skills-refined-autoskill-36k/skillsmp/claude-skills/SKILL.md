---
name: claude-skills
description: Guide for creating Claude Agent Skills. Use when designing Skills, writing SKILL.md files, structuring Skill directories, or understanding progressive disclosure, metadata, and best practices for reusable domain-specific capabilities.
---

# Claude Agent Skills Creation Guide

Create modular, reusable Agent Skills that extend Claude's functionality with domain-specific expertise.

## What are Agent Skills?

**Agent Skills** are filesystem-based capabilities that provide Claude with domain-specific expertise: workflows, context, and best practices. Skills load on-demand and eliminate repeated guidance across conversations.

**Key benefits:**
- **Specialize Claude**: Tailor capabilities for specific tasks
- **Reduce repetition**: Create once, use automatically
- **Compose capabilities**: Combine Skills for complex workflows
- **Progressive disclosure**: Load content only as needed

## Quick Start

### Minimal Skill Structure

```
my-skill/
└── SKILL.md
```

**SKILL.md format:**
```yaml
---
name: my-skill
description: Brief description of when to use this Skill. Include keywords that trigger relevance.
---

# My Skill Name

Quick start content, workflows, and examples.

## Common Task

Step-by-step instructions...
```

### With Reference Files

```
my-skill/
├── SKILL.md           # Main entry point
└── reference/
    ├── guide.md       # Detailed documentation
    └── examples.md    # Comprehensive examples
```

## Core Principles

### 1. Progressive Disclosure (3 Levels)

**Level 1: Metadata** (always loaded)
- YAML frontmatter with `name` and `description`
- Loaded at startup, included in system prompt
- Lightweight - no context penalty
- **Use for:** Skill discovery ("when to use this")

**Level 2: Instructions** (loaded when triggered)
- Main body of SKILL.md
- Loaded when Skill becomes relevant
- **Use for:** Workflows, best practices, guidance

**Level 3: Resources** (loaded as needed)
- Additional markdown files, scripts, templates
- Loaded only when referenced
- **Use for:** Detailed docs, code utilities, reference materials

### 2. Concise is Key

**Challenge every token:**
- Does Claude really need this explanation?
- Can I assume Claude knows this?
- Does this justify its context cost?

**Good (concise):**
```markdown
## Extract PDF text

Use pdfplumber for text extraction:

\`\`\`python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
\`\`\`
```

**Bad (verbose):**
```markdown
## Extract PDF text

PDF (Portable Document Format) files are a common format...
You'll need to use a library. There are many available...
First install it with pip, then use the code below...
```

**Assume Claude is smart.** Only add context Claude doesn't already have.

### 3. Write Clear Metadata

**Description format:**
```yaml
description: What the Skill does. When to use it. Include trigger keywords.
```

**Good examples:**
```yaml
# Specific, clear trigger conditions
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.

# Domain-specific with clear scope
description: Generate API documentation from schemas, including endpoints, request/response examples, and authentication guides. Use when working with APIs, documentation generation, or API specifications.

# Task-focused with keywords
description: Guide for creating git commit messages following Conventional Commits 1.0.0. Use whenever making commits to ensure semantic version-aware commit history.
```

**Bad examples:**
```yaml
# Too vague
description: Helps with documents

# Missing trigger conditions
description: PDF processing utility

# Too broad
description: Everything related to files
```

## Skill Structure Patterns

### Pattern 1: Single File (Simple Skills)

**Best for:** Focused tasks, <300 lines, single domain

```
skill-name/
└── SKILL.md
```

**Example:** git-commit, simple utilities

### Pattern 2: SKILL.md + References (Complex Skills)

**Best for:** Multiple topics, detailed documentation, >300 lines

```
skill-name/
├── SKILL.md          # Overview, quick start, common tasks
└── reference/
    ├── topic-a.md    # Detailed guide for topic A
    ├── topic-b.md    # Detailed guide for topic B
    └── examples.md   # Comprehensive examples
```

**Example:** api-documentation, database-migrations

### Pattern 3: With Scripts/Templates

**Best for:** Deterministic operations, code utilities

```
skill-name/
├── SKILL.md
├── reference/
│   └── guide.md
└── scripts/
    ├── process.py    # Executable utility
    └── template.yaml # Reusable template
```

### Pattern 4: Multi-Level References (Large Skills)

**Best for:** Multiple domains, extensive documentation

```
skill-name/
├── SKILL.md
└── reference/
    ├── getting-started.md
    ├── api/
    │   ├── overview.md
    │   └── reference.md
    ├── patterns/
    │   ├── pattern-a.md
    │   └── pattern-b.md
    └── examples/
        └── examples.md
```

**Example:** Large framework documentation Skills

## Writing Effective SKILL.md

### Structure Template

```markdown
---
name: skill-name
description: What it does, when to use it, trigger keywords
---

# Skill Name

Brief introduction (1-2 sentences).

## Quick Start

Minimal example to get started quickly.

## Core Concepts

Key principles, patterns, or rules (if applicable).

## Common Tasks

### Task 1
Step-by-step instructions...

### Task 2
Step-by-step instructions...

## Reference Documentation

For complete details, see:
- [Topic A](reference/topic-a.md) - Detailed coverage
- [Topic B](reference/topic-b.md) - Advanced patterns

## When to Use This Skill

Clear conditions for when this Skill applies.

## Related Skills

- **other-skill** - Related functionality
```

### Best Practices

**1. Start with Quick Start**
- Provide immediately usable example
- Show the most common use case
- Keep it minimal (5-10 lines)

**2. Use Progressive Disclosure**
- Essential info in SKILL.md
- Detailed info in reference files
- Link to references with clear descriptions

**3. Include Clear Examples**
- Real, working examples
- Common use cases first
- Edge cases in reference files

**4. Document "When to Use"**
- Explicit trigger conditions
- Related Skills for disambiguation
- Clear scope boundaries

**5. Keep It Current**
- Update when functionality changes
- Remove deprecated content immediately
- Version changes in commit messages

## Common Patterns

### Common Project Skills Patterns

**Structure:**
```
.claude/skills/
├── api-documentation/
│   ├── SKILL.md
│   ├── reference/
│   │   ├── endpoints.md
│   │   ├── authentication.md
│   │   └── versioning.md
│   ├── examples/
│   │   └── request-patterns.md
│   └── templates/
│       └── endpoint-template.md
├── database-migrations/
│   ├── SKILL.md
│   ├── migration-guide.md
│   ├── rollback-guide.md
│   └── scripts/
│       ├── validate.py
│       └── rollback.py
├── code-style/
│   ├── SKILL.md
│   └── reference/
│       ├── naming-conventions.md
│       └── patterns.md
└── git-commit/
    └── SKILL.md
```

**Characteristics:**
- Project-local (`.claude/skills/`)
- Domain-specific (APIs, databases, code style, git)
- Progressive disclosure (SKILL.md → references)
- Cross-skill references

### Tool/Framework Skills

**Structure:**
```
framework-skill/
├── SKILL.md           # Quick start, common tasks
├── reference/
│   ├── api.md         # API reference
│   ├── guide.md       # Comprehensive guide
│   └── examples.md    # Examples catalog
└── templates/
    └── starter.yaml   # Starter templates
```

### Workflow Skills

**Structure:**
```
workflow-skill/
├── SKILL.md           # Workflow overview
├── steps/
│   ├── step-1.md      # Individual step guides
│   ├── step-2.md
│   └── step-3.md
└── examples/
    └── complete.md    # End-to-end examples
```

## Testing Your Skill

### Validation Checklist

- [ ] YAML frontmatter is valid
- [ ] Name is lowercase with hyphens
- [ ] Description includes trigger keywords
- [ ] SKILL.md has clear structure
- [ ] Examples are working and tested
- [ ] References are linked correctly
- [ ] File paths use relative references
- [ ] Content is concise (challenge every token)
- [ ] Skill loads and triggers correctly

### Testing Process

1. **Create test conversation**
   - Mention trigger keywords from description
   - Verify Claude loads the Skill

2. **Test workflows**
   - Follow instructions in SKILL.md
   - Verify completeness and accuracy

3. **Check references**
   - Verify links work
   - Test progressive disclosure

4. **Refine metadata**
   - Adjust description if Skill doesn't trigger
   - Add keywords as needed

## Complete Reference Documentation

For comprehensive details on Agent Skills in Claude Code, see:

### [reference/overview.md](reference/overview.md)
Complete overview of Agent Skills:
- Why use Skills
- How Skills work (3-level loading)
- Progressive disclosure architecture
- Skill structure and security
- Sharing Skills in Claude Code
- Runtime environment

### [reference/good-practices.md](reference/good-practices.md)
Best practices for Skill authoring:
- Concise writing principles
- Degrees of freedom (high/medium/low)
- Testing strategies
- Metadata optimization
- Progressive disclosure patterns
- Workflows and feedback loops
- Common pitfalls to avoid

### [reference/claude-skills.md](reference/claude-skills.md)
Comprehensive Claude Code Skills guide:
- Complete specification for Claude Code
- Creating and managing Skills
- Filesystem-based approach
- Debugging and testing
- Sharing via git and plugins
- Production best practices

## Example Skill Structures

### Simple Skill (Single File)

**git-commit** (438 lines, all in SKILL.md):
- Quick reference table
- Full specification
- Workflow steps
- Comprehensive examples
- Project integration guidelines

### Complex Skill (Multi-File)

**api-documentation** (12 files):
- SKILL.md (overview, quick start)
- reference/ (4 files: endpoints, authentication, versioning, testing)
- examples/ (4 files: request-patterns, response-formats, webhooks, pagination)
- templates/ (3 files: endpoint-template, schema-template, changelog-template)

Progressive disclosure: main docs → reference guides → specific examples

### CLI-Focused Skill (5 files)

**database-migrations** (5 files):
- SKILL.md (overview, commands)
- migration-guide.md (complete reference)
- rollback-guide.md (safety procedures)
- workflow.md (development patterns)
- troubleshooting.md (common issues)

Reference-heavy with detailed procedural guidance

### Configuration Skill (4 files)

**code-style** (4 files):
- SKILL.md (quick start, core principles)
- naming-conventions.md (cross-language naming)
- patterns.md (common patterns)
- formatting.md (formatting guidelines)

Multi-language support with shared principles

## When to Use This Skill

Use this Skill when:
- Creating new Agent Skills
- Structuring Skill directories
- Writing SKILL.md files
- Optimizing Skill metadata
- Understanding progressive disclosure
- Deciding between single-file vs multi-file structure
- Debugging Skill loading issues
- Following best practices for Skill authoring
- Migrating documentation to Skill format

## Related Skills

- **git-commit** - Example of single-file Skill with comprehensive content
- **api-documentation** - Example of complex multi-file Skill with references and templates
- **database-migrations** - Example of reference-heavy Skill with workflow guides

## Key Takeaways

1. **Progressive disclosure**: Load content in stages (metadata → instructions → resources)
2. **Concise is key**: Challenge every token, assume Claude is smart
3. **Clear metadata**: Description should include trigger keywords
4. **Structured organization**: Use references for detailed content
5. **Test thoroughly**: Verify triggering, workflows, and references
6. **Keep current**: Update when functionality changes

---

*For the complete Agent Skills specification and advanced patterns, see the reference documentation above*
