---
name: reflect
description: Analyze the current session and propose improvements to skills. Run after using a skill to capture learnings. Use when user says "reflect", "improve skill", "learn from this", or at end of skill-heavy sessions.
argument-hint: "[skill-name] | on | off | status | stats [skill] | validate | improve | reflect"
allowed-tools: Bash, Read, Write, Edit, TodoWrite, Task
model: sonnet
---

# Reflect Skill

Analyze sessions and propose evidence-based skill improvements through a validated workflow.

## Entry Point: Argument Routing

Based on `$ARGUMENTS`, route to the appropriate workflow:

**Analysis workflows:**
- `[skill-name]` or empty: [Main Reflection Workflow](#main-reflection-workflow)
- `validate [skill]`: Validate existing skill against 12-factor principles
- `improve`: Meta-improvement analysis of reflect itself
- `reflect`: Self-reflection on the reflect skill

**State management:**
- `on`: Enable auto-reflect → Run `${CLAUDE_PLUGIN_ROOT}/scripts/reflect.sh on`
- `off`: Disable auto-reflect → Run `${CLAUDE_PLUGIN_ROOT}/scripts/reflect.sh off`
- `status`: Check auto-reflect state → Run `${CLAUDE_PLUGIN_ROOT}/scripts/reflect.sh status`

**Metrics & analysis:**
- `stats [skill]`: Show effectiveness metrics → Run `${CLAUDE_PLUGIN_ROOT}/scripts/reflect-stats.sh [skill]`
- `cleanup`: Clean old memories → Run `${CLAUDE_PLUGIN_ROOT}/scripts/reflect-cleanup-memories.sh`

If arguments match subcommands above, execute and exit. Otherwise, continue to main workflow.

---

## Main Reflection Workflow

### Step 0: Pre-Flight Checks

**Identify skill name:**
```bash
SKILL_NAME="$ARGUMENTS"

# If not provided, detect from conversation or ask user
if [ -z "$SKILL_NAME" ]; then
    # Ask: Which skill should I analyze? (frontend-design, code-reviewer, etc.)
    exit
fi
```

**Check if skill is paused:**

Pause status: !`test -f ~/.claude/reflect-paused-skills/"$ARGUMENTS".paused && cat ~/.claude/reflect-paused-skills/"$ARGUMENTS".paused 2>/dev/null || echo "ACTIVE"`

If paused, display:
```
⚠️  Skill '$SKILL_NAME' is currently paused

[Show pause reason and timestamp from above]

To resume: /reflect resume $SKILL_NAME
To see stats: /reflect stats $SKILL_NAME
```

**Stop here if paused.** Do not proceed to Step 1.

---

### Step 1: Load Context & Memories

**Load accumulated learnings:**

**Cross-skill patterns:**
!`cat ~/.claude/memories/skill-patterns.md 2>/dev/null || echo "# No cross-skill patterns yet"`

**Skill-specific preferences:**
!`cat ~/.claude/memories/"$ARGUMENTS"-prefs.md 2>/dev/null || echo "# No preferences for this skill yet"`

**Meta-learnings (if analyzing reflect itself):**
!`if [ "$ARGUMENTS" = "reflect" ]; then cat ~/.claude/memories/reflect-meta.md 2>/dev/null || echo "# No meta-learnings yet"; fi`

These memories inform what patterns to look for and known user preferences.

---

### Step 2: Gather Signals

**Priority 1: External Feedback (Objective Evidence)**

Recent test/lint/build failures for this skill:
!`grep "\"skill\":\"$ARGUMENTS\"" ~/.claude/reflect-external-feedback/latest-feedback.jsonl 2>/dev/null | tail -10 || echo "No external feedback"`

External feedback types:
- Test failures (pytest, jest, vitest)
- Lint errors (ruff, eslint, mypy)
- Build failures
- Type errors

**Priority 2: Conversation Signals**

For large conversations (>10k tokens), use context compression:
```bash
# Use Task tool with context-manager agent
Task:
  subagent_type: "context-manager"
  description: "Extract reflect signals"
  prompt: "Extract from conversation:
    - User corrections (rejections, change requests)
    - User successes (approvals, positive feedback)
    - Edge cases (unexpected questions, workarounds)
    - Repeated preferences
    Focus on skill: $SKILL_NAME. Remove irrelevant content."
```

Otherwise, analyze full conversation for:

**Signal Types & Confidence:**
- 🔴 **CORRECTIONS** (HIGH confidence): User said "no", explicitly corrected, requested immediate changes
- 🟢 **SUCCESSES** (MEDIUM confidence): User said "perfect"/"great", accepted output, built on it
- 🟡 **EDGE CASES** (MEDIUM confidence): Unanticipated questions, workarounds needed, uncovered features
- 🔵 **PREFERENCES** (LOW confidence): Repeated patterns across sessions

**Count each signal type** - these numbers will be logged to metrics.

📖 **Detailed signal examples**: See `references/signal-examples.md`

---

### Step 3: Generate & Validate Proposal

#### Step 3A: Draft Proposal

Create proposal with confidence-ranked changes:

```
Skill Reflection: $SKILL_NAME
Session: ${CLAUDE_SESSION_ID}

Signals: X corrections, Y successes, Z edge cases, W preferences

Proposed changes:
🔴 HIGH: [Add constraint|Update guideline] - "[specific change]"
🟡 MED:  [Add preference|Clarify ambiguity] - "[specific change]"
🔵 LOW:  [Add preference] - "[specific change]"

Evidence:
- [Quote specific user feedback or external errors]

Commit: "$SKILL_NAME: [concise summary]"
```

**Confidence mapping:**
- HIGH = Corrections + External feedback
- MEDIUM = Strong patterns + Edge cases + Successes
- LOW = Weak signals + Single-instance preferences

📖 **Proposal templates**: See `references/proposal-templates.md`

---

#### Step 3B: Validate with Critic

**CRITICAL**: Before presenting to user, validate with reflect-critic agent.

```bash
# Use Task tool to invoke critic
Task:
  subagent_type: "cainish:reflect-critic"
  description: "Validate reflect proposal"
  prompt: "
    Validate this proposal:

    Skill: $SKILL_NAME
    Signals: X corrections, Y successes, Z edge cases

    Proposed Changes:
    [paste drafted proposal]

    Validate against:
    1. 12-factor agent principles
    2. Signal-to-proposal alignment
    3. Implementation feasibility

    Provide:
    - Score (0-100)
    - Recommendation (APPROVE/APPROVE with suggestions/REVISE/REJECT)
    - Specific feedback
  "
```

**Decision tree:**
- **90-100 (Excellent)**: Proceed to Step 3C with proposal as-is
- **70-89 (Good)**: Incorporate critic suggestions, then proceed to Step 3C
- **50-69 (Needs work)**: Revise proposal based on feedback, re-validate
- **0-49 (Poor)**: Reject proposal, gather more signals or try different approach

📖 **Critic validation details**: See `agents/reflect-critic.md` and `references/proposal-validation-guide.md`

---

#### Step 3C: Present Final Proposal

After validation, present to user:

```
Skill Reflection: $SKILL_NAME
Session: ${CLAUDE_SESSION_ID}

Signals: X corrections, Y successes, Z edge cases

Proposed changes:
🔴 HIGH: [action] - "[description]"
🟡 MED:  [action] - "[description]"
🔵 LOW:  [action] - "[description]"

Commit: "$SKILL_NAME: [summary]"

Critic Score: X/100 ([Excellent|Good|Needs work])
Critic Recommendation: [key insights]

Apply? [Y/n] or describe tweaks
```

---

### Step 4: If Approved

**1. Log metrics with session ID:**
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/reflect-track-proposal.sh \
  "$SKILL_NAME" approved \
  --session "${CLAUDE_SESSION_ID}" \
  --corrections X \
  --successes Y \
  --edge-cases Z \
  --preferences W
```

**2. Update memories (NOT the skill's SKILL.md):**

Choose appropriate memory file based on scope:

**Cross-skill pattern** (applies to multiple skills):
```bash
cat >> ~/.claude/memories/skill-patterns.md <<EOF

---

## [Pattern Name] (Added: $(date +%Y-%m-%d), Session: ${CLAUDE_SESSION_ID})

**Pattern**: [Brief description]

**Applies to**: skill1, skill2, skill3

**Evidence**:
- [Specific examples]
- Session: ${CLAUDE_SESSION_ID}

**Implementation**:
- [Concrete guidance]
EOF
```

**Skill-specific preference**:
```bash
PREFS_FILE=~/.claude/memories/${SKILL_NAME}-prefs.md

# Create if doesn't exist
if [ ! -f "$PREFS_FILE" ]; then
    cat > "$PREFS_FILE" <<EOF
# ${SKILL_NAME^} Preferences

Skill-specific learnings for ${SKILL_NAME}.

Last updated: $(date +%Y-%m-%d)
---
EOF
fi

cat >> "$PREFS_FILE" <<EOF

## [Preference Topic] (Added: $(date +%Y-%m-%d), Session: ${CLAUDE_SESSION_ID})

**Preference**: [Description]

**Source**: [User correction|External feedback|Edge case|Success]

**Evidence**: [What happened]

**Implementation**: [How to apply]
EOF
```

**Meta-learning** (improving reflect itself):
```bash
cat >> ~/.claude/memories/reflect-meta.md <<EOF

## [Learning Topic] (Added: $(date +%Y-%m-%d), Session: ${CLAUDE_SESSION_ID})

**Learning**: [What was learned]

**Evidence**: [Data/research/metrics]

**Application**: [How this changes reflect's behavior]
EOF
```

**3. Only modify SKILL.md for structural changes:**

Only edit actual SKILL.md if:
- Adding new workflow step
- Changing core instructions
- Fixing bugs in the skill logic

For preferences/learnings, use memories.

**4. Commit & push:**
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/reflect-commit-changes.sh \
  "$SKILL_NAME" "[summary]" \
  --session "${CLAUDE_SESSION_ID}"
```

📖 **Git workflow details**: See `references/git-workflow.md`

**5. Confirm:**
```
✓ Memory updated for $SKILL_NAME
✓ Metrics logged (session: ${CLAUDE_SESSION_ID})
✓ Changes committed and pushed
```

---

### Step 5: If Declined

**1. Log rejection metrics:**
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/reflect-track-proposal.sh \
  "$SKILL_NAME" rejected \
  --session "${CLAUDE_SESSION_ID}" \
  --corrections X \
  --successes Y \
  --edge-cases Z \
  --preferences W
```

**2. Optionally save observations:**

Save to `${CLAUDE_PLUGIN_ROOT}/skills/$SKILL_NAME/OBSERVATIONS.md` for future reference.

**3. Check for auto-pause:**

If this is the 3rd consecutive rejection, the skill will be auto-paused by the tracking script.

---

## Advanced Workflows

### Validate Skill

When invoked as `/reflect validate [skill-name]`:

1. Load the skill's SKILL.md
2. Use Task tool with `reflect-critic` agent to validate against 12-factor principles
3. Report score and recommendations without modifying anything

### Meta-Improvement

When invoked as `/reflect improve`:

Run effectiveness analysis:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/reflect-analyze-effectiveness.sh
```

This analyzes metrics to identify patterns in proposal acceptance/rejection and suggests improvements to the reflect workflow itself.

### Self-Reflection

When invoked as `/reflect reflect`:

Apply the reflect workflow to itself:
1. Analyze recent reflect sessions
2. Detect patterns in how reflect works
3. Propose improvements to reflect's own SKILL.md
4. Update `~/.claude/memories/reflect-meta.md`

---

## Reference Documentation

For comprehensive details, see these reference files:

- **`references/signal-examples.md`** - Detailed examples of each signal type with evidence patterns
- **`references/proposal-templates.md`** - Templates for HIGH/MED/LOW confidence proposals
- **`references/12-factor-compliance.md`** - 12-factor agent principles guide
- **`references/proposal-validation-guide.md`** - How critic validates proposals
- **`references/metrics-schema.md`** - JSONL schema for metrics tracking
- **`references/memory-system.md`** - Memory file management patterns
- **`references/git-workflow.md`** - Git commit and push procedures
- **`references/context-compression.md`** - Handling large conversations
- **`references/error-handling.md`** - Error handling patterns
- **`references/automated-cleanup-guide.md`** - Memory cleanup procedures
- **`references/phase-5-guide.md`** - Advanced workflow guidance

---

## Important Notes

- **Always show exact changes** before applying
- **Never modify skills** without explicit user approval
- **Use memories** for accumulated learnings (not SKILL.md)
- **Count signals accurately** for metrics tracking
- **Include session IDs** for better correlation
- **Validate with critic** before presenting proposals
- **Commit messages** should be concise and descriptive

## Example Output

```
Skill Reflection: frontend-design
Session: abc123def456

Signals: 2 corrections, 3 successes, 1 edge case

Proposed changes:
🔴 HIGH: Add constraint - "Never use gradients unless explicitly requested"
🔴 HIGH: Update guideline - "Dark backgrounds: always use #000 not #1a1a1a"
🟡 MED: Add preference - "Prefer CSS Grid over Flexbox for card layouts"

Commit: "frontend-design: no gradients, #000 dark, prefer Grid"

Critic Score: 92/100 (Excellent)
Critic: Strong signal alignment, clear constraints, actionable

Apply? [Y/n]
```
