# Technical Architecture

## System Overview

Photometrics AI is a software platform with four integrated components:

```
Target Lighting Layer → Optimization Engine → Dynamic Scheduling → NLC Integration
     (Mapping)            (AI-accelerated)      (Priority calendar)    (API output)
```

---

## Component 1: Target Lighting Layer (TLL)

**Patent:** US9894736B2 (granted 2018)

A GIS-based raster layer specifying desired horizontal illuminance (lux) for every location in a coverage area.

### Default TLL Values (example)

| Zone | Target Lux |
|------|------------|
| Major roads | 11-18 |
| Collector roads | 9-13 |
| Local streets | 7 |
| Cul-de-sacs | 3 |
| Crosswalks | 20 |
| Bike lanes | 20 |
| Municipal parking | 4 |
| Sidewalks | 2 |
| Curb strips | 2 |
| Front yards | 1 (or 0 after midnight) |
| Building footprints | 0 |
| Undeveloped | 0 |

### Dynamic TLL Variations

Different TLLs are created for different conditions:
- **Halloween TLL**: Local roads and cul-de-sacs treated as crosswalks (20 lux)
- **Late Night TLL**: Sidewalks and front yards reduced to 0 lux after midnight
- **Migratory Bird TLL**: Low-speed/low-crime areas dimmed 2AM-sunrise
- **Demand Response TLL**: Strategic dimming in residential areas
- **Event TLLs**: Enhanced lighting around venues before/after events

---

## Component 2: Optimization Engine

**Patent Pending:** 18/660,680

### The Core Problem

Given:
- Multiple luminaires with overlapping beam spreads
- Target illuminance values for every point in the coverage area
- IES photometric files describing each luminaire's light distribution
- Real-world geometry (elevations, road widths, intersection angles, mast arm positions)

Find: The optimal dimming level (0-100%) for each luminaire that best achieves the TLL while minimizing energy.

### How Traditional Design Fails

Traditional "typical layouts" use:
- Cookie-cutter designs (all roads of type X get fixture Y at spacing Z)
- CAD tools built for indoor spaces
- No accounting for real geometry (slopes, irregular intersections, mast arm offsets)
- Arbitrary dimming schedules chosen from vendor presets

Result: Overlighting in some areas, underlighting in others, no coordination between fixtures.

### Photometrics AI Approach

1. **Image Chip Generation**: Cut the coverage area into small chips centered on each luminaire
2. **Multi-scenario Simulation**: Test dimming levels from 10% to 100% in increments
3. **RMSE Matching**: Calculate root mean square error between achieved illuminance and TLL
4. **Optimal Selection**: Choose dimming level that minimizes RMSE while meeting standards

### Human Vision Insight

Human eyes cannot perceive brightness changes under ~20%, especially at night (scotopic vision uses rods, not cones). This allows significant optimization headroom—a light at 72% vs 100% looks identical to observers but saves substantial energy.

---

## Component 3: Training Pipeline (Deep Learning)

### Before Projects: Model Training

```
Define TLL → Simulate Scenarios → Find Best Match (RMSE) → Build Training Data → Train AI → Add to Repository
```

For each IES file (luminaire type):
1. Generate thousands of synthetic scenarios with known optimal solutions
2. Create labeled training data (input: geometry/TLL chip, output: optimal dimming %)
3. Train deep learning model specific to that luminaire
4. Store trained .pth file in S3 repository

**Key Moat**: Training data is generated in-house with perfect labels (no GIGO). Competitors would need years to replicate this dataset.

### During Projects: Inference

```
Define TLL → Build Input Data → Load Pre-trained Model → Get Optimal Dimming → Schedule → Send to NLC
```

For a 2,000-light project:
- Traditional method: Days to weeks
- Photometrics AI: 3-5 minutes

---

## Component 4: Dynamic Scheduling

### Priority Resolution

When multiple conditions apply simultaneously, the scheduler resolves via strict hierarchy (highest priority wins, no averaging):

