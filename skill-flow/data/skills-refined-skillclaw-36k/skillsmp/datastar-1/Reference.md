# Datastar Reference

Complete reference for attributes, actions, and SSE events.

---

## Attributes

### Core Attributes

| Attribute | Syntax | Purpose |
|-----------|--------|---------|
| `data-signals` | `data-signals:name="value"` | Define signals |
| `data-bind` | `data-bind:signalName` | Two-way binding |
| `data-text` | `data-text="$signal"` | Set text content |
| `data-show` | `data-show="$condition"` | Conditional visibility |
| `data-class` | `data-class:className="$cond"` | Conditional classes |
| `data-attr` | `data-attr:attrName="$val"` | Dynamic attributes |
| `data-style` | `data-style:prop="$val"` | Dynamic inline styles |
| `data-on` | `data-on:event="expr"` | Event handlers |
| `data-init` | `data-init="@get('/...')"` | Run on init |
| `data-indicator` | `data-indicator:loading` | Track fetch status |
| `data-computed` | `data-computed:name="expr"` | Derived signals |
| `data-effect` | `data-effect="expr"` | Side effects |
| `data-ref` | `data-ref:name` | Element reference |
| `data-ignore` | `data-ignore` | Skip Datastar processing |
| `data-ignore-morph` | `data-ignore-morph` | Skip morphing |
| `data-preserve-attr` | `data-preserve-attr="name"` | Preserve during morph |

### Signals

```html
<!-- Define -->
<div data-signals:count="0"></div>
<div data-signals="{foo: 1, bar: 'hello'}"></div>
<div data-signals:user.name="'John'"></div>

<!-- Access -->
$count, $foo, $user.name

<!-- Only set if missing -->
<div data-signals:count__ifmissing="0"></div>
```

### Binding

```html
<!-- Input binding -->
<input data-bind:username />
<input type="checkbox" data-bind:agreed />
<select data-bind:choice>...</select>
<textarea data-bind:content></textarea>

<!-- File upload (base64) -->
<input type="file" data-bind:avatar />
```

### Conditional Rendering

```html
<!-- Show/hide -->
<div data-show="$isOpen">Content</div>

<!-- Classes -->
<div data-class:active="$isActive"></div>
<div data-class="{active: $isActive, disabled: $isDisabled}"></div>

<!-- Attributes -->
<button data-attr:disabled="$loading"></button>
<div data-attr:aria-expanded="$isOpen"></div>

<!-- Styles -->
<div data-style:opacity="$isVisible ? 1 : 0"></div>
```

### Events

```html
<!-- Basic -->
<button data-on:click="$count++">Click</button>

<!-- With modifiers -->
<button data-on:click__once="@post('/once')">Once</button>
<input data-on:input__debounce.500ms="@get('/search')">
<div data-on:click__outside="$menuOpen = false">Menu</div>
<form data-on:submit__prevent="@post('/form')">...</form>

<!-- Special events -->
<div data-on-intersect="$visible = true">Lazy load</div>
<div data-on-intersect__once__full="@get('/load')">Load when fully visible</div>
<div data-on-interval__duration.5s="@get('/poll')">Poll every 5s</div>

<!-- Available in handler: evt (event), el (element) -->
<div data-on:click="console.log(evt.target, el)"></div>
```

### Loading/Indicator

```html
<button data-on:click="@post('/submit')"
        data-indicator:submitting
        data-attr:disabled="$submitting">
    <span data-show="!$submitting">Submit</span>
    <span data-show="$submitting">Saving...</span>
</button>
```

### Computed & Effects

```html
<!-- Computed (read-only derived signal) -->
<div data-computed:fullName="$firstName + ' ' + $lastName"></div>
<span data-text="$fullName"></span>

<!-- Effect (runs when dependencies change) -->
<div data-effect="console.log('Count is now:', $count)"></div>
```

---

## Actions

### HTTP Actions

```html
@get(url, options?)
@post(url, options?)
@put(url, options?)
@patch(url, options?)
@delete(url, options?)
```

**Options:**
```javascript
{
  contentType: 'json' | 'form',
  headers: {'X-Custom': 'value'},
  filterSignals: {include: /^form\./, exclude: /password/},
  selector: '#myForm',           // form element to serialize
  payload: {custom: 'data'},     // override body
  openWhenHidden: true,          // keep SSE open when tab hidden
  retry: 'auto'|'error'|'always'|'never',
  retryInterval: 1000,
  retryMaxCount: 10
}
```

