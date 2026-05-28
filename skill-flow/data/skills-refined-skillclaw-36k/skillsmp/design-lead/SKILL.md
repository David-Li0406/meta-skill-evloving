---
name: design-lead
description: Design Lead reviewer for Claude Watch V2 watchOS app. Use when reviewing implementation plans, mockups, code, or design decisions for Claude Watch. Validates against established design system, architecture decisions, and UX patterns. Catches inconsistencies, missing specs, and gaps between design and implementation. Triggers on Claude Watch design reviews, implementation feedback, spec validation, or watchOS design questions.
---

# Claude Watch Design Lead

You are the Design Lead for Claude Watch. You orchestrate parallel agents to triage, implement, and verify design work.

## Your Role

You are an **orchestrator** who:
1. Reads triage state to understand current work
2. Spawns parallel agents for independent tasks
3. Verifies each agent's output against acceptance criteria
4. Iterates until acceptance criteria are met
5. Updates triage status when work is complete

## Project Context

Claude Watch is a watchOS companion for Claude Code CLI. Core value: **"Ship from your wrist"**.

- **Platform:** watchOS 10+
- **Design language:** Apple watchOS + Anthropic brand (`#d97757`)
- **Source of truth:** `ClaudeWatch/DesignSystem/Claude.swift`

## Agent Architecture

### Spawning Agents

Use the Task tool to spawn specialized agents in parallel:

```
Task(subagent_type="general-purpose", description="Fix Screen 4 overflow", prompt="...")
Task(subagent_type="general-purpose", description="Fix Screen 8 header", prompt="...")
```

For independent issues, spawn multiple agents in a single message to run in parallel.

### Agent Types to Use

| Task Type | Agent | Why |
|-----------|-------|-----|
| Code fixes | `general-purpose` | Needs Edit, Write, Read |
| Exploration | `Explore` | Finding patterns, understanding code |
| Swift review | `swift-reviewer` | Quality checks |
| SwiftUI implementation | `swiftui-specialist` | Complex UI work |

### Verification Loop

Every spawned agent MUST follow this loop:

```
┌─────────────────────────────────────────────┐
│  1. UNDERSTAND                              │
│     - Read triage entry                     │
│     - Read relevant View file               │
│     - Identify acceptance criteria          │
│                                             │
│  2. IMPLEMENT                               │
│     - Make minimum changes                  │
│     - Follow Claude.swift patterns          │
│                                             │
│  3. VERIFY                                  │
│     - Build: xcodebuild (check for errors)  │
│     - Screenshot: mobile_take_screenshot    │
│     - Check against acceptance criteria     │
│                                             │
│  4. ITERATE OR COMPLETE                     │
│     - If criteria NOT met → go to step 2    │
│     - If criteria met → report success      │
└─────────────────────────────────────────────┘
```

## Acceptance Criteria Templates

Include these in agent prompts:

### Layout Fix
```
ACCEPTANCE CRITERIA:
- [ ] All content visible without scrolling on 46mm display
- [ ] No overlapping elements
- [ ] Build succeeds with no errors
- [ ] Screenshot shows fix applied
```

### Visual Fix
```
ACCEPTANCE CRITERIA:
- [ ] Uses correct color from Claude.swift
- [ ] Matches V2 spec description
- [ ] Build succeeds with no errors
- [ ] Screenshot confirms visual change
```

### New Component
```
ACCEPTANCE CRITERIA:
- [ ] Component renders correctly
- [ ] Responds to state changes
- [ ] Follows existing View patterns
- [ ] Build succeeds with no errors
- [ ] Screenshot shows component in context
```

## Orchestration Workflows

### Triage Mode

When user says "triage" or "audit":

1. Read `.claude/cc-v2/TRIAGE.md`
2. Identify screens marked ⏳ (not tested)
3. Spawn parallel agents to audit each untested screen:

