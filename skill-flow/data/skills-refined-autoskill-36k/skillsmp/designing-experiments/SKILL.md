---
name: designing-experiments
description: >-
  Interactive guidance for building Sun lab VR experiment configurations using MCP tools and CLI commands. Covers
  template discovery, experiment configuration generation, and Unity template creation. Use when creating new
  experiments, modifying experiment configurations, or when the user asks about experiment design.
---

# Experiment Design Skill

Provides guidance for interactively building Sun lab experiment configurations. This skill documents the available MCP
tools for project management, template discovery, configuration generation, and validation.

---

## Prerequisites

**Before generating experiment configurations, you MUST verify the acquisition system is properly configured.**

Use the `/acquisition-system-setup` skill to confirm:
1. Working directory is set and accessible
2. Task templates directory is configured and points to sl-unity-tasks Configurations folder
3. System configuration file exists with valid parameters

If these prerequisites are not met, the MCP tools will fail. The acquisition-system-setup skill provides MCP tools for
verification and initial setup.

### Task Templates Directory Verification

**You MUST verify and resolve the task templates directory before template discovery.** Use these MCP tools:

| Tool                                | Purpose                                           |
|-------------------------------------|---------------------------------------------------|
| `get_task_templates_directory_tool` | Returns current path or error if not configured   |
| `set_task_templates_directory_tool` | Sets path to sl-unity-tasks Configurations folder |

**Verification workflow:**

```text
1. Check current configuration:
   get_task_templates_directory_tool()
   -> Task templates directory: /path/to/sl-unity-tasks/Assets/InfiniteCorridorTask/Configurations
   OR
   -> Error: Task templates directory is not configured.

2. If not configured or path is invalid, resolve with user:
   - Ask user for the path to their sl-unity-tasks project
   - The correct path is: {sl-unity-tasks}/Assets/InfiniteCorridorTask/Configurations/
   - Set using: set_task_templates_directory_tool(directory="/path/to/Configurations")

3. Verify templates are accessible:
   list_available_templates_tool()
   -> Available templates: MF_Reward, SSO_Shared_Base, ...
```

**If `list_available_templates_tool` returns an error**, the task templates directory is not correctly configured.
Resolve the path before proceeding with experiment creation.

---

## Tool Availability Overview

The experiment design workflow uses MCP tools as the primary interface, with YAML editing for customization:

| Approach     | Purpose                                            | Tools                                                        |
|--------------|----------------------------------------------------|--------------------------------------------------------------|
| MCP Tools    | Project management, template discovery, generation | `create_project_tool`, `create_experiment_config_tool`, etc. |
| YAML Editing | Customization after generation                     | Direct file editing                                          |

---

## MCP Tools for Experiment Design

Two MCP servers provide tools for experiment design. For system setup and verification tools, see the
`/acquisition-system-setup` skill.

| Server           | Start Command      | Purpose                                          |
|------------------|--------------------|--------------------------------------------------|
| sl-shared-assets | `sl-configure mcp` | Template discovery                               |
| sl-experiment    | `sl-get mcp`       | Project and experiment management, validation    |

### Available Tools

**Task Templates Configuration (sl-shared-assets):**

| Tool                               | Purpose                                                     |
|------------------------------------|-------------------------------------------------------------|
| `get_task_templates_directory_tool`| Returns current path to Unity Configurations folder         |
| `set_task_templates_directory_tool`| Sets path to sl-unity-tasks Configurations folder           |
| `list_available_templates_tool`    | Lists all available task templates as YAML files            |
| `get_template_info_tool`           | Returns template details (cues, segments, trial structures) |

**Project and Experiment Management (sl-experiment):**

| Tool                            | Purpose                                                     |
|---------------------------------|-------------------------------------------------------------|
| `get_projects_tool`             | Lists existing projects                                     |
| `create_project_tool`           | Creates a new project directory structure                   |
| `get_experiments_tool`          | Lists experiments in a project                              |
| `get_experiment_info_tool`      | Returns detailed experiment configuration summary           |
| `create_experiment_config_tool` | Creates experiment configuration from a template            |

### Tool Parameters

**create_project_tool:**

| Parameter | Required | Description                    |
|-----------|----------|--------------------------------|
| `project` | Yes      | Name of the project to create  |

**create_experiment_config_tool:**

