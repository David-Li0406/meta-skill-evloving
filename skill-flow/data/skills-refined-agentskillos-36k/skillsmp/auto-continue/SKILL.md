---
name: auto-continue
description: Intelligent auto-continuation skill for Claude Code sessions. Use when working on extended tasks requiring minimal interruption, continuous development workflows, or Ralph Loop style iterations.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite
user-invocable: true
---

# Auto-Continue Skill

This skill enables intelligent auto-continuation for Claude Code sessions based on confidence scoring. It's designed to work seamlessly with Ralph Loop and extended development workflows.

## How It Works

1. **Confidence Scoring**: Each response is evaluated for continuation confidence
2. **Threshold Comparison**: Score compared against user's threshold (default: 80%)
3. **Auto-Proceed**: If confidence >= threshold, automatically selects "Yes"
4. **Safety Guards**: Dangerous operations always prompt the user

## Confidence Factors

### Positive Signals (Increase Confidence)
- Completed tasks and milestones
- Passing tests
- Successful builds
- Progress indicators
- Todo items marked complete

### Negative Signals (Decrease Confidence)
- Errors or failures
- Ambiguous requirements
- Multiple choice decisions
- Destructive operations
- Security-sensitive changes

## Usage Patterns

### Extended Development Sessions
Perfect for long coding sessions where you want Claude to continue working with minimal interruption.

### Ralph Loop Integration
Works naturally with Ralph Loop for infinite iteration cycles with intelligent stopping.

### Farm Monitoring (MaiFarm)
Ideal for autonomous farm agents that need to continue processing without manual intervention.

## Safety Features

- Never auto-approves destructive commands
- Respects excluded patterns
- Always logs decisions for audit
- User can override via settings

## Configuration

Set threshold via environment variable:
```bash
export INFERENCE_CONTINUEZ_THRESHOLD=85
```

Or via settings file in plugin root.
