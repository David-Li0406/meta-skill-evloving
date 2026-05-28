---
name: perception-strategy-memory
description: Use this skill when you need to recognize situations, design strategies, and manage long-term memory.
---

# Body of the merged SKILL.md

## Overview

This skill integrates perception, strategy formulation, and memory management to assist in recognizing situations, designing actionable strategies, and managing long-term memory storage and retrieval.

---

## Core Functions

### 1. Perception (Aisthēsis)

**Role:** Recognize and infer the current situation based on environmental signals.

**Triggers:**
- New message received
- Session start
- Context unclear
- File changes

**Processing Logic:**
1. **Input Collection:** Gather user input, scan relevant history, and retrieve current context.
2. **Structuring:** Identify temporal context and extract ongoing tasks.
3. **Meaning Inference:** Classify situation labels and calculate uncertainty scores.
4. **Output:** Send situation labels and context summaries to relevant modules.

### 2. Strategy Formulation (Phronēsis)

**Role:** Design strategies based on long-term goals.

**Triggers:**
- How-to questions
- Complex task decomposition
- Options comparison
- Strategy planning

**Processing Logic:**
1. **Goal Clarification:** Extract and define the goal from user input.
2. **Current State Analysis:** Define the current state and identify gaps.
3. **Strategy Design:** Enumerate paths to bridge the gap and evaluate them.
4. **Execution Planning:** Break down the chosen path into milestones and send to relevant modules.

### 3. Memory Management (Anamnēsis)

**Role:** Manage the storage and retrieval of long-term memory.

**Triggers:**
- Session end
- Important event detected
- Memory retrieval needed

**Processing Logic:**
1. **Save Mode:** Evaluate the importance of information and save it to the vault if it meets the threshold.
2. **Recall Mode:** Analyze queries, search the vault, and provide relevant memories to other modules.

---

## Input / Output

### Perception Input
- User utterance (text)
- Chat history (Markdown)
- File/code (optional)
- IDE state (JSON)
- Date/time (ISO 8601)

### Perception Output
- Situation label (Enum)
- Context summary (text)
- Detected entities (JSON)
- Uncertainty score (Float)
- Observation history (JSON)

### Strategy Input
- User queries regarding planning or strategy
- Current goals and constraints

### Strategy Output
- Proposed strategies
- Milestone breakdown

### Memory Input
- Events and decisions made during sessions
- User requests to remember information

### Memory Output
- Archived records in the vault
- Retrieved memories based on queries

---

## Configuration

```yaml
# Perception Configuration
history_scan_days: 7
entity_confidence_threshold: 0.5
uncertainty_threshold: 0.6
max_context_summary_length: 500

# Strategy Configuration
max_paths_to_evaluate: 5
min_feasibility_score: 0.4
force_top_n: 3

# Memory Configuration
importance_threshold: 0.5
max_vault_size_mb: 100
compression_enabled: true
```

---

## Edge Cases / Failure Modes

### Perception
- **Failure:** Empty input
  - **Response:** Infer context from IDE state only.

### Strategy
- **Failure:** Goal unclear
  - **Response:** Prompt user for clarification.

### Memory
- **Failure:** Vault access failure
  - **Response:** Temporarily store in session memory.

---

## Test Cases

### Perception Test
- **Input:** "What should I do now?"
- **Expected Output:** Situation label and context summary.

### Strategy Test
- **Input:** "How should I proceed with this project?"
- **Expected Output:** Proposed strategy and milestones.

### Memory Test
- **Input:** Session end with important events.
- **Expected Output:** Save events to vault.

---

This skill provides a comprehensive approach to recognizing situations, formulating strategies, and managing memory, ensuring effective decision-making and planning.