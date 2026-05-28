---
name: claude-code-cli
description: CLI reference for Claude Code command-line interface. Use when you need help with Claude Code commands, flags, or CLI usage.
user-invocable: true
disable-model-invocation: false
---

# Codex CLI Integration Textbook (Ubuntu 24.04)

Procedural API Reference for Deep Tool Integration and Edge-Case Coverage
Scope: Codex CLI as shipped in the `openai/codex` repository snapshot provided (Rust core + Node distribution wrapper).
Normative terms: **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**.

---

## 0. Contract Baseline

### 0.1 What “integration” means in this text

An “integrator” is any program, agent, IDE, CI system, daemon, or automation that:

* Launches Codex as a subprocess (interactive or non-interactive).
* Consumes Codex outputs (human text or JSONL).
* Provides inputs (prompt text, images, schemas).
* Controls configuration, sandboxing, and policy.
* Optionally runs Codex as a JSON-RPC service (app server) or as an MCP server.

This text treats the source tree as the specification. Where behavior is ambiguous, the **code path is authoritative**.

### 0.2 Supported platforms within this scope

This text is tuned to **Ubuntu 24.04** execution characteristics:

* Linux userland; typical shells `/bin/bash`, `/bin/sh`.
* Kernel with seccomp enabled; Landlock support is expected on Ubuntu 24.04 but may be restricted inside containers or hardened environments.
* Terminals may be real TTYs or pseudo-TTYs; integrations frequently run non-interactively (no TTY).

### 0.3 Key integration surfaces (prioritized)

1. **Headless execution mode** (`codex exec …`) with optional **JSONL streaming** (`--json`).
2. **Filesystem/config discovery and overrides** (global `-c key=value`, feature toggles).
3. **Sandbox + policy** (sandbox modes, Linux sandbox helper, execpolicy rules).
4. **Session persistence** (recorded sessions and resume/fork semantics).
5. **Distribution wrapper** (Node entrypoint installed via npm/bun, and how it forwards signals and sets environment).
6. App server (stdin/stdout JSON-RPC) and MCP server (covered later in this textbook; referenced for completeness here).

---

## 1. Repository Structure and Responsibility Map (Integrator View)

### 1.1 Top-level layout

* `codex-rs/`: Rust workspace implementing the native CLI, core runtime, sandboxing, protocol, exec mode, app server, MCP server.
* `codex-cli/`: Node distribution wrapper that selects a platform binary and `spawn()`s it; used by `npm i -g @openai/codex`.
* `docs/`: developer documentation (not authoritative over code).
* `sdk/`, `shell-tool-mcp/`, etc.: supporting components.

### 1.2 Rust workspace components most relevant to integration

* `codex-rs/cli/`: main `codex` command, subcommand routing, global config overrides (`-c`), feature toggles (`--enable/--disable`), interactive session wrappers.
* `codex-rs/exec/`: headless execution engine and JSONL event output implementation.
* `codex-rs/core/`: config loader, sandbox/policy logic, tool runtime plumbing, session recording.
* `codex-rs/arg0/`: “arg0 multiplexer” allowing a single binary to behave as helper executables (Linux sandbox helper, apply-patch helper) based on `argv[0]` and a secret arg.
* `codex-rs/linux-sandbox/`: Linux sandbox helper implementation (Landlock + seccomp; invoked via `arg0` dispatch).
* `codex-rs/protocol/`: shared data model used for events, sandbox policy, thread/session protocol.
* `codex-rs/app-server/` and `codex-rs/app-server-protocol/`: JSON-RPC service and message types.

---

## 2. Distribution and Process Launch Contracts (Ubuntu 24.04)

### 2.1 Node distribution wrapper (`codex-cli/bin/codex.js`)

If Codex is installed via npm/bun globally, the user-visible `codex` is commonly a Node script which:

* Computes a platform target triple (Linux: `x86_64-unknown-linux-musl` or `aarch64-unknown-linux-musl`).
* Locates the native binary at:

  * `<package>/vendor/<targetTriple>/codex/codex` (Linux) or `codex.exe` (Windows).
