# Hexgrid Algorithms

Hexagonal grid mathematics, coordinate systems, pathfinding, and spatial algorithms.

## Expertise

This skill provides deep knowledge in:

- **Coordinate Systems**: Axial, cube, offset, doubled
- **Hex Math**: Distance, neighbors, rings, lines
- **Pathfinding**: A* on hex grids, movement costs
- **Field of View**: Visibility, fog of war
- **Area Effects**: Spreading, range calculations
- **Map Generation**: Procedural hex terrain
- **Coordinate Conversion**: Between different systems

## When to Use

Invoke this skill when you need to:

- Implement a hex-based map system
- Calculate distances on hex grids
- Find paths between hex cells
- Implement area-of-effect abilities
- Generate hex terrain
- Convert between coordinate systems

## Coordinate Systems

### Axial Coordinates (Recommended)

```
      _____
     /     \
    /  0,-1 \
   /    ↑    \
  /     |     \
  \  -1,0 ← → 1,0  /
   \     |     /
    \  0,1   /
     \_____/
```

```typescript
type AxialCoord = { q: number; r: number };
```

### Cube Coordinates

```typescript
type CubeCoord = { x: number; y: number; z: number };
// Constraint: x + y + z = 0
```

### Conversions

```typescript
// Axial to Cube
function axialToCube(hex: AxialCoord): CubeCoord {
  return { x: hex.q, y: -hex.q - hex.r, z: hex.r };
}

// Cube to Axial
function cubeToAxial(cube: CubeCoord): AxialCoord {
  return { q: cube.x, r: cube.z };
}
```

## Essential Algorithms

### Distance

```typescript
function hexDistance(a: AxialCoord, b: AxialCoord): number {
  return (Math.abs(a.q - b.q)
        + Math.abs(a.q + a.r - b.q - b.r)
        + Math.abs(a.r - b.r)) / 2;
}
```

### Neighbors

```typescript
const DIRECTIONS = [
  { q: 1, r: 0 },  { q: 1, r: -1 }, { q: 0, r: -1 },
  { q: -1, r: 0 }, { q: -1, r: 1 }, { q: 0, r: 1 },
];

function getNeighbors(hex: AxialCoord): AxialCoord[] {
  return DIRECTIONS.map(d => ({ q: hex.q + d.q, r: hex.r + d.r }));
}
```

### Ring

```typescript
function hexRing(center: AxialCoord, radius: number): AxialCoord[] {
  if (radius === 0) return [center];

  const results: AxialCoord[] = [];
  let hex = { q: center.q - radius, r: center.r + radius };

  for (let i = 0; i < 6; i++) {
    for (let j = 0; j < radius; j++) {
      results.push({ ...hex });
      hex = getNeighbor(hex, i);
    }
  }
  return results;
}
```

### A* Pathfinding

```typescript
function findPath(
  start: AxialCoord,
  goal: AxialCoord,
  isPassable: (hex: AxialCoord) => boolean
): AxialCoord[] {
  // Priority queue, came_from map, cost tracking
  // Standard A* with hexDistance as heuristic
}
```

## Pixel Conversion

### Hex to Pixel (Pointy-Top)

```typescript
const SIZE = 32; // hex radius in pixels

function hexToPixel(hex: AxialCoord): { x: number; y: number } {
  const x = SIZE * (Math.sqrt(3) * hex.q + Math.sqrt(3)/2 * hex.r);
  const y = SIZE * (3/2 * hex.r);
  return { x, y };
}
```

### Pixel to Hex

```typescript
function pixelToHex(x: number, y: number): AxialCoord {
  const q = (Math.sqrt(3)/3 * x - 1/3 * y) / SIZE;
  const r = (2/3 * y) / SIZE;
  return hexRound({ q, r });
}
```

## Common Patterns

### Farmland Layout
- Hex grid for crop plots
- 6 neighbors = 6 adjacent plots
- Natural for irrigation spread

### Movement Range
- Ring algorithm for movement display
- Pathfinding for actual movement
- Terrain costs per hex type

### Area Effects
- Flood fill for spreading effects
- Ring for radius-based abilities

## Integration

This skill works alongside:

- `drizzle-game-schema` - Storing hex map data
- `react-game-ui` - Rendering hex grids
- `game-concept-advisor` - Hex-based mechanics

## Usage in Claude Code

```
/hexgrid-algorithms

"Implement A* pathfinding on a hex grid..."
"Calculate all hexes within range 3..."
"Convert pixel clicks to hex coordinates..."
```
