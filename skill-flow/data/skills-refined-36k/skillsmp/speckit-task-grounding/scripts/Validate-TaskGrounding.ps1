# Validate-TaskGrounding.ps1
<#
.SYNOPSIS
    Validates task grounding against planning artifacts for feature readiness assessment.

.DESCRIPTION
    This script performs parallel task grounding validation by:
    1. Loading planning artifacts (spec.md, plan.md, data-model.md, etc.)
    2. Extracting tasks from tasks.md
    3. Searching artifacts for evidence of each task
    4. Scoring grounding level (0-100%)
    5. Assessing risk and identifying gaps
    6. Generating a comprehensive validation report

.PARAMETER FeaturePath
    Path to the feature directory containing planning artifacts and tasks.md

.PARAMETER TaskFilter
    Optional comma-separated list of task IDs to validate (e.g., "T001,T002,T003"). If not specified, all tasks are validated.

.PARAMETER JsonOutput
    Switch to output results in JSON format for aggregation instead of markdown report.

.EXAMPLE
    .\Validate-TaskGrounding.ps1 -FeaturePath "specs/my-feature"

.EXAMPLE
    .\Validate-TaskGrounding.ps1 -FeaturePath "specs/my-feature" -OutputPath "validation-report.md"

.EXAMPLE
    # Validate only specific tasks for parallel processing
    .\Validate-TaskGrounding.ps1 -FeaturePath "specs/my-feature" -TaskFilter "T001,T002" -JsonOutput -OutputPath "reviewer1-assessment.json"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$FeaturePath,

    [string]$OutputPath = "tasks.grounding.md",

    [string]$TaskFilter,  # Optional: "T001,T002,T003" to process only specific tasks

    [switch]$JsonOutput   # Output JSON format for aggregation instead of markdown
)

# Configuration
$artifactNames = @('spec.md','plan.md','research.md','data-model.md','quickstart.md')
$contractsDir = 'contracts'
$taskPattern = '### Task T(\d+): (.+?)\n(.+?)(?=\n###|\n---|\n##|\Z)'

function Get-Artifacts {
    param([string]$Path)

    $artifacts = Get-ChildItem $Path -Filter "*.md" -Recurse |
        Where-Object { $_.Name -in $artifactNames }

    # Also include all .md files from contracts/ directory
    $contractsPath = Join-Path $Path $contractsDir
    if (Test-Path $contractsPath) {
        $contractsFiles = Get-ChildItem $contractsPath -Filter "*.md" -Recurse
        $artifacts += $contractsFiles
    }

    return $artifacts
}

