---
name: RAGtrieval
description: Answer questions from indexed vault content using RAGtriever search, plus setup, configuration, and troubleshooting
---

# RAGtrieval Skill

Claude Code skill for working with RAGtriever (local-first vault indexer with hybrid retrieval).

**Primary Purpose:** Search and answer questions from the indexed vault content, not the RAGtriever codebase.

## When to Use This Skill

- **Answering questions about vault content** - Always use RAGtriever to search indexed content
- Setting up RAGtriever for a new vault
- Configuring image analysis (Tesseract, Gemini API, or Vertex AI)
- Troubleshooting scanning or indexing issues
- Testing search and retrieval functionality
- Working with embeddings and offline mode

## CRITICAL: Answering Questions from Vault Content

**When the user asks ANY question that could be answered from vault content:**

1. **ALWAYS use `ragtriever query` to search the indexed vault**
2. **NEVER answer from memory or assumptions about the codebase**
3. **The vault content is the source of truth** - not the RAGtriever repository code itself
4. **ALWAYS cite sources in your response** - Include the file paths and locations where the information was found

### MANDATORY: Citing Sources in Responses

**Every answer based on vault content MUST include a "Sources" section at the end:**

```
## Sources
- `path/to/file.md` (Section: Heading Name)
- `folder/document.pdf` (Page: 5)
- `presentations/deck.pptx` (Slide: 12)
- `images/diagram.png` (Image analysis)
```

**Source citation rules:**
- List ALL files that contributed to the answer
- Include the specific location within the file (heading, page, slide number)
- For images, note that it came from image analysis
- Use the `rel_path` from search results
- If information comes from multiple chunks in the same file, list it once with all relevant sections

### Question Types to Search For:
- "What ideas do we have?" → Search vault for ideas
- "List all projects" → Search vault for projects
- "Who is working on X?" → Search vault for people/assignments
- "What's the status of Y?" → Search vault for status updates
- "Find information about Z" → Search vault content

### Example Query Pattern:
```bash
source .venv/bin/activate
ragtriever query --config config.toml "user's question keywords" --k 15
```

### Example Response Format:

**User asks:** "What types of agentic workflows exist?"

**Response should be:**
```
Based on the vault content, there are two main types of agentic workflows with LLMs:

1. **Reflexion - Learning from Feedback**
   - Uses self-reflection and evaluation
   - Components: Actor, Evaluator, Experience memory

2. **Multi-Agent Systems**
   - Specialized agents working together
   - Examples: Search agent, Reasoning agent, Hypothesis agent

## Sources
- `99-Images/Pasted image 20240917165150.png` (Image: Agentic workflows diagram)
- `99-Images/Pasted image 20240917165410.png` (Image: Amazon Bedrock Agents)
```

### Current Vault Configuration:
Check `test_config.toml` or the active config to see:
- Vault root path (what content is indexed)
- Index directory (where the database lives)
- Which files are included/ignored

## Pre-flight Checks

Before running any RAGtriever commands:

1. **Check virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **For offline mode (corporate proxies):**
   ```bash
   export HF_HUB_OFFLINE=1
   export TRANSFORMERS_OFFLINE=1
   ```

3. **Verify cached models:**
   ```bash
   ls ~/.cache/huggingface/hub/
   ```

## Discovering CLI Options

**IMPORTANT: Always check CLI help for current options instead of guessing:**

```bash
# Main help - shows all commands
ragtriever --help

# Command-specific help
ragtriever scan --help
ragtriever watch --help
ragtriever query --help
ragtriever init --help
ragtriever mcp --help
ragtriever status --help
```

**Why use --help:**
- Always accurate (reflects current code)
- Shows all available flags
- Includes default values
- Documents new features automatically

**Example workflow:**
```bash
# User asks: "How do I enable logging for scan?"
# Instead of guessing, check:
ragtriever scan --help | grep -A 2 log

# Output shows:
#   --log-file TEXT    Log file path for audit trail
#   --log-level TEXT   Log level: DEBUG, INFO, WARNING, ERROR
#   --verbose, -v      Enable verbose (DEBUG) logging
```

## Managing the Watcher