| Parameter     | Required | Default | Description                                      |
|---------------|----------|---------|--------------------------------------------------|
| `project`     | Yes      | -       | Name of the project                              |
| `experiment`  | Yes      | -       | Name for the experiment (filename without .yaml) |
| `template`    | Yes      | -       | Template name (without .yaml extension)          |
| `state_count` | No       | 1       | Number of experiment states to generate          |

Trial-specific parameters (reward size, puff duration, etc.) use sensible defaults. Customize these values by editing
the generated YAML file based on user requirements.

---

## Workflow Checklist

Copy this checklist when creating a new experiment:

```text
Experiment Creation Progress:
- [ ] Step 1: Verify system configuration (/acquisition-system-setup skill)
- [ ] Step 2: Verify task templates directory (get_task_templates_directory_tool)
- [ ] Step 3: If not configured, set path to sl-unity-tasks Configurations (set_task_templates_directory_tool)
- [ ] Step 4: Check if project exists (get_projects_tool), create if needed (create_project_tool)
- [ ] Step 5: Discover available templates (list_available_templates_tool)
- [ ] Step 6: Review template details (get_template_info_tool)
- [ ] Step 7: Check if experiment exists (get_experiments_tool)
- [ ] Step 8: Generate experiment configuration (create_experiment_config_tool)
- [ ] Step 9: Edit YAML to customize experiment states and trial parameters
- [ ] Step 10: Validate configuration (see VALIDATION_GUIDE.md)
```

---

## Template-Based Workflow

Experiment configurations are created from task templates stored in the sl-unity-tasks project. Templates define the VR
structure (cues, segments, trial zones) which cannot be modified after creation. Only experiment-specific parameters can
be customized via YAML editing.

### What Comes From Templates (Read-Only)

- Cues (visual patterns with unique codes and lengths)
- Segments (cue sequences with optional transition probabilities)
- VR environment settings (corridor spacing, depth, padding prefab)
- Trial zone positions (trigger zones, stimulus locations)
- Trigger types (determines which trial class is used for each trial structure)

### What Can Be Customized (YAML Editing)

- Experiment states (phases like baseline, experiment, cooldown)
- Trial-specific parameters (determined by trial class, e.g., reward size, puff duration)
- State guidance parameters (initial/recovery guided trials, thresholds)

### Supported Trial Types

Trial types are defined in `sl-shared-assets/src/sl_shared_assets/configuration/experiment_configuration.py`. Each trial
type has its own customizable parameters.

**You MUST verify supported trial types before configuring experiments** by reading the trial classes in
`experiment_configuration.py`. Currently supported types include `WaterRewardTrial` and `GasPuffTrial`, but this may
be extended in the future.

---

## Understanding Experiment States

Experiment states define the phases of a data acquisition session. Each state controls the hardware configuration and
trial behavior for that phase of the experiment.

### State Code Fields

| Field                   | Purpose                                                                        |
|-------------------------|--------------------------------------------------------------------------------|
| `experiment_state_code` | Unique identifier for this experiment phase (any positive integer, e.g., 1-10) |
| `system_state_code`     | Hardware configuration to use during this phase (must be a valid system state) |
| `state_duration_s`      | Duration of this phase in seconds                                              |
| `supports_trials`       | Whether experiment trials are executed during this phase (`true` or `false`)   |

### System State Codes

The `system_state_code` determines the hardware configuration during each experiment phase. Each acquisition system
defines its own state codes in its runtime module at `src/sl_experiment/<system>/data_acquisition.py`.

**You MUST verify valid system state codes before configuring experiments:**

1. Read the system's state enumeration to see all defined states and their codes
2. Search for `system_state_code` validation logic to determine which codes are valid for experiment configurations
3. Not all system states may be valid for experiments (e.g., idle or training-specific states)

**Example (Mesoscope-VR):** The `_MesoscopeVRStates` enum defines codes 0-4, but only codes 1 (REST) and 2 (RUN) are
valid for experiment configurations. Other systems will have different states and codes.

### Typical Experiment State Structure

Most experiments use a three-phase structure. The example below uses Mesoscope-VR codes - verify actual codes for the
target system:

| Phase      | experiment_state_code | system_state_code | supports_trials | Purpose                        |
|------------|-----------------------|-------------------|-----------------|--------------------------------|
| baseline   | 1                     | 1 (REST)          | false           | Pre-experiment resting period  |
| experiment | 2                     | 2 (RUN)           | true            | Active trial execution         |
| cooldown   | 3                     | 1 (REST)          | false           | Post-experiment resting period |

