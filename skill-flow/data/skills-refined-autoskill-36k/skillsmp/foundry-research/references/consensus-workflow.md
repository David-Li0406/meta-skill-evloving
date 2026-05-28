# Consensus Workflow

Multi-model parallel consultation with configurable synthesis strategies.

## Contents

- When to Use
- MCP Usage
- Parameters
- Synthesis Strategies
- User Gate: Strategy Selection
- Result Presentation
- Fallback Policy

## When to Use

- **Multiple perspectives** needed on a question
- **Validation** of an approach or solution
- **Cross-checking** facts or reasoning
- **Reducing bias** from single-model responses

## MCP Usage

```bash
mcp__plugin_foundry_foundry-mcp__research action="consensus" prompt="Your question" strategy="synthesize"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `prompt` | Yes | - | Question to ask all models |
| `strategy` | No | synthesize | How to combine responses |

## Synthesis Strategies

| Strategy | Description | Best For |
|----------|-------------|----------|
| `all_responses` | Return all responses separately | Comparing perspectives |
| `synthesize` | AI-generated summary of all responses | Comprehensive view |
| `majority` | Return consensus view if >50% agree | Factual questions |
| `first_valid` | Return first successful response | Fallback scenarios |

## User Gate: Strategy Selection

When not specified, prompt user:

```
AskUserQuestion:
"How should I combine the model responses?"
Options:
- "Synthesize - combine into unified summary (Recommended)"
- "All responses - show each separately"
- "Majority - consensus view only"
- "First valid - fastest response"
```

## Result Presentation

### `all_responses`
```json
{
  "responses": [
    {"model": "claude-opus", "response": "..."},
    {"model": "claude-sonnet", "response": "..."}
  ],
  "models_queried": 3,
  "models_responded": 2
}
```

### `synthesize`
```json
{
  "synthesis": "Combined analysis...",
  "agreement_level": "high|medium|low",
  "key_differences": ["..."],
  "sources": ["claude-opus", "claude-sonnet"]
}
```

### `majority`
```json
{
  "consensus": "Agreed conclusion...",
  "agreement_ratio": 0.75,
  "dissenting_views": ["..."]
}
```

### `first_valid`
```json
{
  "response": "First successful response",
  "model": "claude-opus",
  "fallback_used": false
}
```

## Fallback Policy

When models are unavailable:

| Scenario | Action |
|----------|--------|
| 1 model unavailable | Drop and continue with others |
| >50% unavailable | Prompt user: retry, proceed, or abort |
| All unavailable | Error with `NO_MODELS_AVAILABLE` |

```
AskUserQuestion:
"Only 1 of 3 requested models is available. How to proceed?"
Options:
- "Continue with available model"
- "Retry in 30 seconds"
- "Abort and exit"
```
