### Fundamentals

#### Custom Data Types

There are two ways to create new data types: `struct` and `enum`.

##### Struct

In MoonBit, structs are similar to tuples, but their fields are indexed by field names. A struct can be constructed using a struct literal, which is composed of a set of labeled values and delimited with curly brackets. The type of a struct literal can be automatically inferred if its fields exactly match the type definition. A field can be accessed using the dot syntax `s.f`. If a field is marked as mutable using the keyword `mut`, it can be assigned a new value.

```moonbit
struct User {
  id : Int
  name : String
  mut email : String
}
```

```moonbit
fn main {
  let u = User::{ id: 0, name: "John Doe", email: "john@doe.com" }
  u.email = "john@doe.name"
  //! u.id = 10
  println(u.id)
  println(u.name)
  println(u.email)
}
```

```default
0
John Doe
john@doe.name
```

###### Constructing Struct with Shorthand

If you already have some variable like `name` and `email`, it's redundant to repeat those names when constructing a struct. You can use shorthand instead, it behaves exactly the same:

```moonbit
let name = "john"
let email = "john@doe.com"
let u = User::{ id: 0, name, email }
```

If there's no other struct that has the same fields, it's redundant to add the struct's name when constructing it:

```moonbit
let u2 = { id: 0, name, email }
```

###### Struct Update Syntax

It's useful to create a new struct based on an existing one, but with some fields updated.

```moonbit
fn main {
  let user = { id: 0, name: "John Doe", email: "john@doe.com" }
  let updated_user = { ..user, email: "john@doe.name" }
  println(
    (
      $|{ id: \{user.id}, name: \{user.name}, email: \{user.email} }
      $|{ id: \{updated_user.id}, name: \{updated_user.name}, email: \{updated_user.email} }
    ),
  )
}
```

```default
{ id: 0, name: John Doe, email: john@doe.com }
{ id: 0, name: John Doe, email: john@doe.name }
```

##### Enum

Enum types are similar to algebraic data types in functional languages. Users familiar with C/C++ may prefer calling it tagged union.

An enum can have a set of cases (constructors). Constructor names must start with capitalized letter. You can use these names to construct corresponding cases of an enum, or checking which branch an enum value belongs to in pattern matching:

```moonbit
/// An enum type that represents the ordering relation between two values,
/// with three cases "Smaller", "Greater" and "Equal"
enum Relation {
  Smaller
  Greater
  Equal
}
```

```moonbit
/// compare the ordering relation between two integers
fn compare_int(x : Int, y : Int) -> Relation {
  if x < y {
    // when creating an enum, if the target type is known, 
    // you can write the constructor name directly
    Smaller
  } else if x > y {
    // but when the target type is not known,
    // you can always use `TypeName::Constructor` to create an enum unambiguously
    Relation::Greater
  } else {
    Equal
  }
}

/// output a value of type `Relation`
fn print_relation(r : Relation) -> Unit {
  // use pattern matching to decide which case `r` belongs to
  match r {
    // during pattern matching, if the type is known, 
    // writing the name of constructor is sufficient
    Smaller => println("smaller!")
    // but you can use the `TypeName::Constructor` syntax 
    // for pattern matching as well
    Relation::Greater => println("greater!")
    Equal => println("equal!")
  }
}
```

```moonbit
fn main {
  print_relation(compare_int(0, 1))
  print_relation(compare_int(1, 1))
  print_relation(compare_int(2, 1))
}
```

```default
smaller!
equal!
greater!
```

Enum cases can also carry payload data. Here's an example of defining an integer list type using enum:

```moonbit
enum Lst {
  Nil
  // constructor `Cons` carries additional payload: the first element of the list,
  // and the remaining parts of the list
  Cons(Int, Lst)
}
```

```moonbit
// In addition to binding payload to variables,
// you can also continue matching payload data inside constructors.
// Here's a function that decides if a list contains only one element
fn is_singleton(l : Lst) -> Bool {
  match l {
    // This branch only matches values of shape `Cons(_, Nil)`, 
    // i.e. lists of length 1
    Cons(_, Nil) => true
    // Use `_` to match everything else
    _ => false
  }
}

fn print_list(l : Lst) -> Unit {
  // when pattern-matching an enum with payload,
  // in additional to deciding which case a value belongs to
  // you can extract the payload data inside that case
  match l {
    Nil => println("nil")
    // Here `x` and `xs` are defining new variables 
    // instead of referring to existing variables,
    // if `l` is a `Cons`, then the payload of `Cons` 
    // (the first element and the rest of the list)
    // will be bind to `x` and `xs
    Cons(x, xs) => {
      println("\{x},")
      print_list(xs)
    }
  }
}
```

```moonbit
fn main {
  // when creating values using `Cons`, the payload of by `Cons` must be provided
  let l : Lst = Cons(1, Cons(2, Nil))
  println(is_singleton(l))
  print_list(l)
}
```

```default
false
1,
2,
nil
```

###### Constructor with labelled arguments

Enum constructors can have labelled argument:

```moonbit
enum E {
  // `x` and `y` are labelled argument
  C(x~ : Int, y~ : Int)
}
```

```moonbit
// pattern matching constructor with labelled arguments
fn f(e : E) -> Unit {
  match e {
    // `label=pattern`
    C(x=0, y=0) => println("0!")
    // `x~` is an abbreviation for `x=x`
    // Unmatched labelled arguments can be omitted via `..`
    C(x~, ..) => println(x)
  }
}
```

```moonbit
fn main {
  f(C(x=0, y=0))
  let x = 0
  f(C(x~, y=1)) // <=> C(x=x, y=1)
}
```

```default
0!
0
```

It is also possible to access labelled arguments of constructors like accessing struct fields in pattern matching:

```moonbit
enum Object {
  Point(x~ : Double, y~ : Double)
  Circle(x~ : Double, y~ : Double, radius~ : Double)
}

