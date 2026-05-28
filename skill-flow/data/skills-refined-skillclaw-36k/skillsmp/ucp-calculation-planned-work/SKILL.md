---
name: ucp-calculation-planned-work
description: Calculate Use Case Points (UCP) for software development work using Onshore's v4.0 complete coverage methodology. Includes work item classification (stories/tasks/bugs/tests), transaction counting, Technical Complexity Factor (TCF) calculation, Environmental Complexity Factor (ECF) calculation, Specificity Adjustment Factor (SAF) scoring, and comprehensive reporting. Use when analyzing development effort, estimating projects, calculating billing, generating UCP reports, analyzing Azure DevOps work items, analyzing git repositories, counting use case transactions, or any UCP-related calculation.
---

# UCP Calculation for Planned Work

Calculate Use Case Points for software development projects using Onshore's v4.0 complete work coverage methodology.

## Quick Start

**Minimal invocation:**
```
"Calculate UCP for the Agent Studio Pro project. Input: git repository. Output: comprehensive UCP report."
```

**With Azure DevOps:**
```
"Calculate UCP from Azure DevOps User Stories for the Lighthouse project. Use references/azure-devops-hierarchy.md for work item guidance."
```

**Using scripts:**
```bash
python scripts/count_transactions.py "1. User enters credentials
2. System validates
3. System generates JWT
4. System returns token"
# Output: 3.6 transactions ’ Simple ’ 5 UUCW

python scripts/calculate_ucp.py --uaw 24 --uucw 562.4 --tcf 1.40 --ecf 0.86 --verbose
# Output: Realistic UCP: 494.22
```

## Core Workflow

### Step 1: Determine Input Source

**Option A: Azure DevOps Work Items**
1. Check work item types available (Epic/Feature/User Story/Task)
2. **Prefer User Stories** (95-98% accuracy)
3. If only Features: apply 1.8x calibration factor
4. Read `references/azure-devops-hierarchy.md` for guidance

**Option B: Git Repository**
1. Analyze codebase structure
2. Identify use cases from code (API endpoints, services, features)
3. Count transactions per use case
4. Read `references/git-repository-analysis.md` for methodology

### Step 2: Identify Actors

Count external entities that interact with the system:

- **Simple (Weight 1):** API/SDK (standard protocols)
- **Average (Weight 2):** Interactive UI, automated systems
- **Complex (Weight 3):** Custom protocols, admin dashboards

Calculate UAW (Unadjusted Actor Weight):
```
UAW = (Simple × 1) + (Average × 2) + (Complex × 3)
```

### Step 3: Count and Classify Use Cases

**v4.0 Complete Coverage** - Count ALL work across 4 categories:

#### Category 1: New Functionality (1.0x multiplier)
- User stories, features delivering new capabilities
- Count transactions from acceptance criteria
- Use `scripts/count_transactions.py` for automation

#### Category 2: Enhancements (0.6x multiplier)
- Tasks, refactoring, technical improvements
- Implementation without full scope

#### Category 3: Maintenance (0.4x multiplier)
- Bugs, defects, corrections
- Apply urgency multipliers: Normal 1.0x, High 1.2x, Critical 1.5x

#### Category 4: Quality Assurance (0.3x multiplier)
- Test cases, test suites, QA work

**Transaction Counting Rules:**
- Framework/SDK operations: 0.5 weight (FastAPI routes, ORM queries, API calls)
- Custom business logic: 1.0 weight (workflows, algorithms, state management)

**Classification:**
- Simple: d3 transactions ’ 5 UUCW
- Average: 4-7 transactions ’ 10 UUCW
- Complex: >7 transactions ’ 15 UUCW

Calculate UUCW per category:
```
Final UUCW = Base UUCW × Category Multiplier × (0.7 + 0.3 × SAF)
```

**SAF (Specificity Adjustment Factor):** Assess work item quality (0-1 scale)
- Read `references/saf-methodology.md` for detailed rubric
- 5 dimensions: Clarity, Acceptance Criteria, Technical Detail, Scope, Dependencies

### Step 4: Calculate UUCP

```
UUCP = UAW + Total UUCW (sum of all 4 categories)
```

### Step 5: Assess Technical Complexity (TCF)

Evaluate 13-20 technical factors (ratings 0-5):
- Standard factors (T1-T13): Distributed system, performance, security, etc.
- AI/ML factors (T14-T20): Model complexity, data volume, explainability, etc.

**Read `references/tcf-factors.md` for complete factor definitions and rating criteria.**

```
TFactor = £(Rating × Weight)
TCF = 0.6 + (0.01 × TFactor)
TCF (capped) = min(TCF, 1.4)
```

Use `scripts/calculate_ucp.py` to automate:
```bash
python scripts/calculate_ucp.py --uaw 24 --uucw 562.4 --tcf 1.40 --ecf 0.86
```

### Step 6: Assess Environmental Complexity (ECF)

Evaluate 8 environmental factors (ratings 0-5):
- E1-E6: Favorable when HIGH (experience, motivation, stable requirements)
- E7-E8: Unfavorable when HIGH (part-time staff, difficult language)

```
EFactor = £(Rating × Weight)
ECF = 1.4 + (-0.03 × EFactor)
```

### Step 7: Calculate Final UCP

```
Adjusted UCP = UUCP × TCF × ECF

Realistic UCP = Adjusted UCP × Framework Leverage Factor
(Framework Leverage: 0.6-1.0, typically 0.7 for framework-heavy projects)
```

### Step 8: Generate Report

Use `assets/templates/ucp-report-template.md` as structure.

