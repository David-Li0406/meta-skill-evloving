# Control Methods Reference - MNMUK

## Method Selection by Characteristic Type

### Dimensional Characteristics

| Characteristic | Tolerance Class | Preferred Method | Alternative |
|----------------|-----------------|------------------|-------------|
| Length/Width/Height | ±0.5mm or more | Steel rule, tape | Caliper |
| Length/Width/Height | ±0.1mm to ±0.5mm | Caliper | Height gage |
| Length/Width/Height | ±0.05mm or less | Micrometer, CMM | Gage blocks |
| Diameter (external) | ±0.1mm or more | Caliper | |
| Diameter (external) | ±0.01mm to ±0.1mm | Micrometer | CMM |
| Diameter (external) | <±0.01mm | Air gage, CMM | |
| Diameter (internal) | ±0.1mm or more | Caliper, plug gage | |
| Diameter (internal) | ±0.01mm to ±0.1mm | Bore gage | CMM |
| Diameter (internal) | <±0.01mm | Air gage, CMM | |
| Depth | ±0.1mm or more | Depth micrometer | Caliper depth |
| Depth | <±0.1mm | CMM | Depth micrometer |
| Thread | General | Go/No-go thread gage | Thread micrometer |
| Thread | Pitch diameter | Thread micrometer | |

### Geometric Characteristics

| Characteristic | Tolerance | Preferred Method | Alternative |
|----------------|-----------|------------------|-------------|
| Flatness | ≥0.1mm | Surface plate + indicator | |
| Flatness | <0.1mm | CMM | Optical flat |
| Roundness | ≥0.05mm | V-block + indicator | |
| Roundness | <0.05mm | Roundness tester, CMM | |
| Perpendicularity | ≥0.1mm | Square + indicator | CMM |
| Perpendicularity | <0.1mm | CMM | |
| Position | ≥0.25mm | Height gage, caliper | CMM |
| Position | <0.25mm | CMM | Optical |
| Concentricity | ≥0.05mm | V-block + indicator | |
| Concentricity | <0.05mm | CMM, roundness tester | |
| Runout | All | Indicator on centers/V | CMM |
| Profile | Complex | CMM | Optical comparator |

### Surface Characteristics

| Characteristic | Requirement | Preferred Method | Alternative |
|----------------|-------------|------------------|-------------|
| Surface finish (Ra) | ≥3.2µm | Comparison standard | |
| Surface finish (Ra) | <3.2µm | Profilometer | |
| Visual appearance | General | Visual standard | |
| Visual appearance | Critical | Boundary samples | |
| Coating thickness | All | Coating gage | Cross-section |
| Hardness | All | Hardness tester | Certification |

### Assembly Characteristics

| Characteristic | Type | Preferred Method | Alternative |
|----------------|------|------------------|-------------|
| Torque | Fastener | Torque wrench | Torque analyzer |
| Presence | Component | Poka-yoke sensor | Visual check |
| Orientation | Component | Fixture/vision | Visual check |
| Leak | Seal integrity | Leak tester | Pressure decay |
| Function | Performance | Test stand | Manual test |

---

## Control Method Descriptions

### Variable Measurement Methods

**Caliper (Digital)**
- Range: Typically 0-150mm, 0-300mm
- Resolution: 0.01mm
- Uncertainty: ±0.02mm typical
- Best for: General dimensional checks, medium tolerance
- Gage R&R expectation: <20%

**Micrometer (Outside)**
- Range: 0-25mm, 25-50mm, etc.
- Resolution: 0.001mm
- Uncertainty: ±0.003mm typical
- Best for: Tight tolerance dimensions
- Gage R&R expectation: <10%

**CMM (Coordinate Measuring Machine)**
- Range: Per machine (600x800x500mm typical)
- Resolution: 0.0001mm
- Uncertainty: 2-5µm typical
- Best for: Complex geometry, position, GD&T
- Gage R&R expectation: <10%

**Bore Gage**
- Range: Size-specific
- Resolution: 0.001mm
- Uncertainty: ±0.005mm typical
- Best for: Internal diameters
- Gage R&R expectation: <15%

**Height Gage**
- Range: 0-300mm, 0-600mm typical
- Resolution: 0.01mm
- Uncertainty: ±0.02mm typical
- Best for: Height, depth, step measurements
- Gage R&R expectation: <15%

**Profilometer**
- Range: Per probe
- Resolution: 0.001µm
- Best for: Surface roughness (Ra, Rz)
- Gage R&R expectation: <20%

### Attribute Measurement Methods

**Go/No-Go Plug Gage**
- Go gage: Must pass through
- No-go gage: Must not pass through
- Best for: Hole diameter verification
- MSA: Attribute agreement analysis

