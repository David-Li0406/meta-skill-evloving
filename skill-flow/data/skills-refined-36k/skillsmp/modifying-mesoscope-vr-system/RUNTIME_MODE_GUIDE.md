# Adding Runtime Modes to Mesoscope-VR

This guide covers creating new runtime modes (training sessions, experiment types) for the Mesoscope-VR acquisition
system, including system states, runtime logic functions, visualization modes, session descriptors, and CLI commands.

---

## Concepts Overview

A runtime mode in Mesoscope-VR consists of several interconnected components:

| Component             | Location                        | Purpose                                           |
|-----------------------|---------------------------------|---------------------------------------------------|
| SessionType           | sl-shared-assets                | Identifies session type for data organization     |
| Session Descriptor    | sl-shared-assets                | Stores session parameters (persists across runs)  |
| System State          | data_acquisition.py             | Controls hardware behavior (brake, screens, etc.) |
| State Transition      | _MesoscopeVRSystem class        | Method to switch hardware to the state            |
| Runtime Logic         | data_acquisition.py             | Main function that orchestrates the session       |
| Visualizer Mode       | visualizers.py                  | Configures real-time behavior display             |
| CLI Command           | execute.py                      | User-facing command to start the session          |

---

## Modification Workflow

Adding a new runtime mode requires changes in both repositories:

```
Phase 1: sl-shared-assets (Data Structures)
├── 1.1 Add SessionType enumeration member
├── 1.2 Create session descriptor dataclass
├── 1.3 Register descriptor in preprocessing map
├── 1.4 Export new classes
└── 1.5 Bump version

Phase 2: sl-experiment (Implementation)
├── 2.1 Add system state to _MesoscopeVRStates enum
├── 2.2 Add state transition method to _MesoscopeVRSystem
├── 2.3 Add visualizer mode to VisualizerMode enum
├── 2.4 Update _MesoscopeVRSystem to handle new session type
├── 2.5 Create runtime logic function
├── 2.6 Add CLI command to execute.py
├── 2.7 Export from __init__.py
└── 2.8 Update pyproject.toml dependency
```

---

## Phase 1: Data Structures (sl-shared-assets)

### Step 1.1: Add SessionType

**File:** `sl-shared-assets/src/sl_shared_assets/data/session_data.py`

Add a new member to the `SessionTypes` enumeration:

```python
class SessionTypes(StrEnum):
    """Defines valid session types for data acquisition systems."""

    LICK_TRAINING = "lick_training"
    """Trains animals to operate the lickport."""

    RUN_TRAINING = "run_training"
    """Trains animals to run on the wheel treadmill."""

    MESOSCOPE_EXPERIMENT = "mesoscope_experiment"
    """Full experiment sessions with mesoscope imaging."""

    WINDOW_CHECKING = "window_checking"
    """Maintenance sessions for checking cranial windows."""

    # ADD NEW SESSION TYPE
    NEW_TRAINING = "new_training"
    """Description of what the new training mode accomplishes."""
```

### Step 1.2: Create Session Descriptor

**File:** `sl-shared-assets/src/sl_shared_assets/configuration/mesoscope_descriptors.py`

Create a dataclass to store session parameters:

```python
@dataclass()
class NewTrainingDescriptor(YamlConfig):
    """Stores the runtime parameters for the new training session.

    This descriptor persists session parameters across runs, allowing the system to resume training with previously
    used settings or progress to more challenging parameters.

    Attributes:
        experimenter: Identifier of the person conducting the session.
        mouse_weight_g: Animal weight at session start in grams.
        parameter_a: Description of parameter A and its purpose.
        parameter_b: Description of parameter B and its purpose.
        maximum_training_time_min: Maximum session duration in minutes.
        maximum_water_volume_ml: Maximum water volume to deliver in milliliters.
    """

    # Session metadata (set at runtime, not persisted)
    experimenter: str = ""
    """The unique identifier of the experimenter conducting the session."""

    mouse_weight_g: float = 0.0
    """The weight of the animal at the start of the session, in grams."""

    # Training parameters (persisted across sessions)
    parameter_a: float = 10.0
    """Description of parameter A and its default value."""

    parameter_b: int = 100
    """Description of parameter B and its default value."""

    # Session limits
    maximum_training_time_min: int = 30
    """The maximum duration of the training session, in minutes."""

    maximum_water_volume_ml: float = 1.0
    """The maximum volume of water to deliver during the session, in milliliters."""

    maximum_unconsumed_rewards: int = 3
    """Maximum unconsumed rewards before suspending water delivery."""

    # Reward parameters
    water_reward_size_ul: float = 5.0
    """The volume of water delivered per reward, in microliters."""

    reward_tone_duration_ms: int = 300
    """The duration of the auditory tone accompanying rewards, in milliseconds."""
```

