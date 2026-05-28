---
name: semantic-search
description: Use semantic search to find relevant code and documentation when user asks about specific functionality, features, or implementation patterns. Automatically invoke when user asks "where is...", "how does... work", "find code that...", or similar conceptual queries. More powerful than grep for concept-based searches. Uses odino CLI with BGE embeddings for fully local semantic search.
allowed-tools: Bash, Read
---

# Semantic Search

## Overview

Enable natural language semantic search across codebases and notes using odino CLI with BGE embeddings. Unlike grep (exact text matching) or glob (filename patterns), semantic search finds code by what it does, not what it's called.

## When to Use This Skill

Automatically invoke semantic search when the user:
- Asks "where is [concept]" or "how does [feature] work"
- Wants to find implementation of a concept/pattern
- Needs to understand codebase structure around a topic
- Searches for patterns by meaning, not exact text
- Asks exploratory questions like "show me authentication logic"

**Do not use** for:
- Exact string matching (use grep)
- Filename patterns (use glob)
- Known file paths (use read)
- When the user explicitly requests grep/glob

## Directory Traversal Logic

Odino requires running commands from the directory containing `.odino/` config. To make this transparent (like git), use this helper function:

```bash
# Function to find .odino directory by traversing up the directory tree
find_odino_root() {
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [[ -d "$dir/.odino" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

# Usage in commands
if ODINO_ROOT=$(find_odino_root); then
    echo "Found index at: $ODINO_ROOT"
    (cd "$ODINO_ROOT" && odino query -q "$QUERY")
else
    echo "No .odino index found in current path"
    echo "Suggestion: Run /semq:index to create an index"
fi
```

**Why this matters:**
- User can be in any subdirectory of their project
- Commands automatically find the project root (where `.odino/` lives)
- Mirrors git behavior (works from anywhere in the tree)

## Quick Start

### Check if Directory is Indexed

Before searching, verify an index exists:

```bash
if ODINO_ROOT=$(find_odino_root); then
    (cd "$ODINO_ROOT" && odino status)
else
    echo "No index found. Suggest running /semq:index"
fi
```

### Search Indexed Codebase

```bash
# Basic search
odino query -q "authentication logic"

# With directory traversal
if ODINO_ROOT=$(find_odino_root); then
    (cd "$ODINO_ROOT" && odino query -q "$QUERY")
fi
```

### Parse and Present Results

Odino returns results in a formatted table:
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File                            ┃ Score    ┃ Content                         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ knowledge/Search Algorithms.md  │ 0.361    │    1 ---                        │
│                                 │          │    2 tags: [todo/stub]          │
│                                 │          │    3 module: CMPU 4010          │
│                                 │          │   ...                           │
│                                 │          │    7 # Search Algorithms in AI  │
│                                 │          │   ...                           │
└─────────────────────────────────┴──────────┴─────────────────────────────────┘
Found 2 results
```

**Enhanced workflow:**
1. Parse table to extract file paths, scores, and content previews
2. Read top 2-3 results (score > 0.3) for full context
3. Summarize findings with explanations
4. Use code-pointer to open most relevant file
5. Suggest follow-up queries or related concepts

## Query Inference

Transform user requests into better semantic queries with realistic output examples.

### Example 1: Conceptual Query

**User asks:** "error handling"
**Inferred query:** `error handling exception management try catch validation`
**Sample odino output:**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File                            ┃ Score    ┃ Content                         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ knowledge/Error Handling.md     │ 0.876    │    1 ---                        │
│                                 │          │    2 tags: [software-eng, best- │
│                                 │          │    3 ---                        │
│                                 │          │    4 # Error Handling           │
│                                 │          │    5                            │
│                                 │          │    6 Error handling is the proc │
│                                 │          │    7 runtime errors gracefully  │
│                                 │          │    8 system stability.          │
│                                 │          │    9                            │
│                                 │          │   10 ## Key Concepts            │
│                                 │          │   11 - Try-catch blocks for syn │
│                                 │          │   12 - Promise rejection handli │
│                                 │          │   13 - Input validation to prev │
│                                 │          │   14 - Logging errors for debug │
│                                 │          │   15 - User-friendly error mess │
│                                 │          │   16                            │
│                                 │          │   17 ## Best Practices          │
│                                 │          │   18 1. Fail fast - validate ea │
│                                 │          │   19 2. Log with context - incl │
│                                 │          │   20 3. Don't swallow errors -  │
└─────────────────────────────────┴──────────┴─────────────────────────────────┘
```

