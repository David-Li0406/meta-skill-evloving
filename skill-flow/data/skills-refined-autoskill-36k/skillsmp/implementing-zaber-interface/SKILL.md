---
name: implementing-zaber-interface
description: >-
  Guides implementation of Zaber motor interfaces using the zaber-motion library. Covers motor discovery, position
  management, safety patterns, and binding class patterns. Use when adding Zaber motor support to any acquisition
  system or troubleshooting motor connectivity.
---

# Zaber Interface Implementation

Guides the implementation of Zaber motor interfaces using the zaber-motion library. This skill focuses on the low-level
hardware integration patterns applicable to any acquisition system.

---

## When to Use This Skill

Use this skill when:

- Adding Zaber motor support to an acquisition system
- Troubleshooting Zaber motor connectivity issues
- Verifying motor configuration before runtime
- Understanding the ZaberConnection/ZaberDevice/ZaberAxis API hierarchy
- Configuring motor positions in non-volatile memory

For system-specific integration (modifying sl-shared-assets configuration, integrating into mesoscope-vr), use the
`/modifying-mesoscope-vr-system` skill instead.

---

## Verification Requirements

**Before writing any Zaber code, verify the hardware is connected and accessible.**

### Step 0: Hardware Verification

Use the sl-experiment MCP server for Zaber discovery. Start the server with:
```bash
sl-get mcp
```

**MCP Tool for Verification:**

| Tool                     | Purpose                                            |
|--------------------------|----------------------------------------------------|
| `get_zaber_devices_tool` | Discovers Zaber devices and their ports/axes       |

**Verification workflow:**

1. **Discover Zaber devices**: Run `get_zaber_devices_tool()` to identify connected motors
2. **Note port assignments**: Record which `/dev/ttyUSB*` port corresponds to which motor group
3. **Verify device order**: Confirm daisy-chain order matches expected configuration

**Expected output from `get_zaber_devices_tool()`:**
```
+----------------+------------+-------+---------+-------------+---------+-------------+
|      Port      | Device Num |  ID   |  Label  |    Name     | Axis ID | Axis Label  |
+----------------+------------+-------+---------+-------------+---------+-------------+
| /dev/ttyUSB0   |     1      | 30341 | HeadBar |  X-LDA025A  |    1    |      Z      |
|                |     2      | 30341 |         |  X-LDA025A  |    1    |    Pitch    |
|                |     3      | 30341 |         |  X-LDA025A  |    1    |    Roll     |
+----------------+------------+-------+---------+-------------+---------+-------------+
```

If motors are not detected:
- Check USB connections and power supplies
- Verify port permissions (`sudo usermod -a -G dialout $USER`)
- Ensure motors are powered on before connecting USB
- Check for port conflicts with other applications

### Step 1: Content Verification

| File                                                              | What to Check                            |
|-------------------------------------------------------------------|------------------------------------------|
| `sl-experiment/src/sl_experiment/mesoscope_vr/zaber_bindings.py`  | ZaberConnection/Device/Axis patterns     |
| `sl-experiment/src/sl_experiment/mesoscope_vr/binding_classes.py` | ZaberMotors binding class implementation |
| `sl-experiment pyproject.toml`                                    | Current zaber-motion version dependency  |

---

## Architecture Overview

Zaber motor control uses a tri-class hierarchy:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        ZaberConnection (Port Level)                             │
│  ────────────────────────────────────────────────────────────────────────────── │
│  - Manages serial port connection                                               │
│  - Discovers all devices on the port                                            │
│  - Coordinates shutdown across all devices                                      │
│                                                                                 │
│     ┌─────────────────────────────────────────────────────────────────────────┐ │
│     │                    ZaberDevice (Controller Level)                       │ │
│     │  ─────────────────────────────────────────────────────────────────────  │ │
│     │  - Validates device configuration (checksum verification)               │ │
│     │  - Manages shutdown tracking in non-volatile memory                     │ │
│     │  - Exposes the axis (motor) interface                                   │ │
│     │                                                                         │ │
│     │     ┌─────────────────────────────────────────────────────────────────┐ │ │
│     │     │                   ZaberAxis (Motor Level)                       │ │ │
│     │     │  ────────────────────────────────────────────────────────────── │ │ │
│     │     │  - Executes motion commands (home, move, stop)                  │ │ │
│     │     │  - Manages predefined positions (park, mount, maintenance)      │ │ │
│     │     │  - Enforces communication timing and safety patterns            │ │ │
│     │     └─────────────────────────────────────────────────────────────────┘ │ │
│     └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