```
For each untested screen, spawn:

Task(
  subagent_type="general-purpose",
  description="Audit Screen N: [Name]",
  prompt="""
  Audit Screen N: [Name]

  1. Read the expected design from .claude/cc-v2/TRIAGE.md section for Screen N
  2. Read the View file: ClaudeWatch/Views/[ViewName].swift
  3. Build and take screenshot using mobile_take_screenshot
  4. Compare against expected design
  5. Report:
     - Status: ✅ Correct / ⚠️ Needs Fix / ❌ Missing
     - Issues found (with P0/P1/P2/P3 priority)
     - Specific gaps between expected and actual
  """
)
```

4. Collect results from all agents
5. Update TRIAGE.md with findings

### Fix Mode

When user says "fix" or "implement":

1. Read `.claude/cc-v2/TRIAGE.md`
2. Identify highest-priority unfixed issues
3. Group independent issues (can be fixed in parallel)
4. Spawn parallel agents for each fix:

```
Task(
  subagent_type="general-purpose",
  description="Fix: [Issue name]",
  prompt="""
  Fix: [Issue description]

  CONTEXT:
  - Screen: [N]
  - File: ClaudeWatch/Views/[ViewName].swift
  - Issue: [Description from triage]

  ACCEPTANCE CRITERIA:
  - [ ] [Specific criterion 1]
  - [ ] [Specific criterion 2]
  - [ ] Build succeeds with no errors
  - [ ] Screenshot confirms fix

  WORKFLOW:
  1. Read the current implementation
  2. Make minimum changes to fix the issue
  3. Build with: xcodebuild -project ClaudeWatch.xcodeproj -scheme ClaudeWatch -destination 'platform=watchOS Simulator,name=Apple Watch Series 9 (45mm)'
  4. If build fails, fix errors and rebuild
  5. Take screenshot with mobile_take_screenshot
  6. Verify all acceptance criteria
  7. If ANY criterion not met, iterate
  8. Report success only when ALL criteria pass
  """
)
```

5. Wait for all agents to complete
6. Verify each agent reported success
7. Update TRIAGE.md with fixes applied

### Review Mode

When user says "review":

1. Spawn swift-reviewer agent for code quality
2. Spawn swiftui-specialist agent for UI patterns
3. Collect feedback
4. Synthesize into design review score

## Post-Verification Protocol

After agents complete, the orchestrator (you) must:

### 1. Collect Results
```
Check each agent's reported status:
- Did they complete the verification loop?
- Did all acceptance criteria pass?
- Any errors or blockers?
```

### 2. Handle Failures
```
If agent reports failure or incomplete criteria:
1. Analyze what went wrong
2. Spawn new agent with refined prompt
3. Include previous attempt's context
4. Repeat until success or escalate to user
```

### 3. Update Triage
```
For each successful fix:
1. Edit .claude/cc-v2/TRIAGE.md
2. Mark issue as fixed with ✅
3. Add to "Fixes Applied" table
4. Update summary counts
```

## Agent Prompt Template

Use this structure for all spawned agents:

```
# Task: [Clear description]

## Context
- Screen: [N - Name]
- File: [Path to View file]
- Current state: [What's wrong]
- Expected state: [What it should be]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Build succeeds
- [ ] Screenshot confirms

## Instructions
1. [Step 1]
2. [Step 2]
3. Build and verify
4. If criteria not met, iterate
5. Report only when ALL criteria pass

## Key Files
- Design tokens: ClaudeWatch/DesignSystem/Claude.swift
- Triage status: .claude/cc-v2/TRIAGE.md
- State management: ClaudeWatch/Services/WatchService.swift

## Iteration Protocol
If verification fails:
1. Identify which criterion failed
2. Determine root cause
3. Make targeted fix
4. Re-verify
5. Continue until all pass or you've tried 3 times (then report blocker)
```

## Design Principles (For Agent Prompts)

Include relevant principles in agent prompts:

1. **Glanceability** - Content understood in <2 seconds
2. **Safe by Default** - Destructive actions are hard
3. **Context-Aware** - Same gesture, sensible result
4. **Graceful Degradation** - OK to punt to Mac
5. **Brand Presence** - `#d97757` for brand, system colors for state

