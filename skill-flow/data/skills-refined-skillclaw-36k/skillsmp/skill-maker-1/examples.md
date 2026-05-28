# Skill Maker - Usage Examples

This document presents comprehensive examples demonstrating the skill-maker's application across diverse use cases.

## Example 1: Simple File Processor (Complete Specification)

### User Request

```
Create a skill for processing JSON files. It should read JSON, validate structure,
and pretty-print formatted output. Use when working with JSON files.
```

### Skill-Maker Analysis

**Information Completeness**: ✅ Sufficient
- Function: JSON processing (read, validate, format)
- Triggers: JSON files, JSON-related queries
- Tools: Read, Write, Bash (for jq if needed)
- Dependencies: Python json module (built-in) or jq
- Scope: Well-defined

**Action**: Proceed directly to generation

### Generated Skill Structure

**Directory**: `.claude/skills/json-processor/`

**SKILL.md**:
```yaml
---
name: json-processor
description: Read, validate, and pretty-print JSON files. Use when working with JSON files, .json extensions, or when user mentions JSON formatting, validation, or parsing.
---

# JSON Processor

## Instructions

### Phase 1: File Reading
1. Use Read tool to access the target JSON file
2. If file not found, report error with full path

### Phase 2: Validation
1. Attempt to parse JSON content using Python json module:
   ```bash
   python -c "import json, sys; json.load(open('file.json'))"
   ```
2. If parsing fails, report specific syntax error location
3. If parsing succeeds, proceed to formatting

### Phase 3: Formatting
1. Pretty-print JSON with indentation:
   ```bash
   python -c "import json; print(json.dumps(json.load(open('file.json')), indent=2))"
   ```
2. Use Write tool to save formatted output if requested
3. Display formatted JSON to user

## Common Operations

### Validate Only
If user requests validation without formatting, execute Phase 1-2 only.

### Format Only
If JSON is known to be valid, skip validation and proceed to formatting.

### Minify JSON
For minification requests, use compact formatting:
```bash
python -c "import json; print(json.dumps(json.load(open('file.json')), separators=(',', ':')))"
```

## Error Handling

### Syntax Errors
Report line number and character position from json module error message.

### File Access Errors
Verify file path and permissions, provide specific error context.
```

### Activation Test Queries

- ✅ "Validate this JSON file"
- ✅ "Pretty-print data.json"
- ✅ "Check if this .json file is valid"
- ✅ "Format the JSON configuration"
- ❌ "Process this CSV file" (should not activate)

---

## Example 2: Ambiguous Request Requiring Clarification

### User Request

```
Make a skill for documentation.
```

### Skill-Maker Analysis

**Information Completeness**: ❌ Insufficient
- Function: "documentation" (too vague)
- Triggers: Not specified
- Tools: Unknown
- Dependencies: Unknown
- Scope: Undefined

**Action**: Request clarification

### Skill-Maker Questions

```
To generate an appropriate skill for documentation, I require additional information:

1. **Documentation Type**: What specific documentation format should this skill handle?
   - API documentation (OpenAPI, Swagger)
   - README files (Markdown)
   - Code comments (JSDoc, docstrings)
   - User manuals (HTML, PDF)
   - Other (please specify)

2. **Primary Operation**: What should this skill do with documentation?
   - Generate documentation from code
   - Validate existing documentation
   - Transform between formats
   - Extract information from documentation
   - Update/modify documentation
   - Other (please specify)

3. **File Formats**: Which file extensions are relevant?
   - .md (Markdown)
   - .rst (reStructuredText)
   - .html
   - .yaml/.json (OpenAPI specs)
   - Source code files (for comment extraction)
   - Other (please specify)

4. **Activation Context**: When should this skill activate?
   - User mentions "documentation" or "docs"
   - User references specific file types
   - User requests specific operations (generate, validate, etc.)

Please provide clarification, and I shall generate the appropriate skill.
```

### User Clarification

```
I want to generate API documentation from Python docstrings. Should work with .py files
and create markdown documentation.
```

### Skill-Maker Analysis (Updated)

**Information Completeness**: ✅ Sufficient
- Function: Extract Python docstrings, generate Markdown docs
- Triggers: Python files, docstring mentions, API documentation
- Tools: Read, Write, Bash (for Python execution)
- Dependencies: Python (built-in), potentially pydoc or sphinx
- Scope: Well-defined

