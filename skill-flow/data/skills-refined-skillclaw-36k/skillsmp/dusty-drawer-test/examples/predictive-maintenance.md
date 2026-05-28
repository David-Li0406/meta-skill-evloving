# Example: Predictive Maintenance Model

*A sample application of the dusty drawer test*

---

## Project Proposal

> Develop a machine learning model that predicts equipment failures in manufacturing settings using sensor data. The model would identify patterns preceding failures, enabling maintenance teams to intervene before breakdowns occur.

---

## Evaluation

### Impact Potential

#### 1. Who? (Carrier)

**Score: 1**

The proposal identifies "manufacturing companies" and "maintenance teams" as beneficiaries. But who will *carry* this work forward?

- End beneficiaries: Maintenance technicians, plant managers
- But who takes the model and deploys it? 

The proposal doesn't identify a specific carrier. Options might include:
- A specific manufacturing partner who has agreed to pilot
- A maintenance software vendor who would integrate the model
- An internal team at a specific company

Without a named carrier, this is a "build it and they will come" proposition. The proposer would need to either:
- Establish a relationship with a specific pilot partner before starting
- Target a software vendor who already has distribution to manufacturing

**Gap acknowledged:** Can describe end beneficiaries but cannot name the specific person or organization who will take the model output and deploy it.

---

#### 2. What change? (Indirection)

**Score: 1**

The claimed change: "maintenance teams intervene before breakdowns."

Counting indirection:
1. Proposer builds model
2. Someone must integrate model into existing maintenance workflows
3. Someone must train maintenance staff on the new system
4. Maintenance staff must trust and act on predictions
5. Interventions must actually prevent failures

This is 4 steps removed from the proposer's direct output. Each step can fail:
- Integration might not happen (no carrier identified)
- Staff might not trust ML predictions
- Predictions might not be actionable in practice

The change is concrete in principle (preventive maintenance instead of reactive) but the path is long.

**Honest assessment:** The proposer controls building the model. Everything else depends on others.

---

#### 3. Causal path?

**Score: 1**

Assumptions in the chain:
1. Sensor data contains predictive signal → *testable with historical data*
2. Model can learn this signal → *testable*
3. Someone will deploy the model → *unvalidated, no carrier identified*
4. Predictions will be timely enough to act on → *assumption*
5. Maintenance teams will change behavior based on predictions → *assumption*
6. Changed behavior will prevent failures → *plausible but unvalidated*

The first two links are testable. The rest are assumptions. Link 3 (deployment) is the weakest: without a carrier, the chain breaks regardless of model quality.

---

#### 4. Fit?

**Score: 1**

Partial fit:
- ML expertise: yes
- Manufacturing domain knowledge: unclear
- Access to sensor data: would need partner
- Relationships with potential deployers: not mentioned

The proposer could build a good model but has no apparent advantage in getting it deployed. Others with manufacturing relationships might be better positioned.

---

#### 5. Values?

**Score: 2**

Clear positive value:
- Reduced unplanned downtime (economic benefit)
- Safer operations (fewer emergency repairs)
- Less waste (parts replaced at right time, not too early or too late)

Short path from output to benefit, assuming deployment happens.

---

### Sustainability

#### 6. Feedback?

**Score: 1**

- Model accuracy: testable in weeks against historical data
- Deployment success: months to years (depends on finding partner)
- Actual failure prevention: only measurable after deployment and operation

Intermediate checkpoints exist for model development. But the real test (does it prevent failures?) has a long feedback loop.

---

#### 7. Control?

**Score: 1**

Controllable:
- Building the model
- Validating against historical data
- Publishing methodology
- Learning from the project

Requires others:
- Finding a deployment partner
- Integration into production systems
- Adoption by maintenance teams
- Actual operational use

Can ship a working model. But value requires adoption.

---

## Summary

| Criterion | Score |
|-----------|-------|
| Who (carrier) | 1 |
| What change (indirection) | 1 |
| Causal path | 1 |
| Fit | 1 |
| Values | 2 |
| Feedback | 1 |
| Control | 1 |
| **Total** | **8/14** |

---

## Classification

**Pull type:** Pushed

No one has asked for this. The proposer believes it would be valuable and hopes someone will adopt it. High dusty-drawer risk.

**Ladder ceiling:** Level 2-3 (Shipped → Attention)

Without a carrier, the realistic ceiling is publishing the model/paper. Reaching "behavior change" requires deployment, which depends entirely on others.

---

## Strengths

1. **Clear value proposition** if deployed: preventing equipment failures has obvious economic and safety benefits
2. **Testable early stages**: model development provides intermediate feedback
3. **Learning value**: proposer will build ML skills regardless of adoption

---

## Weaknesses and Risks

1. **No carrier identified**: The biggest gap. Who will take this model and deploy it? Without an answer, this is likely to end up as a paper or GitHub repo that nobody uses.
2. **Long indirection chain**: Four steps between output and claimed change. Each step depends on someone else.
3. **No deployment advantage**: Technical skill in ML doesn't translate to ability to get models deployed in manufacturing settings.

---

## Recommendations

**Reconsider framing** before proceeding.

To strengthen:
- Find a specific manufacturing partner *before* building the model. Even a letter of intent transforms this from "pushed" to "pulled."
- Alternatively, partner with a maintenance software vendor who already has distribution. They become the carrier.
- Narrow scope: instead of "manufacturing," pick one specific equipment type where you have access and relationships.

If no carrier can be identified:
- Be honest that this is a capability-building project, not an impact project. The main output is your own learning. That's valid, but don't pretend it will change maintenance practices.

**The core problem:** This is a solution looking for a deployment path. Reverse it: find someone with a deployment path looking for a solution.
