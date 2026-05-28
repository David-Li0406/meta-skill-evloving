# Auto-Routing

Intent-based workflow selection from natural language prompts.

## Contents

- Architecture
- Shared Logic Pattern
- Signal Detection Per Workflow
- Routing Algorithm
- Score Calculation
- Confidence Threshold
- Ambiguity Gate
- Default Fallback Behavior
- Edge Cases

## Architecture

**Auto-routing lives in the skill (SKILL.md), not the MCP router.** The MCP research router only executes workflows; it does not analyze intent.

## Shared Logic Pattern

Both command and skill use the same routing logic:

```
commandsfoundry-research.md           skillsfoundry-research/SKILL.md
        │                              │
        └──────────┬───────────────────┘
                   │
           Auto-Route Logic
                   │
        ┌──────────┴──────────┐
        │   Signal Detection  │
        │   Score Calculation │
        │   Threshold Check   │
        │   Ambiguity Gate    │
        └─────────────────────┘
```

## Signal Detection Per Workflow

| Workflow | Signal Patterns | Example Triggers |
|----------|-----------------|------------------|
| `chat` | Follow-up markers, pronouns referencing prior context | "tell me more", "what about...", "and also" |
| `consensus` | Comparison, validation, multiple viewpoints | "best approach", "compare", "which is better", "opinions on" |
| `thinkdeep` | Problem investigation, root cause, debugging | "why is", "how come", "root cause", "debug", "investigate" |
| `ideate` | Creative, brainstorming, possibilities | "ideas for", "how might we", "brainstorm", "creative ways" |
| `deep` | Comprehensive research, multiple sources, thorough | "research", "comprehensive", "in-depth", "survey of", "state of the art", "literature review" |

## Routing Algorithm

```python
def auto_route(prompt: str) -> tuple[str, float]:
    scores = {
        'chat': score_chat_signals(prompt),
        'consensus': score_consensus_signals(prompt),
        'thinkdeep': score_thinkdeep_signals(prompt),
        'ideate': score_ideate_signals(prompt),
        'deep': score_deep_signals(prompt)
    }

    top_workflow = max(scores, key=scores.get)
    confidence = scores[top_workflow]

    # Check for ambiguity
    sorted_scores = sorted(scores.values(), reverse=True)
    if sorted_scores[0] - sorted_scores[1] < AMBIGUITY_THRESHOLD:
        return (None, confidence)  # Trigger ambiguity gate

    if confidence < CONFIDENCE_THRESHOLD:
        return ('chat', confidence)  # Default fallback

    return (top_workflow, confidence)

CONFIDENCE_THRESHOLD = 0.4
AMBIGUITY_THRESHOLD = 0.15
```

## Score Calculation

Each workflow has weighted signals:

| Signal Type | Weight | Example |
|-------------|--------|---------|
| Explicit keyword | 0.5 | "brainstorm" → ideate |
| Phrase pattern | 0.3 | "why is X happening" → thinkdeep |
| Context hint | 0.2 | Has thread_id → chat boost |

Final score = sum(matched_signals × weights), normalized to 0-1.

## Confidence Threshold

| Confidence | Action |
|------------|--------|
| ≥ 0.6 | Route directly to workflow |
| 0.4-0.6 | Route with low-confidence notice |
| < 0.4 | Default to chat fallback |

## Ambiguity Gate

When top two scores differ by < 0.15:

```
AskUserQuestion:
"Your query matches multiple workflows. Which approach?"
Options:
- "{workflow1} - {description}" (score: {score1})
- "{workflow2} - {description}" (score: {score2})
- "Let me rephrase my question"
```

## Default Fallback Behavior

When no clear signals detected:
1. Default to `chat` workflow
2. Include notice: "Using chat mode. For specific workflows, try `foundry-research consensus|thinkdeep|ideate|deep`"
3. Allow user to switch mid-conversation

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty prompt | Prompt for input via AskUserQuestion |
| Only stop words | Default to chat |
| Mixed signals | Trigger ambiguity gate |
| Thread context | Boost chat score by 0.2 |
