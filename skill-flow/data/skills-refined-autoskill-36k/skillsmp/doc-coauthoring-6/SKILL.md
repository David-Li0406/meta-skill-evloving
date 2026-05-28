---
name: doc-coauthoring
description: Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs, or similar documentation tasks.
metadata:
  source: https://github.com/anthropics/skills/tree/main/skills/doc-coauthoring
---

# Doc Co-Authoring Workflow

This skill provides a structured workflow for guiding users through collaborative document creation. Act as an active guide, walking users through three stages: Context Gathering, Refinement & Structure, and Reader Testing.

## When to Offer This Workflow
Offer this workflow when the user wants to:
- Write new documentation from scratch
- Create a technical proposal or spec
- Draft a decision document (RFC/ADR)
- Rewrite existing documentation significantly

Do NOT use for:
- Tiny edits (typo fixes)
- Pure code generation tasks
- Unstructured brainstorming

---

## Stage 1: Context Gathering

**Goal:** Extract all necessary information from the user *before* writing a single word of the draft. Avoid "blank page syndrome" by conducting an interview.

### Initial Questions
Start by asking these core questions (adapt tone as needed):
1.  **Who is the audience?** (Developers, stakeholders, users?)
2.  **What is the goal?** (Persuade, inform, tutorial, reference?)
3.  **What is the scope?** (What's in/out?)

### Info Dumping
After the initial questions, encourage the user to "dump" information.
- "Tell me everything you know about this topic loosely."
- "Paste any relevant code snippets or existing notes."
- "Don't worry about structure yet, just get the ideas out."

**Agent Action:**
- actively listen and identify gaps.
- Ask follow-up questions to clarify vague points.
- Do NOT start drafting yet.

---

## Stage 2: Refinement & Structure

**Goal:** Turn the unstructured context into a solid outline, then a draft.

### Step 1: Clarifying Questions
If there are still gaps after the info dump, ask specific targeted questions to fill them.

### Step 2: Brainstorming (Optional)
If the user is unsure about the direction, offer to brainstorm angles or structures.

### Step 3: Curation
Propose an **Outline** based on the gathered info.
- organizing the "info dump" into logical sections.
- asking for approval on this structure before writing.

### Step 4: Gap Check
Ask: "Looking at this outline, is there anything missing? Or any section you're unsure about?"

### Step 5: Drafting
Once the outline is approved, write the First Draft.
- Use best practices for the specific document type (e.g., clear headers for specs, step-by-step for tutorials).
- Mark uncertainties with [TODO] or bold questions.

### Step 6: Iterative Refinement
Present the draft and ask for feedback.
- Iterate based on user feedback.
- Challenge the user if they suggest changes that hurt clarity or miss the goal (gently).

### Quality Checking
Before moving to the next stage, self-correct:
- Is the tone appropriate?
- Is the formatting consistent?
- Are complex terms explained?

### Near Completion
When the document feels "done" to the user, suggest moving to **Reader Testing**.

---

## Stage 3: Reader Testing

**Goal:** Verify the document actually works for a reader who doesn't have the context we just built.

### Testing Approach

**Method A: Sub-Agent (If Available)**
If a sub-agent tool is available, invoke it with just the document content and the question.

**Method B: Simulation (No Tools)**
"I will now attempt to answer these questions as a naive reader, strictly using only the information present in the document."

**Method C: User Testing**
Ask the user to:
1. Open a new chat session.
2. Paste the document.
3. Ask the 5-10 questions generated in Step 1.
4. Report back any confusion or missing info.

### Step 1: Predict Reader Questions
Announce intention to predict what questions readers might ask when trying to discover this document.

Generate 5-10 questions that readers would realistically ask.

### Step 2: Test
Execute one of the methods above (A, B, or C).

### Step 3: Run Additional Checks
Also check for:
- "What in this doc might be ambiguous or unclear to readers?"
- "What knowledge or context does this doc assume readers already have?"
- "Are there any internal contradictions or inconsistencies?"

### Step 4: Report and Fix
If issues found:
- Report specific issues/ambiguities.
- Indicate intention to fix these gaps.
- Loop back to Stage 2 (Refinement) for problematic sections.

---

## Final Review

Once Reader Testing is passed (no major confusion):
1.  Do a final polish (spelling, grammar, formatting).
2.  Hand off the final markdown artifact.
3.  Celebrate!

## Tips for Effective Guidance
- **Be Bossy (Politely):** Don't just wait for instructions. Guide the process. "Next, let's..."
- **Hold the Pen:** Don't ask the user to write. You write, they review.
- **Separate content from form:** Fix the ideas first, then polish the words.
