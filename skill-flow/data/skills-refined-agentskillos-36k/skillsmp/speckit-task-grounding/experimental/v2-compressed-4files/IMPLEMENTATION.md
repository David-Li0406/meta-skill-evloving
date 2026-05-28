# Task Grounding Validation - Implementation & Setup
**Version**: 2.0.0 (Compressed) | **Purpose**: Complete integration guide with automation
**Date**: January 12, 2026

---

## 🚀 Quick Start (5 minutes)

### For Immediate Use (Manual Process)

1. **After tasks.md is generated**, run this checklist:

   ```bash
   # 1. Check artifacts exist
   ls specs/007-*/spec.md specs/007-*/plan.md specs/007-*/tasks.md

   # 2. Read the grounding validation checklist
   cat .claude/skills/speckit-task-grounding/FRAMEWORK.md

   # 3. Generate TASK_GROUNDING_ANALYSIS.md (manual review process)
   # [Use the template from FRAMEWORK.md > Report Template]

   # 4. Review against checklist
   # [Check each item in FRAMEWORK.md > Report Validation Checklist]

   # 5. Approve or block
   # [Mark decision gate: Approved / Needs Clarification / Blocked]
   ```

2. **Review checklist** (10-15 min):
   - Run through "Report Validation Checklist" in FRAMEWORK.md
   - Mark each item ✅
   - Document any ⚠️ or 🔴 findings

3. **Make decision**:
   - If ≥95% items checked → APPROVED
   - If ≥70% items checked → NEEDS CLARIFICATION
   - If <70% items checked → BLOCKED

---

## 🔄 Overall Process Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  tasks.md Generated                         │
│                    (by speckit.tasks)                       │
└────────────────────────────┬────────────────────────────────┘
                             ↓
┌─────────────────────────────────────────────────────────────┐
│          🚪 VALIDATION GATE (15-25 minutes)                 │
│                    ← NEW STEP                               │
│                                                              │
│  1. Extract tasks from tasks.md                             │
│  2. Index planning artifacts                                │
│  3. Map each task to artifact evidence                      │
│  4. Score grounding level (0-100%)                          │
│  5. Identify gaps and risks                                 │
│  6. Generate TASK_GROUNDING_ANALYSIS.md                     │
└────────────────────────────┬────────────────────────────────┘
                             ↓
                    ┌────────────────┐
                    │  Decision Gate │
                    └────────┬───────┘
             ┌──────────────┼──────────────┐
             ↓              ↓              ↓
        ✅ APPROVED    ⚠️ CLARIFY    🔴 BLOCKED
             ↓              ↓              ↓
        PROCEED TO      UPDATE           RETURN TO
        IMPLEMENTATION  ARTIFACTS        PLANNING
             ↓              ↓              ↓
        [Implementation] [Regenerate    [Resolve gaps,
                         tasks.md]      revise spec/plan]
                              ↓              ↓
                          [Revalidate]  [Retry validation]
```

---

## 📊 Decision Matrix (Simple)

```
                    Phase 1/2 Grounding Level
                ┌─────────────┬─────────────┬──────────┐
                │   ≥80%      │   70-79%    │   <70%   │
        ┌───────┼─────────────┼─────────────┼──────────┤
        │ Low   │   ✅ OK     │  ⚠️  REVIEW │ 🔴 BLOCK │
    Gap │ Gaps  │             │             │          │
        ├───────┼─────────────┼─────────────┼──────────┤
        │ Med   │  ⚠️  REVIEW │  🔴 BLOCK   │ 🔴 BLOCK │
        │ Gaps  │             │             │          │
        ├───────┼─────────────┼─────────────┼──────────┤
        │ High  │ 🔴 BLOCK    │  🔴 BLOCK   │ 🔴 BLOCK │
        │ Gaps  │             │             │          │
        └───────┴─────────────┴─────────────┴──────────┘
```

---

## 🛠️ Step-by-Step Integration (6 Steps)

### Step 1: Define Your Artifact Schema

**Create**: `.specify/config/artifact-schema.yaml`

```yaml
# Define which documents are required for task grounding
Features:
  - spec.md:
      Type: specification
      Required: true
      Weight: 1.0

  - plan.md:
      Type: plan
      Required: true
      Weight: 0.9

  - data-model.md:
      Type: design
      Required: false
      Weight: 0.7

  - api-contracts.md:
      Type: contract
      Required: false
      Weight: 0.7

  - research.md:
      Type: research
      Required: false
      Weight: 0.6

  - quickstart.md:
      Type: implementation
      Required: false
      Weight: 0.5

