# File Reading (read_file)

## Contents
- `read_file`

### `read_file`
**Purpose**: Repo-scoped file access (by default) with deterministic scan/chunk/page/search modes, dependency analysis, and read provenance logging. Optional out-of-repo reads are allowed when explicitly enabled.

**Required Parameters:**
- `path` (string): File path (absolute or repo-relative)

**Optional Parameters:**
- `mode`: `scan_only` (default), `chunk`, `line_range`, `page`, `full_stream`, `search`
- `chunk_index`: Chunk index or list of indices (for `chunk` mode)
- `start_line` / `end_line`: Explicit line range (for `line_range`)
- `page_number` / `page_size`: Pagination controls (for `page`)
- `start_chunk` / `max_chunks`: Streaming controls (for `full_stream`)
- `search`: Search term (for `search` mode)
- `query`: Alias for `search` (for `search` mode, defaults to smart inference)
- `search_mode`: `regex` (default) or `literal` - **Note: Default changed from literal to regex**
- `context_lines`: Lines of context around matches (search mode)
- `max_matches`: Max matches to return (search mode)
- `include_dependencies`: `False` (default) or `True` - Enable dependency analysis (Python files only)
- `include_impact`: `False` (default) or `True` - Include impact radius (requires `include_dependencies=True`)
- `allow_outside_repo`: `False` (default) or `True` - Allow reads outside repo_root (denylist still enforced). Paths under `/.claude/skills/` or `/.codex/skills/` are always allowed.
- `format`: `readable` (default), `structured`, or `compact` - Output format

**Scan Mode Enhancements:**
When `mode="scan_only"`, the tool automatically detects file type and extracts structure:

- **Python files**: AST analysis showing functions, classes, methods with line numbers and signatures
- **Markdown files**: Heading hierarchy with line numbers (max 100 headings)
- **JavaScript/TypeScript**: Basic structure detection
- **SKILL.md detection**: Special urgent warning when reading SKILL.md files
- **Navigation hints**: Suggested chunk sizes and example calls for large files

**Dependency Analysis (`include_dependencies=True`):**
Provides static analysis of Python imports with governance features:

1. **Import Categorization**:
   - **Standard Library**: Python stdlib imports (detected via sys.stdlib_module_names)
   - **Third-Party Packages**: External dependencies from pip/conda
   - **Local Modules**: Project-internal imports with path resolution and existence checks

2. **Path Resolution**:
   - Resolves relative imports (e.g., `from ..utils import helper`)
   - Resolves absolute imports (e.g., `from scribe_mcp.tools import append_entry`)
   - Shows resolved file paths with ✓ checkmarks when files exist
   - Detects workspace root automatically (.git, pyproject.toml markers)

3. **Impact Radius (Blast Radius)**:
   - Shows how many files import the current file
   - Categorized by impact level:
     - **Low**: 0-4 importers
     - **Medium**: 5-15 importers (⚠️ warning)
     - **High**: 16+ importers (🚨 high impact)
   - Lists up to 20 files that import this module
   - Helps assess change risk before modifications

4. **Boundary Enforcement**:
   - Checks imports against `.scribe/config/boundary_rules.yaml` rules
   - Detects forbidden import patterns (e.g., "sentinel layer must not import tools")
   - Shows violations with severity levels: ERROR, WARNING, INFO
   - Supports glob patterns with `**` for recursive matching
   - Respects `allowed_exceptions` for legitimate edge cases

5. **Static Analysis Disclaimer**:
   - Automatically included when dependencies or impact radius shown
   - Clarifies that only import-time relationships are detected
   - Honest about limitations: no runtime dependencies, dynamic imports, or reflection patterns

**Example Usage:**
```python
# Basic scan (metadata + structure)
await read_file(path="tools/read_file.py", mode="scan_only")

# Scan with dependency analysis
await read_file(path="tools/read_file.py", mode="scan_only", include_dependencies=True)

# Read specific chunk
await read_file(path="references/Scribe_Usage.md", mode="chunk", chunk_index=[0])

# Regex search (default mode)
await read_file(path="tools/read_file.py", mode="search", query=r"async\s+def\s+\w+")

# Literal search (explicit)
await read_file(path="references/Scribe_Usage.md", mode="search", search="semantic", search_mode="literal")

# Search with context lines
await read_file(path="server.py", mode="search", query="async def", context_lines=2)
```

**Configuration:**
Boundary rules are defined in `.scribe/config/boundary_rules.yaml`:
```yaml
version: 1.0
enabled: true
rules:
  - name: "Sentinel Layer Isolation"
    severity: "error"
    pattern:
      source: "sentinel/**/*.py"
      forbidden_imports:
        - "tools/**"
        - "scribe_mcp.tools.*"
```

**Performance:**
- Dependency analysis: ~20% overhead when enabled (opt-in)
- Impact radius: <3s for typical repositories (<500 Python files)
- Boundary checking: <20ms overhead per file
- Zero overhead when `include_dependencies=False` (default)

**Notes:**
- Every read is logged with provenance (absolute path, hash, byte size, encoding, read mode)
- Enforces repo scope by default; out-of-scope paths are denied
- Dependency analysis is static only - does not execute code or resolve runtime imports
- Impact radius requires workspace root detection (looks for .git, pyproject.toml markers)
