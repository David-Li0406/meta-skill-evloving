---
name: scientific-app-scaffold
description: Scaffolds a high-performance scientific GUI application using a Data-Centric Architecture (PyQt+Visualization).
---

# Scientific App Scaffold Skill

Use this skill to initialize or restructure high-performance scientific/engineering applications. It provides a robust foundation for applications that require heavy computation, complex data visualization, and a responsive GUI.

## 1. Architectural Principles

- **Data-Centric Design**: A central `ScientificData` DTO (Data Transfer Object) acts as the single source of truth, passed between Loaders, Analyzers, and Visualizers.
- **Pipeline Architecture**:
  - **Input**: `loaders/` strategies for different file formats.
  - **Compute**: `algorithms/` for heavy calculations (CPU/GPU).
  - **Output/View**: `visualization/` for rendering (2D generic or 3D PyVista).
- **Separation of Concerns**:
  - `core/`: core data structures and abstract interfaces.
  - `gui/`: UI logic (Widgets, Panels), strictly decoupled from computation.
  - `config.py`: Centralized configuration for physical constants and thresholds.

## 2. Directory Structure Template

```
project_root/
  ├── config.py              # Centralized constants & thresholds
  ├── App.py                 # Application Entry Point
  ├── core/
  │   ├── __init__.py
  │   ├── base.py            # ScientificData, Abstract Interfaces
  │   └── computational_backend.py  # Resource manager (e.g., GPU/Thread pool)
  ├── loaders/
  │   ├── __init__.py
  │   └── [format]_loader.py # Specific format strategies
  ├── algorithms/            # Domain-specific logic
  │   ├── __init__.py
  │   └── [domain]_algo.py
  ├── visualization/         # Rendering Tier
  │   ├── __init__.py
  │   ├── engine.py          # Framework-agnostic rendering logic
  │   └── cameras.py         # View/Camera management
  └── gui/
      ├── __init__.py
      ├── styles.py          # Centralized QSS/Theming
      ├── main_window.py     # Main Layout
      └── panels/            # Domain-specific control panels
          └── [context]_panel.py
```

## 3. Core Boilerplate

### `core/base.py`

```python
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

@dataclass
class ScientificData:
    """Generic DTO for scientific data."""
    primary_data: Any = None      # The main array/tensor/mesh
    secondary_data: Any = None    # Auxiliary data (e.g., derived results)
    spatial_info: Dict = field(default_factory=dict) # Spacing, Origin, Units
    metadata: Dict = field(default_factory=dict)     # Experiment ID, Timestamp

class BaseLoader(ABC):
    @abstractmethod
    def load(self, source: str) -> ScientificData:
        pass

class BaseAnalyzer(ABC):
    @abstractmethod
    def process(self, data: ScientificData, **params) -> ScientificData:
        pass

class BaseVisualizer(ABC):
    @abstractmethod
    def set_data(self, data: ScientificData):
        pass
```

### `config.py`

```python
# System Limits
MAX_MEMORY_MB = 1024
USE_GPU_ACCELERATION = True

# GUI Settings
DEFAULT_THEME = "Dark"
WINDOW_SIZE = (1280, 800)
```

## 4. Visual Style Guidelines

- **Theme**: "Scientific Dark" (reduces eye strain for data analysts).
- **Layout**:
  - **Central View**: Large viewport for Visualization (2D Plot/3D Canvas).
  - **Sidebars**: Collapsible "Parameters" (Controls) and "Data Tree" (Explorer).
- **Feedback**:
  - Status Bar for quick messages.
  - Progress Panels for threaded operations.

## 5. Implementation Steps

1. **Define Domain Data**: subclass `ScientificData` in `core/base.py` to fit specific domain needs (e.g., `SeismicVolume`, `MolecularStructure`).
2. **Establish Pipeline**: Implement at least one `Loader` and one `Visualizer`.
3. **Build GUI Frame**: Create `gui/main_window.py` connecting the Visualizer to the central widget.
4. **Connect Signals**: Use an Event Bus or Signals (PyQt) to propagate `data_loaded` or `params_changed` events.