### Step 1.3: Register in Preprocessing Map

**File:** `sl-shared-assets/src/sl_shared_assets/data/session_data.py` (or preprocessing utilities)

Ensure the new descriptor is mapped to the session type:

```python
DESCRIPTOR_MAP: dict[SessionTypes, type] = {
    SessionTypes.LICK_TRAINING: LickTrainingDescriptor,
    SessionTypes.RUN_TRAINING: RunTrainingDescriptor,
    SessionTypes.MESOSCOPE_EXPERIMENT: MesoscopeExperimentDescriptor,
    SessionTypes.WINDOW_CHECKING: WindowCheckingDescriptor,
    SessionTypes.NEW_TRAINING: NewTrainingDescriptor,  # ADD THIS
}
```

### Step 1.4: Export Classes

**File:** `sl-shared-assets/src/sl_shared_assets/configuration/__init__.py`

```python
from .mesoscope_descriptors import (
    LickTrainingDescriptor,
    RunTrainingDescriptor,
    MesoscopeExperimentDescriptor,
    WindowCheckingDescriptor,
    NewTrainingDescriptor,  # ADD THIS
)
```

**File:** `sl-shared-assets/src/sl_shared_assets/__init__.py`

```python
from .configuration import (
    # ... existing exports ...
    NewTrainingDescriptor,  # ADD THIS
)
```

### Step 1.5: Bump Version

Update `pyproject.toml` version number.

---

## Phase 2: Implementation (sl-experiment)

### Step 2.1: Add System State

**File:** `sl-experiment/src/sl_experiment/mesoscope_vr/data_acquisition.py`

Add a new member to the `_MesoscopeVRStates` enumeration:

```python
class _MesoscopeVRStates(IntEnum):
    """Defines the set of codes used by the Mesoscope-VR data acquisition system to communicate its runtime state."""

    IDLE = 0
    """The system is currently not conducting a data acquisition session."""

    REST = 1
    """The system is conducting the 'rest' period of an experiment session."""

    RUN = 2
    """The system is conducting the 'run' period of an experiment session."""

    LICK_TRAINING = 3
    """The system is conducting the lick training session."""

    RUN_TRAINING = 4
    """The system is conducting the run training session."""

    # ADD NEW STATE
    NEW_TRAINING = 5
    """The system is conducting the new training session."""

    @classmethod
    def to_dict(cls) -> dict[str, int]:
        """Converts the instance's data to a dictionary mapping, replacing underscores with spaces."""
        return {member.name.lower().replace("_", " "): member.value for member in cls}
```

### Step 2.2: Add State Transition Method

**File:** `sl-experiment/src/sl_experiment/mesoscope_vr/data_acquisition.py`

Add a method to `_MesoscopeVRSystem` that configures hardware for the new state:

```python
class _MesoscopeVRSystem:
    # ... existing methods ...

    def new_train(self) -> None:
        """Switches the Mesoscope-VR system to the new training state.

        Notes:
            Describe the hardware configuration for this state:
            - Brake engaged/disengaged
            - Screens on/off
            - Which sensors are monitored
            - Any special configuration

            Calling this method automatically switches the runtime state to 255 (active training).
        """
        # Switches runtime state to 255 (active)
        self.change_runtime_state(new_state=255)

        # Configure VR screens (True = on, False = off/black)
        self._microcontrollers.screens.set_state(state=False)

        # Configure brake (True = engaged, False = disengaged)
        self._microcontrollers.brake.set_state(state=True)

        # Configure encoder monitoring
        self._microcontrollers.wheel_encoder.set_monitoring_state(state=False)

        # Configure torque monitoring
        self._microcontrollers.torque.set_monitoring_state(state=True)

        # Configure lick monitoring
        self._microcontrollers.lick.set_monitoring_state(state=True)

        # Sets system state to the new training code
        self._change_system_state(_MesoscopeVRStates.NEW_TRAINING)
```

