# PC Interface Implementation Guide

Complete reference for implementing ModuleInterface subclasses in sl-experiment. This guide covers the Python
implementation patterns for communicating with microcontroller hardware modules.

---

## Repository Locations

**Module Interfaces:** `src/sl_experiment/shared_components/module_interfaces.py`
- Shared across all acquisition systems
- Contains all ModuleInterface subclasses

**Binding Classes:** `src/sl_experiment/<system_name>/binding_classes.py`
- System-specific (e.g., `mesoscope_vr/binding_classes.py`)
- Contains MicroControllerInterfaces orchestration class

**Communication Library:** `../ataraxis-communication-interface/` (relative to sl-experiment)

Note: The communication library is typically located in the same parent directory as sl-experiment. Use the
Cross-Referenced Library Verification procedure in `CLAUDE.md` to locate and verify the correct version.

---

## Required Imports

```python
from typing import Final

import numpy as np
from ataraxis_communication_interface import (
    ModuleData,
    ModuleState,
    ModuleInterface,
)
from ataraxis_data_structures import SharedMemoryArray
from ataraxis_time import PrecisionTimer

# Type aliases for readability
_ZERO_UINT32: Final[np.uint32] = np.uint32(0)
_FALSE: Final[np.bool_] = np.bool_(False)
_TRUE: Final[np.bool_] = np.bool_(True)
```

---

## ModuleInterface Base Class

All PC interfaces inherit from `ModuleInterface` provided by `ataraxis-communication-interface`.

### Constructor Parameters

| Parameter      | Type                    | Purpose                                               |
|----------------|-------------------------|-------------------------------------------------------|
| `module_type`  | `np.uint8`              | Module family identifier (must match firmware)        |
| `module_id`    | `np.uint8`              | Instance identifier within type (must match firmware) |
| `data_codes`   | `set[np.uint8] \| None` | Event codes requiring `process_received_data()`       |
| `error_codes`  | `set[np.uint8] \| None` | Event codes that trigger RuntimeError                 |

### Required Abstract Methods

| Method                       | Called When                        | Purpose                             |
|------------------------------|------------------------------------|-------------------------------------|
| `initialize_remote_assets()` | Communication process starts       | Initialize non-pickleable resources |
| `terminate_remote_assets()`  | Communication process stops        | Cleanup resources                   |
| `process_received_data()`    | Message event code in `data_codes` | Handle incoming module data         |

### Inherited Methods

| Method                  | Purpose                             |
|-------------------------|-------------------------------------|
| `send_command()`        | Send command to firmware module     |
| `send_parameters()`     | Update firmware runtime parameters  |
| `reset_command_queue()` | Clear all queued commands on module |

---

## Basic Interface Structure

```python
class NewModuleInterface(ModuleInterface):
    """PC interface for the new hardware module.

    This interface communicates with the NewModule firmware class.

    Args:
        configuration_param: Parameter from system configuration.

    Attributes:
        _monitoring: Tracks whether continuous monitoring is active.
        _tracker: SharedMemoryArray for IPC with main process.
    """

    def __init__(self, configuration_param: int) -> None:
        # Define event codes that require processing
        data_codes: set[np.uint8] = {np.uint8(51), np.uint8(52)}

        super().__init__(
            module_type=np.uint8(8),   # Must match firmware module_type
            module_id=np.uint8(1),     # Must match firmware module_id
            data_codes=data_codes,
            error_codes=None,          # Or set of error event codes
        )

        # Store configuration
        self._configuration_param: int = configuration_param

        # Define command codes (must match firmware kModuleCommands)
        self._pulse_command: np.uint8 = np.uint8(1)
        self._on_command: np.uint8 = np.uint8(2)
        self._off_command: np.uint8 = np.uint8(3)

        # State tracking
        self._monitoring: bool = False
        self._enabled: bool = False

        # Create shared memory for IPC (not connected yet)
        self._tracker: SharedMemoryArray = SharedMemoryArray.create_array(
            name=f"{self._module_type}_{self._module_id}_tracker",
            prototype=np.zeros(shape=2, dtype=np.uint32),
            exists_ok=True,
        )

    def initialize_remote_assets(self) -> None:
        """Initializes assets in the communication process.

        Called automatically when MicroControllerInterface starts.
        Connect to shared memory arrays and initialize timers here.
        """
        self._tracker.connect()

    def terminate_remote_assets(self) -> None:
        """Cleans up assets in the communication process.

        Called automatically when MicroControllerInterface stops.
        Disconnect from shared memory arrays here.
        """
        self._tracker.disconnect()

    def process_received_data(self, message: ModuleData | ModuleState) -> None:
        """Processes incoming data from the firmware module.

        Args:
            message: ModuleData (with payload) or ModuleState (status only).
        """
        if message.event == 51:  # kOn status
            self._enabled = True
            self._tracker[0] += 1  # Increment activation count

        elif message.event == 52:  # kOff status
            self._enabled = False
```

