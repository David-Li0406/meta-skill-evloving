---
name: claude-codex-gemini-consensus
description: |
  Comprehensive multi-AI consensus workflow for:
  1. CODE REVIEW - Clinical/technical review following SOP with TODO.md/IDEAS.md tracking
  2. ANALYSIS PLANNING - Statistical/bioinformatic analysis plans saved to analysis/plan.md
  3. ANALYSIS EXECUTION - Conduct analysis per plan with completeness verification
  4. REPORT GENERATION - Publication-ready reports (Methods/Results/Discussion) with figures, tables, PubMed citations
  
  Uses Claude Code CLI, OpenAI Codex CLI, and Google Gemini CLI. All work requires consensus between Claude, Codex, AND Gemini.
  Each agent can consult the other two for validation.
  
  Triggers: "code review", "clinical review", "consensus", "Claude", "Codex", "Gemini", "statistical analysis", "publication", "scientific analysis", "review SOP"
---

# Claude, Codex & Gemini Consensus Workflow

Multi-AI agent consensus system for critical code development and review. Each agent can invoke the other two for validation.

## How to Use This Skill

### Invocation Examples

**For Code Review (SOP-Based):**
```
Review my application using the code review SOP. Start with TODO.md setup.
```
```
Run clinical code review on this project. Follow the consensus SOP.
```
```
Review all modules in src/ using the review SOP. Track in TODO.md.
```

**For Simple Code Review (No SOP):**
```
Review my code in src/ using Codex and Gemini consensus.
```
```
Use consensus workflow to review this Python script critically.
```

**For Planning (Code/Features):**
```
Plan implementation of [feature] with Codex and Gemini consensus.
```
```
I need to build [X]. Create a plan and validate with Codex and Gemini.
```

**For Scientific Analysis Planning:**
```
Plan a statistical analysis for this clinical dataset. Use scientific consensus workflow.
Save the approved plan to analysis/plan.md for later execution.
```
```
Design analysis plan for [study type]. Include Codex/Gemini validation. This is for publication.
Output: analysis/plan.md
```

**For Conducting Analysis (After Plan Approved):**
```
Conduct the analysis according to analysis/plan.md. Validate each step with Codex and Gemini. 
Ensure all planned analyses are completed. Generate publication-ready report.
```
```
Execute the plan in analysis/plan.md. Check completeness - no missing or wrong analyses.
Create analysis/report.md with Methods, Results, Discussion.
```

**For Report Generation:**
```
Generate publication-ready report in analysis/report.md. Include figures, tables, PubMed citations.
Validate clinically and scientifically with Codex and Gemini.
```

### Workflow Modes

| Mode | Trigger Phrases | What Happens |
|------|-----------------|--------------|
| **Code Review (SOP)** | "code review SOP", "clinical review", "TODO.md" | Full SOP workflow with TODO.md/IDEAS.md tracking |
| **Code Review (Simple)** | "review code", "consensus review" | Submit to Codex & Gemini for critical review |
| **Plan Review** | "plan", "design", "architecture" | Draft plan → Codex review → Gemini review → Consensus |
| **Implementation** | "implement", "build", "create" | Implement → **Auto code review by all agents** → Approval |
| **Scientific Analysis** | "statistical analysis", "clinical research", "publication" | Full scientific workflow with completeness checks |
| **Analysis Execution** | "conduct analysis", "execute plan", "run analyses" | Implement + validate + check completeness |
| **Report Generation** | "report", "manuscript", "Methods/Results/Discussion" | Publication-ready output with citations |

> [!IMPORTANT]
> **Implementation workflows ALWAYS include automatic code review:**
> 1. Plan is validated by all agents
> 2. Primary agent executes implementation
> 3. **Remaining agents verify:** features correctly implemented + no regressions
> 4. Each remaining agent must confirm: "Implementation correct, no regressions"
> 5. Only complete when ALL remaining agents approve

### Complete Workflow Example (Scientific Analysis)

**Phase A: Planning (generates analysis/plan.md)**
```
USER: "I have clinical trial data with survival outcomes. 
      Plan a comprehensive analysis with Codex/Gemini consensus."

CLAUDE WILL:
1. [PLAN] Draft statistical analysis plan
2. [VALIDATE] Submit plan to Codex → Get feedback
3. [VALIDATE] Submit plan to Gemini → Get feedback  
4. [CONSENSUS] Synthesize feedback, argue disagreements, iterate until agreed
5. [SAVE] Write approved plan to analysis/plan.md
```

**Phase B: Execution (reads analysis/plan.md, generates report.md)**
```
USER: "Execute the plan in analysis/plan.md. Generate publication-ready report."

CLAUDE WILL:
1. [READ] Load plan from analysis/plan.md
2. [EXECUTE] Implement each analysis
3. [CODE REVIEW] Submit implementation to Codex + Gemini for review
4. [VALIDATE] Ensure all agents approve - no bugs, no regressions
5. [COMPLETENESS] Check: Are ALL planned analyses done? Missing? Incomplete? Wrong?
6. [CORRECT] Fix any issues, re-validate with all agents
7. [REPORT] Generate analysis/report.md (Methods, Results, Discussion)
8. [FIGURES] Create publication-ready figures with captions
9. [CITATIONS] Add and verify PubMed references
10. [FINAL] Clinical + Scientific assessment by all models
```

