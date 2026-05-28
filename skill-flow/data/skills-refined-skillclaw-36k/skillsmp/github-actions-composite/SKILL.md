---
name: github-actions-composite
description: Creates GitHub Actions composite actions. Use when building reusable action.yml files, integrating github-script, or setting up action inputs/outputs.
---

# GitHub Actions Composite Actions

Composite actions bundle multiple workflow steps into a reusable `action.yml` file. Use composite actions when orchestrating shell commands, calling other actions, or adding JavaScript via `github-script`. This guide covers composite actions only (not JavaScript or Docker actions).

## action.yml Structure

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Display name for the action |
| `description` | Yes | Short description of what the action does |
| `inputs.<id>.description` | Yes | Description of the input |
| `inputs.<id>.required` | No | Whether input is required (default: false) |
| `inputs.<id>.default` | No | Default value when not provided |
| `outputs.<id>.description` | Yes | Description of the output |
| `outputs.<id>.value` | Yes | Value expression (usually from step output) |
| `runs.using` | Yes | Must be `"composite"` |
| `runs.steps` | Yes | Array of steps to execute |

## Minimal Example

```yaml
name: 'Greet User'
description: 'Greets a user by name'

inputs:
  name:
    description: 'Name to greet'
    required: true

outputs:
  greeting:
    description: 'The greeting message'
    value: ${{ steps.greet.outputs.greeting }}

runs:
  using: "composite"
  steps:
    - id: greet
      shell: bash
      run: |
        MESSAGE="Hello, ${{ inputs.name }}!"
        echo "greeting=$MESSAGE" >> "$GITHUB_OUTPUT"
```

## Step Properties

| Property | Required | Description |
|----------|----------|-------------|
| `id` | No* | Step identifier. Required if other steps reference this steps outputs. |
| `name` | No | Display name in workflow logs |
| `run` | No** | Shell command to execute |
| `shell` | Yes*** | Required when using `run` (`bash`, `pwsh`, `python`, etc.) |
| `uses` | No** | Call another action. `run` and `uses` are mutually exclusive. |
| `with` | No | Inputs to pass when using `uses` |
| `env` | No | Environment variables for this step |
| `if` | No | Conditional expression |
| `working-directory` | No | Directory for `run` commands |

## Using Other Actions

Composite actions can call other actions with `uses`:

```yaml
steps:
  - uses: actions/checkout@<pinned sha> # <version tag>
    with:
      fetch-depth: 0

  - uses: actions/setup-node@<pinned sha> # <version tag>
    with:
      node-version: '24'

  - id: build
    shell: bash
    run: npm run build
```

The called action runs in the composite action's context. Pass required inputs explicitly.

## Using github-script

Use `actions/github-script` to run JavaScript within composite actions for GitHub API access.

### Available Objects

| Object | Description |
|--------|-------------|
| `github` | Pre-authenticated Octokit REST client (`github.rest.*`) |
| `context` | Workflow context (repo, sha, ref, actor, issue, etc.) |
| `core` | @actions/core (setOutput, setFailed, info, warning, error) |
| `io` | @actions/io for file operations |
| `exec` | @actions/exec for running commands |

### Basic Usage

```yaml
- uses: actions/github-script@<pinned sha> # <version tag>
  with:
    script: |
      const { data: pr } = await github.rest.pulls.get({
        owner: context.repo.owner,
        repo: context.repo.repo,
        pull_number: context.issue.number
      });
      core.setOutput('title', pr.title);
```

### SECURITY: Use Environment Variables for Inputs

**Never** interpolate untrusted input directly into the script:

```yaml
# UNSAFE - vulnerable to script injection
- uses: actions/github-script@<pinned sha> # <version tag>
  with:
    script: |
      const title = "${{ inputs.title }}";  // DANGEROUS

# SAFE - use environment variables
- uses: actions/github-script@<pinned sha> # <version tag>
  env:
    TITLE: ${{ inputs.title }}
  with:
    script: |
      const title = process.env.TITLE;  // Safe
      core.info(`Processing: ${title}`);
```

### Returning Values

Return values are available as `steps.<id>.outputs.result`:

```yaml
- id: get-version
  uses: actions/github-script@60a0d83039c74a4aee543508d2ffcb1c3799cdea # v7.0.1
  with:
    result-encoding: string
    script: |
      const pkg = require('./package.json');
      return pkg.version;

- shell: bash
  run: echo "Version is ${{ steps.get-version.outputs.result }}"
```

## Security Best Practices

### ALWAYS Pin Actions to Full Commit SHAs

**Always pin actions to full commit SHAs. No exceptions.** Tags and versions can be moved to malicious code at any time:

```yaml
# UNSAFE - tag can be moved
- uses: actions/checkout@v4

# SAFE - immutable commit reference
- uses: actions/checkout@<pinned sha> # <version tag>
```

Use `npx pin-github-action` to automatically pin actions to their current SHAs:

```bash
npx pin-github-action .github/actions/my-action/action.yml
```

### Environment Variables for Untrusted Input

Expression syntax (`${{ }}`) is evaluated before the shell runs:

```yaml
# VULNERABLE - if inputs.filename contains: foo; rm -rf /
- shell: bash
  run: cat ${{ inputs.filename }}

# SAFE - shell handles the variable
- shell: bash
  env:
    FILENAME: ${{ inputs.filename }}
  run: cat "$FILENAME"
```

### Input Validation

Validate inputs at the start of your action:

```yaml
- shell: bash
  env:
    INPUT_MODE: ${{ inputs.mode }}
  run: |
    if [[ ! "$INPUT_MODE" =~ ^(create|update|delete)$ ]]; then
      echo "::error::Invalid mode: $INPUT_MODE. Must be create, update, or delete."
      exit 1
    fi
```

### Document Required Permissions

In your action's README, document minimum required permissions:

```yaml
# Required workflow permissions:
# permissions:
#   contents: read
#   pull-requests: write
```

## Common Patterns

### Conditional Steps

```yaml
- if: ${{ inputs.skip-tests != 'true' }}
  shell: bash
  run: npm test
```

### Multi-line Scripts with Outputs

```yaml
- id: extract
  shell: bash
  run: |
    VERSION=$(cat VERSION)
    echo "version=$VERSION" >> "$GITHUB_OUTPUT"
```

### Passing Outputs to Action Output

```yaml
outputs:
  version:
    description: 'Extracted version'
    value: ${{ steps.extract.outputs.version }}
```

### Default Input Values

```yaml
inputs:
  node-version:
    description: 'Node.js version'
    required: false
    default: '20'
```

### Working Directory

```yaml
- shell: bash
  working-directory: ./packages/core
  run: npm install
```

## File Locations

| Location | Use Case |
|----------|----------|
| `action.yml` (repo root) | Published action in dedicated repository |
| `.github/actions/<name>/action.yml` | Private action within a repository |

## Workflow

- [ ] Create `action.yml` in repo root or `.github/actions/<name>/`
- [ ] Set `name`, `description`, and `runs.using: "composite"`
- [ ] Define inputs with descriptions (mark required ones)
- [ ] Define outputs referencing step outputs
- [ ] Add steps with explicit `shell` for all `run` commands
- [ ] Pin ALL external actions to full commit SHAs (no exceptions)
- [ ] Use environment variables for untrusted input
- [ ] Validate inputs at action start
- [ ] Document required permissions in README
