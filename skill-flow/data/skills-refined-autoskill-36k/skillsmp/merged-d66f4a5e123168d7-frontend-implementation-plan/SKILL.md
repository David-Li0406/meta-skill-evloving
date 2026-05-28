---
name: frontend-implementation-plan
description: Use this skill to create atomic implementation plans for frontend tasks, detailing each step with exact code and verification commands.
---

# Plan

## ⚠️ CRITICAL RULES - READ FIRST

1. **DETECT MODE**: Determine if input is an existing task reference or a new requirement description
   - If input looks like `story-user-profile Task 1` or `standalone-fix-login Task 2`: **MODE A**
   - If input is a new requirement (e.g., "Fix login button hover"): **MODE B**

2. **MODE A - Enhance Existing Task**:
   - Read the task file from `docs/reference/frontend/tasks/`
   - User must specify task number (e.g., "Task 1", "Task 2")
   - Add or update the "Implementation Steps" section for that specific task
   - Keep all other sections intact
   - Save back to the same file

3. **MODE B - Create Standalone Task File**:
   - Analyze the requirement - is it simple (1 task) or complex (multiple tasks)?
   - If complex, break into multiple tasks (like task-breakdown does)
   - Use filename: `standalone-{requirement-name}.md` (kebab-case)
   - Save to `docs/reference/frontend/tasks/`
   - File format: same as story-based (multiple task sections)

4. **READ CONSTRAINTS FIRST**:
   - Must read `docs/reference/frontend/design-system.md` for design tokens
   - Must read `docs/reference/frontend/constraints.md` for tech stack
   - If task references a design, read from `docs/reference/frontend/designs/`

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Read task**: Get task details from `docs/reference/frontend/tasks/{story}.md`
2. **Read design**: Load related design from `docs/reference/frontend/designs/`
3. **Read constraints**: Load `docs/reference/frontend/constraints.md`
4. **Break into atomic steps**:
   - Start with file creation/setup
   - One section/feature per step
   - Include verification for each step
   - End with commit
5. **Keep steps atomic**: One action per step
6. **Present plan to user** (do not save to file)

## Implementation Steps Format

Both modes use the same step format:

````markdown
## Implementation Steps

### Step 1: [Action]

**Files**:

- Create: `src/components/[Name].tsx`
- Modify: `src/pages/[Page].tsx:L10-L20`

**Action**:
[Exact code or action to take]

**Verify**:

```bash
[verification command]
```
````

Expected: [expected output]

---

### Step N: Commit

```bash
git add [files]
git commit -m "feat: [description]"
```

````

## Step Granularity

Each step = ONE atomic action:

| Good Steps | Bad Steps |
|------------|-----------|
| Create component file with imports | Create component with all logic |
| Add component skeleton (empty return) | Implement entire component |
| Implement single section | Implement all sections |
| Write one test case | Write all tests |

## Step Types

### Setup Step
```markdown
**Files**: Create: `src/components/ProfileCard.tsx`
**Action**: Create file with basic structure
**Verify**: `npx tsc --noEmit` → No errors
````

### Implementation Step

```markdown
**Files**: Modify: `src/components/ProfileCard.tsx:L8-L10`
**Action**: Implement header section with Avatar and name
**Verify**: `npm run dev` → Component renders correctly
```

### Test Step

```markdown
**Files**: Create: `src/components/__tests__/ProfileCard.test.tsx`
**Action**: Write unit test for profile name rendering
**Verify**: `npm test ProfileCard` → 1 test passed
```

## Key Rules

- ALWAYS include verification command for each step
- MUST keep steps to 2-5 minutes of work
- ALWAYS end with a commit step
- NEVER combine multiple actions into one step

## Common Mistakes

- ❌ Steps too large → ✅ One action per step
- ❌ Skip verification → ✅ Every step has verify command
- ❌ Vague actions → ✅ Include exact code
- ❌ No commit step → ✅ Always end with git commit

## Output

- MODE A: Update specific task section in file with Implementation Steps
- MODE B: Create new standalone-{name}.md file with one or multiple tasks