---
name: implementing-microcontroller-interface
description: >-
  Guides implementation of microcontroller hardware modules and PC interfaces using sl-micro-controllers and
  ataraxis-communication-interface. Covers firmware module creation, PC interface implementation, and integration
  patterns. Use when adding microcontroller-based hardware to any acquisition system.
---

# Microcontroller Interface Implementation

Guides the implementation of microcontroller hardware modules and their corresponding PC interfaces. This skill covers
the complete stack from firmware (C++) to Python interface for hardware controlled by Teensy microcontrollers.

---

## When to Use This Skill

Use this skill when:

- Adding a new hardware module to microcontrollers (sensors, actuators, I/O)
- Implementing the PC-side interface for a firmware module
- Understanding the communication protocol between PC and microcontrollers
- Troubleshooting microcontroller communication issues
- Learning the module development patterns

For system-specific integration (modifying sl-shared-assets configuration, integrating into mesoscope-vr), use the
`/modifying-mesoscope-vr-system` skill instead.

---

## Verification Requirements

**Before writing any microcontroller code, verify the current state of dependent libraries.**

### Step 0: Version Verification

Follow the **Cross-Referenced Library Verification** procedure in `CLAUDE.md`:

1. Check local sl-micro-controllers version against GitHub
2. Check local ataraxis-communication-interface version against GitHub
3. If version mismatch exists, ask the user how to proceed
4. Use the verified source for API reference

### Step 1: Content Verification

| Repository                       | File/Directory           | What to Check                                 |
|----------------------------------|--------------------------|-----------------------------------------------|
| sl-micro-controllers             | `src/*.h`                | Existing module patterns                      |
| sl-micro-controllers             | `src/main.cpp`           | Module registration and controller IDs        |
| ataraxis-communication-interface | `README.md`              | Current API and usage patterns                |
| sl-experiment                    | `module_interfaces.py`   | Existing PC interface patterns                |

### Step 2: Hardware Verification

**Before implementing a new module, verify microcontrollers are connected and accessible using MCP tools.**

The ataraxis-communication-interface library provides an MCP server for hardware discovery. Start the server with:
```bash
axci-mcp
```

**MCP Tools for Microcontroller Verification:**

| Tool                      | Purpose                                              |
|---------------------------|------------------------------------------------------|
| `list_microcontrollers()` | Discovers connected microcontrollers and their ports |
| `check_mqtt_broker()`     | Verifies MQTT broker is running (for Unity comms)    |

**Verification workflow:**

1. **Discover microcontrollers**: Run `list_microcontrollers()` to identify connected devices
2. **Note port assignments**: Record which port corresponds to which controller (ACTOR, SENSOR, ENCODER)
3. **Verify MQTT** (if applicable): Run `check_mqtt_broker(host="127.0.0.1", port=1883)`

**Expected output from `list_microcontrollers()`:**
```
Port: /dev/ttyACM0, Controller ID: 101 (ACTOR)
Port: /dev/ttyACM1, Controller ID: 152 (SENSOR)
Port: /dev/ttyACM2, Controller ID: 203 (ENCODER)
```

If the target microcontroller is not listed:
- Check USB connection
- Verify firmware is uploaded with correct controller ID
- Check for port permission issues (`sudo usermod -a -G dialout $USER`)

---

## Architecture Overview

The microcontroller ecosystem consists of three interconnected layers:

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           Hardware Layer (Teensy 4.1)                           │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │  sl-micro-controllers                                                     │  │
│  │  ────────────────────                                                     │  │
│  │  Module classes (C++)  →  Command handlers  →  GPIO/ADC/PWM control       │  │
│  │  Kernel scheduling     →  Runtime cycle     →  Communication              │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │ Serial/USB
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         Communication Layer (Python)                            │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │  ataraxis-communication-interface                                         │  │
│  │  ────────────────────────────────                                         │  │
│  │  SerialCommunication  →  Message serialization  →  Transport layer        │  │
│  │  MicroControllerInterface  →  Process management  →  Queue routing        │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                    │ API calls
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          Application Layer (Python)                             │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │  sl-experiment                                                            │  │
│  │  ─────────────                                                            │  │
│  │  ModuleInterface subclasses  →  User-facing API  →  SharedMemory IPC      │  │
│  │  MicroControllerInterfaces   →  Orchestration    →  Lifecycle management  │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Workflow

