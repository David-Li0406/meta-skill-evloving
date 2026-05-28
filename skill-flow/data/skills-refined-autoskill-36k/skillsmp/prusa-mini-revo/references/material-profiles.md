# Material Profiles for Prusa Mini+ / Revo Micro / ObXidian Nozzles

Comprehensive profiles based on **official E3D Filament Starter Settings** for 0.25mm, 0.4mm, 0.6mm, and 0.8mm ObXidian nozzles.

---

## E3D Temperature Reference

| Material | Hotend | Bed | Cooling |
|----------|--------|-----|---------|
| PLA | 200°C | 50-60°C | 100% |
| PETG | 240°C | 70-85°C | 30-50% |
| ASA | 240°C | 90-100°C | 10-30% |
| ABS | 245°C | 95-110°C | 0-20% |
| TPU 92A | 230°C | 40-60°C | 50% |
| TPU 85A | 260°C | 40-60°C | 50% |
| TPU 75A | 260°C | 40-60°C | 50% |
| PETG-CF | 250°C | 75-90°C | 30-50% |
| Nylon-CF | 270°C | 70-90°C | 20-40% |

---

## PLA - 200°C

The easiest material to print. Universal compatibility with all nozzle sizes.

### E3D Starter Settings

| Nozzle | Profile | Layer | Wall | Infill |
|--------|---------|-------|------|--------|
| **0.25mm** | Fine | 0.06mm | 15 | 30 |
| | Medium | 0.125mm | 25 | 50 |
| | Coarse | 0.18mm | 30 | 60 |
| **0.40mm** | Fine | 0.10mm | 15 | 30 |
| | Medium | 0.20mm | 25 | 50 |
| | Coarse | 0.30mm | 30 | 60 |
| **0.60mm** | Fine | 0.15mm | 15 | 30 |
| | Medium | 0.30mm | 25 | 50 |
| | Coarse | 0.45mm | 30 | 60 |
| **0.80mm** | Fine | 0.20mm | 15 | 30 |
| | Medium | 0.40mm | 25 | 50 |
| | Coarse | 0.60mm | 30 | 60 |

### Retraction (Bowden)
| Nozzle | Length | Speed |
|--------|--------|-------|
| 0.25mm | 3.0mm | 35 mm/s |
| 0.40mm | 3.5mm | 35 mm/s |
| 0.60mm | 4.0mm | 35 mm/s |
| 0.80mm | 4.5mm | 35 mm/s |

### PLA Notes
- **Bed adhesion**: Textured PEI works great, no adhesive needed
- **First layer**: 0.2mm height, +5°C temp boost
- **Cooling**: 100% after first layer
- **Stringing**: Rare with proper retraction
- Works well with all nozzle sizes

---

## PETG - 240°C

Strong, flexible, and heat-resistant. Requires careful retraction tuning.

### E3D Starter Settings

| Nozzle | Profile | Layer | Wall | Infill |
|--------|---------|-------|------|--------|
| **0.25mm** | Fine | 0.06mm | 15 | 30 |
| | Medium | 0.125mm | 25 | 50 |
| | Coarse | 0.18mm | 30 | 60 |
| **0.40mm** | Fine | 0.10mm | 15 | 30 |
| | Medium | 0.20mm | 25 | 50 |
| | Coarse | 0.30mm | 30 | 60 |
| **0.60mm** | Fine | 0.15mm | 15 | 30 |
| | Medium | 0.30mm | 25 | 50 |
| | Coarse | 0.45mm | 30 | 60 |
| **0.80mm** | Fine | 0.20mm | 15 | 30 |
| | Medium | 0.40mm | 25 | 50 |
| | Coarse | 0.60mm | 30 | 60 |

### Retraction (Bowden) - Increased for PETG
| Nozzle | Length | Speed |
|--------|--------|-------|
| 0.25mm | 3.5mm | 35 mm/s |
| 0.40mm | 4.0mm | 35 mm/s |
| 0.60mm | 4.5mm | 35 mm/s |
| 0.80mm | 5.0mm | 35 mm/s |

### PETG Notes
- **Bed**: 70-85°C, smooth PEI or glass with glue stick
- **Cooling**: 30-50% (too much = poor layer adhesion)
- **Stringing**: Common issue
  - Enable "Wipe while retracting"
  - High travel speed (150+ mm/s)
  - Try 235°C if stringing persists
- **First layer**: Slightly higher Z offset than PLA
- **Removal**: Can bond too well—use release agent

---

## ASA - 240°C

UV-resistant alternative to ABS. Excellent for outdoor parts.

### E3D Starter Settings

