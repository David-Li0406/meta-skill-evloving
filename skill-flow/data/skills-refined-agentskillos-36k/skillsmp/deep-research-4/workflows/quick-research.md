# Quick Research Workflow

For simpler queries where full diffusion loop is overkill.

<when_to_use>
- Simple factual questions
- Single-dimension topics
- Time-sensitive requests
- When user says "quick" or "brief"
</when_to_use>

<process>
1. **Single Worker Round**
   - Spawn 1-2 research workers max
   - No iteration, no gap detection
   - Direct synthesis of findings

2. **Condensed Output**
   - 3-5 bullet point summary
   - Key sources listed
   - No full report structure
</process>

<output_format>
```markdown
## Quick Research: [Topic]

**Key Findings:**
- [Finding 1] ([Source])
- [Finding 2] ([Source])
- [Finding 3] ([Source])

**Sources:**
- [URL 1]
- [URL 2]

*Quick research - for deeper investigation, run full deep-research.*
```
</output_format>