### Guidance Parameters

Guidance parameters control how the system assists animals during trials when they fail to perform correctly.

**Reinforcing (Water Reward) Trial Guidance:**

| Parameter                               | Description                                                      |
|-----------------------------------------|------------------------------------------------------------------|
| `reinforcing_initial_guided_trials`     | Number of guided trials at the start of the experiment state     |
| `reinforcing_recovery_failed_threshold` | Number of consecutive failures before enabling recovery guidance |
| `reinforcing_recovery_guided_trials`    | Number of guided trials to provide during recovery               |

**Aversive (Gas Puff) Trial Guidance:**

| Parameter                            | Description                                                             |
|--------------------------------------|-------------------------------------------------------------------------|
| `aversive_initial_guided_trials`     | Number of guided trials at the start of the experiment state            |
| `aversive_recovery_failed_threshold` | Number of consecutive failures before enabling recovery guidance        |
| `aversive_recovery_guided_trials`    | Number of guided trials to provide during recovery                      |

**Guidance Modes:**
- **Lick trials (reinforcing):** In guidance mode, the animal receives the reward upon colliding with the stimulus
  boundary without needing to lick.
- **Occupancy trials (aversive):** In guidance mode, the system locks the treadmill brake when the animal exits the
  occupancy zone early, preventing them from reaching the armed boundary.

**Fully Guided Phases:** To make an entire phase fully guided (all trials use guidance mode), set
`initial_guided_trials` to a very high number (e.g., 10000) and set both `recovery_failed_threshold` and
`recovery_guided_trials` to 0.

Set all guidance parameters to 0 for phases where trials are disabled (`supports_trials: false`).

---

## Interactive Design Workflow

### 1. Verify System Configuration

Use the `/acquisition-system-setup` skill to verify the system is properly configured before proceeding.

### 2. Verify Task Templates Directory

Check if the task templates directory is configured:

```text
get_task_templates_directory_tool()
-> Task templates directory: /path/to/sl-unity-tasks/Assets/InfiniteCorridorTask/Configurations
```

If the tool returns an error or the path is incorrect, resolve it with the user:

```text
Agent: The task templates directory is not configured. This should point to your sl-unity-tasks project's
       Configurations folder. What is the path to your sl-unity-tasks project?

User: /home/user/projects/sl-unity-tasks

Agent: Setting the task templates directory...
set_task_templates_directory_tool(directory="/home/user/projects/sl-unity-tasks/Assets/InfiniteCorridorTask/Configurations")
-> Task templates directory set to: /home/user/projects/sl-unity-tasks/Assets/InfiniteCorridorTask/Configurations
```

### 3. Check and Create Project

Check if the target project exists:

```text
get_projects_tool()
-> Projects: project_a, project_b, ...
```

If the project does not exist, create it:

```text
create_project_tool(project="my_project")
-> Project created: my_project at /path/to/my_project
```

### 4. Discover Templates

List available templates:

```text
list_available_templates_tool()
-> Available templates: MF_Aversion_Reward, MF_Reward, SSO_Connection, SSO_Merging, SSO_Shared_Base, ...
```

Get template details:

```text
get_template_info_tool(template_name="MF_Reward")
-> Template: MF_Reward | Cues: [...] | Segments: [...] | Trial structures: [...]
```

Guide the user to select a template based on:
- Visual cue patterns needed for the experiment
- Number and type of trials (lick/water reward vs occupancy/gas puff)
- Segment structure and transition probabilities

### 5. Check and Create Experiment

Check if an experiment with the intended name already exists:

```text
get_experiments_tool(project="my_project")
-> Experiments for my_project: existing_exp_1, existing_exp_2, ...
```

Create the experiment configuration:

```text
create_experiment_config_tool(project="my_project", experiment="session_1", template="MF_Reward", state_count=3)
-> Experiment created: session_1 from template 'MF_Reward' at /path/to/session_1.yaml
```

### 6. Customize via YAML Editing

After generation, customize the experiment by editing the YAML file directly. Key sections to modify:

**Experiment States:**

