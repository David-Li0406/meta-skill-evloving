---
name: Dioxus 0.7.x
description: This skill should be used when asking about "Dioxus", "dioxus framework", "Rust UI framework", "RSX macro", "dioxus components", "dioxus signals", "hot reload in Dioxus", "WASM splitting", "wasm_split macro", "Manganis assets", "asset! macro", "dioxus Stores", "nested reactivity", "dioxus renderers", "WriteMutations", or when working on a Rust web/UI project using Dioxus. Provides updated documentation for Dioxus 0.7.x features released after May 2025.
version: 0.7.3
---

# Dioxus 0.7.x Memory Patch

Documentation for Dioxus 0.7.x features that are new or updated since May 2025. Apply this knowledge when building Dioxus applications.

## What's New in 0.7.x

### 1. Subsecond Hot-Patching

Full Rust code hot-reload via jump table indirection. Changes to functions apply without restart.

**Key concepts:**
- Functions called through `subsecond::call()` or `HotFn::current()`
- Runtime looks up function pointer in global `APP_JUMP_TABLE`
- On patch: jump table updated, original binary untouched
- ASLR handled via `main` address as anchor

**Usage:**
```rust
// Standard Dioxus app - automatic
fn main() {
    dioxus::launch(app);
}

// Non-Dioxus apps
fn main() {
    dioxus_devtools::connect_subsecond();
    loop {
        dioxus_devtools::subsecond::call(|| handle_request());
    }
}
```

**Limitations:**
- Struct changes not supported (size/alignment changes cause crashes)
- Thread-locals in tip crate reset on patches
- Only tip crate patches, library crates ignored

For full details: `references/subsecond-hotpatch.md`

### 2. WASM Code Splitting

Split large WASM binaries into lazy-loaded chunks for faster initial load.

**Usage:**
```rust
#[wasm_split(admin_panel)]
async fn load_admin_panel() -> AdminPanel {
    AdminPanel::new()  // In separate module_admin_panel.wasm
}

async fn handle_route(route: Route) {
    match route {
        Route::Admin => {
            let panel = load_admin_panel().await;
            panel.render();
        }
        _ => // ...
    }
}
```

**Output structure:**
```
dist/
├── main.wasm           # Core application
├── module_1_*.wasm     # Feature chunks
├── chunk_1_*.wasm      # Shared code
└── __wasm_split.js     # JavaScript loader
```

**Key points:**
- Split points must be async functions
- Memory shared across all modules
- Requires `--emit-relocs` compilation flag

For full details: `references/wasm-split.md`

### 3. Manganis Asset System

Compile-time asset management via `asset!()` macro with automatic optimization and cache-busting.

**Usage:**
```rust
let img = asset!("/assets/image.png");
let css = asset!("/assets/style.css", AssetOptions::css().minified());

rsx! {
    img { src: "{img}" }
    link { rel: "stylesheet", href: "{css}" }
}
```

**CSS Modules:**
```rust
css_module!(Styles = "/my.module.css", AssetOptions::css_module());

rsx! { div { class: Styles::header } }
```

**How it works:**
1. Macro resolves path relative to CARGO_MANIFEST_DIR
2. Creates `__ASSETS__{hash}` symbol in link section
3. Build tool scans binary, processes assets, patches binary with final paths

**Asset options:**
- `ImageAssetOptions`: format, size, preload
- `CssAssetOptions`: minify, preload
- `JsAssetOptions`: minify, preload
- `FolderAssetOptions`: recursive copy

For full details: `references/manganis-assets.md`

### 4. Stores (Nested Reactivity)

Stores extend signals with granular path-based subscriptions for nested data structures.

**When to use:**
| Scenario | Use |
|----------|-----|
| Scalar state | Signal |
| Nested structures with granular updates | Store |

**Usage:**
```rust
#[derive(Store, Clone)]
struct TodoItem {
    checked: bool,
    contents: String,
}

let store = Store::new(TodoItem {
    checked: false,
    contents: "Buy milk".into(),
});

// Subscribe only to `checked` field
let checked = store.checked();
rsx! { input { checked: checked.read() } }

// Changing `contents` won't re-render above component
store.contents().set("Buy eggs".into());
```

**Key difference from signals:**
- Signal: All readers notified on any change
- Store: Only path-specific readers notified

For full details: `references/stores-signals.md`

### 5. Renderers

All renderers implement `WriteMutations` trait for DOM changes.

| Renderer | Package | Use Case |
|----------|---------|----------|
| Web | dioxus-web | WASM/browser via Sledgehammer JS |
| Desktop | dioxus-desktop | Wry/Tao webview |
| Native | dioxus-native | Blitz/Vello GPU (not a browser) |
| LiveView | dioxus-liveview | WebSocket streaming |
| SSR | dioxus-ssr | Server-side HTML rendering |

For full details: `references/renderers.md`

## Workspace Structure

```
packages/
├── dioxus/           # Main re-export crate
├── core/             # VirtualDOM, components, diffing
├── rsx/              # RSX macro parsing
├── signals/          # Reactive state (Signal, Memo, Store)
├── hooks/            # Built-in hooks
├── router/           # Type-safe routing
├── fullstack/        # SSR, hydration, #[server]
├── cli/              # `dx` build tool
├── web/              # WASM renderer
├── desktop/          # Wry/Tao webview
├── native/           # Blitz/Vello GPU renderer
├── liveview/         # WebSocket streaming
├── manganis/         # asset!() macro (NEW)
├── subsecond/        # Hot-patching system (NEW)
└── wasm-split/       # WASM code splitting (NEW)
```

## Patterns I Already Know

These patterns are unchanged from Dioxus 0.5-0.6:

**Components:**
```rust
#[component]
fn MyComponent(name: String) -> Element {
    let mut count = use_signal(|| 0);
    rsx! { button { onclick: move |_| count += 1, "{name}: {count}" } }
}
```

**Server Functions:**
```rust
#[server]
async fn get_data(id: i32) -> Result<Data, ServerFnError> {
    // Runs on server, auto-RPC from client
}
```

**Routing:**
```rust
#[derive(Routable, Clone)]
enum Route {
    #[route("/")]
    Home {},
    #[route("/blog/:id")]
    Blog { id: usize },
}
```

## Architecture Notes

- **WriteMutations**: Trait all renderers implement for DOM changes
- **Generational-box**: Provides `Copy` semantics for signals via generation counters
- **ReactiveContext**: Tracks which signals a component reads for subscription
- **Template-based rendering**: RSX compiles to static templates, only dynamic parts diffed

## Reference Files

For detailed documentation on each feature, consult:
- **`references/subsecond-hotpatch.md`** - Full hot-patching architecture, ASLR handling, limitations
- **`references/wasm-split.md`** - Complete WASM splitting pipeline, runtime loader
- **`references/manganis-assets.md`** - Asset processing, binary patching, CSS modules
- **`references/stores-signals.md`** - Store derive macro, subscription tree, memory model
- **`references/renderers.md`** - WriteMutations trait, renderer differences
