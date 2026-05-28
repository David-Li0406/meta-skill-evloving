# Claude Code Skills — Procedural Authoring and Execution Reference

## 0. Scope and terminology

A **skill** is a packaged capability discovered by Claude Code and executed from a `SKILL.md` entrypoint. A skill may run **inline** (same session) or in an **isolated subagent** (forked context). Normative terms: MUST, MUST NOT, SHOULD, MAY.

---

## 1. Skill package model

### 1.1 Package shape

A skill MUST be a directory containing `SKILL.md` at its root.

Recommended layout (supporting files are optional):

```
<skill-dir>/
  SKILL.md                 # required: frontmatter + instructions
  reference.md             # optional: large reference docs
  examples/                # optional: expected outputs
  templates/               # optional: fill-in templates
  scripts/                 # optional: executable helpers
```

### 1.2 Storage scope and precedence

A skill MAY be stored at any of the following scopes:

* Enterprise (managed settings)
* Personal: `~/.claude/skills/<skill-name>/SKILL.md`
* Project: `.claude/skills/<skill-name>/SKILL.md`
* Plugin: `<plugin>/skills/<skill-name>/SKILL.md`

Resolution rule for same-name conflicts: **enterprise > personal > project**.
Plugin skills use a `plugin-name:skill-name` namespace and therefore do not collide with non-plugin skills.

### 1.3 Nested discovery (monorepos)

When operating within subdirectories, Claude Code MAY discover additional skills from nested `.claude/skills/` directories located nearer to the working files (e.g., per-package skill sets). Authors SHOULD assume multiple concurrent skill roots may be active and name skills accordingly.

---

## 2. `SKILL.md` format

### 2.1 File grammar

`SKILL.md` MUST be:

1. YAML frontmatter delimited by `---` lines (frontmatter MAY be empty), followed by
2. Markdown instructions (the skill body).

### 2.2 Instructional contract

The Markdown body is the instruction payload Claude follows when the skill is activated. Authors SHOULD write the body as one of two stable patterns:

* **Reference skill (inline augmentation):** conventions, invariants, style guides, domain rules.
* **Task skill (procedural workflow):** explicit steps, side effects, artifact generation; typically invoked manually or run in subagents.

---

## 3. Frontmatter fields (behavioral API)

All fields are optional; defaults apply where stated.

### 3.1 `name` (string)

* Purpose: canonical skill identifier.
* Default: if omitted, the directory name is used.
* Constraints: lowercase letters, digits, hyphens only; max length 64.

### 3.2 `description` (string)

* Purpose: relevance signal used for automatic loading/selection.
* Default: if omitted, Claude Code uses the first paragraph of the Markdown body as the description.
* Authoring rule: description SHOULD include the user-language triggers that should activate the skill and SHOULD be unambiguous about when NOT to use it (by positive specificity, not negation).

### 3.3 `argument-hint` (string)

* Purpose: UI hint indicating expected arguments (e.g., `[issue-id] [format]`).
* Semantics: informational only; no runtime validation implied.

### 3.4 `disable-model-invocation` (boolean; default `false`)

* If `true`: the model MUST NOT automatically invoke/load the skill.
* Intended use: workflows with side effects, timing sensitivity, or high risk.

### 3.5 `user-invocable` (boolean; default `true`)

* If `false`: the skill is hidden from interactive invocation menus.
* Note: this field controls visibility only; it does not prevent programmatic invocation.

### 3.6 `allowed-tools` (string list)

* Purpose: declare which tools Claude may use without asking permission while the skill is active.
* Typical patterns:

  * Read-only exploration: `Read, Grep, Glob`
  * Constrained shell access: `Bash(gh:*)`, `Bash(python:*)`
* Authoring rule: `allowed-tools` SHOULD be minimally sufficient (“least privilege”).

### 3.7 `model` (string)

* Purpose: select the model used when the skill is active.
* Authoring rule: set only when deterministic model selection is required; otherwise inherit defaults.

### 3.8 `context` (string)

* Supported value: `fork`
* If set to `fork`: the skill MUST run in an isolated subagent context (see §6).

### 3.9 `agent` (string; effective only when `context: fork`)

* Purpose: select which subagent configuration executes the forked skill.
* Valid values include built-in agents (`Explore`, `Plan`, `general-purpose`) and any custom subagent defined in `.claude/agents/`.
* Default: `general-purpose` if omitted.

### 3.10 `hooks` (mapping)

* Purpose: define hooks scoped to the skill lifecycle.
* Semantics: hook structure follows the Hooks configuration format; authors MUST treat this as an integration surface and keep hook side effects explicit.

---

## 4. Runtime substitution and argument binding

### 4.1 `$ARGUMENTS`

* `$ARGUMENTS` expands to the raw argument string supplied at invocation.
* If the skill body does not contain `$ARGUMENTS`, Claude Code appends `ARGUMENTS: <value>` to the end of the prompt payload.

### 4.2 `${CLAUDE_SESSION_ID}`

* Expands to the current session identifier.
* Typical use: deterministic file paths, correlation IDs, session-scoped logs.

---

## 5. Supporting files (progressive disclosure)

### 5.1 Loading model

* Skill descriptions are surfaced broadly for relevance.
* Full skill content is loaded when the skill is activated.
* Large reference content SHOULD be placed in supporting files and referenced from `SKILL.md` so it is loaded only when needed.

### 5.2 Authoring rules for supporting files

