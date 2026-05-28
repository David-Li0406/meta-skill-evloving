# How to Use the Code Fix Assistant Skill

Hey Claude—I just added the "code-fix-assistant" skill. Can you help me fix code quality issues in my files?

## Example Invocations

### Example 1: Basic Fix
```
Hey Claude—I just added the "code-fix-assistant" skill. Can you fix the formatting and syntax issues in src/main.py?
```

### Example 2: Complete Fix Pipeline
```
Hey Claude—I just added the "code-fix-assistant" skill. Can you run the complete fix pipeline on src/app.ts:
1. Format the code
2. Fix TypeScript type errors
3. Detect and fix bugs
4. Validate the results
```

### Example 3: Batch Processing
```
Hey Claude—I just added the "code-fix-assistant" skill. Can you fix all Python files in the src/ directory? Focus on formatting and syntax errors.
```

### Example 4: Check Only (No Auto-Apply)
```
Hey Claude—I just added the "code-fix-assistant" skill. Can you analyze main.go for issues and generate a report, but don't auto-apply fixes?
```

### Example 5: Language-Specific Fix
```
Hey Claude—I just added the "code-fix-assistant" skill. Can you:
1. Format this Rust code with rustfmt
2. Run Clippy to detect issues
3. Show me a report of what needs fixing
```

### Example 6: Custom Configuration
```
Hey Claude—I just added the "code-fix-assistant" skill. Can you format this JavaScript file using Prettier with these settings:
- No semicolons
- Single quotes
- 4-space indentation
```

## What to Provide

**Required**:
- File path or code snippet
- Programming language (Python, JavaScript, TypeScript, Java, Go, Rust)

**Optional**:
- Specific fix types to run (format, syntax, bugs, validate)
- Whether to auto-apply fixes or just report
- Severity threshold (error, warning, info)
- Custom configuration (line length, linter rules, etc.)

## What You'll Get

**Fix Report** including:
- Summary of changes applied
- List of issues found and fixed
- Issues that couldn't be auto-fixed (with suggestions)
- Before/after diff
- Validation results (linter status, syntax check)

**Fixed Code** (if auto-apply enabled):
- Updated file with all fixes applied
- Backup of original file (.backup extension)

## Supported Languages

| Language   | Formatter         | Linter          | Type Checker | Bug Detector      |
|------------|-------------------|-----------------|--------------|-------------------|
| Python     | Black, isort      | flake8          | mypy         | Pattern analysis  |
| JavaScript | Prettier          | ESLint          | N/A          | ESLint rules      |
| TypeScript | Prettier          | ESLint          | tsc          | ESLint rules      |
| Java       | google-java-format| Checkstyle      | javac        | Pattern analysis  |
| Go         | gofmt, goimports  | golangci-lint   | N/A          | go vet            |
| Rust       | rustfmt           | Clippy          | rustc        | Clippy            |

## Common Workflows

### 1. Pre-Commit Quality Check
```
Hey Claude, use the code-fix-assistant to check all modified files before I commit. Report issues but don't auto-fix.
```

### 2. Legacy Code Cleanup
```
Hey Claude, I have a legacy Python codebase. Use code-fix-assistant to:
1. Format all .py files with Black
2. Fix obvious syntax issues
3. Generate a report of remaining issues
```

### 3. TypeScript Migration
```
Hey Claude, I'm migrating JavaScript to TypeScript. Use code-fix-assistant to:
1. Check type errors in all .ts files
2. Suggest fixes for type issues
3. Validate with tsc
```

### 4. Quick Fix Single File
```
Hey Claude, quickly fix this file with code-fix-assistant and auto-apply changes: src/utils.js
```

## Tips & Best Practices

1. **Start with Check-Only**: First run without auto-apply to see what will change
2. **Use Version Control**: Always commit code before auto-applying fixes
3. **Review Critical Code**: Manually review fixes to important/production code
4. **Install Tools**: Ensure language-specific tools are installed (see installation guide)
5. **Incremental Fixes**: For large codebases, fix one directory or file type at a time
6. **Custom Configs**: Use project-level config files (.prettierrc, .flake8) for consistency

## Troubleshooting

**"Tool not installed" error**:
- Install the required tool for your language (see README.md)
- Check if the tool is in your PATH

**"Permission denied" error**:
- Check file permissions
- Ensure you have write access to the file

**"Timeout" error**:
- File might be too large (>10,000 lines)
- Try fixing in smaller chunks

**Fixes not applied**:
- Make sure `auto_apply: true` is set
- Check if there were validation errors
- Review the fix report for details
