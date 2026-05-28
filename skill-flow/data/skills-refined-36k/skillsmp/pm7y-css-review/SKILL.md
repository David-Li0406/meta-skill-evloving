---
name: pm7y-css-review
description: Reviews CSS/SCSS changes in the current branch for over-specificity, missed reuse opportunities, and over-engineered abstractions. Produces analysis findings and uses pm7y-ralph-planner to generate TASKS.md for autonomous execution. Use when reviewing CSS changes before commit or PR, or to audit existing styles. Supports @file syntax to target specific files.
allowed-tools: Read, Write, Grep, Glob, Bash, Task
---

# CSS/SCSS Review Skill

Reviews CSS/SCSS changes for unnecessary complexity and missed reuse opportunities. Produces analysis findings that are passed to `pm7y-ralph-planner` for TASKS.md generation.

---

## Overview

This skill analyzes CSS/SCSS files for three categories of issues:

- **Over-specificity** - Complex selectors that could be simpler
- **Missing reuse** - New styles that duplicate existing utilities
- **Over-engineered abstractions** - Unnecessary mixins/variables/extends

**Output:** Analysis findings passed to `pm7y-ralph-planner`, which generates a `TASKS.md` file with validation requirements and learnings tracking for autonomous execution via `pm7y-ralph-loop`.

**When to use:**

- Before committing CSS/SCSS changes
- During PR review of style changes
- Auditing existing stylesheets for cleanup
- After rapid UI development to assess CSS debt

---

## Usage

```
/pm7y-css-review                      # Review all CSS/SCSS changes in branch
/pm7y-css-review @path/to/file.scss   # Review specific file only
```

---

## Review Process

### Step 1: Determine Scope

Parse arguments to determine which files to review:

**If @file argument provided:**
- Extract the file path after the @ symbol
- Verify the file exists and is CSS/SCSS
- Review only that file

**If no arguments (default):**
- Run `git diff main...HEAD --name-only` to find files changed in branch
- Also check `git diff --name-only` for staged/unstaged changes
- Filter to only `.css` and `.scss` files
- If no CSS/SCSS files changed, report "No CSS/SCSS changes found" and stop

### Step 2: Build Style Inventory

Scan the project to understand existing styles:

**Find all style files:**
```bash
# Find all CSS and SCSS files in project (exclude node_modules, dist, build)
find . -type f \( -name "*.css" -o -name "*.scss" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*" \
  -not -path "*/.next/*"
```

**Extract existing patterns:**

For each style file, identify and record:
- **CSS classes** - All `.class-name` selectors
- **SCSS variables** - All `$variable-name` definitions
- **SCSS mixins** - All `@mixin mixin-name` definitions
- **Common property-value pairs** - Frequently used declarations

Store this inventory mentally for comparison during analysis.

### Step 3: Detect Frameworks

Check for CSS frameworks to understand available utilities:

**Tailwind CSS:**
- Check for `tailwind.config.js` or `tailwind.config.ts`
- Look for `@tailwind` directives in CSS files
- If found, note common utilities: flex, grid, spacing (p-*, m-*), colors, etc.

**Bootstrap:**
- Check for Bootstrap in `package.json` dependencies
- Look for Bootstrap imports in SCSS files
- If found, note utility classes: d-flex, justify-content-*, text-*, etc.

**Custom utility systems:**
- Look for files named `utilities.css`, `helpers.scss`, `_utils.scss`
- Identify utility class naming patterns

### Step 4: Analyze Changed Files

For each file in scope, read the content and check for issues:

#### Over-specificity Detection

| Issue | Pattern | Severity |
|-------|---------|----------|
| Deep nesting | Selectors with > 3 levels (e.g., `.a .b .c .d`) | Medium |
| ID selectors | `#id` in selectors | Medium |
| `!important` | Any `!important` declaration | Medium |
| Qualified selectors | Element + class (e.g., `div.button`) | Low |
| Over-qualified | Multiple classes chained (e.g., `.btn.btn-primary.btn-large`) | Low |

#### Missing Reuse Detection

| Issue | Pattern | Severity |
|-------|---------|----------|
| Duplicate utility | Declaration matches existing utility class | High |
| Framework duplicate | Declaration available as framework utility | High |
| Repeated values | Magic numbers used instead of variables | Medium |
| Similar blocks | Near-identical declaration blocks elsewhere | Medium |

#### Over-engineered Abstraction Detection

| Issue | Pattern | Severity |
|-------|---------|----------|
| Single-use mixin | `@mixin` with only one `@include` | Medium |
| Single-use variable | `$variable` used only once (except colors) | Medium |
| `@extend` usage | Any use of `@extend` | Low |
| Deep SCSS nesting | > 3 levels of SCSS nesting | Low |

