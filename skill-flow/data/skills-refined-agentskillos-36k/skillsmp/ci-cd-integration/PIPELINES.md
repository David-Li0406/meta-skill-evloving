# Pipeline Integration

Integrate Claude Code into CI/CD pipelines with quality gates, automated reviews, and release workflows.

## Quality Gates

### Basic Quality Gate

```yaml
# GitHub Actions
- name: Quality Gate
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    result=$(gh pr diff ${{ github.event.pull_request.number }} | \
      claude -p "Analyze this PR. Output JSON:
      {
        \"passed\": boolean,
        \"blockers\": [\"list of blocking issues\"],
        \"warnings\": [\"list of non-blocking warnings\"]
      }

      Blockers (fail the gate):
      - Security vulnerabilities
      - Breaking API changes without version bump
      - Missing tests for new functionality
      - Hardcoded secrets

      Pass if no blockers found." \
      --output-format json \
      --json-schema '{"type":"object","properties":{"passed":{"type":"boolean"},"blockers":{"type":"array","items":{"type":"string"}},"warnings":{"type":"array","items":{"type":"string"}}},"required":["passed","blockers","warnings"]}')

    passed=$(echo "$result" | jq -r '.structured_output.passed')
    if [ "$passed" != "true" ]; then
      echo "Quality gate failed!"
      echo "$result" | jq -r '.structured_output.blockers[]'
      exit 1
    fi
```

### Multi-Stage Quality Gate

```yaml
jobs:
  # Stage 1: Fast checks
  quick-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Fast Quality Check
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          # Check only critical issues
          gh pr diff ${{ github.event.pull_request.number }} | \
          claude -p "Quick check for critical issues only:
          - Secrets in code
          - SQL injection
          - Obvious crashes

          Respond: PASS or FAIL with reason" \
          --max-turns 1

  # Stage 2: Deep analysis (only if quick passes)
  deep-gate:
    needs: quick-gate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Deep Quality Analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Comprehensive quality analysis of PR #${{ github.event.pull_request.number }}.

          Check:
          1. Architecture alignment
          2. Error handling completeness
          3. Test coverage adequacy
          4. Documentation updates
          5. Performance implications

          Output detailed report." \
          --allowedTools "Read,Glob,Grep" \
          --max-turns 10
```

### Coverage Gate

```yaml
- name: Run Tests with Coverage
  run: bun test --coverage > coverage.txt

- name: Coverage Quality Gate
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    result=$(claude -p "Analyze this coverage report:

    $(cat coverage.txt)

    Quality gate criteria:
    - Overall coverage >= 80%
    - No new files with 0% coverage
    - Critical paths (auth, payment, data) >= 90%

    Output JSON:
    {
      \"passed\": boolean,
      \"overall_coverage\": number,
      \"uncovered_critical\": [\"list of critical files under 90%\"],
      \"reason\": \"explanation\"
    }" --output-format json)

    passed=$(echo "$result" | jq -r '.structured_output.passed')
    if [ "$passed" != "true" ]; then
      echo "Coverage gate failed"
      echo "$result" | jq '.structured_output'
      exit 1
    fi
```

### Security Gate

```yaml
- name: Security Gate
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    diff=$(gh pr diff ${{ github.event.pull_request.number }})

    result=$(echo "$diff" | claude -p "Security audit. Check for:

    CRITICAL (block):
    - Hardcoded secrets, API keys, passwords
    - SQL/NoSQL injection
    - Command injection
    - Path traversal
    - Authentication bypass
    - Insecure deserialization

    HIGH (block):
    - XSS vulnerabilities
    - CSRF vulnerabilities
    - Insecure direct object references
    - Missing input validation

    MEDIUM (warn):
    - Verbose error messages
    - Missing rate limiting
    - Weak cryptography

    Output JSON:
    {
      \"secure\": boolean,
      \"critical\": [{\"type\": string, \"location\": string, \"description\": string}],
      \"high\": [{\"type\": string, \"location\": string, \"description\": string}],
      \"medium\": [{\"type\": string, \"location\": string, \"description\": string}]
    }" --output-format json)

    secure=$(echo "$result" | jq -r '.structured_output.secure')
    if [ "$secure" != "true" ]; then
      echo "::error::Security vulnerabilities found"
      echo "$result" | jq '.structured_output'
      exit 1
    fi
```

