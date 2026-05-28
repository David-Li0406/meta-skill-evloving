# AgentSkillOS Architecture

## Quick Nav

| I want to…                        | Go to                                                        |
|-----------------------------------|--------------------------------------------------------------|
| Add a new orchestrator engine     | [Extension Guide: Engine](#new-engine)                       |
| Add a new manager                 | [Extension Guide: Manager](#new-manager)                     |
| Understand the execution flow     | [Call Chains](#call-chains)                                  |
| Debug a WebSocket issue           | `src/web/routes.py`, `src/web/visualizer.py`                 |
| Change the front-end UI           | `src/web/templates/`, `src/web/static/js/`                   |
| Modify search behavior            | `src/manager/tree/searcher.py`, `layered_searcher.py`, `dormant_searcher.py` |
| Use vector search                 | `src/manager/vector/`                                        |
| Manage recipes                    | `src/web/recipe.py`, `src/web/templates/modules/recipe/`     |
| Tweak configuration / defaults    | `src/config.py`, `src/constants.py`                          |
| Run tasks in batch (headless)     | `src/workflow/service.py`, `src/workflow/executor.py`         |
| Run evaluation pipeline           | `src/workflow/evaluation.py`                                 |
| Update active/dormant skill layers | `src/manager/tree/layer_processor.py`, CLI `update-layer`   |

---

## Architecture Overview

```
                           ┌──────────┐
                           │  cli.py  │
                           └────┬─────┘
              ┌─────────────────┼──────────────────┐
              ▼                 │                   ▼
┌──────────────────────┐        │       ┌─────────────────────┐
│       web/           │        │       │     workflow/        │
│                      │        │       │                     │
│  app.py (server)     │        │       │  executor.py (CLI)  │
│  routes.py (WS+HTTP) │        │       │  batch.py           │
│  service.py          │        │       │  service.py         │
│  state.py (FSM)      │        │       │  loader.py (YAML)   │
│  visualizer.py       │        │       │  models.py          │
│  recipe.py           │        │       │  progress.py        │
│                      │        │       │  evaluation.py      │
│  templates/          │        │       └──────────┬──────────┘
│    core/   modules/  │        │                  │
│  static/js/          │        │                  │
│    core/   modules/  │        │                  │
└──────────┬───────────┘        │                  │
           │                    │                  │
           ▼                    ▼                  ▼
┌──────────────────────────────────────────────────────────────┐
│                       Shared Backend                         │
│                                                              │
│  ┌─────────────────────┐    ┌──────────────────────────────┐ │
│  │     manager/        │    │       orchestrator/          │ │
│  │                     │    │                              │ │
│  │  registry.py        │    │  registry.py                 │ │
│  │  base.py (Protocol) │    │  base.py (Protocol)          │ │
│  │                     │    │                              │ │
│  │  tree/              │    │  dag/                        │ │
│  │    builder.py       │    │    engine.py (SkillOrch.)    │ │
│  │    searcher.py      │    │    graph.py  throttler.py    │ │
│  │    layered_searcher │    │    skill_registry.py         │ │
│  │    layer_processor  │    │    prompts.py                │ │
│  │    dormant_searcher │    │                              │ │
│  │    dormant_indexer  │    │  direct/                     │ │
│  │    scheduled_updater│    │    engine.py (DirectEngine)  │ │
│  │    user_prefs.py    │    │                              │ │
│  │    models.py        │    │  freestyle/                  │ │
│  │    skill_scanner.py │    │    engine.py (FreestyleEng.) │ │
│  │    prompts.py       │    │                              │ │
│  │    visualizer.py    │    │  runtime/                    │ │
│  │                     │    │    client.py (SkillClient)   │ │
│  │  direct/            │    │    run_context.py            │ │
│  │    __init__.py      │    │    models.py  prompts.py     │ │
│  │    (DirectManager)  │    │    async_utils.py            │ │
│  │                     │    │                              │ │
│  │  vector/            │    │  visualizers/                │ │
│  │    __init__.py      │    │    protocol.py               │ │
│  │    indexer.py       │    │    web_visualizer.py         │ │
│  │    searcher.py      │    │    null_visualizer.py        │ │
│  └─────────────────────┘    └──────────────────────────────┘ │
│                                                              │
│  cache.py (LiteLLM disk cache)                               │
│  config.py (3-level: CLI > ENV > YAML)                       │
│  constants.py (skill groups, demo tasks, tools)              │
└──────────────────────────────────────────────────────────────┘
```

**Four paths:**

- **Web path** — `cli.py` → `web/app` → `routes` → `service` → manager.search() + orchestrator.create_engine().run()
- **Batch path** — `cli.py cli` → `workflow/executor` → `batch` → `service.run_task()` → manager.search() + orchestrator.create_engine().run()
- **Build path** — `cli.py build` → `manager.create_manager().build()` (builds skill tree; with layering: → `layer_processor` → `dormant_indexer`)
- **Update-layer path** — `cli.py update-layer` → `layer_processor` / `scheduled_updater` → `dormant_indexer` (refreshes active/dormant sets)

Web injects `WebVisualizer` (real-time WebSocket push), Batch injects `NullVisualizer` (silent execution). Both share manager/, orchestrator/, and config/constants.

---

## Directory Structure

```
src/
├── cli.py                        # argparse CLI entry point (webui / build / cli / update-layer)
├── config.py                     # Config singleton, 3-level override: CLI > ENV > YAML
├── constants.py                  # Skill groups, demo tasks, default tools
├── logging_config.py             # Loguru setup
├── cache.py                      # LiteLLM disk cache initialization (thread-safe)
│
├── manager/                      # ── Skill discovery & indexing ──
│   ├── __init__.py               # Re-exports create_manager, list_plugins
│   ├── base.py                   # BaseManager Protocol + RetrievalResult
│   ├── registry.py               # @register_manager + pkgutil auto-discovery
│   │
│   ├── tree/                     # "tree" manager — LLM-guided tree search
│   │   ├── __init__.py           # TreeManager + UI_CONTRIBUTION
│   │   ├── builder.py            # Queue-based parallel tree builder
│   │   ├── searcher.py           # Multi-level LLM search with event callbacks
│   │   ├── layered_searcher.py   # LayeredSearcher — active-first + dormant fallback
│   │   ├── layer_processor.py    # LayerPostProcessor — install-count / directory layering
│   │   ├── dormant_searcher.py   # DormantVectorSearcher — ChromaDB vector search for dormant skills
│   │   ├── dormant_indexer.py    # DormantIndexBuilder — build vector index for dormant skills
│   │   ├── scheduled_updater.py  # ScheduledUpdater — periodic active/dormant refresh
│   │   ├── user_prefs.py         # UserPreferences — pinned skill storage
│   │   ├── models.py             # TreeNode, Skill, DynamicTreeConfig
│   │   ├── skill_scanner.py      # Skill file scanner
│   │   ├── prompts.py            # LLM prompts for tree ops
│   │   ├── visualizer.py         # Tree visualization helpers
│   │   └── __main__.py           # Standalone entry
│   │
│   ├── direct/                   # "direct" manager — returns all skills, no search
│   │   └── __init__.py           # DirectManager (for free-style engine)
│   │
│   └── vector/                   # "vector" manager — ChromaDB vector similarity search
│       ├── __init__.py           # VectorManager + UI_CONTRIBUTION
│       ├── indexer.py            # VectorIndexer — scan skills, embed, store in ChromaDB
│       └── searcher.py           # VectorSearcher — top-k similarity query
│
├── orchestrator/                 # ── Task execution ──
│   ├── __init__.py               # Re-exports engines + base types
│   ├── base.py                   # ExecutionEngine Protocol + EngineRequest/ExecutionResult
│   ├── registry.py               # @register_engine + pkgutil auto-discovery
│   ├── dag/                      # "dag" engine — plan → parallel execute
│   │   ├── engine.py             # SkillOrchestrator (registered as "dag")
│   │   ├── graph.py              # DependencyGraph
│   │   ├── skill_registry.py     # SkillRegistry
│   │   ├── throttler.py          # ExecutionThrottler
│   │   └── prompts.py            # Planner / executor prompts
│   ├── direct/                   # "no-skill" engine — single LLM call
│   │   └── engine.py             # DirectEngine (registered as "no-skill")
│   ├── freestyle/                # "free-style" engine — unconstrained agent
│   │   └── engine.py             # FreestyleEngine (registered as "free-style")
│   ├── runtime/                  # Shared execution infrastructure
│   │   ├── client.py             # SkillClient (wraps Claude SDK)
│   │   ├── run_context.py        # RunContext — isolated work directories
│   │   ├── models.py             # SkillMetadata, NodeStatus, ExecutionPhase
│   │   ├── prompts.py            # Direct / freestyle executor prompts
│   │   └── async_utils.py        # create_tracked_task()
│   └── visualizers/              # Execution visualization
│       ├── __init__.py           # Re-exports
│       ├── protocol.py           # VisualizerProtocol
│       ├── null_visualizer.py    # NullVisualizer (headless)
│       └── web_visualizer.py     # OrchestratorState (WebSocket broadcast)
│
├── web/                          # ── Web UI (FastAPI + Alpine.js) ──
│   ├── __init__.py               # Template assembler (INCLUDE + SLOT directives)
│   ├── app.py                    # run_server() entry
│   ├── routes.py                 # HTTP + WebSocket routes
│   ├── service.py                # WorkflowService
│   ├── state.py                  # WorkflowPhase state machine
│   ├── visualizer.py             # WebVisualizer (WebSocket broadcast)
│   ├── recipe.py                 # Recipe model + storage (reusable skill combinations)
│   ├── templates/                # Jinja-like templates
│   │   ├── base.html             # HTML shell
│   │   ├── unified.html          # Main content with SLOT markers
│   │   ├── core/                 # Shared partials
│   │   │   ├── header.html
│   │   │   ├── log-panel.html
│   │   │   ├── phase-idle.html
│   │   │   ├── completion-modal.html
│   │   │   ├── connection-status.html
│   │   │   ├── end-task-modal.html
│   │   │   └── start-new-task-button.html
│   │   └── modules/              # Plugin partials per manager/engine
│   │       ├── manager_tree/     # tree-search, skill-review, skill-detail-modal, tree-browser-modal
│   │       ├── manager_vector/   # vector-search, skill-review, skill-detail-modal
│   │       ├── orchestrator_dag/ # dag-execute, node-log-modal, plan-preview-modal, plan-selection-modal
│   │       ├── orchestrator_direct/  # direct-execute
│   │       ├── orchestrator_freestyle/ # freestyle-execute
│   │       └── recipe/           # recipe-detail-modal, save-recipe-modal
│   └── static/js/
│       ├── common.js             # Shared utility functions
│       ├── dag-renderer.js       # DAG graph rendering
│       ├── core/                 # App bootstrap: state → ws → hooks → slices → shell
│       └── modules/              # Plugin JS per manager/engine
│           ├── manager_tree/     # tree-search.js, skill-review.js
│           ├── manager_vector/   # vector-search.js, skill-review.js
│           ├── orchestrator_dag/ # dag-execute.js, dag-plan.js
│           ├── orchestrator_direct/  # direct-execute.js
│           ├── orchestrator_freestyle/ # freestyle-execute.js
│           └── recipe/           # recipe.js
│
└── workflow/                     # ── Batch / headless execution ──
    ├── __init__.py               # Re-exports
    ├── service.py                # run_task() — 5-step pipeline
    ├── batch.py                  # run_batch() — parallel batch execution
    ├── executor.py               # BatchExecutor — Rich progress CLI adapter
    ├── loader.py                 # TaskLoader — YAML config loading
    ├── models.py                 # TaskRequest, BatchConfig, BatchResult, etc.
    ├── progress.py               # BatchProgressManager
    └── evaluation.py             # Evaluation pipeline — bridge to benchmark scoring
```

---

## Core Mechanisms

### Plugin Registration (Manager & Engine)

Both `manager/registry.py` and `orchestrator/registry.py` follow the same pattern:

1. **Decorator** — `@register_manager(name)` / `@register_engine(name)` adds the class to a dict
2. **Auto-discovery** — `pkgutil.iter_modules()` scans sub-packages lazily on first call (thread-safe)
3. **Factory** — `create_manager(name)` / `create_engine(name)` instantiates by name

### Layered Skill Management

The tree manager supports a two-layer **active / dormant** strategy to handle large skill libraries efficiently:

1. **Layer Processor** (`layer_processor.py`) — Post-processes a full `tree.yaml` into `active_tree.yaml` + `dormant_index.yaml`. Two modes:
   - **install-count mode** — ranks skills by install count, keeps top-N + user-pinned skills active
   - **directory mode** — uses separate directories for active/dormant skills
2. **Layered Searcher** (`layered_searcher.py`) — Searches the active tree first via `Searcher`, then always suggests dormant skills via `DormantVectorSearcher` as additional options
3. **Dormant Index** (`dormant_indexer.py` + `dormant_searcher.py`) — Builds a ChromaDB vector index for dormant skills, enabling semantic similarity search over 100k+ skills
4. **User Preferences** (`user_prefs.py`) — Persists user-pinned skills that are kept active regardless of ranking
5. **Scheduled Updater** (`scheduled_updater.py`) — Refreshes active/dormant sets from latest install data, promoting/demoting skills while protecting pinned ones

### Template Assembly (Web)

`web/__init__.py` assembles the final HTML page in 5 steps:

1. Load `base.html` + `unified.html`
2. Fill `<!-- SLOT:name -->` markers with plugin partials from `ui_contribution`
3. Recursively resolve `<!-- INCLUDE:path -->` directives (max depth 5)
4. Inject JS: `core/*.js` → `modules/*.js` → `app-shell.js`
5. Fill base placeholders (title, scripts, app_data)

### JS Slice System (Front-end)

Each engine's JS calls `registerExecuteSlice(engineId, sliceFn)` on load. `app-shell.js` delegates execution methods to the active engine's slice based on `executionMode`, enabling runtime engine switching.

### Config

Three-level override: **CLI args > ENV (.env) > config.yaml > defaults**. Singleton via `get_config()`. See `config.py` for all properties.

### State Machine (Web)

```
IDLE → SEARCHING → REVIEWING → PLANNING → EXECUTING → COMPLETE
                                   ↘                    ↗
                                     →→→ ERROR →→→→→→→→→
```

---

## Extension Guide

### <a name="new-engine"></a> New Orchestrator Engine

Create 3 files:

| # | File | Purpose |
|---|------|---------|
| 1 | `src/orchestrator/<name>/engine.py` | Engine class with `@register_engine` |
| 2 | `src/web/templates/modules/orchestrator_<name>/<name>-execute.html` | Execute phase HTML |
| 3 | `src/web/static/js/modules/orchestrator_<name>/<name>-execute.js` | Execute slice JS |

**Minimal `engine.py`:**

```python
from orchestrator.base import EngineRequest, ExecutionResult, EngineMeta
from orchestrator.registry import register_engine

@register_engine("<name>")
class MyEngine:
    ui_contribution = {
        "id": "<name>",
        "partials": {"execute": "modules/orchestrator_<name>/<name>-execute.html"},
        "scripts": ["modules/orchestrator_<name>/<name>-execute.js"],
        "modals": [],
    }
    meta = EngineMeta(
        label="My Engine",
        description="...",
    )

    @classmethod
    def create(cls, *, run_context, **kw):
        return cls(run_context=run_context)

    def __init__(self, run_context=None, **kwargs):
        self.run_context = run_context

    async def run(self, request: EngineRequest) -> ExecutionResult:
        ...
```

**Minimal `<name>-execute.js`:**

```javascript
(function() {
    registerExecuteSlice('<name>', function() {
        return {
            initExecute() {},
            handleNodes(nodes) {},
            handleStatus(status) {},
            handleLog(log) {},
        };
    });
})();
```

### <a name="new-manager"></a> New Manager

There are currently **3 manager implementations**:

| Manager | Registered name | Description |
|---------|----------------|-------------|
| `tree/` | `"tree"` | LLM-guided tree search with optional active/dormant layering |
| `direct/` | `"direct"` | Returns all skills without filtering (designed for free-style engine) |
| `vector/` | `"vector"` | ChromaDB vector similarity search |

To add a new manager, create 3 files:

| # | File | Purpose |
|---|------|---------|
| 1 | `src/manager/<name>/__init__.py` | Manager class with `@register_manager` |
| 2 | `src/web/templates/modules/manager_<name>/*.html` | Search / review partials |
| 3 | `src/web/static/js/modules/manager_<name>/*.js` | Corresponding JS |

**Minimal `__init__.py`:**

```python
from manager.base import BaseManager, RetrievalResult
from manager.registry import register_manager

@register_manager("<name>")
class MyManager:
    ui_contribution = {
        "partials": {
            "search": "modules/manager_<name>/<name>-search.html",
            "review": "modules/manager_<name>/<name>-review.html",
        },
        "scripts": ["modules/manager_<name>/<name>-search.js"],
        "modals": [],
    }

    def build(self, skills_dir=None, output_path=None, verbose=False,
              show_tree=True, generate_html=True) -> dict: ...
    def search(self, query: str, verbose: bool = False) -> RetrievalResult: ...
    def get_visual_data(self): return None
    @property
    def visual_type(self) -> str: return "<name>"
```

---

## Appendix

### <a name="call-chains"></a> Call Chains

**Web UI:**
```
Browser → WebSocket → routes.py → service.py → manager + orchestrator
```

**CLI Batch:**
```
cli.py cmd_run → workflow/executor.BatchExecutor → batch.run_batch()
  → service.run_task() → manager + orchestrator
```

**CLI Build:**
```
cli.py cmd_build → manager.create_manager() → tree/builder.TreeBuilder
  (with layering) → layer_processor → dormant_indexer
```

**CLI Update-layer:**
```
cli.py cmd_update_layer → manager/tree/layer_processor (directory mode)
                        → manager/tree/scheduled_updater (install-count mode)
                        → dormant_indexer
```

### Design Patterns

| Pattern | Where |
|---------|-------|
| Plugin / Registry | `orchestrator/registry.py`, `manager/registry.py` |
| Protocol (structural subtyping) | `manager/base.py`, `orchestrator/base.py`, `visualizers/protocol.py` |
| Factory | `create_engine()`, `create_manager()` |
| Strategy | `dag/engine.py`, `direct/engine.py`, `freestyle/engine.py` |
| Layered Search (fallback) | `tree/layered_searcher.py` — active tree first, dormant vector fallback |
| Vector Index | `manager/vector/indexer.py`, `tree/dormant_indexer.py` — ChromaDB embedding store |
| Context / Environment | `runtime/run_context.py` |
| State Machine | `web/state.py` |
| Event / Callback | `tree/searcher.py`, `web/visualizer.py` |
