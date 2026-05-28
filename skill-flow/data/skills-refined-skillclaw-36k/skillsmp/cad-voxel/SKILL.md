---
name: cad-voxel
description: Create Crossy Road style isometric voxel art using AI-Native CAD. Use this when users request creating voxel characters, vehicles, buildings, or scenes with the CAD system. This skill teaches how to use CAD MCP tools (glob, read, edit, write, lsp, bash) instead of standard file tools.
---

# CAD Voxel Art Skill

Create Crossy Road style isometric voxel art with AI-Native CAD.

## Critical Rules

### Use CAD MCP Tools Only

**Never use standard Read/Write/Glob tools for CAD files.** Always use these MCP tools:

| MCP Tool | Purpose | Instead of |
|----------|---------|------------|
| `mcp__ai-native-cad__glob` | List CAD files | Glob |
| `mcp__ai-native-cad__read` | Read CAD code | Read |
| `mcp__ai-native-cad__edit` | Edit + auto-run | Edit |
| `mcp__ai-native-cad__write` | Write + auto-run | Write |
| `mcp__ai-native-cad__lsp` | Explore functions | - |
| `mcp__ai-native-cad__bash` | Scene commands | Bash |

> **Note**: In examples below, `glob()`, `read()`, etc. are shorthand for the full MCP tool names above.

### ES5 Syntax Only

CAD engine only supports ES5. Use `var`, not `const`/`let`. No arrow functions or template literals.

```javascript
// Correct
var name = 'entity_' + id;
function create(x, y) { return x + y; }

// Wrong
const name = `entity_${id}`;
const create = (x, y) => x + y;
```

## Quick Start Workflow

```javascript
// 1. Check existing code
glob()
read({ file: 'main' })

// 2. Explore available functions
lsp({ operation: 'domains' })
lsp({ operation: 'describe', domain: 'primitives' })
lsp({ operation: 'schema', name: 'drawCircle' })

// 3. Write code (auto-executes)
write({ file: 'main', code: "drawCircle('sun', 0, 100, 30)" })

// 4. Verify result
bash({ command: 'capture' })
bash({ command: 'entity', name: 'sun' })

// 5. Edit if needed (auto-executes, old_code must match exactly)
edit({ file: 'main', old_code: "drawCircle('sun', 0, 100, 30)", new_code: "drawCircle('sun', 0, 100, 50)" })
```

## Design Workflow

Before coding:
1. `lsp({ operation: 'symbols', file: 'main' })` - Check main for similar code
   - Or use `file: '<module_name>'` from `glob()` results
2. Propose approach to user: extend existing vs create new
3. Get confirmation before implementing

During coding:
- 3rd similar pattern? Ask: "Should we abstract this?"
- 2nd patch fix? Ask: "Structural issue - refactor?"

After coding:
- `bash({ command: 'capture' })` - Visual verification
- Ask: "Can we add X with this design?"

## Z-Order Patterns

### Internal Z-Order (Within Objects)

Create parts back-to-front, then apply explicit `drawOrder()`:

```javascript
function car(id, x, y) {
  var n = 'car_' + id;

  // 1. Back parts first (will be occluded)
  box3d(n + '_wheel_back', x, y + 12, ...);

  // 2. Body
  box3d(n + '_body', x, y, ...);

  // 3. Front parts last (visible)
  box3d(n + '_wheel_front', x, y - 12, ...);

  // 4. Explicit z-order (required!)
  var parts = [n + '_wheel_back', n + '_body', n + '_wheel_front'];
  for (var i = 0; i < parts.length; i++) {
    drawOrder(parts[i], 'front');
  }

  // 5. Group
  createGroup(n, parts);
}
```

### Isometric Group Z-Order

Use `depth = x + y` algorithm, sort descending:

```javascript
var isoGroups = [];

function registerIsoGroup(name, x, y) {
  isoGroups.push({ name: name, depth: x + y });
}

function sortIsoGroups() {
  isoGroups.sort(function(a, b) { return b.depth - a.depth; });
  for (var i = 0; i < isoGroups.length; i++) {
    drawOrder(isoGroups[i].name, 'front');
  }
}

// Usage
tree('tree_0', -240, -150);
registerIsoGroup('tree_0', -240, -150);

car('car_0', -160, -100);
registerIsoGroup('car_0', -160, -100);

sortIsoGroups(); // Call once after all objects
```

## Coordinate System

### Local Coordinates for Groups

Place parts at local origin (0,0), then translate the group:

```javascript
function makeCharacter(name, worldX, worldY) {
  // All parts at local coordinates
  box3d(name + '_body', 0, 0, 20, 30, 15, ...);
  box3d(name + '_head', 0, 0, 15, 15, 12, ...);

  createGroup(name, [name + '_body', name + '_head']);

  // Move group to world position
  translate(name, worldX, worldY);
}
```

### Scale in Groups

When scaling group children, use `space: 'local'`:

```javascript
// Correct
scale(name + '_head', 1.2, 1.2, { space: 'local' });

// Wrong - position also changes!
scale(name + '_head', 1.2, 1.2);
```

## Color Palette

```javascript
var PALETTE = {
  grass: [0.4, 0.8, 0.3, 1],
  road: [0.3, 0.3, 0.35, 1],
  water: [0.2, 0.5, 0.8, 1],
  wood: [0.5, 0.35, 0.2, 1],
  skin: [1.0, 0.85, 0.7, 1],
  red: [0.9, 0.2, 0.2, 1],
  white: [1, 1, 1, 1],
  black: [0, 0, 0, 1]
};

// Apply: setFill('entity', PALETTE.grass);
```

## Common Commands

```javascript
// Scene info
bash({ command: 'info' })        // Entity count, bounds
bash({ command: 'tree' })        // Hierarchy
bash({ command: 'groups' })      // Group list
bash({ command: 'draw_order' })  // Z-order (root)
bash({ command: 'draw_order', group: 'robot' }) // Group internal

// Entity coordinates
bash({ command: 'entity', name: 'chicken_body' })
// Returns: { local: {...}, world: { bounds, center } }

// Export
bash({ command: 'capture' })     // PNG screenshot
bash({ command: 'svg' })         // SVG vector
bash({ command: 'json' })        // JSON

// ⚠️ Reset - DESTRUCTIVE! Clears all scene data.
// Cannot be recovered by undo/redo. Export or snapshot first!
bash({ command: 'reset' })
```

## References

For detailed function documentation, see:
- `references/tools-mcp.md` - MCP tool details
- `references/functions-primitives.md` - Shape functions
- `references/functions-transforms.md` - Transform functions
- `references/functions-style.md` - Style and group functions
