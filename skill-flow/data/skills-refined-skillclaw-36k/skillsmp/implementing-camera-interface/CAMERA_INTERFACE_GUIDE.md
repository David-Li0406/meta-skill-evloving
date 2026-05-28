# ataraxis-video-system API Reference

Complete API reference for the ataraxis-video-system library used for camera integration in sl-experiment.

---

## Core Imports

```python
from ataraxis_video_system import (
    VideoSystem,
    VideoEncoders,
    CameraInterfaces,
    CameraInformation,
    OutputPixelFormats,
    InputPixelFormats,
    EncoderSpeedPresets,
    discover_camera_ids,
    add_cti_file,
    check_cti_file,
    check_ffmpeg_availability,
    check_gpu_availability,
    extract_logged_camera_timestamps,
)
```

---

## VideoSystem Class

The main orchestration class for camera acquisition and video encoding.

### Constructor Parameters

| Parameter                | Type                  | Required | Default     | Description                                            |
|--------------------------|-----------------------|----------|-------------|--------------------------------------------------------|
| `system_id`              | `np.uint8`            | Yes      | -           | Unique identifier for DataLogger timestamp correlation |
| `data_logger`            | `DataLogger`          | Yes      | -           | Shared logger instance for frame timestamp logging     |
| `output_directory`       | `Path \| None`        | No       | `None`      | Directory for video output (None disables saving)      |
| `camera_interface`       | `CameraInterfaces`    | No       | `OPENCV`    | Camera backend: HARVESTERS, OPENCV, or MOCK            |
| `camera_index`           | `int`                 | No       | `0`         | Camera index from discovery functions                  |
| `display_frame_rate`     | `int \| None`         | No       | `None`      | Live preview rate in FPS (None disables preview)       |
| `frame_width`            | `int \| None`         | No       | `None`      | Override native camera frame width in pixels           |
| `frame_height`           | `int \| None`         | No       | `None`      | Override native camera frame height in pixels          |
| `frame_rate`             | `int \| None`         | No       | `None`      | Override native camera frame rate in FPS               |
| `gpu`                    | `int`                 | No       | `-1`        | GPU index for hardware encoding (-1 for CPU only)      |
| `video_encoder`          | `VideoEncoders`       | No       | `H265`      | Video codec: H264 or H265                              |
| `encoder_speed_preset`   | `EncoderSpeedPresets` | No       | `SLOW`      | Encoding speed vs quality tradeoff                     |
| `output_pixel_format`    | `OutputPixelFormats`  | No       | `YUV444`    | Output color format: YUV420 or YUV444                  |
| `quantization_parameter` | `int`                 | No       | `15`        | Quality parameter 0-51 (lower = higher quality)        |
| `color`                  | `bool \| None`        | No       | `None`      | Color mode for OpenCV/Mock (True=BGR, False=MONO)      |

### Methods

| Method                 | Returns | Description                                                          |
|------------------------|---------|----------------------------------------------------------------------|
| `start()`              | `None`  | Spawns producer (acquisition) and consumer (encoding) processes      |
| `stop()`               | `None`  | Terminates all processes and releases camera/encoder resources       |
| `start_frame_saving()` | `None`  | Enables writing encoded frames to disk (call after `start()`)        |
| `stop_frame_saving()`  | `None`  | Stops writing frames to disk while keeping acquisition active        |

### Properties

| Property          | Type           | Description                                                   |
|-------------------|----------------|---------------------------------------------------------------|
| `video_file_path` | `Path \| None` | Full path to the output MP4 file (None if saving disabled)    |
| `started`         | `bool`         | True if producer and consumer processes are currently running |
| `system_id`       | `np.uint8`     | The unique system identifier assigned at construction         |