**Key relationships:**
- One `ZaberConnection` per serial port (USB cable)
- Multiple `ZaberDevice` instances per connection (daisy-chained motors)
- One `ZaberAxis` per device (single-axis controllers only)

---

## Motor Discovery

Use the MCP tool `get_zaber_devices_tool()` to discover connected Zaber motors.

### Discovery Output Fields

| Field       | Description                                                          |
|-------------|----------------------------------------------------------------------|
| Port        | Serial port path (e.g., `/dev/ttyUSB0`)                              |
| Device Num  | Position in daisy-chain (1 = closest to USB)                         |
| ID          | Hardware device identifier code                                      |
| Label       | User-assigned label stored in non-volatile memory                    |
| Name        | Manufacturer model name                                              |
| Axis ID     | Axis number within the device (always 1 for single-axis controllers) |
| Axis Label  | User-assigned axis label stored in non-volatile memory               |

### Daisy-Chain Ordering

Motors connected to the same serial port form a daisy-chain. The device number reflects physical position:

```
USB Port ──► Device 1 ──► Device 2 ──► Device 3
             (index 0)    (index 1)    (index 2)
```

**Important:** When adding motors, document the expected daisy-chain order in configuration. Misordering causes motors
to move incorrectly.

---

## Position Management

Zaber motors use predefined positions stored in non-volatile memory for safe operation.

### Position Types

| Position    | Purpose                                           | When Used                        |
|-------------|---------------------------------------------------|----------------------------------|
| Park        | Safe position for shutdown and storage            | System shutdown, storage         |
| Mount       | Position for mounting animal into enclosure       | Session start, animal mounting   |
| Maintenance | Position for system maintenance and cleaning      | Between sessions, maintenance    |

### Position Storage

Positions are stored in non-volatile USER_DATA variables on each motor controller:

| Variable      | Purpose                                              |
|---------------|------------------------------------------------------|
| USER_DATA_11  | Park position (native motor units)                   |
| USER_DATA_12  | Maintenance position (native motor units)            |
| USER_DATA_13  | Mount position (native motor units)                  |

### Position Restoration

The `ZaberMotors` binding class supports restoring motors to previous session positions using `ZaberPositions` from
sl-shared-assets. This enables consistent animal positioning across sessions.

---

## Agentic Configuration Management

Use MCP tools to read and modify Zaber motor configuration stored in non-volatile memory.

### Available MCP Tools

| Tool                                                                          | Purpose                        |
|-------------------------------------------------------------------------------|--------------------------------|
| `get_zaber_devices_tool()`                                                    | Discover connected motors      |
| `get_zaber_device_settings_tool(port, device_index)`                          | Read device configuration      |
| `set_zaber_device_setting_tool(port, device_index, setting, value, confirm)`  | Modify device setting          |
| `validate_zaber_configuration_tool(port, device_index)`                       | Validate device configuration  |
| `get_checksum_tool(input_string)`                                             | Calculate CRC32-XFER checksum  |

### Configuration Workflow

#### Reading Current Configuration

1. Discover devices: `get_zaber_devices_tool()`
2. Read settings: `get_zaber_device_settings_tool(port="/dev/ttyUSB0", device_index=0)`
3. Validate configuration: `validate_zaber_configuration_tool(port="/dev/ttyUSB0", device_index=0)`

#### Modifying Configuration

**Safety Protocol:**

