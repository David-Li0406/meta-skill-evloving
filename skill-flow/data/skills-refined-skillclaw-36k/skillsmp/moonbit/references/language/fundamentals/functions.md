### Fundamentals

#### Functions

Functions take arguments and produce a result. In MoonBit, functions are first-class, which means that functions can be arguments or return values of other functions. MoonBit's naming convention requires that function names should not begin with uppercase letters (A-Z). Compare for constructors in the `enum` section below.

##### Top-Level Functions

Functions can be defined as top-level or local. We can use the `fn` keyword to define a top-level function that sums three integers and returns the result, as follows:

```moonbit
fn add3(x : Int, y : Int, z : Int) -> Int {
  x + y + z
}
```

Note that the arguments and return value of top-level functions require **explicit** type annotations.

##### Local Functions

Local functions can be named or anonymous. Type annotations can be omitted for local function definitions: they can be automatically inferred in most cases. For example:

```moonbit
fn local_1() -> Int {
  fn inc(x) { // named as `inc`
    x + 1
  }
  // anonymous, instantly applied to integer literal 6
  (fn(x) { x + inc(2) })(6)
}

test {
  assert_eq(local_1(), 9)
}
```

For simple anonymous function, MoonBit provides a very concise syntax called arrow function:

```moonbit
  [1, 2, 3].eachi((i, x) => println("\{i} => \{x}"))
  // parenthesis can be omitted when there is only one parameter
  [1, 2, 3].each(x => println(x * x))
```

Functions, whether named or anonymous, are *lexical closures*: any identifiers without a local binding must refer to bindings from a surrounding lexical scope. For example:

```moonbit
let global_y = 3

fn local_2(x : Int) -> (Int, Int) {
  fn inc() {
    x + 1
  }

  fn four() {
    global_y + 1
  }

  (inc(), four())
}

test {
  assert_eq(local_2(3), (4, 4))
}
```

A local function can only refer to itself and other previously defined local functions.
To define  mutually recursive local functions, use the syntax `letrec f = .. and g = ..` instead:

```moonbit
  fn f(x) {
    // `f` can refer to itself here, but cannot use `g`
    if x > 0 {
      f(x - 1)
    }
  }

  fn g(x) {
    // `g` can refer to `f` and `g` itself
    if x < 0 {
      f(-x)
    } else {
      f(x)
    }
  }
  // mutually recursive local functions
  letrec even = x => x == 0 || odd(x - 1)
  and odd = x => x != 0 && even(x - 1)
```

##### Function Applications

A function can be applied to a list of arguments in parentheses:

```moonbit
add3(1, 2, 7)
```

This works whether `add3` is a function defined with a name (as in the previous example), or a variable bound to a function value, as shown below:

```moonbit
test {
  let add3 = fn(x, y, z) { x + y + z }
  assert_eq(add3(1, 2, 7), 10)
}
```

The expression `add3(1, 2, 7)` returns `10`. Any expression that evaluates to a function value is applicable:

```moonbit
test {
  let f = fn(x) { x + 1 }
  let g = fn(x) { x + 2 }
  let w = (if true { f } else { g })(3)
  assert_eq(w, 4)
}
```

##### Partial Applications

Partial application is a technique of applying a function to some of its arguments, resulting in a new function that takes the remaining arguments. In MoonBit, partial application is achieved by using the `_` operator in function application:

```moonbit
fn add(x : Int, y : Int) -> Int {
  x + y
}

test {
  let add10 : (Int) -> Int = add(10, _)
  println(add10(5)) // prints 15
  println(add10(10)) // prints 20
}
```

The `_` operator represents the missing argument in parentheses. The partial application allows multiple `_` in the same parentheses.
For example, `Array::fold(_, _, init=5)` is equivalent to `fn(x, y) { Array::fold(x, y, init=5) }`.

The `_` operator can also be used in enum creation, dot style function calls and in the pipelines.

##### Labelled arguments

**Top-level** functions can declare labelled argument with the syntax `label~ : Type`. `label` will also serve as parameter name inside function body:

```moonbit
fn labelled_1(arg1~ : Int, arg2~ : Int) -> Int {
  arg1 + arg2
}
```

Labelled arguments can be supplied via the syntax `label=arg`. `label=label` can be abbreviated as `label~`:

```moonbit
test {
  let arg1 = 1
  assert_eq(labelled_1(arg2=2, arg1~), 3)
}
```

Labelled function can be supplied in any order. The evaluation order of arguments is the same as the order of parameters in function declaration.

##### Optional arguments

An argument can be made optional by supplying a default expression with the syntax `label?: Type = default_expr`, where the `default_expr` may be omitted. If this argument is not supplied at call site, the default expression will be used:

```moonbit
fn optional(opt? : Int = 42) -> Int {
  opt
}

test {
  assert_eq(optional(), 42)
  assert_eq(optional(opt=0), 0)
}
```

The default expression will be evaluated every time it is used. And the side effect in the default expression, if any, will also be triggered. For example:

```moonbit
fn incr(counter? : Ref[Int] = { val: 0 }) -> Ref[Int] {
  counter.val = counter.val + 1
  counter
}

test {
  inspect(incr(), content="{val: 1}")
  inspect(incr(), content="{val: 1}")
  let counter : Ref[Int] = { val: 0 }
  inspect(incr(counter~), content="{val: 1}")
  inspect(incr(counter~), content="{val: 2}")
}
```

If you want to share the result of default expression between different function calls, you can lift the default expression to a toplevel `let` declaration:

```moonbit
let default_counter : Ref[Int] = { val: 0 }

fn incr_2(counter? : Ref[Int] = default_counter) -> Int {
  counter.val = counter.val + 1
  counter.val
}

test {
  assert_eq(incr_2(), 1)
  assert_eq(incr_2(), 2)
}
```

The default expression can depend on previous arguments, such as:

```moonbit
fn create_rectangle(a : Int, b? : Int = a) -> (Int, Int) {
  (a, b)
}

test {
  inspect(create_rectangle(10), content="(10, 10)")
}
```

###### Optional arguments without default values

It is quite common to have different semantics when a user does not provide a value.
Optional arguments without default values have type `T?` and `None` as the default value.
When supplying this kind of optional argument directly, MoonBit will automatically wrap the value with `Some`:

```moonbit
fn new_image(width? : Int, height? : Int) -> Image {
  if width is Some(w) {
    ...
  }
  ...
}

let img2 : Image = new_image(width=1920, height=1080)
```

Sometimes, it is also useful to pass a value of type `T?` directly,
for example when forwarding optional argument.
MoonBit provides a syntax `label?=value` for this, with `label?` being an abbreviation of `label?=label`:

```moonbit
fn image(width? : Int, height? : Int) -> Image {
  ...
}

fn fixed_width_image(height? : Int) -> Image {
  image(width=1920, height?)
}
```

##### Autofill arguments

MoonBit supports filling specific types of arguments automatically at different call site, such as the source location of a function call.
To declare an autofill argument, simply declare a labelled argument, and add a function attribute `#callsite(autofill(param_a, param_b))`.
Now if the argument is not explicitly supplied, MoonBit will automatically fill it at the call site.

Currently MoonBit supports two types of autofill arguments, `SourceLoc`, which is the source location of the whole function call,
and `ArgsLoc`, which is a array containing the source location of each argument, if any:

```moonbit
###callsite(autofill(loc, args_loc))
fn f(_x : Int, loc~ : SourceLoc, args_loc~ : ArgsLoc) -> String {
  (
    $|loc of whole function call: \{loc}
    $|loc of arguments: \{args_loc}
  )
  // loc of whole function call: <filename>:7:3-7:10
  // loc of arguments: [Some(<filename>:7:5-7:6), Some(<filename>:7:8-7:9), None, None]
}
```

Autofill arguments are very useful for writing debugging and testing utilities.

##### Function alias

MoonBit allows calling functions with alternative names via function alias. Function alias can be declared as follows:

```moonbit
###alias(g)
###alias(h, visibility="pub")
fn k() -> Bool {
  true
}
```

You can also create function alias that has different visibility with the field `visibility`.

