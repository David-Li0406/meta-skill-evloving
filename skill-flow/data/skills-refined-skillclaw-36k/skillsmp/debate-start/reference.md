# Start Debate Reference

Extended guidance for moderating multi-team debates.

---

## Scratchpad Template Structure

```
# Debate: {TOPIC}
{CONTEXT}
Status / Created

## Team Positions
  ### Red/Blue/Green/Yellow/Purple Team + Stance

## Round 1: Opening Arguments
  ### [RED] / [BLUE] / [GREEN] / [YELLOW] / [PURPLE]

## Round 2: Rebuttals
  ### [RED] / [BLUE] / [GREEN] / [YELLOW] / [PURPLE]

## Round 3: Synthesis
  ### [PURPLE]

## Moderator Notes

## Conclusion
  ### Summary / Agreements / Disagreements / Recommendations
```

Full template: [templates/debate-scratchpad.md](templates/debate-scratchpad.md)

---

## Team Perspective Definitions

### Red Team (Required)
**Role:** Challenger / Skeptic / Attacker

- Questions assumptions and status quo
- Identifies weaknesses, risks, and failure modes
- Plays devil's advocate against proposed solutions
- Stress-tests arguments for logical consistency

**Default stance:** "Why this won't work" or "What could go wrong"

### Blue Team (Required)
**Role:** Defender / Advocate / Builder

- Argues for the proposed approach or status quo
- Highlights strengths, benefits, and opportunities
- Provides evidence supporting the position
- Addresses concerns raised by opposition

**Default stance:** "Why this will work" or "How we succeed"

### Green Team (Optional)
**Role:** Pragmatist / Implementer

- Focuses on practical feasibility
- Considers resource constraints and timelines
- Proposes incremental or hybrid approaches
- Bridges theory and execution

**Default stance:** "How we actually build this"

### Yellow Team (Optional)
**Role:** Risk Analyst / Safety Advocate

- Identifies security, safety, and compliance concerns
- Considers edge cases and failure scenarios
- Evaluates long-term consequences
- Proposes safeguards and mitigations

**Default stance:** "What we must protect against"

### Purple Team (Optional)
**Role:** Synthesizer / Integrator

- Finds common ground between positions
- Identifies false dichotomies
- Proposes hybrid solutions
- Facilitates convergence

**Default stance:** "How we combine the best of both"

---

## Intervention Decision Tree

```
After each round, assess:

1. PROGRESS CHECK
   └─ Are teams making new substantive points?
      ├─ Yes → Continue
      └─ No → Intervention: STUCK
              "Team X, consider: [new angle/question]"

2. BALANCE CHECK
   └─ Is discussion one-sided?
      ├─ No → Continue
      └─ Yes → Intervention: IMBALANCE
               "Team Y, respond to Team X's point about [specific]"

3. RELEVANCE CHECK
   └─ Are teams staying on topic?
      ├─ Yes → Continue
      └─ No → Intervention: ASTRAY
              "Refocus: The core question is [restate topic]"

4. DEPTH CHECK
   └─ Are arguments substantive with evidence?
      ├─ Yes → Continue
      └─ No → Intervention: SHALLOW
              "Team X, provide specific evidence for [claim]"

5. ENGAGEMENT CHECK
   └─ Are teams responding to each other?
      ├─ Yes → Continue
      └─ No → Intervention: DISCONNECTED
              "Team X, address Team Y's argument about [specific]"
```

---

## Intervention Format

All interventions are written to the Moderator Notes section:

```markdown
### [MODERATOR] {timestamp}

**Type:** {Stuck|Imbalance|Astray|Shallow|Disconnected}
**Target:** {Team color or "All"}
**Issue:** {Brief description of problem}
**Guidance:** {Specific direction for team(s)}
```

Example:
```markdown
### [MODERATOR] Round 1 Review

**Type:** Disconnected
**Target:** Blue Team
**Issue:** Blue has not addressed Red's security concerns
**Guidance:** Blue Team, in your rebuttal, specifically respond to
Red's point about authentication vulnerabilities in the proposed API design.
```

---

## Common Failure Modes

### 1. Echo Chamber
**Symptom:** Teams agree too quickly without substantive debate
**Cause:** Topic not controversial enough or stances too similar
**Fix:** Sharpen distinctions, assign more adversarial stances

### 2. Talking Past Each Other
**Symptom:** Teams make points but don't engage with opposition
**Cause:** Unclear topic framing or teams not reading opponent arguments
**Fix:** Direct teams to quote and respond to specific opponent claims

### 3. Tunnel Vision
**Symptom:** Team repeats same argument in different words
**Cause:** Team stuck on single angle, not exploring alternatives
**Fix:** Suggest new dimensions: "Consider the [cost/timeline/user] angle"

### 4. Analysis Paralysis
**Symptom:** Teams research endlessly without committing to arguments
**Cause:** Topic too broad or teams too cautious
**Fix:** Set explicit scope, ask for "best current argument given available info"

### 5. Premature Convergence
**Symptom:** Teams agree before fully exploring disagreements
**Cause:** Conflict avoidance or insufficient adversarial framing
**Fix:** Ask probing questions: "But what about X?" "How do you respond to Y?"

---

## Example Debate Flow

**Topic:** "Should we migrate from REST to GraphQL for our public API?"

### Round 1: Opening

**Red (Against migration):**
- Breaking change for existing clients
- Team lacks GraphQL expertise
- Performance concerns with N+1 queries
- Tooling ecosystem less mature

**Blue (For migration):**
- Reduces over-fetching, improves mobile performance
- Single endpoint simplifies client development
- Strong typing improves API documentation
- Industry momentum and developer preference

**Green (Pragmatic):**
- Suggests hybrid: GraphQL for new features, REST maintained
- Proposes 6-month pilot with single client team

### Moderator Intervention
```
[MODERATOR] Red and Blue are presenting solid positions but not engaging.
Blue Team: Address Red's concern about N+1 query performance.
Red Team: Respond to Blue's over-fetching argument with data.
```

### Round 2: Rebuttals

**Blue responds:** DataLoader pattern solves N+1, shows benchmark data
**Red responds:** Over-fetching solvable with sparse fieldsets in REST

### Synthesis

**Purple Team synthesis:**
- Both approaches can work; choice depends on client diversity
- Recommendation: GraphQL for new mobile-first features
- Keep REST for B2B integrations with existing contracts
- Shared schema validation regardless of transport

### Conclusion

**Agreements:**
- Current API has real performance issues worth addressing
- Team needs training regardless of choice

**Disagreements:**
- Migration cost/benefit ratio
- Timeline for full transition

**Recommendation:**
Start GraphQL pilot for new mobile app feature; evaluate after 3 months.
