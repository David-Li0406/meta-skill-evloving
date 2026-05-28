---
name: doc-polisher
description: Polish documents through iterative review loops. Use when user wants to improve a doc, polish a file, fix inconsistencies, make something more concise, or clean up a document.
context: fork
allowed-tools: Task, Read, Write, Edit, Bash(node:*), AskUserQuestion
user-invocable: true
---

# Doc Polisher

Iteratively improve any document through multi-phase review loops:

1. **Phase 1**: Claude self-review loop (find issues → fix → repeat)
2. **Phase 2**: Codex cross-validation loop (find issues Claude missed)
3. **Phase 3**: Interactive resolution (user resolves ambiguities)

## Design Principle: In-Place Enhancement

Unlike plan-fixer, this skill does NOT restructure or convert the file format. It:
- Keeps the original format intact
- Fixes issues in-place
- Only changes content, not structure
- Preserves author's voice and style (unless inconsistent)

## Configuration

- **Max Iterations**: 5 per phase
- **Auto-fix**: Inconsistencies, redundancies, formatting
- **Ask User**: Ambiguities, vague content, unresolved TODOs
- **Preserve**: Structure, format, intentional style choices
- **Codex Timeout**: 1200000ms (20 minutes) - MANDATORY, do not use shorter timeouts

## Parameters

Detect these parameters from the user's request:

| Parameter | Trigger Phrases | Effect |
|-----------|-----------------|--------|
| `codex-fix` | "let Codex fix", "Codex can fix" | Codex fixes issues directly with `--full-auto` |
| `aggressive` | "make it concise", "trim it down", "aggressive" | More aggressive content removal |
| `conservative` | "minimal changes", "conservative", "careful" | Only fix clear errors, preserve more |
| `file_type` | Auto-detected or specified | Adjusts issue criteria (see below) |

### File Type Detection

Auto-detect from extension, or user can specify:

| Type | Extensions | Special Handling |
|------|------------|------------------|
| `markdown` | .md | Check heading hierarchy, link validity |
| `plan` | Contains `<task>`, `<action>` | Use plan-specific criteria |
| `config` | .yml, .yaml, .json, .toml | Check schema consistency |
| `code` | .ts, .js, .py, etc. | Check naming conventions, comments |
| `prose` | .txt, generic .md | Focus on clarity and flow |

## Issue Categories

### Auto-Fixable Issues

| Issue | Description | Fix Strategy | Condition |
|-------|-------------|--------------|-----------|
| **Inconsistent terminology** | Same concept, different names | Standardize to dominant | Auto-fix if dominant term >70%; else ask user |
| **Redundant content** | Same thing said twice | Remove duplicate | Always auto-fix |
| **Formatting inconsistency** | Mixed styles (bullets vs numbers) | Standardize | Always auto-fix |
| **Broken internal refs** | Links to non-existent sections | Fix or flag | Auto-fix if target exists; else ask user |
| **Trailing whitespace** | Extra spaces, blank lines | Clean up | Always auto-fix |
| **Incomplete lists** | List with single item | Convert to prose or expand | Always auto-fix |

### Requires User Input

| Issue | Description | Prompt Strategy |
|-------|-------------|-----------------|
| **Vague instruction** | "handle appropriately" | Offer specific options |
| **Ambiguous scope** | Could mean X or Y | Ask for clarification |
| **Unresolved TODO** | Placeholder content | Ask for resolution |
| **Missing context** | Assumes knowledge not provided | Ask what to add |
| **Subjective choice** | Multiple valid approaches | Let user decide |

## Workflow

### Phase 1: Claude Self-Review Loop

