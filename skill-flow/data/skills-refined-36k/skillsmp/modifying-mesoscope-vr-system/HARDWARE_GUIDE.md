# Adding Hardware to Mesoscope-VR

This guide covers adding physical hardware components to the Mesoscope-VR acquisition system. All hardware must fit
into one of the three supported categories.

---

## Supported Hardware Categories

Mesoscope-VR supports exactly three hardware categories. New hardware must be added to one of these:

| Category          | Configuration Class          | Use For                                        |
|-------------------|------------------------------|------------------------------------------------|
| Cameras           | `MesoscopeCameras`           | Video acquisition devices                      |
| Microcontrollers  | `MesoscopeMicroControllers`  | Sensors, actuators, digital I/O via Teensy     |
| External Assets   | `MesoscopeExternalAssets`    | Zaber motors, network services, other devices  |

Each category can have one or more binding classes in sl-experiment. For example, `MesoscopeExternalAssets` currently
provides configuration for `ZaberMotors`, but additional binding classes can be added as needed.

**New hardware categories are NOT supported.** All hardware must fit into one of these existing categories.

---

## Hardware Type Decision Tree

```
New hardware component
├── Camera (video acquisition)
│   ├── Add configuration fields to MesoscopeCameras
│   ├── Use /camera-interface skill for API details
│   └── Integrate via VideoSystems binding class
│
├── Microcontroller-based (sensors, actuators)
│   ├── Add configuration fields to MesoscopeMicroControllers
│   ├── Use /microcontroller-interface skill for firmware
│   └── Integrate via MicroControllerInterfaces binding class
│
└── External device (Zaber motors, network services, other)
    ├── Add configuration fields to MesoscopeExternalAssets
    └── Integrate via existing binding class, new binding class, or directly in data_acquisition.py
```

---

## Pre-Implementation Verification

**Before writing any hardware code, verify the hardware is connected and accessible using MCP tools.**

Each hardware category has associated MCP tools for discovery and verification. Use these to confirm hardware presence
and identify configuration values (camera indices, serial ports, etc.).

### MCP Servers Required

| Hardware Type     | MCP Server                  | Start Command      |
|-------------------|-----------------------------|--------------------|
| Cameras           | ataraxis-video-system       | `axvs mcp`         |
| Microcontrollers  | ataraxis-comm-interface     | `axci-mcp`         |
| Zaber motors      | sl-experiment               | `sl-get mcp`       |

### Verification Tools by Hardware Type

| Hardware Type     | MCP Tool                        | Purpose                                    |
|-------------------|---------------------------------|--------------------------------------------|
| Cameras           | `list_cameras()`                | Discover cameras and their indices         |
| Cameras           | `check_runtime_requirements()`  | Verify FFMPEG and GPU availability         |
| Cameras           | `get_cti_status()`              | Check GenTL Producer configuration         |
| Microcontrollers  | `list_microcontrollers()`       | Discover controllers and their ports       |
| Microcontrollers  | `check_mqtt_broker()`           | Verify MQTT broker is running              |
| Zaber motors      | `get_zaber_devices_tool()`      | Discover motors and their ports            |

### Pre-Implementation Checklist

Before modifying code for new hardware:

```
- [ ] Started appropriate MCP server for the hardware type
- [ ] Ran discovery tool and confirmed hardware is detected
- [ ] Recorded hardware identifiers (camera index, serial port, device ID)
- [ ] Verified any dependencies (FFMPEG, CTI file, MQTT broker)
```

If hardware is not detected:
- Check physical connections and power
- Verify drivers are installed
- Check port permissions (`sudo usermod -a -G dialout $USER` for serial devices)
- For cameras, ensure CTI file is configured (`set_cti_file()`)

---

## Modification Workflow

Adding new hardware to mesoscope-vr requires changes in both repositories:

```
Phase 0: Pre-Implementation Verification
└── 0.1 Use MCP tools to verify hardware is connected and accessible

Phase 1: sl-shared-assets (Configuration)
├── 1.1 Add fields to existing configuration dataclass
├── 1.2 Export (if adding new classes for complex types)
└── 1.3 Bump version

Phase 2: sl-experiment (Implementation)
├── 2.1 Extend existing binding class
├── 2.2 Integrate into data_acquisition.py lifecycle
├── 2.3 Update CLI commands (if needed)
└── 2.4 Update pyproject.toml dependency

Phase 3: Post-Implementation Verification
└── 3.1 Use MCP tools to verify hardware works with new configuration
```