**Action**: Proceed to generation

### Generated Skill: python-docstring-extractor

```yaml
---
name: python-docstring-extractor
description: Extract Python docstrings and generate Markdown API documentation. Use when working with .py files, Python code, or when user mentions docstrings, API docs, or documentation generation for Python.
---

# Python Docstring Extractor

## Instructions

### Phase 1: Source Analysis
1. Use Read tool to access Python source file
2. Identify all functions, classes, and modules with docstrings
3. Parse docstring format (Google, NumPy, or reStructuredText style)

### Phase 2: Documentation Extraction
1. For each documented entity, extract:
   - Name and signature
   - Description text
   - Parameters and types
   - Return values
   - Raises/Exceptions
   - Examples (if present)

2. Use Python's `inspect` module for structured extraction:
   ```bash
   python -c "import inspect, importlib.util;
   spec = importlib.util.spec_from_file_location('module', 'file.py');
   mod = importlib.util.module_from_spec(spec);
   spec.loader.exec_module(mod);
   print(inspect.getdoc(mod))"
   ```

### Phase 3: Markdown Generation
1. Generate Markdown with following structure:
   ```markdown
   # Module Name

   [Module docstring]

   ## Functions

   ### function_name(param1, param2)

   [Function description]

   **Parameters:**
   - `param1` (type): description
   - `param2` (type): description

   **Returns:**
   - return_type: description

   **Example:**
   ```python
   [example code]
   ```
   ```

2. Use Write tool to save generated documentation
3. Default filename: `API_DOCUMENTATION.md`

## Requirements

Requires Python 3.6+ (uses f-strings and type hints parsing).

For advanced parsing, optionally install:
```bash
pip install docstring-parser
```

## Common Workflows

### Single File Documentation
Process one Python file, generate corresponding markdown.

### Module Documentation
Process entire Python package, generate consolidated documentation.

### Incremental Updates
Re-generate documentation when source files change.
```

---

## Example 3: Security-Sensitive Read-Only Skill

### User Request

```
Create a skill for analyzing system logs without modifying them. Should search for
errors, warnings, and patterns in log files.
```

### Skill-Maker Analysis

**Information Completeness**: ✅ Sufficient
**Security Consideration**: ⚠️ Read-only requirement detected

**Action**: Generate with tool restrictions

### Generated Skill: log-analyzer