* Optionally prepends `<package>/vendor/<targetTriple>/path` to `PATH` if that directory exists.
* Sets exactly one env var to indicate package manager provenance:

  * `CODEX_MANAGED_BY_NPM=1` or `CODEX_MANAGED_BY_BUN=1`.
* Spawns the native binary asynchronously with:

  * `stdio: "inherit"` (TTY and streams are passed through).
  * `env: { ...process.env, PATH: updatedPath }`
* Forwards signals `SIGINT`, `SIGTERM`, `SIGHUP` to the child, then mirrors the child exit semantics:

  * If the child exits via a signal, Node re-emits the same signal on itself.
  * If the child exits via exit code, Node exits with the same code.

**Integrator guidance**

* If you are building a tool that embeds Codex headlessly, you SHOULD prefer executing the native binary directly (to avoid Node’s `stdio: inherit` constraint and to control pipes precisely).
* If you must execute the Node wrapper, you MUST assume `stdin/stdout/stderr` are not independently configurable (inherit mode), unless you modify the wrapper.
* If you want Codex to present update guidance for npm/bun, you MAY set `CODEX_MANAGED_BY_NPM=1` or `CODEX_MANAGED_BY_BUN=1` in the environment even when calling the native binary.

### 2.2 The native binary is also a helper multiplexer (arg0 dispatch)

The Rust binaries frequently begin by calling an “arg0 dispatch” routine. This enables:

* Running a Linux sandbox helper mode when invoked under an alternate executable name (e.g., `codex-linux-sandbox`).
* Running an apply-patch helper mode when invoked with a secret arg.

**Integrator guidance**

* You MUST NOT assume the `codex` binary “only” implements the CLI entrypoint. It also self-hosts helper entrypoints that are selected by `argv[0]` or specific args.
* If you copy or rename the binary, you MAY unintentionally trigger a different arg0 mode. Keep `argv[0]` stable unless you intend helper behavior.

---

## 3. Global Runtime State: CODEX_HOME and `.env` Injection

### 3.1 CODEX_HOME selection

Codex resolves “Codex home” (state + config root) as:

1. If `CODEX_HOME` is set:

   * It MUST refer to an existing directory; otherwise Codex errors.
2. Else:

   * Default is `~/.codex` (may or may not exist; callers may create it).

**Integrator guidance**

* Tools SHOULD set `CODEX_HOME` explicitly when isolation is required (e.g., per-project or per-run state segregation).
* If you set `CODEX_HOME`, you MUST create the directory first (or accept that Codex will fail early).
* You SHOULD treat `CODEX_HOME` as sensitive state (tokens, session logs, caches).

### 3.2 Codex loads a `.env` file early

At startup, Codex attempts to load:

* `${CODEX_HOME}/.env` if it exists.

However, Codex applies a safety filter:

* Variables whose names start with `CODEX_` are **ignored** when loading `.env`.
* Other variables (e.g., `OPENAI_API_KEY`, `HTTP_PROXY`, etc.) may be loaded.

**Integrator guidance**

* Do not rely on `${CODEX_HOME}/.env` to set `CODEX_HOME` or other `CODEX_*` variables; they will be ignored.
* You MAY use `${CODEX_HOME}/.env` to set provider credentials (e.g., API keys) or general environment settings.
* If you need strict reproducibility, you SHOULD avoid `.env` injection and instead set environment variables explicitly at process launch.

### 3.3 Helper-path injection under CODEX_HOME

Codex attempts to create helper aliases under:

* `${CODEX_HOME}/tmp/path/<random-suffix>/`

It then prepends that directory to `PATH`.

This helper-path directory is used to place:

* A symlink or copy of the current executable named `codex-linux-sandbox`.
* A symlink or copy of the current executable named `apply_patch`.

**Security guardrail**

* In release builds, Codex refuses to create these helper files if `CODEX_HOME` appears to be under the system temp directory (anti-hijack hardening).

**Integrator guidance**

