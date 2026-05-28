---
name: ONI Calculator
description: Oxygen Not Included production chain calculator with SQLite database extracted from decompiled game source
---

# ONI Calculator

## Instructions

When helping users with Oxygen Not Included calculations and planning:

1. **Database Location**: `oni-calculator/oni_data.db` - SQLite database with building data
2. **Decompiled Source**: `oni-decompiled/Assembly-CSharp/` - C# source for pattern discovery
3. **Extraction Tool**: `oni-calculator/src/extract.rs` - Rust code that parses C# into SQLite

### Query the Database First

Use sqlite3 to query building data:
```bash
sqlite3 oni-calculator/oni_data.db "SELECT * FROM buildings WHERE id LIKE '%Pump%'"
sqlite3 oni-calculator/oni_data.db "SELECT building_id, rate_kg_per_s FROM building_outputs WHERE resource_id='Oxygen'"
```

### If Data is Missing

1. Grep the decompiled source to find the pattern:
   ```bash
   grep -E "consumptionRate|OutputElement" oni-decompiled/Assembly-CSharp/BuildingNameConfig.cs
   ```

2. Update `oni-calculator/src/extract.rs` with a new regex pattern

3. Re-run extraction:
   ```bash
   cd oni-calculator && cargo run -- extract ../oni-decompiled/Assembly-CSharp --clear
   ```

4. Commit the fix so it persists

### Key Database Tables

- `buildings` - id, name, power_watts (negative=consumes, positive=generates), heat_output_dtu
- `building_inputs` - building_id, resource_id, rate_kg_per_s
- `building_outputs` - building_id, resource_id, rate_kg_per_s

### Common Calculations

- **Buildings needed**: target_rate / building_output_rate
- **Power budget**: Sum of power_watts (negative = consumption)
- **Heat output**: Sum of heat_output_dtu
- **Pump duty cycle**: required_rate / pump_throughput

## Examples

### Example 1: SPOM Planning
```
User: How many electrolyzers do I need for a hydrogen generator?

Claude: [Queries database for Electrolyzer outputs and HydrogenGenerator inputs]
- Electrolyzer produces 0.112 kg/s Hydrogen
- H2 Generator consumes 0.1 kg/s Hydrogen
- Answer: 0.89 Electrolyzers (practically: 1 Electrolyzer with 12% surplus)
```

### Example 2: CO2 Handling
```
User: How many CO2 scrubbers for my coal generators?

Claude: [Queries database]
- Coal Generator outputs 0.02 kg/s CO2
- CO2 Scrubber consumes 0.3 kg/s CO2
- Answer: 1 scrubber handles 15 generators
```

### Example 3: Missing Data
```
User: What's the throughput of a gas pump?

Claude: [Queries DB, finds data missing]
[Greps source: grep consumptionRate oni-decompiled/Assembly-CSharp/GasPumpConfig.cs]
[Finds: elementConsumer.consumptionRate = 0.5f]
[Updates extract.rs with ElementConsumer pattern]
[Re-runs extraction, commits fix]
Answer: 0.5 kg/s
```

### Example 4: Heat Comparison
```
User: Which generator runs coolest?

Claude: [Queries: SELECT id, power_watts, heat_output_dtu FROM buildings WHERE power_watts > 0]
[Calculates DTU per watt for each]
Answer: Hydrogen Generator at 5 DTU/W, Coal is 15 DTU/W
```

---

# Reference

## Useful Queries

```sql
-- All buildings that produce a resource
SELECT building_id, rate_kg_per_s FROM building_outputs WHERE resource_id = 'Oxygen';

-- All inputs for a building
SELECT resource_id, rate_kg_per_s FROM building_inputs WHERE building_id = 'Electrolyzer';

-- Power generators ranked by efficiency
SELECT id, power_watts, heat_output_dtu,
       heat_output_dtu / power_watts as dtu_per_watt
FROM buildings
WHERE power_watts > 0
ORDER BY dtu_per_watt;

-- Buildings that consume a resource
SELECT building_id, rate_kg_per_s FROM building_inputs WHERE resource_id = 'Water';
```

## Extraction Patterns in extract.rs

Currently captured patterns:
- `const string ID = "BuildingName"` - Building IDs
- `EnergyConsumptionWhenActive = 120f` - Power consumption
- `GeneratorWattageRating = 800f` - Power generation
- `ConsumedElement(new Tag("X"), rate)` - ElementConverter inputs
- `ConsumedElement(GameTagExtensions.Create(SimHashes.X), rate)` - Alternative input format
- `OutputElement(rate, SimHashes.X, ...)` - ElementConverter outputs
- `CreateSimpleFormula(input, rate, capacity, output, rate)` - Generator fuel/exhaust
- `elementConsumer.consumptionRate` - Pump throughput
- `conduitConsumer.consumptionRate` - Pipe consumer rates

Patterns NOT yet captured (add when needed):
- Recipe-based buildings (Metal Refinery, Rock Crusher)
- Critter outputs (Hatch coal production, etc.)
- Plant growth rates
- Duplicant consumption rates

## CLI Commands

```bash
cd oni-calculator

# List all buildings
cargo run -- list-buildings

# Show building details
cargo run -- building Electrolyzer

# List producible resources
cargo run -- list-resources

# Calculate production chain (picks first producer alphabetically)
cargo run -- calc Oxygen --rate 1.0 --verbose

# Re-run extraction
cargo run -- extract ../oni-decompiled/Assembly-CSharp --clear
```

## Key ONI Numbers

| Building | Power | Throughput | Heat |
|----------|-------|------------|------|
| Electrolyzer | -120W | 1 kg/s Water → 0.888 O2 + 0.112 H2 | 1250 DTU/s |
| H2 Generator | +800W | 0.1 kg/s H2 | 4000 DTU/s |
| Coal Generator | +600W | 1 kg/s Coal → 0.02 CO2 | 9000 DTU/s |
| Gas Pump | -240W | 0.5 kg/s | 0 DTU/s |
| Liquid Pump | -240W | 10 kg/s | 2000 DTU/s |
| CO2 Scrubber | -120W | 0.3 kg/s CO2 + 1 kg/s Water | 1000 DTU/s |
