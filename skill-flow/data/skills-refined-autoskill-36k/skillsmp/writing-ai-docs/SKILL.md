---
name: writing-ai-docs
description: Creates individual AI-ready documentation files with proper structure, frontmatter, and validation. Use when writing or improving documentation that AI tools must process effectively. Triggers on "write documentation", "create docs", "document this", "make docs AI-ready", or "validate documentation".
---

# Writing AI-Ready Documentation

## Overview

This skill provides comprehensive guidance for creating individual documentation files that AI tools can
effectively process and understand. AI coding assistants process documentation as discrete text chunks through
semantic similarity matching, requiring explicit context, consistent terminology, and self-contained sections.

**This skill is for single-file documentation creation.** For managing entire documentation repositories or
multi-file documentation systems, use the maintaining-docs skill.

## When to Use This Skill

Use this skill when:

- Writing new documentation files (guides, API docs, tutorials)
- Improving existing documentation for AI-readability
- Validating documentation structure and quality
- Creating documentation that both humans and AI tools can effectively use
- Ensuring documentation follows best practices for chunking and retrieval

## Quick Start with Templates

The fastest way to create AI-ready documentation is to start with a template:

**1. List available templates:**

```bash
python scripts/list_templates.py
```

This shows all 17 templates organized by frequency (high/medium/one-time/special).

**2. Create from template:**

```bash
python scripts/create_from_template.py <template-name> <output-path>
```

Examples:

```bash
# API endpoint documentation
python scripts/create_from_template.py api-endpoint docs/api/get-users.md

# How-to guide
python scripts/create_from_template.py how-to-guide docs/guides/deploy-production.md

# Tutorial
python scripts/create_from_template.py tutorial docs/tutorials/first-oauth-app.md

# README
python scripts/create_from_template.py README README.md
```

**3. Fill in placeholders and validate:**

After creating from template:

- Replace all `[placeholders]` with actual content
- Update frontmatter fields (title, description, etc.)
- Run validation scripts (see Step 5 below)

**Templates automatically include:**

- Correct frontmatter structure with all required fields
- Proper heading hierarchy
- Self-contained section structure
- Placeholder code blocks with language tags
- Current date for created/lastUpdated fields

## Documentation Creation Workflow

Follow this workflow when creating or improving documentation:

## Step 1: Determine Document Type and Frontmatter

Every documentation file must start with YAML frontmatter enclosed in `---`. The frontmatter provides essential
metadata for both human navigation and AI context.

**Universal required fields:**

- `title`: Clear, descriptive title (60-70 chars max)
- `description`: Brief 1-2 sentence summary for SEO and AI context
- `type`: Document type (api-endpoint, guide, tutorial, reference, concept, troubleshooting)
- `created`: ISO 8601 date (YYYY-MM-DD)
- `lastUpdated`: ISO 8601 date (YYYY-MM-DD)

**Document type-specific fields:**

- **API:** method, endpoint, authentication
- **Tutorial:** difficulty, duration, prerequisites, outcomes
- **Guide:** difficulty, duration, prerequisites
- **Reference:** version, category
- **Concept:** audience

**Optional discovery fields** for improved AI agent discoverability:

For guides, tutorials, troubleshooting, and concept documentation, add optional discovery fields:

- `when-to-read`: User scenarios/contexts when this document is relevant (e.g., "implementing authentication", "debugging 401 errors")
- `related-to`: Explicit links to related documentation
- `code-references`: Links to relevant source code files

These fields help AI agents find relevant documentation through fuzzy/semantic search based on user intent. Use them when they provide clear value beyond the title and description. See the "Optional Discovery Fields" section in `references/frontmatter-schemas.md` for details.

**For detailed frontmatter schemas:** See `references/frontmatter-schemas.md`

## Step 2: Structure Document for AI Chunking

AI tools split documentation into semantic chunks of 500-1000 tokens. Each section must be self-contained
because chunking may separate related content.

See `references/ai-ready-single-file.md` for core AI-ready principles including:

- Why AI reads differently (chunking, semantic matching)
- The 5 structural rules (headings, self-contained sections, terminology, code blocks, prerequisites)
- The 3 content patterns (explicit language, grouping, context repetition)

**Heading hierarchy rules:**

- ONE H1 per document (matching the title)
- Strict H1→H2→H3 progression (never skip levels)
- Each major section gets H2, subsections get H3

**Self-contained sections:**

- Include necessary context at section start
- Repeat key information rather than referring back
- Use explicit language (avoid vague pronouns)
- Keep related information physically close

See `references/ai-ready-single-file.md` for complete structural rules and examples.
See `references/examples.md` for complete document examples.

## Step 3: Format Code Examples Properly

