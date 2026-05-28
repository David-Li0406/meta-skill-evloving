### Deriving traits

#### FromJson and ToJson

`derive(FromJson)` and `derive(ToJson)` automatically derives round-trippable method implementations
used for serializing the type to and from JSON.
The implementation is mainly for debugging and storing the types in a human-readable format.

```moonbit
struct JsonTest1 {
  x : Int
  y : Int
} derive(FromJson, ToJson, Eq, Show)

enum JsonTest2 {
  A(x~ : Int)
  B(x~ : Int, y~ : Int)
} derive(FromJson(style="legacy"), ToJson(style="legacy"), Eq, Show)

test "json basic" {
  let input = JsonTest1::{ x: 123, y: 456 }
  let expected : Json = { "x": 123, "y": 456 }
  assert_eq(input.to_json(), expected)
  assert_eq(@json.from_json(expected), input)
  let input = JsonTest2::A(x=123)
  let expected : Json = { "$tag": "A", "x": 123 }
  assert_eq(input.to_json(), expected)
  assert_eq(@json.from_json(expected), input)
}
```

Both derive directives accept a number of arguments to configure the exact behavior of serialization and deserialization.

###### WARNING
The actual behavior of JSON serialization arguments is unstable.

###### WARNING
JSON derivation arguments are only for coarse-grained control of the derived format.
If you need to precisely control how the types are laid out,
consider **directly implementing the two traits instead**.

We have recently deprecated a large number of advanced layout tweaking arguments.
For such usage and future usage of them, please manually implement the traits.
The arguments include: `repr`, `case_repr`, `default`, `rename_all`, etc.

```moonbit
struct JsonTest3 {
  x : Int
  y : Int
} derive (
  FromJson(fields(x(rename="renamedX"))),
  ToJson(fields(x(rename="renamedX"))),
  Eq,
  Show,
)

enum JsonTest4 {
  A(x~ : Int)
  B(x~ : Int, y~ : Int)
} derive(FromJson, ToJson, Eq, Show)

test "json args" {
  let input = JsonTest3::{ x: 123, y: 456 }
  let expected : Json = { "renamedX": 123, "y": 456 }
  assert_eq(input.to_json(), expected)
  assert_eq(@json.from_json(expected), input)
  let input = JsonTest4::A(x=123)
  let expected : Json = ["A", { "x": 123 }]
  assert_eq(input.to_json(), expected)
  assert_eq(@json.from_json(expected), input)
}
```

##### Enum styles

There are currently two styles of enum serialization: `legacy` and `flat`,
which the user must select one using the `style` argument.
Considering the following enum definition:

```moonbit
enum E {
  One
  Uniform(Int)
  Axes(x~: Int, y~: Int)
}
```

With `derive(ToJson(style="legacy"))`, the enum is formatted into:

```default
E::One              => { "$tag": "One" }
E::Uniform(2)       => { "$tag": "Uniform", "0": 2 }
E::Axes(x=-1, y=1)  => { "$tag": "Axes", "x": -1, "y": 1 }
```

With `derive(ToJson(style="flat"))`, the enum is formatted into:

```default
E::One              => "One"
E::Uniform(2)       => [ "Uniform", 2 ]
E::Axes(x=-1, y=1)  => [ "Axes", -1, 1 ]
```

###### Deriving `Option`

A notable exception is the builtin type `Option[T]`.
Ideally, it would be interpreted as `T | undefined`, but the issue is that it would be
impossible to distinguish `Some(None)` and `None` for `Option[Option[T]]`.

As a result, it interpreted as `T | undefined` iff it is a direct field
of a struct, and `[T] | null` otherwise:

```moonbit
struct A {
  x : Int?
  y : Int??
  z : (Int?, Int??)
} derive(ToJson)

test {
  @json.inspect({ x: None, y: None, z: (None, None) }, content={
    "z": [null, null],
  })
  @json.inspect({ x: Some(1), y: Some(None), z: (Some(1), Some(None)) }, content={
    "x": 1,
    "y": null,
    "z": [[1], [null]],
  })
  @json.inspect({ x: Some(1), y: Some(Some(1)), z: (Some(1), Some(Some(1))) }, content={
    "x": 1,
    "y": [1],
    "z": [[1], [[1]]],
  })
}
```

##### Container arguments

- `rename_fields` and `rename_cases` (enum only)
  batch renames fields (for enums and structs) and enum cases to the given format.
  Available parameters are:
  - `lowercase`
  - `UPPERCASE`
  - `camelCase`
  - `PascalCase`
  - `snake_case`
  - `SCREAMING_SNAKE_CASE`
  - `kebab-case`
  - `SCREAMING-KEBAB-CASE`

  Example: `rename_fields = "PascalCase"`
  for a field named `my_long_field_name`
  results in `MyLongFieldName`.

  Renaming assumes the name of fields in `snake_case`
  and the name of structs/enum cases in `PascalCase`.
- `cases(...)` (enum only) controls the layout of enum cases.

  #### WARNING
  This might be replaced with case attributes in the future.

  For example, for an enum
  ```moonbit
  enum E {
    A(...)
    B(...)
  }
  ```

  you are able to control each case using `cases(A(...), B(...))`.

  See [Case arguments]() below for details.
- `fields(...)` (struct only) controls the layout of struct fields.

  #### WARNING
  This might be replaced with field attributes in the future.

  For example, for a struct
  ```moonbit
  struct S {
    x: Int
    y: Int
  }
  ```

  you are able to control each field using `fields(x(...), y(...))`

  See [Field arguments]() below for details.

##### Case arguments

- `rename = "..."` renames this specific case,
  overriding existing container-wide rename directive if any.
- `fields(...)` controls the layout of the payload of this case.
  Note that renaming positional fields are not possible currently.

  See [Field arguments]() below for details.

##### Field arguments

- `rename = "..."` renames this specific field,
  overriding existing container-wide rename directives if any.

