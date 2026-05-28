# Browser DevTools Reference

## Opening DevTools

| Browser | Shortcut |
|---------|----------|
| Chrome/Edge | F12 or Ctrl+Shift+I |
| Firefox | F12 or Ctrl+Shift+I |
| Safari | Cmd+Option+I (enable in Preferences first) |

## Elements/Inspector Panel

### Purpose
Inspect and modify HTML/CSS in real-time.

### Key Features
```
- Select element: Ctrl+Shift+C then click
- Edit HTML: Double-click element
- Edit attributes: Double-click attribute
- Delete element: Select and press Delete
- Copy selector: Right-click → Copy → Copy selector
- Force state: Right-click → Force state (:hover, :active, etc.)
```

### Styles Pane
```
- View computed styles
- See which CSS file/line sets each property
- Strikethrough = overridden
- Add new styles in element.style {}
- Toggle properties with checkbox
```

### Box Model
```
- Shows margin/border/padding/content
- Click to edit values
- Blue highlight on page shows area
```

## Console Panel

### Purpose
View logs, errors, and run JavaScript.

### Filtering
```
- Errors only: Click red circle or type "error"
- Warnings only: Click yellow triangle
- By source: Click dropdown or type source name
- Regex: /pattern/
```

### Useful Commands
```javascript
// Clear console
console.clear()
// Or press Ctrl+L

// Log with formatting
console.log('%c Bold Red', 'color: red; font-weight: bold')

// Table format
console.table([{a: 1, b: 2}, {a: 3, b: 4}])

// Group logs
console.group('My Group')
console.log('Inside group')
console.groupEnd()

// Time measurement
console.time('operation')
// ... do stuff ...
console.timeEnd('operation')

// Stack trace
console.trace('Where am I?')

// Assert (logs only if false)
console.assert(x > 0, 'x should be positive')
```

### Quick Selection
```javascript
// Last selected element
$0

// Previous selections
$1, $2, $3, $4

// Query selector (shorthand for document.querySelector)
$('selector')
$$('selector')  // querySelectorAll as array
```

## Network Panel

### Purpose
Monitor HTTP requests/responses.

### Key Columns
```
- Name: URL (click to see details)
- Status: HTTP status code
- Type: Resource type (XHR, JS, CSS, etc.)
- Initiator: What triggered the request
- Size: Transfer size
- Time: Request duration
- Waterfall: Visual timing
```

### Filtering
```
- By type: Click filter buttons (XHR, JS, CSS, Img, etc.)
- By text: Type in filter box
- By status: status-code:200 or status-code:500
- By domain: domain:api.example.com
- Regex: /pattern/
- Negative: -domain:cdn.example.com
```

### Detailed View (click request)
```
Headers tab:
- Request URL, method, status
- Request headers (what browser sent)
- Response headers (what server returned)

Payload tab:
- Query string parameters
- Request body

Preview tab:
- Formatted response

Response tab:
- Raw response body

Timing tab:
- Breakdown of request phases
```

### Useful Features
```
- Preserve log: Keep logs across page loads
- Disable cache: Force fresh requests
- Throttling: Simulate slow network
- Copy as cURL: Right-click → Copy → Copy as cURL
- Block request: Right-click → Block request URL
```

## Sources/Debugger Panel

### Purpose
Debug JavaScript with breakpoints.

### Setting Breakpoints
```
- Click line number to set breakpoint
- Right-click for conditional breakpoint
- Logpoint: Log without stopping

Breakpoint types:
- Line breakpoint: Stop at specific line
- Conditional: Stop only if condition is true
- DOM: Stop when DOM element changes
- XHR: Stop when URL matches pattern
- Event listener: Stop on specific events
```

### Debugging Controls
```
F8 or Ctrl+\  : Resume/Pause
F10 or Ctrl+' : Step over (next line)
F11 or Ctrl+; : Step into (enter function)
Shift+F11     : Step out (exit function)
```

### Watch Expressions
```
- Add expressions to watch their values
- Expressions re-evaluated each pause
- Useful for tracking variables over time
```

### Scope Pane
```
- Local: Current function's variables
- Closure: Closed-over variables
- Global: Window/global object
```

### Call Stack
```
- Shows function call chain
- Click to navigate to each frame
- "Async" shows async boundaries
```

## Performance Panel

### Purpose
Profile runtime performance.

### Recording
```
1. Click record (circle) or Ctrl+E
2. Perform the slow action
3. Click stop
4. Analyze the flame chart
```

### Key Metrics
```
- FPS: Frames per second (green = good)
- CPU: CPU activity over time
- NET: Network requests timeline
- Main: JavaScript execution on main thread
```

### Flame Chart
```
- X-axis: Time
- Y-axis: Call stack depth
- Wider = longer execution
- Click to see details
- Look for long tasks (red triangles)
```

## Memory Panel

### Purpose
Find memory leaks.

### Heap Snapshot
```
1. Click "Take snapshot"
2. Do action that might leak
3. Take another snapshot
4. Compare snapshots
5. Look for objects that shouldn't exist
```

### Allocation Timeline
```
1. Click "Allocation instrumentation on timeline"
2. Record while using app
3. Look for memory that never gets released
4. Blue bars = allocated, gray = freed
```

## Application Panel

### Purpose
Inspect storage, caches, and service workers.

### Storage
```
- Local Storage: Persistent key-value
- Session Storage: Session-only key-value
- IndexedDB: Structured database
- Cookies: View and edit cookies
```

### Cache
```
- Cache Storage: Service worker caches
- Application Cache: Legacy appcache
```

### Service Workers
```
- View registered workers
- Update, unregister, or bypass
- Push and sync testing
```

## React DevTools (Extension)

### Components Tab
```
- View component tree
- See props and state
- Edit props/state live
- Search by component name
```

### Profiler Tab
```
- Record render timings
- See why components re-rendered
- Flame graph of render cost
```

## Vue DevTools (Extension)

### Components Tab
```
- View component tree
- See props, data, computed, vuex state
- Time-travel debugging
```

### Vuex Tab
```
- See all mutations
- Time-travel through state
```

## Keyboard Shortcuts (Chrome)

| Action | Shortcut |
|--------|----------|
| Open DevTools | F12 / Ctrl+Shift+I |
| Open Console | Ctrl+Shift+J |
| Open Elements | Ctrl+Shift+C |
| Switch panels | Ctrl+[ / Ctrl+] |
| Search across files | Ctrl+Shift+F |
| Go to file | Ctrl+P |
| Go to line | Ctrl+G |
| Command menu | Ctrl+Shift+P |
| Toggle device mode | Ctrl+Shift+M |
