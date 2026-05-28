---
id: design-critique
name: "Design Critique"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Design Critique

## Metadata
- **Category:** UX / Design Methods
- **Difficulty:** Beginner
- **Tags:** #methodology #ux #design #critique #feedback
- **Agent:** faion-usability-agent

---

## Problem

Design reviews turn into opinion battles. Feedback is vague: "I don't like it." Good ideas are killed by personal preferences. Junior designers don't get useful feedback. Designs don't improve through iteration. Team alignment is difficult to achieve.

Without structured critique:
- Opinion-based decisions
- Vague, unhelpful feedback
- Inconsistent design quality
- Team misalignment

---

## Framework

### What is Design Critique?

Design critique is a structured conversation about a design where participants analyze work against defined goals and principles, providing specific, actionable feedback to improve the design.

### Critique vs. Criticism

| Critique | Criticism |
|----------|-----------|
| Based on goals | Based on preference |
| Specific and actionable | Vague and personal |
| About the work | About the designer |
| Asks questions | Makes judgments |
| Improves design | Hurts feelings |

### Roles in Critique

| Role | Responsibility |
|------|----------------|
| **Presenter** | Shows work, states goals, asks for feedback |
| **Facilitator** | Keeps on track, ensures everyone speaks |
| **Participants** | Ask questions, give feedback against goals |
| **Note-taker** | Captures feedback and decisions |

---

## Process

### Step 1: Set Context (Presenter)

Before showing designs:

```
Share:
- What problem are we solving?
- Who is the user?
- What are the constraints?
- What stage is this design?
- What type of feedback is needed?
```

**Feedback types:**
- **Directional:** Is this the right approach?
- **Refinement:** How can this be better?
- **Polish:** Is this ready to ship?

### Step 2: Present the Work

**Presenter guidelines:**
- Walk through the design systematically
- Explain key decisions already made
- Point out areas of uncertainty
- Don't over-explain or apologize

```
Good: "The user clicks here to submit. I'm unsure
       about the confirmation message placement."

Bad:  "I know this isn't great, but I tried this
       thing, you probably won't like it..."
```

### Step 3: Clarifying Questions

Participants ask to understand, not judge:

```
Good questions:
- "What's the user's goal at this point?"
- "What happens if they click X?"
- "Is this flow required or optional?"

Bad questions:
- "Why didn't you do it the other way?"
- "Have you considered [my preferred approach]?"
```

### Step 4: Give Feedback

**Feedback structure:**
1. State the observation
2. Connect to goal or principle
3. Explain the impact
4. (Optional) Suggest alternatives

```
Example:
"The submit button is below the fold [observation].
We know from research that users often miss it [principle].
This could hurt conversion [impact].
What if we added a sticky footer? [suggestion]"
```

### Step 5: Capture and Prioritize

Note-taker captures:
- Key feedback points
- Questions raised
- Decisions made
- Action items

Presenter decides what to incorporate (their design, their call).

---

## Templates

### Critique Session Template

```markdown
# Design Critique: [Feature/Screen Name]

**Date:** [Date]
**Duration:** [30-60 min]
**Presenter:** [Name]
**Facilitator:** [Name]
**Participants:** [Names]

## Context

**Problem being solved:**
[What user problem are we addressing?]

**Target user:**
[Who is this for?]

**Constraints:**
- [Technical constraint]
- [Business constraint]
- [Timeline constraint]

**Design stage:**
[ ] Exploration (many directions)
[ ] Iteration (refining one direction)
[ ] Polish (final details)

**Feedback requested:**
[What type of feedback is most helpful now?]

## Design Goals

| Goal | Success looks like |
|------|-------------------|
| [Goal 1] | [How we'll know it's met] |
| [Goal 2] | [How we'll know it's met] |

## Critique Notes

### What's working well
- [Positive observation]
- [Positive observation]

### Questions and concerns
- [Feedback item with reasoning]
- [Feedback item with reasoning]

### Suggestions
- [Specific suggestion]
- [Specific suggestion]

## Action Items

| Item | Priority | Owner |
|------|----------|-------|
| [Action] | H/M/L | [Name] |

## Decisions Made

- [Decision 1]
- [Decision 2]
```

### Feedback Framework Template

```markdown
## Giving Feedback

Use this structure for each piece of feedback:

**Observation:**
I notice that [specific element/behavior]

**Principle/Goal:**
Our goal is [goal] / The principle of [principle] suggests...

**Impact:**
This might [positive/negative impact] because...

**Alternative (optional):**
What if we tried [specific alternative]?

---

**Example:**

**Observation:**
I notice the error message appears at the top of the form.

**Principle:**
Users typically expect errors near the problematic field.

**Impact:**
This might cause confusion as users scroll down to fix the
error but can't see what the error message said.

**Alternative:**
What if we showed inline errors next to each field?
```