---

## Adding Cameras

### Phase 1: Configuration (sl-shared-assets)

**File:** `sl-shared-assets/src/sl_shared_assets/configuration/mesoscope_configuration.py`

Add fields to `MesoscopeCameras`:

```python
@dataclass()
class MesoscopeCameras:
    """Stores the video camera configuration of the Mesoscope-VR data acquisition system."""

    # Existing cameras
    face_camera_index: int = 0
    """The index of the face camera in the list of all available Harvester-managed cameras."""

    face_camera_quantization: int = 20
    """The quantization parameter used by the face camera to encode acquired frames."""

    face_camera_preset: int = 7
    """The encoding speed preset used by the face camera."""

    body_camera_index: int = 1
    """The index of the body camera in the list of all available Harvester-managed cameras."""

    body_camera_quantization: int = 20
    """The quantization parameter used by the body camera to encode acquired frames."""

    body_camera_preset: int = 7
    """The encoding speed preset used by the body camera."""

    # ADD NEW CAMERA FIELDS HERE
    new_camera_index: int = 2
    """The index of the new camera in the list of all available Harvester-managed cameras."""

    new_camera_quantization: int = 20
    """The quantization parameter used by the new camera to encode acquired frames."""

    new_camera_preset: int = 7
    """The encoding speed preset used by the new camera."""
```

### Phase 2: Implementation (sl-experiment)

**File:** `sl-experiment/src/sl_experiment/mesoscope_vr/binding_classes.py`

Extend the `VideoSystems` class:

```python
class VideoSystems:
    """Interfaces with the Ataraxis Video System devices used in Mesoscope-VR."""

    def __init__(
        self,
        data_logger: DataLogger,
        camera_configuration: MesoscopeCameras,
        output_directory: Path,
    ) -> None:
        # Existing cameras...
        self._face_camera_started: bool = False
        self._body_camera_started: bool = False

        # ADD NEW CAMERA
        self._new_camera_started: bool = False
        self._new_camera: VideoSystem = VideoSystem(
            system_id=np.uint8(73),  # Allocate new ID in 50-99 range
            data_logger=data_logger,
            output_directory=output_directory,
            camera_index=camera_configuration.new_camera_index,
            camera_interface=CameraInterfaces.HARVESTERS,
            display_frame_rate=25,
            video_encoder=VideoEncoders.H265,
            gpu=0,
            encoder_speed_preset=EncoderSpeedPresets(camera_configuration.new_camera_preset),
            output_pixel_format=OutputPixelFormats.YUV420,
            quantization_parameter=camera_configuration.new_camera_quantization,
        )

    # Add lifecycle methods for new camera
    def start_new_camera(self) -> None:
        """Starts acquiring frames from the new camera."""
        if self._new_camera_started:
            return
        self._new_camera.start()
        self._new_camera_started = True

    def save_new_camera_frames(self) -> None:
        """Starts saving frames from the new camera to disk."""
        self._new_camera.start_frame_saving()

    def stop(self) -> None:
        """Stops all cameras."""
        # ... existing camera stop logic ...

        # ADD NEW CAMERA STOP
        if self._new_camera_started:
            self._new_camera.stop_frame_saving()
        self._new_camera.stop()
        self._new_camera_started = False
```

For detailed camera API usage, see the `/camera-interface` skill.

---

## Adding Microcontroller Hardware

For hardware controlled by Teensy microcontrollers (sensors, actuators, digital I/O), use the
`/microcontroller-interface` skill for the low-level firmware and PC interface implementation. This section covers the
mesoscope-vr specific integration steps.

Microcontroller modules can be added in two ways:

1. **Add to existing controller** (common case) - Add the module to ACTOR, SENSOR, or ENCODER
2. **Add new controller** (rare case) - Create an entirely new microcontroller

### When to Add a New Controller

Adding a new microcontroller is only necessary when:

- **Communication saturation**: Existing controllers cannot handle additional data throughput
- **Hardware interrupt requirements**: The module requires dedicated hardware interrupts that conflict with existing
  modules (e.g., quadrature encoders require dedicated interrupt pins for accurate pulse counting)
- **Timing isolation**: The module requires precise timing that would be disrupted by other modules on the same
  controller

