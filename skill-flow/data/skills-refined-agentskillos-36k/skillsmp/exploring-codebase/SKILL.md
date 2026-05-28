---
name: exploring-codebase
description: >-
  Performs in-depth codebase exploration at the start of a coding session. Builds comprehensive
  understanding of project structure, architecture, key components, and patterns. Use when starting
  a new session, when asked to understand or explore the codebase, when asked "what does this project
  do", when exploring unfamiliar code, or when the user asks about project structure or architecture.
---

# Codebase Exploration

Performs thorough codebase exploration to build deep understanding before coding work begins.

---

## Exploration Approach

Use the Task tool with `subagent_type: Explore` to investigate the codebase. Focus on understanding:

1. **Project purpose and structure** - README, documentation, directory layout
2. **Architecture** - Main components, how they interact, communication patterns
3. **Core code** - Key classes, data models, utilities
4. **Configuration** - How the project is configured and customized
5. **Dependencies** - External libraries and integrations
6. **Patterns and conventions** - Coding style, naming conventions, design patterns

Adapt exploration depth based on project size and complexity. For small projects, a quick overview
suffices. For large projects, explore systematically.

---

## Guiding Questions

Answer these questions during exploration:

### Architecture
- What is the main entry point or controller?
- How do components communicate (IPC, APIs, events)?
- What external systems does this integrate with?

### Patterns
- What naming conventions are used?
- What design patterns appear (factories, dataclasses, protocols)?
- How is configuration managed?

### Structure
- Where is the core business logic?
- Where are tests located?
- What build/tooling configuration exists?

---

## Output Format

Provide a structured summary including:

- Project purpose (1-2 sentences)
- Key components table
- Important files list with paths
- Notable patterns or conventions
- Any areas of complexity or concern

### Example Output

```markdown
## Project Purpose

Manages scientific data acquisition systems for the Sun Lab at Cornell University. Currently implements
the Mesoscope-VR two-photon imaging system combining brain imaging with virtual reality behavioral tasks.

## Key Components

| Component              | Location                                     | Purpose                                          |
|------------------------|----------------------------------------------|--------------------------------------------------|
| CLI Entry Points       | src/sl_experiment/command_line_interfaces/   | sl-get, sl-manage, sl-run commands               |
| Mesoscope-VR System    | src/sl_experiment/mesoscope_vr/              | Two-photon imaging with VR behavior integration  |
| Shared Components      | src/sl_experiment/shared_components/         | Cross-system utilities for all acquisition types |

## Important Files

- `src/sl_experiment/command_line_interfaces/sl_run.py` - Main experiment execution CLI
- `src/sl_experiment/command_line_interfaces/sl_manage.py` - Session and data management CLI
- `src/sl_experiment/command_line_interfaces/sl_get.py` - Data retrieval CLI
- `src/sl_experiment/mesoscope_vr/runtime.py` - Mesoscope-VR experiment runtime
- `src/sl_experiment/shared_components/session_manager.py` - Session-based data management

## Notable Patterns

- Hardware abstraction via binding classes (Zaber motors, cameras, microcontrollers)
- Shared memory IPC for GUI-runtime communication
- Session-based data management with distributed storage
- MyPy strict mode with full type annotations

## Areas of Concern

- Hardware dependencies require physical equipment for full testing
- Cross-library coordination with sl-shared-assets and ataraxis-video-system
```

---

## Usage

Invoke at session start to ensure full context before making changes. Prevents blind modifications
and ensures understanding of existing patterns.
