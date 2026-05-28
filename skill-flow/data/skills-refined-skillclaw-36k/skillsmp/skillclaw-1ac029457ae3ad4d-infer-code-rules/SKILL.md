---
name: infer-code-rules
description: Use this skill when you need to extract design patterns and conventions from a codebase and document them as local rules.
---

# Infer Code Rules

This skill extracts design patterns and conventions from a codebase and records them as local rules. It is not triggered automatically; it must be invoked explicitly from another skill or through a command.

## Rule File Placement

Place rule files in the following format:

`.claude/rules/local.{category}.md`

Examples:

- `local.react.components.md` - Component patterns
- `local.react.routes.md` - Route patterns
- `local.ui-design.md` - UI design patterns
- `local.tests.md` - Test patterns

The `local.` prefix indicates that these rules are specific to the project.

## Execution Steps

### Step 1: Review Existing Rules

First, read all existing rule files to understand their contents.

```bash
ls .claude/rules/
```

Review the contents of all files to create a list of existing rules.

### Step 2: Explore the Codebase

Explore the target directories to collect patterns.

Examples of target directories:

- `app/routes/` - Route patterns
- `app/components/` - Component patterns
- `app/hooks/` - Hook patterns

### Step 3: Extract Patterns

Consider the following aspects during exploration:

- Component structure
- Usage of UI libraries
- Layout patterns
- Form structures
- Loading/error states

### Step 4: Compare with Existing Rules

Compare the extracted patterns with existing rules to eliminate duplicates.

Criteria for determining duplicates:

- Describing the same concept (e.g., "use type", "do not use interface")
- Describing the same naming convention (e.g., "kebab-case", "hyphen-separated")
- Describing the same file structure (e.g., "one file one function", "one file one component")

Actions to take:

- If duplicates are found → do not add
- If existing rules need clarification or supplementation → reference the existing rules
- If there are contradictions → ask the user for confirmation

### Step 5: Create or Update Rule Files

After user approval, create or update the rule files.

## Rule File Format

```markdown
---
paths: "app/components/**/*.tsx"
---

# Local Component Rules

## Section Name

Description.

Code examples (only if necessary).
```

Specify the applicable scope in the `paths` front matter.

## Notes

- Always confirm with the user if there are contradictions with existing rules.
- Keep code examples concise.
- Document the reasons for each rule.
- Follow the criteria for rule additions outlined in `.workflow.md`.

## Content to Add to Local Rules

- Project-specific patterns (e.g., usage of useHref, pageMetaFunction)
- Specific implementation patterns not covered by existing rules (e.g., initialization order of hooks)
- Framework-specific conventions (e.g., loader patterns in React Router)

## Content Not to Add to Local Rules

- General conventions already covered in existing rule files
- Language-level conventions (type vs interface, naming conventions, file structures)
- General programming principles (SOLID, functional programming)