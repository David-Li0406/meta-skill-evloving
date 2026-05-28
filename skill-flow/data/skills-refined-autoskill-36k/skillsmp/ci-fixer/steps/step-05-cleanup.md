---
name: step-05-cleanup
description: Cleanup artifacts and show final summary
prev_step: steps/step-01-watch-ci.md
---

# Step 5: Cleanup & Summary

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER leave artifacts behind after workflow completion
- ✅ ALWAYS delete the artifacts directory
- ✅ ALWAYS show a final summary
- 📋 YOU ARE THE CLOSER, wrapping up the workflow
- 💬 FOCUS on cleanup and reporting only
- 🚫 FORBIDDEN to start new fix attempts

## EXECUTION PROTOCOLS:

- 🎯 Summarize → Cleanup → Report final status
- 💾 No state changes needed (workflow is ending)
- 📖 This is the final step - workflow ends here
- 🚫 FORBIDDEN to loop back to any previous step

## CONTEXT BOUNDARIES:

From previous steps:

| Variable            | Description                                    |
| ------------------- | ---------------------------------------------- |
| `{auto_mode}`       | Skip confirmations                             |
| `{branch}`          | Current git branch                             |
| `{current_attempt}` | Total attempts made                            |
| `{max_attempts}`    | Max attempts allowed                           |
| `{run_id}`          | Last GitHub Actions run ID                     |
| `{artifacts_dir}`   | Path to artifacts: `.claude/data/ci-{run_id}/` |
| `{fixes_applied}`   | List of all fixes applied                      |
| `{error_source}`    | Last error source (if any)                     |

## YOUR TASK:

Show a final summary of what happened, clean up all artifacts, and end the workflow.

---

## EXECUTION SEQUENCE:

### 1. Determine Final Status

Check how the workflow ended:

| Condition            | Status       |
| -------------------- | ------------ |
| CI passed            | ✅ SUCCESS   |
| No CI configured     | ⚠️ NO CI     |
| Max attempts reached | ❌ FAILED    |
| User cancelled       | ⏹️ CANCELLED |

### 2. Generate Final Summary

**Display summary:**

```
## CI Fixer - Final Summary

**Branch:** {branch}
**Status:** {SUCCESS | FAILED | NO CI | CANCELLED}
**Attempts:** {current_attempt}/{max_attempts}

### Fixes Applied
{If fixes_applied is not empty:}
1. {fix description} - {file}
2. {fix description} - {file}
...

{Else:}
No fixes were needed.

### Commits Made
{List commits made during this session, if any}
```

### 3. Show Git Log of Session (If Fixes Applied)

**If any fixes were committed:**

```bash
git log --oneline -n {current_attempt} --format="%h %s"
```

Display the commits made during this CI fixer session.

### 4. Cleanup Artifacts

**Check if artifacts directory exists:**

```bash
ls -la {artifacts_dir} 2>/dev/null
```

**If artifacts exist, delete them:**

```bash
trash {artifacts_dir}
```

**Confirm cleanup:**

```
Cleaned up artifacts from {artifacts_dir}
```

**If no artifacts exist:**

```
No artifacts to clean up.
```

### 5. Final Status Message

**If SUCCESS:**

```
## ✅ CI is green!

All checks passed. Your PR is ready for review.

Run: https://github.com/{owner}/{repo}/actions/runs/{run_id}
```

**If FAILED (max attempts):**

```
## ❌ CI still failing

Could not fix after {max_attempts} attempts.

**Last errors:**
{last error summary}

**Next steps:**
1. Review the error logs manually
2. Check if the issue requires architectural changes
3. Ask for help from a teammate

Run: https://github.com/{owner}/{repo}/actions/runs/{run_id}
```

**If NO CI:**

```
## ⚠️ No CI configured

No GitHub Actions workflow was triggered for this branch.

To add CI, create a workflow file at `.github/workflows/ci.yml`
```

**If CANCELLED:**

```
## ⏹️ Workflow cancelled

The CI fixer was stopped by user request.

{If fixes were applied:}
Note: {N} fixes were already committed before cancellation.
```

---

## SUCCESS METRICS:

✅ Final status correctly determined
✅ Comprehensive summary displayed
✅ All fixes listed
✅ Commits shown
✅ Artifacts directory deleted
✅ Cleanup confirmed
✅ Workflow ended cleanly

## FAILURE MODES:

❌ Not deleting artifacts
❌ Incomplete summary
❌ Not showing fix history
❌ Trying to continue after this step

## CLEANUP PROTOCOLS:

- Always attempt to delete artifacts
- Use `trash` command first
- Confirm deletion to user
- Never leave stale artifacts behind
- This is the FINAL step - no more actions after this

---

## WORKFLOW END

**This is the final step. The CI fixer workflow is now complete.**

<critical>
Remember: ALWAYS clean up artifacts! The workflow ENDS here - do not loop back.
</critical>
