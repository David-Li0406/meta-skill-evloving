### Method and Trait

#### Trait system

MoonBit provides a trait system for overloading/ad-hoc polymorphism. Traits declare a list of operations, which must be supplied when a type wants to implement the trait. Traits can be declared as follows:

```moonbit
pub(open) trait I {
  method_(Int) -> Int
  method_with_label(Int, label~ : Int) -> Int
  //! method_with_label(Int, label?: Int) -> Int
}
```

In the body of a trait definition, a special type `Self` is used to refer to the type that implements the trait.

##### Extending traits

A trait can depend on other traits, for example:

```moonbit
pub(open) trait Position {
  pos(Self) -> (Int, Int)
}

pub(open) trait Draw {
  draw(Self, Int, Int) -> Unit
}

pub(open) trait Object: Position + Draw {}
```

##### Implementing traits

To implement a trait, a type must explicitly provide all the methods required by the trait
using the syntax `impl Trait for Type with method_name(...) { ... }`. For example:

```moonbit
pub(open) trait MyShow {
  to_string(Self) -> String
}

struct MyType {}

pub impl MyShow for MyType with to_string(self) {
  ...
}

struct MyContainer[T] {}

// trait implementation with type parameters.
// `[X : Show]` means the type parameter `X` must implement `Show`,
// this will be covered later.
pub impl[X : MyShow] MyShow for MyContainer[X] with to_string(self) {
  ...
}
```

Type annotation can be omitted for trait `impl`: MoonBit will automatically infer the type based on the signature of `Trait::method` and the self type.

The author of the trait can also define **default implementations** for some methods in the trait, for example:

```moonbit
pub(open) trait J {
  f(Self) -> Unit
  f_twice(Self) -> Unit = _
}

impl J with f_twice(self) {
  self.f()
  self.f()
}
```

Note that in addition to the actual default implementation `impl J with f_twice`,
a mark `= _` is also required in the declaration of `f_twice` in `J`.
The `= _` mark is an indicator that this method has default implementation,
it enhances readability by allowing readers to know which methods have default implementation at first glance.

Implementers of trait `J` don't have to provide an implementation for `f_twice`: to implement `J`, only `f` is necessary.
They can always override the default implementation with an explicit `impl J for Type with f_twice`, if desired, though.

```moonbit
impl J for Int with f(self) {
  println(self)
}

impl J for String with f(self) {
  println(self)
}

impl J for String with f_twice(self) {
  println(self)
  println(self)
}

```

To implement the sub trait, one will have to implement the super traits,
and the methods defined in the sub trait. For example:

```moonbit
impl Position for Point with pos(self) {
  (self.x, self.y)
}

impl Draw for Point with draw(self, x, y) {
  ()
}

pub fn[O : Object] draw_object(obj : O) -> Unit {
  let (x, y) = obj.pos()
  obj.draw(x, y)
}

test {
  let p = Point::{ x: 1, y: 2 }
  draw_object(p)
}
```

For traits where all methods have default implementation,
it is still necessary to explicitly implement them,
in order to support features such as [abstract trait](packages.md#traits).
For this purpose, MoonBit provides the syntax `impl Trait for Type` (i.e. without the method part).
`impl Trait for Type` ensures that `Type` implements `Trait`,
MoonBit will automatically check if every method in `Trait` has corresponding implementation (custom or default).

In addition to handling traits where every methods has a default implementation,
the `impl Trait for Type` can also serve as documentation, or a TODO mark before filling actual implementation.

###### WARNING
Currently, an empty trait without any method is implemented automatically.

##### Using traits

When declaring a generic function, the type parameters can be annotated with the traits they should implement, allowing the definition of constrained generic functions. For example:

```moonbit
fn[X : Eq] contains(xs : Array[X], elem : X) -> Bool {
  for x in xs {
    if x == elem {
      return true
    }
  } else {
    false
  }
}
```

Without the `Eq` requirement, the expression `x == elem` in `contains` will result in a type error. Now, the function `contains` can be called with any type that implements `Eq`, for example:

```moonbit
struct Point {
  x : Int
  y : Int
}

impl Eq for Point with equal(p1, p2) {
  p1.x == p2.x && p1.y == p2.y
}

test {
  assert_false(contains([1, 2, 3], 4))
  assert_true(contains([1.5, 2.25, 3.375], 2.25))
  assert_false(contains([{ x: 2, y: 3 }], { x: 4, y: 9 }))
}
```

###### Invoke trait methods directly

Methods of a trait can be called directly via `Trait::method`. MoonBit will infer the type of `Self` and check if `Self` indeed implements `Trait`, for example:

```moonbit
test {
  assert_eq(Show::to_string(42), "42")
  assert_eq(Compare::compare(1.0, 2.5), -1)
}
```

Trait implementations can also be invoked via dot syntax, with the following restrictions:

1. if a regular method is present, the regular method is always favored when using dot syntax
2. only trait implementations that are located in the package of the self type can be invoked via dot syntax
   - if there are multiple trait methods (from different traits) with the same name available, an ambiguity error is reported

The above rules ensures that MoonBit's dot syntax enjoys good property while being flexible.
For example, adding a new dependency never break existing code with dot syntax due to ambiguity.
These rules also make name resolution of MoonBit extremely simple:
the method called via dot syntax must always come from current package or the package of the type!

Here's an example of calling trait `impl` with dot syntax:

```moonbit
struct MyCustomType {}

pub impl Show for MyCustomType with output(self, logger) {
  ...
}

fn f() -> Unit {
  let x = MyCustomType::{  }
  let _ = x.to_string()

}
```

##### Trait alias

MoonBit allows using traits with alternative names via trait alias.

###### WARNING
This feature may be removed in the future.

Trait alias can be declared as follows:

```moonbit
traitalias @builtin.Compare as CanCompare
```

