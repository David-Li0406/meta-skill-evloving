<!--
Embedded Navigator Command: plan
Standalone version for plugin-free operation
-->
---
allowed-tools: Task, Glob, Grep, Read, Write, Bash(git branch:*), Bash(git status:*), Bash(git rev-parse:*), Bash(test:*), Bash(mkdir:*), AskUserQuestion
argument-hint: <task description> [--base-branch <branch>]
description: Create implementation spec with atlas context
---

## Context

Arguments: `/spec-plan <TASK_DESCRIPTION> [OPTIONS]`
- **<task>** - Description of the feature, chore, or bug fix
- **--base-branch <branch>** - Branch to base implementation on (default: current branch)

Current directory: !`pwd`
Current branch: !`git branch --show-current`

## Workflow

### 1. Pre-flight

**Verify atlas exists:**
```bash
test -f ".claude/skills/atlas/references/schema.yaml" && echo "EXISTS" || echo "NOT_FOUND"
```

**If not found:**
```
❌ Atlas required.

Run `/chart` to generate an atlas first.
```
**STOP**

**Create specs directory:**
```bash
mkdir -p specs
```

### 2. Load Atlas Context

Read:
- `.claude/skills/atlas/SKILL.md`
- `.claude/skills/atlas/references/schema.yaml`

Extract:
- Domains and their locations
- Pattern guides from `documentation.patterns`
- Task mappings from `task_mappings`
- Validation commands from `validation.commands`

### 3. Build Pattern Keyword Map

**CRITICAL**: Generate a keyword-to-pattern mapping from the atlas schema.

For each pattern in `documentation.patterns`:
1. Read the pattern file
2. Extract the "When to Use" section
3. Identify keywords that trigger this pattern

**Example mapping generation:**
If schema.yaml contains:
```yaml
documentation:
  patterns:
    - patterns/rtk_query.md
    - patterns/redux_slices.md
    - patterns/atomic_design.md
```

Generate a mental map like:
| Keywords | Pattern Guide |
|----------|---------------|
| "api", "endpoint", "fetch", "query", "RTK", "cache" | `patterns/rtk_query.md` |
| "slice", "redux", "state", "reducer", "action" | `patterns/redux_slices.md` |
| "component", "atom", "molecule", "design system" | `patterns/atomic_design.md` |

Also map `task_mappings` keys to patterns:
| Task Mapping | Relevant Pattern |
|--------------|------------------|
| `add_api_endpoint` | `patterns/rtk_query.md` |
| `add_redux_slice` | `patterns/redux_slices.md` |
| `create_reusable_component` | `patterns/atomic_design.md` |

### 4. Analyze Task

**Identify:**
- Task type: feature / chore / bugfix / refactor
- Affected domains (match to atlas)
- Required patterns (using keyword map from step 3)

**Pattern Matching:**
- Scan task description for keywords
- Match to pattern guides using the map
- Load and read matched pattern files
- Extract "Key Conventions" and "Anti-Patterns" sections

**Research:**
- Read relevant domain references
- Find similar implementations
- Check for conflicts

### 5. Capture Git Context

**Determine base branch:**
- If `--base-branch` argument provided → use that value
- Otherwise → use current branch:
  ```bash
  git branch --show-current  # base_branch
  ```

**Verify base branch exists:**
```bash
git rev-parse --verify {base_branch} 2>/dev/null && echo "EXISTS" || echo "NOT_FOUND"
```
If not found → Error: "Base branch '{base_branch}' does not exist"

**Generate target branch:** `{type}/{kebab-case-description}`

**Branch naming rules:**
- 3-6 words, lowercase, hyphen-separated
- Prefix with type: `feature/`, `chore/`, `bugfix/`, `refactor/`

**Example transformation:**
- Task: "Add RTK Query endpoint for user preferences"
- Type: `feature`
- Branch: `feature/add-user-preferences-endpoint`

### 6. Generate Spec

**Create:** `specs/{task-slug}.md`

```markdown
# {Type}: {Title}

## Prerequisites

{dependencies or "None - This task has no dependencies and can be implemented immediately."}

---

**⛔ DO NOT proceed until all prerequisites are verified.**

---

## Branch Information

**Implementation Branch**: `{target_branch}`
**Base Branch**: `{base_branch}`

Compare implementation branch against base branch when reviewing changes.

---

## Task Description

**What**: {what to accomplish}
**Why**: {business value}
**Context**: {background}

**Success Criteria**:
- [ ] {criterion 1}
- [ ] {criterion 2}

---

## Relevant Files

### Pattern Guides

Review these pattern guides before implementing:
{For each matched pattern from step 3/4:}
- `.claude/skills/atlas/references/{pattern-path}` - {Brief description of what it covers}

**Critical conventions for this task**:
{Extract 3-5 most important rules from the matched pattern files' "Key Conventions" sections}
- {Convention 1 - most important rule from pattern}
- {Convention 2 - common pitfall to avoid from anti-patterns}
- {Convention 3 - required structure or naming convention}

**Example (for an RTK Query task):**
```markdown
### Pattern Guides
Review these pattern guides before implementing:
- `.claude/skills/atlas/references/patterns/rtk_query.md` - RTK Query API conventions

**Critical conventions for this task**:
- Use `.api.ts` suffix for API files (NOT `userApi.ts` or `user-api.ts`)
- Import shared `baseQuery` from `../baseQuery` (don't create custom fetchBaseQuery)
- Use `providesTags` on queries and `invalidatesTags` on mutations for cache management
- Register API in `store.ts` reducer AND middleware
```

### Relevant Domains
{domains from atlas schema that this task touches}

### Existing Files
{files to modify with brief explanation}

### New Files
{files to create as part of this task}

---

## Step-by-Step Tasks

**⚠️ Execute steps in order from top to bottom.**

### 1. {First Major Step}
- Specific action item
- Another specific action
- Details about implementation

### 2. {Second Major Step}
- Specific action item
- Expected outcome

{Continue with numbered h3 headers for each major step}

### N. Run Validation
- Execute ALL commands in "Validation Commands" section
- Verify zero errors and regressions
- Fix any issues before marking complete

---

## Validation Commands

**Execute ALL commands to confirm completion with zero regressions.**

```bash
{working_dir from schema.validation.working_dir, if specified}

{For each command in schema.validation.commands:}
# {command.name}
{command.command}
```

**Expected Result**: All commands complete successfully with no errors.

---

## Notes

{Optional: Additional context, gotchas, helpful tips, or links to documentation}
```

### 7. Report

```markdown
## Spec Created

**File:** `specs/{filename}.md`

**Summary:**
- Analyzed task and identified {X} relevant files
- Matched {Y} pattern guide(s): {list pattern names}
- Defined {Z} implementation steps with prerequisites
- Created validation commands for regression testing
- **Base Branch**: `{base_branch}`
- **Implementation Branch**: `{target_branch}`

**Next Steps:** Run `/spec-build specs/{filename}.md` to execute this plan.
- Build will automatically create and checkout the implementation branch
```
