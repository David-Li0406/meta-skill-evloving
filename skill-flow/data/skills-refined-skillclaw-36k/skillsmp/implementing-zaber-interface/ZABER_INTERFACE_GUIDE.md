# Zaber Motor API Reference

Complete API reference for the Zaber motor binding classes used in sl-experiment.

---

## Core Imports

```python
from sl_experiment.mesoscope_vr.zaber_bindings import (
    ZaberConnection,
    ZaberDevice,
    ZaberAxis,
    CRCCalculator,
    discover_zaber_devices,
    get_zaber_devices_info,
)
```

---

## ZaberConnection Class

Manages a serial USB port and all Zaber devices available through that port.

### Constructor

```python
class ZaberConnection:
    def __init__(self, port: str) -> None
```

**Parameters:**

| Parameter | Type  | Required | Description                               |
|-----------|-------|----------|-------------------------------------------|
| `port`    | `str` | Yes      | Serial port path (e.g., `/dev/ttyUSB0`)   |

**Raises:** `TypeError` if port is not a string.

**Notes:**
- Constructor does NOT establish connection - call `connect()` first
- Multiple ZaberConnection instances cannot share the same port

### Methods

| Method         | Returns                  | Description                                          |
|----------------|--------------------------|------------------------------------------------------|
| `connect()`    | `None`                   | Opens port and discovers all connected devices       |
| `disconnect()` | `None`                   | Shuts down devices and closes port connection        |
| `get_device()` | `ZaberDevice`            | Returns device interface by daisy-chain index        |

### Properties

| Property       | Type   | Description                                              |
|----------------|--------|----------------------------------------------------------|
| `is_connected` | `bool` | True if connection is active and devices are responding  |

### get_device Method

```python
def get_device(self, index: int) -> ZaberDevice
```

**Parameters:**

| Parameter | Type  | Description                                                          |
|-----------|-------|----------------------------------------------------------------------|
| `index`   | `int` | Zero-based index in daisy-chain (0 = closest to USB port)            |

**Returns:** `ZaberDevice` instance for the specified controller.

**Raises:** `ConnectionError` if not connected to the port.

### Lifecycle

```
┌──────────────────────────────────────────────────────────────────────────┐
│                      ZaberConnection Lifecycle                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  __init__(port="/dev/ttyUSB0")                                           │
│      │                                                                   │
│      ▼                                                                   │
│  [Connection not established, no devices available]                      │
│      │                                                                   │
│  connect()                                                               │
│      │                                                                   │
│      ▼                                                                   │
│  [Port open, devices discovered and wrapped in ZaberDevice instances]    │
│      │                                                                   │
│      ├──── get_device(0) ───► Returns ZaberDevice for first motor        │
│      ├──── get_device(1) ───► Returns ZaberDevice for second motor       │
│      │                                                                   │
│      ▼                                                                   │
│  disconnect()                                                            │
│      │                                                                   │
│      ▼                                                                   │
│  [All devices shut down, port closed, resources released]                │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## ZaberDevice Class

Manages a Zaber controller that controls a single motor axis.

### Constructor

```python
class ZaberDevice:
    def __init__(self, device: Device) -> None
```

**Parameters:**

| Parameter | Type     | Description                                           |
|-----------|----------|-------------------------------------------------------|
| `device`  | `Device` | zaber-motion Device instance from connection          |

**Notes:**
- Users do not instantiate directly - use `ZaberConnection.get_device()`
- Only supports single-axis controllers

**Raises:**
- `ValueError` if device manages multiple axes
- `ValueError` if checksum validation fails (USER_DATA_0 mismatch)
- Prompts for confirmation if unsafe device was not properly shut down

### Configuration Validation

On initialization, ZaberDevice validates:

1. **Axis count**: Must be exactly 1 (single-axis controller)
2. **Checksum**: USER_DATA_0 must equal CRC32-XFER of device label
3. **Shutdown state**: For unsafe devices, verifies proper previous shutdown

### Methods

| Method       | Returns | Description                                        |
|--------------|---------|----------------------------------------------------|
| `shutdown()` | `None`  | Gracefully shuts down motor and sets shutdown flag |

### Properties

| Property | Type        | Description                          |
|----------|-------------|--------------------------------------|
| `axis`   | `ZaberAxis` | Interface for the motor (axis)       |

---

## ZaberAxis Class

Interfaces with a Zaber motor for motion control.

### Constructor

```python
class ZaberAxis:
    def __init__(self, motor: Axis) -> None
