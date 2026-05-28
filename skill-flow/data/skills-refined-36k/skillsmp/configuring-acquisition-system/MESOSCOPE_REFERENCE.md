# Mesoscope System Configuration Reference

Detailed documentation of all configuration parameters for the `mesoscope` (Two-photon Random Access Mesoscope with
Virtual Reality) acquisition system, based on actual usage in the sl-experiment codebase.

---

## Filesystem Configuration

Directory paths for data storage and network mounts. These paths must be configured before runtime as they have no
meaningful defaults.

### root_directory

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| Type           | `str` (path)                                       |
| Default        | `""` (empty - must be configured)                  |
| Used by        | `MesoscopeData` class in sl-experiment             |
| Discovery tool | None (user-provided)                               |

**What it controls:**
- Root storage location for all project data on the VRPC (Virtual Reality PC)
- Base path for session-specific data aggregation before transfer to server
- Used to construct persistent data paths: `{root_directory}/{project}/{animal}/persistent_data`

**Constraints:**
- Must be a valid, writable filesystem path
- Directory is auto-created if it does not exist

---

### server_directory

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| Type           | `str` (path)                                       |
| Default        | `""` (empty - must be configured)                  |
| Used by        | `_push_data()` in data_preprocessing module        |
| Discovery tool | None (user-provided)                               |

**What it controls:**
- SMB mount point to the Cornell BioHPC server's shared directory
- Final destination for long-term hot storage of processed session data
- Uses same directory structure as root_directory: `{server_directory}/{project}/{animal}/{session}`

**Constraints:**
- Must be an SMB-mounted network path accessible from VRPC
- Requires network connectivity and valid server credentials
- Example: `/mnt/sun_lab_server/sun_data`

---

### nas_directory

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| Type           | `str` (path)                                       |
| Default        | `""` (empty - must be configured)                  |
| Used by        | `_push_data()` in data_preprocessing module        |
| Discovery tool | None (user-provided)                               |

**What it controls:**
- SMB mount point to Synology NAS backup storage
- Final destination for cold/archival storage of session data
- Provides redundant backup alongside server storage
- Data is transferred in parallel to both NAS and server

**Constraints:**
- Must be an SMB-mounted network path to Synology NAS
- Should have substantial storage capacity for archival
- Example: `/mnt/synology_nas/sun_data`

---

### mesoscope_directory

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| Type           | `str` (path)                                       |
| Default        | `""` (empty - must be configured)                  |
| Used by        | `_ScanImagePCData` class in sl-experiment          |
| Discovery tool | None (user-provided)                               |

**What it controls:**
- Root directory where ScanImagePC (MATLAB) saves raw mesoscope frame stacks (.TIFF files)
- Shared directory that aggregates all mesoscope acquisition data during runtime
- Each session's data is initially saved here, then moved to session-specific subdirectory

**Constraints:**
- Must be accessible to both VRPC and ScanImagePC (typically network shared mount)
- Requires sufficient temporary storage during acquisition (hundreds of GB per session)
- Often a dedicated fast SSD or RAID for mesoscope data
- Example: `/mnt/mesoscope_drive/meso_data`

---

## Google Sheets Configuration

Google Sheet identifiers for lab records. Used during data preprocessing (post-session), not during acquisition.

### surgery_sheet_id

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| Type           | `str`                                              |
| Default        | `""` (empty - must be configured)                  |
| Used by        | `_preprocess_google_sheet_data()` via `SurgeryLog` |
| Discovery tool | None (user-provided)                               |

**What it controls:**
- Google Sheets ID for the surgery log containing surgical intervention records
- Used to fetch and cache animal-specific surgery metadata during preprocessing
- Enables tracking of surgical quality and implant dates
- For window-checking sessions, updates surgery quality (0-3 scale)

**Constraints:**
- Must be a valid Google Sheets ID accessible with provided credentials
- Sheet must contain columns: animal_id, surgery_date, quality, etc.
- Requires valid Google service account credentials file

---

### water_log_sheet_id

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| Type           | `str`                                              |
| Default        | `""` (empty - must be configured)                  |
| Used by        | `_preprocess_google_sheet_data()` via `WaterLog`   |
| Discovery tool | None (user-provided)                               |

