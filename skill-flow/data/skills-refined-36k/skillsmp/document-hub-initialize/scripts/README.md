# Documentation Hub Python Tools

This directory contains Python scripts that power the `/document-hub` skills. These tools provide specialized functionality for analyzing, validating, and maintaining project documentation.

## Overview

All scripts follow the [Anthropic Tool Use pattern](https://www.anthropic.com/engineering/advanced-tool-use):
- Accept JSON-structured command-line arguments
- Return structured JSON output
- Use only Python standard library (zero dependencies)
- Are executable and can be invoked directly

## Tools

### 1. validate_hub.py

**Purpose:** Validate documentation hub structure and content

**Usage:**
```bash
python3 validate_hub.py /path/to/project
```

**Returns:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    {
      "file": "systemArchitecture.md",
      "line": 42,
      "message": "Complex diagram with 25 connections"
    }
  ],
  "checks_run": 5
}
```

**Checks:**
- File structure (all required files exist)
- Mermaid diagram syntax
- Cross-references between files
- Glossary structure
- /arch subfolder structure

---

### 2. detect_drift.py

**Purpose:** Detect drift between documentation and actual codebase

**Usage:**
```bash
python3 detect_drift.py /path/to/project
```

**Returns:**
```json
{
  "drift_score": 0.15,
  "status": "good",
  "module_drift": {
    "undocumented": ["analytics", "webhooks"],
    "documented_but_missing": []
  },
  "technology_drift": {
    "undocumented": ["Redis", "BullMQ"],
    "documented_but_missing": []
  },
  "recommendations": [
    "Add analytics module to keyPairResponsibility.md",
    "Add Redis and BullMQ to techStack.md"
  ]
}
```

**Compares:**
- Documented modules vs. actual src/ directories
- Documented technologies vs. package.json/requirements.txt
- Configuration files vs. techStack.md

---

### 3. analyze_changes.py

**Purpose:** Analyze git changes since last documentation update

**Usage:**
```bash
# Auto-detect last doc update
python3 analyze_changes.py /path/to/project

# Analyze since specific commit
python3 analyze_changes.py /path/to/project abc123
```

**Returns:**
```json
{
  "changed_files": 42,
  "since_commit": "abc123",
  "categories": {
    "architecture": 2,
    "modules": 3,
    "config": 1,
    "dependencies": 1
  },
  "descriptions": [
    "Updated 1 dependency file(s)",
    "Changes in modules: src/auth, src/payments"
  ],
  "suggestions": [
    {
      "file": "systemArchitecture.md",
      "reason": "core architecture files changed",
      "priority": "high"
    }
  ],
  "commit_messages": [
    "Add payment processing module",
    "Refactor authentication flow"
  ]
}
```

**Categorizes:**
- Architecture changes
- Module additions/changes
- Configuration updates
- Dependency updates
- Database schema changes
- API/route modifications

---

### 4. extract_glossary.py

**Purpose:** Extract domain-specific terms from codebase

**Usage:**
```bash
# Default: scan all .ts, .tsx, .js, .jsx, .py files
python3 extract_glossary.py /path/to/project

# Custom patterns
python3 extract_glossary.py /path/to/project "**/*.ts,**/*.py"

# With minimum occurrence threshold
python3 extract_glossary.py /path/to/project "**/*.ts" 3
```

**Returns:**
```json
{
  "total_terms": 42,
  "scanned_files": 156,
  "min_occurrences": 2,
  "terms": [
    {
      "term": "FulfillmentJob",
      "occurrences": 15,
      "contexts": [
        "Represents a job in the fulfillment pipeline",
        "Tracks order processing status and completion"
      ],
      "files": ["src/fulfillment/job.ts", "src/api/jobs.ts"],
      "score": 45
    }
  ]
}
```

**Extracts:**
- Class names (TypeScript, JavaScript, Python)
- Function names with domain significance
- Interface and type definitions
- Context from comments and docstrings

**Filters out:**
- Generic programming terms (data, config, handler, etc.)
- Common verbs (get, set, create, etc.)
- Test files
- node_modules and similar directories

---

## Integration with Skills

These tools are invoked by skills via the standard tool use pattern:

```markdown
## In skills/hub/initialize.md

Use the validate_documentation_hub tool to check structure:
- This tool validates all required files exist
- Returns structured errors and warnings
- Claude can parse the JSON output and take action
```

Claude Code recognizes these scripts as available tools and can invoke them during skill execution.

## Testing Tools Standalone

You can test these tools directly from the command line:

```bash
# Navigate to scripts directory
cd ~/.claude/skills/hub/scripts

# Test validation
python3 validate_hub.py ~/applications/my-project

# Test drift detection
python3 detect_drift.py ~/applications/my-project

# Test change analysis
python3 analyze_changes.py ~/applications/my-project

# Test glossary extraction
python3 extract_glossary.py ~/applications/my-project
```

## Error Handling

All scripts follow consistent error handling:

**Exit codes:**
- `0`: Success (even if validation fails - check JSON output)
- `1`: Fatal error (invalid args, file not found, etc.)

**Error format:**
```json
{
  "error": "Description of what went wrong"
}
```

**Warning format:**
```json
{
  "valid": true,
  "errors": [],
  "warnings": [
    {
      "file": "filename.md",
      "line": 42,
      "message": "Warning description"
    }
  ]
}
```

## Dependencies

**None!** All scripts use Python standard library only:
- `json` - JSON parsing
- `sys` - Command-line arguments
- `re` - Regular expressions
- `pathlib` - File path handling
- `subprocess` - Git commands
- `collections` - Data structures

This ensures:
- Fast installation (no pip install needed)
- Maximum compatibility
- Minimal maintenance overhead

## Performance

All tools are optimized for performance:

- **validate_hub.py**: < 1 second for typical projects
- **detect_drift.py**: < 2 seconds for typical projects
- **analyze_changes.py**: < 1 second (git is fast)
- **extract_glossary.py**: 5-10 seconds for large codebases

For very large projects (1000+ files), `extract_glossary.py` may take longer. Consider using file pattern filtering to scope the scan.

## Adding New Tools

To add a new tool:

1. Create `new_tool.py` in this directory
2. Follow the JSON input/output pattern
3. Make it executable: `chmod +x new_tool.py`
4. Add documentation to this README
5. Reference it in the appropriate skill markdown file

**Template:**
```python
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Project path required"}))
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()

    # Your logic here

    output = {
        "result": "success",
        "data": {}
    }

    print(json.dumps(output, indent=2))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

## Troubleshooting

### Script not executable
```bash
chmod +x script_name.py
```

### Python version issues
All scripts require Python 3.6+. Check version:
```bash
python3 --version
```

### JSON parsing errors
Ensure you're capturing stdout only, not stderr:
```bash
python3 script.py /path 2>/dev/null
```

### Git repository required
`analyze_changes.py` requires the project to be a git repository. If not:
```bash
cd /path/to/project
git init
```

## Contributing

When modifying these tools:

1. Maintain backward compatibility
2. Keep JSON output structure consistent
3. Add tests if adding complex logic
4. Update this README
5. Follow PEP 8 style guidelines

## License

These tools are part of the Claude Code configuration and follow the same license as the parent project.
