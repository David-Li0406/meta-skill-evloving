# Practical Examples

Real-world examples for automation, CI/CD, and scripting with Claude Code headless mode.

## Simple One-Shot Tasks

### Quick Code Explanation

```bash
claude -p "Explain what src/auth.ts does in 2 sentences"
```

### Find TODOs in Codebase

```bash
claude -p "Find all TODO comments and list them with file locations" \
  --allowedTools "Grep,Glob,Read"
```

### Generate Git Commit Message

```bash
claude -p "Generate a commit message for staged changes" \
  --allowedTools "Bash(git diff:--cached),Bash(git status:*)"
```

## Code Review Automation

### PR Review Script

```bash
#!/bin/bash
# review-pr.sh

PR_NUMBER=$1

gh pr diff "$PR_NUMBER" | claude -p \
  "Review this PR for:
   1. Potential bugs
   2. Security issues
   3. Performance concerns
   4. Code style violations

   Format as JSON with 'issues' array and 'approved' boolean." \
  --output-format json \
  --json-schema '{"type":"object","properties":{"approved":{"type":"boolean"},"issues":{"type":"array","items":{"type":"object","properties":{"severity":{"type":"string"},"description":{"type":"string"},"line":{"type":"number"}}}},"required":["approved","issues"]}}' \
  | jq '.'
```

### Security Audit

```bash
claude -p "Audit this codebase for security vulnerabilities. Focus on:
- SQL injection
- XSS
- Authentication issues
- Secrets in code" \
  --allowedTools "Read,Glob,Grep" \
  --append-system-prompt "You are a security auditor. Be thorough." \
  --output-format json
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Review PR
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          gh pr diff ${{ github.event.pull_request.number }} | \
          claude -p "Review this diff for issues" \
            --output-format json \
            --max-turns 1 \
            --allowedTools "Read" \
            > review.json

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const review = require('./review.json');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review.result
            });
```

### GitLab CI Pipeline

```yaml
# .gitlab-ci.yml
claude-review:
  image: node:20
  stage: review
  before_script:
    - npm install -g @anthropic-ai/claude-code
  script:
    - |
      git diff origin/main...HEAD | claude -p \
        "Review these changes for issues" \
        --output-format json \
        --max-turns 1 \
        --allowedTools "Read" \
        > review.json
    - cat review.json | jq -r '.result'
  artifacts:
    paths:
      - review.json
```

## Test Automation

### Run and Fix Tests

```bash
claude -p "Run the test suite. If tests fail, analyze the failures and fix them." \
  --allowedTools "Bash(bun test:*),Bash(npm test:*),Read,Edit" \
  --max-turns 10 \
  --output-format json
```

### Generate Missing Tests

```bash
claude -p "Find functions in src/ without corresponding tests and generate test files" \
  --allowedTools "Read,Write,Glob,Grep" \
  --append-system-prompt "Use Bun test framework. Follow existing test patterns."
```

### Coverage Report Analysis

```bash
# Generate coverage first
bun test --coverage > coverage.txt

# Analyze with Claude
cat coverage.txt | claude -p \
  "Analyze this coverage report. Identify files with low coverage and suggest which functions need tests." \
  --output-format json
```

## Documentation Generation

### API Documentation

```bash
claude -p "Generate OpenAPI documentation for all API routes in src/api/" \
  --allowedTools "Read,Glob,Write" \
  --append-system-prompt "Follow OpenAPI 3.0 specification"
```

### README Generation

```bash
claude -p "Analyze this project and generate a comprehensive README.md with:
- Project description
- Installation instructions
- Usage examples
- API reference
- Contributing guidelines" \
  --allowedTools "Read,Glob,Grep,Write"
```

### JSDoc Comments

```bash
# Add JSDoc to a single file
claude -p "Add JSDoc comments to all exported functions in src/utils.ts" \
  --allowedTools "Read,Edit"

# Batch process multiple files
for file in src/*.ts; do
  claude -p "Add JSDoc comments to exported functions in $file" \
    --allowedTools "Read,Edit" \
    --max-turns 3
done
```

## Refactoring Tasks

### Code Migration

```bash
claude -p "Migrate all React class components in src/components/ to functional components with hooks" \
  --allowedTools "Read,Edit,Glob" \
  --max-turns 20 \
  --append-system-prompt "Preserve all functionality. Add TypeScript types."
```

### Dependency Update

```bash
claude -p "Update all deprecated API calls after upgrading React from 17 to 18" \
  --allowedTools "Read,Edit,Glob,Grep,Bash(npm:*)" \
  --max-turns 15
```

### Extract Common Code

```bash
claude -p "Find duplicated code patterns across src/ and extract them into shared utilities" \
  --allowedTools "Read,Write,Edit,Glob,Grep" \
  --max-turns 10
```

## Batch Processing

### Process Multiple Files

```bash
#!/bin/bash
# process-files.sh

files=$(find src -name "*.ts" -type f)

for file in $files; do
  echo "Processing: $file"
  claude -p "Ensure $file follows our coding standards:
    - Uses strict TypeScript
    - Has proper error handling
    - Uses async/await (no .then())
    - Has no console.log statements" \
    --allowedTools "Read,Edit" \
    --max-turns 2 \
    --output-format json \
    | jq -r '.result'
done
```

### Parallel Processing with xargs

```bash
find src -name "*.ts" | xargs -P 4 -I {} sh -c '
  claude -p "Add input validation to functions in {}" \
    --allowedTools "Read,Edit" \
    --max-turns 2
'
```

