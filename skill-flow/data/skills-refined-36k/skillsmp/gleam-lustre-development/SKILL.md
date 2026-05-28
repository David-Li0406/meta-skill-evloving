---
name: gleam-lustre-development
description: Guides Claude through idiomatic Lustre frontend development. Use when building SPAs, UI components, or interactive applications. Based on lustre_ui patterns from the official Lustre team.
---

# Gleam Lustre Development Skill

This skill guides Claude Code through **idiomatic Lustre development** following patterns from the official `lustre_ui` library.

## Primary Sources

1. **[Lustre Documentation](https://hexdocs.pm/lustre/)** - Official docs
2. **[Lustre UI](https://github.com/lustre-labs/ui)** - Official component library (reference implementation)
3. **[Lustre Examples](https://github.com/lustre-labs/lustre/tree/main/examples)** - Official examples

## Core Architecture: Model-Update-View

Every Lustre application follows the Elm Architecture:

```gleam
import lustre
import lustre/effect.{type Effect}
import lustre/element.{type Element}

// TYPES -----------------------------------------------------------------------

type Model {
  Model(
    count: Int,
    // ... state fields
  )
}

type Msg {
  UserClickedIncrement
  UserClickedDecrement
  ApiReturnedData(Result(Data, Error))
}

// MAIN ------------------------------------------------------------------------

pub fn main() {
  let app = lustre.application(init, update, view)
  let assert Ok(_) = lustre.start(app, "#app", Nil)
  Nil
}

// INIT ------------------------------------------------------------------------

fn init(_flags) -> #(Model, Effect(Msg)) {
  let model = Model(count: 0)
  #(model, effect.none())
}

// UPDATE ----------------------------------------------------------------------

fn update(model: Model, msg: Msg) -> #(Model, Effect(Msg)) {
  case msg {
    UserClickedIncrement -> #(Model(..model, count: model.count + 1), effect.none())
    UserClickedDecrement -> #(Model(..model, count: model.count - 1), effect.none())
    ApiReturnedData(Ok(data)) -> #(Model(..model, data: data), effect.none())
    ApiReturnedData(Error(_)) -> #(model, effect.none())
  }
}

// VIEW ------------------------------------------------------------------------

fn view(model: Model) -> Element(Msg) {
  html.div([], [
    html.button([event.on_click(UserClickedDecrement)], [html.text("-")]),
    html.p([], [html.text(int.to_string(model.count))]),
    html.button([event.on_click(UserClickedIncrement)], [html.text("+")]),
  ])
}
```

### Application Levels

```gleam
// Static HTML only (no interactivity)
lustre.element(html.div([], [html.text("Hello")]))

// Interactive without effects (init/update return Model only)
lustre.simple(init, update, view)

// Full application with effects (init/update return #(Model, Effect))
lustre.application(init, update, view)

// Registrable Web Component
lustre.component(init:, update:, view:, options: [...])
```

## MANDATORY: Message Naming Convention

**Messages MUST use Subject-Verb-Object naming that describes WHAT HAPPENED, not what to do:**

```gleam
// ✅ CORRECT: Describes what happened
type Msg {
  UserClickedSubmit
  UserTypedInField(value: String)
  UserPressedEnter
  UserSelectedOption(id: String)
  UserToggledCheckbox(checked: Bool)
  ApiReturnedUsers(Result(List(User), Error))
  ApiReturnedError(Error)
  ParentSetValue(value: String)
  ParentToggledOpen
  TimerFired
  WindowResized(width: Int, height: Int)
}

// ❌ WRONG: Imperative/command style
type Msg {
  Submit           // What does this mean?
  SetValue(String) // Command, not event
  Toggle           // Too vague
  LoadUsers        // Command, not event
  UpdateField      // Command, not event
}
```

**Prefixes by source:**
- `User...` - User interactions (clicks, typing, etc.)
- `Api...` - HTTP/API responses
- `Parent...` - Props from parent component
- `Timer...` / `Window...` / `Dom...` - Browser events
- `Child...` - Events from child components

## Controlled vs Uncontrolled Props

For components that can have state managed by parent OR internally:

```gleam
/// A prop that can be controlled by the parent or managed internally.
pub type Prop(a) {
  Prop(
    value: a,        // Current value
    controlled: Bool, // Is parent controlling this?
    touched: Bool,    // Has user interacted?
  )
}

pub fn new(value: a) -> Prop(a) {
  Prop(value: value, controlled: False, touched: False)
}

/// Set default value (only if not controlled and not touched)
pub fn default(prop: Prop(a), value: a) -> Prop(a) {
  case prop.controlled || prop.touched {
    True -> prop
    False -> Prop(..prop, value: value)
  }
}

/// Control from parent (always updates)
pub fn control(prop: Prop(a), value: a) -> Prop(a) {
  Prop(..prop, value: value, controlled: True)
}

/// User touched (only updates if not controlled)
pub fn touch(prop: Prop(a), value: a) -> Prop(a) {
  case prop.controlled {
    True -> prop
    False -> Prop(..prop, value: value, touched: True)
  }
}
```

**Usage in update:**

```gleam
fn update(model: Model, msg: Msg) -> #(Model, Effect(Msg)) {
  case msg {
    ParentSetDefaultValue(value) ->
      // Only apply if not controlled and not touched by user
      case model.open.controlled || model.open.touched {
        True -> #(model, effect.none())
        False -> {
          let open = Prop(..model.open, value: value)
          #(Model(..model, open: open), effect.none())
        }
      }
      
    ParentSetValue(value) -> {
      // Controlled: always update
      let open = Prop(..model.open, value: value, controlled: True)
      #(Model(..model, open: open), effect.none())
    }
    
    UserToggledOpen ->
      case model.open.controlled {
        // Controlled: emit event, don't update locally
        True -> #(model, emit_change(!model.open.value))
        // Uncontrolled: update locally AND emit event
        False -> {
          let open = Prop(..model.open, value: !model.open.value, touched: True)
          #(Model(..model, open: open), emit_change(!model.open.value))
        }
      }
  }
}
```

## Web Components (Registrable Components)

For reusable components that need their own state:

```gleam
import lustre
import lustre/component

pub const tag: String = "my-component"

pub fn register() -> Result(Nil, lustre.Error) {
  let comp = lustre.component(init:, update:, view:, options: [
    // Don't inherit parent styles
    component.adopt_styles(False),
    
    // React to attribute changes
    component.on_attribute_change("value", fn(value) {
      Ok(ParentSetValue(value))
    }),
    
    // React to property changes (for complex values)
    component.on_property_change("items", {
      decode.list(decode.string)
      |> decode.map(ParentSetItems)
    }),
    
    // React to context from ancestors
    component.on_context_change("theme", {
      use theme <- decode.field("theme", decode.string)
      decode.success(ThemeChanged(theme))
    }),
  ])
  
  lustre.register(comp, tag)
}

// Public element function
pub fn element(
  attributes: List(Attribute(msg)),
  children: List(Element(msg)),
) -> Element(msg) {
  element.element(tag, attributes, children)
}
```

## Opaque Types for Public APIs

Encapsulate internal structure:

```gleam
/// An accordion item with heading and collapsible panel.
pub opaque type Item(msg) {
  Item(
    name: String,
    attributes: List(Attribute(msg)),
    heading: Element(msg),
    panel: Panel(msg),
  )
}

/// Create an accordion item.
pub fn item(
  name name: String,
  attributes attributes: List(Attribute(msg)),
  heading heading: Element(msg),
  panel panel: Panel(msg),
) -> Item(msg) {
  Item(name:, attributes:, heading:, panel:)
}
```

## Effects

```gleam
import lustre/effect

// No effect
effect.none()

// Batch multiple effects
effect.batch([effect1, effect2, effect3])

// Custom effect
effect.from(fn(dispatch) {
  // Do something async
  dispatch(SomethingHappened(result))
})

// Emit custom event (for components)
event.emit("my-event", json.object([
  #("value", json.string(value)),
]))

// Provide context to descendants
effect.provide("context-name", json.object([
  #("theme", json.string("dark")),
]))
```

## Event Handling with Decoders

```gleam
import gleam/dynamic/decode
import lustre/event

// Simple event
pub fn on_click(msg: msg) -> Attribute(msg) {
  event.on_click(msg)
}

// Custom event with detail
pub fn on_change(handler: fn(String) -> msg) -> Attribute(msg) {
  event.on("change", {
    use value <- decode.field("detail", decode.string)
    decode.success(handler(value))
  })
}

// Complex event with multiple fields
pub fn on_item_change(handler: fn(String, Bool) -> msg) -> Attribute(msg) {
  event.on("item:change", {
    use id <- decode.subfield(["detail", "id"], decode.string)
    use open <- decode.subfield(["detail", "open"], decode.bool)
    decode.success(handler(id, open))
  })
}

// Event with preventDefault/stopPropagation
fn handle_keydown() -> Decoder(Handler(Msg)) {
  use key <- decode.field("key", decode.string)
  
  case key {
    "Enter" -> decode.success(event.handler(
      dispatch: UserPressedEnter,
      prevent_default: True,
      stop_propagation: False,
    ))
    _ -> decode.failure(UserPressedEnter, "not enter")
  }
}
```

## CSS Pseudo-States

For component states (open, selected, disabled, etc.):

```gleam
import lustre/component

// In update function
case model.open {
  True -> component.set_pseudo_state("open")
  False -> component.remove_pseudo_state("open")
}

// CSS can use :state(open) selector
// :host(:state(open)) { ... }
```

## Keyed Rendering for Lists

**ALWAYS use keyed rendering for dynamic lists:**

```gleam
import lustre/element/keyed

fn view_items(items: List(Item)) -> Element(Msg) {
  keyed.element("ul", [], {
    list.map(items, fn(item) {
      #(item.id, html.li([], [html.text(item.name)]))
    })
  })
}
```

## Accessibility (MANDATORY)

### ARIA Attributes

```gleam
import lustre/attribute

// Role
attribute.role("button")
attribute.role("region")

// States
attribute.aria_expanded(is_open)
attribute.aria_pressed(is_pressed)
attribute.aria_disabled(is_disabled)
attribute.aria_controls(panel_id)
attribute.aria_labelledby(heading_id)

// For dynamic content
attribute.aria_live("polite")
attribute.aria_atomic(True)
```

### Keyboard Navigation

```gleam
fn handle_keydown(model: Model) -> Decoder(Handler(Msg)) {
  use key <- decode.field("key", decode.string)
  use target <- decode.field("target", element_decoder())
  
  case key {
    "ArrowDown" -> find_next(model, target)
    "ArrowUp" -> find_previous(model, target)
    "Home" -> find_first(model)
    "End" -> find_last(model)
    "Enter" | " " -> activate(target)
    "Escape" -> close(model)
    _ -> decode.failure(NoOp, "unhandled key")
  }
}
```

### Inert for Hidden Content

```gleam
// Make collapsed content inert (unfocusable, hidden from screen readers)
component.default_slot([
  attribute.inert(model.collapsed)
], children)
```

## File Structure

```
src/
├── app.gleam                    # Main application
├── app/
│   ├── router.gleam             # Routing
│   └── pages/
│       ├── home.gleam
│       └── settings.gleam
└── components/
    ├── ui.gleam                 # Re-exports all components
    └── ui/
        ├── button.gleam         # Simple component (just functions)
        ├── accordion.gleam      # Public API for complex component
        └── accordion/
            ├── root.gleam       # Web component (internal)
            ├── item.gleam       # Web component (internal)
            ├── trigger.gleam    # Web component (internal)
            └── panel.gleam      # Web component (internal)
```

## Simple Components (Functions)

For stateless UI elements, use simple functions:

```gleam
//// Button components.

import lustre/attribute.{type Attribute, class}
import lustre/element.{type Element}
import lustre/element/html
import lustre/event

pub type Variant {
  Primary
  Secondary
  Danger
}

/// Render a button.
pub fn button(
  attributes: List(Attribute(msg)),
  variant: Variant,
  children: List(Element(msg)),
) -> Element(msg) {
  let variant_class = case variant {
    Primary -> "btn-primary"
    Secondary -> "btn-secondary"
    Danger -> "btn-danger"
  }
  
  html.button([class("btn " <> variant_class), ..attributes], children)
}

/// Render a button with click handler.
pub fn button_with_action(
  label: String,
  on_click: msg,
  variant: Variant,
) -> Element(msg) {
  button([event.on_click(on_click)], variant, [html.text(label)])
}
```

## Complex Components (Web Components)

For stateful, interactive components:

```gleam
//// Accordion component following WAI-ARIA patterns.
////
//// ```gleam
//// accordion.view([], [
////   accordion.item(
////     name: "section-1",
////     attributes: [],
////     heading: accordion.heading([], 
////       accordion.trigger([], [html.text("Title")])
////     ),
////     panel: accordion.panel([], [
////       html.p([], [html.text("Content...")])
////     ]),
////   ),
//// ])
//// ```

// ... (see lustre_ui/accordion.gleam for full implementation)
```

## Documentation Standards

Every public function needs:

```gleam
/// The root accordion element.
///
/// #### Attributes
///
/// [`default_value`](#default_value), [`multiple`](#multiple), [`loop`](#loop).
///
/// #### Events
///
/// [`on_value_change`](#on_value_change)
///
/// #### Accessibility notes
///
/// - Home/End moves focus to first/last trigger
/// - Arrow Up/Down navigates between triggers
///
/// #### Managed attributes
///
/// These are set automatically and **must not** be set manually:
///
/// - `role`
/// - `aria-orientation`
///
pub fn view(
  attributes: List(Attribute(msg)),
  children: List(Item(msg)),
) -> Element(msg) {
  // ...
}
```

## Common Mistakes to Avoid

1. **Imperative message names**: Use `UserClickedSave` not `Save`
2. **Forgetting to map effects**: Use `effect.map(ChildMsg)` when delegating
3. **Forgetting to map elements**: Use `element.map(ChildMsg)` for child views
4. **Non-keyed lists**: Always use `keyed.element` for dynamic lists
5. **Missing accessibility**: Always add ARIA attributes and keyboard support
6. **Hardcoded IDs**: Generate unique IDs with a shortid generator
7. **Blocking the main thread**: Use effects for async operations
8. **Direct DOM manipulation**: Use Lustre's declarative approach

## Development Tools Configuration

Lustre dev tools are configured via the `[tools.lustre]` table in `gleam.toml`. See the [TOML Reference](https://hexdocs.pm/lustre_dev_tools/toml-reference.html) for all configuration options.

### Common Configuration

```toml
[tools.lustre]

# Build configuration
[tools.lustre.build]
minify = true            # Minify output (reduces size)
outdir = "./dist"        # Output directory

# Dev server configuration
[tools.lustre.dev]
host = "localhost"       # Bind to localhost or "0.0.0.0" for network access
port = 1234              # Server port

# Proxy API requests to backend
[[tools.lustre.dev.proxy]]
from = "/api"
to = "http://localhost:3000"

# HTML document structure
[tools.lustre.html]
title = "My App"         # Document title
```

### CLI Commands

**Download binary dependencies:**
```bash
# Download Bun (JavaScript runtime and bundler)
gleam run -m lustre/dev add bun

# Download Tailwind CSS
gleam run -m lustre/dev add tailwind
```

**Build project:**
```bash
# Build using your app's name (from gleam.toml), generates index.html
gleam run -m lustre/dev build

# Build a specific module, generates index.html
gleam run -m lustre/dev build your_app/module

# Build multiple entry points (requires manual index.html)
gleam run -m lustre/dev build your_app/page1 your_app/page2
```

**Start development server:**
```bash
# Start dev server with file watching and hot reload
gleam run -m lustre/dev start
```

Configuration from `gleam.toml` is automatically applied. Command-line flags (if supported) override configuration settings.

### Tailwind CSS v4 Integration

Create a CSS file in `src/` with the same name as your project (from `gleam.toml`):

```css
/* src/my_project.css */
@import "tailwindcss";

/* Your custom styles */
@theme {
  --color-primary: #3b82f6;
  --font-heading: "Inter", sans-serif;
}
```

Lustre dev tools will automatically detect and compile Tailwind v4. No `tailwind.config.js` needed!

### API Proxying

Forward API requests to a backend server during development:

```toml
[[tools.lustre.dev.proxy]]
from = "/api"
to = "http://localhost:3000"

[[tools.lustre.dev.proxy]]
from = "/auth"
to = "http://localhost:4000"
```

Requests to `/api/*` are forwarded to `http://localhost:3000/api/*` while preserving the path.

## References

- [Lustre Docs](https://hexdocs.pm/lustre/)
- [Lustre Dev Tools CLI](https://hexdocs.pm/lustre_dev_tools/lustre/dev.html)
- [Lustre Dev Tools TOML Reference](https://hexdocs.pm/lustre_dev_tools/toml-reference.html)
- [Lustre UI Source](https://github.com/lustre-labs/ui/tree/hayleigh/headless-redux-redux)
- [WAI-ARIA Patterns](https://www.w3.org/WAI/ARIA/apg/patterns/)
