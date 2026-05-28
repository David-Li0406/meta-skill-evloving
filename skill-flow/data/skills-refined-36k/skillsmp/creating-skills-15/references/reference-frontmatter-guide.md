---
title: Reference File Frontmatter Guide
description: Specification for YAML frontmatter in skill reference files, including required fields, validation rules, and examples for programmatic discovery
keywords: frontmatter, metadata, discovery, reference files, yaml, validation
file-type: reference
skill: creating-skills
---

# Reference File Frontmatter Guide

## Purpose

Frontmatter provides metadata that enables:
- **Programmatic discovery and indexing** - Tools can scan and catalog reference files
- **LLM/AI comprehension** - AI tools understand file purpose without reading entire content
- **Search and navigation** - Users and tools can find relevant references quickly
- **Documentation generation** - Automated systems can build indexes and tables of contents
- **Quality validation** - Scripts can verify completeness and correctness

## Required Fields

### title (string, ≤100 chars)

Short, descriptive title for the reference file.

**Purpose**: Displayed in discovery interfaces, navigation menus, and documentation indexes.

**Format**:
- Use title case (capitalize major words)
- Be concise but descriptive
- Avoid generic titles like "Guide" or "Reference"
- Include the domain/topic

**Examples**:
```yaml
title: Preflight Check Patterns
title: Context Gathering Patterns
title: Skill Quality Review
title: Reference Frontmatter Guide
```

**Validation**:
- Required: Yes
- Max length: 100 characters
- Min length: 5 characters

---

### description (string, ≤500 chars)

Comprehensive description of what the reference contains and when to use it.

**Purpose**: Helps users and AI tools determine relevance without reading the file.

**Format**:
- Explain what the reference contains
- Explain when to use it
- Be specific about the domain
- Use complete sentences
- Third-person perspective

**Examples**:
```yaml
description: Bash command patterns for validating command prerequisites before execution. Includes file existence, git repository, dependency, and state validation checks.

description: Comprehensive quality review framework for skill creation. Use this before packaging or deploying any skill.

description: Specification for YAML frontmatter in skill reference files, including required fields, validation rules, and examples for programmatic discovery.
```

**Validation**:
- Required: Yes
- Max length: 500 characters
- Min length: 20 characters

---

## Optional Fields

### keywords (comma-separated string)

Search terms for enhanced discoverability.

**Purpose**: Improves search results and programmatic matching.

**Format**:
- Comma-separated list
- Lowercase preferred
- Include synonyms and related terms
- Include domain-specific terminology
- 3-10 keywords recommended

**Examples**:
```yaml
keywords: preflight, validation, bash, git checks, dependency checks
keywords: quality, review, validation, scoring, checklists
keywords: frontmatter, metadata, discovery, reference files, yaml
```

**Validation**:
- Required: No (recommended)
- Max length: 200 characters

---

### file-type (string)

Classification of the file type.

**Purpose**: Enables filtering by file type in discovery tools.

**Common values**:
- `reference` - Documentation and reference material (most common)
- `guide` - Step-by-step guides and tutorials
- `specification` - Formal specifications and schemas
- `patterns` - Pattern catalogs and examples

**Examples**:
```yaml
file-type: reference
file-type: guide
file-type: specification
```

**Validation**:
- Required: No
- Recommended: Yes for references/ files

---

### skill (string)

Parent skill name.

**Purpose**: Links reference files to their parent skill.

**Format**:
- Use the skill's directory name
- Lowercase with hyphens

**Examples**:
```yaml
skill: creating-commands
skill: creating-skills
skill: managing-epics
```

**Validation**:
- Required: No
- Recommended: Yes for organizational clarity

---

## Complete Examples

### Minimal Valid Frontmatter

```yaml
---
title: Preflight Patterns
description: Bash patterns for validation checks before command execution.
---
```

### Recommended Complete Frontmatter

```yaml
---
title: Preflight Check Patterns
description: Bash command patterns for validating command prerequisites before execution. Includes file existence, git repository, dependency, and state validation checks.
keywords: preflight, validation, bash, git checks, dependency checks, state checks
file-type: reference
skill: creating-commands
---
```

### Full Example with All Fields

```yaml
---
title: Reference File Frontmatter Guide
description: Specification for YAML frontmatter in skill reference files, including required fields, validation rules, and examples for programmatic discovery.
keywords: frontmatter, metadata, discovery, reference files, yaml, validation
file-type: specification
skill: creating-skills
version: 1.0
author: system
---
```

---

## Validation

### Automated Validation

Run the validation script to check all reference frontmatter:

```bash
python3 scripts/validate_skill.py /path/to/skill --check all
```

The script validates:
- Frontmatter presence in all .md files in references/
- Valid YAML syntax
- Required fields present (title, description)
- Field length limits
- Per-document analysis with specific issues

### Manual Validation Checklist

