# Curriculum: Thermodynamic Economics

**Phase 1 - Acknowledge & Learn**

---

## Course Overview

This curriculum provides the thermodynamic foundations necessary to evaluate economic systems honestly. It addresses the critique that our Mycelial Economics framework lacked energy accounting.

**Prerequisites**: Basic algebra, willingness to question assumptions

**Duration**: Self-paced, approximately 20-30 hours of study

**Outcome**: Ability to calculate EROEI for complex systems and assess thermodynamic viability

---

## Module 1: Laws of Thermodynamics Applied to Economics

### 1.1 The First Law: Conservation

**Principle**: Energy cannot be created or destroyed, only transformed.

**Economic implication**: All economic activity is fundamentally energy transformation. Money is a claim on energy-enabled work, not an independent entity.

```
Production = Energy Input × Conversion Efficiency
Wealth = Accumulated claims on future energy transformations
GDP = Rate of energy throughput × economic productivity per joule
```

**Key insight**: There is no free lunch. Every output requires energy input.

### 1.2 The Second Law: Entropy

**Principle**: In any closed system, entropy (disorder) increases over time. Energy transformations are never 100% efficient.

**Economic implication**: Maintaining economic complexity requires continuous energy input. Without energy flow, systems decay toward equilibrium (death).

```
Maintenance Energy = f(System Complexity)
Economic Growth = New Energy - Entropy Tax - Maintenance

If (New Energy < Entropy Tax + Maintenance):
    System degrades
```

**Key insight**: Complexity has a maintenance cost. The more complex the system, the more energy required just to keep it running.

### 1.3 The Third Law: Absolute Zero

**Principle**: Perfect efficiency (zero entropy) is unattainable.

**Economic implication**: All processes have waste. Accounting that ignores waste is thermodynamically dishonest.

### 1.4 Non-Equilibrium Thermodynamics

**Principle**: Living systems and economies exist far from equilibrium, maintained by energy gradients.

**Economic implication**: Economic vitality requires sufficient energy flow to maintain distance from equilibrium. As energy flow decreases, systems collapse toward equilibrium states.

### Exercises - Module 1

1. Calculate the energy content of your daily food intake in joules
2. Estimate the entropy production of your household (waste heat, garbage, etc.)
3. Identify three economic activities and trace their energy inputs

### Readings - Module 1

**Primary**:
- Georgescu-Roegen, N. (1971). *The Entropy Law and the Economic Process*. Harvard University Press. [Chapters 1-3]

**Supplementary**:
- Daly, H.E. (1996). *Beyond Growth*. Beacon Press. [Chapter 2: "Thermodynamics and Economics"]
- Soddy, F. (1926). *Wealth, Virtual Wealth and Debt*. [Available online]

---

## Module 2: EROEI Analysis Methodology

### 2.1 Definition and Significance

**EROEI** (Energy Return on Energy Invested): The ratio of energy delivered to society versus energy required to extract, process, and deliver that energy.

```
EROEI = Energy Out / Energy In

Where Energy In includes:
- Direct energy for extraction
- Embodied energy in equipment
- Processing and refining
- Transport and distribution
- Waste management
```

**Why it matters**: EROEI determines what's possible. Below certain thresholds, activities cannot sustain themselves.

### 2.2 EROEI Thresholds

| EROEI | What It Supports |
|-------|------------------|
| 1:1 | Break-even (no surplus) |
| 3:1 | Basic agriculture |
| 5:1 | Simple industrial activity |
| 7:1 | Infrastructure maintenance |
| 10:1 | Modern industrial society |
| 14:1 | Education, healthcare, R&D |
| 20+:1 | Complex technology development |

**Critical threshold**: Most researchers estimate 7-10:1 as minimum for maintaining industrial civilization.

### 2.3 The EROEI Calculator

Reference implementation: `eroei_calculator.py`

```python
from eroei_calculator import EnergySystem, EnergyComponent, EnergyType

# Example: Modeling a solar installation
system = EnergySystem(name="Community Solar")

# Add solar array
system.add_component(EnergyComponent(
    name="Solar PV (100 kW)",
    component_type=EnergyType.SOLAR_PV,
    energy_output_kwh_year=150_000,      # Actual annual output
    energy_input_kwh_year=1_000,         # Maintenance
    embodied_energy_kwh=150_000,         # Manufacturing
    lifespan_years=25,
    capacity_factor=0.17
))

# Analyze
analysis = system.analyze()
print(f"System EROEI: {analysis['system_eroei']:.1f}")
print(f"Viability: {analysis['viability_assessment']}")
```

### 2.4 Common EROEI Errors

1. **Ignoring embodied energy**: Not counting manufacturing inputs
2. **Boundary drawing**: Excluding transportation, processing, waste
3. **Quality conflation**: Treating all joules as equivalent (electricity vs. heat)
4. **Time discounting**: Ignoring energy timing (intermittency costs)
5. **Optimistic projections**: Using nameplate vs. actual capacity

### 2.5 Energy Quality and Net Energy

Not all energy is equivalent. Conversion matters:

```
Electricity → Heat:     ~100% efficient
Heat → Electricity:     ~30-40% efficient
Chemical → Mechanical:  ~25-40% efficient

Net Energy = Gross Energy - Energy for Extraction - Conversion Losses
```

### Exercises - Module 2

1. Calculate EROEI for your household energy system
2. Use `eroei_calculator.py` to model a proposed renewable installation
3. Compare EROEI of three different energy sources using the database in `eroei-database.md`

### Readings - Module 2

**Primary**:
- Hall, C.A.S., Lambert, J.G., & Balogh, S.B. (2014). "EROI of different fuels and the implications for society." *Energy Policy* 64, 141-152.

**Supplementary**:
- Murphy, D.J. & Hall, C.A.S. (2011). "Adjusting the economy to the new energy realities of the second half of the age of oil." *Ecological Modelling* 223, 67-71.
- Prieto, P.A. & Hall, C.A.S. (2013). *Spain's Photovoltaic Revolution: The Energy Return on Investment*. Springer.

---

## Module 3: Energy Flow Mapping

### 3.1 System Boundaries

Before calculating EROEI, define system boundaries precisely:

```
NARROW BOUNDARY (EROIstd)
├── Extraction energy
├── On-site processing
└── Direct inputs only

POINT-OF-USE BOUNDARY (EROIpou)
├── All of above, plus:
├── Transportation
├── Refining/conversion
└── Distribution losses

EXTENDED BOUNDARY (EROIext)
├── All of above, plus:
├── Labor energy equivalent
├── Financial sector overhead
└── Societal support systems
```

### 3.2 Flow Diagrams

Map energy flows explicitly:

```
                     ┌─────────────┐
     Solar Flux     │             │
    ─────────────→  │  Capture    │───→ Losses (albedo, heat)
    (1000 W/m²)     │  (PV cells) │
                     └──────┬──────┘
                            │
                     Electricity (150 W/m²)
                            │
                            ↓
                     ┌─────────────┐
                     │  Inverter   │───→ Conversion loss (5%)
                     └──────┬──────┘
                            │
                            ↓
                     ┌─────────────┐
                     │  Storage    │───→ Round-trip loss (10%)
                     └──────┬──────┘
                            │
                            ↓
                     ┌─────────────┐
                     │ Distribution│───→ Transmission loss (5%)
                     └──────┬──────┘
                            │
                            ↓
                      Useful Work
```

### 3.3 Sankey Diagrams

Represent flows with width proportional to magnitude:

```
INPUTS                           OUTPUTS
═══════════════════════════════════════════════════════════
Solar radiation ═══════════════════╗
(1,000 kWh/m²/yr)                  ║
                                   ║══════════╗
                             Electrical Output ║
                                   (150 kWh)   ║
                                               ╠══→ Useful work (120 kWh)
                                               ║
                                               ╠══→ Storage loss (15 kWh)
                                               ║
                                               ╚══→ Transmission loss (15 kWh)
```

### Exercises - Module 3

1. Draw an energy flow diagram for a distributed computing network
2. Identify all loss points in a proposed Hyphal Network node
3. Create a Sankey diagram for the Univrs.io ecosystem (estimate values)

### Readings - Module 3

**Primary**:
- Cullen, J.M. & Allwood, J.M. (2010). "The efficient use of energy: Tracing the global flow of energy from fuel to service." *Energy Policy* 38, 75-81.

---

## Module 4: Dissipative Structures (Prigogine)

### 4.1 Order from Chaos

**Key concept**: Complex, ordered structures can emerge spontaneously in systems far from equilibrium, maintained by energy flow.

Examples:
- Convection cells (Benard cells)
- Chemical oscillations (Belousov-Zhabotinsky)
- Living organisms
- Economic systems

### 4.2 Requirements for Dissipative Structures

1. **Open system**: Energy/matter flows through
2. **Far from equilibrium**: Maintained by external gradients
3. **Nonlinear dynamics**: Small changes can have large effects
4. **Fluctuations**: Random variations seed new structures

```
                    Energy Gradient
                          │
                          ↓
┌─────────────────────────────────────────┐
│                                         │
│    Low Entropy    →    Complexity    →  │──→ High Entropy
│    (organized)         emerges          │    (waste heat)
│                                         │
└─────────────────────────────────────────┘
                          │
                          ↓
                   Structure Maintained
```

### 4.3 Economic Implications

Economies are dissipative structures. They:
- Require continuous energy throughput
- Generate complexity through far-from-equilibrium conditions
- Collapse when energy gradients diminish
- Self-organize but at a thermodynamic cost

**Key insight**: Economic complexity is not free. It is maintained by energy flow. Reduce the flow, lose the complexity.

### 4.4 The Entropy Budget

Every system has an entropy budget:

```
Entropy Production Rate = Energy Throughput × (1 - Efficiency)

For survival:
Entropy Exported > Entropy Generated Internally

For growth:
Energy Input > (Maintenance + Entropy Tax + Growth Energy)
```

### Exercises - Module 4

1. Identify three dissipative structures in your daily life
2. Estimate the energy throughput required to maintain your household complexity
3. Analyze the Hyphal Network as a dissipative structure: what maintains it?