### What This Skill Does Automatically

- **Code review after implementation** - All agents verify code before completion
- **Consensus validation** - Plans require approval from Claude + Codex + Gemini
- **Regression checking** - Agents verify no new issues introduced

### Is This Comprehensive?

**YES, this skill provides end-to-end coverage:**

| Use Case | Covered | How |
|----------|---------|-----|
| **CODE REVIEW** | | |
| Clinical code review (SOP) | ✅ | TODO.md/IDEAS.md tracking, P0-P3 priorities |
| Module-by-module review | ✅ | Systematic workflow, don't stop until done |
| Security review | ✅ | P0: PII/PHI, injection, auth bypass |
| Clinical validity review | ✅ | P1: Calculations, units, data integrity |
| Usability review | ✅ | P2: Error handling, UX, performance |
| Fix verification | ✅ | Pal verifies fixes, checks for regressions |
| **SCIENTIFIC ANALYSIS** | | |
| Analysis planning | ✅ | Consensus plan → analysis/plan.md |
| Analysis execution | ✅ | Per-plan execution with validation |
| Completeness verification | ✅ | ✓/⚠/✗/❌ status tracking |
| Missing analysis detection | ✅ | Compare plan vs results |
| **REPORTING** | | |
| Publication-ready reports | ✅ | Methods/Results/Discussion in report.md |
| Figures with captions | ✅ | 300+ DPI, complete legends |
| Tables with footnotes | ✅ | Proper formatting, statistical notation |
| PubMed citations | ✅ | PMID verification |
| **VALIDATION** | | |
| Clinical assessment | ✅ | Actionable? Meaningful effect sizes? |
| Scientific assessment | ✅ | Methodology sound? Conclusions supported? |
| Validation tracking | ✅ | Internal status tracking (not in outputs) |
| Domain-specific hypotheses | ✅ | Examples provided (e.g., cancer type prediction) |

**Limitations:**
- Requires Codex CLI and Gemini CLI installed and authenticated
- Web search requires `--search` flag (Codex) or is built-in (Gemini)
- Large analyses may need multiple iterations

### Quick-Start Cheatsheet

```bash
# Code Review (SOP-based, comprehensive)
"Review my application using the code review SOP. Track in TODO.md."

# Code Review (simple)
"Review src/main.py with Codex and Gemini consensus"

# Plan something (saves to analysis/plan.md)
"Plan statistical analysis for [data]. Save to analysis/plan.md"

# Execute saved plan
"Execute the plan in analysis/plan.md. Generate report."

# Full scientific workflow
"Plan and conduct analysis for [data]. Generate publication-ready report."

# Just get Codex opinion
"Ask Codex to review this code: [paste code]"

# Just get Gemini opinion  
"Ask Gemini to review this plan: [paste plan]"
```

### analysis/plan.md Template

When planning, Claude generates this file for later execution:

```markdown
# Analysis Plan: [Study Title]

## Metadata
- **Created**: [date]
- **Status**: APPROVED / PENDING

## Objectives
1. Primary: [main research question]
2. Secondary: [additional questions]

## Data Description
- Source: [data source]
- Samples: [n=X]
- Variables: [list key variables]

## Planned Analyses

### 1. [Analysis Name]
- **Objective**: [what this answers]
- **Method**: [statistical test/approach]
- **Variables**: [input variables]
- **Expected output**: [tables, figures]
- **Status**: ☐ Not started

### 2. [Analysis Name]
- **Objective**: ...
- **Method**: ...
- **Status**: ☐ Not started

## Quality Control
- [ ] Data validation
- [ ] Missing data handling
- [ ] Outlier detection

## Review Notes
- [Feedback addressed]
- [Points of discussion]
```

## Core Principle

**All plans must be accepted by Claude, Codex, AND Gemini. All code must be reviewed by all three agents with critical evaluation. Do not accept findings blindly—argue and reach consensus.**

---

## CRITICAL: Preventing Infinite Consensus Loops

> [!CAUTION]
> **INFINITE LOOP PREVENTION** - This section is mandatory reading.
>
> When multiple AI agents have consensus skills installed, invoking each other for reviews can create infinite loops:
> - Claude calls Codex → Codex calls Claude → Claude calls Codex → ∞
>
> **The solution: ORCHESTRATOR vs REVIEWER mode.**

### Two Modes of Operation

| Mode | Role | Can Invoke Other Agents? | Can Read Files? | Can Web Search? |
|------|------|--------------------------|-----------------|-----------------|
| **ORCHESTRATOR** | Primary agent driving the task | ✅ YES | ✅ YES | ✅ YES |
| **REVIEWER** | Agent providing expert review | ❌ NO | ✅ YES | ✅ YES |

### ORCHESTRATOR Mode (Default when user initiates)

