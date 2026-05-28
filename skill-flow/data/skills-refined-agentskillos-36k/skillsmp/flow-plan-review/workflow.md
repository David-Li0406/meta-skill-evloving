# Plan Review Workflow

## Philosophy: Context Over Convenience

The reviewer model only sees selected files—it's blind to the rest of the codebase. RepoPrompt's Context Builder (hereafter "Builder") is AI-powered—its strength is **discovering related context** the reviewer needs:
- Existing patterns the plan should follow
- Similar implementations for consistency
- Architectural context (how things connect)
- Dependencies and side effects

We already KNOW the plan file. Builder's job is finding the **surrounding context** that makes review meaningful.

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
rp-cli -w W -e 'builder "..." && select add plan.md && select get'
```

---

## Phase 1: Parse Arguments & Read the Plan

**Resolve input first:**
1. If file path exists → markdown plan
2. Else if matches Beads ID format or `bd show <arg>` succeeds → Beads issue
3. Else if `bd search "<arg>"` has unique match → use that issue
4. Else: ask user for clarification

Additional text in arguments = focus areas/context. Save these for Phase 3.

**If Beads issue:**
1. Fetch content: `bd show <id>` (text output is clean, includes children)
2. Save output for inclusion in chat prompt
3. Compose a concise summary of what the plan accomplishes (1-2 sentences for simple plans, more for complex epics)

**If markdown plan:**

Read the plan file (replace W with your window ID from Phase 0):
```bash
rp-cli -w W -e 'read <plan-file-from-args>'
```

Compose a **concise but descriptive summary** of what the plan accomplishes (for builder prompt). Simple plans: 1-2 sentences. Complex epics: brief paragraph capturing key scope.

Then search for supporting documentation:
```bash
# Find PRD if exists
rp-cli -w W -e 'search "PRD" --mode path'
rp-cli -w W -e 'search "prd_" --mode path'

# Find beads JSONL
rp-cli -w W -e 'search ".beads/" --mode path'

# Find architecture docs
rp-cli -w W -e 'search "architecture" --mode path'
rp-cli -w W -e 'search "docs/" --mode path'
```

Read any relevant supporting docs you find.

---

## Phase 2: Context Discovery & Selection

### Step 1: Run builder with intent (not details)

Give builder a simple, intent-focused prompt. Let it discover context autonomously:
```bash
rp-cli -w W -e 'builder "Review a plan to [CONCISE SUMMARY OF WHAT PLAN ACCOMPLISHES]"'
```

**Examples:**
- Simple: `"Review a plan to add OAuth authentication to the API"`
- Medium: `"Review a plan to refactor the payment processing module to use the repository pattern and add retry logic"`
- Complex: `"Review a plan to rebuild the notification system with real-time WebSocket delivery, user preferences, batching, and multi-channel support (email, push, in-app)"`

⚠️ **DO NOT** stuff the prompt with file lists, module names, or implementation details. Builder discovers those.

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

# Always add the plan file (builder may not have selected it)
rp-cli -w W -e 'select add <plan-file>'

# Add supporting docs from Phase 1 (PRD, architecture, etc.)
rp-cli -w W -e 'select add <path-to-prd>'
rp-cli -w W -e 'select add <path-to-architecture-doc>'

# Add any files you know are critical that builder missed
```

### Step 4: Verify final selection

```bash
rp-cli -w W -e 'select get'
```

Confirm selection includes:
- The plan file
- Supporting docs from Phase 1
- Related patterns/code builder discovered
- Anything else needed for thorough review

**Why this matters:** Chat only sees selected files. Missing context = incomplete review.

---

## Phase 3: Carmack-Level Review

### Step 1: Build the review prompt

Combine three pieces:
1. **Builder's handoff prompt** (from Phase 2 Step 2) - factual context foundation
2. **Review criteria** - Carmack-level checklist
3. **User's focus areas** (from arguments) - specific concerns to prioritize