**The watcher automatically handles:**
- Individual file changes (create, modify, delete, move)
- Directory operations (delete entire folders, move/rename folders)
- All files within deleted or moved directories are updated in the index
- No manual intervention needed for vault reorganization

### Check if Watcher is Running
```bash
# Check for running watcher process
ps aux | grep -E "[r]agtriever watch"

# Or more precise:
pgrep -f "ragtriever watch"

# If output: process is running
# If no output: watcher is not running
```

### Start the Watcher
```bash
# Activate venv first
source .venv/bin/activate

# Start watcher (foreground)
ragtriever watch --config config.toml

# Start watcher (background with logging)
nohup ragtriever watch --config config.toml > /dev/null 2>&1 &

# Start watcher (background with config-driven logging)
# (Logs automatically to watch_{date}.log if enable_watch_logging=true)
nohup ragtriever watch --config config.toml &
echo $! > logs/watcher.pid  # Save PID for later
```

### Stop the Watcher
```bash
# Method 1: Kill all ragtriever watch processes
pkill -f "ragtriever watch"

# Method 2: Kill specific PID (if you saved it)
kill $(cat logs/watcher.pid)

# Method 3: Find and kill interactively
ps aux | grep "[r]agtriever watch"
kill <PID>

# Verify it stopped
ps aux | grep -E "[r]agtriever watch" || echo "Watcher stopped"
```

### Restart the Watcher
```bash
# Stop existing watcher
pkill -f "ragtriever watch"

# Wait for graceful shutdown
sleep 2

# Start new watcher
source .venv/bin/activate
nohup ragtriever watch --config config.toml &
echo $! > logs/watcher.pid

# Verify it started
ps aux | grep "[r]agtriever watch" && echo "Watcher running"
```

### Check Watcher Status
```bash
# Is it running?
if pgrep -f "ragtriever watch" > /dev/null; then
    echo "✓ Watcher is running"
    ps aux | grep "[r]agtriever watch" | grep -v grep
else
    echo "✗ Watcher is not running"
fi

# Check recent activity (if logging enabled)
tail -20 logs/watch_$(date +%Y%m%d).log
```

### Watcher Health Check
```bash
# 1. Check if process is running
pgrep -f "ragtriever watch" > /dev/null || echo "ERROR: Watcher not running"

# 2. Check if it's actually indexing (log activity in last 5 minutes)
find logs/ -name "watch_*.log" -mmin -5 | grep -q . && echo "✓ Recent activity" || echo "⚠ No recent log activity"

# 3. Check for errors in logs
tail -100 logs/watch_$(date +%Y%m%d).log | grep -i error && echo "⚠ Errors found" || echo "✓ No recent errors"
```

### Watcher Management Script (Simplified)

**For convenience, use the included management script:**

```bash
# Check status
./scripts/manage_watcher.sh status

# Start watcher
./scripts/manage_watcher.sh start

# Stop watcher
./scripts/manage_watcher.sh stop

# Restart watcher
./scripts/manage_watcher.sh restart

# Run health check
./scripts/manage_watcher.sh health
```

**The script handles:**
- Virtual environment activation
- PID file management
- Graceful shutdown
- Health checks (process, logs, errors)
- Log file detection

## Configuration Checklist

When setting up or modifying `config.toml`:

### Basic Setup
- [ ] `[vault]` - Set vault root path (absolute path)
- [ ] `[vault]` - Configure ignore patterns (Office temp files, .git, .obsidian/cache)
- [ ] `[index]` - Set index directory (usually `~/.ragtriever/indexes/<vault-name>`)
- [ ] `[embeddings]` - Choose provider and model
- [ ] `[embeddings]` - Set offline_mode (true if behind proxy)

### Image Analysis Provider Options

#### For Local OCR (Fastest, No API):
```toml
[image_analysis]
provider = "tesseract"
# Requires: pip install pytesseract + tesseract-ocr system package
```

#### For Gemini API (Good quality, API key):
```toml
[image_analysis]
provider = "gemini"
gemini_model = "gemini-2.0-flash"
# Set GEMINI_API_KEY environment variable
```

