# All Plan (Codex Version)

Collaborative planning with all mounted CLIs (Codex, Claude, Gemini, OpenCode) for comprehensive solution design. Codex serves as the primary coordinator.

**Usage**: For complex features or architectural decisions requiring diverse perspectives.

---

## Input Parameters

From `$ARGUMENTS`:
- `requirement`: User's initial requirement or feature request
- `context`: Optional project context or constraints

---

## Execution Flow

### Phase 1: Requirement Refinement & Project Analysis

**1.1 Structured Clarification (Option-Based)**

Use the **5-Dimension Planning Readiness Model** to ensure comprehensive requirement capture.

#### Readiness Dimensions (100 pts total)

| Dimension | Weight | Focus | Priority |
|-----------|--------|-------|----------|
| Problem Clarity | 30pts | What problem? Why solve it? | 1 |
| Functional Scope | 25pts | What does it DO? Key features | 2 |
| Success Criteria | 20pts | How to verify done? | 3 |
| Constraints | 15pts | Time, resources, compatibility | 4 |
| Priority/MVP | 10pts | What first? Phased delivery? | 5 |

#### Clarification Flow

```
ROUND 1:
  1. Parse initial requirement
  2. Identify 2 lowest-confidence dimensions (use Priority order for ties)
  3. Present 2 questions with options (1 per dimension)
  4. User selects options
  5. Update dimension scores based on answers
  6. Display Scorecard to user

IF readiness_score >= 80: Skip Round 2, proceed to 1.2
ELSE:
  ROUND 2:
    1. Re-identify 2 lowest-scoring dimensions
    2. Ask 2 more questions
    3. Update scores
    4. Proceed regardless (with gap summary)

QUICK-START OVERRIDE:
  - User can select "Proceed anyway" at any point
  - All dimensions marked as "assumption" in summary
```

#### Option Bank Reference

**Problem Clarity (30pts)**
```
Question: "What type of problem are you solving?"
Options:
  A. "Specific bug or defect with clear reproduction" → 27pts
  B. "New feature with defined business value" → 27pts
  C. "Performance/optimization improvement" → 24pts
  D. "General improvement or refactoring" → 18pts
  E. "Not sure yet - need exploration" → 9pts (flag)
  F. "Other: ___" → 12pts (flag)
```

**Functional Scope (25pts)**
```
Question: "What is the scope of functionality?"
Options:
  A. "Single focused component/module" → 23pts
  B. "Multiple related components" → 20pts
  C. "Cross-cutting system change" → 18pts
  D. "Unclear - need codebase analysis" → 10pts (flag)
  E. "Other: ___" → 10pts (flag)
```

**Success Criteria (20pts)**
```
Question: "How will you verify success?"
Options:
  A. "Automated tests (unit/integration/e2e)" → 18pts
  B. "Performance benchmarks with targets" → 18pts
  C. "Manual testing with checklist" → 14pts
  D. "User feedback/acceptance" → 12pts
  E. "Not defined yet" → 6pts (flag)
  F. "Other: ___" → 8pts (flag)
```

**Constraints (15pts)**
```
Question: "What are the primary constraints?"
Options:
  A. "Time-sensitive (deadline driven)" → 14pts
  B. "Must maintain backward compatibility" → 14pts
  C. "Resource/budget limited" → 12pts
  D. "Security/compliance critical" → 14pts
  E. "No specific constraints" → 10pts
  F. "Other: ___" → 8pts (flag)
```

**Priority/MVP (10pts)**
```
Question: "What is the delivery approach?"
Options:
  A. "MVP first, iterate later" → 9pts
  B. "Full feature, single release" → 9pts
  C. "Phased rollout planned" → 9pts
  D. "Exploratory - scope TBD" → 5pts (flag)
  E. "Other: ___" → 5pts (flag)
```

#### Gap Classification Rules

| Dimension Score | Classification | Handling |
|-----------------|----------------|----------|
| ≥70% of weight | ✓ Defined | Include in Design Brief |
| 50-69% of weight | ⚠️ Assumption | Carry forward as risk |
| <50% of weight | 🚫 Gap | Flag in brief, may need validation |

Example thresholds:
- Problem Clarity: ≥21 Defined, 15-20 Assumption, <15 Gap
- Functional Scope: ≥18 Defined, 13-17 Assumption, <13 Gap
- Success Criteria: ≥14 Defined, 10-13 Assumption, <10 Gap
- Constraints: ≥11 Defined, 8-10 Assumption, <8 Gap
- Priority/MVP: ≥7 Defined, 5-6 Assumption, <5 Gap

#### Clarification Summary Output

After clarification, generate:

```
CLARIFICATION SUMMARY
=====================
Readiness Score: [X]/100

Dimensions:
- Problem Clarity: [X]/30 [✓/⚠️/🚫]
- Functional Scope: [X]/25 [✓/⚠️/🚫]
- Success Criteria: [X]/20 [✓/⚠️/🚫]
- Constraints: [X]/15 [✓/⚠️/🚫]
- Priority/MVP: [X]/10 [✓/⚠️/🚫]

Assumptions & Gaps:
- [Dimension]: [assumption or gap description]
- [Dimension]: [assumption or gap description]

Proceeding to project analysis...
```

Save as `clarification_summary`.

**1.2 Analyze Project Context**

Use available tools to understand:
- Existing codebase structure (Glob, Grep, Read)
- Current architecture patterns
- Dependencies and tech stack
- Related existing implementations

**1.3 Research (if needed)**

If the requirement involves:
- New technologies or frameworks
- Industry best practices
- Performance benchmarks
- Security considerations

Use WebSearch to gather relevant information.

**1.4 Formulate Complete Brief**

Create a comprehensive design brief incorporating clarification results:

```
DESIGN BRIEF
============
Readiness Score: [X]/100

Problem: [clear problem statement]
Context: [project context, tech stack, constraints]

Requirements:
- [requirement 1]
- [requirement 2]
- [requirement 3]

Success Criteria:
- [criterion 1]
- [criterion 2]

Assumptions (from clarification):
- [assumption 1]
- [assumption 2]

Gaps to Validate:
- [gap 1]
- [gap 2]

Research Findings: [if applicable]
```

Save as `design_brief`.

---

### Phase 2: Parallel Independent Design

Send the design brief to all other mounted CLIs for independent design.

**2.1 Dispatch to Claude**

```bash
lask --sync -q <<'EOF'
Design a solution for this requirement:

[design_brief]

Provide:
- Goal (1 sentence)
- Architecture approach
- Implementation steps (3-7 key steps)
- Technical considerations
- Potential risks
- Acceptance criteria (max 3)

Be specific and concrete.
EOF
```

Save response as `claude_design`.

**2.2 Dispatch to Gemini**

```bash
gask <<'EOF'
Design a solution for this requirement:

[design_brief]

Provide:
- Goal (1 sentence)
- Architecture approach
- Implementation steps (3-7 key steps)
- Technical considerations
- Potential risks
- Acceptance criteria (max 3)

Be specific and concrete.
EOF
```

Wait for response. Save as `gemini_design`.

**2.3 Dispatch to OpenCode**

```bash
oask <<'EOF'
Design a solution for this requirement:

[design_brief]

Provide:
- Goal (1 sentence)
- Architecture approach
- Implementation steps (3-7 key steps)
- Technical considerations
- Potential risks
- Acceptance criteria (max 3)

Be specific and concrete.
EOF
```

Wait for response. Save as `opencode_design`.

**2.4 Codex's Independent Design**

While waiting for responses, create YOUR own design (do not look at others yet):
- Goal (1 sentence)
- Architecture approach
- Implementation steps (3-7 key steps)
- Technical considerations
- Potential risks
- Acceptance criteria (max 3)

Save as `codex_design`.

---

### Phase 3: Collect & Analyze All Designs

**3.1 Collect All Responses**

Gather all four designs:
- Claude design → `claude_design`
- Gemini design → `gemini_design`
- OpenCode design → `opencode_design`
- Codex design → `codex_design`

**3.2 Comparative Analysis**

Analyze all four designs (Codex, Claude, Gemini, OpenCode):

Create a comparison matrix:
```
DESIGN COMPARISON
=================

1. Goals Alignment
   - Common goals across all designs
   - Unique perspectives from each

2. Architecture Approaches
   - Overlapping patterns
   - Divergent approaches
   - Pros/cons of each

3. Implementation Steps
   - Common steps (high confidence)
   - Unique steps (need evaluation)
   - Missing steps in some designs

4. Technical Considerations
   - Shared concerns
   - Unique insights from each CLI
   - Critical issues identified

5. Risk Assessment
   - Commonly identified risks
   - Unique risks from each perspective
   - Risk mitigation strategies

6. Acceptance Criteria
   - Overlapping criteria
   - Additional criteria to consider
```

Save as `comparative_analysis`.

---

### Phase 4: Iterative Refinement with Claude

**4.1 Draft Merged Design**

Based on comparative analysis, create initial merged design:
```
MERGED DESIGN (Draft v1)
========================
Goal: [synthesized goal]

Architecture: [best approach from analysis]

Implementation Steps:
1. [step 1]
2. [step 2]
3. [step 3]
...

Technical Considerations:
- [consideration 1]
- [consideration 2]

Risks & Mitigations:
- Risk: [risk 1] → Mitigation: [mitigation 1]
- Risk: [risk 2] → Mitigation: [mitigation 2]

Acceptance Criteria:
- [criterion 1]
- [criterion 2]
- [criterion 3]

Open Questions:
- [question 1]
- [question 2]
```

Save as `merged_design_v1`.

**4.2 Discussion Round 1 - Review & Critique**

