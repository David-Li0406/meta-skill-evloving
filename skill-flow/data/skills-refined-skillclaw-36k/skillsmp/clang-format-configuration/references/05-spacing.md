# Spacing Options

[← Prev: Indentation](04-indentation.md) | [Back to Index](index.md) | [Next: Includes →](06-includes.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Fine-tune whitespace placement throughout your code.

## Parentheses and Brackets

### SpaceBeforeParens

Add space before opening parentheses.

**Type:** `SpaceBeforeParensStyle` **Values:**

- `Never` - **Deprecated.** Use `Custom` with all `SpaceBeforeParensOptions` except `AfterPlacementOperator` set to `false`
- `ControlStatements` - Only before control statement parens
- `ControlStatementsExceptControlMacros` - Control statements except macros
- `NonEmptyParentheses` - Only if parentheses aren't empty
- `Always` - Always add space
- `Custom` - Use `SpaceBeforeParensOptions`

**Examples:**

`Never`:

```cpp
void f() {
  if(true) {
    f();
  }
}
```

`ControlStatements`:

```cpp
void f() {
  if (true) {
    f();
  }
}
```

`Always`:

```cpp
void f () {
  if (true) {
    f ();
  }
}
```

### SpaceBeforeParensOptions

Fine-grained control when `SpaceBeforeParens: Custom`.

**Sub-options:**

- `AfterControlStatements` (bool) - Space between control statement keywords and opening parentheses
- `AfterForeachMacros` (bool) - Space between foreach macros and opening parentheses
- `AfterFunctionDeclarationName` (bool) - Space between function declaration name and opening parentheses
- `AfterFunctionDefinitionName` (bool) - Space between function definition name and opening parentheses
- `AfterIfMacros` (bool) - Space between if macros and opening parentheses
- `AfterOverloadedOperator` (bool) - Space between operator overloading and opening parentheses
- `AfterPlacementOperator` (bool) - Space between operator `new`/`delete` and opening parentheses
- `AfterRequiresInClause` (bool) - Space between requires keyword in requires clause and opening parentheses
- `AfterRequiresInExpression` (bool) - Space between requires keyword in requires expression and opening parentheses
- `BeforeNonEmptyParentheses` (bool) - Space before opening parentheses only if not empty

### SpacesInParens

Defines in which cases spaces will be inserted after `(` and before `)`.

**Type:** `SpacesInParensStyle` **Values:**

- `Never` - Never put a space in parentheses
- `Custom` - Use `SpacesInParensOptions`

**Example:**

`Never`:

```cpp
void f() {
  if(true) {
    f();
  }
}
```

### SpacesInParensOptions

Control of individual spaces in parentheses when `SpacesInParens: Custom`.

**Sub-options:**

- `ExceptDoubleParentheses` (bool) - Override other options to prevent space when both opening and closing use multiple parentheses
- `InConditionalStatements` (bool) - Space in parentheses inside conditional statements
- `InCStyleCasts` (bool) - Space in C style casts
- `InEmptyParentheses` (bool) - Space in empty parentheses, i.e. `()`
- `Other` (bool) - Space in parentheses not covered by preceding options

**Example:**

```yaml
SpacesInParens: Custom
SpacesInParensOptions:
  InConditionalStatements: true
  Other: true
```

### SpacesInParentheses

**Deprecated:** Use `SpacesInParens` with `Custom` and set all `SpacesInParensOptions` to `true` except `InCStyleCasts` and `InEmptyParentheses`.

Add spaces inside parentheses.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
t f( Deleted & ) & = delete;
```

`false`:

```cpp
t f(Deleted &) & = delete;
```

### SpaceInEmptyParentheses

**Deprecated:** Use `InEmptyParentheses` in `SpacesInParensOptions`.

### SpacesInCStyleCastParentheses

**Deprecated:** Use `InCStyleCasts` in `SpacesInParensOptions`.

### SpacesInConditionalStatement

**Deprecated:** Use `InConditionalStatements` in `SpacesInParensOptions`.

### SpacesInSquareBrackets

Add spaces inside square brackets.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
int a[ 5 ];
```

`false`:

```cpp
int a[5];
```

### SpaceBeforeSquareBrackets

Add spaces before `[`.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
int a [5];
int a [5][5];
```

`false`:

```cpp
int a[5];
int a[5][5];
```

**Note:** Lambdas will not be affected. Only the first `[` gets a space.

### SpacesInAngles

Add spaces inside angle brackets.

**Type:** `SpacesInAnglesStyle` **Values:**

- `Never` - Remove spaces after `<` and before `>`
- `Always` - Add spaces after `<` and before `>`
- `Leave` - Keep a single space if any were present

**Example:**

`Always`:

```cpp
static_cast< int >(arg);
std::vector< int > vec;
```

## Operators and Assignments

### SpaceBeforeAssignmentOperators

Add space before assignment operators.

**Type:** `Boolean` **Default:** `true`

**Example:**

`true`:

```cpp
int a = 5;
a += 42;
```

`false`:

```cpp
int a= 5;
a+= 42;
```

### SpaceBeforeRangeBasedForLoopColon

Add space before colon in range-based for loop.

**Type:** `Boolean` **Default:** `true`

**Example:**

`true`:

```cpp
for (auto v : values) {}
```

`false`:

```cpp
for (auto v: values) {}
```

### SpaceInEmptyBlock

**Deprecated:** Use `Block` in `SpaceInEmptyBraces`.

Add space in empty blocks.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
void f() { }
while (true) { }
```

`false`:

```cpp
void f() {}
while (true) {}
```

### SpaceInEmptyBraces

Specifies when to insert a space in empty braces.

**Type:** `SpaceInEmptyBracesStyle` **Values:**

- `Always` - Always insert a space in empty braces
- `Block` - Only insert a space in empty blocks
- `Never` - Never insert a space in empty braces

**Note:** This option doesn't apply to initializer braces if `Cpp11BracedListStyle` is not `Block`.

**Examples:**

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
int x{};
```

`Never`:

```cpp
void f() {}
class Unit {};
auto a = [] {};
int x{};
```

## Casts and Templates

### SpaceAfterCStyleCast

Add space after C-style cast.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
(int) i;
```

`false`:

```cpp
(int)i;
```

### SpaceAfterLogicalNot

Add space after logical not operator (!).

**Type:** `Boolean`

**Example:**

`true`:

```cpp
! someExpression();
```

`false`:

```cpp
!someExpression();
```

### SpaceAfterTemplateKeyword

Add space after template keyword.

**Type:** `Boolean` **Default:** `true`

**Example:**

`true`:

```cpp
template <int> void foo();
```

`false`:

```cpp
template<int> void foo();
```

### SpaceBeforeCaseColon

Add space before case colon.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
switch (x) {
  case 1 : break;
}
```

`false`:

```cpp
switch (x) {
  case 1: break;
}
```

### SpaceBeforeCpp11BracedList

Add space before C++11 braced list.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
Foo foo { bar };
Foo {};
vector<int> { 1, 2, 3 };
new int[3] { 1, 2, 3 };
```

`false`:

```cpp
Foo foo{ bar };
Foo{};
vector<int>{ 1, 2, 3 };
new int[3]{ 1, 2, 3 };
```

### SpaceBeforeCtorInitializerColon

Add space before constructor initializer colon.

**Type:** `Boolean` **Default:** `true`

**Example:**

`true`:

```cpp
Foo::Foo() : a(a) {}
```

`false`:

```cpp
Foo::Foo(): a(a) {}
```

### SpaceBeforeInheritanceColon

Add space before inheritance colon.

**Type:** `Boolean` **Default:** `true`

**Example:**

`true`:

```cpp
class Foo : Bar {}
```

`false`:

```cpp
class Foo: Bar {}
```

### SpaceBeforeJsonColon

Add space before JSON colon.

**Type:** `Boolean`

**Example:**

`true`:

```javascript
{
  "key" : "value"
}
```

`false`:

```javascript
{
  "key": "value"
}
```

**Note:** For other languages like JavaScript, use `SpacesInContainerLiterals` instead.

## Containers and Comments

### SpacesBeforeTrailingComments

Number of spaces before trailing comments.

**Type:** `Unsigned` **Default:** `1`

**Example:**

`2`:

```cpp
void f() {
  if (true) {
    f();  // comment
  }       // comment
}
```

### SpacesInContainerLiterals

Add spaces in container literals.

**Type:** `Boolean`

**Example:**

`true` (JavaScript/JSON):

```javascript
var arr = [1, 2, 3];
obj = { a: 1, b: 2, c: 3 };
```

`false`:

```javascript
var arr = [1, 2, 3];
obj = { a: 1, b: 2, c: 3 };
```

**Note:** For JSON, use `SpaceBeforeJsonColon` instead.

### SpacesInLineCommentPrefix

Spaces in line comment prefix.

**Type:** `SpacesInLineComment` **Sub-options:**

- `Minimum` - Minimum spaces
- `Maximum` - Maximum spaces (use `-1` for no max)

**Example:**

`Minimum: 1, Maximum: -1` (no max):

```cpp
//A comment
// A comment
//  A comment
```

### SpaceAroundPointerQualifiers

Configure spaces around pointer qualifiers.

**Type:** `SpaceAroundPointerQualifiersStyle` **Values:**

- `Default`, `Before`, `After`, `Both`

**Examples:**

`Default`:

```cpp
void* const* x = NULL;
```

`Before`:

```cpp
void *const *x = NULL;
```

`After`:

```cpp
void* const* x = NULL;
```

`Both`:

```cpp
void * const * x = NULL;
```

## Bit Fields

### BitFieldColonSpacing

Spacing around bit field colon.

**Type:** `BitFieldColonSpacingStyle` **Values:**

- `Both` - Add spaces on both sides
- `None` - No spaces
- `Before` - Space before only
- `After` - Space after only

**Examples:**

`Both`:

```cpp
unsigned bf : 2;
```

`None`:

```cpp
unsigned bf:2;
```

`Before`:

```cpp
unsigned bf :2;
```

`After`:

```cpp
unsigned bf: 2;
```

## Empty Lines

### MaxEmptyLinesToKeep

Maximum consecutive empty lines to keep.

**Type:** `Unsigned` **Default:** `1`

**Example:**

`1`:

```cpp
int f() {
  int = 1;

  return i;
}
```

`2`:

```cpp
int f() {
  int i = 1;


  return i;
}
```

### KeepEmptyLines

Which empty lines are kept.

**Type:** `KeepEmptyLinesStyle` **Sub-options:**

- `AtEndOfFile` (bool) - Keep empty lines at end of file
- `AtStartOfBlock` (bool) - Keep empty lines at start of blocks
- `AtStartOfFile` (bool) - Keep empty lines at start of file

**Note:** `MaxEmptyLinesToKeep` determines how many consecutive empty lines are kept.

**Example:**

```yaml
KeepEmptyLines:
  AtEndOfFile: false
  AtStartOfBlock: false
  AtStartOfFile: false
```

### KeepEmptyLinesAtTheStartOfBlocks

**Deprecated:** Use `AtStartOfBlock` in `KeepEmptyLines`.

Keep empty lines at start of blocks.

**Type:** `Boolean` **Default:** `true`

**Example:**

`false`:

```cpp
void f() {
  foo();
}
```

`true`:

```cpp
void f() {

  foo();
}
```

### KeepEmptyLinesAtEOF

**Deprecated:** Use `AtEndOfFile` in `KeepEmptyLines`.

Keep empty lines at end of file.

**Type:** `Boolean`

## Common Patterns

### Minimal Spacing (Compact)

```yaml
SpaceBeforeParens: Never
SpaceBeforeAssignmentOperators: true
SpaceInEmptyBraces: Never
SpacesInParens: Never
SpacesInSquareBrackets: false
SpacesInAngles: Never
SpaceAfterCStyleCast: false
SpaceAfterLogicalNot: false
SpacesBeforeTrailingComments: 1
MaxEmptyLinesToKeep: 1
```

### Standard Spacing

```yaml
SpaceBeforeParens: ControlStatements
SpaceBeforeAssignmentOperators: true
SpaceInEmptyBraces: Never
SpacesInParens: Never
SpacesInSquareBrackets: false
SpacesInAngles: Never
SpaceAfterCStyleCast: false
SpaceAfterLogicalNot: false
SpaceAfterTemplateKeyword: true
SpaceBeforeCpp11BracedList: false
SpacesBeforeTrailingComments: 2
MaxEmptyLinesToKeep: 1
KeepEmptyLines:
  AtStartOfBlock: false
```

### Generous Spacing (Readable)

```yaml
SpaceBeforeParens: ControlStatements
SpaceBeforeAssignmentOperators: true
SpaceInEmptyBraces: Always
SpacesInParens: Never
SpacesInSquareBrackets: false
SpacesInAngles: Never
SpaceAfterCStyleCast: true
SpaceAfterLogicalNot: true
SpaceAfterTemplateKeyword: true
SpaceBeforeCpp11BracedList: true
SpacesBeforeTrailingComments: 2
MaxEmptyLinesToKeep: 2
KeepEmptyLines:
  AtStartOfBlock: true
```

## Tips

1. **Consistency**: Apply spacing rules uniformly across the codebase
2. **Readability**: More spaces can improve readability but increase line length
3. **Language Conventions**: Some languages have strong spacing conventions
4. **Trailing Comments**: Use at least 2 spaces before trailing comments for clarity
5. **Empty Lines**: Limit `MaxEmptyLinesToKeep` to prevent excessive whitespace
6. **Containers**: Enable `SpacesInContainerLiterals` for JSON/JavaScript readability
7. **Deprecations**: Prefer newer options like `SpacesInParens` over deprecated `SpacesInParentheses`
8. **Custom Control**: Use `Custom` settings with fine-grained options for precise control

## See Also

- [Alignment](01-alignment.md) - Align code elements
- [Indentation](04-indentation.md) - Control indentation
- [Breaking](02-breaking.md) - Control line breaks
- [Full Style Options Reference](complete/clang-format-style-options.md)

---

[← Prev: Indentation](04-indentation.md) | [Back to Index](index.md) | [Next: Includes →](06-includes.md)