#### For Vertex AI (Best quality, Service account):
```toml
[image_analysis]
provider = "vertex_ai"

[vertex_ai]
project_id = "your-gcp-project-id"  # or set GOOGLE_CLOUD_PROJECT
location = "global"  # Recommended for model availability
credentials_file = "/path/to/service-account.json"  # or set GOOGLE_APPLICATION_CREDENTIALS
model = "gemini-2.0-flash-exp"
```

**Vertex AI Checklist:**
- [ ] Credentials file exists and is readable
- [ ] Use `location = "global"` for best model availability
- [ ] Unset `GEMINI_API_KEY` to avoid conflicts
- [ ] Service account has `roles/aiplatform.user` permission

#### To Disable Image Analysis:
```toml
[image_analysis]
provider = "off"
```

## Common Commands

### Initial Setup
```bash
# Install RAGtriever in development mode
pip install -e ".[dev]"

# Generate starter config
ragtriever init --vault "/path/to/vault" --index "~/.ragtriever/indexes/myvault"

# Edit config.toml to configure image analysis and embeddings
```

### Scanning and Indexing
```bash
# Full scan (re-index everything) - uses parallel processing by default
ragtriever scan --config config.toml --full

# Full scan with explicit parallel settings
ragtriever scan --config config.toml --full --workers 8

# Sequential scan (disable parallelization)
ragtriever scan --config config.toml --full --no-parallel

# Incremental scan (only changed files)
ragtriever scan --config config.toml

# Watch mode (continuous indexing)
ragtriever watch --config config.toml
```

### Scanning with Logging and Profiling
```bash
# Scan with logging to file
ragtriever scan --config config.toml --full --log-file logs/scan.log

# Scan with verbose (DEBUG) logging
ragtriever scan --config config.toml --full --log-file logs/scan.log --verbose

# Scan with profiling (performance analysis)
ragtriever scan --config config.toml --full --profile logs/profile.txt

# Scan with both logging and profiling
ragtriever scan --config config.toml --full \
    --log-file logs/scan.log \
    --profile logs/profile.txt \
    --verbose

# Watch mode with logging
ragtriever watch --config config.toml --log-file logs/watch.log --verbose
```

### Parallel Scanning (3.6x faster)
Parallel scanning is enabled by default. Configure in `config.toml`:
```toml
[indexing]
extraction_workers = 8    # Parallel file extraction workers (default: 8)
embed_batch_size = 256    # Cross-file embedding batch size
image_workers = 8         # Parallel image API workers (default: 8)
parallel_scan = true      # Enable/disable parallel scanning
```

### Logging Configuration (Audit Trail)
Configure automatic logging with date patterns in `config.toml`:
```toml
[logging]
dir = "logs"                                # Log directory
scan_log_file = "logs/scan_{date}.log"      # Daily rotation: scan_20260123.log
watch_log_file = "logs/watch_{datetime}.log" # Per-run: watch_20260123_142030.log
level = "INFO"                              # DEBUG, INFO, WARNING, ERROR
enable_scan_logging = false                 # Auto-enable for scan (false = manual via CLI)
enable_watch_logging = true                 # Auto-enable for watch (true = always log)
```

**Date patterns:**
- `{date}` → `20260123` (YYYYMMDD - daily rotation)
- `{datetime}` → `20260123_142030` (YYYYMMDD_HHMMSS - per-run logs)

**Priority:** CLI flags > config settings > no logging

**Example usage:**
```bash
# With config enable_watch_logging=true, watch automatically logs
ragtriever watch  # → logs/watch_20260123.log

# CLI flags override config
ragtriever scan --full --log-file logs/custom.log

# Check indexing results
grep '\[scan\] Complete:' logs/scan_20260123.log
grep '\[watch\] Indexed:' logs/watch_20260123.log
```

### Querying
```bash
# Basic search (hybrid: semantic + lexical)
ragtriever query --config config.toml "search term" --k 10

# More results
ragtriever query --config config.toml "kubernetes deployment" --k 20
```

### MCP Server (Claude Desktop Integration)
```bash
# Start MCP server
ragtriever mcp --config config.toml

# Add to Claude Desktop config.json:
{
  "mcpServers": {
    "ragtriever": {
      "command": "ragtriever",
      "args": ["mcp", "--config", "/full/path/to/config.toml"]
    }
  }
}
```

