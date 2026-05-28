# Indentation Options

[← Prev: Braces](03-braces.md) | [Back to Index](index.md) | [Next: Spacing →](05-spacing.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Control indentation behavior for various code constructs.

## Basic Indentation

### IndentWidth

Number of columns for each indentation level.

**Type:** `Unsigned` **Default:** `2`

```yaml
IndentWidth: 4
```

**Example:**

```cpp
void function() {
    if (condition) {
        doSomething();
    }
}
```

### UseTab

The way to use tab characters in the resulting file.

**Type:** `UseTabStyle` **Values:**

- `Never` - Never use tab
- `ForIndentation` - Use tabs only for indentation
- `ForContinuationAndIndentation` - Fill all leading whitespace with tabs, and use spaces for alignment that appears within a line (e.g. consecutive assignments and declarations)
- `AlignWithSpaces` - Use tabs for line continuation and indentation, and spaces for alignment
- `Always` - Use tabs whenever we need to fill whitespace that spans at least from one tab stop to the next one

**Examples:**

`Never`:

```cpp
void f() {
••••int i;
}
```

`ForIndentation`:

```cpp
void f() {
→   int i;
}
```

`Always`:

```cpp
void f() {
→   int i;
}
```

### TabWidth

Visual width of a tab character.

**Type:** `Unsigned` **Default:** `8`

```yaml
TabWidth: 4
```

Affects how existing tabs are displayed and formatted.

### ContinuationIndentWidth

Indent for line continuations.

**Type:** `Unsigned` **Default:** `4`

```yaml
ContinuationIndentWidth: 4
```

**Example:**

```cpp
int var = function1() +
    function2();

result = longFunction(
    parameter1,
    parameter2);
```

## Access Modifiers

### AccessModifierOffset

Offset for access modifiers (public, private, protected).

**Type:** `Integer` **Default:** `0`

Negative values indent left, positive values indent right.

**Examples:**

`AccessModifierOffset: -2`:

```cpp
class C {
public:
  void f();
};
```

`AccessModifierOffset: 0`:

```cpp
class C {
  public:
  void f();
};
```

`AccessModifierOffset: 2`:

```cpp
class C {
    public:
  void f();
};
```

### IndentAccessModifiers

Indent access modifiers

.

**Type:** `Boolean` **Default:** `false`

**Example:**

`true`:

```cpp
class C {
    public:
        void f();
};
```

`false`:

```cpp
class C {
  public:
    void f();
};
```

## Case Labels and Switch

### IndentCaseLabels

Indent case labels from switch statement.

**Type:** `Boolean` **Default:** `false`

**Examples:**

`false`:

```cpp
switch (fool) {
case 1:
  bar();
  break;
default:
  plop();
}
```

`true`:

```cpp
switch (fool) {
  case 1:
    bar();
    break;
  default:
    plop();
}
```

### IndentCaseBlocks

Indent case blocks.

**Type:** `Boolean` **Default:** `false`

**Examples:**

`false`:

```cpp
switch (fool) {
case 1: {
  bar();
} break;
default: {
  plop();
}
}
```

`true`:

```cpp
switch (fool) {
case 1:
  {
    bar();
  }
  break;
default:
  {
    plop();
  }
}
```

## Preprocessor Directives

### PPIndentWidth

Number of columns for preprocessor statement indentation.

**Type:** `Integer` **Default:** `-1` (uses `IndentWidth`)

```yaml
PPIndentWidth: 1
```

**Example:**

```cpp
#ifdef __linux__
# define FOO
#else
# define BAR
#endif
```

When set to -1 (default), `IndentWidth` is used also for preprocessor statements.

### IndentPPDirectives

Indent preprocessor directives.

**Type:** `PPDirectiveIndentStyle` **Values:**

- `None` - Don't indent directives
- `AfterHash` - Indent after the hash
- `BeforeHash` - Indent before the hash
- `Leave` - Leave indentation as-is (ignores `PPIndentWidth`)

**Examples:**

`None`:

```cpp
#if FOO
#if BAR
#include <foo>
#endif
#endif
```

`AfterHash`:

```cpp
#if FOO
#  if BAR
#    include <foo>
#  endif
#endif
```

`BeforeHash`:

```cpp
#if FOO
  #if BAR
    #include <foo>
  #endif
#endif
```

`Leave`:

```cpp
#if FOO
    #if BAR
#include <foo>
    #endif
#endif
```

## Special Constructs

### IndentGotoLabels

Indent goto labels.

**Type:** `Boolean` **Default:** `true`

**Examples:**

`true`:

```cpp
int f() {
  if (foo()) {
  label1:
    bar();
  }
label2:
  return 1;
}
```

`false`:

```cpp
int f() {
  if (foo()) {
label1:
    bar();
  }
label2:
  return 1;
}
```

### IndentExternBlock

Indent extern blocks.

**Type:** `IndentExternBlockStyle` **Values:**

- `AfterExternBlock` - Indent after extern
- `NoIndent` - Don't indent
- `Indent` - Indent extern block

**Examples:**

`AfterExternBlock`:

```cpp
extern "C" {
void f();
}

extern "C"
{
void g();
}
```

`NoIndent`:

```cpp
extern "C" {
void f();
}
```

`Indent`:

```cpp
extern "C" {
  void f();
}
```

### IndentRequiresClause

Indent C++20 requires clause. This only applies when `RequiresClausePosition` is `OwnLine`, `OwnLineWithBrace`, or `WithFollowing`.

**Type:** `Boolean`

Note: In clang-format 12, 13 and 14 this was named `IndentRequires`.

**Example:**

`true`:

```cpp
template <typename It>
  requires Iterator<It>
void sort(It begin, It end) {
  //....
}
```

`false`:

```cpp
template <typename It>
requires Iterator<It>
void sort(It begin, It end) {
  //....
}
```

### IndentWrappedFunctionNames

Indent wrapped function names after line break.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
LoooooooooooooooooooooooooooooongReturnType
    LoooooooooooooooooooongFunctionDeclaration();
```

`false`:

```cpp
LoooooooooooooooooooooooooooooongReturnType
LoooooooooooooooooooongFunctionDeclaration();
```

### ConstructorInitializerIndentWidth

Indent width for constructor initializers and inheritance lists.

**Type:** `Unsigned` **Default:** Uses `IndentWidth`

```yaml
ConstructorInitializerIndentWidth: 2
```

**Example:**

```cpp
Constructor()
  : member1(),
    member2() {}
```

### BracedInitializerIndentWidth

Number of columns to indent braced init list contents.

**Type:** `Integer` **Default:** Uses `ContinuationIndentWidth` if unset or negative **Since:** clang-format 17

```yaml
AlignAfterOpenBracket: AlwaysBreak
BracedInitializerIndentWidth: 2
```

**Example:**

```cpp
void f() {
  SomeClass c{
    "foo",
    "bar",
    "baz",
  };
  auto s = SomeStruct{
    .foo = "foo",
    .bar = "bar",
    .baz = "baz",
  };
  SomeArrayT a[3] = {
    {
      foo,
      bar,
    },
    {
      foo,
      bar,
    },
    SomeArrayT{},
  };
}
```

## Language-Specific

### IndentExportBlock

Indent export blocks (JavaScript). If `true`, clang-format will indent the body of an `export { ... }` block. This doesn't affect the formatting of anything else related to exported declarations.

**Type:** `Boolean` **Since:** clang-format 20

**Example:**

`true`:

```javascript
export { foo, bar };
```

`false`:

```javascript
export { foo, bar };
```

### ObjCBlockIndentWidth

Number of columns for indentation of ObjC blocks.

**Type:** `Unsigned`

```yaml
ObjCBlockIndentWidth: 4
```

**Example:**

```objc
[operation setCompletionBlock:^{
    [self onOperationDone];
}];
```

## Common Patterns

### Minimal Indentation (2 spaces)

```yaml
IndentWidth: 2
UseTab: Never
ContinuationIndentWidth: 2
AccessModifierOffset: -2
IndentCaseLabels: false
IndentCaseBlocks: false
IndentGotoLabels: true
IndentPPDirectives: None
IndentWrappedFunctionNames: false
```

### Standard Indentation (4 spaces)

```yaml
IndentWidth: 4
UseTab: Never
TabWidth: 4
ContinuationIndentWidth: 4
AccessModifierOffset: 0
IndentAccessModifiers: false
IndentCaseLabels: true
IndentCaseBlocks: false
IndentGotoLabels: true
IndentPPDirectives: AfterHash
PPIndentWidth: -1
IndentWrappedFunctionNames: true
BracedInitializerIndentWidth: 4
```

### Tab-Based Indentation

```yaml
IndentWidth: 4
UseTab: ForIndentation
TabWidth: 4
ContinuationIndentWidth: 4
AccessModifierOffset: -4
IndentCaseLabels: true
IndentPPDirectives: AfterHash
```

### Large Indentation (8 spaces, Linux style)

```yaml
IndentWidth: 8
UseTab: Always
TabWidth: 8
ContinuationIndentWidth: 8
AccessModifierOffset: -8
IndentCaseLabels: false
IndentGotoLabels: false
IndentPPDirectives: None
```

## Tips

1. **Consistency**: Use the same indentation throughout your project
2. **Tab Width**: If using tabs, ensure `TabWidth` matches team editor settings
3. **Continuation**: Set `ContinuationIndentWidth` to help distinguish continuations from blocks
4. **Access Modifiers**: Negative `AccessModifierOffset` creates outdent effect
5. **Preprocessor**: Be careful with `IndentPPDirectives` in complex macro code; use `PPIndentWidth` to control preprocessor indentation separately
6. **Mixed Tabs/Spaces**: Avoid mixing; use `Never` or `ForIndentation` for consistent results
7. **Braced Initializers**: Use `BracedInitializerIndentWidth` (clang-format 17+) to control indentation of braced init lists independently
8. **Leave Option**: The `Leave` value for `IndentPPDirectives` preserves existing preprocessor indentation without changes

## See Also

- [Alignment](01-alignment.md) - Align code elements
- [Spacing](05-spacing.md) - Control whitespace
- [Braces](03-braces.md) - Configure brace placement
- [Full Style Options Reference](complete/clang-format-style-options.md)

---

[← Prev: Braces](03-braces.md) | [Back to Index](index.md) | [Next: Spacing →](05-spacing.md)
