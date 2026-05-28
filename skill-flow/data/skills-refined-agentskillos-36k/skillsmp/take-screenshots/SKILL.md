---
name: take-screenshots
description: A Windows screenshot skill that provides both programmatic full-screen capture and interactive region selection.
license: ""
compatibility: opencode
---

# take-screenshots

## Purpose

RegionSnip is a Windows screenshot capture utility written in C# that provides both programmatic full-screen capture and interactive region selection. It supports JPEG formats, with options for quality compression and image scaling to optimize file size.

## Usage

RegionSnip is designed to be called programmatically and outputs JSON results to stdout.

### Command Line Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `--mode <mode>` | Capture mode: `full` or `region` (default: region) | `--mode full` |
| `--out <path>` | Output file path (required). Use `.jpg` or `.jpeg` for JPEG compression. | `--out screenshot.jpg` |
| `--all` | Capture all monitors (full mode only) | `--all` |
| `--monitor <n>` | Specific monitor index (0-based, full mode only) | `--monitor 1` |
| `--prompt <text>` | Custom prompt text for region selection | `--prompt "Select area"` |
| `--quality <n>` | JPEG quality level (1-100, default: 80) | `--quality 75` |
| `--scale <n>` | Image scaling factor (0.1-1.0, default: 0.75 for full, 1.0 for region) | `--scale 0.5` |

### Examples

#### Full-screen capture of primary monitor:
```bash
./scripts/RegionSnip.exe --mode full --out screenshot.jpg
```

#### Full-screen capture of all monitors:
```bash
./scripts/RegionSnip.exe --mode full --out screenshot.jpg --all
```

#### Full-screen capture of specific monitor:
```bash
./scripts/RegionSnip.exe --mode full --out screenshot.jpg --monitor 1
```

#### Interactive region selection:
```bash
./scripts/RegionSnip.exe --mode region --out screenshot.jpg
```

#### Interactive region selection with custom prompt:
```bash
./scripts/RegionSnip.exe --mode region --out screenshot.jpg --prompt "Drag to select the area to capture"
```

#### Optimized Capture Prefered (JPEG + Scaling):
To significantly reduce file size (e.g., for sending to LLMs), use `.jpg` extension along with quality and scale parameters.

```bash
# Reduces size by using JPEG compression (80%) and scaling down to 50%
./scripts/RegionSnip.exe --mode full --out screenshot.jpg --quality 80 --scale 0.5
```

## Output Format

RegionSnip outputs JSON to stdout with the following structure:

### Success Response (Full Mode):
```json
{
  "ok": true,
  "path": "screenshot.jpg",
  "mode": "full",
  "monitorIndex": 0,
  "all": false,
  "rect": {
    "x": 0,
    "y": 0,
    "width": 1920,
    "height": 1080
  },
  "width": 1920,
  "height": 1080
}
```

### Success Response (Region Mode):
```json
{
  "ok": true,
  "path": "screenshot.jpg",
  "mode": "region",
  "rect": {
    "x": 100,
    "y": 100,
    "width": 800,
    "height": 600
  },
  "width": 800,
  "height": 600
}
```

### Error Response:
```json
{
  "ok": false,
  "error": "Description of what went wrong",
  "mode": "region"
}
```

### Cancellation Response (Region Mode):
```json
{
  "ok": false,
  "cancelled": true,
  "mode": "region"
}
```

## Error Handling

- Always check the `ok` field in the response
- For region selection, users can cancel the operation (results in `cancelled: true`)
- Common errors include invalid monitor indices, permission issues, or timeout
- Screenshots are saved as JPEG files to the specified path
- Base64 image data is included when `includeImage=true` for further processing
