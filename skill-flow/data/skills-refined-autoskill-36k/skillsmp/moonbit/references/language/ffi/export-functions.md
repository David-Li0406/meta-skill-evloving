### Foreign Function Interface (FFI)

#### Export Functions

For public functions that are neither methods nor polymorphic, they can be exported by configuring the `exports` field in [link configuration](../toolchain/moon/package.md#link-options).

```json
{
  "link": {
    "<backend>": {
      "exports": [ "add", "fib:test" ]
    }
  }
}
```

The previous example exports functions `add` and `fib`, where `fib` will be exported as `test`.

##### Wasm & Wasm GC

###### NOTE
It is only effective for the package that configures it, i.e. it doesn't affect the downstream packages.

##### JavaScript

###### NOTE
It is only effective for the package that configures it, i.e. it doesn't affect the downstream packages.

There's another `format` option to export as CommonJS module (`cjs`), ES Module (`esm`), or `iife`.

##### C

###### NOTE
It is only effective for the package that configures it, i.e. it doesn't affect the downstream packages.

Renaming the exported function is not supported for now

