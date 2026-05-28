---
id: business-process-analysis
name: "Business Process Analysis"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Business Process Analysis

## Metadata
- **Category:** BA Framework / Requirements Analysis and Design Definition
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #process #analysis #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

Nobody understands how work actually gets done. Processes exist only in people's heads. Different people do the same task differently. Inefficiencies are hidden in complex workflows. Process improvement happens without understanding the current state.

Without process analysis:
- Tribal knowledge risks
- Inconsistent execution
- Hidden inefficiencies
- Failed process changes

---

## Framework

### What is Business Process Analysis?

Business Process Analysis examines how work flows through an organization to:
- Understand current operations
- Identify improvement opportunities
- Design future state processes
- Support system requirements

### Process Analysis Stages

```
Identify Processes → Document Current State → Analyze → Design Future State → Validate
```

### Step 1: Identify Processes

List processes in scope:

| Process | Owner | Priority | In Scope |
|---------|-------|----------|----------|
| [Process 1] | [Name] | High | Yes |
| [Process 2] | [Name] | Medium | Yes |
| [Process 3] | [Name] | Low | No |

### Step 2: Document Current State

Map how process works today:

**Elements to capture:**
- Activities (what is done)
- Actors (who does it)
- Inputs and outputs
- Decisions and rules
- Systems used
- Exceptions and workarounds

### Step 3: Analyze the Process

Evaluate for issues:

| Analysis Type | Purpose |
|---------------|---------|
| **Value analysis** | Which steps add value? |
| **Time analysis** | Where are delays? |
| **Cost analysis** | What are the costs? |
| **Quality analysis** | Where do errors occur? |
| **Pain point analysis** | What frustrates people? |

**Value classification:**
- **Value-adding:** Directly serves customer/business
- **Business necessary:** Required but not directly valuable (compliance, reporting)
- **Non-value-adding:** Waste (waiting, rework, unnecessary approvals)

### Step 4: Design Future State

Create improved process:

**Improvement techniques:**
- Eliminate non-value steps
- Automate manual steps
- Parallelize sequential steps
- Simplify complex decisions
- Reduce handoffs

### Step 5: Validate and Plan

Confirm future state:
- Review with stakeholders
- Identify implementation requirements
- Plan transition
- Define metrics

---

## Process Modeling Notation

### BPMN Elements

| Symbol | Meaning | Example |
|--------|---------|---------|
| Rounded rectangle | Activity | "Review application" |
| Diamond | Gateway (decision) | "Approved?" |
| Circle | Start event | Process begins |
| Bold circle | End event | Process ends |
| Arrow | Flow | Sequence of steps |
| Rectangle | Pool/lane | Actor/department |

### Simple Flow Example

```
[Start] → [Receive Order] → <Check Stock>
                                ↓ Yes
                           [Ship Order] → [End]
                                ↓ No
                           [Backorder] → [Notify Customer] → [End]
```

---

## Templates

### Process Documentation Template

```markdown
# Process Documentation: [Process Name]

**Version:** [X.X]
**Date:** [Date]
**Process Owner:** [Name]
**Analyst:** [Name]

## Process Overview

**Purpose:** [Why this process exists]
**Trigger:** [What starts the process]
**Outcome:** [What the process produces]
**Frequency:** [How often it runs]

## Scope

**In Scope:**
- [Activity 1]
- [Activity 2]

**Out of Scope:**
- [Exclusion 1]
- [Exclusion 2]

## Actors

| Actor | Role | Responsibilities |
|-------|------|------------------|
| [Actor 1] | [Role] | [What they do] |
| [Actor 2] | [Role] | [What they do] |

## Inputs and Outputs

**Inputs:**
- [Input 1]: [Description]
- [Input 2]: [Description]

**Outputs:**
- [Output 1]: [Description]
- [Output 2]: [Description]

## Process Steps

| Step | Activity | Actor | System | Input | Output | Rules |
|------|----------|-------|--------|-------|--------|-------|
| 1 | [Activity] | [Who] | [System] | [Input] | [Output] | [Rules] |
| 2 | [Activity] | [Who] | [System] | [Input] | [Output] | [Rules] |

## Business Rules

| Rule ID | Rule | Applies To |
|---------|------|------------|
| BR-01 | [Rule description] | Step [X] |
| BR-02 | [Rule description] | Step [X] |

## Exceptions

| Exception | Handling | Frequency |
|-----------|----------|-----------|
| [Exception] | [How handled] | [How often] |

## Systems Used

| System | Steps | Purpose |
|--------|-------|---------|
| [System] | [Steps] | [Purpose] |

## Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Cycle time | [Value] | [Value] |
| Error rate | [Value] | [Value] |
| Cost per transaction | [Value] | [Value] |
```

