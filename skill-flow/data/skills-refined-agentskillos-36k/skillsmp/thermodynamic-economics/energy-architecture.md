# Three-Layer Energy Architecture for Univrs.io

## Overview

This document defines the thermodynamic architecture required for the Univrs.io ecosystem to achieve energy honesty. Following Dr. Arnoux's critique, we acknowledge that the mycelium metaphor describes a heterotrophic (distribution) layer only. This architecture adds the missing autotrophic (energy capture) layer and formalizes all three layers with measurable energy flows.

```
+==============================================================================+
|                    THREE-LAYER ENERGY ARCHITECTURE                           |
+==============================================================================+

                              SUNLIGHT / GEOTHERMAL / KINETIC
                                          |
                                          v
+------------------------------------------------------------------------------+
|  LAYER 1: AUTOTROPHIC (Energy Capture)                                       |
|                                                                              |
|   +--------+     +--------+     +--------+     +--------+                    |
|   | Solar  |     |  Wind  |     | Hydro  |     |  Geo   |                    |
|   |  PV    |     |Turbine |     |Turbine |     |thermal |                    |
|   +---+----+     +---+----+     +---+----+     +---+----+                    |
|       |              |              |              |                          |
|       v              v              v              v                          |
|   +--------+     +--------+     +--------+     +--------+                    |
|   |Battery |     |Battery |     |Pumped  |     |Thermal |                    |
|   |Storage |     |Storage |     |Storage |     |Storage |                    |
|   +---+----+     +---+----+     +---+----+     +---+----+                    |
|       |              |              |              |                          |
|       +------+-------+------+-------+------+------+                          |
|              |              |              |                                  |
|              v              v              v                                  |
+------------------------------------------------------------------------------+
                                    |
                            Energy Surplus
                          (must be positive)
                                    |
                                    v
+------------------------------------------------------------------------------+
|  LAYER 2: DISTRIBUTION (Hyphal Network)                                      |
|                                                                              |
|       +---+         +---+         +---+         +---+                        |
|       |N01|---------|N02|---------|N03|---------|N04|                        |
|       +---+    \    +---+    /    +---+    \    +---+                        |
|         |       \    |      /       |       \    |                           |
|         |        \   |     /        |        \   |                           |
|       +---+       +---+   +---+   +---+       +---+                          |
|       |N05|-------|N06|---|N07|---|N08|-------|N09|                          |
|       +---+       +---+   +---+   +---+       +---+                          |
|         |          /  \    |     / |           |                             |
|         |         /    \   |    /  |           |                             |
|       +---+     +---+   +---+  +---+         +---+                           |
|       |N10|-----|N11|---|N12|--|N13|---------|N14|                           |
|       +---+     +---+   +---+  +---+         +---+                           |
|                                                                              |
|   Properties:                                                                |
|   - Clustering coefficient C >= 0.4 (local redundancy)                       |
|   - Path length L ~ log(N) (efficient routing)                               |
|   - Small-world sigma > 1.0                                                  |
|   - Energy cost per edge: P_edge watts                                       |
+------------------------------------------------------------------------------+
                                    |
                            Distributed Power
                          (minus network losses)
                                    |
                                    v
+------------------------------------------------------------------------------+
|  LAYER 3: HETEROTROPHIC (Productive Work)                                    |
|                                                                              |
|   +-------------+   +-------------+   +-------------+                        |
|   | Computation |   | Coordination|   |    Value    |                        |
|   |   (VUDO)    |   |  (Spirit)   |   |  Creation   |                        |
|   +-------------+   +-------------+   +-------------+                        |
|                                                                              |
|   - Spirit execution costs (joules per operation)                            |
|   - VUDO VM runtime overhead                                                 |
|   - Consensus and validation energy                                          |
|   - User interface and display                                               |
+------------------------------------------------------------------------------+

```

## Layer 1: Autotrophic (Energy Capture)

### Purpose

Convert ambient energy (solar radiation, wind, water flow, geothermal) into usable electrical power. This is the "missing layer" identified by Dr. Arnoux's critique.