For most new hardware, adding to an existing controller is sufficient.

---

### Option A: Adding Module to Existing Controller

This is the common case for most new microcontroller hardware.

#### Phase 1: Configuration (sl-shared-assets)

**File:** `sl-shared-assets/src/sl_shared_assets/configuration/mesoscope_configuration.py`

Add fields to `MesoscopeMicroControllers`:

```python
@dataclass()
class MesoscopeMicroControllers:
    """Configuration for microcontroller-managed hardware."""

    # Existing controller ports...
    actor_port: str = "/dev/ttyACM0"
    sensor_port: str = "/dev/ttyACM1"
    encoder_port: str = "/dev/ttyACM2"

    # Existing module parameters...
    lick_threshold_adc: int = 100

    # ADD NEW MODULE CONFIGURATION FIELDS
    new_module_parameter_a: int = 1000
    """Description of parameter A for the new module."""

    new_module_parameter_b: float = 2.5
    """Description of parameter B for the new module."""
```

#### Phase 2: Implementation (sl-experiment)

After implementing the firmware module and PC interface class using `/microcontroller-interface` (the interface class
is created in `shared_components/module_interfaces.py`):

```
Integration Steps:
├── 2.1 Import interface class from shared_components into binding_classes.py
├── 2.2 Instantiate interface in MicroControllerInterfaces.__init__
├── 2.3 Add to appropriate controller's module_interfaces tuple
├── 2.4 Call initialize_local_assets() in MicroControllerInterfaces.start()
├── 2.5 Configure parameters in MicroControllerInterfaces.start()
└── 2.6 Use interface in data_acquisition.py runtime
```

**File:** `sl-experiment/src/sl_experiment/mesoscope_vr/binding_classes.py`

```python
from sl_experiment.shared_components import (
    # Existing imports...
    BrakeInterface,
    ValveInterface,
    NewModuleInterface,  # ADD IMPORT
)

class MicroControllerInterfaces:
    """Manages microcontroller communication for Mesoscope-VR."""

    def __init__(
        self,
        data_logger: DataLogger,
        config: MesoscopeMicroControllers,
    ) -> None:
        # Existing interfaces...
        self.brake = BrakeInterface(...)
        self.valve = ValveInterface(...)

        # ADD NEW INTERFACE
        self.new_module = NewModuleInterface(
            parameter_a=config.new_module_parameter_a,
            parameter_b=config.new_module_parameter_b,
        )

        # Add to appropriate controller's module_interfaces tuple
        self._actor: MicroControllerInterface = MicroControllerInterface(
            controller_id=np.uint8(101),
            data_logger=data_logger,
            module_interfaces=(
                self.brake,
                self.valve,
                self.gas_puff_valve,
                self.screens,
                self.new_module,  # ADD TO TUPLE
            ),
            buffer_size=8192,
            port=config.actor_port,
            baudrate=115200,
        )

    def start(self) -> None:
        """Starts all microcontroller communication."""
        self._actor.start()
        self._sensor.start()
        self._encoder.start()

        # Initialize local assets for interfaces that need them
        self.wheel_encoder.initialize_local_assets()
        self.valve.initialize_local_assets()
        self.new_module.initialize_local_assets()  # ADD THIS

        # Configure module parameters
        self.new_module.set_parameters(
            parameter_a=np.uint32(...),
            parameter_b=np.float32(...),
        )
```

#### Controller Assignment

Assign modules to the appropriate existing controller based on function:

| Controller | ID  | Use For                                     | Modules Tuple Location            |
|------------|-----|---------------------------------------------|-----------------------------------|
| ACTOR      | 101 | Output control (valves, brakes, LEDs)       | `self._actor` module_interfaces   |
| SENSOR     | 152 | Input monitoring (lick, torque, TTL)        | `self._sensor` module_interfaces  |
| ENCODER    | 203 | High-speed timing (quadrature encoders)     | `self._encoder` module_interfaces |

---

### Option B: Adding a New Controller

Use this approach only when existing controllers cannot accommodate the new module due to communication saturation,
hardware interrupt conflicts, or timing isolation requirements.

#### Phase 1: Configuration (sl-shared-assets)

**File:** `sl-shared-assets/src/sl_shared_assets/configuration/mesoscope_configuration.py`

Add the new controller port and module parameters:

```python
@dataclass()
class MesoscopeMicroControllers:
    """Configuration for microcontroller-managed hardware."""

    # Existing controller ports...
    actor_port: str = "/dev/ttyACM0"
    sensor_port: str = "/dev/ttyACM1"
    encoder_port: str = "/dev/ttyACM2"

    # ADD NEW CONTROLLER PORT
    new_controller_port: str = "/dev/ttyACM3"
    """Serial port for the new controller managing [description of function]."""

    # ADD NEW MODULE CONFIGURATION FIELDS
    new_module_parameter_a: int = 1000
    """Description of parameter A for the new module."""

    new_module_parameter_b: float = 2.5
    """Description of parameter B for the new module."""
```

#### Phase 2: Implementation (sl-experiment)

**File:** `sl-experiment/src/sl_experiment/mesoscope_vr/binding_classes.py`

Add the new controller to `MicroControllerInterfaces`:

```python
class MicroControllerInterfaces:
    """Manages microcontroller communication for Mesoscope-VR."""

    def __init__(
        self,
        data_logger: DataLogger,
        config: MesoscopeMicroControllers,
    ) -> None:
        # Existing controllers and interfaces...
        self._actor: MicroControllerInterface = MicroControllerInterface(...)
        self._sensor: MicroControllerInterface = MicroControllerInterface(...)
        self._encoder: MicroControllerInterface = MicroControllerInterface(...)

        # ADD NEW INTERFACE
        self.new_module = NewModuleInterface(
            parameter_a=config.new_module_parameter_a,
            parameter_b=config.new_module_parameter_b,
        )

        # ADD NEW CONTROLLER
        self._new_controller: MicroControllerInterface = MicroControllerInterface(
            controller_id=np.uint8(204),  # Allocate new ID in 100-199 range
            data_logger=data_logger,
            module_interfaces=(
                self.new_module,  # Module(s) for this controller
            ),
            buffer_size=8192,
            port=config.new_controller_port,
            baudrate=115200,
        )

    def start(self) -> None:
        """Starts all microcontroller communication."""
        self._actor.start()
        self._sensor.start()
        self._encoder.start()
        self._new_controller.start()  # ADD THIS

        # Initialize local assets
        self.wheel_encoder.initialize_local_assets()
        self.valve.initialize_local_assets()
        self.new_module.initialize_local_assets()  # ADD THIS

    def stop(self) -> None:
        """Stops all microcontroller communication."""
        self._actor.stop()
        self._sensor.stop()
        self._encoder.stop()
        self._new_controller.stop()  # ADD THIS
```

---

### Using the Module in Runtime

**File:** `sl-experiment/src/sl_experiment/mesoscope_vr/data_acquisition.py`

```python
# Enable monitoring (for sensor modules)
self._microcontrollers.new_module.start_monitoring()

# Trigger commands
self._microcontrollers.new_module.execute_action()

# Read state
if self._microcontrollers.new_module.is_active:
    value = self._microcontrollers.new_module.current_value

# Disable monitoring
self._microcontrollers.new_module.stop_monitoring()
```

---

## Adding External Assets

External assets include Zaber motors and network services like Google Sheets integration.

For Zaber motor hardware, use the `/zaber-interface` skill for the low-level API documentation including:
- ZaberConnection/ZaberDevice/ZaberAxis class hierarchy
- Motor discovery and configuration validation
- Position management (park, mount, maintenance)
- Safety patterns (park/unpark workflow)

This section covers the mesoscope-vr specific integration steps.

### Phase 1: Configuration (sl-shared-assets)

**File:** `sl-shared-assets/src/sl_shared_assets/configuration/mesoscope_configuration.py`

Add fields to `MesoscopeExternalAssets`:

```python
@dataclass()
class MesoscopeExternalAssets:
    """Configuration for external assets (motors, network services)."""

    # Existing fields...
    headbar_port: str = "/dev/ttyUSB0"
    wheel_port: str = "/dev/ttyUSB1"
    lickport_port: str = "/dev/ttyUSB2"
    spreadsheet_id: str = ""
    sheet_name: str = "Sheet1"

    # ADD NEW EXTERNAL ASSET FIELDS
    new_motor_port: str = "/dev/ttyUSB3"
    """Serial port for the new Zaber motor."""

    new_motor_speed: float = 10.0
    """Default movement speed for the new motor in mm/s."""
```

