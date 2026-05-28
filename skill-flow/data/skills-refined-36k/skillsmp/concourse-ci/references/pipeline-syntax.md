# Concourse CI Pipeline Syntax Reference

Complete YAML schema reference for Concourse CI pipelines.

## Pipeline Root Schema

```yaml
# Required
jobs: []  # At least one job required

# Optional
resources: []           # External versioned artifacts
resource_types: []      # Custom resource type definitions
var_sources: []         # Variable sources (Vault, SSM, etc.)
groups: []              # UI organization
display:                # Visual customization
  background_image: ""
  background_filter: "opacity(30%) grayscale(100%)"
```

## Resource Schema

```yaml
resources:
- name: resource-name        # Required: identifier
  type: git                  # Required: resource type
  source: {}                 # Required: type-specific config

  # Optional
  old_name: previous-name    # Rename while preserving history
  icon: gitlab               # Material Design icon name
  version: { ref: abc123 }   # Pin specific version
  check_every: 1m            # Check interval (default: 1m)
  check_timeout: 1h          # Check timeout (default: 1h)
  tags: [private-network]    # Worker selection tags
  public: false              # Expose metadata publicly
  webhook_token: secret      # Webhook trigger token
  expose_build_created_by: false
```

## Resource Type Schema

```yaml
resource_types:
- name: slack-notification   # Required: identifier
  type: registry-image       # Required: image source type
  source:                    # Required: image location
    repository: cfcommunity/slack-notification-resource
    tag: latest

  # Optional
  privileged: false          # Run with full capabilities
  params: {}                 # Default get params
  check_every: 1m            # Version check interval
  tags: []                   # Worker selection tags
  defaults: {}               # Default source config
```

## Job Schema

```yaml
jobs:
- name: job-name             # Required: identifier
  plan: []                   # Required: steps to execute (alias: steps)

  # Optional
  old_name: previous-name    # Rename preserving history
  serial: false              # Sequential execution only
  serial_groups: []          # Serialize jobs sharing groups
  max_in_flight: 1           # Max concurrent builds
  public: false              # Public build logs
  disable_manual_trigger: false
  interruptible: false       # Allow worker shutdown

  # Build log retention
  build_log_retention:
    days: 30                 # Keep builds from last N days
    builds: 100              # Keep last N builds
    minimum_succeeded_builds: 1

  # Lifecycle hooks
  on_success: { step }       # Run on success
  on_failure: { step }       # Run on failure
  on_error: { step }         # Run on error
  on_abort: { step }         # Run on abort
  ensure: { step }           # Always run
```

## Step Types

### Get Step

```yaml
- get: resource-name         # Resource to fetch

  # Optional
  resource: actual-resource  # Override resource name
  version: latest            # Version selection: latest, every, { ref: x }
  passed: [job1, job2]       # Only versions passing these jobs
  params: {}                 # Resource-specific get params
  trigger: false             # Auto-trigger on new versions
  tags: []                   # Worker selection
  timeout: 1h                # Step timeout
  attempts: 1                # Retry count

  # Hooks
  on_success: { step }
  on_failure: { step }
  on_error: { step }
  on_abort: { step }
  ensure: { step }
```

### Put Step

```yaml
- put: resource-name         # Resource to update

  # Optional
  resource: actual-resource  # Override resource name
  inputs: detect             # Input artifacts: detect, all, [list]
  params: {}                 # Resource-specific put params
  get_params: {}             # Implicit get params
  no_get: false              # Skip implicit get after put
  tags: []                   # Worker selection
  timeout: 1h
  attempts: 1

  # Hooks
  on_success: { step }
  on_failure: { step }
  on_error: { step }
  on_abort: { step }
  ensure: { step }
```

### Task Step

```yaml
- task: task-name            # Required: task identifier

  # Config source (choose one)
  config: { task-config }    # Inline configuration
  file: path/to/task.yml     # File from input artifact

  # Optional
  image: input-name          # Use input artifact as image
  privileged: false          # Run as root
  vars: {}                   # Static variables for config
  params: {}                 # Environment variables
  input_mapping:             # Rename inputs
    task-input: get-name
  output_mapping:            # Rename outputs
    task-output: result
  tags: []
  timeout: 1h
  attempts: 1
  container_limits:
    cpu: 1024                # CPU shares
    memory: 1073741824       # Memory in bytes

  # Hooks
  on_success: { step }
  on_failure: { step }
  on_error: { step }
  on_abort: { step }
  ensure: { step }
```

### Task Configuration Schema

