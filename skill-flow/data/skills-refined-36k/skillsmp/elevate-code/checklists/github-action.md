# GitHub Action Checklist

Complete validation checklist for GitHub Actions.

Based on official GitHub Actions documentation.

---

## Project Structure

### Composite Action
```
my-action/
├── action.yml             # Action definition
├── src/                   # Source code (if any)
├── dist/                  # Compiled code (for JS actions)
├── tests/
├── README.md
├── CLAUDE.md
└── LICENSE
```

### Docker Action
```
my-action/
├── action.yml
├── Dockerfile
├── entrypoint.sh
├── src/
├── tests/
├── README.md
└── LICENSE
```

---

## action.yml Structure

```yaml
name: 'My Action'
description: 'Clear description of what this action does'
author: 'Your Name'

branding:
  icon: 'check-circle'
  color: 'green'

inputs:
  input-name:
    description: 'What this input does'
    required: true
    default: 'default-value'

outputs:
  output-name:
    description: 'What this output contains'
    value: ${{ steps.step-id.outputs.result }}

runs:
  using: 'composite'  # or 'node20' or 'docker'
  steps:
    - name: Step name
      shell: bash
      run: echo "Hello"
```

---

## The Triad (Adapted for Actions)

### Health (Doctor)
- [ ] Validate required inputs at start
- [ ] Check for required tools/dependencies
- [ ] Clear error messages for invalid configuration
- [ ] Fail fast on missing requirements

### Safety (Safety Net)
- [ ] Dry-run input for destructive operations
- [ ] Preview changes before applying
- [ ] Idempotent operations where possible
- [ ] No force-push without explicit confirmation

### Resilience (Statekeeper)
- [ ] Retry transient failures (API rate limits)
- [ ] Graceful handling of partial failures
- [ ] Output artifacts for debugging
- [ ] Clear exit codes

---

## Input/Output Design

### Inputs
- [ ] All inputs documented with descriptions
- [ ] Required vs optional clearly marked
- [ ] Sensible defaults provided
- [ ] Input validation in action code
- [ ] Sensitive inputs marked as such

### Outputs
- [ ] All outputs documented
- [ ] Outputs set correctly (`$GITHUB_OUTPUT`)
- [ ] Machine-parseable format (JSON if complex)
- [ ] Error state clearly indicated

---

## Action Types

### Composite Action
```yaml
runs:
  using: 'composite'
  steps:
    - name: Validate inputs
      shell: bash
      run: |
        if [ -z "${{ inputs.required-input }}" ]; then
          echo "Error: required-input is required"
          exit 1
        fi

    - name: Main logic
      shell: bash
      run: |
        # Your action logic here
        echo "result=success" >> $GITHUB_OUTPUT
```

### JavaScript Action
```yaml
runs:
  using: 'node20'
  main: 'dist/index.js'
```

### Docker Action
```yaml
runs:
  using: 'docker'
  image: 'Dockerfile'
  args:
    - ${{ inputs.input-name }}
```

---

## Best Practices

### Performance
- [ ] Cache dependencies (actions/cache)
- [ ] Minimize Docker image size
- [ ] Use specific action versions (not `@main`)
- [ ] Parallelize independent steps

### Security
- [ ] Pin action versions with SHA
- [ ] Don't expose secrets in logs
- [ ] Use `GITHUB_TOKEN` minimally
- [ ] Validate external inputs
- [ ] No eval of user input

### Reliability
- [ ] Handle rate limiting gracefully
- [ ] Set appropriate timeouts
- [ ] Use retry for API calls
- [ ] Test with different OS/runners

---

## Error Handling

```bash
# Good: Clear error messages
if ! command -v required-tool &> /dev/null; then
  echo "::error::required-tool not found. Please install it."
  exit 1
fi

# Use GitHub Actions workflow commands
echo "::error file=app.js,line=10::Error message"
echo "::warning::This is a warning"
echo "::notice::This is a notice"
```

---

## Testing

### Local Testing
- [ ] Test script runs locally
- [ ] act for local workflow testing
- [ ] Test with different input combinations
- [ ] Test error scenarios

### CI Testing
- [ ] Workflow that tests the action
- [ ] Test on multiple OS (ubuntu, macos, windows)
- [ ] Test with different input values
- [ ] Integration test with real use case

```yaml
# .github/workflows/test.yml
name: Test Action

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Test action
        uses: ./
        with:
          input-name: 'test-value'

      - name: Verify output
        run: |
          if [ "${{ steps.test.outputs.result }}" != "expected" ]; then
            echo "Test failed!"
            exit 1
          fi
```

---

## Documentation

### README.md
- [ ] Action name and description
- [ ] All inputs documented with examples
- [ ] All outputs documented
- [ ] Usage example (copy-pasteable)
- [ ] Prerequisites listed
- [ ] Troubleshooting section

```markdown
## Usage

```yaml
- uses: owner/action-name@v1
  with:
    input-name: 'value'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `input-name` | What it does | Yes | - |

## Outputs

| Output | Description |
|--------|-------------|
| `result` | The result of the operation |
```

---

## Versioning

- [ ] Semantic versioning (v1.0.0)
- [ ] Major version tag (v1) points to latest v1.x.x
- [ ] Changelog maintained
- [ ] Breaking changes in major version
- [ ] Release notes with each version

```bash
# Tag releases properly
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Update major version tag
git tag -fa v1 -m "Update v1 tag"
git push origin v1 --force
```

---

## Publishing to Marketplace

- [ ] Action has clear name
- [ ] Description is comprehensive
- [ ] Branding (icon and color) configured
- [ ] README has usage example
- [ ] Released version exists
- [ ] Repository is public

---

## Quick Validation

```bash
# Validate action.yml
cat action.yml | yq .

# Check inputs are documented
grep -A5 "inputs:" action.yml

# Check for security issues
grep -rE "eval|exec\(" src/

# Test locally with act
act -j test

# Lint workflow files
actionlint .github/workflows/*.yml
```