### Phase 2: Implementation (sl-experiment)

External assets have flexible binding options:

- **Zaber motors**: Extend the existing `ZaberMotors` class in `binding_classes.py`
- **New device type**: Create a new binding class in `binding_classes.py`
- **Simple integration**: Add directly in `data_acquisition.py` without a dedicated binding class

**For Zaber motors**, follow the patterns documented in `/zaber-interface`:

1. Add a new `ZaberConnection` for the motor group in `ZaberMotors.__init__`
2. Connect and extract `ZaberAxis` instances for each motor
3. Add position methods following the existing pattern (unpark → move → wait → park)
4. Update `wait_until_idle()` to include new motor axes
5. Update `disconnect()` to close the new connection
6. Update `ZaberPositions` dataclass in sl-shared-assets if position restoration is needed

---

## Existing Configuration Reference

### MesoscopeCameras

| Field                       | Type  | Default | Description                            |
|-----------------------------|-------|---------|----------------------------------------|
| `face_camera_index`         | `int` | `0`     | Face camera index from discovery       |
| `face_camera_quantization`  | `int` | `20`    | Face camera encoding quality (0-51)    |
| `face_camera_preset`        | `int` | `7`     | Face camera encoding speed preset      |
| `body_camera_index`         | `int` | `1`     | Body camera index from discovery       |
| `body_camera_quantization`  | `int` | `20`    | Body camera encoding quality (0-51)    |
| `body_camera_preset`        | `int` | `7`     | Body camera encoding speed preset      |

### MesoscopeMicroControllers

| Field                                  | Type    | Description                               |
|----------------------------------------|---------|-------------------------------------------|
| `actor_port`                           | `str`   | Actor AMC serial port                     |
| `sensor_port`                          | `str`   | Sensor AMC serial port                    |
| `encoder_port`                         | `str`   | Encoder AMC serial port                   |
| `lick_threshold_adc`                   | `int`   | Lick detection threshold (ADC units)      |
| `valve_calibration_data`               | `tuple` | Water valve calibration curve points      |
| `minimum_brake_strength_g_cm`          | `int`   | Minimum brake torque (g*cm)               |
| `maximum_brake_strength_g_cm`          | `int`   | Maximum brake torque (g*cm)               |
| `wheel_encoder_ppr`                    | `int`   | Wheel encoder pulses per revolution       |
| `wheel_diameter_cm`                    | `float` | Running wheel diameter (cm)               |

### MesoscopeExternalAssets

| Field            | Type  | Description                            |
|------------------|-------|----------------------------------------|
| `headbar_port`   | `str` | Headbar Zaber motor group serial port  |
| `wheel_port`     | `str` | Wheel Zaber motor serial port          |
| `lickport_port`  | `str` | Lickport Zaber motor group serial port |
| `spreadsheet_id` | `str` | Google Sheets document ID              |
| `sheet_name`     | `str` | Target worksheet name                  |

---

## System ID Allocation

Current mesoscope-vr allocations:

| ID    | Component              | Purpose                    |
|-------|------------------------|----------------------------|
| 51    | Face camera            | Frame timestamp logging    |
| 62    | Body camera            | Frame timestamp logging    |
| 101   | Actor AMC              | Microcontroller events     |
| 152   | Sensor AMC             | Microcontroller events     |
| 203   | Encoder AMC            | Microcontroller events     |

**Available ID ranges:**
- 50-99: Cameras (next available: 73)
- 100-199: Microcontrollers
- 200-255: Other hardware

---

## Module Type Codes

Current allocations in mesoscope-vr (must not reuse):

| Type Code | Module           | Controller |
|-----------|------------------|------------|
| 1         | TTLModule        | SENSOR     |
| 2         | EncoderModule    | ENCODER    |
| 3         | BrakeModule      | ACTOR      |
| 4         | LickModule       | SENSOR     |
| 5         | ValveModule      | ACTOR      |
| 6         | TorqueModule     | SENSOR     |
| 7         | ScreenModule     | ACTOR      |

**Next available type code:** 8

---

## Verification Checklist

### Camera Hardware

