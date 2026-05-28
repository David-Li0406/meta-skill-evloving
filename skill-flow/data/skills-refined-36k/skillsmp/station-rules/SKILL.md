---
name: station-rules
description: Station development patterns and best practices for js/stations
files: ["js/stations/**"]
---

# Station Development Rules

When working on files in `js/stations/`, follow these established patterns to maintain consistency across all stations.

## File Organization

**Each station must have its own file.** Do not combine multiple stations in a single file. Create a new file following the naming convention below.

## Naming Conventions

1. **File name**: Use lowercase, single word (e.g., `helm.js`, `comms.js`, `navigation.js`, `tactical.js`)
2. **Class name**: PascalCase with "Station" suffix (e.g., `HelmStation`, `CommsStation`, `NavigationStation`)
3. **Export name**: camelCase with "Station" suffix (e.g., `helmStation`, `commsStation`, `navigationStation`)

## Required Structure

Every station class must implement the following pattern:

```javascript
/**
 * [Station Name] Station
 * [Brief description of station purpose]
 */

import { gameState } from '../core/state.js';
import { renderer } from '../core/renderer.js';  // Only if using canvas
import { audio } from '../core/audio.js';

class [StationName]Station {
    constructor() {
        this.container = null;
        // Add station-specific properties here
    }

    init(container) {
        this.container = container;
        this.render();
        this.setupEventListeners();
    }

    render() {
        // Generate HTML structure
        this.container.innerHTML = `...`;
    }

    setupEventListeners() {
        // Attach all event listeners
    }

    update(timestamp) {
        // Called every frame for game loop updates
    }

    destroy() {
        // Cleanup when station is switched away
    }
}

export const [stationname]Station = new [StationName]Station();
```

## Required Methods

1. **`init(container)`**: Initialize the station with a DOM container. Must call `render()` and `setupEventListeners()`.
2. **`render()`**: Generate and insert the station's HTML structure into `this.container`.
3. **`setupEventListeners()`**: Attach all DOM event listeners. Called once during initialization.
4. **`update(timestamp)`**: Called every frame by the simulation loop. Update displays, animations, and game state.
5. **`destroy()`**: Cleanup method called when switching stations. Remove listeners, clear intervals, etc.

## Layout Structure

All stations should use the `station-layout` class with a station-specific layout class:

```html
<div class="station-layout [stationname]-layout">
    <!-- Station content -->
</div>
```

Examples: `helm-layout`, `comms-layout`, `tactical-layout`, etc.

## Registration

After creating a new station file, register it in `js/main.js`:

1. Add import: `import { [stationname]Station } from './stations/[stationname].js';`
2. Add to stations registry: `[stationname]: [stationname]Station,`
3. Add corresponding tab in `index.html` if needed

## Common Patterns

- **Canvas usage**: If the station uses a canvas, store it as `this.canvas` and initialize with `renderer.init(this.canvas)`
- **State listeners**: Use `gameState.on('eventName', callback)` for reactive updates
- **Audio feedback**: Use `audio.playClick()`, `audio.playBeep()`, `audio.playError()`, etc. for user interactions
- **Update frequency**: In `update()`, use timestamp-based checks to avoid excessive updates (e.g., `if (Math.floor(timestamp / 500) % 2 === 0)`)

## Best Practices

- Keep station logic self-contained within the class
- Use descriptive method names that indicate purpose
- Handle edge cases (null checks, disabled states, etc.)
- Follow the existing visual style and UI patterns
- Ensure proper cleanup in `destroy()` to prevent memory leaks