# Minimum coverage thresholds
MinimumCoverage:
  RequiredArtifacts: 2  # Must have spec.md + plan.md
  TotalArtifacts: 4     # Minimum 4 artifacts total
  CoveragePercentage: 71%

# Grounding thresholds by phase
GroundingThresholds:
  Phase1:
    MinLevel: 80%
    ApprovalPercentage: 90%  # ≥90% of tasks at 80%+

  Phase2:
    MinLevel: 70%
    ApprovalPercentage: 80%  # ≥80% of tasks at 70%+

  Phase3Plus:
    MinLevel: 60%
    ApprovalPercentage: 70%  # ≥70% of tasks at 60%+
```

### Step 2: Create Report Template

**Create**: `.specify/templates/task-grounding-template.md`

```markdown
# Task Grounding Analysis: [FEATURE_NAME]
**Feature**: [FEATURE_ID] | **Date**: [DATE]
**Status**: 🔄 In Review

---

## Executive Summary

[Generated by: Extract from tasks.md, count tasks per phase]

| Phase | Status | Count | Avg Grounding | Risk |
|-------|--------|-------|---------------|------|
| Phase 1 | ⏳ | [N] | [N]% | 🟢 |
| Phase 2 | ⏳ | [N] | [N]% | 🟡 |

---

## Phase [N]: [PHASE_NAME]

[For each task in tasks.md]

### Task T[NNN]: [Task Title]

**Artifact Mapping**:
- **Primary**: [artifact.md - Section]
- **Secondary**: [artifact2.md, artifact3.md]
- **Grounding Level**: [0-100%]

**Evidence**:
[Copy quote from artifact with context]

**Assessment**: [Fully/Partially/Weakly Grounded]
- ✅ [Positive finding]
- ⚠️ [Concern if any]

---

## Cross-Artifact Consistency

| Item | Artifact A | Artifact B | Match |
|------|-----------|-----------|-------|
| [Item] | [Value] | [Value] | ✅ |

---

## Critical Gaps & Resolutions

### Gap: [Specific Gap Title]
**Related Tasks**: T[NNN], T[MMM]
**Root Cause**: [Why this gap exists]
**Impact**: [Why it matters]
**Resolution**:
- [ ] [Actionable step 1]
- [ ] [Actionable step 2]
- [ ] [Actionable step 3]

---

## Risk Assessment Summary

| Risk Level | Tasks | Mitigation Required |
|------------|-------|-------------------|
| 🟢 Low | [N] | None |
| 🟡 Medium | [N] | Verification needed |
| 🔴 High | [N] | Block until resolved |

---

## Recommendations

### Immediate Actions
- [ ] [Action for next 1-2 days]

### Before Implementation
- [ ] [Action before coding starts]

### During Implementation
- [ ] [Action during development]

---

## Decision Gate

**Status**: ✅ APPROVED / ⚠️ NEEDS CLARIFICATION / 🔴 BLOCKED

**Rationale**:
[Brief explanation of decision based on grounding levels, gaps, and risks]

**Next Steps**:
[What happens next based on decision]

**Reviewer**: [Your Name]
**Date**: [YYYY-MM-DD]
```

### Step 3: Create Validation Script (PowerShell)

**Create**: `.specify/scripts/powershell/validate-task-grounding.ps1`

```powershell
<#
.SYNOPSIS
    Validates task grounding against planning artifacts

.DESCRIPTION
    This script automates the initial validation of task grounding by:
    1. Checking artifact existence
    2. Extracting tasks from tasks.md
    3. Performing basic artifact indexing
    4. Generating preliminary analysis

.PARAMETER FeaturePath
    Path to the feature directory containing artifacts

.PARAMETER ConfigPath
    Path to the artifact schema configuration file

.EXAMPLE
    .\validate-task-grounding.ps1 -FeaturePath "specs/007-lifeline-invitation-auto-role-mvp"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$FeaturePath,

    [string]$ConfigPath = ".specify/config/artifact-schema.yaml"
)

# Load configuration
$config = Get-Content $ConfigPath | ConvertFrom-Yaml

# Validate artifact existence
$artifacts = Get-ChildItem -Path $FeaturePath -Include "*.md" -Recurse
$missingArtifacts = @()

foreach ($artifact in $config.Features) {
    $artifactName = $artifact.Keys[0]
    $artifactConfig = $artifact.Values[0]

    if ($artifactConfig.Required -and -not (Test-Path "$FeaturePath/$artifactName")) {
        $missingArtifacts += $artifactName
    }
}

