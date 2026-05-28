---
name: audit-paper
description: Rigorously audit scientific papers from arXiv or PDF. Runs 5-agent pipeline with adversarial review, mathematical verification, and code execution. Use when asked to review, audit, or analyze an academic paper.
---

# Paper Auditing Pipeline

## Overview

You are orchestrating a rigorous 5-agent pipeline to audit a scientific/technical paper. Your goal is to produce a comprehensive, adversarial review that catches issues before publication.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 "Audit this paper"                           │
│              (YOU - Main Orchestrator)                       │
└──────────────────────────┬──────────────────────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Agent A: Deconstructor                          │
│   Input: arXiv ID or PDF path                                │
│   Output: Structured claim extraction (JSON)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Agent B    │    │  Agent C    │    │  Agent D    │
│  Formalist  │    │  SKEPTIC    │    │  Verifier   │
│  Math Audit │    │  ADVERSARY  │    │  Code Exec  │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │
       └──────────────────┼──────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│              Agent E: Editor-in-Chief                        │
│   Synthesizes all reports → Final Decision Memo              │
└─────────────────────────────────────────────────────────────┘
```

## Input Parsing

Parse the user's input to determine the paper source:

**arXiv ID formats:**
- `arXiv:2512.15605`
- `2512.15605`
- `https://arxiv.org/abs/2512.15605`

**Local PDF:**
- `./path/to/paper.pdf`
- `/absolute/path/to/paper.pdf`

```python
def parse_input(arg):
    # arXiv patterns
    arxiv_patterns = [
        r'arXiv:(\d{4}\.\d{4,5})',
        r'^(\d{4}\.\d{4,5})$',
        r'arxiv\.org/abs/(\d{4}\.\d{4,5})'
    ]

    for pattern in arxiv_patterns:
        match = re.search(pattern, arg)
        if match:
            return {'type': 'arxiv', 'id': match.group(1)}

    # Local PDF
    if arg.endswith('.pdf'):
        return {'type': 'pdf', 'path': arg}

    raise ValueError(f"Cannot parse input: {arg}")
```

## Execution Flow

### Phase 1: Paper Acquisition

**For arXiv papers:**
```bash
# Create output directory
mkdir -p output/{paper_id}

# Fetch paper metadata and PDF using arxiv API or web fetch
```

Use WebFetch to get the paper from arXiv:
- Abstract page: `https://arxiv.org/abs/{paper_id}`
- PDF: `https://arxiv.org/pdf/{paper_id}.pdf`

**For local PDFs:**
- Verify file exists
- Extract paper ID from filename or generate one
- Copy to output directory

### Phase 2: Agent A - Deconstruction

Run Agent A to extract structured claims:

```
Invoke skill: paper-audit:agent-a-deconstructor

Input: The paper content (PDF text or arXiv data)
Output: output/{paper_id}/deconstruction.json
```

**Agent A deliverables:**
- [ ] `deconstruction.json` with all claim categories
- [ ] Identified: theoretical_claims, empirical_claims, comparative_claims, novelty_claims
- [ ] Reproducibility artifacts catalogued

### Phase 3: Parallel Agent Execution (B, C, D)

**IMPORTANT:** Agents B, C, and D can run in PARALLEL since they all depend only on Agent A's output.

Launch these agents concurrently using the Task tool:

#### Agent B: Formalist (Math Audit)
```
Invoke skill: paper-audit:agent-b-formalist
Condition: Only if deconstruction.json has non-empty theoretical_claims
Output: output/{paper_id}/math_audit.md
```

#### Agent C: Skeptic (Adversarial Review)
```
Invoke skill: paper-audit:agent-c-skeptic
CRITICAL: This is the core adversarial agent - ensure maximum skepticism
Output:
  - output/{paper_id}/adversarial_review.md
  - output/{paper_id}/contradicting_papers.md
```

**Agent C MUST:**
- [ ] Execute web searches for contradicting papers
- [ ] Generate 15+ adversarial questions with severity scores
- [ ] Cover all 8 attack vectors
- [ ] Calculate rebuttal difficulty score

#### Agent D: Verifier (Code Execution)
```
Invoke skill: paper-audit:agent-d-verifier
Output:
  - output/{paper_id}/verification/main.py
  - output/{paper_id}/verification/results.json
  - output/{paper_id}/verification/execution_log.txt
  - output/{paper_id}/verification/plots/
```

**Agent D MUST:**
- [ ] Generate verification code for verifiable claims
- [ ] Execute code (with timeout and error handling)
- [ ] Attempt self-healing if code fails
- [ ] Save scripts for user modification

### Phase 4: Agent E - Synthesis

After all parallel agents complete:

```
Invoke skill: paper-audit:agent-e-editor
Input: All outputs from Agents A, B, C, D
Output:
  - output/{paper_id}/decision_memo.md
  - output/{paper_id}/FULL_RESEARCH_PROPOSAL.md
  - output/{paper_id}/exploration_notebook.ipynb
  - output/{paper_id}/literature_gaps.md
```

### Phase 5: Create README Index

**IMPORTANT:** After all agents complete, create a `README.md` in the output directory to help users navigate the generated files. Users may be confused by the number of files generated.

Create `output/{paper_id}/README.md` with this structure:

```markdown
# Paper Audit: {paper_title}
**arXiv:** {paper_id} | **Date:** {date} | **Decision:** {ACCEPT/MAJOR REVISION/REJECT}

## Quick Start - What to Read

| Priority | File | Description |
|----------|------|-------------|
| 1️⃣ | `decision_memo.md` | **START HERE** - Final editorial decision with score breakdown |
| 2️⃣ | `adversarial_review.md` | Critical issues and adversarial questions |
| 3️⃣ | `math_audit.md` | Mathematical rigor analysis |

## All Generated Files

### Core Reports
- `decision_memo.md` - Final editorial decision (read first)
- `adversarial_review.md` - Skeptical analysis with 15+ adversarial questions
- `math_audit.md` - Mathematical rigor and calculation verification
- `contradicting_papers.md` - Prior art and conflicting research

### Research Outputs
- `FULL_RESEARCH_PROPOSAL.md` - Future research directions based on gaps found
- `literature_gaps.md` - Identified gaps in the literature
- `exploration_notebook.ipynb` - Interactive Jupyter notebook for exploration

### Data & Verification
- `deconstruction.json` - Structured extraction of all paper claims
- `verification/` - Code verification artifacts
  - `main.py` - Verification scripts
  - `results.json` - Verification results
  - `plots/` - Generated visualizations

## Score Summary
- **Final Score:** {score}/10
- **Decision:** {decision}
- **Rebuttal Difficulty:** {difficulty}/10
```

### Phase 6: Final Report

Display the final summary to the user and **direct them to README.md**:

```
═══════════════════════════════════════════════════════════════
                    AUDIT COMPLETE: {paper_id}
═══════════════════════════════════════════════════════════════
  Paper: {title}
  Authors: {authors}

  DECISION: {ACCEPT/MAJOR REVISION/REJECT}

  Score Breakdown:
  ├─ Agent B (Math):     {score}/10 (weight: 30%)
  ├─ Agent C (Skeptic):  {score}/10 (weight: 40%)
  └─ Agent D (Verifier): {score}/10 (weight: 30%)
  ────────────────────────────────────
  FINAL SCORE: {weighted_total}/10

  Agent C Verdict: {SUSPICIOUS/QUESTIONABLE/DEFENSIBLE/ROBUST}
  Rebuttal Difficulty: {score}/10

  Verification Status: {X}/{Y} claims verified

  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📂 START HERE: output/{paper_id}/README.md

  The README provides a guided reading order for all generated
  files based on your goals (quick summary, deep dive, research).
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
═══════════════════════════════════════════════════════════════
```

**IMPORTANT:** Always end by pointing users to `README.md` as their entry point.

## Progress Reporting

As orchestrator, report progress at each phase:

```
[paper-audit] Starting audit of {paper_id}...

[Phase 1] Fetching paper...
  ✓ Paper downloaded: {title}
  ✓ Output directory: output/{paper_id}/

[Phase 2] Agent A: Deconstructing paper...
  ✓ Found {N} theoretical claims
  ✓ Found {N} empirical claims
  ✓ Found {N} comparative claims
  ✓ Found {N} novelty claims
  ✓ Saved: deconstruction.json

[Phase 3] Running parallel agents...
  [Agent B] Auditing mathematical rigor...
  [Agent C] Launching adversarial review...
  [Agent C] Searching for contradicting papers...
  [Agent D] Generating verification code...
  [Agent D] Executing verification...

  ✓ Agent B complete: {SOUND/QUESTIONABLE/N/A}
  ✓ Agent C complete: {verdict}, {N} questions generated
  ✓ Agent D complete: {X}/{Y} claims verified

[Phase 4] Agent E: Synthesizing reports...
  ✓ Decision memo generated
  ✓ Research proposal generated
  ✓ Exploration notebook generated

[Phase 5] Creating README index...
  ✓ README.md generated with reading guide

[Phase 6] Audit complete!
  📂 Start here: output/{paper_id}/README.md
```

## Error Handling

### Paper Not Found
```
ERROR: Could not fetch paper {paper_id}
- Check if the arXiv ID is correct
- Check if the PDF path exists
- Try alternative format: arXiv:XXXX.XXXXX
```

### Agent Failure
```
WARNING: Agent {X} failed with error: {error}
- Continuing with partial results
- {Agent} output will be marked as UNAVAILABLE
- Final score adjusted accordingly
```

### Verification Code Failure
```
WARNING: Verification code failed after 3 self-healing attempts
- Manual intervention may be required
- See execution_log.txt for details
- Saved failing code for debugging
```

## Configuration

### Timeouts
- Paper fetch: 60 seconds
- Agent A: 5 minutes
- Agent B: 5 minutes
- Agent C: 10 minutes (includes web search)
- Agent D: 10 minutes (includes code execution)
- Agent E: 5 minutes

### Verification Sandbox
- Prefer Docker if available
- Fallback to local subprocess with timeout
- Max execution time per script: 5 minutes

## Checklist for Orchestrator

Before starting:
- [ ] Input parsed correctly (arXiv ID or PDF path)
- [ ] Output directory created

After Agent A:
- [ ] deconstruction.json exists and is valid JSON
- [ ] All claim categories populated (may be empty arrays)

After parallel agents:
- [ ] Agent B output exists (or marked N/A)
- [ ] Agent C adversarial_review.md exists
- [ ] Agent C contradicting_papers.md exists
- [ ] Agent D verification directory exists
- [ ] Agent D results.json exists

After Agent E:
- [ ] decision_memo.md is complete
- [ ] FULL_RESEARCH_PROPOSAL.md is complete
- [ ] exploration_notebook.ipynb is valid
- [ ] literature_gaps.md is complete

After README creation:
- [ ] README.md exists in output/{paper_id}/
- [ ] README includes priority reading order
- [ ] README lists all generated files with descriptions
- [ ] README shows score summary

Final:
- [ ] Summary displayed to user
- [ ] **User directed to README.md as entry point**
- [ ] All artifact paths reported
- [ ] Any errors/warnings surfaced

## Example Invocation

```
User: Audit this paper: arXiv:2512.15605