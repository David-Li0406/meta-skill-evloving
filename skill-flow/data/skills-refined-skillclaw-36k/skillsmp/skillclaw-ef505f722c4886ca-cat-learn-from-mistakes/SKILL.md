---
name: cat:learn-from-mistakes
description: Use this skill when analyzing mistakes in CAT orchestration, particularly focusing on conversation length and context degradation.
---

# Skill body

## Purpose

Analyze mistakes using the 5-whys technique with CAT-specific consideration of conversation length and context degradation. This skill integrates token tracking to identify context-related failures and recommend preventive measures.

## When to Use

- Any mistake during CAT orchestration
- Subagent produces incorrect or incomplete results
- Task requires rework or correction
- Build, test, or logical errors
- Repeated attempts at the same operation
- Quality degradation over time

## Workflow

### 1. Verify Event Sequence (MANDATORY)

**CRITICAL: Do NOT rely on memory for root cause analysis.**

Verify the actual event sequence using `get-history`:

```bash
/cat:get-history
# Look for: When stated? Action order? User corrections? Actual trigger?
```

**Anti-Pattern (M037):** Avoid root cause analysis based on memory without `get-history` verification, as memory can be unreliable for causation, timing, and attribution.

**If `get-history` is unavailable:** Document analysis based on the current context only; it may be incomplete.

### 2. Document the Mistake

```yaml
mistake:
  timestamp: 2026-01-10T16:30:00Z
  type: incorrect_implementation
  description: |
    Subagent implemented parser with wrong precedence rules.
    Expressions like "a + b * c" parsed as "(a + b) * c" instead of "a + (b * c)".
  impact: |
    All tests using operator precedence failing. Required complete rewrite.
```

### 3. Gather Context Metrics

**CAT-specific: Always collect token data**

```bash
SESSION_ID="${SUBAGENT_SESSION}"
SESSION_FILE="/home/node/.config/claude/projects/-workspace/${SESSION_ID}.jsonl"

TOKENS_AT_ERROR=$(jq -s 'map(select(.type == "assistant")) |
  map(.message.usage | .input_tokens + .output_tokens) | add' "${SESSION_FILE}")
COMPACTIONS=$(jq -s '[.[] | select(.type == "summary")] | length' "${SESSION_FILE}")
MESSAGE_COUNT=$(jq -s '[.[] | select(.type == "assistant")] | length' "${SESSION_FILE}")
SESSION_DURATION=$(calculate_duration "${SESSION_FILE}")
```

### 4. Perform Root Cause Analysis

**A/B TEST IN PROGRESS** - See [RCA-AB-TEST.md](RCA-AB-TEST.md) for full specification.

**Method Assignment Rule:** Use mistake ID modulo 3:
- IDs ending in 6, 9, 2, 5, 8 (mod 3 = 0) → Method A (5-Whys)
- IDs ending in 7, 0, 3 (mod 3 = 1) → Method B (Taxonomy)
- IDs ending in 8, 1, 4 (mod 3 = 2) → Method C (Causal Barrier)