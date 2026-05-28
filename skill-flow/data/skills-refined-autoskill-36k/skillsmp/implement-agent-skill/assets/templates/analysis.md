---
name: analyze-[subject]
description: [Action] [Context] to identify issues or patterns. Use when [User Trigger].
license: Apache-2.0
metadata:
  author: [Author]
  version: "1.0"
---

# [Subject] Analysis

This skill provides a framework for investigating [Subject].

## When to use this skill

Use this skill when the task requires [Type of Analysis] (e.g., investigating [Problem], auditing [Subject]).

## Investigation Strategy

1.  **Symptom Matching**:
    - If [Symptom A], check [Log File 1].
    - If [Symptom B], check [Service Status].

2.  **Data Gathering**:
    - Run `grep [Pattern] [File]` to find errors.
    - Use `curl` to test endpoints.

## Evaluation Criteria

- **Critical**: Service is down or data loss risk.
- **Warning**: Performance degradation.
- **Info**: Configuration noise.

## Report Format

Produce a report in the following structure:

### Executive Summary

[Brief overview]

### Findings

- **Issue 1** (Severity: [Level]): [Description]
  - _Evidence_: [Log snippet]
  - _Recommendation_: [Fix]

## Progressive Disclosure

If analysis requires specific scripts, place them in `scripts/`. Large datasets or log samples should be referenced via `assets/`.
