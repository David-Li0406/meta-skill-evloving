### Fundamentals

#### Built-in Data Structures

##### Unit

`Unit` is a built-in type in MoonBit that represents the absence of a meaningful value. It has only one value, written as `()`. `Unit` is similar to `void` in languages like C/C++/Java, but unlike `void`, it is a real type and can be used anywhere a type is expected.

The `Unit` type is commonly used as the return type for functions that perform some action but do not produce a meaningful result:

```moonbit
fn print_hello() -> Unit {
  println("Hello, world!")
}
```

Unlike some other languages, MoonBit treats `Unit` as a first-class type, allowing it to be used in generics, stored in data structures, and passed as function arguments.

##### Boolean

MoonBit has a built-in boolean type, which has two values: `true` and `false`. The boolean type is used in conditional expressions and control structures.

```moonbit
let a = true
let b = false
let c = a && b
let d = a || b
let e = not(a)
```

##### Number

MoonBit have integer type and floating point type:

| type     | description                                       | example                    |
|----------|---------------------------------------------------|----------------------------|
| `Int16`  | 16-bit signed integer                             | `(42 : Int16)`             |
| `Int`    | 32-bit signed integer                             | `42`                       |
| `Int64`  | 64-bit signed integer                             | `1000L`                    |
| `UInt16` | 16-bit unsigned integer                           | `(14 : UInt16)`            |
| `UInt`   | 32-bit unsigned integer                           | `14U`                      |
| `UInt64` | 64-bit unsigned integer                           | `14UL`                     |
| `Double` | 64-bit floating point, defined by IEEE754         | `3.14`                     |
| `Float`  | 32-bit floating point                             | `(3.14 : Float)`           |
| `BigInt` | represents numeric values larger than other types | `10000000000000000000000N` |

MoonBit also supports numeric literals, including decimal, binary, octal, and hexadecimal numbers.

To improve readability, you may place underscores in the middle of numeric literals such as `1_000_000`. Note that underscores can be placed anywhere within a number, not just every three digits.

- Decimal numbers can have underscore between the numbers.

  By default, an int literal is signed 32-bit number. For unsigned numbers, a postfix `U` is needed; for 64-bit numbers, a postfix `L` is needed.
  ```moonbit
  let a = 1234
  let b : Int = 1_000_000 + a
  let unsigned_num       : UInt   = 4_294_967_295U
  let large_num          : Int64  = 9_223_372_036_854_775_807L
  let unsigned_large_num : UInt64 = 18_446_744_073_709_551_615UL
  ```
- A binary number has a leading zero followed by a letter "B", i.e. `0b`/`0B`.
  Note that the digits after `0b`/`0B` must be `0` or `1`.
  ```moonbit
  let bin = 0b110010
  let another_bin = 0B110010
  ```
- An octal number has a leading zero followed by a letter "O", i.e. `0o`/`0O`.
  Note that the digits after `0o`/`0O` must be in the range from `0` through `7`:
  ```moonbit
  let octal = 0o1234
  let another_octal = 0O1234
  ```
- A hexadecimal number has a leading zero followed by a letter "X", i.e. `0x`/`0X`.
  Note that the digits after the `0x`/`0X` must be in the range `0123456789ABCDEF`.
  ```moonbit
  let hex = 0XA
  let another_hex = 0xA_B_C
  ```
- A floating-point number literal is 64-bit floating-point number. To define a float, type annotation is needed.
  ```moonbit
  let double = 3.14 // Double
  let float : Float = 3.14
  let float2 = (3.14 : Float)
  ```

  A 64-bit floating-point number can also be defined using hexadecimal format:
  ```moonbit
  let hex_double = 0x1.2P3 // (1.0 + 2 / 16) * 2^(+3) == 9
  ```

When the expected type is known, MoonBit can automatically overload literal, and there is no need to specify the type of number via letter postfix:

```moonbit
let int : Int = 42
let uint : UInt = 42
let int64 : Int64 = 42
let double : Double = 42
let float : Float = 42
let bigint : BigInt = 42
```

###### SEE ALSO
[Overloaded Literals]()

##### String

`String` holds a sequence of UTF-16 code units. You can use double quotes to create a string, or use `#|` to write a multi-line string.

```moonbit
let a = "兔rabbit"
println(a[0].to_char())
println(a[1].to_char())
let b =
  #| Hello
  #| MoonBit\n
  #|
println(b)
```

```default
Some('兔')
Some('r')
 Hello
 MoonBit\n

```

In double quotes string, a backslash followed by certain special characters forms an escape sequence:

| escape sequences       | description                                          |
|------------------------|------------------------------------------------------|
| `\n`, `\r`, `\t`, `\b` | New line, Carriage return, Horizontal tab, Backspace |
| `\\`                   | Backslash                                            |
| `\u5154` , `\u{1F600}` | Unicode escape sequence                              |

MoonBit supports string interpolation. It enables you to substitute variables within interpolated strings. This feature simplifies the process of constructing dynamic strings by directly embedding variable values into the text. Variables used for string interpolation must implement the [`Show` trait](methods.md#builtin-traits).

```moonbit
let x = 42
println("The answer is \{x}")
```

###### NOTE
The interpolated expression can not contain newline, `{}` or `"`.

Multi-line strings can be defined using the leading `#|` or `$|`, where the former will keep the raw string and the former will perform the escape and interpolation:

```moonbit
let lang = "MoonBit"
let str =
  #| Hello
  #| ---
  $| \{lang}\n
  #| ---
println(str)
```

```default
 Hello
 ---
 MoonBit

 ---
```

The [VSCode extension](../toolchain/vscode/index.md#actions) can help you switch between a plain text and the MoonBit's multiline string.

When the expected type is `String` , the array literal syntax is overloaded to
construct the `String` by specifying each character in the string.

```moonbit
test {
  let c : Char = '中'
  let s : String = [c, '文']
  inspect(s, content="中文")
}
```

###### SEE ALSO
API: [https://mooncakes.io/docs/moonbitlang/core/string](https://mooncakes.io/docs/moonbitlang/core/string)

[Overloaded Literals]()

##### Char

`Char` represents a Unicode code point.

```moonbit
let a : Char = 'A'
let b = '兔'
let zero = '\u{30}'
let zero = '\u0030'
```

Char literals can be overloaded to type `Int` when the expected type is `Int`:

```moonbit
test {
  let s : String = "hello"
  // op_get returns type Int, and char literal can be used as Int
  let b = s[0] - 'a'
  inspect(b, content="7")
}
```

###### SEE ALSO
API: [https://mooncakes.io/docs/moonbitlang/core/char](https://mooncakes.io/docs/moonbitlang/core/char)

[Overloaded Literals]()

##### Byte(s)

A byte literal in MoonBit is either a single ASCII character or a single escape, have the form of `b'...'`. Byte literals are of type `Byte`. For example:

```moonbit
fn main {
  let b1 : Byte = b'a'
  println(b1.to_int())
  let b2 = b'\xff'
  println(b2.to_int())
}
```

```default
97
255
```

A `Bytes` is an immutable sequence of bytes. Similar to byte, bytes literals have the form of `b"..."`. For example:

```moonbit
test {
  let b1 : Bytes = b"abcd"
  let b2 = b"\x61\x62\x63\x64"
  assert_eq(b1, b2)
}
```

The byte literal and bytes literal also support escape sequences, but different from those in string literals. The following table lists the supported escape sequences for byte and bytes literals:

| escape sequences       | description                                          |
|------------------------|------------------------------------------------------|
| `\n`, `\r`, `\t`, `\b` | New line, Carriage return, Horizontal tab, Backspace |
| `\\`                   | Backslash                                            |
| `\x41`                 | Hexadecimal escape sequence                          |
| `\o102`                | Octal escape sequence                                |

###### NOTE
You can use `@buffer.T` to construct bytes by writing various types of data. For example:

```moonbit
test "buffer 1" {
  let buf : @buffer.Buffer = @buffer.new()
  buf.write_bytes(b"Hello")
  buf.write_byte(b'!')
  assert_eq(buf.contents(), b"Hello!")
}
```

When the expected type is `Bytes`, the `b` prefix can be omitted. Array literals can also be overloaded to construct a `Bytes` sequence by specifying each byte in the sequence.

```moonbit
test {
  let b : Byte = '\xFF'
  let bs : Bytes = [b, '\x01']
  inspect(
    bs,
    content=(
      #|b"\xff\x01"
    ),
  )
}
```

###### SEE ALSO
API for `Byte`: [https://mooncakes.io/docs/moonbitlang/core/byte](https://mooncakes.io/docs/moonbitlang/core/byte)<br />
\\\\
API for `Bytes`: [https://mooncakes.io/docs/moonbitlang/core/bytes](https://mooncakes.io/docs/moonbitlang/core/bytes)<br />
\\\\
API for `@buffer.T`: [https://mooncakes.io/docs/moonbitlang/core/buffer](https://mooncakes.io/docs/moonbitlang/core/buffer)

[Overloaded Literals]()

##### Tuple

A tuple is a collection of finite values constructed using round brackets `()` with the elements separated by commas `,`. The order of elements matters; for example, `(1,true)` and `(true,1)` have different types. Here's an example:

```moonbit
fn main {
  fn pack(
    a : Bool,
    b : Int,
    c : String,
    d : Double
  ) -> (Bool, Int, String, Double) {
    (a, b, c, d)
  }

  let quad = pack(false, 100, "text", 3.14)
  let (bool_val, int_val, str, float_val) = quad
  println("\{bool_val} \{int_val} \{str} \{float_val}")
}
```

```default
false 100 text 3.14
```

Tuples can be accessed via pattern matching or index:

```moonbit
test {
  let t = (1, 2)
  let (x1, y1) = t
  let x2 = t.0
  let y2 = t.1
  assert_eq(x1, x2)
  assert_eq(y1, y2)
}
```

##### Ref

A `Ref[T]` is a mutable reference containing a value `val` of type `T`.

It can be constructed using `{ val : x }`, and can be accessed using `ref.val`. See [struct]() for detailed explanation.

```moonbit
let a : Ref[Int] = { val: 100 }

test {
  a.val = 200
  assert_eq(a.val, 200)
  a.val += 1
  assert_eq(a.val, 201)
}
```

###### SEE ALSO
API: [https://mooncakes.io/docs/moonbitlang/core/ref](https://mooncakes.io/docs/moonbitlang/core/ref)

##### Option and Result

`Option` and `Result` are the most common types to represent a possible error or failure in MoonBit.

- `Option[T]` represents a possibly missing value of type `T`. It can be abbreviated as `T?`.
- `Result[T, E]` represents either a value of type `T` or an error of type `E`.

See [enum]() for detailed explanation.

```moonbit
test {
  let a : Int? = None
  let b : Option[Int] = Some(42)
  let c : Result[Int, String] = Ok(42)
  let d : Result[Int, String] = Err("error")
  match a {
    Some(_) => assert_true(false)
    None => assert_true(true)
  }
  match d {
    Ok(_) => assert_true(false)
    Err(_) => assert_true(true)
  }
}
```

###### SEE ALSO
API for `Option`: [https://mooncakes.io/docs/moonbitlang/core/option](https://mooncakes.io/docs/moonbitlang/core/option)<br />
\\\\
API for `Result`: [https://mooncakes.io/docs/moonbitlang/core/result](https://mooncakes.io/docs/moonbitlang/core/result)

##### Array

An array is a finite sequence of values constructed using square brackets `[]`, with elements separated by commas `,`. For example:

```moonbit
let numbers = [1, 2, 3, 4]
```

You can use `numbers[x]` to refer to the xth element. The index starts from zero.

```moonbit
test {
  let numbers = [1, 2, 3, 4]
  let a = numbers[2]
  numbers[3] = 5
  let b = a + numbers[3]
  assert_eq(b, 8)
}
```

There are `Array[T]` and `FixedArray[T]`:

`Array[T]` can grow in size, while `FixedArray[T]` has a fixed size, thus it needs to be created with initial value.

###### WARNING
A common pitfall is creating `FixedArray` with the same initial value:

```moonbit
test {
  let two_dimension_array = FixedArray::make(10, FixedArray::make(10, 0))
  two_dimension_array[0][5] = 10
  assert_eq(two_dimension_array[5][5], 10)
}
```

This is because all the cells reference to the same object (the `FixedArray[Int]` in this case). One should use `FixedArray::makei()` instead which creates an object for each index.

```moonbit
test {
  let two_dimension_array = FixedArray::makei(10, fn(_i) {
    FixedArray::make(10, 0)
  })
  two_dimension_array[0][5] = 10
  assert_eq(two_dimension_array[5][5], 0)
}
```

When the expected type is known, MoonBit can automatically overload array, otherwise
`Array[T]` is created:

```moonbit
let fixed_array_1 : FixedArray[Int] = [1, 2, 3]

let fixed_array_2 = ([1, 2, 3] : FixedArray[Int])

let array_3 = [1, 2, 3] // Array[Int]
```

###### SEE ALSO
API: [https://mooncakes.io/docs/moonbitlang/core/array](https://mooncakes.io/docs/moonbitlang/core/array)

[Overloaded Literals]()

###### ArrayView

Analogous to `slice` in other languages, the view is a reference to a
specific segment of collections. You can use `data[start:end]` to create a
view of array `data`, referencing elements from `start` to `end` (exclusive).
Both `start` and `end` indices can be omitted.

###### NOTE
`ArrayView` is an immutable data structure on its own, but the underlying `Array` or `FixedArray`
could be modified.

```moonbit
test {
  let xs = [0, 1, 2, 3, 4, 5]
  let s1 : ArrayView[Int] = xs[2:]
  inspect(s1, content="[2, 3, 4, 5]")
  inspect(xs[:4], content="[0, 1, 2, 3]")
  inspect(xs[2:5], content="[2, 3, 4]")
  inspect(xs[:], content="[0, 1, 2, 3, 4, 5]")
}
```

###### SEE ALSO
API: [https://mooncakes.io/docs/moonbitlang/core/array](https://mooncakes.io/docs/moonbitlang/core/array)

##### Map

MoonBit provides a hash map data structure that preserves insertion order called `Map` in its standard library.
`Map`s can be created via a convenient literal syntax:

```moonbit
let map : Map[String, Int] = { "x": 1, "y": 2, "z": 3 }
```

Currently keys in map literal syntax must be constant. `Map`s can also be destructed elegantly with pattern matching, see [Map Pattern]().

###### SEE ALSO
API: [https://mooncakes.io/docs/moonbitlang/core/builtin#Map](https://mooncakes.io/docs/moonbitlang/core/builtin#Map)

[Overloaded Literals]()

##### Json

MoonBit supports convenient json handling by overloading literals.
When the expected type of an expression is `Json`, number, string, array and map literals can be directly used to create json data:

```moonbit
let moon_pkg_json_example : Json = {
  "import": ["moonbitlang/core/builtin", "moonbitlang/core/coverage"],
  "test-import": ["moonbitlang/core/random"],
}
```

Json values can be pattern matched too, see [Json Pattern]().

###### SEE ALSO
API: [https://mooncakes.io/docs/moonbitlang/core/json](https://mooncakes.io/docs/moonbitlang/core/json)

[Overloaded Literals]()

