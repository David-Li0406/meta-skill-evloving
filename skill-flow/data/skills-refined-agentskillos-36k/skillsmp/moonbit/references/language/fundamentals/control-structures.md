### Fundamentals

#### Control Structures

##### Conditional Expressions

A conditional expression consists of a condition, a consequent, and an optional `else` clause or `else if` clause.

```moonbit
if x == y {
  expr1
} else if x == z {
  expr2
} else {
  expr3
}
```

The curly brackets around the consequent are required.

Note that a conditional expression always returns a value in MoonBit, and the return values of the consequent and the else clause must be of the same type. Here is an example:

```moonbit
let initial = if size < 1 { 1 } else { size }
```

The `else` clause can only be omitted if the return value has type `Unit`.

##### Match Expression

The `match` expression is similar to conditional expression, but it uses [pattern matching]() to decide which consequent to evaluate and extracting variables at the same time.

```moonbit
fn decide_sport(weather : String, humidity : Int) -> String {
  match weather {
    "sunny" => "tennis"
    "rainy" => if humidity > 80 { "swimming" } else { "football" }
    _ => "unknown"
  }
}

test {
  assert_eq(decide_sport("sunny", 0), "tennis")
}
```

If a possible condition is omitted, the compiler will issue a warning, and the program will terminate if that case were reached.

##### Guard Statement

The `guard` statement is used to check a specified invariant.
If the condition of the invariant is satisfied, the program continues executing
the subsequent statements and returns. If the condition is not satisfied (i.e., false),
the code in the `else` block is executed and its evaluation result is returned (the subsequent statements are skipped).

```moonbit
fn guarded_get(array : Array[Int], index : Int) -> Int? {
  guard index >= 0 && index < array.length() else { None }
  Some(array[index])
}

test {
  inspect(guarded_get([1, 2, 3], -1), content="None")
}
```

###### Guard statement and is expression

The `let` statement can be used with [pattern matching](). However, `let` statement can only handle one case. And using [is expression]() with `guard` statement can solve this issue.

In the following example, `getProcessedText` assumes that the input `path` points to resources that are all plain text,
and it uses the `guard` statement to ensure this invariant while extracting the plain text resource.
Compared to using a `match` statement, the subsequent processing of `text` can have one less level of indentation.

```moonbit
enum Resource {
  Folder(Array[String])
  PlainText(String)
  JsonConfig(Json)
}

fn getProcessedText(
  resources : Map[String, Resource],
  path : String,
) -> String raise Error {
  guard resources.get(path) is Some(resource) else { fail("\{path} not found") }
  guard resource is PlainText(text) else { fail("\{path} is not plain text") }
  process(text)
}
```

When the `else` part is omitted, the program terminates if the condition specified
in the `guard` statement is not true or cannot be matched.

```moonbit
guard condition  // <=> guard condition else { panic() }
guard expr is Some(x)
// <=> guard expr is Some(x) else { _ => panic() }
```

##### While loop

In MoonBit, `while` loop can be used to execute a block of code repeatedly as long as a condition is true. The condition is evaluated before executing the block of code. The `while` loop is defined using the `while` keyword, followed by a condition and the loop body. The loop body is a sequence of statements. The loop body is executed as long as the condition is true.

```moonbit
fn main {
  let mut i = 5
  while i > 0 {
    println(i)
    i = i - 1
  }
}
```

```default
5
4
3
2
1
```

The loop body supports `break` and `continue`. Using `break` allows you to exit the current loop, while using `continue` skips the remaining part of the current iteration and proceeds to the next iteration.

```moonbit
fn main {
  let mut i = 5
  while i > 0 {
    i = i - 1
    if i == 4 {
      continue
    }
    if i == 1 {
      break
    }
    println(i)
  }
}
```

```default
3
2
```

The `while` loop also supports an optional `else` clause. When the loop condition becomes false, the `else` clause will be executed, and then the loop will end.

```moonbit
fn main {
  let mut i = 2
  while i > 0 {
    println(i)
    i = i - 1
  } else {
    println(i)
  }
}
```

```default
2
1
0
```

When there is an `else` clause, the `while` loop can also return a value. The return value is the evaluation result of the `else` clause. In this case, if you use `break` to exit the loop, you need to provide a return value after `break`, which should be of the same type as the return value of the `else` clause.

```moonbit
fn main {
  let mut i = 10
  let r = while i > 0 {
    i = i - 1
    if i % 2 == 0 {
      break 5
    }
  } else {
    7
  }
  println(r)
}
```

```default
5
```

```moonbit
fn main {
  let mut i = 10
  let r = while i > 0 {
    i = i - 1
  } else {
    7
  }
  println(r)
}
```

```default
7
```

##### For Loop

MoonBit also supports C-style For loops. The keyword `for` is followed by variable initialization clauses, loop conditions, and update clauses separated by semicolons. They do not need to be enclosed in parentheses.
For example, the code below creates a new variable binding `i`, which has a scope throughout the entire loop and is immutable. This makes it easier to write clear code and reason about it:

```moonbit
fn main {
  for i = 0; i < 5; i = i + 1 {
    println(i)
  }
}
```

```default
0
1
2
3
4
```

The variable initialization clause can create multiple bindings:

```moonbit
for i = 0, j = 0; i + j < 100; i = i + 1, j = j + 1 {
  println(i)
}
```

It should be noted that in the update clause, when there are multiple binding variables, the semantics are to update them simultaneously. In other words, in the example above, the update clause does not execute `i = i + 1`, `j = j + 1` sequentially, but rather increments `i` and `j` at the same time. Therefore, when reading the values of the binding variables in the update clause, you will always get the values updated in the previous iteration.