```

**Parameters:**

| Parameter | Type   | Description                                    |
|-----------|--------|------------------------------------------------|
| `motor`   | `Axis` | zaber-motion Axis instance from device         |

**Notes:**
- Users do not instantiate directly - access via `ZaberDevice.axis`
- Validates predefined positions are within motion limits

**Raises:** `ValueError` if any predefined position exceeds motion limits.

### Methods

| Method         | Returns | Description                                              |
|----------------|---------|----------------------------------------------------------|
| `home()`       | `None`  | Moves motor to home sensor position (non-blocking)       |
| `move()`       | `None`  | Moves motor to absolute position (non-blocking)          |
| `stop()`       | `None`  | Decelerates and stops motor (emergency-safe)             |
| `park()`       | `None`  | Parks motor and saves position to non-volatile memory    |
| `unpark()`     | `None`  | Unparks motor to allow motion commands                   |
| `shutdown()`   | `None`  | Stops movement and parks motor                           |
| `get_position` | `float` | Returns current absolute position in native units        |

### Properties

| Property               | Type   | Description                                           |
|------------------------|--------|-------------------------------------------------------|
| `is_homed`             | `bool` | True if motor has established home reference          |
| `is_parked`            | `bool` | True if motor is parked (cannot accept commands)      |
| `is_busy`              | `bool` | True if motor is currently executing a command        |
| `park_position`        | `int`  | Predefined park position (native units)               |
| `mount_position`       | `int`  | Predefined mount position (native units)              |
| `maintenance_position` | `int`  | Predefined maintenance position (native units)        |

### home Method

```python
def home(self) -> None
```

Moves the motor towards its home sensor until the sensor triggers. Establishes the reference point for all position
commands.

**Behavior:**
- Non-blocking - returns immediately, motor moves asynchronously
- Does nothing if motor is parked or busy
- Call `is_busy` or `wait_until_idle()` to check completion

### move Method

```python
def move(self, position: int) -> None
```

Moves the motor to the specified absolute position.

**Parameters:**

| Parameter  | Type  | Description                              |
|------------|-------|------------------------------------------|
| `position` | `int` | Target position in native motor units    |

**Behavior:**
- Non-blocking - returns immediately, motor moves asynchronously
- Does nothing if motor is parked, busy, or not homed
- Does nothing if position exceeds motion limits

### stop Method

```python
def stop(self) -> None
```

Stops motor movement with deceleration.

**Behavior:**
- Bypasses communication timing guards for emergency use
- First call: decelerates and stops
- Second rapid call: immediate stop (no deceleration)
- Non-blocking

### Communication Timing

ZaberAxis enforces a 5ms minimum delay between consecutive hardware interactions to prevent overwhelming the serial
interface. This timing is handled automatically by internal `_padded_method_call()`.

---

## Non-Volatile Memory Settings

Zaber controllers store configuration in non-volatile USER_DATA variables:

| Setting                     | Variable     | Purpose                                       |
|-----------------------------|--------------|-----------------------------------------------|
| `checksum`                  | USER_DATA_0  | CRC32-XFER checksum of device label           |
| `shutdown_flag`             | USER_DATA_1  | 1 = proper shutdown, 0 = abnormal termination |
| `unsafe_flag`               | USER_DATA_10 | 1 = requires safe position for homing         |
| `axis_park_position`        | USER_DATA_11 | Park position in native units                 |
| `axis_maintenance_position` | USER_DATA_12 | Maintenance position in native units          |
| `axis_mount_position`       | USER_DATA_13 | Mount position in native units                |

**Understanding shutdown_flag vs unsafe_flag:**

- **shutdown_flag**: Managed during runtime. Set to `0` at startup, set to `1` during proper shutdown. If a motor with
  `unsafe_flag=1` has `shutdown_flag=0`, the system will prompt for manual verification before homing. To recover from
  improper shutdown, have the user verify the motor is safe, then set `shutdown_flag` to `1`.

- **unsafe_flag**: Set once during initial hardware setup. Reflects whether the motor's physical mounting allows it to
  be positioned in a way that makes homing dangerous (e.g., could cause collision). This flag should NOT be modified
  to work around improper shutdown - use `shutdown_flag` instead.

### Motion Limit Settings

| Setting         | Zaber Constant | Purpose                                     |
|-----------------|----------------|---------------------------------------------|
| `maximum_limit` | LIMIT_MAX      | Maximum allowed position relative to home   |
| `minimum_limit` | LIMIT_MIN      | Minimum allowed position relative to home   |
| `position`      | POS            | Current absolute position relative to home  |

---

## CRCCalculator Class

Calculates CRC32-XFER checksums for device label validation.

### Constructor

```python
class CRCCalculator:
    def __init__(self) -> None
