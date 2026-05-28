# Aggregate-TaskGrounding.ps1
<#
.SYNOPSIS
    Aggregates individual task grounding assessments into a comprehensive feature report.

.DESCRIPTION
    This script combines parallel task validation results from multiple reviewers into
    a single comprehensive TASK_GROUNDING_ANALYSIS.md report. It handles:

    - Merging individual task assessments
    - Calculating aggregate statistics
    - Generating final decision gates
    - Maintaining consistent formatting

.PARAMETER FeatureName
    Name of the feature being validated

.PARAMETER AssessmentFiles
    Array of individual assessment files (JSON format from individual validations)

.PARAMETER OutputPath
    Path for the final aggregated report (default: tasks.grounding.md)

.PARAMETER Validator
    Name of the person performing final aggregation

.EXAMPLE
    # Aggregate multiple individual assessments
    .\Aggregate-TaskGrounding.ps1 -FeatureName "my-feature" -AssessmentFiles @("reviewer1-tasks.json", "reviewer2-tasks.json")

.EXAMPLE
    # Custom output location
    .\Aggregate-TaskGrounding.ps1 -FeatureName "my-feature" -AssessmentFiles @("*.json") -OutputPath "final-report.md"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$FeatureName,

    [Parameter(Mandatory=$true)]
    [string[]]$AssessmentFiles,

    [string]$OutputPath = "tasks.grounding.md",

    [string]$Validator = "Aggregated Review"
)

function Import-TaskAssessments {
    param([string[]]$Files)

    $allTasks = @()

    foreach ($file in $Files) {
        if (Test-Path $file) {
            try {
                $assessments = Get-Content $file -Raw | ConvertFrom-Json
                $allTasks += $assessments.Tasks
                Write-Host "Loaded $($assessments.Tasks.Count) tasks from $file"
            }
            catch {
                Write-Warning "Failed to load $file : $_"
            }
        } else {
            Write-Warning "Assessment file not found: $file"
        }
    }

    # Sort tasks by ID for consistent ordering
    $allTasks = $allTasks | Sort-Object { [int]($_.Id -replace 'T', '') }

    return $allTasks
}

function Calculate-AggregateStatistics {
    param([PSCustomObject[]]$Tasks)

    $totalTasks = $tasks.Count
    $avgGrounding = [math]::Round(($tasks | Measure-Object -Property GroundingLevel -Average).Average, 1)

    $approvedTasks = ($tasks | Where-Object { $_.GroundingLevel -ge 80 }).Count
    $clarifyTasks = ($tasks | Where-Object { $_.GroundingLevel -ge 50 -and $_.GroundingLevel -lt 80 }).Count
    $blockedTasks = ($tasks | Where-Object { $_.GroundingLevel -lt 50 }).Count

    $approvalRate = [math]::Round(($approvedTasks / $totalTasks) * 100, 1)

    $highRiskTasks = ($tasks | Where-Object { $_.Risk -eq "High" }).Count
    $mediumRiskTasks = ($tasks | Where-Object { $_.Risk -eq "Medium" }).Count
    $lowRiskTasks = ($tasks | Where-Object { $_.Risk -eq "Low" }).Count

    # Identify phases based on task IDs (assuming T001-T003 = Phase 1, etc.)
    $phase1Tasks = $tasks | Where-Object { $_.Id -match '^T00[1-3]$' }
    $phase2Tasks = $tasks | Where-Object { $_.Id -match '^T00[4-5]$' }
    $phase3Tasks = $tasks | Where-Object { $_.Id -match '^T00[6-9]$|^T\d{3}$' }

    $phase1Stats = Get-PhaseStats -Tasks $phase1Tasks -PhaseName "Setup"
    $phase2Stats = Get-PhaseStats -Tasks $phase2Tasks -PhaseName "Foundation"
    $phase3Stats = Get-PhaseStats -Tasks $phase3Tasks -PhaseName "Features"

    return @{
        TotalTasks = $totalTasks
        AverageGrounding = $avgGrounding
        ApprovalRate = $approvalRate
        ApprovedTasks = $approvedTasks
        ClarifyTasks = $clarifyTasks
        BlockedTasks = $blockedTasks
        HighRiskTasks = $highRiskTasks
        MediumRiskTasks = $mediumRiskTasks
        LowRiskTasks = $lowRiskTasks
        Phase1 = $phase1Stats
        Phase2 = $phase2Stats
        Phase3 = $phase3Stats
    }
}