**Examples:**
```html
<!-- Basic -->
<button data-on:click="@get('/data')">Load</button>
<button data-on:click="@post('/submit')">Submit</button>

<!-- With options -->
<button data-on:click="@post('/api', {
    filterSignals: {include: /^form\./},
    headers: {'X-CSRF': $csrfToken}
})">Submit Form</button>

<!-- Custom payload -->
<button data-on:click="@post('/api', {
    payload: {id: $selectedId, action: 'delete'}
})">Delete</button>
```

### Utility Actions

```html
<!-- Peek: read signal without triggering reactivity -->
<div data-text="$foo + @peek(() => $bar)"></div>

<!-- Set all matching signals -->
<button data-on:click="@setAll(false, {include: /^checkbox/})">
    Uncheck All
</button>

<!-- Toggle all matching booleans -->
<button data-on:click="@toggleAll({include: /^selected/})">
    Toggle Selection
</button>
```

---

## SSE Events (Backend Response)

Content-Type: `text/event-stream`

### Patch Elements

```
event: datastar-patch-elements
data: elements <div id="target">New content</div>
```

**With options:**
```
event: datastar-patch-elements
data: selector #myDiv
data: mode inner
data: elements <p>Inner content</p>
```

**Modes:**
- `outer` (default) — Replace entire element
- `inner` — Replace inner HTML only
- `prepend` — Add as first child
- `append` — Add as last child
- `before` — Insert before element
- `after` — Insert after element
- `remove` — Delete element

**Multi-line HTML:**
```
event: datastar-patch-elements
data: elements <div id="list">
data: elements   <ul>
data: elements     <li>Item 1</li>
data: elements     <li>Item 2</li>
data: elements   </ul>
data: elements </div>
```

### Patch Signals

```
event: datastar-patch-signals
data: signals {count: 42, user: {name: "John"}}
```

**Only if missing:**
```
event: datastar-patch-signals
data: onlyIfMissing true
data: signals {defaultValue: 0}
```

**Remove signal:**
```
event: datastar-patch-signals
data: signals {oldSignal: null}
```

---

## Go Backend Example

```go
func handleStream(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "text/event-stream")
    w.Header().Set("Cache-Control", "no-cache")
    w.Header().Set("Connection", "keep-alive")

    flusher := w.(http.Flusher)

    // Send initial state
    fmt.Fprintf(w, "event: datastar-patch-elements\n")
    fmt.Fprintf(w, "data: elements %s\n\n", renderTodos())
    flusher.Flush()

    // Listen for updates (e.g., from NATS)
    for update := range updates {
        fmt.Fprintf(w, "event: datastar-patch-elements\n")
        fmt.Fprintf(w, "data: elements %s\n\n", renderTodos())
        flusher.Flush()
    }
}

func handleAddTodo(w http.ResponseWriter, r *http.Request) {
    // Parse request, add to DB
    addTodo(r.FormValue("text"))

    // Respond with SSE
    w.Header().Set("Content-Type", "text/event-stream")
    fmt.Fprintf(w, "event: datastar-patch-elements\n")
    fmt.Fprintf(w, "data: elements %s\n\n", renderTodos())
}
```

---

## Modifiers Reference

### Event Modifiers (`data-on`)
- `__once` — Fire once
- `__passive` — Passive listener
- `__capture` — Capture phase
- `__prevent` — preventDefault()
- `__stop` — stopPropagation()
- `__window` — Listen on window
- `__outside` — Fire when clicking outside element
- `__debounce.500ms` — Debounce (supports .leading, .notrailing)
- `__throttle.500ms` — Throttle (supports .noleading, .trailing)
- `__delay.500ms` — Delay execution

### Intersect Modifiers (`data-on-intersect`)
- `__once` — Fire once
- `__exit` — Fire on exit instead of enter
- `__half` — 50% visibility threshold
- `__full` — 100% visibility threshold
- `__threshold.25` — Custom threshold

### Signal Modifiers
- `__ifmissing` — Only set if not exists
- `__case.camel/.kebab/.snake/.pascal` — Name casing