function Get-Tasks {
    param([string]$TasksFilePath)

    if (!(Test-Path $TasksFilePath)) {
        throw "tasks.md not found at: $TasksFilePath"
    }

    $tasksContent = Get-Content $TasksFilePath -Raw
    $matches = [regex]::Matches($tasksContent, $taskPattern, 'Singleline')

    $tasks = $matches | ForEach-Object {
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

    return $tasks
}

function Search-Evidence {
    param(
        [PSCustomObject]$Task,
        [System.IO.FileInfo[]]$Artifacts
    )

    $evidence = @()
    $totalScore = 0
    $evidenceCount = 0

    foreach ($artifact in $Artifacts) {
        $content = Get-Content $artifact.FullName -Raw

        # Search for task title or key terms
        $titleMatch = $content | Select-String -Pattern $Task.Title -AllMatches
        $keyTerms = ($Task.Description -split ' ') | Where-Object { $_.Length -gt 3 } | Select-Object -First 5

        foreach ($term in $keyTerms) {
            $termMatch = $content | Select-String -Pattern $term -AllMatches
            if ($termMatch) {
                $evidence += "$($artifact.Name): Contains term '$term'"
                $evidenceCount++
            }
        }

        if ($titleMatch) {
            $evidence += "$($artifact.Name): Direct reference to task title"
            $evidenceCount += 2  # Higher weight for direct matches
        }
    }

    # Calculate grounding score (simplified algorithm)
    if ($evidenceCount -ge 4) { $totalScore = 100 }
    elseif ($evidenceCount -ge 3) { $totalScore = 90 }
    elseif ($evidenceCount -ge 2) { $totalScore = 80 }
    elseif ($evidenceCount -ge 1) { $totalScore = 70 }
    elseif ($evidenceCount -eq 0) { $totalScore = 20 }

    # Assess risk
    $risk = switch ($true) {
        ($totalScore -ge 90) { "Low" }
        ($totalScore -ge 70) { "Medium" }
        default { "High" }
    }

    # Identify gaps
    $gaps = @()
    if ($totalScore -lt 70) {
        $gaps += "Insufficient evidence found in planning artifacts"
    }
    if ($evidenceCount -eq 0) {
        $gaps += "No references found - task may be ungrounded assumption"
    }

    return @{
        Evidence = $evidence
        GroundingLevel = $totalScore
        Risk = $risk
        Gaps = $gaps
    }
}

function New-ValidationReport {
    param(
        [PSCustomObject[]]$Tasks,
        [string]$FeatureName,
        [string]$OutputPath
    )

    $date = Get-Date -Format "yyyy-MM-dd"
    $totalTasks = $tasks.Count
    $avgGrounding = [math]::Round(($tasks | Measure-Object -Property GroundingLevel -Average).Average, 1)

    $approvedTasks = ($tasks | Where-Object { $_.GroundingLevel -ge 80 }).Count
    $approvalRate = [math]::Round(($approvedTasks / $totalTasks) * 100, 1)

    $report = @"
# Task Grounding Analysis: $FeatureName
**Date**: $date | **Validator**: Automated Script
**Focus**: Grounding validation against planning artifacts

---

## Executive Summary

| Phase                 | Grounding Status     | Tasks     | Coverage                 | Next Action                 |
| --------------------- | -------------------- | --------- | ------------------------ | --------------------------- |
| Phase 1: Setup        | $(if ($approvalRate -ge 90) {"🟢 Mostly Documented"} elseif ($approvalRate -ge 70) {"🟡 Partially Inferred"} else {"🔴 Poorly Grounded"}) | T001-T$($totalTasks.ToString("D3")) | $approvedTasks/$totalTasks Fully | $(if ($approvalRate -ge 90) {"Ready to implement"} else {"Needs clarification"}) |

---

## Task Grounding Matrix

| Task                                                                                                    | Grounding Status                        | Primary Evidence                                                                                                                                                                                                           | Gaps                                            | Next Step                                             |
| ------------------------------------------------------------------------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------- |
"@

    foreach ($task in $tasks) {
        $status = switch ($true) {
            ($task.GroundingLevel -ge 80) { "🟢 **Documented**<br/>(Fully Grounded)" }
            ($task.GroundingLevel -ge 50) { "🟡 **Inferred**<br/>(Partially Grounded)" }
            default { "🔴 **Missing**<br/>(Ungrounded)" }
        }

        $evidence = if ($task.Evidence.Count -gt 0) {
            "• " + ($task.Evidence -join "<br>• ")
        } else {
            "None found"
        }

        $gaps = if ($task.Gaps.Count -gt 0) {
            $task.Gaps -join ", "
        } else {
            "None"
        }

        $nextStep = switch ($true) {
            ($task.GroundingLevel -ge 80) { "Ready to implement" }
            ($task.GroundingLevel -ge 50) { "**BLOCKED**: Needs clarification" }
            default { "**BLOCKED**: Requires specification" }
        }

        $report += @"

| **$($task.Id)**<br/>$($task.Title) | $status | $evidence | $gaps | $nextStep |"
    }

    $report += @"


## Observations

### Summary Statistics
- **Total Tasks**: $totalTasks
- **Average Grounding**: $avgGrounding%
- **Approval Rate**: $approvalRate%
- **High Risk Tasks**: $(($tasks | Where-Object { $_.Risk -eq "High" }).Count)

### Gaps Identified
"@

    $allGaps = $tasks | Where-Object { $_.Gaps.Count -gt 0 } | ForEach-Object { $_.Gaps } | Select-Object -Unique
    if ($allGaps.Count -gt 0) {
        foreach ($gap in $allGaps) {
            $report += "- $gap`n"
        }
    } else {
        $report += "- No significant gaps identified`n"
    }

    $decision = if ($approvalRate -ge 90) { "✅ APPROVE" } elseif ($approvalRate -ge 70) { "⚠️ NEEDS CLARIFICATION" } else { "🔴 BLOCK" }

    $report += @"

## Decision Gate

**Overall Assessment**: $decision
**Rationale**: $approvalRate% of tasks meet grounding thresholds
**Next Steps**:
1. Review high-risk tasks requiring clarification
2. Address identified gaps before implementation
3. Re-validate after gap resolution

**Validator**: Automated Script | **Date**: $date
"@

    $report | Out-File -FilePath $OutputPath -Encoding UTF8
    Write-Host "Validation report generated: $OutputPath"
}

# Main execution
try {
    Write-Host "Starting task grounding validation for: $FeaturePath"

    # Validate feature path
    if (!(Test-Path $FeaturePath)) {
        throw "Feature path not found: $FeaturePath"
    }

    # Load artifacts
    $artifacts = Get-Artifacts -Path $FeaturePath
    Write-Host "Found $($artifacts.Count) planning artifacts"

    # Extract tasks
    $tasksFile = Join-Path $FeaturePath "tasks.md"
    $tasks = Get-Tasks -TasksFilePath $tasksFile
    Write-Host "Found $($tasks.Count) tasks to validate"

    # Filter tasks if specified
    if ($TaskFilter) {
        $filterIds = $TaskFilter -split ',' | ForEach-Object { $_.Trim() }
        $tasks = $tasks | Where-Object { $_.Id -in $filterIds }
        Write-Host "Filtered to $($tasks.Count) tasks: $($filterIds -join ', ')"
    }

    # Validate each task (sequential for simplicity - could be parallel)
    foreach ($task in $tasks) {
        Write-Host "Validating $($task.Id): $($task.Title)"
        $result = Search-Evidence -Task $task -Artifacts $artifacts

        $task.Evidence = $result.Evidence
        $task.GroundingLevel = $result.GroundingLevel
        $task.Risk = $result.Risk
        $task.Gaps = $result.Gaps
    }

    # Generate output
    $featureName = Split-Path $FeaturePath -Leaf

    if ($JsonOutput) {
        # Ensure validation directory exists
        $outputDir = Split-Path $OutputPath -Parent
        if (!(Test-Path $outputDir)) {
            New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
        }

        # Output JSON format for aggregation
        $jsonOutput = @{
            FeatureName = $featureName
            ValidationDate = Get-Date -Format "yyyy-MM-dd"
            Tasks = $tasks
        } | ConvertTo-Json -Depth 10

        $jsonOutput | Out-File -FilePath $OutputPath -Encoding UTF8
        Write-Host "JSON assessment generated: $OutputPath"
    } else {
        # Generate markdown report
        New-ValidationReport -Tasks $tasks -FeatureName $featureName -OutputPath $OutputPath
    }

    Write-Host "Validation complete!"

} catch {
    Write-Error "Validation failed: $_"
    exit 1
}