#### Existing State Configurations Reference

| State         | Brake    | Screens | Encoder | Torque | Lick | Use Case                    |
|---------------|----------|---------|---------|--------|------|-----------------------------|
| REST          | Engaged  | Off     | Off     | On     | On   | Rest periods in experiments |
| RUN           | Released | On      | On      | Off    | On   | Active VR task periods      |
| LICK_TRAINING | Engaged  | Off     | Off     | On     | On   | Teaching lickport operation |
| RUN_TRAINING  | Released | Off     | On      | Off    | On   | Teaching wheel running      |

### Step 2.3: Add Visualizer Mode

**File:** `sl-experiment/src/sl_experiment/mesoscope_vr/visualizers.py`

Add a new member to the `VisualizerMode` enumeration:

```python
class VisualizerMode(IntEnum):
    """Defines the display modes for the BehaviorVisualizer."""

    LICK_TRAINING = 0
    """Displays only lick sensor and valve plots."""

    RUN_TRAINING = 1
    """Displays lick, valve, and running speed plots."""

    EXPERIMENT = 2
    """Displays all plots including the trial performance panel."""

    # ADD NEW MODE (if visualization differs from existing modes)
    NEW_TRAINING = 3
    """Displays plots specific to the new training mode."""
```

If your new mode uses the same visualization as an existing mode, you can reuse that mode instead of adding a new one.

### Step 2.4: Update _MesoscopeVRSystem Initialization

**File:** `sl-experiment/src/sl_experiment/mesoscope_vr/data_acquisition.py`

Update the `_MesoscopeVRSystem` class to handle the new session type:

```python
class _MesoscopeVRSystem:
    def __init__(
        self,
        session_data: SessionData,
        session_descriptor: MesoscopeExperimentDescriptor | LickTrainingDescriptor | RunTrainingDescriptor
                           | NewTrainingDescriptor,  # ADD TYPE
        experiment_configuration: MesoscopeExperimentConfiguration | None = None,
    ) -> None:
        # ... existing initialization ...

        # Determine visualizer mode based on session type
        if self._session_data.session_type == SessionTypes.LICK_TRAINING:
            visualizer_mode = VisualizerMode.LICK_TRAINING
        elif self._session_data.session_type == SessionTypes.RUN_TRAINING:
            visualizer_mode = VisualizerMode.RUN_TRAINING
        elif self._session_data.session_type == SessionTypes.NEW_TRAINING:  # ADD THIS
            visualizer_mode = VisualizerMode.NEW_TRAINING  # Or reuse existing mode
        else:
            visualizer_mode = VisualizerMode.EXPERIMENT
```

### Step 2.5: Create Runtime Logic Function

**File:** `sl-experiment/src/sl_experiment/mesoscope_vr/data_acquisition.py`

Create the main function that orchestrates the session. Follow this pattern:

