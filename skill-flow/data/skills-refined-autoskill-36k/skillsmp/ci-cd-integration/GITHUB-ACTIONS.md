# GitHub Actions Integration

Complete workflows for integrating Claude Code with GitHub Actions for automated code review, testing, and deployment.

## Prerequisites

### Repository Secrets

Set up these secrets in your repository (Settings > Secrets and variables > Actions):

| Secret | Required | Description |
|--------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key |

### Permissions

Most workflows need these permissions:

```yaml
permissions:
  contents: read
  pull-requests: write
  issues: write
```

## Complete PR Review Workflow

```yaml
name: Claude PR Review
on:
  pull_request:
    types: [opened, synchronize, reopened]

permissions:
  contents: read
  pull-requests: write

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Get PR Info
        id: pr
        run: |
          echo "diff<<EOF" >> $GITHUB_OUTPUT
          gh pr diff ${{ github.event.pull_request.number }} >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
        env:
          GH_TOKEN: ${{ github.token }}

      - name: Run Claude Review
        id: review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          review=$(cat << 'PROMPT' | claude -p - --output-format text
          Review this pull request diff for:

          1. **Security Issues** - SQL injection, XSS, auth bypasses, secrets
          2. **Logic Errors** - Off-by-one, null handling, race conditions
          3. **Performance** - N+1 queries, unnecessary loops, memory leaks
          4. **Code Quality** - Naming, complexity, duplication
          5. **Testing** - Missing tests, edge cases

          PR Diff:
          ${{ steps.pr.outputs.diff }}

          Format as markdown with severity (Critical/Warning/Info) for each finding.
          If no issues found, say "No issues found. LGTM!"
          PROMPT
          )

          echo "review<<EOF" >> $GITHUB_OUTPUT
          echo "$review" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const review = `## Claude Code Review

            ${{ steps.review.outputs.review }}

            ---
            *Automated review by Claude Code*`;

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: review
            });
```

## Targeted File Review

Review only specific file types or paths:

```yaml
name: Claude Review - TypeScript Only
on:
  pull_request:
    paths:
      - '**.ts'
      - '**.tsx'

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get Changed TypeScript Files
        id: files
        run: |
          files=$(gh pr diff ${{ github.event.pull_request.number }} --name-only | grep -E '\.tsx?$' || true)
          echo "files<<EOF" >> $GITHUB_OUTPUT
          echo "$files" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
        env:
          GH_TOKEN: ${{ github.token }}

      - name: Review TypeScript Changes
        if: steps.files.outputs.files != ''
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          for file in ${{ steps.files.outputs.files }}; do
            echo "Reviewing $file..."
            claude -p "Review TypeScript file $file for type safety, proper error handling, and React best practices (if applicable). Be concise." \
              --allowedTools "Read" \
              --max-turns 2
          done
```

## Security-Focused Review

