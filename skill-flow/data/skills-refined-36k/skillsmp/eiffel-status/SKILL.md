---
name: eiffel-status
description: Shows current Eiffel Spec Kit phase, evidence files, and workflow status. Use with /eiffel.status command to see where you are in the process.
allowed-tools: Read, Grep, Glob, Bash
---

# /eiffel.status - Workflow Status

**Purpose:** Show current phase and evidence trail. Answer "where are we?"

## Usage

```
/eiffel.status <project-path>
```

**Example:**
```
/eiffel.status d:\prod\simple_cache
```

If no path provided, ask: "Which project? Provide the full path."

## Workflow

### Step 1: Verify Project Exists

```bash
test -d <project-path>/.eiffel-workflow && echo "Workflow initialized" || echo "No workflow - run /eiffel.intent first"
```

### Step 2: Check Evidence Files

| Evidence File | Phase |
|---------------|-------|
| evidence/phase0-intent.txt | Phase 0: Intent |
| evidence/phase1-compile.txt | Phase 1: Contracts |
| evidence/phase2-chain.txt | Phase 2: Review |
| evidence/phase3-tasks.txt | Phase 3: Tasks |
| evidence/phase4-compile.txt | Phase 4: Implement |
| evidence/phase5-tests.txt | Phase 5: Verify |
| evidence/phase6-tests.txt | Phase 6: Harden |
| evidence/phase7-ship.txt | Phase 7: Ship |

### Step 3: Display Status

```
╔══════════════════════════════════════════════════════════════╗
║           EIFFEL SPEC KIT STATUS                             ║
║           Project: <project-path>                            ║
╠══════════════════════════════════════════════════════════════╣
║ Phase 0: Intent      [✓] intent-v2.md approved               ║
║ Phase 1: Contracts   [✓] Compiled                            ║
║ Phase 2: Review      [✓] Synopsis approved                   ║
║ Phase 3: Tasks       [✓] 5 tasks defined                     ║
║ Phase 4: Implement   [→] IN PROGRESS                         ║
║ Phase 5: Verify      [ ] Pending                             ║
║ Phase 6: Harden      [ ] Pending                             ║
║ Phase 7: Ship        [ ] Pending                             ║
╠══════════════════════════════════════════════════════════════╣
║ Current: Phase 4 - Implementation                            ║
║ Next: Complete implementation, then /eiffel.verify           ║
╚══════════════════════════════════════════════════════════════╝
```

### Step 4: Drift Detection

Check for signs of drift:
- Contracts modified since Phase 2?
- Tasks.md out of sync?
- Evidence files missing?
- Skills modified during workflow?

```
DRIFT WARNINGS:
- [!] Contracts changed since review (re-run /eiffel.review)
- [!] phase4-compile.txt missing (compile not verified)
- [!] Skill files modified since workflow start (queue changes for after ship)
```

### Step 4b: Skill Version Lock Check

**Why:** Modifying skills mid-workflow causes drift. Discovered improvements should be queued for after ship.

Check skill modification times vs workflow start:
```bash
# Get workflow start time (phase0 evidence)
WORKFLOW_START=$(stat -c %Y <project-path>/.eiffel-workflow/evidence/phase0-intent.txt 2>/dev/null)

# Check if any eiffel-* skills were modified after workflow started
find ~/.claude/skills/eiffel-* -name "SKILL.md" -newer <project-path>/.eiffel-workflow/evidence/phase0-intent.txt
```

**If skills were modified during workflow:**
```
SKILL DRIFT WARNING:
- Skills modified during workflow execution
- Changes made: [list files]
- Recommendation: Complete current workflow, then formalize skill improvements
```

**Best Practice:** Create `<project-path>/.eiffel-workflow/skill-improvements.md` to queue discovered improvements:
```markdown
# Skill Improvements Discovered During This Workflow

## To Apply After Ship
1. [Improvement description]
2. [Improvement description]

## Applied During Workflow (drift)
1. [What was changed and why]
```

### Step 5: Suggest Next Action

Based on current state, suggest the next command:

```
Suggested next command:
  /eiffel.implement <project-path>   (continue implementation)

Or if implementation done:
  /eiffel.verify <project-path>      (run tests)
```

## Context Management (RLM Pattern)

This skill focuses ONLY on: `<project-path>`

**DO NOT:**
- Read files outside this project directory
- Load entire ecosystem into context to check status
- Keep large file contents in working memory

**DO:**
- Only read `.eiffel-workflow/` directory and evidence files
- Use Task tool with Explore agent if you need ecosystem-wide status

**Example - Ecosystem Query:**
```
Need to check if dependencies have workflow issues? Don't read all projects.
Instead: Task(subagent_type=Explore) → "Does simple_mml have a .eiffel-workflow directory?"
```

The sub-agent searches and returns ONLY what you need. Your context stays focused on this project.

## Output

Always show:
1. Phase checklist with status
2. Current phase
3. Drift warnings (if any)
4. Suggested next command