When the **user directly asks you** to review code, plan analysis, or run consensus:
- You ARE the orchestrator
- You MAY invoke other agents (Codex, Gemini, Claude) for reviews
- You synthesize feedback and make final decisions
- You drive the workflow to completion

### REVIEWER Mode (When invoked by another agent)

When **another AI agent invokes you via CLI**, you are a REVIEWER:
- You provide YOUR expert opinion only
- You MAY read files to understand context
- You MAY use web search to verify facts
- You **MUST NOT** invoke other agent CLIs (codex, claude, gemini)
- Your review is a "leaf node" - final, not the start of another consensus

### How to Detect You Are a REVIEWER

You are in REVIEWER mode if ANY of these are true:
1. Your prompt contains `REVIEWER_MODE` marker
2. Your prompt contains `DO NOT INVOKE OTHER AGENTS`
3. You were invoked via CLI with a specific review task (not a user conversation)
4. The prompt is clearly a single-shot review request (not interactive)

### REVIEWER Mode Constraints

When in REVIEWER mode, you **MUST**:

```
✅ ALLOWED:
- Read files (cat, Read tool, etc.)
- Search code (grep, Grep tool, etc.)
- Web search for verification and literature
- Run quick sanity checks (execute code to verify calculations)
- Run existing tests to validate implementations
- Provide detailed expert review
- Point out issues, bugs, security concerns
- Give APPROVED/NEEDS_CHANGES verdict

❌ FORBIDDEN:
- Invoke `codex exec ...` or `codex ...`
- Invoke `claude ...` or `claude -p ...`
- Invoke `gemini ...` or `gemini -p ...`
- Start your own consensus workflow
- Delegate review to other agents
- Create sub-reviews or nested consensus
```

**Key distinction:** Reviewers CAN execute code for verification (run tests, check calculations) but CANNOT invoke other AI agent CLIs.

### Why This Works

```
USER → ORCHESTRATOR (Claude)
         ├── REVIEWER (Codex) → Reviews, returns verdict, STOPS
         └── REVIEWER (Gemini) → Reviews, returns verdict, STOPS
       ← Synthesizes feedback, reaches conclusion
```

Each reviewer is a terminal node. No recursive invocations. Clean consensus.

---

## Cross-Agent Consultation

| You are running | Consult these agents | They operate in |
|-----------------|---------------------|-----------------|
| **Claude** (orchestrator) | Codex + Gemini | REVIEWER mode |
| **Codex** (orchestrator) | Claude + Gemini | REVIEWER mode |
| **Gemini** (orchestrator) | Claude + Codex | REVIEWER mode |

---

## Reviewer Tool Permissions

### What REVIEWERS Can Use

When in REVIEWER_MODE, agents have access to tools for **reading, searching, and verification**:

| Tool Category | Allowed Tools | Purpose |
|---------------|---------------|---------|
| **File Reading** | `cat`, `Read`, `head`, `tail` | Understand code context |
| **Code Search** | `grep`, `Grep`, `rg`, `find`, `Glob` | Find relevant code |
| **Web Search** | `--search` flag, web search tools | Verify facts, find literature |
| **Directory Listing** | `ls`, `tree` | Understand project structure |
| **Sanity Checks** | `python`, `Rscript`, test runners | Verify calculations, run tests |

### What REVIEWERS Cannot Use

REVIEWERS are **forbidden** from using:

| Forbidden | Why |
|-----------|-----|
| `codex exec ...`, `codex ...` | Would create recursive loop |
| `claude ...`, `claude -p ...` | Would create recursive loop |
| `gemini ...`, `gemini -p ...` | Would create recursive loop |
| File writes (`Write`, `Edit`, `>`, `>>`) | Reviewers observe, don't modify |
| `git commit`, `git push` | Reviewers don't make changes |

**Note:** Reviewers CAN run code for verification (sanity checks, tests) but CANNOT invoke other AI agents.

### Reviewer Prompt Template

Always include this header when invoking other agents:

```
REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS (claude, codex, gemini).
You MAY read files and web search to verify. Provide YOUR expert review only.
```

This 2-line header prevents infinite loops while allowing thorough reviews.

---

## Guaranteed REVIEWER_MODE: Wrapper Script

> [!TIP]
> **Use `scripts/review.sh` to GUARANTEE REVIEWER_MODE is always included.**
>
> The wrapper script automatically prepends REVIEWER_MODE to every prompt, eliminating human error.

### Usage

```bash
# Instead of manually adding REVIEWER_MODE to prompts:
./scripts/review.sh codex "Review this code for bugs"
./scripts/review.sh gemini "Validate this analysis plan"
./scripts/review.sh claude "Check for security issues"

# With options:
./scripts/review.sh codex "Search for best practices" --search
./scripts/review.sh codex "Review in context" --cd /path/to/project
```

### Why Use the Wrapper?

| Manual Prompts | Wrapper Script |
|----------------|----------------|
| Must remember to add REVIEWER_MODE | Automatic injection |
| Risk of forgetting | Guaranteed protection |
| Copy-paste errors | Consistent format |
| Verbose commands | Simple interface |

