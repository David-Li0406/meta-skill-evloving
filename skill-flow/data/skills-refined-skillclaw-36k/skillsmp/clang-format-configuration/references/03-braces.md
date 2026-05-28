# Brace Styles

[← Prev: Breaking](02-breaking.md) | [Back to Index](index.md) | [Next: Indentation →](04-indentation.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Configure brace placement and wrapping for various code constructs.

## Overview

Brace style is one of the most visible formatting choices. clang-format supports all major brace styles through the `BreakBeforeBraces` option and fine-grained control via `BraceWrapping`.

## BreakBeforeBraces

The main option controlling brace style.

**Type:** `BraceBreakingStyle`

### Predefined Styles

#### Attach (K&R style)

```cpp
namespace N {
class C {
  void f() {
    if (x) {
    } else {
    }
  }
};
}
```

#### Linux

```cpp
namespace N
{
class C
{
  void f()
  {
    if (x) {
    } else {
    }
  }
};
}
```

#### Mozilla

```cpp
namespace N {
class C
{
  void f()
  {
    if (x) {
    } else {
    }
  }
};
}
```

#### Stroustrup

```cpp
namespace N {
class C {
  void f()
  {
    if (x) {
    }
    else {
    }
  }
};
}
```

#### Allman

```cpp
namespace N
{
class C
{
  void f()
  {
    if (x)
    {
    }
    else
    {
    }
  }
};
}
```

#### Whitesmiths

```cpp
namespace N
  {
class C
  {
  void f()
    {
    if (x)
      {
      }
    else
      {
      }
    }
  };
  }
```

#### GNU

```cpp
namespace N
{
class C
  {
    void f()
      {
        if (x)
          {
          }
        else
          {
          }
      }
  };
}
```

#### WebKit

```cpp
namespace N {
class C {
  void f()
  {
    if (x) {
    } else {
    }
  }
};
}
```

#### Custom

Use `Custom` to configure individual brace wrapping with `BraceWrapping`.

```yaml
BreakBeforeBraces: Custom
BraceWrapping:
  AfterFunction: true
  AfterControlStatement: Never
  # ... more options
```

## BraceWrapping

Fine-grained control over brace wrapping when `BreakBeforeBraces: Custom`.

**Type:** `BraceWrappingFlags`

### Sub-Options

#### AfterCaseLabel

Wrap case labels.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
switch (foo)
{
  case 1:
  {
    bar();
    break;
  }
  default:
  {
    plop();
  }
}
```

`false`:

```cpp
switch (foo) {
  case 1: {
    bar();
    break;
  }
  default: {
    plop();
  }
}
```

#### AfterClass

Wrap class definitions.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
class foo
{};
```

`false`:

```cpp
class foo {};
```

#### AfterControlStatement

Wrap control statements (if/for/while/switch).

**Type:** `BraceWrappingAfterControlStatementStyle` **Values:**

- `Never` - Never wrap
- `MultiLine` - Wrap if multi-line
- `Always` - Always wrap

**Examples:**

`Never`:

```cpp
if (foo) {
} else {
}
for (int i = 0; i < 10; ++i) {
}
```

`MultiLine`:

```cpp
if (foo) {
} else {
}
for (int i = 0; i < 10; ++i)
{
}
```

`Always`:

```cpp
if (foo)
{
}
else
{
}
for (int i = 0; i < 10; ++i)
{
}
```

#### AfterEnum

Wrap enum definitions.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
enum X : int
{
  B
};
```

`false`:

```cpp
enum X : int { B };
```

#### AfterFunction

Wrap function definitions.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
void foo()
{
  bar();
}
```

`false`:

```cpp
void foo() {
  bar();
}
```

#### AfterNamespace

Wrap namespace definitions.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
namespace
{
int foo();
}
```

`false`:

```cpp
namespace {
int foo();
}
```

#### AfterStruct

Wrap struct definitions.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
struct foo
{
  int x;
};
```

`false`:

```cpp
struct foo {
  int x;
};
```

#### AfterUnion

Wrap union definitions.

**Type:** `Boolean`

Similar to `AfterStruct`.

#### AfterExternBlock

Wrap extern blocks.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
extern "C"
{
  int foo();
}
```

`false`:

```cpp
extern "C" {
  int foo();
}
```

#### AfterObjCDeclaration

Wrap ObjC definitions (interfaces, implementations...).

**Type:** `Boolean`

**Note:** `@autoreleasepool` and `@synchronized` blocks are wrapped according to `AfterControlStatement` flag.

#### BeforeCatch

Wrap before catch.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
try {
  foo();
}
catch () {
}
```

`false`:

```cpp
try {
  foo();
} catch () {
}
```

#### BeforeElse

Wrap before else.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
if (foo()) {
}
else {
}
```

`false`:

```cpp
if (foo()) {
} else {
}
```

#### BeforeLambdaBody

Wrap before lambda body.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
connect(
  []()
  {
    foo();
    bar();
  });
```

`false`:

```cpp
connect(
  []() {
    foo();
    bar();
  });
```

#### BeforeWhile

Wrap before while in do-while.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
do {
  foo();
}
while (1);
```

`false`:

```cpp
do {
  foo();
} while (1);
```

#### IndentBraces

Indent wrapped braces themselves.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
void foo()
  {
  if (true)
    {
    }
  }
```

`false`:

```cpp
void foo()
{
  if (true)
  {
  }
}
```

#### SplitEmptyFunction

Split empty functions.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
int f()
{
}
```

`false`:

```cpp
int f() {}
```

#### SplitEmptyRecord

Split empty classes/structs.

**Type:** `Boolean`

**Example:**

`true`:

```cpp
class Foo
{
}
```

`false`:

```cpp
class Foo {}
```

#### SplitEmptyNamespace

Split empty namespaces.

**Type:** `Boolean`

Similar to `SplitEmptyRecord`.

## Related Options

### BracedInitializerIndentWidth

Indent width for braced initializers.

**Type:** `Integer` **Default:** If unset or negative, `ContinuationIndentWidth` is used

**Example:**

`BracedInitializerIndentWidth: 2`:

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

### InsertBraces

Automatically insert optional braces after control statements.

**Type:** `Boolean` **Default:** `false`

**Example:**

`true`:

```cpp
if (isa<FunctionDecl>(D)) {
  handleFunctionDecl(D);
} else if (isa<VarDecl>(D)) {
  handleVarDecl(D);
} else {
  return;
}

while (i--) {
  for (auto *A : D.attrs()) {
    handleAttr(A);
  }
}

do {
  --i;
} while (i);
```

`false`:

```cpp
if (isa<FunctionDecl>(D))
  handleFunctionDecl(D);
else if (isa<VarDecl>(D))
  handleVarDecl(D);
else
  return;

while (i--)
  for (auto *A : D.attrs())
    handleAttr(A);

do
  --i;
while (i);
```

**Warning:** Insert braces after control statements (`if`, `else`, `for`, `do`, and `while`) in C++ unless the control statements are inside macro definitions or the braces would enclose preprocessor directives. Setting this option to `true` could lead to incorrect code formatting due to clang-format's lack of complete semantic information. As such, extra care should be taken to review code changes made by this option.

### RemoveBracesLLVM

Remove optional braces of control statements according to the LLVM coding style.

**Type:** `Boolean` **Default:** `false`

**Example:**

`true`:

```cpp
if (isa<FunctionDecl>(D))
  handleFunctionDecl(D);
else if (isa<VarDecl>(D))
  handleVarDecl(D);

if (isa<VarDecl>(D)) {
  for (auto *A : D.attrs())
    if (shouldProcessAttr(A))
      handleAttr(A);
}

if (isa<FunctionDecl>(D))
  for (auto *A : D.attrs())
    handleAttr(A);

if (auto *D = (T)(D)) {
  if (shouldProcess(D))
    handleVarDecl(D);
  else
    markAsIgnored(D);
}

if (a)
  b();
else if (c)
  d();
else
  e();
```

`false`:

```cpp
if (isa<FunctionDecl>(D)) {
  handleFunctionDecl(D);
} else if (isa<VarDecl>(D)) {
  handleVarDecl(D);
}

if (isa<VarDecl>(D)) {
  for (auto *A : D.attrs()) {
    if (shouldProcessAttr(A)) {
      handleAttr(A);
    }
  }
}

if (isa<FunctionDecl>(D)) {
  for (auto *A : D.attrs()) {
    handleAttr(A);
  }
}

if (auto *D = (T)(D)) {
  if (shouldProcess(D)) {
    handleVarDecl(D);
  } else {
    markAsIgnored(D);
  }
}

if (a) {
  b();
} else {
  if (c) {
    d();
  } else {
    e();
  }
}
```

**Warning:** Remove optional braces of control statements (`if`, `else`, `for`, and `while`) in C++ according to the LLVM coding style. This option will be renamed and expanded to support other styles. Setting this option to `true` could lead to incorrect code formatting due to clang-format's lack of complete semantic information. As such, extra care should be taken to review code changes made by this option.

## Common Brace Styles

### K&R / Kernel Style (Attach)

```yaml
BreakBeforeBraces: Attach
```

```cpp
int foo() {
    if (true) {
        return 0;
    } else {
        return 1;
    }
}
```

### Allman / BSD Style

```yaml
BreakBeforeBraces: Allman
```

```cpp
int foo()
{
    if (true)
    {
        return 0;
    }
    else
    {
        return 1;
    }
}
```

### Stroustrup Style

```yaml
BreakBeforeBraces: Stroustrup
```

```cpp
int foo()
{
    if (true) {
        return 0;
    }
    else {
        return 1;
    }
}
```

### Linux Kernel Style

```yaml
BreakBeforeBraces: Linux
```

```cpp
namespace N
{
int foo()
{
    if (true) {
        return 0;
    } else {
        return 1;
    }
}
}
```

### Custom: Functions Only

```yaml
BreakBeforeBraces: Custom
BraceWrapping:
  AfterFunction: true
  AfterClass: false
  AfterStruct: false
  AfterControlStatement: Never
  BeforeElse: false
  BeforeCatch: false
```

```cpp
class Foo {
    void bar()
    {
        if (x) {
        } else {
        }
    }
};
```

### Custom: Maximum Wrapping

```yaml
BreakBeforeBraces: Custom
BraceWrapping:
  AfterCaseLabel: true
  AfterClass: true
  AfterControlStatement: Always
  AfterEnum: true
  AfterFunction: true
  AfterNamespace: true
  AfterObjCDeclaration: true
  AfterStruct: true
  AfterUnion: true
  AfterExternBlock: true
  BeforeCatch: true
  BeforeElse: true
  BeforeLambdaBody: true
  BeforeWhile: true
  IndentBraces: false
  SplitEmptyFunction: true
  SplitEmptyRecord: true
  SplitEmptyNamespace: true
```

## Tips

1. **Consistency**: Choose one style and stick with it across your project
2. **Team Preference**: Match your team's existing conventions
3. **Language Idioms**: Some languages have stronger conventions (e.g., Java typically uses Attach style)
4. **Readability**: Consider what's most readable for your codebase's complexity
5. **Diff Size**: Styles with more wrapping create larger diffs when changing code

## See Also

- [Breaking & Line Wrapping](02-breaking.md) - Control line breaks
- [Indentation](04-indentation.md) - Control indentation within braces
- [Quick Reference](quick-reference.md) - Complete configuration examples
- [Full Style Options Reference](complete/clang-format-style-options.md)

---

[← Prev: Breaking](02-breaking.md) | [Back to Index](index.md) | [Next: Indentation →](04-indentation.md)