```python
def new_training_logic(
    experimenter: str,
    project_name: str,
    animal_id: str,
    animal_weight: float,
    parameter_a: float | None = None,
    parameter_b: int | None = None,
    maximum_water_volume: float | None = None,
    maximum_training_time: int | None = None,
    maximum_unconsumed_rewards: int | None = None,
) -> None:
    """Trains the animal using the new training paradigm.

    Notes:
        Describe what this training accomplishes and how it works. Include details about:
        - The training goal
        - How progression works (if applicable)
        - When the session ends

        Most arguments to this function are optional overrides. If an argument is not provided, the system loads the
        argument's value used during a previous session (if available) or uses a system-defined default value.

    Args:
        experimenter: The unique identifier of the experimenter conducting the training session.
        project_name: The name of the project in which the trained animal participates.
        animal_id: The unique identifier of the animal being trained.
        animal_weight: The weight of the animal, in grams, at the beginning of the session.
        parameter_a: Description of parameter A override.
        parameter_b: Description of parameter B override.
        maximum_water_volume: The maximum volume of water, in milliliters, that can be delivered.
        maximum_training_time: The maximum training time, in minutes.
        maximum_unconsumed_rewards: Maximum unconsumed rewards before suspending delivery.
    """
    message = "Initializing the new training session..."
    console.echo(message=message, level=LogLevel.INFO)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 1: Configuration and Validation
    # ─────────────────────────────────────────────────────────────────────────

    # Query system configuration
    system_configuration = get_system_configuration()

    # Verify project exists
    project_directory = system_configuration.filesystem.root_directory.joinpath(project_name)
    if not project_directory.exists():
        message = (
            f"Unable to execute the new training session for the animal {animal_id} participating in the project "
            f"{project_name}. The {system_configuration.name} data acquisition system is not configured to acquire "
            f"data for this project. Use the 'sl-configure project' command to configure the project before running "
            f"data acquisition sessions."
        )
        console.error(message=message, error=FileNotFoundError)

    # Verify animal project assignment
    animal_projects = get_animal_project(animal_id=animal_id)
    if len(animal_projects) > 1:
        message = (
            f"Unable to execute the new training session for the animal {animal_id} participating in the project "
            f"{project_name}. The animal is associated with multiple projects managed by the "
            f"{system_configuration.name} data acquisition system, which is not allowed."
        )
        console.error(message=message, error=ValueError)
    elif len(animal_projects) == 1 and animal_projects[0] != project_name:
        message = (
            f"Unable to execute the new training session for the animal {animal_id} participating in the project "
            f"{project_name}. The animal is already associated with a different project '{animal_projects[0]}'."
        )
        console.error(message=message, error=ValueError)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 2: Session Data Initialization
    # ─────────────────────────────────────────────────────────────────────────

    # Get version information
    python_version, library_version = get_version_data()

    # Initialize session data hierarchy
    session_data = SessionData.create(
        project_name=project_name,
        animal_id=animal_id,
        session_type=SessionTypes.NEW_TRAINING,  # USE NEW SESSION TYPE
        python_version=python_version,
        sl_experiment_version=library_version,
    )
    mesoscope_data = MesoscopeData(session_data=session_data, system_configuration=system_configuration)

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 3: Descriptor Loading and Configuration
    # ─────────────────────────────────────────────────────────────────────────

    # Load previous session parameters if available
    previous_descriptor_path = mesoscope_data.vrpc_data.session_descriptor_path
    previous_descriptor: NewTrainingDescriptor | None = None
    if previous_descriptor_path.exists():
        previous_descriptor = NewTrainingDescriptor.from_yaml(file_path=previous_descriptor_path)
        message = "Previous session's configuration parameters: Applied."
        console.echo(message=message, level=LogLevel.SUCCESS)
    else:
        message = "Previous session's configuration parameters: Not found. Using defaults..."
        console.echo(message=message, level=LogLevel.INFO)

    # Initialize descriptor with current session metadata
    descriptor = NewTrainingDescriptor(
        experimenter=experimenter,
        mouse_weight_g=animal_weight,
    )

    # Apply previous session parameters if available
    if previous_descriptor is not None:
        descriptor.parameter_a = previous_descriptor.parameter_a
        descriptor.parameter_b = previous_descriptor.parameter_b
        descriptor.maximum_water_volume_ml = previous_descriptor.maximum_water_volume_ml
        descriptor.maximum_training_time_min = previous_descriptor.maximum_training_time_min
        descriptor.maximum_unconsumed_rewards = previous_descriptor.maximum_unconsumed_rewards
        descriptor.water_reward_size_ul = previous_descriptor.water_reward_size_ul
        descriptor.reward_tone_duration_ms = previous_descriptor.reward_tone_duration_ms

    # Apply argument overrides
    if parameter_a is not None:
        descriptor.parameter_a = parameter_a
    if parameter_b is not None:
        descriptor.parameter_b = parameter_b
    if maximum_water_volume is not None:
        descriptor.maximum_water_volume_ml = maximum_water_volume
    if maximum_training_time is not None:
        descriptor.maximum_training_time_min = maximum_training_time
    if maximum_unconsumed_rewards is not None:
        descriptor.maximum_unconsumed_rewards = maximum_unconsumed_rewards

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 4: Runtime Variables Initialization
    # ─────────────────────────────────────────────────────────────────────────

    # Initialize timers
    runtime_timer = PrecisionTimer(precision=TimerPrecisions.SECOND)

    # Convert training time from minutes to seconds
    training_time = descriptor.maximum_training_time_min * 60

    # Initialize tracking variables
    previous_time = 0

    # ─────────────────────────────────────────────────────────────────────────
    # SECTION 5: System Initialization and Main Loop
    # ─────────────────────────────────────────────────────────────────────────

    system: _MesoscopeVRSystem | None = None
    try:
        # Initialize system class
        system = _MesoscopeVRSystem(session_data=session_data, session_descriptor=descriptor)

        # Start system and guide user through preparation
        system.start()

        # Check for early termination during initialization
        if system.terminated:
            message = "The session was terminated early due to user request."
            console.echo(message=message, level=LogLevel.SUCCESS)
            raise RecursionError  # noqa: TRY301

        # Mark session as initialized (prevents auto-purge)
        session_data.runtime_initialized()

        # Switch to new training state
        system.new_train()

        # Start runtime timer
        runtime_timer.reset()

        # ─────────────────────────────────────────────────────────────────────
        # MAIN TRAINING LOOP
        # ─────────────────────────────────────────────────────────────────────

        with console.progress_bar(description="New Training Progress", total=training_time) as progress_bar:
            while True:
                # Execute runtime cycle (handles data, visualization, UI)
                system.runtime_cycle()

                # Check termination conditions
                if system.terminated:
                    break

                # Check time limit
                elapsed_time = runtime_timer.elapsed
                if elapsed_time >= training_time:
                    break

                # Check water limit
                delivered_volume = system.delivered_water_volume
                if delivered_volume >= descriptor.maximum_water_volume_ml * 1000:
                    break

                # Update progress bar
                current_time = int(elapsed_time)
                if current_time > previous_time:
                    progress_bar.update(advance=current_time - previous_time)
                    previous_time = current_time

                # ─────────────────────────────────────────────────────────────
                # TRAINING-SPECIFIC LOGIC HERE
                # ─────────────────────────────────────────────────────────────

                # Example: Check conditions and deliver rewards
                # if some_condition_met:
                #     system.resolve_reward(
                #         reward_size=descriptor.water_reward_size_ul,
                #         tone_duration=descriptor.reward_tone_duration_ms,
                #     )

    except RecursionError:
        # Handle early termination (user request during initialization)
        pass

    except Exception:
        # Log unexpected errors
        message = "New training session: Failed due to unexpected error."
        console.echo(message=message, level=LogLevel.ERROR)
        raise

    finally:
        # ─────────────────────────────────────────────────────────────────────
        # SECTION 6: Cleanup
        # ─────────────────────────────────────────────────────────────────────

        if system is not None:
            system.stop()

        # Copy descriptor to session directory for persistence
        sh.copy2(
            src=session_data.raw_data.session_descriptor_path,
            dst=mesoscope_data.vrpc_data.session_descriptor_path,
        )

    message = "New training session: Complete."
    console.echo(message=message, level=LogLevel.SUCCESS)
```

### Step 2.6: Add CLI Command

**File:** `sl-experiment/src/sl_experiment/command_line_interfaces/execute.py`

Add the import and CLI command:

```python
from ..mesoscope_vr import (
    experiment_logic,
    maintenance_logic,
    run_training_logic,
    lick_training_logic,
    window_checking_logic,
    new_training_logic,  # ADD IMPORT
)

# ... existing commands ...

@run.command()
@click.option(
    "--maximum-time",
    type=int,
    help="Maximum training time in minutes.",
)
@click.option(
    "--maximum-water",
    type=float,
    help="Maximum water volume in milliliters.",
)
@click.option(
    "--parameter-a",
    type=float,
    help="Description of parameter A.",
)
@click.option(
    "--parameter-b",
    type=int,
    help="Description of parameter B.",
)
@click.option(
    "--maximum-unconsumed-rewards",
    type=int,
    help="Maximum unconsumed rewards before suspending delivery.",
)
@click.pass_context
def new_training(
    ctx: click.Context,
    maximum_time: int | None,
    maximum_water: float | None,
    parameter_a: float | None,
    parameter_b: int | None,
    maximum_unconsumed_rewards: int | None,
) -> None:
    """Runs the new training session for the specified animal.

    This command trains the animal using the new training paradigm. Describe what the training accomplishes
    and any important notes about usage.
    """
    new_training_logic(
        experimenter=ctx.obj["user"],
        project_name=ctx.obj["project"],
        animal_id=ctx.obj["animal"],
        animal_weight=ctx.obj["weight"],
        parameter_a=parameter_a,
        parameter_b=parameter_b,
        maximum_water_volume=maximum_water,
        maximum_training_time=maximum_time,
        maximum_unconsumed_rewards=maximum_unconsumed_rewards,
    )
```