### How It Works

The script prepends this header to EVERY prompt:

```
REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS (claude, codex, gemini).
You MAY read files, web search, and run sanity checks. Provide YOUR expert review only.
```

This makes infinite loops **impossible** when using the wrapper.

---

## Best Practice: Subagent/Task-Based Reviews

> [!IMPORTANT]
> **Architectural Enforcement > Prompt-Based Enforcement**
>
> Instead of relying on REVIEWER_MODE prompts, spawn reviews as **subagents/tasks** with limited tool access. This provides hard enforcement at the system level.

### Why Subagents Are Better

| Approach | Enforcement | Loop Risk |
|----------|-------------|-----------|
| CLI with REVIEWER_MODE prompt | Soft (honor system) | Low if followed |
| Subagent with limited tools | **Hard (architectural)** | **Impossible** |

### Claude Code: Task Tool Pattern

When Claude is the orchestrator, use the **Task tool** to spawn reviewers:

```
Use the Task tool to spawn a review subagent:
- subagent_type: "Explore" or "general-purpose"
- The subagent has Read, Grep, Glob, WebSearch - but NO Bash for CLI invocations
- Natural termination: subagent completes task and returns
```

**Example prompt for Task tool:**

```
Review this code for bugs, security issues, and performance problems.

Code to review:
[PASTE CODE]

Provide output in this format:
- BUGS: [list or 'None']
- SECURITY: [list or 'None']
- PERFORMANCE: [list or 'None']
- VERDICT: APPROVED/NEEDS_CHANGES
```

### Why This Works

```
USER → ORCHESTRATOR (Claude with Task tool)
         ├── SUBAGENT (Explore) → Has Read/Search, NO Bash → Cannot invoke CLIs
         └── SUBAGENT (Explore) → Has Read/Search, NO Bash → Cannot invoke CLIs
       ← Results returned, synthesized
```

Subagents **physically cannot** invoke `codex`, `gemini`, or `claude` CLIs because they don't have Bash access.

### When to Use Each Approach

| Scenario | Recommended Approach |
|----------|---------------------|
| Claude orchestrating | **Task tool subagents** (architectural enforcement) |
| Codex orchestrating | CLI with REVIEWER_MODE + wrapper script |
| Gemini orchestrating | CLI with REVIEWER_MODE + wrapper script |
| Quick single review | `./scripts/review.sh` wrapper |
| Complex multi-file review | Task tool with Explore subagent |

### Hybrid Approach (Recommended)

For maximum safety, combine both:

1. **Claude orchestrates** using Task tool (spawns subagents without Bash)
2. **If CLI needed**, use `scripts/review.sh` wrapper (injects REVIEWER_MODE)
3. **Subagents** naturally terminate and return results

```bash
# From Claude orchestrator - spawn review subagent via Task tool
# Subagent gets: Read, Grep, Glob, WebSearch, WebFetch
# Subagent does NOT get: Bash (cannot invoke codex/gemini/claude CLIs)
```

This provides **defense in depth**: architectural limits + prompt-based instructions.

---

## Quick Reference

### Claude Code CLI (Full Permissions - Concise Output)

```bash
# Standard command with concise output request
claude --dangerously-skip-permissions \
  
  -p "BE CONCISE. Output only: findings, issues, recommendations. No preamble.

YOUR_PROMPT"

# JSON output for minimal, structured response
claude --dangerously-skip-permissions \
  --output-format json \
  -p "YOUR_PROMPT"
```

**Output Control:**
- Add `"BE CONCISE. No preamble. Bullet points only."` to prompts
- Use `--output-format json` for structured output
- Request specific format: `"Output as: ✓/✗ checklist only"`

### Codex CLI (Full Permissions - Concise Output)

```bash
# Standard command with concise output request
codex exec --dangerously-bypass-approvals-and-sandbox \
  \
  --skip-git-repo-check \
  --cd "$(pwd)" \
  "BE CONCISE. Output only: findings, issues, recommendations. No preamble.

YOUR_PROMPT"

# JSON output for minimal, structured response
codex exec --dangerously-bypass-approvals-and-sandbox \
  \
  --skip-git-repo-check \
  --json \
  "YOUR_PROMPT"

# With web search
codex exec --dangerously-bypass-approvals-and-sandbox \
  \
  --skip-git-repo-check \
  --search \
  "BE CONCISE. YOUR_PROMPT"
```

**Output Control:**
- Add `"BE CONCISE. No preamble. Bullet points only."` to prompts
- Use `--json` flag for structured output (parseable, minimal)
- Request specific format: `"Output as: ✓/✗ checklist only"`

### Gemini CLI (Full Auto - Concise Output)

```bash
# Standard with concise instruction
gemini --yolo \
  \
  -p "BE CONCISE. Bullet points only. No preamble.

YOUR_PROMPT"

# JSON output for scripting
gemini --yolo \
  \
  --output-format json \
  -p "YOUR_PROMPT"
```

## Reducing Output Verbosity

**Problem:** Codex/Gemini can produce verbose output that wastes context.

