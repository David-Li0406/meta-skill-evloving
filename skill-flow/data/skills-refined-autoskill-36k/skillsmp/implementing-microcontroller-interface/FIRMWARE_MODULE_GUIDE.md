# Firmware Module Implementation Guide

Complete reference for implementing hardware modules in the sl-micro-controllers firmware library. This guide covers
the C++ implementation patterns for Teensy 4.1 microcontrollers using the ataraxis-micro-controller library.

---

## Repository Locations

**sl-micro-controllers** (typically `../sl-micro-controllers/` relative to sl-experiment):
- `src/main.cpp` - Module registration and controller configuration
- `src/*.h` - Module implementation files (header-only)

**ataraxis-micro-controller** (typically `../ataraxis-micro-controller/` or installed via PlatformIO):
- `src/module.h` - Module base class
- `src/communication.h` - Communication class
- `src/kernel.h` - Kernel class
- `src/axmc_shared_assets.h` - Protocol codes and data structures

Note: These libraries are typically located in the same parent directory as sl-experiment. Use the Cross-Referenced
Library Verification procedure in `CLAUDE.md` to locate and verify the correct versions.

---

## Module Base Class API

All modules inherit from the `Module` base class provided by ataraxis-micro-controller.

### ExecutionControlParameters Structure

The `execution_parameters` member tracks command execution state:

```cpp
struct ExecutionControlParameters
{
    uint8_t command          = 0;      // Currently executed command
    uint8_t stage            = 0;      // Stage of currently executed command (starts at 1)
    bool noblock             = false;  // Blocking/non-blocking flag
    uint8_t next_command     = 0;      // Next command to execute
    bool next_noblock        = false;  // Noblock flag for next command
    bool new_command         = false;  // Tracks if next_command is new
    bool run_recurrently     = false;  // Tracks if next_command is recurrent
    uint32_t recurrent_delay = 0;      // Delay in microseconds between repetitions
    elapsedMicros recurrent_timer;     // Measures recurrent delays
    elapsedMicros delay_timer;         // Measures delays between stages
};
```

### Required Virtual Methods

Every module MUST override these three pure virtual methods:

| Method                   | Purpose                                        | Return Value             |
|--------------------------|------------------------------------------------|--------------------------|
| `SetupModule()`          | Initialize hardware and set default parameters | `true` if successful     |
| `SetCustomParameters()`  | Extract runtime parameters from PC message     | `true` if successful     |
| `RunActiveCommand()`     | Dispatch and execute commands                  | `true` if command found  |

### Protected Utility Methods

| Method                                      | Purpose                                              |
|---------------------------------------------|------------------------------------------------------|
| `GetActiveCommand()`                        | Returns current command code (uint8_t)               |
| `AdvanceCommandStage()`                     | Increments stage counter and resets delay timer      |
| `CompleteCommand()`                         | Marks command as finished (MUST call when done)      |
| `AbortCommand()`                            | Cancels command and resets execution state           |
| `WaitForMicros(uint32_t)`                   | Non-blocking delay (returns true when elapsed)       |
| `SendData(uint8_t event_code)`              | Sends status code without data payload               |
| `SendData(uint8_t, kPrototypes, data)`      | Sends status code with typed data payload            |
| `AnalogRead(uint8_t pin, uint16_t pool)`    | Reads and averages analog pin values                 |
| `DigitalRead(uint8_t pin, uint16_t pool)`   | Reads and averages digital pin values                |

### Core Status Codes (Reserved 0-50)

| Code | Constant                | Purpose                |
|------|-------------------------|------------------------|
| 0    | `kStandBy`              | Module idle            |
| 1    | `kTransmissionError`    | Communication failure  |
| 2    | `kCommandCompleted`     | Command finished       |
| 3    | `kCommandNotRecognized` | Unknown command code   |

---

## Module Template Pattern

Modules use C++ templates for compile-time hardware configuration:

```cpp
#pragma once

#include "module.h"

template <
    const uint8_t kPin,
    const bool kNormallyOff,
    const bool kStartOff = true>
class NewModule final : public Module
{
  public:
    explicit NewModule(
        const uint8_t module_type,
        const uint8_t module_id,
        Communication& communication
    ) : Module(module_type, module_id, communication) {}

    bool SetupModule() override;
    bool SetCustomParameters() override;
    bool RunActiveCommand() override;

  private:
    // Enums, parameters, and methods defined below
};
```