```yaml
experiment_states:
  baseline:
    experiment_state_code: 1
    system_state_code: 0
    state_duration_s: 600.0
    supports_trials: false
    reinforcing_initial_guided_trials: 0
    reinforcing_recovery_failed_threshold: 0
    reinforcing_recovery_guided_trials: 0
    aversive_initial_guided_trials: 0
    aversive_recovery_failed_threshold: 0
    aversive_recovery_guided_trials: 0

  experiment:
    experiment_state_code: 2
    system_state_code: 0
    state_duration_s: 3000.0
    supports_trials: true
    reinforcing_initial_guided_trials: 3
    reinforcing_recovery_failed_threshold: 9
    reinforcing_recovery_guided_trials: 3
    aversive_initial_guided_trials: 3
    aversive_recovery_failed_threshold: 9
    aversive_recovery_guided_trials: 3

  cooldown:
    experiment_state_code: 3
    system_state_code: 0
    state_duration_s: 600.0
    supports_trials: false
    # All guidance parameters set to 0
```

**Trial Parameters (WaterRewardTrial):**

```yaml
trial_structures:
  ABC:
    segment_name: "Segment_abc_40cm"
    stimulus_trigger_zone_start_cm: 168.0
    stimulus_trigger_zone_end_cm: 192.0
    stimulus_location_cm: 188.0
    show_stimulus_collision_boundary: false
    trigger_type: "lick"
    cue_sequence: [1, 0, 2, 0, 3, 0]
    trial_length_cm: 240.0
    reward_size_ul: 5.0
    reward_tone_duration_ms: 300
```

**Trial Parameters (GasPuffTrial):**

```yaml
trial_structures:
  ABCD:
    segment_name: "Segment_airPuff1"
    stimulus_trigger_zone_start_cm: 107.5
    stimulus_trigger_zone_end_cm: 142.5
    stimulus_location_cm: 157.5
    show_stimulus_collision_boundary: false
    trigger_type: "occupancy"
    cue_sequence: [1, 2, 3, 4]
    trial_length_cm: 200.0
    puff_duration_ms: 100
    occupancy_duration_ms: 1000
```

### 7. Validate Configuration

After editing, manually validate the configuration using the [VALIDATION_GUIDE.md](VALIDATION_GUIDE.md) checklist.

Key validations:
- System state codes are valid for the target acquisition system (verify against source code)
- Trial zone positions are properly ordered (end >= start, stimulus >= start)
- Guidance parameters are non-negative and consistent with trial types present
- States with `supports_trials: false` have all guidance parameters set to 0

---

## Creating New Unity Templates

When existing templates do not meet experimental requirements, create new templates in the sl-unity-tasks project. This
requires editing YAML files and creating corresponding Unity prefabs.

### Template File Location

Templates are stored in: `sl-unity-tasks/Assets/InfiniteCorridorTask/Configurations/`

### Template YAML Schema

```yaml
# Project: ProjectName
# Purpose: Single sentence describing the task structure.
# Layout:  Description of segments and zone placements.
# Related: Related template names with explanations.

cue_offset_cm: 10.0  # Distance from corridor start to first cue

cues:
  - name: "Gray"
    code: 0           # Unique uint8 code (0-255) for MQTT communication
    length_cm: 40.0   # Length of cue in centimeters

  - name: "A"
    code: 1
    length_cm: 40.0

segments:
  - name: "Segment_abc_40cm"           # Must match Unity prefab filename
    cue_sequence: ["A", "Gray", "B", "Gray", "C", "Gray"]
    transition_probabilities: [0.5, 0.5]  # Optional; uniform if omitted

vr_environment:
  corridor_spacing_cm: 20.0       # Distance between corridor instances
  segments_per_corridor: 3        # Depth for teleportation illusion
  padding_prefab_name: "Padding"  # Empty corridor prefab name
  cm_per_unity_unit: 10.0         # Conversion factor

trial_structures:
  ABC:
    segment_name: "Segment_abc_40cm"
    stimulus_trigger_zone_start_cm: 168.0
    stimulus_trigger_zone_end_cm: 192.0
    stimulus_location_cm: 188.0
    show_stimulus_collision_boundary: false
    trigger_type: "lick"  # or "occupancy"
```

### Template Field Reference

**Cues:**

| Field       | Type  | Required | Description                               |
|-------------|-------|----------|-------------------------------------------|
| `name`      | str   | Yes      | Visual identifier (e.g., 'A', 'Gray')     |
| `code`      | int   | Yes      | Unique uint8 code (0-255) for MQTT        |
| `length_cm` | float | Yes      | Length of cue in centimeters              |

