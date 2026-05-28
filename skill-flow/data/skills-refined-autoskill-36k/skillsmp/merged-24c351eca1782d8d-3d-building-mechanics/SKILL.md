---
name: 3d-building-mechanics
description: Use this skill when developing survival, crafting, or sandbox games with player-constructed structures in Three.js, incorporating spatial indexing, structural physics, and multiplayer networking.
---

# 3D Building Mechanics

Complete building system for Three.js games with performance optimization, structural physics, and multiplayer networking.

## When to Use This Skill

Use when building:
- Survival/crafting games with base building
- Creative sandbox games
- Multiplayer construction games
- Any 3D building mechanics in Three.js

## Quick Start

```javascript
import { SpatialHashGrid } from './scripts/spatial-hash-grid.js';
import { HeuristicValidator } from './scripts/heuristic-validator.js';
import { ClientPrediction } from './scripts/client-prediction.js';

// Set up spatial indexing
const spatialIndex = new SpatialHashGrid(10);
spatialIndex.insert(piece, piece.position);
const nearby = spatialIndex.queryRadius(position, 15);

// Set up structural validation (Rust/Valheim style)
const validator = new HeuristicValidator({ mode: 'heuristic' });
validator.addPiece(piece);
const canPlace = validator.validatePlacement(newPiece);

// For multiplayer - client prediction
const prediction = new ClientPrediction(buildingSystem);
```

## Reference Files

Read these for detailed implementation guidance:

- `references/performance-at-scale.md` - Spatial partitioning, chunk loading, instancing
- `references/structural-physics-advanced.md` - Arcade vs heuristic vs realistic physics
- `references/multiplayer-networking.md` - Authority models, delta sync, conflict resolution

## Scripts

### Performance
- `scripts/spatial-hash-grid.js` - O(1) queries for uniform distribution
- `scripts/octree.js` - Adaptive queries for clustered bases
- `scripts/chunk-manager.js` - World streaming for large maps
- `scripts/performance-profiler.js` - Benchmarking utilities

### Structural Physics
- `scripts/heuristic-validator.js` - Fast validation (Fortnite/Rust/Valheim modes)
- `scripts/stability-optimizer.js` - Caching and batch updates
- `scripts/damage-propagation.js` - Damage states, cascading collapse
- `scripts/physics-engine-lite.js` - Optional realistic physics

### Multiplayer
- `scripts/delta-compression.js` - Only send changed state
- `scripts/client-prediction.js` - Optimistic placement with rollback
- `scripts/conflict-resolver.js` - Handle simultaneous builds
- `scripts/building-network-manager.js` - Complete server/client system

## Key Patterns

### Spatial Indexing Selection
| Pieces | Distribution | Use |
|--------|-------------|-----|
| <1,000 | Any | Array |
| 1-5k | Uniform | SpatialHashGrid |
| 1-5k | Clustered | Octree |
| 5k+ | Any | ChunkManager + Octree |

### Physics Mode Selection
- **Arcade** (Fortnite): Connectivity only, instant collapse, best for combat
- **Heuristic** (Rust/Valheim): Stability %, predictable, best for survival
- **Realistic**: Full stress/strain, expensive, best for engineering sims

### Multiplayer Pattern
Server-authoritative with client prediction. Use delta compression for sync and conflict resolution strategies such as first-write, timestamp, or lock-based methods.