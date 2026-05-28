# Common AILANG Patterns

> **Note:** Run `ailang prompt` first for the most current syntax and examples.
> This reference shows common patterns - the CLI prompt is the source of truth.

## Recursion (No Loops!)

AILANG has no `for` or `while`. Use recursion instead.

### Sum a List
```ailang
export func sum(xs: [int]) -> int {
  match xs {
    [] => 0,
    hd :: tl => hd + sum(tl)
  }
}
```

### Map over a List
```ailang
export func map[a, b](f: func(a) -> b, xs: [a]) -> [b] {
  match xs {
    [] => [],
    hd :: tl => f(hd) :: map(f, tl)
  }
}
```

### Filter a List
```ailang
export func filter[a](pred: func(a) -> bool, xs: [a]) -> [a] {
  match xs {
    [] => [],
    hd :: tl => if pred(hd) then hd :: filter(pred, tl) else filter(pred, tl)
  }
}
```

### Fold (Reduce)
```ailang
export func fold[a, b](f: func(b, a) -> b, init: b, xs: [a]) -> b {
  match xs {
    [] => init,
    hd :: tl => fold(f, f(init, hd), tl)
  }
}
```

## Effects and IO

### Basic IO
```ailang
import std/io (println, readLine)

export func main() -> () ! {IO} {
  println("What is your name?");
  let name = readLine();
  println("Hello, " ++ name ++ "!")
}
```

### File IO
```ailang
import std/fs (readFile, writeFile)

export func copyFile(src: string, dst: string) -> () ! {FS} {
  let contents = readFile(src);
  writeFile(dst, contents)
}
```

### Multiple Effects
```ailang
import std/io (println)
import std/fs (readFile)

export func showFile(path: string) -> () ! {IO, FS} {
  let contents = readFile(path);
  println(contents)
}
```

## Pattern Matching

### Option Type
```ailang
type Option[a] = Some(a) | None

export func map[a, b](f: func(a) -> b, opt: Option[a]) -> Option[b] {
  match opt {
    Some(x) => Some(f(x)),
    None => None
  }
}

export func getOrElse[a](opt: Option[a], default: a) -> a {
  match opt {
    Some(x) => x,
    None => default
  }
}
```

### Result Type
```ailang
type Result[a, e] = Ok(a) | Err(e)

export func map[a, b, e](f: func(a) -> b, res: Result[a, e]) -> Result[b, e] {
  match res {
    Ok(x) => Ok(f(x)),
    Err(e) => Err(e)
  }
}
```

### Nested Patterns
```ailang
type Tree[a] = Leaf(a) | Node(Tree[a], a, Tree[a])

export func sumTree(t: Tree[int]) -> int {
  match t {
    Leaf(x) => x,
    Node(left, x, right) => sumTree(left) + x + sumTree(right)
  }
}
```

## Records

### Create and Access
```ailang
type Person = {name: string, age: int, email: string}

let alice: Person = {name: "Alice", age: 30, email: "alice@example.com"}

-- Access fields
let name = alice.name
let age = alice.age
```

### Record Updates
```ailang
export func birthday(p: Person) -> Person {
  {p | age: p.age + 1}
}

export func changeEmail(p: Person, newEmail: string) -> Person {
  {p | email: newEmail}
}
```

### Multiple Field Updates
```ailang
export func updatePerson(p: Person, newName: string, newAge: int) -> Person {
  {p | name: newName, age: newAge}
}
```

## Common Mistakes

### Wrong: Using Loops
```ailang
-- WRONG: No loops in AILANG!
for i in range(10) {
  println(i)
}
```

### Right: Use Recursion
```ailang
export func printRange(start: int, end: int) -> () ! {IO} {
  if start >= end then () else {
    println(show(start));
    printRange(start + 1, end)
  }
}
```

### Wrong: Mutable Variables
```ailang
-- WRONG: No mutation!
let mut x = 5;
x = x + 1;
```

### Right: Create New Values
```ailang
let x = 5;
let y = x + 1;  -- New binding, x is unchanged
```

### Wrong: Flags After Filename
```bash
# WRONG: Flags are ignored!
ailang run file.ail --caps IO
```

### Right: Flags Before Filename
```bash
# CORRECT
ailang run --caps IO --entry main file.ail
```

### Wrong: Missing Semicolons
```ailang
-- WRONG: Missing semicolon
export func compute() -> int {
  let x = 10   -- ERROR: missing semicolon
  let y = 20
  x + y
}
```

### Right: Semicolons Between Statements
```ailang
export func compute() -> int {
  let x = 10;  -- Semicolon after each statement
  let y = 20;
  x + y        -- No semicolon on final expression
}
```

## JSON Handling

### Decode JSON
```ailang
import std/json (decode)

type Config = {host: string, port: int}

export func parseConfig(jsonStr: string) -> Config {
  decode[Config](jsonStr)
}
```

### Encode JSON
```ailang
import std/json (encode)

export func toJson(config: Config) -> string {
  encode(config)
}
```

## HTTP / Network

### Simple GET Request
```ailang
module myproject/http_demo
import std/net (httpGet)
import std/io (println)

export func main() -> () ! {IO, Net} {
  let body = httpGet("https://httpbin.org/get");
  println(body)
}
```

Run with: `ailang run --caps IO,Net --entry main http_demo.ail`

### POST with JSON
```ailang
module myproject/post_demo
import std/net (httpPost)
import std/json (encode)
import std/io (println)

export func main() -> () ! {IO, Net} {
  let data = encode({message: "hello", count: 42});
  let response = httpPost("https://httpbin.org/post", data);
  println(response)
}
```

## FizzBuzz (Complete Example)

```ailang
module myproject/fizzbuzz
import std/io (println)

export func fb(n: int) -> () ! {IO} {
  let m3 = n % 3 == 0;
  let m5 = n % 5 == 0;
  if m3 && m5 then {
    println("FizzBuzz")
  } else {
    if m3 then {
      println("Fizz")
    } else {
      if m5 then {
        println("Buzz")
      } else {
        println(show(n))
      }
    }
  }
}

export func main() -> () ! {IO} {
  fb(1);   -- prints: 1
  fb(3);   -- prints: Fizz
  fb(5);   -- prints: Buzz
  fb(15)   -- prints: FizzBuzz
}
```

## AI Effect (Calling LLMs)

AILANG has a built-in AI effect for calling language models:

```ailang
module myproject/ai_demo
import std/ai (call)
import std/io (println)

export func main() -> () ! {IO, AI} {
  let response = call("What is 2+2? Reply with just the number.");
  println("AI says: " ++ response)
}
```

Run with: `ailang run --caps IO,AI --entry main ai_demo.ail`

**Note:** Requires environment variables for the AI provider (e.g., `ANTHROPIC_API_KEY`).

## Arrays (O(1) Access)

For performance-critical code or game grids, use Arrays instead of Lists:

```ailang
module myproject/array_demo
import std/array as A
import std/io (println)

export func main() -> () ! {IO} {
  let arr = #[1, 2, 3, 4, 5];           -- Array literal
  let val = A.get(arr, 2);               -- O(1) access, returns 3
  let safe = A.getOpt(arr, 10);          -- Safe access, returns None
  let updated = A.set(arr, 0, 100);      -- Returns new array
  println(show(val))
}
```
