### Foreign Function Interface (FFI)

#### Declare Foreign Type

You can declare a foreign type using the `#extern` attribute like this:

```moonbit
###external
type ExternalRef
```

##### Wasm & Wasm GC

This will be interpreted as an [`externref`](https://webassembly.github.io/spec/core/syntax/types.html#reference-types).

##### JavaScript

This will be interpreted as a JavaScript value.

##### C

This will be interpreted as `void*`.

