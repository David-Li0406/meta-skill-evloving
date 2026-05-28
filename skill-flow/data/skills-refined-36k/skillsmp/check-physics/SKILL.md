---
name: check_physics
description: 実装内容が数学的・物理学的に妥当か検証する
---

# Verify Physics

This skill performs a review of the code specifically focusing on physics and math correctness.

## Instructions

1. **Dimensional Analysis**:
    * Check if unit handling (e.g., `astropy.units`, `quantities`) is used correctly.
    * Ensure operations are physically valid (e.g., not adding Length to Time).
    * **Unit-Safe Assignment**: Avoid direct slice assignment `series[:] = raw_array` if `series` has units. Use `series.value[:] = raw_array` to update data while preserving unit metadata.

2. **Mathematical Inspection**:
    * Verify equations against known reference papers or standard textbooks.
    * Check for numerical stability issues (e.g., division by zero, floating point precision loss).
    * Check edge cases (e.g., $f=0$, infinite limits).

3. **Sanity Checks**:
    * **Conservation Laws**: Create a script to verify energy conservation (Parseval's theorem) for FFT/PSD transformations. Ratio of frequency-domain energy to time-domain energy should be ~1.0.
    * **Theoretical Benchmarks**: Use known signals (Sine wave, Gaussian noise) to verify peak frequency, amplitude, and spectral flatness.
    * **Multi-domain Verification**: For multi-dimensional fields, verify transformations along *all* applicable axes (e.g., spatial FFT as well as temporal FFT).
    * Verify that reasonable inputs produce physically reasonable outputs.

4. **Report**:
    * Provide a summary of the analysis, pointing out any suspect logic or confirming validity.
