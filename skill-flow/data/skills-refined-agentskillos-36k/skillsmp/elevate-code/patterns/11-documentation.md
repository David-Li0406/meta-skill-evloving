# Pattern 11: Documentation

**Problem**: No one knows how the tool works. New contributors can't onboard. AI assistants can't help effectively.

**Solution**: Write a README for users, CLAUDE.md for AI, and inline docs for developers.

---

## Concept

Documentation answers: **"How does this work?"**

Good documentation provides:
1. **Quick Start** — Users can try it in 2 minutes
2. **Reference** — Complete option documentation
3. **Architecture** — AI and developers understand the design
4. **Examples** — Real-world usage patterns

---

## README.md Template

```markdown
# My Tool

One-line description of what this tool does.

## Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## Installation

```bash
# pip (Python)
pip install my-tool

# npm (Node.js)
npm install -g my-tool

# Homebrew (macOS)
brew install my-tool
```

## Quick Start

```bash
# Basic usage
my-tool process input.txt

# With options
my-tool process input.txt -o output.txt --format json

# Check setup
my-tool doctor
```

## Usage

### process

Process input files and generate output.

```bash
my-tool process <input> [options]
```

**Arguments:**
- `<input>` - Input file or glob pattern

**Options:**
- `-o, --output <path>` - Output file (default: stdout)
- `-f, --format <type>` - Output format: text, json, csv (default: text)
- `-v, --verbose` - Enable verbose output
- `--dry-run` - Preview changes without applying

**Examples:**

```bash
# Process single file
my-tool process data.txt -o result.txt

# Process multiple files
my-tool process "*.txt" --format json

# Preview changes
my-tool process data.txt --dry-run
```

### doctor

Check dependencies and configuration.

```bash
my-tool doctor
```

## Configuration

Configuration file location: `~/.config/my-tool/config.json`

```json
{
  "api_key": "your-api-key",
  "output_format": "text",
  "verbose": false
}
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MY_TOOL_API_KEY` | API key for service | (required) |
| `MY_TOOL_CONFIG` | Config file path | `~/.config/my-tool/config.json` |

## Troubleshooting

### "API key not found"

Set your API key:

```bash
export MY_TOOL_API_KEY=your-key
# or
my-tool config set api_key your-key
```

### "Command not found"

Ensure the tool is in your PATH:

```bash
# Check installation
which my-tool

# Reinstall if needed
pip install --force-reinstall my-tool
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup.

## License

MIT License - see [LICENSE](LICENSE) for details.
```

---

## CLAUDE.md Template

CLAUDE.md is specifically for AI assistants (Claude, Copilot, etc.) to understand your project.

```markdown
# My Tool - AI Collaboration Guide

## Project Overview

My Tool is a [type] that [what it does]. It's built with [tech stack]
and follows [architecture pattern].

**Key files:**
- `src/my_tool/cli.py` - Entry point, argument parsing
- `src/my_tool/pipeline.py` - Main processing logic
- `src/my_tool/models.py` - Data structures

## Architecture

```
Input → Preprocessor → Processor → Formatter → Output
```

### Data Flow

1. CLI parses arguments into `Config` dataclass
2. `Pipeline` orchestrates processing stages
3. Each stage transforms data and passes to next
4. `Formatter` outputs in requested format

### Key Patterns

- **Doctor pattern**: `cli.py:doctor()` checks dependencies
- **State persistence**: `.state.json` for crash recovery
- **Undo log**: `deletion_log.json` for reversibility

## Conventions

### Code Style
- Python 3.10+, type hints required
- Ruff for linting (line length 100)
- Dataclasses for all data structures
- No raw dicts in function signatures

### Naming
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `SCREAMING_SNAKE_CASE`

### Error Handling
- Custom exceptions inherit from `ToolError`
- Error messages include: what, why, fix
- Retry transient errors with exponential backoff

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/my_tool

# Run specific test
pytest tests/test_pipeline.py -k "test_process"
```

### Test Organization
- `tests/conftest.py` - Shared fixtures
- Mock external APIs (no real network calls)
- Use `@pytest.mark.slow` for integration tests

## Common Tasks

### Adding a new command

1. Add handler in `cli.py`
2. Create business logic in appropriate module
3. Add tests in `tests/test_<module>.py`
4. Update README.md with usage

### Adding a new output format

1. Add formatter in `formatters.py`
2. Register in `FORMATTERS` dict
3. Add `--format` option in CLI
4. Add tests for new format

### Debugging

```bash
# Verbose output
my-tool process input.txt -v

# Debug mode (shows stack traces)
MY_TOOL_DEBUG=1 my-tool process input.txt
```

## Dependencies

### Runtime
- `click` - CLI framework
- `rich` - Terminal formatting
- `requests` - HTTP client

### Development
- `pytest` - Testing
- `ruff` - Linting
- `mypy` - Type checking

## Gotchas

- **FFmpeg version**: Requires 4.x-7.x (not 8.x)
- **API rate limits**: 100 req/min, use `--delay` for batch
- **Large files**: Use `--stream` to avoid memory issues
```

---

## Inline Documentation

### Python Docstrings

```python
def process_file(
    input_path: str,
    output_path: str | None = None,
    format: str = "text"
) -> ProcessResult:
    """Process a file and generate output.

    Reads the input file, applies transformations, and writes
    the result to the output path or stdout.

    Args:
        input_path: Path to the input file. Supports glob patterns.
        output_path: Path for output. If None, writes to stdout.
        format: Output format - "text", "json", or "csv".

    Returns:
        ProcessResult containing the output and metadata.

    Raises:
        FileNotFoundError: If input_path doesn't exist.
        ValidationError: If input file is invalid.
        ProcessingError: If transformation fails.

    Example:
        >>> result = process_file("data.txt", format="json")
        >>> print(result.output)
        {"items": [...]}
    """
    pass
```

### TypeScript JSDoc

```typescript
/**
 * Process a file and generate output.
 *
 * Reads the input file, applies transformations, and writes
 * the result to the output path or stdout.
 *
 * @param inputPath - Path to the input file
 * @param options - Processing options
 * @param options.outputPath - Path for output (default: stdout)
 * @param options.format - Output format: "text" | "json" | "csv"
 * @returns Promise resolving to ProcessResult
 * @throws {FileNotFoundError} If input doesn't exist
 * @throws {ValidationError} If input is invalid
 *
 * @example
 * const result = await processFile("data.txt", { format: "json" });
 * console.log(result.output);
 */
async function processFile(
  inputPath: string,
  options?: ProcessOptions
): Promise<ProcessResult> {
  // ...
}
```

---

## Documentation Checklist

### README.md
- [ ] One-line description
- [ ] Installation instructions (all methods)
- [ ] Quick start (< 2 minutes to first use)
- [ ] All commands documented with examples
- [ ] Configuration options listed
- [ ] Troubleshooting section

### CLAUDE.md
- [ ] Project overview and architecture
- [ ] Key files and their purposes
- [ ] Code conventions and patterns
- [ ] Testing instructions
- [ ] Common development tasks
- [ ] Known gotchas

### Inline Docs
- [ ] All public functions have docstrings
- [ ] Complex logic has inline comments
- [ ] Examples in docstrings
- [ ] Type hints throughout

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| No README | Users can't get started | Write basic README |
| README only | AI can't help effectively | Add CLAUDE.md |
| Outdated docs | Worse than no docs | Docs in CI (fail on mismatch) |
| Too much docs | No one reads it | Focus on quick start + reference |
