### Method and Trait

#### Trait objects

MoonBit supports runtime polymorphism via trait objects.
If `t` is of type `T`, which implements trait `I`,
one can pack the methods of `T` that implements `I`, together with `t`,
into a runtime object via `t as &I`.
When the expected type of an expression is known to be a trait object type, `as &I` can be omitted.
Trait object erases the concrete type of a value,
so objects created from different concrete types can be put in the same data structure and handled uniformly:

```moonbit
pub(open) trait Animal {
  speak(Self) -> String
}

struct Duck(String)

fn Duck::make(name : String) -> Duck {
  Duck(name)
}

impl Animal for Duck with speak(self) {
  "\{self.0}: quack!"
}

struct Fox(String)

fn Fox::make(name : String) -> Fox {
  Fox(name)
}

impl Animal for Fox with speak(_self) {
  "What does the fox say?"
}

test {
  let duck1 = Duck::make("duck1")
  let duck2 = Duck::make("duck2")
  let fox1 = Fox::make("fox1")
  let animals : Array[&Animal] = [duck1, duck2, fox1]
  inspect(
    animals.map(fn(animal) { animal.speak() }),
    content=(
      #|["duck1: quack!", "duck2: quack!", "What does the fox say?"]
    ),
  )
}
```

Not all traits can be used to create objects.
"object-safe" traits' methods must satisfy the following conditions:

- `Self` must be the first parameter of a method
- There must be only one occurrence of `Self` in the type of the method (i.e. the first parameter)

Users can define new methods for trait objects, just like defining new methods for structs and enums:

```moonbit
pub(open) trait Logger {
  write_string(Self, String) -> Unit
}

pub(open) trait CanLog {
  log(Self, &Logger) -> Unit
}

fn[Obj : CanLog] &Logger::write_object(self : &Logger, obj : Obj) -> Unit {
  obj.log(self)
}

// use the new method to simplify code
pub impl[A : CanLog, B : CanLog] CanLog for (A, B) with log(self, logger) {
  let (a, b) = self
  logger
  ..write_string("(")
  ..write_object(a)
  ..write_string(", ")
  ..write_object(b)
  ..write_string(")")
}
```

