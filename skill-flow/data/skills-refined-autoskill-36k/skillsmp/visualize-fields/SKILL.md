---
name: visualize_fields
description: 多次元フィールドデータ（Field4D/Matrix等）の抽出ロジックと描画APIを、物理的整合性を保ちながら実装する
---

# Visualize Fields Best Practices

When implementing visualization for multi-dimensional data (3D, 4D, Matrix, etc.), design using the following three-layer structure to ensure maintainability and physical accuracy.

## 1. Infrastructure (Coordinate & Utility Layer)

Separate the conversion logic between physical coordinates and array indices from the class body, and implement it as reusable functions.

- **`nearest_index(axis, value)`**: A nearest-neighbor search that ensures mutual conversion between unit systems (Astropy Units).
- **`select_value(data, mode)`**: Extract `real`, `abs`, `power`, etc., from complex data.
- **Location**: `gwexpy/plot/utils.py` or `_coord.py`. This prevents the data type classes (Types layer) from directly depending on plotting libraries (such as Matplotlib).

## 2. Extraction API Layer

Add methods to data type classes that generate "subsets" for visualization.

- **`extract_points` / `slice_map2d`**: Returns data formatted for immediate use in drawing.
- **Convention**: Maintain the original class (e.g., Field4D) where possible, or return standard `TimeSeries`/`FrequencySeries`.

## 3. Plotting API Layer

Drawing methods called directly by the user.

- **Naming Convention**: `plot_map2d`, `plot_profile`, `plot_timeseries_points`, etc.
- **Spectral Visualization**:
  - `freq_space_map` (Waterfall, etc.) is a 2D map where the time axis is replaced by a frequency axis.
  - When plotting spectral density (PSD), consider using a log scale (`norm=LogNorm` or `set_yscale('log')`) by default.

## Physical Consistency Checklist

- [ ] **Unit Propagation**: Does the unit become `unit^2` in `power` mode? Is `angle` in `rad`?
- [ ] **Coordinate Accuracy**: Do the values of the plotted axis correspond correctly to the physical axis of the original data via `nearest_index`?
- [ ] **Dimensional Maintenance**: Are dimensions unexpectedly lost (Squeeze) through slicing operations, breaking the drawing logic?
- [ ] **Memory Efficiency**: For large-scale data, are unnecessary copies (`copy=True`) avoided?