* If you set `CODEX_HOME` to `/tmp/...` (or similar), you SHOULD expect failures in release builds.
* If PATH injection fails, Codex logs a warning and continues; integrations MUST be resilient to missing helper aliases (especially if you call helper names explicitly).
* For hermetic environments, you MAY disable reliance on helper names by calling the main `codex` binary explicitly for sandbox execution (not recommended; the core expects helper availability in some flows).

---

## 4. CLI Surface: Root Command, Global Overrides, and Subcommands

### 4.1 Root command structure (`codex`)

The Rust `codex` binary is implemented as a multi-tool command:

* If no subcommand is provided: it runs the interactive TUI.
* If a subcommand is provided: it routes to that subcommand’s implementation.

### 4.2 Global configuration overrides: `-c key=value`

Codex supports repeatable configuration overrides:

* `-c <KEY>=<VALUE>` or `--config <KEY>=<VALUE>`
* Repeatable; each occurrence is applied in sequence.

Parsing semantics:

* Keys are dotted paths; each component becomes a nested table key.
* Values are parsed as TOML if possible.

  * If TOML parsing fails, the raw string is used as a TOML string.
* Later overrides override earlier ones.

Precedence semantics in the main CLI:

* Root-level `-c` overrides are **prepended** to subcommand overrides, so **subcommand overrides win** if they modify the same key.

**Integrator guidance**

* If you are launching Codex with both global overrides and per-operation overrides, use the same ordering as Codex: apply global first, then operation-specific.
* To avoid ambiguity, tools SHOULD avoid relying on override order within a single argument vector; explicitly construct the full override list in the desired precedence order.
* Tools SHOULD validate override keys and values against Codex’s JSON schema (`codex-rs/core/config.schema.json`) when generating overrides.

### 4.3 Global feature toggles: `--enable FEATURE`, `--disable FEATURE`

Codex supports toggling known feature flags:

* `--enable <FEATURE>` is equivalent to `-c features.<FEATURE>=true`
* `--disable <FEATURE>` is equivalent to `-c features.<FEATURE>=false`

Validation:

* Features are validated against Codex’s known feature registry.
* Unknown feature names cause CLI parse failure with a specific error.

Precedence:

* Feature-toggle derived overrides are appended to root `-c` overrides, meaning toggles override earlier root `-c` values.
* Subcommand `-c` overrides still take precedence over root-level toggles because of the prepend rule.

**Integrator guidance**

* For deterministic behavior, tools SHOULD prefer `-c features.<name>=…` rather than `--enable/--disable` unless user-facing ergonomics require the latter.
* Tools MUST NOT assume feature toggles can enforce security restrictions; they are configuration inputs, not mandatory policy.

### 4.4 Subcommands relevant to automation (high level)

This textbook begins with the **headless automation path**; other subcommands are covered in later parts.

Key subcommands:

* `codex exec …`: headless execution engine (primary automation interface).
* `codex review …`: wrapper that internally uses exec review mode.
* `codex app-server …`: JSON-RPC service (stdin/stdout) for IDE integration.
* `codex mcp …` / `codex mcp-server`: MCP server integration (stdio) and management tools.
* `codex resume …`, `codex fork …`: interactive session continuation; relevant when your tool wants to drive interactive sessions or replay.

---

## 5. Non-Interactive Execution (`codex exec`) — Operational Model

### 5.1 Purpose

`codex exec` is designed to run Codex without a TUI. It supports:

* A single “run” initiated by a prompt.
* Optional streaming of progress and results in **JSONL**.
* Optional schema-constrained final output.
* Optional persistence to “last message” files.

### 5.2 Invocation modes

`codex exec` supports multiple command variants inside the exec subsystem:

* `codex exec` (default “exec” action)
* `codex exec reply …`
* `codex exec review …`

Codex also exposes a top-level `codex review` wrapper that internally maps to `codex exec review`.

This section covers the default “exec” action unless stated otherwise.

### 5.3 Prompt input contract

`codex exec` accepts prompt text via:

* `--prompt <TEXT>` (short `-p`)
* `--prompt -` meaning “read the entire prompt from stdin”

If `--prompt` is omitted, the default is **read from stdin** (behavioral equivalence to `--prompt -`).

