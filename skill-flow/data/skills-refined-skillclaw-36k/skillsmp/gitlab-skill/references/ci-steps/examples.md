# GitLab CI/CD Steps: Usage Examples and Patterns

Real-world step composition patterns extracted from official GitLab documentation.

Source: <https://docs.gitlab.com/ci/steps/>

## Basic Step Execution

### Echo Step with Input Interpolation

```yaml
job:
  variables:
    CI_SAY_HI_TO: "Sally"
  run:
    - name: say_hi
      step: gitlab.com/gitlab-org/ci-cd/runner-tools/echo-step@v1.0.0
      inputs:
        message: "hello, ${{job.CI_SAY_HI_TO}}"
```

Behavior: Prints "hello, Sally" to job log. Demonstrates expression evaluation from CI/CD variables.

### Script Step with Expression

```yaml
my_job:
  run:
    - name: say_hi
      script: echo hello ${{job.GITLAB_USER_LOGIN}}
```

Behavior: Executes bash script with interpolated GitLab user login variable.

## Step Location Patterns

### File System Reference

```yaml
job:
  run:
    - name: my_step
      step: ./path/to/my-step
```

Directory structure requirement: `./path/to/my-step/step.yml` must exist.

### Git Repository with Branch

```yaml
job:
  run:
    - name: specifying_a_branch
      step: gitlab.com/components/echo@main
```

Loads `steps/step.yml` from `main` branch of repository.

### Git Repository with Tag

```yaml
job:
  run:
    - name: specifying_a_tag
      step: gitlab.com/components/echo@v1.0.0
```

Loads from specific version tag.

### Git Repository with Commit

```yaml
job:
  run:
    - name: specifying_a_commit
      step: gitlab.com/components/echo/-/reverse/my-step.yml@3c63f399ace12061db4b8b9a29f522f41a3d7f25
```

Loads from specific commit hash.

### Expanded Git Syntax with Custom Directory

```yaml
job:
  run:
    - name: custom_location
      step:
        git:
          url: gitlab.com/components/echo
          rev: main
          dir: my-steps/sub-directory
          file: my-step.yml
```

Loads `my-steps/sub-directory/my-step.yml` from repository.

## Environment Variables

### Passing Environment Variables to Step

```yaml
job:
  variables:
    CI_SAY_HI_TO: "Sally"
  run:
    - name: say_hi
      step: gitlab.com/components/echo@v1.0.0
      env:
        USER: "Fred"
      inputs:
        message: "hello ${{job.CI_SAY_HI_TO}}"
```

Behavior: Echo step receives both environment variable USER and input message.

### Sequence-Level Environment Variables

```yaml
job:
  run:
    - env:
        FIRST_NAME: Sally
        LAST_NAME: Seashells
    - name: install_go
      step: ./go-steps/install-go
    - name: format_code
      step: ./go-steps/go-fmt
```

Both steps have access to FIRST_NAME and LAST_NAME variables.

## Output Chaining

### Using Prior Step Outputs

```yaml
job:
  run:
    - name: generate_rand
      step: gitlab.com/components/random-string
    - name: echo_random
      step: gitlab.com/components/echo
      inputs:
        message: "The random value is: ${{steps.generate_rand.outputs.random_value}}"
```

Behavior: Second step receives output from first step via expression.

### Returning Output from Sequence

```yaml
job:
  run:
    - name: install_java
      step: ./common/install-java
  outputs:
    java_version: "${{steps.install_java.outputs.java_version}}"
```

Behavior: Job returns `java_version` output from install_java step.

## Step Definition Patterns

### Command Execution Step

```yaml
spec:
  inputs:
    message:
      type: string
---
exec:
  command:
    - bash
    - -c
    - echo '${{inputs.message}}'
```

Executes bash command with input parameter.

### Command Execution with Working Directory

```yaml
spec:
---
exec:
  work_dir: ${{step_dir}}
  command:
    - bash
    - -c
    - "echo ${PWD}"
```

Prints step directory to log.

### Environment Variable Export from Executable

```yaml
spec:
---
exec:
  command:
    - bash
    - -c
    - echo '{"name":"GOPATH","value":"/go"}' >${{export_file}}
```

Behavior: Sets GOPATH environment variable for subsequent steps.

### Output Return from Executable

```yaml
spec:
  outputs:
    car:
      type: string
---
exec:
  command:
    - bash
    - -c
    - echo '{"name":"car","value":"Range Rover"}' >${{output_file}}
```

Behavior: Returns structured output value.

### Step Sequencing with Input Passing

