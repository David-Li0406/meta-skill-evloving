---
title: "Documentation Quality Checklist"
description: "Comprehensive checklist for validating AI-ready documentation quality before publishing"
skill: writing-ai-docs
type: reference
created: 2025-10-28
lastUpdated: 2025-10-28
---

# Documentation Quality Checklist

Use this checklist before finalizing any documentation to ensure it meets AI-ready standards.

## Frontmatter Validation

- [ ] YAML frontmatter present (enclosed in `---`)
- [ ] `title` field present and under 70 characters
- [ ] `description` field present (1-2 sentences, 100-200 chars)
- [ ] `type` field specified (api-endpoint, guide, tutorial, reference, concept, troubleshooting)
- [ ] `created` field in ISO 8601 format (YYYY-MM-DD)
- [ ] `lastUpdated` field in ISO 8601 format (YYYY-MM-DD)
- [ ] Document type-specific fields included (method/endpoint for API, difficulty/duration for tutorials)
- [ ] Optional discovery fields used appropriately (when-to-read, related-to, code-references)

## Structure Validation

- [ ] ONE H1 heading that matches title
- [ ] Strict heading hierarchy (H1→H2→H3, no skipped levels)
- [ ] Logical section progression
- [ ] Opening paragraph states purpose and audience
- [ ] Prerequisites section present and explicit
- [ ] Each major section has an H2
- [ ] Subsections properly nested under H2 with H3

## Content Validation

