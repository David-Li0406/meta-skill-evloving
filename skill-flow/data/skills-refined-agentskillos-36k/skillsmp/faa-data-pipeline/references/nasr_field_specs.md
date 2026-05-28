# NASR Field Specifications

Field positions and formats for FAA NASR fixed-width files.

## APT.txt (Airport Data)

| Field | Start | End | Length | Description |
|-------|-------|-----|--------|-------------|
| Record Type | 1 | 3 | 3 | Always "APT" |
| Facility Site Number | 4 | 14 | 11 | Unique identifier |
| Facility Type | 15 | 27 | 13 | AIRPORT, HELIPORT, etc. |
| Location ID | 28 | 31 | 4 | FAA identifier (e.g., LAX) |
| Effective Date | 32 | 41 | 10 | MM/DD/YYYY |
| FAA Region | 42 | 44 | 3 | AWP, ASW, etc. |
| State Code | 49 | 50 | 2 | Two-letter state code |
| State Name | 51 | 70 | 20 | Full state name |
| County Name | 71 | 91 | 21 | County name |
| City Name | 94 | 133 | 40 | Associated city |
| Facility Name | 134 | 183 | 50 | Official airport name |
| Ownership Type | 184 | 185 | 2 | PU=Public, PR=Private |
| Use Type | 186 | 187 | 2 | PU=Public, PR=Private |
| Latitude (DMS) | 524 | 538 | 15 | DD-MM-SS.SSSN |
| Latitude (Secs) | 539 | 550 | 12 | High-precision seconds |
| Longitude (DMS) | 551 | 565 | 15 | DDD-MM-SS.SSSW |
| Longitude (Secs) | 566 | 578 | 13 | High-precision seconds |
| Elevation | 580 | 586 | 7 | Tenths of feet MSL |
| Magnetic Variation | 588 | 590 | 3 | Degrees |
| Mag Var Direction | 591 | 591 | 1 | E or W |
| Pattern Altitude | 596 | 599 | 4 | AGL in feet |
| Sectional Chart | 600 | 629 | 30 | Chart name |
| ICAO Identifier | 1211 | 1217 | 7 | 4-letter ICAO code |

## RWY.txt (Runway Data)

| Field | Start | End | Length | Description |
|-------|-------|-----|--------|-------------|
| Record Type | 1 | 3 | 3 | Always "RWY" |
| Facility Site Number | 4 | 14 | 11 | Links to APT |
| Runway ID | 17 | 23 | 7 | e.g., "09/27" |
| Runway Length | 24 | 28 | 5 | Feet |
| Runway Width | 29 | 32 | 4 | Feet |
| Surface Type | 33 | 44 | 12 | ASPH, CONC, TURF, etc. |
| Base End ID | 66 | 68 | 3 | e.g., "09" |
| Base True Heading | 69 | 71 | 3 | Degrees |
| Base Latitude | 89 | 103 | 15 | Threshold lat |
| Base Longitude | 116 | 130 | 15 | Threshold lon |
| Base Elevation | 144 | 150 | 7 | Tenths of feet |
| Base TORA | 162 | 166 | 5 | Takeoff Run Available |
| Base TODA | 167 | 171 | 5 | Takeoff Distance Available |
| Base ASDA | 172 | 176 | 5 | Accelerate Stop Distance |
| Base LDA | 177 | 181 | 5 | Landing Distance Available |

## NAV.txt (NAVAID Data)

| Field | Start | End | Length | Description |
|-------|-------|-----|--------|-------------|
| Record Type | 1 | 4 | 4 | NAV1, NAV2, etc. |
| Facility ID | 5 | 8 | 4 | NAVAID identifier |
| Facility Type | 9 | 28 | 20 | VOR, VORTAC, NDB, etc. |
| Name | 43 | 72 | 30 | NAVAID name |
| City | 73 | 112 | 40 | City |
| State Code | 113 | 114 | 2 | State |
| Latitude (DMS) | 372 | 385 | 14 | Position |
| Longitude (DMS) | 398 | 412 | 15 | Position |
| Elevation | 456 | 462 | 7 | Tenths of feet |
| Magnetic Variation | 463 | 467 | 5 | DDDDX format |
| Frequency | 519 | 524 | 6 | MHz or kHz |
| TACAN Channel | 515 | 518 | 4 | Channel number |