1. Read current value using `get_zaber_device_settings_tool()`
2. Show user the current value and proposed change
3. Preview change: `set_zaber_device_setting_tool(..., confirm=False)`
4. Execute change: `set_zaber_device_setting_tool(..., confirm=True)`
5. Verify change: `get_zaber_device_settings_tool()`

### Configurable Settings

| Setting                  | Type  | Description                              | Constraints                   |
|--------------------------|-------|------------------------------------------|-------------------------------|
| `park_position`          | `int` | Shutdown position (native units)         | Must be within motion limits  |
| `maintenance_position`   | `int` | Maintenance position (native units)      | Must be within motion limits  |
| `mount_position`         | `int` | Animal mounting position (native units)  | Must be within motion limits  |
| `shutdown_flag`          | `int` | Proper shutdown indicator (see below)    | 0 or 1                        |
| `unsafe_flag`            | `int` | Requires safe position for homing        | 0 or 1 (rarely modified)      |
| `device_label`           | `str` | Device identifier                        | Auto-updates checksum         |
| `axis_label`             | `str` | Axis identifier (optional, see below)    | No constraints                |

### Read-Only Settings

| Setting            | Description                      |
|--------------------|----------------------------------|
| `checksum`         | Auto-calculated from device_label|
| `limit_min`        | Hardware motion limit            |
| `limit_max`        | Hardware motion limit            |
| `current_position` | Live motor position              |

### Understanding shutdown_flag vs unsafe_flag

**shutdown_flag (USER_DATA_1):**
- Set to `1` during proper system shutdown, set to `0` at startup
- If a motor with `unsafe_flag=1` has `shutdown_flag=0`, the system prompts for manual verification before homing
- **This is the flag you typically manage** when recovering from improper shutdown (power loss, crash, etc.)
- To recover: manually verify the motor is in a safe position, then set `shutdown_flag` to `1`

**unsafe_flag (USER_DATA_10):**
- Indicates whether the motor can be positioned unsafely for homing (e.g., where homing could cause collision)
- **This flag is set during initial hardware setup** and reflects physical assembly constraints
- **Do NOT modify this flag** unless the physical hardware configuration has changed
- If a motor's physical mounting allows safe homing from any position, `unsafe_flag` should be `0`
- If a motor could be left in a position that makes homing dangerous, `unsafe_flag` should be `1`

**Recovery workflow for improper shutdown:**
1. User confirms the motor is physically positioned safely for homing
2. Agent sets `shutdown_flag` to `1` using `set_zaber_device_setting_tool`
3. System can now initialize normally without the improper shutdown warning

### Understanding axis_label vs device_label

**device_label:**
- Required for all motors. Used for checksum validation to verify the device is configured for the binding library.
- Examples: "HeadBar", "Wheel", "Lickport"

**axis_label:**
- Optional and typically unused for Zaber motors. A missing axis_label is not an issue.
- Axis labels are primarily used for third-party motors where the label reflects the specific motor name.
- For Zaber single-axis controllers, the device_label is sufficient for identification.
- Do not flag missing axis_label as a configuration problem.

### Initial Device Setup Workflow

For new motors not yet configured for use with the binding library:

1. **Discover device**: `get_zaber_devices_tool()`
2. **Set device label**: `set_zaber_device_setting_tool(port, index, "device_label", "HeadBar", confirm=True)`
   (This automatically calculates and sets the checksum)
3. **Set axis label**: `set_zaber_device_setting_tool(port, index, "axis_label", "Z", confirm=True)`
4. **Set positions**: Configure park, maintenance, and mount positions
5. **Set unsafe flag** (if needed): Only set this during initial setup based on physical hardware constraints.
   Set to `1` if the motor can be positioned unsafely for homing (e.g., where homing could cause collision).
6. **Validate**: `validate_zaber_configuration_tool(port, index)`

### Improper Shutdown Recovery Workflow

When a motor with `unsafe_flag=1` was not properly shut down:

1. **Read current settings**: `get_zaber_device_settings_tool(port, index)` to confirm `shutdown_flag=0`
2. **User verification**: Ask the user to physically verify the motor is in a safe position for homing
3. **Reset shutdown flag**: `set_zaber_device_setting_tool(port, index, "shutdown_flag", "1", confirm=True)`
4. **Validate**: `validate_zaber_configuration_tool(port, index)` should now show no warnings

**Important:** Never modify `unsafe_flag` to work around improper shutdown. The `unsafe_flag` reflects physical
hardware constraints and should only be changed if the hardware assembly changes.

---

## Safety Patterns

### Park/Unpark Workflow

Motors use a parking mechanism to prevent accidental movement:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Motor Safety State Machine                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────┐                                                          │
│   │  PARKED  │ ◄──── park() ──── Motors cannot move                     │
│   └────┬─────┘                                                          │
│        │                                                                │
│    unpark()                                                             │
│        │                                                                │
│        ▼                                                                │
│   ┌──────────┐                                                          │
│   │ UNPARKED │ ◄──── Motors can execute commands                        │
│   └────┬─────┘                                                          │
│        │                                                                │
│    home() / move() / etc.                                               │
│        │                                                                │
│        ▼                                                                │
│   ┌──────────┐                                                          │
│   │  MOVING  │ ◄──── is_busy = True                                     │
│   └────┬─────┘                                                          │
│        │                                                                │
│    wait_until_idle()                                                    │
│        │                                                                │
│        ▼                                                                │
│   ┌──────────┐                                                          │
│   │   IDLE   │ ◄──── is_busy = False, ready for next command            │
│   └──────────┘                                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Critical pattern:** Always call `unpark_motors()` before movement and `park_motors()` after completion.

### Shutdown Safety

Motors use non-volatile flags to detect improper shutdown:

| Flag          | Variable      | Purpose                                                |
|---------------|---------------|--------------------------------------------------------|
| Shutdown flag | USER_DATA_1   | Set to 1 on proper shutdown, 0 on startup              |
| Unsafe flag   | USER_DATA_10  | Indicates motor requires specific position for homing  |

If a motor with `unsafe_flag=True` was not properly shut down, the system prompts for manual verification before
proceeding.

### Checksum Validation

Each device stores a CRC32-XFER checksum of its label in USER_DATA_0. This validates that the motor is configured for
use with the binding library:

```python
# Calculate expected checksum
from sl_experiment.mesoscope_vr import CRCCalculator
calculator = CRCCalculator()
expected = calculator.string_checksum("HeadBar")  # Device label
```

Use the MCP tool `get_checksum_tool(input_string)` to calculate checksums for configuration.

---

## ZaberAxis API Reference

See [ZABER_INTERFACE_GUIDE.md](ZABER_INTERFACE_GUIDE.md) for the complete API reference including:

- ZaberConnection constructor and methods
- ZaberDevice configuration validation
- ZaberAxis motion commands and properties
- Non-volatile memory settings structure
- Complete code examples

---

## Binding Class Patterns

When implementing Zaber motor support in a binding class, follow these patterns:

### Basic Structure

```python
class ZaberMotors:
    """Manages Zaber motor groups for the acquisition system.

    Args:
        zaber_positions: Previous session positions or None for defaults.
        zaber_configuration: Motor configuration from system config.

    Attributes:
        _connection: ZaberConnection for the motor group.
        _axis: ZaberAxis for the motor.
    """

    def __init__(
        self,
        zaber_positions: ZaberPositions | None,
        zaber_configuration: ExternalAssetsConfig,
    ) -> None:
        # Initialize connection
        self._connection: ZaberConnection = ZaberConnection(
            port=zaber_configuration.motor_port
        )

        # Connect and get device/axis
        self._connection.connect()
        self._axis: ZaberAxis = self._connection.get_device(index=0).axis

        # Store previous positions for restoration
        self._previous_positions = zaber_positions

    def restore_position(self) -> None:
        """Restores motors to previous session positions."""
        self.unpark_motors()

        if self._previous_positions is not None:
            self._axis.move(position=self._previous_positions.motor_position)
        else:
            self._axis.move(position=self._axis.mount_position)

        self.wait_until_idle()
        self.park_motors()

    def wait_until_idle(self) -> None:
        """Blocks until all motors finish moving."""
        while self._axis.is_busy:
            pass

    def disconnect(self) -> None:
        """Shuts down motors and closes connection."""
        self._connection.disconnect()

    def park_motors(self) -> None:
        """Parks all motors to prevent accidental movement."""
        self._axis.park()

    def unpark_motors(self) -> None:
        """Unparks motors to allow movement commands."""
        self._axis.unpark()
```