**Segments:**

| Field                      | Type        | Required | Description                                  |
|----------------------------|-------------|----------|----------------------------------------------|
| `name`                     | str         | Yes      | Must match Unity prefab filename             |
| `cue_sequence`             | list[str]   | Yes      | Ordered list of cue names                    |
| `transition_probabilities` | list[float] | No       | Probability distribution; uniform if omitted |

**VR Environment:**

| Field                   | Type  | Required | Description                           |
|-------------------------|-------|----------|---------------------------------------|
| `corridor_spacing_cm`   | float | Yes      | Distance between parallel corridors   |
| `segments_per_corridor` | int   | Yes      | Number of segments for depth illusion |
| `padding_prefab_name`   | str   | Yes      | Name of empty corridor prefab         |
| `cm_per_unity_unit`     | float | Yes      | Conversion factor (typically 10.0)    |

**Trial Structures:**

| Field                              | Type  | Required | Description                             |
|------------------------------------|-------|----------|-----------------------------------------|
| `segment_name`                     | str   | Yes      | Must reference a defined segment        |
| `stimulus_trigger_zone_start_cm`   | float | Yes      | Zone start position from segment start  |
| `stimulus_trigger_zone_end_cm`     | float | Yes      | Zone end position from segment start    |
| `stimulus_location_cm`             | float | Yes      | Stimulus delivery position              |
| `show_stimulus_collision_boundary` | bool  | Yes      | Whether to render the stimulus boundary |
| `trigger_type`                     | str   | Yes      | Either "lick" or "occupancy"            |

### Unity Prefab Requirements

After creating the YAML template, corresponding Unity prefabs must exist:

1. Each segment needs a prefab in `Assets/InfiniteCorridorTask/Prefabs/` matching the segment name
2. Segment prefabs contain cue GameObjects with materials matching cue names
3. Use the CreateTask editor tool in Unity to generate the task prefab from the template

For detailed Unity prefab creation, refer to the sl-unity-tasks documentation and the `/verifying-task-templates` skill
in that project.

---

## Example Session

```text
User: I need to create an experiment for the SSO_Shared_Base task with baseline, experiment, and cooldown phases.

Agent: Let me help you create that experiment configuration.

1. First, I'll check the available templates:
   list_available_templates_tool()
   -> Available templates: ... SSO_Shared_Base ...

2. Let me get details about this template:
   get_template_info_tool(template_name="SSO_Shared_Base")
   -> Template: SSO_Shared_Base
      Cue offset: 10.0cm
      Cues: Gray(code=0), A(code=1), B(code=2), C(code=3)
      Segments: Segment_abc_40cm
      Trial structures:
        - ABC (lick): segment=Segment_abc_40cm

3. This template has one lick-type (water reward) trial. Let me check if the project exists and create the configuration:

   get_projects_tool()
   -> Projects: other_project_1, other_project_2

   create_project_tool(project="my_project")
   -> Project created: my_project at /path/to/my_project

   create_experiment_config_tool(
       project="my_project",
       experiment="sso_base_session",
       template="SSO_Shared_Base",
       state_count=3
   )
   -> Experiment created: sso_base_session from template 'SSO_Shared_Base' at /path/to/sso_base_session.yaml

4. Now I'll edit the generated YAML file to configure the three phases properly:
   - Rename state_1 to "baseline" (600s, supports_trials=false)
   - Rename state_2 to "experiment" (3000s, supports_trials=true, guidance params)
   - Rename state_3 to "cooldown" (600s, supports_trials=false)

The experiment configuration is ready at: {working_dir}/my_project/configuration/sso_base_session.yaml
```

---

## Best Practices

1. **Always use MCP tools**: Use MCP tools for project and experiment management; avoid CLI when MCP alternative exists
2. **Verify system configuration first**: Use `/acquisition-system-setup` skill before starting experiment design
3. **Review template before use**: Use `get_template_info_tool` to understand trial types and structure
4. **Check before creating**: Use `get_projects_tool` and `get_experiments_tool` before creating new resources
5. **Customize via YAML editing**: After generation, modify experiment states and trial parameters directly
6. **Validate against source code**: Verify system state codes against the actual system's state enumeration
7. **Create new templates carefully**: New templates require corresponding Unity prefabs in sl-unity-tasks
