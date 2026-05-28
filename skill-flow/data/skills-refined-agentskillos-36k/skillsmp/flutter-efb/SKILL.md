---
name: flutter-efb
description: Flutter development patterns for aviation Electronic Flight Bag (EFB) applications. Use when building moving map displays, aviation calculations, offline-first architectures, BLoC state management, or implementing EFB-specific UI patterns like day/night themes and flight instruments.
---

# Flutter EFB Development

## Overview

Patterns, algorithms, and best practices for building Electronic Flight Bag applications with Flutter.

## Quick Start

### Create a New Feature
```bash
python scripts/create_feature.py --name weather --bloc
```

### Create a Domain Entity
```bash
python scripts/create_entity.py --name Airport --fields "id:String,name:String,lat:double,lon:double"
```

## Architecture

MagentaLine follows Clean Architecture with three layers:

```
┌─────────────────────────────────────────┐
│           Presentation Layer            │
│     (Widgets, BLoCs, ViewModels)        │
├─────────────────────────────────────────┤
│             Domain Layer                │
│  (Entities, Use Cases, Repositories)    │
├─────────────────────────────────────────┤
│              Data Layer                 │
│ (Data Sources, Models, Implementations) │
└─────────────────────────────────────────┘
```

See `references/architecture.md` for detailed documentation.

## Aviation Math

Core calculations for flight planning and navigation:

- **Haversine Distance** - Great circle distance between coordinates
- **Initial Bearing** - True bearing from point A to B
- **Wind Correction Angle** - Heading adjustment for wind
- **Ground Speed** - Actual speed over ground with wind
- **Density Altitude** - Pressure altitude corrected for temperature
- **Magnetic Variation** - Conversion between true and magnetic headings

See `references/navigation_math.md` for formulas and implementations.

## Key Features

### Moving Map
- flutter_map with MBTiles offline tiles
- SpatiaLite queries for nearby features
- Real-time GPS tracking

### Offline First
- SQLite for aviation data
- MBTiles for chart tiles
- Cached weather data

### Day/Night Themes
- Automatic switching based on sun position
- High contrast cockpit-friendly colors
- Red-tinted night mode

### State Management
- BLoC pattern for complex features
- Riverpod for simple state
- Event-driven architecture

## Dependencies

See `assets/pubspec_template.yaml` for recommended dependencies:
- `flutter_bloc` - State management
- `flutter_map` - Moving map display
- `sqlite3_flutter_libs` - SQLite support
- `geolocator` - GPS access
- `freezed` - Immutable models

## References

| Document | Description |
|----------|-------------|
| `references/architecture.md` | Clean Architecture patterns |
| `references/navigation_math.md` | Aviation calculations |
| `references/map_integration.md` | flutter_map setup |
| `references/bloc_patterns.md` | BLoC best practices |
| `references/offline_first.md` | Offline architecture |
| `references/widget_catalog.md` | Common EFB widgets |
