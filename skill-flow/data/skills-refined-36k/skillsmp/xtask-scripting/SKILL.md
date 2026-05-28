---
name: xtask-scripting
description: Standards for writing development scripts using the cargo-xtask pattern with xshell.
---
# Xtask API Textbook

## 0. Scope

This document specifies:

1. The **Cargo integration contract** for `cargo xtask` (the `cargo-xtask` pattern).
2. The **binary interface contract** for an `xtask` crate used as a project-local command runner.
3. An **execution framework API** suitable for developer scripts with:

   * streaming output/events,
   * cooperative cancellation,
   * checkpoints,
   * rollback (compensation).

The term “API” here includes both:

* the **Cargo-facing invocation surface** (alias + arguments), and
* the **internal Rust API** used to implement tasks and compositions.

---

## 1. Cargo Integration Contract

### 1.1. Definition

`cargo xtask` is implemented via a Cargo **alias** that expands to a `cargo run ...` invocation of a workspace binary crate named `xtask`. ([GitHub][1])

`cargo-xtask` is explicitly described as a configuration-based method to extend stable Cargo with project-local commands (“xtasks”), and it is not a Cargo built-in feature. ([GitHub][1])

### 1.2. Repository layout

The canonical layout is:

* Workspace root contains:

  * `Cargo.toml` (workspace manifest)
  * `.cargo/config.toml` (alias)
  * `xtask/` (binary crate)
  * other workspace members

Example directory layout and the requirement to commit both `.cargo/config.toml` and the `xtask` directory are stated in the `cargo-xtask` specification. ([GitHub][1])

### 1.3. Alias definition (minimal)

Minimal alias:

```toml
# .cargo/config.toml
[alias]
xtask = "run --package xtask --"
```

This is the alias shown in the `cargo-xtask` specification. ([GitHub][1])

### 1.4. Alias definition (isolated target dir)

An alternative alias variant configures a dedicated target directory for xtask builds:

```toml
# .cargo/config.toml
[alias]
xtask = "run --target-dir target/xtask --package xtask --bin xtask --"
```

This form is used/documented by the `tracel-ai/xtask` project. ([GitHub][2])

### 1.5. Config discovery and placement constraints

Cargo discovers configuration files by searching the current directory and parent directories for `.cargo/config.toml` (and legacy `.cargo/config`). ([Rust Documentation][3])

When invoked from a workspace root, Cargo does not read `.cargo/config.toml` files from crates within the workspace; therefore, the alias is placed at the workspace root. ([Rust Documentation][3])

### 1.6. Invocation forms

Equivalent invocations (modulo alias config):

* Via alias:

  * `cargo xtask <args...>`

* Without alias:

  * `cargo run --package xtask -- <args...>`

The alias expands to `cargo run` against the `xtask` package. ([GitHub][1])

### 1.7. Limitations (Cargo lifecycle)

The pattern does not integrate with the Cargo lifecycle; you cannot intercept `cargo build` or add hooks into standard Cargo commands. The `cargo-xtask` specification states that post-processing requires a separate task such as `cargo xtask build` which internally calls `cargo build`. ([GitHub][1])

Xtasks are project-local and cannot be used as dependency-provided commands; sharing is possible only by publishing shared logic as crates. ([GitHub][1])

---

## 2. Xtask Binary Interface Contract

### 2.1. Binary identity

The `xtask` crate is a **binary crate** (typically `xtask/src/main.rs`) built and executed via Cargo alias. ([GitHub][1])

### 2.2. Argument contract

The `cargo-xtask` specification states:

* the `xtask` binary **expects at least one positional argument**: the task name, and
* tasks are implemented in Rust and may call arbitrary crates. ([GitHub][1])

In practice, most modern implementations use a subcommand-based CLI (e.g., via `clap`) rather than manual “first arg = task name” parsing. The spec states the current recommendation is to define tasks as subcommands of a single `xtask` binary. ([GitHub][1])

### 2.3. Task discovery / listing

