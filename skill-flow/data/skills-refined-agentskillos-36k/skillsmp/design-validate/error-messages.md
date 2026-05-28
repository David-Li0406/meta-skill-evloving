# Design Doc Validation Error Messages

Complete reference for all validation error messages with fix instructions.

## Missing Frontmatter

```text
ERROR: Missing or invalid frontmatter
- Expected: YAML frontmatter starting with '---' on line 1
- Found: {what was found}
- Fix: Add valid YAML frontmatter to the top of the file
```

## Invalid Field Value

```text
ERROR: Invalid value for field '{field}'
- Expected: {expected value/type}
- Found: {actual value}
- Fix: Update frontmatter to use valid value
```

## Module Not Found

```text
ERROR: Module '{module}' not found in config
- Field: module
- Value: {module}
- Available: {list of modules}
- Fix: Update module field to match config or add module to config
```

## Date Format Error

```text
ERROR: Invalid date format for '{field}'
- Expected: YYYY-MM-DD
- Found: {actual value}
- Fix: Use ISO date format (e.g., 2026-01-17)
```

## Date Order Error

```text
ERROR: Date '{field1}' must be >= '{field2}'
- {field1}: {date1}
- {field2}: {date2}
- Fix: Update dates to correct chronological order
```

## Category Not Allowed

```text
ERROR: Category '{category}' not allowed for module '{module}'
- Allowed categories: {list}
- Fix: Use one of the allowed categories or add to module config
```

## Missing Section

```text
ERROR: Missing required section: {section}
- Expected: ## {section}
- Fix: Add section to document following template structure
```

## Broken Reference

```text
ERROR: Referenced file does not exist
- Field: {related|dependencies}
- Path: {path}
- Fix: Create the referenced file or remove the reference
```

## Status-Completeness Mismatch

```text
WARNING: Status '{status}' doesn't match completeness {completeness}
- Completeness: {completeness}
- Expected status: {expected}
- Current status: {actual}
- Fix: Update status to match completeness level
```

## Markdown Linting Error

```text
ERROR: Markdown linting failed
- Rule: {rule-id}
- Line: {line-number}
- Message: {message}
- Fix: Run 'pnpm lint:md:fix' or fix manually
```