* `SKILL.md` SHOULD act as an index and operational entrypoint; keep it concise (recommended: under ~500 lines).
* Supporting files SHOULD be linked explicitly with a short purpose statement, e.g.:

  * “For full API constraints, see `reference.md`.”
  * “For expected outputs, see `examples/sample.md`.”
* Executable helpers in `scripts/` SHOULD be treated as tools to run, not as context to load.

---

## 6. Subagent-executed skills (`context: fork`)

### 6.1 Execution semantics

If `context: fork` is set:

1. Claude Code creates a new isolated subagent context.
2. The skill body becomes the subagent’s primary task prompt.
3. The selected `agent` determines the subagent environment (model/tools/permissions).
4. The subagent returns results to the main session as a summary/output.

The forked subagent does not rely on main-session conversation history; authors MUST assume the subagent only sees what the skill payload provides (plus standard persistent project context such as applicable memory files).

### 6.2 Mandatory authoring contract for forked skills

A forked skill MUST include an explicit task specification. At minimum:

* Objective statement (what “done” means).
* Inputs (what `$ARGUMENTS` encodes; any required files/paths).
* Procedure (ordered steps; decision points).
* Output contract (format, required sections, file references, artifacts).
* Constraints (tool limits implied by `allowed-tools`; safety/side effects rules).

A “guidelines-only” body without an actionable task SHOULD NOT be used with `context: fork`, because the subagent will receive instructions without work to execute and may return low-value output.

### 6.3 Agent selection constraints

* If `agent` is a read-only agent type (e.g., exploration/planning agents that deny edits), the skill body MUST NOT require write/edit operations and MUST phrase tasks as discovery/summarization.
* If the workflow requires file modifications, the skill MUST use an agent configuration that permits those tools.

### 6.4 Forked-skill template (minimal)

```yaml
---
name: <skill-name>
description: <when to use; include trigger phrases>
context: fork
agent: <Explore|Plan|general-purpose|custom>
allowed-tools: <least-privilege tool set>
---

TASK: <single-sentence objective>.

INPUTS:
- Arguments: $ARGUMENTS
- Required files: <paths or discovery rules>

PROCEDURE:
1) ...
2) ...
3) ...

OUTPUT:
- Provide: <structured output>
- Include: <file references / diffs / commands executed>
```

---

## 7. Skills preloaded into subagents (subagent “skills” field)

### 7.1 Model

A subagent definition MAY preload skills as embedded reference modules. In that mode:

* The full content of each listed skill is injected into the subagent at startup.
* Subagents do not inherit skills from the parent session; preloading is explicit.

### 7.2 Operational implications

* Preloaded skills are always present for that subagent; therefore, each preloaded skill SHOULD be concise and stable.
* Large, volatile, or rarely-needed material SHOULD remain in supporting files and be referenced procedurally to avoid inflating subagent context.

### 7.3 Pattern comparison (choose one)

* **Forked skill (`context: fork`):** the skill supplies the task prompt; the agent type supplies the execution environment.
* **Custom subagent with preloaded skills:** the subagent supplies the system prompt; delegation supplies the task; preloaded skills supply durable reference context.

Use forked skills for reusable, self-contained workflows. Use preloaded-skill subagents for durable specialist roles that repeatedly apply the same policy/convention set.

---

## 8. Dynamic context injection (pre-execution command substitution)

### 8.1 Syntax

Within the skill body, the form:

```
!`<shell-command>`
```

executes `<shell-command>` before the prompt is sent to Claude, and replaces the directive with the command output.

### 8.2 Semantics

* Commands run during preprocessing.
* Claude sees only the rendered output, not the command text.
* Authors MUST ensure the required tool permission is granted via `allowed-tools` (e.g., constrained `Bash(...)` patterns).
* Authors SHOULD bound output volume (filter, truncate, or summarize) to avoid excessive prompt injection.

### 8.3 Canonical use cases

* Inject live diffs, file lists, PR metadata, build outputs, environment snapshots.
* Construct a deterministic “context block” at the top of a task prompt.

---

## 9. Skill access control and governance

### 9.1 Per-skill gating (author-controlled)

* To prevent automatic activation: set `disable-model-invocation: true`.
* To hide from interactive menus: set `user-invocable: false` (does not block programmatic use).

### 9.2 System policy gating (administrator-controlled)

Skill tool access can be controlled by permission rules. Supported forms:

* Allow exact: `Skill(name)`
* Allow prefix/arguments: `Skill(name:*)`
* Deny exact/prefix similarly.

Authors SHOULD design skill names and argument conventions to support prefix-based allowlists for least privilege (e.g., separate “read-only” vs “side-effecting” skills by name prefix).

---

## 10. Operational limits and failure modes

### 10.1 Description budget

Skill descriptions are loaded for relevance, but the total description set is subject to a character budget; if exceeded, some skills may be excluded from relevance consideration. Authors SHOULD keep descriptions short, specific, and non-redundant; consolidate overlapping skills; and move depth into supporting files.

### 10.2 Mis-triggering remediation

If a skill activates unexpectedly:

* Increase specificity of `description` (narrow triggers; include domain qualifiers).
* For manual-only workflows, set `disable-model-invocation: true`.

If a skill fails to activate:

* Ensure `description` matches realistic user phrasing.
* Reduce ambiguity with explicit trigger phrases and scope markers (repo name, subsystem, artifact type).