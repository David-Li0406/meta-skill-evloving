---
name: doc-update
description: Update vive docs to match code changes.
---

# Documentation Update Guide (vive)

コード変更に合わせてドキュメントを更新する。

## Mapping: Code to Docs

コード変更の種類に応じて更新先を決定する。

| Code Change Type    | Affected Files (src/)              | Target Doc (docs/)       | Action                                                    |
| :------------------ | :--------------------------------- | :----------------------- | :-------------------------------------------------------- |
| **Concept/Vision**  | N/A                                | `concept.md`             | Update high-level vision or core philosophy.              |
| **Architecture**    | `main.rs`, `core/`, `orchestrator/`| `architecture.md`        | Update component design, data flow, or tech stack details.|
| **Requirements**    | New features, CLI args             | `requirements.md`        | Update functional requirements list.                      |
| **UI/TUI Layout**   | `ui/`, `tui/`                      | `architecture.md`        | Update TUI layer descriptions.                            |

## Consistency Checklist

- [ ] Does `architecture.md` accurately reflect the current Rust struct/module structure?
- [ ] Are all implemented features marked as completed in `requirements.md`?
- [ ] Do unit/integration tests match the requirements?
