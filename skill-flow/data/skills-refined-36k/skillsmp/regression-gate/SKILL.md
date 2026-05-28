---
name: regression_gate
description: "Atomic Validation Protocol: Unified validator for Chroma Check and Librarian Audit."
version: 2.1.0 (Unified)
author: Antigravity
---

# Operational Instructions

This skill is the **Quality Guardian**. It must never be bypassed.

## 🛠️ The Unified Command
Instead of running scattered commands, use the unified eval runner:

### Syntax
```bash
uv run --with chromadb .agent/evals/runner.py --protocol
```

This command validates:
1. **FixLog Canary**: `AG.fix.eval.metadata_gate` in `fix_logs` collection.
2. **Research Canary**: `AG.research.eval.metadata_gate` in `research_summaries` collection.

## 🚨 Failure Protocol
If the script returns an error (Exit Code 1):

1. **STOP**: Do not proceed with any other actions.
2. **CONSULT**: Read `.agent/skills/regression_gate/examples/correct_metadata.md` for guidance.
3. **FIX**: Correct metadata in Chroma or clean ghost files.
4. **RETRY**: Re-run the gate until you get `🚀 READY FOR DEPLOY`.

## Technical Notes
- The script handles `uv run` internally for dependencies (`chromadb`).
- Designed to be "Zero Silence": prints exact errors in red.

