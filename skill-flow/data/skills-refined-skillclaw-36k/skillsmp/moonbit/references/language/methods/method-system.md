### Method and Trait

#### Method system

MoonBit supports methods in a different way from traditional object-oriented languages. A method in MoonBit is just a toplevel function associated with a type constructor.
To define a method, prepend `SelfTypeName::` in front of the function name, such as `fn SelfTypeName::method_name(...)`, and the method belongs to `SelfTypeName`.
Within the signature of the method declaration, you can use `Self` to refer to `SelfTypeName`.

###### WARNING
Currently, there is a shorthand syntax for defining methods.
When the name of the first parameter is `self`, a function declaration will be considered a method for the type of `self`.
This syntax may be deprecated in the future, and we do not recommend using it in new code.

```moonbit
fn method_name(self : SelfType) -> Unit { ... }
```

```moonbit
enum List[X] {
  Nil
  Cons(X, List[X])
}

///|
fn[X] List::length(xs : List[X]) -> Int {
  ...
}
```

To call a method, you can either invoke using qualified syntax `T::method_name(..)`, or using dot syntax where the first argument is the type of `T`:

```moonbit
let l : List[Int] = Nil
println(l.length())
println(List::length(l))
```

When the first parameter of a method is also the type it belongs to, methods can be called using dot syntax `x.method(...)`. MoonBit automatically finds the correct method based on the type of `x`, there is no need to write the type name and even the package name of the method:

```moonbit
pub(all) enum List[X] {
  Nil
  Cons(X, List[X])
}

pub fn[X] List::concat(list : List[List[X]]) -> List[X] {
  ...
}
```

```moonbit
// assume `xs` is a list of lists, all the following two lines are equivalent
let _ = xs.concat()
let _ = @list.List::concat(xs)
```

Unlike regular functions, methods defined using the `TypeName::method_name` syntax support overloading:
different types can define methods of the same name, because each method lives in a different name space:

```moonbit
struct T1 {
  x1 : Int
}

fn T1::default() -> T1 {
  { x1: 0 }
}

struct T2 {
  x2 : Int
}

fn T2::default() -> T2 {
  { x2: 0 }
}

test {
  let t1 = T1::default()
  let t2 = T2::default()

}
```

##### Local method

To ensure single source of truth in method resolution and avoid ambiguity,
[methods can only be defined in the same package as its type](packages.md#trait-implementations).
However, there is one exception to this rule: MoonBit allows defining *private* methods for foreign types locally.
These local methods can override methods from the type's own package (MoonBit will emit a warning in this case),
and provide extension/complementary to upstream API:

```moonbit
fn Int::my_int_method(self : Int) -> Int {
  self * self + self
}

test {
  assert_eq((6).my_int_method(), 42)
}
```

##### Alias methods as functions

MoonBit allows calling methods with alternative names via alias.

The method alias will create a method with the corresponding name.
You can also choose to create a function with the corresponding name.
The visibility can also be controlled.

```moonbit
###alias(m)
###alias(n, visibility="priv")
###as_free_fn(m)
###as_free_fn(n, visibility="pub")
fn List::f() -> Bool {
  true
}
test {
  assert_eq(List::f(), List::m())
  assert_eq(List::m(), m())
}
```

