# Code Review Playbook

Edge case handling and decision trees for review scenarios.

---

## Timeout Handling

### OpenCode Timeout (> 5 minutes)

**Symptom:** `timeout` command exits with code 124

**Response:**
1. Continue with completed reviews
2. Add warning to output:
   ```
   Note: [Reviewer] timed out after 5 minutes.
   Results are partial. Consider re-running with fewer reviewers.
   ```
3. Proceed with synthesis using available data

### Claude Subagent Timeout

**Symptom:** Task tool returns timeout error

**Response:**
1. If other reviewers succeeded: use their results
2. If all failed: report failure, suggest retry
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

## Input Type Detection

### Disambiguation Flags

Flags override auto-detection:

| Flag | Forces |
|------|--------|
| `--spec` | Spec mode (final review) |
| `--rev` | Git rev/range mode |
| `--path` | Path mode |
| `--diff` | Diff mode (staged/unstaged) |

### Auto-Detection Priority (no flag)

1. **Spec** - `test -d ./specs/active/{arg}/`
2. **Git rev** - `git rev-parse --verify {arg}`
3. **Git range** - contains `..` or valid range syntax
4. **Path** - `test -e {arg}`
5. **Diff** - no argument, use staged/unstaged

### Ambiguous Input

**Symptom:** Input could match multiple types (e.g., "main" is both a branch and could be a spec)

**Response:**
1. If flag provided → use flag, skip detection
2. Otherwise, follow priority order (spec → git → path)
3. Suggest flag if detection seems wrong:
   ```
   Detected "main" as spec. Use --rev main for git branch.
   ```

---

## Review Storage

### Spec Mode

**Location:** `./specs/active/<spec>/review.yaml`
**Persistence:** Committed with spec, part of audit trail

### Other Modes (Ephemeral)

**Location:** `~/.claude/reviews/<generated-name>.md`
**Persistence:** Ephemeral, like Claude's internal plans

**Naming:**
```
review-<sha>-<timestamp>.md           # Git rev
review-<from>..<to>-<timestamp>.md    # Git range
review-<path-slug>-<timestamp>.md     # Path
review-staged-<timestamp>.md          # Staged changes
```

**Cleanup:** User manages `~/.claude/reviews/` manually

---

## Code Target Edge Cases

### No Argument, No Changes

**Symptom:** No path provided, `git diff` returns empty

**Response:**
1. Check `git diff --cached` for staged changes
2. If still empty: list recently modified files
3. Ask user to specify target

### Invalid Path

**Symptom:** Provided path doesn't exist

**Response:**
1. Check for typos (suggest closest match)
2. List files in parent directory
3. Ask user to correct

### Binary Files

**Symptom:** Target includes binary files

**Response:**
1. Skip binary files
2. Note: "Skipped N binary files"
3. Review text files only

### Large Diff

**Symptom:** Diff exceeds reasonable size (> 2000 lines)

**Response:**
1. Warn: "Large diff detected (N lines)"
2. Suggest reviewing in chunks or specific files
3. Proceed if user confirms

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
1. Deduplicate by location + semantic similarity
2. Combine into single issue
3. Mark `found_by: [both]` for higher confidence

---

## Empty Results

### Reviewer Returns No Issues

**Symptom:** `issues: []` in report

**Response:**
1. Valid result (code may be solid)
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
  ├─ Detect input type
  │   ├─ Spec exists? → Spec mode (final review)
  │   ├─ Valid git rev? → Git rev mode
  │   ├─ Contains '..'? → Git range mode
  │   ├─ Path exists? → Path mode
  │   └─ No argument? → Diff mode (staged/unstaged)
  │
  ├─ Load review context
  │   ├─ Spec → Read spec.md, tasks.yaml, review.yaml, validation.yaml
  │   ├─ Git → git show/diff, commit messages
  │   ├─ Path → Read files
  │   └─ Diff → git diff --cached or git diff
  │
  ├─ Select reviewers
  │   ├─ Spec → Use validation.yaml config (no prompt)
  │   └─ Other → Prompt user with AskUserQuestion
  │
  ├─ Dispatch reviewers (parallel)
  │   ├─ All succeed → Synthesize
  │   ├─ Some fail → Use available, note partial
  │   └─ All fail → Report failure, suggest retry
  │
  ├─ Parse results
  │   ├─ YAML valid → Continue
  │   └─ YAML invalid → Attempt recovery, note issues
  │
  ├─ Synthesize
  │   ├─ Deduplicate issues
  │   ├─ Aggregate gates
  │   └─ Prioritize by severity
  │
  ├─ Write review output
  │   ├─ Spec → ./specs/active/<spec>/review.yaml
  │   └─ Other → ~/.claude/reviews/<name>.md (ephemeral)
  │
  ├─ Present results
  │   ├─ Gate summary table
  │   ├─ Issues by severity
  │   └─ Spec: spec compliance + deferred issues
  │
  ├─ Recommend action
  │   ├─ All pass → Ready to merge/commit
  │   └─ Issues → Address before proceeding
  │
  └─ End
```