---

## Lifecycle Methods

### initialize_local_assets()

Optional method called in the main process before communication starts. Use for connecting shared memory that needs
to be accessed from the main process:

```python
def initialize_local_assets(self) -> None:
    """Initializes shared memory in the main process.

    Called explicitly by MicroControllerInterfaces.start() in binding_classes.py.
    """
    self._tracker.connect()
    self._tracker.enable_buffer_destruction()  # Clean up on process exit
```

### initialize_remote_assets()

Required method called in the communication process. Use for resources that cannot be pickled:

```python
def initialize_remote_assets(self) -> None:
    """Initializes assets in the communication process."""
    self._tracker.connect()
    self._timer = PrecisionTimer(unit=TimeUnits.MICROSECOND)
```

### terminate_remote_assets()

Required method for cleanup:

```python
def terminate_remote_assets(self) -> None:
    """Cleans up assets in the communication process."""
    self._tracker.disconnect()
```

---

## Sending Commands

### send_command() Parameters

| Parameter          | Type          | Purpose                                           |
|--------------------|---------------|---------------------------------------------------|
| `command`          | `np.uint8`    | Command code (must match firmware enum value)     |
| `noblock`          | `np.bool_`    | Allow concurrent command execution                |
| `repetition_delay` | `np.uint32`   | Microseconds between repeats (0 = execute once)   |

### One-Shot Commands

```python
def turn_on(self) -> None:
    """Activates the hardware output."""
    if self._enabled:
        return  # Already enabled
    self.send_command(
        command=self._on_command,
        noblock=_FALSE,
        repetition_delay=_ZERO_UINT32,
    )
    self._enabled = True
```

### Repeated Commands (Polling)

```python
def start_monitoring(self) -> None:
    """Starts continuous sensor monitoring."""
    if self._monitoring:
        return
    self.send_command(
        command=self._check_state_command,
        noblock=_TRUE,
        repetition_delay=np.uint32(1000),  # Every 1ms
    )
    self._monitoring = True

def stop_monitoring(self) -> None:
    """Stops continuous sensor monitoring."""
    if not self._monitoring:
        return
    self.reset_command_queue()  # Clear the repeated command
    self._monitoring = False
```

---

## Sending Parameters

### send_parameters() Guidelines

The parameter tuple MUST match the firmware `CustomRuntimeParameters` struct:

1. **Same order** as struct definition
2. **Same types** (numpy types)
3. **Same count** of parameters

```python
def set_parameters(
    self,
    pulse_duration_ms: int,
    threshold: int,
    averaging_count: int,
    enabled: bool,
) -> None:
    """Updates firmware runtime parameters.

    Args:
        pulse_duration_ms: Pulse duration in milliseconds.
        threshold: Detection threshold in ADC units.
        averaging_count: Number of samples to average.
        enabled: Whether the module is enabled.
    """
    # Convert to microseconds
    pulse_duration_us = np.uint32(pulse_duration_ms * 1000)

    # Types must match firmware CustomRuntimeParameters exactly
    self.send_parameters(
        parameter_data=(
            pulse_duration_us,          # uint32_t pulse_duration
            np.uint16(threshold),       # uint16_t threshold
            np.uint8(averaging_count),  # uint8_t averaging_count
            np.bool_(enabled),          # bool enabled
        )
    )
```

