---
id: cognitive-walkthrough
name: "Cognitive Walkthrough"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Cognitive Walkthrough

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #research #cognitive-walkthrough #usability-inspection
- **Agent:** faion-usability-agent

---

## Problem

New users struggle with your product but you don't understand why. User testing is not available for early designs. The team thinks the interface is intuitive but users disagree. Onboarding is complex but you can't pinpoint problems. You need to evaluate learnability specifically.

Without cognitive walkthrough:
- Learnability issues hidden
- First-time user struggles missed
- Onboarding problems unclear
- Unintuitive flows remain

---

## Framework

### What is Cognitive Walkthrough?

A cognitive walkthrough is a usability inspection method where evaluators step through a task from the user's perspective, focusing on whether a first-time user can figure out how to complete the task without prior training.

### Focus Areas

| Area | Questions |
|------|-----------|
| **Learnability** | Can new users figure it out? |
| **Action visibility** | Is the next step obvious? |
| **Understanding** | Will users know what to do? |
| **Feedback** | Will users know they did right? |

### Cognitive Walkthrough vs. Heuristic Evaluation

| Aspect | Cognitive Walkthrough | Heuristic Evaluation |
|--------|----------------------|----------------------|
| Focus | Task completion by new user | Broad usability principles |
| Method | Step-by-step task analysis | Expert review against heuristics |
| Questions | 4 specific questions per step | 10 general heuristics |
| Best for | Learnability, onboarding | General usability issues |

---

## Process

### Step 1: Define Prerequisites

**Identify:**
- Target user persona
- Task to evaluate
- Correct action sequence
- Interface to evaluate (prototype or live)

```
Example:
Persona: First-time user, no prior experience
Task: Create a new account and set up profile
Correct sequence:
1. Click "Sign Up"
2. Enter email
3. Enter password
4. Click "Create Account"
5. Enter profile name
6. Upload photo (optional)
7. Click "Complete Setup"
```

### Step 2: Assemble Evaluators

**Who should participate:**
- UX designers
- Product managers
- Developers
- Anyone who understands users

**Group size:** 2-4 evaluators

### Step 3: Walk Through Each Step

For each action in the sequence, ask:

**Question 1: Will the user try to achieve the right effect?**
- Does the user know they need to do something?
- Does the user understand the goal?

**Question 2: Will the user notice that the correct action is available?**
- Is the action visible?
- Is it in an expected location?

**Question 3: Will the user associate the correct action with the desired effect?**
- Does the label make sense?
- Is the purpose clear?

**Question 4: If the correct action is performed, will the user see that progress is being made?**
- Is there feedback?
- Does the user know it worked?

### Step 4: Document Issues

For any "No" answer:
- Describe the problem
- Explain why it's an issue
- Suggest a solution

### Step 5: Summarize Findings

- List all issues found
- Prioritize by severity
- Recommend fixes

---

## Templates

### Walkthrough Planning Template

```markdown
# Cognitive Walkthrough Plan

**Date:** [Date]
**Facilitator:** [Name]
**Evaluators:** [Names]

## User Profile

**Persona:** [Name or description]
**Experience level:** [First-time user / Occasional / etc.]
**Prior knowledge:** [What they already know]
**Goal:** [What they're trying to achieve]

## Task Definition

**Task:** [Clear task statement]

**Success criteria:** [What counts as completion]

## Correct Action Sequence

| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | [Action] | [Result] |
| 2 | [Action] | [Result] |
| 3 | [Action] | [Result] |

## Interface

**Type:** Prototype / Staging / Production
**Link:** [URL or file location]

## Scope

- Pages/screens included: [List]
- What's out of scope: [List]
```

### Walkthrough Evaluation Form

```markdown
# Cognitive Walkthrough Evaluation

**Task:** [Task name]
**Step:** [Step number and description]

## Question 1: Will user try to achieve the right effect?

**Answer:** Yes / No / Partial

**Notes:**
[Why or why not]

---

## Question 2: Will user notice correct action is available?

**Answer:** Yes / No / Partial

**Notes:**
[Why or why not]

---

## Question 3: Will user associate action with desired effect?

**Answer:** Yes / No / Partial

**Notes:**
[Why or why not]

---

## Question 4: Will user see progress is being made?

**Answer:** Yes / No / Partial

**Notes:**
[Why or why not]

---

## Issues Found

| Issue | Question | Severity | Suggestion |
|-------|----------|----------|------------|
| [Issue] | Q1/Q2/Q3/Q4 | H/M/L | [Fix] |

## Screenshot

[Annotated screenshot if applicable]
```

### Summary Report Template