### Process Analysis Template

```markdown
# Process Analysis: [Process Name]

**Date:** [Date]
**Analyst:** [Name]

## Current State Summary
[Brief description of current process]

## Analysis Findings

### Value Analysis

| Step | Activity | Value Type | Time | Notes |
|------|----------|------------|------|-------|
| 1 | [Activity] | VA/BN/NVA | [Time] | [Notes] |
| 2 | [Activity] | VA/BN/NVA | [Time] | [Notes] |

**Value Summary:**
- Value-Adding: [X%]
- Business Necessary: [X%]
- Non-Value-Adding: [X%]

### Pain Points

| Issue | Impact | Frequency | Root Cause |
|-------|--------|-----------|------------|
| [Issue] | [Impact] | [Frequency] | [Cause] |

### Bottlenecks

| Location | Wait Time | Cause | Impact |
|----------|-----------|-------|--------|
| [Step] | [Time] | [Cause] | [Impact] |

### Improvement Opportunities

| Opportunity | Type | Benefit | Effort |
|-------------|------|---------|--------|
| [Opportunity] | Eliminate/Automate/Simplify | [Benefit] | H/M/L |

## Recommendations

### Quick Wins (< 1 month)
1. [Recommendation]

### Medium-term (1-3 months)
1. [Recommendation]

### Long-term (3+ months)
1. [Recommendation]

## Future State Summary
[Description of improved process]

## Expected Benefits

| Metric | Current | Future | Improvement |
|--------|---------|--------|-------------|
| [Metric] | [Value] | [Value] | [%] |
```

---

## Examples

### Example 1: Order Processing Analysis

**Current State:**
1. Customer calls with order (5 min)
2. Rep enters into System A (10 min)
3. Manager approves > $500 (wait 2 hours avg)
4. Rep copies to System B (5 min)
5. Warehouse receives notification (next day)
6. Warehouse picks and packs (30 min)
7. Ships (1 day)

**Total cycle time:** 1.5 days

**Analysis:**
- Step 3 (approval wait): 2 hours - bottleneck
- Step 4 (copy to System B): Non-value-adding - manual integration
- Step 5 (next day notification): Unnecessary delay

**Future State Improvements:**
- Auto-approve orders < $1000 (eliminate step 3 for 80% of orders)
- Integrate System A and B (eliminate step 4)
- Real-time notification to warehouse (eliminate step 5 delay)

**Expected cycle time:** 4 hours (80% improvement)

### Example 2: Value Analysis

**Expense Report Process:**

| Step | Activity | Value Type | Time |
|------|----------|------------|------|
| 1 | Employee completes report | VA | 30 min |
| 2 | Upload receipts | BN | 15 min |
| 3 | Manager reviews | BN | 10 min |
| 4 | Correction cycle (avg 2x) | NVA | 40 min |
| 5 | Finance verification | BN | 20 min |
| 6 | Payment processing | VA | 5 min |

**Totals:**
- VA: 35 min (29%)
- BN: 45 min (38%)
- NVA: 40 min (33%)

**Opportunity:** Eliminate correction cycle with better upfront validation

---

## Common Mistakes

1. **Documenting the ideal** - Not the actual process
2. **Too detailed** - Missing the big picture
3. **No metrics** - Cannot quantify improvement
4. **Skipping stakeholders** - Missing workarounds and exceptions
5. **Analysis paralysis** - Over-analyzing before improving

---

## Process Improvement Patterns

| Pattern | Description | Example |
|---------|-------------|---------|
| **Eliminate** | Remove unnecessary steps | Remove redundant approval |
| **Simplify** | Reduce complexity | Fewer form fields |
| **Automate** | Use technology | Auto-calculate totals |
| **Integrate** | Connect systems | Single data entry |
| **Parallelize** | Run steps concurrently | Review while processing |
| **Standardize** | Consistent approach | One way to do task |

---

## Next Steps

After process analysis:
1. Validate with process owners
2. Prioritize improvements
3. Design detailed future state
4. Identify system requirements
5. Connect to Data Analysis methodology

---

## References

- BA Framework Guide v3 - Requirements Analysis and Design Definition
- BA industry Business Process Analysis Guidelines
