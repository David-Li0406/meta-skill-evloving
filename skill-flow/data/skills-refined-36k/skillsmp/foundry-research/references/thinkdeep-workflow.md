# ThinkDeep Workflow

Hypothesis-driven systematic investigation for complex problems.

## When to Use

- **Complex problems** requiring structured analysis
- **Debugging** difficult issues with unknown root cause
- **Root cause analysis** for failures or unexpected behavior
- **Multi-factor problems** with interacting variables

## MCP Usage

```bash
mcp__plugin_foundry_foundry-mcp__research action="thinkdeep" prompt="Why is X happening?" thread_id="thread-abc123" depth="thorough"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `prompt` | Yes | - | Problem description or question |
| `thread_id` | No | New thread | Continue investigation |
| `depth` | No | standard | Investigation depth: quick, standard, thorough |

## Confidence Levels

| Level | Description | Evidence Required |
|-------|-------------|-------------------|
| `speculation` | Initial hypothesis, untested | Logical reasoning only |
| `possible` | Some supporting evidence | 1-2 data points |
| `probable` | Multiple supporting factors | 3+ consistent findings |
| `confirmed` | Verified through testing | Reproducible evidence |

## Investigation Flow

```
1. Problem Definition
   └→ Clarify scope, symptoms, context

2. Hypothesis Generation
   └→ List possible causes with initial confidence

3. Evidence Gathering
   └→ For each hypothesis:
      ├→ Identify testable predictions
      ├→ Gather relevant data
      └→ Update confidence level

4. Synthesis
   └→ Rank hypotheses by confidence
   └→ Identify most likely root cause

5. Recommendations
   └→ Next steps to confirm or remediate
```

## Findings Format

```json
{
  "problem": "Original question/problem statement",
  "thread_id": "thread-abc123",
  "hypotheses": [
    {
      "id": "H1",
      "description": "Hypothesis description",
      "confidence": "probable",
      "evidence": ["Finding 1", "Finding 2"],
      "counter_evidence": []
    }
  ],
  "conclusion": {
    "most_likely": "H1",
    "confidence": "probable",
    "summary": "Root cause analysis summary"
  },
  "next_steps": [
    "Recommended action 1",
    "Recommended action 2"
  ]
}
```

## Depth Levels

| Depth | Hypotheses | Evidence Rounds | Time |
|-------|------------|-----------------|------|
| `quick` | 2-3 | 1 | Fast |
| `standard` | 3-5 | 2 | Moderate |
| `thorough` | 5-7 | 3+ | Comprehensive |