Stdin reading guardrails:

* If stdin is a TTY and prompt-from-stdin is requested implicitly or explicitly, Codex exits with an error indicating you must pass a prompt explicitly or pipe stdin.

Prompt decoding:

* Prompt bytes are decoded as:

  * UTF-8 (with or without UTF-8 BOM), OR
  * UTF-16LE/UTF-16BE if a UTF-16 BOM is present.
* UTF-32 BOM is explicitly rejected.
* If decoding fails, Codex exits with an error.

Empty prompt:

* If the decoded prompt contains only whitespace (`trim().is_empty()`), Codex exits with an error.

**Integrator guidance**

* For maximum robustness, tools SHOULD pass the prompt explicitly via `--prompt <TEXT>` when possible.
* If the prompt may exceed typical shell quoting limits, tools SHOULD write the prompt to stdin and pass `--prompt -`, ensuring stdin is not a TTY.
* Tools MUST provide UTF-8 without BOM or UTF-16 with BOM; other encodings are not accepted.
* Tools SHOULD treat “prompt stdin read” as a full-buffer read (not line-based).

### 5.4 Images

`codex exec` supports attaching images:

* `--image <PATH>` repeatable; also supports comma-delimited values.

Images are read from filesystem paths.

**Integrator guidance**

* Tools MUST ensure the paths exist and are readable by the Codex process user.
* Tools SHOULD assume images are loaded eagerly at startup (failure causes early termination).

### 5.5 Output controls: schema and persistence

* `--output-schema <PATH>`:

  * Loads JSON from the given path and uses it as a “final output schema” for the model output formatting.
* `--output-last-message <PATH>`:

  * Writes the final agent message to the specified file, if available.

**Integrator guidance**

* Tools SHOULD use `--output-schema` when machine parsing is required and you can provide a stable schema.
* Tools MUST treat schema load errors as fatal to the run (Codex does).
* Tools SHOULD treat `--output-last-message` as an idempotent “best effort” artifact; validate file presence after execution.

### 5.6 JSONL mode

* `--json` switches the output mode from human-readable printing to **JSONL event streaming** on stdout.

When JSONL mode is enabled:

* stdout becomes a stream of JSON objects, one per line.
* human-readable progress is not emitted to stdout.
* stderr may still contain diagnostics.

**Integrator guidance**

* Tools consuming JSONL MUST treat stdout as machine-only; do not attempt to parse interleaved human text.
* Tools SHOULD keep stderr for logs and display; do not parse it as structured output.
* Tools MUST implement line-delimited JSON parsing; framing is newline-based.

---

## 6. `codex exec --json` JSONL Event Stream — Normative Contract

### 6.1 Transport framing

* Each event is encoded as a single JSON object.
* Each JSON object is terminated by `\n`.
* Encoding is UTF-8.
* Events are written sequentially; consumers MUST NOT assume batching or chunk alignment.

**Consumer algorithm (normative)**

1. Read bytes from stdout until `\n`.
2. Decode the line as UTF-8.
3. Parse JSON to an object.
4. Route by `event` field (string).
5. Maintain per-thread state keyed by `thread_id` when present.

### 6.2 Event envelope

Each JSONL line is an `ExecEvent` with:

* `event`: string discriminator
* `data`: event-specific payload

Example shape:

```json
{"event":"thread_started","data":{"thread_id":"..."}}
```

### 6.3 Event types (current implementation)

This stream is derived from a mapping of core “thread events” into exec-specific events.

#### 6.3.1 `thread_started`

Emitted when a session is configured and execution begins.

Payload:

* `thread_id`: string (UUID-like)

Notes:

* In the current implementation, this event does **not** include a full config summary.

#### 6.3.2 `turn_started`

Emitted when a new “turn” begins (user input is accepted by the agent runtime).

Payload:

* `turn_id`: string (opaque id)
* `input`: string (the prompt text used for the run)

Notes:

* The `input` field is the user prompt as provided/decoded (not necessarily trimmed).
* Consumers SHOULD treat `turn_id` as opaque and unique within the thread.