### Template Parameter Guidelines

| Type       | Use Case                              | Example                        |
|------------|---------------------------------------|--------------------------------|
| `uint8_t`  | Pin numbers, counts                   | `kValvePin`, `kEncoderPinA`    |
| `bool`     | Hardware polarity, default states     | `kNormallyClosed`, `kStartOff` |
| `uint16_t` | Larger constants (calibration)        | `kDefaultThreshold`            |

**Sentinel values:** Use `255` for optional pins that may not be configured:
```cpp
template <const uint8_t kTonePin = 255>  // 255 = not configured
// In implementation:
if (kTonePin != 255) { /* configure tone pin */ }
```

---

## Code Definitions

### Module Commands Enum

```cpp
private:
    enum class kModuleCommands : uint8_t
    {
        kSendPulse = 1,  // Opens output, waits, closes output.
        kToggleOn  = 2,  // Enables the output.
        kToggleOff = 3,  // Disables the output.
    };
```

### Custom Status Codes Enum

Custom codes MUST use values 51-250 (0-50 reserved for system):

```cpp
private:
    enum class kCustomStatusCodes : uint8_t
    {
        kActivated   = 51,  // Output activated.
        kDeactivated = 52,  // Output deactivated.
        kValueRead   = 53,  // Sensor value read.
    };
```

---

## Runtime Parameters Structure

Parameters must use `PACKED_STRUCT` macro for correct binary serialization:

```cpp
private:
    struct CustomRuntimeParameters
    {
        uint32_t pulse_duration = 100000;  // Default: 100ms in microseconds.
        uint16_t threshold      = 2000;    // Default: 2000 ADC units.
        uint8_t pool_size       = 10;      // Default: 10 samples.
    } PACKED_STRUCT _custom_parameters;
```

### Supported Parameter Types

| C++ Type   | Size     | Python Equivalent | Use Case                    |
|------------|----------|-------------------|-----------------------------|
| `bool`     | 1 byte   | `np.bool_`        | Enable flags                |
| `uint8_t`  | 1 byte   | `np.uint8`        | Small counts, codes         |
| `uint16_t` | 2 bytes  | `np.uint16`       | ADC values, medium counts   |
| `uint32_t` | 4 bytes  | `np.uint32`       | Microsecond durations       |
| `int8_t`   | 1 byte   | `np.int8`         | Signed small values         |
| `int16_t`  | 2 bytes  | `np.int16`        | Signed medium values        |
| `int32_t`  | 4 bytes  | `np.int32`        | Signed large values         |

**Critical:** Parameter order and types in the struct must EXACTLY match the PC's `send_parameters()` tuple.

---

## SetupModule() Implementation

Initialize hardware and set parameter defaults:

```cpp
bool SetupModule() override
{
    // Configure GPIO pins
    pinModeFast(kPin, OUTPUT);

    // Set initial state based on template parameters
    if (kStartOff)
    {
        digitalWriteFast(kPin, kNormallyOff ? LOW : HIGH);
        SendData(static_cast<uint8_t>(kCustomStatusCodes::kDeactivated));
    }
    else
    {
        digitalWriteFast(kPin, kNormallyOff ? HIGH : LOW);
        SendData(static_cast<uint8_t>(kCustomStatusCodes::kActivated));
    }

    // Reset parameters to defaults
    _custom_parameters.pulse_duration = 100000;
    _custom_parameters.threshold      = 2000;
    _custom_parameters.pool_size      = 10;

    return true;
}
```

**Pattern rules:**
- Use `pinModeFast()` and `digitalWriteFast()` (not standard Arduino functions)
- Send initial status to PC with `SendData()`
- Reset all `_custom_parameters` fields to default values
- Return `true` on success

---

## SetCustomParameters() Implementation

Extract parameters from PC message into the parameters' struct:

```cpp
bool SetCustomParameters() override
{
    // Extract entire struct at once (NOT individual parameters)
    if (_communication.ExtractModuleParameters(_custom_parameters))
    {
        // Post-processing: calculate derived values if needed
        _derived_value = _custom_parameters.threshold * 2;
        return true;
    }
    return false;
}
```

**Critical:** `ExtractModuleParameters()` extracts into the WHOLE struct at once. The PC must send parameters in the
exact same order and types as the struct definition.

**With post-processing (from ValveModule):**