### Energy Sources

| Source | EROEI Range | Capacity Factor | Notes |
|--------|-------------|-----------------|-------|
| Solar PV | 10-20:1 | 15-25% | Location-dependent |
| Wind (onshore) | 15-25:1 | 25-40% | Intermittent |
| Wind (offshore) | 10-18:1 | 35-45% | Higher cost |
| Hydroelectric | 40-60:1 | 40-60% | Site-limited |
| Geothermal | 5-15:1 | 85-95% | Very site-limited |

### Capture Efficiency Calculations

```
Gross Capture = Nameplate_Capacity x Capacity_Factor x Hours_per_Year

Net Capture = Gross_Capture x Conversion_Efficiency - Parasitic_Losses

Example (1 MW Solar PV):
  Nameplate:          1,000,000 W
  Capacity Factor:    0.17 (mid-latitude)
  Hours/Year:         8,760
  Conversion Eff:     0.20 (panel efficiency)
  Parasitic Losses:   2% (inverter, wiring)

  Gross Capture:      1,000,000 x 0.17 x 8,760 = 1,489,200 kWh/year
  Net Capture:        1,489,200 x 0.98 = 1,459,416 kWh/year
```

### Storage Options

#### Battery Storage (Lithium-ion)

```
Round-trip Efficiency:  85-92%
Cycle Life:            3,000-5,000 cycles
Energy Density:        150-250 Wh/kg
Embodied Energy:       ~100-200 kWh per kWh capacity

EROEI Impact:
  Storage adds ~5-15% to system energy input
  Must be factored into overall system EROEI
```

#### Thermal Storage

```
Round-trip Efficiency:  70-85%
Applications:          CSP, industrial heat
Cost:                  Lower $/kWh than batteries
Limitations:           Only for thermal loads
```

#### Hydrogen Storage

```
Round-trip Efficiency:  30-40% (electrolysis + fuel cell)
Energy Density:        Very high (volumetric)
Use Case:              Long-duration, seasonal storage
EROEI Impact:          Significant - only viable with very high EROEI source
```

### Energy Budget Calculation

```
+------------------------------------------+
| AUTOTROPHIC LAYER ENERGY BUDGET          |
+------------------------------------------+
| (+) Gross Solar Capture    1,500,000 kWh |
| (-) Panel Manufacturing     -60,000 kWh  | (amortized over 25 years)
| (-) Maintenance             -10,000 kWh  |
| (-) Inverter Losses         -30,000 kWh  |
| (-) Battery Round-trip     -150,000 kWh  | (10% of throughput)
| (-) Battery Embodied        -53,333 kWh  | (amortized over 15 years)
+------------------------------------------+
| = Net to Distribution     1,196,667 kWh  |
+------------------------------------------+
| Layer EROEI:                      ~4.9:1 |
+------------------------------------------+
```

## Layer 2: Distribution (Hyphal Network)

### Purpose

Route energy and information between producers and consumers using small-world network topology. This is the "mycelial" layer in our original metaphor.

### Network Topology Requirements

```
+---------------------------------------------------------------+
|                 SMALL-WORLD PROPERTIES                        |
+---------------------------------------------------------------+
| Metric              | Target        | Why                     |
|---------------------|---------------|-------------------------|
| Clustering (C)      | >= 0.4        | Local fault tolerance   |
| Path Length (L)     | O(log N)      | Efficient routing       |
| Sigma               | > 1.0         | Verified small-world    |
| Degree Distribution | k >= 4        | Minimum connectivity    |
+---------------------------------------------------------------+

For N = 1000 nodes:
  C_target:     >= 0.4
  L_target:     <= log(1000) / log(4) = 4.98 hops
  L_random:     ~4.5 hops (for comparison)

For N = 10000 nodes:
  C_target:     >= 0.4
  L_target:     <= log(10000) / log(4) = 6.64 hops
```

### Energy Cost Per Node