**Solution:** Always use structured output requests:

| Verbose Prompt | Concise Prompt |
|----------------|----------------|
| "Review this code and tell me what's wrong" | "BE CONCISE. Output: BUGS: [list] VERDICT: [pass/fail]" |
| "Is this plan good?" | "BE CONCISE. Output: ISSUES: [list or 'None'] VERDICT: APPROVED/REJECTED" |
| "Check completeness" | "BE CONCISE. Table only: \| # \| Item \| Status \|" |

**Concise Output Templates:**

```
# For reviews
"BE CONCISE. Output: ISSUES: [list] | VERDICT: [pass/fail]"

# For validation
"BE CONCISE. Output: ERRORS: [list or 'None'] | VALID: Y/N"

# For checklists
"BE CONCISE. Table only: | # | Item | ✓/✗ |"

# For recommendations
"BE CONCISE. Output: 1. [action] 2. [action] 3. [action]"
```

### Ultra-Concise Mode (Minimum Context)

For maximum context savings, use strict output limits:

```bash
# Codex with strict format
codex exec --dangerously-bypass-approvals-and-sandbox \
  \
  --skip-git-repo-check \
  "STRICT FORMAT. Max 10 lines. No prose.

[TASK]

Output ONLY:
✓/✗ [check1]
✓/✗ [check2]
VERDICT: [word]"

# Pipe to head for hard truncation (if output still verbose)
codex exec --dangerously-bypass-approvals-and-sandbox \
  \
  --skip-git-repo-check \
  "YOUR_PROMPT" | head -20
```

**Context-Saving Rules:**
1. Always use `"BE CONCISE."` prefix
2. Specify exact output format (bullets, table, one-liners)
3. Use `--json` when parsing programmatically
4. Pipe to `head -N` for hard limits
5. Request `"Max N lines"` in prompt

## Consensus Workflow

### Concise Output Instructions

**Always prepend to prompts:**
```
BE CONCISE. No preamble. Output format:
- ISSUES: [bullet list]
- RECOMMENDATIONS: [bullet list]  
- VERDICT: APPROVED / NEEDS CHANGES
```

### Phase 1: Planning

1. **Claude proposes** initial implementation plan
2. **Submit to Codex** for critical review:
   ```bash
   codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
     "REVIEWER_MODE. You are reviewing for consensus - DO NOT INVOKE OTHER AGENTS.
You MAY read files and web search. Provide YOUR expert review only.

BE CONCISE. No preamble. Review this plan. Output:
- ISSUES: [list]
- MISSING: [list]
- VERDICT: APPROVED/NEEDS CHANGES

Plan: [PASTE_PLAN]"
   ```
3. **Submit to Gemini** for independent review:
   ```bash
   gemini --yolo \
     -p "REVIEWER_MODE. You are reviewing for consensus - DO NOT INVOKE OTHER AGENTS.
You MAY read files and web search. Provide YOUR expert review only.

BE CONCISE. No preamble. Review this plan. Output:
- ISSUES: [list]
- MISSING: [list]
- VERDICT: APPROVED/NEEDS CHANGES

Plan: [PASTE_PLAN]"
   ```
4. **Synthesize feedback**, argue points of disagreement, reach consensus
5. **Iterate** until all three agents agree

### Phase 2: Implementation

1. Claude implements based on consensus plan
2. Code review cycle (see below)

### Phase 3: Code Review

Submit code to both agents for critical review:

```bash
# Codex review (concise) - REVIEWER_MODE prevents infinite loops
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS (claude, gemini).
You MAY read files and web search to verify. Provide YOUR expert review only.

BE CONCISE. Review code. Output only:
- BUGS: [list or 'None']
- SECURITY: [list or 'None']
- PERFORMANCE: [list or 'None']
- VERDICT: APPROVED/NEEDS CHANGES

Code: [PASTE_CODE]"

# Gemini review (concise) - REVIEWER_MODE prevents infinite loops
gemini --yolo \
  -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS (claude, codex).
You MAY read files and web search to verify. Provide YOUR expert review only.

BE CONCISE. Review code. Output only:
- BUGS: [list or 'None']
- SECURITY: [list or 'None']
- PERFORMANCE: [list or 'None']
- VERDICT: APPROVED/NEEDS CHANGES

Code: [PASTE_CODE]"
```

---

## Code Review SOP (Clinical/Application Review)

**Use this workflow when asked to review an application, run clinical code review, or follow the review SOP.**

**Reference:** See `references/code-review-sop.md` for full details.

### Core Principle

All changes require **consensus** between Claude and Pal (Codex/Gemini). Review systematically using TODO.md and IDEAS.md tracking.

### Priority Levels

| Level | Name | Examples |
|-------|------|----------|
| **P0** | Critical | Security vulnerabilities, PII/PHI leaks, data corruption, auth bypass |
| **P1** | High | Clinical validity issues, incorrect calculations, data integrity |
| **P2** | Medium | Usability issues, error handling gaps, performance concerns |
| **P3** | Low | Code style, documentation, minor optimizations |

### Required Files

**Create if missing:**

