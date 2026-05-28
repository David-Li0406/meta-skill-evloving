---
name: step-01-analyze
description: Pure context gathering - explore codebase to understand WHAT EXISTS
next_step: steps/step-02-plan.md
---

# Step 1: Analyze (Context Gathering)

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER plan or design solutions - that's step 2
- 🛑 NEVER create todos or implementation tasks
- 🛑 NEVER decide HOW to implement anything
- ✅ ALWAYS focus on discovering WHAT EXISTS
- ✅ ALWAYS report findings with file paths and line numbers
- 📋 YOU ARE AN EXPLORER, not a planner
- 💬 FOCUS on "What is here?" NOT "What should we build?"
- 🚫 FORBIDDEN to suggest implementations or approaches

## EXECUTION PROTOCOLS:

- 🎯 Launch parallel exploration agents (unless economy_mode)
- 💾 Append findings to output file (if save_mode)
- 📖 Document patterns with specific file:line references
- 🚫 FORBIDDEN to proceed until context is complete

## CONTEXT BOUNDARIES:

- Variables from step-00-init are available
- No implementation decisions have been made yet
- Codebase state is unknown - must be discovered
- Don't assume knowledge about the codebase

## YOUR TASK:

Gather ALL relevant context about WHAT CURRENTLY EXISTS in the codebase related to the task.

---

<available_state>
From step-00-init:

| Variable             | Description                   |
| -------------------- | ----------------------------- |
| `{task_description}` | What to implement             |
| `{task_id}`          | Kebab-case identifier         |
| `{auto_mode}`        | Skip confirmations            |
| `{examine_mode}`     | Auto-proceed to review        |
| `{save_mode}`        | Save outputs to files         |
| `{test_mode}`        | Include test steps            |
| `{economy_mode}`     | No subagents, direct tools    |
| `{output_dir}`       | Path to output (if save_mode) |

</available_state>

---

## EXECUTION SEQUENCE:

### 1. Initialize Save Output (if save_mode)

**If `{save_mode}` = true:**

```bash
bash {skill_dir}/scripts/update-progress.sh "{task_id}" "01" "analyze" "in_progress"
```

Append findings to `{output_dir}/01-analyze.md` as you work.

### 2. Extract Search Keywords

From the task description, identify:

- **Domain terms**: auth, user, payment, etc.
- **Technical terms**: API, route, component, etc.
- **Action hints**: create, update, fix, add, etc.

These keywords guide exploration - NOT planning.

### 3. Explore Codebase

**If `{economy_mode}` = true:**
→ Use direct tools (see step-00b-economy.md for rules)

```
1. Glob to find files: **/*{keyword}*
2. Grep to search content in likely locations
3. Read the most relevant 3-5 files
4. Skip web research unless stuck
```

**If `{economy_mode}` = false:**
→ Launch parallel exploration agents

**CRITICAL: Launch ALL agents in a SINGLE message for parallel execution.**

**Agent 1: Codebase Exploration** (`explore-codebase`)

```
Find existing code related to: {task_description}

Report ONLY what exists:
1. Files that contain related code (with paths and line numbers)
2. Existing patterns used for similar features
3. Utility functions that might be relevant
4. How similar features are currently structured
5. Test file locations and patterns

DO NOT suggest what to build. Just report what's there.
```

**Agent 2: Documentation Research** (`explore-docs`)

```
Research documentation for libraries used in: {task_description}

Find:
1. How the relevant libraries/frameworks work
2. API documentation for tools being used
3. Best practices from official docs
```

**Agent 3: Web Research** (`websearch`)

```
Search for context about: {task_description}

Find:
1. How this is typically implemented
2. Common patterns and approaches
3. Known pitfalls or gotchas
```

### 4. Synthesize Findings

Combine results into structured context:

```markdown
## Codebase Context

### Related Files Found

| File                    | Lines | Contains                      |
| ----------------------- | ----- | ----------------------------- |
| `src/auth/login.ts`     | 1-150 | Existing login implementation |
| `src/utils/validate.ts` | 20-45 | Email validation helper       |

### Patterns Observed

- **Route pattern**: Uses Next.js App Router with `route.ts`
- **Validation**: Uses zod schemas in `schemas/` folder
- **Error handling**: Throws custom ApiError classes

### Utilities Available

- `src/lib/auth.ts` - JWT sign/verify functions
- `src/lib/db.ts` - Prisma client instance

### Similar Implementations

- `src/auth/login.ts:42` - Login flow (reference for patterns)

### Test Patterns

- Tests in `__tests__/` folders
- Uses vitest with testing-library

## Documentation Insights

### Libraries Used

- **jose**: JWT library - uses `SignJWT` class
- **prisma**: ORM - uses `prisma.user.create()` pattern

## Research Findings

### Common Approaches

- Registration: validate → hash → create → issue token
- Use httpOnly cookies for tokens
```

**If `{save_mode}` = true:** Append synthesis to 01-analyze.md

### 5. Infer Acceptance Criteria

Based on task and context, infer success criteria:

```markdown
## Inferred Acceptance Criteria

Based on "{task_description}" and existing patterns:

- [ ] AC1: [specific measurable outcome]
- [ ] AC2: [specific measurable outcome]
- [ ] AC3: [specific measurable outcome]

_These will be refined in the planning step._
```

**If `{save_mode}` = true:** Update 00-context.md with acceptance criteria

### 6. Present Context Summary

**Always (regardless of auto_mode):**

Present summary and proceed directly to planning:

```
**Context Gathering Complete**

**Files analyzed:** {count}
**Patterns identified:** {count}
**Utilities found:** {count}

**Key findings:**
- {summary of relevant files}
- {patterns that will guide implementation}

→ Proceeding to planning phase...
```

<critical>
Do NOT ask for user confirmation here - always proceed directly to step-02-plan.
</critical>

### 7. Complete Save Output (if save_mode)

**If `{save_mode}` = true:**

Append summary to `{output_dir}/01-analyze.md` then:

```bash
bash {skill_dir}/scripts/update-progress.sh "{task_id}" "01" "analyze" "complete"
bash {skill_dir}/scripts/update-progress.sh "{task_id}" "02" "plan" "in_progress"
```

---

## SUCCESS METRICS:

✅ Related files identified with paths and line numbers
✅ Existing patterns documented with specific examples
✅ Available utilities noted
✅ Dependencies listed
✅ Acceptance criteria inferred
✅ NO planning or implementation decisions made
✅ Output saved (if save_mode)

## FAILURE MODES:

❌ Starting to plan or design (that's step 2!)
❌ Suggesting implementations or approaches
❌ Missing obvious related files
❌ Not documenting patterns with file:line references
❌ Launching agents sequentially instead of parallel
❌ Using subagents when economy_mode is true
❌ **CRITICAL**: Blocking workflow with unnecessary confirmation prompts

## ANALYZE PROTOCOLS:

- This step is ONLY about discovery
- Report what EXISTS, not what SHOULD BE
- Include file paths and line numbers for all findings
- Don't assume - verify by reading files
- In economy mode, use direct tools only

---

## NEXT STEP:

Always proceed directly to `./step-02-plan.md` after presenting context summary.

<critical>
Remember: Analysis is ONLY about "What exists?" - save all planning for step-02!
Do NOT ask for confirmation - proceed directly!
</critical>