```yaml
name: Security Review
on:
  pull_request:
    paths:
      - 'src/api/**'
      - 'src/auth/**'
      - '**/*security*'
      - '**/*auth*'

jobs:
  security-review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      security-events: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Security Analysis
        id: security
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          diff=$(gh pr diff ${{ github.event.pull_request.number }})

          result=$(echo "$diff" | claude -p "Security audit this code change.

          Check for:
          - SQL/NoSQL injection
          - XSS vulnerabilities
          - Authentication/authorization issues
          - Sensitive data exposure
          - Hardcoded secrets or API keys
          - Insecure cryptography
          - Path traversal
          - Command injection
          - SSRF vulnerabilities

          Output JSON:
          {
            \"risk_level\": \"high|medium|low|none\",
            \"findings\": [{
              \"severity\": \"critical|high|medium|low\",
              \"type\": \"vulnerability type\",
              \"description\": \"what's wrong\",
              \"file\": \"filename\",
              \"recommendation\": \"how to fix\"
            }]
          }" --output-format json)

          echo "result<<EOF" >> $GITHUB_OUTPUT
          echo "$result" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
        env:
          GH_TOKEN: ${{ github.token }}

      - name: Check Security Gate
        run: |
          risk=$(echo '${{ steps.security.outputs.result }}' | jq -r '.structured_output.risk_level // .risk_level // "unknown"')
          if [ "$risk" = "high" ] || [ "$risk" = "critical" ]; then
            echo "::error::Security review found high-risk issues"
            exit 1
          fi

      - name: Post Security Report
        uses: actions/github-script@v7
        with:
          script: |
            const result = JSON.parse(`${{ steps.security.outputs.result }}`);
            const findings = result.structured_output?.findings || result.findings || [];

            let report = '## Security Review Report\n\n';

            if (findings.length === 0) {
              report += 'No security issues found.\n';
            } else {
              report += '| Severity | Type | Description | File |\n';
              report += '|----------|------|-------------|------|\n';
              for (const f of findings) {
                report += `| ${f.severity} | ${f.type} | ${f.description} | ${f.file || 'N/A'} |\n`;
              }
            }

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: report
            });
```

## Automated Test Fixing

```yaml
name: Fix Failing Tests
on:
  workflow_dispatch:
  push:
    branches: [main, develop]

jobs:
  test-and-fix:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1

      - name: Install Dependencies
        run: bun install

      - name: Run Tests
        id: test
        continue-on-error: true
        run: |
          bun test 2>&1 | tee test-output.txt
          echo "status=$?" >> $GITHUB_OUTPUT

      - name: Fix Failing Tests
        if: steps.test.outputs.status != '0'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          npm install -g @anthropic-ai/claude-code

          claude -p "The tests are failing. Here's the output:

          $(cat test-output.txt)

          Analyze the failures and fix them. Make minimal changes.
          After fixing, run the tests again to verify." \
          --allowedTools "Read,Edit,Bash(bun test:*)" \
          --max-turns 10

      - name: Verify Fix
        run: bun test

      - name: Commit Fixes
        if: success()
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add -A
          git diff --staged --quiet || git commit -m "fix: auto-fix failing tests"
          git push
```

## Documentation Generation

```yaml
name: Generate Documentation
on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - '!src/**/*.test.ts'

jobs:
  docs:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Generate API Docs
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Generate or update API documentation for all public exports in src/.
          Update docs/API.md with:
          - Function signatures
          - Parameter descriptions
          - Return types
          - Usage examples

          Follow JSDoc conventions." \
          --allowedTools "Read,Write,Glob,Grep" \
          --max-turns 15

      - name: Commit Documentation
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/
          git diff --staged --quiet || git commit -m "docs: auto-update API documentation"
          git push
```

## Release Automation

```yaml
name: Prepare Release
on:
  workflow_dispatch:
    inputs:
      version_type:
        description: 'Version bump type'
        required: true
        default: 'patch'
        type: choice
        options:
          - patch
          - minor
          - major

jobs:
  release:
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Generate Changelog
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
          if [ -n "$last_tag" ]; then
            commits=$(git log $last_tag..HEAD --oneline)
          else
            commits=$(git log --oneline -50)
          fi

          claude -p "Generate a changelog entry from these commits:

          $commits

          Format as:
          ## [version] - $(date +%Y-%m-%d)

          ### Breaking Changes
          - List breaking changes (if any)

          ### Features
          - List new features

          ### Bug Fixes
          - List bug fixes

          ### Other
          - List other changes

          Remove empty sections. Be concise." \
          --output-format text > CHANGELOG_ENTRY.md

      - name: Update Version
        run: npm version ${{ inputs.version_type }} --no-git-tag-version

      - name: Create Release PR
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          version=$(node -p "require('./package.json').version")
          branch="release/v$version"

          git checkout -b "$branch"
          git add package.json package-lock.json CHANGELOG_ENTRY.md
          git commit -m "chore: prepare release v$version"
          git push origin "$branch"

          gh pr create \
            --title "Release v$version" \
            --body "$(cat CHANGELOG_ENTRY.md)" \
            --base main \
            --head "$branch"
```

