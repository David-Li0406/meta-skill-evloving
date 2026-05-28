---
name: Document Search
description: This skill should be used when the user asks to "search documents", "find in my files", "look for documents about", "semantic search", "find related documents", or when searching project files by meaning rather than exact text. Provides hybrid search combining grep (literal) and embeddings (semantic) for comprehensive document discovery.
version: 0.2.0
---

# Document Search Skill

Hybrid document search combining literal text matching (grep) with semantic similarity (embeddings) for comprehensive search across project documents.

## When to Use

Activate this skill when:
- Searching for documents by concept or meaning ("find discussions about budget")
- Looking for related documents without knowing exact terms
- Needing both exact matches and conceptually similar results
- Working with PDFs, Word docs, presentations, or text files in the project
- Filtering documents by collection, author, type, or topic

## How It Works

The search tool runs both grep and semantic search simultaneously, merging results:

1. **Grep search**: Fast literal text matching in document chunks
2. **Semantic search**: Embedding-based similarity using Xenova/all-MiniLM-L6-v2
3. **Result merging**: Combines and deduplicates, boosting documents found by both methods

## Prerequisites

Before searching, ensure documents are indexed. The tool stores a unified index in `.embeddings/index.json`.

### Indexing

Run the indexer to create embeddings for all documents:

```bash
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts index .
```

#### Chunking Strategies

Choose a chunking strategy based on your use case:

```bash
# Sliding window (default) - best for precise retrieval
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts index . --strategy sliding

# Paragraph-based - best for structured documents
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts index . --strategy paragraph

# Sentence-based - best for natural language queries
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts index . --strategy sentence
```

### Text Extraction for Binary Files

For PDFs, Word docs, and presentations, extract text first by creating a `.txt` sidecar:

```
report.pdf      → report.pdf.txt (extracted text)
slides.pptx     → slides.pptx.txt (extracted text)
```

Use an LLM to extract text from binary documents before indexing.

## Searching

Run hybrid search with a query:

```bash
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts search "budget concerns"
```

### Search with Filters

Filter by metadata extracted from documents:

```bash
# Filter by collection (derived from directory names)
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts search "love" --collection "jane austin"

# Filter by document type
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts search "proposal" --type report

# Filter by author
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts search "meeting" --author "John Smith"

# Filter by topic
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts search "conflict" --topic marriage

# Filter by date range
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts search "quarterly review" --after 2024-01-01 --before 2024-04-01

# Combine multiple filters
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts search "proposal" --type report --after 2024-01-01
```

### Understanding Results

Results include:
- **path**: Document location
- **score**: Relevance (0-1, higher is better)
- **type**: `grep` (literal match) or `semantic` (meaning-based)
- **location**: Line numbers and byte offsets for the matched chunk
- **metadata**: Extracted title, collection, document type, author
- **excerpt**: Relevant snippet from document

Documents found by both grep AND semantic search receive boosted scores.

## Discovering Taxonomy

View all discovered collections, document types, authors, and topics:

```bash
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts taxonomy .
```

## Listing Files

List indexed files matching filters (without searching):

```bash
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts files --collection "jane austin" --type novel
```

## Index Statistics

View index information:

```bash
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts stats .
```

## Data Storage

Index is stored in `.embeddings/index.json`:

```
project/
├── .embeddings/
│   └── index.json       # Unified index with chunks and metadata
├── report.pdf
├── report.pdf.txt       # Pre-extracted text (for binary files)
└── notes.md
```

The index contains:
- File metadata (path, size, mtime, content hash)
- Document chunks with 384-dimensional embeddings
- Extracted metadata (title, author, collection, topics, people)
- Taxonomy aggregations

## Workflow Example

When a user asks "Find documents about the Q4 budget review":

1. **Check for index**: Look for `.embeddings/index.json` in the project
2. **Index if needed**: Run the indexer if no index exists
3. **Search**: Run hybrid search with the query
4. **Present results**: Show top matches with excerpts, scores, and metadata

```bash
# Step 1: Index (if needed)
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts index .

# Step 2: Search
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts search "Q4 budget review"
```

## Supported File Types

Directly indexed (text readable):
- `.txt` - Plain text
- `.md` - Markdown

Requires text extraction first:
- `.pdf` - PDF documents
- `.doc`, `.docx` - Word documents
- `.ppt`, `.pptx` - PowerPoint presentations

## Auto-Indexing Behavior

When searching a directory without an existing index:
1. Detect missing `.embeddings/index.json`
2. Run indexer automatically with sliding window strategy
3. Proceed with search

This ensures seamless first-use experience.

## CLI Reference

```
npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts index [path] [options]
  Index documents in directory (default: current directory)

  Options:
    --strategy <type>    Chunking: sliding (default), paragraph, sentence
    --window <size>      Window size in chars (default: 300)
    --overlap <size>     Overlap in chars (default: 100)

npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts search <query> [path] [options]
  Search indexed documents

  Options:
    --collection <name>  Filter by collection
    --type <type>        Filter by document type
    --author <name>      Filter by author
    --topic <topic>      Filter by topic
    --path <pattern>     Filter by file path pattern
    --after DATE         Only documents modified after this date
    --before DATE        Only documents modified before this date

npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts taxonomy [path]
  Show discovered taxonomy (collections, types, authors, topics)

npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts files [path] [options]
  List files matching filters

npx tsx ${CLAUDE_PLUGIN_ROOT}/src/cli.ts stats [path]
  Show index statistics
```

## Technical Details

- **Embedding model**: Xenova/all-MiniLM-L6-v2 (~23MB, downloads on first use)
- **Vector dimensions**: 384
- **Similarity metric**: Cosine similarity
- **Index version**: 5
- **Storage**: Single JSON index file (no database required)
- **Incremental updates**: Content hash comparison skips unchanged files