### Lifecycle

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         VideoSystem Lifecycle                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  __init__()                                                              │
│      │                                                                   │
│      ▼                                                                   │
│  start() ─────────────────────────────────────────────────────────────┐  │
│      │                                                                │  │
│      ▼                                                                │  │
│  [Frame acquisition active, preview displayed if configured]          │  │
│      │                                                                │  │
│      ├──── start_frame_saving() ───┐                                  │  │
│      │                             │                                  │  │
│      │                             ▼                                  │  │
│      │              [Frames written to MP4 file]                      │  │
│      │                             │                                  │  │
│      ├──── stop_frame_saving() ◄───┘                                  │  │
│      │                                                                │  │
│      ▼                                                                │  │
│  stop() ◄─────────────────────────────────────────────────────────────┘  │
│      │                                                                   │
│      ▼                                                                   │
│  [Resources released]                                                    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Enumerations

### CameraInterfaces

```python
class CameraInterfaces(StrEnum):
    HARVESTERS = "harvesters"  # GeniCam-compatible cameras (GigE, USB3 Vision)
    OPENCV = "opencv"          # Consumer-grade USB cameras
    MOCK = "mock"              # Testing only (simulated camera)
```

**Usage guidance:**
- Use `HARVESTERS` for scientific/industrial cameras (requires CTI file configuration)
- Use `OPENCV` for standard USB webcams
- Use `MOCK` for testing without physical hardware

### VideoEncoders

```python
class VideoEncoders(StrEnum):
    H264 = "H264"  # Wider compatibility, larger file size
    H265 = "H265"  # Better compression (recommended for production)
```

**Recommendation:** Use H265 for production workloads. Use H264 when compatibility with older players is required.

### EncoderSpeedPresets

```python
class EncoderSpeedPresets(IntEnum):
    FASTEST = 1   # CPU: veryfast, GPU: p1
    FASTER = 2    # CPU: faster, GPU: p2
    FAST = 3      # CPU: fast, GPU: p3
    MEDIUM = 4    # CPU: medium, GPU: p4
    SLOW = 5      # CPU: slow, GPU: p5 (default)
    SLOWER = 6    # CPU: slower, GPU: p6
    SLOWEST = 7   # CPU: veryslow, GPU: p7
```

**Trade-offs:**
- Faster presets reduce CPU/GPU load but increase file size
- Slower presets improve compression but cause frame buffering under load, risking OOM errors
- For real-time acquisition, start with `MEDIUM` and adjust based on system performance

### OutputPixelFormats

```python
class OutputPixelFormats(StrEnum):
    YUV420 = "yuv420p"  # Standard, half-bandwidth chrominance
    YUV444 = "yuv444p"  # Better color accuracy (default)
```

**Recommendation:** Default YUV444 provides minimal chromatic data loss. Use YUV420 for smaller file sizes when color
accuracy is less critical, for example, when using Monochrome cameras.

### InputPixelFormats

```python
class InputPixelFormats(StrEnum):
    MONOCHROME = "gray"   # Grayscale images
    BGR = "bgr24"         # Color images (BGR channel order)
```

---

## Discovery Functions

### discover_camera_ids

Discovers all cameras accessible through both OpenCV and Harvesters interfaces.

```python
def discover_camera_ids() -> tuple[CameraInformation, ...]
```

**Returns:** Tuple of `CameraInformation` dataclass instances for all discovered cameras.

**Notes:**
- OpenCV cameras are discovered first, followed by Harvesters cameras
- For Harvesters cameras, requires a valid CTI file (see `add_cti_file()`)
- If no CTI file is configured, Harvesters camera discovery is skipped

### CameraInformation

Dataclass containing discovered camera details:

```python
@dataclass()
class CameraInformation:
    camera_index: int              # Index for VideoSystem
    interface: CameraInterfaces    # OPENCV or HARVESTERS
    frame_width: int               # Native frame width in pixels
    frame_height: int              # Native frame height in pixels
    acquisition_frame_rate: int    # Native frame rate in FPS
    serial_number: str | None      # Harvesters only
    model: str | None              # Harvesters only
```

**Example:**

