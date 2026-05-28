---
name: step-03-synthesize
description: Multi-lens synthesis phase - analyze from 5 expert perspectives
next_step: steps/step-04-action.md
---

# Phase 3: Multi-Lens Synthesis

**Role: MULTI-LENS SYNTHESIZER** - See from every angle, find the patterns

---

<available_state>
From previous steps:

- `{topic}` - The research topic
- `{economy_mode}` - If true, use direct tool calls instead of subagents
- `{fast_mode}` - If true, use 3 perspectives instead of 5
- `{save_file}` - If true, save session to file
- `{session_path}` - Path to session file (if saving)
- `{phase_1_discoveries}` - Broad findings from Phase 1
- `{phase_2_challenges}` - Challenges from Phase 2 (empty if fast_mode skipped Phase 2)
  </available_state>

---

<mandatory_rules>

## MANDATORY EXECUTION RULES (READ FIRST)

- 🎭 ADOPT each perspective FULLY before moving to next
- 🔗 FIND patterns that emerge across multiple perspectives
- ⚖️ WEIGHT insights by strength of reasoning, not by popularity
- 🔍 DO targeted research for each perspective if needed
- 🚫 FORBIDDEN: Staying in one perspective too long
- 🚫 FORBIDDEN: Skipping perspectives that feel uncomfortable
  </mandatory_rules>

---

<the_five_lenses>

## Expert Perspectives

**Standard mode (5 perspectives):**
| Lens | Character | Core Question |
|------|-----------|---------------|
| 1 | The Pragmatist | What actually works in the real world? |
| 2 | The Perfectionist | What's the ideal solution if constraints didn't exist? |
| 3 | The Skeptic | What could go terribly wrong? |
| 4 | The Expert | What would a 10-year veteran prioritize? |
| 5 | The Beginner | What obvious questions are we not asking? |

**Fast mode (3 perspectives):** Pragmatist, Skeptic, Expert only
</the_five_lenses>

---

<execution_sequence>

<prepare>
**1. Prepare for Multi-Perspective Analysis**

Review available findings to ground the analysis:

**If `{fast_mode}` = true:**
"With Phase 1 complete (Phase 2 skipped for speed), we have:

- **Broad landscape** from exploration

Now I'll analyze `{topic}` through 3 expert lenses (Pragmatist, Skeptic, Expert)."

**If `{fast_mode}` = false:**
"With Phases 1 and 2 complete, we have:

- **Broad landscape** from exploration
- **Stress-tested findings** from challenges
- **Updated beliefs** based on evidence

Now I'll analyze `{topic}` through 5 expert lenses to build a complete picture."
</prepare>

<lens_1_pragmatist>
**2. LENS 1: The Pragmatist**

_"Theory is nice, but what actually works in production?"_

**Targeted research** (quick websearch if needed):

- Real-world case studies and post-mortems
- Production experiences from practitioners

**Analysis:**

```
## The Pragmatist's View

**What actually works:**
- [Approach that has proven track record]
- [Pattern that teams consistently succeed with]

**What looks good but fails in practice:**
- [Approach that sounds good but has hidden issues]

**The 80/20:**
- 80% of value comes from: [simple approach]
- Avoid premature optimization of: [complex approach]

**Pragmatist's recommendation:**
"If I had to ship this tomorrow, I would..."
```

</lens_1_pragmatist>

<lens*2_perfectionist>
**3. LENS 2: The Perfectionist** ⏭️ \_Skip if `{fast_mode}` = true*

_"If we had unlimited time and resources, what's the ideal?"_

**Analysis:**

```
## The Perfectionist's View

**The ideal solution:**
- [Theoretically perfect approach]
- [Why this is considered "best" in the abstract]

**What we'd need to get there:**
- [Resource 1]
- [Capability 2]
- [Time investment 3]

**Is perfection worth pursuing?**
- Gap between pragmatic and perfect: [assessment]
- Value of closing that gap: [analysis]

**Perfectionist's recommendation:**
"The gold standard would be... but consider [tradeoffs]"
```

</lens_2_perfectionist>

<lens_3_skeptic>
**4. LENS 3: The Skeptic**

_"What's the worst that could happen? What are the hidden risks?"_

**Targeted research** (quick websearch if needed):

- Security incidents, failures, vulnerabilities
- Long-term consequences and technical debt

**Analysis:**