**Always use properly formatted code blocks with language tags.** AI tools struggle when commands are embedded
in sentences.

**Good:** Code in fenced blocks with language tags
**Bad:** Commands inline in prose

See `references/examples.md` for complete before/after examples showing proper code formatting.

## Step 4: Write for AI Comprehension

**Key principles:**

- **Explicit over implicit** - Use specific names, not vague pronouns ("it", "this", "they")
- **Consistent terminology** - Pick ONE term per concept throughout document
- **Specific prerequisites** - List all requirements explicitly with versions
- **Self-contained sections** - Each section works independently

See `references/ai-ready-single-file.md` for detailed content patterns and anti-patterns.
See `references/examples.md` for complete before/after examples.

## Step 5: Validate Documentation

Use the validation scripts to check documentation:

**Check document quality:**

```bash
python scripts/check_doc_quality.py path/to/your-doc.md
```

**Lint markdown:**

```bash
bash scripts/lint_markdown.sh path/to/your-doc.md
```

**Auto-fix linting issues:**

```bash
npx markdownlint-cli --config .markdownlint.json --fix path/to/your-doc.md
```

**Check for broken links:**

```bash
bash scripts/check_links.sh path/to/your-doc.md
```

All scripts support multiple files and glob patterns. See scripts/ section below for details.

**For frontmatter validation**, use the maintaining-docs skill:

```bash
# Invoke maintaining-docs skill for comprehensive validation
Skill(command='maintaining-docs')
# Then use that skill's validation tools
```

**Run all validators** before considering documentation complete.

## Step 6: Review for AI-Ready Patterns

**Self-contained sections:**

- Each section comprehensible independently
- Include necessary context at section start
- Brief summaries after major headings

**Proper document length:**

- Under 1000 lines ideal for chunking
- Under 4000 tokens preferred (~16,000 characters)
- If longer, ensure sections are especially self-contained

**Examples over explanations:**

- Include runnable, complete examples
- Show both input and output
- Test all examples before publishing

**Semantic proximity:**

- Keep definitions near their applications
- Keep prerequisites adjacent to procedures
- Don't scatter related concepts

See `references/quality-checklist.md` for a comprehensive validation checklist.

## Resources

### scripts/

**Validation scripts**:

**check_doc_quality.py** - Checks documentation quality metrics

- Validates heading hierarchy (no skipped levels)
- Checks code block formatting (language tags required)
- Analyzes document length for chunking
- Detects vague language patterns
- Verifies section structure

**lint_markdown.sh** - Lints markdown with markdownlint-cli

- Uses npx markdownlint-cli (no global install needed)
- Custom rules aligned with AI-ready principles
- Auto-fix option available
- Configuration in `.markdownlint.json`

**check_links.sh** - Checks for broken links in markdown files

- Uses npx markdown-link-check (no global install needed)
- Validates both internal links (files and sections) and external links (HTTP/HTTPS)
- Detects broken, unreachable, or invalid links
- Configuration in `.markdown-link-check.json`
- Ignores localhost URLs and placeholder domains
- Handles rate limiting with retries

**Template management**:

**list_templates.py** - Lists all available templates with descriptions

```bash
python scripts/list_templates.py
```

Output example:

```text
📋 Available Documentation Templates
======================================================================

🔥 High-Frequency Templates
   Use multiple times per project

   • api-endpoint.md              REST/GraphQL API endpoint documentation
   • how-to-guide.md               Task-oriented step-by-step guides
   • cli-command.md                Command-line interface reference
   ...

📖 Usage:

   Create from template:
   $ python scripts/create_from_template.py <template-name> <output-path>
```

Features:

- Organized by category (high-frequency, medium, one-time, special)
- Shows template descriptions from frontmatter
- Displays usage examples

**create_from_template.py** - Creates new documentation from template

```bash
python scripts/create_from_template.py <template-name> <output-path>

# Examples:
python scripts/create_from_template.py api-endpoint docs/api/get-users.md
python scripts/create_from_template.py tutorial docs/tutorials/oauth.md
python scripts/create_from_template.py README README.md
```

Features:

- Copies template to specified path
- Auto-updates dates to current date (YYYY-MM-DD)
- Creates parent directories if needed
- Prompts before overwriting existing files
- Shows next steps after creation

**Complete workflow example:**

```bash
# 1. List available templates
python scripts/list_templates.py

# 2. Create from template
python scripts/create_from_template.py api-endpoint docs/api/create-user.md

# 3. Edit the file (replace [placeholders])
# ... edit docs/api/create-user.md ...

# 4. Validate
python scripts/check_doc_quality.py docs/api/create-user.md
bash scripts/lint_markdown.sh docs/api/create-user.md

# 5. Auto-fix any linting issues
npx markdownlint-cli --config .markdownlint.json --fix docs/api/create-user.md
```

