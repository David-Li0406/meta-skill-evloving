# Implementation Review Workflow

## Philosophy: Context Over Convenience

The reviewer model only sees selected files—it's blind to the rest of the codebase. RepoPrompt's Context Builder (hereafter "Builder") is AI-powered—its strength is **discovering related context** the reviewer needs:
- Existing patterns the changes should follow
- Similar implementations for consistency
- Architectural context (how things connect)
- Dependencies and side effects

We already KNOW the changed files. Builder's job is finding the **surrounding context** that makes review meaningful.

**Key insight:** Builder produces a handoff prompt (factual, non-opinionated). We take that as foundation, then add our review criteria on top.

---

## Phase 0: Window Selection

**CRITICAL**: Always start by listing windows and selecting the correct one.

```bash
rp-cli -e 'windows'
```

Output shows window IDs with workspace names. **Identify the window for the project you're reviewing.**

For all subsequent commands, use `-w <id>` to target that window:
```bash
rp-cli -w 1 -e 'tree --folders'
```

**Tab Isolation (for parallel agents):**

`builder` automatically creates an isolated compose tab with an AI-generated name. Subsequent commands in the same rp-cli invocation stay in that tab. For separate invocations, rebind by name or UUID:
```bash
# Builder output includes: Tab: <UUID> • <Name>
# Rebind in later commands:
rp-cli -w 1 -e 'workspace tab "<Name>" && select add file.md'
```

When possible, chain commands in single invocations to maintain tab context:
```bash
rp-cli -w W -e 'builder "..." && select add changed.ts && select get'
```

---

## Phase 1: Identify Changes & Extract Intent

Get the current branch and changed files:
```bash
git branch --show-current
git log main..HEAD --oneline 2>/dev/null || git log master..HEAD --oneline
git diff main..HEAD --name-only 2>/dev/null || git diff master..HEAD --name-only
git diff main..HEAD --stat 2>/dev/null || git diff master..HEAD --stat
```

Save the list of changed files for later selection (Phase 3).

**Compose a concise but descriptive summary** of what the changes accomplish (for builder prompt). Simple changes: 1-2 sentences. Large features: brief paragraph capturing key scope. Look at:
- Commit messages
- Branch name
- Nature of the changes

**Examples:**
- Simple: "Add OAuth authentication to the API"
- Medium: "Fix race condition in payment processing by adding mutex locks and retry logic"
- Complex: "Rebuild notification system with WebSocket delivery, user preferences, batching, and multi-channel support"

---

## Phase 2: Gather Supporting Docs

Search for the plan, PRD, and beads issue that drove this work (replace W with your window ID from Phase 0):
```bash
# Find plan files
rp-cli -w W -e 'search "docs/plan" --mode path'
rp-cli -w W -e 'search "docs/impl" --mode path'

# Find PRD
rp-cli -w W -e 'search "PRD" --mode path'
rp-cli -w W -e 'search "prd_" --mode path'

# Find beads JSONL
rp-cli -w W -e 'search ".beads/" --mode path'

# Check commit messages for issue references
git log main..HEAD --format="%B" 2>/dev/null || git log master..HEAD --format="%B"
```

Read any relevant docs you find:
```bash
rp-cli -w W -e 'read docs/plan/xxx.md'
```

**Beads context**: If you know which Beads issue(s) this work relates to (from conversation, commits, or user), save for inclusion in the review prompt via `bd show <id>`.

---

## Phase 3: Context Discovery & Selection

### Step 1: Run builder with intent (not details)

Give builder a simple, intent-focused prompt. Let it discover context autonomously:
```bash
rp-cli -w W -e 'builder "Review implementation of [CONCISE SUMMARY FROM PHASE 1] on the current branch"'
```

**Examples:**
- Simple: `"Review implementation of OAuth authentication on the current branch"`
- Medium: `"Review implementation of payment race condition fix with mutex locks and retry logic on the current branch"`
- Complex: `"Review implementation of notification system rebuild with WebSocket delivery, preferences, and multi-channel support on the current branch"`

⚠️ **DO NOT** list changed files in the prompt. Builder discovers relevant context; we add changed files after.

⚠️ **WAIT**: Builder takes 30s-5min. Do NOT proceed until it returns output. Do NOT send another builder command—just wait for the current one to complete.

### Step 2: Capture builder's handoff prompt

Builder returns:
- File selection (what it discovered as relevant)
- Handoff prompt (factual summary of context)
- Open questions (ambiguities it identified)

**Save the handoff prompt** - this becomes the foundation for your review prompt.

Get the current prompt:
```bash
rp-cli -w W -e 'prompt get'
```

### Step 3: Review and augment selection

