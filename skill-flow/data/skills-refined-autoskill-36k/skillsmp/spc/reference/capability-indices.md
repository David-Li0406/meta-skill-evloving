# Process Capability Indices Reference

## Overview of Indices

| Index | Full Name | Measures | Considers Centering? |
|-------|-----------|----------|---------------------|
| Cp | Process Capability | Spread vs. tolerance | No |
| Cpk | Process Capability Index | Actual capability | Yes |
| Pp | Process Performance | Overall spread vs. tolerance | No |
| Ppk | Process Performance Index | Overall performance | Yes |
| Cpm | Taguchi Capability | Deviation from target | Yes |

---

## Cp - Process Capability

### Definition
Measures the process spread relative to the specification width. Assumes process is centered.

### Formula
```
Cp = (USL - LSL) / 6σ

Where:
σ = process standard deviation (within-subgroup estimate)
σ = R̄/d₂ (from control chart) or S̄/c₄
```

### Interpretation

| Cp | Meaning | Notes |
|----|---------|-------|
| <1.0 | Spread exceeds tolerance | Not capable, even if centered |
| 1.0 | Spread equals tolerance | Barely capable if centered |
| 1.33 | Spread is 75% of tolerance | Minimum automotive standard |
| 1.67 | Spread is 60% of tolerance | Preferred for critical |
| 2.0 | Spread is 50% of tolerance | Excellent |

### Limitation
Cp assumes the process is centered. A Cp of 2.0 is meaningless if the process is off-center.

---

## Cpk - Process Capability Index

### Definition
Measures actual capability considering both spread and centering. Most commonly used index.

### Formula
```
Cpu = (USL - X̄) / 3σ    (Upper capability)
Cpl = (X̄ - LSL) / 3σ    (Lower capability)
Cpk = Min(Cpu, Cpl)
```

### Alternative Formula
```
Cpk = Cp × (1 - k)

Where k = |Target - X̄| / (Tolerance/2)
k represents how far off-center the process is
```

### Interpretation

| Cpk | Est. PPM | Sigma Level | Interpretation |
|-----|----------|-------------|----------------|
| 0.33 | 317,400 | 1σ | Very poor |
| 0.50 | 133,600 | 1.5σ | Poor |
| 0.67 | 45,500 | 2σ | Poor |
| 1.00 | 2,700 | 3σ | Barely capable |
| 1.33 | 66 | 4σ | Capable (minimum auto) |
| 1.50 | 6.8 | 4.5σ | Good |
| 1.67 | 0.6 | 5σ | Very good (CC target) |
| 2.00 | 0.002 | 6σ | Excellent |

### Relationship to Cp
- If process is perfectly centered: Cpk = Cp
- If process is off-center: Cpk < Cp
- The difference (Cp - Cpk) indicates centering opportunity

---

## Pp - Process Performance

### Definition
Similar to Cp but uses overall standard deviation instead of within-subgroup estimate.

### Formula
```
Pp = (USL - LSL) / 6s

Where:
s = overall sample standard deviation
s = √[Σ(xi - X̄)² / (n-1)]
```

### When to Use
- Initial capability assessment
- When process may not be in statistical control
- Long-term performance assessment
- Includes both common and special cause variation

---

## Ppk - Process Performance Index

### Definition
Similar to Cpk but uses overall standard deviation.

### Formula
```
Ppu = (USL - X̄) / 3s
Ppl = (X̄ - LSL) / 3s
Ppk = Min(Ppu, Ppl)
```

### When to Use
- Initial process assessment
- PPAP submissions (may be customer-specified)
- Long-term performance tracking
- When process not in statistical control

---

## Cp/Cpk vs Pp/Ppk Comparison

| Aspect | Cp/Cpk | Pp/Ppk |
|--------|--------|--------|
| Variation estimate | Within-subgroup (R̄/d₂ or S̄/c₄) | Overall (sample s) |
| Represents | Process potential | Actual performance |
| Includes | Common cause only | Common + special cause |
| Typically | Higher value | Lower value |
| Requires | Statistical control | No requirement |
| Use for | Predicting future capability | Describing past performance |

### Relationship
If process is in control: Pp ≈ Cp and Ppk ≈ Cpk

