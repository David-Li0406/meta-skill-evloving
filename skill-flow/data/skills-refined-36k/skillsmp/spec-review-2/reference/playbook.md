# Spec Review Playbook

Edge case handling and decision trees for review scenarios.

---

## Timeout Handling

### OpenCode Timeout (> 5 minutes)

**Symptom:** `timeout` command exits with code 124

**Response:**
1. Continue with Claude-only results
2. Add warning to output:
   ```
   Note: OpenCode review timed out after 5 minutes.
   Results are from Claude reviewer only.
   Consider re-running with single reviewer for faster results.
   ```
3. Proceed with synthesis using available data

### Claude Subagent Timeout

**Symptom:** Task tool returns timeout error

**Response:**
1. If OpenCode succeeded: use OpenCode results only
2. If both failed: report failure, suggest retry
3. Never proceed with zero reviews

---

## Parse Failures

### YAML Not Found in Output

**Symptom:** Reviewer output lacks `reviewer_report:` block

**Response:**
1. Search for partial YAML (may be malformed)
2. If found: attempt parse, report issues
3. If not found: mark reviewer as failed
4. Continue with available data

### Malformed YAML

**Symptom:** YAML parsing error

**Response:**
1. Report which reviewer's output failed to parse
2. Include raw output snippet for debugging
3. Continue with parseable reviewer(s)

---

## Reviewer Selection Edge Cases

### No Reviewers Selected

**Symptom:** User deselects all options

**Response:**
1. Default to claude-opus only
2. Warn: "No reviewers selected, defaulting to Claude. Consider external reviewer for fresh perspective."

### OpenCode Not Available

**Symptom:** `opencode` command not found

**Response:**
1. Warn: "OpenCode not installed, using Claude only"
2. Proceed with Claude reviewer
3. Suggest: `go install github.com/opencode-ai/opencode@latest`

---

## Spec Not Found

### No Argument, No Recent Specs

**Symptom:** No spec name provided, no specs in `./specs/draft/`

**Response:**
1. Check `./specs/active/` as fallback
2. If specs exist: list them, ask user to specify
3. If no specs: report "No specs found. Create one with /spec.create"

### Invalid Spec Name

**Symptom:** Provided name doesn't match any spec directory

**Response:**
1. List available specs
2. Suggest closest match if typo likely
3. Ask user to confirm or correct

---

## Conflicting Reviews

### Reviewers Disagree on Gate

**Symptom:** Claude passes, OpenCode fails (or vice versa)

**Response:**
1. Gate status = FAIL (conservative)
2. In summary table, show which failed
3. Include both perspectives in issues

### Reviewers Find Same Issue Differently

**Symptom:** Similar description, different wording

**Response:**
1. Deduplicate by semantic similarity
2. Combine into single issue
3. Mark `found_by: [both]` for higher confidence

---

## Empty Results

### Reviewer Returns No Issues

**Symptom:** `issues: []` in report

**Response:**
1. Valid result (spec may be solid)
2. Check if gates still passed
3. Report as clean review

### Reviewer Returns Only Strengths

**Symptom:** No issues, only strengths listed

**Response:**
1. Treat as passing review
2. Include strengths in synthesis
3. Proceed to recommendation

---

## Decision Tree

```
Start
  │
  ├─ Spec found?
  │   ├─ No → List available, ask user
  │   └─ Yes → Continue
  │
  ├─ Reviewers selected?
  │   ├─ None → Default to Claude, warn
  │   └─ Some → Continue
  │
  ├─ Dispatch reviewers
  │   │
  │   ├─ Both succeed → Synthesize
  │   ├─ One fails → Use available, note partial
  │   └─ Both fail → Report failure, suggest retry
  │
  ├─ Parse results
  │   ├─ YAML valid → Continue
  │   └─ YAML invalid → Attempt recovery, note issues
  │
  ├─ Synthesize
  │   ├─ Deduplicate issues
  │   ├─ Aggregate gates
  │   └─ Prioritize questions
  │
  ├─ Any gates failed?
  │   ├─ Yes → Recommend addressing issues
  │   └─ No → Recommend promoting
  │
  └─ End
```
