---
name: vor-anachb
description: Use this skill when you need to query real-time departures, plan routes, or check service disruptions for Austrian public transport, including trains, buses, trams, and metro (U-Bahn).
---

# VOR AnachB - Austrian Public Transport API

Query Austrian public transport for real-time departures, route planning, and service disruptions using the HAFAS API.

## Quick Reference

| Script | Purpose |
|--------|---------|
| `search.sh` | Find stations/stops by name |
| `departures.sh` | Real-time departures at a station |
| `route.sh` | Plan a trip between two locations |
| `disruptions.sh` | Current service disruptions |

**API:** HAFAS (Hacon Fahrplan-Auskunfts-System)  
**Endpoint:** `https://vao.demo.hafas.de/gate`

---

## 1. Search Stations/Stops

Find station IDs by name:

```bash
./search.sh "Stephansplatz"
./search.sh "Wien Hauptbahnhof"
./search.sh "Linz"
./search.sh "Salzburg Hbf"
```

Returns station names, IDs (extId), and coordinates.

**Response fields:**
- `name`: Station name
- `extId`: Station ID for use in other queries
- `type`: S (Station), A (Address), P (POI)
- `coordinates`: WGS84 coordinates (lon/lat in 1e-6 format)

---

## 2. Real-Time Departures

Get next departures from a station:

```bash
./departures.sh <station-id> [count]

# Examples:
./departures.sh 490132000        # Wien Stephansplatz, 10 departures
./departures.sh 490132000 20     # Wien Stephansplatz, 20 departures
./departures.sh 490060200        # Wien Hauptbahnhof
./departures.sh 444130000        # Linz Hbf
./departures.sh 455000100        # Salzburg Hbf
```

**Response fields:**
- `line`: Line name (U1, S1, RJ, etc.)
- `direction`: Final destination
- `departure`: Scheduled departure time
- `delay`: Delay in minutes (if any)
- `platform`: Platform/track number

---

## 3. Route Planning

Plan a trip between two stations:

```bash
./route.sh <from-id> <to-id> [results]

# Examples:
./route.sh 490132000 490060200        # Stephansplatz → Hauptbahnhof
./route.sh 490132000 444130000 5      # Wien → Linz, 5 results
./route.sh "Graz Hbf" "Wien Hbf"      # Search by name (slower)
```

**Response fields:**
- `departure`: Departure time
- `arrival`: Arrival time
- `duration`: Trip duration
- `changes`: Number of transfers
- `legs`: Array of trip segments with line info

---

## 4. Disruptions

Check current service disruptions:

```bash
./disruptions.sh
```

Returns a list of current service disruptions affecting the public transport network.