```

### Methods

| Method             | Returns | Description                                   |
|--------------------|---------|-----------------------------------------------|
| `string_checksum`  | `int`   | Calculates CRC32-XFER checksum for string     |

### string_checksum Method

```python
def string_checksum(self, string: str) -> int
```

**Parameters:**

| Parameter | Type  | Description                    |
|-----------|-------|--------------------------------|
| `string`  | `str` | Input string (typically label) |

**Returns:** Integer CRC32-XFER checksum value.

**Example:**

```python
from sl_experiment.mesoscope_vr import CRCCalculator

calculator = CRCCalculator()
checksum = calculator.string_checksum("HeadBar")
print(f"Checksum for 'HeadBar': {checksum}")
# Use this value to configure USER_DATA_0 on the motor controller
```

---

## Discovery Functions

### discover_zaber_devices

Scans all serial ports and prints discovered device information.

```python
def discover_zaber_devices() -> None
```

**Notes:** Prints formatted table to stdout. Use `get_zaber_devices_info()` for programmatic access.

### get_zaber_devices_info

Scans all serial ports and returns formatted device information.

```python
def get_zaber_devices_info() -> str
```

**Returns:** Formatted table string containing port, device, and axis information.

**Notes:** Used by MCP tool `get_zaber_devices_tool()`.

---

## Configuration Functions

### get_zaber_device_settings

Reads all configuration settings from a device's non-volatile memory.

```python
def get_zaber_device_settings(port: str, device_index: int) -> ZaberDeviceSettings
```

**Parameters:**

| Parameter      | Type  | Description                                           |
|----------------|-------|-------------------------------------------------------|
| `port`         | `str` | Serial port path (e.g., `/dev/ttyUSB0`)               |
| `device_index` | `int` | Zero-based index in daisy-chain (0 = closest to USB)  |

**Returns:** `ZaberDeviceSettings` dataclass containing:

| Attribute              | Type    | Source         |
|------------------------|---------|----------------|
| `device_label`         | `str`   | device.label   |
| `axis_label`           | `str`   | axis.label     |
| `checksum`             | `int`   | USER_DATA_0    |
| `shutdown_flag`        | `int`   | USER_DATA_1    |
| `unsafe_flag`          | `int`   | USER_DATA_10   |
| `park_position`        | `int`   | USER_DATA_11   |
| `maintenance_position` | `int`   | USER_DATA_12   |
| `mount_position`       | `int`   | USER_DATA_13   |
| `limit_min`            | `float` | LIMIT_MIN      |
| `limit_max`            | `float` | LIMIT_MAX      |
| `current_position`     | `float` | POS            |

**Raises:**

- `ConnectionError`: If unable to connect to the specified port.
- `IndexError`: If device_index is out of range for the connected devices.

### set_zaber_device_setting

Writes a single setting to device non-volatile memory with validation.

```python
def set_zaber_device_setting(
    port: str,
    device_index: int,
    setting: str,
    value: int | str
) -> str
```

**Parameters:**

| Parameter      | Type        | Description                                               |
|----------------|-------------|-----------------------------------------------------------|
| `port`         | `str`       | Serial port path                                          |
| `device_index` | `int`       | Zero-based index in daisy-chain                           |
| `setting`      | `str`       | Setting name (see table below)                            |
| `value`        | `int \| str`| Value to write (int for positions/flags, str for labels)  |

**Valid Settings:**

| Setting                | Type  | Validation                            |
|------------------------|-------|---------------------------------------|
| `park_position`        | `int` | Must be within [limit_min, limit_max] |
| `maintenance_position` | `int` | Must be within [limit_min, limit_max] |
| `mount_position`       | `int` | Must be within [limit_min, limit_max] |
| `shutdown_flag`        | `int` | Must be 0 or 1                        |
| `unsafe_flag`          | `int` | Must be 0 or 1 (rarely modified)      |
| `device_label`         | `str` | Auto-updates checksum                 |
| `axis_label`           | `str` | Optional, no validation               |

**Returns:** Success message containing old and new values.

**Raises:**

- `ConnectionError`: If unable to connect to the specified port.
- `IndexError`: If device_index is out of range.
- `ValueError`: If setting name is invalid, value type is incorrect, or value is out of range.

**Notes:** Label changes automatically update USER_DATA_0 (checksum) to maintain device validation. The `checksum`
setting cannot be modified directly as it is managed by the binding library.

**Important - shutdown_flag vs unsafe_flag:**
- `shutdown_flag`: Set to 1 for proper shutdown recovery. Use this when a motor wasn't properly shut down and the user
  has verified the motor is in a safe position for homing.
- `unsafe_flag`: Reflects physical hardware constraints. Only modify during initial setup if the hardware assembly
  changes. Do NOT modify this flag to work around improper shutdown issues.

**Note on axis_label:**
- The `axis_label` is optional and typically unused for Zaber motors. A missing axis_label is not a configuration issue.
- Axis labels are primarily used for third-party motors where the label reflects the motor name.
- For Zaber single-axis controllers, the `device_label` is sufficient for identification.

### validate_zaber_device_configuration

Validates device configuration for use with the binding library.

```python
def validate_zaber_device_configuration(port: str, device_index: int) -> ZaberValidationResult
```

**Parameters:**

| Parameter      | Type  | Description                            |
|----------------|-------|----------------------------------------|
| `port`         | `str` | Serial port path                       |
| `device_index` | `int` | Zero-based index in daisy-chain        |

**Returns:** `ZaberValidationResult` dataclass containing:

| Attribute         | Type              | Description                                              |
|-------------------|-------------------|----------------------------------------------------------|
| `is_valid`        | `bool`            | Overall validation result                                |
| `checksum_valid`  | `bool`            | Whether stored checksum matches calculated               |
| `positions_valid` | `bool`            | Whether all positions are within motion limits           |
| `errors`          | `tuple[str, ...]` | Critical issues preventing use with binding library      |
| `warnings`        | `tuple[str, ...]` | Non-critical issues that may affect device operation     |

**Raises:**

- `ConnectionError`: If unable to connect to the specified port.
- `IndexError`: If device_index is out of range.

---

## Dependencies

### External Requirements

| Dependency       | Required | Purpose                                        |
|------------------|----------|------------------------------------------------|
| zaber-motion     | Yes      | Python bindings for Zaber ASCII protocol       |
| USB serial port  | Yes      | Physical connection to Zaber controllers       |
| Port permissions | Yes      | User must be in `dialout` group on Linux       |

### Python Requirements

```
zaber-motion>=6.0.0
crc>=7.0.0
tabulate>=0.9.0
ataraxis-time>=2.0.0
```

---

## Code Examples

### Basic Motor Control

```python
from sl_experiment.mesoscope_vr.zaber_bindings import ZaberConnection