Builder is AI-driven and non-deterministic. Review what it found, then add must-haves:
```bash
# Check what builder selected
rp-cli -w W -e 'select get'

# Add ALL changed files from Phase 1 (builder may not have selected them all)
rp-cli -w W -e 'select add path/to/changed/file1.ts'
rp-cli -w W -e 'select add path/to/changed/file2.ts'
# ... add all changed files

# Add supporting docs from Phase 2 (plan, PRD, etc.)
rp-cli -w W -e 'select add <path-to-plan>'

# Add any files you know are critical that builder missed
```

### Step 4: Verify final selection

```bash
rp-cli -w W -e 'select get'
```

Confirm selection includes:
- All changed files from Phase 1
- Supporting docs from Phase 2
- Related patterns/code builder discovered
- Anything else needed for thorough review

**Why this matters:** Chat only sees selected files. Missing context = incomplete review.

---

## Phase 4: Carmack-Level Review

### Step 1: Build the review prompt

Combine three pieces:
1. **Builder's handoff prompt** (from Phase 3 Step 2) - factual context foundation
2. **Review criteria** - Carmack-level checklist
3. **User's focus areas** (from arguments) - specific concerns to prioritize

**Prompt structure:**
```
[BUILDER'S HANDOFF PROMPT - paste as-is]

---

## Changes Under Review
Branch: [BRANCH_NAME]
Files changed: [LIST FILES]
Commits: [COMMIT SUMMARY]

## Original Plan/Spec
[INCLUDE PLAN CONTENT OR `bd show` OUTPUT IF BEADS]

## Review Focus
[USER'S FOCUS AREAS FROM ARGUMENTS, if any]

## Review Criteria

Conduct a John Carmack-level review. Evaluate against:

### 1. Correctness
- Matches plan/spec?
- Logic errors?
- All requirements met?

### 2. Simplicity & Minimalism
- Simplest solution?
- Unnecessary abstraction?
- Dead code / unused imports?
- Over-engineering?

### 3. DRY & Code Reuse
- Duplicated logic?
- Reinventing utilities?
- Could leverage existing patterns?

### 4. Idiomatic Code
- Follows codebase patterns?
- Naming conventions consistent?
- Type safety appropriate?

### 5. Architecture & Design
- Data flow makes sense?
- Clear boundaries?
- Circular dependencies?

### 6. Edge Cases & Error Handling
- Unhandled failure modes?
- Race conditions?
- Errors swallowed?

### 7. Testability & Tests
- Tests adequate?
- Edge case coverage?
- Testing behavior vs implementation?

### 8. Performance
- O(n²) or worse?
- Unnecessary allocations?
- N+1 queries?

### 9. Security
- Injection vulnerabilities?
- Auth/authz gaps?
- Input sanitization?

### 10. Maintainability
- Future devs will understand?
- Abstractions earning complexity?
- Self-documenting?

## Issue Quality

- Only flag issues **introduced by this change**
- Cite **actual affected code**
- Specify **trigger conditions**

## Output Format

For each issue:
1. **Severity**: Critical / Major / Minor / Nitpick
2. **File:Line**: Exact location
3. **Problem**: What's wrong
4. **Suggestion**: How to fix (with code if helpful)
5. **Rationale**: Why it matters

End with:
- Overall: Ship / Needs Work / Major Rethink
- Patterns from codebase the code should adopt
- What the implementation does well

**List ALL issues.** Agent fixes all Critical/Major/Minor before re-review.
```

### Step 2: Execute review

Use chat in **chat mode**. The chat sees all selected files.

**Initial review** - MUST use raw `call chat_send` with `"new_chat": true`:
```bash
rp-cli -w W -e 'call chat_send {"message": "<COMBINED_PROMPT>", "mode": "chat", "new_chat": true, "chat_name": "Impl Review: [BRANCH_NAME]"}'
```

⚠️ **JSON escaping**: Message must use `\n` for newlines, not literal line breaks.

⚠️ **WAIT FOR RESPONSE**: Chat takes 1-5+ minutes. Do NOT re-send or follow up until it returns.

**Follow-up/re-review command**:
```bash
rp-cli -w W -e 'call chat_send {"message": "<FOLLOW_UP_MESSAGE>", "mode": "chat"}'
```

Note: Files are automatically refreshed on each message - no `selected_paths` needed for follow-ups.

---

## Phase 4 Alternative: Export for External Review

If user chose **export mode**, skip the chat and export context instead.

### Step 1: Set the review prompt

Build the combined prompt (same structure as Phase 4 Step 1), then set it:
```bash
rp-cli -w W -e 'prompt set "<COMBINED_PROMPT>"'
```

The prompt should include:
- Builder's handoff prompt (foundation)
- Changes summary (branch, files, commits)
- Plan/spec content if found
- User's focus areas
- Review criteria checklist

### Step 2: Export to file

```bash
rp-cli -w W -e 'prompt export ~/Desktop/impl-review-[BRANCH].md'
```

This exports: file tree, codemaps, selected file contents, and the review prompt.

### Step 3: Open for user