function Get-PhaseStats {
    param(
        [PSCustomObject[]]$Tasks,
        [string]$PhaseName
    )

    if ($tasks.Count -eq 0) {
        return @{
            Name = $PhaseName
            TaskCount = 0
            Status = "N/A"
            Coverage = "0/0"
            Action = "No tasks in phase"
        }
    }

    $approved = ($tasks | Where-Object { $_.GroundingLevel -ge 80 }).Count
    $total = $tasks.Count
    $coverage = "$approved/$total"

    # Determine status based on phase thresholds
    $approvalPercent = ($approved / $total) * 100

    $status = switch {
        ($PhaseName -eq "Setup" -and $approvalPercent -ge 90) { "🟢 Mostly Documented" }
        ($PhaseName -eq "Foundation" -and $approvalPercent -ge 80) { "🟢 Mostly Documented" }
        ($PhaseName -eq "Features" -and $approvalPercent -ge 70) { "🟢 Mostly Documented" }
        ($approvalPercent -ge 50) { "🟡 Partially Inferred" }
        default { "🔴 Poorly Grounded" }
    }

    $action = switch {
        ($status -match "🟢") { "Ready to proceed" }
        ($status -match "🟡") { "Needs clarification" }
        default { "Blocked - requires specification" }
    }

    return @{
        Name = $PhaseName
        TaskCount = $total
        Status = $status
        Coverage = $coverage
        Action = $action
    }
}

function Get-OverallDecision {
    param([hashtable]$Stats)

    # Determine blocking conditions
    $criticalGaps = $stats.BlockedTasks -gt 0
    $highRiskRatio = $stats.HighRiskTasks / $stats.TotalTasks

    if ($criticalGaps -or $highRiskRatio -gt 0.5) {
        return "🔴 BLOCK"
    }
    elseif ($stats.ApprovalRate -ge 80) {
        return "✅ APPROVE"
    }
    else {
        return "⚠️ NEEDS CLARIFICATION"
    }
}