Adding a new microcontroller hardware module requires changes in multiple repositories:

```
Phase 1: Firmware Implementation (sl-micro-controllers)
├── 1.1 Create module header file (new_module.h)
├── 1.2 Define type codes, command codes, data codes
├── 1.3 Implement command handlers
├── 1.4 Register module in main.cpp
└── 1.5 Upload firmware to microcontroller

Phase 2: PC Interface Implementation (sl-experiment)
├── 2.1 Create ModuleInterface subclass in module_interfaces.py
├── 2.2 Define matching codes and parameters
├── 2.3 Implement lifecycle methods
├── 2.4 Add to MicroControllerInterfaces binding class
└── 2.5 Integrate into data_acquisition.py
```

---

## Phase 1: Firmware Implementation

See [FIRMWARE_MODULE_GUIDE.md](FIRMWARE_MODULE_GUIDE.md) for the complete firmware implementation reference including:

- Module class structure and inheritance
- Template parameter patterns
- Command handler implementation
- Multi-stage command execution
- Parameter structures and serialization
- Module registration in main.cpp

### Quick Reference: Module Structure

```cpp
template <const uint8_t kPin, const bool kDefaultState>
class NewModule final : public Module {
  public:
    // Constructor registers with communication
    explicit NewModule(
        const uint8_t module_type,
        const uint8_t module_id,
        Communication& communication
    ) : Module(module_type, module_id, communication) {}

    // Required virtual methods
    bool SetupModule() override;
    bool SetCustomParameters() override;
    bool RunActiveCommand() override;

  private:
    // Module-specific enums and parameters
    enum class kModuleCommands : uint8_t { kCommand1 = 1, kCommand2 = 2 };
    enum class kCustomStatusCodes : uint8_t { kStatus1 = 51, kStatus2 = 52 };

    struct CustomRuntimeParameters {
        uint32_t parameter_a = 1000;
    } PACKED_STRUCT _custom_parameters;

    // Command handler methods
    void ExecuteCommand1();
    void ExecuteCommand2();
};
```

---

## Phase 2: PC Interface Implementation

See [PC_INTERFACE_GUIDE.md](PC_INTERFACE_GUIDE.md) for the complete PC interface implementation reference including:

- ModuleInterface class structure
- Lifecycle methods (initialize_remote_assets, terminate_remote_assets)
- Command sending patterns
- Data processing with process_received_data
- SharedMemoryArray IPC patterns
- Integration with MicroControllerInterfaces

### Quick Reference: Interface Structure

```python
class NewModuleInterface(ModuleInterface):
    """PC interface for the new hardware module.

    Args:
        parameter_a: Configuration parameter from system config.
    """

    def __init__(self, parameter_a: int) -> None:
        data_codes: set[np.uint8] = {np.uint8(51), np.uint8(52)}
        super().__init__(
            module_type=np.uint8(X),      # Must match firmware
            module_id=np.uint8(Y),        # Must match firmware
            data_codes=data_codes,
            error_codes=None,
        )
        self._parameter_a: int = parameter_a
        self._command1: np.uint8 = np.uint8(1)  # Must match firmware

    def initialize_remote_assets(self) -> None:
        """Called in communication process before message loop."""
        pass  # Connect to shared memory if needed

    def terminate_remote_assets(self) -> None:
        """Called in communication process during shutdown."""
        pass  # Disconnect from shared memory

    def process_received_data(self, message: ModuleData | ModuleState) -> None:
        """Processes incoming data from the module."""
        if message.event == 51:
            # Handle status 1
            pass

    def execute_command1(self) -> None:
        """User-facing method to trigger command 1."""
        self.send_command(
            command=self._command1,
            noblock=np.bool_(False),
            repetition_delay=np.uint32(0),
        )
```

