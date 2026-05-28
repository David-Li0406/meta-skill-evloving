### Foreign Function Interface (FFI)

#### Backends

MoonBit currently have five backends:

- Wasm
- Wasm GC
- JavaScript
- C
- LLVM (experimental)

##### Wasm

By Wasm we refer to WebAssembly with some post-MVP proposals including:

- bulk-memory-operations
- multi-value
- reference-types

For better compatibility, the `init` function will be compiled as [`start` function](https://webassembly.github.io/spec/core/syntax/modules.html#start-function), and the `main` function will be exported as `_start`.

###### NOTE
For Wasm backends, all functions interacting with outside world relies on the host. For example, the `println` for Wasm and Wasm GC backend relies on importing a function `spectest.print_char` that prints a UTF-16 code unit for each call. The `env` package in standard library and some packages in `moonbitlang/x` relies on specific host function defined for MoonBit runtime. Avoid using them if you want to make the generated Wasm portable.

##### Wasm GC

By Wasm GC we refer to WebAssembly with Garbage Colleciton proposal, meaning that data structures will be represented with reference types such as `struct` `array` and the linear memory would not be used by default. It also supports other post-MVP proposals including:

- multi-value
- JS string builtins

For better compatibility, the `init` function will be compiled as [`start` function](https://webassembly.github.io/spec/core/syntax/modules.html#start-function), and the `main` function will be exported as `_start`.

###### NOTE
For Wasm backends, all functions interacting with outside world relies on the host. For example, the `println` for Wasm and Wasm GC backend relies on importing a function `spectest.print_char` that prints a UTF-16 code unit for each call. The `env` package in standard library and some packages in `moonbitlang/x` relies on specific host function defined for MoonBit runtime. Avoid using them if you want to make the generated Wasm portable.

##### JavaScript

JavaScript backend will generate a JavaScript file, which can be a CommonJS module, an ES module or an IIFE based on the [configuration](../toolchain/moon/package.md#js-backend-link-options).

##### C

C backend will generate a C file. The MoonBit toolchain will also compile the project and generate an executable based on the [configuration](../toolchain/moon/package.md#native-backend-link-options).

##### LLVM

LLVM backend will generate an object file. The backend is experimental and does not support FFIs.