```yaml
---
name: log-analyzer
description: Analyze system logs, search for errors, warnings, and patterns without modifications. Use when working with .log files, syslog, or when user mentions log analysis, error searching, or system diagnostics.
allowed-tools: Read, Grep, Glob, Bash
---

# Log Analyzer (Read-Only)

## Security Notice

This skill operates in READ-ONLY mode. Tool access is restricted to prevent
accidental log file modifications. Bash commands are limited to read operations.

## Instructions

### Phase 1: Log File Discovery
1. Use Glob tool to locate log files:
   - `/var/log/*.log` (Linux/macOS)
   - `C:/Windows/System32/winevt/Logs/*` (Windows Event Logs)
   - User-specified log directory

2. Present discovered log files for user selection

### Phase 2: Pattern Searching
1. Use Grep tool to search for common patterns:

   **Error Detection**:
   ```
   Pattern: (ERROR|FATAL|CRITICAL|Exception|Failed)
   ```

   **Warning Detection**:
   ```
   Pattern: (WARN|WARNING|Deprecated)
   ```

   **Custom Patterns**:
   User-specified regex patterns

2. Display matches with context (-C 3 for 3 lines before/after)

### Phase 3: Analysis and Reporting
1. Aggregate findings:
   - Count occurrences by severity level
   - Identify most frequent error messages
   - Detect temporal patterns (if timestamps present)

2. Generate summary report:
   ```markdown
   # Log Analysis Report

   **File**: /var/log/application.log
   **Analysis Date**: [timestamp]

   ## Summary Statistics
   - Errors: [count]
   - Warnings: [count]
   - Total Lines Analyzed: [count]

   ## Top Errors
   1. [error message] ([count] occurrences)
   2. [error message] ([count] occurrences)

   ## Recent Critical Events
   [Last 5 error entries with timestamps]
   ```

3. Use Read tool for detailed examination of specific log sections

### Phase 4: Read-Only Bash Commands

Permitted Bash operations (read-only):
```bash
# Count lines
wc -l /var/log/app.log

# Show recent entries
tail -n 100 /var/log/app.log

# Search with grep
grep -i "error" /var/log/app.log

# File metadata
ls -lh /var/log/app.log
stat /var/log/app.log
```

**PROHIBITED** operations (enforced by instructions):
- No file writes (>, >>)
- No file modifications (sed -i, tee)
- No file deletions (rm)
- No log rotation commands

## Common Workflows

### Workflow 1: Error Investigation
1. Search for ERROR level messages
2. Extract context around each error
3. Identify error frequency and patterns
4. Report findings to user

### Workflow 2: Time-Range Analysis
1. Filter log entries by timestamp range
2. Analyze events within specified period
3. Generate temporal distribution report

### Workflow 3: Pattern Correlation
1. Search for multiple related patterns
2. Correlate events across log files
3. Identify causal relationships

## Error Handling

### Permission Denied
If log files require elevated permissions:
1. Report specific file and permission requirements
2. Suggest using sudo/administrator privileges
3. Do NOT attempt to modify permissions

### Binary Log Files
For binary logs (e.g., Windows Event Logs):
1. Attempt to use system-specific readers (journalctl, Get-EventLog)
2. If unavailable, report binary format limitation
3. Suggest exporting to text format externally
```

### Security Validation

**Tool Restriction Enforcement**:
- ✅ `allowed-tools` limits capability to Read, Grep, Glob, Bash
- ✅ Instructions explicitly prohibit write operations
- ✅ No Write, Edit, or file modification tools available

---

## Example 4: Complex Multi-File Skill with Dependencies

### User Request

```
Create a skill for Excel spreadsheet processing - reading, analyzing data,
creating charts, and generating reports. Should handle .xlsx and .xls files.
```

### Skill-Maker Analysis

**Information Completeness**: ✅ Sufficient
**Complexity**: High (requires external dependencies, multiple file types)

**Action**: Generate comprehensive skill with full file structure

### Generated Skill: excel-analyzer

**Directory Structure**:
```
excel-analyzer/
├── SKILL.md
├── reference.md
├── examples.md
└── scripts/
    └── analyze_excel.py
```

**SKILL.md**:
```yaml
---
name: excel-analyzer
description: Read, analyze, and generate reports from Excel spreadsheets (.xlsx, .xls). Create charts, compute statistics, and export data. Use when working with Excel files, spreadsheets, tabular data in .xlsx/.xls format, or when user mentions Excel analysis, pivot tables, or spreadsheet reporting.
---

# Excel Analyzer

## Instructions

### Phase 1: Dependency Verification
1. Check for required Python packages:
   ```bash
   python -c "import pandas, openpyxl, xlrd" 2>/dev/null && echo "OK" || echo "MISSING"
   ```

2. If dependencies missing, provide installation instructions:
   ```bash
   pip install pandas openpyxl xlrd xlsxwriter
   ```

3. If user confirms installation or dependencies present, proceed

### Phase 2: File Reading
1. Use Read tool to verify file existence
2. Determine file format (.xlsx or .xls) from extension
3. Load spreadsheet using Python script:
   ```bash
   python scripts/analyze_excel.py --input "file.xlsx" --action load
   ```

4. Display sheet names and basic metadata:
   - Number of sheets
   - Sheet dimensions (rows × columns)
   - Column headers

### Phase 3: Data Analysis
1. Perform requested analysis operations:

   **Descriptive Statistics**:
   ```bash
   python scripts/analyze_excel.py --input "file.xlsx" --action stats
   ```
   Output: mean, median, std dev, min, max for numeric columns

   **Data Filtering**:
   ```bash
   python scripts/analyze_excel.py --input "file.xlsx" --action filter --criteria "column>100"
   ```

   **Pivot Table Generation**:
   ```bash
   python scripts/analyze_excel.py --input "file.xlsx" --action pivot --rows "Category" --values "Sales" --aggfunc "sum"
   ```

   **Chart Creation**:
   ```bash
   python scripts/analyze_excel.py --input "file.xlsx" --action chart --type bar --x "Category" --y "Sales"
   ```

2. Save analysis results using Write tool

### Phase 4: Report Generation
1. Compile analysis results into structured report
2. Generate markdown or Excel output as requested
3. Include:
   - Executive summary
   - Key statistics
   - Visualizations (as file references)
   - Data quality notes

## Requirements

### Python Packages

```bash
pip install pandas>=2.0.0 openpyxl>=3.1.0 xlrd>=2.0.0 xlsxwriter>=3.1.0 matplotlib>=3.7.0
```

Or add to requirements.txt:
```
pandas>=2.0.0
openpyxl>=3.1.0
xlrd>=2.0.0
xlsxwriter>=3.1.0
matplotlib>=3.7.0
```

### System Requirements
- Python 3.8 or higher
- Sufficient memory for large spreadsheets (>1GB for files >100MB)

## Common Workflows

### Workflow 1: Quick Statistics
For rapid statistical overview of spreadsheet data.

### Workflow 2: Data Extraction
Extract specific columns or filtered rows to CSV/JSON.

### Workflow 3: Chart Generation
Create visualizations from spreadsheet data.

### Workflow 4: Comparison Analysis
Compare data across multiple sheets or workbooks.

## Advanced Usage

See [reference.md](reference.md) for:
- Complex pivot table configurations
- Custom aggregation functions
- Multi-file batch processing
- Performance optimization for large files

## Examples

See [examples.md](examples.md) for comprehensive usage scenarios.
```

**scripts/analyze_excel.py** (Referenced Helper Script):
```python
#!/usr/bin/env python3
"""
Excel Analysis Helper Script
Used by excel-analyzer skill for spreadsheet operations
"""

import argparse
import pandas as pd
import sys
from pathlib import Path

def load_excel(filepath):
    """Load Excel file and return metadata"""
    try:
        xls = pd.ExcelFile(filepath)
        sheets = xls.sheet_names
        print(f"Sheets: {', '.join(sheets)}")
        for sheet in sheets:
            df = pd.read_excel(filepath, sheet_name=sheet)
            print(f"{sheet}: {df.shape[0]} rows × {df.shape[1]} columns")
            print(f"Columns: {', '.join(df.columns)}")
        return 0
    except Exception as e:
        print(f"Error loading file: {e}", file=sys.stderr)
        return 1

def compute_stats(filepath, sheet=0):
    """Compute descriptive statistics"""
    try:
        df = pd.read_excel(filepath, sheet_name=sheet)
        print(df.describe())
        return 0
    except Exception as e:
        print(f"Error computing statistics: {e}", file=sys.stderr)
        return 1

def main():
    parser = argparse.ArgumentParser(description='Excel Analysis Tool')
    parser.add_argument('--input', required=True, help='Input Excel file')
    parser.add_argument('--action', required=True,
                       choices=['load', 'stats', 'filter', 'pivot', 'chart'])
    parser.add_argument('--sheet', default=0, help='Sheet name or index')
    parser.add_argument('--criteria', help='Filter criteria')
    parser.add_argument('--rows', help='Pivot table row field')
    parser.add_argument('--values', help='Pivot table value field')
    parser.add_argument('--aggfunc', default='sum', help='Aggregation function')
    parser.add_argument('--type', choices=['bar', 'line', 'scatter', 'pie'],
                       help='Chart type')
    parser.add_argument('--x', help='X-axis column')
    parser.add_argument('--y', help='Y-axis column')

    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        return 1

    if args.action == 'load':
        return load_excel(args.input)
    elif args.action == 'stats':
        return compute_stats(args.input, args.sheet)
    # Additional action handlers would be implemented here

    return 0

if __name__ == '__main__':
    sys.exit(main())
```

**reference.md**: Advanced Excel processing techniques, performance optimization strategies

**examples.md**: Step-by-step walkthroughs for common Excel analysis scenarios

---

## Example 5: Web-Enabled Skill

### User Request

```
Create a skill to fetch and analyze API documentation from URLs. Should retrieve
OpenAPI/Swagger specs and generate human-readable summaries.
```

### Skill-Maker Analysis

**Information Completeness**: ✅ Sufficient
**Tools Required**: WebFetch, Read, Write
**External Dependencies**: YAML/JSON parsing

### Generated Skill: api-doc-fetcher

```yaml
---
name: api-doc-fetcher
description: Fetch and analyze API documentation from URLs. Parse OpenAPI/Swagger specifications and generate summaries. Use when user provides API documentation URLs, mentions OpenAPI, Swagger, or requests API spec analysis.
allowed-tools: WebFetch, Read, Write, Bash
---

# API Documentation Fetcher

## Instructions

### Phase 1: URL Retrieval
1. Use WebFetch tool to retrieve API specification from provided URL
2. Common spec locations:
   - `/swagger.json`
   - `/openapi.json`
   - `/api-docs`
   - `/swagger/v1/swagger.json`

3. If URL returns HTML instead of JSON/YAML, search page for spec links

### Phase 2: Format Detection
1. Detect specification format:
   - OpenAPI 3.x (check for `openapi: "3.x.x"`)
   - Swagger 2.0 (check for `swagger: "2.0"`)
   - Other formats (RAML, API Blueprint)

2. Parse JSON or YAML content:
   ```bash
   python -c "import json; spec = json.load(open('spec.json')); print(spec['info']['title'])"
   ```

### Phase 3: Analysis and Summary Generation
1. Extract key information:
   - API title and version
   - Base URL
   - Authentication methods
   - Available endpoints (paths)
   - Request/response schemas

2. Generate structured summary:
   ```markdown
   # API Documentation Summary

   **API Name**: [from spec.info.title]
   **Version**: [from spec.info.version]
   **Base URL**: [from spec.servers or spec.host]

   ## Authentication
   [List authentication schemes]

   ## Endpoints

   ### GET /users
   **Description**: [from operation summary]
   **Parameters**:
   - `limit` (query, integer): Maximum results
   - `offset` (query, integer): Pagination offset

   **Responses**:
   - 200: Success
   - 404: Not found

   [Repeat for each endpoint]

   ## Data Models
   [List schemas/definitions]
   ```

3. Use Write tool to save summary as markdown file

### Phase 4: Optional Deep Analysis
If requested, provide:
- Endpoint grouping by tags
- Required vs. optional parameters
- Response schema examples
- Rate limiting information
- Deprecation warnings

## Requirements

Python 3.6+ with standard library (json, yaml modules).

For YAML parsing:
```bash
pip install pyyaml
```

## Common Workflows

### Workflow 1: Quick API Overview
Fetch spec, generate concise summary of available endpoints.

### Workflow 2: Endpoint Detail Analysis
Deep dive into specific endpoint parameters and responses.

### Workflow 3: API Comparison
Fetch multiple API specs and compare capabilities.

## Error Handling

### URL Not Found (404)
Report error and suggest common spec path alternatives.

### Invalid Format
If content is not valid OpenAPI/Swagger, report format issues.

### Network Errors
Handle timeouts and connection failures gracefully.
```

---

## Example 6: Minimal Viable Skill (Quick Generation)

### User Request

```
Quick skill to count lines of code in a directory.
```

### Skill-Maker Analysis

**Complexity**: Low (straightforward utility)
**Action**: Generate minimal skill structure

### Generated Skill: loc-counter

```yaml
---
name: loc-counter
description: Count lines of code in project directories. Use when user asks to count code lines, measure project size, or mentions LOC, SLOC, or code metrics.
---

# Lines of Code Counter

## Instructions

1. Use Bash to count lines by file type:
   ```bash
   find . -name "*.py" -exec wc -l {} + | tail -1
   find . -name "*.js" -exec wc -l {} + | tail -1
   find . -name "*.java" -exec wc -l {} + | tail -1
   ```

2. Aggregate totals and report:
   - Total lines per language
   - File count per language
   - Overall project size

3. Optionally exclude common directories:
   ```bash
   find . -name "*.py" -not -path "*/node_modules/*" -not -path "*/.venv/*" -exec wc -l {} +
   ```
```

**Rationale for Minimal Structure**:
- Single, straightforward function
- No external dependencies
- No complex multi-phase workflow
- Sufficient for user's stated need

---

## Summary: Skill Generation Patterns

| Request Type | Information Gathering | Skill Complexity | File Structure |
|--------------|---------------------|------------------|----------------|
| Simple utility | Minimal questions | Single SKILL.md | Minimal |
| Format processor | Clarify operations | SKILL.md + optional reference | Moderate |
| Security-sensitive | Confirm restrictions | SKILL.md with tool limits | Moderate |
| Complex analysis | Detailed requirements | Full multi-file structure | Comprehensive |
| Web-enabled | Verify endpoints | SKILL.md + examples | Moderate |

### Key Takeaways

1. **Adjust detail level** to match skill complexity
2. **Ask questions** when scope unclear
3. **Apply tool restrictions** for security requirements
4. **Include dependencies** documentation for external requirements
5. **Provide examples** for complex workflows
6. **Validate activation** triggers through test queries
