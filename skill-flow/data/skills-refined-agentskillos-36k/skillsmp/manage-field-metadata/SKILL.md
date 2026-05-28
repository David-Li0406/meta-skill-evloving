---
name: manage_field_metadata
description: 多次元フィールド（ScalarField等）の4D構造維持、ドメイン変換（時間・空間・周波数・波数）、および物理単位の整合性を管理する
---

# Manage Field Metadata

Provides design patterns for maintaining physical consistency (domains and units) and preventing dimensionality loss when handling multi-dimensional field data (such as `ScalarField`) in `gwexpy`.

## 1. Metadata-Preserving Indexing (4D Structure Maintenance)

Ensures that during slicing operations, even if a specific dimension becomes length 1, the axis is not removed, and the 4-dimensional structure is maintained to prevent the loss of metadata.

*   **Implementation Pattern**:
    ```python
    def _force_4d_item(self, item):
        # Convert integer indices to slice(i, i+1) to preserve dimensions
        new_item = list(item)
        for i, val in enumerate(new_item):
            if isinstance(val, int):
                new_item[i] = slice(val, val + 1)
        return tuple(new_item)
    ```

## 2. Domain Conversion and Coordinate Updates

When domains are transformed via FFT or PSD (e.g., Time -> Frequency, Real -> K-space), the following four elements are updated as a set:

1.  **Data Values**: Application of the transformation algorithm.
2.  **Axis Coordinates (Index)**: Generation of new sampling coordinates based on $1/(\Delta x)$.
3.  **Axis Names (Name)**: Prefixes/name changes such as `t` -> `f`, `x` -> `kx`.
4.  **Domain State**: Update of `axis0_domain` or `space_domains` metadata.

## 3. Spectral Unit Tracking (Physical Unit Propagation)

Automatically calculates units after transformation.

*   **PSD (Density scaling)**: $[unit]^2 / [1/axis\_unit]$ (e.g., $V^2/Hz$)
*   **PSD (Spectrum scaling)**: $[unit]^2$
*   **Wavenumber**: $[axis\_unit]^{-1}$ (e.g., $1/m$)

## 4. Validation for Generalized Axis Processing

Signal processing methods (such as `spectral_density`) must verify that the target axis meets the following conditions:

*   **Regularity**: Must be `AxisDescriptor.regular`.
*   **Size**: Sufficient data length for the transform (typically 2 or more).
*   **Current Domain**: Must not already be transformed (e.g., trying to apply PSD to an already frequency-domain axis).

## Application Examples
- `spectral_density` method in `gwexpy/fields/scalar.py`
- `_validate_axis_for_spectral` internal function in `gwexpy/fields/signal.py`
