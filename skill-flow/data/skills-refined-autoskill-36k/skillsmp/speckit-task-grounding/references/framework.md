# Task Grounding Validator - Single Page Complete Framework
**Version**: v3-single-page | **Approach**: Parallel Task-by-Task Validation
**Date**: January 12, 2026

---

## 🎯 Core Concept: Parallel Task Validation

**Each task grounding check is independent** → **Process one task at a time** → **Execute in parallel**

```
For each task in tasks.md:
├── 1. Extract task details
├── 2. Search artifacts for evidence
├── 3. Score grounding level (0-100%)
├── 4. Assess risk & identify gaps
└── 5. Document findings

Then: Aggregate results → Make decision gate → Proceed/Clarify/Block
```

**Time**: 2-3 minutes per task (parallelizable) | **Total**: 15-25 minutes per feature

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Check Prerequisites
```bash
# Verify artifacts exist
ls specs/your-feature/spec.md specs/your-feature/plan.md specs/your-feature/tasks.md
```

### Step 2: Process Each Task (Parallel)
For each task in tasks.md:
1. **Read task** from tasks.md
2. **Search artifacts** for evidence
3. **Score 0-100%** using guidelines below
4. **Note gaps/risks** if any
5. **Record findings**

### Step 3: Generate Report
Use the template below to document your findings:

1. **Executive Summary Table**: Fill in phase status, task counts, and coverage
2. **Task Grounding Matrix**: Document each task with status indicators (🟢🟡🔴)
3. **Observations**: Detail gaps with impact and resolution steps
4. **Action Plan**: Provide immediate, phase-specific execution steps
5. **Risk Assessment**: Assign risk levels with mitigation strategies
6. **Decision Gate**: Apply thresholds and make final recommendation

---

## 📊 Grounding Score Calculator (0-100%)

### Quick Scoring Guide

| Score | Meaning | Evidence Required | Action |
|-------|---------|-------------------|--------|
| **100%** | Explicit | Direct quote: "Add X to Y file" | ✅ Execute |
| **90%** | Detailed | Code example or schema provided | ✅ Execute |
| **80%** | Referenced | Clear spec with implementation notes | ✅ Execute |
| **70%** | Pattern | Documented pattern to follow | ⚠️ Verify pattern |
| **60%** | Inferred | Multiple weak references | ⚠️ Clarify |
| **50%** | Assumed | Single weak reference | 🔴 High risk |
| **<50%** | Missing | No evidence found | 🔴 Block |

