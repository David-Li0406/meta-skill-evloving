---
name: format-validation
description: Validate JSON file formats by scanning directories and checking for correct JSON syntax
---

## Overview
This Skill validates JSON files in specified directories to ensure they have correct syntax and valid format. When you need to verify JSON files are well-formed and can be parsed correctly, use this Skill. It scans the specified path, finds all JSON files, and validates their format.

## When to Use
Use this Skill when:
- Verifying JSON configuration files are valid
- Checking data files before processing
- Validating JSON schema compliance
- Troubleshooting JSON parsing errors
- Auditing codebase for malformed JSON files

## Validation Process
The validation process includes:
1. Scanning the specified directory recursively
2. Identifying all files with .json extension
3. Parsing each JSON file to check syntax validity
4. Reporting validation results with file paths and error details
5. Providing summary statistics (total files, valid, invalid)

## Usage
Invoke this Skill by specifying the path to validate:
```
Validate JSON files in /path/to/directory
```

The Skill will:
- Scan the directory tree
- Validate each JSON file found
- Return detailed validation results

## Dependencies
Python 3.8+ or Go 1.16+

## Resources
- scripts/validate_json.py: Python implementation of JSON validation
- scripts/validate_json.go: Go implementation of JSON validation