#### Existing Pattern Violation Detection

This detection leverages the pattern inventory from Step 2 to identify when new/changed code violates or duplicates established patterns. Use the same discovery approach as `pm7y-scss-patterns` skill.

| Issue | Pattern | Severity |
|-------|---------|----------|
| Duplicate mixin | New mixin does the same thing as existing mixin with different name | High |
| Duplicate variable | New variable serves same purpose as existing variable (e.g., two `$primary-color` and `$brand-color` both #3B82F6) | High |
| Duplicate utility class | New utility class provides same styles as existing utility | High |
| Naming convention violation | New class doesn't follow established naming pattern (BEM, OOCSS, etc.) | Medium |
| Variable value mismatch | Using hardcoded value when matching variable exists | Medium |
| Inconsistent mixin usage | Not using established mixin where it would apply | Low |

**Detection approach:**

1. **Duplicate mixins:** Compare new `@mixin` definitions against existing mixins. Two mixins are duplicates if they produce equivalent CSS output (same properties and values). Flag when a new mixin's body matches an existing mixin's body.

2. **Duplicate variables:** Compare new `$variable` definitions against existing variables. Flag when:
   - Two variables have the same value (exact match)
   - Two color variables are visually identical (hex/rgb equivalence)
   - Two spacing variables resolve to the same pixel value

3. **Duplicate utility classes:** Compare new class definitions against existing utilities. Flag when a new class has the same declarations as an existing utility class.

4. **Naming convention violations:** If the codebase uses BEM (`.block__element--modifier`), flag classes that don't follow this pattern. Similarly for other conventions detected in the inventory phase.

**Example violations:**

```scss
// DUPLICATE MIXIN - existing @mixin flex-center does the same thing
@mixin center-content {
  display: flex;
  justify-content: center;
  align-items: center;
}

// DUPLICATE VARIABLE - $color-primary already equals #3B82F6
$brand-blue: #3B82F6;

// DUPLICATE UTILITY - .flex-center already exists with same styles
.centered {
  display: flex;
  justify-content: center;
  align-items: center;
}

// NAMING CONVENTION VIOLATION - project uses BEM but this doesn't
.cardHeader { } // Should be .card__header
```

### Step 5: Pass Findings to pm7y-ralph-planner

After completing the analysis, invoke the `pm7y-ralph-planner` agent using the Task tool. Pass your findings as structured input so the planner can generate a proper TASKS.md with validation requirements and learnings tracking.

**Invoke pm7y-ralph-planner with this prompt:**

```
Generate a TASKS.md for CSS/SCSS refactoring.

## Goal
Fix CSS/SCSS issues identified during code review.

## Project Context
- **Branch:** [current branch name]
- **Files reviewed:** [count]
- **Issues found:** [X total] ([Y] high, [Z] medium, [W] low)
- **CSS Framework:** [Tailwind/Bootstrap/Custom/None]
- **Build command:** [detected build command, e.g., npm run build]
- **Lint command:** [detected lint command, if any]

## Findings

### HIGH Priority (should be fixed first)

- **[filepath]:[line]** - [Issue type]: [Description]. **Fix:** [Specific action to take].

[Repeat for each high priority finding]

### MEDIUM Priority

- **[filepath]:[line]** - [Issue type]: [Description]. **Fix:** [Specific action to take].

[Repeat for each medium priority finding]

### LOW Priority (fix if time permits)

- **[filepath]:[line]** - [Issue type]: [Description]. **Fix:** [Specific action to take].

[Repeat for each low priority finding]

## Notes
- Each fix should be verified by running the build/lint commands
- Verify changes don't break existing styles visually
```

**Example findings to pass:**

```markdown
### HIGH Priority

- **src/components/Card.scss:42** - Duplicate utility: `display: flex; justify-content: center; align-items: center;` duplicates existing `.flex-center` class. **Fix:** Remove these properties and add `@extend .flex-center;` or apply `.flex-center` class in HTML.
- **src/styles/modal.scss:18** - Framework duplicate: `margin-left: auto; margin-right: auto;` available as Tailwind `mx-auto`. **Fix:** Remove CSS properties and add `mx-auto` class to element in JSX/HTML.

### MEDIUM Priority

- **src/components/Header.scss:67** - Deep nesting: Selector `.header .nav .menu .item a` has 5 levels. **Fix:** Flatten to `.header-nav-link` or similar BEM-style class.
- **src/styles/buttons.scss:23** - Single-use mixin: `@mixin button-shadow` is only used once. **Fix:** Inline the mixin content directly into `.primary-button`.
- **src/styles/utils.scss:45** - Duplicate mixin: `@mixin center-content` produces same CSS as existing `@mixin flex-center` in `_mixins.scss:12`. **Fix:** Remove `@mixin center-content` and use `@include flex-center` instead.
- **src/components/Card.scss:8** - Duplicate variable: `$brand-blue: #3B82F6` duplicates existing `$color-primary` in `_variables.scss:5`. **Fix:** Remove `$brand-blue` and use `$color-primary`.

### LOW Priority

- **src/styles/layout.scss:89** - Over-qualified selector: `div.container` can be simplified. **Fix:** Remove element qualifier, use `.container` only.
- **src/components/Modal.scss:15** - Naming convention violation: `.modalHeader` doesn't follow BEM pattern used in codebase. **Fix:** Rename to `.modal__header`.
```

**Why use pm7y-ralph-planner:**

The planner will:
1. Add proper validation requirements (build, lint checks)
2. Include the Learnings Log section for preserving insights across iterations
3. Add the iteration workflow guidance
4. Format tasks for optimal autonomous execution

### Step 6: Report Summary and Stop

After invoking pm7y-ralph-planner, output a brief summary:

```
CSS Review Complete

Files reviewed: N
Issues found: X (Y high, Z medium, W low)

TASKS.md generated via pm7y-ralph-planner - ready for ralph-loop execution:
  pwsh ./ralph-loop.ps1 -PromptFile TASKS.md
```

Then STOP. Do not attempt to fix any issues.

---

## Issue Examples

### Over-specificity Examples

**Deep nesting:**
```scss
// Bad - 4 levels
.header .nav .menu .item a { color: blue; }

// Recommendation: Simplify to
.header-nav-link { color: blue; }
```

**ID selector:**
```scss
// Bad
#main-content .sidebar { width: 300px; }

// Recommendation: Use class instead
.main-content .sidebar { width: 300px; }
```

**!important:**
```scss
// Bad
.modal { z-index: 1000 !important; }

// Recommendation: Fix specificity issue at source
```

### Missing Reuse Examples

**Duplicate utility:**
```scss
// Bad - if .flex-center exists
.card { display: flex; justify-content: center; align-items: center; }

// Recommendation: Use existing .flex-center class
```

**Framework duplicate (Tailwind):**
```scss
// Bad - when using Tailwind
.button { margin-left: auto; margin-right: auto; }

// Recommendation: Use Tailwind's mx-auto class
```

### Over-engineered Examples

**Single-use mixin:**
```scss
// Bad
@mixin card-shadow {
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.card { @include card-shadow; }

// Recommendation: Inline the styles
.card { box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
```

**Single-use variable:**
```scss
// Bad
$card-padding: 16px;
.card { padding: $card-padding; }

// Recommendation: Use value directly or existing spacing variable
```

---

## Critical Rules

### Rule 1: Inventory Before Analysis

ALWAYS build the style inventory before analyzing changed files. Without knowing what exists, you cannot identify reuse opportunities.

### Rule 2: Framework Awareness

ALWAYS check for CSS frameworks. Tailwind and Bootstrap provide extensive utilities that should be preferred over custom CSS.

### Rule 3: Line Numbers Required

EVERY finding MUST include specific line number(s). Vague references like "in this file" are not acceptable.

### Rule 4: Actionable Fix Instructions

EVERY finding MUST include a concrete **Fix:** instruction. Name specific existing classes, variables, or utility names when suggesting reuse. The fix must be specific enough for autonomous execution.

### Rule 5: Use pm7y-ralph-planner

ALWAYS pass findings to `pm7y-ralph-planner` for TASKS.md generation. This ensures proper validation requirements, learnings tracking, and iteration workflow are included.

### Rule 6: Stop After Output

After invoking pm7y-ralph-planner, STOP. Do not modify any CSS files. Do not attempt to fix issues. The user will run ralph-loop to fix them.

---

## Validation Checklist

Before passing findings to pm7y-ralph-planner:

- [ ] Parsed arguments correctly (@file or branch diff)
- [ ] Built style inventory from all project CSS/SCSS files
- [ ] Checked for Tailwind, Bootstrap, or custom utility systems
- [ ] Analyzed all files in scope
- [ ] Every finding has exact file path and line number
- [ ] Every finding has clear issue description
- [ ] Every finding has specific **Fix:** instruction
- [ ] Findings grouped by priority (HIGH → MEDIUM → LOW)
- [ ] Findings ordered by file path within each priority section
- [ ] Empty priority sections omitted
- [ ] Invoked pm7y-ralph-planner with structured findings
- [ ] Summary output provided
- [ ] DID NOT attempt to fix any issues