### Evidence Types (Search Order)
1. **spec.md** (requirements) - Highest authority
2. **plan.md** (technical plan) - Implementation details
3. **research.md** (decisions) - Research findings and context
4. **data-model.md** (schemas) - Data structures and entities
5. **contracts/** (interfaces) - API contracts and specifications
6. **quickstart.md** (guides) - Implementation docs and validation scenarios

---

## 🔍 Task Validation Process (Per Task)

### Template for Each Task
```markdown
### Task T[ID]: [Task Title]

**File**: [path/to/file]
**Phase**: [1/2/3+]

#### Evidence Search
**Primary Artifact**: [artifact.md > section]
**Quote**: "[exact text with context]"
**Match Type**: [explicit/reference/implicit/external]

#### Grounding Assessment
**Level**: [0-100%]
**Rationale**: [why this score]
**Risk**: [Low/Medium/High]

#### Gaps Identified
- [ ] [Gap description and resolution needed]
```

### Decision Rules Per Task
- **✅ Proceed**: ≥80% grounding (Phase 1) or ≥70% (Phase 2+)
- **⚠️ Clarify**: 50-79% grounding, resolvable gaps
- **🔴 Block**: <50% grounding or critical gaps

---

## 📋 Complete Checklist (All-in-One)

### Pre-Validation Setup
- [ ] `spec.md` exists and current
- [ ] `plan.md` exists and current
- [ ] `tasks.md` exists and current
- [ ] At least 4 of 6 artifacts available
- [ ] Tasks follow format: `### Task T001: Title`

### Per-Task Validation
For each task:
- [ ] Task extracted from tasks.md
- [ ] Primary artifact identified
- [ ] Evidence quote captured (with context)
- [ ] Grounding level assigned (0-100%)
- [ ] Risk level assessed (Low/Med/High)
- [ ] Gaps identified with resolutions
- [ ] Assessment documented

### Cross-Task Validation
- [ ] All tasks from tasks.md covered
- [ ] Consistent scoring methodology used
- [ ] No contradictory evidence found
- [ ] Phase boundaries respected

### Report Generation
- [ ] Executive Summary table completed with phase status and coverage
- [ ] Task Grounding Matrix populated for all tasks
- [ ] Visual status indicators used (🟢🟡🔴)
- [ ] Primary evidence documented with artifact references
- [ ] Gaps identified with specific descriptions
- [ ] Next steps defined for each task
- [ ] Observations section includes gap analysis with impact/resolution
- [ ] Action Plan structured (Immediate/Phase 1/Phase 2)
- [ ] Risk assessment table completed with mitigation strategies
- [ ] Decision Gate applied with rationale and next steps

---

## ⚡ Decision Matrix (Complete)

### Phase Thresholds
```
Phase 1 (Setup)       | ≥90% tasks at ≥80% | ✅ APPROVE
Phase 1 (Setup)       | 70-89% tasks at ≥80% | ⚠️ CLARIFY
Phase 1 (Setup)       | <70% tasks at ≥80% | 🔴 BLOCK

Phase 2 (Foundation)  | ≥80% tasks at ≥70% | ✅ APPROVE
Phase 2 (Foundation)  | 60-79% tasks at ≥70% | ⚠️ CLARIFY
Phase 2 (Foundation)  | <60% tasks at ≥70% | 🔴 BLOCK

Phase 3+ (Features)   | ≥70% tasks at ≥60% | ✅ APPROVE
Phase 3+ (Features)   | 50-69% tasks at ≥60% | ⚠️ CLARIFY
Phase 3+ (Features)   | <50% tasks at ≥60% | 🔴 BLOCK
```

### Risk Multipliers
- **Low Risk** (×1.0): ≥90% grounding, no gaps
- **Medium Risk** (×0.8): 70-89% grounding, resolvable gaps
- **High Risk** (×0.6): <70% grounding, critical gaps

### Gap Impact
- **Minor Gap** (×0.9): Documentation missing, easily resolved
- **Major Gap** (×0.7): Implementation uncertainty, needs clarification
- **Critical Gap** (×0.5): Blocks implementation, return to planning

---

## 📝 Report Template (Complete)

```markdown
# Task Grounding Analysis: [FEATURE_NAME]
**Date**: [YYYY-MM-DD] | **Validator**: [NAME]
**Focus**: Grounding validation against planning artifacts

---

## Executive Summary

| Phase                 | Grounding Status     | Tasks     | Coverage                 | Next Action                 |
| --------------------- | -------------------- | --------- | ------------------------ | --------------------------- |
| Phase 1: [Phase Name] | 🟢 Mostly Documented  | T001-T003 | 2/3 Fully, 1/3 Partially | [Action needed]             |
| Phase 2: [Phase Name] | 🟡 Partially Inferred | T004-T005 | 0/2 Fully, 2/2 Partially | [Action needed]             |

---

## Task Grounding Matrix

| Task                                                                                                    | Grounding Status                        | Primary Evidence                                                                                                                                                                                                           | Gaps                                            | Next Step                                             |
| ------------------------------------------------------------------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------- |
| **T001**<br/>[Task Title]                                                                               | 🟢 **Documented**<br/>(Fully Grounded)   | • [artifact.md]: [Brief evidence description]<br>• [artifact.md]: [Additional evidence]<br>• [artifact.md]: [More evidence]                                                         | None                                            | Ready to implement                                    |
| **T002**<br/>[Task Title]                                                                               | 🟢 **Documented**<br/>(Fully Grounded)   | • [artifact.md]: [Brief evidence description]<br>• [artifact.md]: [Additional evidence]                                                                                            | None                                            | Ready to implement                                    |
| **T003**<br/>[Task Title]                                                                               | 🟡 **Inferred**<br/>(Partially Grounded) | • Assumed [pattern] exists ([reference])<br>• [artifact.md]: Shows [evidence]<br>• [artifact.md]: No explicit [reference]                                                          | [Gap description]                               | **BLOCKED**: [Action required]                        |
| **T004**<br/>[Task Title]                                                                               | 🟡 **Inferred**<br/>(Partially Grounded) | • [artifact.md]: [Reference] only<br>• [artifact.md]: Only mentions [related item]<br>• [artifact.md]: No [specific] specification                                                  | [Gap description]                               | **BLOCKED**: [Action required]                        |
| **T005**<br/>[Task Title]                                                                               | 🟡 **Inferred**<br/>(Partially Grounded) | • [artifact.md]: [Pattern] documented<br>• [artifact.md]: [Pattern] for events<br>• Depends on T004 completion                                                                     | [Gap description]                               | **BLOCKED**: Depends on T004 + [additional checks]    |

## Observations

### Gaps
**Gap 1: [Gap Title]**
*Impact*: [Impact description]
*Evidence*: [Evidence supporting the gap]
*Resolution*: [Resolution steps]

**Gap 2: [Gap Title]**
*Impact*: [Impact description]
*Evidence*: [Evidence supporting the gap]
*Resolution*: [Resolution steps]

**Gap 3: [Gap Title]**
*Impact*: [Impact description]
*Evidence*: [Evidence supporting the gap]
*Resolution*: [Resolution steps]

### Action Plan
**Immediate (Before Any Implementation)**
1. [Immediate action 1]
2. [Immediate action 2]
3. [Immediate action 3]

**Phase 1 Execution (After Verification)**
1. [Phase 1 action 1]
2. [Phase 1 action 2]

**Phase 2 Execution (After Verification)**
1. [Phase 2 action 1]
2. [Phase 2 action 2]

### Risks
| Task | Level    | Mitigation                       |
| ---- | -------- | -------------------------------- |
| T001 | 🟢 Low    | [Mitigation strategy]            |
| T002 | 🟢 Low    | [Mitigation strategy]            |
| T003 | 🟡 Medium | [Mitigation strategy]            |
| T004 | 🟡 Medium | [Mitigation strategy]            |
| T005 | 🟡 Medium | [Mitigation strategy]            |

## Decision Gate

**Overall Assessment**: [✅ APPROVE / ⚠️ NEEDS CLARIFICATION / 🔴 BLOCK]
**Rationale**: [Explanation of decision based on thresholds and gaps]
**Next Steps**:
1. [Next step 1]
2. [Next step 2]
3. [Next step 3]
4. [Final step]

**Validator**: [NAME] | **Date**: [YYYY-MM-DD]
```

---

## 🛠️ Implementation Automation

### PowerShell Script Template
```powershell
# Validate-TaskGrounding.ps1
param(
    [string]$FeaturePath,
    [string]$OutputPath = "tasks.grounding.md"
)

# Load artifacts
$artifacts = Get-ChildItem $FeaturePath -Filter "*.md" -Recurse |
    Where-Object { $_.Name -in @('spec.md','plan.md','research.md','data-model.md','quickstart.md') }

# Also include all .md files from contracts/ directory
$contractsPath = Join-Path $FeaturePath 'contracts'
if (Test-Path $contractsPath) {
    $contractsFiles = Get-ChildItem $contractsPath -Filter "*.md" -Recurse
    $artifacts += $contractsFiles
}

# Extract tasks
$tasksContent = Get-Content "$FeaturePath/tasks.md" -Raw
$taskPattern = '### Task T(\d+): (.+?)\n(.+?)(?=\n###|\n---|\n##|\Z)'
$tasks = [regex]::Matches($tasksContent, $taskPattern, 'Singleline') | ForEach-Object {
    [PSCustomObject]@{
        Id = "T$($_.Groups[1].Value)"
        Title = $_.Groups[2].Value.Trim()
        Description = $_.Groups[3].Value.Trim()
        GroundingLevel = 0
        Evidence = @()
        Risk = "Unknown"
        Gaps = @()
    }
}

# Parallel processing (conceptual - implement per your needs)
$results = $tasks | ForEach-Object -Parallel {
    # Search artifacts for evidence
    # Score grounding level
    # Assess risk
    # Identify gaps
    # Return assessment
}

# Generate report
# [Report generation logic...]
```

### GitHub Actions Integration
```yaml
name: Task Grounding Validation
on:
  pull_request:
    paths: ['specs/**/tasks.md']

