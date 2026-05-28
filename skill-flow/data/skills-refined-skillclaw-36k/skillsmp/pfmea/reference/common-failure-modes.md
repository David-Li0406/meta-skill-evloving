# Common Failure Modes by Department - MNMUK

## Machine Shop

### CNC Turning Operations

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Diameter oversize | Part scrapped, no rework | Tool wear, offset error, thermal expansion | 8 | 3-5 | SPC, first piece, in-process gage |
| Diameter undersize | Assembly interference, scrap | Offset error, program error | 7-8 | 3-5 | SPC, first piece, in-process gage |
| Length out of spec | Assembly issue, stack-up | Z-axis offset, locating error | 6-7 | 4 | First piece check, fixture design |
| Poor surface finish | Customer complaint, function | Tool wear, wrong parameters, chatter | 5-6 | 4-5 | Visual check, profilometer |
| Concentricity OOS | Runout issue, vibration | Chuck pressure, locating, deflection | 6-7 | 4 | Runout check, fixture validation |
| Taper | Assembly issue | Tool deflection, axis alignment | 6 | 3-4 | Multi-point measurement |
| Thread damage | Non-functional, scrap | Tool breakage, wrong pitch, entry | 7-8 | 3-4 | Thread gage, go/no-go |

### CNC Milling Operations

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Position out of tolerance | Assembly failure | Fixture location, program error, thermal | 7-8 | 3-5 | CMM check, fixture validation |
| Hole size incorrect | Fastener won't fit, loose | Tool wear, runout, wrong tool | 6-7 | 3-4 | Pin gage, CMM |
| Missing feature | Part non-functional | Program error, tool breakage, skip | 8-9 | 2-3 | Post-process inspection |
| Burrs | Assembly issue, injury risk | Tool wear, wrong parameters | 4-5 | 5-6 | Visual, deburr operation |
| Wrong surface profile | Fit/function issue | Cutter compensation, tool deflection | 6-7 | 3-4 | CMM, surface check |
| Tool marks/chatter | Cosmetic reject | Tool wear, parameters, rigidity | 5 | 4-5 | Visual inspection |

### Grinding Operations

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Diameter out of spec | Fit failure | Wheel wear, dressing, thermal | 7-8 | 3-4 | In-process gage, SPC |
| Burn/temper damage | Hardness loss, failure | Excessive heat, wrong parameters | 8-9 | 3-4 | Temper etch, hardness test |
| Out of round | Vibration, wear | Wheel balance, workholding | 6-7 | 3-4 | Roundness measurement |
| Surface finish poor | Function, cosmetic | Wheel condition, coolant, speed | 5-6 | 4-5 | Profilometer, visual |
| Taper | Assembly issue | Wheel wear, alignment | 6 | 3-4 | Multi-point measurement |

### EDM Operations

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Overcut (size error) | Fit failure | Electrode wear, offset error | 7-8 | 3-4 | First piece, in-process |
| White layer too thick | Fatigue failure | Parameters, flush | 8 | 4-5 | Cut/etch inspection |
| Surface defects | Function/cosmetic | Arc instability, contamination | 5-6 | 4-5 | Visual, CMM |
| Recast layer cracks | Part failure | Thermal stress, parameters | 8-9 | 3-4 | Metallurgical check |
| Wrong position | Part scrapped | Fixture error, program error | 8 | 2-3 | CMM verification |

---

## Damper Assembly

### Seal Installation

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Seal damaged during install | Leak at customer | Wrong tool, excessive force | 8 | 4-5 | Visual check, leak test |
| Seal missing | Leak, field failure | Operator error, part missing | 9 | 3-4 | Poka-yoke, leak test |
| Seal twisted | Leak, reduced life | Installation method | 7 | 4-5 | Fixture design, visual |
| Wrong seal | Leak, fit issue | Part mix-up, similar appearance | 8 | 3-4 | Barcode scan, visual |
| Seal contaminated | Seal degradation, leak | Oil/debris on seal | 6-7 | 4-5 | Clean handling, visual |

### Fastening Operations

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Under-torque | Joint loosens, leak, failure | Wrong setting, tool error | 8-9 | 3-4 | Torque monitoring, audit |
| Over-torque | Thread strip, crack | Wrong setting, tool malfunction | 7-8 | 3-4 | Torque monitoring |
| Missing fastener | Part separation, failure | Operator skip, part shortage | 9 | 3-4 | Poka-yoke, torque count |
| Wrong fastener | Joint failure | Part mix-up, similar parts | 8 | 3-4 | Barcode, visual, size check |
| Cross-threaded | Thread damage, weak joint | Alignment, technique | 7 | 4-5 | Start torque monitoring |

