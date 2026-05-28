# East

East is a programming language for the Elara platform (originally meaning "Elara AST").

## Purpose

Elara is a real-time analytics platform for business optimization.
Solutions are developed declaritively with a TypeScript SDK and a "template" of the solution is uploaded to the Elara platform to host and execute.
Logic in these solutions can appear in many places: 

 * Transformation of business data
 * Implementation of business logic and simulations of businesses
 * Algorithms for optimization problems
 * To define how values a displayed in end-user-facing dashboards and layouts
 * End-user-defined filters and transforms in the web UI

## Design

People using Elara's SDK will be business analysts, consultants and data scientists (i.e. NOT software engineers).
East needs to be easy to understand and write while being fast and safe to execute on Elara's servers, user's browsers, etc.
These requirements lead to the following design principles:

 * A simple and familiar language for expressing logic and algorithms
 * Statically typed for speed and correctness
 * Structurally typed for ease of use and lightweight scripting
 * Designed with controlled side-effects, security and embedding in platforms in mind
 * Uses serializable IR as a "narrow waist" so that logic can be saved, transmitted, and executed in different environments / other runtimes

## Structure

East is a single-dependency TypeScript package containing the core language IR, a fluent interface to define expressions, a type checker and compiler(s).

 * /src - source code for the main East language package, including unit tests for this package
 * /src/containers - JavaScript runtime containers for sorted sets, dicts and variants (i.e. tagged union/sum type)
 * /src/expr - Front-end fluent interface for building East expressions in TypeScript
 * /src/serialization - reading and writing data
 * /src/datetime_format - datetime format specifiers, printers and parsers
 * /test - compliance suite for the East language, executed on a self-hosted test platform (and other backends to check compliance)
 * /devdocs - living documentation on East design
 * /example - informal example programs to experiment with East functionality
 * /contrib - place to store examples, scripts and experiments

## Development

When making changes to the East codebase always run:

 * `npm run build` - compile TypeScript to JavaScript
 * `npm run test` - run the test suite (runs the compiled .js - requires build first)
 * `npm run lint` - check code quality with ESLint (must pass before committing)

ESLint is configured to be compiler-friendly: `any` types are allowed due to type erasure needs and TypeScript's recursive type limitations.
Avoid `any` as much as possible.

Our JavaScript compiler uses a simple and robust closure-compiler technique to produce a relatively efficient JS function that can be executed. This is our reference compiler and must be kept functional and correct at ALL times. In future we will be creating backends that can evaluate IR in other languages such as Julia and Python (the Julia one in particilar will compile to fast, native code using metaprogramming techniques).

## Documentation and Testing Standards

**CRITICAL: All development MUST follow the standards defined in [STANDARDS.md](./STANDARDS.md).**

This file contains mandatory requirements for:
- **TypeDoc documentation** for all public APIs (classes, methods, types, functions)
- **USAGE.md documentation** patterns for end-user facing documentation
- **Testing standards** for the compliance test suite in `/test`

Key highlights:
- **Expression classes** (in `/src/expr/` and `/src/expr/libs/`):
  - Examples MUST use complete `East.function()` → `East.compile()` → execution flow
  - All examples MUST be validated using the `mcp__east-mcp__east_compile` tool
  - Use `@throws East runtime error if <condition>` format
- **Regular classes** (all other code):
  - Examples show typical usage patterns (no compile flow required)
  - Use `@throws {ErrorType} <description>` format
  - No `mcp__east-mcp__east_compile` validation needed
- USAGE.md MUST follow precise table formatting and example structure
- All functionality MUST have comprehensive test coverage in `/test`

**See [STANDARDS.md](./STANDARDS.md) for complete, detailed requirements.**

## Type system

 * Never ("bottom" type)
 * Null ("unit" type) - `null`
 * Boolean - `true`, `false`
 * Integer - `0`, `42`, `-10`
 * Float - `0.0`, `3.14`, `-1e6`, `Infinity`, `-Infinity`, `NaN`
 * DateTime - `2025-01-01T00:00:00.000`
 * String - `""`, `"abc"`
 * Blob (binary bytes, immutable much like a string) - `0x`, `0x00ff`
 * Array (mutable, ordered collection of values) - `[]`, `[1, 2, 3]`
 * Set (mutable, sorted collection of keys) - `{}`, `{"a", "b", "c"}`
 * Dict (mutable, sorted collection of keys and values) - `{:}`, `{"a": 1, "b": 2, "c": 3}`
 * Struct (product type, immutable) - `(a=1, b=true)`
 * Variant (sum type, immutable) - `.some 42`, `.none` (for `.none null`)
 * Recursive (immutable, allows tree, DAG or circular data structures) - transparent semantics
 * Function (first-class, concretely-typed, multiple arguments, can be serialized as IR but not as "data") - no syntax

There are no abstract types (though builtin functions are generic, like getting an element from an array is `Array<T> -> T`).
All types (except functions) have a defined total ordering (even Floats).

**Serialization**: For a comprehensive specification of how East types and values are represented, compared, and serialized across different formats (East text, JSON, BEAST v1/v2), see [SERIALIZATION.md](devdocs/SERIALIZATION.md). This document is the canonical reference for implementing East in other languages.

## Semantics

East is a relatively standard imperative language that includes variable declaration/reassignment, loops, conditionals, blocks, throw-try-catch, early returns and labelled break/continue - very much like a "strongly typed JavaScript" with sum-types and an expression-based grammar.
The only mechanism to create a "union" type is via polymorphic variants with distinct tags, and there is no `any`/`unknown`/"top" type.
Type inference is forward-only (no unification step) and functions must include concrete type signatures.

East is an embedded language (like Lua) and each program is intended to run on a "platform".
Platforms inject functions that may perform effects in the platform the code is executing on.
The builtin functions can e.g. mutate arrays but not perform any external effects (including logging or writing to stdout - these must be provided by the platform).
Even undesirable mutation of data by user scripts can be avoided by platforms "freezing" input data and using runtime checking (static checking was deemed too complex for the front-end, but a sophisticated back-end might take that approach instead).
The parsers here provide an option for producing frozen data out-of-the-box.
This way we end up with fast imperative code that is also safe and secure to execute without a complex sandbox.

East takes care to avoid undefined behavior and unexpected runtime errors.
Operations like indexing are treated carefully with out-of-bounds errors handled as an explicit branch by the language.
East supports exceptions and try-catch for error handling.
(Generally we use the Option type and exceptions, but not the Result type).

East code is to be considered single-threaded with no provided async or parallelism capabilities (though the platform/runtime is free to execute a script asynchronously, so long as effects are presented to the script as "blocking" and any data shared in parallel is frozen).
