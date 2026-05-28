# East Module System

This document describes the module system for East, including the structure of modules, programs, and runtime linking.

## Overview

East modules are self-contained units of IR that can be composed into larger programs. The key principles are:

1. **Modules are IR that evaluate to a value** - East is expression-based, and a module's IR is an expression whose result becomes its export.
2. **Single export per module** - A module exports exactly one value (typically a struct of functions).
3. **Modules execute once** - Upon first import, a module's IR is evaluated and the result is cached.
4. **Programs are callable modules** - A "program" is a module whose export type is `.Function`.

## Module Structure

A module is represented as an East value with the following `EastType`:

```ts
type ModuleType = StructType<{
    name: StringType,
    type: EastTypeValueType,
    ir: IR,
    imports: DictType<StringType, ImportType>,
}>;

type ImportType = VariantType<{
    bundled: ModuleType,
    external: StructType<{
        package: String, // the name of the package
        name: String, // the name of the module (the same as in `ModuleType`)
        type: EastTypeValueType,
    }>,
}>;
```

The `imports` dictionary maps local names (arbitrary strings chosen by the module author) to either:
- **bundled**: An inline module included in this bundle
- **external**: A reference to a module in another package, identified by package name and module name

### Example

```
(
    name="main",
    type=.Function (inputs=[.Array .String], output=.Integer, platforms=[]),
    ir=...,
    imports={
        "math": .bundled (
            name="math",
            type=.Struct [(name="add", type=.Function ...)],
            ir=...,
            imports={:},
        ),
        "east-python/fs": .external (package="east-python", name="fs", type=...),
        "east-core/json": .external (package="east-core", name="json", type=...),
    },
)
```

In this example:
- `"math"` is a local name for a bundled module
- `"fs"` refers to the `fs` module from the `east-python` package
- `"json"` refers to the `json` module from the `east-core` package

## ImportIR

`PlatformIR` is replaced with `ImportIR`:

```
ImportIR = Variant<"Import", {
    type: EastType,
    location: Location,
    name: String,
}>
```

When evaluated, `ImportIR`:
1. Looks up `name` in the current module's `imports` dict
2. If not found, raises a linking error
3. If `.bundled`, returns the cached value (executing the module if not yet cached)
4. If `.external`, looks up the module in the runtime environment and returns its cached value

## Runtime Environment Contract

The East language specification does not define packages, package management, or module resolution. These are concerns of the runtime environment (e.g., e3).

The specification requires only that:

1. **Uniqueness**: The environment MUST ensure that external module references (`package`, `module` pairs) resolve unambiguously.
2. **Availability**: The environment MUST ensure that all external modules are available before execution begins.
3. **Linking errors**: If an external module cannot be resolved, the environment MUST produce an error during linking, prior to execution.
4. **Type checking**: The environment SHOULD verify that resolved modules have types compatible with what importers expect.

## Runtime Evaluation

The runtime maintains a module cache: `Dict<ModuleIdentity, Value>`.

When evaluating a module:

1. Check if module is in cache → return cached value
2. For each import in the module's `imports`:
   - If `.bundled`: recursively evaluate the bundled module
   - If `.external`: retrieve from environment (must already be linked)
3. Execute the module's IR with imports available
4. Cache and return the result

### Circular Dependencies

Circular imports are **not supported**. The module dependency graph must be acyclic. Attempting to import a module that is currently being evaluated results in a runtime error.

This keeps the semantics simple. If cyclic structures are needed, they should be expressed within a single module using East's recursive types.

## Programs

A **program** is a module whose `type` is a `Function`. The function's signature defines how the program is invoked:

- `(args: Array<String>) => Integer` - CLI program
- `(request: HttpRequest) => HttpResponse` - HTTP handler
- `(input: T) => U` - Generic transformation (for e3 tasks/dataflows)

The runner determines what signature(s) it supports and how to provide arguments.

## Package Publishing (e3 Concern)

When publishing a module as part of a package:

1. The publisher provides a **package name** (e.g., `east-python`, `myapp`)
2. The publisher declares which modules are **public** and their names within the package namespace (e.g., `fs`, `clock`, `net`)
3. The full module identifier becomes `{package}/{module}` (e.g., `east-python/fs`)
4. Private/internal modules are bundled but not exposed in the package's public API

This namespacing ensures that module names are globally unique when combined with their package name.

## Front-End Considerations

The East language does not yet have a concrete syntax. The current implementation uses a TypeScript fluent interface.

When a concrete syntax is defined, import specifiers in source code might look like:
```
import fs from "east-python/fs"      // external package module
import json from "east-core/json"    // external package module
import utils from "./utils"          // relative (same package)
```

The front-end/bundler is responsible for:
1. Resolving relative imports to module definitions
2. Assigning local names in the `imports` dict
3. Bundling dependencies or leaving them as external references
4. Deduplicating shared bundled dependencies
