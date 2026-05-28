---
name: review-code
description: Comprehensive code review tool for Clean Code principles and project architecture. Supports single-file review (/review-code) and project-wide analysis (/review-code <directory>). Checks variable naming, function length, redundant comments, and generates actionable reports. Supports JavaScript, Python, and Java.
---

# Code Reviewer

Comprehensive code review tool for Clean Code principles - supports both single-file and project-wide analysis.

## Quick Start

### Single File Review
```
/review-code
```
Analyzes the current file or provided code snippet.

### Project-Wide Review
```
/review-code <directory_path>
```
Recursively scans all code files in the directory and generates an integrated report.

## Usage Modes

### Mode 1: Single File Review

When triggered without arguments, review the current file or code snippet:

1. **Identify the language** - Determine programming language
2. **Check variable naming** - Flag unclear or misleading names
3. **Assess function length** - Identify overly long functions
4. **Evaluate comments** - Find redundant comments
5. **Research solutions** - For complex logic issues or performance optimization needs, automatically use `google_search` tool to find latest solutions and integrate search results into suggested fixes
6. **Generate report** - List issues with line numbers and actionable recommendations

### Mode 2: Project Review

When provided with a directory path:

1. **Scan directory** - Recursively find all code files
2. **Apply checks** - Run Clean Code checks on each file
3. **Research solutions** - For complex logic issues or performance optimization needs, automatically use `google_search` tool to find latest solutions and best practices
4. **Aggregate results** - Generate integrated report sorted by file path with research-backed recommendations
5. **Prioritize** - Rank files by issue count and severity

**Supported file extensions:**
- Python: `.py`
- JavaScript/TypeScript: `.js`, `.ts`, `.jsx`, `.tsx`
- Java: `.java`

**Excluded directories:**
- `__pycache__`, `.git`, `.venv`, `venv`, `node_modules`, `.pytest_cache`, `dist`, `build`

## Clean Code Checks

### Variable Naming Review

Check for:
- Single letter names (except loop counters i, j, k)
- Unclear abbreviations (e.g., `d`, `tmp`, `val`)
- Non-descriptive names (e.g., `data`, `info`, `obj`)
- Names that don't reveal intent (e.g., `flag`, `check`)
- Misleading names that don't match actual purpose

**Good examples:**
- `userAge` not `a`
- `isAuthenticated` not `flag`
- `customerOrders` not `list`

### Function Length Review

Language-specific line count guidelines (excluding blank lines and braces):

- **JavaScript/TypeScript**: 20 lines
- **Python**: 20 lines
- **Java**: 25 lines

Flag functions exceeding these limits. Functions doing multiple things should be split into smaller, focused functions.

### Redundant Comments Review

Identify comments that:
- Repeat what the code clearly states
- Explain obvious operations
- Are outdated or misleading
- Could be replaced by better naming

**Redundant examples:**
```javascript
// Increment counter
counter++;

// Loop through users
for (const user of users) {
```

**Valuable comments explain WHY, not WHAT:**
```javascript
// Using exponential backoff to avoid API rate limits
await retry(apiCall, { maxAttempts: 3 });
```

## Research & Solution Discovery

When encountering complex issues during code review, use the `google_search` tool to find modern solutions and best practices.

### When to Use google_search

Automatically search for solutions when you identify:

1. **Performance Issues**
   - Inefficient algorithms (O(n²) or worse)
   - Memory leaks or excessive memory usage
   - Slow database queries or API calls

2. **Complex Logic Problems**
   - Overly complex conditional logic
   - Nested loops that could be optimized
   - Code that's hard to understand or maintain

3. **Modern Best Practices**
   - Outdated patterns or deprecated APIs
   - Security vulnerabilities
   - Framework-specific optimizations

4. **Language-Specific Optimizations**
   - Python: List comprehensions, generators, async/await
   - JavaScript: Promise patterns, async patterns, ES6+ features
   - Java: Stream API, Optional, modern concurrency

### Search Query Guidelines