```
iteration = 0
issues_fixed_total = 0
attempted_fixes = []  # Track issues already attempted
change_log = []       # Audit trail of all changes (see references/change-log-format.md)

while iteration < 5:
    1. Spawn issue-finder agent on the file
       - Input: file_path, file_type, mode (aggressive/conservative)
       - Output: [{issue, severity, type, location, quote, auto_fixable, suggestions}]
       - Note: `suggestions` is always an array (use suggestions[0] for auto-fix)

    2. Separate issues:
       - auto_fixable_issues = issues where auto_fixable == true
       - user_issues = issues where auto_fixable == false
       - Note: Only issues with auto_fixable == false go to Phase 3

    3. If no auto_fixable issues with severity "critical" or "major":
       - Fix any remaining minor auto_fixable issues (formatting, whitespace, etc.)
       - Store user_issues for Phase 3
       - Exit Phase 1

    4. For each auto_fixable issue (critical/major first):
       # Duplicate detection - skip issues already attempted
       issue_key = hash(issue.type + issue.location + issue.quote)
       IF issue_key in attempted_fixes:
         - Log: "Skipping duplicate issue at [location]"
         - continue
       attempted_fixes.append(issue_key)

       - Report: "Found: [issue] at [location]"
       - Spawn issue-fixer agent
       - Report: "Fixed: [description]"
       - Log change: change_log.append({phase: 1, issue, before, after, source: "claude"})
       - issues_fixed_total++

    5. iteration++

Report: "Phase 1 complete. Fixed [N] issues in [M] iterations."
Store: user_issues for Phase 3
```

### Phase 2: Codex Cross-Validation Loop

#### Error Handling

```
ON codex-bridge failure (timeout, connection error, crash):
  - Log warning: "⚠️ Codex unavailable, skipping Phase 2"
  - Set phase2_skipped = true
  - Skip to Phase 3
  - Note in final report: "Phase 2 skipped (Codex unavailable)"

ON invalid JSON from Codex:
  - Log warning: "⚠️ Codex returned invalid response, retrying..."
  - Retry once with same prompt
  - If still invalid:
    - Log warning: "⚠️ Codex response invalid after retry, skipping Phase 2"
    - Set phase2_skipped = true
    - Skip to Phase 3
    - Note in final report: "Phase 2 skipped (invalid Codex response)"

ON empty response from Codex:
  - Treat as "no issues found"
  - Exit Phase 2 normally
```

#### Schema Validation

After parsing Codex JSON response, validate each issue object:

```
VALID_TYPES = [
  "vague_instruction", "ambiguous_scope", "unresolved_todo",
  "inconsistent_terminology", "broken_reference", "redundant_content",
  "formatting_inconsistency", "missing_definition", "contradiction",
  "trailing_whitespace", "incomplete_list", "missing_context"
]

for each issue in codex_response:
  # Required fields check
  IF missing(issue.issue, issue.severity, issue.location, issue.quote):
    Log: "Warning: Codex issue missing required fields, skipping"
    continue

  # Type validation
  IF issue.type not in VALID_TYPES:
    Log: "Warning: Unknown issue type '[issue.type]', treating as non-auto-fixable"
    issue.type = "unknown"
    issue.auto_fixable = false

  # Severity validation
  IF issue.severity not in ["critical", "major", "minor"]:
    Log: "Warning: Invalid severity '[issue.severity]', defaulting to 'major'"
    issue.severity = "major"

  # Ensure suggestions array exists
  IF issue.suggestions is undefined or not array:
    issue.suggestions = [issue.suggestion] if issue.suggestion else []
```

#### Default Mode (codex-fix: OFF)
```
iteration = 0
codex_attempted_fixes = []  # Prevent infinite loops on same Codex finding

while iteration < 5:
    1. Call Codex via codex-bridge:
       "Review this document for issues Claude may have missed..."

    2. Parse Codex response for issues (see schema validation below)

    3. Spawn codex-validator agent to verify each finding:
       - Is this a real issue?
       - Was it already fixed?
       - Is it subjective preference?

       IF validation == "INVALID":
         - Log: "Rejected Codex finding: [rejection_reason]"
         - Skip this issue (do not add to user_issues)
         - continue to next finding

    4. If no valid issues → exit Phase 2

    5. For each validated issue (validation == "VALID"):
       # Duplicate detection - prevent infinite loops
       issue_key = hash(issue.type + issue.location + issue.quote)
       IF issue_key in codex_attempted_fixes:
         - Log: "Skipping duplicate Codex finding at [location]"
         - continue
       codex_attempted_fixes.append(issue_key)

       - If auto_fixable:
         - Report: "Codex found: [issue]"
         - Spawn issue-fixer agent
         - Report: "Fixed: [description]"
         - Log change: change_log.append({phase: 2, issue, before, after, source: "codex"})
       - If requires user input:
         - Add to user_issues for Phase 3

    6. iteration++

Report: "Phase 2 complete."
```