### Parameter Optimization

Cache previous parameters to avoid redundant sends:

```python
def set_pulse_duration(self, duration_ms: int) -> None:
    """Updates pulse duration parameter."""
    if duration_ms == self._previous_duration:
        return  # Skip if unchanged

    self.send_parameters(
        parameter_data=(np.uint32(duration_ms * 1000),)
    )
    self._previous_duration = duration_ms
```

---

## Processing Received Data

### Message Types

| Type          | Has Data Payload | Use Case                        |
|---------------|------------------|---------------------------------|
| `ModuleData`  | Yes              | Sensor values, measurements     |
| `ModuleState` | No               | Status notifications only       |

### Accessing Message Properties

```python
def process_received_data(self, message: ModuleData | ModuleState) -> None:
    # Common properties (both types)
    module_type = message.module_type    # np.uint8
    module_id = message.module_id        # np.uint8
    command = message.command            # np.uint8 (command that triggered this)
    event = message.event                # np.uint8 (status/event code)

    # Data payload (ModuleData only)
    if isinstance(message, ModuleData):
        data = message.data_object       # numpy scalar or array
        prototype = message.prototype_code
```

### Event Processing Pattern

```python
def process_received_data(self, message: ModuleData | ModuleState) -> None:
    """Processes incoming module events."""
    if message.event == 51:  # kActivated
        self._handle_activated()

    elif message.event == 52:  # kDeactivated
        self._handle_deactivated()

    elif message.event == 53 and isinstance(message, ModuleData):
        # kValueChanged with data payload
        self._handle_value_changed(message.data_object)

def _handle_activated(self) -> None:
    """Handles activation event."""
    self._enabled = True

def _handle_deactivated(self) -> None:
    """Handles deactivation event."""
    self._enabled = False

def _handle_value_changed(self, value: np.uint16) -> None:
    """Handles value change event."""
    self._tracker[0] = value
```

---

## SharedMemoryArray IPC

SharedMemoryArray enables communication between the main process and communication process.

### Creation (in __init__)

```python
# Create array (not connected yet)
self._tracker: SharedMemoryArray = SharedMemoryArray.create_array(
    name=f"{self._module_type}_{self._module_id}_tracker",
    prototype=np.zeros(shape=2, dtype=np.float64),
    exists_ok=True,
)
```

### Connection Patterns

```python
# Main process connection (initialize_local_assets)
def initialize_local_assets(self) -> None:
    self._tracker.connect()
    self._tracker.enable_buffer_destruction()  # Cleanup on exit

# Communication process connection (initialize_remote_assets)
def initialize_remote_assets(self) -> None:
    self._tracker.connect()  # No destruction flag (main process owns cleanup)

# Cleanup (terminate_remote_assets)
def terminate_remote_assets(self) -> None:
    self._tracker.disconnect()
```

### Read/Write Operations

```python
# Write from communication process (in process_received_data)
self._tracker[0] += motion_value    # Accumulate
self._tracker[1] = position_value   # Overwrite

# Read from main process (via property)
@property
def total_motion(self) -> float:
    """Total accumulated motion value."""
    return float(self._tracker[0])

# Reset from main process
def reset_tracker(self) -> None:
    """Resets tracking values to zero."""
    self._tracker[0] = np.float64(0.0)
    self._tracker[1] = np.float64(0.0)
```

---

## Properties for User Access

Expose state via properties:

```python
@property
def is_enabled(self) -> bool:
    """Returns whether the module is currently enabled."""
    return self._enabled

@property
def is_monitoring(self) -> bool:
    """Returns whether continuous monitoring is active."""
    return self._monitoring

@property
def activation_count(self) -> int:
    """Returns the total number of activations."""
    return int(self._tracker[0])

@property
def current_value(self) -> float:
    """Returns the most recent sensor value."""
    return float(self._tracker[1])
```

---

## Integration with MicroControllerInterfaces

Each acquisition system has its own binding class that orchestrates microcontroller communication. The pattern below
shows how to integrate a new ModuleInterface into a system's MicroControllerInterfaces class.

