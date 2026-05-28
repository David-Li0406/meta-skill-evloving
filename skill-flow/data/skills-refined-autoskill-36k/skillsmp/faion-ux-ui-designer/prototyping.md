---
id: prototyping
name: "Prototyping"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Prototyping

## Metadata
- **Category:** UX / Design Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #design #prototyping #testing
- **Agent:** faion-usability-agent

---

## Problem

Static designs cannot convey interactions. Stakeholders do not understand how something will work. Usability issues hide until development. Building the wrong thing is expensive. Words cannot communicate experience.

Without prototyping:
- Interaction issues undetected
- Stakeholder misunderstanding
- Expensive development mistakes
- Delayed user feedback

---

## Framework

### What is Prototyping?

A prototype is an interactive representation of a product that simulates user experience before development.

### Prototype Fidelity

| Fidelity | Detail | Time to Create | Use For |
|----------|--------|----------------|---------|
| **Low** | Paper, basic clicks | Hours | Concept testing |
| **Medium** | Key interactions | Days | Design validation |
| **High** | Near-final | Weeks | Detailed testing |

### Prototype Types

| Type | Description | Best For |
|------|-------------|----------|
| **Paper** | Sketches, paper screens | Very early ideas |
| **Clickable** | Linked screens | Flow testing |
| **Interactive** | Animated, responsive | Experience testing |
| **Code** | HTML/CSS prototype | Technical validation |

---

## Process

### Step 1: Define Goals

What will the prototype help you learn?

```
Examples:
- Can users complete checkout?
- Is the navigation structure clear?
- Does the onboarding flow make sense?
```

### Step 2: Determine Fidelity

| If You Need... | Choose... |
|----------------|-----------|
| Quick concept validation | Low fidelity |
| Flow testing | Medium fidelity |
| Realistic experience | High fidelity |
| Technical feasibility | Code prototype |

### Step 3: Create Prototype

**Essential elements:**
- Key screens
- Critical interactions
- Realistic content (enough)
- Clear user path

### Step 4: Test Prototype

Run usability tests:
- Define tasks
- Observe users
- Note problems
- Gather feedback

### Step 5: Iterate

Based on findings:
- Fix major issues
- Re-test if needed
- Document decisions
- Hand off to development

---

## Templates

### Prototype Plan Template

```markdown
# Prototype Plan: [Feature/Product]

**Version:** [X.X]
**Date:** [Date]
**Designer:** [Name]

## Objectives
What questions will this prototype answer?
1. [Question 1]
2. [Question 2]

## Fidelity
**Level:** Low / Medium / High
**Rationale:** [Why this level]

## Scope

### Included
- [Screen/Flow 1]
- [Screen/Flow 2]
- [Key interaction]

### Not Included
- [What is out of scope]

## User Flows to Prototype

### Flow 1: [Name]
1. [Start screen]
2. [Step 2]
3. [Step 3]
4. [End screen]

### Flow 2: [Name]
[Same structure]

## Interactive Elements

| Element | Interaction | Behavior |
|---------|-------------|----------|
| [Element] | [Click/Tap/Etc] | [What happens] |

## Testing Plan
- **Participants:** [How many, who]
- **Tasks:** [What users will try]
- **Method:** [Moderated/Unmoderated]

## Timeline
- Design: [Date range]
- Testing: [Date range]
- Iteration: [Date range]
```

### Prototype Testing Notes Template

```markdown
# Prototype Testing Notes

**Participant:** [ID]
**Date:** [Date]
**Facilitator:** [Name]

## Task 1: [Task Description]

**Success:** Yes / No / Partial
**Time:** [Duration]

**Observations:**
- [What user did]
- [Where they struggled]
- [What they said]

**Quote:** "[User quote]"

## Task 2: [Task Description]
[Same structure]

## Overall Feedback
- Liked: [What worked]
- Disliked: [What didn't work]
- Confused by: [What was unclear]

## Issues Found

| Issue | Severity | Location | Notes |
|-------|----------|----------|-------|
| [Issue] | H/M/L | [Screen] | [Notes] |

## Recommendations
- [Recommendation 1]
- [Recommendation 2]
```

---

## Examples

### Paper Prototype

```
Materials: Paper, scissors, pens

Process:
1. Draw screens on paper
2. Cut out interactive elements
3. User "clicks" by pointing
4. Swap paper to show next screen

Pros: Fast, cheap, anyone can do it
Cons: Limited realism
```

### Clickable Prototype (Figma)

```
Process:
1. Create screen designs
2. Add click areas (hotspots)
3. Link screens together
4. Define transitions

Pros: Quick, testable, shareable
Cons: Limited interaction depth
```

### Interactive Prototype

```
Process:
1. Create high-fidelity designs
2. Add animations
3. Create realistic interactions
4. Add variable content

Pros: Realistic experience
Cons: Time-intensive
```

---

## Tools

| Tool | Fidelity | Best For |
|------|----------|----------|
| **Paper** | Very low | Early ideas |
| **Figma** | Low-High | All-around choice |
| **Framer** | High | Complex interactions |
| **ProtoPie** | High | Advanced animations |
| **InVision** | Low-Medium | Quick prototypes |
| **Principle** | High | Micro-interactions |
| **Code (React)** | Highest | Technical validation |

---

## Best Practices

### Do
- Focus on what you need to learn
- Use realistic content
- Test early and often
- Start low fidelity
- Prototype the risky parts

### Don't
- Over-polish before testing
- Prototype everything
- Skip user testing
- Ignore technical constraints
- Forget edge cases

---

## Common Mistakes

1. **Too high fidelity too early** - Wastes time
2. **Not testing** - Building prototype but not learning
3. **Prototyping everything** - Focus on key flows
4. **Ignoring findings** - Testing but not changing
5. **No clear hypothesis** - What are you trying to learn?

---

## Prototype Critique Questions

- Does it answer our research questions?
- Are the key flows covered?
- Is fidelity appropriate for our goals?
- Is there enough content to feel real?
- Are interactive elements clear?
- What scenarios are missing?

---

## From Prototype to Production

### Handoff Includes

| Artifact | Purpose |
|----------|---------|
| Prototype link | Interactive reference |
| Screen specs | Detailed measurements |
| Interaction specs | How things behave |
| Assets | Icons, images |
| Component library | Reusable elements |
| Edge cases | Error states, empty states |

---

## Checklist

- [ ] Clear testing objectives
- [ ] Appropriate fidelity chosen
- [ ] Key flows prototyped
- [ ] Realistic enough content
- [ ] Interactions defined
- [ ] User testing conducted
- [ ] Findings documented
- [ ] Iterations made
- [ ] Ready for development handoff

---

## References

- Sprint by Jake Knapp
- Prototyping: A Practitioner's Guide
- UX research community: Prototyping