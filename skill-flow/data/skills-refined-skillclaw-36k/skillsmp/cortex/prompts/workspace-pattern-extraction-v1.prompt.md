# Workspace Pattern Extraction Prompt v1

## Purpose

Extract workspace-level conventions and patterns from AI sessions that work on a specific codebase or project. These become shared knowledge for all agents operating in that workspace.

## Input

- **Channel**: The AI platform (cursor, claude-code, codex, etc.)
- **Workspace Path**: The root path of the workspace being worked on
- **Session Name**: The name/title of the AI session
- **Messages**: An AI conversation session

## Task

Extract patterns and conventions that apply to this workspace:

1. **Project structure** — Where things live, how code is organized
2. **Coding conventions** — Style, patterns, idioms used in this codebase
3. **Tool usage** — Which tools to use and how
4. **Build/run patterns** — How to build, test, run the project
5. **Domain terminology** — Project-specific terms and their meanings
6. **Gotchas** — Things that are non-obvious or easy to get wrong

### Pattern Categories

| Category | Examples |
|----------|----------|
| **structure** | "Skills live in skills/", "State is in state/" |
| **conventions** | "Use AGENTS.md for agent config", "Prompts go in prompts/" |
| **tools** | "Use nexus CLI for status", "Run cortex sync for data" |
| **build** | "Use make build", "Tests run with go test ./..." |
| **terminology** | "Checkpoint means session fork point", "Facet means extracted value" |
| **gotchas** | "Don't modify state/ directly, use CLI", "JSONL files are append-only" |

---

## Output Format

```json
{
  "extraction_metadata": {
    "channel": "cursor",
    "workspace_path": "/Users/tyler/nexus",
    "session_name": "nexus-cli-development",
    "message_count": 120,
    "date_range": {
      "start": "2024-01-15T10:00:00Z",
      "end": "2024-01-15T18:00:00Z"
    }
  },
  "workspace_patterns": [
    {
      "category": "structure",
      "pattern": "Skill definitions live in skills/{type}/{name}/SKILL.md",
      "memory_entry": "structure: Skill definitions live in skills/{type}/{name}/SKILL.md",
      "evidence": "Create the skill in skills/tools/example/SKILL.md following the existing pattern",
      "confidence": "high",
      "source_type": "explicit"
    },
    {
      "category": "conventions",
      "pattern": "Use AGENTS.md as the root configuration file",
      "memory_entry": "conventions: Use AGENTS.md as the root configuration file",
      "evidence": "The AGENTS.md file defines the core behavior, always read it first",
      "confidence": "high",
      "source_type": "demonstrated"
    },
    {
      "category": "tools",
      "pattern": "Use 'nexus status' to check current state before taking action",
      "memory_entry": "tools: Use 'nexus status' to check current state before taking action",
      "evidence": "Run nexus status to see what capabilities are available",
      "confidence": "high",
      "source_type": "explicit"
    },
    {
      "category": "build",
      "pattern": "Run 'make build' to compile, 'make test' for tests",
      "memory_entry": "build: Run 'make build' to compile, 'make test' for tests",
      "evidence": "After changes, run make build && make test",
      "confidence": "high",
      "source_type": "demonstrated"
    },
    {
      "category": "terminology",
      "pattern": "A 'checkpoint' is a forkable point in conversation history",
      "memory_entry": "terminology: A 'checkpoint' is a forkable point in conversation history",
      "evidence": "Checkpoints are created at every assistant response boundary",
      "confidence": "high",
      "source_type": "explained"
    },
    {
      "category": "gotchas",
      "pattern": "Don't modify state/ files directly - use nexus CLI commands",
      "memory_entry": "gotchas: Don't modify state/ files directly - use nexus CLI commands",
      "evidence": "Wait, don't edit that file directly. Use nexus credential add instead.",
      "confidence": "high",
      "source_type": "correction"
    }
  ]
}
```

---

## Important Rules

1. **Focus on workspace-level patterns** — Not user preferences or agent-specific learnings
2. **Include memory_entry** — A compact sentence suitable for MEMORY.md (prefix with category)
3. **These should help any agent** — Patterns should be useful for anyone working on this codebase
4. **Quote evidence** — Include text that establishes the pattern
5. **Confidence levels**:
   - **high**: Explicitly stated or corrected
   - **medium**: Demonstrated through usage
   - **low**: Inferred from single instance
6. **Source types**:
   - `explicit`: Directly stated as a pattern/rule
   - `demonstrated`: Shown through consistent usage
   - `correction`: Revealed when someone did it wrong
   - `explained`: Definition or explanation given
7. **Filter out user-specific patterns** — "Tyler prefers X" → user memory, not workspace
8. **Be specific to the workspace** — Generic coding advice doesn't belong here

---

## Workspace Detection

Only extract patterns that are specific to this workspace, not generic best practices:

**Include:**
- "In nexus, skills are defined in skills/{type}/{name}/SKILL.md"
- "Use nexus CLI for all state management"
- "The cortex adapter pattern uses Sync() method"

**Exclude:**
- "Use meaningful variable names"
- "Write tests for new code"
- "Commit frequently"

---

## Conversation
{{{segment_text}}}
