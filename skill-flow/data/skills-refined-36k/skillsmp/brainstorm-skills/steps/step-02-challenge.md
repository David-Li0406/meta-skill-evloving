---
name: step-02-challenge
description: Critical challenge phase - devil's advocate stress-testing all findings
next_step: steps/step-03-synthesize.md
---

# Phase 2: Critical Challenge

**Role: DEVIL'S ADVOCATE** - Question everything mercilessly

---

<available_state>
From previous steps:

- `{topic}` - The research topic
- `{economy_mode}` - If true, use direct tool calls instead of subagents
- `{fast_mode}` - If true, this step was SKIPPED (you shouldn't be here)
- `{save_file}` - If true, save session to file
- `{session_path}` - Path to session file (if saving)
- `{phase_1_discoveries}` - Broad findings from Phase 1
  </available_state>

---

<mandatory_rules>

## MANDATORY EXECUTION RULES (READ FIRST)

- 🔥 CHALLENGE every finding from Phase 1 - nothing is sacred
- ❓ SEARCH for contradicting evidence and opposing viewpoints
- 🕳️ IDENTIFY gaps, assumptions, and weak points
- 🧠 UPDATE mental model based on challenges - change your mind!
- 🚫 FORBIDDEN: Accepting anything at face value
- 🚫 FORBIDDEN: Defending Phase 1 findings against legitimate challenges
  </mandatory_rules>

---

<execution_sequence>

<review_findings>
**1. Review Phase 1 with Skeptical Eyes**

Look at `{phase_1_discoveries}` and ask for EACH finding:

- What evidence supports this? Is it strong or weak?
- Who benefits from this being true? (follow the incentives)
- What's the sample size / scope of this claim?
- Is this recency bias? survivorship bias? selection bias?
- What would need to be true for this to be wrong?

**Mark each finding:**

- ✅ Strong evidence (multiple independent sources)
- ⚠️ Moderate evidence (some support, some gaps)
- ❌ Weak evidence (assumption, anecdote, or single source)
  </review_findings>

<challenge_agents>
**2. Execute Challenge Research**

<economy_mode_research>
**If `{economy_mode}` = true:** Use direct tool calls

**Web Search** (use WebSearch tool directly)

- Search: `{topic} problems failures criticisms`
- Search: `{topic} downsides risks hidden costs`
- Search: `{topic} alternatives why not to use`

Focus on finding counter-arguments and failures.
</economy_mode_research>

<standard_mode_research>
**If `{economy_mode}` = false:** Launch parallel subagents

**CRITICAL: Launch ALL agents in a SINGLE message for parallel execution.**

**Agent 1: Devil's Advocate Search** (`websearch`)

```
Search for criticisms and problems with: {topic} + [popular approaches from Phase 1]

Find:
1. Criticisms and failures of the popular approaches
2. Failed implementations and why they failed
3. Experts who disagree with the mainstream view
4. Hidden costs, risks, or downsides
5. Cautionary tales and horror stories

Focus on finding the OTHER side of the story.
```

**Agent 2: Gap Analysis Search** (`websearch`)

```
Search for what's missing from discussions about: {topic}

Find:
1. Edge cases rarely discussed
2. Long-term consequences often ignored
3. Alternative approaches that get overlooked
4. Questions that experts avoid answering
5. Assumptions that are rarely questioned

Focus on what's NOT being said.
```

</standard_mode_research>
</challenge_agents>

<systematic_challenge>
**3. Challenge Each Phase 1 Finding**

For each major finding from Phase 1:

**Finding: "[Phase 1 finding]"**

**Challenge Questions:**

- What evidence contradicts this?
- Who disagrees and why might they be right?
- What could go wrong if we act on this belief?
- What's the weakest link in the reasoning?
- What assumption is this built on?

**Counter-evidence found:**

- [Contradicting source/evidence]

**Updated belief:**

- Original confidence: [High/Medium/Low]
- New confidence: [Higher/Same/Lower]
- Reason for change: [What new info emerged]

Repeat for each major finding.
</systematic_challenge>

<gap_analysis>
**4. Identify Gaps and Assumptions**

**Unanswered Questions:**

- [Critical question that Phase 1 didn't answer]
- [Question that emerged from challenges]

**Hidden Assumptions:**

- We're assuming [assumption 1] - but is this valid?
- We're assuming [assumption 2] - what if we're wrong?

**Missing Evidence:**

- We don't have data on [important aspect]
- No one seems to address [gap]

**Blind Spots:**

- Phase 1 research may have missed [area]
- We should have also looked at [unexplored angle]
  </gap_analysis>

<synthesize_challenges>
**5. Synthesize Challenge Findings**

```
## Phase 2 Challenges: {topic}

**Findings That Survived Challenge:**
- [Finding]: Still confident because [reason]

**Findings Now In Doubt:**
- [Finding]: Challenged by [evidence], new confidence: [level]

**Completely Reversed:**
- [Finding]: Was wrong because [reason]

**Critical Gaps Identified:**
1. [Gap 1] - This matters because...
2. [Gap 2] - We can't proceed without knowing...

**Assumptions We're Making:**
1. [Assumption] - Risk if wrong: [consequence]

**Updated Mental Model:**
After challenging Phase 1 findings, my view has shifted:
- [What changed]
- [What stayed the same but is now more confident]
- [What needs more investigation]
```

Store in `{phase_2_challenges}`
</synthesize_challenges>

<save_progress>
**6. Save Progress** (if `{save_file}` is true)

Append to `{session_path}`:

```markdown
## Phase 2: Critical Challenge

[Phase 2 challenges content]

---
```

</save_progress>

</execution_sequence>

---

<success_metrics>

- Every Phase 1 finding actively challenged
- Counter-evidence actively searched for
- Assumptions explicitly identified
- Mental model updated based on challenges
- Confidence levels adjusted honestly
- Gaps and blind spots documented
  </success_metrics>

<failure_modes>

- Defending Phase 1 findings instead of challenging them
- Only seeking weak counter-arguments to dismiss
- Not actually changing beliefs based on evidence
- Skipping the gap analysis
- Being skeptical in word but not in action
  </failure_modes>

---

<next_step_directive>
**CRITICAL:** After presenting Phase 2 challenges, immediately state:

"**Phase 2 complete.** We've stress-tested our findings and updated our mental model.

**What changed:**

- [Key shift in understanding]
- [Finding that was strengthened]
- [Finding that was weakened or reversed]

**NEXT: Phase 3 - Multi-Lens Synthesis**

Now I become the MULTI-LENS SYNTHESIZER. We'll examine everything through 5 different expert perspectives to find patterns and build a complete picture.

Loading `step-03-synthesize.md`..."

Then load and execute `steps/step-03-synthesize.md`.
</next_step_directive>