## Multi-Turn Workflows

### Iterative Development

```bash
#!/bin/bash
# iterative-dev.sh

# Start a feature
SESSION=$(claude -p "Start implementing a user authentication feature. Begin with the database schema." \
  --output-format json \
  --allowedTools "Read,Write,Edit" \
  | jq -r '.session_id')

# Continue implementation
claude -p "Now implement the API routes for login and logout" \
  --resume "$SESSION" \
  --allowedTools "Read,Write,Edit"

# Add tests
claude -p "Add unit tests for the authentication module" \
  --resume "$SESSION" \
  --allowedTools "Read,Write,Bash(bun test:*)"

# Final review
claude -p "Review the entire authentication feature and fix any issues" \
  --resume "$SESSION" \
  --allowedTools "Read,Edit,Bash(bun test:*)" \
  --output-format json
```

### Code Review Conversation

```bash
# Initial review
SESSION=$(claude -p "Review src/api/ for code quality issues" \
  --output-format json \
  --allowedTools "Read,Glob,Grep" \
  | jq -r '.session_id')

# Drill down
claude -p "Focus on the authentication handlers specifically" \
  --resume "$SESSION"

# Get fixes
claude -p "Fix the issues you found" \
  --resume "$SESSION" \
  --allowedTools "Read,Edit"
```

## Structured Output Examples

### Extract Code Metrics

```bash
claude -p "Analyze src/ and extract code metrics" \
  --output-format json \
  --json-schema '{
    "type": "object",
    "properties": {
      "totalFiles": {"type": "number"},
      "totalLines": {"type": "number"},
      "functions": {"type": "number"},
      "classes": {"type": "number"},
      "complexity": {"type": "string", "enum": ["low", "medium", "high"]}
    },
    "required": ["totalFiles", "totalLines", "complexity"]
  }' \
  --allowedTools "Read,Glob,Grep"
```

### Dependency Analysis

```bash
claude -p "Analyze package.json and list outdated or problematic dependencies" \
  --output-format json \
  --json-schema '{
    "type": "object",
    "properties": {
      "outdated": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "name": {"type": "string"},
            "current": {"type": "string"},
            "latest": {"type": "string"}
          }
        }
      },
      "security": {
        "type": "array",
        "items": {"type": "string"}
      },
      "unused": {
        "type": "array",
        "items": {"type": "string"}
      }
    }
  }' \
  --allowedTools "Read,Bash(npm:*)"
```

## Error Handling Patterns

### Robust Script with Retries

```bash
#!/bin/bash
# robust-claude.sh

MAX_RETRIES=3
RETRY_DELAY=5

run_claude() {
  local prompt="$1"
  local attempt=1

  while [ $attempt -le $MAX_RETRIES ]; do
    result=$(claude -p "$prompt" \
      --output-format json \
      --max-turns 5 \
      --allowedTools "Read,Edit" \
      2>&1)

    if [ $? -eq 0 ]; then
      echo "$result"
      return 0
    fi

    echo "Attempt $attempt failed, retrying in ${RETRY_DELAY}s..." >&2
    sleep $RETRY_DELAY
    ((attempt++))
  done

  echo "All retries failed" >&2
  return 1
}

# Usage
run_claude "Fix TypeScript errors in src/"
```

### Validate Output

```bash
#!/bin/bash
# validate-output.sh

result=$(claude -p "Analyze code quality" \
  --output-format json \
  --allowedTools "Read,Glob")

# Check if valid JSON
if ! echo "$result" | jq . > /dev/null 2>&1; then
  echo "Error: Invalid JSON response"
  exit 1
fi

# Check for required fields
if ! echo "$result" | jq -e '.result' > /dev/null 2>&1; then
  echo "Error: Missing 'result' field"
  exit 1
fi

# Extract and use result
echo "$result" | jq -r '.result'
```

## Budget Control

### Set Spending Limit

```bash
claude -p "Analyze entire codebase" \
  --max-budget-usd 5.00 \
  --allowedTools "Read,Glob,Grep" \
  --output-format json
```

### Monitor Usage

```bash
result=$(claude -p "Complex analysis" \
  --output-format json \
  --allowedTools "Read")

# Check usage
echo "$result" | jq '.usage'
# Output: {"input_tokens": 5000, "output_tokens": 1500}
```

## Security Best Practices

### Minimal Permissions

```bash
# Read-only analysis
claude -p "Analyze code for issues" \
  --allowedTools "Read,Glob,Grep" \
  --disallowedTools "Bash,Write,Edit"
```

### Sandbox Dangerous Operations

```bash
# Only in Docker/sandbox
docker run --rm -v $(pwd):/workspace node:20 sh -c '
  npm install -g @anthropic-ai/claude-code
  cd /workspace
  claude -p "Clean up and refactor" \
    --dangerously-skip-permissions \
    --allowedTools "Read,Edit,Bash"
'
```

### Audit Trail

```bash
#!/bin/bash
# audit-claude.sh

AUDIT_LOG="claude-audit.log"

run_with_audit() {
  local prompt="$1"
  local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  echo "[$timestamp] Prompt: $prompt" >> "$AUDIT_LOG"

  result=$(claude -p "$prompt" \
    --output-format json \
    --verbose 2>&1)

  echo "[$timestamp] Result: $result" >> "$AUDIT_LOG"
  echo "$result"
}

run_with_audit "Deploy to production"
```
