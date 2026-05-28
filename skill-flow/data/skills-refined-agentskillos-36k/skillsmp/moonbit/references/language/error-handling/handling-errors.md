### Error handling

#### Handling Errors

Applying the function normally will rethrow the error directly in case of an
error. For example:

```moonbit
fn div_reraise(x : Int, y : Int) -> Int raise DivError {
  div(x, y) // Rethrow the error if `div` raised an error
}
```

However, you may want to handle the errors.

##### Try ... Catch

You can use `try` and `catch` to catch and handle errors, for example:

```moonbit
fn main {
  try div(42, 0) catch {
    DivError(s) => println(s)
  } noraise {
    v => println(v)
  }
}
```

```default
division by zero
```

Here, `try` is used to call a function that might throw an error, and `catch` is
used to match and handle the caught error. If no error is caught, the catch
block will not be executed and the `noraise` block will be executed instead.

The `noraise` block can be omitted if no action is needed when no error is
caught. For example:

```moonbit
try { println(div(42, 0)) } catch {
  _ => println("Error")
}
```

When the body of `try` is a simple expression, the curly braces, and even the
`try` keyword can be omitted. For example:

```moonbit
let a = div(42, 0) catch { _ => 0 }
println(a)
```

##### Transforming to Result

You can also catch the potential error and transform into a first-class value of
the [`Result`](fundamentals.md#option-and-result) type, by using
`try?` before an expression that may throw error:

```moonbit
test {
  let res = try? (div(6, 0) * div(6, 3))
  inspect(
    res,
    content=(
      #|Err("division by zero")
    ),
  )
}
```

##### Panic on Errors

You can also panic directly when an unexpected error occurs:

```moonbit
fn remainder(a : Int, b : Int) -> Int raise DivError {
  if b == 0 {
    raise DivError("division by zero")
  }
  let div = try! div(a, b)
  a - b * div
}
```

##### Error Inference

Within a `try` block, several different kinds of errors can be raised. When that
happens, the compiler will use the type `Error` as the common error type.
Accordingly, the handler must use the wildcard `_` to make sure all errors are
caught, and `e => raise e` to reraise the other errors. For example,

```moonbit
fn f1() -> Unit raise E1 {
  ...
}

fn f2() -> Unit raise E2 {
  ...
}

try {
  f1()
  f2()
} catch {
  E1(_) => ...
  E2 => ...
  e => raise e
}
```

