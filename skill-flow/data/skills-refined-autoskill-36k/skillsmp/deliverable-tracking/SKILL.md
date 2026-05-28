---
name: deliverable-tracking
description: "Create GitHub Issues for client deliverables in DaveX2001/deliverable-tracking repo (discovery: rubber-duck). Evaluate at requirements-clarity when user mentions tracking, deliverables, commitments, or 'create deliverable'. Extracts What/Why/Done from conversation context, prompts for missing info via AskUserQuestion, applies dynamic client labels."
---

# Deliverable Tracking

Create structured GitHub Issues for client deliverables after clarity phases establish shared understanding.

## Workflow

### Step 1: Extract from Conversation Context

Review the conversation above to extract:
- **What?** - The deliverable description (from Requirements-Clarity)
- **Why?** - Motivation/importance (from Requirements-Clarity)
- **Definition of Done** - Success criteria (from Evaluation-Clarity)
- **Notes** - Any references, blockers, or context mentioned (optional)
- **Client** - Which client this deliverable is for

### Step 2: Prompt for Missing Info

Use AskUserQuestion to gather any fields not clearly extractable from context:

```
Required fields:
- Client name (for label and title prefix)
- Brief description (for title)
- What (if not clear from conversation)
- Why (if not clear from conversation)
- Definition of Done (if not clear from conversation)

Optional:
- Notes (references, blockers, context)
- Human Witness Hints (anything the tester should watch out for during Human Witness)
```

Format questions with 2-4 concrete options when possible. For free-form input, let user select "Other".

### Step 3: Create GitHub Issue

**Title format:** `{Client}: {Brief description}`

**Body format (minimal - details live in tracking file):**
```markdown
## What?
[Deliverable description]

## Why?
[Motivation/importance]

## Tracking
📋 [DoD + AC](https://github.com/{owner}/{repo}/blob/main/.claude/tracking/issue-{N}/tracking.md)

## Human Witness Hints
[Optional: things the tester should watch out for during Human Witness - "pay attention to X", "test this in context Y"]

## Notes
[Optional: references, blockers, context]

🤖
```

**Note:** The Tracking link is a placeholder. It will be updated after the tracking file is created and pushed in Step 5.5.

### Step 4: Route to Repository

```
IF client == "CLAUDE-CODE-IMPROVEMENTS":
    repo = "DaveX2001/claude-code-improvements"
ELSE:
    repo = "DaveX2001/deliverable-tracking"
```

### Step 5: Create Issue

Create the issue with `backlog` label + client label:
```bash
# Check plugin path first, then ~/.claude/lib
script="$([ -f "${CLAUDE_PLUGIN_ROOT}/lib/create_tracking_issue.sh" ] && echo "${CLAUDE_PLUGIN_ROOT}/lib/create_tracking_issue.sh" || echo ~/.claude/lib/create_tracking_issue.sh)"
"$script" --repo {repo} --title "{title}" --body "{formatted body}" --label "backlog,{client}"
```

**Label strategy:**
- `backlog` = initial triage status (all new issues start here)
- `{client}` = client label for filtering (e.g., WILSCH-AI-INTERNAL, IITR)

### Step 6: Legacy Issue Migration (if issue already exists)

**When creating tracking file for an EXISTING issue:**

1. **Move DoD from issue body → tracking file**
   - DoD lives ONLY in tracking file
   - REMOVE DoD section from issue body

2. **Update issue body to minimal format:**
```markdown
## What?
[Keep existing description]

## Why?
[Keep existing motivation]

## Tracking
📋 [DoD + AC](https://github.com/{owner}/{repo}/blob/main/.claude/tracking/issue-{N}/tracking.md)

## Human Witness Hints
[Optional: things the tester should watch out for]

## Notes
[Keep existing notes]
```

3. **Use `gh issue edit` to update body:**
```bash
gh issue edit {N} --repo {repo} --body "{minimal body WITHOUT DoD}"
```

**Why:** Single source of truth. DoD in issue body + tracking file = confusion.

### Step 6.5: AC Precondition Check

**Before creating tracking.md, use AI judgment to determine if AC content exists in the conversation.**

- **If AC exists** (Given-When-Then specs were defined via ac-create or rubber-duck): Proceed to Step 7 - create tracking.md with DoD + AC
- **If NO AC exists** (issue created for quick capture, design session not done yet): Do NOT create tracking.md. Instead:
  - Issue body contains placeholder: "📋 [DoD + AC](to be created via /rubber-duck)"
  - Skip to Step 8 (Confirm Creation)
  - Remind user: "Run /rubber-duck to define AC before implementation"

**Why this matters:** A tracking.md without AC content is a pointless placeholder. The file should only be created when there's actual AC to put in it.

### Step 7: Create Local Tracking File

**YOU MUST create the tracking file immediately after issue creation. No exceptions.**

After issue is created (or for legacy issues, after deciding to add tracking), extract the issue number and:

1. **Create tracking file:**
```bash
# Check plugin path first, then ~/.claude/lib
script="$([ -f "${CLAUDE_PLUGIN_ROOT}/lib/create_tracking_file.sh" ] && echo "${CLAUDE_PLUGIN_ROOT}/lib/create_tracking_file.sh" || echo ~/.claude/lib/create_tracking_file.sh)"
"$script" {N} "{title}"
```

2. **Add DoD items** to the file using Edit tool

**Pass Structure Preservation:** If ac-create produced DoD with pass headers (### Pass N: [description]), YOU MUST preserve this structure when writing to tracking.md. Do NOT flatten passes into a single list.

```markdown
## Definition of Done

### Pass 1: [description]
- [ ] item 1
- [ ] item 2

### Pass 2: [description]
- [ ] item 3
```

Same applies to AC section - preserve pass headers and AC numbering (AC1.1, AC2.1, etc.).

**Markdown Line Break Rule (REQUIRED for readability):**

Any element you want on its own line MUST have a blank line before it. Without blank lines, markdown renders consecutive lines as a single paragraph - unreadable for humans.

```markdown
**Line 1** content here

**Line 2** content here

**Line 3** content here
```

3. **Commit + push immediately:**
```bash
git add .claude/tracking/issue-{N}/
git commit -m "Create tracking file for #{N}"
git push
```

4. **Update issue body with GitHub URL:**
After push, update the Tracking link in the issue body to point to the pushed file:
```bash
gh issue edit {N} --repo {repo} --body "{updated body with correct GitHub URL}"
```

**Why this matters:** The tracking file must be pushed before linking. Local paths = version conflicts. Pushed = authoritative source.

### Step 8: Confirm Creation

Report:
- Issue URL
- Tracking file path (GitHub URL)
- Reminder: "Run /rubber-duck to define AC before implementation"

### Step 9: Save AC (post rubber-duck)

**Trigger:** After `/rubber-duck` session defines AC in conversation.

1. **Extract AC** from conversation (Given-When-Then format)

2. **Update tracking file:**
```bash
# Edit .claude/tracking/issue-{N}/tracking.md
# Replace AC placeholder with defined AC
```

3. **Commit + push:**
```bash
git add .claude/tracking/issue-{N}/
git commit -m "Add AC for #{N}"
git push
```

**Note:** This step is invoked separately after rubber-duck, not during initial issue creation.
