# Research Assistant Skill

This skill teaches Claude to proactively search the vault for context during a session, supporting the user's synthesis work without concluding for them.

## What This Skill Provides

1. **Proactive searching** - Fetches vault context without explicit requests
2. **PARA awareness** - Knows where to look (Inbox, Projects, Areas)
3. **Natural integration** - Quotes passages and cites sources conversationally
4. **GCTR alignment** - Supports user synthesis, doesn't conclude

## Activation

**Explicit:**
- "/research"
- "research mode"
- "help me find context"

**Inferred (Claude activates when appropriate):**
- Names of people, projects, or teams
- Timeframes ("this week", "Tuesday", "last month")
- Questions about past decisions
- Requests to "think through" something

**Deactivation:**
- "stop researching"
- "be less aggressive"

## Key Behaviors

When active, Claude will:
- Search vault proactively when topics come up
- Quote relevant passages with file citations
- Present findings without interpreting them
- Focus on recent and relevant content

Claude will not:
- Ask permission before each search
- Draw conclusions from found content
- Overwhelm with every possible match
- Present speculative connections

## Tools Used

No custom scripts. Uses existing Claude Code tools:
- **Grep** - Content search across vault
- **Glob** - File pattern matching (dates, directories)
- **Read** - Full file content retrieval

## When Claude Uses This Skill

Triggers on phrases like:
- "research mode" / "/research"
- "help me think through..."
- "what do I know about..."
- "based on my notes..."
- "what have I written about..."
- "let's talk about [topic]"

Also activates when conversation naturally benefits from vault context (person names, project references, timeframes).

## File Structure

```
research-assistant/
├── SKILL.md    # Main skill documentation
└── README.md   # This file
```

## Integration

Complements other vault skills:
- **Task Management** - Research adds context to task discussions
- **Daily Review** - Research provides historical context
- **Synthesis** - Research fetches material; user synthesizes

## Installation

Automatically available when placed in:
- `~/.claude/skills/research-assistant/`

Claude discovers it via SKILL.md metadata and loads when triggered.
