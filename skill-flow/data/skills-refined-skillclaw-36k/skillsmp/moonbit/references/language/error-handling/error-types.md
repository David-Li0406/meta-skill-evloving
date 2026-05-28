### Error handling

#### Error Types

In MoonBit, all the error values can be represented by the `Error` type, a
generalized error type.

However, an `Error` cannot be constructed directly. A concrete error type must
be defined, in the following forms:

```moonbit
suberror E1 Int // error type E1 has one constructor E1 with an Int payload

suberror E2 // error type E2 has one constructor E2 with no payload

suberror E3 { // error type E3 has three constructors like a normal enum type
  A
  B(Int, x~ : String)
  C(mut x~ : String, Char, y~ : Bool)
}
```

The error types can be promoted to the `Error` type automatically, and pattern
matched back:

```moonbit
suberror CustomError UInt

test {
  let e : Error = CustomError(42)
  guard e is CustomError(m)
  assert_eq(m, 42)
}
```

Since the type `Error` can include multiple error types, pattern matching on the
`Error` type must use the wildcard `_` to match all error types. For example,

```moonbit
fn f(e : Error) -> Unit {
  match e {
    E2 => println("E2")
    A => println("A")
    B(i, x~) => println("B(\{i}, \{x})")
    _ => println("unknown error")
  }
}
```

The `Error` is meant to be used where no concrete error type is needed, or a
catch-all for all kinds of sub-errors is needed.

##### Failure

A builtin error type is `Failure`.

There's a handly `fail` function, which is merely a constructor with a
pre-defined output template for showing both the error and the source location.
In practice, `fail` is always preferred over `Failure`.

<!-- MANUAL CHECK -->
```moonbit
###callsite(autofill(loc))
pub fn[T] fail(msg : String, loc~ : SourceLoc) -> T raise Failure {
  raise Failure("FAILED: \{loc} \{msg}")
}
```