### Step 2.7: Export from __init__.py

**File:** `sl-experiment/src/sl_experiment/mesoscope_vr/__init__.py`

```python
from .data_acquisition import (
    lick_training_logic,
    run_training_logic,
    experiment_logic,
    window_checking_logic,
    new_training_logic,  # ADD THIS
)
```

### Step 2.8: Update Dependencies

**File:** `sl-experiment/pyproject.toml`

```toml
dependencies = [
    "sl-shared-assets>=X.Y.Z",  # Match version with new session type
]
```

---

## Existing Components Reference

### Current Session Types

| SessionType            | Descriptor                      | System State    | Visualizer Mode |
|------------------------|---------------------------------|-----------------|-----------------|
| `LICK_TRAINING`        | `LickTrainingDescriptor`        | `LICK_TRAINING` | `LICK_TRAINING` |
| `RUN_TRAINING`         | `RunTrainingDescriptor`         | `RUN_TRAINING`  | `RUN_TRAINING`  |
| `MESOSCOPE_EXPERIMENT` | `MesoscopeExperimentDescriptor` | `REST` / `RUN`  | `EXPERIMENT`    |
| `WINDOW_CHECKING`      | `WindowCheckingDescriptor`      | N/A             | N/A             |

### Current System States

| State           | Code | Brake    | Screens | Encoder | Torque | Lick |
|-----------------|------|----------|---------|---------|--------|------|
| `IDLE`          | 0    | N/A      | N/A     | N/A     | N/A    | N/A  |
| `REST`          | 1    | Engaged  | Off     | Off     | On     | On   |
| `RUN`           | 2    | Released | On      | On      | Off    | On   |
| `LICK_TRAINING` | 3    | Engaged  | Off     | Off     | On     | On   |
| `RUN_TRAINING`  | 4    | Released | Off     | On      | Off    | On   |

**Next available state code:** 5

### Runtime State Convention

- Runtime state `0`: Idle/paused
- Runtime state `1-254`: Experiment state codes (for multi-phase experiments)
- Runtime state `255`: Active training (used by training modes)

---

## Verification Checklist

### Phase 1 (sl-shared-assets)

```
- [ ] Added SessionType enumeration member
- [ ] Created session descriptor dataclass with all parameters
- [ ] Descriptor inherits from YamlConfig
- [ ] Each field has docstring explaining its purpose
- [ ] Registered descriptor in DESCRIPTOR_MAP (if applicable)
- [ ] Exported from configuration/__init__.py
- [ ] Exported from top-level __init__.py
- [ ] Bumped version in pyproject.toml
- [ ] MyPy strict passes
```

### Phase 2 (sl-experiment)

```
- [ ] Added system state to _MesoscopeVRStates enum
- [ ] Added state transition method to _MesoscopeVRSystem
- [ ] Method configures all hardware (brake, screens, sensors)
- [ ] Added visualizer mode (or reuse existing)
- [ ] Updated _MesoscopeVRSystem to handle new session type
- [ ] Created runtime logic function following pattern
- [ ] Function validates project and animal
- [ ] Function loads/saves descriptor for persistence
- [ ] Function has proper error handling and cleanup
- [ ] Added CLI command with appropriate options
- [ ] CLI command passes context to logic function
- [ ] Exported logic function from __init__.py
- [ ] Updated pyproject.toml dependency version
- [ ] MyPy strict passes
```

---

## Common Patterns

### Reward Delivery

```python
# Deliver reward with consumption tracking
delivered = system.resolve_reward(
    reward_size=descriptor.water_reward_size_ul,
    tone_duration=descriptor.reward_tone_duration_ms,
)
if delivered:
    # Actual water was delivered
    pass
else:
    # Tone only (unconsumed limit reached)
    pass
```

### Progress Tracking

```python
# Track delivered water volume
delivered_volume = system.delivered_water_volume  # In microliters

# Track running speed
running_speed = system._running_speed  # In cm/s

# Track lick count
lick_count = system._microcontrollers.lick.lick_count
```

### Threshold Progression

```python
# Update visualizer thresholds (for run training style modes)
system.update_visualizer_thresholds(
    speed_threshold=np.float64(current_speed_threshold),
    duration_threshold=np.float64(current_duration_threshold),
)
```
