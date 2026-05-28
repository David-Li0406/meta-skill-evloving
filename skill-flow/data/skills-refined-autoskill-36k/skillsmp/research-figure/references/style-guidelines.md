# Style Guidelines (Paper Figures)

## Typography
- Use serif fonts: "Times New Roman", "CMU Serif", "DejaVu Serif".
- Use sizes: base 10, axis labels 10-11, title 11, legend 9, ticks 9.
- Disable top and right spines for cleaner framing.

## Color Palettes
- Palette A (balanced): #3C5488, #F39B7F, #00A087, #E64B35, #4DBBD5, #91D1C2
- Palette B (muted):   #2E4057, #F18F01, #99C24D, #9A348E, #5BC0BE, #C1CAD6
- Emphasize the main method with the deepest color; keep baselines softer.

## Lines and Markers
- Default line width: 1.4-1.8; highlight 2.2 for the key method.
- Marker size: 5; highlight 7; white marker edge helps visibility.

## Bars
- Use white bar edges, linewidth 0.5.
- Use hatch or slight color shift to show ablations.

## Layout
- Use y-grid with dashed lines, alpha 0.35-0.4; keep grid behind data.
- Prefer 3.0 in height for single-row plots; 6.4-7.0 in width for two-column layouts.
- Call `tight_layout()` and `bbox_inches="tight"` on save.