## Troubleshooting

### Issue: Office Temp Files (`~$*.pptx`)

**Symptom:** `PackageNotFoundError: Package not found at '~$document.pptx'`

**Solution:**
1. Close all Office applications before scanning
2. Add to ignore patterns in config.toml:
   ```toml
   [vault]
   ignore = [
       ".git/**",
       ".obsidian/cache/**",
       "**/.DS_Store",
       "**/~$*",           # Office temp files
       "**/.~lock.*"       # LibreOffice lock files
   ]
   ```
3. Remove existing temp files:
   ```bash
   find /path/to/vault -name "~$*" -delete
   ```

### Issue: Offline Mode with Uncached Model

**Symptom:** `OSError: We couldn't connect to 'https://huggingface.co'`

**Solution:**
```bash
# Option 1: Temporarily disable offline mode
export HF_OFFLINE_MODE=0
ragtriever scan --config config.toml

# Then re-enable offline mode
export HF_OFFLINE_MODE=1

# Option 2: Use a cached model
ls ~/.cache/huggingface/hub/
# Update config.toml to use one of the cached models
```

### Issue: Vertex AI Rate Limits (429 errors)

**Symptom:** `Vertex AI analysis failed: TooManyRequests`

**Expected Behavior:** This is normal with multiple images. The scan continues and processes other files.

**Solutions:**
- Most images will succeed despite some 429 errors
- Re-run scan - successful images are cached
- Consider using Gemini API or Tesseract for large image sets

### Issue: Vertex AI Authentication Errors

**Solution:**
1. Verify credentials file exists:
   ```bash
   test -r $GOOGLE_APPLICATION_CREDENTIALS && echo "OK"
   ```
2. Check environment variables:
   ```bash
   echo $GOOGLE_APPLICATION_CREDENTIALS
   echo $GOOGLE_CLOUD_PROJECT
   ```
3. Ensure `GEMINI_API_KEY` is **unset** (conflicts with Vertex AI):
   ```bash
   unset GEMINI_API_KEY
   ```
4. Test authentication:
   ```bash
   gcloud auth activate-service-account \
       --key-file=$GOOGLE_APPLICATION_CREDENTIALS
   gcloud ai models list --region=global
   ```

### Issue: FTS5 Syntax Errors with Special Characters

**Symptom:** `fts5: syntax error near "-"`

**Solution:** This is handled automatically as of recent versions. Queries with hyphens, slashes, etc. work correctly:
```bash
ragtriever query "T-DXd treatment"     # Works
ragtriever query "CDK4/6 inhibitor"    # Works
ragtriever query "HR+/HER2- cancer"    # Works
```

## Development Workflow

### Making Changes
```bash
# 1. Create feature branch
git checkout -b feature/your-feature

# 2. Make changes to code

# 3. Reinstall after code changes
pip install -e ".[dev]"

# 4. Run linting
ruff check src/ tests/

# 5. Run tests
pytest
```

### Testing Image Analysis
```bash
# Test with small vault first (1-3 images)
ragtriever scan --config config.toml --full

# Check logs for errors
# tail -100 scan.log

# Query for image content
ragtriever query --config config.toml "image description" --k 5

# Verify results include image metadata
```

## Verifying Successful Indexing

### Scan Mode
**Console output:**
```
Scan complete: 135 files, 963 chunks in 133.0s
```

**Log file (if logging enabled):**
```bash
# View summary
grep '\[scan\] Complete:' logs/scan_20260123.log

# Check phases
grep '\[scan\] Phase' logs/scan_20260123.log

# Output:
# [scan] Phase 1: 135 files extracted, 0 failed
# [scan] Phase 2: 963 chunks, 963 embeddings
# [scan] Complete: 135 files indexed in 133.0s
```

### Watch Mode
**Individual file indexing (INFO level):**
```bash
# List all indexed files
grep '\[watch\] Indexed:' logs/watch_20260123.log

# Output:
# [watch] Indexed: path/to/file1.pdf
# [watch] Indexed: path/to/file2.md
# [watch] Indexed: image.jpg
```