```markdown
# TODO.md
## Module Inventory
- [ ] [PENDING] module1.py
- [ ] [PENDING] module2.py

## Current Session
- **Active Module:** None
```

```markdown
# IDEAS.md
## Nice-to-Have Features
## Unresolved Discussions
```

### The Workflow Loop

**For each module (don't stop until all are [DONE]):**

#### 1. Analysis & Discussion

```bash
# Claude reviews independently for P0-P3 issues

# Pal reviews independently (concise) - REVIEWER_MODE
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Code review. Clinical context.

Output: P0: [list] | P1: [list] | P2: [list] | P3: [list]

Code: $(cat [MODULE])"
```

**Consensus:** Compare findings. For disagreements:
```bash
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS.

BE CONCISE. Is [ISSUE] valid? Output: Y/N | REASON"
```

#### 2. Implementation Strategy

```bash
# Validate fix plan - REVIEWER_MODE
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files to verify.

BE CONCISE. Validate fix plan.

Issues: [LIST]
Fixes: [LIST]

Output per fix: CORRECT/INCORRECT | [concern]"
```

#### 3. Execution & Verification

After implementing fixes, **ALL agents must verify** the fix is correct and there are no regressions:

```bash
# Claude reviews the fix first, then submits to other agents:

# Codex verification - REVIEWER_MODE
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check --search \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS (claude, gemini).
You MAY read files and web search. Provide YOUR expert verification only.

BE CONCISE. Verify these fixes are correct and no regressions introduced.

Issues fixed: [LIST]
Code changes: [DIFF or CODE]

Output:
| Issue | Fix Correct? | Regressions? |
VERDICT: APPROVED / NEEDS_CHANGES

Code: $(cat [MODULE])"

# Gemini verification (independent) - REVIEWER_MODE
gemini --yolo \
  -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS (claude, codex).
You MAY read files and web search. Provide YOUR expert verification only.

BE CONCISE. Verify fixes are correct. Check for regressions.

Issues fixed: [LIST]
Code: $(cat [MODULE])

Output: | Issue | Correct | Regression | VERDICT: APPROVED/REJECTED"

# Claude verification (if Codex/Gemini are primary) - REVIEWER_MODE
claude --dangerously-skip-permissions -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS (codex, gemini).
You MAY read files and web search. Provide YOUR expert verification only.

BE CONCISE. Verify fixes. No regressions?
Issues: [LIST]
Code: $(cat [MODULE])
Output: | Issue | Fixed | Regression | VERDICT: APPROVED/REJECTED"
```

> [!IMPORTANT]
> **Do NOT mark module as complete until ALL agents confirm:**
> 1. Each fix is correct
> 2. No regressions introduced
> 3. VERDICT is APPROVED from all agents

#### 4. Completion

1. Confirm **all agents approved** (Claude + Codex + Gemini)
2. Mark `[DONE]` in TODO.md
3. Log nice-to-haves to IDEAS.md
4. **Pick next [PENDING] module - DON'T STOP**

### Quick Commands

```bash
# Initial review
"BE CONCISE. P0-P3 review. Output: P0: | P1: | P2: | P3:"

# Disagreement
"BE CONCISE. Is [X] valid issue? Y/N | REASON"

# Fix validation
"BE CONCISE. Fix correct? CORRECT/INCORRECT | concern"

# Verification
"BE CONCISE. Fixes applied? FIXED/NOT_FIXED per issue"
```

---

## Scientific Analysis Workflow (On Request Only)

**Use this workflow ONLY when explicitly asked for scientific analysis, clinical research, or publication-ready reports.**

For clinical research projects requiring publication-ready outputs, follow this extended workflow.

### Full Analysis Workflow Summary

1. **Initial Analysis** → Data exploration, research question validation
2. **Analysis Plan** → Draft and validate with Codex/Gemini → Save to analysis/plan.md
3. **Execute Analysis** → Implement with validation at each step
4. **Completeness Check** → Verify ALL planned analyses done correctly (missing/incomplete/wrong)
5. **Conduct Corrections** → Implement missing, complete incomplete, fix wrong analyses
6. **Draft Report** → Create `analysis/report.md` with Methods, Results, Discussion
7. **Figures & Tables** → Publication-ready with complete captions (standalone scripts)
8. **Final Validation** → Clinical AND scientific assessment by all models
9. **Citations** → Verify all PubMed citations (PMIDs)

**See [references/scientific-analysis-workflow.md](references/scientific-analysis-workflow.md) for complete workflow.**

### Domain-Specific Hypothesis Example (Oncology)

For oncology research, you may want to add a cancer type hypothesis step:

```bash
# Example only - adapt to your domain - REVIEWER_MODE
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check --search \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY web search for PMIDs.

BE CONCISE. Hypothesize cancer type. Output:
1. [Type] - [confidence] - [evidence] - PMID:X
Data: [PASTE_DATA_SUMMARY]"
```

See `references/scientific-analysis-workflow.md` Appendix for more domain-specific examples.

### Report Structure (analysis/report.md)

```markdown
# [Study Title]

## Methods
- Study design, data sources, statistical methods
- Include software versions and AI consensus validation note

## Results  
- Primary/secondary outcomes with statistics
- Publication-ready figures (300+ DPI, captions)
- Publication-ready tables (with footnotes)

## Discussion
- Principal findings, comparison with literature
- Clinical implications, limitations, future directions

## References
- Vancouver style with PMIDs verified
```

### Clinical + Scientific Validation

```bash
# Clinical assessment (concise) - REVIEWER_MODE
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY web search for clinical references.

BE CONCISE. Clinical assessment.
OUTPUT: ACTIONABLE: Y/N | EFFECT SIZE: meaningful/marginal | GENERALIZABLE: Y/N | VERDICT: [pass/fail]
Report: [PASTE_REPORT]"

# Scientific assessment (concise) - REVIEWER_MODE
gemini --yolo \
  -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY web search for references.

BE CONCISE. Scientific assessment.
OUTPUT: METHODS: sound/flawed | CONCLUSIONS: supported/unsupported | NOVEL: Y/N | VERDICT: [pass/fail]
Report: [PASTE_REPORT]"
```

### Analysis Completeness Verification

**CRITICAL: Verify ALL planned analyses are completed correctly.**

```bash
# Check for missing/incomplete analyses (concise output) - REVIEWER_MODE
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Compare analysis/plan.md vs results.

OUTPUT (table only):
| # | Analysis | Status | Action |
STATUS: ✓=Done ⚠=Partial ✗=Missing ❌=Wrong"

# Gemini verification (concise) - REVIEWER_MODE
gemini --yolo \
  -p "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. Verify: analysis/plan.md vs results. Table only: | # | Analysis | Status |"
```

After verification, **conduct/correct** all flagged items, then re-validate.

### Additional Analyses Discovery

After completing planned analyses:

```bash
# REVIEWER_MODE - agent suggests but does not invoke others
codex exec --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check \
  "REVIEWER_MODE. DO NOT INVOKE OTHER AGENTS. You MAY read files.

BE CONCISE. What additional analyses needed?
OUTPUT: 1. [analysis] - [rationale]  2. [analysis] - [rationale]
Current: [PASTE_ANALYSIS]"
```

Document additions in `analysis/plan.md`, then implement.


## Detailed CLI References

For comprehensive command-line options:
- **Claude Code CLI**: See [references/claude-cli.md](references/claude-cli.md)
- **Codex CLI**: See [references/codex-cli.md](references/codex-cli.md)
- **Gemini CLI**: See [references/gemini-cli.md](references/gemini-cli.md)
- **Scientific Workflow**: See [references/scientific-analysis-workflow.md](references/scientific-analysis-workflow.md)
- **MCP Integration**: See [references/mcp-workflow.md](references/mcp-workflow.md)

## Environment Setup

### Prerequisites

```bash
# Install Claude Code CLI (macOS, Linux, WSL)
curl -fsSL https://claude.ai/install.sh | bash
# Or via Homebrew: brew install --cask claude-code

# Install Codex CLI
npm i -g @openai/codex

# Install Gemini CLI
npm i -g @google/gemini-cli

# Authenticate Claude (Claude subscription or API key)
claude  # Follow OAuth prompts
# Or: export ANTHROPIC_API_KEY="your-key"

# Authenticate Codex (ChatGPT OAuth or API key)
codex login
# Or: export OPENAI_API_KEY="your-key"

# Authenticate Gemini
export GEMINI_API_KEY="your-key"
# Or use Google account OAuth on first run
```

### Verification

```bash
# Verify Claude
claude --version

# Verify Codex
codex login status

# Verify Gemini
gemini --help
```

## Timeout Requirements

> [!IMPORTANT]
> CLI tools should be run with a timeout of **at least 30 minutes** per task. Complex analyses, code reviews, and consensus workflows may require extended execution time.

```bash
# Example with timeout command
timeout 30m codex exec --yolo "YOUR_TASK"
timeout 30m gemini --yolo -p "YOUR_TASK"
timeout 30m claude --dangerously-skip-permissions -p "YOUR_TASK"
```

## Recommended Configurations

### Codex Config (~/.codex/config.toml)

```toml
model = "gpt-5.2-codex"
approval_policy = "never"  # Full auto for consensus workflows
sandbox_mode = "danger-full-access"
web_search = true  # Always enable web search

[sandbox_workspace_write]
network_access = true
```

### Gemini Config (~/.gemini/settings.json)

```json
{
  "model": "gemini-3-pro-preview",
  "yolo": true,
  "theme": "dark",
  "output": {
    "format": "text"
  },
  "tools": {
    "enableToolOutputTruncation": false,
    "truncateToolOutputThreshold": -1
  }
}
```

> [!NOTE]
> - `output.format: "text"` ensures clean text output without JSON wrapper
> - `truncateToolOutputThreshold: -1` disables truncation
> - Gemini has built-in web search via `google_web_search` tool


## Critical Review Prompts (Concise Format)

### For Plan Review

```
BE CONCISE. No preamble. Review this plan.

OUTPUT FORMAT:
- ISSUES: [bullet list or 'None']
- MISSING: [bullet list or 'None']
- SECURITY: [concerns or 'None']
- VERDICT: APPROVED / NEEDS CHANGES

Plan:
[PASTE_PLAN]
```

### For Code Review

```
BE CONCISE. No preamble. Review this code.

OUTPUT FORMAT:
- BUGS: [list or 'None']
- EDGE CASES: [list or 'None']
- SECURITY: [list or 'None']
- PERFORMANCE: [list or 'None']
- VERDICT: APPROVED / NEEDS CHANGES

Code:
[PASTE_CODE]
```

### For Analysis Validation

```
BE CONCISE. No preamble. Validate this analysis.

OUTPUT FORMAT:
- STATISTICAL ERRORS: [list or 'None']
- MISSING CHECKS: [list or 'None']
- INTERPRETATION ISSUES: [list or 'None']
- VERDICT: VALID / INVALID

Analysis:
[PASTE_ANALYSIS]
```

### For Clinical Research (when applicable)

Add to prompts:
```
CONTEXT: Clinical research. Be rigorous.
```

## Session Management

### Codex Sessions

```bash
# Resume last session
codex resume --last

# Resume specific session
codex resume SESSION_ID

# List sessions
codex resume --all
```

### Gemini Sessions

```bash
# Resume latest session
gemini --resume latest

# Resume specific session
gemini --resume SESSION_UUID
```

## Troubleshooting

### Codex Issues

| Issue | Solution |
|-------|----------|
| "Not a git repository" | Add `--skip-git-repo-check` flag |
| Permission/sandbox errors | Use `--dangerously-bypass-approvals-and-sandbox` (or `--yolo`) |
| Network blocked | Already bypassed with `--yolo` flag |
| Auth loops | Run `codex logout` then `codex login` |

### Gemini Issues

| Issue | Solution |
|-------|----------|
| Tool confirmation spam | Use `--yolo` flag |
| Sandbox not working | Ensure Docker/Podman installed |
| Model not found | Check `--model` spelling |

## MCP Integration (Advanced)

Both tools support Model Context Protocol for extending capabilities:

```bash
# Codex MCP
codex mcp add myserver -- npx -y @my/mcp-server
codex mcp list

# Gemini MCP (in settings.json)
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

## Skill Contents

This skill includes:

| File | Purpose |
|------|---------|
| `SKILL.md` | Main instructions, quick reference, invocation guide |
| `references/code-review-sop.md` | **Full Code Review SOP** - TODO.md/IDEAS.md templates, P0-P3 priorities, workflow loop |
| `references/codex-cli.md` | Complete Codex CLI command reference |
| `references/gemini-cli.md` | Complete Gemini CLI command reference |
| `references/scientific-analysis-workflow.md` | Full scientific analysis workflow (750+ lines) |
| `references/mcp-workflow.md` | MCP integration patterns |
| `scripts/review.sh` | **GUARANTEED REVIEWER_MODE** - Wrapper that auto-injects REVIEWER_MODE |
| `scripts/consensus-review.sh` | Helper script for batch consensus reviews |

**Total coverage**: ~2500+ lines of instructions and references.

---

## Summary: What This Skill Does

| Task | Input | Output | Tracking |
|------|-------|--------|----------|
| **Code Review (SOP)** | Application code | Fixed code, verified | TODO.md, IDEAS.md |
| **Analysis Planning** | Data description | Approved plan | analysis/plan.md |
| **Analysis Execution** | plan.md | Results + validation | Status markers ✓/⚠/✗/❌ |
| **Report Generation** | Analysis results | Publication-ready report | analysis/report.md |

---

## IMPORTANT: Output Confidentiality

**Do NOT include in any output files (plan.md, report.md, etc.):**
- References to multi-AI consensus
- Mentions of Codex, Gemini, or Claude validation
- Descriptions of the AI review workflow
- "Consensus" terminology referring to model agreement

**This methodology is proprietary.** Generated documents should follow standard scientific manuscript style without revealing the validation process.

---

## Python Environment & Script Requirements

### Virtual Environment

**All Python analysis scripts MUST use `~/.venv`**

```bash
# Setup (run once)
python3 -m venv ~/.venv
source ~/.venv/bin/activate
pip install pandas numpy matplotlib seaborn scipy lifelines scikit-learn statsmodels openpyxl xlsxwriter

# Run scripts
~/.venv/bin/python your_script.py
```

### Standalone Figure/Table Scripts

**Every figure and table MUST have its own standalone script:**

```
analysis/scripts/figures/fig01_survival_curve.py  →  analysis/figures/fig01_survival_curve.png
analysis/scripts/tables/tab01_baseline.py         →  analysis/tables/tab01_baseline.csv
```

**Script requirements:**
- Header with description, input/output paths, USAGE
- Venv check at top (warn if not using ~/.venv)
- Configuration section with all modifiable parameters
- Multiple output formats (PNG+PDF / CSV+XLSX)
- 300+ DPI for publication quality
- Self-contained - can run independently
