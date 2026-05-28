# RLM Context Manager

**Version:** 1.0.0
**Category:** cross-model
**Status:** ACTIVE
**Added:** 2026-01-19

## Overview

The RLM (Recursive Language Model) Context Manager enables Claude to process documents and contexts that exceed typical context window limits. This skill implements the RLM architecture from [arXiv:2512.24601](https://arxiv.org/abs/2512.24601) (Zhang, Kraska, Khattab - MIT CSAIL), allowing Claude to match Gemini's 2M token context capability through intelligent chunking, sub-LLM delegation, and synthesis.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ROOT LLM (Opus 4.5)                       │
│                 Main Claude Conversation                     │
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Scout     │───▶│   Chunk     │───▶│  Synthesize │     │
│  │   Context   │    │   Content   │    │   Results   │     │
│  └─────────────┘    └──────┬──────┘    └─────────────┘     │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              PERSISTENT REPL (rlm_repl.py)                  │
│                                                              │
│  • Stores large context externally (pickle)                 │
│  • Provides peek(), grep(), chunk_indices() helpers         │
│  • Materializes chunks to files for sub-LLM processing      │
│  • Maintains buffers for intermediate results               │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│              SUB-LLM (Haiku via Task Agent)                 │
│                                                              │
│  • Processes individual chunks                              │
│  • Extracts query-relevant information                      │
│  • Returns structured JSON results                          │
│  • Fast, parallel execution                                 │
└─────────────────────────────────────────────────────────────┘
```

## Components

| Component | File | Purpose |
|-----------|------|---------|
| Skill Definition | `SKILL.md` | Main skill interface and commands |
| Persistent REPL | `scripts/rlm_repl.py` | Python REPL for context externalization |
| Sub-LLM Agent | `agents/rlm-subcall.md` | Haiku agent for chunk processing |
| State Directory | `state/` | Runtime state (gitignored) |

## Quick Start

### 1. Initialize with a Large Context File

```bash
python3 skills/rlm-context-manager/scripts/rlm_repl.py \
  --state skills/rlm-context-manager/state/state.pkl \
  init /path/to/large_document.txt
```

### 2. Check Status

```bash
python3 skills/rlm-context-manager/scripts/rlm_repl.py \
  --state skills/rlm-context-manager/state/state.pkl \
  status
```

### 3. Scout the Context

```bash
# Peek at beginning
python3 skills/rlm-context-manager/scripts/rlm_repl.py \
  --state skills/rlm-context-manager/state/state.pkl \
  exec -c "print(peek(0, 3000))"

# Search for patterns
python3 skills/rlm-context-manager/scripts/rlm_repl.py \
  --state skills/rlm-context-manager/state/state.pkl \
  exec -c "print(grep('pattern', max_matches=10))"
```

### 4. Create Chunks

```bash
python3 skills/rlm-context-manager/scripts/rlm_repl.py \
  --state skills/rlm-context-manager/state/state.pkl \
  exec <<'PY'
paths = write_chunks('skills/rlm-context-manager/state/chunks', size=150000, overlap=5000)
print(f"Created {len(paths)} chunks")
PY
```

### 5. Process with Sub-LLM

In Claude Code, use the Task tool to spawn Haiku agents for each chunk:

```
Task: rlm-subcall
Model: haiku
Prompt: "Query: <your question>. Chunk file: <chunk_path>. Extract relevant information."
```

## Commands

| Command | Description |
|---------|-------------|
| `/rlm init <path>` | Initialize REPL with large context file |
| `/rlm status` | Show current state (chars, chunks, buffers) |
| `/rlm query <question>` | Query loaded context via sub-LLM chunks |
| `/rlm chunk` | Materialize context into chunk files |
| `/rlm synthesize` | Merge collected evidence into final answer |
| `/rlm reset` | Clear RLM state |
| `/rlm export` | Export buffers to file |

## REPL Helper Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `peek` | `peek(start=0, end=1000)` | Return substring of context |
| `grep` | `grep(pattern, max_matches=20, window=120)` | Regex search with context |
| `chunk_indices` | `chunk_indices(size=200000, overlap=0)` | Calculate chunk boundaries |
| `write_chunks` | `write_chunks(out_dir, size, overlap, prefix)` | Materialize chunks to files |
| `add_buffer` | `add_buffer(text)` | Store intermediate results |

## Sub-LLM Output Format

The rlm-subcall agent returns structured JSON:

```json
{
  "chunk_id": "chunk_0003.txt",
  "relevant": [
    {
      "point": "Key finding or fact",
      "evidence": "short quote or paraphrase",
      "confidence": "high|medium|low"
    }
  ],
  "missing": ["what could not be determined"],
  "suggested_next_queries": ["follow-up questions"],
  "answer_if_complete": "answer if chunk alone answers query, else null",
  "mnemosyne_seeds": ["concepts for cross-session memory"]
}
```

## IRP Integration

### Mnemosyne Ledger
- Extract `mnemosyne_seeds` from sub-LLM results
- Format as Mnemosyne packets for cross-session persistence

### CRTP Packets
- RLM outputs can be formatted as CRTP packets for multi-model relay
- Enables Gemini-Claude bridging workflows

### Cross-Model Collaboration
- Load Gemini's large context exports
- Chunk and analyze for Claude consumption
- Synthesize into IRP-compatible format

## Performance Characteristics

| Metric | Typical Value |
|--------|---------------|
| Context capacity | 1M+ characters |
| Chunk size | 100k-200k chars |
| Sub-LLM model | Haiku (fast) |
| Parallel chunks | Yes |
| Synthesis model | Opus 4.5 |

## File Structure

```
rlm-context-manager/
├── README.md              # This file
├── SKILL.md               # Skill definition
├── scripts/
│   └── rlm_repl.py        # Persistent Python REPL
├── agents/
│   └── rlm-subcall.md     # Sub-LLM agent definition
└── state/                 # Runtime state (gitignored)
    ├── state.pkl          # Persisted REPL state
    └── chunks/            # Materialized chunk files
```

## Credits

- **RLM Paper:** Zhang, Kraska, Khattab (MIT CSAIL) - [arXiv:2512.24601](https://arxiv.org/abs/2512.24601)
- **Claude Code Implementation:** [Brainqub3](https://github.com/Brainqub3/claude_code_RLM)
- **IRP Integration:** Pack3t C0nc3pts / starwreck

## Changelog

### v1.0.0 (2026-01-19)
- Initial integration into IRP Methodologies
- Adapted from claude_code_RLM repository
- Added Mnemosyne/CRTP integration points
- Created rlm-subcall agent for chunk processing
- Updated SKILL_REGISTRY.md with RLM entry
