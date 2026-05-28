---
name: modifying-mesoscope-vr-system
description: >-
  Guides modifications to the Mesoscope-VR acquisition system, including adding new hardware, creating runtime modes,
  and extending the system with new components. Routes to specialized guides for specific tasks.
---

# Modifying the Mesoscope-VR System

This skill guides modifications to the Mesoscope-VR acquisition system in sl-experiment. It routes to specialized
guides based on the type of modification.

---

## Task Router

**Determine which guide to read based on your task:**

| Task                                         | Guide to Read                                  |
|----------------------------------------------|------------------------------------------------|
| Add camera, sensor, motor, or other hardware | [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md)         |
| Add microcontroller-based hardware module    | [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md)         |
| Create new training mode (like lick/run)     | [RUNTIME_MODE_GUIDE.md](RUNTIME_MODE_GUIDE.md) |
| Add new system state (IDLE, REST, RUN, etc.) | [RUNTIME_MODE_GUIDE.md](RUNTIME_MODE_GUIDE.md) |
| Create new runtime logic function            | [RUNTIME_MODE_GUIDE.md](RUNTIME_MODE_GUIDE.md) |
| Add new visualization mode                   | [RUNTIME_MODE_GUIDE.md](RUNTIME_MODE_GUIDE.md) |
| Add new CLI command for sessions             | [RUNTIME_MODE_GUIDE.md](RUNTIME_MODE_GUIDE.md) |
| Create new session descriptor                | [RUNTIME_MODE_GUIDE.md](RUNTIME_MODE_GUIDE.md) |

---

## When to Use This Skill

Use this skill when:

- Adding new hardware (cameras, sensors, motors) to mesoscope-vr
- Modifying existing hardware configuration parameters
- Creating new training modes or session types
- Adding new system states for runtime behavior
- Integrating new binding classes into data_acquisition.py
- Updating CLI commands for mesoscope-vr
- Understanding the mesoscope-vr architecture

**For other tasks, use these skills instead:**

| Task                                         | Use This Skill               |
|----------------------------------------------|------------------------------|
| Low-level camera API (ataraxis-video-system) | `/camera-interface`          |
| Low-level microcontroller firmware           | `/microcontroller-interface` |

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                              sl-shared-assets                                  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  mesoscope_configuration.py                                              │  │
│  │  ───────────────────────────                                             │  │
│  │  MesoscopeFileSystem       - Storage paths                               │  │
│  │  MesoscopeCameras          - Camera indices, encoding params             │  │
│  │  MesoscopeMicroControllers - Port assignments, thresholds                │  │
│  │  MesoscopeExternalAssets   - Zaber motor ports, Google Sheets            │  │
│  │  MesoscopeSystemConfiguration - Container with all components            │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  mesoscope_descriptors.py                                                │  │
│  │  ────────────────────────                                                │  │
│  │  LickTrainingDescriptor     - Lick training session parameters           │  │
│  │  RunTrainingDescriptor      - Run training session parameters            │  │
│  │  MesoscopeExperimentDescriptor - Experiment session parameters           │  │
│  │  WindowCheckingDescriptor   - Window checking session parameters         │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  session_data.py                                                         │  │
│  │  ───────────────                                                         │  │
│  │  SessionTypes              - Enumeration of valid session types          │  │
│  │  SessionData               - Session metadata and file hierarchy         │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────┬──────────────────────────────────────────────┘
                                  │ imports configuration
┌─────────────────────────────────▼──────────────────────────────────────────────┐
│                              sl-experiment                                     │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  binding_classes.py                                                      │  │
│  │  ──────────────────                                                      │  │
│  │  ZaberMotors              - Motor position management                    │  │
│  │  MicroControllerInterfaces - AMC communication                           │  │
│  │  VideoSystems             - Camera frame acquisition                     │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  data_acquisition.py                                                     │  │
│  │  ───────────────────                                                     │  │
│  │  _MesoscopeVRStates       - System state enumeration (IDLE, REST, etc.)  │  │
│  │  _MesoscopeVRSystem       - Hardware orchestration and state machine     │  │
│  │  lick_training_logic()    - Lick training runtime function               │  │
│  │  run_training_logic()     - Run training runtime function                │  │
│  │  experiment_logic()       - Experiment runtime function                  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  visualizers.py                                                          │  │
│  │  ──────────────                                                          │  │
│  │  VisualizerMode           - Display mode enumeration                     │  │
│  │  BehaviorVisualizer       - Real-time behavior plotting                  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │  command_line_interfaces/execute.py                                      │  │
│  │  ──────────────────────────────────                                      │  │
│  │  lick_training()          - CLI command for lick training                │  │
│  │  run_training()           - CLI command for run training                 │  │
│  │  experiment()             - CLI command for experiments                  │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## Verification Requirements