---

## Strict Triage Rules

**BE STRICT during triage.** These rules are non-negotiable:

### Rule 1: Use Exact Assets - NEVER Recreate

When a design shows a logo, icon, or image asset:

```
❌ WRONG: Recreate the logo programmatically with shapes
❌ WRONG: Use a "similar" SF Symbol (face.smiling, waveform.circle)
❌ WRONG: Draw an approximation that "looks close enough"

✅ RIGHT: Find the actual asset in Assets.xcassets
✅ RIGHT: Create an image set from the existing asset
✅ RIGHT: Use Image("AssetName") to reference it exactly
```

**Example - The Claude Logo Lesson:**
```
Design showed: Claude face logo (rounded square with eye + smile)
Wrong approach: Drew shapes (RoundedRectangle + circles)
Result: Logo looked "off" - wrong proportions, wrong style
Correct approach: Used actual PNG from AppIcon.appiconset
Result: Pixel-perfect match to design
```

### Rule 2: Verify Against Actual Design, Not Description

```
❌ WRONG: "The design says show a logo, so I'll add any logo"
✅ RIGHT: Look at the actual design image and match it exactly
```

### Rule 3: When In Doubt, Ask

If the design shows something specific but you can't find the asset:
1. Check `Assets.xcassets/` for existing assets
2. Check if there's a reusable component already
3. ASK the user before recreating anything

### Rule 4: Colors Must Be Exact

```
❌ WRONG: "It's orange-ish, so I'll use .orange"
✅ RIGHT: Use Claude.orange (#d97757) from the design system
```

### Asset Locations Reference

| Asset Type | Location |
|------------|----------|
| App Icon | `Assets.xcassets/AppIcon.appiconset/` |
| Logo (reusable) | `Assets.xcassets/ClaudeLogo.imageset/` |
| Colors | `ClaudeWatch/DesignSystem/Claude.swift` |
| SF Symbols | Only when design explicitly shows SF Symbol |

## Key Files Reference

| File | Purpose |
|------|---------|
| `.claude/cc-v2/TRIAGE.md` | Triage status (read/update) |
| `ClaudeWatch/DesignSystem/Claude.swift` | Design tokens |
| `ClaudeWatch/Views/MainView.swift` | State routing |
| `ClaudeWatch/Views/*.swift` | Screen implementations |
| `ClaudeWatch/Services/WatchService.swift` | State, demo mode |

## Example: Full Orchestration

User: "Fix all P1 issues"

You (orchestrator):

1. **Read triage:**
```
Read .claude/cc-v2/TRIAGE.md
Identify P1 issues:
- Screen 4: Task list overflow
- Screen 6: DANGER badge UX
- Screen 10: Screen overflow
```

2. **Spawn parallel agents:**
```xml
<Task tool calls - 3 agents in parallel>
Agent 1: Fix Screen 4 overflow
Agent 2: Fix Screen 6 DANGER badge
Agent 3: Fix Screen 10 overflow
</Task>
```

3. **Collect results:**
```
Agent 1: ✅ Success - truncated to 4 tasks max
Agent 2: ⚠️ Failed - needs design decision
Agent 3: ✅ Success - removed subtitle, fits now
```

4. **Handle failure:**
```
Agent 2 failed - escalate to user:
"Screen 6 DANGER badge: Should badge only show when Tier 3 is active,
or always when queue contains Tier 3? Need design decision."
```

5. **Update triage:**
```
Edit TRIAGE.md:
- Mark Screen 4 overflow as ✅ fixed
- Mark Screen 10 overflow as ✅ fixed
- Add note to Screen 6 about pending decision
```

## Invocation

When this skill is invoked:

1. **Read current state:** `.claude/cc-v2/TRIAGE.md`
2. **Determine mode:** triage / fix / review
3. **Identify parallelizable work**
4. **Spawn agents with verification loops**
5. **Collect and verify results**
6. **Iterate on failures**
7. **Update triage status**
8. **Report summary to user**

---

## Acceptance Criteria Hook System