Variable initialization clauses, loop conditions, and update clauses are all optional. For example, the following two are infinite loops:

```moonbit
for i = 1; ; i = i + 1 {
  println(i)
}
for {
  println("loop forever")
}
```

The `for` loop also supports `continue`, `break`, and `else` clauses. Like the `while` loop, the `for` loop can also return a value using the `break` and `else` clauses.

The `continue` statement skips the remaining part of the current iteration of the `for` loop (including the update clause) and proceeds to the next iteration. The `continue` statement can also update the binding variables of the `for` loop, as long as it is followed by expressions that match the number of binding variables, separated by commas.

For example, the following program calculates the sum of even numbers from 1 to 6:

```moonbit
fn main {
  let sum = for i = 1, acc = 0; i <= 6; i = i + 1 {
    if i % 2 == 0 {
      println("even: \{i}")
      continue i + 1, acc + i
    }
  } else {
    acc
  }
  println(sum)
}
```

```default
even: 2
even: 4
even: 6
12
```

##### `for .. in` loop

MoonBit supports traversing elements of different data structures and sequences via the `for .. in` loop syntax:

```moonbit
for x in [1, 2, 3] {
  println(x)
}
```

`for .. in` loop is translated to the use of `Iter` in MoonBit's standard library. Any type with a method `.iter() : Iter[T]` can be traversed using `for .. in`.
For more information of the `Iter` type, see [Iterator]() below.

`for .. in` loop also supports iterating through a sequence of integers, such as:

```moonbit
test {
  let mut i = 0
  for j in 0..<10 {
    i += j
  }
  assert_eq(i, 45)
  let mut k = 0
  for l in 0..=10 {
    k += l
  }
  assert_eq(k, 55)
}
```

In addition to sequences of a single value, MoonBit also supports traversing sequences of two values, such as `Map`, via the `Iter2` type in MoonBit's standard library.
Any type with method `.iter2() : Iter2[A, B]` can be traversed using `for .. in` with two loop variables:

```moonbit
for k, v in { "x": 1, "y": 2, "z": 3 } {
  println(k)
  println(v)
}
```

Another example of `for .. in` with two loop variables is traversing an array while keeping track of array index:

```moonbit
fn main {
  for index, elem in [4, 5, 6] {
    let i = index + 1
    println("The \{i}-th element of the array is \{elem}")
  }
}
```

```default
The 1-th element of the array is 4
The 2-th element of the array is 5
The 3-th element of the array is 6
```

Control flow operations such as `return`, `break` and error handling are supported in the body of `for .. in` loop:

```moonbit
fn main {
  let map = { "x": 1, "y": 2, "z": 3, "w": 4 }
  for k, v in map {
    if k == "y" {
      continue
    }
    println("\{k}, \{v}")
    if k == "z" {
      break
    }
  }
}
```

```default
x, 1
z, 3
```

If a loop variable is unused, it can be ignored with `_`.

##### Functional loop

Functional loop is a powerful feature in MoonBit that enables you to write loops in a functional style.

A functional loop consumes an argument and returns a value. It is defined using the `loop` keyword, followed by its argument and the loop body. The loop body is a sequence of clauses, each of which consists of a pattern and an expression. The clause whose pattern matches the input will be executed, and the loop will return the value of the expression. If no pattern matches, the loop will panic. Use the `continue` keyword with arguments to start the next iteration of the loop. Use the `break` keyword with an argument to return a value from the loop. The `break` keyword can be omitted if the value is the last expression in the loop body.

```moonbit
test {
  fn sum(xs : @list.List[Int]) -> Int {
    loop (xs, 0) {
      (Empty, acc) => break acc // <=> Nil, acc => acc
      (More(x, tail=rest), acc) => continue (rest, x + acc)
    }
  }

  assert_eq(sum(@list.from_array([1, 2, 3])), 6)
}
```

##### Labelled Continue/Break

When a loop is labelled, it can be referenced from a `break` or `continue` from
within a nested loop. For example:

```moonbit
test "break label" {
  let mut count = 0
  let xs = [1, 2, 3]
  let ys = [4, 5, 6]
  let res = outer~: for i in xs {
    for j in ys {
      count = count + i
      break outer~ j
    }
  } else {
    -1
  }
  assert_eq(res, 4)
  assert_eq(count, 1)
}

test "continue label" {
  let mut count = 0
  let init = 10
  let res = outer~: loop init {
    0 => 42
    i =>
      for {
        count = count + 1
        continue outer~ i - 1
      }
  }
  assert_eq(res, 42)
  assert_eq(count, 10)
}
```

##### `defer` expression

`defer` expression can be used to perform reliable resource cleanup.
The syntax for `defer` is as follows:

```moonbit
defer <expr>
<body>
```

Whenever the program leaves `body`, `expr` will be executed.
For example, the following program:

```moonbit
  defer println("perform resource cleanup")
  println("do things with the resource")
```

will first print `do things with the resource`, and then `perform resource cleanup`.
`defer` expression will always get executed no matter how its body exits.
It can handle [error](error-handling.md),
as well as control flow constructs including `return`, `break` and `continue`.

Consecutive `defer` will be executed in reverse order, for example, the following:

```moonbit
  defer println("first defer")
  defer println("second defer")
  println("do things")
```

will output first `do things`, then `second defer`, and finally `first defer`.

`return`, `break` and `continue` are disallowed in the right hand side of `defer`.
Currently, raising error or calling `async` function is also disallowed in the right hand side of `defer`.