If Pp/Ppk << Cp/Cpk: Special causes present (process not in control)

---

## Cpm - Taguchi Capability Index

### Definition
Considers deviation from target, not just specification limits.

### Formula
```
Cpm = (USL - LSL) / 6τ

Where:
τ = √[σ² + (X̄ - Target)²]
```

### When to Use
- When being on target is critical
- Taguchi loss function philosophy
- Customer values target, not just within spec

### Interpretation
- Cpm penalizes deviation from target
- Process exactly on target: Cpm = Cp
- Process off target: Cpm < Cp

---

## One-Sided Specifications

### Upper Specification Only (USL only)
```
Cpu = (USL - X̄) / 3σ
Cpk = Cpu

Examples: Maximum runout, maximum surface finish
```

### Lower Specification Only (LSL only)
```
Cpl = (X̄ - LSL) / 3σ
Cpk = Cpl

Examples: Minimum hardness, minimum strength
```

---

## Industry Standards

### Automotive (IATF 16949)

| Phase | Index | Minimum |
|-------|-------|---------|
| PPAP (initial) | Ppk | 1.67 |
| Production (ongoing) | Cpk | 1.33 |
| Critical characteristics | Cpk | 1.67 |

### Other Common Standards

| Industry | Standard Cpk |
|----------|--------------|
| General manufacturing | ≥1.00 |
| Precision manufacturing | ≥1.33 |
| Aerospace | ≥1.33 to ≥1.67 |
| Medical devices | ≥1.33 (often higher) |
| Six Sigma target | ≥2.00 |

---

## Capability and Defect Levels

| Cpk | Z-score | PPM (one side) | PPM (both sides) | Sigma Level |
|-----|---------|----------------|------------------|-------------|
| 0.33 | 1.0 | 158,655 | 317,310 | 1σ |
| 0.50 | 1.5 | 66,807 | 133,614 | 1.5σ |
| 0.67 | 2.0 | 22,750 | 45,500 | 2σ |
| 0.83 | 2.5 | 6,210 | 12,419 | 2.5σ |
| 1.00 | 3.0 | 1,350 | 2,700 | 3σ |
| 1.17 | 3.5 | 233 | 465 | 3.5σ |
| 1.33 | 4.0 | 32 | 63 | 4σ |
| 1.50 | 4.5 | 3.4 | 6.8 | 4.5σ |
| 1.67 | 5.0 | 0.29 | 0.57 | 5σ |
| 2.00 | 6.0 | 0.001 | 0.002 | 6σ |

---

## Common Scenarios

### High Cp, Low Cpk
- Process spread is good
- Process is off-center
- **Action:** Center the process (easy improvement)

### Low Cp, Low Cpk
- Process spread is too wide
- May also be off-center
- **Action:** Reduce variation first, then center

### Cp = Cpk
- Process is centered
- Variation may or may not be acceptable
- **Action:** If not capable, must reduce variation

### Ppk < Cpk
- Special causes present
- Process not in statistical control
- **Action:** Bring to control first, then assess true capability

---

## Calculation Examples

### Example 1: Standard Bilateral Tolerance

Specification: 25.00 ± 0.10 mm
Data: X̄ = 25.02, σ = 0.025

```
USL = 25.10, LSL = 24.90, Target = 25.00

Cp = (25.10 - 24.90) / (6 × 0.025) = 0.20 / 0.15 = 1.33

Cpu = (25.10 - 25.02) / (3 × 0.025) = 0.08 / 0.075 = 1.07
Cpl = (25.02 - 24.90) / (3 × 0.025) = 0.12 / 0.075 = 1.60
Cpk = Min(1.07, 1.60) = 1.07
```

**Interpretation:** Cp = 1.33 (capable spread), Cpk = 1.07 (off-center)
**Action:** Center process to improve Cpk

### Example 2: One-Sided Specification

Specification: Runout ≤ 0.05 mm (USL only)
Data: X̄ = 0.02, σ = 0.008

```
Cpu = (0.05 - 0.02) / (3 × 0.008) = 0.03 / 0.024 = 1.25
Cpk = 1.25
```

**Interpretation:** Cpk = 1.25, slightly below 1.33 target.