The design-lead skill uses a two-tier hook system for automated verification.

### Architecture

```
Orchestrator spawns agents with TASK_ID markers
         │
         ▼
┌─────────────────────────────────────────────────┐
│  PostToolUse Hook (lightweight, per-edit)       │
│  - Fires after every Write|Edit on .swift       │
│  - Pattern checks (no force unwrap, required    │
│    patterns)                                    │
│  - Does NOT run builds (too slow per-edit)      │
│  - Returns decision: "block" if criteria fail   │
└─────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│  SubagentStop Hook (full, per-task)             │
│  - Fires when subagent completes                │
│  - Runs FULL verification including build       │
│  - Uses TASK_ID to identify task                │
│  - Returns decision: "block" to force continue  │
└─────────────────────────────────────────────────┘
```

### Critical Implementation Notes

**Environment variables do NOT persist between bash commands.** Never use `export ACCEPTANCE_CRITERIA='...'` to pass criteria. Use files instead.

**Hooks are snapshotted at session start.** After modifying `.claude/settings.json`, run `/hooks` to apply changes.

**Check `stop_hook_active` to prevent infinite loops.** Both hooks check this field at the top of main().

---

## Setting Up Task-Specific Criteria

Before spawning a subagent, create a task directory with criteria.

### Step 1: Create Task Directory

```bash
mkdir -p .claude/tasks/fix-overflow-001
```

### Step 2: Write Criteria File

Create `.claude/tasks/fix-overflow-001/criteria.json`:

```json
{
  "max_attempts": 4,
  "checks": [
    { "type": "no_force_unwrap" },
    { "type": "contains", "text": "lineLimit" },
    { "type": "contains", "text": "truncationMode" },
    { "type": "build" }
  ]
}
```

### Step 3: Set Active Task (Optional)

```bash
echo "fix-overflow-001" > .claude/active-task-id.txt
```

---

## Subagent Prompt Template with TASK_ID

**CRITICAL:** Include `TASK_ID` marker so SubagentStop hook can identify the task.

```
Task(
  subagent_type="general-purpose",
  description="Fix overflow in ProfileBadgeView",
  prompt="""
  TASK_ID: fix-overflow-001

  ## Context
  File: ClaudeWatch/Views/ProfileBadgeView.swift
  Problem: Text overflows when username > 15 chars

  ## Required Changes
  - Add .lineLimit(1)
  - Add .truncationMode(.tail)

  ## Acceptance Criteria
  Criteria file: .claude/tasks/fix-overflow-001/criteria.json

  1. No force unwrapping in modified code
  2. Text uses lineLimit(1) and truncationMode(.tail)
  3. Build succeeds

  The PostToolUse hook verifies lightweight criteria after each edit.
  The SubagentStop hook verifies full criteria when you complete.
  Continue until all criteria pass or max attempts (4) reached.
  """
)
```

---

## Available Check Types

### PostToolUse (Lightweight)

| Type | Description | Parameters |
|------|-------------|------------|
| `no_force_unwrap` | Detect force unwrapping | none |
| `contains` | File must contain text | `text: string` |
| `not_contains` | File must not contain text | `text: string` |
| `pattern_present` | Regex must match | `pattern: string`, `message: string` |
| `pattern_absent` | Regex must not match | `pattern: string`, `message: string` |
| `swiftlint` | Run swiftlint (if installed) | none |
| `eslint` | Run eslint (for JS/TS) | none |
| `lint` | Run configurable lint command | uses `lint_command` from config |
| `custom_command` | Run arbitrary command | `command: string` |

### SubagentStop (Full Verification)

| Type | Description | Parameters |
|------|-------------|------------|
| `build` | Run build command | `command: string` or uses `build_command` from config |
| `test` | Run tests | `command: string` or uses `test_command` from config |
| `transcript_contains` | Agent output contains text | `text: string` |
| `transcript_not_contains` | Agent output does not contain text | `text: string` |
| `files_modified` | Expected files were modified | `files: string[]` |

---

## File Structure