A standard UX pattern is: `cargo xtask` with no subcommand prints a list of available tools/tasks and short descriptions.

OpenVMM documents this behavior explicitly (“Running `cargo xtask` will list what tools are available, along with brief descriptions”). ([OpenVMM][4])

### 2.4. Exit status contract

For a developer script runner:

* `0`: command succeeded.
* non-zero: command failed or was cancelled (cancellation is typically distinct if a machine consumer needs it).

If the tool produces a structured event stream (Section 5), exit status is redundant but still required for shell/CI semantics.

### 2.5. `cargo` execution contract

If tasks invoke Cargo internally, the `cargo-xtask` specification advises using the `CARGO` environment variable to locate the appropriate Cargo binary. ([GitHub][1])

---

## 3. Common Module Topologies in Real Xtask Crates

### 3.1. “Monolithic binary with modules”

Example: rust-analyzer’s `xtask` crate defines multiple modules (`codegen`, `dist`, `install`, `publish`, `release`, etc.) within a single binary. ([rust-lang.github.io][5])

This topology maps to a CLI with subcommands, each delegating to a module.

### 3.2. “Shared library + thin binary”

A reusable library provides operations and compositions; the `xtask` binary crate becomes:

* argument parsing,
* wiring of event sinks,
* construction of plans,
* engine execution.

`tracel-xtask` is an example of a reusable xtask-oriented library with macros for declaring commands and base command sets. ([GitHub][2])

---

## 4. Internal API: Minimal Primitive Set

This section defines a minimal API surface for implementing developer scripts in an `xtask` crate (or a sibling library crate).

### 4.1. Primitive: Workspace root resolution

**Requirement:** Resolve the workspace root deterministically.

* Source options:

  * `CARGO_MANIFEST_DIR` for the `xtask` crate, then `..` to workspace root (if xtask is at `<root>/xtask`).
  * A marker file strategy (`Cargo.toml` with `[workspace]`) when layout is not fixed.

**API shape:**

```rust
pub struct WorkspaceRoot(PathBuf);

pub fn workspace_root() -> WorkspaceRoot;
pub fn path_in_workspace(root: &WorkspaceRoot, rel: impl AsRef<Path>) -> PathBuf;
```

### 4.2. Primitive: Structured command execution (no shell)

**Requirement:** All external processes are spawned with explicit argv vectors (no shell parsing).

**API shape:**

```rust
pub struct ProcessSpec {
    pub program: OsString,
    pub args: Vec<OsString>,
    pub cwd: Option<PathBuf>,
    pub env: EnvPolicy,
    pub stdin: StdinPolicy,
}

pub enum EnvPolicy {
    Inherit,
    Clean { allowlist: Vec<OsString>, set: Vec<(OsString, OsString)> },
}

pub enum StdinPolicy { Inherit, Null, Piped(Vec<u8>) }

pub struct Exit {
    pub code: Option<i32>,
    pub signal: Option<i32>, // unix
}

pub trait ProcessRunner {
    fn spawn(&self, spec: ProcessSpec) -> Result<ChildHandle>;
}

pub trait ChildHandle {
    fn pid(&self) -> u32;
    fn kill(&mut self) -> Result<()>;
    fn wait(&mut self) -> Result<Exit>;
    fn stream(&mut self) -> Result<OutputStream>;
}
```

### 4.3. Primitive: Event emission

The execution engine emits a single event stream that can be rendered to:

* human console output, or
* machine-consumable NDJSON.

**API shape:**

```rust
pub enum Event {
    RunStart { run_id: String, argv: Vec<String> },
    StepStart { step_id: String, name: String },
    Output { step_id: String, stream: Stream, chunk: Vec<u8> },
    Progress { step_id: String, completed: u64, total: Option<u64>, unit: Option<String> },
    Checkpoint { step_id: String, checkpoint_id: String },
    StepEnd { step_id: String, status: StepStatus },
    RunEnd { run_id: String, status: RunStatus },
}

pub enum Stream { Stdout, Stderr }
pub enum StepStatus { Ok, Failed { message: String }, Cancelled }
pub enum RunStatus { Ok, Failed, Cancelled }

pub trait EventSink: Send + Sync {
    fn emit(&self, ev: Event);
}
```

