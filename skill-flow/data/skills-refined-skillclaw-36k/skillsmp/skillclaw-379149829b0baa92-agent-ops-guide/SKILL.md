---
name: agent-ops-guide
description: Use this skill when you are unsure what to do next, need help navigating AgentOps, or want to understand available tools.
---

# AgentOps Workflow Guide

## Purpose

Help users navigate the AgentOps workflow by asking diagnostic questions and recommending the appropriate next step.

## When to Use

- User says "help", "what should I do", "where do I start"
- User seems lost or confused about workflow
- User wants to understand available tools
- First time using AgentOps in a project

## Diagnostic Procedure

### Step 1: Assess State Files

First, silently check which state files exist:

```
□ .agent/constitution.md  → Project setup complete?
□ .agent/baseline.md      → Baseline captured?
□ .agent/focus.md         → Has session context?
□ .agent/issues/          → Has defined issues?
□ .agent/memory.md        → Has learned conventions?
```

### Step 2: Ask Situational Question

Ask ONE question to understand user's intent:

> "What brings you here today?"
> 
> **A)** Starting a new project or first time here  
> **B)** Returning to continue previous work  
> **C)** Have a specific task or feature to implement  
> **D)** Something's broken and need to fix it  
> **E)** Want to explore or understand the codebase  
> **F)** Need to review code quality  
> **G)** Wrapping up work, ready to commit  
> **H)** Want to create a new Python project  
> **I)** Need to review/audit an API  

### Step 3: Recommend Based on State + Intent

| Intent | Missing Constitution | Missing Baseline | Has Tasks | Recommendation |
|--------|---------------------|------------------|-----------|----------------|
| A (new) | ✗ | — | — | `/agent-init` then `/agent-constitution` |
| A (new) | ✓ | ✗ | — | `/agent-baseline` |
| B (resume) | — | — | — | Read focus.md, summarize status |
| C (task) | ✗ | — | — | `/agent-constitution` first |
| C (task) | ✓ | ✗ | — | `/agent-baseline` first |
| C (task) | ✓ | ✓ | ✗ | `/agent-task` to define task |
| C (task) | ✓ | ✓ | ✓ | `/agent-plan` for next task |
| D (broken) | — | — | — | `/agent-debug` then `/agent-recover` |
| E (explore) | — | — | — | `/agent-map` or `agent-ops-critical-review` |
| F (review) | — | — | — | `/agent-review` or `/agent-validation` |
| G (finish) | — | ✗ | — | `/agent-baseline` then `/agent-review` |
| G (finish) | — | ✓ | — | `/agent-validation` |