### Adding to Binding Class

**File:** `src/sl_experiment/<system_name>/binding_classes.py`

```python
class MicroControllerInterfaces:
    """Manages microcontroller communication for the acquisition system."""

    def __init__(
        self,
        data_logger: DataLogger,
        config: SystemMicroControllers,  # System-specific config dataclass
    ) -> None:
        # Existing interfaces...
        self.existing_module = ExistingInterface(...)

        # ADD NEW INTERFACE
        self.new_hardware = NewModuleInterface(
            configuration_param=config.new_hardware_param,
        )

        # Add to appropriate controller's module_interfaces tuple
        self._controller: MicroControllerInterface = MicroControllerInterface(
            controller_id=np.uint8(101),  # Must match firmware controller ID
            data_logger=data_logger,
            module_interfaces=(
                self.existing_module,
                self.new_hardware,  # ADD TO TUPLE
            ),
            buffer_size=8192,
            port=config.controller_port,
            baudrate=115200,
        )

    def start(self) -> None:
        """Starts all microcontroller communication."""
        self._controller.start()

        # Initialize local assets for interfaces that need shared memory
        self.existing_module.initialize_local_assets()
        self.new_hardware.initialize_local_assets()  # ADD THIS

        # Configure parameters
        self.new_hardware.set_parameters(...)

    def stop(self) -> None:
        """Stops all microcontroller communication."""
        self._actor.stop()
        self._sensor.stop()
        self._encoder.stop()
```

---

## Usage in data_acquisition.py

### Starting Hardware

```python
# In session setup
self._microcontrollers.new_hardware.set_parameters(
    pulse_duration_ms=100,
    threshold=2000,
    averaging_count=10,
    enabled=True,
)

# Start monitoring if applicable
self._microcontrollers.new_hardware.start_monitoring()
```

### Runtime Operations

```python
# Trigger one-shot command
self._microcontrollers.new_hardware.send_pulse()

# Read current state
if self._microcontrollers.new_hardware.is_enabled:
    count = self._microcontrollers.new_hardware.activation_count
```

### Cleanup

```python
# Stop monitoring
self._microcontrollers.new_hardware.stop_monitoring()

# Hardware stops automatically via MicroControllerInterfaces.stop()
```

---

## Complete Interface Example

Full implementation of a digital output interface:

