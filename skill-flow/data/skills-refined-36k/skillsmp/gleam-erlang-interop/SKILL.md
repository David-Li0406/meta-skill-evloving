---
name: gleam-erlang-interop
description: Guides Claude through integrating Gleam with Erlang and Elixir code using FFI, external functions, and BEAM libraries. Use when building for Erlang target, calling Erlang libraries, or integrating with existing BEAM systems.
---

# Gleam Erlang Interop Skill

This skill guides Claude Code through integrating Gleam with Erlang and Elixir code.

**IMPORTANT**: Always prefer pure Gleam solutions. Use externals only when there is no suitable alternative.

## Primary Sources

1. **[Gleam Externals Documentation](https://gleam.run/documentation/externals/)** - Official FFI guide
2. **[Gleam Erlang Package](https://hexdocs.pm/gleam_erlang/)** - Erlang integration utilities
3. **[Gleam OTP](https://hexdocs.pm/gleam_otp/)** - OTP framework integration
4. **[Gleam FAQ - Elixir Integration](https://gleam.run/frequently-asked-questions/)** - Using Elixir code

## Erlang Target

### Building for Erlang

```bash
gleam build  # Defaults to Erlang target
gleam build --target erlang
```

Output in `build/dev/erlang/`.

### Running Erlang Builds

```bash
gleam run  # Run your main function
erl -pa build/dev/erlang/*/ebin  # Start Erlang shell with your code
```

## @external Attribute Syntax

**Syntax**: `@external(erlang, "module", "function")`

- **module**: Erlang module name (lowercase with underscores)
- **function**: Erlang function name
- **Type annotations are MANDATORY**

### Basic Erlang External

```gleam
@external(erlang, "lists", "reverse")
pub fn reverse_list(list: List(element)) -> List(element)
```

This calls the Erlang `lists:reverse/1` function.

See: [External Functions - Erlang](https://gleam.run/documentation/externals/)

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

## Data Type Mapping

### Gleam to Erlang

| Gleam Type | Erlang Type | Notes |
|------------|-------------|-------|
| `Int` | Integer | |
| `Float` | Float | |
| `String` | Binary | `<<"text"/utf8>>` |
| `Bool` | Atom | `true`/`false` |
| `Nil` | Atom | `nil` |
| `List(a)` | List | `[a]` |
| `#(a, b)` | Tuple | `{a, b}` |
| `Result(a, e)` | Tagged tuple | `{ok, a}` or `{error, e}` |
| Custom types | Tagged tuples | |
| `BitArray` | Binary | |

### Custom Type Representation

```gleam
pub type Status {
  Loading
  Success
  Error
}
```

Maps to Erlang atoms: `loading`, `success`, `error`

**PascalCase variants convert to snake_case atoms in Erlang.**

```gleam
pub type User {
  Guest
  LoggedIn(id: Int, name: String)
}
```

Maps to Erlang:
- `guest` (single atom for variant without fields)
- `{logged_in, 123, <<"Alice"/utf8>>}` (tagged tuple for variant with fields)

## Common Erlang Modules

### Lists Module

```gleam
@external(erlang, "lists", "reverse")
pub fn reverse(list: List(a)) -> List(a)

@external(erlang, "lists", "sort")
pub fn sort(list: List(a)) -> List(a)

@external(erlang, "lists", "flatten")
pub fn flatten(list: List(List(a))) -> List(a)
```

### String/Binary Module

```gleam
@external(erlang, "string", "trim")
pub fn trim(s: String) -> String

@external(erlang, "string", "uppercase")
pub fn uppercase(s: String) -> String
```

### Crypto Module

```gleam
import gleam/dynamic.{type Dynamic}

@external(erlang, "crypto", "hash")
fn hash_ffi(algorithm: Dynamic, data: BitArray) -> BitArray

pub fn sha256(data: String) -> BitArray {
  data
  |> bit_array.from_string
  |> hash_ffi(dynamic.from("sha256"), _)
}

@external(erlang, "crypto", "strong_rand_bytes")
pub fn random_bytes(n: Int) -> BitArray
```

**Important**: Atoms should be passed as `Dynamic` when calling Erlang functions.

### Timer Module

```gleam
import gleam/erlang/process

pub fn sleep(milliseconds: Int) -> Nil {
  process.sleep(milliseconds)
}
```

Use `gleam/erlang/process.sleep` instead of calling `timer:sleep` directly.

## Elixir Integration

### Calling Elixir Modules

Elixir modules require `Elixir.` prefix:

```gleam
@external(erlang, "Elixir.String", "upcase")
pub fn upcase(string: String) -> String

@external(erlang, "Elixir.Enum", "map")
pub fn enum_map(list: List(a), f: fn(a) -> b) -> List(b)
```

**Important**: The target is still `erlang`, not `elixir`.

See: [External Functions - Elixir](https://gleam.run/documentation/externals/)

### Using Elixir Macros

**Elixir macros cannot be called from Gleam**. They must be wrapped in regular functions.

```elixir
# In Elixir (lib/my_wrapper.ex)
defmodule MyWrapper do
  def use_macro(arg) do
    # Call macro here
    SomeMacro.macro_function(arg)
  end
end
```

```gleam
// In Gleam
@external(erlang, "Elixir.MyWrapper", "use_macro")
pub fn use_macro(arg: String) -> Result(Value, Error)
```

See: [Gleam FAQ - Elixir Macros](https://gleam.run/frequently-asked-questions/)

## OTP Integration

### Using gleam_otp

For OTP functionality, use the `gleam_otp` package:

```gleam
import gleam/otp/actor
import gleam/erlang/process.{type Subject}

pub fn start_worker() -> Result(Subject(Message), actor.StartError) {
  actor.new(initial_state)
  |> actor.on_message(handle_message)
  |> actor.start
}
```

See: [Gleam OTP Documentation](https://hexdocs.pm/gleam_otp/)

### Atoms

```gleam
import gleam/erlang/atom.{type Atom}

pub fn create_atom(name: String) -> Atom {
  atom.create_from_string(name)
}
```

See: [gleam_erlang - Atom](https://hexdocs.pm/gleam_erlang/gleam/erlang/atom.html)

### ETS (Erlang Term Storage)

```gleam
import gleam/erlang/atom.{type Atom}

pub type Table

@external(erlang, "ets", "new")
pub fn new(name: Atom, options: List(Atom)) -> Table

@external(erlang, "ets", "insert")
pub fn insert(table: Table, objects: List(#(a, b))) -> Bool

@external(erlang, "ets", "lookup")
pub fn lookup(table: Table, key: a) -> List(#(a, b))
```

## Bit Strings / Binary Data

### Pattern Matching on Binaries

```gleam
pub fn parse_packet(data: BitArray) -> Result(Packet, ParseError) {
  case data {
    <<version:8, type_:8, length:16, body:bytes>> -> {
      Ok(Packet(version, type_, length, body))
    }
    _ -> Error(InvalidPacket)
  }
}
```

See: [Bit Array Syntax](https://gearsco.de/blog/bit-array-syntax/)

### Bit Array Options

- **Size**: `value:32` (32 bits)
- **Type**: `int`, `float`, `bytes`, `bits`, `utf8`, `utf16`, `utf32`
- **Signedness**: `signed`, `unsigned`
- **Endianness**: `big`, `little`, `native`
- **Unit**: Multiplier for size

```gleam
<<value:size(32)-unsigned-big-integer>> = data
```

## Calling Erlang Libraries

### HTTP Clients

For HTTP requests, prefer Gleam packages:
- [gleam_http](https://hexdocs.pm/gleam_http/) - HTTP types
- [gleam_httpc](https://hexdocs.pm/gleam_httpc/) - HTTP client
- [gleam_fetch](https://hexdocs.pm/gleam_fetch/) - Fetch API (JavaScript/Erlang)

### HTTP Servers

For web servers, prefer:
- [Mist](https://hexdocs.pm/mist/) - Native Gleam HTTP server
- [Wisp](https://hexdocs.pm/wisp/) - Web framework

### Database

For databases:
- [gleam_pgo](https://hexdocs.pm/gleam_pgo/) - PostgreSQL
- [sqlight](https://hexdocs.pm/sqlight/) - SQLite

## Compiling with Elixir Code

### Mix Projects

Gleam code can be part of Elixir Mix projects:

1. Add `mix_gleam` to dependencies
2. Place Gleam code in `src/`
3. Run `mix compile`

See: [mix_gleam](https://hexdocs.pm/mix_gleam/)

### Using Gleam from Elixir

```elixir
# Call Gleam module from Elixir
:my_gleam_module.my_function("arg")
```

Gleam module `my_package/my_module` becomes Erlang module `:my_package@my_module`.

## Error Handling Interop

### Converting Erlang Error Tuples

```gleam
import gleam/erlang/atom

@external(erlang, "file", "read_file")
fn do_read_file(path: String) -> Result(BitArray, Atom)

pub fn read_file(path: String) -> Result(String, FileError) {
  case do_read_file(path) {
    Ok(content) -> {
      case bit_array.to_string(content) {
        Ok(text) -> Ok(text)
        Error(_) -> Error(InvalidEncoding)
      }
    }
    Error(reason) -> Error(FileSystemError(atom.to_string(reason)))
  }
}
```

### Erlang Exceptions

Erlang exceptions become Gleam panics. Wrap risky Erlang calls with proper error handling.

## Multi-Target Support

Write code that works on both targets:

```gleam
@external(erlang, "crypto", "strong_rand_bytes")
@external(javascript, "node:crypto", "randomBytes")
pub fn random_bytes(size: Int) -> BitArray
```

Or with fallback:

```gleam
@external(erlang, "lists", "reverse")
pub fn reverse(list: List(a)) -> List(a) {
  // Pure Gleam fallback
  do_reverse(list, [])
}

fn do_reverse(remaining: List(a), reversed: List(a)) -> List(a) {
  case remaining {
    [] -> reversed
    [x, ..xs] -> do_reverse(xs, [x, ..reversed])
  }
}
```

## Testing Erlang Integration

```gleam
pub fn erlang_interop_test() {
  let reversed = reverse_list([1, 2, 3])
  let assert [3, 2, 1] = reversed

  let upper = uppercase("hello")
  let assert "HELLO" = upper
}
```

Test both Gleam and Erlang implementations when available.

## Performance Considerations

### Tail Call Optimization

Erlang optimizes tail calls. Write recursive functions in tail position:

```gleam
// Tail recursive (optimized)
pub fn sum(list: List(Int), acc: Int) -> Int {
  case list {
    [] -> acc
    [x, ..rest] -> sum(rest, acc + x)
  }
}

// Not tail recursive (uses stack)
pub fn sum_bad(list: List(Int)) -> Int {
  case list {
    [] -> 0
    [x, ..rest] -> x + sum_bad(rest)  // Not tail position
  }
}
```

### Binary Handling

Binaries are efficient on BEAM. Use them for large data:

```gleam
// Efficient: builds binary once
pub fn build_large_string(parts: List(String)) -> String {
  string.concat(parts)
}
```

## Debugging

### Erlang Observer

Monitor your application:

```bash
erl -pa build/dev/erlang/*/ebin
```

Then in Erlang shell:
```erlang
observer:start().
```

### IO Debugging

```gleam
import gleam/io

pub fn debug(value: a) -> a {
  io.debug(value)
  value
}
```

## Best Practices

### DO: Wrap FFI in Safe APIs (MANDATORY)

```gleam
// Private FFI function
@external(erlang, "my_erlang_lib", "risky_function")
fn do_risky_function(arg: String) -> Dynamic

// Public safe wrapper
pub fn safe_function(arg: String) -> Result(Value, Error) {
  do_risky_function(arg)
  |> decode_response
  |> result.map_error(error_to_string)
}
```

### DO: Document Platform Requirements (MANDATORY)

```gleam
/// Hashes data using SHA-256.
///
/// **Platform**: Erlang only
/// **Requires**: Erlang crypto module
///
pub fn sha256(data: String) -> BitArray {
  // ...
}
```

### DO: Test Extensively (MANDATORY)

Write comprehensive tests for all external functions.

### DON'T: Skip Error Handling (FORBIDDEN)

Always wrap external calls with proper error handling.

### DON'T: Use FFI for Simple Operations (ANTI-PATTERN)

```gleam
// Bad - unnecessary FFI
@external(erlang, "math", "add")
pub fn add(a: Int, b: Int) -> Int

// Good - pure Gleam
pub fn add(a: Int, b: Int) -> Int {
  a + b
}
```

## Common Patterns

### Wrapping Erlang Libraries

Create type-safe wrappers for Erlang code:

```gleam
import gleam/dynamic.{type Dynamic}

// Low-level external
@external(erlang, "my_erlang_lib", "risky_function")
fn do_risky_function(arg: String) -> Dynamic

// Safe wrapper
pub fn safe_function(arg: String) -> Result(Value, Error) {
  let decoder = dynamic.tuple2(
    dynamic.string,
    decode_value,
  )

  do_risky_function(arg)
  |> decoder
  |> result.then(fn(tuple) {
    case tuple {
      #("ok", value) -> Ok(value)
      #("error", _) -> Error(OperationFailed)
      _ -> Error(UnexpectedResponse)
    }
  })
  |> result.map_error(fn(_) { DecodeFailed })
}
```

---

**Remember**: Gleam's Erlang target gives you full access to the BEAM ecosystem. Wrap external code for type safety.

See: [External Functions](../../rules/external-functions.md)
