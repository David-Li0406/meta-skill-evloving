# Board SDK Vendor Documentation Index

Complete index of Board SDK documentation available in this skill.

## Documentation Location

All vendor documentation is in [`vendor-docs/`](vendor-docs/) (local to this skill).

---

## Overview

| File | Description |
| ---- | ----------- |
| [overview.md](vendor-docs/overview.md) | SDK introduction, what it provides (Input, Session, Save, Pause) |

---

## Get Started (4 files)

Step-by-step setup guides for new projects.

| File | Description |
| ---- | ----------- |
| [Installation.md](vendor-docs/get-started/Installation.md) | SDK package installation, BDB tool setup, Piece Set models |
| [project-setup.md](vendor-docs/get-started/project-setup.md) | Android settings, Input System, BoardInputSettings, Application ID |
| [build-deploy.md](vendor-docs/get-started/build-deploy.md) | APK building, BDB commands (install, launch, logs, stop) |
| [sample-scene.md](vendor-docs/get-started/sample-scene.md) | Importing and running the SDK sample scene |

---

## Learn (5 files)

Conceptual understanding of Board hardware and SDK architecture.

| File | Description |
| ---- | ----------- |
| [architecture.md](vendor-docs/learn/architecture.md) | SDK component overview: BoardInput, BoardSession, BoardApplication, BoardSaveGameManager |
| [concepts.md](vendor-docs/learn/concepts.md) | Core terminology: Piece, Glyph, Contact, Phase, Tracking, Noise Rejection |
| [hardware.md](vendor-docs/learn/hardware.md) | Display specs (1920x1080), processor (MediaTek Genio 700), storage, ports |
| [pieces.md](vendor-docs/learn/pieces.md) | Physical Piece detection, position/rotation/touch state, glyph patterns |
| [touch-system.md](vendor-docs/learn/touch-system.md) | Unlimited contacts, dedicated NPU, noise rejection, contact lifecycle |

---

## Guides (6 files)

Implementation guides for specific features.

| File | Description |
| ---- | ----------- |
| [touch-input.md](vendor-docs/guides/touch-input.md) | Contact handling, filtering by type, phase processing, debug overlay (264 lines) |
| [simulator.md](vendor-docs/guides/simulator.md) | Editor simulation setup, placing/moving/rotating contacts, keyboard shortcuts |
| [pause-menu.md](vendor-docs/guides/pause-menu.md) | SetPauseScreenContext, custom buttons, audio sliders, exit handling |
| [player-management.md](vendor-docs/guides/player-management.md) | BoardSession.players, Profile vs Guest, player change events |
| [profile-switcher.md](vendor-docs/guides/profile-switcher.md) | ShowProfileSwitcher/HideProfileSwitcher, when to show/hide |
| [save-game-system.md](vendor-docs/guides/save-game-system.md) | CreateSaveGame, metadata, cover images, storage quotas, player associations |

---

## Reference (10 files)

Complete API documentation for all SDK classes.

| File | Classes/Content |
| ---- | --------------- |
| [README.md](vendor-docs/reference/README.md) | API overview, namespace index, common workflows |
| [Board.Core.md](vendor-docs/reference/Board.Core.md) | BoardApplication, BoardLogger, BoardPlayer, BoardPauseCustomButton |
| [Board.Input.md](vendor-docs/reference/Board.Input.md) | BoardInput, BoardContact, BoardContactPhase, BoardInputSettings, BoardUIInputModule (575 lines) |
| [Board.Input.Debug.md](vendor-docs/reference/Board.Input.Debug.md) | BoardInputDebugView, BoardContactDebugView |
| [Board.Input.Simulation.md](vendor-docs/reference/Board.Input.Simulation.md) | BoardContactSimulation, BoardContactSimulationSettings, BoardContactSimulationIcon |
| [Board.Session.md](vendor-docs/reference/Board.Session.md) | BoardSession, BoardSessionPlayer |
| [Board.Save.md](vendor-docs/reference/Board.Save.md) | BoardSaveGameManager, BoardSaveGameMetadata, BoardSaveGameMetadataChange |
| [enums.md](vendor-docs/reference/enums.md) | BoardContactType, BoardContactPhase, BoardPlayerType, BoardPauseAction, BoardLogLevel |
| [delegates.md](vendor-docs/reference/delegates.md) | Event handler signatures |

---

## Sample Project

SDK sample code demonstrating input handling patterns.

**Location:** `Assets/Samples/Board SDK/3.0.0/Input/`

| File | Demonstrates |
| ---- | ------------ |
| `Scripts/BoardInputManager.cs` | Contact lifecycle, Dictionary tracking by contactId, Update loop structure |
| `Scripts/BoardContactDebugInfo.cs` | Visualization, screen-to-world coordinate conversion, Y-axis flip |
| `Scenes/BoardInput.unity` | Complete scene setup with input handling |

See [sample-code-guide.md](sample-code-guide.md) for a detailed walkthrough.

---

## Online Resources

- **API Reference**: [https://harris-hill.github.io/board-docs/api/](https://harris-hill.github.io/board-docs/api/) (source of truth)
- **SDK Guides**: [https://harris-hill.github.io/board-docs/guides/](https://harris-hill.github.io/board-docs/guides/)

---

## Quick Reference: Namespace to File

| Namespace | Reference File | Key Classes |
| --------- | -------------- | ----------- |
| `Board.Core` | [Board.Core.md](vendor-docs/reference/Board.Core.md) | BoardApplication, BoardLogger |
| `Board.Input` | [Board.Input.md](vendor-docs/reference/Board.Input.md) | BoardInput, BoardContact |
| `Board.Input.Debug` | [Board.Input.Debug.md](vendor-docs/reference/Board.Input.Debug.md) | BoardInputDebugView |
| `Board.Input.Simulation` | [Board.Input.Simulation.md](vendor-docs/reference/Board.Input.Simulation.md) | BoardContactSimulation |
| `Board.Session` | [Board.Session.md](vendor-docs/reference/Board.Session.md) | BoardSession |
| `Board.Save` | [Board.Save.md](vendor-docs/reference/Board.Save.md) | BoardSaveGameManager |

---

## Class Counts by Namespace

| Namespace | Classes | Structs | Enums |
| --------- | ------- | ------- | ----- |
| Board.Core | 7 | 5 | 4 |
| Board.Input | 4 | 3 | 2 |
| Board.Input.Debug | 2 | 0 | 0 |
| Board.Input.Simulation | 4 | 1 | 0 |
| Board.Session | 2 | 1 | 0 |
| Board.Save | 6 | 3 | 0 |
| **Total** | **25** | **13** | **6** |
