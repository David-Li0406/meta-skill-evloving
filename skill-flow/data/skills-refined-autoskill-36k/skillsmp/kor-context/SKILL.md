---
name: kor_context
description: Deep context and architectural understanding of the KOR SDK project. Use this skill when you need to understand the codebase structure, design patterns, or how to implement features in the "KOR Way".
---

# KOR SDK Context & Architecture

You are working on the **KOR SDK**, an Enterprise Developer Platform built on a **Vertical Architecture**.

## 1. Core Philosophy: The "KOR Way"

- **Vertical Architecture**: Code is organized by domain (`mcp`, `lsp`, `skills`, `plugin`), not by technical layer (models, views). Each domain is self-contained.
- **Consolidated Modules**: We prefer single-file modules (e.g., `events.py`, `search.py`, `commands.py`) over scattered `__init__.py` files when the complexity is low (< 5 files).
- **Facade First**: The public API is the `Kor` class in `kor_core.api`. Always design for the user accessing functionality via `kor = Kor()`.
- **Pythonic & Explicit**: We use explicit typing, dataclasses, and standard Python patterns. We avoid "magic" where possible (e.g., rigid frameworks).

## 2. Directory Map (Deep Dive)

`packages/kor-core/src/kor_core/`:

### Core Infrastructure

- **`api.py` (The Facade)**: The ONLY intended public entry point.
  - *Rule*: Never import `Kernel` in user code. Use `from kor_core import Kor`.
- **`kernel.py` (The Engine)**: Orchestrates lifecycle.
  - *Key*: It is a Singleton. Access via `get_kernel()` internally if needed, but prefer passing dependencies.
- **`config.py`**: Pydantic-based configuration.
  - *Pattern*: Start with `ConfigManager().load()`. Supports `~/.kor/config.toml`.
- **`events.py`**: Unified Event Bus and Telemetry.
  - *Key*: Use `HookEvent` enum for lifecycle events. Contains `TelemetrySubscriber` and `LoggingTelemetrySink`.

### Vertical Domains

- **`mcp/`**: Model Context Protocol.
  - *Structure*: `client.py` (connects to servers), `server.py` (hosts resources).
- **`lsp/`**: Language Server Protocol.
  - *Feature*: Provides Code Intelligence (Hover, Definition) to Agents.
- **`skills.py`**: Skills System.
  - *Pattern*: `SkillLoader` inherits `BaseLoader`. `SkillRegistry` inherits `SearchableRegistry`.

### Plugin System

- **`plugin.py`**: Plugin System.
  - *Consolidated*: Contains `manifest`, `loader`, `context`.
  - *Workflow*: Plugins are loaded by `kernel.py` at boot.

### Utilities

- **`search.py`**: Unified Search Infrastructure.
  - *Provides*: `Searchable` protocol, `SearchableRegistry[T]`, `RegexBackend`, `BM25Backend`.
  - *Pattern*: All registries (Tools, Skills, Commands, Agents) inherit from `SearchableRegistry`.
- **`commands.py`**: Slash Commands System.
  - *Pattern*: `CommandLoader` inherits `BaseLoader`. `CommandRegistry` extends `SearchableRegistry`.

### Agent System

- **`agent/`**: Multi-Agent Orchestration.
  - `state.py`: `AgentState`, `PlanTask` TypedDicts.
  - `planning.py`: `Planner` class with file sync, events.
  - `archiver.py`: `PlanArchiver` for long-term memory.
  - `graph.py`: LangGraph workflow builder.
  - `nodes/`: Worker nodes (Supervisor, Architect, Coder, etc.).

## 2.5 Native Planning Architecture

The SDK includes a **Plan-and-Execute** system for autonomous agents:

- **Entry Flow**: `AutoPlanner → EnsurePlan → Supervisor → Workers`
- **File Sync**: Agent state syncs with `PLAN.md` (GFM checklist).
- **Events**: `TASK_STARTED`, `TASK_COMPLETED`, `PLAN_FINISHED`.
- **Memory**: Completed plans archived to `~/.kor/memory/plans.jsonl`.
- **Tool**: `ManagePlanTool` with actions: `add_task`, `add_subtask`, `update_status`, `finish_task`.

## 3. Implementation Recipes

### How to add a new Tool

1. **Create Class**: In `kor_core/tools/<category>.py` (or generic `tools.py`).
2. **Inherit**: From `BaseTool` (pydantic `BaseModel`).
3. **Register**: In `kor_core.kernel.Kernel._register_core_tools()`.
4. **Tag**: Add tags/keywords for semantic search discovery.

### How to Add a New LLM Provider

1. **Do NOT create a new file**: Modify `kor_core/llm/provider.py`.
2. **Update `UnifiedProvider`**: Ensure `_create_client` handles the new `base_url` or signature.
3. **Config**: Map it in `kor_core/config.py` under `LLMConfig`.

### How to Create a Declarative Plugin

1. **Folder**: `plugins/kor-plugin-<name>/`.
2. **Manifest**: `plugin.json` (defines commands, tools).
3. **Scripts**: `scripts/my_script.py` (executable logic).
4. **No Init**: Do NOT verify `__init__.py` for declarative plugins.

## 4. Coding Standards & Best Practices

- **Typing**: Strict `mypy` compatibility. Use `typing.List`, `typing.Optional`.
- **Imports**:
  - Vertical: `from . import models` (relative within module).
  - Horizontal: `from kor_core.other import thing` (absolute across modules).
  - *Avoid circular imports*: Use `if TYPE_CHECKING:` for type-only dependencies.
- **Async/Sync**:
  - The Kernel is primarily **Async**.
  - `boot_sync()` is a wrapper for CLI convenience.
  - Always `await` I/O operations (LLM, File, Network).
- **Error Handling**:
  - Use specific exceptions from `kor_core.exceptions`.
  - Never swallow exceptions silently in the Kernel.

## 5. Architecture Decision Records (ADR) - Simplified

- **ADR-001 Vertical Arch**: We moved from Layered (loaders/, registries/) to Vertical (mcp/, lsp/) to localize complexity.
- **ADR-002 Facade**: We hid the `Kernel` complexity behind `Kor` to make the library approachable for beginners.
- **ADR-003 Resources**: We moved prompts/markdown OUT of `src/` to `resources/` to separate code from data.
- **ADR-004 Single File Modules**: We merged small folders into single `.py` files to reduce "tab fatigue".
- **ADR-005 CLI Decoupling**: The CLI (`chat`) is Agent-Agnostic. It renders generic events (`messages`, `next_step`) rather than hardcoding agent names.
- **ADR-006 Native Planning**: Agents use file-backed `PLAN.md` for transparent, human-editable planning.

Use this skill to simulate "Senior Engineer" context when editing the codebase.