## Automated Reviews

### PR Review Pipeline

```yaml
name: Automated PR Review Pipeline
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Get PR Context
        id: context
        run: |
          echo "diff<<EOF" >> $GITHUB_OUTPUT
          gh pr diff ${{ github.event.pull_request.number }} >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

          echo "description<<EOF" >> $GITHUB_OUTPUT
          gh pr view ${{ github.event.pull_request.number }} --json body -q '.body' >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

          echo "files<<EOF" >> $GITHUB_OUTPUT
          gh pr diff ${{ github.event.pull_request.number }} --name-only >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
        env:
          GH_TOKEN: ${{ github.token }}

      - name: Architecture Review
        id: arch
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          review=$(claude -p "Architecture review of PR.

          Changed files:
          ${{ steps.context.outputs.files }}

          Diff:
          ${{ steps.context.outputs.diff }}

          Evaluate:
          1. Does this follow existing patterns?
          2. Is the structure appropriate?
          3. Are there architectural concerns?

          Be concise." --max-turns 3 --output-format text)

          echo "review<<EOF" >> $GITHUB_OUTPUT
          echo "$review" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Code Quality Review
        id: quality
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          review=$(echo "${{ steps.context.outputs.diff }}" | claude -p "Code quality review.

          Check:
          - Clean code principles
          - Error handling
          - Edge cases
          - Naming conventions
          - Code duplication

          Format findings as bullet points." --max-turns 3 --output-format text)

          echo "review<<EOF" >> $GITHUB_OUTPUT
          echo "$review" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Security Review
        id: security
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          review=$(echo "${{ steps.context.outputs.diff }}" | claude -p "Security-focused review.

          Look for:
          - Input validation issues
          - Authentication/authorization problems
          - Data exposure risks
          - Injection vulnerabilities

          Only report actual findings, not general advice." --max-turns 3 --output-format text)

          echo "review<<EOF" >> $GITHUB_OUTPUT
          echo "$review" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Post Combined Review
        uses: actions/github-script@v7
        with:
          script: |
            const review = `## Automated Code Review

            ### Architecture
            ${{ steps.arch.outputs.review }}

            ### Code Quality
            ${{ steps.quality.outputs.review }}

            ### Security
            ${{ steps.security.outputs.review }}

            ---
            *Automated review by Claude Code Pipeline*`;

            await github.rest.issues.createComment({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              body: review
            });
```

### Incremental Review

Only review changed parts on subsequent pushes:

```yaml
- name: Get New Changes
  id: changes
  run: |
    # Get diff since last review
    last_reviewed=$(gh api repos/${{ github.repository }}/issues/${{ github.event.pull_request.number }}/comments \
      --jq '[.[] | select(.body | contains("Automated review by Claude"))] | last | .created_at' || echo "")

    if [ -n "$last_reviewed" ]; then
      # Get commits since last review
      new_commits=$(gh pr view ${{ github.event.pull_request.number }} --json commits \
        --jq "[.commits[] | select(.committedDate > \"$last_reviewed\")] | length")

      if [ "$new_commits" -eq 0 ]; then
        echo "skip=true" >> $GITHUB_OUTPUT
        exit 0
      fi
    fi

    echo "skip=false" >> $GITHUB_OUTPUT
  env:
    GH_TOKEN: ${{ github.token }}

- name: Review New Changes
  if: steps.changes.outputs.skip != 'true'
  run: |
    claude -p "Review only the NEW changes in this PR update..."
```

## Release Pipelines

### Semantic Version Determination