**Prompt structure:**
```
[BUILDER'S HANDOFF PROMPT - paste as-is]

---

## Plan Under Review
[PASTE PLAN CONTENT - or for Beads, include `bd show` output]

## Review Focus
[USER'S FOCUS AREAS FROM ARGUMENTS, if any]

## Review Criteria

Conduct a John Carmack-level review. Evaluate against:

### 1. Simplicity & Minimalism
- Simplest possible solution?
- Unnecessary abstraction layers?
- YAGNI violations?

### 2. DRY & Code Reuse
- Duplicated logic?
- Reinventing existing utilities?
- Could leverage existing patterns?

### 3. Idiomatic Code
- Follows codebase patterns?
- Naming conventions consistent?

### 4. Architecture & Design
- Data flow makes sense?
- Clear boundaries/responsibilities?
- Circular dependencies?

### 5. Edge Cases & Error Handling
- Unhandled failure modes?
- Race conditions?

### 6. Testability
- Structure easily testable?
- Dependencies injectable?

### 7. Performance
- O(n²) or worse?
- Unnecessary allocations?

### 8. Security
- Injection vulnerabilities?
- Auth/authz gaps?

### 9. Maintainability
- Future devs will understand?
- Abstractions earning complexity?

## Output Format

For each issue:
1. **Severity**: Critical / Major / Minor / Nitpick
2. **Location**: Where in the plan
3. **Problem**: What's wrong
4. **Suggestion**: How to fix
5. **Rationale**: Why it matters

End with:
- Overall: Ship / Needs Work / Major Rethink
- Patterns from codebase the plan should adopt

**List ALL issues.** Agent fixes all Critical/Major/Minor before re-review.
```

### Step 2: Execute review

Use chat in **chat mode**. The chat sees all selected files.

**Initial review** - MUST use raw `call chat_send` with `"new_chat": true`:
```bash
rp-cli -w W -e 'call chat_send {"message": "<COMBINED_PROMPT>", "mode": "chat", "new_chat": true, "chat_name": "Plan Review: [PLAN_NAME]"}'
```

⚠️ **JSON escaping**: Message must use `\n` for newlines, not literal line breaks.

⚠️ **WAIT FOR RESPONSE**: Chat takes 1-5+ minutes. Do NOT re-send or follow up until it returns.

**Follow-up/re-review command** - MUST use `call chat_send` with `selected_paths` to ensure files remain visible:
```bash
rp-cli -w W -e 'call chat_send {"message": "<FOLLOW_UP_MESSAGE>", "mode": "chat", "selected_paths": ["<FILE1>", "<FILE2>"]}'
```

⚠️ **CRITICAL**: Chat follow-ups do NOT automatically see the selection. You MUST pass `selected_paths` with the same files from your initial selection, or the reviewer loses file context.

---

## Phase 3 Alternative: Export for External Review

If user chose **export mode**, skip the chat and export context instead.

### Step 1: Set the review prompt

Build the combined prompt (same structure as Phase 3 Step 1), then set it:
```bash
rp-cli -w W -e 'prompt set "<COMBINED_PROMPT>"'
```

The prompt should include:
- Builder's handoff prompt (foundation)
- Plan content (or Beads issue summary)
- User's focus areas
- Review criteria checklist

### Step 2: Export to file

```bash
rp-cli -w W -e 'prompt export ~/Desktop/plan-review-[PLAN_NAME].md'
```

This exports: file tree, codemaps, selected file contents, and the review prompt.

### Step 3: Open for user

```bash
open ~/Desktop/plan-review-[PLAN_NAME].md
```

### Step 4: Inform user

Tell the user:
```
Exported review context to ~/Desktop/plan-review-[PLAN_NAME].md

The file contains:
- Full file tree with selected files marked
- Code maps (signatures/structure)
- Complete file contents (plan + supporting docs)
- Review prompt with Carmack-level criteria

Paste into ChatGPT Pro, Claude web, or your preferred LLM.
After receiving feedback, return here to implement fixes.
```

**Skip the Iteration and Fix loops** — user handles those externally.

---

## Iteration

Continue the chat to drill deeper if needed (remember to include `selected_paths`):
```bash
rp-cli -w W -e 'call chat_send {"message": "Elaborate on the [SPECIFIC CONCERN]. What exactly would you change?", "mode": "chat", "selected_paths": ["<FILE1>", "<FILE2>"]}'
```