```
+---------------------------------------------------------------+
|                 NODE ENERGY BREAKDOWN                         |
+---------------------------------------------------------------+
| Component                    | Power (W)  | Annual (kWh)     |
|------------------------------|------------|------------------|
| Base compute (idle)          | 20         | 175              |
| Network interface            | 5          | 44               |
| Storage I/O                  | 10         | 88               |
| Active processing (avg)      | 40         | 350              |
| Cooling overhead (1.2x PUE)  | 15         | 131              |
|------------------------------|------------|------------------|
| TOTAL per node               | 90         | 788              |
+---------------------------------------------------------------+

For N = 1000 nodes:
  Network Energy = 788,000 kWh/year

For N = 10000 nodes:
  Network Energy = 7,880,000 kWh/year
```

### Network Overhead

```
Edge Energy Cost:
  E_edge = Base + Distance_Factor x d

  where:
    Base = 0.1 W per edge (switching/routing)
    Distance_Factor = 0.01 W per logical hop
    d = number of hops

For small-world with average L = 5 hops:
  E_edge = 0.1 + 0.01 x 5 = 0.15 W

For N = 1000, k = 4 (average degree):
  Total edges = N x k / 2 = 2000
  Edge energy = 2000 x 0.15 x 8760 = 2,628 kWh/year
```

### Distribution Losses

```
+---------------------------------------------------------------+
|              DISTRIBUTION LAYER LOSSES                        |
+---------------------------------------------------------------+
| Loss Type                    | Percentage | Notes             |
|------------------------------|------------|-------------------|
| Transmission (local)         | 2-5%       | Depends on grid   |
| Protocol overhead            | 3-5%       | Consensus cost    |
| Redundancy overhead          | 10-20%     | For fault tolerance|
| Idle power (standby)         | 5-10%      | Always-on nodes   |
+---------------------------------------------------------------+
| Total Layer Overhead         | 20-40%     |                   |
+---------------------------------------------------------------+
```

## Layer 3: Heterotrophic (Productive Work)

### Purpose

Perform useful computation, coordination, and value creation. This layer consumes the net energy surplus after Layers 1 and 2.

### Work Categories

#### Computation (VUDO)

```
Spirit Execution Costs:
  Simple operation:     0.001 kJ
  Database query:       0.01 kJ
  Complex calculation:  0.1 kJ
  ML inference:         1-10 kJ

VM Runtime Overhead:
  Context switch:       0.0001 kJ
  Memory allocation:    0.0001 kJ per MB
  I/O operation:        0.001 kJ
```

#### Coordination (Spirit Consensus)

```
Consensus Costs by Type:
  Local validation:     0.01 kJ per transaction
  Network consensus:    0.1 kJ per transaction (small-world routing)
  Full replication:     1.0 kJ per transaction (avoided by Hyphal design)
```

#### Value Creation

```
Net Energy Required per Unit Work:
  Document creation:    10 kJ (human-equivalent effort hour)
  Code compilation:     100 kJ (per 1000 lines)
  Data processing:      1 kJ per MB
```

### Heterotrophic Budget

```
+------------------------------------------+
| HETEROTROPHIC LAYER BUDGET (1000 nodes)  |
+------------------------------------------+
| Available from Distribution  956,000 kWh |
| (-) VUDO Runtime            -200,000 kWh |
| (-) Spirit Consensus        -100,000 kWh |
| (-) User Interfaces         -150,000 kWh |
+------------------------------------------+
| = Net Productive Work        506,000 kWh |
+------------------------------------------+
```

## Complete System Energy Flow