**Include:**
1. Executive Summary (all metrics)
2. Actor Summary Table
3. Work Item Analysis (all 4 categories)
4. SAF Distribution
5. UUCP Calculation
6. TCF Assessment (with TFactor breakdown)
7. ECF Assessment (with EFactor breakdown)
8. UCP Calculation
9. Effort Estimation (productivity factor: 18-22 hours/UCP typical)

## Key Concepts

**v4.0 Complete Work Coverage:** Unlike traditional UCP (50-60% coverage), v4.0 captures ALL development work across 4 categories with differentiated multipliers.

**Specificity Adjustment Factor (SAF):** Rewards high-quality specifications, reduces credit for vague requirements. Ranges 0.70x (no spec) to 1.00x (excellent spec).

**Framework Leverage:** Accounts for framework-provided functionality (FastAPI routing, SQLAlchemy ORM, etc.). Typically 0.7 for modern frameworks.

**Azure DevOps Hierarchy:**
- **Epic** (Strategic) ’ **Feature** (Functional) ’ **User Story** (Use Case ) ’ **Task** (Implementation)
- **Count User Stories for UCP**, not Epics or Tasks
- If only Features available: apply 1.8x calibration

**Transaction Weighting:**
- 0.5 for framework operations (HTTP routing, ORM queries, SDK calls)
- 1.0 for custom logic (business rules, workflows, algorithms)

## Available Resources

### Scripts
- **scripts/count_transactions.py**  Parse acceptance criteria, count weighted transactions, classify complexity
  ```bash
  python scripts/count_transactions.py --file user_story.txt --verbose
  ```

- **scripts/calculate_ucp.py**  Calculate UCP from UAW, UUCW, TCF, ECF
  ```bash
  python scripts/calculate_ucp.py --uaw 24 --uucw 562.4 --tcf 1.40 --ecf 0.86 --framework-leverage 0.70
  ```

### References
- **references/tcf-factors.md**  Complete TCF factor definitions (T1-T20), rating criteria, examples
- **references/saf-methodology.md**  SAF 5-dimension rubric, impact calculations, quality assessment
- **references/azure-devops-hierarchy.md**  Work item hierarchy, calibration factors, decision matrix
- **references/git-repository-analysis.md**  Code-based UCP analysis methodology

### Assets
- **assets/templates/ucp-report-template.md**  Complete report structure for filling in calculated values

## Output Format

Generate comprehensive UCP Analysis Report with:

**Section 1: Executive Summary** (key metrics table)
**Section 2: Actor Summary** (classification table, UAW calculation)
**Section 3: Work Item Analysis** (4 categories, transaction counts, SAF scores, UUCW calculations)
**Section 4: SAF Distribution** (quality assessment)
**Section 5: UUCP Calculation** (UAW + UUCW)
**Section 6: TCF Assessment** (factor ratings, TFactor, TCF formula)
**Section 7: ECF Assessment** (factor ratings, EFactor, ECF formula)
**Section 8: UCP Calculation** (Adjusted UCP, Framework Leverage, Realistic UCP)
**Section 9: Effort Estimation** (productivity factor, estimated hours)

**Include interpretations:** What TCF/ECF values mean, accuracy notes, comparison to traditional UCP (v3.0 vs v4.0).

## Decision Matrix for Input Sources

| Input Source | Accuracy | Speed | Use When |
|--------------|----------|-------|----------|
| User Stories (Azure DevOps) | 95-98% | Fast | Work items available with acceptance criteria |
| Features (Azure DevOps) | 80-90% | Fast | No User Stories, apply 1.8x calibration |
| Git Repository | 95-98% | Slow | Retrospective analysis, 100% coverage needed |
| Mixed Sources | 85-95% | Medium | Some User Stories, some Features |

## Common Patterns

**Pattern 1: Azure DevOps with User Stories**
1. Export User Stories with acceptance criteria
2. Count transactions per story using `scripts/count_transactions.py`
3. Calculate SAF for each story (typically 0.65-0.85)
4. Calculate UUCW per category
5. Assess actors, TCF, ECF
6. Generate final UCP report

**Pattern 2: Azure DevOps with Features Only**
1. Read `references/azure-devops-hierarchy.md`
2. Extract Key Deliverables from Features
3. Estimate transactions per deliverable
4. Apply 1.8x calibration factor
5. Add 25-30% for untracked infrastructure
6. Note ±20% margin of error in report

**Pattern 3: Git Repository Analysis**
1. Read `references/git-repository-analysis.md`
2. Analyze codebase structure (API routes, services, components)
3. Identify use cases from code organization
4. Count transactions (framework 0.5x, custom 1.0x)
5. Calculate UUCW with 100% coverage
6. Most accurate result (±5-10%)

## Important Reminders

1. **Always use User Stories over Features**  95% accuracy vs 80% accuracy
2. **v4.0 counts ALL work**  Stories, Tasks, Bugs, Tests (not just stories)
3. **SAF rewards quality**  Well-specified work gets full credit (1.0x), vague work gets reduced credit (0.7x minimum)
4. **Check for missing categories**  Infrastructure, monitoring, logging, deployment often untracked
5. **Framework leverage is real**  Modern frameworks provide 60-80% of functionality, account for it
6. **TCF typically 0.95-1.15**  Values >1.30 indicate exceptional complexity
7. **ECF typically 0.70-0.90**  Favorable teams ~0.85, challenging environments ~0.70
8. **Productivity factor 18-22 hrs/UCP**  For moderate challenges, adjust based on ECF

## Token Efficiency Notes

- Scripts handle deterministic calculations (transaction counting, UCP math)
- References contain detailed rubrics (TCF 20 factors, SAF 5 dimensions)
- Template provides report structure (fill-in-the-blanks)
- SKILL.md focuses on workflow and decision-making (when to use what)

This progressive disclosure keeps core instructions concise while making detailed reference material available when needed.
