# Competitive Positioning

## Primary Competition: Industry Practice

Photometrics AI's main competitor is **how the industry currently operates**, not a specific vendor.

### Traditional Lighting Design Problems

**"Cookie Cutter" Typical Layouts**
- Cities broken into a few design categories
- All roads of type X get the same treatment
- Ignores real-world geometry:
  - Road widths vary
  - Intersections don't meet at right angles
  - Mast arms hang over intersection centers
  - Slopes, bike lanes, sidewalk presence
  - Cul-de-sacs lumped with local streets

**CAD Tools Built for Indoor Spaces**
- Lighting professionals trained in architectural concepts
- Tools designed for rectangular rooms, not irregular streets
- Cannot handle real outdoor geometry at scale
- Result: overlighting, dark spots, wasted energy

**Arbitrary Dimming Schedules**
- Vendors offer preset profiles ("Dusk 100% - Dimming - Morning 100%")
- Not data-driven—just options to choose from
- Never based on actual usage, grid data, or safety outcomes
- Applied uniformly across all fixtures

### The Fundamental Gap

"The combination of rigid hardware selection and static dimming profiles locks cities into performance that often doesn't match real-world needs."

---

## Indirect Competition: Networked Lighting Controls (NLCs)

NLCs are **complements, not competitors**. They provide the infrastructure; Photometrics AI provides the intelligence.

### What NLCs Do Well

- Communications infrastructure
- Basic scheduling (astronomical, time-based)
- Health monitoring and fault detection
- On/off control
- Grouping (geographic, functional)
- High-level dimming (uniform % across groups)
- Utility-grade metering
- Non-lighting IoT integration (sensors, cameras, air quality)

### What NLCs Cannot Do

- **No photometric evaluation**: Don't calculate actual illuminance achieved
- **No per-luminaire optimization**: Apply same settings to large groups
- **No geography awareness**: Don't account for real road geometry
- **No standards verification**: Can't confirm compliance with RP-8, CIE 115
- **No overlapping beam analysis**: Don't coordinate adjacent fixtures
- **No multi-priority resolution**: Can't dynamically balance competing goals

### The Relationship

```
NLC provides: Control mechanism + Communications + Metering
Photometrics AI provides: Intelligence about WHAT to control
```

NLCs create large, undifferentiated groups → static, non-flexible load
Photometrics AI creates per-luminaire parameters → flexible, optimized resource

---

## Direct Competition: GRADIS (Poland)

### What GRADIS Does

- Graph-based lighting control with mathematical modeling
- Improved static layouts over traditional methods
- Requires real-time sensor inputs
- Still groups geography rather than per-luminaire optimization

### Photometrics AI Advantages Over GRADIS

| Factor | GRADIS | Photometrics AI |
|--------|--------|-----------------|
| Geography | Groups areas | Per-luminaire optimization |
| Sensors | Requires additional hardware | Software-only |
| Implementation | Hardware complexity/cost | API integration in weeks |
| Dynamic optimization | Static layouts | Context-aware scheduling |
| Training data | Unknown | Proprietary in-house dataset |

### Key Differentiators

1. **No sensors required**: GRADIS needs hardware; we're pure software
2. **True per-luminaire**: We optimize each fixture individually
3. **Dynamic, not static**: Our schedules respond to real-time triggers
4. **Simpler deployment**: API integration vs sensor installation
5. **Stronger energy impact**: More optimization headroom without hardware constraints

---

## Competitive Moat

### 1. Patented Technology

- **US9894736B2** (2018): Target Lighting Layers
- **18/660,680** (pending): AI-labeled training data methodology

### 2. Proprietary Training Data

- In-house generated with perfect labels
- Thousands of lighting scenarios per luminaire type
- No "garbage in, garbage out"—synthetic data with known optimal solutions
- **This is the hardest part of AI to replicate**

### 3. Multi-Year Head Start

- EvariLUX (predecessor) deployed in major US cities
- Existing relationships with municipalities and utilities
- Integrated with production NLC systems
- While incumbents focus on hardware (lumens/watt) and non-lighting IoT

### 4. Domain Expertise

- Founder (Ari) built Evari GIS Consulting, national leader in roadway lighting design
- LED conversions and control integrations in San Jose, SF, Chicago, Boston
- Deep relationships = direct market access

---

## Why Lighting Industry Hasn't Solved This

### Attention Elsewhere

- "Innovation" in lighting = lumens per watt (hardware efficiency)
- Controls vendors focused on non-lighting IoT (sensors, smart city platforms)
- Nobody applying GIS + AI to photometric optimization

### Skills Gap

- Lighting professionals trained in architecture, not geography
- CAD and spreadsheet workflows, not GIS
- Building codes, not transportation standards
- Lighting not even in MUTCD (federal transportation safety regulation)

### Fragmented Market

- Municipalities buy from different vendors
- No standardization across NLC platforms
- Each city is an island—nobody optimizing at scale

---

## Positioning Statements

### vs. Traditional Practice
"Traditional lighting design is outdated. Let's fix it with data-driven decisions."

### vs. NLCs
"Current NLCs provide control but not optimization. They lack photometric intelligence and do not generate per-luminaire operating parameters."

### vs. Status Quo
"Lighting is the last mile of infrastructure that hasn't caught up to the age of smart everything. Photometrics AI is fixing that."

### For Utilities
"Photometrics AI replaces static design and broad control groups with fixture-level optimization."

### For Investors
"Competitors today are still using cookie-cutter designs, CAD tools, and one-size-fits-all dimming. Our moat is measured not just in patents, but in years of traction and datasets competitors can't easily catch up to."
