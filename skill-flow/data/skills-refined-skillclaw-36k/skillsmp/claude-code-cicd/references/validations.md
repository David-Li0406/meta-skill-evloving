# Claude Code Cicd - Validations

## API Key in Plain Text

### **Id**
exposed-api-key
### **Severity**
critical
### **Type**
regex
### **Pattern**
sk-ant-[a-zA-Z0-9-_]{20,}|ANTHROPIC_API_KEY\s*[=:]\s*["\x27][^$]
### **Message**
API key appears in plain text. Use secrets or environment variables.
### **Fix Action**
Use ${{ secrets.ANTHROPIC_API_KEY }} or masked variables
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml
  - .gitlab-ci.yml
  - *.sh

## Echoing Secret Value

### **Id**
echo-secret
### **Severity**
critical
### **Type**
regex
### **Pattern**
echo.*\$.*API_KEY|echo.*\$.*SECRET|printf.*\$.*KEY
### **Message**
Echoing secret values exposes them in logs.
### **Fix Action**
Remove echo statements that print secrets
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml
  - .gitlab-ci.yml
  - *.sh

## Unrestricted Bash in allowedTools

### **Id**
unrestricted-bash
### **Severity**
high
### **Type**
regex
### **Pattern**
--allowedTools.*["'\']Bash["'\']|--allowedTools.*Bash[^(]
### **Message**
Unrestricted Bash access in CI. Specify allowed commands.
### **Fix Action**
Use --allowedTools "Bash(npm test),Bash(npm run lint)"
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml
  - .gitlab-ci.yml
  - *.sh

## Claude Command Without Timeout

### **Id**
missing-timeout
### **Severity**
medium
### **Type**
regex
### **Pattern**
claude\s+-p\s+
### **Negative Pattern**
timeout-minutes|timeout:|--max-tokens
### **Message**
Claude command without timeout or token limit may hang CI.
### **Fix Action**
Add timeout-minutes to step or --max-tokens to command
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml
  - .gitlab-ci.yml

## Missing Output Format for Parsing

### **Id**
no-output-format
### **Severity**
medium
### **Type**
regex
### **Pattern**
claude.*-p.*\|\s*jq
### **Negative Pattern**
--output-format\s+(json|stream-json)
### **Message**
Using jq but Claude output may not be JSON.
### **Fix Action**
Add --output-format json for JSON output
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml
  - .gitlab-ci.yml
  - *.sh

## Parallel Jobs Without Concurrency Limit

### **Id**
no-concurrency-limit
### **Severity**
medium
### **Type**
regex
### **Pattern**
jobs:\s*\n\s+\w+:
### **Negative Pattern**
concurrency:|resource_group:
### **Message**
Multiple Claude jobs may hit rate limits without concurrency control.
### **Fix Action**
Add concurrency group to limit parallel API calls
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml
  - .gitlab-ci.yml

## Auto-Merge Based on AI Review

### **Id**
auto-merge-enabled
### **Severity**
high
### **Type**
regex
### **Pattern**
auto.*merge|merge.*auto
### **Message**
Auto-merging based on AI review is risky. Require human approval.
### **Fix Action**
Use AI for review suggestions, require human merge approval
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml
  - .gitlab-ci.yml

## Claude Triggered on Every Commit

### **Id**
every-commit-trigger
### **Severity**
medium
### **Type**
regex
### **Pattern**
on:\s*\n\s+push:\s*$
### **Negative Pattern**
paths:|branches:|pull_request
### **Message**
Claude runs on every push. Consider PR-only or path filtering.
### **Fix Action**
Add paths filter or use pull_request trigger
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml

## Large Model for Simple Tasks

### **Id**
large-model-for-triage
### **Severity**
low
### **Type**
regex
### **Pattern**
claude.*-p.*(label|triage|categorize).*--model.*(opus|sonnet)
### **Message**
Using large model for simple triage. Consider claude-haiku for cost savings.
### **Fix Action**
Use --model claude-haiku-3-5 for simple tasks
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml
  - .gitlab-ci.yml
  - *.sh

## Claude Command Without Error Handling

### **Id**
no-error-handling
### **Severity**
low
### **Type**
regex
### **Pattern**
claude\s+-p.*\n\s*-\s*name:
### **Negative Pattern**
\|\||if.*then|2>&1|set\s+-e
### **Message**
Claude command without error handling. Failures may go unnoticed.
### **Fix Action**
Add error handling: || echo 'Review failed' or if condition
### **Applies To**
  - .github/workflows/*.yml
  - .github/workflows/*.yaml