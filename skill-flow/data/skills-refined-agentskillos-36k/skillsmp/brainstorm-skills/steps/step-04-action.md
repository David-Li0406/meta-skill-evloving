---
name: step-04-action
description: Action crystallization phase - transform insights into clear recommendations and actions
---

# Phase 4: Action Crystallization

**Role: STRATEGIC ADVISOR** - Transform insight into clear, actionable recommendations

---

<available_state>
From previous steps:

- `{topic}` - The research topic
- `{economy_mode}` - If true, used direct tool calls instead of subagents
- `{fast_mode}` - If true, skipped Phase 2 and used 3 perspectives in Phase 3
- `{save_file}` - If true, save session to file
- `{session_path}` - Path to session file (if saving)
- `{phase_1_discoveries}` - Broad findings from Phase 1
- `{phase_2_challenges}` - Challenges from Phase 2 (empty if fast_mode)
- `{phase_3_synthesis}` - Multi-perspective analysis from Phase 3
  </available_state>

---

<mandatory_rules>

## MANDATORY EXECUTION RULES (READ FIRST)

- 🎯 FORM clear, defensible recommendations - no wishy-washy conclusions
- 📊 ASSIGN confidence levels HONESTLY - admit uncertainty
- ⚔️ PRESENT the strongest contrarian view - steelman the opposition
- 📋 CREATE actionable next steps - specific, not vague
- 🔗 CITE sources for key claims
- 🚫 FORBIDDEN: Vague conclusions like "it depends" without specifics
- 🚫 FORBIDDEN: Hiding uncertainty behind confident language
  </mandatory_rules>

---

<execution_sequence>

<ultra_think>
**1. ULTRA THINK: Deep Synthesis**

Before producing output, deeply consider:

**What do the phases tell us?**

- Phase 1 (Exploration): The landscape is...
- Phase 2 (Challenge): After stress-testing, the strongest findings are... _(skip if fast_mode)_
- Phase 3 (Multi-lens): Across perspectives, the clearest signals are...

**What's my honest recommendation?**

- If I had to advise someone today, I would say...
- The confidence I have in this is... because...

**What would change my mind?**

- If [evidence/event], I would reconsider
- The weakest part of my reasoning is...

**What's the strongest argument against my recommendation?**

- The best counter-argument is...
- Why someone might reasonably disagree...
  </ultra_think>

<generate_output>
**2. Generate Final Output**

Produce the final brainstorm output in this format:

```markdown
## 🧠 Brainstorm: {topic}

### Research Summary

**Process completed:**

- **Phase 1 (Exploration):** [# of sources], [breadth of coverage]
- **Phase 2 (Challenge):** [# of findings challenged], [# revised] _(skipped if fast_mode)_
- **Phase 3 (Synthesis):** [3 or 5] perspectives analyzed, [key patterns found]
- **Mode:** [Standard / Economy / Fast / Economy+Fast]

**Key areas investigated:**

- [Area 1]
- [Area 2]
- [Area 3]

---

### Key Insights

1. **[Insight 1]** - Confidence: **High/Medium/Low**
   - [Supporting evidence and reasoning]

2. **[Insight 2]** - Confidence: **High/Medium/Low**
   - [Supporting evidence and reasoning]

3. **[Insight 3]** - Confidence: **High/Medium/Low**
   - [Supporting evidence and reasoning]

4. **[Insight 4]** - Confidence: **High/Medium/Low**
   - [Supporting evidence and reasoning]

5. **[Insight 5]** - Confidence: **High/Medium/Low**
   - [Supporting evidence and reasoning]

---

### Recommendation

**Primary recommendation:**
[Clear, specific recommendation]

**Rationale:**
[Why this recommendation based on all research]

**Key tradeoffs accepted:**

- [Tradeoff 1]: We're choosing [X] over [Y] because...
- [Tradeoff 2]: We're accepting [risk] for [benefit]

**Overall Confidence: [High/Medium/Low]**

- Would change to higher if: [evidence needed]
- Would change to lower if: [counter-evidence]

---

### Contrarian View

**The strongest argument against this recommendation:**

[Steelman the opposing view - present it as compellingly as possible]

**Why someone might reasonably choose differently:**

- [Reason 1]
- [Reason 2]

**When the contrarian view might be right:**

- If [condition], then [alternative] would be better

---

### Open Questions

**Still needs investigation:**

1. [Question 1] - Why it matters: [impact]
2. [Question 2] - Why it matters: [impact]
3. [Question 3] - Why it matters: [impact]

**Assumptions that need validation:**

- [Assumption] - How to validate: [method]

---

### Immediate Actions

**This week:**

1. [Specific action 1]
2. [Specific action 2]
3. [Specific action 3]

**Before committing fully:**

- [Validation step or experiment to run]

---

### Sources

**Key references:**

- [Source 1]: [What it contributed]
- [Source 2]: [What it contributed]
- [Source 3]: [What it contributed]

**Perspectives consulted:**

- [Expert/Source] on [topic]
- [Expert/Source] on [topic]
```

</generate_output>

<save_final>
**3. Save Final Output** (if `{save_file}` is true)

Append to `{session_path}`:

```markdown
## Phase 4: Action Crystallization

[Complete final output above]

---

## Session Complete

**Total research phases:** 4
**Research completed:** {current_date}
```

Also announce: "Session saved to `{session_path}`"
</save_final>

<completion>
**4. Completion Message**

```
---

**✅ Brainstorm Complete**

This research covered:
- Broad exploration with parallel agents
- Skeptical challenge of all findings
- Analysis through 5 expert perspectives
- Crystallization into actionable recommendations

**Confidence summary:**
- [# High confidence] insights
- [# Medium confidence] insights
- [# Low confidence] insights

**Next steps are clear:** [summarize top 1-2 actions]

**Open for follow-up:** Ask me to dig deeper on any specific area.
```

</completion>

</execution_sequence>

---

<confidence_calibration>

## Confidence Level Guidelines

**High Confidence:**

- Multiple independent sources agree
- Survived skeptical challenge
- Multiple perspectives converge
- Clear evidence, minimal assumptions

**Medium Confidence:**

- Good evidence but some gaps
- Some perspectives diverge
- Reasonable assumptions required
- More investigation would help

**Low Confidence:**

- Limited evidence
- Significant uncertainty
- Conflicting perspectives
- Important assumptions untested
  </confidence_calibration>

---

<success_metrics>

- Clear, specific recommendations (not "it depends")
- Honest confidence levels with calibration
- Strongest contrarian view presented fairly
- Actionable next steps (specific, not vague)
- Open questions acknowledge what we don't know
- Sources cited for key claims
- Complete output format followed
  </success_metrics>

<failure_modes>

- Vague recommendations that don't commit
- Overconfident conclusions hiding uncertainty
- Weak strawman of contrarian view
- "Next steps" that are too generic to act on
- Forgetting to cite sources
- Rushing the synthesis without ULTRA THINK
  </failure_modes>

---

<workflow_complete>

## Workflow Complete

The brainstorm-skills workflow has completed all 4 phases:

1. ✅ **Expansive Exploration** - Cast wide net
2. ✅ **Critical Challenge** - Stress-tested findings
3. ✅ **Multi-Lens Synthesis** - 5 perspectives analyzed
4. ✅ **Action Crystallization** - Clear recommendations

The user now has battle-tested insights ready for action.
</workflow_complete>