### Readings - Module 4

**Primary**:
- Prigogine, I. & Stengers, I. (1984). *Order Out of Chaos: Man's New Dialogue with Nature*. Bantam Books. [Chapters 5-7]

**Supplementary**:
- Schneider, E.D. & Kay, J.J. (1994). "Life as a manifestation of the second law of thermodynamics." *Mathematical and Computer Modelling* 19(6-8), 25-48.

---

## Module 5: The Fourth Transition Framework (Arnoux)

### 5.1 Historical Energy Transitions

| Transition | From | To | EROEI Impact |
|------------|------|----|----|
| First | Muscle power | Fire/agriculture | Modest gain |
| Second | Biomass | Coal | Large gain |
| Third | Coal | Oil | Massive gain (100:1 early) |
| Fourth | Fossil | ??? | Crisis point |

### 5.2 The Energy Seneca

Dr. Arnoux's framework: Energy surplus rises slowly but falls quickly.

```
       Net Energy    |    ___________
       Surplus       |   /           \
                     |  /             \
                     | /               \
                     |/                 \______ (Seneca cliff)
                     +──────────────────────────→ Time
                           Slow rise, fast fall
```

Causes:
1. Best resources extracted first (depletion)
2. Remaining resources require more energy to extract
3. Infrastructure maintenance costs accumulate
4. Feedback loops accelerate decline

### 5.3 The Three Thermodynamic Traps

1. **Energy Cannibalism**: Using energy to produce energy-producing equipment, depleting net available energy
2. **EROEI Cliff**: Non-linear drop in net energy as EROEI approaches critical threshold
3. **Complexity Trap**: Maintaining existing complexity consumes energy needed for transition

### 5.4 The Autopoiesis Question

Dr. Arnoux's claim: "Humankind has ceased being autopoietic since 2010-2020."

Meaning:
- Industrial civilization can no longer reproduce itself from available energy flows
- We are consuming accumulated stocks (fossil fuels = ancient sunlight)
- When stocks deplete, systems that depend on them cease

```python
# Autopoietic test
def is_autopoietic(system):
    """Check if system can reproduce from flows (not stocks)."""

    energy_from_flows = system.renewable_energy_capture()
    energy_needed_for_reproduction = system.reproduction_energy_requirement()

    # Include energy to produce reproduction equipment!
    energy_for_equipment = system.equipment_production_energy()

    net_available = energy_from_flows - energy_for_equipment

    return net_available > energy_needed_for_reproduction
```

### 5.5 Implications for Univrs.io

The Hyphal Network, as designed, has EROEI = 0 (pure consumer). To be thermodynamically viable:

1. **Specify autotrophic sources**: Solar, wind, hydro, etc.
2. **Calculate system EROEI**: Including network overhead
3. **Verify viability threshold**: System EROEI > 7 minimum
4. **Design for autopoiesis**: Can system reproduce itself from flows?

### Exercises - Module 5

1. Calculate: At current EROEI decline rates, when do we hit the cliff?
2. Identify energy cannibalism in the renewable energy transition
3. Propose how Univrs.io could specify its autotrophic layer

### Readings - Module 5

**Primary**:
- Arnoux, L. (2020). "Thermodynamics, Fossil Fuels and Renewables." Medium series. [fourthtr.com]
- Arnoux, L. "The Fourth Transition." [Available at fourthtransitionwealth.com]

**Supplementary**:
- Tainter, J. (1988). *The Collapse of Complex Societies*. Cambridge University Press.
- Greer, J.M. (2008). *The Long Descent*. New Society Publishers.

---

## Assessment

### Module Quizzes

Each module should be followed by self-assessment:

1. Can you explain the concept to someone unfamiliar?
2. Can you calculate relevant metrics?
3. Can you apply the framework to new situations?

### Capstone Project

**Project**: EROEI Analysis of Univrs.io Ecosystem

Requirements:
1. Model all energy-consuming components (nodes, network, storage)
2. Specify at least two autotrophic source scenarios
3. Calculate system EROEI for each scenario
4. Assess viability against 7:1 threshold
5. Propose modifications to achieve viability if needed

Deliverable: Report using `eroei_calculator.py` with full analysis

---

## Additional Resources

### Tools

- `eroei_calculator.py` - Energy system modeling
- `eroei-database.md` - Reference EROEI values

### Communities

- Fourth Transition Institute - [fourthtr.com](https://fourthtr.com)
- Biophysical Economics - [biophyseco.org](https://biophyseco.org)
- Post Carbon Institute - [postcarbon.org](https://postcarbon.org)

### Extended Reading List

1. Odum, H.T. (2007). *Environment, Power, and Society for the Twenty-First Century*
2. Hall, C.A.S. (2017). *Energy Return on Investment: A Unifying Principle for Biology, Economics, and Sustainability*
3. Smil, V. (2017). *Energy and Civilization: A History*

---

*Phase 1 - Acknowledge & Learn*
*Thermodynamic Economics Learning Initiative*
*Generated: 2026-01-02*
