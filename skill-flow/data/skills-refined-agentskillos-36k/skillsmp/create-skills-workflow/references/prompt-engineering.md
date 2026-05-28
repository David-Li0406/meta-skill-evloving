# Prompt Engineering for Workflow Skills

Best practices for writing effective prompts in workflow steps.

---

## Core Principles

### 1. Be Explicit, Not Vague

❌ **Bad:**

```
Try to find relevant files.
Consider the patterns.
```

✅ **Good:**

```
Find ALL files matching: **/*auth*.ts
Document EACH pattern with file path and line number.
```

### 2. Use Positive Framing

❌ **Bad:**

```
Don't forget to check for errors.
Don't skip the validation.
```

✅ **Good:**

```
Always check for errors before proceeding.
Run validation after each change.
```

### 3. Define Success Criteria

❌ **Bad:**

```
Make sure it works properly.
```

✅ **Good:**

```
<success_criteria>
- Typecheck passes: `pnpm typecheck` exits 0
- Lint passes: `pnpm lint` exits 0
- Tests pass: All tests green
- No console errors
</success_criteria>
```

### 4. Handle Edge Cases

❌ **Bad:**

```
Process the files.
```

✅ **Good:**

```
Process the files:
- If no files found: Report "No matching files" and ask user
- If file is empty: Skip with note
- If file is too large (>1000 lines): Read in chunks
- If file has errors: Log error and continue to next
```

---

## XML Structure

Use semantic XML tags for clear organization:

```xml
<objective>
What this step accomplishes.
</objective>

<context>
Background information and prerequisites.
</context>

<execution_sequence>
Step-by-step instructions.
</execution_sequence>

<success_criteria>
How to know if this step succeeded.
</success_criteria>

<failure_modes>
What can go wrong and how to handle it.
</failure_modes>
```

### Benefits of XML Tags

- Clear section boundaries
- Semantic meaning built-in
- Lower token usage than markdown
- Programmatically parseable
- Easy to reference: "Using the rules in `<execution_sequence>`..."

---

## Instruction Patterns

### Pattern 1: Conditional Behavior

```markdown
**If `{auto_mode}` = true:**
→ Use recommended option automatically
→ Skip confirmation dialogs
→ Proceed without waiting

**If `{auto_mode}` = false:**
→ Present options to user
→ Wait for confirmation
→ Handle user response
```

### Pattern 2: Numbered Steps

```markdown
**1. First Action**

- Sub-step A
- Sub-step B

**2. Second Action**

- Sub-step A
- Sub-step B

**3. Third Action**

- Depends on step 2 completing successfully
```

### Pattern 3: Decision Trees

```markdown
<decision_tree>
IF condition_a:
→ Action A
→ Load step-X

ELSE IF condition_b:
→ Action B
→ Load step-Y

ELSE:
→ Default action
→ Load step-Z
</decision_tree>
```

### Pattern 4: CRITICAL Markers

Use for absolutely essential instructions:

```markdown
**CRITICAL: Never skip this step.**

**CRITICAL: Use AskUserQuestion tool, NOT plain text prompts.**

**CRITICAL: Launch ALL agents in a SINGLE message for parallel execution.**
```

---

## Tool Usage Patterns

### AskUserQuestion Pattern

````markdown
**CRITICAL: Use AskUserQuestion tool, NOT plain text 1/2/3 prompts.**

Use AskUserQuestion:

```yaml
questions:
  - header: 'Header'
    question: 'Full question?'
    options:
      - label: 'Option A (Recommended)'
        description: 'What this does'
      - label: 'Option B'
        description: 'What this does'
    multiSelect: false
```
````

````

### Parallel Agent Pattern

```markdown
**CRITICAL: Launch ALL agents in a SINGLE message for parallel execution.**

**Agent 1:** (`explore-codebase`)
````

Find files related to: {task}
Return: file paths with line numbers

```

**Agent 2:** (`explore-docs`)
```

Research documentation for: {task}
Return: key findings with references

```

**Agent 3:** (`websearch`)
```

Search for: {task}
Return: best practices and patterns

```

```

### Tool Selection Pattern

```markdown
**Use the RIGHT tool:**

- File search → Glob (not find)
- Content search → Grep (not grep command)
- Read files → Read (not cat)
- Edit files → Edit (not sed)
- Complex exploration → Task with explore agent
- User input → AskUserQuestion (not plain text)
```

---

## State Documentation

### Available State Section

```markdown
<available_state>
From previous step:

| Variable             | Description           |
| -------------------- | --------------------- |
| `{task_description}` | What to implement     |
| `{task_id}`          | Kebab-case identifier |
| `{auto_mode}`        | Skip confirmations    |
| `{files_found}`      | List from step 1      |

</available_state>
```

### Produces Section

```markdown
<produces>
This step produces:

| Variable         | Description                  |
| ---------------- | ---------------------------- |
| `{plan_items}`   | List of implementation steps |
| `{file_changes}` | Map of files to changes      |

</produces>
```

---

## Error Handling Patterns

### Graceful Failure

```markdown
<error_handling>
**If validation fails:**

1. Log the specific error
2. Attempt auto-fix if possible
3. If auto-fix fails:
   - **If `{auto_mode}` = true:** Try alternative approach
   - **If `{auto_mode}` = false:** Ask user for guidance
4. Never proceed with failing checks
   </error_handling>
```

### Retry Pattern

```markdown
<retry_pattern>
max_attempts = 3
attempt = 0

WHILE attempt < max_attempts:
attempt += 1

    Try the operation

    IF success:
        → Continue

    IF failure AND attempt < max_attempts:
        → Log error
        → Apply fix
        → Retry

    IF failure AND attempt >= max_attempts:
        → Stop and ask user

</retry_pattern>
```

---

## Formatting Guidelines

### Code Blocks

Use triple backticks with language hints:

````markdown
```bash
pnpm typecheck
```
````

```typescript
const result = await validate(input)
```

```yaml
questions:
  - header: 'Test'
```

````

### Tables for Structured Data

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
````

### Lists for Steps

```markdown
1. First step
2. Second step
   - Sub-step A
   - Sub-step B
3. Third step
```

---

## Anti-Patterns to Avoid

❌ **Vague instructions**

```
Handle the errors appropriately.
```

❌ **Missing conditions**

```
Ask the user what to do.  # What if auto_mode?
```

❌ **Plain text prompts**

```
Choose 1, 2, or 3:  # Use AskUserQuestion!
```

❌ **Sequential when parallel possible**

```
Launch Agent 1, wait, then launch Agent 2  # Launch together!
```

❌ **Assuming state exists**

```
Use {files_found} to...  # What if empty?
```

❌ **Missing next step directive**

```
# Step ends without saying what's next
```
