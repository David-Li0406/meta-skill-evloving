# Claude Code Cicd - Sharp Edges

## Headless Output Format

### **Id**
headless-output-format
### **Summary**
Wrong output format causes parsing failures
### **Severity**
high
### **Situation**
CI script can't parse Claude's response
### **Why**
  Default output is text, not structured.
  JSON output requires --output-format json.
  Stream JSON is different from regular JSON.
  
### **Solution**
  // Output formats for CI/CD
  
  // TEXT OUTPUT (default)
  claude -p "Explain this code" src/main.ts
  # Returns: Human-readable text, may include markdown
  
  // JSON OUTPUT
  claude -p "Return JSON with issues" --output-format json
  # Returns: {"result": "...", "usage": {...}}
  # Parse with: jq .result
  
  // STREAM JSON (for real-time processing)
  claude -p "Long analysis" --output-format stream-json
  # Returns: Multiple JSON lines (JSONL format)
  # Each line: {"type": "...", "content": "..."}
  
  // PARSING IN BASH
  # JSON:
  result=$(claude -p "..." --output-format json)
  issues=$(echo $result | jq -r '.result')
  
  # Stream JSON:
  claude -p "..." --output-format stream-json | while read line; do
    type=$(echo $line | jq -r '.type')
    if [ "$type" = "result" ]; then
      content=$(echo $line | jq -r '.content')
      echo $content
    fi
  done
  
  // COMMON MISTAKE: Expecting JSON from text mode
  # WRONG
  result=$(claude -p "Return JSON: {status: ok}")
  echo $result | jq .status  # Fails - result is text, not JSON
  
  # RIGHT
  result=$(claude -p "Return JSON: {status: ok}" --output-format json)
  echo $result | jq -r '.result' | jq .status
  
  // NODE.JS PARSING
  import { execSync } from 'child_process';
  
  const output = execSync(
    'claude -p "..." --output-format json'
  ).toString();
  
  const parsed = JSON.parse(output);
  const result = parsed.result;
  
### **Symptoms**
  - jq: parse error
  - Unexpected token in JSON
  - Empty or truncated output
### **Detection Pattern**
jq.*claude -p|--output-format text.*jq

## Ci Timeout Issues

### **Id**
ci-timeout-issues
### **Summary**
Claude times out in CI, job fails
### **Severity**
high
### **Situation**
Long-running Claude commands exceed CI timeout
### **Why**
  Complex analysis can take minutes.
  CI jobs have default timeouts.
  No streaming means no visibility during execution.
  
### **Solution**
  // Handle timeouts in CI
  
  // GITHUB ACTIONS - Set timeout
  - name: Claude Review
    timeout-minutes: 10  # Increase from default 6
    run: |
      claude -p "Review code" --max-tokens 2000
  
  // GITLAB CI - Set timeout
  claude-review:
    timeout: 15 minutes
    script:
      - claude -p "Review code"
  
  // LIMIT OUTPUT LENGTH
  claude -p "Brief review, max 500 words" \
    --max-tokens 1000
  
  // USE SMALLER MODEL FOR SPEED
  # Haiku is faster than Sonnet
  claude -p "Quick triage" --model claude-haiku-3-5
  
  // SPLIT LARGE TASKS
  # Instead of reviewing all files at once
  for file in $(git diff --name-only); do
    claude -p "Review $file briefly" --max-tokens 500
  done
  
  // BACKGROUND WITH TIMEOUT
  timeout 300 claude -p "Long analysis" > result.txt &
  pid=$!
  
  # Poll for completion
  while kill -0 $pid 2>/dev/null; do
    echo "Still running..."
    sleep 10
  done
  
  // STREAMING FOR VISIBILITY
  # Stream shows progress during execution
  claude -p "Analysis" --output-format stream-json | \
    while read line; do
      echo "Progress: $(echo $line | jq -r .type)"
    done
  
### **Symptoms**
  - Job killed after timeout
  - No output before failure
  - Works locally, fails in CI
### **Detection Pattern**
timeout-minutes.*[0-2]|SIGTERM|killed

## Environment Variable Exposure

### **Id**
environment-variable-exposure
### **Summary**
API keys or prompts appear in logs
### **Severity**
critical
### **Situation**
Secrets visible in CI logs
### **Why**
  CI logs are often accessible to team.
  echo/debug statements expose values.
  Error messages may include sensitive data.
  
### **Solution**
  // Secure secret handling in CI
  
  // GITHUB ACTIONS - Use secrets
  - name: Review
    env:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    run: |
      # Key is in env, not in command line
      claude -p "Review code"
  
  // MASK VALUES
  - name: Setup
    run: |
      echo "::add-mask::${{ secrets.ANTHROPIC_API_KEY }}"
  
  // DON'T ECHO PROMPTS WITH SENSITIVE DATA
  # WRONG
  echo "Running: claude -p '$PROMPT_WITH_DATA'"
  claude -p "$PROMPT_WITH_DATA"
  
  # RIGHT
  echo "Running Claude review..."
  claude -p "$PROMPT_WITH_DATA" 2>/dev/null
  
  // USE PROMPT FILES INSTEAD
  # Store prompt in file, not variable
  cat > prompt.txt << 'EOF'
  Review this code for security issues
  EOF
  cat prompt.txt | claude -p -
  
  // GITLAB CI - Use masked variables
  variables:
    ANTHROPIC_API_KEY:
      value: $ANTHROPIC_API_KEY
      masked: true
  
  // CLEAN UP AFTER
  - name: Cleanup
    if: always()
    run: |
      rm -f prompt.txt analysis.json
      unset ANTHROPIC_API_KEY
  
  // CHECK FOR LEAKED SECRETS IN OUTPUT
  - name: Validate output
    run: |
      if grep -q "sk-ant-" result.txt; then
        echo "ERROR: API key in output!"
        exit 1
      fi
  
### **Symptoms**
  - API key visible in logs
  - Security scan alerts
  - Unauthorized API usage
### **Detection Pattern**
echo.*API_KEY|echo.*\$\{.*KEY|--api-key.*\$

## Allowed Tools Bypass

### **Id**
allowed-tools-bypass
### **Summary**
Claude uses tools you didn't intend to allow
### **Severity**
high
### **Situation**
Claude executes unexpected commands in CI
### **Why**
  Default allows many tools.
  --allowedTools requires exact matching.
  Wildcard patterns may over-permit.
  
### **Solution**
  // Properly restrict tools in CI
  
  // DENY BY DEFAULT - Explicit allow list
  claude -p "Fix bugs" \
    --allowedTools "Read,Edit,Write"
    # Only file operations, no Bash
  
  // ALLOW SPECIFIC COMMANDS
  claude -p "Run tests and fix" \
    --allowedTools "Read,Edit,Bash(npm test),Bash(npm run lint)"
    # Can only run npm test and lint
  
  // PATTERNS FOR BASH
  --allowedTools "Bash(npm *)"      # Any npm command
  --allowedTools "Bash(git status)" # Only git status
  --allowedTools "Bash(ls *)"       # Only ls commands
  
  // DANGEROUS - DON'T DO THIS
  --allowedTools "Bash"             # All bash commands!
  --allowedTools "Bash(*)"          # Same as above
  --allowedTools "Bash(rm *)"       # Can delete anything!
  
  // RECOMMENDED CI PROFILES
  # Review only (no changes):
  --allowedTools "Read,Grep,Glob"
  
  # Fix issues (controlled changes):
  --allowedTools "Read,Edit,Bash(npm run lint:fix)"
  
  # Full implementation (careful!):
  --allowedTools "Read,Write,Edit,Bash(npm test),Bash(npm run build)"
  
  // VERIFY RESTRICTIONS
  # Test your restrictions locally first
  claude -p "Delete all files" \
    --allowedTools "Read,Edit"
  # Should refuse to use rm
  
  // AUDIT TOOL USAGE
  # Log which tools were used
  claude -p "..." --output-format stream-json | \
    jq 'select(.type == "tool_use") | .name' | \
    sort | uniq
  
### **Symptoms**
  - Unexpected file changes
  - Commands run that shouldn't
  - Security violations
### **Detection Pattern**
--allowedTools.*Bash[^(]|--allowedTools.*\\*

## Rate Limit Handling

### **Id**
rate-limit-handling
### **Summary**
CI fails due to API rate limits
### **Severity**
medium
### **Situation**
Multiple concurrent jobs hit rate limits
### **Why**
  CI runs many jobs in parallel.
  Each job makes API calls.
  Rate limits are per-organization.
  
### **Solution**
  // Handle rate limits in CI
  
  // RETRY WITH BACKOFF
  max_retries=3
  retry_delay=60
  
  for i in $(seq 1 $max_retries); do
    if claude -p "Review" --output-format json > result.json 2>&1; then
      break
    fi
  
    if grep -q "rate_limit" result.json; then
      echo "Rate limited, waiting ${retry_delay}s..."
      sleep $retry_delay
      retry_delay=$((retry_delay * 2))
    else
      echo "Failed for non-rate-limit reason"
      exit 1
    fi
  done
  
  // LIMIT CONCURRENCY
  # GitHub Actions
  jobs:
    review:
      concurrency:
        group: claude-api
        cancel-in-progress: false
  
  # GitLab CI
  claude-review:
    resource_group: claude-api
  
  // QUEUE LARGE BATCHES
  # Instead of parallel, use sequential
  - name: Review files sequentially
    run: |
      for file in src/*.ts; do
        claude -p "Review $file" >> reviews.md
        sleep 2  # Rate limit buffer
      done
  
  // USE CACHING
  # Don't re-review unchanged files
  - uses: actions/cache@v4
    with:
      path: .claude-review-cache
      key: claude-review-${{ hashFiles('src/**') }}
  
  - name: Review
    run: |
      if [ ! -f .claude-review-cache/result.md ]; then
        claude -p "Review" > .claude-review-cache/result.md
      fi
  
  // MONITOR USAGE
  # Track costs and rate limit hits
  claude -p "..." --output-format json | \
    jq '{tokens: .usage, timestamp: now}' >> usage.log
  
### **Symptoms**
  - 429 Too Many Requests
  - Random job failures
  - Works sometimes, fails others
### **Detection Pattern**
rate_limit|429|too.many.requests

## Context Window Overflow

### **Id**
context-window-overflow
### **Summary**
Large PRs exceed Claude's context window
### **Severity**
medium
### **Situation**
Analysis fails or truncates on large changes
### **Why**
  Context window has limits.
  Large diffs exceed capacity.
  No clear error for overflow.
  
### **Solution**
  // Handle large contexts in CI
  
  // CHECK DIFF SIZE FIRST
  diff_lines=$(git diff --stat | tail -1 | grep -oE '[0-9]+' | head -1)
  
  if [ "$diff_lines" -gt 1000 ]; then
    echo "Large diff ($diff_lines lines) - splitting review"
  
    # Review file by file
    for file in $(git diff --name-only); do
      echo "## Reviewing $file" >> review.md
      claude -p "Review only this file: $file" >> review.md
    done
  else
    # Normal review
    claude -p "Review all changes" > review.md
  fi
  
  // SUMMARIZE THEN DETAIL
  # First pass: summary
  summary=$(claude -p "Summarize these changes in 100 words" \
    --max-tokens 200)
  
  # Second pass: focused reviews
  for critical_file in $(identify-critical-files); do
    claude -p "Deep review of $critical_file" >> reviews.md
  done
  
  // FILTER NOISE
  # Skip generated files, tests, etc.
  git diff --name-only | \
    grep -v 'package-lock.json\|\.generated\.\|\.test\.' | \
    xargs claude -p "Review these files"
  
  // CHUNK LARGE FILES
  split_file() {
    local file=$1
    local chunk_size=200  # lines per chunk
  
    split -l $chunk_size $file /tmp/chunk_
  
    for chunk in /tmp/chunk_*; do
      claude -p "Review this code chunk from $file" $chunk
    done
  }
  
  // SET EXPLICIT LIMITS
  claude -p "Brief review (max 500 words)" \
    --max-tokens 1000 \
    $(git diff --name-only | head -10)  # First 10 files only
  
### **Symptoms**
  - Incomplete reviews
  - Model errors about length
  - Truncated output
### **Detection Pattern**
max.*context|too.long|truncat