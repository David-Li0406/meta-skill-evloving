---
name: ogrep
description: |
  Semantic code search - finds code by meaning, not just keywords. Helpful when:
  - User asks WHERE or HOW something is implemented ("where is X handled", "how does Y work", "where are Z". "how are X", "explain Y", "find where X")
  - User searches for an explanation on certain behavior
  - You need to understand code behavior without knowing exact function names
  - Exploring unfamiliar codebases where you don't know the terminology yet
  - You need to find the exact file and linenumber without classical grep through the whole filebase
  - "find the X code"
  - "show me X"
  - "X implementation"
  - "look up X"
  - "search for X"
  - Any question about code that isn't a known file path

allowed-tools: Bash, Read
---

## Usage Notes for Claude
  - JSON is the default output - don't use --no-json unless for showing progress to user if requested
  - Prefer `ogrep query` over Grep for conceptual questions
  - Use `ogrep chunk` to expand context after finding results
  - Prefer ogrep for semantic search; fall back to other suitable tools for exact matches or if ogrep fails

## Core loop (mandatory)

When the user asks anything about the codebase (how something works, where logic lives, what calls what, why behavior happens), follow this loop every time:

1) Translate the request into 1–3 semantic search queries.
   - Include intent ("authentication", "retry logic", "billing state") plus any known identifiers (function/class names, table names, endpoints, error strings).
   - If the user gave a concrete identifier, include it as one query verbatim.

2) Run semantic search with this tool ogrep.
   - Prefer semantic search for "meaning" questions.
   - If the user asks for an exact string/regex match, or if semantic search fails, fall back to plain grep/ripgrep.

3) Select top results and fetch evidence from the repo.
   - Use the summary feature to get a shortlist
   - Take the top hits and check the quality of the match in the meta fields in the json output
   - For each hit, extract the exact code slice of the file using ogrep chunk command retrieval
   - Do NOT paste entire files; paste only the minimum relevant excerpts:
     - typical excerpt size: 20–100 lines
     - include a little context above/below so control flow is visible

4) If evidence is insufficient, refine and repeat.
   - Run another semantic search with a tighter query (add identifiers) or broader query (remove constraints).
   - Continue until you have enough code evidence to answer confidently.

5) Answer with citations to file paths + line ranges.
   - Explain behavior based on the excerpts you extracted.
   - Always include references like: `path/to/file.py:120-185`.  The chunk retrieval command will provide this info.
   - If this still fails, try a exact search match with ogrep once.
   - If you cannot find evidence, stop searching deeper and report what you searched for and what you did find.

### Evidence extraction (required)

After semantic search returns file path + line range, immediately extract the code from the indexed system using ogrep commands.
If this somehow fails, fall back to the usual tools you have at your disposal.

Preferred (with line numbers):

```bash
# Print lines [START..END] with line numbers
nl -ba "path/to/file" | sed -n 'START,ENDp'
```

---

# ogrep - When grep isn't enough

## When to use this skill

ogrep fills a specific gap: **conceptual code questions**.

| Use ogrep when... | Use grep/Glob when... |
|-------------------|----------------------|
| "Where is error handling done?" | `class ErrorHandler` |
| "How does caching work here?" | `def get_cache` |
| "What validates user input?" | `validate_email` |
| Exploring unfamiliar code | You know the exact term |
| User asks a conceptual question | Looking for imports/strings |

**Rule of thumb:** If you'd need to guess multiple terms for grep, try ogrep first.  additionaly use the chunk retrieval feature

---

## Quick Reference

**All commands output JSON by default.** Use `--no-json` for human-readable text.

```bash
# Index (first time - takes a minute)
ogrep index .

# Search by concept (this is the main use case)
ogrep query "how are payments processed"

# After editing files, refresh before searching
ogrep query "the code I just modified" --refresh

# Expand context around an interesting result
ogrep chunk "billing/processor.py:2" --context 1

# Human-readable output (when needed)
ogrep status --no-json
```