```yaml
- name: Determine Version
  id: version
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "v0.0.0")
    commits=$(git log $last_tag..HEAD --oneline)

    bump=$(claude -p "Analyze these commits and determine semantic version bump:

    $commits

    Rules:
    - MAJOR: Breaking changes (API changes, removed features)
    - MINOR: New features (backward compatible)
    - PATCH: Bug fixes, documentation, refactoring

    Look for:
    - 'BREAKING:' or '!' in commit messages = major
    - 'feat:' = minor
    - 'fix:', 'docs:', 'chore:', 'refactor:' = patch

    Output ONLY: major, minor, or patch" --max-turns 1 --output-format text)

    echo "bump=$(echo $bump | tr -d '[:space:]')" >> $GITHUB_OUTPUT
```

### Changelog Generation

```yaml
- name: Generate Changelog
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
  run: |
    last_tag=$(git describe --tags --abbrev=0 2>/dev/null || echo "")

    if [ -n "$last_tag" ]; then
      commits=$(git log $last_tag..HEAD --pretty=format:"%h %s")
    else
      commits=$(git log --pretty=format:"%h %s" -50)
    fi

    claude -p "Generate a changelog entry from these commits:

    $commits

    Format:
    ## [${{ steps.version.outputs.new_version }}] - $(date +%Y-%m-%d)

    ### Breaking Changes
    - List any breaking changes

    ### Added
    - List new features

    ### Changed
    - List changes to existing features

    ### Fixed
    - List bug fixes

    ### Security
    - List security fixes

    Remove empty sections. Group related changes. Be user-friendly." \
    --output-format text > CHANGELOG_ENTRY.md
```

### Release Notes Pipeline

```yaml
name: Release Pipeline
on:
  push:
    tags:
      - 'v*'

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

      - name: Generate Release Notes
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          prev_tag=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")

          if [ -n "$prev_tag" ]; then
            commits=$(git log $prev_tag..${{ github.ref_name }} --pretty=format:"- %s (%h)")
            diff_link="https://github.com/${{ github.repository }}/compare/$prev_tag...${{ github.ref_name }}"
          else
            commits=$(git log --pretty=format:"- %s (%h)" -50)
            diff_link=""
          fi

          claude -p "Generate release notes for version ${{ github.ref_name }}:

          Commits:
          $commits

          Include:
          1. Highlights (most important changes)
          2. Breaking Changes (if any)
          3. New Features
          4. Bug Fixes
          5. Contributors (extract from commits if possible)
          6. Full changelog link: $diff_link

          Write for end users, not developers. Be concise and highlight value." \
          --output-format text > RELEASE_NOTES.md

      - name: Create GitHub Release
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          gh release create ${{ github.ref_name }} \
            --title "Release ${{ github.ref_name }}" \
            --notes-file RELEASE_NOTES.md
```

## Pipeline Stages

### Standard CI Pipeline

```yaml
name: CI Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  # Stage 1: Build and Test
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: oven-sh/setup-bun@v1
      - run: bun install
      - run: bun run build
      - run: bun test

  # Stage 2: Code Quality (parallel with security)
  quality:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: bun run lint
      - name: Type Check
        run: bun run typecheck
      - name: Claude Quality Review
        if: github.event_name == 'pull_request'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          npm install -g @anthropic-ai/claude-code
          gh pr diff ${{ github.event.pull_request.number }} | \
            claude -p "Quick quality review" --max-turns 2
        env:
          GH_TOKEN: ${{ github.token }}

  # Stage 2: Security (parallel with quality)
  security:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Dependency Audit
        run: bun audit || true
      - name: Claude Security Review
        if: github.event_name == 'pull_request'
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          npm install -g @anthropic-ai/claude-code
          gh pr diff ${{ github.event.pull_request.number }} | \
            claude -p "Security-focused review" --max-turns 2
        env:
          GH_TOKEN: ${{ github.token }}

  # Stage 3: Gate
  gate:
    needs: [quality, security]
    runs-on: ubuntu-latest
    steps:
      - name: All Checks Passed
        run: echo "All quality and security checks passed"

  # Stage 4: Deploy (main only)
  deploy:
    needs: gate
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy
        run: echo "Deploying..."
```

### Deployment Pipeline