```
Pre-Implementation (MCP verification via axvs mcp):
- [ ] Ran list_cameras() and confirmed new camera is detected
- [ ] Recorded camera index from discovery output
- [ ] Ran check_runtime_requirements() to verify FFMPEG/GPU
- [ ] Verified CTI file is configured (for Harvesters cameras)

Implementation:
- [ ] Added fields to MesoscopeCameras (index, quantization, preset)
- [ ] Each field has docstring explaining its purpose
- [ ] Bumped sl-shared-assets version
- [ ] Extended VideoSystems class with new camera
- [ ] Added start/stop/save methods for new camera
- [ ] Allocated unique system ID (50-99 range)
- [ ] Integrated into data_acquisition.py lifecycle
- [ ] Updated pyproject.toml dependency version
- [ ] MyPy strict passes

Post-Implementation:
- [ ] Tested camera with MCP start_video_session() tool
- [ ] Verified frames are acquired and displayed correctly
```

### Microcontroller Hardware (Adding to Existing Controller)

```
Pre-Implementation (MCP verification via axci-mcp):
- [ ] Ran list_microcontrollers() and confirmed target controller is detected
- [ ] Recorded controller port from discovery output
- [ ] Verified controller ID matches expected (ACTOR=101, SENSOR=152, ENCODER=203)

Implementation:
- [ ] Firmware module implemented (see /microcontroller-interface skill)
- [ ] PC interface implemented (see /microcontroller-interface skill)
- [ ] Module parameter fields added to MesoscopeMicroControllers
- [ ] Bumped sl-shared-assets version
- [ ] Interface instantiated in MicroControllerInterfaces.__init__
- [ ] Interface added to correct controller's module_interfaces tuple
- [ ] initialize_local_assets() called in MicroControllerInterfaces.start()
- [ ] Parameters configured in MicroControllerInterfaces.start()
- [ ] Interface used in data_acquisition.py runtime
- [ ] Updated pyproject.toml dependency version
- [ ] MyPy strict passes

Post-Implementation:
- [ ] Ran list_microcontrollers() to verify controller still responds
- [ ] Tested module commands through binding class
```

### Microcontroller Hardware (Adding New Controller)

Use only when existing controllers cannot accommodate the module (communication saturation, hardware interrupt
conflicts, or timing isolation requirements).

```
Pre-Implementation (MCP verification via axci-mcp):
- [ ] Ran list_microcontrollers() and confirmed new controller is detected
- [ ] Recorded new controller port from discovery output
- [ ] Verified new controller has unique ID (not 101, 152, or 203)

Implementation:
- [ ] Firmware module implemented (see /microcontroller-interface skill)
- [ ] PC interface implemented (see /microcontroller-interface skill)
- [ ] New controller port field added to MesoscopeMicroControllers
- [ ] Module parameter fields added to MesoscopeMicroControllers
- [ ] Bumped sl-shared-assets version
- [ ] Interface instantiated in MicroControllerInterfaces.__init__
- [ ] New MicroControllerInterface created with unique ID (100-199 range)
- [ ] Interface added to new controller's module_interfaces tuple
- [ ] New controller started in MicroControllerInterfaces.start()
- [ ] New controller stopped in MicroControllerInterfaces.stop()
- [ ] initialize_local_assets() called in MicroControllerInterfaces.start()
- [ ] Parameters configured in MicroControllerInterfaces.start()
- [ ] Interface used in data_acquisition.py runtime
- [ ] Updated pyproject.toml dependency version
- [ ] MyPy strict passes

Post-Implementation:
- [ ] Ran list_microcontrollers() to verify all controllers respond
- [ ] Tested module commands through binding class
```

### External Asset Hardware

```
Pre-Implementation (MCP verification via sl-get mcp for Zaber motors):
- [ ] Ran get_zaber_devices_tool() and confirmed device is detected (if Zaber)
- [ ] Recorded device port from discovery output
- [ ] Verified device axes and capabilities match requirements

Implementation:
- [ ] Added fields to MesoscopeExternalAssets
- [ ] Each field has docstring explaining its purpose
- [ ] Bumped sl-shared-assets version
- [ ] Implemented binding (one of the following):
      - [ ] Extended existing ZaberMotors class (for Zaber motors)
      - [ ] Created new binding class in binding_classes.py (for new device types)
      - [ ] Added direct integration in data_acquisition.py (for simple cases)
- [ ] Updated pyproject.toml dependency version
- [ ] MyPy strict passes

Post-Implementation:
- [ ] Ran get_zaber_devices_tool() to verify device still responds (if Zaber)
- [ ] Tested device commands through binding class
```