if ($missingArtifacts.Count -gt 0) {
    Write-Warning "Missing required artifacts: $($missingArtifacts -join ', ')"
    exit 1
}

# Extract tasks from tasks.md
$tasksContent = Get-Content "$FeaturePath/tasks.md" -Raw
$taskPattern = '### Task T(\d+): (.+?)\n(.+?)(?=\n###|\n---|\n##|\Z)'
$taskMatches = [regex]::Matches($tasksContent, $taskPattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)

$tasks = @()
foreach ($match in $taskMatches) {
    $taskId = $match.Groups[1].Value
    $taskTitle = $match.Groups[2].Value.Trim()
    $taskDescription = $match.Groups[3].Value.Trim()

    $tasks += @{
        Id = "T$taskId"
        Title = $taskTitle
        Description = $taskDescription
        GroundingLevel = 0  # To be determined
        Evidence = @()
    }
}

# Basic artifact indexing
$artifactIndex = @{}
foreach ($artifact in $artifacts) {
    $content = Get-Content $artifact.FullName -Raw
    $artifactIndex[$artifact.Name] = @{
        Path = $artifact.FullName
        Content = $content
        Keywords = [regex]::Matches($content, '\b[A-Z][a-z]+[A-Z][a-zA-Z]*\b') | ForEach-Object { $_.Value }
    }
}

# Generate preliminary analysis
$analysisPath = "$FeaturePath/TASK_GROUNDING_ANALYSIS.md"
$analysisContent = @"
# Task Grounding Analysis: $(Split-Path $FeaturePath -Leaf)
**Date**: $(Get-Date -Format 'yyyy-MM-dd')
**Status**: 🔄 Preliminary Analysis (Manual Review Required)

---

## Artifact Coverage

**Found Artifacts**: $($artifacts.Count)
**Required Artifacts**: $($config.MinimumCoverage.RequiredArtifacts)
**Coverage**: $([math]::Round(($artifacts.Count / $config.MinimumCoverage.TotalArtifacts) * 100))%

"@

if ($missingArtifacts.Count -gt 0) {
    $analysisContent += @"

**Missing Artifacts**:
$(foreach ($missing in $missingArtifacts) { "- $missing`n" })
"@
}

$analysisContent += @"

---

## Task Extraction

**Total Tasks Found**: $($tasks.Count)

$(foreach ($task in $tasks) {
    "### $($task.Id): $($task.Title)`n"
    "$($task.Description)`n"
    "**Preliminary Assessment**: Manual review required`n`n"
})

---

## Next Steps

1. Manually review each task against artifacts
2. Assign grounding levels (0-100%)
3. Document evidence and gaps
4. Make approval decision

*Generated by validate-task-grounding.ps1*
"@

$analysisContent | Out-File -FilePath $analysisPath -Encoding UTF8

Write-Host "Preliminary analysis generated: $analysisPath"
Write-Host "Next: Manual review required for grounding assessment"
```

### Step 4: Integrate into SpecKit Workflow

**Option A: GitHub Actions Integration**

Create `.github/workflows/task-grounding-validation.yml`:

```yaml
name: Task Grounding Validation

on:
  pull_request:
    paths:
      - 'specs/**/tasks.md'

jobs:
  validate-grounding:
    runs-on: windows-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup PowerShell
      uses: microsoft/setup-powershell@v1

    - name: Validate Task Grounding
      run: |
        $featurePath = "specs/$(Get-ChildItem specs -Directory | Where-Object { Test-Path "$_/tasks.md" } | Select-Object -First 1)"
        ./.specify/scripts/powershell/validate-task-grounding.ps1 -FeaturePath $featurePath

    - name: Comment PR with Analysis
      uses: actions/github-script@v6
      with:
        script: |
          const fs = require('fs');
          const analysis = fs.readFileSync('TASK_GROUNDING_ANALYSIS.md', 'utf8');
          github.rest.issues.createComment({
            issue_number: context.issue.number,
            owner: context.repo.owner,
            repo: context.repo.repo,
            body: '## 🤖 Task Grounding Analysis\n\n' + analysis
          });