```yaml
name: Deploy Pipeline
on:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [staging, production]

jobs:
  pre-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Pre-deployment Check
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          npm install -g @anthropic-ai/claude-code

          claude -p "Pre-deployment checklist for ${{ inputs.environment }}:

          1. Check for pending migrations
          2. Verify environment variables
          3. Check for breaking changes
          4. Verify rollback plan exists

          Output JSON:
          {
            \"ready\": boolean,
            \"checklist\": [{\"item\": string, \"status\": \"pass\"|\"fail\"|\"warn\", \"note\": string}]
          }" \
          --allowedTools "Read,Glob,Grep" \
          --output-format json

  deploy-staging:
    needs: pre-deploy
    if: inputs.environment == 'staging'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to Staging
        run: echo "Deploying to staging..."

  deploy-production:
    needs: pre-deploy
    if: inputs.environment == 'production'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy to Production
        run: echo "Deploying to production..."

  post-deploy:
    needs: [deploy-staging, deploy-production]
    if: always() && (needs.deploy-staging.result == 'success' || needs.deploy-production.result == 'success')
    runs-on: ubuntu-latest
    steps:
      - name: Post-deployment Verification
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          npm install -g @anthropic-ai/claude-code

          claude -p "Generate post-deployment verification steps for ${{ inputs.environment }}.

          Include:
          1. Health check endpoints to verify
          2. Key user flows to test
          3. Metrics to monitor
          4. Rollback triggers" \
          --max-turns 2
```

## Pipeline Patterns

### Fail Fast

```yaml
- name: Quick Validation
  run: |
    # Fast checks first
    bun run lint || exit 1
    bun run typecheck || exit 1

    # Only then run expensive checks
    claude -p "Deep review" --max-turns 5
```

### Parallel Execution

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - run: bun run lint

  typecheck:
    runs-on: ubuntu-latest
    steps:
      - run: bun run typecheck

  claude-review:
    runs-on: ubuntu-latest
    steps:
      - run: claude -p "Review"

  # Wait for all parallel jobs
  gate:
    needs: [lint, typecheck, claude-review]
    steps:
      - run: echo "All passed"
```

### Conditional Depth

```yaml
- name: Determine Review Depth
  id: depth
  run: |
    # Check PR size
    additions=$(gh pr view ${{ github.event.pull_request.number }} --json additions -q '.additions')

    # Check file sensitivity
    sensitive=$(gh pr diff ${{ github.event.pull_request.number }} --name-only | grep -E '(auth|security|payment)' || true)

    if [ "$additions" -gt 500 ] || [ -n "$sensitive" ]; then
      echo "turns=10" >> $GITHUB_OUTPUT
    else
      echo "turns=3" >> $GITHUB_OUTPUT
    fi
  env:
    GH_TOKEN: ${{ github.token }}

- name: Claude Review
  run: |
    claude -p "Review PR" --max-turns ${{ steps.depth.outputs.turns }}
```

## Best Practices

### Pipeline Design

| Practice | Benefit |
|----------|---------|
| Fail fast | Quick feedback on obvious issues |
| Parallelize independent jobs | Faster overall pipeline |
| Cache dependencies | Reduce execution time |
| Use job outputs | Share data between jobs |

### Cost Optimization

| Practice | Benefit |
|----------|---------|
| Skip unchanged files | Fewer tokens |
| Use targeted prompts | Focused analysis |
| Set `--max-turns` limits | Bounded cost |
| Run expensive checks last | Avoid waste on failures |

### Reliability

| Practice | Benefit |
|----------|---------|
| Set timeouts | Prevent hung pipelines |
| Handle API errors | Graceful degradation |
| Log outputs | Debugging |
| Use `continue-on-error` wisely | Non-blocking warnings |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pipeline timeout | Add `--max-turns`, increase job timeout |
| API rate limits | Add retry logic, spread load |
| Large PR fails | Chunk diff, filter files |
| Inconsistent results | Use JSON schemas for structured output |
| Secret not found | Check repository/environment secrets |
| Permission denied | Check job permissions block |