```python
from ataraxis_video_system import discover_camera_ids, CameraInterfaces

cameras = discover_camera_ids()
for cam in cameras:
    print(f"Index: {cam.camera_index}, Interface: {cam.interface}")
    print(f"Resolution: {cam.frame_width}x{cam.frame_height} @ {cam.acquisition_frame_rate} fps")
    if cam.interface == CameraInterfaces.HARVESTERS:
        print(f"Model: {cam.model}, Serial: {cam.serial_number}")
```

### add_cti_file

Configures the GenTL Producer file for Harvesters camera support.

```python
def add_cti_file(cti_path: Path) -> None
```

**Parameters:**
- `cti_path`: Path to the .cti GenTL Producer file

**Notes:**
- Must be called before `discover_camera_ids()` or creating a VideoSystem with `CameraInterfaces.HARVESTERS`
- The setting persists across sessions (stored in user data directory)
- Any valid CTI file works; camera vendor-specific CTI files are typically best

### check_cti_file

Checks whether a valid CTI file is configured.

```python
def check_cti_file() -> Path | None
```

**Returns:** Path to the configured CTI file if valid, or None if not configured/invalid.

**Example:**

```python
from ataraxis_video_system import check_cti_file, add_cti_file
from pathlib import Path

cti_path = check_cti_file()
if cti_path is None:
    # Configure CTI file (example path - use your camera vendor's CTI file)
    add_cti_file(Path("/opt/mvIMPACT_Acquire/lib/x86_64/mvGenTLProducer.cti"))
```

---

## Utility Functions

### check_ffmpeg_availability

```python
def check_ffmpeg_availability() -> bool
```

**Returns:** True if FFMPEG is installed and accessible, False otherwise.

### check_gpu_availability

```python
def check_gpu_availability() -> bool
```

**Returns:** True if NVIDIA GPU hardware encoding is available, False otherwise.

### extract_logged_camera_timestamps

Extracts frame acquisition timestamps from a DataLogger archive.

```python
def extract_logged_camera_timestamps(log_path: Path, n_workers: int = -1) -> tuple[np.uint64, ...]
```

**Parameters:**
- `log_path`: Path to the assembled .npz log archive
- `n_workers`: Number of parallel workers (-1 for all cores, 1 for sequential)

**Returns:** Tuple of timestamps (microseconds since UTC epoch) in frame order.

**Example:**

```python
from ataraxis_video_system import extract_logged_camera_timestamps
from pathlib import Path

timestamps = extract_logged_camera_timestamps(Path("051_log.npz"))
frame_times_seconds = [ts / 1e6 for ts in timestamps]  # Convert to seconds
```

---

## Data Logging

VideoSystem logs frame acquisition timestamps using the DataLogger class from ataraxis-data-structures.

### Log Entry Format

Each log entry is a 1D numpy uint8 array:

| Offset | Size    | Content                                        |
|--------|---------|------------------------------------------------|
| 0      | 1 byte  | System ID (uint8)                              |
| 1      | 8 bytes | Timestamp (uint64, microseconds since onset)   |

### Onset Entry Format

The first log entry for each VideoSystem uses a special format:

| Offset | Size    | Content                                        |
|--------|---------|------------------------------------------------|
| 0      | 1 byte  | System ID (uint8)                              |
| 1      | 8 bytes | Zero (indicates onset entry)                   |
| 9      | 8 bytes | UTC timestamp (microseconds since epoch)       |

---

## Dependencies

### External Requirements

