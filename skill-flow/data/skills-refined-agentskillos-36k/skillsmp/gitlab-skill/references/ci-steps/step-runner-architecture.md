# Step Runner Architecture

Step Runner implements GitLab Steps RFC through Protocol Buffer-based CI/CD step execution engine. The architecture provides deterministic, composable step execution with expression-based interpolation and multi-protocol step loading.

## Architectural Components

### Protocol Buffer Core

Step Runner utilizes Protocol Buffers as the fundamental data model. The `proto/step.proto` defines all execution structures.

Source: <https://gitlab.com/gitlab-org/step-runner/-/raw/main/proto/step.proto?ref_type=heads>

#### Message Structures

```text
Step                    - Single step invocation containing name, reference, env, inputs
Step.Reference         - Multi-protocol step locator with url, path, version, registry
StepResult             - Execution result with status, outputs, exports, exec details
SpecDefinition         - Spec and definition pair from step.yml files
Definition             - Implementation via exec/steps/function types
Spec                   - Interface contract defining inputs/outputs with types
StepRunner service     - gRPC service for Run, Close, FollowLogs, Status operations
```

#### Value Type System

```text
ValueType enum:
- string  (2)
- number  (3)
- boolean (4)
- struct  (5)
- array   (6)
```

Inputs support typed defaults. Outputs produce string-only values via key=value format written to STEP_RUNNER_OUTPUT.

#### Step Reference Protocols

```text
StepReferenceProtocol enum:
- local      (1) - Filesystem relative paths
- git        (2) - Git repository URLs
- zip        (3) - Archive files
- oci        (4) - OCI container images
- dist       (5) - Bundled distribution steps
- dynamic    (6) - Runtime resolution
- spec_def   (7) - Inline definitions
- function   (8) - Built-in functions
```

### Command Architecture

Entry point hierarchy via Cobra commands:

```text
cmd/root.go           - Base command initialization
cmd/ci/ci.go          - CI environment execution (STEPS variable)
cmd/run/run.go        - Direct step execution
cmd/serve/serve.go    - gRPC server mode
cmd/proxy/proxy.go    - Proxy server for remote execution
cmd/bootstrap/bootstrap.go - Bootstrap operations
```

Source: <https://gitlab.com/gitlab-org/step-runner/-/raw/main/cmd/ci/ci.go?ref_type=heads>

The `ci` command implements GitLab CI integration:

1. Reads STEPS environment variable
2. Wraps steps in SpecDefinition
3. Initializes dependency injection container
4. Creates GlobalContext with CI variables
5. Parses step through StepParser
6. Executes via StepsContext
7. Writes step-results.json artifact

### Runner Package Architecture

Core execution engine in `pkg/runner/`:

#### Execution Components

```text
runner.go             - Base types: Params, input defaults
executable_step.go    - Command execution via exec.CommandContext
sequence_of_steps.go  - Sequential step composition
lazily_loaded_step.go - Deferred step loading
step_parser.go        - Step parsing and validation
```

#### Context Management

```text
global_context.go     - Job-level context with workdir, variables, stdout/stderr
steps_context.go      - Step-level context with env, inputs, outputs
environment.go        - Environment variable management with lexical scoping
global_env.go         - CI/GITLAB/DOCKER variable extraction
```

#### Resource Loading

```text
step_resource_parser.go    - Protocol-based resource resolution
file_system_step_resource.go - Local filesystem steps
git_step_resource.go       - Git repository steps
dist_step_resource.go      - Bundled distribution steps
dynamic_step_resource.go   - Runtime-resolved steps
function_step_resource.go  - Built-in function steps
fixed_step_resource.go     - Inline spec_def steps
```

Source: <https://gitlab.com/gitlab-org/step-runner/-/raw/main/pkg/runner/step_resource_parser.go?ref_type=heads>

### Expression System

Expression evaluation via `pkg/internal/expression/`:

```text
expression.go         - Core evaluation engine
interpolation.go      - String interpolation with ${{ }} syntax
interpolation_context.go - Context object for expression evaluation
value_type.go         - Type system implementation
```

Expression syntax supports:

- Dot notation for nested access: `inputs.foo.bar`
- Environment variables: `env.VAR_NAME`
- Step outputs: `steps.step-name.outputs.key`
- Step exports: `steps.step-name.exports.VAR`
- Context variables: `job`, `work_dir`, `step_dir`

