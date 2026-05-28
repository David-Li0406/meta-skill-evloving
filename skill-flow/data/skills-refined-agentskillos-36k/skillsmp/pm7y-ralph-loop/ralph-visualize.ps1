#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Visualizes Claude CLI stream-json output with colors and formatting.

.DESCRIPTION
    Reads JSON lines from stdin (Claude's --output-format=stream-json) and displays
    formatted, colorized output. Pairs tool calls with their results and provides
    concise summaries of operations.

.PARAMETER ShowTimestamps
    Show timestamps for each message

.EXAMPLE
    claude -p "hello" --output-format=stream-json | ./ralph-visualize.ps1

.EXAMPLE
    Get-Content log.jsonl | ./ralph-visualize.ps1 -ShowTimestamps
#>

[CmdletBinding()]
param(
    [Parameter(ValueFromPipeline)]
    [string]$InputLine,

    [switch]$ShowTimestamps
)

begin {
    # Ensure UTF-8 output for proper character display
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8

    # Track tool calls to pair with results
    $script:toolCalls = @{}
    $script:lastText = ""

    function Format-ToolInput {
        param([string]$ToolName, $ToolInput)

        if (-not $ToolInput) { return "" }

        # Helper to safely get property
        function Get-Prop { param($Obj, $Name) if ($Obj.PSObject.Properties[$Name]) { $Obj.$Name } else { $null } }

        $summary = switch ($ToolName) {
            "Read" {
                $fp = Get-Prop $ToolInput "file_path"
                if ($fp) { Split-Path $fp -Leaf } else { "" }
            }
            "Write" {
                $fp = Get-Prop $ToolInput "file_path"
                $content = Get-Prop $ToolInput "content"
                $len = if ($content) { $content.Length } else { 0 }
                if ($fp) { "$(Split-Path $fp -Leaf) ($len chars)" } else { "($len chars)" }
            }
            "Edit" {
                $fp = Get-Prop $ToolInput "file_path"
                if ($fp) { Split-Path $fp -Leaf } else { "" }
            }
            "Bash" {
                $desc = Get-Prop $ToolInput "description"
                $cmd = Get-Prop $ToolInput "command"
                if ($desc) {
                    $desc
                } elseif ($cmd) {
                    if ($cmd.Length -gt 60) { $cmd.Substring(0, 57) + "..." } else { $cmd }
                } else { "" }
            }
            "Glob" {
                $pattern = Get-Prop $ToolInput "pattern"
                $path = Get-Prop $ToolInput "path"
                if ($pattern) { "$pattern in $($path ?? '.')" } else { "" }
            }
            "Grep" {
                $pattern = Get-Prop $ToolInput "pattern"
                $path = Get-Prop $ToolInput "path"
                if ($pattern) { "`"$pattern`" in $($path ?? '.')" } else { "" }
            }
            "Task" {
                $type = Get-Prop $ToolInput "subagent_type"
                $desc = Get-Prop $ToolInput "description"
                if ($type) { "${type}: $desc" } else { $desc ?? "" }
            }
            "WebFetch"    { Get-Prop $ToolInput "url" }
            "WebSearch"   { Get-Prop $ToolInput "query" }
            "TodoWrite"   {
                $todos = Get-Prop $ToolInput "todos"
                Format-TodoList $todos
            }
            "AskUserQuestion" {
                $questions = Get-Prop $ToolInput "questions"
                if ($questions) {
                    ($questions | ForEach-Object { $_.question }) -join "; "
                } else { "question" }
            }
            default {
                # Generic: show first property value
                try {
                    if ($ToolInput.PSObject -and $ToolInput.PSObject.Properties.Count -gt 0) {
                        $first = $ToolInput.PSObject.Properties | Select-Object -First 1
                        $val = "$($first.Value)"
                        if ($val.Length -gt 60) { $val.Substring(0, 57) + "..." } else { $val }
                    } else { "" }
                } catch { "" }
            }
        }

        return $summary
    }

    function Format-TodoList {
        param($Todos)

        if (-not $Todos -or $Todos.Count -eq 0) { return "(empty)" }

        $completed = @($Todos | Where-Object { $_.status -eq "completed" }).Count
        $inProgress = @($Todos | Where-Object { $_.status -eq "in_progress" }).Count
        $total = $Todos.Count

        return "$completed/$total done, $inProgress active"
    }

    function Format-ToolResult {
        param($Content, $IsError)

        # Handle is_error which might be bool, string, or missing
        if ($IsError -eq $true -or $IsError -eq "true") {
            return "ERROR"
        }

        if (-not $Content) { return "OK" }

        if ($Content -is [string]) {
            $lines = $Content.Split("`n").Count
            $chars = $Content.Length
            if ($lines -gt 3 -or $chars -gt 100) {
                return "$lines lines, $chars chars"
            }
            return $Content.Trim().Substring(0, [Math]::Min(80, $Content.Trim().Length))
        }

        return "OK"
    }

    function Get-Timestamp {
        return [DateTime]::Now.ToString("HH:mm:ss")
    }

    function Write-Prefix {
        param([string]$Icon, [string]$Color)
        $ts = if ($ShowTimestamps) { "[$(Get-Timestamp)] " } else { "" }
        Write-Host "$ts$Icon " -ForegroundColor $Color -NoNewline
    }
}

process {
    $line = $InputLine

    # Skip empty lines
    if ([string]::IsNullOrWhiteSpace($line)) { return }

    try {
        $msg = $line | ConvertFrom-Json -ErrorAction Stop
    }
    catch {
        # Not JSON, print as-is
        Write-Host $line -ForegroundColor Gray
        return
    }

    # Handle different message types from Claude CLI stream-json

    switch ($msg.type) {
        "system" {
            # System messages
            if ($msg.subtype -eq "init") {
                $model = $msg.model ?? "unknown"
                Write-Prefix "[SYS]" "Magenta"
                Write-Host "Session: $model ($($msg.num_turns ?? 0) tools available)"
            }
            elseif ($msg.subtype -eq "hook_started") {
                # Skip hook started messages (too noisy)
            }
            elseif ($msg.subtype -eq "hook_response") {
                # Only show hook errors
                if ($msg.outcome -eq "error") {
                    Write-Prefix "[HOOK]" "DarkYellow"
                    Write-Host "$($msg.hook_name): error (exit $($msg.exit_code))"
                }
            }
            elseif ($msg.message) {
                Write-Prefix "[SYS]" "Magenta"
                Write-Host $msg.message
            }
        }

        "assistant" {
            # Assistant messages - content is in msg.message.content
            $content = $msg.message.content
            if (-not $content) { return }

            foreach ($block in $content) {
                if ($block.type -eq "text" -and $block.text) {
                    $text = $block.text.Trim()
                    # Dedupe repeated text
                    if ($text -and $text -ne $script:lastText) {
                        Write-Prefix "[AI]" "Green"
                        if ($text.Length -gt 200) {
                            Write-Host "$($text.Substring(0, 197))..."
                        } else {
                            Write-Host $text
                        }
                        $script:lastText = $text
                    }
                }
                elseif ($block.type -eq "tool_use") {
                    # Store tool call for pairing with result
                    $script:toolCalls[$block.id] = @{
                        name = $block.name
                        input = $block.input
                    }

                    $summary = Format-ToolInput $block.name $block.input
                    Write-Prefix "[>>>]" "Cyan"
                    Write-Host "$($block.name): $summary"
                }
            }
        }

        "user" {
            # User messages - tool results are in msg.message.content
            $content = $msg.message.content
            if (-not $content) { return }

            foreach ($block in $content) {
                if ($block.type -eq "tool_result") {
                    $toolId = $block.tool_use_id
                    $call = $script:toolCalls[$toolId]
                    $resultSummary = Format-ToolResult $block.content $block.is_error

                    if ($call) {
                        Write-Prefix "[<<<]" "Yellow"
                        Write-Host "$($call.name) -> $resultSummary"
                        $script:toolCalls.Remove($toolId)
                    }
                    else {
                        Write-Prefix "[<<<]" "Yellow"
                        Write-Host $resultSummary
                    }
                }
                elseif ($block.type -eq "text" -and $block.text) {
                    # User text (the prompt)
                    $text = $block.text.Trim()
                    if ($text.Length -gt 100) {
                        $text = $text.Substring(0, 97) + "..."
                    }
                    Write-Prefix "[USR]" "Blue"
                    Write-Host $text
                }
            }
        }

        "result" {
            # Final result
            Write-Host ""
            if ($msg.subtype -eq "success") {
                $duration = [math]::Round($msg.duration_ms / 1000, 1)
                $turns = $msg.num_turns
                $cost = if ($msg.total_cost_usd) { [math]::Round($msg.total_cost_usd, 4) } else { 0 }

                $inputTokens = 0
                $outputTokens = 0
                if ($msg.usage) {
                    $inputTokens = $msg.usage.input_tokens + $msg.usage.cache_read_input_tokens + $msg.usage.cache_creation_input_tokens
                    $outputTokens = $msg.usage.output_tokens
                }

                Write-Prefix "[END]" "White"
                Write-Host "Completed: $turns turns, ${duration}s, `$$cost"
                Write-Host "      Tokens: $inputTokens in / $outputTokens out" -ForegroundColor DarkGray
            }
            elseif ($msg.subtype -eq "error") {
                Write-Prefix "[ERR]" "Red"
                Write-Host ($msg.error ?? "Unknown error")
            }
        }

        "error" {
            Write-Prefix "[ERR]" "Red"
            Write-Host ($msg.message ?? $msg.error ?? "Unknown error")
        }

        default {
            # Unknown - skip silently
            # Uncomment for debugging:
            # Write-Host "[???] $($msg.type)" -ForegroundColor DarkGray
        }
    }
}