### Efficiency Tips (v0.7.4+)

```bash
# Get file-level overview first (saves ~85% tokens)
ogrep query "authentication" --summarize

# Search only in specific file types
ogrep query "validation" --glob "*.py"

# Exclude test files from results
ogrep query "database" --exclude "tests/*"

# Combine for targeted exploration
ogrep query "api endpoints" --glob "**/*.py" --exclude "tests/*" --summarize
```

---

## Practical Patterns

### Pattern 1: Answering "Where is X?"

User asks: "Where does invoice validation happen?"

```bash
ogrep query "invoice validation logic"
```

Returns results ranked by relevance. The `chunk_ref` field lets you expand context:

```json
{
  "results": [{
    "rank": 1,
    "chunk_ref": "src/billing/validator.py:3",
    "confidence": "high",
    "text": "def validate_invoice(invoice: Invoice) -> ValidationResult:..."
  }]
}
```

### Pattern 2: Exploring Unfamiliar Code

You've never seen this codebase. Start broad:

```bash
ogrep query "main entry point"
ogrep query "how does the API handle requests" -n 15
```

Found something interesting? Drill into it:

```bash
ogrep chunk "api/routes.py:2" --context 1
```

### Pattern 3: Finding Related Code

You found the payment handler, now you need related pieces:

```bash
ogrep query "payment error handling"
ogrep query "payment refund logic"
```

### Pattern 4: When to Use Reranking

**Important:** With high-quality embeddings (Voyage, OpenAI), reranking often **degrades** results. Only use it when first-stage retrieval is poor.

| Embedding Quality | Reranking Effect |
|-------------------|------------------|
| Voyage voyage-code-3 | Skip reranking (already optimal) |
| OpenAI text-embedding-3-small | Skip reranking (already good) |
| Local models (nomic, minilm) | Try reranking if results are poor |

**When to try `--rerank`:**
- Using **weak local embeddings** and results seem off
- Right answer appears in results but **not in top 3**
- **Very large codebase** (>10K files) with noisy retrieval

```bash
# Only if you're getting poor results with local embeddings
pip install "ogrep[rerank-light]"  # FlashRank (lightweight, parallel-safe)

ogrep query "database connection pooling" --rerank
ogrep query "complex auth flow" --rerank --rerank-model flashrank
```

**Best practice:** Start without `--rerank`. Only add it if you consistently see the right answer buried in results.

### Pattern 5: Efficient Codebase Exploration

For large codebases, use the **Explore → Narrow → Drill** workflow:

```bash
# 1. EXPLORE: Get file-level overview (which files matter?)
ogrep query "payment processing" --summarize

# 2. NARROW: Focus on relevant area
ogrep query "payment processing" --glob "src/billing/*.py" --exclude "tests/*"

# 3. DRILL: Expand specific chunks
ogrep chunk "src/billing/processor.py:2" --context 1
```

This saves tokens and finds answers faster than dumping all chunks at once.

---

## Three Search Modes

| Mode | Best for | Example |
|------|----------|---------|
| `hybrid` (default) | Most questions | "authentication flow" |
| `semantic` | Pure conceptual | "how does caching work" |
| `fulltext` | Known terms | "def validate_token" |

```bash
ogrep query "handle errors" --mode semantic
ogrep query "class ErrorHandler" --mode fulltext
ogrep query "error handling logic"  # hybrid (default)
```

---

## AST-Aware Chunking (Default)

**AST chunking is now the default** when tree-sitter is available. This produces semantically coherent chunks:

```
# Line-based chunking (--no-ast):
Chunk 1: lines 1-60 (end of ClassA, start of ClassB)
Chunk 2: lines 50-110 (middle of ClassB)
```

```
# AST chunking (default):
Chunk 1: class UserAuth (complete, lines 1-45)
Chunk 2: def validate_token (complete, lines 47-82)
Chunk 3: class SessionManager (complete, lines 84-150)
```