```bash
open ~/Desktop/impl-review-[BRANCH].md
```

### Step 4: Inform user

Tell the user:
```
Exported review context to ~/Desktop/impl-review-[BRANCH].md

The file contains:
- Full file tree with selected files marked
- Code maps (signatures/structure)
- Complete file contents
- Review prompt with Carmack-level criteria

Paste into ChatGPT Pro, Claude web, or your preferred LLM.
After receiving feedback, return here to implement fixes.
```

**Skip the Iteration and Fix loops** — user handles those externally.

---

## Iteration

Continue the chat to drill deeper if needed:
```bash
rp-cli -w W -e 'call chat_send {"message": "Elaborate on the [SPECIFIC CONCERN]. Show me exactly what you would change in [FILE].", "mode": "chat"}'
```

---

## Fix and Re-Review Loop

**CRITICAL**: After receiving review feedback, **implement all fixes directly**—edit the code, don't just acknowledge issues.

### What MUST be fixed:
- **Critical**: Fix immediately, no exceptions
- **Major**: Fix immediately, no exceptions
- **Minor**: Fix immediately—these are real issues, not optional polish

### What MAY be skipped:
- **Nitpick**: Optional style/preference items—fix if easy, skip if not

### The Loop

1. **Parse the review**: Extract all issues by severity
2. **Fix Critical → Major → Minor**: Edit the code files to address each
   - Use Edit tool for targeted changes
   - Run tests/lints after each batch of fixes
3. **Augment selection** (if needed): Add any files touched during fixes that aren't already selected
   ```bash
   rp-cli -w W -e 'select add path/to/newly-edited-file.ts'
   ```
4. **Re-review**: Continue the existing chat with detailed fix explanations

**Re-review message template:**
```
## Fixes Applied

### Critical fixes:
[If any - list with explanations]

### Major fixes:
1. [Issue name]: [What was wrong] → [What you changed] — [Why this approach]
   - File: [path/to/file.ts]
   - Change: [brief description of code change]
2. ...

### Minor fixes:
1. [Issue name]: [Brief explanation of fix]
2. ...

## Code Changes Summary
- [File X]: [What changed and why]
- [File Y]: [What changed and why]
- Added/removed [what] because [why]

## Trade-offs / Decisions
- [Any architectural decisions or trade-offs made]

Please re-review. Verify the actual code changes, not just this summary.
```

**Use raw JSON for multi-line messages**:
```bash
rp-cli -w W -e 'call chat_send {"message": "<RE_REVIEW_MESSAGE>", "mode": "chat"}'
```

⚠️ **JSON escaping**: Use `\n` for newlines, `\"` for quotes inside the message string.

⚠️ **CRITICAL**: The reviewer sees updated file contents automatically, but may over-trust your fix summary. Ensure fixes are actually committed so the reviewer can verify the actual code, not just your description.

5. **Repeat**: Continue until review passes (Ship)

**Why skip builder on re-reviews?** The chat already has full context from the initial review. Builder's job was discovery—that's done. Re-reviews verify fixes, not discover new context.

**Why detailed re-review messages?** The reviewer needs to understand:
- What concrete code changes were made
- Why you chose that approach (patterns, trade-offs)
- How the implementation evolved (not just "trust me, I fixed it")

**When to skip a fix** (rare—default is to fix):
- Reviewer lacked context (didn't see related code, missed a constraint)
- Reviewer misunderstood the requirement or intent
- Suggested fix would break something else
- Conflicts with established codebase patterns or requirements

If skipping, explain WHY clearly in the re-review message so the reviewer can reconsider with full context.

**Anti-pattern**: Skipping Minor issues. "Minor" means "real issue, lower priority"—not "optional". Fix them.

---

## Key Guidelines

**Always use -w flag:** Every rp-cli command (except `windows`) needs `-w <id>` to target the correct window. W = your window ID from Phase 0.

**Token budget:** Stay under ~160k tokens. Builder manages this, but verify with `select get`.

**Chat sees only selection:** Ensure all changed files, related code, and supporting docs are selected before starting the review chat.

**Include the diff:** The chat sees current file state, not the diff. Reference specific changes in your prompts.

---

## Anti-patterns to Avoid

- **Stuffing builder prompt** – don't list changed files; give intent, let builder discover context
- **Ignoring builder's handoff prompt** – it's the foundation; add criteria on top, don't replace
- **Forgetting `-w <id>` flag** – commands will fail with "Multiple windows" error
- Skipping `builder` – you'll miss how changes interact with existing code
- Reviewing without plan/beads context – you won't know what was intended
- Shallow review – thorough analysis takes time; don't rush
- Missing changed files in selection – chat can't see what's not selected
- Ignoring test changes – tests are code too
- Documenting issues instead of fixing – after review feedback, edit the code directly
- **Skipping Minor issues** – "Minor" ≠ "optional"; fix all Critical/Major/Minor before re-review
