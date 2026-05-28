# Advanced & Experimental Options

[← Prev: Comments](08-comments.md) | [Back to Index](index.md) | [Quick Reference](quick-reference.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Experimental, advanced, and less commonly used options.

## Experimental Options

### ExperimentalAutoDetectBinPacking

Automatically detect bin packing from existing code.

**Type:** `Boolean` **Default:** `false` **Status:** Experimental

When enabled, clang-format attempts to detect whether arguments/parameters are bin-packed in the existing code and maintains that style.

**Warning:** This is experimental and may not work perfectly.

## C++ Specific

### Cpp11BracedListStyle

Use C++11 braced list style.

**Type:** `BracedListStyle` **Default:** `true`

**Example:**

`true`:

```cpp
vector<int> x{1, 2, 3, 4};
vector<T> x{{}, {}, {}, {}};
f(MyMap[{composite, key}]);
new int[3]{1, 2, 3};
```

`false`:

```cpp
vector<int> x{ 1, 2, 3, 4 };
vector<T> x{ {}, {}, {}, {} };
f(MyMap[{ composite, key }]);
new int[3]{ 1, 2, 3 };
```

### AlwaysBreakTemplateDeclarations

Control breaking after template declarations (deprecated).

**Type:** `BreakTemplateDeclarationsStyle` **Note:** Use `BreakTemplateDeclarations` instead

### AlwaysBreakAfterDefinitionReturnType

Control breaking after function definition return type (deprecated).

**Type:** `DefinitionReturnTypeBreakingStyle` **Note:** Use `BreakAfterReturnType` instead

### AllowAllConstructorInitializersOnNextLine

Allow constructor initializers on next line (deprecated).

**Type:** `Boolean` **Default:** `true` **Note:** Deprecated in favor of `PackConstructorInitializers`

### ConstructorInitializerAllOnOneLineOrOnePerLine

Format constructor initializers (deprecated).

**Type:** `Boolean` **Note:** Deprecated in favor of `PackConstructorInitializers`

### PackConstructorInitializers

How to pack constructor initializers.

**Type:** `PackConstructorInitializersStyle` **Values:**

- `Never` - Always put one per line
- `BinPack` - Bin-pack constructor initializers
- `CurrentLine` - Pack on current line if it fits
- `NextLine` - Pack on next line

## BinPacking

### BinPackLongBracedList

Bin-pack long braced lists.

**Type:** `Boolean`

When true, long braced lists will be bin-packed even if arguments aren't.

## Breaking Binary Operations

### BreakBinaryOperations

Control breaking of binary operations.

**Type:** `BreakBinaryOperationsStyle` **Values:**

- `RespectPrecedence` - Break respecting precedence
- `OnePerLine` - One operation per line
- `Never` - Don't break

**Example:**

`OnePerLine`:

```cpp
auto x =
    (aaaaa
     + bbbbb
     + ccccc);
```

## Template Behavior

### BreakBeforeTemplateCloser

Break before `>` in template declarations.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
template<typename T
        >
class Foo {};
```

`false`:

```cpp
template<typename T>
class Foo {};
```

### AlwaysBreakBeforeMultilineStrings

Always break before multiline string literals.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
aaaa =
    "bbbb"
    "cccc";
```

`false`:

```cpp
aaaa = "bbbb"
       "cccc";
```

## Special Case Handling

### AllowShortCaseExpressionOnASingleLine

Allow short case expressions on one line (for pattern matching languages).

**Type:** `Boolean`

### AllowShortCompoundRequirementOnASingleLine

Allow short compound requirements on one line (C++20 concepts).

**Type:** `Boolean`

### AllowShortNamespacesOnASingleLine

Allow short namespace declarations on one line.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
namespace a { class A; }
```

`false`:

```cpp
namespace a {
class A;
}
```

### AllowBreakBeforeNoexceptSpecifier

Control breaking before noexcept specifier.

**Type:** `BreakBeforeNoexceptSpecifierStyle` **Values:**

- `Never`, `OnlyWithParen`, `Always`

### AllowBreakBeforeQtProperty

Allow breaking before Qt property keywords.

**Type:** `Boolean` **Since:** v22

Allow breaking before `Q_Property` keywords `READ`, `WRITE`, etc. as if they were preceded by a comma. This allows them to be formatted according to `BinPackParameters`.

**Example:**

When enabled with appropriate bin-packing settings, Qt property declarations can have their keywords broken across lines more flexibly.

## Numeric Literals

### NumericLiteralCase

Capitalization style for numeric literals.

**Type:** `NumericLiteralCaseStyle` **Since:** v22

Separate control for each numeric literal component.

**Sub-options:**

- `ExponentLetter` - Format floating point exponent separator letter case
- `HexDigit` - Format hexadecimal digit case
- `Prefix` - Format integer prefix case
- `Suffix` - Format suffix case (excludes case-sensitive reserved suffixes like `min` in C++)

**Values for each component:**

- `Leave` - Leave this component as is
- `Upper` - Format with uppercase characters
- `Lower` - Format with lowercase characters

**Example:**

```yaml
NumericLiteralCase:
  ExponentLetter: Leave
  HexDigit: Lower
  Prefix: Upper
  Suffix: Lower
```

**Before:**

```cpp
float a = 6.02e23 + 1.0E10;
a = 0xaBcDeF;
a = 0xF0 | 0b1;
a = 1uLL;
```

**After (with config above):**

```cpp
float a = 6.02e23 + 1.0E10;  // ExponentLetter: Leave
a = 0xabcdef;                 // HexDigit: Lower
a = 0XF0 | 0B1;               // Prefix: Upper
a = 1ull;                     // Suffix: Lower
```

## Spacing in Empty Constructs

### SpaceInEmptyBraces

Specifies when to insert a space in empty braces.

**Type:** `SpaceInEmptyBracesStyle` **Since:** v22 **Note:** Replaces deprecated `SpaceInEmptyBlock` option

**Values:**

- `Always` - Always insert a space in empty braces
- `Block` - Only insert a space in empty blocks (functions, classes, lambdas)
- `Never` - Never insert a space in empty braces

**Example:**

`Always`:

```cpp
void f() { }
class Unit { };
auto a = [] { };
int x{ };
```

`Block`:

```cpp
void f() { }
class Unit { };
auto a = [] { };
int x{};  // No space in initializer braces
```

`Never`:

```cpp
void f() {}
class Unit {};
auto a = [] {};
int x{};
```

**Note:** This option does not apply to initializer braces if `Cpp11BracedListStyle` is not `Block`.

## Penalty System

These options control clang-format's internal penalty system for choosing formatting. Higher values make clang-format less likely to choose that formatting.

### PenaltyBreakAssignment

Penalty for breaking around assignment operator.

**Type:** `Unsigned`

### PenaltyBreakBeforeFirstCallParameter

Penalty for breaking before first call parameter.

**Type:** `Unsigned`

### PenaltyBreakBeforeMemberAccess

Penalty for breaking before a member access operator (`.` or `->`).

**Type:** `Unsigned` **Since:** v20

Controls how reluctant clang-format is to break before member access operators. Higher values make it less likely to break.

**Example:**

With lower penalty:

```cpp
object
    ->member
    ->anotherMember();
```

With higher penalty:

```cpp
object->member->anotherMember();
```

### PenaltyBreakComment

Penalty for breaking inside comment.

**Type:** `Unsigned`

### PenaltyBreakFirstLessLess

Penalty for breaking before first `<<`.

**Type:** `Unsigned`

### PenaltyBreakOpenParenthesis

Penalty for breaking after open parenthesis.

**Type:** `Unsigned`

### PenaltyBreakScopeResolution

Penalty for breaking after scope resolution operator (`::`).

**Type:** `Unsigned` **Since:** v18

Controls how reluctant clang-format is to break after `::` in qualified names. Higher values make it less likely to break.

**Example:**

With lower penalty:

```cpp
namespace::
    ClassName::
    memberFunction();
```

With higher penalty:

```cpp
namespace::ClassName::memberFunction();
```

### PenaltyBreakString

Penalty for breaking string literals.

**Type:** `Unsigned`

### PenaltyBreakTemplateDeclaration

Penalty for breaking after template declaration.

**Type:** `Unsigned`

### PenaltyExcessCharacter

Penalty for each character outside column limit.

**Type:** `Unsigned`

### PenaltyIndentedWhitespace

Penalty for indented whitespace.

**Type:** `Unsigned`

### PenaltyReturnTypeOnItsOwnLine

Penalty for putting return type on its own line.

**Type:** `Unsigned`

### ShortNamespaceLines

Maximum lines for considering namespace short.

**Type:** `Unsigned`

## Raw String Formatting

### RawStringFormats

Configure formatting of raw string literals.

**Type:** `List of RawStringFormat`

**Example:**

```yaml
RawStringFormats:
  - Language: TextProto
    Delimiters:
      - pb
      - proto
    EnclosingFunctions:
      - PARSE_TEXT_PROTO
    BasedOnStyle: Google
```

This allows formatting embedded protocol buffer text within raw strings.

## Namespace Handling

### NamespaceIndentation

Indent content in namespaces.

**Type:** `NamespaceIndentationKind` **Values:**

- `None` - Don't indent
- `Inner` - Indent inner namespaces only
- `All` - Indent all namespaces

**Example:**

`None`:

```cpp
namespace out {
namespace in {
class foo {};
}
}
```

`Inner`:

```cpp
namespace out {
namespace in {
  class foo {};
}
}
```

`All`:

```cpp
namespace out {
  namespace in {
    class foo {};
  }
}
```

### NamespaceMacros

Macros that behave like namespace declarations.

**Type:** `List of Strings`

## Fine-Tuning

### PPIndentWidth

Indentation width for preprocessor statements.

**Type:** `Integer` **Default:** Uses `IndentWidth`

Separate from `IndentPPDirectives`, this controls the width when indenting.

## When to Use Advanced Options

1. **Penalties**: Only adjust if default formatting doesn't match preferences
2. **Experimental Features**: Use with caution in production code
3. **Deprecated Options**: Migrate to newer equivalents
4. **Special Cases**: Handle edge cases in complex codebases

## Tips

1. **Start Simple**: Begin with predefined styles and common options
2. **Test Thoroughly**: Advanced options can have unexpected interactions
3. **Document Choices**: Explain why specific advanced options are used
4. **Monitor Changes**: Watch for behavioral changes in new clang-format versions
5. **Penalty Tuning**: Only adjust penalties as a last resort after trying other options

## Debugging Formatting

To understand why clang-format makes certain choices:

```bash
# See effective configuration
clang-format --dump-config file.cpp

# Verbose output (if available in your version)
clang-format --verbose file.cpp

# Check specific formatting
clang-format --style="{BasedOnStyle: llvm, ColumnLimit: 100}" --dry-run file.cpp
```

## See Also

- [Breaking & Line Wrapping](02-breaking.md) - Core breaking options
- [Comments & Misc](08-comments.md) - Common miscellaneous options
- [Quick Reference](quick-reference.md) - Complete working examples
- [Full Style Options Reference](complete/clang-format-style-options.md)

---

[← Prev: Comments](08-comments.md) | [Back to Index](index.md) | [Quick Reference](quick-reference.md)
