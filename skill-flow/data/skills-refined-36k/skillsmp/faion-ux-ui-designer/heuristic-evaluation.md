---
id: heuristic-evaluation
name: "Heuristic Evaluation"
domain: UX
skill: faion-ux-ui-designer
category: "ux-design"
---

# Heuristic Evaluation

## Metadata
- **Category:** UX / Research Methods
- **Difficulty:** Intermediate
- **Tags:** #methodology #ux #research #heuristic-evaluation #expert-review
- **Agent:** faion-usability-agent

---

## Problem

Full usability testing is expensive and time-consuming. You need quick feedback on a design. Obvious usability problems should be found before testing with users. Resources are limited but you need quality assessment.

Without heuristic evaluation:
- Obvious problems reach users
- Testing resources wasted on known issues
- No expert perspective
- Slower iteration

---

## Framework

### What is Heuristic Evaluation?

Heuristic evaluation is a usability inspection method where evaluators examine an interface against established usability principles (heuristics).

### Nielsen's 10 Heuristics

| # | Heuristic | Core Question |
|---|-----------|---------------|
| 1 | Visibility of system status | Is user informed? |
| 2 | Match real world | Does it use user language? |
| 3 | User control | Can user undo and exit? |
| 4 | Consistency | Is it predictable? |
| 5 | Error prevention | Does it prevent mistakes? |
| 6 | Recognition over recall | Are options visible? |
| 7 | Flexibility and efficiency | Does it support experts? |
| 8 | Aesthetic minimalist | Is it clutter-free? |
| 9 | Error recovery | Are errors helpful? |
| 10 | Help and documentation | Is help available? |

### When to Use

| Situation | Heuristic Eval Appropriate |
|-----------|---------------------------|
| Early design review | Yes |
| Before usability testing | Yes |
| Quick assessment needed | Yes |
| Deep user insights needed | No, use testing |
| Validating with real users | No, use testing |

---

## Process

### Step 1: Prepare

**Define scope:**
- Which parts of interface
- Which user flows
- Which heuristics to focus on

**Gather materials:**
- Interface or prototype access
- Task scenarios
- Evaluation template

### Step 2: Select Evaluators

**Ideal:**
- 3-5 evaluators
- UX expertise
- Domain knowledge helpful

**Why multiple?**
- Different evaluators find different problems
- 3-5 finds ~75% of problems

### Step 3: Conduct Individual Evaluations

Each evaluator independently:
1. Explores interface freely
2. Goes through key tasks
3. Notes violations of heuristics
4. Rates severity

**Important:** Independent evaluation first, then combine.

### Step 4: Compile Findings

Combine all evaluator findings:
- Remove duplicates
- Aggregate severity ratings
- Organize by heuristic or location

### Step 5: Prioritize Issues

| Severity | Description | Priority |
|----------|-------------|----------|
| **0** | Not a problem | N/A |
| **1** | Cosmetic | Fix if time |
| **2** | Minor | Low priority |
| **3** | Major | High priority |
| **4** | Catastrophe | Fix immediately |

### Step 6: Report and Recommend

Document findings with:
- Problem description
- Location
- Heuristic violated
- Severity
- Recommendation

---

## Templates

### Evaluation Template

```markdown
# Heuristic Evaluation: [Product/Feature]

**Evaluator:** [Name]
**Date:** [Date]
**Version:** [Prototype/Live]

## Scope
- Pages/screens evaluated: [List]
- User flows: [List]

## Findings

### Issue 1
- **Location:** [Where in interface]
- **Heuristic:** [Which heuristic violated]
- **Problem:** [Description of issue]
- **Severity:** [0-4]
- **Recommendation:** [Suggested fix]
- **Screenshot:** [If applicable]

### Issue 2
[Same structure]

## Summary

| Heuristic | Issues Found |
|-----------|--------------|
| 1. Visibility | [Count] |
| 2. Match real world | [Count] |
| ... | |

## Top Priority Issues
1. [Most critical]
2. [Second]
3. [Third]
```

### Compiled Report Template

```markdown
# Heuristic Evaluation Report: [Product]

**Date:** [Date]
**Evaluators:** [Names]
**Scope:** [What was evaluated]

## Executive Summary
[High-level findings]

## Methodology
- [X] evaluators independently reviewed
- Used Nielsen's 10 heuristics
- Severity rated 0-4

## Findings by Severity

### Severity 4 (Catastrophic)
[Issues that must be fixed]

### Severity 3 (Major)
[Issues that should be fixed]

### Severity 2 (Minor)
[Issues to fix if possible]

### Severity 1 (Cosmetic)
[Issues for polish]

## Findings by Heuristic

### 1. Visibility of System Status
| Location | Problem | Severity | Recommendation |
|----------|---------|----------|----------------|
| [Location] | [Problem] | [0-4] | [Fix] |

### 2. Match Between System and Real World
[Same structure]

[Continue for all 10]

## Statistics

| Heuristic | Issues | % of Total |
|-----------|--------|------------|
| [Heuristic] | [X] | [X%] |

## Recommendations
1. [Priority recommendation]
2. [Second recommendation]
3. [Third recommendation]

## Appendix
- Full issue list
- Screenshots
```

---

## Examples

### Example Finding

```markdown
**Location:** Checkout page, payment form
**Heuristic:** #5 Error Prevention
**Problem:** No validation for credit card number format.
Users can enter letters and invalid numbers without warning
until form submission.
**Severity:** 3 (Major)
**Recommendation:** Add real-time format validation.
Show checkmarks as user enters valid sections.
Detect card type automatically.
```

### Severity Rating Examples

| Severity | Example |
|----------|---------|
| 0 | Preference, not usability issue |
| 1 | Icon could be clearer |
| 2 | Help link is hard to find |
| 3 | Cannot complete task without confusion |
| 4 | Critical function is broken |

---

## Common Mistakes

1. **Evaluators collaborate** - Must be independent first
2. **Only one evaluator** - Misses many issues
3. **Too general findings** - "UI is confusing" not actionable
4. **No severity rating** - All issues seem equal
5. **Ignoring findings** - Report but no action

---

## Heuristic Evaluation vs. Usability Testing

| Aspect | Heuristic Eval | Usability Testing |
|--------|----------------|-------------------|
| Who | UX experts | Real users |
| Finds | Standards violations | Real struggles |
| Speed | Fast | Slower |
| Cost | Lower | Higher |
| Insights | Expert opinion | User behavior |
| Best for | Quick assessment | Deep understanding |

**Best approach:** Heuristic evaluation to find obvious issues, then usability testing.

---

## Heuristic Cheat Sheet

### Quick Check Questions

| # | Quick Question |
|---|----------------|
| 1 | Does the user always know system status? |
| 2 | Is language user-friendly? |
| 3 | Can user undo and go back? |
| 4 | Is everything consistent? |
| 5 | Are errors prevented? |
| 6 | Are options visible? |
| 7 | Are there shortcuts for experts? |
| 8 | Is it clean and minimal? |
| 9 | Do errors help fix problems? |
| 10 | Is help available? |

---

## Checklist

- [ ] Scope defined
- [ ] Heuristics selected
- [ ] 3-5 evaluators recruited
- [ ] Evaluators trained on method
- [ ] Independent evaluations completed
- [ ] Findings compiled
- [ ] Severity ratings assigned
- [ ] Findings prioritized
- [ ] Recommendations provided
- [ ] Report shared with team

---

## References

- UX research community: Heuristic Evaluation
- How to Conduct a Heuristic Evaluation
- Usability Inspection Methods