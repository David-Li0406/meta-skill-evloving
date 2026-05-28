---
name: Datastar
description: Hypermedia-driven UI with SSE. USE WHEN building interactive web UI, forms, real-time updates. PHILOSOPHY FIRST - read this before writing any code.
---

# Datastar - Hypermedia, Not React

**STOP. Read this first.** Datastar is not React. It's not Vue. It's not a JS framework at all. It's a return to hypermedia - the backend sends HTML, the frontend renders it. If you find yourself thinking about "components", "state management", or "client-side routing", you're already wrong.

---

## The Tao (Memorize This)

> make an MPA
> each page is a resource
> keep a stream open on the current state of that resource
> ship, touch grass, repeat
> — Delaney

**URLs are fast-travel locations, not points in time.** — Anders

---

## Core Philosophy

1. **Backend is the source of truth** — All state lives on the server. The frontend is just a view.

2. **Send HTML, not JSON** — The server renders HTML fragments and sends them via SSE. No client-side templating.

3. **Morph, don't diff** — Datastar morphs the DOM efficiently. Send "fat" chunks of HTML; trust the algorithm.

4. **Signals are for UI only** — Frontend signals (`$foo`) are for transient UI state (form inputs, toggles). NOT for application state.

5. **SSE for real-time** — Keep a stream open. Server pushes updates. No polling, no websocket complexity.

6. **CQRS naturally emerges** — Commands (`@post`) mutate state. Queries (`@get` or SSE) read state. Don't mix them.

---

## STOP: Anti-Patterns (React Brain)

**DO NOT:**

| React Brain | Datastar Way |
|-------------|--------------|
| Store state in frontend | Store state in backend (DB/session) |
| Fetch JSON, render client-side | Server renders HTML, sends via SSE |
| Client-side routing (React Router) | Normal `<a href>` links, let browser handle |
| Component hierarchies | HTML templates on server |
| Optimistic UI updates | Wait for server confirmation |
| `useEffect` for data fetching | `data-init="@get('/resource')"` |
| Query params for filters | Session/cookie state, URLs identify resources |
| Manual DOM manipulation | Trust morphing |

**URL Anti-Pattern:**
```
BAD:  /products?color=red&sort=price&page=2  (state in URL)
GOOD: /products  (resource) + session stores user's filter preferences
```

---

## Quick Reference

### Backend Actions
```html
<button data-on:click="@get('/endpoint')">Fetch</button>
<button data-on:click="@post('/endpoint')">Submit</button>
<button data-on:click="@put('/endpoint')">Update</button>
<button data-on:click="@delete('/endpoint')">Remove</button>
```

### Signals (UI State Only)
```html
<div data-signals:count="0"></div>
<button data-on:click="$count++">+1</button>
<span data-text="$count"></span>
```

### Two-Way Binding
```html
<input data-bind:username />
<span data-text="$username"></span>
```

### Conditional Display
```html
<div data-show="$isVisible">Shown when $isVisible is truthy</div>
```

### Loading Indicators
```html
<button data-on:click="@post('/submit')"
        data-indicator:loading
        data-attr:disabled="$loading">
    <span data-show="!$loading">Submit</span>
    <span data-show="$loading">Loading...</span>
</button>
```

### CQRS Pattern (THE Pattern)
```html
<div id="todos" data-init="@get('/todos/stream')">
    <!-- Server pushes HTML updates here via SSE -->
    <button data-on:click="@post('/todos', {payload: {text: $newTodo}})">
        Add Todo
    </button>
</div>
```

---

## SSE Response Format

Backend sends `text/event-stream`:

**Patch HTML:**
```
event: datastar-patch-elements
data: elements <div id="todos">...new HTML...</div>
```

**Patch Signals:**
```
event: datastar-patch-signals
data: signals {count: 42}
```

**Modes:** `outer` (default), `inner`, `prepend`, `append`, `before`, `after`, `remove`

---

## The Northstar Pattern (Idiomatic)

From the canonical example (zangster300/northstar):

1. **Embedded NATS** — Use NATS KV for real-time state sync
2. **Templ templates** — Server-side Go templates
3. **SSE streams** — Keep connection open for live updates
4. **No REST API** — Server directly renders HTML, no JSON intermediary

```
Architecture:
  Browser ←──SSE──→ Go Server ←──→ NATS KV (state)
                        ↓
                   Templ (HTML)
```

---

## Decision Tree

```
What are you building?
        │
        ├─→ Static content? → Use <a href>, no Datastar needed
        │
        ├─→ Form submission? → @post + SSE response with updated HTML
        │
        ├─→ Real-time updates? → data-init="@get('/stream')" + SSE
        │
        └─→ Interactive UI? → Signals for UI state + @get/@post for persistence
```

---

## Context Files

- `Reference.md` — Complete attribute/action/SSE reference
- `Patterns.md` — Idiomatic patterns and examples
- `Philosophy.md` — Deep dive: community insights, microlith, SQLite, compression

---

## Final Reminder

**The backend controls the UI.** The frontend is a dumb terminal that displays HTML. If you're writing JavaScript logic beyond simple UI toggles, you're doing it wrong. Ship HTML from the server.
