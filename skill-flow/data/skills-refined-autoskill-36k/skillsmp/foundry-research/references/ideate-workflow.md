# Ideate Workflow

Creative brainstorming with structured four-phase approach.

## Contents

- When to Use
- MCP Usage
- Parameters
- Four Phases
- User Gates at Phase Transitions
- Phase-Specific Guidance
- Response Format

## When to Use

- **Brainstorming** new features or solutions
- **Creative problem-solving** with novel approaches
- **Exploring alternatives** before committing
- **Innovation sessions** requiring structured ideation

## MCP Usage

```bash
mcp__plugin_foundry_foundry-mcp__research action="ideate" prompt="How might we improve X?" thread_id="thread-abc123" phase="divergent"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `prompt` | Yes | - | Creative challenge or question |
| `thread_id` | No | New thread | Continue ideation session |
| `phase` | No | divergent | Current phase: divergent, convergent, selection, elaboration |

## Four Phases

| Phase | Goal | Output |
|-------|------|--------|
| `divergent` | Generate many ideas, no judgment | 10-20 raw ideas |
| `convergent` | Group, refine, combine ideas | 5-8 themed clusters |
| `selection` | Evaluate and prioritize | Top 2-3 candidates |
| `elaboration` | Develop selected ideas fully | Detailed proposals |

## User Gates at Phase Transitions

### Divergent → Convergent
```
AskUserQuestion:
"Generated {n} ideas. Ready to converge and refine?"
Options:
- "Yes, start convergent phase"
- "Generate more ideas first"
- "Review ideas before continuing"
```

### Convergent → Selection
```
AskUserQuestion:
"Refined to {n} idea clusters. Ready to select top candidates?"
Options:
- "Yes, evaluate and select"
- "Continue refining"
- "Show cluster details"
```

### Selection → Elaboration
```
AskUserQuestion:
"Selected top {n} ideas. Elaborate on which?"
Options:
- "Elaborate on #{1}: {title}"
- "Elaborate on #{2}: {title}"
- "Elaborate on all selected"
```

## Phase-Specific Guidance

### Divergent Phase
- Quantity over quality
- No criticism or filtering
- Build on previous ideas
- Welcome wild ideas

### Convergent Phase
- Group similar ideas
- Combine complementary concepts
- Identify themes
- Refine language

### Selection Phase
- Apply evaluation criteria
- Consider feasibility, impact, effort
- Rank candidates
- Document reasoning

### Elaboration Phase
- Develop implementation details
- Identify requirements
- Note risks and mitigations
- Create actionable next steps

## Response Format

```json
{
  "thread_id": "thread-abc123",
  "phase": "selection",
  "ideas": [
    {
      "id": "I1",
      "title": "Idea title",
      "description": "Full description",
      "phase_added": "divergent",
      "cluster": "Theme A"
    }
  ],
  "selected": ["I1", "I3"],
  "elaborated": {
    "I1": {
      "implementation": "How to build...",
      "requirements": ["R1", "R2"],
      "risks": ["Risk 1"]
    }
  }
}
```