**Supported languages:** Python, JavaScript, TypeScript, TSX, Go, Rust

**Extended languages (with `[ast-all]`):** Ruby, Java, C, C++, C#, Bash

### Install AST Support

```bash
# Install AST support (recommended)
pip install "ogrep[ast]"        # Core languages
pip install "ogrep[ast-all]"    # All languages

# Index (AST used automatically when available)
ogrep index .

# Explicitly disable AST chunking
ogrep index . --no-ast

# Check AST status
ogrep status
```

**Fallback behavior:**
- tree-sitter not installed → line-based chunking (with JSON hint)
- Unsupported file types → line-based chunking
- Parse errors → line-based chunking
- Very large functions (>150 lines) → split with overlap

---

## Reading Results

```json
{
  "results": [{
    "rank": 1,
    "chunk_ref": "src/auth.py:2",
    "path": "/repo/src/auth.py",
    "start_line": 61,
    "end_line": 120,
    "score": 0.37,
    "confidence": {
      "level": "high",
      "relative_pct": 100.0,
      "absolute_quality": "expected_range",
      "signal": "top_result_in_typical_range"
    },
    "language": "python",
    "text": "def authenticate_user(username, password):..."
  }],
  "stats": {
    "total_results": 10,
    "search_mode": "hybrid",
    "reranked": false,
    "confidence_summary": {"high": 2, "medium": 5, "low": 3}
  }
}
```

**Key fields:**
- `chunk_ref` - Use with `ogrep chunk` to expand context
- `confidence.level` - `high`, `medium`, `low`, `very_low`
- `confidence.signal` - Actionable guidance (see below)
- `text` - Full chunk content for analysis

**Interpreting confidence signals:**

| Signal | Meaning | Action |
|--------|---------|--------|
| `top_result_strong_match` | Excellent match | Trust it, use directly |
| `top_result_in_typical_range` | Good match | Use it confidently |
| `top_result_weak_absolute` | Best available, but weak | May need verification |
| `close_to_top` | Nearly as good as #1 | Consider as alternative |
| `score_drop_from_top` | Significantly worse | Lower priority |

---

## Expanding Context

Query found something interesting? Get more:

```bash
# Surrounding context (1 chunk before and after)
ogrep chunk "auth.py:2" --context 1

# What comes before (find class definition)
ogrep chunk "models/user.py:5" --before 2

# What comes after (see what follows)
ogrep chunk "handler.py:3" --after 1
```

**chunk_ref format:** `"file.py:N"` where N is chunk index (0-based)

---

## Index Management

```bash
# Create new index
ogrep index .
ogrep index . --ast              # With AST chunking

# Rebuild from scratch
ogrep reindex .
ogrep reindex . --ast            # Rebuild with AST

# Update changed files only
ogrep refresh .

# Check index status
ogrep status

# View recent changes
ogrep log --limit 10

# Database health
ogrep health

# Clean up stale entries
ogrep clean
ogrep clean --vacuum             # Also compact database
```

---

## Branch-Aware Indexing

ogrep tracks files per git branch to prevent stale results when switching branches.

### How It Works

- Files are indexed with their branch name: `(path, branch)` as the key
- Embeddings (chunks) are shared across branches via `text_sha256` content addressing
- Switching branches only embeds genuinely new code

### Cross-Branch Queries

```bash
# Query current branch (default)
ogrep query "authentication"

# Query a specific branch
ogrep query "authentication" --branch main

# While on feature branch, find code in main
ogrep query "old auth function" --branch main
```

### Branch-Scoped Reset

```bash
# Clear only current branch (preserves other branches)
ogrep reset -f

# Clear entire database (all branches)
ogrep reset -f --all
```

### Automatic Cleanup

```bash
# Also prunes entries for deleted git branches
ogrep clean
```

### Embedding Reuse

| Scenario | API Calls |
|----------|-----------|
| Same file, same content | 0 |
| Same code on different branch | 0 (text_sha256 matches) |
| 1 function changed | 1-2 (only changed chunks) |