### 4.4. Primitive: Cancellation token

Cancellation is cooperative. Cancellation is a first-class input to step execution and process execution.

**API shape:**

```rust
#[derive(Clone)]
pub struct CancellationToken { /* ... */ }

impl CancellationToken {
    pub fn cancel(&self);
    pub fn is_cancelled(&self) -> bool;
    pub fn checkpoint(&self) -> Result<(), Cancelled>; // returns Err if cancelled
}

pub struct Cancelled;
```

---

## 5. Plan/Step API (Checkpoints and Rollback)

### 5.1. Definitions

* **Plan**: an ordered or dependency-structured set of steps to execute.
* **Step**: an executable unit with defined side effects and compensation behavior.
* **Checkpoint**: a persistent record that a step completed, including rollback metadata.
* **Rollback**: compensation applied to restore invariants after partial execution, step failure, or cancellation.

### 5.2. Step interface (sync or async)

The interface is defined in terms of:

* `preflight`: reject early if requirements are not met.
* `execute`: perform effects; must emit events.
* `checkpoint`: persist checkpoint after successful execution.
* `rollback`: compensate effects if required.

**API shape (sync):**

```rust
pub trait Step {
    fn id(&self) -> &'static str;
    fn name(&self) -> &'static str;

    fn preflight(&self, ctx: &Context) -> Result<()>;

    fn execute(&self, ctx: &Context) -> Result<CheckpointRecord>;

    fn rollback(&self, ctx: &Context, ckpt: &CheckpointRecord) -> Result<()>;
}
```

**API shape (async):** (if using async runtime)

* Replace `execute` / `rollback` with `async fn` via `async_trait` or generic `Future`.

### 5.3. Context object

`Context` is the shared capability container.

```rust
pub struct Context<'a> {
    pub root: &'a WorkspaceRoot,
    pub events: &'a dyn EventSink,
    pub cancel: CancellationToken,
    pub runner: &'a dyn ProcessRunner,
    pub checkpoints: &'a dyn CheckpointStore,
    pub policy: RunPolicy,
}
```

### 5.4. Checkpoint persistence

Checkpoint store is append-only.

```rust
pub struct CheckpointRecord {
    pub step_id: String,
    pub checkpoint_id: String,
    pub data: serde_json::Value, // rollback metadata, artifact hashes, etc.
}

pub trait CheckpointStore {
    fn append(&self, run_id: &str, record: &CheckpointRecord) -> Result<()>;
    fn load(&self, run_id: &str) -> Result<Vec<CheckpointRecord>>;
}
```

Checkpoint file location is commonly under `target/` (or `target/xtask` if isolated). The alias variant `--target-dir target/xtask` provides a stable anchor directory for xtask-managed artifacts. ([GitHub][2])

### 5.5. Rollback policy

```rust
pub enum RollbackPolicy {
    Always,          // rollback on any failure or cancellation after first side effect
    OnFailureOnly,   // rollback on failure, but not on cancellation
    Never,           // no rollback attempt
}

pub struct RunPolicy {
    pub rollback: RollbackPolicy,
    pub dry_run: bool,
}
```

### 5.6. Engine execution algorithm (linear plan)

For an ordered plan:

1. Emit `RunStart`.
2. For each step:

   * emit `StepStart`
   * `preflight`
   * check cancellation
   * `execute`
   * append checkpoint
   * emit `Checkpoint`
   * emit `StepEnd(Ok)`
3. On step failure or cancellation:

   * emit `StepEnd(Failed|Cancelled)`
   * if rollback policy requires rollback:

     * rollback completed steps in reverse checkpoint order
4. Emit `RunEnd`.

---

## 6. Cancellation Semantics and Cancel-Safety Requirements

### 6.1. Cooperative cancellation boundary

