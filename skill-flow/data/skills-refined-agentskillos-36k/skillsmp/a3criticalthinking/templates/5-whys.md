# 5 Whys Analysis Worksheet

**Problem:** [State the problem clearly]
**Date:** [YYYY-MM-DD]
**Analyst:** [Name]

---

## Priority Check First

Before analyzing, verify:
- [ ] **SAFETY:** Is this a safety issue? If YES → escalate immediately
- [ ] **QUALITY:** Does this affect customer? If YES → containment required
- [ ] **COST:** Is this efficiency only? Safe to analyze normally

---

## The Problem Statement

**What happened?**
[Describe the specific event or condition - facts only, no assumptions]

**When did it happen?**
[Date/time/shift]

**Where did it happen?**
[Location, machine, workstation]

**How often does it happen?**
[Frequency, pattern]

---

## 5 Whys Analysis

### Chain 1 (Primary)

| Level | Why? | Answer | Evidence |
|-------|------|--------|----------|
| **1** | Why did [problem] occur? | | |
| **2** | Why did [answer 1] occur? | | |
| **3** | Why did [answer 2] occur? | | |
| **4** | Why did [answer 3] occur? | | |
| **5** | Why did [answer 4] occur? | | |

**Root Cause 1:** [State root cause]

---

### Chain 2 (If problem has multiple branches)

| Level | Why? | Answer | Evidence |
|-------|------|--------|----------|
| **1** | Why did [alternate factor] occur? | | |
| **2** | Why did [answer 1] occur? | | |
| **3** | Why did [answer 2] occur? | | |
| **4** | Why did [answer 3] occur? | | |
| **5** | Why did [answer 4] occur? | | |

**Root Cause 2:** [State root cause]

---

## Verification Checklist

For each root cause identified:

- [ ] Is it based on fact, not assumption?
- [ ] Have you observed it directly (genchi genbutsu)?
- [ ] Is there data to support it?
- [ ] Is it something you can control?
- [ ] If you fix this, will the problem be prevented?

---

## Rules for Good 5 Whys

1. **Stay factual** - Each answer must be verified, not guessed
2. **One cause per branch** - If multiple factors, start new chain
3. **Don't blame people** - Look for system/process failures
4. **Stop at controllable root** - When you can take action
5. **May need <5 or >5** - "5" is a guideline, not a rule

---

## Common Pitfalls

| Bad Practice | Better Approach |
|--------------|-----------------|
| "Operator error" | "Why did the system allow the error?" |
| "They didn't follow the procedure" | "Why was the procedure not followed?" |
| Stopping at symptoms | Keep asking until you reach the system |
| Assuming without verification | Go see, verify with data |

---

## Example

**Problem:** Customer received wrong part

| Level | Why? | Answer |
|-------|------|--------|
| 1 | Why wrong part shipped? | Wrong part picked from shelf |
| 2 | Why wrong part picked? | Parts looked similar, wrong bin |
| 3 | Why in wrong bin? | Bins not clearly labeled |
| 4 | Why not labeled? | Labels faded, no refresh schedule |
| 5 | Why no schedule? | No visual management standard |

**Root Cause:** Missing visual management standard for bin labeling

**Countermeasure:** Implement monthly label inspection checklist

---

## Next Steps

1. Document root cause(s) in A3 Section 4
2. Develop countermeasures following priority hierarchy
3. Verify fix is effective
4. Deploy horizontally to similar processes
