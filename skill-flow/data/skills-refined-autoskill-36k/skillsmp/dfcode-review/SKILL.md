---
name: df:code-review
description: Core code review logic. Trigger when invoked by review commands. Do not trigger directly from user requests - use /df:review or /df:azdo:review instead.
---

# Code Review Skill v2

Analyzes code diffs by data source, not category. Each agent has a unique investigation scope with no overlap.

**Expected input from invoking command:**

- Diff content (saved to temp file)
- List of changed files
- Optional: PR metadata (title, description, author)

---

## Phase 1: Context Gathering (Sequential, Haiku)

Run these steps sequentially. Each step outputs JSON for Phase 2.

### Step 1.0: Verify Rule Files Exist

```bash
fd CLAUDE.md --type f
fd . .claude/rules --type f 2>/dev/null
```

If neither CLAUDE.md nor .claude/rules/ exist, abort: "No rule files found. Create CLAUDE.md or .claude/rules/ to enable code review."

### Step 1.1: Collect Rule Paths

**Agent instructions:**

```
Find ALL rule files in this repo. Return JSON array of absolute paths.

Search for:
- Root CLAUDE.md
- CLAUDE.md in any subdirectory
- All files in .claude/rules/
- Any linter/formatter config files in the repo root

Do not read file contents. Only return paths.

Output format: ["path/to/CLAUDE.md", ".claude/rules/sfc-structure.md", ...]
```

### Step 1.2: Detect Project Context

**Agent instructions:**

```
Detect the project type from config files and file extensions. Return JSON.

Look at:
- Config files in repo root to identify language/framework
- File extensions of changed files
- Any project-specific conventions

Output format: { "projectType": "description", "fileTypes": [".ext1", ".ext2"], "configNotes": "relevant settings" }
```

### Step 1.3: Summarize Changes

**Agent instructions:**

```
Read the diff. Return JSON summary.

Include:
- Brief summary (2-3 sentences max)
- Changed files grouped: { new: [], modified: [], deleted: [], renamed: [] }
- Imports added/removed

Do not analyze for issues yet.

Output format: { "summary": "...", "changedFiles": {...}, "importChanges": [...] }
```

---

## Phase 2: Parallel Review Agents (Sonnet)

Launch all 5 agents in parallel using Sonnet model.

**Common input to ALL agents:**

- Diff file path
- Rule file paths (from Step 1.1)
- Project context (from Step 1.2)
- Changed files list (from Step 1.3)

**False positive list (provide verbatim to ALL agents):**

```
SKIP THESE - they are false positives:

- Pre-existing issues not introduced by this diff
- Issues a linter/typechecker/compiler would catch
- Style preferences NOT explicitly in rule files
- Changes on lines not modified in the diff
- Intentional changes aligned with the PR purpose
- Test files with intentionally "bad" code
- Issues silenced by inline ignore/disable comments
- General quality issues (test coverage, docs) unless explicitly required in rules
- Obvious functionality changes that are intentional
```

---

### Agent 1: Rules Compliance

**Data source:** Rule files (.claude/rules/\*, CLAUDE.md)

**Instructions:**

```
Read EVERY rule file from the provided paths list.

For each rule file:
1. Extract each specific requirement/rule
2. Check if the diff violates that requirement
3. If violation found, cite EXACT rule text

IMPORTANT:
- Do NOT interpret or paraphrase rules
- Quote the rule verbatim
- Check exactly what the rule says, nothing more
- If rule is ambiguous, skip it

Output format per issue:
{
  "file": "path/to/file.ext",
  "line": 42,
  "issue": "Brief description of the violation",
  "ruleFile": "path/to/rule/file",
  "ruleText": "Exact quote from the rule file",
  "severity": "important"
}
```

**Investigation scope:** Rule files + diff only

---

### Agent 2: Shallow Bug Scan

**Data source:** Diff only (no external files)

**Instructions:**

```
Read the diff. Check ONLY changed/added lines for obvious bugs.

Look for:
- Logic that is clearly wrong (inverted conditions, wrong operators)
- Code that contradicts itself within the diff
- Patterns that project rules explicitly flag as bugs

Derive what counts as a "bug" from:
- Project CLAUDE.md or .claude/rules/
- Linter configs detected in Step 1.1
- Context of what the code is trying to do

Do NOT:
- Assume any particular language or framework
- Follow imports to other files
- Look at unchanged code
- Flag stylistic issues

Focus on OBVIOUS bugs only. Skip anything uncertain.

Output format per issue:
{
  "file": "path/to/file.ext",
  "line": 81,
  "issue": "Brief description of the bug",
  "why": "Explanation of why this is a bug and what will happen",
  "severity": "important"
}
```

**Investigation scope:** Diff only

---

### Agent 3: Dependency & Type Verification

**Data source:** Diff + imported files + type definitions

**Instructions:**

