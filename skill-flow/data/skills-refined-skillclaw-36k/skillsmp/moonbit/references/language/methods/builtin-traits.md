### Method and Trait

#### Builtin traits

MoonBit provides the following useful builtin traits:

<!-- MANUAL CHECK https://github.com/moonbitlang/core/blob/80cf250d22a5d5eff4a2a1b9a6720026f2fe8e38/builtin/traits.mbt -->
```moonbit
trait Eq {
  op_equal(Self, Self) -> Bool
}

trait Compare : Eq {
  // `0` for equal, `-1` for smaller, `1` for greater
  compare(Self, Self) -> Int
}

trait Hash {
  hash_combine(Self, Hasher) -> Unit // to be implemented
  hash(Self) -> Int // has default implementation
}

trait Show {
  output(Self, Logger) -> Unit // to be implemented
  to_string(Self) -> String // has default implementation
}

trait Default {
  default() -> Self
}
```

##### Deriving builtin traits

MoonBit can automatically derive implementations for some builtin traits:

```moonbit
struct T {
  a : Int
  b : Int
} derive(Eq, Compare, Show, Default)

test {
  let t1 = T::default()
  let t2 = T::{ a: 1, b: 1 }
  inspect(t1, content="{a: 0, b: 0}")
  inspect(t2, content="{a: 1, b: 1}")
  assert_not_eq(t1, t2)
  assert_true(t1 < t2)
}
```

See [Deriving](derive.md) for more information about deriving traits.