**Go/No-Go Ring Gage**
- Go gage: Must pass over
- No-go gage: Must not pass over
- Best for: Shaft diameter verification
- MSA: Attribute agreement analysis

**Thread Gage**
- Go: Must thread fully
- No-go: Must not thread more than 3 turns
- Best for: Thread verification
- MSA: Attribute agreement analysis

**Pin Gage**
- Range: Available in 0.001mm increments
- Best for: Hole size verification, position
- MSA: Attribute agreement analysis

### Visual Inspection Methods

**Visual Standard**
- Documented acceptable appearance
- Photos of acceptable vs. unacceptable
- Lighting conditions specified
- Best for: General appearance
- MSA: Attribute agreement (Kappa)

**Boundary Samples**
- Physical samples at accept/reject boundary
- Maintained under controlled conditions
- Regular replacement/verification
- Best for: Subjective characteristics
- MSA: Attribute agreement (Kappa)

**Optical Comparator**
- Magnified silhouette comparison
- Overlay with tolerance zone
- Best for: Profile, thread form
- Gage R&R: <20%

### Error-Proofing Methods

**Presence Sensor**
- Proximity, photoelectric, vision
- Detects component presence
- Interlocked to process
- Best for: Missing component prevention

**Position Sensor**
- Verifies correct location/orientation
- Interlocked to process
- Best for: Orientation errors

**Fixture Poka-Yoke**
- Part only fits one way
- Prevents wrong orientation
- Best for: Assembly errors

**Count Verification**
- Confirms correct quantity
- Torque gun count, weigh scale
- Best for: Missing fasteners, short counts

---

## Recording Methods

### SPC Charts

**X-bar/R Chart**
- Use: Variable data, subgroups n=2-9
- Control limits: X-bar ± A2*R-bar
- Best for: Process mean and variation

**X-bar/S Chart**
- Use: Variable data, subgroups n≥10
- Best for: Higher volume sampling

**Individual/Moving Range (I-MR)**
- Use: Individual measurements, n=1
- Best for: Low volume, long cycle time

**p Chart**
- Use: Proportion defective
- Best for: Attribute data, varying sample size

**np Chart**
- Use: Count of defectives
- Best for: Attribute data, fixed sample size

**c Chart**
- Use: Count of defects per unit
- Best for: Defects per item (constant area)

**u Chart**
- Use: Defects per unit, varying sample
- Best for: Defects per area (varying area)

### Data Recording

**Check Sheet**
- Simple pass/fail or count
- Operator marks checkbox or tally
- Low overhead
- Best for: Visual checks, presence

**Data Log**
- Actual measurements recorded
- Spreadsheet or form
- Allows trend analysis
- Best for: Traceability, capability

**Electronic/MES**
- Direct data capture
- Automated where possible
- Real-time visibility
- Best for: High volume, integration

**Traveler**
- Travels with part/lot
- Documents history
- Serial number linked
- Best for: Traceability, low volume

---

## Method Selection Decision Tree

```
Start
  │
  ├─ Is characteristic measurable?
  │     │
  │     ├─ YES → Variable measurement
  │     │         │
  │     │         ├─ Tight tolerance (<0.05mm)?
  │     │         │     ├─ YES → CMM, micrometer, air gage
  │     │         │     └─ NO → Caliper, go/no-go
  │     │         │
  │     │         └─ Complex geometry?
  │     │               ├─ YES → CMM
  │     │               └─ NO → Standard gage
  │     │
  │     └─ NO → Attribute check
  │             │
  │             ├─ Can be error-proofed?
  │             │     ├─ YES → Poka-yoke (preferred)
  │             │     └─ NO → Go/no-go or visual
  │             │
  │             └─ Subjective?
  │                   ├─ YES → Boundary samples, visual standard
  │                   └─ NO → Go/no-go gage
  │
  └─ Recording method?
        │
        ├─ SPC required? → Control chart
        ├─ Traceability required? → Data log, traveler
        ├─ High volume? → Electronic/MES
        └─ Simple check? → Check sheet
```

---

## MSA Requirements by Method

| Method Type | MSA Study | Acceptance Criteria |
|-------------|-----------|---------------------|
| Variable (critical) | Gage R&R | <10% |
| Variable (standard) | Gage R&R | <30% |
| Attribute | Attribute Agreement | Kappa >0.75 |
| Visual | Attribute Agreement | Kappa >0.70 |
| Poka-yoke | Effectiveness validation | 100% detection |

---

## Gage Selection Guidelines

1. **10:1 Rule**: Gage resolution should be 1/10 of tolerance
2. **30% Rule**: Gage uncertainty should be <30% of tolerance (ideally <10%)
3. **Appropriate range**: Gage range covers full characteristic range
4. **Ease of use**: Operator can use correctly and consistently
5. **Durability**: Survives production environment
6. **Calibration**: Can be calibrated to traceable standard