All scripts are executable and provide clear error/success output.

### references/

**ai-ready-single-file.md** - Core principles for AI-readable documentation

- Why AI reads differently (chunking, semantic matching)
- The 5 structural rules (headings, self-contained sections, terminology, code blocks, prerequisites)
- The 3 content patterns (explicit language, grouping, context repetition)
- The 5 worst anti-patterns that break AI comprehension
- Complete example structure and validation checklist

**frontmatter-schemas.md** - Frontmatter templates for common document types

- Universal core fields (title, description, type, created, lastUpdated)
- Schemas for API, tutorial, guide, reference, concept, and troubleshooting docs
- Field guidelines and common mistakes
- Required vs recommended fields

**examples.md** - Complete before/after examples

- API documentation (bad vs good)
- Tutorial documentation (assumed context vs complete)
- Concept explanation (scattered vs grouped)
- Shows exactly what works and what breaks AI

**api-doc-patterns.md** - Standard structure for API endpoint documentation

- Consistent endpoint structure patterns
- Request/response formatting
- Error handling patterns
- Code examples and verification

**quality-checklist.md** - Comprehensive validation checklist

- Frontmatter validation
- Structure validation
- Content validation
- Code examples validation
- Document type-specific checks
- Common anti-patterns to avoid

**Refer to these files when creating documentation** for detailed guidance and examples.

### templates/

Ready-to-use templates for common documentation types. Each template includes proper frontmatter, structure,
and placeholder content following AI-ready principles.

**High-frequency templates** (use multiple times per project):

- `api-endpoint.md` - REST/GraphQL API endpoint documentation
- `how-to-guide.md` - Task-oriented step-by-step guides
- `troubleshooting-entry.md` - Problem-solution documentation
- `cli-command.md` - Command-line interface reference
- `config-option.md` - Configuration option reference

**Medium-frequency templates** (several per project):

- `tutorial.md` - Step-by-step learning tutorial
- `concept-explanation.md` - Architecture and design concepts
- `error-reference.md` - Error code documentation

**One-time templates** (project essentials):

- `getting-started.md` - Quick start guide
- `installation-guide.md` - Installation instructions

**Special documentation**:

- `CHANGELOG.md` - Version history and release notes
- `README.md` - Project overview and introduction
- `adr-template.md` - Architecture Decision Records
- `personas.md` - User persona documentation
- `faq.md` - Frequently Asked Questions
- `glossary.md` - Terminology and definitions

**Fallback**:

- `generic-template.md` - Flexible template for any documentation type

**Usage**: Copy appropriate template, fill in placeholders, run validation scripts.

## Examples

**Example request 1:** "Document this API endpoint for AI tools"

**Response approach:**

1. Determine it's an API endpoint → use api-endpoint frontmatter schema
2. Structure with Request/Response/Examples sections (see references/api-doc-patterns.md)
3. Format all code with language tags
4. Run validators to ensure quality
5. Check for self-contained sections and explicit language

**Example request 2:** "Help me improve this documentation file"

**Response approach:**

1. Read the current documentation
2. Run validators to identify issues
3. Check frontmatter completeness
4. Verify heading hierarchy
5. Review for AI-ready patterns (see references/ai-ready-single-file.md)
6. Suggest specific improvements with examples (see references/examples.md)

**Example request 3:** "Create a tutorial for implementing OAuth"

**Response approach:**

1. Use tutorial frontmatter schema with difficulty, duration, prerequisites, outcomes
2. Structure with clear numbered steps
3. Ensure each step is self-contained
4. Include complete, runnable code examples
5. Add explicit prerequisites and expected outcomes
6. Validate before finalizing

## Key Takeaways

1. **Always start with proper frontmatter** - Required for AI context and navigation
2. **Use strict heading hierarchy** - H1→H2→H3, never skip levels
3. **Format code properly** - Language tags, code blocks, not inline
4. **Be explicit, not implicit** - Avoid vague pronouns and references
5. **Make sections self-contained** - AI chunking separates content
6. **Use consistent terminology** - One term per concept throughout
7. **Validate before finalizing** - Run all validation scripts
8. **Examples over explanations** - Complete, runnable code examples
9. **Think about chunking** - Keep related information physically close
10. **Use the reference files** - Comprehensive guidance available in references/

## Related Skills

**For project-wide documentation management:**

Use the maintaining-docs skill for:

- Project-wide documentation validation
- llms.txt generation
- Documentation structure management
- Frontmatter validation across multiple files

```bash
Skill(command='maintaining-docs')
```

**For writing agent prompts or instructions:**

Use the crafting-agentic-prompts skill (not this skill) when documenting:

- System prompts
- Agent behaviors
- Agentic workflows