```
## The Skeptic's View

**Hidden risks no one talks about:**
- [Risk 1]: Could happen if [condition]
- [Risk 2]: Often overlooked because [reason]

**Worst-case scenarios:**
- If [approach] fails, the consequence is [impact]

**Long-term concerns:**
- Technical debt: [assessment]
- Lock-in risks: [analysis]
- Scalability cliffs: [prediction]

**What could make this completely wrong:**
- [Scenario that would invalidate the approach]

**Skeptic's warning:**
"Watch out for... and have a plan for..."
```

</lens_3_skeptic>

<lens_4_expert>
**5. LENS 4: The Expert**

_"What would someone with 10 years of experience prioritize?"_

**Analysis:**

```
## The Expert's View

**What experts actually focus on:**
- [Priority 1]: Because experience shows...
- [Priority 2]: This is what separates success from failure

**Common mistakes of those newer to this:**
- [Mistake 1]: Seems right but leads to...
- [Mistake 2]: Overlooking...

**The non-obvious insight:**
- [Counterintuitive wisdom that comes from experience]

**Expert's prioritization:**
1. [Most important]: Because...
2. [Second priority]: Then...
3. [Can wait]: Worry about this later...

**Expert's recommendation:**
"If you only do one thing right, make it..."
```

</lens_4_expert>

<lens*5_beginner>
**6. LENS 5: The Beginner** ⏭️ \_Skip if `{fast_mode}` = true*

_"What basic questions are we not asking because we assume everyone knows?"_

**Analysis:**

```
## The Beginner's View

**Questions that feel "too basic" to ask:**
- Why do we actually need [assumption]?
- What if we just [simple alternative]?
- Has anyone tried NOT doing [standard practice]?

**Assumptions we're making:**
- We assume [X] is necessary, but is it?
- We assume [Y] is the goal, but who decided?

**Fresh perspective:**
- [Observation that experts overlook due to familiarity]

**Beginner's challenge:**
"Wait, why don't we just...?"
```

</lens_5_beginner>

<pattern_recognition>
**7. Find Patterns Across Perspectives**

**Cross-Perspective Analysis:**

**If `{fast_mode}` = true (3 perspectives):**

```
## Patterns Emerging (Fast Mode)

**Convergence:**
- [Insight that Pragmatist, Skeptic, and Expert all agree on]

**Key tension:**
- Pragmatist vs Skeptic: [tradeoff between speed and caution]

**Synthesis:**
The clearest signal across all 3 perspectives is...
```

**If `{fast_mode}` = false (5 perspectives):**

```
## Patterns Emerging

**Convergence (all perspectives agree):**
- [Insight that appears in 3+ perspectives]
- [Consistent recommendation]

**Tension (perspectives conflict):**
- Pragmatist vs Perfectionist: [tradeoff]
- Expert vs Beginner: [assumption being challenged]

**Strongest signal:**
When [multiple perspectives] all point to [conclusion], that's our strongest insight.

**Surprising emergence:**
The Beginner's question about [X] actually exposed a blind spot in the Expert's view about [Y].

**Synthesis:**
Weighing all perspectives, the clearest thread is...
```

Store in `{phase_3_synthesis}`
</pattern_recognition>

<save_progress>
**8. Save Progress** (if `{save_file}` is true)

Append to `{session_path}`:

```markdown
## Phase 3: Multi-Lens Synthesis

### The Pragmatist

[Pragmatist analysis]

### The Perfectionist

[Perfectionist analysis]

### The Skeptic

[Skeptic analysis]

### The Expert

[Expert analysis]

### The Beginner

[Beginner analysis]

### Patterns Emerging

[Cross-perspective synthesis]

---
```

</save_progress>

</execution_sequence>

---

<success_metrics>

- All perspectives explored (5 standard, 3 if fast_mode)
- Each lens given genuine consideration
- Targeted research done where perspectives needed data
- Patterns and tensions identified across perspectives
- Synthesis captures the strongest emergent insights
  </success_metrics>

<failure_modes>

- Giving lip service to perspectives without genuine analysis
- Skipping the Skeptic because findings are uncomfortable
- Letting one perspective dominate the synthesis
- Not finding the cross-perspective patterns
- Treating perspectives as checklist rather than genuine lenses
  </failure_modes>

---

<next_step_directive>
**CRITICAL:** After presenting multi-lens synthesis, immediately state:

"**Phase 3 complete.** We've seen `{topic}` from 5 expert perspectives and found the patterns.

**Strongest insights:**

- [Key convergence across perspectives]
- [Important tension to navigate]

**NEXT: Phase 4 - Action Crystallization**

Now I become the STRATEGIC ADVISOR. Time to crystallize everything into clear recommendations, honest confidence levels, and actionable next steps.

Loading `step-04-action.md`..."

Then load and execute `steps/step-04-action.md`.
</next_step_directive>