```
For each new/changed import in the diff:
1. Read the imported file/module
2. Find the function/type being used
3. Verify usage matches the API

For each function call to external code:
1. Find the definition (use LSP or grep)
2. Check parameter types match
3. Check return type is handled correctly

For any reusable functions/modules:
- Check if usage matches the definition
- Verify expected input types are provided
- Check if return values are handled correctly

Output format per issue:
{
  "file": "path/to/file.ext",
  "line": 123,
  "issue": "Brief description of the mismatch",
  "dependency": "function or module name",
  "expectedUsage": "correct usage pattern",
  "actualUsage": "what the code does",
  "severity": "important"
}
```

**Investigation scope:** Diff + all imported files + type definitions

---

### Agent 4: Historical Context

**Data source:** Git blame + git log

**Instructions:**

```
For each modified file:
1. Run: git blame <file>
2. For sections with recent changes: git log -p -5 -- <file>

Look for:
- Reverted changes being reintroduced
- Patterns that were previously fixed (then broken again)
- Comments explaining WHY code was written a certain way
- Recent commits that established a pattern now being violated

Check if this change contradicts recent intentional decisions.

Output format per issue:
{
  "file": "path/to/file",
  "line": 50,
  "issue": "Reintroducing pattern that was removed in abc123",
  "historicalContext": "Commit abc123 removed this because...",
  "commitRef": "abc123",
  "severity": "important"
}
```

**Investigation scope:** Git blame + git log for modified files only

---

### Agent 5: Code Comments Compliance

**Data source:** Full file content (not just diff)

**Instructions:**

```
For each modified file, read the FULL file content.

Find all comments in the file (any comment syntax for the file type).

Pay special attention to:
- TODO, FIXME, HACK, NOTE, WARNING markers
- Comments that explain WHY code is written a certain way

Check if the changes:
1. Violate guidance in nearby comments
2. Remove TODOs without resolving them
3. Ignore warnings in comments
4. Break invariants described in comments

Output format per issue:
{
  "file": "path/to/file",
  "line": 42,
  "issue": "Change violates comment above",
  "commentText": "// WARNING: Do not modify without updating X",
  "severity": "important"
}
```

**Investigation scope:** Full file content for modified files

---

## Phase 3: Issue Scoring (Parallel Haiku)

For EACH issue from Phase 2, launch a separate Haiku agent.

**Limit:** Score max 15 issues. If more found, sort by apparent severity first.

**Agent instructions:**

```
You are verifying a potential code review issue.

Issue: {issue.issue}
File: {issue.file}
Line: {issue.line}
Found by: {agent name}
Reason: {issue.why or issue.ruleText}

Rule files available: {paths from Step 1.1}
Relevant diff section: {context around the line}

TASK: Score this issue 0-100.

SCORING RUBRIC (use exactly):

0: False positive. Doesn't stand up to scrutiny. Pre-existing issue. Not actually a bug.

25: Might be real but unverified. If stylistic, not explicitly in any rule file.

50: Real but minor. Nitpick. Rarely hit in practice. Low impact.

75: Verified real issue. Will impact functionality. OR explicitly mentioned in rule files.

100: Definitely real. Confirmed with evidence. Will happen frequently. High impact.

VERIFICATION STEPS:
- For rule-based issues: Re-read the rule file. Confirm it actually says this.
- For bug issues: Trace the code path. Confirm the bug can actually occur.
- For dependency issues: Check if surrounding code handles the case.

Output: { "score": 75, "reasoning": "..." }
```

---

## Phase 4: Filter & Format

### Filtering

1. Keep only issues with score ≥ 75
2. If zero issues remain, output "No issues found"

### Grouping

- Critical: score ≥ 90
- Important: score 75-89

### Output Format

```markdown
## Code Review: {branch or PR title}

**Files changed:** X | **Issues found:** X critical, X important

### Critical Issues (score ≥90)

- **[file:line]** Issue description
  - **Evidence:** {rule text / commit ref / comment}
  - **Fix:** Suggested resolution

### Important Issues (score 75-89)

- **[file:line]** Issue description
  - **Evidence:** {rule text / commit ref / comment}
  - **Fix:** Suggested resolution

### Minor Notes (informational)

{Any observations that didn't meet threshold but worth mentioning}

### Summary

- **Recommendation:** approve | request-changes | needs-discussion
- **Risk areas:** {list if any}
```

### Save to File

After generating the review, save it to `.aiwork/reviews/`:

1. Create directory if needed: `mkdir -p .aiwork/reviews`
2. Generate timestamp: `date +%Y-%m-%d_%H-%M`
3. Save as: `.aiwork/reviews/{timestamp}_{branch-name}.md`
   - Example: `.aiwork/reviews/2025-01-15_14-30_feature-auth.md`
4. Confirm save location to user

---

## Error Handling

- **Failed agents:** Skip, continue with others. Log warning. Partial review > no review.
- **Large diffs (>50 files):** Warn user and ask whether to proceed or filter by priority.
- **Missing rules:** Require CLAUDE.md or .claude/rules/ to exist. Abort with message if neither found.
- **Unparseable files:** Auto-skip binary/minified/generated. No output noise.

## Notes

- This skill is invoked by commands, not directly by users
- Commands provide the diff; skill provides the analysis
- Agents defined by data source, not category - ensures no overlap
- Rules passed as paths; agents read directly - no paraphrasing