| Dependency | Required | Purpose                                                           |
|------------|----------|-------------------------------------------------------------------|
| FFMPEG     | Yes      | Backend for H.264/H.265 video encoding                            |
| CTI file   | No       | GenTL Producer for Harvesters cameras (any vendor's CTI works)    |
| NVIDIA GPU | No       | Required for hardware-accelerated encoding (optional)             |

**Note:** For Harvesters cameras, any valid CTI file works. Camera vendor-specific CTI files (e.g., from Basler, FLIR,
Allied Vision) are typically recommended. The mvImpactAcquire CTI file is one example that works with many cameras.

### Python Requirements

```
ataraxis-video-system>=2.3.0
ataraxis-data-structures>=5.0.0
```

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                        VideoSystem                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Main Process                                            │  │
│  │  - Initialization and configuration                      │  │
│  │  - Lifecycle management (start/stop)                     │  │
│  │  - Frame saving control                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│           │                           │                        │
│           ▼                           ▼                        │
│  ┌────────────────────┐   ┌────────────────────────────────┐   │
│  │  Producer Process  │   │      Consumer Process          │   │
│  │  ───────────────── │   │  ──────────────────────────────│   │
│  │  - Camera driver   │   │  - Frame encoding (FFMPEG)     │   │
│  │  - Frame grabbing  │──▶│  - MP4 container writing       │   │
│  │  - Timestamp gen   │   │  - Live preview display        │   │
│  └────────────────────┘   └────────────────────────────────┘   │
│           │                                                    │
│           ▼                                                    │
│  ┌────────────────────┐                                        │
│  │    DataLogger      │                                        │
│  │  ───────────────── │                                        │
│  │  - Timestamp I/O   │                                        │
│  │  - .npy file write │                                        │
│  └────────────────────┘                                        │
└────────────────────────────────────────────────────────────────┘
```

---

## Code Examples

### Basic Camera Acquisition

```python
from pathlib import Path
import numpy as np
from ataraxis_data_structures import DataLogger
from ataraxis_video_system import VideoSystem, CameraInterfaces, VideoEncoders

if __name__ == "__main__":
    output_dir = Path("/tmp/camera_test")
    output_dir.mkdir(exist_ok=True)

    logger = DataLogger(output_directory=output_dir, instance_name="test")
    logger.start()

    camera = VideoSystem(
        system_id=np.uint8(51),
        data_logger=logger,
        output_directory=output_dir,
        camera_interface=CameraInterfaces.OPENCV,
        camera_index=0,
        display_frame_rate=15,
        video_encoder=VideoEncoders.H264,
    )

    camera.start()
    # Preview mode - frames displayed but not saved

    camera.start_frame_saving()
    # Recording mode - frames saved to MP4

    # ... acquisition runs ...

    camera.stop_frame_saving()
    camera.stop()
    logger.stop()
```

### GeniCam Camera Setup

```python
from pathlib import Path
import numpy as np
from ataraxis_data_structures import DataLogger
from ataraxis_video_system import (
    VideoSystem,
    CameraInterfaces,
    VideoEncoders,
    EncoderSpeedPresets,
    OutputPixelFormats,
    add_cti_file,
    check_cti_file,
    discover_camera_ids,
)

if __name__ == "__main__":
    # Check/configure CTI file (use your camera vendor's CTI file)
    if check_cti_file() is None:
        add_cti_file(Path("/path/to/your/camera/vendor.cti"))

    # Discover cameras
    cameras = discover_camera_ids()
    harvesters_cameras = [c for c in cameras if c.interface == CameraInterfaces.HARVESTERS]
    print(f"Found {len(harvesters_cameras)} Harvesters cameras")

    # Setup for high-quality recording
    logger = DataLogger(output_directory=Path("/data/session"), instance_name="camera")
    logger.start()

    camera = VideoSystem(
        system_id=np.uint8(51),
        data_logger=logger,
        output_directory=Path("/data/session"),
        camera_interface=CameraInterfaces.HARVESTERS,
        camera_index=harvesters_cameras[0].camera_index,
        display_frame_rate=25,
        video_encoder=VideoEncoders.H265,
        gpu=0,  # Use GPU encoding (use -1 for CPU)
        encoder_speed_preset=EncoderSpeedPresets.MEDIUM,
        output_pixel_format=OutputPixelFormats.YUV444,
        quantization_parameter=15,
    )

    camera.start()
    camera.start_frame_saving()
    # ... acquisition ...
    camera.stop()
    logger.stop()
```
