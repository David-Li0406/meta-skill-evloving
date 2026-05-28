# Figures and Tables Reference

## Contents
1. [When to Use Which](#when-to-use-which)
2. [Figure Design](#figure-design)
3. [Table Design](#table-design)
4. [Captions and Legends](#captions-and-legends)
5. [Common Figure Types](#common-figure-types)
6. [Statistical Presentation](#statistical-presentation)

---

## When to Use Which

| Use Tables When | Use Figures When |
|-----------------|------------------|
| Exact values matter | Trends/patterns matter |
| Many variables to compare | Relationships to visualize |
| Precise numbers needed | Quick comprehension desired |
| Text would be repetitive | Data distribution shown |

**General rule**: ~1 table or figure per 1,000 words of text.

**Never duplicate**: Information should appear in text, table, OR figure—not multiple.

---

## Figure Design

### Principles
1. **Self-explanatory**: Reader understands without text
2. **Clean**: Remove chartjunk, unnecessary gridlines, 3D effects
3. **Accessible**: Colorblind-friendly, sufficient contrast
4. **Publication-ready**: 300+ DPI, appropriate file format

### Essential Elements
- Clear title in caption (not on figure)
- Labeled axes with units
- Legend if multiple groups/conditions
- Error bars with definition (SD, SEM, 95% CI)
- Sample sizes (n)
- Statistical annotations (* p<0.05, ** p<0.01, *** p<0.001)
- Scale bars for images

### Color Guidelines
- Use colorblind-friendly palettes (viridis, ColorBrewer)
- Distinguish by pattern/shape in addition to color
- Ensure grayscale readability
- Consistent colors across all figures

### Technical Specifications

| Format | Use Case | Resolution |
|--------|----------|------------|
| TIFF | Print publication | 300-600 DPI |
| EPS/PDF | Vector graphics | Scalable |
| PNG | Web/screen | 150+ DPI |
| JPEG | Photos only | 300 DPI |

**Typical dimensions**: Single column (8.5 cm), double column (17.5 cm)

---

## Table Design

### Principles
1. **Organized**: Logical row/column arrangement
2. **Sparse**: Minimal lines (top, bottom, header only)
3. **Aligned**: Decimal alignment for numbers
4. **Complete**: All abbreviations defined in footnotes

### Essential Elements
- Descriptive title above table
- Clear column headers with units
- Consistent decimal places
- Sample sizes per group
- Statistical test results
- Footnotes for abbreviations and symbols

### Structure
```
Table 1. Baseline characteristics of study participants

Characteristic        Intervention (n=50)    Control (n=50)    p-value
─────────────────────────────────────────────────────────────────────
Age, years            45.2 ± 12.3           44.8 ± 11.9        0.87
Female, n (%)         28 (56)               25 (50)            0.55
BMI, kg/m²            27.4 ± 4.2            28.1 ± 3.9         0.38
─────────────────────────────────────────────────────────────────────
Values are mean ± SD unless otherwise indicated.
BMI, body mass index.
```

### Common Table Types
1. **Baseline/demographics**: Participant characteristics by group
2. **Results summary**: Primary/secondary outcomes
3. **Comparison**: Multiple studies or methods
4. **Model results**: Regression coefficients, odds ratios

---

## Captions and Legends

### Figure Captions

**Format**: Figure [number]. [Title]. [Methods/details]. [Abbreviations].

**Example**:
```
Figure 2. Effect of treatment on cognitive scores over time. Mean Mini-Mental 
State Examination (MMSE) scores at baseline, 3 months, and 6 months for 
intervention (n=50) and control (n=50) groups. Error bars represent 95% 
confidence intervals. *p<0.05, **p<0.01 vs. control at same timepoint.
```

### Table Titles

**Format**: Table [number]. [Descriptive title]

**Example**:
```
Table 3. Predictors of treatment response in multivariable logistic regression
```

### Caption Checklist
- [ ] Describes what is shown
- [ ] Includes sample sizes
- [ ] Defines error bars/statistical measures
- [ ] Explains symbols and abbreviations
- [ ] States statistical tests used
- [ ] Readable without main text

---

## Common Figure Types

### Bar Graphs
- Use for comparing discrete categories
- Include individual data points when n<30
- Error bars: typically SEM or 95% CI
- Baseline at zero (don't truncate y-axis)

### Line Graphs
- Use for continuous data over time
- Connect only related data points
- Include error bars at each timepoint
- Distinguish groups by line style AND symbol

### Scatter Plots
- Use for correlations/relationships
- Include regression line with equation and R²
- Show confidence bands if appropriate
- Consider density plots for large n

### Box Plots
- Use for distributions and comparisons
- Show: median, IQR, whiskers, outliers
- Define whisker convention (1.5×IQR, range, etc.)
- Overlay individual points when feasible

### Heatmaps
- Use for matrices, gene expression, correlations
- Include color scale with units
- Cluster rows/columns if meaningful
- Ensure color scale is intuitive

### Forest Plots
- Use for meta-analyses, subgroup analyses
- Show: effect estimate, CI, weight
- Include overall effect with diamond
- Order by effect size or predefined grouping

---

## Statistical Presentation

### Descriptive Statistics
| Data Type | Report |
|-----------|--------|
| Normal continuous | Mean ± SD |
| Non-normal continuous | Median (IQR) or Median [range] |
| Categorical | n (%) |

### Inferential Statistics
Always report: test statistic, degrees of freedom, p-value, effect size

```
t(48) = 2.31, p = .025, d = 0.67
F(2, 147) = 4.56, p = .012, η² = 0.06
χ²(2) = 8.92, p = .012, V = 0.21
r = .45, p < .001
OR = 2.3, 95% CI [1.4, 3.8]
```

### P-value Conventions
- Report exact values: p = .034, not p < .05
- For very small: p < .001
- Never p = .000

### Effect Size Interpretation (Cohen's conventions)
| Measure | Small | Medium | Large |
|---------|-------|--------|-------|
| d | 0.2 | 0.5 | 0.8 |
| r | 0.1 | 0.3 | 0.5 |
| η² | 0.01 | 0.06 | 0.14 |

---

## Quality Checklist

### Figures
- [ ] High resolution (300+ DPI)
- [ ] Axes labeled with units
- [ ] Legend included and clear
- [ ] Error bars defined
- [ ] Colorblind accessible
- [ ] Caption complete and standalone

### Tables
- [ ] Title descriptive
- [ ] Headers clear with units
- [ ] Decimal places consistent
- [ ] Abbreviations defined
- [ ] Sample sizes included
- [ ] Statistical results complete