**Before modifying system code, verify the current state of dependent libraries.**

Follow the **Cross-Referenced Library Verification** procedure in `CLAUDE.md`:

1. Check local sl-shared-assets version against GitHub
2. If version mismatch exists, ask the user how to proceed
3. Use the verified source for configuration patterns

### Files to Verify

| Repository       | File                                                | What to Check                         |
|------------------|-----------------------------------------------------|---------------------------------------|
| sl-shared-assets | `configuration/mesoscope_configuration.py`          | Current dataclass structure           |
| sl-shared-assets | `configuration/mesoscope_descriptors.py`            | Descriptor dataclass structure        |
| sl-shared-assets | `data/session_data.py`                              | SessionTypes enumeration              |
| sl-shared-assets | `configuration/configuration_utilities.py`          | Registry patterns                     |
| sl-experiment    | `mesoscope_vr/binding_classes.py`                   | Binding class patterns                |
| sl-experiment    | `mesoscope_vr/data_acquisition.py`                  | Lifecycle integration                 |
| sl-experiment    | `mesoscope_vr/visualizers.py`                       | Visualization patterns                |

### Pre-Implementation Hardware Verification

**Before implementing hardware modifications, verify the target hardware is connected and accessible.**

Use MCP tools to confirm hardware connectivity before writing integration code:

| Hardware Type    | Verification Skill           | MCP Tool                   | MCP Server              |
|------------------|------------------------------|----------------------------|-------------------------|
| Cameras          | `/camera-interface`          | `list_cameras()`           | ataraxis-video-system   |
| Microcontrollers | `/microcontroller-interface` | `list_microcontrollers()`  | ataraxis-comm-interface |
| Zaber motors     | `/zaber-interface`           | `get_zaber_devices_tool()` | sl-experiment           |

**Verification workflow:**

1. Start the appropriate MCP server for the hardware type
2. Run the discovery tool to confirm the hardware is detected
3. Note hardware identifiers (camera indices, serial ports, device numbers)
4. If hardware is not detected, troubleshoot connectivity before proceeding

This ensures the target hardware is accessible and properly configured before writing binding class code. Implementing
code for hardware that cannot be verified leads to untestable integration.

---

## Guide Summaries

### HARDWARE_GUIDE.md

Covers adding physical hardware components to the mesoscope-vr system:

- Configuration dataclasses in sl-shared-assets
- Binding classes in sl-experiment
- Integration into `_MesoscopeVRSystem` lifecycle
- Microcontroller module integration patterns
- System ID allocation

### RUNTIME_MODE_GUIDE.md

Covers creating new runtime modes and session types:

- System state enumeration (`_MesoscopeVRStates`)
- State transition methods in `_MesoscopeVRSystem`
- Runtime logic functions (like `lick_training_logic()`)
- Visualization modes (`VisualizerMode`)
- Session descriptors for parameter persistence
- CLI command registration
- SessionTypes enumeration in sl-shared-assets

---

## Quick Decision Tree

```
Need to modify mesoscope-vr?
│
├── Adding physical hardware?
│   ├── Camera → Read HARDWARE_GUIDE.md, use /camera-interface for API details
│   ├── Microcontroller module → Read HARDWARE_GUIDE.md, use /microcontroller-interface for firmware
│   └── Other device (motor, etc.) → Read HARDWARE_GUIDE.md
│
├── Creating new training/session mode?
│   └── Read RUNTIME_MODE_GUIDE.md
│
├── Adding system state (like REST, RUN)?
│   └── Read RUNTIME_MODE_GUIDE.md
│
└── Adding CLI command?
    └── Read RUNTIME_MODE_GUIDE.md
```

---

## Proceed to Guide

Based on your task, read the appropriate guide file in this skill directory:

- **Hardware modifications**: Read [HARDWARE_GUIDE.md](HARDWARE_GUIDE.md)
- **Runtime mode modifications**: Read [RUNTIME_MODE_GUIDE.md](RUNTIME_MODE_GUIDE.md)
