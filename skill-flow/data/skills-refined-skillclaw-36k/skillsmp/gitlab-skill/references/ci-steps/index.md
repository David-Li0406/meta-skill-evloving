# GitLab CI/CD Steps Reference

Navigation hub for GitLab CI/CD Steps documentation. Steps are reusable job-level units composed with the `run` keyword, replacing traditional `script`/`before_script`/`after_script` patterns.

## Feature Overview

CI/CD Steps enable job composition through reusable, independently testable units with explicit input/output contracts. Steps run in Docker containers, execute commands, sequence other steps, or invoke GitHub Actions. Currently Linux-only (Windows/macOS support pending per epic 15074).

Access CI/CD Steps documentation:

- [Steps Overview and Core Concepts](./steps-overview.md) - Feature capabilities, limitations, workflow execution model
- [Usage Examples and Patterns](./examples.md) - Real-world step composition patterns with runnable YAML
- [Step Runner Architecture](./step-runner-architecture.md) - Internal architecture, execution engine, Protocol Buffer model

## Core Concepts

### Step Types

Step definitions support three execution modes:

1. Command execution (`exec` keyword) - Run commands in bash/sh with optional working directory
2. Step sequencing (`run` keyword) - Compose other steps with input/output chaining
3. GitHub Actions (`action` keyword) - Execute actions directly (requires `dind` service)

### Step Locations

Steps load from three sources:

1. File system - Relative paths starting with `.` (forward slashes required)
2. Git repositories - GitLab.com or external Git sources with branch/tag/commit specifications
3. Expanded syntax - Specify custom directory and filename outside default `steps` folder

### Expressions

Mini-language enclosed in `${{ }}` evaluated at step execution. Access: `env`, `inputs`, `job` (CI*/DOCKER*/GITLAB\_ prefixed only), `steps.*.outputs`, `step_dir`, `work_dir`, `output_file`, `export_file`.

Distinguished from components which use `$[[ ]]` (evaluated at pipeline creation).

### Constraints

- Cannot combine `run` with `script`, `before_script`, or `after_script`
- Actions cannot directly upload artifacts; use filesystem/cache
- Limited CI/CD variable access (CI*, DOCKER*, GITLAB\_ prefixed only)
- Container environment isolation in development
- HTTPS certificate validation required for remote steps

## Step Composition Model

Jobs using `run` keyword execute steps sequentially. Each step defines:

- Inputs - Optional typed parameters (string, number, boolean, array, struct)
- Outputs - Optional typed return values
- Environment - Variables accessible to execution or sub-steps
- Execution - Command, step sequence, or action

Output chaining: `${{steps.step_name.outputs.variable}}` enables downstream dependencies.

Environment precedence (highest to lowest):

1. `step.yml` `env` keyword
2. Passed `env` keyword
3. Sequence-level `env` keyword
4. Previously exported variables (via `${{export_file}}`)
5. Runner environment
6. Container environment

## Creating Custom Steps

Steps require `step.yml` containing two YAML documents:

Document 1 (Specification): Defines inputs/outputs types and defaults Document 2 (Definition): Specifies `exec`, `env`, or `run` implementation

Output delegation: `outputs: delegate` in spec returns all sub-step outputs.

## Status and Tracking

- Experimental status: Available across Free, Premium, Ultimate tiers on GitLab.com, Self-Managed, Dedicated
- Runner requirement: GitLab Runner 17.11+ for Docker executor
- Future capability tracking:
  - Multi-OS support: [epic 15074](https://gitlab.com/groups/gitlab-org/-/epics/15074)
  - Full environment access: [epic 15073](https://gitlab.com/groups/gitlab-org/-/epics/15073)
  - Job environment execution: [epic 15073](https://gitlab.com/groups/gitlab-org/-/epics/15073)

## Source Documentation

Official GitLab CI/CD Steps documentation: <https://docs.gitlab.com/ci/steps/>

YAML syntax reference: <https://docs.gitlab.com/ci/yaml/#run>