**What it controls:**
- Google Sheets ID for the water restriction log
- Records daily water intake for each animal during training sessions
- Critical for animal welfare tracking and experimental compliance
- Automatically updated post-session during preprocessing

**Constraints:**
- Must be a valid Google Sheets ID
- Sheet must have session date, animal_id, and water volume columns
- Only used for non-window-checking sessions

---

## Cameras Configuration

Video camera indices and H.265 encoding parameters. Cameras are managed via the Harvester GenICam interface.

### face_camera_index

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| Type           | `int`                                              |
| Default        | `0`                                                |
| Valid range    | 0 to N (number of connected cameras - 1)           |
| Used by        | `VideoSystems` class via `VideoSystem` constructor |
| Discovery tool | `list_cameras()` from ataraxis-video-system        |

**What it controls:**
- Index of the face camera in the Harvester camera interface list
- Determines which of multiple available GeniCam cameras captures eye/face video
- Harvester enumerates all connected cameras with sequential indices

**Constraints:**
- 0-based index corresponding to order in Harvester camera list
- Must match actual camera hardware availability
- Index order depends on USB connection order and system boot sequence
- Must be different from body_camera_index

---

### body_camera_index

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| Type           | `int`                                              |
| Default        | `1`                                                |
| Valid range    | 0 to N (number of connected cameras - 1)           |
| Used by        | `VideoSystems` class via `VideoSystem` constructor |
| Discovery tool | `list_cameras()` from ataraxis-video-system        |

**What it controls:**
- Index of the body camera in the Harvester camera interface
- Captures full-body behavior video during acquisition

**Constraints:**
- Must be different from face_camera_index
- Verify camera order after any hardware changes or reboots

---

### face_camera_quantization

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| Type           | `int`                                              |
| Default        | `20`                                               |
| Valid range    | 0-51 (H.265 quantization parameter scale)          |
| Used by        | `VideoSystem` via ataraxis-video-system            |
| Discovery tool | None (user preference)                             |

**What it controls:**
- H.265 video encoding quantization parameter for face camera
- Controls compression quality/file size tradeoff
- Lower values = better quality but larger files

**Guidelines:**
- 0-20: High quality, large files (~2-3 GB/hour at 1080p 25fps)
- 20-30: Good balance for research-grade video
- 30-51: Lower quality, smaller files

---

### face_camera_preset

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| Type           | `int`                                              |
| Default        | `7`                                                |
| Valid range    | 0-9 (H.265 speed preset values)                    |
| Used by        | `VideoSystem` via `EncoderSpeedPresets` enum       |
| Discovery tool | None (user preference)                             |

**What it controls:**
- H.265 encoding speed preset for face camera
- Affects computational cost vs. encoding efficiency tradeoff

**Guidelines:**
- 0-3: Faster encoding, lower compression (for real-time constraints)
- 4-6: Balanced performance
- 7-9: Slower encoding, higher compression (better quality at same bitrate)

---

### body_camera_quantization / body_camera_preset

Same as face camera settings. Default values: quantization=20, preset=7.

---

## Microcontroller Configuration

USB ports and hardware calibration parameters for the three microcontroller boards (Actor, Sensor, Encoder).

### USB Port Assignments

| Parameter      | Default          | Controller Function                               |
|----------------|------------------|---------------------------------------------------|
| `actor_port`   | `/dev/ttyACM0`   | Controls outputs: valve, brake, gas puff, screens |
| `sensor_port`  | `/dev/ttyACM1`   | Monitors inputs: lick, torque, mesoscope TTL      |
| `encoder_port` | `/dev/ttyACM2`   | High-precision wheel encoder with HW interrupts   |

**Discovery tool:** `list_microcontrollers()` from ataraxis-communication-interface

**Constraints:**
- Valid Linux device paths: `/dev/ttyACM0`, `/dev/ttyACM1`, `/dev/ttyACM2`, etc.
- Must be unique for each controller
- USB enumeration order can change after system restart if cables are replugged

---

### keepalive_interval_ms

| Property       | Value                                              |
|----------------|----------------------------------------------------|
| Type           | `int`                                              |
| Default        | `500`                                              |
| Valid range    | 100-5000 ms                                        |
| Used by        | All `MicroControllerInterface` instances           |
| Discovery tool | None (user preference)                             |

**What it controls:**
- How frequently microcontrollers must send keepalive messages to confirm responsiveness
- VRPC closes connection if no keepalive received within timeout period

