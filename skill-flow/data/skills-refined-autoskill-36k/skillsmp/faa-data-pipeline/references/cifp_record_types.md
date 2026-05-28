# CIFP Record Types (ARINC 424)

Reference for FAA CIFP (Coded Instrument Flight Procedures) data in ARINC 424 format.

## Record Structure

All ARINC 424 records are 132 bytes (characters) in fixed-width format.

```
Position 1:     Record Type (always 'S' for standard)
Position 2-4:   Customer/Area Code (e.g., 'USA')
Position 5:     Section Code
Position 6:     Subsection Code
Position 7+:    Section-specific data
```

## Section Codes

| Code | Description |
|------|-------------|
| P | Airport (and related) |
| D | NAVAID (VOR, NDB, etc.) |
| E | Enroute |
| H | Heliport |
| T | Company Routes |
| U | Airspace |

## Airport (P) Subsection Codes

| Subsection | Description |
|------------|-------------|
| A | Airport Reference Point |
| B | Airport Gates |
| C | Airport Terminal Waypoints |
| D | SID (Standard Instrument Departure) |
| E | STAR (Standard Terminal Arrival Route) |
| F | Approach Procedure |
| G | Runway |
| I | ILS/MLS Localizer |
| K | TAA (Terminal Arrival Altitude) |
| L | MLS Approach |
| N | Terminal NDB |
| P | Path Point |
| R | Runway Threshold |
| S | MSA (Minimum Sector Altitude) |
| T | GLS (GBAS Landing System) |
| V | Communication |

## Path Termination (Leg Types)

| Code | Name | Description |
|------|------|-------------|
| IF | Initial Fix | Defines start of procedure |
| TF | Track to Fix | Track from previous fix to this fix |
| CF | Course to Fix | Fly specified course to fix |
| DF | Direct to Fix | Direct course to fix |
| FA | Fix to Altitude | Track to fix, then climb to altitude |
| FC | Track from Fix (Distance) | Track from fix for specified distance |
| FD | Track from Fix (DME) | Track from fix to DME distance |
| FM | From Fix to Manual | Track from fix until manual termination |
| CA | Course to Altitude | Fly course until reaching altitude |
| CD | Course to DME | Fly course until DME distance |
| CI | Course to Intercept | Fly course to intercept next leg |
| CR | Course to Radial | Fly course until intercepting radial |
| RF | Constant Radius Arc | Fixed-radius arc to fix |
| AF | DME Arc to Fix | DME arc to fix |
| VA | Heading to Altitude | Fly heading until altitude |
| VD | Heading to DME | Fly heading until DME distance |
| VI | Heading to Intercept | Fly heading to intercept |
| VM | Heading to Manual | Fly heading until manual termination |
| VR | Heading to Radial | Fly heading until intercepting radial |
| PI | Procedure Turn | Course reversal procedure |
| HA | Racetrack (Alt Terminate) | Holding to altitude |
| HF | Racetrack (Fix Terminate) | Holding until over fix |
| HM | Racetrack (Manual) | Holding until manual termination |

## Route Types

| Code | Procedure Type | Description |
|------|----------------|-------------|
| 0 | SID/STAR | Engine Out SID |
| 1 | SID | Standard Runway Transition |
| 2 | SID | Standard Common Route |
| 3 | SID | Standard Enroute Transition |
| 4 | SID | RNAV Runway Transition |
| 5 | SID | RNAV Common Route |
| 6 | SID | RNAV Enroute Transition |
| 7 | SID/STAR | FMS Runway Transition |
| 8 | SID/STAR | FMS Common Route |
| 9 | SID/STAR | FMS Enroute Transition |
| A | Approach | Approach Transition |
| B | Approach | Localizer/Back Course |
| D | Approach | VOR/DME |
| F | Approach | FMS |
| G | Approach | IGS |
| H | Approach | Helicopter |
| I | Approach | ILS |
| J | Approach | GLS |
| L | Approach | LOC Only |
| M | Approach | MLS |
| N | Approach | NDB |
| P | Approach | GPS |
| Q | Approach | NDB/DME |
| R | Approach | RNAV |
| S | Approach | VOR/TACAN |
| T | Approach | TACAN |
| U | Approach | SDF |
| V | Approach | VOR |
| W | Approach | MLS Type A |
| X | Approach | LDA |
| Y | Approach | MLS Type B/C |
| Z | Approach | Missed Approach |

## Altitude Description Codes

| Code | Description |
|------|-------------|
| + | At or above altitude |
| - | At or below altitude |
| @ | At altitude |
| B | Between altitudes (alt1 to alt2) |
| C | At or above alt1, at or below alt2 |
| G | Glide slope altitude (MSL) |
| H | At or above alt1, glide slope alt2 |
| I | Glide slope intercept |
| J | Glide slope at alt1, at or above alt2 |
| V | Altitude for vertical navigation |
| X | At alt1, on glide slope at alt2 |
| Y | At or below alt1, on glide slope at alt2 |
| (blank) | No altitude specified |

## Waypoint Description Codes

4-character code describing waypoint:

| Position | Values | Meaning |
|----------|--------|---------|
| 1 | A | Airport as waypoint |
| 1 | E | Essential waypoint |
| 1 | F | Off-airway floating waypoint |
| 1 | G | Runway as waypoint |
| 1 | H | Heliport as waypoint |
| 1 | N | NDB NAVAID as waypoint |
| 1 | P | Phantom waypoint |
| 1 | R | Non-essential waypoint |
| 1 | T | Transition waypoint |
| 1 | V | VHF NAVAID as waypoint |
| 2 | A | Final approach fix |
| 2 | B | Initial approach fix, final approach fix |
| 2 | C | Initial approach fix, intermediate fix |
| 2 | D | Intermediate fix |
| 2 | E | Off-route intersection |
| 2 | F | Off-route intersection, final approach fix |
| 2 | I | Initial approach fix |
| 2 | M | Missed approach point |
| 2 | P | Oceanic entry/exit point |
| 2 | U | FIR/UIR or control boundary |
| 3 | A | Unnamed charted intersection |
| 3 | B | Bearing/distance fix, MAP |
| 3 | C | Charted NAVAID intersection |
| 3 | D | Database-named waypoint |
| 3 | G | Bearing/distance from NAVAID |
| 3 | M | Middle marker |
| 3 | N | NAVAID |
| 3 | O | Outer marker |
| 3 | R | Named intersection |
| 3 | U | Unnamed non-charted intersection |
| 4 | E | End of SID/STAR route |
| 4 | F | FAF |
| 4 | H | Holding fix |
| 4 | R | Required altitude |
| 4 | Y | Flyover waypoint |

## Parsing Example

```python
# Parse CIFP line (132 bytes)
line = "SUSAP KLAXKLAX  011..."  # Example

record_type = line[0]           # 'S'
area_code = line[1:4]           # 'USA'
section = line[4]               # 'P' (Airport)
subsection = line[12]           # 'F' (Approach)
airport_id = line[6:10]         # 'KLAX'
procedure_id = line[13:19]      # 'ILS25L'
path_term = line[47:49]         # 'TF'
fix_id = line[29:34]            # 'LIMMA'
altitude1 = line[84:89]         # '02500'
```
