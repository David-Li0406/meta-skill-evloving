---
name: step-02-analyze-errors
description: Fetch and analyze error logs from all CI/CD sources
prev_step: steps/step-01-watch-ci.md
next_step: steps/step-03-fix-locally.md
---

# Step 2: Analyze Errors

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER guess at errors - always fetch actual logs
- ✅ ALWAYS save artifacts to `.claude/data/ci-{run_id}/`
- ✅ ALWAYS check multiple sources (GitHub Actions, Vercel, Netlify)
- 📋 YOU ARE AN ANALYST, not a fixer (that comes next)
- 💬 FOCUS on understanding what failed
- 🚫 FORBIDDEN to start fixing before full analysis

## EXECUTION PROTOCOLS:

- 🎯 Setup artifacts dir → Fetch logs → Parse errors → Use agents if needed → Report
- 💾 Store error details in `{error_logs}` and `{error_source}`
- 💾 Save all logs to `{artifacts_dir}`
- 📖 Complete analysis before loading next step
- 🚫 FORBIDDEN to load step-03 until errors are understood

## CONTEXT BOUNDARIES:

From previous steps:

| Variable            | Description            |
| ------------------- | ---------------------- |
| `{auto_mode}`       | Skip confirmations     |
| `{run_id}`          | GitHub Actions run ID  |
| `{branch}`          | Current git branch     |
| `{current_attempt}` | Current attempt number |

## YOUR TASK:

Create artifacts directory, fetch error logs from all CI/CD sources, use agents for complex analysis if needed, and categorize errors for fixing.

---

## EXECUTION SEQUENCE:

### 1. Setup Artifacts Directory

**Create the artifacts directory structure:**

```bash
mkdir -p .claude/data/ci-{run_id}/github/artifacts
mkdir -p .claude/data/ci-{run_id}/vercel
mkdir -p .claude/data/ci-{run_id}/netlify
```

**Set state variable:**

```
{artifacts_dir} = ".claude/data/ci-{run_id}/"
```

### 2. Fetch GitHub Actions Logs

**Get failed job logs and save:**

```bash
gh run view {run_id} --log-failed > {artifacts_dir}/github/failed-logs.txt
```

**Download artifacts if available:**

```bash
gh run download {run_id} --dir {artifacts_dir}/github/artifacts 2>/dev/null || echo "No artifacts to download"
```

**Parse for common error patterns:**

- Test failures: `FAIL`, `Error:`, `AssertionError`
- Lint errors: `error`, `warning`, ESLint/Prettier messages
- Build errors: `Cannot find module`, `TypeScript error`
- Dependency errors: `npm ERR!`, `ERESOLVE`

### 3. Check Vercel Deployment (if applicable)

**Detect if project uses Vercel:**

```bash
ls -la vercel.json .vercel 2>/dev/null
```

**If Vercel detected, get deployment status:**

```bash
vercel ls --output json 2>/dev/null | head -10 > {artifacts_dir}/vercel/deployment.json
```

**If deployment failed, get logs:**

```bash
# Get latest deployment URL
DEPLOY_URL=$(vercel ls --output json 2>/dev/null | jq -r '.[0].url' 2>/dev/null)

if [ -n "$DEPLOY_URL" ]; then
    vercel inspect "$DEPLOY_URL" > {artifacts_dir}/vercel/logs.txt 2>&1
fi
```

### 4. Check Netlify (if applicable)

**Detect if project uses Netlify:**

```bash
ls -la netlify.toml 2>/dev/null
```

**If Netlify detected:**

```bash
netlify status > {artifacts_dir}/netlify/build-logs.txt 2>&1
```

### 5. Use Agents for Complex Analysis (If Needed)

**If errors are unclear or complex, use agents:**

**For codebase exploration (find related files):**

```
Use Task tool with subagent_type="Explore":
- "Find all files related to the failing test in {test_file}"
- "Search for usages of {failing_function}"
```

**For documentation lookup (if dependency/config issue):**

```
Use Task tool with subagent_type="explore-docs":
- "How to configure {library} for {use_case}"
- "What causes {error_message} in {framework}"
```

**For web search (if error is unfamiliar):**

```
Use Task tool with subagent_type="websearch":
- "How to fix {specific_error_message}"
- "{framework} {error_type} solution"
```

### 6. Categorize Errors

Based on log analysis, categorize into:

| Error Type         | Source           | Priority |
| ------------------ | ---------------- | -------- |
| `test-failure`     | Test output      | High     |
| `lint-error`       | ESLint/Prettier  | Medium   |
| `type-error`       | TypeScript       | High     |
| `build-error`      | Webpack/Next.js  | High     |
| `dependency-error` | npm/yarn         | High     |
| `deployment-error` | Vercel/Netlify   | Medium   |
| `env-error`        | Missing env vars | High     |

**Set `{error_source}`** to the primary source:

- `github-actions` for test/lint/build failures
- `vercel` for Vercel deployment issues
- `netlify` for Netlify deployment issues

**Set `{error_logs}`** with parsed error summary.

### 7. Save Error Summary

**Write summary to artifacts:**

```bash
cat > {artifacts_dir}/summary.md << 'EOF'
# CI Failure Analysis

**Run ID:** {run_id}
**Branch:** {branch}
**Attempt:** {current_attempt}/{max_attempts}
**Error Source:** {error_source}

## Errors Found
{list of errors with file:line references}

## Root Cause Analysis
{brief analysis}

## Suggested Fixes
{list of suggested fixes}
EOF
```

### 8. Display Error Summary

Present a clear summary to the user:

```
## CI Failure Analysis (Attempt {current_attempt}/{max_attempts})

**Error Source:** {error_source}
**Error Type:** {categorized type}
**Artifacts saved to:** {artifacts_dir}

### Errors Found:
- Error 1: description (file:line)
- Error 2: description (file:line)

### Files Affected:
- file1.ts:123
- file2.ts:456

### Root Cause Analysis:
{brief analysis of what caused the failure}
```

### 9. Confirm Analysis

**If `{auto_mode}` = true:**
→ Proceed to fixing

**If `{auto_mode}` = false:**
Use AskUserQuestion:

```yaml
questions:
  - header: "Analysis"
    question: "I found {N} errors. Proceed to fix them locally?"
    options:
      - label: "Fix all (Recommended)"
        description: "Attempt to fix all identified errors"
      - label: "Show details"
        description: "Show more details before proceeding"
      - label: "Manual investigation"
        description: "Stop here, I'll investigate myself"
    multiSelect: false
```

---

## SUCCESS METRICS:

✅ Artifacts directory created at `.claude/data/ci-{run_id}/`
✅ GitHub Actions logs fetched and saved
✅ Deployment platform detected and checked
✅ Agents used for complex analysis when needed
✅ Errors parsed and categorized
✅ Summary saved to artifacts
✅ Clear summary presented

## FAILURE MODES:

❌ Not creating artifacts directory
❌ Not saving logs to artifacts
❌ Not fetching actual logs
❌ Missing deployment platform checks
❌ Vague error descriptions
❌ Not using agents when errors are unclear

## ANALYSIS PROTOCOLS:

- Save ALL logs to `{artifacts_dir}` for reference
- Extract exact error messages and line numbers
- Identify affected files specifically
- Don't guess at causes - use log evidence
- Use agents for complex analysis or unknown errors
- Check ALL potential sources, not just GitHub

---

## NEXT STEP:

After analysis complete, load `./step-03-fix-locally.md`

<critical>
Remember: This step is ONLY about analysis - understand the errors completely before trying to fix! Use agents if the error is unclear.
</critical>