1. Dispatch triggers (emergency response)
2. Grid emergency (demand response)
3. Transportation safety windows
4. Crime prevention zones
5. Special events
6. Environmental protection (migratory birds)
7. Default operating profile

### Schedule Types

- **Time-based**: Astronomical (dusk/dawn), clock-based (midnight), seasonal
- **Event-based**: Calendar entries (Halloween, sports games, holidays)
- **Trigger-based**: API calls from external systems (CAD dispatch, CAISO, BirdCast)

---

## Component 5: NLC Integration

### API Architecture

Photometrics AI communicates with NLC platforms via their APIs:
- Receives: Asset inventory, luminaire locations, IES file assignments, current schedules
- Sends: Optimized per-luminaire dimming parameters, schedule assignments

### Current Integrations

- 2 major lighting control systems (production)
- Architecture supports additional platforms via adapter pattern

### What NLCs Provide (Photometrics AI Does Not Replace)

- Communications infrastructure
- Utility-grade metering
- Health monitoring and fault detection
- On/off control
- Non-lighting IoT (sensors, cameras)

### What Photometrics AI Adds

- Photometric intelligence
- Per-luminaire optimization
- Standards compliance verification
- Dynamic context-aware scheduling
- Multi-priority resolution

---

## Data Flow Architecture

### Frontend (Base44 → AWS Migration)

```
User uploads → Data Standardization Lambda → Point/Polygon GPKG (UTM) + IES → Backend
                                          ↓
                                    Elevation DEM
```

### Backend Training

```
IES Upload → Router Lambda → Training Lambda → EC2 Worker → .pth to S3 → DynamoDB Job
```

### Backend Inference

```
Queue/Hash Check → Chipper (Fargate) → Images → AI Inference (Docker) → Results → S3
                                                                              ↓
                                                                    Join back to original
                                                                              ↓
                                                                         Grouping
                                                                              ↓
                                                                    FlatGeoBuf → Frontend
```

### Frontend Display

- MapLibre GL JS for visualization
- StreetLightMap view (points with dimming values)
- TargetLightingMap view (TLL raster)
- Statistics panel (global/viewport averages, min/max)

---

## Key Technical Facts

### Operating Hours Definition

Street lights operate from the end of civil dusk (beginning of nautical dusk) to the end of nautical dawn (beginning of civil dawn). This period is called "dusk-to-dawn" and averages approximately 4,100-4,165 hours annually (11.4 hours per night).

| Twilight Phase | Sun Position | Lighting State |
|----------------|--------------|----------------|
| Civil dusk ends | 6° below horizon | Lights ON |
| Nautical/Astronomical | 6-18° below | Lights ON |
| Night | >18° below | Lights ON |
| Nautical dawn ends | 6° below horizon | Lights OFF |

**Not** sunset to sunrise. The distinction matters for accurate energy calculations and schedule programming.

### Lighting Physics

- Light differs in: Intensity (dimming), Color (CCT), Distribution (beam spread)
- Current NLCs control dimming only; color and distribution becoming software-controllable
- IES files describe photometric characteristics of each luminaire model
- Manufacturers release hundreds of variants per product line

### Standards Compliance

Photometrics AI optimizes to meet:
- ANSI/IES RP-8 (US roadway lighting)
- CIE 115 (international)
- AS/NZS 1158 (Australia/New Zealand)

Typical compliance rate: 91-97% of calculation points

### Luminaire Characteristics

- Average luminaire: 70W
- LED baseline: 100% output on astronomical schedule
- Optimized output: 55-85% depending on geometry
- Average night length: 11-12 hours

### Market Context

- 374M streetlights worldwide by 2029
- 15% currently on NLCs (22.7% CAGR growth)
  - 2019: 10.0M (3.2%)
  - 2025: 41.2M (12%)
  - 2030: 119.6M (32%)
- Street lighting = 2.3% of global electricity
- All lighting = 15-20% of global electricity ($260.5B market)