- [ ] Consistent terminology (ONE term per concept)
- [ ] Explicit language (no vague pronouns like "it", "this", "they" without clear antecedent)
- [ ] Self-contained sections (each section comprehensible independently)
- [ ] Prerequisites listed explicitly with versions/requirements
- [ ] Related information grouped together (not scattered)
- [ ] Context repeated in major sections (doesn't assume prior sections read)
- [ ] Document under 1000 lines (ideal for chunking)
- [ ] Document under 4000 tokens (~16,000 characters preferred)

## Code Examples Validation

- [ ] All code in fenced blocks (not inline in prose)
- [ ] All code blocks have language tags (bash, javascript, python, yaml, json, http, etc.)
- [ ] No commands embedded in sentences
- [ ] Examples are complete and runnable
- [ ] Expected output shown for examples
- [ ] Code includes context-rich comments
- [ ] Error cases covered in examples

## File Naming Validation

- [ ] Filename is lowercase-kebab-case.md
- [ ] Filename under 50 characters
- [ ] Filename descriptive (not abbreviated)
- [ ] No spaces, underscores, or capital letters (except README.md, CHANGELOG.md, etc.)
- [ ] Filename matches document content/purpose

## AI-Readability Validation

- [ ] Sections self-contained with necessary context
- [ ] Definitions near their applications
- [ ] Prerequisites adjacent to procedures
- [ ] No scattered related concepts
- [ ] Common issues/troubleshooting section included
- [ ] Next steps or related documentation provided
- [ ] Semantic proximity maintained (related info physically close)

## Automated Validation

Run all validation scripts:

```bash
# Check documentation quality (includes basic frontmatter validation)
python scripts/check_doc_quality.py your-doc.md

# Lint markdown syntax
bash scripts/lint_markdown.sh your-doc.md

# Check for broken links
bash scripts/check_links.sh your-doc.md
```

**Note:** For comprehensive frontmatter validation across your entire docs folder, use the maintaining-docs skill with `Skill(command='maintaining-docs')`. This provides full documentation structure validation including advanced frontmatter schema checking.

## Auto-Fix Common Issues

Fix linting issues automatically:

```bash
npx markdownlint-cli --config .markdownlint.json --fix your-doc.md
```

## Document Type-Specific Checks

### API Reference Documentation

- [ ] Method in title (GET, POST, PUT, DELETE, PATCH)
- [ ] Endpoint path in title
- [ ] Request section includes endpoint URL, headers, parameters
- [ ] Response section includes success response with status code
- [ ] Error responses documented with status codes and solutions
- [ ] curl example included and tested
- [ ] Related endpoints linked
- [ ] Parameters documented with type, required, description

### Tutorial Documentation

- [ ] Difficulty level specified (beginner, intermediate, advanced)
- [ ] Estimated duration provided
- [ ] Prerequisites listed explicitly
- [ ] Expected outcomes/learning objectives stated
- [ ] Clear numbered steps
- [ ] Verification steps included
- [ ] Common issues section present
- [ ] Next steps provided

### How-To Guide Documentation

- [ ] Task-oriented focus (how to accomplish X)
- [ ] Prerequisites stated upfront
- [ ] Clear numbered steps
- [ ] Each step has verification
- [ ] Expected results shown
- [ ] Troubleshooting section included
- [ ] Related guides linked

### Reference Documentation

- [ ] Comprehensive coverage of topic
- [ ] Consistent formatting throughout
- [ ] Table format for structured data
- [ ] Alphabetical or logical ordering
- [ ] Version applicability specified
- [ ] Examples for each major item

### Concept/Explanation Documentation

- [ ] Clear conceptual overview
- [ ] Why/when context provided
- [ ] Diagrams or examples included
- [ ] Comparison with alternatives (if applicable)
- [ ] Use cases documented
- [ ] Best practices section
- [ ] Related concepts linked

### Troubleshooting Documentation

- [ ] Problem/symptom clearly described
- [ ] Cause explained
- [ ] Solution with step-by-step instructions
- [ ] Verification steps included
- [ ] Prevention tips provided
- [ ] Related issues linked

## Common Anti-Patterns to Avoid

### Structure Anti-Patterns

- ❌ Skipped heading levels (H1→H3 without H2)
- ❌ Multiple H1 headings in one document
- ❌ Missing frontmatter
- ❌ Invalid YAML syntax in frontmatter

### Content Anti-Patterns

- ❌ Inline code without formatting (commands in prose)
- ❌ Inconsistent terminology (API key / access token / auth credential)
- ❌ Vague references ("it", "this", "they" without antecedent)
- ❌ Scattered information (definition separated from usage)
- ❌ Missing prerequisites
- ❌ Assuming prior knowledge without stating it

### Code Anti-Patterns

- ❌ Code blocks without language tags
- ❌ Incomplete examples (won't run as-is)
- ❌ No expected output shown
- ❌ Missing error handling in examples
- ❌ Pseudocode instead of real code

### File Anti-Patterns

- ❌ Filename with spaces or uppercase
- ❌ Vague filename (install.md, api.md, docs.md)
- ❌ Abbreviated filename (tut-1st-app.md)
- ❌ Inconsistent naming across documentation set

## Validation Frequency

**Before commit:**
- Run all 4 validation scripts
- Fix all errors and warnings
- Auto-fix markdown linting issues

**During review:**
- Verify checklist items manually
- Check for context and clarity
- Test all code examples
- Verify all links work

**After updates:**
- Update `lastUpdated` field
- Re-run validation scripts
- Check if related docs need updates

## Quality Thresholds

**Minimum standards:**

- All validation scripts pass with zero errors
- All checklist items checked
- No broken links
- All code examples tested
- Consistent terminology throughout

**Excellence standards:**

- Self-contained sections work when read independently
- Examples include both success and error cases
- Troubleshooting covers common issues
- Related documentation cross-referenced
- Next steps guide reader's journey

## Red Flags (Fix Immediately)

If you see any of these, stop and fix before proceeding:

- 🚨 Bad filename (spaces, capitals, underscores, abbreviations)
- 🚨 Skipped heading levels (H1→H3)
- 🚨 Multiple terms for same concept
- 🚨 Inline code without blocks
- 🚨 Vague pronouns ("it", "this", "they")
- 🚨 Related content scattered across document
- 🚨 Missing frontmatter fields
- 🚨 Code blocks without language tags
- 🚨 Broken links or invalid references
- 🚨 Commands that won't run as written

## Success Indicators

Your documentation is AI-ready when:

✅ All validation scripts pass
✅ All checklist items complete
✅ Document under 1000 lines
✅ Sections work independently
✅ Consistent terminology throughout
✅ All code blocks properly formatted
✅ Prerequisites explicitly stated
✅ Examples complete and tested
✅ Common issues documented
✅ Clear next steps provided

## Resources

See also:

- **references/ai-ready-single-file.md** - Core AI-ready principles
- **references/examples.md** - Before/after examples
- **references/frontmatter-schemas.md** - Frontmatter templates
- **references/api-doc-patterns.md** - API documentation patterns
