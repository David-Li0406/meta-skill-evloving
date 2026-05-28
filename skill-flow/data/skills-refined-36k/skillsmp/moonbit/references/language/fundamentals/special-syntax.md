### Fundamentals

#### Special Syntax

##### Pipelines

MoonBit provides a convenient pipe syntax `x |> f(y)`, which can be used to chain regular function calls:

```moonbit
5 |> ignore // <=> ignore(5)
[] |> Array::push(5) // <=> Array::push([], 5)
1
|> add(5) // <=> add(1, 5)
|> ignore // <=> ignore(add(1, 5))
```

The MoonBit code follows the *data-first* style, meaning the function places its "subject" as the first argument.
Thus, the pipe operator inserts the left-hand side value into the first argument of the right-hand side function call by default.
For example, `x |> f(y)` is equivalent to `f(x, y)`.

You can use the `_` operator to insert `x` into any argument of the function `f`, such as `x |> f(y, _)`, which is equivalent to `f(y, x)`. Labeled arguments are also supported.

##### Cascade Operator

The cascade operator `..` is used to perform a series of mutable operations on
the same value consecutively. The syntax is as follows:

```moonbit
[]..append([1])
```

- `x..f()..g()` is equivalent to `{ x.f(); x.g(); }`.
- `x..f().g()` is equivalent to `{ x.f(); x.g(); }`.

Consider the following scenario: for a `StringBuilder` type that has methods
like `write_string`, `write_char`, `write_object`, etc., we often need to perform
a series of operations on the same `StringBuilder` value:

```moonbit
let builder = StringBuilder::new()
builder.write_char('a')
builder.write_char('a')
builder.write_object(1001)
builder.write_string("abcdef")
let result = builder.to_string()
```

To avoid repetitive typing of `builder`, its methods are often designed to
return `self` itself, allowing operations to be chained using the `.` operator.
To distinguish between immutable and mutable operations, in MoonBit,
for all methods that return `Unit`, cascade operator can be used for
consecutive operations without the need to modify the return type of the methods.

```moonbit
let result = StringBuilder::new()
  ..write_char('a')
  ..write_char('a')
  ..write_object(1001)
  ..write_string("abcdef")
  .to_string()
```

##### is Expression

The `is` expression tests whether a value conforms to a specific pattern. It
returns a `Bool` value and can be used anywhere a boolean value is expected,
for example:

```moonbit
fn[T] is_none(x : T?) -> Bool {
  x is None
}

fn start_with_lower_letter(s : String) -> Bool {
  s is ['a'..='z', ..]
}
```

Pattern binders introduced by `is` expressions can be used in the following
contexts:

1. In boolean AND expressions (`&&`):
   binders introduced in the left-hand expression can be used in the right-hand
   expression
   ```moonbit
   fn f(x : Int?) -> Bool {
     x is Some(v) && v >= 0
   }
   ```
2. In the first branch of `if` expression: if the condition is a sequence of
   boolean expressions `e1 && e2 && ...`, the binders introduced by the `is`
   expression can be used in the branch where the condition evaluates to `true`.
   ```moonbit
   fn g(x : Array[Int?]) -> Unit {
     if x is [v, .. rest] && v is Some(i) && i is (0..=10) {
       println(v)
       println(i)
       println(rest)
     }
   }
   ```
3. In the following statements of a `guard` condition:
   ```moonbit
   fn h(x : Int?) -> Unit {
     guard x is Some(v)
     println(v)
   }
   ```
4. In the body of a `while` loop:
   ```moonbit
   fn i(x : Int?) -> Unit {
     let mut m = x
     while m is Some(v) {
       println(v)
       m = None
     }
   }
   ```

Note that `is` expression can only take a simple pattern. If you need to use
`as` to bind the pattern to a variable, you have to add parentheses. For
example:

```moonbit
fn j(x : Int) -> Int? {
  Some(x)
}

fn init {
  guard j(42) is (Some(a) as b)
  println(a)
  println(b)
}
```

##### Spread Operator

MoonBit provides a spread operator to expand a sequence of elements when
constructing `Array`, `String`, and `Bytes` using the array literal syntax. To
expand such a sequence, it needs to be prefixed with `..`, and it must have
`iter()` method that yields the corresponding type of element.

For example, we can use the spread operator to construct an array:

```moonbit
test {
  let a1 : Array[Int] = [1, 2, 3]
  let a2 : FixedArray[Int] = [4, 5, 6]
  let a3 : @list.List[Int] = @list.from_array([7, 8, 9])
  let a : Array[Int] = [..a1, ..a2, ..a3, 10]
  inspect(a, content="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]")
}
```

Similarly, we can use the spread operator to construct a string:

```moonbit
test {
  let s1 : String = "Hello"
  let s2 : StringView = "World".view()
  let s3 : Array[Char] = [..s1, ' ', ..s2, '!']
  let s : String = [..s1, ' ', ..s2, '!', ..s3]
  inspect(s, content="Hello World!Hello World!")
}
```

The last example shows how the spread operator can be used to construct a bytes
sequence.

```moonbit
test {
  let b1 : Bytes = "hello"
  let b2 : BytesView = b1[1:4]
  let b : Bytes = [..b1, ..b2, 10]
  inspect(
    b,
    content=(
      #|b"helloell\x0a"
    ),
  )
}
```

##### TODO syntax

The `todo` syntax (`...`) is a special construct used to mark sections of code that are not yet implemented or are placeholders for future functionality. For example:

```moonbit
fn todo_in_func() -> Int {
  ...
}
```

