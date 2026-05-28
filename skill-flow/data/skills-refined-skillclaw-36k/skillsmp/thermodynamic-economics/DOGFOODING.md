# Thermodynamic Calculators - Dogfooding DOL

The Python calculators have been replaced with DOL Spirits that compile through the Univrs.io toolchain:

```
DOL source -> Rust codegen -> cargo build -> WASM -> Spirit runtime
```

## Why DOL Instead of Python?

1. **Type Safety** - DOL constraints enforce thermodynamic invariants at compile time
2. **Dual Target** - Same source compiles to native binary AND WebAssembly
3. **Ecosystem Integration** - Runs in VUDO VM sandbox as a Spirit
4. **Dogfooding** - We use our own tools to build our learning materials

## Installation

### CLI Tool

```bash
# Build from source
cd ~/repos/univrs-vudo/spirits/thermodynamic
cargo install --path .

# Run EROEI analysis
thermo solar --nodes 1000

# Run network analysis
thermo network --nodes 100 --degree 6 --rewire 0.1
```

### Browser/WASM

```bash
# Build WASM package
cd ~/repos/univrs-vudo/spirits/thermodynamic
wasm-pack build --target web --release
```

```typescript
// Usage in TypeScript
import init, { EnergySystem } from '@univrs/thermodynamic';

await init();
const system = EnergySystem.new("Solar + Hyphal Network");
system.add_component(solarComponent);
system.add_component(networkComponent);

console.log(`EROEI: ${system.system_eroei()}`);
console.log(`Viable: ${system.is_viable()}`);
```

## DOL Source Files

The DOL schemas are in `univrs-vudo/spirits/thermodynamic/dol/`:

- `eroei.dol` - Energy Return on Energy Invested types and calculations
- `small_world.dol` - Watts-Strogatz network metrics
- `energy-flow.dol` - Energy flow accounting (moved from krzy)

## Legacy Python (Reference Only)

The Python files in this directory are **deprecated** and kept only for reference:

- `eroei_calculator.py` - Original Python implementation
- `small_world_metrics.py` - Original Python implementation

These files will NOT be updated. Use the DOL Spirits for new development.

## Key Results from Analysis

The calculators demonstrate:

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Solar PV EROEI | 30.54 | Excellent |
| Hyphal Network EROEI | 0 | Pure consumer |
| Solar + 1000 nodes | 3.20 | Subsistence |
| 1 MW solar capacity | ~3,457 nodes | Maximum supported |
| Dunbar cluster (150) sigma | 8.50 | Small-world confirmed |

See `analysis-results.md` for full details.

## Related Documentation

- [Thermodynamic Economics Initiative](./INITIATIVE_SUMMARY.md)
- [Response to Dr. Arnoux](./response-to-dr-arnoux.md)
- [Analysis Results](./analysis-results.md)
