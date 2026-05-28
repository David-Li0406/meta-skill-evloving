---
name: ask-repo
description: Analyze any GitHub repo to learn from implementations. Auto-clones repos locally using your own Claude setup. Use when exploring how other projects solve problems, finding prior art, or understanding unfamiliar codebases. Triggers on GitHub URLs with questions, "how does X implement...", "show me examples of...", "analyze this repo".
---

# ask-repo

Explore and learn from any GitHub repository without leaving your terminal.

## Workflow

### 1. Clone
Run `scripts/clone_repo.sh <github-url>` to shallow-clone the repo:
- Clones to `/tmp/ask-repo/<owner>-<repo>/`
- Uses `--depth 1` for speed (~5-10s for most repos)
- Handles HTTPS and SSH URLs
- Cleans up clones older than 24 hours

### 2. Orient (30 seconds)
Read key files in this order to understand the project:

| Priority | Files | Purpose |
|----------|-------|---------|
| 1 | README.md, README | Project overview, setup |
| 2 | package.json, pyproject.toml, Cargo.toml, go.mod, Gemfile | Tech stack, dependencies |
| 3 | src/index.*, src/main.*, lib/index.*, app.* | Entry points, architecture |
| 4 | Directory listing (`ls -la`, `tree -L 2`) | Structure overview |

### 3. Explore (parallel)
Launch 2-3 Explore agents simultaneously with different focuses:

```
Agent 1: "Map the directory structure and identify key abstractions/interfaces in <repo-path>"
Agent 2: "<user's specific question> in <repo-path>"
Agent 3: "Find implementations of <related-pattern> in <repo-path>"
```

Use `subagent_type: "Explore"` with the Task tool. These agents are optimized for fast codebase search.

### 4. Synthesize
Combine findings into a concise response:
- Answer the user's question directly
- Include `file:line` references for key findings
- Keep it scannable (bullets, not paragraphs)

## File Priority by Language

**JavaScript/TypeScript**: package.json → src/index.ts → lib/ → tests/
**Python**: pyproject.toml/setup.py → src/__init__.py → main.py → tests/
**Rust**: Cargo.toml → src/lib.rs → src/main.rs → examples/
**Go**: go.mod → main.go → cmd/ → internal/

## Output Format

Always include file references:
```
The streaming implementation uses async generators:
- `src/streaming.py:45` - StreamManager class handles chunked responses
- `src/client.py:123` - Client.stream() method wraps the generator
```

## Tips

- For large repos, grep for keywords before reading files
- Check tests/ for usage examples - often clearer than docs
- Look at recent commits (`git log --oneline -20`) to understand active areas