```python
from typing import Final

import numpy as np
from ataraxis_communication_interface import (
    ModuleData,
    ModuleState,
    ModuleInterface,
)
from ataraxis_data_structures import SharedMemoryArray

_ZERO_UINT32: Final[np.uint32] = np.uint32(0)
_FALSE: Final[np.bool_] = np.bool_(False)


class DigitalOutputInterface(ModuleInterface):
    """PC interface for the DigitalOutputModule firmware.

    Controls a digital output pin with pulse, on, and off commands.

    Args:
        default_pulse_duration_ms: Default pulse duration in milliseconds.

    Attributes:
        _enabled: Current output state.
        _pulse_count: Shared memory for tracking pulse count.
    """

    def __init__(self, default_pulse_duration_ms: int = 100) -> None:
        data_codes: set[np.uint8] = {np.uint8(51), np.uint8(52)}

        super().__init__(
            module_type=np.uint8(8),
            module_id=np.uint8(1),
            data_codes=data_codes,
            error_codes=None,
        )

        # Command codes (match firmware kModuleCommands)
        self._pulse_command: np.uint8 = np.uint8(1)
        self._on_command: np.uint8 = np.uint8(2)
        self._off_command: np.uint8 = np.uint8(3)

        # State
        self._enabled: bool = False
        self._default_duration: int = default_pulse_duration_ms
        self._previous_duration: int = default_pulse_duration_ms

        # Shared memory for pulse counting
        self._pulse_count: SharedMemoryArray = SharedMemoryArray.create_array(
            name=f"{self._module_type}_{self._module_id}_pulse_count",
            prototype=np.zeros(shape=1, dtype=np.uint32),
            exists_ok=True,
        )

    def initialize_local_assets(self) -> None:
        """Connects shared memory from main process."""
        self._pulse_count.connect()
        self._pulse_count.enable_buffer_destruction()

    def initialize_remote_assets(self) -> None:
        """Connects shared memory from communication process."""
        self._pulse_count.connect()

    def terminate_remote_assets(self) -> None:
        """Disconnects shared memory."""
        self._pulse_count.disconnect()

    def process_received_data(self, message: ModuleData | ModuleState) -> None:
        """Processes output state changes."""
        if message.event == 51:  # kOn
            self._enabled = True
        elif message.event == 52:  # kOff
            if self._enabled:  # Was on, now off = completed pulse
                self._pulse_count[0] += 1
            self._enabled = False

    def set_pulse_duration(self, duration_ms: int) -> None:
        """Sets the pulse duration parameter.

        Args:
            duration_ms: Pulse duration in milliseconds.
        """
        if duration_ms == self._previous_duration:
            return
        self.send_parameters(
            parameter_data=(np.uint32(duration_ms * 1000),)
        )
        self._previous_duration = duration_ms

    def send_pulse(self, duration_ms: int | None = None) -> None:
        """Sends a timed pulse.

        Args:
            duration_ms: Optional override for pulse duration.
        """
        if duration_ms is not None:
            self.set_pulse_duration(duration_ms)
        self.send_command(
            command=self._pulse_command,
            noblock=_FALSE,
            repetition_delay=_ZERO_UINT32,
        )

    def turn_on(self) -> None:
        """Enables the output continuously."""
        if self._enabled:
            return
        self.send_command(
            command=self._on_command,
            noblock=_FALSE,
            repetition_delay=_ZERO_UINT32,
        )

    def turn_off(self) -> None:
        """Disables the output."""
        if not self._enabled:
            return
        self.send_command(
            command=self._off_command,
            noblock=_FALSE,
            repetition_delay=_ZERO_UINT32,
        )

    @property
    def is_enabled(self) -> bool:
        """Returns whether the output is currently enabled."""
        return self._enabled

    @property
    def pulse_count(self) -> int:
        """Returns the total number of completed pulses."""
        return int(self._pulse_count[0])

    def reset_pulse_count(self) -> None:
        """Resets the pulse counter to zero."""
        self._pulse_count[0] = np.uint32(0)
```

---

## Type Matching Reference

Ensure parameter types match between Python and C++:

| Firmware Type | Python Type      | Creation                   |
|---------------|------------------|----------------------------|
| `bool`        | `np.bool_`       | `np.bool_(True)`           |
| `uint8_t`     | `np.uint8`       | `np.uint8(255)`            |
| `int8_t`      | `np.int8`        | `np.int8(-128)`            |
| `uint16_t`    | `np.uint16`      | `np.uint16(65535)`         |
| `int16_t`     | `np.int16`       | `np.int16(-32768)`         |
| `uint32_t`    | `np.uint32`      | `np.uint32(4000000)`       |
| `int32_t`     | `np.int32`       | `np.int32(-2000000000)`    |
| `float`       | `np.float32`     | `np.float32(3.14)`         |

---

## PC Interface Verification Checklist

```
- [ ] Class inherits from ModuleInterface
- [ ] module_type matches firmware constructor parameter
- [ ] module_id matches firmware constructor parameter
- [ ] data_codes set includes all firmware kCustomStatusCodes that need processing
- [ ] Command codes match firmware kModuleCommands enum values
- [ ] send_parameters() tuple order matches firmware CustomRuntimeParameters struct
- [ ] send_parameters() types match firmware parameter types exactly
- [ ] initialize_local_assets() connects and enables destruction on shared memory
- [ ] initialize_remote_assets() connects to shared memory
- [ ] terminate_remote_assets() disconnects from shared memory
- [ ] process_received_data() handles all event codes in data_codes
- [ ] User-facing methods have docstrings
- [ ] Properties expose state for external access
- [ ] Added to MicroControllerInterfaces binding class
- [ ] Added to module_interfaces tuple in binding class
- [ ] initialize_local_assets() called in binding class start()
- [ ] MyPy strict passes
```
