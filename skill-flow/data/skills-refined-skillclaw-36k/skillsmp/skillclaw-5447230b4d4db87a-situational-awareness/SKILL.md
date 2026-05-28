---
name: situational-awareness
description: Use this skill when you need to assess the current context and determine the appropriate actions based on the situation.
---

# Skill body

## Overview

This skill helps in recognizing the current situation by processing incoming information and determining the necessary actions based on context and urgency.

## When to Use

- When a new message is received.
- At the start of a session.
- When the context is unclear.
- When there are changes in relevant files or IDE state.

## When Not to Use

- When the situation is already understood and you are in the decision-making phase.
- During the execution of a clear task.

## Core Function

The skill's primary role is to structure environmental signals and assign meaning to them, allowing for informed decision-making.

## Processing Logic

1. **Input Reception**
   - Collect user input.
   - Scan relevant history (default: last 7 days).
   - Retrieve the current context and IDE state.

2. **Structuring Information**
   - Identify temporal context.
   - Extract ongoing tasks.
   - Detect entities.

3. **Meaning Inference**
   - Classify the situation into labels (urgent, decision required, information gathering, reflection, routine).
   - Calculate an uncertainty score (U) ranging from 0 to 1.

4. **Output Generation**
   - Based on the uncertainty score, determine the next steps:
     - If U < 0.3, proceed to decision-making.
     - If 0.3 ≤ U < 0.6, recommend further exploration.
     - If U ≥ 0.6, initiate an exploration phase to gather more information.

## Input / Output

### Input

- User input (text)
- Chat history (Markdown)
- Relevant files (optional)
- IDE state (JSON)
- Timestamp (ISO 8601)

### Output

- Situation label (Enum)
- Context summary (text)
- Detected entities (JSON)
- Uncertainty score (Float)
- Observation history (JSON)

## Situation Classification

| Label                | Criteria                                      | Example                          |
|----------------------|-----------------------------------------------|----------------------------------|
| **urgent**           | Explicit urgent keywords or deadline < 24h   | "Now", "Urgent", "By today"     |
| **decision_required**| Options presented or in question form        | "Which should I choose, A or B?"|
| **information_gathering** | Research or inquiry keywords            | "Find out", "Tell me", "What is"|
| **reflection**       | Reflective keywords                           | "Review", "Summarize"           |
| **routine**          | None of the above                            | Normal task request              |

## Edge Cases / Failure Modes

- **Failure to Recognize Context**: If the context cannot be determined, prompt the user for clarification.
- **High Uncertainty**: If the uncertainty score is high, initiate an exploration phase to gather more information.

This skill integrates the functionalities of Aisthēsis, Krisis, and Peira to provide a comprehensive approach to situational awareness and decision-making.