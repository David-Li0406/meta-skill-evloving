# Skill Quality Checklist

Use this checklist before finalizing or publishing a skill.

## Contents

- [Pre-Creation Checklist](#pre-creation-checklist)
- [SKILL.md Checklist](#skillmd-checklist)
- [Progressive Disclosure Checklist](#progressive-disclosure-checklist)
- [Splitting Large Skills](#splitting-large-skills)
- [Testing Checklist](#testing-checklist)

---

## Pre-Creation Checklist

Before writing the skill:

- [ ] Identified 3-5 concrete usage examples
- [ ] Listed trigger phrases users would say
- [ ] Determined what context agent doesn't already have
- [ ] Planned which resources to include (scripts/references/assets)
- [ ] Confirmed this isn't duplicate of existing skill

---

## SKILL.md Checklist

### Frontmatter

- [ ] `name` is lowercase with hyphens only
- [ ] `name` is 1-64 characters
- [ ] `name` matches parent directory name
- [ ] `name` has no leading/trailing/consecutive hyphens
- [ ] `description` is non-empty
- [ ] `description` is under 1024 characters (aim for ~200)
- [ ] `description` includes what the skill does
- [ ] `description` includes "Use when..." triggers
- [ ] `description` includes natural keywords
- [ ] `description` uses third person ("Creates..." not "I help...")

### Body Content

- [ ] No "When to Use This Skill" section (belongs in description)
- [ ] Uses imperative form ("Create..." not "Creating...")
- [ ] Brief overview (2-3 sentences max)
- [ ] Core workflow is clear and actionable
- [ ] Code examples are concise and working
- [ ] No verbose explanations of common knowledge
- [ ] No README, CHANGELOG, or auxiliary files
- [ ] Under 500 lines total

### References

- [ ] References are one level deep (no nested references)
- [ ] Each reference file has clear purpose described in SKILL.md
- [ ] Reference files under 100 lines each (or have TOC)
- [ ] No duplicate content between SKILL.md and references
- [ ] Relative paths used: `[file](references/file.md)`

---

## Progressive Disclosure Checklist

### Level 1: Metadata (~100 tokens)

- [ ] Name is descriptive and unique
- [ ] Description captures all trigger scenarios
- [ ] Description is optimized for discovery

### Level 2: SKILL.md (<5k tokens)

- [ ] Contains only essential workflow
- [ ] Detailed content moved to references
- [ ] Links clearly describe when to read each reference

### Level 3: Resources (as needed)

- [ ] Scripts are tested and working
- [ ] References are focused and self-contained
- [ ] Assets are ready to use (no setup needed)

---

## Splitting Large Skills

When a skill exceeds 500 lines or feels unwieldy, follow this process:

### Step 1: Identify Separable Content

Look for:

- **Variant-specific details**: Framework options, platform differences
- **Extensive examples**: Full working code samples
- **Reference material**: API docs, schemas, field definitions
- **Advanced patterns**: Edge cases, complex scenarios
- **Conditional content**: Only needed for specific use cases

### Step 2: Plan the Split

Decide what stays in SKILL.md:

- Core workflow (essential steps)
- Quick start example
- Navigation to reference files
- Most common use case

Decide what moves to references/:

- Detailed examples → `references/examples.md`
- API/schema docs → `references/api.md`
- Advanced patterns → `references/patterns.md`
- Framework variants → `references/{framework}.md`

### Step 3: Extract Content

1. Create the reference file with extracted content
2. Add table of contents if file > 100 lines
3. Remove content from SKILL.md
4. Add navigation link with description:
   ```markdown
   See [references/patterns.md](references/patterns.md) for advanced patterns including composition and transactions.
   ```

### Step 4: Verify No Duplication

Content must exist in exactly ONE place:

- SKILL.md for core workflow
- Reference files for detailed/variant content

### Split Patterns

**Pattern: Examples Extraction**

```
Before: 600-line SKILL.md with 15 examples
After:
├── SKILL.md (150 lines, 2 key examples)
└── references/
    └── examples.md (full examples collection)
```

**Pattern: Framework Variants**

```
Before: 800-line SKILL.md covering React, Vue, Angular
After:
├── SKILL.md (100 lines, framework selection)
└── references/
    ├── react.md
    ├── vue.md
    └── angular.md
```

**Pattern: Domain Organization**

```
Before: 700-line SKILL.md with all database schemas
After:
├── SKILL.md (80 lines, overview + navigation)
└── references/
    ├── users.md (user tables)
    ├── orders.md (order tables)
    └── products.md (product tables)
```

---

## Testing Checklist

### Before Finalizing

- [ ] Triggered skill with natural phrases from description
- [ ] Verified correct skill loads (not a similar one)
- [ ] Tested main workflow end-to-end
- [ ] Confirmed code examples work
- [ ] Tested any bundled scripts
- [ ] Verified reference files load correctly

### After Real Usage

- [ ] Observed agent using the skill on real tasks
- [ ] Noted any struggles or confusion
- [ ] Identified missing context
- [ ] Updated skill based on observations
- [ ] Re-tested after changes

### Quality Verification

Run through these scenarios:

1. Ask for the task using exact description keywords
2. Ask for the task using synonyms/variations
3. Ask for a related but different task (should NOT trigger)
4. Complete a full task using only the skill's guidance

---

## Common Issues

### Skill Doesn't Trigger

- Description too vague
- Missing trigger keywords
- Keywords don't match natural phrasing

**Fix**: Add more specific "Use when..." triggers and natural keywords.

### Agent Ignores Instructions

- Instructions buried in verbose text
- Critical steps not emphasized
- Too many options without clear recommendation

**Fix**: Make instructions concise, use imperative form, provide clear defaults.

### Agent Reads Wrong Reference

- Navigation unclear
- Multiple files cover similar topics
- Missing description of when to read each

**Fix**: Add clear descriptions: "See X for Y scenario" not just "See X".

### Inconsistent Results

- Too much freedom in instructions
- Missing constraints for critical steps
- No examples of expected output

**Fix**: Add more specific patterns, constraints, and output examples.