jobs:
  validate:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v3
    - name: Validate Grounding
      run: .\validate-task-grounding.ps1 -FeaturePath "specs/${{ github.event.pull_request.title }}"
    - name: Comment Results
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const report = fs.readFileSync('tasks.grounding.md', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: '## 🤖 Task Grounding Analysis\n\n' + report
          });
```

---

## 📊 Scoring Examples (Real Cases)

### Example 1: Perfect Grounding (100%)
**Task**: Add `LifelineAutoRoleAssignment` to `TenantFeatureFlag` enum
**Status**: 🟢 **Documented** (Fully Grounded)
**Evidence**:
• data-model.md: Explicit enum addition with Display attribute
• plan.md: Feature flag controls tenant enablement
• quickstart.md: Implementation checklist item
• contracts/: Display name mapping
**Assessment**: ✅ Ready to implement - explicit specification with exact location and format

### Example 2: Pattern-Based (70%)
**Task**: Add role name constants following FSHRoles.cs pattern
**Status**: 🟡 **Inferred** (Partially Grounded)
**Evidence**:
• Assumed FSHRoles.cs pattern exists (follows FSHPermissions.cs)
• data-model.md: Shows hardcoded strings in examples
• plan.md: No explicit FSHRoles.cs reference
**Gap**: FSHRoles.cs existence not verified
**Assessment**: ⚠️ BLOCKED - Pattern existence unverified, requires codebase inspection

### Example 3: Weak Inference (50%)
**Task**: Define `SessionGroupParticipantInvitationSentEvent`
**Status**: 🟡 **Inferred** (Partially Grounded)
**Evidence**:
• contracts/: Schema reference only
• research.md: Only mentions AcceptedEvent
• plan.md: No SentEvent specification
**Gap**: No detailed spec for SentEvent requirements
**Assessment**: ⚠️ BLOCKED - Spec requirements unclear, verify FR-001 requires SentEvent

### Example 4: Ungrounded (20%)
**Task**: Add logging for performance monitoring
**Status**: 🔴 **Missing** (Ungrounded)
**Evidence**: None found in any artifact
**Gap**: Task appears to be developer assumption without specification
**Assessment**: 🔴 BLOCK - No evidence found, likely should be removed or specified

---

## 🚨 Red Flags & Common Issues

### Critical Red Flags (Auto-Block)
- [ ] >50% tasks score <50% grounding
- [ ] No spec.md or plan.md exists
- [ ] Tasks contradict artifact specifications
- [ ] Critical functionality (security, data integrity) ungrounded

### Warning Signs (Needs Review)
- [ ] ≥30% tasks score 50-69% grounding
- [ ] Multiple gaps requiring major artifact updates
- [ ] Inconsistent evidence across artifacts
- [ ] Risk assessments incomplete

### Quality Issues (Fix Before Proceed)
- [ ] Evidence quotes lack context
- [ ] Grounding scores inconsistent with evidence
- [ ] Gaps identified but no resolution steps
- [ ] Risk levels not justified

---

## 🔧 Customization Guide

### Adjust Thresholds for Your Project
```yaml
# Conservative (high quality bar)
phase1: { minGrounding: 80, approvalThreshold: 95 }
phase2: { minGrounding: 75, approvalThreshold: 90 }