#### 6.3.3 `item_completed`

Emitted when an “item” finishes.

Payload:

* `item`: object with:

  * `id`: string (opaque item id)
  * `item_type`: string discriminator
  * `content`: type-specific structure

`item_type` currently maps to `ThreadItemDetails` variants, including (non-exhaustive):

* `web_search`: includes query and related metadata.
* `exec_command`: includes command string, exit code, stdout/stderr, and timing.
* `apply_patch`: includes patch text and apply results.
* `agent_message`: includes agent message text and/or structured final output.
* Additional types exist in the protocol but may not yet be emitted by the exec mapper depending on runtime behavior.

**Critical edge case**

* Partial streaming of command output is not guaranteed in the current JSONL mapper: “command output delta” events are intentionally dropped (no incremental stdout/stderr streaming). Consumers should use `exec_command` item completion fields for full captured output.

#### 6.3.4 `turn_completed`

Emitted when the turn finishes successfully.

Payload:

* `turn_id`: string
* `output`: string (final agent message, if available; may be empty depending on failure/interrupt)
* `status`: `"completed"`

If `--output-last-message` was provided, Codex attempts to write `output` to the configured path when this completes.

#### 6.3.5 `turn_failed`

Emitted when the turn ends in a failure state.

Payload:

* `turn_id`: string
* `error`: string (human-readable error)
* `status`: `"failed"`

#### 6.3.6 `error`

Emitted on runtime errors (distinct from turn failure).

Payload:

* `message`: string
* `code`: optional numeric or string code (implementation-dependent)
* `fatal`: boolean (best-effort indicator)

**Exit code coupling**

* If any `error` event is emitted during the run, the `codex exec` process exits with code `1` even if a final message exists.

#### 6.3.7 `status`

Emitted for general progress updates.

Payload:

* `message`: string

### 6.4 Ordering guarantees

Within a single run:

* `thread_started` occurs before any `turn_started`.
* A `turn_started` occurs before the corresponding `turn_completed`/`turn_failed`.
* `item_completed` events for a turn occur after its `turn_started` and before its completion event, but consumers MUST tolerate out-of-order items if future implementations change concurrency.

### 6.5 Non-interactive elicitation handling (hard edge case)

In exec mode, Codex automatically refuses interactive elicitation:

* If the agent runtime requests an “elicitation” (i.e., a question requiring user input mid-run), exec mode cancels it automatically.
* This behavior is implemented by responding to elicitation requests with a “cancel” action rather than asking the user.

**Integrator guidance**

* Tools MUST NOT assume mid-turn interactive prompts are possible in `codex exec`.
* If your workflow requires interactive Q&A, you must use an interactive surface (TUI or a service protocol) or precompute all necessary inputs into the initial prompt.

---

## 7. Exec Exit Codes and Failure Semantics (Automation-Critical)

### 7.1 Exit code rules (observed)

`codex exec` exits with:

* `0` when:

  * The run completes and no runtime error events were observed.
* `1` when:

  * Any runtime error event was observed, OR
  * Startup/config/schema/prompt parsing fails, OR
  * The run fails.

### 7.2 Signals

In native mode, signals behave as normal for a CLI process.
In npm/bun distribution mode:

* Node forwards `SIGINT`, `SIGTERM`, `SIGHUP` to the native child.
* Node mirrors the termination reason so your parent shell sees the expected signal or exit code.

**Integrator guidance**

* When embedding, you SHOULD implement:

  * `SIGINT` propagation to Codex.
  * A timeout kill policy (SIGTERM then SIGKILL) if you need strict bounded execution.
* When consuming JSONL, you MUST handle abrupt stream termination (partial lines) if the process is interrupted. Treat incomplete trailing line as discard.

---

## 8. Sandboxing and Approval: Behavioral Defaults in `codex exec`

### 8.1 Sandbox modes (CLI-facing abstraction)

Sandbox is controlled by a “sandbox mode” input which maps to a concrete runtime policy:

