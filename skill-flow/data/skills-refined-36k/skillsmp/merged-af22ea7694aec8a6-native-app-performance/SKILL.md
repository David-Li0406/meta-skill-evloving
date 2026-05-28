---
name: native-app-performance
description: Use this skill when you need to profile, analyze, or optimize the performance of native macOS/iOS applications using CLI tools without opening the Instruments UI.
---

# Native App Performance (CLI-only)

Goal: Record Time Profiler via `xctrace`, extract samples, symbolicate, and propose hotspots without opening Instruments.

## Quick start (CLI)

1. **Record Time Profiler (attach)**:

    ```bash
    # Start app yourself, then attach
    xcrun xctrace record --template 'Time Profiler' --time-limit 90s --output /tmp/App.trace --attach <pid>
    ```

2. **Record Time Profiler (launch)**:

    ```bash
    xcrun xctrace record --template 'Time Profiler' --time-limit 90s --output /tmp/App.trace --launch -- /path/App.app/Contents/MacOS/App
    ```

3. **Extract time samples**:

    ```bash
    scripts/extract_time_samples.py --trace /tmp/App.trace --output /tmp/time-sample.xml
    ```

4. **Get load address for symbolication**:

    ```bash
    # While app is running
    vmmap <pid> | rg -m1 "__TEXT" -n
    ```

5. **Symbolicate + rank hotspots**:

    ```bash
    scripts/top_hotspots.py --samples /tmp/time-sample.xml \
      --binary /path/App.app/Contents/MacOS/App \
      --load-address 0x100000000 --top 30
    ```

## Workflow notes

- Confirm you’re profiling the correct binary (local build vs /Applications). Prefer direct binary path for `--launch`.
- Trigger the slow path during capture (menu open/close, refresh, etc.).
- If stacks are empty, capture longer or avoid idle sections.
- Use `xcrun xctrace help record` and `xcrun xctrace help export` for correct flags.

## Included scripts

- `scripts/record_time_profiler.sh`: Record via attach or launch.
- `scripts/extract_time_samples.py`: Export time-sample XML from a trace.
- `scripts/top_hotspots.py`: Symbolicate and rank top app frames.

## Gotchas

- ASLR means you must use the runtime `__TEXT` load address from `vmmap`.
- If using a new build, update the `--binary` path; symbols must match the trace.
- CLI-only flow: no need to open Instruments if stacks are symbolicated via `atos`.