---

## Code Matching Requirements

The firmware and PC interface MUST use matching codes:

| Code Type     | Firmware Location              | PC Location                     |
|---------------|--------------------------------|---------------------------------|
| Module type   | Constructor parameter          | `__init__` `module_type`        |
| Module ID     | Constructor parameter          | `__init__` `module_id`          |
| Commands      | `kModuleCommands` enum         | `np.uint8` command constants    |
| Data codes    | `kCustomStatusCodes` enum      | `data_codes` set in `__init__`  |
| Error codes   | `kCustomStatusCodes` enum      | `error_codes` set in `__init__` |
| Parameters    | `CustomRuntimeParameters`      | `send_parameters()` tuple order |

**Critical:** Parameter types and order in `send_parameters()` must exactly match the firmware's 
`CustomRuntimeParameters` struct. Mismatches cause communication failures or data corruption.

---

## Module Type Code Allocation

Current sl-micro-controllers allocations:

| Type Code | Module              | Controller | Purpose                    |
|-----------|---------------------|------------|----------------------------|
| 1         | TTLModule           | SENSOR     | TTL input/output           |
| 2         | EncoderModule       | ENCODER    | Quadrature encoder         |
| 3         | BrakeModule         | ACTOR      | Electromagnetic brake      |
| 4         | LickModule          | SENSOR     | Conductive lick sensor     |
| 5         | ValveModule         | ACTOR      | Solenoid valves            |
| 6         | TorqueModule        | SENSOR     | Torque sensor              |
| 7         | ScreenModule        | ACTOR      | Screen power control       |

**Available type codes:** 8-255 (reserve 8-49 for common modules, 50+ for specialized)

---

## Controller ID Allocation

Current microcontroller assignments:

| Controller ID | Type    | Purpose                               |
|---------------|---------|---------------------------------------|
| 101           | ACTOR   | Controls outputs (valves, brakes)     |
| 152           | SENSOR  | Monitors inputs (lick, torque, TTL)   |
| 203           | ENCODER | High-speed encoder monitoring         |

---

## Troubleshooting

### Communication Failures

1. Verify port assignment matches physical connection
2. Check keepalive interval matches between PC and firmware
3. Verify module type/ID codes match between firmware and PC
4. Check parameter types match exactly (numpy types on PC)

### Command Not Executing

1. Verify command code matches firmware enum value
2. Check module is registered in firmware main.cpp
3. Verify module instance is added to MicroControllerInterface

### Data Not Received

1. Verify data codes are in `data_codes` set
2. Check `process_received_data()` handles the event code
3. Verify SharedMemoryArray is connected in both processes

---

## Implementation Checklist

Before integrating a new microcontroller module:

### Firmware (sl-micro-controllers)

```
- [ ] Created module header file with template parameters
- [ ] Defined module commands enum (kModuleCommands)
- [ ] Defined status codes enum (kCustomStatusCodes, codes >= 51)
- [ ] Implemented SetupModule() with hardware initialization
- [ ] Implemented SetCustomParameters() for runtime parameters
- [ ] Implemented RunActiveCommand() with command dispatch
- [ ] Created command handler methods
- [ ] Added module registration to main.cpp for appropriate controller
- [ ] Compiled and uploaded firmware successfully
```

### PC Interface (sl-experiment)

```
- [ ] Created ModuleInterface subclass with matching type/ID codes
- [ ] Defined matching command codes as np.uint8 constants
- [ ] Added data_codes set with matching status codes
- [ ] Implemented initialize_remote_assets() (connect shared memory)
- [ ] Implemented terminate_remote_assets() (disconnect shared memory)
- [ ] Implemented process_received_data() for all data codes
- [ ] Created user-facing methods using send_command()
- [ ] Created parameter setter using send_parameters()
- [ ] Added to MicroControllerInterfaces binding class
- [ ] Integrated into data_acquisition.py lifecycle
- [ ] MyPy strict passes
```