```

**Option B: VS Code Extension Integration**

Add to `.vscode/settings.json`:

```json
{
  "specKit.taskGrounding": {
    "enabled": true,
    "artifactSchema": ".specify/config/artifact-schema.yaml",
    "templatePath": ".specify/templates/task-grounding-template.md",
    "validationScript": ".specify/scripts/powershell/validate-task-grounding.ps1"
  }
}
```

**Option C: Pre-commit Hook Integration**

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check if tasks.md was modified
if git diff --cached --name-only | grep -q "tasks.md"; then
    echo "🔍 Running task grounding validation..."

    # Find the feature directory
    FEATURE_DIR=$(git diff --cached --name-only | grep "tasks.md" | head -1 | xargs dirname)

    # Run validation
    pwsh .specify/scripts/powershell/validate-task-grounding.ps1 -FeaturePath "$FEATURE_DIR"

    # Check if analysis was generated
    if [ -f "$FEATURE_DIR/TASK_GROUNDING_ANALYSIS.md" ]; then
        echo "✅ Task grounding analysis generated"
        echo "📋 Please review: $FEATURE_DIR/TASK_GROUNDING_ANALYSIS.md"
        echo "⚠️  Commit blocked - manual review required"
        exit 1
    else
        echo "❌ Task grounding validation failed"
        exit 1
    fi
fi
```

### Step 5: Create Decision Framework (YAML)

**Create**: `.specify/config/task-grounding-decisions.yaml`

```yaml
# Decision rules for task grounding approval
decisionRules:
  approval:
    phase1:
      minGroundingLevel: 80
      approvalThreshold: 90  # ≥90% of tasks must be ≥80%
      maxBlockThreshold: 10  # Block if >10% of tasks <50%

    phase2:
      minGroundingLevel: 70
      approvalThreshold: 80  # ≥80% of tasks must be ≥70%
      maxBlockThreshold: 20  # Block if >20% of tasks <50%

    phase3plus:
      minGroundingLevel: 60
      approvalThreshold: 70  # ≥70% of tasks must be ≥60%
      maxBlockThreshold: 30  # Block if >30% of tasks <50%

  riskAssessment:
    lowRisk:
      - groundingLevel: ">= 90"
      - gapSeverity: "low"
      - artifactCoverage: ">= 80%"

    mediumRisk:
      - groundingLevel: "70-89"
      - gapSeverity: "medium"
      - artifactCoverage: "60-79%"

    highRisk:
      - groundingLevel: "< 70"
      - gapSeverity: "high"
      - artifactCoverage: "< 60%"

  gapSeverity:
    critical:
      - affects: "data integrity"
      - affects: "security"
      - affects: "compliance"
      - blocks: "core functionality"

    high:
      - affects: "performance"
      - affects: "scalability"
      - blocks: "important features"

    medium:
      - affects: "user experience"
      - creates: "technical debt"
      - requires: "workarounds"

    low:
      - affects: "edge cases"
      - creates: "minor inconvenience"
      - easily: "fixable"

# Custom rules for your project
customRules:
  # Add project-specific decision criteria here
  securityCritical:
    - if: "task contains 'security' or 'auth'"
    - then: "require 100% grounding"
    - and: "mandatory security review"

  performanceCritical:
    - if: "task affects performance"
    - then: "require 90% grounding"
    - and: "performance impact assessment"
```

### Step 6: Review Checklist Integration

**Create**: `.specify/config/review-checklist.yaml`