* `read-only`
* `workspace-write`
* `danger-full-access` (often exposed as “dangerously bypass” / “yolo” semantics)
* `external` (signals that an external sandbox already exists; behavior may differ by platform)

### 8.2 `codex exec` default approval policy is “never prompt”

Exec mode imposes a harness-level override:

* Approval prompting is disabled (never ask).
* This is not merely a config default; it is a high-precedence override applied during config resolution.

Practical effect:

* If an operation would require prompting for approval, exec mode cannot prompt and therefore either:

  * forbids the operation, or
  * relies on sandboxing and safe-command heuristics to allow it without prompting.

### 8.3 Full-auto and bypass flags

Exec mode provides:

* `--full-auto`:

  * a convenience for low-friction automated execution under a workspace-write sandbox.
* `--dangerously-bypass-approvals-and-sandbox` (alias `--yolo`):

  * disables sandboxing and confirmation. Intended only for externally sandboxed environments.

**Integrator guidance**

* For Ubuntu automation, `--full-auto` is the safest “hands off” mode that still attempts to constrain filesystem/network access.
* `--yolo` MUST be treated as a hazardous operational mode. Tools SHOULD only expose it behind explicit policy checks and should log/attest when used.

---

## 9. Linux Sandbox Helper (Ubuntu 24.04) — Mechanism and Failure Modes

### 9.1 Invocation model

On Linux, Codex runs sandboxed commands by spawning a helper entrypoint that:

* Is the same executable as `codex`, but invoked under an alternate name via arg0 dispatch (`codex-linux-sandbox`).
* Receives:

  * `--sandbox-policy-cwd <PATH>`
  * `--sandbox-policy <SANDBOX_POLICY_JSON_OR_STRUCT>`
  * `-- <COMMAND> <ARG...>`

### 9.2 Applied restrictions (current implementation)

The Linux sandbox helper applies restrictions on the current thread before `execvp()`:

1. `PR_SET_NO_NEW_PRIVS` if disk write or network is restricted.
2. A **seccomp** filter when network is restricted:

   * Blocks outbound network-related syscalls (connect/bind/listen/send*, setsockopt, etc.).
   * Allows AF_UNIX sockets; denies other socket domains.
   * Allows `recvfrom` explicitly for compatibility with some toolchains (notably those that rely on socketpair/process management).
3. A **Landlock** filesystem ruleset when disk write is restricted:

   * Read access to `/` (entire filesystem).
   * Write access to `/dev/null`.
   * Write access to declared “writable roots” (typically the workspace root plus optional configured roots).

### 9.3 Known limitation: subpath read-only enforcement is not active

The protocol supports “writable roots” with “read-only subpaths” (e.g., `.git`, `.codex`) intended to remain protected even when the workspace is writable.

However, in the current Linux sandbox helper implementation:

* Only writable root paths are passed to Landlock.
* Read-only subpaths are not enforced via mounts (mount logic exists in the codebase but is not invoked by the current helper entrypoint).

**Integrator impact**

* Under Linux `workspace-write` sandbox, **shell commands may be able to write into `.git` and `.codex`** if those directories reside under the writable workspace root.
* Certain internal safety checks (notably for patch application) may still refuse writes into read-only subpaths, but the kernel sandbox does not currently guarantee it for arbitrary shell commands.

**Mitigations**

* Use `read-only` sandbox if you must prevent any workspace mutation.
* Use external sandboxing (containers/VMs) and treat Codex’s internal sandbox as defense-in-depth only.
* Add execpolicy rules to forbid dangerous filesystem commands or `.git` modifications if your threat model includes untrusted codebases.

### 9.4 Failure modes on Ubuntu 24.04

The Linux helper can fail and terminate (panic) if:

* Landlock is unavailable or returns “not enforced”.
* Seccomp cannot be installed.
* `execvp` fails.

In such cases:

* The tool command fails; Codex will treat this as a tool execution failure.
* In headless mode, there is no interactive remediation; your integration MUST handle failure.

**Integrator guidance**

* If you are running inside containers or restricted environments, you SHOULD test sandbox viability early (see debug sandbox command in later chapters).
* If sandbox consistently fails due to kernel policy, you MAY need `external` or `danger-full-access` mode with your own sandbox boundary.