**Batch writes (DEBUG level):**
```bash
# See database writes
grep '\[batch\] Stored' logs/watch_20260123.log

# Output:
# [batch] Stored 8 docs, 335 chunks, 335 embeddings
```

**Real-time monitoring:**
```bash
# Terminal 1: Run watcher
ragtriever watch

# Terminal 2: Monitor indexing
tail -f logs/watch_20260123.log | grep '\[watch\] Indexed:'
```

### Check for Failures
```bash
# Scan or watch failures
grep -E 'Failed:|ERROR' logs/*.log

# Count indexed files
grep -c '\[watch\] Indexed:' logs/watch_20260123.log
```

### Verify in Database
```bash
ragtriever status
# Output: Indexed files: 135, Indexed chunks: 963
```

## Key Files Reference

### Code
- `src/ragtriever/extractors/image.py` - Image extractor implementations
- `src/ragtriever/config.py` - Configuration management (includes [logging] support)
- `src/ragtriever/cli.py` - CLI commands (scan, watch, query with logging/profiling)
- `src/ragtriever/indexer/indexer.py` - Main indexer orchestration
- `src/ragtriever/retrieval/retriever.py` - Hybrid search implementation

### Configuration
- `examples/config.toml.example` - Configuration template with [logging] section
- `config.toml` - User configuration

### Documentation
- `docs/ARCHITECTURE.md` - Complete system architecture
- `docs/LOGGING_CONFIGURATION.md` - Logging setup and usage guide
- `docs/WHERE_TO_SEE_INDEXING.md` - How to verify indexing success
- `docs/SCAN_AND_WATCH_TESTING.md` - Testing guide with profiling
- `docs/vertex_ai_setup.md` - Vertex AI setup guide
- `docs/troubleshooting.md` - Detailed troubleshooting
- `IMPROVEMENTS.md` - Planned enhancements

### Testing Scripts
- `scripts/test_scan_and_watch.sh` - Automated test with logging and profiling

## Architecture Quick Reference

### Data Flow (Parallel Pipeline)
```
Vault (filesystem)
  → File Discovery (Reconciler)
  → Phase 1: Parallel Extraction + Chunking (ThreadPoolExecutor)
  → Phase 2: Batched Embedding (cross-file batches of 256)
  → Phase 3: Parallel Image Analysis (if enabled)
  → Store (SQLite + FTS5)
  → Retrieval (hybrid search)
```

### Image Analysis Pipeline
```
Image file
  → ImageExtractor (Tesseract/Gemini/Vertex AI)
  → Structured analysis (description, OCR, topics, entities)
  → Chunking
  → Indexing
  → Searchable via query
```

### Execution Modes
- **CLI**: `ragtriever scan/query/watch/mcp`
- **Watch Mode**: Continuous filesystem monitoring
- **MCP Server**: Integration with Claude Desktop
- **Python API**: Programmatic import and use

## Success Criteria

After running a scan, verify:
- [ ] Scan completes without fatal errors
- [ ] Rate limit errors (429) are logged but don't stop scan
- [ ] Database created: `~/.ragtriever/indexes/<vault>/vaultrag.sqlite`
- [ ] Query returns results
- [ ] Image content is searchable (if images in vault)
- [ ] Metadata includes analysis_provider and model name

**Check indexing stats:**
```bash
# Count documents
sqlite3 ~/.ragtriever/indexes/myvault/vaultrag.sqlite \
    "SELECT COUNT(*) FROM documents WHERE deleted=0;"

# Count chunks
sqlite3 ~/.ragtriever/indexes/myvault/vaultrag.sqlite \
    "SELECT COUNT(*) FROM chunks;"

# Show file types
sqlite3 ~/.ragtriever/indexes/myvault/vaultrag.sqlite \
    "SELECT file_type, COUNT(*) FROM documents WHERE deleted=0 GROUP BY file_type;"
```

## Quick Workflows

