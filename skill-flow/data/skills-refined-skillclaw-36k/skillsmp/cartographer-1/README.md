# Cartographer

```
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║     ██████╗ █████╗ ██████╗ ████████╗ ██████╗  ██████╗         ║
    ║    ██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔════╝         ║
    ║    ██║     ███████║██████╔╝   ██║   ██║   ██║██║  ███╗        ║
    ║    ██║     ██╔══██║██╔══██╗   ██║   ██║   ██║██║   ██║        ║
    ║    ╚██████╗██║  ██║██║  ██║   ██║   ╚██████╔╝╚██████╔╝        ║
    ║     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝  ╚═════╝         ║
    ║                                                               ║
    ║           🗺️  Map Any Codebase with Any LLM  🧭               ║
    ║                                                               ║
    ║         ┌─────────┐    ┌─────────┐    ┌─────────┐            ║
    ║         │ Scan 📡 │───▶│ Analyze │───▶│ Map 📍  │            ║
    ║         └─────────┘    └─────────┘    └─────────┘            ║
    ║              │              │              │                  ║
    ║              ▼              ▼              ▼                  ║
    ║         File Tree     Subagents     CODEBASE_MAP.md          ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
```

A tool that maps and documents codebases of any size using parallel AI subagents. Works with **any LLM**, with **MiniMax-M2.1** preferred for its massive 1M token context.

## What it Does

Cartographer orchestrates multiple LLM subagents to analyze your entire codebase in parallel, then synthesizes their findings into:

- `docs/CODEBASE_MAP.md` - Detailed architecture map with file purposes, dependencies, data flows, and navigation guides
- Updates your project docs with a summary pointing to the map

## How it Works

```
You invoke Cartographer
        │
        ▼
┌───────────────────────────────────┐
│  1. Scan Codebase                 │
│     • Recursive file tree         │
│     • Token count per file        │
│     • Respects .gitignore         │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  2. Plan Subagent Assignments     │
│     • Group files by module       │
│     • Balance token budgets       │
│     • Target 50% of context max   │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  3. Spawn Subagents in PARALLEL   │
│     • Each reads assigned files   │
│     • Analyzes purpose, deps      │
│     • Returns structured summary  │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  4. Synthesize All Reports        │
│     • Merge subagent outputs      │
│     • Build architecture diagram  │
│     • Create navigation guides    │
└───────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────┐
│  5. Write docs/CODEBASE_MAP.md    │
│     Update project docs           │
└───────────────────────────────────┘
```

## Model Support

| Model | Context Window | Tokens per Subagent |
|-------|---------------|---------------------|
| **MiniMax-M2.1** ⭐ | 1,000,000 | 500,000 |
| Claude Sonnet | 1,000,000 | 500,000 |
| Gemini 1.5 Pro | 2,000,000 | 800,000 |
| GPT-4 Turbo | 128,000 | 60,000 |
| Llama 3.1 405B | 128,000 | 60,000 |
| Other | 32,000 | 15,000 |

**Why MiniMax-M2.1?** Its 1M token context means fewer subagents, better cross-file understanding, and faster mapping. For codebases under 800k tokens, a single call can map everything.

## Usage

### 1. Scan your codebase

```bash
python3 cartographer/scripts/scan-codebase.py . --format tree
```

### 2. Follow the workflow

See [SKILL.md](SKILL.md) for the complete orchestration workflow.

### 3. Get your map

Your LLM will generate `docs/CODEBASE_MAP.md` with:
- System architecture diagram (Mermaid)
- Directory structure with annotations
- Module-by-module documentation
- Data flow diagrams
- Conventions and gotchas
- Navigation guide for common tasks

## Update Mode

Already have a map? Run Cartographer again and it will:

1. Check git history for changes since last mapping
2. Only re-analyze changed modules
3. Merge updates with existing documentation

## Requirements

- Python 3.8+
- Optional: `pip install tiktoken` for accurate token counts (falls back to character estimation)

## Project Structure

```
cartographer/
├── README.md              # This file
├── SKILL.md               # Full workflow instructions for LLMs
└── scripts/
    └── scan-codebase.py   # Codebase scanner with token counting
```

## License

MIT

---

<p align="center">
  <i>Originally inspired by <a href="https://github.com/kingbootoshi/cartographer">kingbootoshi/cartographer</a></i><br>
  <i>Generalized for any LLM with MiniMax-M2.1 preference</i>
</p>
