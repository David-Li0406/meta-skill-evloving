# Comments & Miscellaneous Options

[← Prev: Languages](07-languages.md) | [Back to Index](index.md) | [Next: Advanced →](09-advanced.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Comment formatting and miscellaneous options.

## Comment Formatting

### ReflowComments

Comment reformatting style.

**Type:** `ReflowCommentsStyle` **Default:** `Always` **Version:** clang-format 3.8

**Values:**

- `Never` - Leave comments untouched
- `Always` - Apply indentation rules and reflow long comments into new lines, trying to obey the ColumnLimit

**Example:**

`Always`:

```cpp
// This is a very long comment that will be automatically
// reflowed to fit within the column limit when enabled
```

`Never`:

```cpp
// This is a very long comment that will not be reflowed even if it exceeds column limit
```

### CommentPragmas

A regular expression that describes comments with special meaning, which should not be split into lines or otherwise changed.

**Type:** `String` **Default:** `^\\s*IWYU pragma:` **Version:** clang-format 3.7

Comments matching this regex will not be reflowed.

**Example:**

```yaml
CommentPragmas: "^ FOOBAR pragma:"
```

```cpp
#include <vector> // FOOBAR pragma: keep
```

### FixNamespaceComments

Add/fix end-of-namespace comments for namespaces and fixes invalid existing ones. This doesn't affect short namespaces, which are controlled by `ShortNamespaceLines`.

**Type:** `Boolean` **Default:** `true` **Version:** clang-format 5

**Example:**

`true`:

```cpp
namespace longNamespace {
void foo();
void bar();
} // namespace longNamespace

namespace shortNamespace {
void baz();
}
```

`false`:

```cpp
namespace longNamespace {
void foo();
void bar();
}

namespace shortNamespace {
void baz();
}
```

### CompactNamespaces

If `true`, consecutive namespace declarations will be on the same line. If `false`, each namespace is declared on a new line.

**Type:** `Boolean` **Default:** `false` **Version:** clang-format 5

**Example:**

`true`:

```cpp
namespace Foo { namespace Bar {
}}
```

`false`:

```cpp
namespace Foo {
namespace Bar {
}
}
```

### ShortNamespaceLines

The maximal number of unwrapped lines that a short namespace spans. Defaults to 1.

**Type:** `Unsigned` **Default:** `1` **Version:** clang-format 13

This determines the maximum length of short namespaces by counting unwrapped lines (i.e. containing neither opening nor closing namespace brace) and makes `FixNamespaceComments` omit adding end comments for those.

**Example:**

`ShortNamespaceLines: 1`:

```cpp
namespace a {
  int foo;
}

namespace b {
  int foo;
  int bar;
} // namespace b
```

`ShortNamespaceLines: 0`:

```cpp
namespace a {
  int foo;
} // namespace a

namespace b {
  int foo;
  int bar;
} // namespace b
```

### WrapNamespaceBodyWithEmptyLines

Wrap namespace body with empty lines.

**Type:** `WrapNamespaceBodyWithEmptyLinesStyle` **Version:** clang-format 20

**Values:**

- `Never` - Remove all empty lines at the beginning and the end of namespace body
- `Always` - Always have at least one empty line at the beginning and the end of namespace body except that the number of empty lines between consecutive nested namespace definitions is not increased
- `Leave` - Keep existing newlines at the beginning and the end of namespace body. `MaxEmptyLinesToKeep` still applies

**Example:**

`Never`:

```cpp
namespace N1 {
namespace N2 {
function();
}
}
```

`Always`:

```cpp
namespace N1 {
namespace N2 {

function();

}
}
```

`Leave`:

```cpp
// Keeps existing empty lines as they are
```

## Macros

### AttributeMacros

A vector of strings that should be interpreted as attributes/qualifiers instead of identifiers. This can be useful for language extensions or static analyzer annotations.

**Type:** `List of Strings` **Version:** clang-format 12

**Example:**

```yaml
AttributeMacros: [__capability, __output, __unused]
```

```cpp
x = (char *__capability)&y;
int function(void) __unused;
void only_writes_to_buffer(char *__output buffer);
```

### ForEachMacros

A vector of macros that should be interpreted as foreach loops instead of as function calls.

**Type:** `List of Strings` **Version:** clang-format 3.7

These are expected to be macros of the form:

```cpp
FOREACH(<variable-declaration>, ...)
  <loop-body>
```

**Example:**

```yaml
ForEachMacros: [RANGES_FOR, FOREACH]
```

For example: BOOST_FOREACH

```cpp
FOREACH(item, list) {
  doSomething(item);
}
```

### IfMacros

A vector of macros that should be interpreted as conditionals instead of as function calls.

**Type:** `List of Strings` **Version:** clang-format 13

These are expected to be macros of the form:

```cpp
IF(...)
  <conditional-body>
else IF(...)
  <conditional-body>
```

**Example:**

```yaml
IfMacros: [IF]
```

For example: KJ_IF_MAYBE

### StatementAttributeLikeMacros

Macros which are ignored in front of a statement, as if they were an attribute. So that they are not parsed as identifier, for example for Qt's emit.

**Type:** `List of Strings` **Version:** clang-format 12

**Example:**

```yaml
AlignConsecutiveDeclarations: true
StatementAttributeLikeMacros: []
unsigned char data = 'x';
emit          signal(data); // This is parsed as variable declaration.

AlignConsecutiveDeclarations: true
StatementAttributeLikeMacros: [emit]
unsigned char data = 'x';
emit signal(data); // Now it's fine again.
```

### StatementMacros

A vector of macros that should be interpreted as complete statements.

**Type:** `List of Strings` **Version:** clang-format 8

Typical macros are expressions and require a semicolon to be added. Sometimes this is not the case, and this allows to make clang-format aware of such cases.

**Example:**

For example: Q_UNUSED

```yaml
StatementMacros:
  - Q_UNUSED
  - QT_REQUIRE_VERSION
```

### TypenameMacros

A vector of macros that should be interpreted as type declarations instead of as function calls.

**Type:** `List of Strings` **Version:** clang-format 9

These are expected to be macros of the form:

```cpp
STACK_OF(...)
```

**Example:**

For example: OpenSSL STACK_OF, BSD LIST_ENTRY

```yaml
TypenameMacros:
  - STACK_OF
  - LIST
```

### WhitespaceSensitiveMacros

A vector of macros which are whitespace-sensitive and should not be touched.

**Type:** `List of Strings` **Version:** clang-format 11

These are expected to be macros of the form:

```cpp
STRINGIZE(...)
```

**Example:**

For example: BOOST_PP_STRINGIZE

```yaml
WhitespaceSensitiveMacros:
  - STRINGIZE
  - PP_STRINGIZE
```

## Line Endings and Formatting Control

### LineEnding

Line ending style (`\n` or `\r\n`) to use.

**Type:** `LineEndingStyle` **Version:** clang-format 16

**Values:**

- `LF` - Use `\n` (Unix/Linux/Mac)
- `CRLF` - Use `\r\n` (Windows)
- `DeriveLF` - Use `\n` unless the input has more lines ending in `\r\n`
- `DeriveCRLF` - Use `\r\n` unless the input has more lines ending in `\n`

**Example:**

```yaml
LineEnding: LF        # Unix/Linux/Mac
LineEnding: CRLF      # Windows
LineEnding: DeriveLF  # Auto-detect, prefer LF
```

### DeriveLineEnding

**DEPRECATED** - This option is deprecated. See `DeriveLF` and `DeriveCRLF` of `LineEnding`.

Automatically detect line ending style.

**Type:** `Boolean` **Default:** `true` **Version:** clang-format 10

### UseCRLF

**DEPRECATED** - This option is deprecated. See `LF` and `CRLF` of `LineEnding`.

Use Windows-style line endings (CRLF).

**Type:** `Boolean` **Default:** `false` **Version:** clang-format 10

**Example:**

`true` - Use `\r\n` (Windows) `false` - Use `\n` (Unix/Linux/Mac)

### DisableFormat

Completely disable formatting.

**Type:** `Boolean`

When `true`, clang-format won't modify the file at all.

### InsertNewlineAtEOF

Insert newline at end of file.

**Type:** `Boolean`

Ensures file ends with a newline character.

### KeepFormFeed

Keep form feed characters.

**Type:** `Boolean`

Preserves ASCII form feed characters (\\f) in source.

## Trailing Commas

### InsertTrailingCommas

Automatically insert trailing commas.

**Type:** `TrailingCommaStyle` **Values:**

- `None` - Don't insert trailing commas
- `Wrapped` - Insert trailing commas in wrapped function calls

**Example:**

`Wrapped` (JavaScript):

```javascript
const x = {
  a: 1,
  b: 2, // trailing comma added
};
```

### EnumTrailingComma

Insert a comma (if missing) or remove the comma at the end of an `enum` enumerator list.

**Type:** `EnumTrailingCommaStyle` **Version:** clang-format 21

**Warning:** Setting this option to any value other than `Leave` could lead to incorrect code formatting due to clang-format's lack of complete semantic information. As such, extra care should be taken to review code changes made by this option.

**Values:**

- `Leave` - Don't insert or remove trailing commas
- `Insert` - Insert trailing commas

**Example:**

`Leave`:

```cpp
enum { a, b, c, };
enum Color { red, green, blue };
```

`Insert`:

```cpp
enum { a, b, c, };
enum Color { red, green, blue, };
```

## Integer Literals

### IntegerLiteralSeparator

Configure digit separators in integer literals.

**Type:** `IntegerLiteralSeparatorStyle` **Sub-options:**

- `Binary` - Separator for binary literals (0b)
- `BinaryMinDigits` - Minimum digits for binary
- `Decimal` - Separator for decimal
- `DecimalMinDigits` - Minimum digits for decimal
- `Hex` - Separator for hexadecimal
- `HexMinDigits` - Minimum digits for hex

**Example:**

```yaml
IntegerLiteralSeparator:
  Binary: 4
  Decimal: 3
  Hex: 2
```

```cpp
int a = 100'000'000;   // Decimal separator every 3 digits
int b = 0b1010'1010;   // Binary separator every 4 digits
int c = 0xDEAD'BEEF;   // Hex separator every 2 digits
```

## Empty Lines

### EmptyLineAfterAccessModifier

Add empty line after access modifiers.

**Type:** `EmptyLineAfterAccessModifierStyle` **Values:**

- `Never`, `Leave`, `Always`

**Example:**

`Always`:

```cpp
class Foo {
private:

  int x;
public:

  void bar();
};
```

### EmptyLineBeforeAccessModifier

Add empty line before access modifiers.

**Type:** `EmptyLineBeforeAccessModifierStyle` **Values:**

- `Never`, `Leave`, `Always`, `LogicalBlock`

**Example:**

`Always`:

```cpp
class Foo {
  int x;

private:
  int y;

public:
  void bar();
};
```

## Pointer and Reference Alignment

### PointerAlignment

Alignment of pointers and references.

**Type:** `PointerAlignmentStyle` **Values:**

- `Left` - Align to left
- `Right` - Align to right
- `Middle` - Align to middle

**Examples:**

`Left`:

```cpp
int* a;
int& b;
```

`Right`:

```cpp
int *a;
int &b;
```

`Middle`:

```cpp
int * a;
int & b;
```

### DerivePointerAlignment

Derive pointer alignment from existing code.

**Type:** `Boolean`

When `true`, overrides `PointerAlignment` based on majority style in file.

### ReferenceAlignment

Separate alignment for references (overrides PointerAlignment for references).

**Type:** `ReferenceAlignmentStyle` **Values:**

- `Pointer` - Same as pointers
- `Left`, `Right`, `Middle`

## Qualifier Alignment

### QualifierAlignment

Position of const/volatile qualifiers.

**Type:** `QualifierAlignmentStyle` **Values:**

- `Leave` - Don't change
- `Left` - const int
- `Right` - int const
- `Custom` - Use QualifierOrder

**Example:**

`Left`:

```cpp
const int a;
const int* b;
```

`Right`:

```cpp
int const a;
int const* b;
```

### QualifierOrder

Custom qualifier order when `QualifierAlignment: Custom`.

**Type:** `List of Strings`

**Example:**

```yaml
QualifierAlignment: Custom
QualifierOrder:
  - inline
  - static
  - constexpr
  - const
  - volatile
  - type
```

## Common Patterns

### Namespace and Comment Handling

```yaml
FixNamespaceComments: true
CompactNamespaces: false
ReflowComments: true
CommentPragmas: "^ IWYU pragma:|^ NOLINT"
```

### Line Endings

Modern (v16+):

```yaml
LineEnding: DeriveLF # Auto-detect, prefer Unix
InsertNewlineAtEOF: true
```

Legacy (deprecated):

```yaml
DeriveLineEnding: true # DEPRECATED - use LineEnding: DeriveLF
UseCRLF: false # DEPRECATED - use LineEnding: LF
InsertNewlineAtEOF: true
```

### Pointer Style (Left-Aligned)

```yaml
PointerAlignment: Left
ReferenceAlignment: Left
DerivePointerAlignment: false
```

### Pointer Style (Right-Aligned)

```yaml
PointerAlignment: Right
ReferenceAlignment: Right
DerivePointerAlignment: false
```

## Tips

1. **Comment Reflow**: Disable `ReflowComments` if you have carefully formatted comments
2. **Namespace Comments**: `FixNamespaceComments` helps navigate large codebases
3. **Namespace Empty Lines**: Use `WrapNamespaceBodyWithEmptyLines` (v20+) to control empty lines in namespace bodies
4. **Macro Lists**: Maintain accurate macro lists for correct formatting
5. **Pointer Alignment**: Choose one style and enforce it with `DerivePointerAlignment: false`
6. **Line Endings**: Use `LineEnding: DeriveLF` (v16+) for mixed-platform teams. Replaces deprecated `DeriveLineEnding` and `UseCRLF`
7. **Trailing Commas**: Useful in JavaScript/TypeScript for cleaner diffs
8. **Enum Trailing Commas**: Use `EnumTrailingComma` (v21+) carefully, as it may cause formatting issues
9. **Integer Separators**: Improves readability of large numeric literals

## See Also

- [Spacing](05-spacing.md) - Control whitespace
- [Languages](07-languages.md) - Language-specific options
- [Advanced](09-advanced.md) - Experimental features
- [Full Style Options Reference](complete/clang-format-style-options.md)

---

[← Prev: Languages](07-languages.md) | [Back to Index](index.md) | [Next: Advanced →](09-advanced.md)
