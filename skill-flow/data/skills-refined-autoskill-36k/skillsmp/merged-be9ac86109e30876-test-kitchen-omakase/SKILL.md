---
name: test-kitchen-omakase
description: Use this skill when you want to explore multiple design or implementation approaches in parallel for a feature or project.
---

# Test Kitchen Omakase

This skill facilitates parallel exploration of design and implementation approaches when building features. It combines brainstorming and decision-making processes to help users navigate uncertainty and indecision.

## Core Principles

- **Indecision Detection**: Recognizes when users are uncertain about architectural decisions and offers to explore multiple approaches.
- **Parallel Exploration**: Implements several designs or plans simultaneously, allowing tests to determine the best solution.

## Workflow Overview

| Phase | Description |
|-------|-------------|
| **0. Entry** | Present options for brainstorming or omakase choice |
| **1. Brainstorm** | Engage in collaborative design discussions |
| **1.5. Decision** | Detect indecision and offer parallel exploration |
| **2. Plan** | Generate implementation plans for each variant |
| **3. Implement** | Dispatch all agents in a single message |
| **4. Evaluate** | Run tests and review results |
| **5. Complete** | Finalize the winning approach and clean up |

## Triggers

### Trigger 1: BEFORE Brainstorming

**When:** User expresses intent to build, create, or implement something.

**Response:**
```
Before we brainstorm, would you like to:
1. Brainstorm together - We'll explore requirements and design step by step.
2. Omakase (chef's choice) - I'll generate 3-5 best approaches and implement them in parallel.
```

### Trigger 2: DURING Brainstorming (Indecision Detection)

**Detection Signals:**
- Multiple uncertain responses on architectural decisions.
- Phrases like "not sure", "either works", "you pick".

**Response:**
```
You seem flexible on the approach. Would you like to:
1. I'll pick what seems best and continue brainstorming.
2. Explore multiple approaches in parallel (omakase).
```

### Trigger 3: Explicitly Requested

- User explicitly asks to try both approaches or explore multiple options.

## Omakase Mode

If the user opts for "Omakase":
1. Quick context gathering (1-2 questions).
2. Generate 3-5 best architectural approaches.
3. Implement all in parallel.
4. Tests determine the winner.

## Cookoff Mode

If the user opts for "Cookoff" after design:
1. Each agent reads the same design document.
2. Each agent creates their own implementation plan.
3. All implement in parallel.
4. Compare results and select a winner.

## Slot Classification

| Type | Examples | Worth Exploring? |
|------|----------|------------------|
| **Architectural** | Storage engine, framework, auth method | Yes |
| **Trivial** | File location, naming, config format | No |

Only architectural decisions become slots for parallel exploration.

## Critical Rules

1. **Dispatch ALL variants in a SINGLE message**.
2. **MUST use scenario-testing** for evaluation.
3. **Fresh-eyes review** on survivors before final judgment.
4. **Always clean up losers** after evaluation.
5. **Document results** in a final report.

## Example Flow

```
User: "I need to build a CLI todo app."

Claude: [Triggers omakase]
Before we dive in, how would you like to approach this?
1. Brainstorm together
2. Omakase (chef's choice)

User: "1"

Claude: [Brainstorming proceeds, detects indecision on storage]

You seem flexible on storage (JSON vs SQLite). Would you like to:
1. Explore in parallel - I'll implement both variants.
2. Best guess - I'll pick JSON (simpler).

User: "1"

[Creates plans for variant-json, variant-sqlite]
[Dispatches parallel agents in SINGLE message]
[Runs scenario tests on both]
[Fresh-eyes review on survivors]
[Presents comparison, user picks winner]
[Cleans up loser, finishes winner branch]
```