#### Codex-Fix Mode (codex-fix: ON)
```
iteration = 0

while iteration < 5:
    1. Call Codex with --full-auto:
       "Find AND fix issues in this document..."

    2. Spawn codex-validator to verify fixes:
       - Were fixes appropriate?
       - Any regressions introduced?

    3. If fixes invalid:
       - Revert changes
       - Spawn issue-fixer agent instead

    4. If no changes made → exit Phase 2

    5. iteration++

Report: "Phase 2 complete."
```

### Phase 3: Interactive Resolution

**Types that reach Phase 3** (auto_fixable == false):
- `vague_instruction`, `ambiguous_scope`, `unresolved_todo`, `missing_context`
- `broken_reference` (when target can't be auto-resolved)
- `missing_definition`, `contradiction`
- `inconsistent_terminology` (only when no term has >70% majority)

**Types that should NOT reach Phase 3** (auto-fixed in Phase 1/2):
- `redundant_content`, `formatting_inconsistency`, `trailing_whitespace`, `incomplete_list`
- `inconsistent_terminology` (when one term has >70% majority)

```
# Handle empty user_issues
IF user_issues is empty:
  Report: "✅ No ambiguities require user input"
  Skip to Final Output

For each issue in user_issues (sorted by severity):

    1. Build prompt based on issue type:

       IF issue.type == "vague_instruction":
         AskUserQuestion:
           question: "This instruction is vague: '[quote]'. What should it specify?"
           options:
             - label: issue.suggestions[0]
             - label: issue.suggestions[1]
             - label: "Keep as-is (context makes it clear)"
             - label: "Remove (not needed)"

       IF issue.type == "ambiguous_scope":
         AskUserQuestion:
           question: "'[quote]' could mean different things. Which interpretation?"
           options:
             - label: "Interpretation A: [description]"
             - label: "Interpretation B: [description]"
             - label: "Both (clarify in text)"
             - label: "Keep ambiguous (intentional flexibility)"

       IF issue.type == "unresolved_todo":
         AskUserQuestion:
           question: "Found unresolved: '[TODO text]'"
           options:
             - label: "Replace with: [suggestion]"
             - label: "Remove TODO entirely"
             - label: "Keep TODO (will resolve later)"

       IF issue.type == "inconsistent_terminology":
         # Only reaches Phase 3 when term counts are close (no term >70%)
         AskUserQuestion:
           question: "Mixed terms with similar frequency: [term1] (Nx), [term2] (Nx). Which to standardize?"
           options:
             - label: "Use '[term1]' everywhere"
             - label: "Use '[term2]' everywhere"
             - label: "Keep as-is (intentionally different meanings)"

       IF issue.type == "broken_reference":
         # Only reaches Phase 3 when target cannot be auto-resolved
         AskUserQuestion:
           question: "Broken reference: '[quote]' points to non-existent target."
           options:
             - label: "Update to: [suggested_target]"
             - label: "Remove the reference entirely"
             - label: "Keep as-is (will fix target later)"

       IF issue.type == "missing_definition":
         AskUserQuestion:
           question: "Term '[quote]' is used but never defined."
           options:
             - label: "Add definition: [suggestion]"
             - label: "Link to external documentation"
             - label: "Remove usage of undefined term"
             - label: "Keep as-is (readers will understand)"

       IF issue.type == "contradiction":
         AskUserQuestion:
           question: "Contradiction found: '[quote1]' conflicts with '[quote2]'."
           options:
             - label: "Keep first statement, remove second"
             - label: "Keep second statement, remove first"
             - label: "Rewrite to reconcile both"
             - label: "Keep both (different contexts)"

       IF issue.type == "missing_context":
         AskUserQuestion:
           question: "This assumes knowledge not provided: '[quote]'"
           options:
             - label: "Add context: [suggestion]"
             - label: "Link to prerequisite documentation"
             - label: "Remove assumption"
             - label: "Keep as-is (target audience knows this)"

       # Fallback for unknown or unmapped issue types
       ELSE:
         Log: "Warning: Unknown issue type '[issue.type]' - using generic prompt"
         AskUserQuestion:
           question: "Issue found: [issue.issue] at [location]"
           options:
             - label: "Apply suggested fix: [suggestion]"
             - label: "Keep as-is"
             - label: "Remove problematic content"

    2. Apply user's choice:
       - Spawn issue-fixer with specific instruction
       - Report: "Applied: [choice]"
       - Log change: change_log.append({phase: 3, issue, before, after, source: "user"})

    3. Continue to next issue

Report: "Phase 3 complete. Resolved [N] ambiguities."
```

### Post-Phase 3: Final Validation

```
# Verify fixes didn't introduce new issues
1. Run issue-finder one final time (conservative mode)

2. Compare new issues against change_log:
   - Filter out issues that existed before we started
   - Identify genuinely NEW issues introduced by fixes

3. IF new_issues found:
   - Warn: "⚠️ Fixes may have introduced [N] new issues:"
   - List each new issue with likely cause (which fix introduced it)
   - Add to final report

4. IF no new issues:
   - Report: "✅ Validation passed - no residual issues"

5. Generate final report with change_log
```

## How to Execute

When user asks to polish/improve a document:

1. **Read the file**
2. **Detect file type** (from extension or content)
3. **Determine mode** (aggressive/conservative/default)
4. **Execute Phase 1** (Claude Self-Review):
   - Use Task tool with `issue-finder` agent
   - Parse response for issues
   - For auto-fixable issues, use Task tool with `issue-fixer` agent
   - Collect user-input issues for Phase 3
   - Re-analyze until clean or max iterations
5. **Execute Phase 2** (Codex Cross-Validation):
   - Call codex-bridge with document content
   - Use Task tool with `codex-validator` agent
   - Fix valid issues, collect ambiguities for Phase 3
   - Re-ask Codex until clean or max iterations
6. **Execute Phase 3** (Interactive Resolution):
   - For each collected ambiguity
   - Use AskUserQuestion with relevant options
   - Apply user choices via issue-fixer
7. **Execute Final Validation**:
   - Run issue-finder one last time
   - Check for new issues introduced by fixes
   - Warn if regressions found
8. **Report completion** with change log

## Progress Update Format

```
📄 Doc Polisher Starting...
📖 File: [filename]
📋 Type: [detected type]
⚙️ Mode: [default|aggressive|conservative]

🔄 Phase 1: Claude Self-Review
   Iteration 1/5:
   - Analyzing for issues...
   - Found 4 issues (2 auto-fixable, 2 need input)
   - Fixing: Inconsistent terminology "user/customer" → Standardized to "user" ✓
   - Fixing: Redundant paragraph in section 3 → Removed ✓
   - Deferred: Vague instruction at line 45 (will ask in Phase 3)
   - Deferred: Unresolved TODO at line 78 (will ask in Phase 3)

   Iteration 2/5:
   - Analyzing for issues...
   - Found 1 issue (1 auto-fixable)
   - Fixing: Inconsistent bullet style → Standardized ✓

   Iteration 3/5:
   - Analyzing for issues...
   - No auto-fixable issues found
   ✅ Phase 1 complete (3 iterations, 3 issues fixed)

🔄 Phase 2: Codex Cross-Validation
   Iteration 1/5:
   - Asking Codex for issues Claude missed...
   - Codex found 2 potential issues
   - Validating: "Missing error handling" → Valid, auto-fixing ✓
   - Validating: "Could be more concise" → Subjective, skipping

   Iteration 2/5:
   - Asking Codex for issues...
   - No issues found
   ✅ Phase 2 complete (2 iterations, 1 issue fixed)

💬 Phase 3: Interactive Resolution

   ┌─────────────────────────────────────────────────┐
   │ Issue 1/2: Vague Instruction                    │
   ├─────────────────────────────────────────────────┤
   │ "Validate the input appropriately"             │
   │                                                 │
   │ What validation is needed?                      │
   │ ○ Format validation only                        │
   │ ○ Format + sanitization (XSS/injection)         │
   │ ○ Format + sanitization + business rules        │
   │ ○ Keep as-is                                    │
   └─────────────────────────────────────────────────┘
   User selected: "Format + sanitization"
   - Applied ✓

   ┌─────────────────────────────────────────────────┐
   │ Issue 2/2: Unresolved TODO                      │
   ├─────────────────────────────────────────────────┤
   │ "TODO: decide on caching strategy"              │
   │                                                 │
   │ ○ Use Redis with 5min TTL                       │
   │ ○ No caching for MVP                            │
   │ ○ Keep TODO (resolve later)                     │
   │ ○ Remove entirely                               │
   └─────────────────────────────────────────────────┘
   User selected: "No caching for MVP"
   - Applied ✓

   ✅ Phase 3 complete (2 ambiguities resolved)

🎉 Document polished!
   File: [filename]
   Issues fixed: 6 (Claude: 3, Codex: 1, User: 2)
   Iterations: Phase 1 (3) + Phase 2 (2) + Phase 3 (2 prompts)
```

## Codex Integration

**Setup (run once per session):**
```bash
# Find codex-bridge script (marketplace install path)
CODEX_BRIDGE=$(ls -1 "$HOME/.claude/plugins/cache/saurun-marketplace/saurun/"*/skills/codex-bridge/codex-bridge.mjs 2>/dev/null | head -1)

# MANDATORY: Define timeout constant - DO NOT change this value
CODEX_TIMEOUT=1200000  # 20 minutes in milliseconds
```

**CRITICAL:** Always pass `--working-dir "<project-path>"` so Codex can read project files.

**⚠️ MANDATORY TIMEOUT: Always use `--timeout 1200000` (20 minutes) for ALL Codex calls.**
- DO NOT use shorter timeouts (e.g., 300000)
- Codex needs time to analyze documents thoroughly
- Short timeouts cause premature failures

### Review Prompt (Default Mode)

```bash
node "$CODEX_BRIDGE" --timeout 1200000 "Review this document for issues that may have been missed.

DOCUMENT TYPE: [file_type]
MODE: [aggressive|conservative|default]

LOOK FOR:
1. Vague instructions (reader would have to guess intent)
2. Inconsistent terminology (same thing, different names)
3. Missing information (referenced but not defined)
4. Redundant content (same thing said multiple ways)
5. Unclear scope (ambiguous boundaries)
6. Broken references (links/mentions to non-existent things)
7. Unresolved placeholders (TODOs, TBDs, ???)

DO NOT FLAG:
- Stylistic preferences (unless inconsistent)
- Subjective "could be better" suggestions
- Things already flagged and fixed

Return a JSON array:
[{
  \"issue\": \"description\",
  \"type\": \"issue type (e.g., vague_instruction, inconsistent_terminology)\",
  \"severity\": \"critical|major|minor\",
  \"location\": \"line number or section\",
  \"quote\": \"the problematic text\",
  \"auto_fixable\": true|false,
  \"suggestions\": [\"array of fix options\"]
}]

Note: Schema validation will normalize responses (see Phase 2 Schema Validation section).

If no issues: []

===== DOCUMENT =====
[FULL DOCUMENT CONTENT]
===== END DOCUMENT =====
" --working-dir "$PROJECT_PATH"
```

### Review + Fix Prompt (Codex-Fix Mode)

```bash
node "$CODEX_BRIDGE" --timeout 1200000 "Review this document for issues and FIX them directly.

DOCUMENT TYPE: [file_type]
MODE: [aggressive|conservative|default]

FIX THESE ISSUES:
1. Inconsistent terminology → standardize to most common term
2. Redundant content → remove duplicates, keep best version
3. Formatting inconsistencies → standardize style
4. Minor clarity issues → reword for clarity

DO NOT FIX (flag only):
- Vague instructions (need user input)
- Ambiguous scope (need user decision)
- Unresolved TODOs (need user resolution)
- Missing information (need user to provide)

After fixing, return JSON summary:
{
  \"fixed\": [{
    \"issue\": \"what was wrong\",
    \"type\": \"issue type\",
    \"fix\": \"what you changed\",
    \"location\": \"where\"
  }],
  \"needs_user\": [{
    \"issue\": \"description\",
    \"type\": \"issue type\",
    \"location\": \"where\",
    \"suggestions\": [\"option1\", \"option2\"]
  }]
}

Note: Schema validation will normalize responses.

FILE TO EDIT: [filepath]

===== DOCUMENT =====
[FULL DOCUMENT CONTENT]
===== END DOCUMENT =====
" --full-auto --working-dir "$PROJECT_PATH"
```

## Sub-Agents

This skill uses three sub-agents defined in the `agents/` folder:

1. **issue-finder**: Analyzes document for issues, returns structured list
2. **issue-fixer**: Fixes a specific issue in-place
3. **codex-validator**: Validates whether a Codex-identified issue is real (reuse from plan-fixer)

## Final Output

```
╔══════════════════════════════════════════════════════════════╗
║                   DOCUMENT POLISH REPORT                     ║
╠══════════════════════════════════════════════════════════════╣
║ File: [filename]                                             ║
║ Type: [file_type]                                            ║
║ Mode: [default|aggressive|conservative]                      ║
║ Status: ✅ POLISHED | ⚠️ PARTIALLY POLISHED | ❌ MAX ITERATIONS║
╠══════════════════════════════════════════════════════════════╣
║ PHASE 1: Claude Self-Review                                  ║
╟──────────────────────────────────────────────────────────────╢
║ Iterations: 3                                                ║
║ Issues found: 4                                              ║
║ Auto-fixed: 2                                                ║
║ Deferred to Phase 3: 2                                       ║
╠══════════════════════════════════════════════════════════════╣
║ PHASE 2: Codex Cross-Validation                              ║
╟──────────────────────────────────────────────────────────────╢
║ Status: ✅ Completed | ⚠️ Skipped (Codex unavailable)         ║
║ Iterations: 2                                                ║
║ Issues found: 2                                              ║
║ Valid issues: 1                                              ║
║ Fixed: 1                                                     ║
╠══════════════════════════════════════════════════════════════╣
║ PHASE 3: Interactive Resolution                              ║
╟──────────────────────────────────────────────────────────────╢
║ Ambiguities presented: 2                                     ║
║ User resolved: 2                                             ║
║ Kept as-is: 0                                                ║
╠══════════════════════════════════════════════════════════════╣
║ CHANGE LOG (abbreviated)                                     ║
╟──────────────────────────────────────────────────────────────╢
║ [p1-i1-c1] inconsistent_terminology @ line 12                ║
║   "user" → "customer"                                        ║
║ [p1-i1-c2] redundant_content @ section "Overview"            ║
║   Removed duplicate paragraph                                ║
║ [p2-i1-c3] formatting_inconsistency @ lines 45-50            ║
║   Mixed bullets → "-"                                        ║
║ ... (full log available if verbose mode)                     ║
╠══════════════════════════════════════════════════════════════╣
║ SUMMARY                                                      ║
╟──────────────────────────────────────────────────────────────╢
║ Total issues fixed: 5                                        ║
║   - By Claude: 2                                             ║
║   - By Codex: 1                                              ║
║   - By User: 2                                               ║
║ Validation: ✅ Passed | ⚠️ [N] new issues introduced          ║
║ Document ready: ✅                                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Status Definitions

- **✅ POLISHED**: All phases completed, no remaining issues
- **⚠️ PARTIALLY POLISHED**: Completed but user skipped some ambiguities
- **❌ MAX ITERATIONS**: Hit iteration limit, issues may remain

## References

- `references/issue-criteria.md` - Issue type enumeration and detection criteria per file type
- `references/change-log-format.md` - Change tracking format for audit trail
