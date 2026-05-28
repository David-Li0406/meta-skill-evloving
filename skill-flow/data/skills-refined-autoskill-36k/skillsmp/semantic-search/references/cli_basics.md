# Odino CLI Basics

Reference guide for odino CLI syntax, commands, and options.

## Installation

```bash
# Install via pipx (recommended)
pipx install odino

# Verify installation
odino --version
```

## Core Commands

### `odino index`

Index a directory for semantic search.

```bash
# Index current directory
odino index

# Index specific directory
odino index /path/to/project

# Specify model (recommended: BGE for efficiency)
odino index --model BAAI/bge-small-en-v1.5

# Force reindex (ignores existing index)
odino index --force
```

**Configuration:**
- Creates `.odino/` directory in indexed location
- Stores config in `.odino/config.json`
- Stores embeddings in `.odino/chroma_db/`

**Default model:** EmmanuelEA/eea-embedding-gemma (600MB)
**Recommended model:** BAAI/bge-small-en-v1.5 (133MB, faster)

### `odino query`

Search indexed directory using natural language.

```bash
# Basic search
odino query -q "authentication logic"

# Search with custom number of results
odino query -q "database connections" -n 10

# Search specific path
odino query -q "error handling" -p /path/to/indexed/dir
```

**Options:**
- `-q, --query <QUERY>` - Natural language search query (required)
- `-n, --num-results <N>` - Number of results to return (default: 5)
- `-p, --path <PATH>` - Path to indexed directory (default: current dir)

**Output format:**
```
Score: 0.85 | Path: src/auth/middleware.js
Score: 0.78 | Path: src/auth/tokens.js
Score: 0.72 | Path: src/utils/validation.js
```

### `odino status`

Show indexing status and statistics.

```bash
# Status for current directory
odino status

# Status for specific path
odino status -p /path/to/project
```

**Output includes:**
- Number of indexed files
- Total chunks generated
- Model name
- Index location
- Last modified date

## Configuration File

Location: `.odino/config.json` in indexed directory

```json
{
  "model_name": "BAAI/bge-small-en-v1.5",
  "embedding_batch_size": 16,
  "chunk_size": 512,
  "chunk_overlap": 50
}
```

**Key settings:**
- `model_name` - Embedding model to use
- `embedding_batch_size` - Batch size for GPU/CPU (16 for GPU, 8 for CPU)
- `chunk_size` - Token length for text chunks
- `chunk_overlap` - Overlap between chunks

## .odinoignore File

Create `.odinoignore` in project root to exclude files/directories (gitignore syntax):

```
# Build artifacts
build/
dist/
*.pyc
__pycache__/

# Dependencies
node_modules/
venv/
.venv/

# Config files
.env
.env.local
*.secret
```

## Model Comparison

| Model | Size | Params | MTEB Score | Speed |
|-------|------|--------|------------|-------|
| eea-embedding-gemma | 600MB | 308M | 69.67 | Slower |
| bge-small-en-v1.5 | 133MB | 33M | ~62-63 | Faster |

**Recommendation:** Use BGE for most cases (smaller, faster, good quality)

## Common CLI Patterns

**Index with BGE model:**
```bash
odino index --model BAAI/bge-small-en-v1.5
```

**Search from subdirectory:**
```bash
# Requires finding .odino directory first (see SKILL.md)
cd project/src/utils
odino query -q "validation" -p ../..
```

**Reindex after code changes:**
```bash
odino index --force
```

**Check if directory is indexed:**
```bash
if [[ -d .odino ]]; then
    echo "Directory is indexed"
    odino status
else
    echo "Directory is not indexed"
fi
```

## Performance Tips

1. **Use BGE model** - 78% smaller, 90% fewer parameters, only ~7 point MTEB drop
2. **Adjust batch size** - Use 16 for GPU, 8 for CPU
3. **Use .odinoignore** - Exclude build artifacts, dependencies, config files
4. **GPU acceleration** - Much faster indexing if CUDA available
5. **Chunking strategy** - Default 512 tokens works well for most code

## Troubleshooting

**"Command not found: odino"**
```bash
# Ensure pipx bin directory is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Or reinstall
pipx install odino
```

**"No index found"**
```bash
# Check for .odino directory
ls -la .odino

# If missing, index first
odino index --model BAAI/bge-small-en-v1.5
```

**GPU out of memory**
```bash
# Reduce batch size in .odino/config.json
{
  "embedding_batch_size": 8  # or even 4
}

# Then reindex
odino index --force
```

**Slow indexing**
```bash
# Use smaller model
odino index --model BAAI/bge-small-en-v1.5

# Reduce batch size if GPU memory limited
# Edit .odino/config.json: "embedding_batch_size": 8
```

## Exit Codes

- `0` - Success
- `1` - General error (no index, invalid path, etc.)
- `2` - Invalid arguments

## Environment Variables

Odino respects standard environment variables:
- `CUDA_VISIBLE_DEVICES` - GPU selection
- `HF_HOME` - Hugging Face cache directory (for model downloads)
