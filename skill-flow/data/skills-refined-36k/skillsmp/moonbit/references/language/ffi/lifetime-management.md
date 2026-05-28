### Foreign Function Interface (FFI)

#### Lifetime management

MoonBit is a programming language with garbage collection. Thus when handling external object or passing MoonBit object to host, it is essential to keep in mind the lifetime management. Currently, MoonBit uses reference counting for Wasm backend and C backend. For Wasm GC backend and JavaScript backend, the runtime's GC is reused.

##### Lifetime management of external object

When handling external object/resource in MoonBit, it is important to destroy object or release resource in time to prevent memory/resource leak.

###### NOTE
For C backend only

`moonbit.h` provides an API `moonbit_make_external_object` for handling lifetime of external object/resource using MoonBit's own automatic memory management system:

```c
void *moonbit_make_external_object(
  void (*finalize)(void *self),
  uint32_t payload_size
);
```

`moonbit_make_external_object` will create a new MoonBit object of size `payload_size + sizeof(finalize)`,
the layout of the object is as follows:

```default
| MoonBit object header | ... payload | finalize function |
                        ^
                        |
                        |_
                           pointer returned by `moonbit_make_external_object`
```

so you can treat the object as a pointer to its payload directly. When MoonBit's automatic memory management system finds that an object created by `moonbit_make_external_object` is no longer alive, it will invoke the function `finalize` with the object itself as argument. Now, `finalize` can release external resource/memory held by the object's payload.

###### NOTE
`finalize` **must not** drop the object itself, as this is handled by MoonBit runtime.

On the MoonBit side, objects returned by `moonbit_make_external_object`
should be bind to an *abstract* type, declared using `type T`,
so that MoonBit's memory management system will not ignore the object.

##### Lifetime management of MoonBit object

When passing MoonBit objects to the host through functions, it is essential to take care of the lifetime management of MoonBit itself. As mentioned before, MoonBit's Wasm backend and C backend uses compiler-optimized reference counting to manage lifetime of objects. To avoid memory error or leak, FFI functions must properly maintain the reference count of MoonBit objects.

###### NOTE
For C backend and for Wasm backend only.

###### The calling convention of reference counting

By default, MoonBit uses an owned calling convention for reference counting. That is, callee (the function being invoked) is responsible for dropping its parameters using the `moonbit_decref` / `$moonbit.decref` function. If the parameter is used more than once, the callee should increase the reference count using the `moonbit_incref` / `$moonbit.incref` function. Here are the rules for the necessary operations to perform in different circumstances:

| event                            | operation   |
|----------------------------------|-------------|
| read field/element               | nothing     |
| store into data structure        | `incref`    |
| passed to MoonBit function       | `incref`    |
| passed to other foreign function | nothing     |
| returned                         | nothing     |
| end of scope (not returned)      | `decref`    |

For example, here's a lifetime-correct binding to the standard `open` function for opening a file:

```moonbit
extern "C" fn open(filename : Bytes, flags : Int) -> Int = "open_ffi"
```

```c
int open_ffi(moonbit_bytes_t filename, int flags) {
  int fd = open(filename, flags);
  moonbit_decref(filename);
  return fd;
}
```

###### The managed types

The following types are always unboxed, so there is no need to manage their lifetime:

- builtin number types, such as `Int` and `Double`
- constant `enum` (`enum` where all constructors have no payload)

The following types are always boxed and reference counted:

- `FixedArray[T]`, `Bytes` and `String`
- abstract types (`type T`)

External types (`#external type T`) are also boxed, but they represent external pointers,
so MoonBit will not perform any reference counting operations on them.

The layout of `struct`/`enum` with payload is currently unstable.

###### The borrow and owned attribute

When passing a parameter through the FFI, its ownership may or may not be kept.
The `#borrow` and `#owned` attributes can be used to specify these two conditions.

###### WARNING
We are in the process of migrating the default semantics to `#borrow` instead of `#owned`

The syntax of `#borrow` and `#owned` are as follows:

```moonbit
###borrow(params..)
extern "C" fn c_ffi(..) -> .. = ..
```

where `params` is a subset of the parameters of `c_ffi`.

Parameters of `#borrow` will be passed using borrow based calling convention, that is, the invoked function does not need to `decref` these parameters. If the FFI function only read its parameter locally (i.e. does not return its parameters and does not store them in data structures), you can directly use the `#borrow` attribute. For example, the `open` function mentioned above could be rewritten using `#borrow` as follows:

```moonbit
###borrow(filename)
extern "C" fn open(filename : Bytes, flags : Int) -> Int = "open"
```

There is no need for a stub function anymore: we are binding to the original version of `open` here. With the `#borrow` attribute, this version is still lifetime-correct.

Even if a stub function is still necessary for other reasons, `#borrow` can often simplify the lifetime management. Here are the rules for the necessary operations to perform **on borrow parameters** in different circumstances:

| event                                                   | operation   |
|---------------------------------------------------------|-------------|
| read field / element                                    | nothing     |
| store into data structure                               | `incref`    |
| passed to MoonBit function                              | `incref`    |
| passed to other C function / `#borrow` MoonBit function | nothing     |
| returned                                                | `incref`    |
| end of scope (not returned)                             | nothing     |

The opposite is the `#owned` semantic, where the parameter is stored by the FFI function, and the `decref` needs to be executed manually later.
One use case is registering the callback where the closure would be **owned**.