---

## Examples

### Example 1: Mobile Checkout Flow

**Context:** Redesigning checkout for mobile, goal is to reduce abandonment.

**Feedback given:**

1. "The progress indicator shows 5 steps. Research shows mobile users abandon at 4+ steps. Could any steps be combined?"

2. "The keyboard covers the 'Next' button on the address form. This breaks our principle of always-visible CTAs."

3. "Love how the saved payment method is one tap. This aligns perfectly with our 'reduce effort' goal."

### Example 2: Dashboard Redesign

**Context:** New analytics dashboard, goal is quick insight discovery.

**Bad feedback:** "I don't like the colors."

**Good feedback:** "The color coding uses red for both 'urgent' and 'error' states. This might confuse users trying to prioritize actions. What if urgent used a different color family?"

---

## Critique Principles

### For Giving Feedback

| Do | Don't |
|----|-------|
| Connect to goals | Base on personal preference |
| Be specific | Be vague ("make it pop") |
| Ask questions first | Assume you understand |
| Offer alternatives | Only criticize |
| Focus on work, not person | Make it personal |
| Consider constraints | Ignore reality |

### For Receiving Feedback

| Do | Don't |
|----|-------|
| Listen fully | Defend immediately |
| Ask clarifying questions | Argue each point |
| Thank people | Take it personally |
| Decide what to incorporate | Accept everything |
| Follow up on decisions | Ignore feedback |

### For Facilitating

| Do | Don't |
|----|-------|
| Keep discussion on track | Let it wander |
| Ensure everyone speaks | Let one voice dominate |
| Redirect opinion to goals | Allow taste debates |
| Time-box discussions | Let them run over |
| Summarize key points | Skip the summary |

---

## Common Mistakes

1. **No stated goals** - Feedback becomes opinion without criteria
2. **Wrong stage feedback** - Polish feedback on exploration work
3. **Solutioning not critiquing** - Designing in the meeting
4. **Too many cooks** - Everyone redesigning instead of analyzing
5. **Defending instead of listening** - Presenter argues every point

---

## Critique Formats

### Quick Critique (15 min)

```
- Context: 2 min
- Present: 5 min
- Feedback: 5 min
- Wrap-up: 3 min
```
Best for: Daily check-ins, small decisions

### Standard Critique (30-45 min)

```
- Context: 5 min
- Present: 10 min
- Questions: 5 min
- Feedback: 15 min
- Wrap-up: 5 min
```
Best for: Feature reviews, design iterations

### Deep Dive (60+ min)

```
- Context: 10 min
- Present: 15 min
- Silent review: 10 min
- Structured feedback: 20 min
- Discussion: 10 min
- Action items: 5 min
```
Best for: Major features, strategic decisions

---

## Async Critique

For remote/async teams:

### Format

```markdown
## [Designer] requests critique on [Feature]

**Context:** [Problem, user, constraints]
**Design stage:** [Exploration/Iteration/Polish]
**Feedback requested by:** [Date]

[Link to designs]

---

**Please comment on:**
1. Does this solve the problem?
2. Does it follow our design principles?
3. What concerns do you have?
4. What's working well?

Use the format: Observation → Principle → Impact → (Suggestion)
```

### Async Tips

- Set clear deadlines
- Use commenting tools (Figma, Loom)
- Number feedback for reference
- Presenter summarizes and responds

---

## Building Critique Culture

### Getting Started

```
1. Start small (2-3 people)
2. Model good feedback
3. Create safe environment
4. Celebrate learning from feedback
5. Expand as culture develops
```

### Ground Rules

Post these in critique sessions:

```
1. Critique the work, not the person
2. Be specific, not vague
3. Connect feedback to goals
4. Ask questions before judging
5. Suggest, don't dictate
6. Everyone participates
7. Presenter decides what to incorporate
```

---

## Checklist

Before critique:
- [ ] Goals clearly defined
- [ ] Designs ready to share
- [ ] Right people invited
- [ ] Time allocated appropriately
- [ ] Feedback type specified

During critique:
- [ ] Context shared
- [ ] Questions asked before feedback
- [ ] Feedback connected to goals
- [ ] Everyone participated
- [ ] Notes captured

After critique:
- [ ] Action items clear
- [ ] Decisions documented
- [ ] Follow-up scheduled if needed
- [ ] Thank participants

---

## References

- Discussing Design by Adam Connor & Aaron Irizarry
- Articulating Design Decisions by Tom Greever
- Design Critiques: Encourage a Positive Culture - NNg