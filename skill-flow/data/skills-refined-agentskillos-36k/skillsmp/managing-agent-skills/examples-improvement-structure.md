# Skill Improvement Examples: Structure and Organization

Before/After transformations for improving file structure, organization, and progressive disclosure.

## Transformation 1: Adding Progressive Disclosure

### ❌ Before (Monolithic)
```
api-integration/
└── SKILL.md (900 lines with all details)
```

**SKILL.md contains:**
- Workflow (50 lines)
- Authentication specs (200 lines)
- All API endpoints (300 lines)
- Error codes (150 lines)
- Rate limiting details (100 lines)
- Examples (100 lines)

**Problems:**
- Way over 500 line target
- Information overload
- Hard to find specific information
- All details loaded even when not needed

---

### ✅ After (Progressive Disclosure)
```
api-integration/
├── SKILL.md (250 lines - workflow + references)
├── authentication.md (200 lines)
├── endpoints.md (300 lines)
├── error-handling.md (150 lines)
└── examples.md (100 lines)
```

**SKILL.md (focused):**
```markdown
# API Integration Workflow

## Step 1: Authenticate
- Identify auth method (OAuth2, API Key, JWT)
- **For detailed authentication specs, see authentication.md**
- Verify credentials valid

## Step 2: Call Endpoint
- Construct request from user requirements
- **For complete endpoint list, see endpoints.md**
- Execute request with proper headers

## Step 3: Handle Response
- Parse response data
- **If errors occur, see error-handling.md**
- Return formatted results

## When to Load Supporting Files
- **authentication.md**: When setting up auth or troubleshooting auth errors
- **endpoints.md**: When you need specific endpoint parameters or response schemas
- **error-handling.md**: When API returns error codes
- **examples.md**: When user needs usage examples
```

**Improvements:**
- ✅ SKILL.md under 500 lines
- ✅ Clear workflow without excessive detail
- ✅ Guidance on when to load each file
- ✅ Details loaded only when needed

---

## Transformation 2: Improving File Organization

### ❌ Before
```markdown
## See Also

For more information:
- guide.md
- details.md
- reference.md
- specs.md
- help.md
```

**Problems:**
- No context on what each file contains
- No guidance on when to load
- Unclear purpose of each file

---

### ✅ After
```markdown
## Supporting Resources

Load these files when needed:

- **validation-rules.md**: Load when validating data or results. Contains specific criteria for data quality, calculation ranges, and output requirements.

- **calculation-reference.md**: Load when you need formulas for specific ratios or metrics. Contains mathematical definitions and company-specific adjustments.

- **error-handling.md**: Load when script errors occur or calculations fail. Contains common error scenarios and resolution steps.

- **examples.md**: Load when user requests examples or you need to demonstrate usage. Contains sample inputs, calculations, and outputs.

**When to Load Multiple Files:**
- Initial setup: validation-rules.md + calculation-reference.md
- Troubleshooting: error-handling.md
- User education: examples.md
```

**Improvements:**
- ✅ Clear purpose for each file
- ✅ Guidance on when to load
- ✅ Context about what each contains
- ✅ Multi-file loading scenarios

---

## Key Patterns: Structure and Organization Improvements

### Progressive Disclosure Best Practices

**When to split SKILL.md:**
- File exceeds 500 lines
- Contains detailed reference information
- Has multiple distinct sections
- Includes extensive examples

**How to split:**
1. Keep workflow in SKILL.md (high-level steps)
2. Move detailed specs to dedicated files
3. Move examples to examples.md
4. Move reference data to reference.md

**File naming conventions:**
- `validation-rules.md` - Specific validation criteria
- `calculation-reference.md` - Formulas and calculations
- `error-handling.md` - Error scenarios and fixes
- `examples.md` - Usage examples
- `templates/` - Template files (subdirectory)
- `scripts/` - Executable scripts (subdirectory)

### Reference Organization

**Clear file purposes:**
```markdown
## Progressive Disclosure References

- **file-name.md**: When to load + what it contains

Example:
- **authentication.md**: Load when setting up auth or troubleshooting auth errors. Contains OAuth2 flows, API key management, and token refresh procedures.
```

**Anti-patterns:**
- ❌ "See also: guide.md" (no context)
- ❌ "More info in docs/" (too vague)
- ❌ "Load reference files as needed" (no specifics)

**Good patterns:**
- ✅ "Load validation-rules.md when validating input data. Contains field requirements and format specifications."
- ✅ "If errors occur, load error-handling.md for resolution steps."
- ✅ "For formula details, load calculation-reference.md."

### File Structure Guidelines

**Target sizes:**
- SKILL.md: Under 500 lines (ideally 250-350)
- Supporting files: 100-300 lines each
- Reference files: 200-400 lines max
- Example files: 100-200 lines

**Semantic splits:**
- Split by **purpose** (not arbitrary line counts)
- Group related information together
- Keep one topic per file
- Maintain clear boundaries

**One level deep:**
```
✅ Good: SKILL.md → reference.md (one level)
❌ Bad: SKILL.md → guide.md → details.md → specs.md (deep nesting)
```

### Supporting File Template

```markdown
# [File Purpose]

[Brief description of what this file contains and when to use it]

## Section 1
[Content organized logically]

## Section 2
[More content]

## Quick Reference
[Optional: Key information at a glance]
```

### Directory Structure Examples

**Simple skill (single domain):**
```
skill-name/
├── SKILL.md (main workflow)
├── reference.md (detailed specs)
└── examples.md (usage examples)
```

**Complex skill (multiple capabilities):**
```
skill-name/
├── SKILL.md (main workflow)
├── validation-rules.md
├── calculation-reference.md
├── error-handling.md
├── examples.md
├── templates/
│   ├── report-template.md
│   └── config-template.json
└── scripts/
    ├── calculate_ratios.py
    └── validate_input.py
```

## Summary: Structure Improvement Patterns

### From Monolithic to Modular
1. Identify natural content boundaries
2. Split into focused files (100-400 lines each)
3. Keep SKILL.md as high-level workflow
4. Add clear loading guidance for each file

### From Vague to Clear References
1. Replace "see also" with specific loading guidance
2. Explain what each file contains
3. Specify when to load each file
4. Group related files by usage scenario

### From Flat to Organized
1. Use subdirectories for templates and scripts
2. Name files descriptively (purpose-focused)
3. Keep references one level deep
4. Maintain consistent naming conventions

### Context Efficiency (AI Optimization)
**Progressive disclosure primarily benefits AI:**
- Load only what's needed → saves context tokens
- Clear file names → faster decisions without reading
- Semantic splits → targeted information retrieval
- Smaller files → reduced re-reading overhead

**Token savings example:**
- Before: Load 900-line SKILL.md (3000 tokens) to find one detail
- After: Load specific 200-line file (650 tokens)
- **Savings: 2350 tokens per targeted read**
