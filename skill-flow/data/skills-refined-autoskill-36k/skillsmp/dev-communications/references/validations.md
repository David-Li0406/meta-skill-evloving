# Dev Communications - Validations

## Vague Commit Message

### **Id**
devcomm-vague-commit
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ^(fix|update|change|modify)\s*$
  - ^(wip|temp|test)\s*$
  - ^(stuff|things|misc)\s*$
### **Message**
Vague commit message. Describe what and why.
### **Fix Action**
Use format: 'fix: resolve auth timeout by increasing session TTL'
### **Applies To**
  - .git/COMMIT_EDITMSG

## Missing PR Description

### **Id**
devcomm-no-pr-description
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^\s*$
  - ^\s*-\s*$
### **Message**
Empty PR description. Explain changes, impact, and testing.
### **Fix Action**
Add: ## What - ## Why - ## Testing - ## Screenshots (if UI)
### **Applies To**
  - .github/pull_request_template.md
  - PULL_REQUEST_TEMPLATE.md

## Missing Changelog Entry

### **Id**
devcomm-no-changelog
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - version.*\d+\.\d+\.\d+(?!.*##\s*Changed|.*##\s*Added|.*##\s*Fixed)
### **Message**
Version bump without changelog entry. Document changes.
### **Fix Action**
Add to CHANGELOG.md: ## [version] - YYYY-MM-DD with entries
### **Applies To**
  - package.json
  - CHANGELOG.md

## Complex Logic Without Comment

### **Id**
devcomm-uncommented-complex
### **Severity**
info
### **Type**
regex
### **Pattern**
  - (for|while)\s*\([^)]*\)\s*\{[^}]*\{[^}]*\{(?!.*//)
  - \?[^:]*:[^;]*\?[^:]*:(?!.*//)
### **Message**
Complex nested logic without explanation comment.
### **Fix Action**
Add comment explaining the logic: // Why this approach...
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Missing README

### **Id**
devcomm-no-readme
### **Severity**
error
### **Type**
file_exists
### **File**
README.md
### **Message**
No README.md found. Add project documentation.
### **Fix Action**
Create README.md with: purpose, setup, usage, contributing
### **Applies To**
  - .

## Complex Type Without JSDoc

### **Id**
devcomm-no-type-docs
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - type\s+\w+\s*=\s*\{[^}]{100,}\}(?!.*\/\*\*)
  - interface\s+\w+\s*\{[^}]{100,}\}(?!.*\/\*\*)
### **Message**
Complex type definition without JSDoc documentation.
### **Fix Action**
Add JSDoc: /** Description @property field - what it does */
### **Applies To**
  - **/*.ts
  - **/*.tsx

## Magic Number Without Context

### **Id**
devcomm-magic-number-uncommented
### **Severity**
info
### **Type**
regex
### **Pattern**
  - [^\d\.](86400|3600|60000|1000|100|50)(?!\d)(?!.*//)
### **Message**
Magic number without explanation. Add comment or constant.
### **Fix Action**
Add: const SECONDS_PER_DAY = 86400; // 24 * 60 * 60
### **Applies To**
  - **/*.ts
  - **/*.js

## Breaking Change Without Notice

### **Id**
devcomm-breaking-change-no-notice
### **Severity**
error
### **Type**
regex
### **Pattern**
  - BREAKING CHANGE
  - breaking:
### **Message**
Breaking change detected. Ensure it's documented in PR and changelog.
### **Fix Action**
Add to PR: ## BREAKING CHANGE section with migration guide
### **Applies To**
  - .git/COMMIT_EDITMSG

## Exported Function Without JSDoc

### **Id**
devcomm-function-no-jsdoc
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - export\s+(async\s+)?function\s+\w+\s*\([^)]*\)(?!.*\/\*\*)
  - export\s+const\s+\w+\s*=\s*(async\s*)?\([^)]*\)\s*=>(?!.*\/\*\*)
### **Message**
Exported function without JSDoc. Document parameters and return value.
### **Fix Action**
Add: /** @param x - description @returns description */
### **Applies To**
  - **/*.ts
  - **/*.js

## API Endpoint Without Documentation

### **Id**
devcomm-api-endpoint-no-docs
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - app\.(get|post|put|delete|patch)\(['"][^'"]+['"](?!.*\/\*\*)
  - router\.(get|post|put|delete|patch)\(['"][^'"]+['"](?!.*\/\*\*)
### **Message**
API endpoint without documentation. Document request/response.
### **Fix Action**
Add JSDoc: /** @route POST /api/users @body { name, email } */
### **Applies To**
  - **/*.ts
  - **/*.js

## Environment Variable Without Docs

### **Id**
devcomm-env-var-no-docs
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - process\.env\.[A-Z_]+(?!.*README|.*\.env\.example)
### **Message**
Environment variable used but not documented in README or .env.example.
### **Fix Action**
Add to .env.example: VAR_NAME=example_value # description
### **Applies To**
  - **/*.ts
  - **/*.js

## Error Without Context

### **Id**
devcomm-error-no-context
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - throw\s+new\s+Error\(['"]\w+['"]\)
  - throw\s+['"]\w+['"]
### **Message**
Generic error message. Add context about what failed and why.
### **Fix Action**
Improve: throw new Error(`Failed to fetch user ${id}: ${reason}`)
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx