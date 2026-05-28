---
name: ccw
description: Use this skill when you need a stateless workflow orchestrator that automatically selects the optimal workflow based on task intent.
---

# Skill body

## Overview

CCW (Claude Code Workflow) is a stateless workflow orchestrator designed to streamline the software development lifecycle by automatically selecting the most suitable workflow based on the task intent.

## Allowed Tools

- Task(*)
- SlashCommand(*)
- AskUserQuestion(*)
- Read(*)
- Bash(*)
- Grep(*)
- TodoWrite(*)

## Workflow Systems

CCW provides two main workflow systems: **Main Workflow** and **Issue Workflow**.

### Main Workflow

The Main Workflow consists of four levels, each designed to handle different complexities of tasks:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Main Workflow                                  │
│                                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐     │
│  │   Level 1   │ → │   Level 2   │ → │   Level 3   │ → │   Level 4   │     │
│  │   Rapid     │   │ Lightweight │   │  Standard   │   │ Brainstorm  │     │
│  │             │   │             │   │             │   │             │     │
│  │ lite-lite-  │   │ lite-plan   │   │    plan     │   │ brainstorm  │     │
│  │    lite     │   │ lite-fix    │   │  tdd-plan   │   │  :auto-     │     │
│  │             │   │ multi-cli-  │   │ test-fix-   │   │  parallel   │     │
│  │             │   │    plan     │   │    gen      │   │     ↓       │     │
│  └─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘     │
│                                                                             │
│  Complexity: ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━▶  │
│              Low                                                    High    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Issue Workflow

The Issue Workflow is designed for post-development processes and consists of three stages:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Issue Workflow                                 │
│                                                                             │
│     ┌──────────────┐         ┌──────────────┐         ┌──────────────┐     │
│     │  Accumulate  │    →    │    Plan      │    →    │   Execute    │     │
│     │  Discover &  │         │    Batch     │         │   Parallel   │     │
│     │   Collect    │         │   Planning   │         │  Execution   │     │
│     └──────────────┘         └──────────────┘         └──────────────┘     │
└─────────────────────────────────────────────────────────────────────────────┘
```