### Fluid Fill

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Wrong fluid level | Performance issue | Fill equipment, operator | 7-8 | 3-4 | Automated fill, weigh check |
| Wrong fluid type | Performance/failure | Container mix-up | 9 | 2-3 | Barcode verification |
| Air entrainment | Performance issue | Fill method, leak | 6-7 | 4-5 | Vacuum fill, bleed procedure |
| Contamination | Seal damage, wear | Dirty equipment, handling | 7-8 | 4-5 | Cleanliness control, filter |

---

## LVA (Low Volume Assembly)

### Component Installation

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Wrong component | Non-function, field failure | Similar parts, mislabeling | 8-9 | 4-5 | Traveler verification, barcode |
| Missing component | Non-function | Operator skip, shortage | 8-9 | 4-5 | Checklist, final inspection |
| Reversed orientation | Non-function, damage | Symmetric parts, unclear WI | 7-8 | 4-5 | Asymmetric design, visual guide |
| Damaged component | Function issue, scrap | Handling, tools | 6-7 | 4-5 | Protected handling, visual |

### Manual Assembly Steps

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Skipped step | Non-function, safety | Training, distraction | 7-9 | 4-5 | Checklist, sequential work |
| Steps out of sequence | Quality issue | Training, unclear WI | 6-7 | 4-5 | Sequential instructions |
| Wrong tool used | Damage, quality issue | Availability, knowledge | 5-6 | 4-5 | Tool kitting, shadow boards |
| Incorrect technique | Quality issue, damage | Training, ergonomics | 5-7 | 4-5 | Training, work instruction |

---

## FML (Final Manufacturing Line)

### Final Test

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Test not performed | Defect ships | Equipment down, skip | 9-10 | 2-3 | Interlocked test, record check |
| Test pass false positive | Defect ships | Equipment calibration, setup | 9-10 | 2-3 | MSA, daily verification |
| Test fail false negative | Good part scrapped | Equipment calibration | 4 | 3-4 | MSA, verification parts |
| Wrong test program | Wrong characteristics tested | Part mix-up, selection error | 8 | 2-3 | Barcode/part number interlock |

### Labeling/Traceability

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Wrong label | Traceability lost, mix-up | Printer error, operator | 7-8 | 3-4 | Barcode verification |
| Missing label | Traceability lost | Printer/applicator failure | 7 | 3-4 | Presence sensor, visual |
| Label not readable | Scan failure, manual entry | Print quality, damage | 5-6 | 4-5 | Barcode grade verification |
| Wrong data on label | Customer complaint, recall | Data entry, system error | 8 | 3-4 | Scan verification, audit |

### Packaging

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Part damaged in packaging | Customer complaint | Wrong dunnage, handling | 6-7 | 4-5 | Packaging specification, audit |
| Wrong quantity | Customer complaint, line down | Count error, labeling | 6-7 | 4-5 | Weigh count, scan verification |
| Wrong part in package | Customer line issue | Mix-up, labeling error | 8-9 | 3-4 | Final verification, barcode |
| Missing protection | Shipping damage | Procedure not followed | 5-6 | 4-5 | Packaging checklist |

---

## Cross-Departmental Failure Modes

### Material Handling

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Part dropped | Scrap, damage | Handling method, ergonomics | 5-7 | 4-5 | Handling fixtures, training |
| Part mixed with scrap | Defect ships | Identification, container | 8-9 | 3-4 | Red bin, clear segregation |
| FIFO violated | Obsolete part used, traceability | Storage method | 5-6 | 4-5 | FIFO lanes, date marking |
| Wrong material used | Function failure, recall | Similar appearance, labeling | 9 | 2-3 | Material certification, color code |

### Inspection

| Failure Mode | Potential Effects | Typical Causes | Typical S | Typical O | Common Controls |
|--------------|-------------------|----------------|-----------|-----------|-----------------|
| Measurement error | Bad part accepted/good rejected | Technique, gage, training | 7-8 | 4-5 | MSA, training, procedure |
| Wrong gage used | Incorrect data | Gage control, identification | 6-7 | 3-4 | Gage log, calibration sticker |
| Inspection skipped | Defect ships | Time pressure, not scheduled | 8-9 | 3-4 | Process interlock, audit |
| Data not recorded | Traceability lost | Procedure, time pressure | 5-6 | 4-5 | Electronic capture, audit |

---

## Using This Reference

1. **Starting PFMEA**: Review relevant department section for common failure modes
2. **Team brainstorming**: Use as checklist - "Have we considered X?"
3. **New processes**: Adapt similar failure modes to new context
4. **After quality issues**: Verify failure mode is captured in PFMEA
5. **Cross-reference**: Link to actual MNMUK scrap/complaint data when available
