# How to Use This Skill

Hey Claude—I just added the "api-document-generator" skill. Can you generate API documentation from my code files?

## Example Invocations

**Example 1: Generate documentation from a directory**
Hey Claude—I just added the "api-document-generator" skill. Can you generate OpenAPI documentation from the `src/api/` directory?

**Example 2: Generate documentation from a specific file**
Hey Claude—I just added the "api-document-generator" skill. Can you parse this Python file and create API documentation?

**Example 3: Generate documentation with custom options**
Hey Claude—I just added the "api-document-generator" skill. Can you generate documentation from `backend/routes/` and include example requests?

**Example 4: Check recent documentation**
Hey Claude—I just added the "api-document-generator" skill. Can you show me the most recent API documentation files generated?

## What to Provide

- **File or directory path**: Path to the file or directory containing API/interface definitions
- **Optional parameters** (as JSON or natural language):
  - `output_format`: "markdown" or "json" (default: "markdown")
  - `include_examples`: true/false (default: true)
  - `validate_openapi`: true/false (default: true)
  - `cleanup_old_files`: true/false (default: true)
  - `max_files_to_keep`: number (default: 10)
  - `metadata`: Custom title, description, version

## What You'll Get

- **Generated documentation**: OpenAPI-compliant markdown file with timestamp
- **Output location**: Files saved to `.claude/api_doc/` directory
- **Comprehensive content**:
  - API endpoints with methods, parameters, and descriptions
  - Request/response schemas
  - Authentication information
  - Example requests and responses
  - Error codes and handling
  - Table of contents and navigation
- **Statistics**: Processing summary with endpoints count, file types, etc.
- **Validation warnings**: Any issues found during parsing or generation

## Supported File Types

The skill can parse:
- **Python** (.py): FastAPI, Flask, Django patterns
- **JavaScript/TypeScript** (.js, .ts): Express.js, REST API patterns
- **JSON** (.json): OpenAPI specifications, API definitions
- **YAML** (.yaml, .yml): OpenAPI specifications, configuration files

## Output File Format

Generated documentation files follow this naming pattern:
```
api_documentation_YYYY-MM-DD_HH-MM-SS.md
```

Example: `api_documentation_2025-12-15_14-30-45.md`

## Installation and Setup

1. **Install the skill**: Place the `api-document-generator` folder in your `.claude/skills/` directory
2. **Test with sample**: Use the sample input to verify the skill works
3. **Configure output**: The skill automatically creates `.claude/api_doc/` directory

## Tips for Best Results

1. **Organize your code**: Keep API-related files in structured directories
2. **Use clear naming**: Descriptive endpoint names and parameter names help parsing
3. **Include comments**: Code comments are used to enhance documentation
4. **Follow conventions**: Use standard framework patterns (FastAPI decorators, Express routes, etc.)
5. **Validate output**: Always review generated documentation for accuracy

## Common Use Cases

- **API documentation generation**: Automatically create docs from existing code
- **Codebase analysis**: Understand API structure by parsing endpoints
- **Documentation updates**: Keep API docs in sync with code changes
- **Team collaboration**: Share standardized API documentation
- **API testing**: Use generated docs to create test cases

## Troubleshooting

**Issue**: No endpoints found in files
**Solution**: Ensure files use supported framework patterns and check file extensions

**Issue**: Generated documentation is incomplete
**Solution**: Add more descriptive comments and follow standard API patterns

**Issue**: Output directory not created
**Solution**: Check write permissions in current directory

**Issue**: Parsing errors for specific file types
**Solution**: Verify file format and encoding (UTF-8 recommended)