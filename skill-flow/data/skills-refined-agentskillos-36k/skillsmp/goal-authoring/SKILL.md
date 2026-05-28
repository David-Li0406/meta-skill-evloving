---
name: goal-authoring
description: Writing effective Ralph goal files for CDD execution
---

# Goal Authoring

Writing effective goal files for Ralph loop execution in `$CDD_DIR/goals/`.

## File Naming Convention

Goal files MUST be named: `<name>-ralph-goal.md`

**Examples:**
- `list-tool-ralph-goal.md` ✓
- `web-fetch-ralph-goal.md` ✓
- `list-tool-goal.md` ✗ (missing "ralph")
- `list-tool.md` ✗ (missing "ralph-goal")

## Core Principle

**Ralph has unlimited context through iteration.** Don't artificially limit goals or references - Ralph can read all plan documents, iterate through failures, and persist until outcomes are achieved.

## Goal File Format

```markdown
## Objective
[Complete objective - not tiny steps]

## Reference
[All relevant plan/research/user-story docs + codebase examples]

## Outcomes
[Measurable, verifiable outcomes]

## Acceptance
[Success criteria: make check, specific tests, etc.]
```

## Key Principles

1. **Specify WHAT, never HOW** - Outcomes, not steps/order
2. **Reference liberally** - All relevant docs, Ralph reads across iterations
3. **One cohesive objective** - Not artificially small, not entire release
4. **Complete acceptance criteria** - Ralph needs to know when done
5. **Trust Ralph to iterate** - Discovers path, learns from failures
6. **Be explicit about discovery** - If work requires finding all instances of X, state it clearly in both objective and outcomes. Ralph has gotten stuck when discovery wasn't explicit. Write "Discover and fix all hardcoded paths" not "Fix hardcoded paths" or "Fix paths at lines 10, 25, 40"

## Example: Bad vs Good

**Bad (context-limited thinking):**
```markdown
## Objective
Create the web_fetch_t struct.

## Reference
plan/web-fetch.md section 2.1

## Outcomes
- Struct defined in src/web_fetch.h
```

Problems: Artificially small, minimal reference, no acceptance criteria.

**Good (leverages unlimited context):**
```markdown
## Objective
Implement web-fetch tool with HTML-to-markdown conversion per plan/web-fetch.md.

## Reference
- $CDD_DIR/plan/web-fetch.md - Interface and behavior spec
- $CDD_DIR/plan/tool-integration.md - Registry integration
- $CDD_DIR/plan/html-markdown.md - Conversion approach
- $CDD_DIR/research/html-to-markdown.md - Library rationale
- $CDD_DIR/user-stories/web-fetch.md - Expected behaviors
- src/tool_registry.c - Registration pattern
- tests/unit/tool_bash/ - Test structure

## Outcomes
- web_fetch tool implemented per plan/web-fetch.md
- HTML-to-markdown working per plan/html-markdown.md
- Integrated with registry per plan/tool-integration.md
- Unit tests in tests/unit/web_fetch/ pass
- User stories in user-stories/web-fetch.md satisfied

## Acceptance
- `make check` passes
- `make lint` passes
- Manual: `./ikigai` → `/web-fetch https://example.com` returns markdown
```

Why better: Complete objective, comprehensive references, measurable outcomes, clear acceptance.

**Discovery example:**
```markdown
## Objective
Discover all hardcoded ~/.config/ikigai path references in tests/ directory and update them to use IKIGAI_CONFIG_DIR environment variable.

## Reference
- tests/test_utils.c:692-730 - test_paths_setup_env() sets IKIGAI_CONFIG_DIR
- .envrc:3 - Shows IKIGAI_CONFIG_DIR=$PWD/etc/ikigai

## Outcomes
- All hardcoded ~/.config/ikigai references in tests/ discovered via grep
- All discovered test files updated to use getenv("IKIGAI_CONFIG_DIR")
- No hardcoded ~/.config/ikigai paths remain in tests directory

## Acceptance
- grep -r "\.config/ikigai" tests/ returns no hardcoded paths
- check-unit passes
```

Why explicit discovery matters: Objective starts with "Discover", first outcome confirms discovery happened. Ralph won't skip the grep step.

## Anti-Patterns

❌ **Step-by-step instructions** - "First do X, then Y" (Ralph discovers path)
❌ **Minimal references** - "Save context" (Ralph iterates, include all relevant)
❌ **Vague outcomes** - "Feature implemented" (Be specific and measurable)
❌ **Tiny goals** - Breaking cohesive work into artificial steps
❌ **Pre-discovered work** - Listing specific file:line locations to fix (Ralph should discover)

✅ **Do this:** Comprehensive objective, all references, measurable outcomes, trust Ralph to iterate and discover.