# Connect to motor group
connection = ZaberConnection(port="/dev/ttyUSB0")
connection.connect()

# Get motor interface
motor = connection.get_device(index=0).axis

# Home motor (establishes reference)
motor.unpark()
motor.home()
while motor.is_busy:
    pass  # Wait for homing to complete

# Move to mount position
motor.move(position=motor.mount_position)
while motor.is_busy:
    pass

# Park and disconnect
motor.park()
connection.disconnect()
```

### Multi-Motor Coordination

```python
from sl_experiment.mesoscope_vr.zaber_bindings import ZaberConnection

# Connect to daisy-chained motors
connection = ZaberConnection(port="/dev/ttyUSB0")
connection.connect()

# Get all motor axes
z_axis = connection.get_device(index=0).axis
pitch_axis = connection.get_device(index=1).axis
roll_axis = connection.get_device(index=2).axis

# Unpark all motors
z_axis.unpark()
pitch_axis.unpark()
roll_axis.unpark()

# Home all motors in parallel (non-blocking)
z_axis.home()
pitch_axis.home()
roll_axis.home()

# Wait for all to complete
while z_axis.is_busy or pitch_axis.is_busy or roll_axis.is_busy:
    pass

# Move all motors to park position in parallel
z_axis.move(position=z_axis.park_position)
pitch_axis.move(position=pitch_axis.park_position)
roll_axis.move(position=roll_axis.park_position)