```bash
lask --sync -q <<'EOF'
Review this merged design based on all CLI inputs:

COMPARATIVE ANALYSIS:
[comparative_analysis]

MERGED DESIGN v1:
[merged_design_v1]

Analyze:
1. Does this design capture the best ideas from all perspectives?
2. Are there any conflicts or contradictions?
3. What's missing or unclear?
4. Are the implementation steps logical and complete?
5. Are risks adequately addressed?

Provide specific recommendations for improvement.
EOF
```

Save as `claude_review_1`.

**4.3 Discussion Round 2 - Resolve & Finalize**

Based on Claude's review, refine the design:

```bash
lask --sync -q <<'EOF'
Refined design based on your feedback:

MERGED DESIGN v2:
[merged_design_v2]

Changes made:
- [change 1]
- [change 2]

Remaining concerns:
- [concern 1 if any]

Final approval or additional suggestions?
EOF
```

Save as `claude_review_2`.

---

### Phase 5: Final Output

**5.1 Finalize Design**

Incorporate Claude's final feedback and create the complete solution design.

**5.2 Save Plan Document**

Write the final plan to a markdown file:

**File path**: `plans/{feature-name}-plan.md`

Use this template:

```markdown
# {Feature Name} - Solution Design

> Generated by all-plan collaborative design process (Codex-led)

## Overview

**Goal**: [Clear, concise goal statement]

**Readiness Score**: [X]/100

**Generated**: [Date]

---

## Requirements Summary

### Problem Statement
[Clear problem description]

### Scope
[What's in scope and out of scope]

### Success Criteria
- [ ] [criterion 1]
- [ ] [criterion 2]
- [ ] [criterion 3]

### Constraints
- [constraint 1]
- [constraint 2]

### Assumptions
- [assumption 1 from clarification]
- [assumption 2 from clarification]

---

## Architecture

### Approach
[Chosen architecture approach with rationale]

### Key Components
- **[Component 1]**: [description]
- **[Component 2]**: [description]

### Data Flow
[If applicable, describe data flow]

---

## Implementation Plan

### Step 1: [Title]
- **Actions**: [specific actions]
- **Deliverables**: [what will be produced]
- **Dependencies**: [what's needed first]

### Step 2: [Title]
- **Actions**: [specific actions]
- **Deliverables**: [what will be produced]
- **Dependencies**: [what's needed first]

### Step 3: [Title]
- **Actions**: [specific actions]
- **Deliverables**: [what will be produced]
- **Dependencies**: [what's needed first]

[Continue for all steps...]

---

## Technical Considerations

- [consideration 1]
- [consideration 2]
- [consideration 3]

---

## Risk Management

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| [risk 1] | High/Med/Low | High/Med/Low | [strategy] |
| [risk 2] | High/Med/Low | High/Med/Low | [strategy] |

---

## Acceptance Criteria

- [ ] [criterion 1]
- [ ] [criterion 2]
- [ ] [criterion 3]

---

## Design Contributors

| CLI | Key Contributions |
|-----|-------------------|
| Codex | [contributions] |
| Claude | [contributions] |
| Gemini | [contributions] |
| OpenCode | [contributions] |

---

## Appendix

### Clarification Summary
[Include the clarification summary from Phase 1.1]

### Alternative Approaches Considered
[Brief notes on approaches that were evaluated but not chosen]
```

**5.3 Output to User**

After saving the file, display to user:

```
PLAN COMPLETE
=============

✓ Plan saved to: plans/{feature-name}-plan.md

Summary:
- Goal: [1-sentence goal]
- Steps: [N] implementation steps
- Risks: [N] identified with mitigations
- Readiness: [X]/100

Next: Review the plan and proceed with implementation when ready.
```

---

## Principles

1. **Structured Clarification**: Use option-based questions to systematically capture requirements
2. **Readiness Scoring**: Quantify requirement completeness before proceeding
3. **True Independence**: All CLIs design independently without seeing others' work first
4. **Diverse Perspectives**: Leverage unique strengths of each CLI (Codex: code, Claude: context, Gemini: analysis, OpenCode: alternatives)
5. **Evidence-Based Synthesis**: Merge based on comparative analysis, not arbitrary choices
6. **Iterative Refinement**: Use Claude discussion to validate and improve merged design
7. **Concrete Deliverables**: Output actionable plan document, not just discussion notes
8. **Attribution**: Acknowledge contributions from each CLI to maintain transparency
9. **Research When Needed**: Don't hesitate to use WebSearch for external knowledge
10. **Max 2 Iteration Rounds**: Avoid endless discussion; converge on practical solution
11. **Document Output**: Always save final plan as markdown file

---

## Notes

- This skill is designed for complex features or architectural decisions
- For simple tasks, use dual-design or direct implementation instead
- Codex uses `lask --sync` for synchronous communication with Claude
- `gask` and `oask` may require waiting for async responses
- If any CLI is not available, proceed with available CLIs and note the absence
- Plans are saved to `plans/` directory with descriptive filenames