function New-AggregatedReport {
    param(
        [PSCustomObject[]]$Tasks,
        [hashtable]$Stats,
        [string]$FeatureName,
        [string]$OutputPath,
        [string]$Validator
    )

    $date = Get-Date -Format "yyyy-MM-dd"
    $decision = Get-OverallDecision -Stats $stats

    $report = @"
# Task Grounding Analysis: $FeatureName
**Date**: $date | **Validator**: $Validator
**Focus**: Aggregated parallel task grounding validation

---

## Executive Summary

| Phase                 | Grounding Status     | Tasks     | Coverage                 | Next Action                 |
| --------------------- | -------------------- | --------- | ------------------------ | --------------------------- |
| Phase 1: $($stats.Phase1.Name) | $($stats.Phase1.Status) | T001-T003 | $($stats.Phase1.Coverage) | $($stats.Phase1.Action) |
| Phase 2: $($stats.Phase2.Name) | $($stats.Phase2.Status) | T004-T005 | $($stats.Phase2.Coverage) | $($stats.Phase2.Action) |
| Phase 3+: $($stats.Phase3.Name) | $($stats.Phase3.Status) | T006+ | $($stats.Phase3.Coverage) | $($stats.Phase3.Action) |

---

## Task Grounding Matrix

| Task                                                                                                    | Grounding Status                        | Primary Evidence                                                                                                                                                                                                           | Gaps                                            | Next Step                                             |
| ------------------------------------------------------------------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------- |
"@

    foreach ($task in $tasks) {
        $status = switch {
            ($task.GroundingLevel -ge 80) { "🟢 **Documented**<br/>(Fully Grounded)" }
            ($task.GroundingLevel -ge 50) { "🟡 **Inferred**<br/>(Partially Grounded)" }
            default { "🔴 **Missing**<br/>(Ungrounded)" }
        }

        $evidence = if ($task.Evidence -and $task.Evidence.Count -gt 0) {
            "• " + ($task.Evidence -join "<br>• ")
        } else {
            "None found"
        }

        $gaps = if ($task.Gaps -and $task.Gaps.Count -gt 0) {
            $task.Gaps -join ", "
        } else {
            "None"
        }

        $nextStep = switch {
            ($task.GroundingLevel -ge 80) { "Ready to implement" }
            ($task.GroundingLevel -ge 50) { "**BLOCKED**: Needs clarification" }
            default { "**BLOCKED**: Requires specification" }
        }

        $report += @"

| **$($task.Id)**<br/>$($task.Title) | $status | $evidence | $gaps | $nextStep |"
    }

    # Aggregate all gaps
    $allGaps = $tasks | Where-Object { $_.Gaps -and $_.Gaps.Count -gt 0 } | ForEach-Object { $_.Gaps } | Select-Object -Unique

    $report += @"


## Observations

### Summary Statistics
- **Total Tasks**: $($stats.TotalTasks)
- **Average Grounding**: $($stats.AverageGrounding)%
- **Approval Rate**: $($stats.ApprovalRate)%
- **Approved Tasks**: $($stats.ApprovedTasks)
- **Needs Clarification**: $($stats.ClarifyTasks)
- **Blocked Tasks**: $($stats.BlockedTasks)

### Risk Distribution
- **🟢 Low Risk**: $($stats.LowRiskTasks) tasks
- **🟡 Medium Risk**: $($stats.MediumRiskTasks) tasks
- **🔴 High Risk**: $($stats.HighRiskTasks) tasks

### Gaps Identified
"@

    if ($allGaps.Count -gt 0) {
        foreach ($gap in $allGaps) {
            $report += "- $gap`n"
        }
    } else {
        $report += "- No significant gaps identified`n"
    }

    $report += @"

## Decision Gate

**Overall Assessment**: $decision
**Rationale**: $($stats.ApprovalRate)% of tasks meet grounding thresholds with $($stats.BlockedTasks) critical gaps
**Next Steps**:
1. Address blocked tasks requiring specification
2. Clarify tasks needing additional information
3. Re-validate after gap resolution

**Aggregated by**: $Validator | **Date**: $date
"@

    $report | Out-File -FilePath $OutputPath -Encoding UTF8
    Write-Host "Aggregated report generated: $OutputPath"
}

# Main execution
try {
    Write-Host "Starting parallel task grounding aggregation for: $FeatureName"

    # Load all individual assessments
    $allTasks = Import-TaskAssessments -Files $AssessmentFiles

    if ($allTasks.Count -eq 0) {
        throw "No valid task assessments found in provided files"
    }

    Write-Host "Aggregating $($allTasks.Count) tasks from $($AssessmentFiles.Count) reviewers"

    # Calculate aggregate statistics
    $stats = Calculate-AggregateStatistics -Tasks $allTasks

    # Generate final report
    New-AggregatedReport -Tasks $allTasks -Stats $stats -FeatureName $FeatureName -OutputPath $OutputPath -Validator $Validator

    Write-Host "Aggregation complete!"
    Write-Host "Final Statistics:"
    Write-Host "- Total Tasks: $($stats.TotalTasks)"
    Write-Host "- Average Grounding: $($stats.AverageGrounding)%"
    Write-Host "- Approval Rate: $($stats.ApprovalRate)%"
    Write-Host "- Decision: $(Get-OverallDecision -Stats $stats)"

} catch {
    Write-Error "Aggregation failed: $_"
    exit 1
}