```cpp
bool SetCustomParameters() override
{
    if (_communication.ExtractModuleParameters(_custom_parameters))
    {
        // Adjust values based on configuration
        if (kTonePin == 255) _custom_parameters.tone_duration = 0;
        if (_custom_parameters.tone_duration > _custom_parameters.pulse_duration)
            _tone_time_delta = _custom_parameters.tone_duration - _custom_parameters.pulse_duration;
        else _tone_time_delta = 0;
        return true;
    }
    return false;
}
```

---

## RunActiveCommand() Implementation

Dispatch commands to handler methods:

```cpp
bool RunActiveCommand() override
{
    switch (static_cast<kModuleCommands>(GetActiveCommand()))
    {
        case kModuleCommands::kSendPulse: SendPulse(); return true;
        case kModuleCommands::kToggleOn:  Activate();  return true;
        case kModuleCommands::kToggleOff: Deactivate(); return true;
        default: return false;  // Command not recognized
    }
}
```

**Pattern rules:**
- Cast `GetActiveCommand()` to the module's `kModuleCommands` enum
- Each case calls a private handler method
- Return `true` for recognized commands
- Return `false` for unrecognized commands (triggers `kCommandNotRecognized`)

---

## Command Handler Patterns

### Simple Immediate Command

For commands that complete in one step:

```cpp
void Activate()
{
    digitalWriteFast(kPin, kNormallyOff ? HIGH : LOW);
    SendData(static_cast<uint8_t>(kCustomStatusCodes::kActivated));
    CompleteCommand();  // MUST call to mark command done
}
```

### Multi-Stage Command with Non-Blocking Delay

For commands requiring timed steps. **Stages start at 1, not 0:**

```cpp
void SendPulse()
{
    switch (execution_parameters.stage)
    {
        // Stage 1: Activate output
        case 1:
            digitalWriteFast(kPin, kNormallyOff ? HIGH : LOW);
            SendData(static_cast<uint8_t>(kCustomStatusCodes::kActivated));
            AdvanceCommandStage();
            return;

        // Stage 2: Wait for pulse duration
        case 2:
            if (!WaitForMicros(_custom_parameters.pulse_duration)) return;
            AdvanceCommandStage();
            return;

        // Stage 3: Deactivate output
        case 3:
            digitalWriteFast(kPin, kNormallyOff ? LOW : HIGH);
            SendData(static_cast<uint8_t>(kCustomStatusCodes::kDeactivated));
            CompleteCommand();
            return;

        default: AbortCommand();
    }
}
```

**Key patterns:**
- Access stage via `execution_parameters.stage` directly
- Stages start at **1** (not 0)
- `WaitForMicros()` returns `false` while waiting, `true` when duration elapsed
- Call `return` after `AdvanceCommandStage()` to exit and re-enter on next cycle
- Call `CompleteCommand()` on final stage
- `default` case should call `AbortCommand()`

### Sensor Polling Command

For repeated sensor readings with static state:

```cpp
void CheckState()
{
    // Static variables persist between calls
    static uint16_t previous_readout = 0;

    // Read sensor with averaging
    const uint16_t signal = AnalogRead(kPin, _custom_parameters.pool_size);

    // Calculate change
    const auto delta = static_cast<uint16_t>(
        abs(static_cast<int32_t>(signal) - static_cast<int32_t>(previous_readout))
    );

    // Only send if change exceeds threshold
    if (delta <= _custom_parameters.delta_threshold)
    {
        CompleteCommand();
        return;
    }

    previous_readout = signal;

    // Send updated value
    if (signal >= _custom_parameters.signal_threshold)
    {
        SendData(
            static_cast<uint8_t>(kCustomStatusCodes::kValueRead),
            kPrototypes::kOneUint16,
            signal
        );
    }

    CompleteCommand();
}
```

### Blocking Command (Use Sparingly)

For operations that must complete atomically:

```cpp
void Calibrate()
{
    // Blocking loop - microcontroller unresponsive during execution
    for (uint16_t i = 0; i < _custom_parameters.calibration_count; ++i)
    {
        digitalWriteFast(kPin, HIGH);
        delayMicroseconds(_custom_parameters.pulse_duration);
        digitalWriteFast(kPin, LOW);
        delayMicroseconds(kCalibrationDelay);
    }

    SendData(static_cast<uint8_t>(kCustomStatusCodes::kCalibrated));
    CompleteCommand();
}
```