---

## Fix and Re-Review Loop

**CRITICAL**: After receiving review feedback, **implement all fixes directly**—edit the plan file or Beads issue, don't just document issues.

### What MUST be fixed:
- **Critical**: Fix immediately, no exceptions
- **Major**: Fix immediately, no exceptions
- **Minor**: Fix immediately—these are real issues, not optional polish

### What MAY be skipped:
- **Nitpick**: Optional style/preference items—fix if easy, skip if not

### The Loop

1. **Parse the review**: Extract all issues by severity
2. **Fix Critical → Major → Minor**: Edit the plan to address each
   - For markdown plans: use Edit tool to update the file
   - For Beads issues: use `bd update <id> --body "..."`
3. **Augment selection** (if needed): Add any files touched during fixes that aren't already selected
   ```bash
   rp-cli -w W -e 'select add path/to/newly-relevant-file.ts'
   ```
4. **Re-review**: Continue the existing chat with detailed fix explanations

**Re-review message template:**
```
## Fixes Applied

### Critical fixes:
[If any - list with explanations]

### Major fixes:
1. [Issue name]: [What was wrong] → [What you changed] — [Why this approach]
2. ...

### Minor fixes:
1. [Issue name]: [Brief explanation of fix]
2. ...

## Plan Changes Summary
- [Section X] rewritten to [describe change]
- Added [new section/content] for [reason]
- Removed/simplified [what] because [why]

## Trade-offs Acknowledged
- [Any trade-offs or compromises made]

Please re-review.
```

**Use raw JSON for multi-line messages** - include `selected_paths` to maintain file context:
```bash
rp-cli -w W -e 'call chat_send {"message": "<RE_REVIEW_MESSAGE>", "mode": "chat", "selected_paths": ["<FILE1>", "<FILE2>"]}'
```

⚠️ **JSON escaping**: Use `\n` for newlines, `\"` for quotes inside the message string.

⚠️ **CRITICAL**: Always include `selected_paths` with the files from your initial selection. Without this, the reviewer cannot see file contents in follow-up messages.

5. **Repeat**: Continue until review passes (Ship)

**Why skip builder on re-reviews?** The chat already has full context from the initial review. Builder's job was discovery—that's done. Re-reviews verify fixes, not discover new context.

**Why detailed re-review messages?** The reviewer needs to understand:
- What concrete changes were made to the plan
- Why you chose that approach (trade-offs, patterns)
- How the plan evolved (not just "trust me, I fixed it")

**When to skip a fix** (rare—default is to fix):
- Reviewer lacked context (didn't see related docs, missed a constraint)
- Reviewer misunderstood the requirement or intent
- Suggested change would conflict with other plan sections
- Conflicts with established patterns or requirements

If skipping, explain WHY clearly in the re-review message so the reviewer can reconsider with full context.

**Anti-pattern**: Skipping Minor issues. "Minor" means "real issue, lower priority"—not "optional". Fix them.

---

## Key Guidelines

**Always use -w flag:** Every rp-cli command (except `windows`) needs `-w <id>` to target the correct window. W = your window ID from Phase 0.

**Token budget:** Stay under ~160k tokens. Builder manages this, but verify with `select get`.

**Chat sees only selection:** Ensure the plan file, PRD, and relevant code are all selected before starting the review chat.

---

## Anti-patterns to Avoid

- **Stuffing builder prompt** – don't list files/modules/details; give intent, let builder discover
- **Ignoring builder's handoff prompt** – it's the foundation; add criteria on top, don't replace
- **Forgetting `-w <id>` flag** – commands will fail with "Multiple windows" error
- Skipping `builder` – you'll miss architectural context
- Reviewing without PRD/beads context – you won't know the "why"
- Shallow review – thorough analysis takes time; don't rush
- Not selecting supporting docs – chat can't see what's not selected
- Documenting issues instead of fixing – after review feedback, edit the plan directly
- **Skipping Minor issues** – "Minor" ≠ "optional"; fix all Critical/Major/Minor before re-review