```yaml
platform: linux              # Required: linux, darwin, windows

# Image (required for linux)
image_resource:
  type: registry-image
  source:
    repository: alpine
    tag: latest
  params: {}
  version: {}

# Private registry example
image_resource:
  type: registry-image
  source:
    repository: registry.example.com/org/build-tools
    username: ((registry.user))
    password: ((registry.pass))
    tag: "1.2.3"

# OR use docker-image type (legacy)
image_resource:
  type: docker-image
  source:
    repository: registry.example.com/org/build-tools
    username: ((registry.user))
    password: ((registry.pass))

# OR use rootfs_uri for pre-uploaded images
rootfs_uri: /path/to/rootfs

inputs:
- name: input-name           # Required
  path: custom-path          # Optional: override directory name
  optional: false            # Allow missing input

outputs:
- name: output-name
  path: custom-path

caches:
- path: node_modules         # Persistent across runs

params:
  ENV_VAR: value             # Environment variables
  SECRET: ((vault:secret))   # From credential manager

run:
  path: /bin/bash            # Required: executable
  args: [-c, "echo hello"]   # Command arguments
  dir: input-name            # Working directory
  user: root                 # Execution user

container_limits:
  cpu: 1024
  memory: 1073741824
```

### Set Pipeline Step

```yaml
- set_pipeline: pipeline-name
  file: config/pipeline.yml  # Required: config file

  # Optional
  vars: {}                   # Variables to pass
  var_files: []              # Variable files
  instance_vars: {}          # Instance pipeline variables
  team: other-team           # Target team (default: current)
```

### Load Var Step

```yaml
- load_var: var-name
  file: path/to/file         # Required: file with value

  # Optional
  format: json               # json, yaml, trim, raw
  reveal: false              # Show in UI (false redacts)
```

### In Parallel Step

```yaml
- in_parallel:
    steps:                   # Required: steps to parallelize
    - get: resource-a
    - get: resource-b
    - task: parallel-work

    # Optional
    limit: 3                 # Max concurrent steps
    fail_fast: false         # Abort remaining on first failure
```

### Do Step

```yaml
- do:                        # Sequential step sequence
  - get: resource
  - task: step1
  - task: step2
```

### Try Step

```yaml
- try:                       # Continue regardless of outcome
    task: optional-step
```

### Across Step Modifier

```yaml
- task: deploy
  across:
  - var: region
    values: [us-east, us-west, eu-west]
  - var: env
    values: [staging, prod]
    max_in_flight: 1         # Serial across this dimension
  file: ci/tasks/deploy.yml
  vars:
    region: ((.:region))
    environment: ((.:env))
```

## Step Modifiers

Apply to any step:

```yaml
- task: example
  timeout: 30m               # Step timeout
  attempts: 3                # Retry on failure
  tags: [specialized]        # Worker selection

  # Hooks run after step
  on_success: { put: notify }
  on_failure: { put: alert }
  on_error: { put: page }
  on_abort: { put: cleanup }
  ensure: { task: always-run }
```

## Groups Schema

```yaml
groups:
- name: group-name           # Required
  jobs:                      # Required: job references
  - job-name
  - deploy-*                 # Glob patterns
  - terraform-{dev,prod}     # Brace expansion
```

## Var Sources Schema

```yaml
var_sources:
- name: vault
  type: vault
  config:
    url: https://vault.example.com
    path_prefix: /concourse
    auth_backend: token
    auth_params:
      token: ((VAULT_TOKEN))

- name: ssm
  type: ssm
  config:
    region: us-east-1

- name: secrets-manager
  type: secretsmanager
  config:
    region: us-east-1
```

## Display Schema

```yaml
display:
  background_image: https://example.com/bg.png
  background_filter: "blur(5px) brightness(0.5)"
```

## Variable Syntax Reference

```yaml
# Basic var
((var-name))

# Var with source
((source:path))

# Var with field
((source:path.field))

# Local var (from load_var)
((.:local-var))

# Nested field access
((vault:secret/app.data.password))
```

## YAML Anchor Patterns

```yaml
# Define anchor
common-config: &common
  username: ((git.user))
  password: ((git.pass))

# Reference anchor
resources:
- name: repo
  source:
    <<: *common
    uri: https://github.com/org/repo

# Anchor with override
- name: other-repo
  source:
    <<: *common
    uri: https://github.com/org/other
    branch: develop  # Override common setting
```

## Identifier Rules

Pipeline, job, resource, and resource type names must:
- Start with a lowercase letter
- Contain only lowercase letters, numbers, hyphens, periods, underscores
- Cannot be purely numeric
- Cannot contain consecutive special characters

Valid: `my-pipeline`, `build_v2`, `deploy.prod`
Invalid: `My-Pipeline`, `123`, `build--test`