Format search queries to get the most relevant results:

**Good query examples:**
- "Python optimize nested loops performance 2024"
- "JavaScript async await best practices"
- "Java Stream API vs traditional loop performance"
- "React useEffect cleanup pattern"

**Include:**
- Programming language name
- Specific problem or pattern
- Year (for latest solutions)
- Keywords: "best practices", "performance", "optimize"

### Integrating Search Results

After searching:
1. Summarize the most relevant solution
2. Provide code example from search results
3. Explain why this solution is better
4. Include source URL for reference

**Example in report:**
```
Performance Issue (Line 45-60):
- Current: Nested loops with O(n²) complexity
- Recommended: Use hash map for O(n) lookup
- Source: [Modern Python Performance Patterns](https://example.com)
```

## Language-Specific Rules

For detailed language-specific conventions:

- **JavaScript/TypeScript**: See [javascript.md](references/language-specific/javascript.md)
- **Python**: See [python.md](references/language-specific/python.md)
- **Java**: See [java.md](references/language-specific/java.md)

Load these files only when reviewing code in that specific language.

## Report Formats

### Single File Report

```
Clean Code Review Results:

Variable Naming Issues:
- Line 12: 'd' -> Use descriptive name like 'deliveryDate'
- Line 25: 'tmp' -> Rename to indicate purpose like 'sortedUsers'

Function Length Issues:
- calculateTotal() (lines 45-78): 34 lines -> Split into smaller functions

Redundant Comments:
- Line 10: "// Set name" -> Remove, code is self-explanatory
- Line 52: "// Return result" -> Remove obvious comment

Summary: 5 issues found (2 naming, 1 length, 2 comments)
```

### Project Review Report

```
=== Project Code Review Report ===

Executive Summary:
- Files Scanned: 15
- Total Issues: 47
- Top 3 Files Needing Refactoring:
  1. src/utils/helper.py (12 issues)
  2. src/main.py (9 issues)
  3. tests/test_api.py (8 issues)

=== Detailed Results ===

File: src/main.py (9 issues)
├─ Variable Naming (4):
│  ├─ Line 12: 'd' -> Use descriptive name
│  ├─ Line 25: 'tmp' -> Rename to indicate purpose
│  ├─ Line 40: 'x' -> Use meaningful name
│  └─ Line 55: 'flag' -> Use descriptive boolean name
├─ Function Length (2):
│  ├─ process_data() (lines 30-55): 26 lines
│  └─ handle_request() (lines 60-85): 26 lines
└─ Redundant Comments (3):
   ├─ Line 10: "// Set name" - Remove
   ├─ Line 35: "// Loop through items" - Remove
   └─ Line 70: "// Return result" - Remove

File: src/utils/helper.py (12 issues)
[... similar format ...]

=== Recommendations ===

Priority 1 - Critical (>10 issues):
- src/utils/helper.py: Heavy refactoring needed

Priority 2 - High (6-10 issues):
- src/main.py: Focus on variable naming and function splitting
- tests/test_api.py: Improve test function names

Priority 3 - Medium (3-5 issues):
- src/api/routes.py: Minor improvements needed

Priority 4 - Low (1-2 issues):
- src/config.py: Minimal changes required

Common Patterns:
- Frequent use of single-letter variables across 8 files
- Long functions (>20 lines) found in 5 files
- Redundant comments in 10 files
```

## Error Handling

Handle common errors gracefully:

- **Directory not found**: Display clear error message with the attempted path
- **No code files found**: Report that the directory contains no supported files
- **File read errors**: Skip the file and note it in the report
- **Permission errors**: Note files that couldn't be accessed

## Performance Considerations

For large projects (>100 files):
- Process files in batches
- Provide progress updates
- Consider offering to focus on specific subdirectories
- Limit detailed output for files with minimal issues

## Best Practices

- Keep reports focused and actionable
- Only list actual violations found
- Provide specific line numbers for all issues
- Suggest concrete improvements, not just problems
- Prioritize issues by severity and impact
