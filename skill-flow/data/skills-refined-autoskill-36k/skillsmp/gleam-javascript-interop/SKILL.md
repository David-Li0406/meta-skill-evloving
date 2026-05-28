---
name: gleam-javascript-interop
description: Guides Claude through integrating Gleam with JavaScript code using FFI, external functions, and NPM packages. Use when building for JavaScript target, using browser APIs, or wrapping JS libraries.
---

# Gleam JavaScript Interop Skill

This skill guides Claude Code through integrating Gleam with JavaScript code.

**IMPORTANT**: Always prefer pure Gleam solutions. Use externals only when there is no suitable alternative.

## Primary Sources

1. **[Gleam Externals Documentation](https://gleam.run/documentation/externals/)** - Official FFI guide
2. **[Gleam JavaScript Package](https://hexdocs.pm/gleam_javascript/)** - JavaScript integration utilities
3. **[Gleam Fetch](https://hexdocs.pm/gleam_fetch/)** - Fetch API bindings
4. **[ESGleam](https://hexdocs.pm/esgleam/)** - esbuild integration

## JavaScript Target

### Building for JavaScript

```bash
gleam build --target javascript
```

Output in `build/dev/javascript/`.

### Running JavaScript Builds

```bash
node build/dev/javascript/my_project/my_module.mjs
```

## @external Attribute Syntax

**Syntax**: `@external(javascript, module_path, function_name)`

- **module_path**: Relative path to `.mjs` file or npm package name
- **function_name**: JavaScript function to call
- **Type annotations are MANDATORY**

### Basic JavaScript External

```gleam
@external(javascript, "./my_ffi.mjs", "myFunction")
pub fn my_function(arg: String) -> Int
```

### Creating FFI Files

Create `my_ffi.mjs` (must use `.mjs` extension):

```javascript
// src/my_ffi.mjs

export function myFunction(arg) {
  return arg.length;
}
```

**Important**: Paths are relative to the Gleam source file.

## Type Safety and Testing (CRITICAL)

### The Compiler Cannot Verify External Types

From official documentation:

> The Gleam compiler will ensure that all uses of the function will be correct for the annotated types, but **it cannot verify that the function implemented in the other language returns the specified types**.

**You are responsible for ensuring the external function matches the types you declare.**

### Write More Tests (MANDATORY)

Because externals bypass compiler analysis:

- **Write more unit tests than usual** when using external functions
- Test all edge cases thoroughly
- Verify type conversions are correct
- Test error handling paths

```gleam
pub fn external_function_test() {
  let result = my_external_function("test")
  let assert Ok(value) = result
  assert value == expected
}
```

## JavaScript API for Gleam Data (v1.13+)

Gleam v1.13+ provides construction functions for data types.

### Lists

```javascript
import { List$Empty, List$NonEmpty } from "./gleam.mjs";

// Empty list
const empty = List$Empty();

// List [1, 2, 3]
const list = List$NonEmpty(1, List$NonEmpty(2, List$NonEmpty(3, List$Empty())));

// Helper: Convert array to Gleam List
function arrayToList(arr) {
  let list = List$Empty();
  for (let i = arr.length - 1; i >= 0; i--) {
    list = List$NonEmpty(arr[i], list);
  }
  return list;
}
```

### Results

```javascript
import { Result$Ok, Result$Error } from "./gleam.mjs";

// Success
const success = Result$Ok(42);

// Error
const failure = Result$Error("not found");

// Example: Parse number
export function parseNumber(input) {
  const num = parseInt(input);
  if (isNaN(num)) {
    return Result$Error("Not a number");
  }
  return Result$Ok(num);
}
```

### Options

```javascript
import { Some, None } from "./gleam.mjs";

// Some value
const some = Some(42);

// None
const none = None();

// Example: Find first
export function findFirst(arr) {
  if (arr.length === 0) {
    return None();
  }
  return Some(arr[0]);
}
```

### Custom Types

Pattern: `TypeName$VariantName(fields...)`

```gleam
// In Gleam
pub type User {
  Guest
  LoggedIn(id: Int, name: String)
}
```

```javascript
// In JavaScript FFI
import { User$Guest, User$LoggedIn } from "./user.mjs";

export function createGuest() {
  return User$Guest();  // No arguments
}

export function createLoggedIn(id, name) {
  return User$LoggedIn(id, name);
}

// Accessing fields
export function getUserId(user) {
  // Field access pattern: TypeName$VariantName$index
  if (user["User$LoggedIn$0"] !== undefined) {
    return Result$Ok(user["User$LoggedIn$0"]);  // id
  }
  return Result$Error("Guest has no ID");
}
```

## Data Type Mapping

| Gleam | JavaScript | Notes |
|-------|-----------|-------|
| `Int` | `number` | |
| `Float` | `number` | |
| `String` | `string` | |
| `Bool` | `boolean` | |
| `Nil` | `undefined` | |
| `List(a)` | Object | Use helper functions |
| `#(a, b)` | Array | `[a, b]` |
| `Result(a, e)` | Object | Use helper functions |
| `BitArray` | `Uint8Array` | |
| Custom types | Object | Tagged with variant |

## Working with Promises

Use `gleam/javascript/promise`:

```gleam
import gleam/javascript/promise.{type Promise}

@external(javascript, "./async_ffi.mjs", "fetchData")
fn fetch_data_ffi(url: String) -> Promise(Dynamic)

pub fn fetch_data(url: String) -> Promise(Result(Data, String)) {
  fetch_data_ffi(url)
  |> promise.map(decode_data)
}
```

```javascript
// async_ffi.mjs
export async function fetchData(url) {
  const response = await fetch(url);
  return response.json();
}
```

See: [gleam_javascript - Promise](https://hexdocs.pm/gleam_javascript/)

## NPM Integration

### Installing NPM Packages

```bash
npm install <package-name>
```

### Using NPM Packages

```javascript
// src/lodash_ffi.mjs
import { debounce } from "lodash";

export function debounceFunction(fn, wait) {
  return debounce(fn, wait);
}
```

```gleam
// src/lodash.gleam
@external(javascript, "lodash", "debounce")
pub fn debounce(fn: fn() -> Nil, wait: Int) -> fn() -> Nil
```

## Browser APIs

### Fetch API

Use `gleam_fetch`:

```gleam
import gleam/fetch
import gleam/javascript/promise

pub fn get_user(id: String) -> Promise(Result(String, fetch.FetchError)) {
  let url = "https://api.example.com/users/" <> id
  fetch.send(fetch.to(url))
  |> promise.try_await(fetch.read_text_body)
}
```

See: [gleam_fetch Documentation](https://hexdocs.pm/gleam_fetch/)

### DOM Manipulation

```gleam
pub type Element

@external(javascript, "./dom_ffi.mjs", "getElementById")
pub fn get_element_by_id(id: String) -> Result(Element, Nil)

@external(javascript, "./dom_ffi.mjs", "setInnerHTML")
pub fn set_inner_html(element: Element, html: String) -> Nil
```

```javascript
// dom_ffi.mjs
import { Result$Ok, Result$Error } from "../gleam.mjs";

export function getElementById(id) {
  const element = document.getElementById(id);
  if (element === null) {
    return Result$Error(undefined);
  }
  return Result$Ok(element);
}

export function setInnerHTML(element, html) {
  element.innerHTML = html;
}
```

### Event Listeners

```gleam
pub type Event

@external(javascript, "./events_ffi.mjs", "addEventListener")
pub fn add_event_listener(
  element: Element,
  event: String,
  handler: fn(Event) -> Nil,
) -> Nil
```

```javascript
// events_ffi.mjs
export function addEventListener(element, event, handler) {
  element.addEventListener(event, handler);
}
```

### Timers

```gleam
@external(javascript, "./timer_ffi.mjs", "setTimeout")
pub fn set_timeout(callback: fn() -> Nil, ms: Int) -> Nil
```

```javascript
// timer_ffi.mjs
export function setTimeout(callback, ms) {
  globalThis.setTimeout(callback, ms);
}
```

## Error Handling

Always convert JavaScript errors to Gleam Results:

```javascript
import { Result$Ok, Result$Error } from "../gleam.mjs";

export function riskyOperation(input) {
  try {
    const result = doSomethingRisky(input);
    return Result$Ok(result);
  } catch (error) {
    return Result$Error(error.message);
  }
}
```

## Multi-Target Support

Write code that works on both targets:

```gleam
@external(erlang, "crypto", "strong_rand_bytes")
@external(javascript, "node:crypto", "randomBytes")
pub fn random_bytes(size: Int) -> BitArray
```

Or with fallback:

```gleam
@external(javascript, "./fast_ffi.mjs", "fastSort")
pub fn fast_sort(list: List(Int)) -> List(Int) {
  // Pure Gleam fallback
  list.sort(list, int.compare)
}
```

## Testing JavaScript Target

```bash
gleam test --target javascript
```

Platform-specific tests:

```gleam
@target(javascript)
pub fn javascript_specific_test() {
  let result = javascript_only_function()
  let assert Ok(value) = result
  assert value == expected
}
```

## Frontend Frameworks

### Lustre (Recommended)

Gleam's Elm-inspired framework for full frontend applications:

```gleam
import lustre
import lustre/element/html
import lustre/element.{text}

pub fn main() {
  let app = lustre.simple(init, update, view)
  let assert Ok(_) = lustre.start(app, "#app", Nil)
}

fn init(_flags) {
  0
}

fn update(model, msg) {
  case msg {
    Increment -> model + 1
    Decrement -> model - 1
  }
}

fn view(model) {
  html.div([], [
    html.button([event.on_click(Decrement)], [text("-")]),
    html.p([], [text(int.to_string(model))]),
    html.button([event.on_click(Increment)], [text("+")]),
  ])
}
```

See: [Lustre Documentation](https://hexdocs.pm/lustre/)

## Build Tools

### esbuild Integration

Use `esgleam` for bundling:

```bash
gleam add --dev esgleam
```

Create build script:

```javascript
// build.mjs
import * as esbuild from "esbuild";
import * as gleam from "esgleam";

await esbuild.build({
  entryPoints: ["build/dev/javascript/my_project/my_module.mjs"],
  bundle: true,
  outfile: "dist/bundle.js",
  format: "esm",
  plugins: [gleam.plugin()],
});
```

See: [ESGleam Documentation](https://hexdocs.pm/esgleam/)

## Debugging

### Console Logging

```gleam
import gleam/io

pub fn debug(value: anything) -> anything {
  io.debug(value)  // Outputs to console with inspect format
  value
}
```

### Debugging Externals

Add logging to FFI files:

```javascript
export function myFunction(arg) {
  console.log("Called with:", arg);
  const result = doSomething(arg);
  console.log("Result:", result);
  return result;
}
```

## Best Practices

### DO: Wrap FFI in Safe APIs (MANDATORY)

```gleam
// Private FFI function
@external(javascript, "./api_ffi.mjs", "dangerousCall")
fn dangerous_call_ffi(input: String) -> Dynamic

// Public safe wrapper
pub fn safe_call(input: String) -> Result(Output, String) {
  dangerous_call_ffi(input)
  |> decode_output
  |> result.map_error(error_to_string)
}
```

### DO: Document Platform Requirements (MANDATORY)

```gleam
/// Fetches data from the browser's localStorage.
///
/// **Platform**: JavaScript only (browser environment)
/// **Requires**: Browser with localStorage API
///
@external(javascript, "./storage_ffi.mjs", "getItem")
pub fn get_item(key: String) -> Result(String, Nil)
```

### DO: Test Extensively (MANDATORY)

Write comprehensive tests for all external functions.

### DON'T: Skip Error Handling (FORBIDDEN)

Always wrap external calls with proper error handling.

### DON'T: Use FFI for Simple Operations (ANTI-PATTERN)

```gleam
// Bad - unnecessary FFI
@external(javascript, "./math.mjs", "add")
pub fn add(a: Int, b: Int) -> Int

// Good - pure Gleam
pub fn add(a: Int, b: Int) -> Int {
  a + b
}
```

## Limitations

### JavaScript Target Limitations

- No UTF codepoint pattern matching in bit arrays
- No `native` endianness option
- JavaScript lacks tail call optimization
- Different runtime behavior from Erlang target

### Performance Considerations

- Different garbage collection characteristics
- Consider target when designing recursive algorithms
- Lists are not native JavaScript arrays (performance impact)

---

**Remember**: Use JavaScript interop sparingly. Prefer Gleam implementations when possible for type safety and cross-platform compatibility.

See: [External Functions](../../rules/external-functions.md)