```markdown
# Cognitive Walkthrough Report

**Date:** [Date]
**Task:** [Task evaluated]
**Evaluators:** [Names]

## Executive Summary

**Steps evaluated:** [Number]
**Issues found:** [Number]
**Critical issues:** [Number]

**Key finding:** [Most important takeaway]

## Task Overview

**Persona:** [User description]
**Goal:** [What user is trying to do]
**Optimal path:** [Number of steps]

## Findings by Step

### Step 1: [Action description]

**Issues found:**
- [Issue 1]: [Description]
  - Question affected: [Q1/Q2/Q3/Q4]
  - Impact: [Description]
  - Recommendation: [Fix]

### Step 2: [Action description]

[Same structure]

## Issues Summary

| Step | Issue | Question | Severity | Status |
|------|-------|----------|----------|--------|
| 1 | [Issue] | Q2 | High | Open |
| 2 | [Issue] | Q4 | Medium | Open |

## Priority Recommendations

### Critical (Fix before launch)
1. [Recommendation]
2. [Recommendation]

### Important (Fix soon)
1. [Recommendation]

### Nice to have
1. [Recommendation]

## Positive Findings

[What worked well - don't change these]

## Appendix

- Detailed evaluation forms
- Screenshots
- Prototype links
```

---

## Examples

### Example 1: Sign-Up Flow

**Step:** Click "Get Started" button

| Question | Answer | Notes |
|----------|--------|-------|
| Q1: Will try? | Yes | Clear value proposition above button |
| Q2: Will notice? | Partial | Button visible but competes with "Sign In" |
| Q3: Will associate? | No | "Get Started" unclear if it means sign up or demo |
| Q4: Progress visible? | Yes | Takes user to registration form |

**Issue:** "Get Started" is ambiguous
**Fix:** Change to "Create Free Account"

### Example 2: File Upload

**Step:** Drag file to upload zone

| Question | Answer | Notes |
|----------|--------|-------|
| Q1: Will try? | Partial | Users might look for browse button first |
| Q2: Will notice? | Yes | Large drop zone visible |
| Q3: Will associate? | Yes | Icon and text suggest drag-drop |
| Q4: Progress visible? | No | No indication file is uploading |

**Issue:** Missing upload progress indicator
**Fix:** Add progress bar and file name during upload

---

## The Four Questions Deep Dive

### Q1: Will user try to achieve right effect?

**Checks:**
- Is the goal clear?
- Does user know action is needed?
- Is motivation present?

**Common failures:**
- User doesn't know something is required
- User thinks they're done when they're not
- Goal is unclear

### Q2: Will user notice correct action available?

**Checks:**
- Is control visible?
- Is it in expected location?
- Does it stand out?

**Common failures:**
- Action is below the fold
- Control doesn't look clickable
- Too many competing options

### Q3: Will user associate action with effect?

**Checks:**
- Is the label clear?
- Is the icon recognizable?
- Does it match user's mental model?

**Common failures:**
- Jargon in labels
- Ambiguous icons
- Unexpected location

### Q4: Will user see progress is being made?

**Checks:**
- Is there feedback?
- Does UI change appropriately?
- Is success communicated?

**Common failures:**
- No loading indicator
- Page looks the same after action
- Error not displayed

---

## Common Mistakes

1. **Using power users** - Should evaluate for first-time users
2. **Skipping steps** - Must evaluate every action
3. **Not documenting "Yes"** - Record positive findings too
4. **Vague issues** - Be specific about what's wrong
5. **No recommendations** - Always suggest a fix

---

## Best Practices

### Before the Walkthrough

```
Preparation:
- Have working interface ready
- Print evaluation forms
- Define realistic user persona
- Identify complete action sequence
- Brief evaluators on method
```

### During the Walkthrough

```
Process:
- Go step by step, don't skip ahead
- Answer all four questions for every step
- Take notes on the spot
- Capture screenshots
- Discuss disagreements
```

### After the Walkthrough

```
Follow-up:
- Compile findings immediately
- Prioritize issues
- Share with team
- Track fixes
- Consider re-evaluation
```

---

## When to Use

| Situation | Cognitive Walkthrough Appropriate |
|-----------|-----------------------------------|
| Early prototypes | Yes |
| Before user testing | Yes |
| Onboarding flows | Yes |
| New feature launch | Yes |
| Complex workflows | Yes |
| Frequent tasks | No, use heuristic evaluation |
| Expert users | No, focus on efficiency instead |

---

## Checklist

Before walkthrough:
- [ ] User persona defined
- [ ] Task clearly stated
- [ ] Correct sequence documented
- [ ] Interface accessible
- [ ] Evaluators briefed
- [ ] Forms prepared

During walkthrough:
- [ ] Each step evaluated
- [ ] All four questions answered
- [ ] Issues documented with details
- [ ] Recommendations captured
- [ ] Screenshots taken

After walkthrough:
- [ ] Report compiled
- [ ] Issues prioritized
- [ ] Findings shared
- [ ] Fixes assigned
- [ ] Re-evaluation scheduled

---

## References

- Usability Inspection Methods by Nielsen & Mack
- Cognitive Walkthroughs by Wharton et al.
- UX research community: Cognitive Walkthroughs