# Standard (balanced)
phase1: { minGrounding: 80, approvalThreshold: 90 }
phase2: { minGrounding: 70, approvalThreshold: 80 }

# Lenient (faster approval)
phase1: { minGrounding: 70, approvalThreshold: 80 }
phase2: { minGrounding: 60, approvalThreshold: 70 }
```

### Add Custom Artifact Types
```yaml
customArtifacts:
  - security-review.md: { weight: 100, required: true }
  - performance.md: { weight: 85, required: false }
  - architecture.md: { weight: 90, required: false }
```

### Project-Specific Rules
```yaml
rules:
  - if: "task contains 'security'"
    then: "require 100% grounding"
  - if: "task affects performance"
    then: "require 90% grounding"
  - if: "task uses external API"
    then: "require contracts/ reference"
```

---

## 📈 Metrics & Success Tracking

### Key Metrics to Monitor
- **Approval Rate**: % features approved first time (target: ≥75%)
- **Average Grounding**: Mean grounding score across all tasks (target: ≥80%)
- **Gap Resolution**: % gaps resolved before implementation (target: ≥90%)
- **Validation Time**: Minutes spent per feature (target: 15-25 min)
- **Rework Rate**: % features requiring regeneration (target: <20%)

### Dashboard Template
```markdown
# Task Grounding Metrics - [MONTH YEAR]