Cancellation may occur at any time. Correctness requires that:

* The system either:

  * completes an effect and records a checkpoint, or
  * compensates the effect and records rollback outcome.

For async implementations, cancellation occurs when futures are dropped; cancel-safety constraints apply at `.await` points to avoid leaving shared state invalid. ([RFD][6])

### 6.2. Child process cancellation

A cancellable process runner implements escalation:

1. On cancellation request:

   * send a soft termination (e.g., SIGINT on Unix, CTRL_BREAK_EVENT if supported on Windows)
2. After grace period:

   * hard kill (SIGKILL / TerminateProcess)

All behavior is surfaced via events.

### 6.3. Drop behavior

If cancellation is implemented by dropping async tasks:

* the engine must still execute rollback or emit a durable “rollback required” record.
* cancellation must not rely on `Drop` of arbitrary types to complete async rollback (Rust does not support async drop on stable).

---

## 7. Streaming Output API (Agent-Compatible)

### 7.1. Output routing

The engine emits `Event::Output { stream, chunk }` events for:

* child process stdout/stderr
* engine-generated logs

Console mode renders events to terminal with stable prefixes.
Machine mode emits newline-delimited JSON (NDJSON).

### 7.2. NDJSON schema constraints

Requirements for machine consumers:

* One JSON object per line.
* Each object includes:

  * `type`: event variant name
  * `ts`: RFC3339 timestamp or monotonic time
  * `run_id`
  * `step_id` when applicable
* `Output.chunk` is either:

  * base64-encoded bytes, or
  * UTF-8 string with explicit encoding tag

The schema is versioned:

```json
{ "schema": "xtask.events.v1", "type": "StepStart", ... }
```

---

## 8. Useful Compositions of the API

This section specifies compositions as reusable higher-order steps.

### 8.1. Sequence (pipeline)

A pipeline is an ordered list of steps with rollback in reverse order.

```rust
pub struct Pipeline { steps: Vec<Box<dyn Step>> }
```

Execution semantics are identical to Section 5.6.

### 8.2. Conditional step

A conditional step executes only if predicate is true, and emits `Skipped` as a step end status.

```rust
pub struct When {
    pub predicate: Box<dyn Fn(&Context) -> Result<bool>>,
    pub step: Box<dyn Step>,
}
```

Rollback: if skipped, no rollback.

### 8.3. Group step (sub-plan)

A group step executes a nested plan and surfaces a single step id externally.

```rust
pub struct Group {
    pub id: &'static str,
    pub name: &'static str,
    pub plan: Pipeline,
}
```

Rollback: group rollback rolls back nested checkpoints within the group boundary.

### 8.4. Retry wrapper

Retry wraps a step and re-executes on failure.

```rust
pub struct Retry {
    pub attempts: u32,
    pub step: Box<dyn Step>,
    pub classify: fn(&anyhow::Error) -> RetryClass,
}
pub enum RetryClass { Retryable, Fatal }
```

Checkpoint semantics:

* A retried step must not append a checkpoint until it succeeds.
* On partial failure inside an attempt, the attempt performs internal cleanup before retry.

### 8.5. Parallel map (matrix execution)

A parallel map runs independent steps concurrently.

```rust
pub struct Parallel {
    pub max_concurrency: usize,
    pub steps: Vec<Box<dyn Step>>,
}
```

Constraints:

* Rollback for parallel steps requires a deterministic ordering of compensation (typically reverse completion time or declared ordering).
* Output events must include `step_id` to allow multiplexing.

### 8.6. Cacheable step (content-addressed)

A cacheable step declares inputs and outputs; it is skipped if inputs hash matches a prior checkpoint.

```rust
pub trait CacheableStep: Step {
    fn inputs(&self) -> Vec<PathBuf>;
    fn outputs(&self) -> Vec<PathBuf>;
}
```

Checkpoint data includes:

* input file hashes
* output file hashes
* tool version hash (Rust toolchain or xtask version)

---

## 9. Standard Task Shapes (Non-Standardized Names)