### Test Scan & Watch (Automated)
```bash
# Automated test with logging, profiling, and watcher
./scripts/test_scan_and_watch.sh

# This will:
# 1. Clean database
# 2. Run full scan with 10 workers and profiling
# 3. Show profiling summary
# 4. Show scan log summary
# 5. Prompt to test watcher

# Logs saved to: logs/scan_YYYYMMDD_HHMMSS.log
# Profile saved to: logs/scan_profile_YYYYMMDD_HHMMSS.txt
# Watch logs: logs/watch_YYYYMMDD_HHMMSS.log
```

### Setup New Vault (Tesseract)
```bash
source .venv/bin/activate
ragtriever init --vault ~/vault --index ~/.ragtriever/indexes/myvault
# Edit config.toml: set provider = "tesseract"
ragtriever scan --config config.toml --full
ragtriever query --config config.toml "test query" --k 5
```

### Setup with Vertex AI
```bash
source .venv/bin/activate
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/creds.json"
export HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
unset GEMINI_API_KEY
ragtriever init --vault ~/vault --index ~/.ragtriever/indexes/myvault
# Edit config.toml: configure [vertex_ai] section
ragtriever scan --config config.toml --full
ragtriever query --config config.toml "image content" --k 5
```

### Incremental Updates
```bash
source .venv/bin/activate
ragtriever scan --config config.toml  # Only changed files
```

### Watch Mode (Background)
```bash
source .venv/bin/activate

# Start watcher in background
nohup ragtriever watch --config config.toml &
echo $! > logs/watcher.pid

# Check if running
pgrep -f "ragtriever watch" && echo "✓ Watcher running"

# Stop watcher later
pkill -f "ragtriever watch"
```

## Additional Resources

- **README.md**: User guide and quick start
- **CLAUDE.md**: Project architecture for Claude Code
- **docs/architecture.md**: Complete system documentation
- **docs/vertex_ai_setup.md**: Vertex AI service account setup
- **docs/troubleshooting.md**: Comprehensive troubleshooting guide
- **IMPROVEMENTS.md**: Planned features (Gemini 3, better error handling, etc.)

## Tips for Claude Code Users

When helping users with RAGtriever:

1. **ALWAYS search vault content first** - When user asks questions, use `ragtriever query` to search indexed vault
2. **ALWAYS cite sources** - Every response MUST end with a "Sources" section listing file paths and locations
3. **Vault content ≠ RAGtriever code** - Don't confuse searching the vault (user's content) with RAGtriever repository code
4. **Use --help to discover options** - Run `ragtriever <command> --help` instead of guessing flags or parameters
5. **Check if watcher is running** - Use `pgrep -f "ragtriever watch"` before starting/restarting
6. **Always check config first** - Most issues stem from configuration (now includes [logging] section)
7. **Verify virtual environment** - Commands fail if venv not activated
8. **Check file paths** - Use absolute paths, expand ~
9. **Office temp files** - First thing to check if PPTX extraction fails
10. **Offline mode** - Corporate users need this; verify model is cached
11. **Rate limits are OK** - 429 errors are expected with many images
12. **Test incrementally** - Small vault first, then scale up
13. **Use logging for debugging** - Enable `--log-file` to trace indexing issues
14. **Verify indexing success** - Check `[scan] Complete:` or `[watch] Indexed:` in logs
15. **Profile performance** - Use `--profile` to identify bottlenecks
16. **Enable watch logging by default** - Set `enable_watch_logging = true` for production
17. **Restart watcher when needed** - After config changes, code updates, or if it stops responding

### Watcher Management Workflow

When user mentions watcher issues:
```bash
# 1. Check if running
pgrep -f "ragtriever watch" || echo "Not running"

# 2. If not running, start it
source .venv/bin/activate
nohup ragtriever watch --config config.toml &

# 3. If running but needs restart
pkill -f "ragtriever watch"
sleep 2
source .venv/bin/activate
nohup ragtriever watch --config config.toml &

# 4. Verify it's working
tail -20 logs/watch_$(date +%Y%m%d).log
```

## Notes

- RAGtriever is a standalone tool, not a Claude Code skill itself
- This skill provides workflow assistance for using RAGtriever
- RAGtriever runs independently and can work without Claude
- Optional MCP integration enables Claude Desktop to search your vault
