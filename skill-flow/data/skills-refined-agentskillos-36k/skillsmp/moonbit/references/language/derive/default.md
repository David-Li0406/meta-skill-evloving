### Deriving traits

#### Default

`derive(Default)` will generate a method that returns the default value of the type.

For structs, the default value is the struct with all fields set as their default value.

```moonbit
struct DeriveDefault {
  x : Int
  y : String?
} derive(Default, Eq, Show)

test "derive default struct" {
  let p = DeriveDefault::default()
  assert_eq(p, DeriveDefault::{ x: 0, y: None })
}
```

For enums, the default value is the only case that has no parameters.

```moonbit
enum DeriveDefaultEnum {
  Case1(Int)
  Case2(label~ : String)
  Case3
} derive(Default, Eq, Show)

test "derive default enum" {
  assert_eq(DeriveDefaultEnum::default(), DeriveDefaultEnum::Case3)
}
```

Enums that has no cases or more than one cases without parameters cannot derive `Default`.

<!-- MANUAL CHECK  should not compile -->
```moonbit
enum CannotDerive1 {
    Case1(String)
    Case2(Int)
} derive(Default) // cannot find a constant constructor as default

enum CannotDerive2 {
    Case1
    Case2
} derive(Default) // Case1 and Case2 are both candidates as default constructor
```