### Example 2: Code Query

**User asks:** "DB connection code"
**Inferred query:**
```
database connection pooling setup
import mysql.connector
pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host="localhost",
    database="mydb"
)
connection = pool.get_connection()
```
**Sample odino output:**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File                            ┃ Score    ┃ Content                         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ src/db/connection.js            │ 0.924    │    1 const mysql = require('mys │
│                                 │          │    2                            │
│                                 │          │    3 // Create connection pool  │
│                                 │          │    4 const pool = mysql.createP │
│                                 │          │    5   host: process.env.DB_HOS │
│                                 │          │    6   user: process.env.DB_USE │
│                                 │          │    7   password: process.env.DB │
│                                 │          │    8   database: process.env.DB │
│                                 │          │    9   waitForConnections: true │
│                                 │          │   10   connectionLimit: 10,     │
│                                 │          │   11   queueLimit: 0            │
│                                 │          │   12 });                        │
│                                 │          │   13                            │
│                                 │          │   14 // Test connection         │
│                                 │          │   15 pool.getConnection((err, c │
│                                 │          │   16   if (err) {               │
│                                 │          │   17     console.error('DB conn │
│                                 │          │   18     process.exit(1);       │
│                                 │          │   19   }                        │
│                                 │          │   20   console.log('Connected t │
└─────────────────────────────────┴──────────┴─────────────────────────────────┘
```

### Example 3: Algorithm Query (with code)

**User asks:** "BFS algorithm in Python"
**Inferred query:**
```
breadth first search BFS graph traversal queue
def bfs(graph, start):
    visited = set()
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            queue.extend(graph[node])
    return visited
```
**Sample odino output:**
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ File                            ┃ Score    ┃ Content                         ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ knowledge/Search Algorithms.md  │ 0.891    │    1 ---                        │
│                                 │          │    2 tags: [ai, algorithms]     │
│                                 │          │    3 module: CMPU 4010 AI       │
│                                 │          │    4 ---                        │
│                                 │          │    5 # Search Algorithms in AI  │
│                                 │          │    6                            │
│                                 │          │    7 Algorithms for finding sol │
│                                 │          │    8 problem spaces. Used in pa │
│                                 │          │    9 game AI, and optimization. │
│                                 │          │   10                            │
│                                 │          │   11 ## Types                   │
│                                 │          │   12                            │
│                                 │          │   13 ### Uninformed Search      │
│                                 │          │   14 - **BFS**: Explores level  │
│                                 │          │   15 - **DFS**: Explores deeply │
│                                 │          │   16 - **Uniform Cost**: Expand │
│                                 │          │   17                            │
│                                 │          │   18 ### Informed Search        │
│                                 │          │   19 - **A***: Uses heuristic + │
│                                 │          │   20 - **Greedy**: Only conside │
│                                 │          │   21 - **Hill Climbing**: Local │
└─────────────────────────────────┴──────────┴─────────────────────────────────┘
```

### Inference Patterns

- **Expand abbreviations:** DB → database, auth → authentication
- **Code queries include sample code:** User asks "connection pooling" → Query includes Python example with `pool.get_connection()`
- **Use specified language:** User mentions "JavaScript" → Use JavaScript syntax in query
- **Default to Python:** No language specified → Use Python code examples
- **Add related concepts:** "search" → include BFS, DFS, A* terminology
- **Add context words:** "handling", "management", "setup", "configuration"

## Core Capabilities

### 1. Semantic Search

Find code by describing what it does, not exact text:

**User asks:** "Where is the database connection handling?"

**Workflow:**
1. Check if directory is indexed (use `find_odino_root`)
2. Run `odino query -q "database connection handling"`
3. Parse results and rank by score
4. Read top 2-3 results for context
5. Summarize findings with file paths
6. Suggest using code-pointer to open specific files

**Example:**
```bash
if ODINO_ROOT=$(find_odino_root); then
    RESULTS=$(cd "$ODINO_ROOT" && odino query -q "database connection handling")
    # Parse results, read top files, summarize
else
    echo "No index found. Would you like me to index this directory?"
fi
```

### 2. Index Status Check

Verify indexing status before operations:

```bash
if ODINO_ROOT=$(find_odino_root); then
    (cd "$ODINO_ROOT" && odino status)
    # Shows: indexed files, model, last update
else
    echo "No .odino index found"
fi
```

### 3. Integration with Other Tools

**Semantic search → code-pointer:**
```bash
# After finding relevant file
echo "Found authentication logic in src/auth/middleware.js:42"
echo "Opening file..."
code -g src/auth/middleware.js:42
```

**Semantic search → grep refinement:**
```bash
# Use semantic search to find the area
odino query -q "API endpoint handlers"
# Then use grep for exact matches in those files
grep -n "app.get\|app.post" src/routes/*.js
```

### 4. Handling Edge Cases

**No index found:**
```bash
if ! ODINO_ROOT=$(find_odino_root); then
    echo "No semantic search index found in current path."
    echo ""
    echo "To create an index, run:"
    echo "  /semq:index"
    echo ""
    echo "This will index the current directory for semantic search."
fi
```

**Empty results:**
```bash
if [[ -z "$RESULTS" ]]; then
    echo "No results found for query: $QUERY"
    echo ""
    echo "Suggestions:"
    echo "- Try a different query (more general or specific)"
    echo "- Verify the index is up to date (/semq:status)"
    echo "- Consider using grep for exact text matching"
fi
```

## Slash Commands

This skill provides several slash commands for explicit control:

- **`/semq:search <query>`** - Search indexed codebase
- **`/semq:here <query>`** - Search with automatic directory traversal
- **`/semq:index [path]`** - Index directory for semantic search
- **`/semq:status [path]`** - Show indexing status and stats

## Best Practices

1. **Always check for index first** - Use `find_odino_root` before search operations
2. **Parse results clearly** - Show scores, file paths, and context
3. **Combine with other tools** - Use code-pointer for opening files, grep for exact matches
4. **Handle failures gracefully** - Suggest solutions when no index or no results
5. **Read top results** - Provide context by reading the most relevant files
6. **Use directory traversal** - Don't assume user is in project root

## Effective Query Patterns

Good queries are conceptual, not literal:
- ❌ "config.js" → Use glob instead
- ✅ "configuration loading logic"

- ❌ "validateEmail" → Use grep instead
- ✅ "email validation functions"

- ❌ "class AuthService" → Use grep instead
- ✅ "authentication service implementation"

## Technical Details

**Model:** BAAI/bge-small-en-v1.5 (33M params, ~133MB)
**Vector DB:** ChromaDB (stored in `.odino/chroma_db/`)
**Index location:** `.odino/` directory in project root
**Embedding batch size:** 16 (GPU) or 8 (CPU)

## Reference Documentation

For detailed information, see:

- **`references/cli_basics.md`** - Odino CLI syntax, commands, and options
- **`references/search_patterns.md`** - Effective query examples and tips
- **`references/integration.md`** - Workflows with code-pointer, grep, glob

Load these references as needed for deeper technical details or complex use cases.
