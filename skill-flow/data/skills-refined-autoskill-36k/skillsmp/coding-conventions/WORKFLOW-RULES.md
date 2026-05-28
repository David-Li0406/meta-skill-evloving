# Workflow Coding Conventions

Rules for writing and structuring workflow documents (`.windsurf/workflows/*.md`).

## Principle

**ASANAPAP**: As Short As Necessary, As Precise As Possible.

Workflows should be concise but unambiguous. Remove redundancy, keep precision.

## Formatting

- Format workflow references as inline code: `/verify`, `/research`, `/recap`
- Workflows implement AGEN verbs but should NOT contain `[VERB]` references in their content
  - BAD: `## Verb: [COMMIT]` or `Implements [COMMIT] verb`
  - GOOD: Use plain English in workflow body. Or reference specific `/workflow` like this.
- Frontmatter should only contain `description` field
  - BAD: `phase: DESIGN` or other extra fields
  - GOOD: Only `description: ...` in frontmatter
- No redundant `## Usage` sections that just show the workflow command
  - BAD: `## Usage` with just `/continue` in a code block
  - GOOD: Usage section with examples showing parameters: `/build "Add auth API"`
  - Workflow name already indicates basic usage; only add if showing parameters
- No replication of higher-order rules defined elsewhere
  - BAD: Listing all document types in a workflow (duplicates `devsystem-core.md`)
  - GOOD: Reference the source: "See `devsystem-core.md` section X for details"
  - Keep workflows focused on steps, not definitions

## Structure (Recommended)

Prefer separating GLOBAL-RULES and CONTEXT-SPECIFIC sections:

```markdown
# [Workflow Name] Workflow

## Usage
...

## GLOBAL-RULES

Apply to ALL contexts:
- Rule 1
- Rule 2

# CONTEXT-SPECIFIC

## Context A
- Context-specific rule 1

## Context B
- Context-specific rule 2
```

**Reference**: See `/verify` workflow as canonical example.

## Quality Checks

When verifying workflows, look for:

- **Ambiguities** - Unclear instructions that could be interpreted multiple ways
- **Term conflicts** - Same concept named differently, or different concepts with same name
- **Underspecified behavior** - Missing edge cases, undefined outcomes, gaps in logic
- **Outdated references** - Broken links to workflows, skills, rules, concepts, or states that no longer exist or have been renamed

**Cross-reference checklist:**
- [ ] All `/workflow` references exist in `.windsurf/workflows/`
- [ ] All `@skill` references exist in `.windsurf/skills/`
- [ ] All `[VERB]` references are valid AGEN verbs
- [ ] All `[STATE]` references are defined in ID-REGISTRY.md
- [ ] All document references (`_SPEC_*.md`, etc.) use correct naming conventions

## Benefits

- **Clarity**: Global rules read once, context rules read as needed
- **Maintainability**: Easy to add new contexts without duplicating global rules
- **Consistency**: Same pattern across all complex workflows
