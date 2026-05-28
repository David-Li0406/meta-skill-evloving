---
id: usability-testing
name: "Usability Testing"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Usability Testing

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #research #usability #testing
- **Agent:** faion-usability-agent

---

## Problem

Products are launched without validation. Design decisions are based on assumptions. Issues are discovered after development is complete. Users struggle with interfaces that seemed intuitive to designers. Costly redesigns happen post-launch.

Without usability testing:
- Usability problems undetected
- Poor user experience
- Higher development costs
- Lower conversion/adoption

---

## Framework

### What is Usability Testing?

Usability testing observes real users attempting to complete tasks with a product. It reveals what works, what confuses, and where users struggle.

### Test Types

| Type | Description | When to Use |
|------|-------------|-------------|
| **Moderated** | Facilitator present | Complex tasks, need probing |
| **Unmoderated** | Remote, automated | Scale, quick feedback |
| **Think-aloud** | User verbalizes thoughts | Understanding mental model |
| **First-click** | Where users click first | Navigation, IA |

### What Usability Measures

| Metric | What It Shows |
|--------|---------------|
| **Effectiveness** | Can users complete tasks? |
| **Efficiency** | How long does it take? |
| **Satisfaction** | How do users feel? |
| **Errors** | What mistakes do users make? |
| **Learnability** | How quickly do users learn? |

---

## Process

### Step 1: Define Goals

What do you want to learn?

```
Goal examples:
- Can users complete checkout in under 3 minutes?
- Do users understand the navigation structure?
- What blocks users from signing up?
```

### Step 2: Create Test Plan

| Element | Description |
|---------|-------------|
| **Objectives** | What to learn |
| **Participants** | Who to test |
| **Tasks** | What users will do |
| **Metrics** | What to measure |
| **Environment** | Where/how |

### Step 3: Write Tasks

**Good tasks:**
- Realistic scenarios
- Clear goals
- No hints about solution

**Task template:**
```
Scenario: [Context]
Task: [What to accomplish]
Success criteria: [How to measure]
```

### Step 4: Recruit Participants

- 5-8 participants per segment
- Match target user profile
- Mix of experience levels

### Step 5: Conduct Sessions

**Session structure:**
1. Introduction (5 min)
2. Pre-test questions (5 min)
3. Tasks (30-45 min)
4. Post-test questions (10 min)
5. Debrief (5 min)

### Step 6: Analyze Results

- Review recordings
- Note problems and severity
- Quantify metrics
- Prioritize findings

### Step 7: Report and Act

- Document findings
- Recommend solutions
- Share with team
- Plan fixes

---

## Templates

### Test Plan Template

```markdown
# Usability Test Plan: [Product/Feature]

**Version:** [X.X]
**Date:** [Date]
**Researcher:** [Name]

## Objectives
What questions will this study answer?
1. [Question 1]
2. [Question 2]

## Methodology
- **Type:** Moderated / Unmoderated
- **Format:** In-person / Remote
- **Duration:** [X] minutes per session
- **Think-aloud:** Yes / No

## Participants
- **Number:** [X] participants
- **Profile:** [Description of target users]
- **Recruitment:** [How recruited]
- **Compensation:** [Incentive]

## Test Environment
- **Location:** [Where]
- **Equipment:** [Devices, recording]
- **Prototype/Product:** [What they will test]

## Tasks

### Task 1: [Name]
**Scenario:** [Context for user]
**Task:** [What to accomplish]
**Success criteria:** [How to measure success]
**Time limit:** [X minutes]

### Task 2: [Name]
[Same structure]

## Metrics

| Metric | How Measured |
|--------|--------------|
| Task success rate | % completing task |
| Time on task | Duration |
| Error rate | Mistakes counted |
| Satisfaction | Post-task rating |

## Schedule
| Date | Time | Participant |
|------|------|-------------|
| [Date] | [Time] | P1 |

## Deliverables
- [ ] Test recordings
- [ ] Findings report
- [ ] Recommendations
```

### Session Script Template

```markdown
# Usability Test Script

## Introduction (5 min)

"Hi [name], thanks for joining today. I'm [name], and I'll be
guiding you through this session.

We're testing [product], not testing you. There are no wrong
answers. We want honest feedback to improve the product.

I'd like you to think aloud as you work - tell me what you're
thinking, what you expect, and what confuses you.

Do you have any questions before we start?"

## Pre-test Questions (5 min)
1. What is your experience with [domain]?
2. Have you used similar products before?

## Tasks (30-45 min)

### Task 1
"Imagine you want to [scenario].
Starting from this screen, please [task].
Remember to think aloud."

[Observe and note without helping]

**Post-task questions:**
- On a scale of 1-5, how easy was that?
- What was confusing, if anything?

### Task 2
[Same structure]

## Post-test Questions (10 min)
1. What was your overall impression?
2. What would you change?
3. Would you use this product? Why/why not?

## Close
"Thank you so much for your time and feedback.
Do you have any final questions for me?"
```

---

## Examples

### Good Task Examples

```
Scenario: You need to change your delivery address for an
upcoming order.

Task: Find your recent order and update the shipping address.

Success: User locates order and changes address.
```

### Bad Task Examples

```
Bad: "Click the account button and select orders"
(Gives away the answer)

Better: "Find your order history"
(Clear goal, no hints)
```

---

## Severity Ratings

| Severity | Description | Priority |
|----------|-------------|----------|
| **Critical** | Users cannot complete task | Fix immediately |
| **High** | Significant difficulty | Fix before launch |
| **Medium** | Some struggle | Fix soon |
| **Low** | Minor friction | Fix when possible |

---

## Common Findings Format

```markdown
## Finding: [Title]

**Severity:** Critical / High / Medium / Low
**Task:** [Which task]
**Frequency:** [X of Y participants]

### Problem
[What happened / what users struggled with]

### Evidence
- "[Quote from user]"
- [Observed behavior]

### Impact
[Why this matters]

### Recommendation
[How to fix]
```

---

## Common Mistakes

1. **Helping users** - Resist urge to guide
2. **Too few participants** - Need 5+ for patterns
3. **Wrong participants** - Not matching target users
4. **Leading tasks** - Hints in task wording
5. **No metrics** - Subjective observations only

---

## Moderated vs. Unmoderated

| Aspect | Moderated | Unmoderated |
|--------|-----------|-------------|
| Facilitator | Present | None |
| Probing | Can ask follow-up | Pre-set questions |
| Scale | Fewer sessions | More sessions |
| Cost | Higher | Lower |
| Insights | Deeper | Broader |
| Best for | Complex, exploratory | Validation, metrics |

---

## Checklist

- [ ] Test plan documented
- [ ] Tasks written without hints
- [ ] Participants recruited (right profile)
- [ ] Prototype/product ready
- [ ] Recording equipment tested
- [ ] Consent forms prepared
- [ ] Facilitator trained (no helping)
- [ ] Analysis completed
- [ ] Findings prioritized by severity
- [ ] Recommendations actionable

---

## References

- UX research community: Usability Testing
- Rocket Surgery Made Easy by Steve Krug
- Measuring the User Experience