---

## 10. Exec Policy (“execpolicy”) — Where It Fits in Automation

### 10.1 Role

Execpolicy is a rules engine that classifies shell commands and determines:

* Allow (possibly with sandbox bypass).
* Prompt (not usable in exec mode due to “never prompt”).
* Forbid.

In exec mode, execpolicy becomes especially important because:

* There is no mid-run prompting.
* Dangerous command heuristics can forbid a command unless it is explicitly allowed by policy.

### 10.2 Policy file discovery (multi-layer)

Execpolicy files are discovered by scanning config folders for each config layer, typically:

* System
* User
* Project `.codex` folders (including nested repository layers)

Policy discovery:

* Looks under `<config_folder>/rules/` for `*.rules` files.
* Files are loaded in a deterministic order (sorted by path).

**Critical edge case**

* Even when a project config folder is “disabled” due to trust gating, its `.codex` folder may still be included for execpolicy file discovery in the current implementation.
* This means untrusted projects may contribute rules unless your configuration disables that feature.

### 10.3 Interaction with approval policy in `codex exec`

Because exec mode never prompts:

* Any execpolicy “prompt” decision becomes effectively a “forbid” for automation purposes.
* To ensure automation reliability, your policy must resolve commands to “allow” or “forbid” deterministically.

**Integrator guidance**

* If you depend on automation completing, you SHOULD:

  * pre-authorize required commands via execpolicy allow rules, OR
  * avoid commands that the heuristics would label dangerous.
* You SHOULD treat execpolicy content as sensitive security configuration and manage it as code with auditing.

---

## 11. Session Recording and Resume/Fork (Automation-Relevant Summary)

### 11.1 Session storage layout

Codex records sessions under:

* `${CODEX_HOME}/sessions/<YYYY>/<MM>/<DD>/rollout-<timestamp>-<uuid>.jsonl`

There is also an archive directory:

* `${CODEX_HOME}/sessions-archived/…`

### 11.2 Log format (high-level)

* JSONL file.
* First line: session metadata (id, timestamp, cwd, originator, model provider, etc.).
* Subsequent lines: protocol events.

### 11.3 Resume/fork filtering behavior (interactive wrapper)

When selecting the “most recent session” for resume/fork:

* Codex filters recorded sessions to those whose recorded `cwd` matches the current working directory, unless an “all sessions” flag is used.

**Integrator guidance**

* If your tool intends to “resume the last session” programmatically, you SHOULD supply the session id explicitly rather than relying on cwd-based “last session” heuristics.

---

## 12. Immediate Integration Recipes (Ubuntu 24.04)

### 12.1 Minimal headless run (no JSON)

Procedure:

1. Launch `codex exec --prompt <TEXT>` as a subprocess.
2. Capture stdout as final message output.
3. Capture stderr for diagnostics.
4. Treat exit code 0 as success.

### 12.2 Headless run with JSONL streaming

Procedure:

1. Launch `codex exec --json --prompt <TEXT>`.
2. Read stdout line-by-line; parse each JSON object.
3. Maintain state by `thread_id`, then `turn_id`.
4. Extract final output from `turn_completed.output`.
5. If exit code is 1, treat the run as failed even if output exists; your tool MAY still display the output but must annotate the run as error-bearing.

### 12.3 Schema-constrained final output

Procedure:

1. Write a JSON schema file to a temporary path.
2. Launch `codex exec --output-schema <PATH> --json --prompt <TEXT>`.
3. Parse events; in `item_completed` and `turn_completed`, prefer structured data if present (implementation-dependent).
4. Validate the final output against your schema client-side; do not assume server-side validation guarantees correctness.

### 12.4 Safe automation baseline (recommended)

Procedure:

1. Launch `codex exec --full-auto --json --prompt <TEXT>`.
2. Keep CODEX_HOME on persistent storage (not `/tmp`) unless you understand helper-path behavior.
3. Provide execpolicy allow rules for required build/test commands if your workflow needs them.