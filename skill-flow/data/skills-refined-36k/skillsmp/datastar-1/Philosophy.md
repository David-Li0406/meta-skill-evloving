# Datastar Philosophy (Deep Dive)

Additional context from the community, presentations, and real-world implementations.

---

## The Server Takes Back Control

From zweiundeins.gmbh (production Datastar users):

> "The server regains control over the application state."

The SPA era distributed state across client and server, creating synchronization nightmares. Datastar inverts this: **the server is the single source of truth**. The client is just a view.

**Their formula:** `view = f(state)`

The display is purely a function of server state. No client-side state machines, no Redux, no client-side caching headaches.

---

## Why Compression Beats Diffing

From Hyperlith (Clojure + Datastar):

> "HTML compresses really well...reduction in size by 90-100x! Sometimes more."

The common objection: "Won't sending full HTML be slow?"

No. Modern compression (Brotli, especially over HTTP/2) achieves 90-100x compression on HTML. Re-renders of similar content compress even better because the compression dictionary learns the patterns.

**This is why "fat morph" works:** Send the full component HTML. Trust compression. Trust morphing. Don't build a diffing system.

---

## Backpressure is a Feature

From zweiundeins:

> "The server determines when, how often, and how much data is sent."

With SSE, the server controls the flow. No client polling hammering your endpoints. No websocket complexity. The server pushes when it has something to say.

This is **backpressure by design** — the server never gets overwhelmed by client demands because the server initiates all updates.

---

## The Microlith Philosophy

Hyperlith coined "hypermedia-based monolith" but the community calls it a **microlith**: all the simplicity of a monolith with the reactivity of a modern SPA.

Key patterns:

1. **Single render function per page** — One function produces the complete view
2. **No connection state** — Failed events resolve via the next render
3. **Stateless connections** — The server doesn't track connection state
4. **CQRS naturally** — Commands modify DB, queries push views

---

## CQRS Without the Ceremony

CQRS (Command Query Responsibility Segregation) sounds enterprise-y, but Datastar makes it natural:

```
Commands: @post, @put, @delete → Modify state
Queries: @get, SSE stream → Read state, push HTML
```

That's it. No event buses, no projections, no eventual consistency headaches. The server changes state, then renders HTML.

---

## SQLite in Production

Both zweiundeins and the Northstar pattern use **embedded SQLite** in production.

Why?
- Zero network latency for reads
- ACID without a database server
- Perfect for hypermedia (read-heavy, write-light)
- Backups are just file copies

The "but SQLite doesn't scale" objection is mostly myth for web apps. Most apps never need more than one server.

---

## The Anti-HTMX Positioning

The presentation positions Datastar as addressing HTMX's limitations:

- **Signals** — HTMX has no built-in reactive state
- **SSE-first** — HTMX was designed for request/response, SSE is bolted on
- **Smaller** — Datastar is ~15kb, HTMX + extensions gets bigger

But the philosophy is similar: both reject the SPA orthodoxy in favor of hypermedia.

---

## "The Web Deserves It"

From the presentation:

> "Give it a shot. You deserve it. The web deserves it."

The framing is counter-cultural. The web industry spent a decade building increasingly complex client-side architectures. Datastar says: the web was already good. Server-rendered HTML with progressive enhancement was right all along. We just needed better tooling for real-time updates.

---

## Real-World Stack (zweiundeins)

A production stack from people using this approach daily:

- **PHP** + Swoole (async runtime for SSE)
- **SQLite** (embedded, production)
- **Datastar** (hypermedia client)
- **Caddy** (HTTP/2, auto-TLS)
- **Brotli** (compression)

No Kubernetes. No microservices. No React. Ship the whole thing on a $5 VPS.

---

## The Caveman Demo Principle

From the community (Anders' demos):

> "He tends to do things the most caveman way possible, and because the stack is so good, it's still fast and performant on a potato."

This is the acid test: can you build something obviously unoptimized and have it still be fast? With Datastar + SSE + compression, yes.

If your optimized React app is slower than a "caveman" Datastar app, maybe the architecture was wrong.

---

## Questions to Ask Yourself

Before reaching for a complex solution:

1. **Does the client need this state?** Usually no. Keep it on the server.
2. **Do I need diffing?** No. Trust morphing + compression.
3. **Do I need a separate API?** No. Server renders HTML directly.
4. **Do I need websockets?** No. SSE is simpler and sufficient.
5. **Do I need microservices?** No. A monolith with SQLite scales further than you think.

---

## The Goal

Build web apps the way the web was designed: server renders HTML, browser displays it. Add real-time updates via SSE. Add interactivity via declarative attributes. Ship it.

No build step. No node_modules. No state management library. No GraphQL. No Kubernetes.

Just HTML, streamed from the server, morphed into the DOM.
