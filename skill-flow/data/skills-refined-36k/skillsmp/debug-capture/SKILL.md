---
name: debug_capture
description: Guide for debugging and modifying Wayland capture logic in hdmi-wifi
---

# Debug & Modify Wayland Capture

This skill helps you navigate `src/screencopy_capture.rs` and debug issues related to Wayland screen capture (wlr-screencopy-unstable-v1).

## 🧠 Context
The capture module is responsible for:
1.  Connecting to the Wayland display.
2.  Requesting frames via `zwlr_screencopy_manager_v1`.
3.  Handling buffer copy (Linux DMABUF or POSIX SHM).
4.  Handling "buffer done" events to feed the encoder.

## 🛠️ Common Issues & Fixes

### 1. "Protocol not found" or "Compositor not supported"
**Symptom**: The app crashes at startup claiming the global interface is missing.
**Cause**: The compositor does not support `wlr-screencopy-unstable-v1`.
**Verification**:
```bash
# Check if the Wayland global is available
wayland-info | grep screencopy
```
**Fix**: Ensure you are using Sway, Hyprland, Wayfire, or a wlroots compositor. GNOME/Mutter is **not** supported.

### 2. Black Screen / Invalid Buffer
**Symptom**: Stream is connected but video is black or garbage.
**Cause**: Mismatched buffer strides or pixel formats.
**Debugging**:
-   Inspect the `frame` events in `screencopy_capture.rs`.
-   Add logging to print `buffer_width`, `buffer_height`, `stride`, and `format`.
```rust
// In src/screencopy_capture.rs
tracing::debug!("Format: {:?}, Stride: {}", format, stride);
```
-   The encoder expects `AV_PIX_FMT_BGR0` or `AV_PIX_FMT_BGRA`. If the compositor sends `XRGB8888`, ensure the colorspace conversion handles it.

### 3. High Latency / Laggy Capture
**Cause**: Blocking the Wayland event loop or slow copy.
**Check**:
-   Ensure `event_queue.dispatch()` is called frequently.
-   Verify we are using DMABUF (zero-copy) if possible, though currently the project might rely on `mmap` (SHM).

## 🚀 Key Code Paths

### `src/screencopy_capture.rs`

-   **`Capture::new()`**: Usage of `GlobalManager` to find `zwlr_screencopy_manager_v1`.
-   **`capture_output()`**: The main loop where we ask for `capture_output`.
-   **`FrameHandler`**: Callbacks for `buffer`, `linux_dmabuf`, `buffer_done`.

## 🧪 Verification Commands

Run with debug logs to see protocol events:
```bash
RUST_LOG=hdmi_wifi=debug,wayland_client=debug ./target/release/hdmi-wifi
```