The `cargo-xtask` specification states there is no ecosystem-wide standard set of xtasks, though recurring patterns exist. ([GitHub][1])

This section defines shapes, not names.

### 9.1. Format/lint/test lane

Plan composition:

1. `PreflightToolchain`
2. `FmtCheck`
3. `Clippy`
4. `Tests`

Rollback: typically none (read-only), except for auto-fix commands which must checkpoint modified files and rollback via backups or VCS reset.

### 9.2. Distribution lane (“dist” shape)

Plan composition:

1. `CleanDistDir` (rollback: restore previous dist dir snapshot if any)
2. `BuildReleaseBinary` (rollback: delete produced artifacts)
3. `GenerateManpages` (rollback: delete generated docs)
4. `PackageArchive` (rollback: delete archive)

### 9.3. Release lane

Plan composition:

1. `VerifyCleanRepo` (preflight)
2. `BumpVersion` (rollback: revert file edits)
3. `TagCommit` (rollback: delete tag)
4. `PublishCrates` (rollback: may be non-reversible; requires explicit policy and durable audit events)

---

## 10. Security Constraints (Developer Script Runner)

### 10.1. Shell avoidance

All process execution is argument-vector based. No `sh -c`, no string interpolation into a shell.

### 10.2. Environment control

Use `EnvPolicy::Clean` for steps that:

* invoke network tools,
* run compilers with dynamic linking,
* interact with credentials.

Allowlist only required variables (including `CARGO` if used).

### 10.3. Path constraints

* Canonicalize workspace root.
* Reject operations outside workspace root unless explicitly enabled.
* Emit events on any out-of-root path access.

### 10.4. Secret handling

* Redaction occurs at event emission.
* No secrets in:

  * command-line echo logs,
  * checkpoint data,
  * error chains.

---

## 11. Integration Examples (Concrete Cargo-Facing API)

### 11.1. Minimal alias + workspace

From `cargo-xtask` specification:

* `.cargo/config.toml` contains `[alias] xtask = "run --package xtask --"`.
* `xtask/` is committed.
* Workspace includes `xtask` as a member. ([GitHub][1])

### 11.2. Behavior contract for `cargo xtask` with no args

In OpenVMM, running `cargo xtask` lists available tools with brief descriptions. ([OpenVMM][4])

### 11.3. Example of subcommand-oriented implementation

The `cargo-xtask` specification explicitly recommends implementing tasks as subcommands of a single `xtask` binary. ([GitHub][1])

---

## 12. Reference: Pattern Positioning in the Rust Ecosystem

* `cargo-xtask` is described as:

  * free-form automation,
  * bootstrapped from `cargo` and `rustc`,
  * cross-platform relative to shell scripting,
  * a specification of configuration rather than a code dependency. ([GitHub][1])

* Large workspace guidance explicitly references the xtask pattern as a mechanism to consolidate automation in Rust in a dedicated crate. ([matklad.github.io][7])

* rust-analyzer documents that its `xtask` binary is integrated into Cargo via alias and houses commands not expressible with stock Cargo alone. ([rust-lang.github.io][5])

[1]: https://github.com/matklad/cargo-xtask "GitHub - matklad/cargo-xtask"
[2]: https://github.com/tracel-ai/xtask "GitHub - tracel-ai/xtask: Reusable and Extensible xtask commands to manage repositories."
[3]: https://doc.rust-lang.org/cargo/reference/config.html "Configuration - The Cargo Book"
[4]: https://openvmm.dev/guide/dev_guide/dev_tools/xtask.html "cargo xtask - The OpenVMM Guide"
[5]: https://rust-lang.github.io/rust-analyzer/xtask/index.html "xtask - Rust"
[6]: https://rfd.shared.oxide.computer/rfd/400?utm_source=chatgpt.com "RFD 400 Dealing with cancel safety in async Rust"
[7]: https://matklad.github.io/2021/08/22/large-rust-workspaces.html "Large Rust Workspaces"