| Nozzle | Profile | Layer | Wall | Infill |
|--------|---------|-------|------|--------|
| **0.25mm** | Fine | 0.06mm | 15 | 30 |
| | Medium | 0.125mm | 25 | 50 |
| | Coarse | 0.18mm | 30 | 60 |
| **0.40mm** | Fine | 0.10mm | 15 | 30 |
| | Medium | 0.20mm | 25 | 50 |
| | Coarse | 0.30mm | 30 | 60 |
| **0.60mm** | Fine | 0.15mm | 15 | 30 |
| | Medium | 0.30mm | 25 | 50 |
| | Coarse | 0.45mm | 30 | 60 |
| **0.80mm** | Fine | 0.20mm | 15 | 30 |
| | Medium | 0.40mm | 25 | 50 |
| | Coarse | 0.60mm | 30 | 60 |

### ASA Notes
- **Bed**: 90-100°C
- **Cooling**: 10-30% (less is better)
- **Enclosure**: Strongly recommended
- **Warping**: Use brim for large parts
- E3D notes: ASA works best even with 0.25mm nozzles

---

## ABS - 245°C

Traditional engineering plastic. Requires controlled environment.

Use ASA settings with these adjustments:
- **Hotend**: 245°C (+5°C over ASA)
- **Bed**: 95-110°C
- **Cooling**: 0-20% (minimal)
- **Enclosure**: Required

### ABS Notes
- More prone to warping than ASA
- Produces fumes—ventilate or filter
- Pre-heat enclosure 10+ minutes
- Use brim or raft for bed adhesion
- E3D notes: ABS works best even with 0.25mm nozzles

---

## TPU 92A - 230°C

Standard flexible filament. Shore 92A hardness.

### E3D Starter Settings

| Nozzle | Profile | Layer | Wall | Infill |
|--------|---------|-------|------|--------|
| **0.25mm** | Fine | 0.06mm | 15 | 30 |
| | Medium | 0.125mm | 25 | 50 |
| | Coarse | 0.18mm | 30 | 60 |
| **0.40mm** | Fine | 0.10mm | 15 | 30 |
| | Medium | 0.20mm | 30 | 60 |
| | Coarse | 0.30mm | 40 | 80 |
| **0.60mm** | Fine | 0.15mm | 15 | 30 |
| | Medium | 0.30mm | 25 | 50 |
| | Coarse | 0.45mm | 30 | 60 |
| **0.80mm** | Fine | 0.20mm | 15 | 30 |
| | Medium | 0.40mm | 25 | 50 |
| | Coarse | 0.60mm | 30 | 60 |

### TPU 92A Notes
- **Retraction**: Disable or use 0.5mm max
- **Linear Advance**: Disable
- **Acceleration**: Reduce to 500 mm/s²
- **Bowden**: Will work but expect challenges
- **First layer**: Very slow (10-15 mm/s)

---

## TPU 85A / 75A - 260°C

Softer flexible filaments. Challenging on bowden systems.

Same layer heights as TPU 92A, but:
- **Temperature**: 260°C (higher for softer TPU)
- **Speed**: Use Fine profile speeds for all
- ⚠️ **Bowden warning**: Very difficult with soft TPU
  - Direct drive (Hemera) recommended by E3D
  - Expect jams and inconsistent extrusion
  - If attempting: disable retraction entirely

---

## PETG Carbon Fiber (XT-CF) - 250°C

Stiff, strong composite. **Use 0.4mm or larger nozzle only.**

### E3D Starter Settings

| Nozzle | Profile | Layer | Wall | Infill |
|--------|---------|-------|------|--------|
| **0.40mm** | Fine | 0.10mm | 15 | 30 |
| | Medium | 0.20mm | 25 | 50 |
| | Coarse | 0.30mm | 30 | 60 |
| **0.60mm** | Fine | 0.15mm | 15 | 30 |
| | Medium | 0.30mm | 25 | 50 |
| | Coarse | 0.45mm | 30 | 60 |
| **0.80mm** | Fine | 0.20mm | 15 | 30 |
| | Medium | 0.40mm | 25 | 50 |
| | Coarse | 0.60mm | 30 | 60 |

### PETG-CF Notes
- ❌ **Avoid 0.25mm** - Fiber particles cause clogs
- **0.8mm recommended** - Lowest clog risk
- **Bed**: 75-90°C
- **Cooling**: 30-50%
- **ObXidian advantage**: Wear-resistant tip handles CF
- **Layer adhesion**: Reduced vs plain PETG

---

## Nylon Carbon Fiber - 270°C

High-strength engineering composite. **Use 0.4mm or larger nozzle only.**

