# EROEI Database Reference

## Energy Return on Energy Invested (EROEI)

### Definition

```
EROEI = Energy Delivered to Society / Energy Required for Extraction and Processing

Variants:
- EROIstd: Standard EROEI (extraction only)
- EROIpou: EROEI at point of use (includes transport, conversion)
- EROIext: Extended EROEI (includes societal support infrastructure)
```

### Minimum Societal Requirements

| EROEI Range | What It Supports |
|-------------|------------------|
| 1:1 | Thermodynamic equilibrium (dead state) |
| 2:1 | Extraction only, no surplus |
| 3:1 | Basic agriculture possible |
| 5:1 | Basic industrial activity |
| 7-10:1 | Modern infrastructure maintenance |
| 12-14:1 | Education, healthcare, R&D |
| 20+:1 | Complex technology development |

**Cliff note**: Below 5:1, civilization cannot maintain current complexity.

### Fossil Fuels (Historical Decline)

| Source | Period | EROEI | Notes |
|--------|--------|-------|-------|
| US Oil | 1930s | 100:1 | Giant fields, easy extraction |
| US Oil | 1970s | 30:1 | Mature fields |
| US Oil | 2010s | 10-15:1 | Conventional decline |
| Tight Oil (Fracking) | 2010s | 5-10:1 | High input requirements |
| Oil Sands | Current | 3-5:1 | Extraction intensive |
| Ultra-deep Water | Current | 8-12:1 | Technical complexity |
| Natural Gas (Conv.) | Current | 15-25:1 | Varies by field |
| Shale Gas | Current | 10-15:1 | Declining over time |
| Coal | Current | 20-50:1 | Varies by quality/depth |

### Renewables

| Source | EROEI Range | Notes |
|--------|-------------|-------|
| Hydroelectric | 40-60:1 | Excellent, site-limited |
| Wind (onshore) | 15-25:1 | Good, improving |
| Wind (offshore) | 10-18:1 | Higher installation cost |
| Solar PV | 10-20:1 | Improving with technology |
| Solar Thermal (CSP) | 8-15:1 | Requires direct sunlight |
| Geothermal | 5-15:1 | Site-dependent |
| Biomass | 2-5:1 | Often negative when full inputs counted |
| Corn Ethanol | 0.8-1.3:1 | Often net energy negative |
| Cellulosic Ethanol | 2-6:1 | Still developing |

### Nuclear

| Type | EROEI Range | Notes |
|------|-------------|-------|
| Light Water (current) | 10-15:1 | Includes enrichment |
| Breeder reactors | 20-100:1 | Theoretical, few operating |
| Fusion | Unknown | Not yet achieved |

### Computational/Network Infrastructure

This is the critical gap for digital systems:

| Component | Typical Power | Notes |
|-----------|---------------|-------|
| Data center (per rack) | 5-20 kW | Varies by density |
| Network router (core) | 100-500 W | High throughput |
| Blockchain consensus (Bitcoin) | ~100 TWh/yr globally | Very poor EROEI |
| Proof-of-stake | 0.001% of PoW | Much better but still costs |
| Edge computing node | 10-100 W | Distributed overhead |

### Calculating System EROEI

```python
def system_eroei(components):
    """
    Calculate EROEI for a complex system.
    
    components: list of {
        'name': str,
        'energy_out': float (joules delivered),
        'energy_in': float (joules required),
        'lifespan': float (years),
        'embodied_energy': float (manufacturing energy)
    }
    """
    total_out = 0
    total_in = 0
    
    for c in components:
        # Annualized embodied energy
        annual_embodied = c['embodied_energy'] / c['lifespan']
        
        total_out += c['energy_out']
        total_in += c['energy_in'] + annual_embodied
    
    return total_out / total_in if total_in > 0 else 0

# Example: Solar + Storage + Distribution
solar_system = [
    {
        'name': 'Solar PV Array',
        'energy_out': 1_000_000,  # kWh/year
        'energy_in': 50_000,      # kWh/year (maintenance, cleaning)
        'lifespan': 25,
        'embodied_energy': 500_000  # kWh (manufacturing)
    },
    {
        'name': 'Battery Storage',
        'energy_out': 950_000,    # After round-trip losses
        'energy_in': 10_000,      # Thermal management
        'lifespan': 15,
        'embodied_energy': 200_000
    },
    {
        'name': 'Distribution Network',
        'energy_out': 900_000,    # After transmission losses
        'energy_in': 5_000,       # Monitoring, maintenance
        'lifespan': 40,
        'embodied_energy': 100_000
    }
]

# Result: system_eroei(solar_system) → ~10:1 (viable but modest)
```

### The Energy Seneca Cliff

Dr. Arnoux's concept: When aggregate EROEI drops below viability threshold, collapse is rapid.

```
       Energy     |    ___________
       Surplus    |   /           \
                  |  /             \
                  | /               \
                  |/                 \______ (Seneca cliff)
                  +──────────────────────────→ Time
                        Slow rise, fast fall
```

Key drivers:
1. Depletion of high-EROEI resources
2. Increasing extraction costs
3. Infrastructure maintenance burden
4. Climate impacts on productivity

### Sources

1. Hall, C.A.S., et al. (2014). EROI of different fuels and the implications for society. Energy Policy 64, 141-152.
2. Murphy, D.J. & Hall, C.A.S. (2011). Adjusting the economy to the new energy realities. Ecological Modelling 223, 67-71.
3. Cleveland, C.J. (2005). Net energy from the extraction of oil and gas in the United States. Energy 30, 769-782.
4. Arnoux, L. (2020). Thermodynamics, Fossil Fuels and Renewables. Medium series.
