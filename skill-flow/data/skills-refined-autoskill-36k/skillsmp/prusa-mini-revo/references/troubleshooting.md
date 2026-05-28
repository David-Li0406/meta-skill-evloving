# Troubleshooting Guide: Prusa Mini+ / Revo Micro / ObXidian

Diagnostic guide for common print issues with 0.25mm, 0.4mm, 0.6mm, and 0.8mm ObXidian nozzles.

---

## Quick Diagnosis Table

| Issue | Most Likely Cause | First Fix |
|-------|-------------------|-----------|
| Clogging | Temp too low / debris | +10°C, cold pull |
| Under-extrusion | Flow too low / partial clog | Check flow, clean nozzle |
| Over-extrusion | Flow too high | Reduce flow 2-5% |
| Stringing | Retraction / temp | More retraction, lower temp |
| First layer fail | Live Z / bed level | Re-calibrate Z |
| Warping | Bed temp / adhesion | Higher bed temp, brim |
| Layer separation | Temp too low / cooling | +5-10°C, reduce cooling |
| Blobs/zits | Pressure / retraction | Tune pressure advance |

---

## Clogging / Partial Clogs

### Symptoms
- Extruder clicking
- Under-extrusion mid-print
- Filament grinding
- No extrusion at all

### Nozzle-Specific Patterns

| Nozzle | Clog Risk | Common Cause |
|--------|-----------|--------------|
| 0.25mm | **High** | Particles, debris, filled filaments |
| 0.40mm | Medium | Contamination, heat creep |
| 0.60mm | Low | Usually heat creep or burnt material |
| 0.80mm | Very Low | Rare—usually burnt material only |

### Solutions

**Immediate fixes:**
1. **Cold pull** - Heat to 250°C, cool to 90°C, pull firmly
2. **Atomic pull** - Repeat cold pull 3-5 times
3. **Nozzle swap** - Revo makes this instant

**Prevention:**
- Keep filament clean (wipe before extruder)
- Use correct temperature (check E3D settings)
- Avoid filled filaments in 0.25mm nozzle
- Store filament dry

### 0.25mm Specific
- ❌ Never use carbon fiber, glass fiber, or glow filaments
- Clean filament path regularly
- Higher clog risk with PLA due to heat creep
- Consider slightly higher temps (+5°C)

---

## Under-Extrusion

### Symptoms
- Gaps in walls
- Weak infill
- Visible layer lines
- Poor layer adhesion

### By Nozzle Size

| Nozzle | Common Cause | Typical Fix |
|--------|--------------|-------------|
| 0.25mm | Partial clog, wrong flow | Cold pull, calibrate flow |
| 0.40mm | E-steps, flow rate | Check flow calibration |
| 0.60mm | Speed too high | Reduce speed or flow limit |
| 0.80mm | Heater can't keep up | Slower speed, check 60W upgrade |

### Solutions

1. **Check volumetric flow** - Don't exceed limits:
   | Nozzle | Max PLA | Max PETG |
   |--------|---------|----------|
   | 0.25mm | 5 mm³/s | 4 mm³/s |
   | 0.40mm | 11 mm³/s | 8 mm³/s |
   | 0.60mm | 15 mm³/s | 11 mm³/s |
   | 0.80mm | 17 mm³/s | 13 mm³/s |

2. **Calibrate flow** - Print single-wall cube, measure:
   | Nozzle | Target Wall |
   |--------|-------------|
   | 0.25mm | 0.25-0.27mm |
   | 0.40mm | 0.40-0.44mm |
   | 0.60mm | 0.60-0.65mm |
   | 0.80mm | 0.80-0.86mm |

3. **Check temperature** - E3D Revo recommendations:
   - PLA: 200°C
   - PETG: 240°C
   - ASA: 240°C
   - TPU: 230°C

---

## Over-Extrusion

### Symptoms
- Bulging walls
- Rough surface
- Blobs on corners
- Elephant foot on first layer

### Solutions