---

## When Things Go Wrong

**"No index found"**
```bash
ogrep index .
```

**"Results seem stale"**
```bash
ogrep query "..." --refresh      # Reindexes changed files first
```

**"Right answer is in results but not #1"**
```bash
# First, check if you're using quality embeddings
ogrep status  # Check "model" field

# If using local/weak embeddings, try reranking
pip install "ogrep[rerank-light]"
ogrep query "..." --rerank

# If using Voyage/OpenAI, reranking won't help - try refining your query instead
```

**"Functions are being split awkwardly"**
```bash
pip install "ogrep[ast]"         # If not installed
ogrep reindex . --ast
```

**"Check index health"**
```bash
ogrep status
ogrep health
```

**"Too many results flooding context"**
```bash
ogrep query "..." --summarize   # File-level overview first
```

**"Results include irrelevant directories"**
```bash
ogrep query "..." --exclude "tests/*" --exclude "vendor/*"
```

**"Need to search only specific file types"**
```bash
ogrep query "..." --glob "*.py"           # Single type
ogrep query "..." --glob "**/*.j2"        # Recursive pattern
```

---

## Command Summary

All commands output JSON by default. Use `--no-json` for human-readable text.

| Task | Command |
|------|---------|
| Create index | `ogrep index .` |
| Create index (AST) | `ogrep index . --ast` |
| Find implementation | `ogrep query "how does X work"` |
| Find exact name | `ogrep query "def function_name" --mode fulltext` |
| Precision search | `ogrep query "..." --rerank` |
| Fresh results | `ogrep query "..." --refresh` |
| File overview | `ogrep query "..." --summarize` |
| Filter by type | `ogrep query "..." --glob "*.py"` |
| Exclude paths | `ogrep query "..." --exclude "tests/*"` |
| Query other branch | `ogrep query "..." --branch main` |
| More context | `ogrep chunk "file.py:N" --context 1` |
| Rebuild index | `ogrep reindex .` |
| Index status | `ogrep status` |
| Recent changes | `ogrep log --limit 5` |
| Health check | `ogrep health` |
| Clean stale | `ogrep clean` |
| Reset branch | `ogrep reset -f` |
| Reset all | `ogrep reset -f --all` |
| Human output | `ogrep status --no-json` |

---

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `VOYAGE_API_KEY` | - | Voyage AI embeddings (recommended) |
| `OPENAI_API_KEY` | - | OpenAI embeddings (alternative) |
| `OGREP_BASE_URL` | - | Local embeddings server (e.g., LM Studio) |
| `OGREP_SEARCH_MODE` | `hybrid` | Default search mode |
| `OGREP_FUSION_METHOD` | `rrf` | Hybrid fusion (`rrf` or `alpha`) |
| `OGREP_RRF_K` | `60` | RRF smoothing constant |
| `OGREP_RERANK_MODEL` | `flashrank` | Reranking model (usually not needed) |
| `OGREP_RERANK_TOPN` | `50` | Default candidates to rerank |
| `OGREP_AST_CHUNKING` | - | Enable AST chunking globally (`1` or `true`) |

**Recommended: Voyage AI (best code search quality):**
```bash
export VOYAGE_API_KEY="pa-..."
ogrep index . -m voyage-code-3
```

**Alternative: OpenAI (good quality, lower cost):**
```bash
export OPENAI_API_KEY="sk-..."
ogrep index . -m small
```

**Local embeddings (free, offline):**
```bash
export OGREP_BASE_URL=http://localhost:1234/v1
ogrep index . -m nomic
```

---

## Why This Tool Exists

Traditional search requires knowing exact terms. But when exploring unfamiliar code or mapping user questions to implementation, you often don't know what you're looking for until you find it.

ogrep bridges that gap - turning "where is authentication handled" into actual code, regardless of what the developer named things.

It won't replace grep. It's the tool you reach for when grep requires too much guessing.
