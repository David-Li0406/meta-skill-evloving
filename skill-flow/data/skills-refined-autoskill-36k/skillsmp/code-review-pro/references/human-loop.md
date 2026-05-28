# Human-in-the-Loop Review Workflows

## The Efficiency Spectrum
- **Low-Level (AI)**: Syntax, simple logic, security scanners, performance benchmarks.
- **High-Level (Human)**: Architectural soundness, business intent, developer experience (DX).

---

### 1. The "First Pass" Protocol
AI performs the first pass of every review. It flags the "Noise" so the human reviewer can focus on the "Signal."
- **Output**: An AI comment that summarizes the technical health of the PR.

### 2. Guided Code Reviews
The AI provides "Context Snippets" to the human reviewer.
- *Example*: "This function replaces `oldFunc`. Note that `oldFunc` was also used in 3 other places. Are we sure we want to delete it?"

### 3. Conflict Resolution
If the AI and human disagree:
- **Rule**: Human judgment always wins for architecture and business logic.
- **Rule**: AI judgment usually wins for security and performance benchmarks (if backed by data).

### 4. Continuous Learning
The AI reviews the *Human's* comments.
- **Feedback Loop**: If a human consistently adds a comment that the AI missed, the AI should update its local "Review Guidelines" to include that check.
