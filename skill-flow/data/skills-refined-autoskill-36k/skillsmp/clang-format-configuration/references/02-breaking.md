# Breaking & Line Wrapping Options

[← Prev: Alignment](01-alignment.md) | [Back to Index](index.md) | [Next: Braces →](03-braces.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Control where lines break and how code wraps when it exceeds column limits.

## Overview

Breaking options determine where and how clang-format inserts line breaks. These options work together with `ColumnLimit` to control code width and readability.

## Column Limit

### ColumnLimit

Maximum line length before wrapping.

**Type:** `Unsigned` **Default:** `80`

```yaml
ColumnLimit: 100  # 100 characters per line
ColumnLimit: 0    # No limit
```

**Example:**

```cpp
// ColumnLimit: 80
void function(int param1,
              int param2,
              int param3);

// ColumnLimit: 120
void function(int param1, int param2, int param3);
```

## Allow Short Constructs on Single Line

These options control when short code blocks can remain on one line.

### AllowShortBlocksOnASingleLine

**Type:** `ShortBlockStyle` **Values:**

- `Never` - Never merge blocks into single line
- `Empty` - Only merge empty blocks
- `Always` - Always merge short blocks

**Examples:**

`Never`:

```cpp
while (true) {
}
while (true) {
  continue;
}
```

`Empty`:

```cpp
while (true) {}
while (true) {
  continue;
}
```

`Always`:

```cpp
while (true) {}
while (true) { continue; }
```

### AllowShortCaseLabelsOnASingleLine

Keep short case labels on a single line.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
switch (a) {
case 1: x = 1; break;
case 2: return;
}
```

`false`:

```cpp
switch (a) {
case 1:
  x = 1;
  break;
case 2:
  return;
}
```

### AllowShortEnumsOnASingleLine

Keep short enums on a single line.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
enum { A, B } myEnum;

enum class Color { Red, Green, Blue };
```

`false`:

```cpp
enum {
  A,
  B
} myEnum;

enum class Color {
  Red,
  Green,
  Blue
};
```

### AllowShortFunctionsOnASingleLine

**Type:** `ShortFunctionStyle` **Values:**

- `None` - Never merge functions
- `InlineOnly` - Only merge functions defined inside a class
- `Empty` - Only merge empty functions
- `Inline` - Merge inline and functions defined in class
- `All` - Merge all functions

**Examples:**

`InlineOnly`:

```cpp
class Foo {
  void f() { foo(); }
};
void f() {
  foo();
}
```

`Empty`:

```cpp
void f() {}
void f2() {
  bar();
}
```

`All`:

```cpp
class Foo {
  void f() { foo(); }
};
void f() { bar(); }
```

### AllowShortIfStatementsOnASingleLine

**Type:** `ShortIfStyle` **Values:**

- `Never` - Never put short ifs on one line
- `WithoutElse` - Only if without else
- `OnlyFirstIf` - Only first if without else
- `AllIfsAndElse` - All short if/else on one line

**Examples:**

`Never`:

```cpp
if (a)
  return;

if (b)
  return;
else
  return;
```

`WithoutElse`:

```cpp
if (a) return;

if (b)
  return;
else
  return;
```

`AllIfsAndElse`:

```cpp
if (a) return;

if (b) return;
else return;
```

### AllowShortLambdasOnASingleLine

**Type:** `ShortLambdaStyle` **Values:**

- `None` - Never merge lambdas
- `Empty` - Only empty lambdas
- `Inline` - Lambdas inside function calls
- `All` - All lambdas

**Examples:**

`None`:

```cpp
auto lambda = []() {
  return 1;
};
```

`Empty`:

```cpp
auto lambda = []() {};
auto lambda2 = []() {
  return 1;
};
```

`All`:

```cpp
auto lambda = []() { return 1; };
```

### AllowShortLoopsOnASingleLine

Keep short loops on a single line.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
while (true) continue;
for (int i = 0; i < 10; ++i) {}
```

`false`:

```cpp
while (true)
  continue;
for (int i = 0; i < 10; ++i) {
}
```

## Breaking Before/After Elements

### BreakBeforeBinaryOperators

Where to wrap binary operators.

**Type:** `BinaryOperatorStyle` **Values:**

- `None` - Break after operators
- `NonAssignment` - Break before non-assignment operators
- `All` - Break before all binary operators

**Examples:**

`None`:

```cpp
LooooooooooongType loooooooooooooooooooooongVariable =
    someLooooooooooooooooongFunction();

bool value = aaaaaaaaaaaaaaaaaaaaa +
                 aaaaaaaaaaaaaaaaaaa ==
             aaaaaaaaaaaaaaaaaaaaaaa &&
```

`NonAssignment`:

```cpp
LooooooooooongType loooooooooooooooooooooongVariable =
    someLooooooooooooooooongFunction();

bool value = aaaaaaaaaaaaaaaaaaaaa + aaaaaaaaaaaaaaaaaaa
                 == aaaaaaaaaaaaaaaaaaaaaaa
             && aaaaaaaaaaaaaaaaaaaaaaaa;
```

`All`:

```cpp
LooooooooooongType loooooooooooooooooooooongVariable
    = someLooooooooooooooooongFunction();

bool value = aaaaaaaaaaaaaaaaaaaaa + aaaaaaaaaaaaaaaaaaa
                 == aaaaaaaaaaaaaaaaaaaaaaa
             && aaaaaaaaaaaaaaaaaaaaaaaa;
```

### BreakBeforeTernaryOperators

Break before ternary operators.

**Type:** `Boolean`

**Examples:**

`true`:

```cpp
veryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryLongDescription
    ? firstValue
    : secondValue;
```

`false`:

```cpp
veryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryLongDescription ?
    firstValue :
    secondValue;
```

### BreakBinaryOperations

**Type:** `BreakBinaryOperationsStyle` **Since:** clang-format 20

The break binary operations style to use.

**Values:**

- `Never` - Don't break binary operations
- `OnePerLine` - Binary operations will either be all on same line, or each operation will have one line each
- `RespectPrecedence` - Binary operations of a particular precedence that exceed the column limit will have one line each

**Examples:**

`Never`:

```cpp
aaa + bbbb * ccccc - ddddd +
eeeeeeeeeeeeeeee;
```

`OnePerLine`:

```cpp
aaa +
bbbb *
ccccc -
ddddd +
eeeeeeeeeeeeeeee;
```

`RespectPrecedence`:

```cpp
aaa +
bbbb * ccccc -
ddddd +
eeeeeeeeeeeeeeee;
```

### BreakConstructorInitializers

Break constructor initializers.

**Type:** `BreakConstructorInitializersStyle` **Values:**

- `BeforeColon` - Break before `:` and `,`
- `BeforeComma` - Break before `,`
- `AfterColon` - Break after `:`

**Examples:**

`BeforeColon`:

```cpp
Constructor()
    : initializer1()
    , initializer2()
```

`BeforeComma`:

```cpp
Constructor()
    : initializer1(),
      initializer2()
```

`AfterColon`:

```cpp
Constructor() :
    initializer1(),
    initializer2()
```

### BreakInheritanceList

Break inheritance list.

**Type:** `BreakInheritanceListStyle` **Values:**

- `BeforeColon` - Break before `:`
- `BeforeComma` - Break before `,`
- `AfterColon` - Break after `:`
- `AfterComma` - Break after `,`

**Examples:**

`BeforeColon`:

```cpp
class Foo
    : Base1
    , Base2
{};
```

`AfterColon`:

```cpp
class Foo :
    Base1,
    Base2
{};
```

### BreakStringLiterals

Allow breaking string literals.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
const char* x = "veryVeryVeryVeryVeryVe"
                "ryVeryVeryVeryVeryVery"
                "VeryLongString";
```

`false` (exceeds column limit):

```cpp
const char* x = "veryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryVeryLongString";
```

### BreakAdjacentStringLiterals

Break adjacent string literals.

**Type:** `Boolean` **Default:** `true`

**Example:**

`true`:

```cpp
return "Code" "Llama";
```

`false`:

```cpp
return "CodeLlama";
```

## Breaking Templates and Return Types

### BreakAfterReturnType

Control breaking after return types.

**Type:** `ReturnTypeBreakingStyle` **Values:**

- `None` - Automatic
- `All` - Always break after return type
- `TopLevel` - Break after top-level function return types
- `AllDefinitions` - Break after all definition return types
- `TopLevelDefinitions` - Break after top-level definition return types

**Examples:**

`None`:

```cpp
class A {
  int f() { return 0; }
};
int f();
int f() { return 1; }
```

`All`:

```cpp
class A {
  int
  f() {
    return 0;
  }
};
int
f();
int
f() {
  return 1;
}
```

`TopLevel`:

```cpp
class A {
  int f() { return 0; }
};
int
f();
int
f() {
  return 1;
}
```

### BreakTemplateDeclarations

Breaking around template declarations.

**Type:** `BreakTemplateDeclarationsStyle` **Values:**

- `No` - Don't force breaks
- `MultiLine` - Break multi-line template declarations
- `Yes` - Always break after template declaration

**Examples:**

`No`:

```cpp
template <typename T> T foo() {
}
template <typename T> T foo(int aaaaaaaaaaaaaaaaaaaaa,
                              int bbbbbbbbbbbbbbbbbbbbb) {
}
```

`MultiLine`:

```cpp
template <typename T> T foo() {
}
template <typename T>
T foo(int aaaaaaaaaaaaaaaaaaaaa,
      int bbbbbbbbbbbbbbbbbbbbb) {
}
```

`Yes`:

```cpp
template <typename T>
T foo() {
}
template <typename T>
T foo(int aaaaaaaaaaaaaaaaaaaaa,
      int bbbbbbbbbbbbbbbbbbbbb) {
}
```

### BreakAfterAttributes

Break after attributes.

**Type:** `AttributeBreakingStyle` **Values:**

- `Always` - Always break after attributes
- `Leave` - Leave as is
- `Never` - Never break after attributes

**Example:**

`Always`:

```cpp
[[nodiscard]]
int f();

[[gnu::const]] [[nodiscard]]
int g();
```

`Never`:

```cpp
[[nodiscard]] int f();

[[gnu::const]] [[nodiscard]] int g();
```

## Special Breaking Options

### BreakBeforeConceptDeclarations

Break before C++20 concept declarations.

**Type:** `BreakBeforeConceptDeclarationsStyle` **Values:**

- `Never` - Keep on same line
- `Allowed` - Break if needed
- `Always` - Always break

**Example:**

`Always`:

```cpp
template <typename T>
concept ...
```

`Never`:

```cpp
template <typename T> concept ...
```

### BreakBeforeTemplateCloser

**Type:** `Boolean` **Since:** clang-format 21

If `true`, break before a template closing bracket (`>`) when there is a line break after the matching opening bracket (`<`).

**Examples:**

`true`:

```cpp
template <typename Foo, typename Bar>

template <typename Foo,
          typename Bar>

template <
    typename Foo,
    typename Bar
>
```

`false`:

```cpp
template <typename Foo, typename Bar>

template <typename Foo,
          typename Bar>

template <
    typename Foo,
    typename Bar>
```

### BreakBeforeInlineASMColon

Break before inline ASM colon.

**Type:** `BreakBeforeInlineASMColonStyle` **Values:**

- `Never`, `OnlyMultiline`, `Always`

### BreakFunctionDefinitionParameters

Break function definition parameters.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
void functionDeclaration(int A, int B);

void functionDefinition(
    int A,
    int B
) {
  // function body
}
```

## Parameter and Argument Control

### AllowAllArgumentsOnNextLine

Allow putting all arguments on the next line.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
callFunction(
    a, b, c, d);
```

`false` (will try to fit some on same line):

```cpp
callFunction(a,
             b, c, d);
```

### AllowAllParametersOfDeclarationOnNextLine

Allow all parameters of declaration on next line.

**Type:** `Boolean`

Similar to `AllowAllArgumentsOnNextLine` but for declarations.

### AllowBreakBeforeQtProperty

**Type:** `Boolean` **Since:** clang-format 22

Allow breaking before `Q_Property` keywords `READ`, `WRITE`, etc. as if they were preceded by a comma. This allows them to be formatted according to `BinPackParameters`.

### BinPackArguments

Pack function arguments together.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
void f() {
  f(aaaaaaaaaaaaaaaaaaaa, aaaaaaaaaaaaaaaaaaaa,
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa);
}
```

`false`:

```cpp
void f() {
  f(aaaaaaaaaaaaaaaaaaaa,
    aaaaaaaaaaaaaaaaaaaa,
    aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa);
}
```

### BinPackLongBracedList

**Type:** `Boolean` **Since:** clang-format 21

If `true`, overrides `BinPackArguments` when there are 20 or more items in a braced initializer list.

**Example:**

`false`:

```cpp
vector<int> x{
    1,
    2,
    ...,
    20,
    21};
```

`true`:

```cpp
vector<int> x{1, 2, ...,
              20, 21};
```

### BinPackParameters

Pack function parameters together.

**Type:** `BinPackParametersStyle` **Values:**

- `BinPack` - Bin-pack parameters
- `OnePerLine` - All on current line if they fit, otherwise one per line
- `AlwaysOnePerLine` - Always put each parameter on its own line

**Examples:**

`BinPack`:

```cpp
void f(int a, int bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb,
       int ccccccccccccccccccccccccccccccccccccccccccc);
```

`OnePerLine`:

```cpp
void f(int a, int b, int c);

void f(int a,
       int b,
       int ccccccccccccccccccccccccccccccccccccc);
```

`AlwaysOnePerLine`:

```cpp
void f(int a,
       int b,
       int c);
```

## Common Patterns

### Conservative Breaking (Wide Lines)

```yaml
ColumnLimit: 120
AllowShortFunctionsOnASingleLine: All
AllowShortIfStatementsOnASingleLine: AllIfsAndElse
AllowShortLoopsOnASingleLine: true
AllowShortBlocksOnASingleLine: Always
BreakBeforeBinaryOperators: None
BinPackArguments: true
BinPackParameters: BinPack
```

### Aggressive Breaking (Narrow Lines)

```yaml
ColumnLimit: 80
AllowShortFunctionsOnASingleLine: None
AllowShortIfStatementsOnASingleLine: Never
AllowShortLoopsOnASingleLine: false
AllowShortBlocksOnASingleLine: Never
BreakBeforeBinaryOperators: All
BinPackArguments: false
BinPackParameters: Never
AlwaysBreakTemplateDeclarations: Yes
```

### Balanced Breaking

```yaml
ColumnLimit: 100
AllowShortFunctionsOnASingleLine: InlineOnly
AllowShortIfStatementsOnASingleLine: WithoutElse
AllowShortLoopsOnASingleLine: false
AllowShortBlocksOnASingleLine: Empty
BreakBeforeBinaryOperators: NonAssignment
BinPackArguments: true
BinPackParameters: BinPackFirstParameter
```

## See Also

- [Brace Styles](03-braces.md) - Configure brace placement
- [Indentation](04-indentation.md) - Control indentation
- [Alignment](01-alignment.md) - Align code elements
- [Full Style Options Reference](complete/clang-format-style-options.md)

---

[← Prev: Alignment](01-alignment.md) | [Back to Index](index.md) | [Next: Braces →](03-braces.md)
