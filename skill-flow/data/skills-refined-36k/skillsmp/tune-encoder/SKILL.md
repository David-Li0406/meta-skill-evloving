---
name: tune_encoder
description: Guide for tuning x264 encoder settings (latency vs quality)
---

# Tune Video Encoder

This skill helps you adjust `src/encoder.rs` to optimize the H.264 encoding pipeline for the desired balance between **latency** and **image quality**.

## 🧠 Context
The encoder uses `libx264` (exposed via C bindings or the `x264` crate).
Key parameters:
-   **Preset**: Speed vs Compression efficiency (`ultrafast`, `superfast`, `veryfast`, `medium`, `slow`).
-   **Tune**: Optimization target (`zerolatency`, `film`, `animation`).
-   **Bitrate / CRF**: Constant bitrate or Constant Rate Factor (quality).

## 🛠️ Configuration Guide

### 1. Achieving Lowest Latency
To minimize delay (Glass-to-glass latency), prioritize speed over compression.

```rust
// In src/encoder.rs

// 1. Use 'ultrafast' or 'superfast'
// 2. Set tune 'zerolatency' (CRITICAL)
let mut param = x264_param_t::default();
x264_param_default_preset(&mut param, "superfast\0".as_ptr() as *const i8, "zerolatency\0".as_ptr() as *const i8);
```

**Tradeoff**: Higher bitrate required for same quality, or lower quality at same bitrate.

### 2. Improving Image Quality
If the image is blocky or blurry:
-   **Lower CRF**: (Lower is better quality). Range 0-51. Default ~23. Try 18-20 for high quality.
-   **Increase Bitrate**: If using CBR/ABR.
-   **Slower Preset**: switch to `veryfast` or `faster`.

```rust
// Adjusting Quality (CRF)
param.rc.i_rc_method = X264_RC_CRF;
param.rc.f_rf_constant = 20.0; // Higher quality than default
```

### 3. Handling Profiling (High/Main/Baseline)
Some H/W decoders on clients (older phones) only support Baseline.
```rust
x264_param_apply_profile(&mut param, "baseline\0".as_ptr() as *const i8);
```

## 🚀 Performance Tips
-   **Threads**: x264 is multithreaded. Ensure `param.i_threads` is set to auto (`0`) or specific count.
-   **Slicing**: For strict low latency, use `i_slice_max_size` to send smaller NAL units, reducing jitter.

## 🧪 Verification
Monitor the stats endpoint (`/stats`) to see if `frames_captured` matches `frames_encoded`. If dropped frames increase, the encoder is too slow (CPU bottleneck).

Also run the unit tests to ensure configuration validity:
```bash
cargo test
```