## Overall Performance
| Metric | This Month | Target | Status |
|--------|------------|--------|--------|
| Features Validated | 12 | - | - |
| First-Time Approval | 83% | ≥75% | ✅ |
| Average Grounding | 85% | ≥80% | ✅ |
| Critical Gaps Found | 3 | <5 | ✅ |

## Trends
- Grounding scores improving: +5% from last month
- Validation time stable: ~18 min average
- Gap resolution: 95% resolved before implementation

## Top Issues This Month
1. Missing contracts/ references (3 cases)
2. Pattern assumptions without verification (2 cases)
3. Incomplete data-model.md specifications (1 case)
```

---

## 🎯 Training & Adoption

### Level 1: Basic User (30 min)
- Read this page completely
- Practice scoring on 3 example tasks
- Understand decision matrix
- Can validate simple features

### Level 2: Power User (60 min)
- Study all examples and edge cases
- Learn customization options
- Practice on real feature
- Can handle complex validations

### Level 3: Administrator (2 hours)
- Understand automation setup
- Customize for team needs
- Set up metrics tracking
- Train other team members

### Quick Training Checklist
- [ ] Understand grounding scale (0-100%)
- [ ] Can identify evidence types
- [ ] Knows decision thresholds
- [ ] Can spot red flags
- [ ] Understands parallel processing
- [ ] Can write gap resolutions
- [ ] Familiar with report template

---

## ❓ FAQ & Troubleshooting

### Q: How long should validation take?
**A**: 2-3 minutes per task. For a typical feature (8 tasks), expect 15-25 minutes total.

### Q: What if artifacts don't exist?
**A**: Block the feature. Cannot validate without spec.md and plan.md minimum.

### Q: Can I validate tasks in parallel?
**A**: Yes! Each task validation is independent. Distribute tasks among reviewers.

### Q: What if I find contradictory evidence?
**A**: Document the contradiction as a critical gap. Requires artifact synchronization.

### Q: How do I handle "MVP" assumptions?
**A**: Score as 50% max. Document as high-risk gap requiring future specification.

### Q: When should I block vs clarify?
**A**: Block if >50% tasks <50% grounded OR critical gaps unresolved. Clarify for resolvable issues.

### Q: Can I customize scoring?
**A**: Yes, but document your custom rules and apply consistently across all validations.

---

## 📞 Support & Resources

### Getting Help
- **Scoring Questions**: Reference examples above
- **Process Questions**: Re-read "Task Validation Process" section
- **Technical Issues**: Check automation scripts
- **Customization**: See "Customization Guide"

### Related Files (Historical)
- `v1-original/`: Complete original documentation (13 files)
- `v2-compressed-4files/`: Four-file compressed version
- `references/tasks.grounding.md`: Example report template
- `v3-future-iterations/`: This file and future iterations

### Version History
- **v1**: 13 files, comprehensive but overwhelming
- **v2**: 4 files, logical grouping, 69% reduction
- **v3**: 1 file, parallel task focus, maximum compression

---

## 🎉 Ready to Validate!

**Process**: For each task → Search → Score → Assess → Document → Aggregate → Decide

**Time**: 2-3 min per task (parallelizable)

**Output**: tasks.grounding.md report with Executive Summary, Task Grounding Matrix, Observations, Action Plan, and Decision Gate

**Decision**: ✅ Approve / ⚠️ Clarify / 🔴 Block based on phase thresholds and gap analysis

**This single page contains everything needed for complete task grounding validation. Process tasks in parallel for maximum efficiency!** 🚀