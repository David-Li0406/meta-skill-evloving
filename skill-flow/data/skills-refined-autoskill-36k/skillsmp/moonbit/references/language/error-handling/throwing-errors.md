### Error handling

#### Throwing Errors

The keyword `raise` is used to interrupt the function execution and return an
error.

The type declaration of a function can use `raise` with an Error type to
indicate that the function might raise an error during an execution. For
example, the following function `div` might return an error of type `DivError`:

```moonbit
suberror DivError String

fn div(x : Int, y : Int) -> Int raise DivError {
  if y == 0 {
    raise DivError("division by zero")
  }
  x / y
}
```

The `Error` can be used when the concrete error type is not important. For
convenience, you can omit the error type after the `raise` to indicate that the
`Error` type is used. For example, the following function signatures are
equivalent:

```moonbit
fn f() -> Unit raise {
  ...
}

fn g() -> Unit raise Error {
  let h : () -> Unit raise = fn() raise { fail("fail") }
  ...
}
```

For functions that are generic in the error type, you can use the `Error` bound
to do that. For example,

```moonbit
// Result::unwrap_or_error
fn[T, E : Error] unwrap_or_error(result : Result[T, E]) -> T raise E {
  match result {
    Ok(x) => x
    Err(e) => raise e
  }
}
```

For functions that do not raise an error, you can add `noraise` in the
signature. For example:

```moonbit
fn add(a : Int, b : Int) -> Int noraise {
  a + b
}
```

##### Error Polymorphism

It happens when a higher order function accepts another function as parameter.
The function as parameter may or may not throw error, which in turn affects the
behavior of this function.

A notable example is `map` of `Array`:

```moonbit
fn[T] map(array : Array[T], f : (T) -> T raise) -> Array[T] raise {
  let mut res = []
  for x in array {
    res.push(f(x))
  }
  res
}
```

However, writing so would make the `map` function constantly having the
possibility of throwing errors, which is not the case.

Thus, the error polymorphism is introduced. You may use `raise?` to signify that
an error may or may not be throw.

```moonbit
fn[T] map_with_polymorphism(
  array : Array[T],
  f : (T) -> T raise?
) -> Array[T] raise? {
  let mut res = []
  for x in array {
    res.push(f(x))
  }
  res
}

fn[T] map_without_error(
  array : Array[T],
  f : (T) -> T noraise,
) -> Array[T] noraise {
  map_with_polymorphism(array, f)
}

fn[T] map_with_error(array : Array[T], f : (T) -> T raise) -> Array[T] raise {
  map_with_polymorphism(array, f)
}
```

The signature of the `map_with_polymorphism` will be determined by the actual
parameter.

