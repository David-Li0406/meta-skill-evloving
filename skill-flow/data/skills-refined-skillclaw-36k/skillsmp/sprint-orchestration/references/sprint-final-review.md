# Sprint Final Review

After all PRs in a sprint have been implemented (first draft complete), perform a cross-cutting review to identify simplifications across the entire sprint's changes.

---

## When to Use

Trigger on phrases like:
- "perform the final review for sprint N"
- "do the sprint N final review"
- "review sprint N as a whole"

This review happens AFTER all PRs are drafted but BEFORE merging.

---

## Process

### Step 1: Identify the Sprint Scope

Find the changes included in the sprint using jj:

```bash
# Check current working copy state
jj status

# View the diff against the base (typically main)
jj diff --from main --stat
```

### Step 2: Invoke Code-Simplifier for Holistic Review

Use the Task tool with `subagent_type="code-simplifier:code-simplifier"` and pass these instructions:

```markdown
## Sprint Final Review Task

Review the current state of sprint <N> PRs in their totality and look for cross-cutting simplifications across this set of changes.

### Scope

Diff the current state against `main`:
```bash
jj diff --from main --stat
```

### IMPORTANT: Large File Handling

Some PRs may have added VERY large files containing:
- Snapshot data (PNG files, test snapshots)
- Markdown documentation
- Generated code or lock files

You CANNOT load the entire diff all at once.

**Required approach:**
1. First, list ALL changed files with their line counts:
   ```bash
   jj diff --from main --stat
   ```

2. Identify files to EXCLUDE from detailed review:
   - Binary files (images, snapshots)
   - Lock files (uv.lock, package-lock.json)
   - Generated files
   - Files with >500 lines of changes that are pure data

3. Review remaining files selectively using:
   ```bash
   jj diff --from main <specific-file>
   ```

### Output Requirements

**DO NOT make code changes.**

Instead, write a document at `mddocs/frontend/sprints/sprint<N>-review.md` containing:

1. **Files Reviewed** - List of files included in review (and why large files were excluded)

2. **Cross-Cutting Observations** - Patterns, inconsistencies, or issues that span multiple PRs

3. **Suggested Simplifications** - Specific recommendations with:
   - File and line references
   - What to change
   - Why it's an improvement
   - Estimated complexity (trivial/moderate/significant)

4. **Code Quality Assessment** - Overall observations about:
   - Consistency across the sprint
   - Adherence to project patterns
   - Potential technical debt introduced

5. **Recommended Actions** - Prioritized list of follow-up tasks (if any)
```

### Step 3: Review the Output

After the code-simplifier completes:

1. Read the generated review document at `mddocs/frontend/sprints/sprint<N>-review.md`
2. Present a summary to the user
3. Ask if they want to address any of the identified simplifications before merging

---

## Example Invocation

```
Invoke the code-simplifier agent with subagent_type="code-simplifier:code-simplifier"
and pass the Sprint Final Review Task instructions above, substituting the actual
sprint number.
```

---

## Notes

- This review is advisory; the user decides which simplifications to pursue
- Large snapshot files and binary data should be excluded from review scope
- The review document becomes part of the sprint documentation