## FIX.txt (Fix/Waypoint Data)

| Field | Start | End | Length | Description |
|-------|-------|-----|--------|-------------|
| Record Type | 1 | 4 | 4 | FIX1, FIX2, etc. |
| Fix ID | 5 | 34 | 30 | Fix identifier |
| State Code | 35 | 36 | 2 | State |
| Latitude (DMS) | 39 | 52 | 14 | Position |
| Longitude (DMS) | 67 | 81 | 15 | Position |
| Category | 97 | 99 | 3 | MIL, CIV, etc. |
| ARTCC High | 122 | 125 | 4 | Controlling ARTCC |
| Fix Use | 130 | 144 | 15 | RNAV, etc. |

## TWR.txt (Tower/Frequency Data)

| Field | Start | End | Length | Description |
|-------|-------|-----|--------|-------------|
| Record Type | 1 | 4 | 4 | TWR1, TWR3, etc. |
| Terminal ID | 5 | 8 | 4 | Facility ID |
| Facility Site Number | 19 | 29 | 11 | Links to APT |
| Facility Name | 105 | 154 | 50 | Airport name |
| Facility Type | 218 | 229 | 12 | ATCT, NON-ATCT |

### TWR3 (Frequency) Fields

| Field | Start | End | Length | Description |
|-------|-------|-----|--------|-------------|
| Frequency Use | 9 | 23 | 15 | ATIS, GND, TWR, etc. |
| Frequency | 24 | 67 | 44 | Frequency value(s) |
| Sectorization | 69 | 138 | 70 | Sector description |

## AWY.txt (Airway Data)

| Field | Start | End | Length | Description |
|-------|-------|-----|--------|-------------|
| Record Type | 1 | 4 | 4 | AWY1, AWY2 |
| Airway ID | 5 | 9 | 5 | V1, J146, T100, etc. |
| Sequence Number | 14 | 18 | 5 | Segment order |
| From Fix | 19 | 48 | 30 | Start fix name |
| To Fix | 53 | 82 | 30 | End fix name |
| MEA | 87 | 91 | 5 | Min Enroute Alt (100s ft) |
| Distance | 108 | 111 | 4 | Segment distance NM |

## DOF.DAT (Obstacle Data)

| Field | Start | End | Length | Description |
|-------|-------|-----|--------|-------------|
| OAS Number | 1 | 9 | 9 | Unique identifier |
| Country | 20 | 21 | 2 | US |
| State | 23 | 24 | 2 | State code |
| City | 26 | 41 | 16 | City name |
| Latitude | 43 | 54 | 12 | DD-MM-SS.SSX |
| Longitude | 56 | 68 | 13 | DDD-MM-SS.SSX |
| Obstacle Type | 70 | 87 | 18 | TOWER, BLDG, etc. |
| AGL Height | 91 | 95 | 5 | Feet AGL |
| MSL Height | 97 | 101 | 5 | Feet MSL |
| Lighting | 103 | 103 | 1 | R, D, W, N, etc. |

## Coordinate Format

NASR uses sexagesimal (DMS) format:
- Latitude: `DD-MM-SS.SSSN` or `DD-MM-SS.SSSS`
- Longitude: `DDD-MM-SS.SSSW` or `DDD-MM-SS.SSSW`

Where:
- DD/DDD = Degrees
- MM = Minutes
- SS.SSS = Seconds with decimal
- N/S/E/W = Direction

### Conversion to Decimal Degrees

```python
decimal = degrees + (minutes / 60) + (seconds / 3600)
if direction in ('S', 'W'):
    decimal = -decimal
```
