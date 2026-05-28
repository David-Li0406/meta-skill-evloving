# Reference: Semantic Graph Analysis (llm-tldr)

## Overview
`llm-tldr` provides a graph-based view of the project. It doesn't just see files; it sees relationships (Callers, Callees, Importers, Exporters).

## 🛠️ MCP Toolset Usage

### 1. `tldr callers [function_name]`
**Goal:** Identify the "Blast Radius" of a change.
If you rename a function, run this to find every single place that will break.

### 2. `tldr callee [function_name]`
**Goal:** Understand the implementation details of a function without reading the full body.
It lists all the internal calls, giving you a functional overview.

### 3. `tldr context [entry_point] --depth 2`
**Goal:** The "Gold Standard" for context retrieval.
It recursively finds every type, constant, and utility function required by the entry point up to 2 levels deep. This is the ultimate "Token Saver."

---

## 🔍 Semantic Search Strategy
When text-based `grep` (ripgrep) fails because the naming is inconsistent, use `tldr semantic`.

**Effective Queries:**
- "Where is the main entry point for the payment gateway?"
- "Find the logic that handles JWT token rotation."
- "Show me all components that use the 'Bento Grid' layout."

---

## 🏗️ Architectural Audits
Use `tldr arch` to detect:
- **Circular Dependencies:** Where File A imports File B, which imports File A. (High technical debt).
- **Layer Violations:** Where the UI layer directly imports the DB layer, bypassing the API.
- **Dead Code:** Functions or classes that have 0 callers and 0 importers.

## 🏁 Summary
The graph is the truth. The file is just a container. Master the graph to master the codebase.