Source: <https://gitlab.com/gitlab-org/step-runner/-/raw/main/pkg/internal/expression/expression.go?ref_type=heads>

### Dependency Injection

DI container in `pkg/di/` manages component lifecycle:

```text
container.go - Service registration and resolution
```

Components registered:

- StepParser
- GitFetcher
- DistFetcher
- StepFunctionRepository

### Step Execution Flow

#### Phase 1: Initialization

1. Parse step reference protocol
2. Load step resource via appropriate loader
3. Read step.yml containing spec and definition
4. Validate inputs against spec

#### Phase 2: Context Preparation

1. Create StepsContext from GlobalContext
2. Apply lexical environment scoping
3. Initialize output/export file paths
4. Set working directory

#### Phase 3: Execution

For exec steps:

1. Expand expressions in command arguments
2. Expand working directory expression
3. Execute via exec.CommandContext
4. Capture exit code

For steps type:

1. Iterate sub-steps sequentially
2. Pass outputs between steps
3. Accumulate exports to environment

#### Phase 4: Result Processing

1. Read outputs from STEP_RUNNER_OUTPUT file
2. Read exports from STEP_RUNNER_ENV file
3. Build StepResult with status, outputs, exports
4. Update global environment with exports

### Distribution Steps

Built-in steps in `dist/steps/`:

```text
script/              - Script execution step
step/oci/            - OCI image operations (build, fetch, promote)
```

OCI step architecture:

- Authentication via keychain lookup
- Multi-platform image support
- Cache layer management
- Remote registry operations

Source: <https://gitlab.com/gitlab-org/step-runner/-/raw/main/dist/steps/step/oci/cmd/build/main.go?ref_type=heads>

### Schema Package

YAML schema validation in `schema/v1/`:

- Syntactic sugar processing
- YAML to Proto conversion
- Schema validation

### Cache Package

Caching implementations in `pkg/cache/`:

```text
git/     - Git repository caching
dist/    - Distribution step caching
```

### Report Package

Result reporting in `pkg/report/`:

- JSON format output
- step-results.json generation
- Status aggregation

## Integration Points

### GitLab Runner Integration

Runner injects step-runner via:

1. Feature flag: FF_USE_NATIVE_STEPS
2. Docker executor support
3. Automatic platform selection
4. Container image: registry.gitlab.com/gitlab-org/step-runner:v0

### CI Variable Access

Restricted to prefixed variables:

- CI\_\*
- GITLAB\_\*
- DOCKER\_\*

Access via `job` context in expressions.

### File System Conventions

```text
STEP_RUNNER_OUTPUT   - Output key=value pairs
STEP_RUNNER_ENV      - Export key=value pairs
CI_PROJECT_DIR       - Default working directory
step.yml             - Step definition file
step-results.json    - Execution results artifact
```

## Design Principles

### Deterministic Execution

- Protocol Buffer serialization ensures consistent data structures
- Expression evaluation produces predictable results
- Exit codes captured for exec steps
- Sequential step execution order guaranteed

### Composability

- Steps compose through inputs/outputs
- Environment variables propagate through exports
- Nested step definitions via steps type
- Protocol abstraction enables multiple sources

### Isolation

- Each step maintains separate context
- Lexical environment scoping
- Working directory isolation
- Output/export file separation

### Extensibility

- Protocol-based step loading supports new sources
- Function steps enable custom logic
- DI container allows component replacement
- gRPC service enables remote execution

## Error Handling

Step Runner implements error propagation:

1. Expression evaluation errors terminate step
2. Exec failures return exit code in StepResult
3. Resource loading errors prevent execution
4. Context errors bubble to job level
5. Validation errors fail fast

## Performance Characteristics

- Lazy step loading reduces memory usage
- Git caching minimizes network operations
- Parallel capability via gRPC service
- Container reuse through Docker executor

## Security Considerations

- HTTPS required for remote steps
- Sensitive input/output marking
- Restricted CI variable access
- Container isolation for execution
- No shell expansion in exec commands

## See Also

- [Steps Overview and Core Concepts](./steps-overview.md)
- [Usage Examples and Patterns](./examples.md)
- GitLab Steps Blueprint: <https://docs.gitlab.com/ee/architecture/blueprints/gitlab_steps/>
- Step Runner Repository: <https://gitlab.com/gitlab-org/step-runner>