1. **Reduce flow rate** - Start at 95%, adjust by 1%
2. **Check extrusion width** - Should be ~nozzle diameter
3. **First layer** - Reduce first layer flow to 95%
4. **Elephant foot** - Use elephant foot compensation (0.1-0.2mm)

---

## Stringing

### Severity by Nozzle

| Nozzle | Stringing Risk | Notes |
|--------|----------------|-------|
| 0.25mm | Low | Small orifice limits ooze |
| 0.40mm | Medium | Standard, manageable |
| 0.60mm | High | Larger orifice = more ooze |
| 0.80mm | Highest | Most aggressive retraction needed |

### Solutions

**Retraction settings (Bowden):**
| Nozzle | PLA | PETG |
|--------|-----|------|
| 0.25mm | 3.0mm | 3.5mm |
| 0.40mm | 3.5mm | 4.0mm |
| 0.60mm | 4.0mm | 4.5mm |
| 0.80mm | 4.5mm | 5.0mm |

**Additional fixes:**
- Lower temperature 5-10°C
- Enable "Wipe while retracting"
- Increase travel speed (150+ mm/s)
- Enable Z-hop (0.2-0.3mm)
- Coasting 0.02-0.05mm³

**PETG specifically:**
- Use Wipe into Infill
- Reduce temp to 235°C
- Dry filament thoroughly

---

## First Layer Issues

### Symptoms
- Not sticking
- Peeling corners
- Too squished
- Gaps in first layer

### Live Z Calibration per Nozzle

Each nozzle needs separate calibration!

| Nozzle | Typical Live Z Range | First Layer Height |
|--------|---------------------|-------------------|
| 0.25mm | -0.400 to -1.200 | 0.20mm |
| 0.40mm | -0.600 to -1.500 | 0.20mm |
| 0.60mm | -0.800 to -1.700 | 0.20mm |
| 0.80mm | -1.000 to -1.900 | 0.25mm |

### Diagnostic: First Layer Appearance

| Appearance | Problem | Fix |
|------------|---------|-----|
| Gaps between lines | Z too high | Lower Live Z |
| Transparent/thin | Z too low | Raise Live Z |
| Rough/scraped | Z way too low | Raise Live Z significantly |
| Perfect squish | Correct | Document this value! |

### Bed Adhesion by Material

| Material | Bed Temp | Surface | Adhesive |
|----------|----------|---------|----------|
| PLA | 60°C | Textured PEI | None |
| PETG | 85°C | Smooth PEI | Glue stick |
| ABS/ASA | 100°C | Smooth PEI | Glue stick |
| TPU | 50°C | Smooth PEI | None |
| Nylon | 80°C | Garolite/G10 | Glue stick |

---

## Surface Quality Issues

### Rough/Bumpy Surface

| Cause | Fix |
|-------|-----|
| Over-extrusion | Reduce flow 2-5% |
| Temp too high | Lower by 5-10°C |
| Speed too fast | Slow down walls |
| Wet filament | Dry filament |

### Layer Lines Visible

More visible with larger nozzles:
| Nozzle | Visibility | Mitigation |
|--------|------------|------------|
| 0.25mm | Minimal | N/A |
| 0.40mm | Low | Normal |
| 0.60mm | Moderate | Lower layer height |
| 0.80mm | High | Accept or use 0.3mm layers |

### Ringing/Ghosting

- Reduce acceleration (500-1000 mm/s²)
- Reduce jerk (8-10 mm/s)
- Tighten belts
- Check for loose parts

---

## Dimensional Accuracy

### Calibration Steps

1. **E-steps** - Extrude 100mm, measure
2. **Flow rate** - Single wall cube
3. **XY compensation** - Shrinkage adjustment

### Typical Adjustments by Nozzle

| Nozzle | XY Compensation | Notes |
|--------|-----------------|-------|
| 0.25mm | -0.02 to 0mm | Most accurate |
| 0.40mm | -0.02 to -0.05mm | Standard |
| 0.60mm | -0.05 to -0.10mm | Check hole sizes |
| 0.80mm | -0.10 to -0.15mm | Least accurate |

### Hole Compensation