## Scheduled Maintenance

```yaml
name: Weekly Code Health
on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 9 AM

jobs:
  health-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Code Health Analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Analyze the codebase health:

          1. Find TODOs, FIXMEs, and HACKs
          2. Identify unused exports
          3. Find overly complex functions (cyclomatic complexity)
          4. Check for outdated patterns
          5. Identify potential tech debt

          Output a markdown report suitable for a GitHub issue." \
          --allowedTools "Read,Glob,Grep" \
          --max-turns 10 > health-report.md

      - name: Create Issue
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh issue create \
            --title "Weekly Code Health Report - $(date +%Y-%m-%d)" \
            --body "$(cat health-report.md)" \
            --label "tech-debt,automated"
```

## Matrix Testing

```yaml
name: Cross-Platform Test
on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node: [18, 20]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}

      - name: Install Dependencies
        run: npm install

      - name: Run Tests
        id: test
        continue-on-error: true
        run: npm test 2>&1 | tee test-output.txt

      - name: Analyze Failures
        if: steps.test.outcome == 'failure'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          npm install -g @anthropic-ai/claude-code
          claude -p "Analyze test failure on ${{ matrix.os }} with Node ${{ matrix.node }}:

          $(cat test-output.txt)

          Is this a platform-specific issue? What's the root cause?" \
          --max-turns 2
```

## Workflow Caching

Speed up workflows by caching Claude Code installation:

```yaml
- name: Cache Claude Code
  uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-claude-code-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-claude-code-

- name: Install Claude Code
  run: npm install -g @anthropic-ai/claude-code
```

## Error Handling Patterns

### Graceful Failure

```yaml
- name: Claude Review
  id: review
  continue-on-error: true
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    timeout 300 claude -p "Review code" --max-turns 3 || echo "Review timed out or failed"

- name: Fallback on Failure
  if: steps.review.outcome == 'failure'
  run: echo "Claude review unavailable. Please review manually."
```

### Retry Logic

```yaml
- name: Claude Review with Retry
  uses: nick-fields/retry@v3
  with:
    timeout_minutes: 5
    max_attempts: 3
    command: |
      claude -p "Review code" --output-format json > review.json
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

## Conditional Workflows

### Skip on Draft PRs

```yaml
jobs:
  review:
    if: github.event.pull_request.draft == false
    runs-on: ubuntu-latest
```

### Skip Bot PRs

```yaml
jobs:
  review:
    if: github.actor != 'dependabot[bot]' && github.actor != 'renovate[bot]'
    runs-on: ubuntu-latest
```

### Size-Based Review Depth

```yaml
- name: Get PR Size
  id: size
  run: |
    additions=$(gh pr view ${{ github.event.pull_request.number }} --json additions -q '.additions')
    if [ "$additions" -gt 500 ]; then
      echo "depth=thorough" >> $GITHUB_OUTPUT
    else
      echo "depth=quick" >> $GITHUB_OUTPUT
    fi
  env:
    GH_TOKEN: ${{ github.token }}

- name: Quick Review
  if: steps.size.outputs.depth == 'quick'
  run: claude -p "Quick review" --max-turns 2

- name: Thorough Review
  if: steps.size.outputs.depth == 'thorough'
  run: claude -p "Thorough review" --max-turns 10
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "ANTHROPIC_API_KEY not set" | Add secret to repository settings |
| "Permission denied" | Check workflow permissions block |
| "Rate limited" | Add retry logic or reduce frequency |
| Workflow hangs | Add `--max-turns` and `timeout` |
| Large diffs fail | Filter files or chunk the diff |
| Comment creation fails | Ensure `pull-requests: write` permission |
