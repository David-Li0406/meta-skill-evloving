# Spec Delta: The Pain-Driven Invariant Process

> "New invariants come from real failures, not theoretical concerns."

Spec Delta is the feedback loop that evolves our design invariants based on actual production incidents. Every invariant in our system should trace back to a specific failure that caused real pain. This ensures our guardrails stay practical, enforceable, and valuable.

---

## Why "Only From Pain"?

Theoretical invariants tend to be:
- **Too broad**: Trying to prevent every possible failure leads to alert fatigue
- **Too vague**: "Systems should be reliable" isn't testable
- **Too numerous**: Death by a thousand checks, none of which feel important
- **Easily ignored**: If it didn't prevent real pain, why follow it?

Pain-driven invariants are:
- **Specific**: They prevent a known failure class
- **Testable**: We can prove they would have caught the original incident
- **Justified**: The story of why they exist makes them memorable
- **Respected**: Teams know these rules saved someone's weekend

---

## The Spec Delta Process

### 1. Incident Occurs
Something breaks. A postmortem happens. During the "prevention" discussion, someone identifies that an invariant could have prevented this.

### 2. Document the Failure
Use the `template.md` to capture:
- What exactly happened (timeline, impact, root cause)
- Why existing invariants didn't catch it
- What invariant would have prevented it

**Critical**: Be specific about the pain. Include dollar amounts, hours of downtime, number of users affected. This justification lives with the invariant forever.

### 3. Validate the Proposed Invariant
Before proposing a new invariant, prove it works:

1. **Retrospective Test**: Would this invariant have actually blocked the incident?
   - Reconstruct the pre-incident state
   - Run the proposed check
   - Confirm it would have failed

2. **False Positive Analysis**: Would it block legitimate changes?
   - Review last 30 days of deployments
   - Estimate how many would trigger this invariant
   - Design override mechanisms for legitimate cases

3. **Implementation Feasibility**: Can we actually enforce this?
   - Static analysis possible?
   - Runtime check required?
   - Cross-system integration needed?

### 4. Review and Approval
Spec Delta proposals require:
- **Author**: The person who experienced or analyzed the failure
- **Tech Lead**: Confirms the invariant is implementable and valuable
- **Platform Owner**: Approves the enforcement level (hard block vs. warning)

Review should happen within 1 week of proposal. Invariants lose urgency and context if they languish.

### 5. Implementation
Once approved:
1. Create the enforcement mechanism (linter rule, pre-commit hook, deployment check)
2. Add the invariant to the canonical invariant list
3. Update `stats.md` to track this invariant's effectiveness
4. Announce to affected teams with the "story" of why this invariant exists

---

## When to Add a New Invariant

**Good candidates for new invariants:**
- The failure was significant (>4 hours recovery, customer-visible, data loss)
- The root cause was systemic (could happen to any team)
- The check is automatable (can be enforced without human judgment)
- The invariant is specific (not "be more careful")

**Poor candidates for new invariants:**
- One-off human error that wouldn't recur
- Already covered by existing invariant (strengthen that one instead)
- Requires judgment call that can't be automated
- Would generate excessive false positives (>10% of legitimate changes blocked)

---

## When to Fix the Spec Instead

Not every incident needs a new invariant. Sometimes the right response is:

### Strengthen Existing Invariant
The invariant exists but wasn't specific enough. Example: INVARIANT-12 said "backups must exist" but didn't verify restoration was tested. Fix INVARIANT-12, don't create INVARIANT-47.

### Improve Tooling
The invariant is fine, but the tooling didn't surface violations clearly. Improve the error message or dashboard, don't add redundant checks.

### Training Issue
The team knew the rule but didn't understand why. Add the incident story to the invariant's documentation. Make the "why" more visceral.

### Process Gap
The failure wasn't about design invariants at all—it was about access control, change management, or communication. Create a process change, not an invariant.

---

## File Naming Convention

```
spec-delta/
├── README.md                           # This file
├── template.md                         # Template for new proposals
├── stats.md                            # ROI tracking for all invariants
├── YYYY-MM-DD-invariant-XX.md         # Approved spec deltas
└── drafts/                            # Work-in-progress proposals
    └── YYYY-MM-DD-draft-title.md
```

Date format: ISO 8601 (YYYY-MM-DD)
Invariant numbers: Sequential, assigned upon approval

---

## Escalation Path

**Disagreement on whether to add an invariant?**
1. Author and Tech Lead discuss, aim for consensus
2. If no consensus, Platform Owner decides
3. If Platform Owner is the author, escalate to VP Engineering

**Invariant causing too many false positives post-deployment?**
1. Track in `stats.md` under "False Positive Incidents"
2. If >3 false positives in 30 days, trigger re-review
3. Can demote from Hard Block to Soft Warning while refining

**Emergency override needed?**
1. Use the documented override mechanism
2. Create incident ticket linking the override
3. Review in next Spec Delta meeting whether the invariant needs refinement

---

## Meeting Cadence

**Weekly Spec Delta Review** (30 min)
- Review any new proposals
- Check stats on existing invariants
- Discuss any override incidents

**Monthly Invariant Audit** (60 min)
- Which invariants have caught real violations?
- Which invariants have never triggered? (Consider retiring)
- Any patterns suggesting new invariant categories?

---

## Success Metrics

A healthy Spec Delta process shows:
- **Invariant count grows slowly**: 2-5 new invariants per quarter, not 20
- **Each invariant has a story**: No orphan invariants without documented origin
- **Violations decrease over time**: Teams learn from invariants
- **Few false positives**: <5% of legitimate changes blocked
- **High catch rate**: When incidents occur, we ask "which invariant should have caught this?" and usually the answer is "none, this is genuinely novel"

---

## Getting Started

1. Read an example Spec Delta: `2026-01-20-invariant-44.md`
2. Copy `template.md` for your proposal
3. Fill in all sections—incomplete proposals won't be reviewed
4. Submit for review in #platform-guardrails

Remember: The goal isn't to have the most invariants. It's to have the right invariants—each one earned through real pain, each one preventing future suffering.
