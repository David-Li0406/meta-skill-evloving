### Method and Trait

#### Operator Overloading

MoonBit supports overloading infix operators of builtin operators via several builtin traits. For example:

```moonbit
struct T {
  x : Int
}

impl Add for T with add(self : T, other : T) -> T {
  { x: self.x + other.x }
}

test {
  let a = { x: 0 }
  let b = { x: 2 }
  assert_eq((a + b).x, 2)
}
```

Other operators are overloaded via methods with annotations, for example `_[_]` and `_[_]=_`:

```moonbit
struct Coord {
  mut x : Int
  mut y : Int
} derive(Show)

###alias("_[_]")
fn Coord::get(coord : Self, key : String) -> Int {
  match key {
    "x" => coord.x
    "y" => coord.y
  }
}

###alias("_[_]=_")
fn Coord::set(coord : Self, key : String, val : Int) -> Unit {
  match key {
    "x" => coord.x = val
    "y" => coord.y = val
  }
}
```

```moonbit
fn main {
  let c = { x: 1, y: 2 }
  println(c)
  println(c["y"])
  c["x"] = 23
  println(c)
  println(c["x"])
}
```

```default
{x: 1, y: 2}
2
{x: 23, y: 2}
23
```

Currently, the following operators can be overloaded:

| Operator Name         | overloading mechanism   |
|-----------------------|-------------------------|
| `+`                   | trait `Add`             |
| `-`                   | trait `Sub`             |
| `*`                   | trait `Mul`             |
| `/`                   | trait `Div`             |
| `%`                   | trait `Mod`             |
| `==`                  | trait `Eq`              |
| `<<`                  | trait `Shl`             |
| `>>`                  | trait `Shr`             |
| `-` (unary)           | trait `Neg`             |
| `_[_]` (get item)     | method + alias `_[_]`   |
| `_[_] = _` (set item) | method + alias `_[_]=_` |
| `_[_:_]` (view)       | method + alias `_[_:_]` |
| `&`                   | trait `BitAnd`          |
| `|`                   | trait `BitOr`           |
| `^`                   | trait `BitXOr`          |

When overloading `_[_]`/`_[_] = _`/`_[_:_]`, the method must have a correcnt signature:

- `_[_]` should have signature `(Self, Index) -> Result`, used as `let result = self[index]`
- `_[_]=_` should have signature `(Self, Index, Value) -> Unit`, used as `self[index] = value`
- `_[_:_]` should have signature `(Self, start? : Index, end? : Index) -> Result`, used as `let result = self[start:end]`

By implementing `_[_:_]` method, you can create a view for a user-defined type. Here is an example:

```moonbit
struct DataView(String)

struct Data {}

###alias("_[_:_]")
fn Data::as_view(_self : Data, start? : Int = 0, end? : Int) -> DataView {
  "[\{start}, \{end.unwrap_or(100)})"
}

test {
  let data = Data::{  }
  inspect(data[:].0, content="[0, 100)")
  inspect(data[2:].0, content="[2, 100)")
  inspect(data[:5].0, content="[0, 5)")
  inspect(data[2:5].0, content="[2, 5)")
}
```