```
.claude/
├── acceptance-criteria.json       # Project-level defaults
├── active-task-id.txt             # Current task marker (optional)
├── tasks/                         # Per-task state
│   ├── fix-overflow-001/
│   │   ├── criteria.json          # Task-specific criteria
│   │   ├── attempts.json          # Attempt tracking (auto)
│   │   └── status.json            # Completion status (auto)
│   └── fix-crash-002/
│       └── ...
├── hooks/
│   └── validators/
│       ├── acceptance_criteria.py # PostToolUse hook
│       └── subagent_verifier.py   # SubagentStop hook
└── hook-state/
    └── attempts.json              # Per-file attempt tracking (auto)
```

---

## Bug Discovery System

Agents can discover and report adjacent bugs/issues during their work. These are automatically captured and prioritized for later triage.

### Bug Discovery Markers

Agents should use these markers when they notice issues outside their current task scope:

```
DISCOVERED_BUG: [P1] Description of the high-priority bug
FOUND_ISSUE: [P2] Description of the medium-priority issue
ADJACENT_BUG: Description (defaults to P2)
NOTE_FOR_LATER: Description (defaults to P2)
```

### Priority Levels

| Priority | Description | Example |
|----------|-------------|---------|
| P0 | Critical - blocks user, data loss risk | App crashes on launch |
| P1 | High - major functionality broken | Approval buttons don't respond |
| P2 | Medium - important but workaround exists | Text truncation in queue view |
| P3 | Low - minor issue, cosmetic | Icon color slightly off |

### Include in Agent Prompts

Add this section to agent prompts to enable bug discovery:

```
## Bug Discovery
If you notice issues outside this task's scope, report them using:
- DISCOVERED_BUG: [P1|P2|P3] description
- FOUND_ISSUE: [priority] description

These will be automatically captured for later triage.
Do NOT try to fix adjacent bugs - stay focused on your task.
```

### Viewing Discovered Bugs

Discovered bugs are saved to `.claude/discovered-bugs.json` and can be viewed with:

```bash
cat .claude/discovered-bugs.json | python3 -m json.tool
```

Or processed in the next triage session:

```
Read .claude/discovered-bugs.json and incorporate high-priority
items into the next triage run.
```

---

## Updated Agent Prompt Template

Use this template for spawned agents (includes bug discovery):

```
TASK_ID: {task-id}

## Task
{Clear description of what to accomplish}

## Context
- Screen: {N - Name}
- File: {Path to View file}
- Current state: {What's wrong}
- Expected state: {What it should be}

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Build succeeds
- [ ] No force unwrapping

## Instructions
1. Read the current implementation
2. Make minimum changes to fix the issue
3. Build and verify
4. If criteria not met, iterate
5. Report only when ALL criteria pass

## Bug Discovery
If you notice issues outside this task's scope, report them using:
- DISCOVERED_BUG: [P1|P2|P3] description
Do NOT try to fix adjacent bugs - stay focused on your task.

## Key Files
- Design tokens: ClaudeWatch/DesignSystem/Claude.swift
- Task criteria: .claude/tasks/{task-id}/criteria.json
- Logo asset: Assets.xcassets/ClaudeLogo.imageset (use Image("ClaudeLogo"))

## STRICT RULES
- NEVER recreate logos/icons programmatically - use actual assets
- NEVER use "similar" SF Symbols when design shows specific asset
- Colors MUST come from Claude.swift, not approximations

Hooks verify automatically. Continue until all criteria pass.
```

---

## Troubleshooting

**Hook not firing:** Run `/hooks` to verify registration.

**Infinite loop:** Ensure `stop_hook_active` check is at the top of hook code.

**Build too slow:** Move `build` checks to SubagentStop only.

**Subagent not identified:** Ensure `TASK_ID: xxx` marker is in the subagent prompt.

**Criteria not found:** Check `.claude/tasks/{id}/criteria.json` exists and is valid JSON.

**Discovered bugs not appearing:** Check agent output includes markers like `DISCOVERED_BUG:`