### Key Patterns

| Pattern                | Purpose                                          |
|------------------------|--------------------------------------------------|
| Park/unpark guards     | Prevent accidental movement during idle periods  |
| Position restoration   | Maintain consistent animal positioning           |
| Wait until idle        | Coordinate multi-motor movements                 |
| Destructor disconnect  | Ensure proper shutdown on garbage collection     |

---

## Configuration Requirements

Motor configuration must be defined in sl-shared-assets before implementation.

### Required Configuration Fields

| Field          | Type  | Description                                  |
|----------------|-------|----------------------------------------------|
| `*_port`       | `str` | Serial port path (e.g., `/dev/ttyUSB0`)      |

### Configuration Dataclass Pattern

```python
@dataclass()
class SystemExternalAssets:
    """External asset configuration for the acquisition system."""

    headbar_port: str = "/dev/ttyUSB0"
    """Serial port for the headbar motor group."""

    wheel_port: str = "/dev/ttyUSB1"
    """Serial port for the wheel position motor."""
```

### Position Data Pattern

```python
@dataclass()
class ZaberPositions:
    """Stores motor positions for session restoration."""

    headbar_z: int = 0
    """Headbar Z-axis position in native motor units."""

    headbar_pitch: int = 0
    """Headbar pitch-axis position in native motor units."""

    headbar_roll: int = 0
    """Headbar roll-axis position in native motor units."""
```

---

## Troubleshooting

### Motor Not Detected

1. Verify USB cable is connected and motor is powered
2. Check port permissions: `ls -la /dev/ttyUSB*`
3. Add user to dialout group: `sudo usermod -a -G dialout $USER` (requires logout)
4. Verify no other application is using the port
5. Run `get_zaber_devices_tool()` to check discovery

### Checksum Validation Failure

1. Motor not configured for use with binding library
2. Calculate expected checksum: `get_checksum_tool("DeviceLabel")`
3. Use Zaber Launcher to set USER_DATA_0 to calculated checksum
4. Verify device label matches expected value

### Improper Shutdown Warning

1. Motor was not shut down properly in previous session
2. Verify motor is positioned safely for homing
3. Enter 'yes' when prompted to proceed
4. Or manually set USER_DATA_1 to 1 in Zaber Launcher

### Movement Not Executing

1. Verify motor is unparked: `is_parked` property
2. Verify motor is homed: `is_homed` property
3. Verify motor is idle: `is_busy` property
4. Check target position is within limits

### Daisy-Chain Order Mismatch

1. Run `get_zaber_devices_tool()` to see actual order
2. Compare Device Num with expected configuration
3. Physically reorder cables if necessary
4. Update configuration to match actual order

---

## Implementation Checklist

Before integrating Zaber motors into an acquisition system:

```
- [ ] Discovered motors using get_zaber_devices_tool()
- [ ] Recorded port assignments for each motor group
- [ ] Verified daisy-chain order matches expected configuration
- [ ] Calculated and verified checksum for each device label
- [ ] Confirmed motors have predefined positions in non-volatile memory
- [ ] Created configuration dataclass in sl-shared-assets
- [ ] Implemented binding class with park/unpark safety patterns
- [ ] Added position snapshot and restoration support
- [ ] Integrated into data_acquisition.py lifecycle
- [ ] MyPy strict passes
```