**Guidelines:**
- Too low (< 200ms): False disconnections, CPU overhead
- Too high (> 2000ms): Slow failure detection

---

### Brake Calibration

| Parameter                     | Type    | Default     |
|-------------------------------|---------|-------------|
| `minimum_brake_strength_g_cm` | `float` | `43.2047`   |
| `maximum_brake_strength_g_cm` | `float` | `1152.1246` |

**Discovery tool:** None (hardware-specific calibration required)

**What they control:**
- Calibration curve for electromagnetic particle brake on running wheel
- Maps voltage input to actual braking torque (gram-centimeters)
- Used to brake wheel when animal needs to stop in VR

**Used by:** `BrakeInterface` class

**Constraints:**
- Values are hardware-specific and must be calibrated for each brake unit
- Typical range: 40-1200 g·cm

---

### Wheel Configuration

| Parameter                             | Type    | Default   | Valid Range  |
|---------------------------------------|---------|-----------|--------------|
| `wheel_diameter_cm`                   | `float` | `15.0333` | 10-25 cm     |
| `wheel_encoder_ppr`                   | `int`   | `8192`    | 256-8192     |
| `wheel_encoder_report_cw`             | `bool`  | `false`   | true/false   |
| `wheel_encoder_report_ccw`            | `bool`  | `true`    | true/false   |
| `wheel_encoder_delta_threshold_pulse` | `int`   | `15`      | 0-255 pulses |
| `wheel_encoder_polling_delay_us`      | `int`   | `500`     | 100-10000 us |

**Discovery tool:** None (hardware-specific)

**What they control:**
- `wheel_diameter_cm`: Physical wheel diameter, converts encoder pulses to distance traveled
- `wheel_encoder_ppr`: Encoder resolution in Pulses Per Revolution
- `wheel_encoder_report_cw/ccw`: Which rotation directions to report (mouse wheels typically CCW only)
- `wheel_encoder_delta_threshold_pulse`: Minimum pulse change before reporting (filters noise)
- `wheel_encoder_polling_delay_us`: Time between encoder reads in microseconds

**Used by:** `EncoderInterface` class

---

### Lick Sensor Calibration

| Parameter                   | Type  | Default | Valid Range | Description                         |
|-----------------------------|-------|---------|-------------|-------------------------------------|
| `lick_threshold_adc`        | `int` | `600`   | 0-4095      | ADC threshold for tongue contact    |
| `lick_signal_threshold_adc` | `int` | `300`   | 0-4095      | Minimum ADC to report (noise floor) |
| `lick_delta_threshold_adc`  | `int` | `300`   | 0-4095      | Minimum change between readings     |
| `lick_averaging_pool_size`  | `int` | `2`     | 1-4         | Number of readings to average       |

**Discovery tool:** None (hardware-specific calibration)

**What they control:**
- Thresholds and filtering for capacitive lick sensor on water spout
- ADC range: 0-4095 (12-bit 3.3V ADC)
- Prevents false positives from electrical noise

**Used by:** `LickInterface` class

**Guidelines:**
- `lick_threshold_adc`: Higher = less sensitive, fewer false positives
- `lick_signal_threshold_adc`: Values below this are treated as zero
- `lick_averaging_pool_size`: Higher = smoother signal but slower response

---

### Torque Sensor Calibration

| Parameter                     | Type    | Default    | Valid Range | Description                      |
|-------------------------------|---------|------------|-------------|----------------------------------|
| `torque_baseline_voltage_adc` | `int`   | `2048`     | 0-4095      | ADC reading at zero torque       |
| `torque_maximum_voltage_adc`  | `int`   | `3443`     | 0-4095      | ADC reading at max torque        |
| `torque_sensor_capacity_g_cm` | `float` | `720.0779` | 500-1000    | Maximum measurable torque (g·cm) |
| `torque_report_cw`            | `bool`  | `true`     | true/false  | Report clockwise torque          |
| `torque_report_ccw`           | `bool`  | `true`     | true/false  | Report counter-clockwise torque  |
| `torque_signal_threshold_adc` | `int`   | `150`      | 0-4095      | Minimum ADC to report            |
| `torque_delta_threshold_adc`  | `int`   | `100`      | 0-4095      | Minimum change between readings  |
| `torque_averaging_pool_size`  | `int`   | `4`        | 2-8         | Number of readings to average    |

