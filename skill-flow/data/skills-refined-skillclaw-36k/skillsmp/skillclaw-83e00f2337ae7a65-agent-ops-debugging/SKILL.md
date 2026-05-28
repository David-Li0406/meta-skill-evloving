---
name: agent-ops-debugging
description: Use this skill when something isn't working and the cause is unclear, to systematically isolate and fix software defects.
---

# Skill body

## Purpose

Systematic problem isolation, root cause analysis, and defect resolution. Use when something isn't working and the cause is unclear.

## Core Principles

### 1. Understand Before Acting

- **Reproduce the issue**: Can you consistently trigger the problem?
- **Define expected vs actual**: What should happen vs what is happening?
- **Gather context**: When does this occur? Under what conditions?
- **Recent changes**: What changed before this appeared?

### 2. Isolate the Problem

- **Binary search**: Comment out half the code, test, repeat.
- **Minimize reproduction**: Create a minimal test case.
- **Control variables**: Change one thing at a time.
- **Eliminate noise**: Remove unrelated factors.

### 3. Form Hypotheses

- **State your assumption**: "I believe X is causing Y because..."
- **Make predictions**: "If my hypothesis is true, then Z should happen."
- **Test predictions**: Verify or refute each hypothesis.
- **Iterate**: Refine hypothesis based on evidence.

### 4. Fix and Verify

- **Address root cause**: Not just symptoms.
- **Minimize changes**: Smallest fix that resolves the issue.
- **Add tests**: Prevent regression.
- **Verify fix**: Test the specific scenario and related scenarios.

## Systematic Debugging Process

### Phase 1: Problem Definition

1. **Describe the bug** in one sentence.
2. **List reproduction steps** (minimal set).
3. **Specify expected behavior**.
4. **Capture actual behavior** (screenshots, logs, error messages).
5. **Identify scope**: How widespread is this?

### Phase 2: Information Gathering

1. **Check logs**: Application logs, system logs, crash reports.
2. **Inspect state**: Database records, cache contents, file system.
3. **Review code**: Recent changes, related code paths.
4. **Compare environments**: Dev vs staging vs production differences.
5. **Monitor resources**: CPU, memory, disk, network during the issue.

### Phase 3: Hypothesis Formation

Common failure patterns:

| Pattern | Symptoms | Where to Look |
|---------|----------|----------------|