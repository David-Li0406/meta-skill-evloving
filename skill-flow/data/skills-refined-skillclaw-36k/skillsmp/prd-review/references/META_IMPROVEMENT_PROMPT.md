# Meta-Review Protocol: Elevating the PRD Review Skill

**To the Reviewing Agent:**
You are an Expert Methodologist and Systems Architect. Your objective is not to review a PRD, but to review the **PRD Review Skill itself**. Your goal is to elevate this process from "Rigorous" to "Generative" and "Anti-Fragile," ensuring it serves the Holonic axioms effectively without devolving into bureaucracy.

## 1. Required Reading (Context Load)

Before beginning the analysis, ingest the following context to understand the system's "Physics" and "Constitution":

1.  **The Constitution:**
    *   `documents/skills/holonic-agent-network/references/principia-holonic.md` (Axioms of Existence, Truth, and Economy)
    *   `documents/skills/holonic-agent-network/references/agent-native-software.md` (Architectural Doctrine)

2.  **The Target System (The Skill):**
    *   `documents/skills/prd-review/SKILL.md` (The Protocol)
    *   `documents/skills/prd-review/references/REVIEW_RUBRIC.md` (The Gates)
    *   `documents/skills/prd-review/references/ANGLE_PROMPTS.md` (The Reasoning Lenses)
    *   `documents/skills/prd-review/references/FINDING_CATEGORIES.md` (The Taxonomy)
    *   `documents/skills/prd-review/references/FEEDBACK_LOOPS.md` (The Self-Correction Mechanism)

## 2. The Analysis Matrix

Perform your audit by applying the following four high-order reasoning modes to the process.

### Mode A: Epistemic Depth Audit (Truth-Seeking)
*Critique the cognitive load of the Angle Prompts.*
*   **Question:** Do the prompts in `ANGLE_PROMPTS.md` force the agent to *reason*, or just *pattern-match*?
*   **Test:** Select 3 prompts. Can they be satisfied by a "lazy" LLM providing generic text? If yes, the prompt is defective.
*   **Goal:** Refine prompts to require **Evidence-Based Inference**. (e.g., instead of "Is it feasible?", ask "Identify the constraint that creates the tightest bound on performance.")

### Mode B: System Dynamics Analysis (Process Physics)
*Critique the flow of the review process.*
*   **Question:** Does this process create negative feedback loops (Compliance Theater)?
*   **Check:** Look at `GATE-PRD-CONTENT`. Is the rigorous 8-angle requirement likely to cause "Alert Fatigue" or "Rubber Stamping"?
*   **Goal:** Identify where we can apply **Sampling** or **Heuristic Pruning** instead of exhaustive checking for every PRD, while maintaining safety.

### Mode C: Tradeoff Analysis (Optimization)
*Critique the balance of Rigor vs. Velocity.*
*   **Question:** What is the cost of this review process in terms of Token Budget and Latency?
*   **Check:** Is the `BLOCKER` severity threshold calibrated correctly? Are we blocking on style (INFO/MINOR) disguised as quality?
*   **Goal:** Propose a "Fast Path" vs. "Deep Path" logic based on PRD risk profile.

### Mode D: Axiomatic Alignment (Constitutional Check)
*Critique the alignment with `Principia Holonica`.*
*   **Question:** Does this skill respect the **Lease Constraint** (waste is sin) and **Janus Dualism** (autonomy vs. integration)?
*   **Check:** Does the skill encourage the production of **Artifacts** (truth) over Narrative (noise)?
*   **Goal:** Ensure the output of a review is a durable, machine-readable asset (`EvidenceBundle`), not just a chat log.

## 3. Execution Steps

1.  **Diagnostic Pass:** Read the files. List 3 specific areas where the current prompts or rubrics are "shallow" (susceptible to hallucination or laziness).
2.  **Structural Critique:** Identify one feedback loop in `FEEDBACK_LOOPS.md` that is theoretical but likely broken in practice. Explain why.
3.  **Optimization Proposal:** Propose a modification to `SKILL.md` that allows high-trust authors or low-risk changes to bypass the heaviest gates without compromising the ledger.
4.  **Prompt Engineering:** Rewrite the `TRADEOFF_ANALYSIS` and `SYSTEM_DYNAMICS` prompts in `ANGLE_PROMPTS.md` to be even more biting and specific.

## 4. Output Format

Produce your report as a markdown document titled `documents/reviews/SKILL_IMPROVEMENT_PLAN.md` with the following sections:

1.  **Epistemic Vulnerabilities:** Where the agent can be "tricked" or "lazy."
2.  **Process Bottlenecks:** Where the system creates friction without value.
3.  **Proposed Amendments:**
    *   Diff for `ANGLE_PROMPTS.md`
    *   Diff for `SKILL.md` (Process logic)
4.  **The "Anti-Fragile" Vision:** A paragraph describing how this skill gets stronger the more it is used.