```yaml
spec:
  inputs:
    code_path:
      type: string
---
run:
  - name: install_go
    step: ./go-steps/install-go
    inputs:
      version: "1.22"
  - name: format_go_code
    step: ./go-steps/go-fmt
    inputs:
      code_path: ${{inputs.code_path}}
```

Behavior: First step installs Go, second step uses Go binary and receives input parameter.

### Delegated Output from Sequence

```yaml
spec:
  outputs: delegate
---
run:
  - name: install_java
    step: ./common/install-java
    delegate: install_java
```

Behavior: All outputs from install_java step returned by parent step.

## Compound Input/Output Types

### Array Input Type

```yaml
spec:
  inputs:
    items:
      type: array
---
run:
  - name: process
    step: ./processor
    inputs:
      items: ["a", "b", "c"]
```

### Struct Input Type

```yaml
spec:
  inputs:
    config:
      type: struct
---
run:
  - name: deploy
    step: ./deploy
    inputs:
      config:
        host: "example.com"
        port: 8080
        ssl: true
```

### Number Output Type

```yaml
spec:
  outputs:
    count:
      type: number
---
exec:
  command:
    - bash
    - -c
    - echo '{"name":"count","value":42}' >${{output_file}}
```

## GitHub Actions Integration

### Using yq Action

```yaml
my_job:
  run:
    - name: say_hi_again
      action: mikefarah/yq@master
      inputs:
        cmd: echo ["hi ${{job.GITLAB_USER_LOGIN}} again!"] | yq .[0]
```

Requires `dind` service for Docker-in-Docker capability.

## Certificate Handling

### Installing Certificates Before Step Fetch

```yaml
ubuntu_job:
  image: ubuntu:24.04
  run:
    - name: install_certs
      script: apt update && apt install --assume-yes --no-install-recommends ca-certificates
    - name: echo_step
      step: https://gitlab.com/user/my_steps/hello_world@main
```

Behavior: First script step installs CA certificates, enabling second step to fetch via HTTPS.

## Components and Steps Integration

### Component Using Steps Internally

`.gitlab-ci.yml`:

```yaml
include:
  - component: gitlab.com/my-components/go@main
    inputs:
      fmt_packages: "./..."
```

Component template (`templates/go.yml`):

```yaml
spec:
  inputs:
    fmt_packages:
      description: Go packages to format
    go_version:
      default: "1.22"
---
format_code:
  run:
    - name: install_go
      step: ./languages/go/install
      inputs:
        version: $[[ inputs.go_version ]]
    - name: format_code
      step: ./languages/go/go-fmt
      inputs:
        go_binary: ${{ steps.install_go.outputs.go_binary }}
        fmt_packages: $[[ inputs.fmt_packages ]]
```

Behavior: Component (square bracket expressions) uses steps (brace expressions) internally.

## Input/Output Default Values

### Optional Input with Default

```yaml
spec:
  inputs:
    greeting:
      type: string
      default: "hello, world"
---
exec:
  command:
    - bash
    - -c
    - echo '${{inputs.greeting}}'
```

Behavior: Uses "hello, world" if not provided when calling step.

### Output with Default

```yaml
spec:
  outputs:
    result:
      type: string
      default: "no_result"
---
exec:
  command:
    - bash
    - -c
    - exit 0 # doesn't write output
```

Behavior: Returns "no_result" if step doesn't write output.

## Multi-Step Composition

### Complex Workflow: Build, Test, Deploy

```yaml
ci_job:
  run:
    - name: checkout
      step: ./steps/git-checkout
      inputs:
        ref: ${{job.CI_COMMIT_SHA}}
    - name: build
      step: gitlab.com/components/docker-build@v1
      inputs:
        image: my-app
        dockerfile: ./Dockerfile
      env:
        REGISTRY: registry.example.com
    - name: run_tests
      step: ./steps/test-runner
      inputs:
        test_command: "npm test"
      env:
        NODE_ENV: test
    - name: deploy
      step: ./steps/deploy
      inputs:
        environment: production
        image: ${{steps.build.outputs.image_sha}}
```

Behavior: Sequential steps for build pipeline with output chaining from build to deploy.

## Real Repository Step Examples

### gitlab.com/components/echo

Standard echo step hosted on GitLab.com:

```yaml
spec:
  inputs:
    message:
      type: string
---
exec:
  command:
    - bash
    - -c
    - echo '${{inputs.message}}'
```

### Custom Local Step Structure

Directory structure for `./my-step`:

```text
./my-step/
├── step.yml
├── script.sh
├── lib/
│   └── helper.sh
└── data/
    └── config.json
```

All files in directory available to step during execution via `${{step_dir}}`.