```yaml
# Review checklist for task grounding validation
checklist:
  preValidation:
    - id: "artifacts_exist"
      title: "Required artifacts exist"
      description: "spec.md, plan.md, tasks.md present"
      required: true
      severity: "block"

    - id: "minimum_coverage"
      title: "Minimum artifact coverage met"
      description: "At least 71% of defined artifacts present"
      required: true
      severity: "warn"

  reportStructure:
    - id: "executive_summary"
      title: "Executive summary present"
      description: "1-2 paragraphs summarizing findings"
      required: true
      severity: "warn"

    - id: "summary_table"
      title: "Summary table included"
      description: "Phase | Status | Tasks | Grounded | Risk columns"
      required: true
      severity: "warn"

    - id: "task_coverage"
      title: "All tasks covered"
      description: "Every task from tasks.md analyzed"
      required: true
      severity: "block"

  groundingEvidence:
    - id: "primary_artifact"
      title: "Primary artifact identified"
      description: "Each task links to at least one artifact"
      required: true
      severity: "block"

    - id: "evidence_quotes"
      title: "Evidence quotes provided"
      description: "Artifact quotes with context included"
      required: true
      severity: "warn"

    - id: "grounding_levels"
      title: "Grounding levels assigned"
      description: "0-100% score for each task"
      required: true
      severity: "block"

  consistencyValidation:
    - id: "cross_checks"
      title: "Consistency checks performed"
      description: "Key items validated across artifacts"
      required: true
      severity: "warn"

    - id: "discrepancies"
      title: "Discrepancies documented"
      description: "Any inconsistencies identified and explained"
      required: false
      severity: "info"

  gapAnalysis:
    - id: "gaps_identified"
      title: "Gaps identified"
      description: "Missing or weakly grounded tasks documented"
      required: true
      severity: "warn"

    - id: "resolutions"
      title: "Resolutions provided"
      description: "Actionable steps to resolve gaps"
      required: true
      severity: "warn"

  riskAssessment:
    - id: "risk_levels"
      title: "Risk levels assigned"
      description: "Low/Medium/High for each task"
      required: true
      severity: "warn"

    - id: "mitigations"
      title: "Mitigations specified"
      description: "Risk mitigation plans included"
      required: true
      severity: "warn"

  decisionGate:
    - id: "decision_stated"
      title: "Decision clearly stated"
      description: "Approved/Needs Clarification/Blocked"
      required: true
      severity: "block"

    - id: "rationale"
      title: "Rationale provided"
      description: "Explanation of decision criteria"
      required: true
      severity: "warn"

# Scoring weights for automated validation
scoring:
  weights:
    preValidation: 20
    reportStructure: 15
    groundingEvidence: 25
    consistencyValidation: 10
    gapAnalysis: 10
    riskAssessment: 10
    decisionGate: 10

  thresholds:
    approved: 95  # ≥95% checklist items pass
    needsClarification: 70  # ≥70% checklist items pass
    blocked: 70  # <70% checklist items pass
```

---

## 🔍 Task Grounding Scoring Process

```
┌──────────────────────────────────────────────────────────┐
│ For Each Task in tasks.md                                │
└──────────────────────────────────────┬───────────────────┘
                                       ↓
                    ┌──────────────────────────────────┐
                    │ Step 1: Find Evidence            │
                    │ Search planning artifacts for    │
                    │ requirement statement            │
                    └──────────┬───────────────────────┘
                               ↓
                    ┌──────────────────────────────────┐
                    │ Step 2: Count Sources            │
                    │ How many artifacts mention this? │
                    │ - 1 source: 60%                  │
                    │ - 2 sources: 75%                 │
                    │ - 3+ sources: 85%+              │
                    └──────────┬───────────────────────┘
                               ↓
                    ┌──────────────────────────────────┐
                    │ Step 3: Rate Evidence Quality    │
                    │ Explicit = 100%                  │
                    │ Detailed = 90%                   │
                    │ Reference = 70%                  │
                    │ Implicit = 50%                   │
                    │ Assumed = 20%                    │
                    └──────────┬───────────────────────┘
                               ↓
                    ┌──────────────────────────────────┐
                    │ Step 4: Calculate Score          │
                    │ Average quality × source count   │
                    │ = Grounding Level (0-100%)       │
                    └──────────┬───────────────────────┘
                               ↓
                    ┌──────────────────────────────────┐
                    │ Step 5: Assign Risk              │
                    │ 100% = Low risk                  │
                    │ 70-90% = Medium risk             │
                    │ <70% = High risk                 │
                    └──────────┬───────────────────────┘
                               ↓
                    ┌──────────────────────────────────┐
                    │ Step 6: Document Gaps            │
                    │ Identify missing evidence        │
                    │ Suggest resolutions             │
                    └──────────────────────────────────┘
```

---

## 🔧 Troubleshooting Guide

### Issue: Script fails to find artifacts

**Symptoms**: "Missing required artifacts" error

**Solutions**:
1. Check file paths in artifact schema
2. Verify files exist in feature directory
3. Update schema if artifact names changed
4. Use absolute paths if relative paths fail

### Issue: Tasks not extracted correctly

**Symptoms**: Wrong task count or missing tasks

**Solutions**:
1. Check tasks.md format matches expected pattern
2. Verify task IDs are sequential (T001, T002, etc.)
3. Ensure task titles don't contain special characters
4. Update regex pattern in script if needed

### Issue: Grounding analysis incomplete

**Symptoms**: Many tasks show 0% grounding

**Solutions**:
1. Review artifact content for relevant keywords
2. Check if artifacts contain implementation details
3. Add missing specifications to artifacts
4. Consider if tasks are actually needed

### Issue: Decision rules too strict/lenient