```
+==============================================================================+
|                        COMPLETE ENERGY FLOW DIAGRAM                          |
+==============================================================================+

                           SOLAR RADIATION
                          (1000 W/m^2 peak)
                                 |
                                 v
                    +------------------------+
                    |   SOLAR PV ARRAY       |
                    |   1 MW nameplate       |
                    |   17% capacity factor  |
                    +------------------------+
                                 |
                          1,489,200 kWh/year gross
                                 |
                                 v
                    +------------------------+
                    |   LOSSES & EMBODIED    |
                    |   -292,533 kWh/year    |
                    +------------------------+
                                 |
                          1,196,667 kWh/year net
                    (Layer 1 EROEI: 4.9:1)
                                 |
          +---------------------+---------------------+
          |                                           |
          v                                           v
+-------------------+                     +-------------------+
| BATTERY STORAGE   |                     | DIRECT TO GRID    |
| 400 kWh capacity  |                     | (excess/shortfall)|
| 90% round-trip    |                     +-------------------+
+-------------------+
          |
          v
+-------------------+
| DISTRIBUTION      |
| 1000-node network |
| C=0.45, L=4.8     |
+-------------------+
          |
    -240,667 kWh/year (20% overhead)
          |
          v
    956,000 kWh/year to heterotrophic
          |
          +-----------+-----------+-----------+
          |           |           |           |
          v           v           v           v
    +---------+ +---------+ +---------+ +---------+
    |  VUDO   | | Spirit  | |  User   | |   Net   |
    | Runtime | |Consensus| |Interface| |Productive|
    | 200,000 | | 100,000 | | 150,000 | | 506,000 |
    |  kWh    | |   kWh   | |   kWh   | |   kWh   |
    +---------+ +---------+ +---------+ +---------+

+==============================================================================+
|  SYSTEM SUMMARY                                                              |
|  -------------                                                               |
|  Input:          1,489,200 kWh/year (solar radiation captured)               |
|  Output:           506,000 kWh/year (productive work)                        |
|  System EROEI:        0.34:1 (NOT VIABLE without grid supplement)            |
|                                                                              |
|  NOTE: This illustrates the heterotroph problem. The network consumes        |
|  more energy than a single solar installation can provide. See               |
|  solar-integration.md for scaling calculations.                              |
+==============================================================================+
```

## Integration Points

### With EROEI Calculator

```python
# Use eroei_calculator.py to validate these numbers
from eroei_calculator import EnergySystem, EnergyComponent, EnergyType

system = EnergySystem("Three-Layer Architecture")

# Add autotrophic layer
system.add_component(EnergyComponent(
    name="Solar PV (1 MW)",
    component_type=EnergyType.SOLAR_PV,
    energy_output_kwh_year=1_489_200,
    energy_input_kwh_year=10_000,
    embodied_energy_kwh=1_500_000,
    lifespan_years=25
))

# Add distribution layer
system.add_component(EnergyComponent(
    name="Hyphal Network (1000 nodes)",
    component_type=EnergyType.NETWORK,
    energy_output_kwh_year=0,
    energy_input_kwh_year=788_000,
    embodied_energy_kwh=500_000,
    lifespan_years=5
))

# Analyze
analysis = system.analyze()
print(f"System EROEI: {analysis['system_eroei']:.2f}")
```

### With Small-World Metrics

```python
# Use small_world_metrics.py to validate network topology
# Network must achieve sigma > 1.0 to claim small-world properties
```

## Key Insights

1. **The heterotroph problem is real**: Without explicit autotrophic capacity, the network is a pure consumer.

2. **Scale matters**: 1 MW of solar supports ~1,000 nodes marginally. 10,000 nodes requires ~10 MW dedicated capacity.

3. **Storage is expensive**: Battery storage reduces system EROEI by 15-25%. Long-duration storage (hydrogen) is even worse.

4. **Distribution overhead is significant**: The small-world network adds 20-40% overhead. This is the cost of fault tolerance and global connectivity.

5. **Honest accounting required**: Must include embodied energy, maintenance, and all parasitic losses to get true EROEI.

## Next Steps

See:
- `solar-integration.md` - Detailed solar capacity calculations
- `grid-reality.md` - Honest assessment of grid dependence
- `energy-flow.dol` - Formal DOL schema for energy accounting

---

*Generated: 2026-01-02*
*Phase 2 Deliverable: Three-Layer Energy Architecture*
*Initiative: Thermodynamic Economics*