**Warning:** Blocking commands prevent all other processing. Use multi-stage patterns for long operations.

---

## Sending Data to PC

### Status Only (No Data Payload)

```cpp
SendData(static_cast<uint8_t>(kCustomStatusCodes::kActivated));
```

### Status with Typed Data Payload

```cpp
// Single uint16 value
SendData(
    static_cast<uint8_t>(kCustomStatusCodes::kValueRead),
    kPrototypes::kOneUint16,
    sensor_value
);

// Single uint32 value
SendData(
    static_cast<uint8_t>(kCustomStatusCodes::kDuration),
    kPrototypes::kOneUint32,
    elapsed_microseconds
);
```

### Data Prototypes (kPrototypes)

| Prototype          | C++ Type   | Bytes | Use Case                 |
|--------------------|------------|-------|--------------------------|
| `kOneBool`         | `bool`     | 1     | Boolean flags            |
| `kOneUint8`        | `uint8_t`  | 1     | Small counts, codes      |
| `kOneUint16`       | `uint16_t` | 2     | ADC values               |
| `kOneUint32`       | `uint32_t` | 4     | Timestamps, durations    |
| `kOneInt32`        | `int32_t`  | 4     | Signed encoder counts    |
| `kOneFloat32`      | `float`    | 4     | Calibrated values        |
| `kTwoUint8s`       | array      | 2     | Two byte values          |
| `kFourUint16s`     | array      | 8     | Four 16-bit values       |

See `axmc_shared_assets.h` for the complete list of 120+ prototypes.

---

## Compile-Time Calculations

Use `static constexpr` for hardware-dependent constants:

```cpp
private:
    // Calculate logical states based on polarity
    static constexpr bool kActivate = kNormallyOff ? HIGH : LOW;
    static constexpr bool kDeactivate = kNormallyOff ? LOW : HIGH;

    // For encoders with optional direction inversion
    static constexpr int32_t kMultiplier = kInvertDirection ? -1 : 1;
```

---

## Module Registration (main.cpp)

### Step 1: Include Header

```cpp
#ifdef ACTOR
    #include "new_module.h"
    // ... existing includes
#endif
```

### Step 2: Instantiate Module

```cpp
#ifdef ACTOR
    constexpr uint8_t kControllerID = 101;

    // Template<pin, polarity, start_state> instance(type, id, communication);
    NewModule<37, true, true> new_hardware(8, 1, axmc_communication);

    // Add to modules array
    Module* modules[] = {
        &wheel_brake,
        &reward_valve,
        &gas_puff_valve,
        &screen_trigger,
        &new_hardware  // Add new module
    };
#endif
```

**Constructor pattern:** `ModuleClass<template_params>(module_type, module_id, communication)`

### Controller Types

| Controller | ID  | Define     | Use For                                |
|------------|-----|------------|----------------------------------------|
| ACTOR      | 101 | `#ACTOR`   | Outputs (valves, brakes, LEDs)         |
| SENSOR     | 152 | `#SENSOR`  | Inputs (lick sensors, torque, TTL)     |
| ENCODER    | 203 | `#ENCODER` | High-speed timing (quadrature encoder) |

---

## Compile and Upload

### Step 1: Set Target Controller

Edit `main.cpp` line 26:

```cpp
// Uncomment ONE to select target controller
#define ACTOR
// #define SENSOR
// #define ENCODER
```

### Step 2: Connect Hardware

Connect ONLY the target microcontroller (one at a time).

### Step 3: Build and Upload

```bash
cd ../sl-micro-controllers  # Navigate to sl-micro-controllers directory
pio run --target upload
```

---

## Static Assertions

Add compile-time validation at the **top of the class body**, immediately after the opening brace:

```cpp
template <const uint8_t kPin, const bool kNormallyOff>
class NewModule final : public Module
{
        // Static assertions go HERE - at the top of class body
        static_assert(
            kPin != LED_BUILTIN,
            "The LED-connected pin is reserved for LED manipulation. Select a different pin."
        );

  public:
        // Constructor and methods follow...
};
```

For modules with multiple pins:

```cpp
class EncoderModule final : public Module
{
        // Validate all pins at class top
        static_assert(kPinA != kPinB, "EncoderModule PinA and PinB cannot be the same!");
        static_assert(kPinA != LED_BUILTIN, "Select a different Channel A pin.");
        static_assert(kPinB != LED_BUILTIN, "Select a different Channel B pin.");

  public:
        // ...
};
```