**Discovery tool:** None (hardware-specific calibration)

**What they control:**
- Calibration and filtering for wheel torque sensor
- Detects force exerted by animal on wheel
- Quadrature voltage from AD620 amplifier

**Used by:** `TorqueInterface` class

**Notes:**
- `torque_baseline_voltage_adc` should be ~2048 (mid-scale) for balanced sensor
- Values are hardware-specific and should be calibrated per sensor unit

---

### Valve Calibration

| Property       | Value                                                |
|----------------|------------------------------------------------------|
| Type           | Dict mapping `int` (time_us) to `float` (volume_ul)  |
| Default        | `{15000: 1.1, 30000: 3.0, 45000: 6.25, 60000: 10.9}` |
| Used by        | `ValveInterface` class                               |
| Discovery tool | None (hardware-specific calibration)                 |

**What it controls:**
- Water delivery solenoid valve calibration curve
- Maps valve open time (microseconds) to water volume delivered (microliters)
- Critical for precise reward delivery during training

**YAML Format:**
```yaml
valve_calibration_data:
          15000: 1.1
          30000: 3.0
          45000: 6.25
          60000: 10.9
```

Each entry: `open_time_microseconds: water_volume_microliters`

**Constraints:**
- Minimum 2 calibration points (for linear interpolation)
- Points should be sorted by time (increasing)
- Time range: typically 10000-60000 us
- Volume range: typically 0.5-15 uL

**Calibration procedure:**
1. Collect water dispensed at multiple valve open times
2. Weigh water to determine volume (1 mg = 1 uL)
3. Enter calibration points in YAML format

---

### Timing Configuration

| Parameter                             | Type    | Default | Valid Range | Description                         |
|---------------------------------------|---------|---------|-------------|-------------------------------------|
| `sensor_polling_delay_ms`             | `int`   | `1`     | 1-10 ms     | Time between sensor readouts        |
| `screen_trigger_pulse_duration_ms`    | `int`   | `500`   | 100-1000 ms | TTL pulse width for screen toggle   |
| `cm_per_unity_unit`                   | `float` | `10.0`  | 5-50 cm     | Real cm per Unity distance unit     |
| `mesoscope_frame_averaging_pool_size` | `int`   | `0`     | 0-4         | TTL signal averaging for frame sync |

**Discovery tool:** None (user preference / VR configuration)

**What they control:**
- `sensor_polling_delay_ms`: Affects temporal resolution of lick, torque, and TTL sensors
- `screen_trigger_pulse_duration_ms`: Duration of TTL pulse to toggle VR screen power
- `cm_per_unity_unit`: Conversion factor for synchronizing VR corridor with physical space
- `mesoscope_frame_averaging_pool_size`: Number of digital pin readouts to average when determining the logic level
  of the incoming TTL signal from the mesoscope at frame acquisition onset. Set to 0 to disable averaging.

---

## External Assets Configuration

Zaber motor controllers and MQTT broker settings.

### Zaber Motor Ports

| Parameter       | Default          | Motor Group                              |
|-----------------|------------------|------------------------------------------|
| `headbar_port`  | `/dev/ttyUSB0`   | Headbar motors (Z, Pitch, Roll axes)     |
| `lickport_port` | `/dev/ttyUSB1`   | Lickport motors (Z, Y, X axes)           |
| `wheel_port`    | `/dev/ttyUSB2`   | Wheel motor (X-axis horizontal position) |

**Discovery tool:** `get_zaber_devices_tool()` from sl-experiment

**What they control:**
- Serial port connections to three independent Zaber motor controller groups
- Each port connects to daisy-chained stepper motor controllers via USB

**Used by:** `ZaberMotors` class via `ZaberConnection`

**Motor group structure:**
- Headbar: 3 daisy-chained motors (Z-Pitch-Roll)
- Lickport: 3 daisy-chained motors (Z-Y-X)
- Wheel: 1 motor (X-axis only)

**Constraints:**
- Valid USB device paths: `/dev/ttyUSB0`, `/dev/ttyUSB1`, `/dev/ttyUSB2`, etc.
- Must be unique for each motor group
- Note: Zaber motors use `/dev/ttyUSB*` while microcontrollers use `/dev/ttyACM*`

