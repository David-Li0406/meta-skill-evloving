---
name: h3c-test-script-generation
description: Use this skill when you need to generate automated test scripts for H3C network devices, following a structured three-phase workflow and utilizing a comprehensive knowledge base for accurate implementation.
---

# Skill body

## 1. Three-Phase Workflow Framework

**Phase 1: Specification**  
Analyze user requirements and the provided `conftest.py`. Use comprehensive database retrieval and iterative analysis to produce `topoConfig.md` (topology and configuration analysis) and `spec.md` (test specifications).

**Phase 2: Tasks**  
Based on the deliverables from Phase 1, continue detailed database retrieval to produce `tasks.md` (task list).

**Phase 3: Implementation & Archiving**  
Complete coding based on the deliverables from the first two phases and ensure mandatory archiving of process documentation.

**Mandatory Delivery Order**: Complete `spec.md` and `tasks.md` before starting coding. Clean up the environment after coding is complete.

## 2. Tool Usage and Database Retrieval Standards

Utilize the following tools to retrieve information from the cloud knowledge base.  
**Retrieval Strategy (Mandatory)**: In each phase, traverse all index names. After initial retrieval, read the returned content, extract more accurate terminology or command snippets, and optimize the search terms (Description) for iterative retrieval until sufficiently precise information is obtained.

### 2.1 Retrieve Background and Environment (`background_ke`)
- **Purpose**: Find similar business backgrounds to understand the logic of the provided `conftest.py`.
- **Command**:
  ```bash
  /opt/coder/venvs/comware-test/bin/python {current_skill_path}/script/data_search_h3c_example.py --description "[business description]" --indexname "background_ke"
  ```

### 2.2 Retrieve Network Configuration (`v9_press_example`)
- **Purpose**: Find common network configurations, such as multi-segment communication configurations for switches.
- **Command**:
  ```bash
  /opt/coder/venvs/comware-test/bin/python {current_skill_path}/script/data_search_h3c_example.py --description "[configuration description]" --indexname "v9_press_example"
  ```

### 2.3 Retrieve Test Code Implementation (`example_ke`)
- **Purpose**: Find specific implementation code for test cases (Reference Code).
- **Command**:
  ```bash
  /opt/coder/venvs/comware-test/bin/python {current_skill_path}/script/data_search_h3c_example.py --description "[function description]" --indexname "example_ke"
  ```

### 2.4 Retrieve Device Command Line (`cmd_ke`)
- **Purpose**: Query specific network device command lines (CLI).
- **Command**:
  ```bash
  /opt/coder/venvs/comware-test/bin/python {current_skill_path}/script/data_search_h3c_example.py --description "[command intent]" --indexname "cmd_ke"
  ```

### 2.5 Retrieve Configuration Steps Description (`press_config_des`)
- **Purpose**: Query standardized configuration processes, parameter descriptions, and step descriptions.
- **Command**:
  ```bash
  /opt/coder/venvs/comware-test/bin/python {current_skill_path}/script/data_search_h3c_example.py --description "[configuration logic]" --indexname "press_config_des"
  ```

## 3. General Constraints and Principles

### 3.1 Code Generation Principles
- **Single Requirement/Single Script**: Generate one script file per test requirement.
- **No Empty Files**: Prohibit the generation of useless `__init__.py`.
- **Clear Module Imports**: Ensure header files clearly import necessary modules:
  ```python
  import pytest
  from pytest_atf.atf_globalvar import globalVar as gl
  from pytest_atf import run_multithread, atf_assert, atf_check, atf_skip, atf_logs
  ```

### 3.2 Documentation Reference Standards
All designs and code implementations must be traceable:
- **Background Environment**: Refer to the user-provided `conftest.py`, supplemented by `background_ke`.
- **Business Logic**: Sourced from `v9_press_example` / `press_config_des`.
- **Code References**: Sourced from `example_ke`.
- **Specific Commands**: Sourced from `cmd_ke`.

### 3.3 Device and Configuration Consistency
- **Naming Consistency**: Device names in scripts (e.g., `gl.DUTx`) must strictly correspond to those in the `.topox` topology file.
- **Configuration Priority**: **Prioritize reusing configurations provided by the user in the directory**.
- **Mandatory Cleanup**: All `teardown_class` must implement complete configuration cleanup logic.