### E3D Starter Settings

| Nozzle | Profile | Layer | Wall | Infill |
|--------|---------|-------|------|--------|
| **0.40mm** | Fine | 0.10mm | 15 | 30 |
| | Medium | 0.20mm | 30 | 60 |
| | Coarse | 0.30mm | 40 | 80 |
| **0.60mm** | Fine | 0.15mm | 15 | 30 |
| | Medium | 0.30mm | 30 | 60 |
| | Coarse | 0.45mm | 40 | 80 |
| **0.80mm** | Fine | 0.20mm | 15 | 30 |
| | Medium | 0.40mm | 30 | 60 |
| | Coarse | 0.60mm | 40 | 80 |

### Nylon-CF Notes
- ❌ **Avoid 0.25mm** - Guaranteed clogs
- **Dry thoroughly** - Nylon is extremely hygroscopic
- Use drybox during printing
- **Bed**: 70-90°C with Garolite/G10 or glue stick
- **Enclosure**: Recommended
- **40W HeaterCore**: May struggle at high flow with 0.8mm

---

## Additional Materials (Not in E3D Starter Guide)

### Plain Nylon (PA) - 260-270°C

| Nozzle | Profile | Layer | Wall | Infill |
|--------|---------|-------|------|--------|
| 0.40mm | Medium | 0.20mm | 25 | 50 |
| 0.60mm | Medium | 0.30mm | 25 | 50 |
| 0.80mm | Medium | 0.40mm | 25 | 50 |

- **Bed**: 70-80°C
- **Dry filament** before every print
- **Enclosure**: Highly recommended

### Wood-Filled PLA - 200°C

⚠️ **Use 0.6mm or 0.8mm only**

| Nozzle | Profile | Layer | Wall | Infill |
|--------|---------|-------|------|--------|
| 0.60mm | Medium | 0.30mm | 25 | 50 |
| 0.80mm | Medium | 0.40mm | 30 | 60 |

- Wood particles clog small nozzles
- Temperature affects color (higher = darker)
- Don't leave hot in nozzle—clogs quickly

### Glow-in-the-Dark PLA - 200°C

⚠️ **Very abrasive** - Strontium aluminate particles

| Nozzle | Profile | Layer | Wall | Infill |
|--------|---------|-------|------|--------|
| 0.40mm | Medium | 0.20mm | 20 | 40 |
| 0.60mm | Medium | 0.30mm | 25 | 50 |
| 0.80mm | Medium | 0.40mm | 30 | 60 |

- **0.8mm best** for production runs
- Print slowly to reduce wear
- ObXidian handles it well

---

## Material/Nozzle Compatibility Matrix

| Material | 0.25mm | 0.4mm | 0.6mm | 0.8mm |
|----------|--------|-------|-------|-------|
| PLA | ✅ | ✅ | ✅ | ✅ |
| PETG | ✅ | ✅ | ✅ | ✅ |
| ASA | ✅ Best | ✅ | ✅ | ✅ |
| ABS | ✅ Best | ✅ | ✅ | ✅ |
| TPU 92A | ⚠️ | ✅ | ✅ | ✅ |
| TPU 85A/75A | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| PETG-CF | ❌ | ✅ | ✅ | ✅ Best |
| Nylon-CF | ❌ | ✅ | ✅ | ✅ Best |
| Wood | ❌ | ❌ | ✅ | ✅ Best |
| Glow | ⚠️ Slow | ✅ | ✅ | ✅ Best |

Legend: ✅ Recommended | ⚠️ Caution | ❌ Avoid

---

## First Layer Settings

| Nozzle | Height | Width | Speed | Temp Boost |
|--------|--------|-------|-------|------------|
| 0.25mm | 0.20mm | 0.30mm | 10 mm/s | +5°C |
| 0.40mm | 0.20mm | 0.45mm | 15 mm/s | +5°C |
| 0.60mm | 0.20mm | 0.70mm | 15 mm/s | +5°C |
| 0.80mm | 0.25mm | 0.90mm | 12 mm/s | +5°C |

---

## Retraction Quick Reference

| Nozzle | PLA | PETG | ABS/ASA | TPU |
|--------|-----|------|---------|-----|
| 0.25mm | 3.0mm | 3.5mm | 3.0mm | 0.5mm |
| 0.40mm | 3.5mm | 4.0mm | 3.5mm | 0.5mm |
| 0.60mm | 4.0mm | 4.5mm | 4.0mm | 0.5mm |
| 0.80mm | 4.5mm | 5.0mm | 4.5mm | 0.5mm |

Speed: 35 mm/s for all (except TPU: 20 mm/s)