suberror NotImplementedError derive(Show)

fn Object::distance_with(
  self : Object,
  other : Object,
) -> Double raise NotImplementedError {
  match (self, other) {
    // For variables defined via `Point(..) as p`,
    // the compiler knows it must be of constructor `Point`,
    // so you can access fields of `Point` directly via `p.x`, `p.y` etc.
    (Point(_) as p1, Point(_) as p2) => {
      let dx = p2.x - p1.x
      let dy = p2.y - p1.y
      (dx * dx + dy * dy).sqrt()
    }
    (Point(_), Circle(_)) | (Circle(_), Point(_)) | (Circle(_), Circle(_)) =>
      raise NotImplementedError
  }
}
```

```moonbit
fn main {
  let p1 : Object = Point(x=0, y=0)
  let p2 : Object = Point(x=3, y=4)
  let c1 : Object = Circle(x=0, y=0, radius=2)
  try {
    println(p1.distance_with(p2))
    println(p1.distance_with(c1))
  } catch {
    e => println(e)
  }
}
```

```default
5
NotImplementedError
```

###### Constructor with mutable fields

It is also possible to define mutable fields for constructor. This is especially useful for defining imperative data structures:

```moonbit
// A set implemented using mutable binary search tree.
struct Set[X] {
  mut root : Tree[X]
}

fn[X : Compare] Set::insert(self : Set[X], x : X) -> Unit {
  self.root = self.root.insert(x, parent=Nil)
}

// A mutable binary search tree with parent pointer
enum Tree[X] {
  Nil
  // only labelled arguments can be mutable
  Node(
    mut value~ : X,
    mut left~ : Tree[X],
    mut right~ : Tree[X],
    mut parent~ : Tree[X]
  )
}

// In-place insert a new element to a binary search tree.
// Return the new tree root
fn[X : Compare] Tree::insert(
  self : Tree[X],
  x : X,
  parent~ : Tree[X],
) -> Tree[X] {
  match self {
    Nil => Node(value=x, left=Nil, right=Nil, parent~)
    Node(_) as node => {
      let order = x.compare(node.value)
      if order == 0 {
        // mutate the field of a constructor
        node.value = x
      } else if order < 0 {
        // cycle between `node` and `node.left` created here
        node.left = node.left.insert(x, parent=node)
      } else {
        node.right = node.right.insert(x, parent=node)
      }
      // The tree is non-empty, so the new root is just the original tree
      node
    }
  }
}
```

##### Tuple Struct

MoonBit supports a special kind of struct called tuple struct:

```moonbit
struct UserId(Int)

struct UserInfo(UserId, String)
```

Tuple structs are similar to enum with only one constructor (with the same name as the tuple struct itself). So, you can use the constructor to create values, or use pattern matching to extract the underlying representation:

```moonbit
fn main {
  let id : UserId = UserId(1)
  let name : UserInfo = UserInfo(id, "John Doe")
  let UserId(uid) = id // uid : Int
  let UserInfo(_, uname) = name // uname: String
  println(uid)
  println(uname)
}
```

```default
1
John Doe
```

Besides pattern matching, you can also use index to access the elements similar to tuple:

```moonbit
fn main {
  let id : UserId = UserId(1)
  let info : UserInfo = UserInfo(id, "John Doe")
  let uid : Int = id.0
  let uname : String = info.1
  println(uid)
  println(uname)
}
```

```default
1
John Doe
```

##### Type alias

MoonBit supports type alias via the syntax `type NewType = OldType`:

###### WARNING
The old syntax `typealias OldType as NewType` may be removed in the future.

```moonbit
pub typealias Int as Index
pub type MyIndex = Int
pub type MyMap = Map[Int, String]
```

Unlike all other kinds of type declaration above, type alias does not define a new type,
it is merely a type macro that behaves exactly the same as its definition.
So for example one cannot define new methods or implement traits for a type alias.

##### Local types

MoonBit supports declaring structs/enums at the top of a toplevel
function, which are only visible within the current toplevel function. These
local types can use the generic parameters of the toplevel function but cannot
introduce additional generic parameters themselves. Local types can derive
methods using derive, but no additional methods can be defined manually. For
example:

```moonbit
fn[T : Show] toplevel(x : T) -> Unit {
  enum LocalEnum {
    A(T)
    B(Int)
  } derive(Show)
  struct LocalStruct {
    a : (String, T)
  } derive(Show)
  struct LocalStructTuple(T) derive(Show)
  ...
}
```

Currently, local types do not support being declared as error types.