---

## Complete Module Example

```cpp
#pragma once

#include "module.h"

template <const uint8_t kPin, const bool kNormallyOff, const bool kStartOff = true>
class DigitalOutputModule final : public Module
{
        // Static assertions at TOP of class body
        static_assert(
            kPin != LED_BUILTIN,
            "The LED-connected pin is reserved for LED manipulation. Select a different pin."
        );

  public:
    explicit DigitalOutputModule(
        const uint8_t module_type,
        const uint8_t module_id,
        Communication& communication
    ) : Module(module_type, module_id, communication) {}

    bool SetupModule() override
    {
        pinModeFast(kPin, OUTPUT);

        if (kStartOff)
        {
            digitalWriteFast(kPin, kDeactivate);
            SendData(static_cast<uint8_t>(kCustomStatusCodes::kOff));
        }
        else
        {
            digitalWriteFast(kPin, kActivate);
            SendData(static_cast<uint8_t>(kCustomStatusCodes::kOn));
        }

        _custom_parameters.pulse_duration = 100000;

        return true;
    }

    bool SetCustomParameters() override
    {
        return _communication.ExtractModuleParameters(_custom_parameters);
    }

    bool RunActiveCommand() override
    {
        switch (static_cast<kModuleCommands>(GetActiveCommand()))
        {
            case kModuleCommands::kPulse: Pulse(); return true;
            case kModuleCommands::kOn:    TurnOn(); return true;
            case kModuleCommands::kOff:   TurnOff(); return true;
            default: return false;
        }
    }

  private:
    enum class kModuleCommands : uint8_t
    {
        kPulse = 1,
        kOn    = 2,
        kOff   = 3,
    };

    enum class kCustomStatusCodes : uint8_t
    {
        kOn  = 51,
        kOff = 52,
    };

    struct CustomRuntimeParameters
    {
        uint32_t pulse_duration = 100000;
    } PACKED_STRUCT _custom_parameters;

    static constexpr bool kActivate = kNormallyOff ? HIGH : LOW;
    static constexpr bool kDeactivate = kNormallyOff ? LOW : HIGH;

    void TurnOn()
    {
        digitalWriteFast(kPin, kActivate);
        SendData(static_cast<uint8_t>(kCustomStatusCodes::kOn));
        CompleteCommand();
    }

    void TurnOff()
    {
        digitalWriteFast(kPin, kDeactivate);
        SendData(static_cast<uint8_t>(kCustomStatusCodes::kOff));
        CompleteCommand();
    }

    void Pulse()
    {
        switch (execution_parameters.stage)
        {
            case 1:
                digitalWriteFast(kPin, kActivate);
                SendData(static_cast<uint8_t>(kCustomStatusCodes::kOn));
                AdvanceCommandStage();
                return;

            case 2:
                if (!WaitForMicros(_custom_parameters.pulse_duration)) return;
                AdvanceCommandStage();
                return;

            case 3:
                digitalWriteFast(kPin, kDeactivate);
                SendData(static_cast<uint8_t>(kCustomStatusCodes::kOff));
                CompleteCommand();
                return;

            default: AbortCommand();
        }
    }
};
```

---

## Firmware Verification Checklist

```
- [ ] Module header file created with correct includes
- [ ] Template parameters use `const` keyword
- [ ] kModuleCommands enum defines commands (values >= 1)
- [ ] kCustomStatusCodes enum defines statuses (values >= 51)
- [ ] CustomRuntimeParameters struct uses PACKED_STRUCT macro
- [ ] All struct fields have default values
- [ ] SetupModule() uses pinModeFast/digitalWriteFast
- [ ] SetupModule() calls SendData() for initial status
- [ ] SetupModule() resets _custom_parameters to defaults
- [ ] SetCustomParameters() calls _communication.ExtractModuleParameters(_custom_parameters)
- [ ] RunActiveCommand() casts GetActiveCommand() to kModuleCommands
- [ ] RunActiveCommand() returns true for recognized, false for unrecognized
- [ ] Command handlers call CompleteCommand() when done
- [ ] Multi-stage commands use execution_parameters.stage (starts at 1)
- [ ] Multi-stage commands call AdvanceCommandStage() then return
- [ ] Static assertions at TOP of class body (after opening brace, before public:)
- [ ] Module registered in main.cpp for correct controller
- [ ] Firmware compiles without warnings
```