Holes print smaller than designed:
| Nozzle | Add to Hole Diameter |
|--------|---------------------|
| 0.25mm | +0.1mm |
| 0.40mm | +0.2mm |
| 0.60mm | +0.3mm |
| 0.80mm | +0.4mm |

---

## Overhang & Bridging

### Maximum Overhang by Nozzle

| Nozzle | Max Overhang (no support) | Bridging |
|--------|--------------------------|----------|
| 0.25mm | 60° | Excellent |
| 0.40mm | 55° | Good |
| 0.60mm | 50° | Moderate |
| 0.80mm | 45° | Poor |

### Improving Overhangs

1. **Reduce layer height** - Better overhang with thinner layers
2. **Increase cooling** - 100% for PLA overhangs
3. **Reduce speed** - Slow down for overhangs
4. **Lower temp** - Less sag with cooler filament

### Improving Bridges

- **Bridge flow**: 90-95%
- **Bridge speed**: 20-25 mm/s
- **Cooling**: 100% during bridges
- **Fan delay**: Ensure fan is at full before bridge

---

## Revo-Specific Issues

### HeaterCore Problems

**Thermal runaway errors:**
- Check thermistor resistance (~100kΩ at room temp)
- Verify wiring connections
- Check for damaged wires

**Inconsistent temperature:**
- Ensure HeaterCore is fully seated
- Check for drafts on hotend
- Verify PID tuning

### Nozzle Issues

**Won't thread:**
- Cool down completely
- Check for cross-threading
- Clean threads with brass brush

**Leaking at nozzle:**
- Revo shouldn't leak if finger-tight
- If leaking: replace nozzle (seal may be damaged)

**E3DLC coating peeling:**
- Normal after extended use
- Doesn't affect print quality
- Replace when tip shows significant wear

---

## Bowden-Specific Issues

### Filament Grinding

**Causes:**
- Excessive retraction
- Partial clog
- Too much extruder tension
- Wrong temperature

**Fixes:**
- Reduce retraction length
- Cold pull to clear clog
- Loosen extruder tension
- Increase temperature

### Inconsistent Extrusion

**Causes:**
- PTFE tube not seated
- Loose bowden fittings
- Worn PTFE tube

**Fixes:**
- Re-seat PTFE tube firmly
- Replace bowden clips
- Replace PTFE tube (especially at hotend end)

### TPU Issues (Bowden-Specific)

⚠️ Bowden systems struggle with flexible filaments

- Use TPU 92A or stiffer (not 85A/75A)
- Disable retraction entirely
- Print very slowly (15-20 mm/s)
- Reduce acceleration
- E3D recommends direct drive (Hemera) for soft TPU

---

## Print Time Comparison

Approximate times for 20mm calibration cube:

| Nozzle | Fine | Medium | Coarse |
|--------|------|--------|--------|
| 0.25mm | 45 min | 25 min | 18 min |
| 0.40mm | 30 min | 15 min | 10 min |
| 0.60mm | 20 min | 10 min | 7 min |
| 0.80mm | 15 min | 8 min | 5 min |

Use larger nozzles for faster prototyping!

---

## Emergency Procedures

### Complete Blockage
1. Heat to 250°C
2. Remove bowden tube
3. Push filament through with cleaning filament
4. If still blocked: swap nozzle (Revo is instant)

### Thermal Runaway
1. Power off printer immediately
2. Check all wiring connections
3. Measure thermistor resistance
4. Replace HeaterCore if faulty

### Extruder Jam
1. Release extruder tension completely
2. Heat hotend
3. Try to manually push/pull filament
4. If stuck: remove from extruder, cut, re-load

---

## Calibration Checklist

Run these calibrations when:
- Changing nozzle size
- Changing material type
- After any hardware changes

| Calibration | Frequency | Tool |
|-------------|-----------|------|
| First Layer (Live Z) | Per nozzle | Printer menu |
| Flow Rate | Per material | Single wall cube |
| Retraction | Per material | Retraction tower |
| Temperature | Per filament brand | Temp tower |
| Pressure Advance | Per nozzle/material | PA test pattern |