# Wait and park
while z_axis.is_busy or pitch_axis.is_busy or roll_axis.is_busy:
    pass

z_axis.park()
pitch_axis.park()
roll_axis.park()

connection.disconnect()
```

### Position Snapshot and Restoration

```python
from sl_experiment.mesoscope_vr.zaber_bindings import ZaberConnection
from sl_shared_assets import ZaberPositions

# Connect
connection = ZaberConnection(port="/dev/ttyUSB0")
connection.connect()
motor = connection.get_device(index=0).axis

# Take position snapshot
current_position = int(motor.get_position())
positions = ZaberPositions(headbar_z=current_position)

# Later: restore from snapshot
motor.unpark()
motor.move(position=positions.headbar_z)
while motor.is_busy:
    pass
motor.park()

connection.disconnect()
```

### Emergency Stop

```python
from sl_experiment.mesoscope_vr.zaber_bindings import ZaberConnection

connection = ZaberConnection(port="/dev/ttyUSB0")
connection.connect()
motor = connection.get_device(index=0).axis

motor.unpark()
motor.move(position=50000)  # Start moving

# Emergency stop (can be called anytime, bypasses timing guards)
motor.stop()  # First call: decelerate and stop
motor.stop()  # Second rapid call: immediate stop

connection.disconnect()
```

---

## Integration with ZaberMotors Binding Class

The `ZaberMotors` class in `binding_classes.py` demonstrates the complete integration pattern:

### Initialization Pattern

```python
def __init__(
    self,
    zaber_positions: ZaberPositions | None,
    zaber_configuration: MesoscopeExternalAssets,
) -> None:
    # Create connections for each motor group
    self._headbar = ZaberConnection(port=zaber_configuration.headbar_port)
    self._wheel = ZaberConnection(port=zaber_configuration.wheel_port)
    self._lickport = ZaberConnection(port=zaber_configuration.lickport_port)

    # Connect and extract axes
    self._headbar.connect()
    self._headbar_z = self._headbar.get_device(index=0).axis
    self._headbar_pitch = self._headbar.get_device(index=1).axis
    self._headbar_roll = self._headbar.get_device(index=2).axis

    # Store previous positions for restoration
    self._previous_positions = zaber_positions
```

### Movement Pattern

```python
def park_position(self) -> None:
    """Moves all motors to park positions."""
    # 1. Unpark to allow movement
    self.unpark_motors()

    # 2. Issue all move commands (non-blocking)
    self._headbar_z.move(position=self._headbar_z.park_position)
    self._headbar_pitch.move(position=self._headbar_pitch.park_position)
    self._headbar_roll.move(position=self._headbar_roll.park_position)
    self._wheel_x.move(position=self._wheel_x.park_position)

    # 3. Wait for all movements to complete
    self.wait_until_idle()

    # 4. Park to prevent accidental movement
    self.park_motors()
```

### Wait Pattern

```python
def wait_until_idle(self) -> None:
    """Blocks until all motors finish moving."""
    while (
        self._headbar_z.is_busy
        or self._headbar_pitch.is_busy
        or self._headbar_roll.is_busy
        or self._wheel_x.is_busy
    ):
        pass  # Built-in delay in is_busy prevents overwhelming interface
```

### Disconnect Pattern

```python
def disconnect(self) -> None:
    """Shuts down all motors and closes connections."""
    self._headbar.disconnect()
    self._wheel.disconnect()
    self._lickport.disconnect()
```