**Symptoms**: Too many blocks or approvals

**Solutions**:
1. Adjust thresholds in decision framework YAML
2. Customize rules for your project type
3. Review grounding level assignments
4. Consider project risk tolerance

### Issue: Integration with CI/CD fails

**Symptoms**: Pipeline doesn't trigger or script fails

**Solutions**:
1. Check YAML syntax in workflow files
2. Verify PowerShell execution permissions
3. Test script locally first
4. Check file paths in automation scripts

---

## 📊 Metrics & Monitoring

### Success Metrics to Track

```yaml
# Create .specify/config/metrics.yaml
metrics:
  grounding:
    target: ">= 80%"
    calculation: "average grounding level across all tasks"

  approvalRate:
    target: ">= 75%"
    calculation: "percentage of features approved first time"

  reworkRate:
    target: "<= 20%"
    calculation: "percentage of features requiring regeneration"

  validationTime:
    target: "15-25 min"
    calculation: "average time spent on validation"

  gapResolution:
    target: "<= 10%"
    calculation: "percentage of tasks with unresolved gaps"
```

### Dashboard Setup

**Create**: `.specify/scripts/powershell/generate-metrics-dashboard.ps1`

```powershell
# Generate metrics dashboard from validation reports
param(
    [string]$ReportsPath = "specs",
    [string]$OutputPath = "TASK_GROUNDING_METRICS.md"
)

$reports = Get-ChildItem -Path $ReportsPath -Recurse -Filter "TASK_GROUNDING_ANALYSIS.md"

$metrics = @{
    TotalFeatures = 0
    ApprovedFirstTime = 0
    AverageGrounding = 0
    TotalGaps = 0
    ResolvedGaps = 0
}

# Parse reports and calculate metrics
# [Implementation details...]

# Generate dashboard
$dashboard = @"
# Task Grounding Metrics Dashboard
**Generated**: $(Get-Date -Format 'yyyy-MM-dd HH:mm')

## Overall Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Features Analyzed | $($metrics.TotalFeatures) | - | - |
| First-Time Approval | $($metrics.ApprovedFirstTime)% | ≥75% | $(if ($metrics.ApprovedFirstTime -ge 75) { "✅" } else { "⚠️" }) |
| Average Grounding | $($metrics.AverageGrounding)% | ≥80% | $(if ($metrics.AverageGrounding -ge 80) { "✅" } else { "⚠️" }) |
| Gap Resolution | $([math]::Round(($metrics.ResolvedGaps / $metrics.TotalGaps) * 100))% | ≥90% | $(if (($metrics.ResolvedGaps / $metrics.TotalGaps) -ge 0.9) { "✅" } else { "⚠️" }) |

## Trends

[Chart showing grounding levels over time]

## Recent Validations

| Feature | Date | Grounding | Decision | Gaps |
|---------|------|-----------|----------|------|
$(# [List recent validations...]
)

---
*Auto-generated by generate-metrics-dashboard.ps1*
"@

$dashboard | Out-File -FilePath $OutputPath -Encoding UTF8
```

---

## 🎓 Training & Adoption

### Level 1: Basic User (15 min)
- Read MASTER_GUIDE.md
- Understand grounding concept
- Can perform basic validation

### Level 2: Power User (45 min)
- Read FRAMEWORK.md
- Master checklists and scoring
- Can handle complex validations

### Level 3: Administrator (2 hours)
- Read IMPLEMENTATION.md
- Set up automation and metrics
- Customize for team needs

### Training Materials

**Create**: `.specify/training/`

```
training/
├── quick-reference.pdf          # 1-pager for desks
├── scoring-examples.md          # Real examples with explanations
├── decision-scenarios.md        # Common situations and decisions
├── customization-guide.md       # How to adapt for your project
└── faq.md                       # Answers to common questions
```

---

## 🔄 Maintenance & Updates

### Monthly Tasks
- [ ] Review metrics dashboard
- [ ] Update training materials
- [ ] Refine decision rules based on feedback
- [ ] Audit validation quality

### Quarterly Tasks
- [ ] Major version updates
- [ ] Process improvements
- [ ] Team training refresh
- [ ] Tool enhancements

### Annual Tasks
- [ ] Complete framework review
- [ ] Industry best practice updates
- [ ] Major automation improvements

---

**This IMPLEMENTATION.md provides complete setup instructions. Use [TOOLS.md](TOOLS.md) for practical templates and [FRAMEWORK.md](FRAMEWORK.md) for detailed methodology.**