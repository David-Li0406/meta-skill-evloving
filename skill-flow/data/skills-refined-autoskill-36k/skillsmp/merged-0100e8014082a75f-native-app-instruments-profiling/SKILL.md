---
name: native-app-instruments-profiling
description: Use this skill for performance profiling and stack analysis of native macOS/iOS apps using Instruments and xctrace, focusing on CLI-based workflows and correct binary selection.
---

# Native App Instruments Profiling (CLI)

Goal: Record performance data using Time Profiler via `xctrace`, extract samples, symbolicate, and identify hotspots without opening the Instruments UI.

## Quick Start (CLI)

1. **List available templates**:
   ```bash
   xcrun xctrace list templates
   ```

2. **Record Time Profiler (attach)**:
   ```bash
   # Start app yourself, then attach
   xcrun xctrace record --template 'Time Profiler' --time-limit 90s --output /tmp/App.trace --attach <pid>
   ```

3. **Record Time Profiler (launch)**:
   ```bash
   xcrun xctrace record --template 'Time Profiler' --time-limit 90s --output /tmp/App.trace --launch -- /path/App.app/Contents/MacOS/App
   ```

4. **Extract time samples**:
   ```bash
   scripts/extract_time_samples.py --trace /tmp/App.trace --output /tmp/time-sample.xml
   ```

5. **Get load address for symbolication**:
   ```bash
   # While app is running
   vmmap <pid> | rg -m1 "__TEXT" -n
   ```

6. **Symbolicate and rank hotspots**:
   ```bash
   scripts/top_hotspots.py --samples /tmp/time-sample.xml \
     --binary /path/App.app/Contents/MacOS/App \
     --load-address 0x100000000 --top 30
   ```

## Workflow Notes

- Always confirm you’re profiling the correct binary (local build vs /Applications). Prefer direct binary path for `--launch`.
- Ensure you trigger the slow path during capture (menu open/close, refresh, etc.).
- If stacks are empty, capture longer or avoid idle sections.
- Use `xcrun xctrace help record` and `xcrun xctrace help export` for correct flags.

## Command Arguments (xctrace)

- `--template 'Time Profiler'`: specify the template for profiling.
- `--launch -- <cmd>`: everything after `--` is the target command (binary or app bundle).
- `--attach <pid|name>`: attach to a running process.
- `--output <path>`: specify the output path for the trace file.
- `--time-limit 60s|5m`: set the duration for capturing data.
- `--device <name|UDID>`: required for profiling on iOS devices.

## Gotchas & Fixes

- **Wrong app profiled**: Instruments may profile the wrong app if LaunchServices resolves a different bundle. Use direct binary paths or attach with known PID.
- **No samples / empty trace**: If the app exits quickly or does not perform work, increase capture duration and ensure workload is triggered during recording.
- **Privacy prompts**: `xctrace` may require Developer Tools permission. Allow Terminal/Xcode in System Settings → Privacy & Security → Developer Tools.
- **Large XML exports**: Filter with XPath and aggregate offline to manage size.

## iOS Specific Notes

- Use `xcrun xctrace list devices` and `--device <UDID>` for iOS profiling.
- Launch via Xcode if necessary; attach with `xctrace --attach`.
- Ensure debug symbols are available for meaningful stack traces.

## Verification Checklist

- Confirm the trace process path matches the target build.
- Ensure stacks show expected app frames.
- Capture covers the slow operation (startup/refresh).
- Export stacks for automated diffing if optimizing.

## Included Scripts

- `scripts/record_time_profiler.sh`: record via attach or launch.
- `scripts/extract_time_samples.py`: export time-sample XML from a trace.
- `scripts/top_hotspots.py`: symbolicate and rank top app frames.