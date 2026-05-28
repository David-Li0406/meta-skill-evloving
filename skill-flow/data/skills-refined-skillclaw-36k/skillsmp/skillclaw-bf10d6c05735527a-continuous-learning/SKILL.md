---
name: continuous-learning
description: Use this skill when you want to capture non-obvious solutions and insights gained from debugging, experimentation, or trial-and-error, ensuring that valuable knowledge is retained for future use.
---

# Continuous Learning Skill

## Overview

The Continuous Learning Skill enables agents to autonomously extract reusable patterns from debugging discoveries. This skill captures high-value insights as structured documents, preventing the loss of knowledge at the end of a session.

### Problem Addressed

Agents often discover non-obvious solutions during debugging, but this knowledge can be lost when:
- Context windows compact or clear
- Sessions end without explicit knowledge capture
- Similar problems are re-investigated from scratch

The Continuous Learning Skill transforms ephemeral discoveries into persistent, retrievable knowledge.

## Activation Triggers

The skill activates when ANY of these conditions are detected:

### Trigger 1: Non-Obvious Solution Discovery

Agent completed debugging where the solution wasn't immediately apparent from the error message or documentation.

**Signals**:
- Multiple investigation steps before resolution
- Solution differs from first hypothesis
- Required reading source code or experimentation

### Trigger 2: Workaround Through Investigation

Agent found a workaround through trial-and-error or systematic investigation rather than known solutions.

**Signals**:
- Tested multiple approaches before success
- Solution involved undocumented behavior
- Required combining information from multiple sources

### Trigger 3: Non-Apparent Root Cause

Agent resolved an error where the root cause wasn't clear from initial symptoms.

**Signals**:
- Error message was misleading or generic
- Actual cause was upstream of reported location
- Required tracing through multiple layers