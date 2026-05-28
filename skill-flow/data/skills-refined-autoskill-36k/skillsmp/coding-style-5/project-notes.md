# SC Interdiction - Project Notes & Scratchpad

## Overview
Star Citizen interdiction planning tool that analyzes trade routes to predict valuable targets.

## Architecture
- **api-client**: UEX Corporation API client for trade data
- **intel**: Target prediction and route analysis
- **route-graph**: Graph-based route planning and chokepoint detection
- **server**: REST API server (axum)
- **cli**: Command-line interface with TUI dashboard (ratatui)

## Data Sources
- **UEX API**: https://uexcorp.space/api/documentation/
  - `commodities_prices_all` - All commodity prices at all terminals
  - `terminals` - Trade locations with type (commodity, fuel, refinery, etc.)
  - Terminal types: commodity (159), fuel (93), refinery (21), item (451), vehicle_rent (32), commodity_raw (19), vehicle_buy (9)
- **Fleet Yards API**: https://fleetyards.net/
  - Ship specifications including cargo capacity and fuel tank sizes
  
## Data Gaps & Placeholders

### Fuel Pricing (CRITICAL - NEEDS VERIFICATION)
**Current Status**: Using placeholder values without real data source
- `HYDROGEN_FUEL_PRICE_PER_UNIT = 1.0 aUEC` - **UNVERIFIED PLACEHOLDER**
- `QUANTUM_FUEL_PRICE_PER_UNIT = 1.5 aUEC` - **UNVERIFIED PLACEHOLDER**

**Needed**:
1. In-game measurement at refueling stations (screenshot with prices)
2. Check if UEX API has fuel as a commodity with pricing
3. Community data sources (spectrum forums, star citizen tools, etc.)

**Impact**: Refueling cost calculations are functional but use arbitrary values.
Route profitability calculations that include refueling costs will be inaccurate
until real pricing data is added.

**Action Items**:
- [ ] Measure hydrogen fuel price in-game at major refueling stations
- [ ] Measure quantum fuel price in-game at major refueling stations
- [ ] Query UEX API for fuel commodity pricing
- [ ] Document actual prices with screenshot evidence
- [ ] Update constants in `crates/route-graph/src/fuel.rs`

## Current Limitations & Planned Improvements

### Ship Docking Restrictions
- [x] Hull C requires stations with freight elevators (name contains "Station")
- [ ] Other Hull series ships (Hull A, B, D, E) when added

### Route Realism
- [ ] **Round-trip validation**: Currently treats inbound/outbound as separate routes. Should link them as complete trade runs.
- [ ] **Fuel range**: Ships have limited fuel. Long routes need refueling stops.
  - Need to add `fuel_capacity` and `fuel_consumption` to `CargoShip`
  - Use fuel terminals (type=fuel) as waypoints
  - Validate that routes are achievable with available fuel stops
- [ ] **Distance calculation**: Need terminal coordinates for accurate distance/fuel calculations
  - Approximate positions exist in `estimate_location_position()` for major locations
  - UEX API may have coordinate data (investigate)

### Mining/Refinery Support
- [ ] Connect asteroid mining locations to refineries (type=refinery)
- [ ] Different workflow: mine -> refine -> sell refined materials

## Ship Database Notes
Ships that require special docking:
- **Hull C**: 4608 SCU, requires external freight elevator (stations only)
- **Hull D/E**: Not yet in game, will also require freight elevators

## API Quirks
- Terminal names include location hierarchy: "Commodity Shop - Admin - ARC-L1 (Stanton > ArcCorp)"
- Some fields can be null, use `#[serde(default)]`
- `commodities_routes` endpoint changed, now use `commodities_prices_all` + calculate routes

## Testing
Run with: `export CARGO_TARGET_DIR="/tmp/cargo-target" && cargo run -p sc-interdiction -- <command>`

Example commands:
```bash
# TUI dashboard
cargo run -p sc-interdiction -- dashboard --location Crusader

# Intel for location
cargo run -p sc-interdiction -- intel Crusader --json

# List terminals
cargo run -p sc-interdiction -- terminals --json
```