For each reference file in `references/`:

- [ ] File has YAML frontmatter (starts with `---`, ends with `---`)
- [ ] YAML is valid (no syntax errors)
- [ ] `title` field present and ≤100 characters
- [ ] `description` field present and ≤500 characters
- [ ] `keywords` field present (recommended)
- [ ] `file-type` set to `reference` (recommended)
- [ ] `skill` matches parent skill name (recommended)

---

## Common Issues

### Missing Frontmatter

**Problem**: File has no frontmatter at all.

**Symptom**: Validation error "Missing YAML frontmatter"

**Fix**: Add frontmatter at the top of the file:
```markdown
---
title: [Your Title]
description: [Your Description]
---

# File Content Starts Here
```

---

### Invalid YAML Syntax

**Problem**: Frontmatter has syntax errors.

**Symptoms**:
- Unclosed quotes
- Missing colons
- Incorrect indentation
- Special characters not escaped

**Fix**: Ensure proper YAML syntax:
```yaml
---
title: "Use quotes for titles with: colons"
description: |
  Multi-line descriptions
  use the pipe operator
keywords: comma, separated, no quotes needed
---
```

---

### Missing Required Fields

**Problem**: Frontmatter lacks `title` or `description`.

**Symptom**: Validation error "Missing required field: 'title'" or "'description'"

**Fix**: Add both required fields:
```yaml
---
title: Must Have Title
description: Must have description explaining what this reference contains.
---
```

---

### Field Too Long

**Problem**: `title` >100 chars or `description` >500 chars.

**Symptom**: Validation error "Title too long" or "Description too long"

**Fix**: Condense the content:
```yaml
# Bad (too long)
title: This Is An Extremely Long Title That Exceeds The Maximum Character Limit And Needs To Be Shortened Significantly

# Good (concise)
title: Long Title Shortened

# Bad (too verbose)
description: This is a very detailed description that goes into extensive detail about every single aspect of what this reference file contains, including all the various patterns, examples, use cases, and edge cases that are covered within the documentation...

# Good (concise but complete)
description: Comprehensive guide covering patterns, examples, use cases, and edge cases for the specified domain.
```

---

## Best Practices

1. **Write titles for humans** - They appear in UI and navigation
2. **Write descriptions for search** - Include key terms and use cases
3. **Add keywords generously** - More terms = better discoverability
4. **Be consistent** - Use same format across all references in a skill
5. **Validate early** - Run validation after creating each reference file
6. **Keep metadata current** - Update frontmatter when content changes significantly

---

## Integration with Other Systems

### Discovery Tools

Discovery tools can scan frontmatter to build indexes:

```python
import yaml

def index_references(skill_path):
    """Build searchable index from reference frontmatter."""
    index = []
    for ref_file in (skill_path / "references").glob("*.md"):
        with open(ref_file) as f:
            content = f.read()
            if content.startswith("---"):
                # Extract frontmatter
                fm_end = content.find("---", 3)
                fm = yaml.safe_load(content[3:fm_end])
                index.append({
                    'file': ref_file.name,
                    'title': fm.get('title'),
                    'description': fm.get('description'),
                    'keywords': fm.get('keywords', '').split(', '),
                })
    return index
```

### Documentation Generators

Auto-generate reference documentation:

```python
def generate_toc(skill_path):
    """Generate table of contents from frontmatter."""
    refs = index_references(skill_path)
    toc = "# Reference Files\n\n"
    for ref in sorted(refs, key=lambda r: r['title']):
        toc += f"## {ref['title']}\n"
        toc += f"{ref['description']}\n\n"
        toc += f"[Read more]({ref['file']})\n\n"
    return toc
```

### Search and Filtering

Enable semantic search:

```python
def search_references(query, skill_path):
    """Search references by keywords and description."""
    refs = index_references(skill_path)
    query_lower = query.lower()

    matches = []
    for ref in refs:
        score = 0
        if query_lower in ref['title'].lower():
            score += 10
        if query_lower in ref['description'].lower():
            score += 5
        if query_lower in ' '.join(ref['keywords']).lower():
            score += 3

        if score > 0:
            matches.append((score, ref))

    return [ref for score, ref in sorted(matches, reverse=True)]
```

---

## Summary

Reference frontmatter is **mandatory** for all `.md` files in `references/`:

| Field | Required | Max Length | Purpose |
|-------|----------|------------|---------|
| `title` | ✓ Yes | 100 chars | Display name |
| `description` | ✓ Yes | 500 chars | Purpose and use cases |
| `keywords` | ⊙ Recommended | 200 chars | Search terms |
| `file-type` | ⊙ Recommended | 50 chars | Classification |
| `skill` | ⊙ Recommended | 50 chars | Parent skill |

**Validation**: Run `python3 scripts/validate_skill.py <skill-path> --check all`

**Template**: Use the recommended complete frontmatter template for new reference files.