---

### MQTT Broker Configuration

| Parameter    | Type  | Default       | Description                    |
|--------------|-------|---------------|--------------------------------|
| `unity_ip`   | `str` | `"127.0.0.1"` | MQTT broker IP address         |
| `unity_port` | `int` | `1883`        | MQTT broker port number        |

**Discovery tool:** `check_mqtt_broker(host, port)` from ataraxis-communication-interface

**Used by:** `MQTTCommunication` in data_acquisition module for Unity game engine communication.

**What they control:**
- `unity_ip`: IP address of the MQTT broker for VR communication
- `unity_port`: Port number of the MQTT broker

**Constraints:**
- The MQTT broker (typically Mosquitto) must be running at the specified address before starting experiments
- For local Unity instances, use the default `127.0.0.1:1883`
- For remote Unity PCs, configure the appropriate network address

**MQTT topics used by sl-experiment:**
- `CUE_SEQUENCE`: Wall cue sequence from VR
- `UNITY_TERMINATION`: Signal to end task
- `UNITY_STARTUP`: Startup handshake
- `UNITY_SCENE`: Scene information exchange
- `STIMULUS`: Trial stimulus commands
- `TRIGGER_DELAY`: Timing adjustments
- `ENCODER_DATA`: Wheel position to VR

---

## Configuration Priority Summary

### Must Configure (No Defaults)

These parameters have empty defaults and must be configured before system use:

| Parameter             | Section     | Why Required                              |
|-----------------------|-------------|-------------------------------------------|
| `root_directory`      | Filesystem  | Local data storage path                   |
| `server_directory`    | Filesystem  | Network storage for processed data        |
| `nas_directory`       | Filesystem  | Backup storage mount                      |
| `mesoscope_directory` | Filesystem  | ScanImagePC output directory              |
| `surgery_sheet_id`    | Sheets      | Surgery log tracking                      |
| `water_log_sheet_id`  | Sheets      | Animal welfare compliance                 |

### Should Verify (Hardware-Dependent)

These parameters have defaults but should be verified for your specific hardware using MCP discovery tools:

| Parameter                     | Section          | Discovery Tool                   |
|-------------------------------|------------------|----------------------------------|
| `face_camera_index`           | Cameras          | `list_cameras()`                 |
| `body_camera_index`           | Cameras          | `list_cameras()`                 |
| `actor_port`                  | Microcontrollers | `list_microcontrollers()`        |
| `sensor_port`                 | Microcontrollers | `list_microcontrollers()`        |
| `encoder_port`                | Microcontrollers | `list_microcontrollers()`        |
| `headbar_port`                | External Assets  | `get_zaber_devices_tool()`       |
| `lickport_port`               | External Assets  | `get_zaber_devices_tool()`       |
| `wheel_port`                  | External Assets  | `get_zaber_devices_tool()`       |
| `valve_calibration_data`      | Microcontrollers | None (hardware calibration)      |
| `minimum_brake_strength_g_cm` | Microcontrollers | None (hardware calibration)      |
| `maximum_brake_strength_g_cm` | Microcontrollers | None (hardware calibration)      |

### Can Use Defaults (Typically Unchanged)

These parameters have sensible defaults that work for most setups:

| Parameter                   | Section          | Default  | Notes                         |
|-----------------------------|------------------|----------|-------------------------------|
| `face_camera_quantization`  | Cameras          | `20`     | Good quality/size balance     |
| `face_camera_preset`        | Cameras          | `7`      | Good encoding efficiency      |
| `body_camera_quantization`  | Cameras          | `20`     | Good quality/size balance     |
| `body_camera_preset`        | Cameras          | `7`      | Good encoding efficiency      |
| `keepalive_interval_ms`     | Microcontrollers | `500`    | Responsive failure detection  |
| `wheel_diameter_cm`         | Microcontrollers | `15.03`  | Standard mouse wheel          |
| `wheel_encoder_ppr`         | Microcontrollers | `8192`   | High-resolution encoder       |
| `lick_threshold_adc`        | Microcontrollers | `600`    | Typical lick detection        |
| `sensor_polling_delay_ms`   | Microcontrollers | `1`      | 1 kHz sampling rate           |
| `cm_per_unity_unit`         | Microcontrollers | `10.0`   | Standard VR scaling           |
