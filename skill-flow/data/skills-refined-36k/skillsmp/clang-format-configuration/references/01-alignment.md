# Alignment Options

[← Back to Index](index.md) | [CLI Usage](cli-usage.md) | [Next: Breaking →](02-breaking.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Options for aligning code elements to improve readability and consistency.

## Overview

Alignment options control how clang-format aligns various code elements vertically. These options help create visually organized code where related elements line up in columns.

## Quick Examples

**Aligned Assignments:**

```cpp
int a        = 1;
int somelongname = 2;
double c     = 3;
```

**Aligned Declarations:**

```cpp
int         aaaa = 12;
float       b = 23;
std::string ccc = 23;
```

**Aligned Macros:**

```cpp
#define SHORT_NAME       42
#define LONGER_NAME      0x007f
#define EVEN_LONGER_NAME (2)
```

## Core Alignment Options

### AlignAfterOpenBracket

Controls alignment of parameters after an opening bracket.

**Type:** `BracketAlignmentStyle` **Values:**

- `Align` - Align parameters on the open bracket
- `DontAlign` - Don't align, use ContinuationIndentWidth
- `AlwaysBreak` - Always break after bracket
- `BlockIndent` - Always break and increase indent

**Examples:**

`Align`:

```cpp
someLongFunction(argument1,
                 argument2);
```

`DontAlign`:

```cpp
someLongFunction(argument1,
    argument2);
```

`AlwaysBreak`:

```cpp
someLongFunction(
    argument1, argument2);
```

`BlockIndent`:

```cpp
someLongFunction(
    argument1,
    argument2
);
```

### AlignArrayOfStructures

Align array of structures horizontally.

**Type:** `ArrayInitializerAlignmentStyle` **Values:**

- `None` - Don't align array initializers
- `Left` - Align and left-justify initializers
- `Right` - Align and right-justify initializers

**Examples:**

`None`:

```cpp
struct test demo[] = {
    {56, 23, "hello"},
    {-1, 93463, "world"},
    {7, 5, "!"}
};
```

`Left`:

```cpp
struct test demo[] = {
    {56,    23, "hello"},
    {-1, 93463, "world"},
    {7,      5, "!"    }
};
```

`Right`:

```cpp
struct test demo[] = {
    {   56,    23, "hello"},
    {   -1, 93463, "world"},
    {    7,     5, "!"    }
};
```

### AlignConsecutiveAssignments

Align consecutive assignment statements.

**Type:** `AlignConsecutiveStyle` **Sub-options:**

- `Enabled` (bool) - Enable alignment
- `AcrossEmptyLines` (bool) - Align across empty lines
- `AcrossComments` (bool) - Align across comments
- `AlignCompound` (bool) - Align compound assignments
- `PadOperators` (bool) - Pad operators to right

**Examples:**

`Enabled: true`:

```cpp
int a            = 1;
int somelongname = 2;
double c         = 3;
```

`Enabled: true, AcrossEmptyLines: true`:

```cpp
int a            = 1;
int somelongname = 2;

double c         = 3;
int d            = 4;
```

`Enabled: true, AlignCompound: true`:

```cpp
a   &= 2;
bbb  = 2;
```

`Enabled: true, PadOperators: true`:

```cpp
a   >>= 2;
bbb   = 2;
```

**Shorthand:**

```yaml
# Boolean shorthand
AlignConsecutiveAssignments: true

# Full control
AlignConsecutiveAssignments:
  Enabled: true
  AcrossEmptyLines: false
  AcrossComments: true
  AlignCompound: true
  PadOperators: true
```

### AlignConsecutiveBitFields

Align consecutive bit field declarations.

**Type:** `AlignConsecutiveStyle`

**Example:**

```cpp
int aaaa : 1;
int b    : 12;
int ccc  : 8;
```

### AlignConsecutiveDeclarations

Align consecutive declarations.

**Type:** `AlignConsecutiveStyle` **Sub-options:**

- `Enabled` (bool) - Enable alignment
- `AcrossEmptyLines` (bool) - Align across empty lines
- `AcrossComments` (bool) - Align across comments
- `AlignFunctionDeclarations` (bool) - Align function declarations
- `AlignFunctionPointers` (bool) - Align function pointers

**Examples:**

`Enabled: true`:

```cpp
int         aaaa = 12;
float       b = 23;
std::string ccc;
```

`Enabled: true, AcrossEmptyLines: true`:

```cpp
int         aaaa = 12;
float       b = 23;

std::string ccc;
int         d = 45;
```

`Enabled: true, AlignFunctionDeclarations: true`:

```cpp
unsigned int f1(void);
void         f2(void);
size_t       f3(void);
```

`Enabled: true, AlignFunctionPointers: true`:

```cpp
unsigned i;
int     &r;
int     *p;
int      (*f)();
```

### AlignConsecutiveMacros

Align consecutive macro definitions.

**Type:** `AlignConsecutiveStyle`

**Examples:**

`Enabled: true`:

```cpp
#define SHORT_NAME       42
#define LONGER_NAME      0x007f
#define EVEN_LONGER_NAME (2)
#define foo(x)           (x * x)
```

`Enabled: true, AcrossEmptyLines: true`:

```cpp
#define SHORT_NAME       42
#define LONGER_NAME      0x007f

#define EVEN_LONGER_NAME (2)
#define foo(x)           (x * x)
```

### AlignConsecutiveShortCaseStatements

Align consecutive short case labels.

**Type:** `ShortCaseStatementsAlignmentStyle` **Sub-options:**

- `Enabled` (bool)
- `AcrossEmptyLines` (bool)
- `AcrossComments` (bool)
- `AlignCaseColons` (bool) - Align case colons
- `AlignCaseArrows` (bool) - Align case arrows (for languages like Verilog)

**Example:**

`Enabled: true`:

```cpp
switch (x) {
case 1:  return "one";
case 2:  return "two";
case 10: return "ten";
}
```

`Enabled: true, AlignCaseColons: true`:

```cpp
switch (x) {
case 1  : return "one";
case 2  : return "two";
case 10 : return "ten";
}
```

### AlignEscapedNewlines

Align escaped newlines in macros.

**Type:** `EscapedNewlineAlignmentStyle` **Values:**

- `DontAlign` - Don't align
- `Left` - Align to the left
- `Right` - Align to the right
- `LeftWithLastLine` - Align to left, but relative to last line

**Examples:**

`Left`:

```cpp
#define A \
  int aaaa; \
  int b; \
  int dddddddddd;
```

`Right`:

```cpp
#define A                                                                      \
  int aaaa;                                                                    \
  int b;                                                                       \
  int dddddddddd;
```

### AlignOperands

Align operands of binary and ternary expressions.

**Type:** `OperandAlignmentStyle` **Values:**

- `DontAlign` - Don't align
- `Align` - Align operands
- `AlignAfterOperator` - Align after operators

**Examples:**

`Align`:

```cpp
int aaa = bbbbbbbbbbbbbbb +
          ccccccccccccccc;
```

`AlignAfterOperator`:

```cpp
int aaa = bbbbbbbbbbbbbbb
        + ccccccccccccccc;
```

### AlignTrailingComments

Align trailing comments.

**Type:** `TrailingCommentsAlignmentStyle` **Sub-options:**

- `Kind` - Alignment kind (Leave, Always, Never)
- `OverEmptyLines` - Lines to align over

**Examples:**

`Kind: Always`:

```cpp
int a;      // Comment a
int b = 2;  // Comment b
```

`Kind: Always, OverEmptyLines: 1`:

```cpp
int a;  // Comment a

int b;  // Comment b (aligned with comment a)
```

**Shorthand:**

```yaml
# Boolean shorthand
AlignTrailingComments: true

# Full control
AlignTrailingComments:
  Kind: Always
  OverEmptyLines: 0
```

## TableGen-Specific Alignment

These options apply specifically to LLVM TableGen code.

### AlignConsecutiveTableGenBreakingDAGArgColons

Align colons in breaking DAG arguments.

**Type:** `AlignConsecutiveStyle`

### AlignConsecutiveTableGenCondOperatorColons

Align colons in condition operators.

**Type:** `AlignConsecutiveStyle`

### AlignConsecutiveTableGenDefinitionColons

Align colons in definitions.

**Type:** `AlignConsecutiveStyle`

## Common Patterns

### Minimal Alignment (Performance-Focused)

```yaml
AlignAfterOpenBracket: DontAlign
AlignConsecutiveAssignments: false
AlignConsecutiveBitFields: false
AlignConsecutiveDeclarations: false
AlignConsecutiveMacros: false
AlignEscapedNewlines: DontAlign
AlignOperands: DontAlign
AlignTrailingComments: false
```

### Maximum Alignment (Readability-Focused)

```yaml
AlignAfterOpenBracket: Align
AlignArrayOfStructures: Left
AlignConsecutiveAssignments:
  Enabled: true
  AcrossEmptyLines: true
  AcrossComments: true
  AlignCompound: true
  PadOperators: true
AlignConsecutiveBitFields:
  Enabled: true
AlignConsecutiveDeclarations:
  Enabled: true
  AlignFunctionDeclarations: true
  AlignFunctionPointers: true
AlignConsecutiveMacros:
  Enabled: true
  AcrossEmptyLines: true
AlignEscapedNewlines: Right
AlignOperands: Align
AlignTrailingComments:
  Kind: Always
  OverEmptyLines: 1
```

### Moderate Alignment (Balanced)

```yaml
AlignAfterOpenBracket: Align
AlignConsecutiveAssignments: false
AlignConsecutiveBitFields: true
AlignConsecutiveDeclarations: false
AlignConsecutiveMacros: true
AlignEscapedNewlines: Right
AlignOperands: Align
AlignTrailingComments: true
```

## Tips

1. **Performance Impact**: Extensive alignment can make diffs noisier and may slow formatting slightly
2. **Maintenance**: Aligned code may require more adjustments when making changes
3. **Consistency**: Choose alignment settings that match your team's preferences
4. **Selective Use**: Consider aligning only specific elements (e.g., macros but not assignments)
5. **Empty Lines**: Use `AcrossEmptyLines` carefully as it can create large alignment blocks

## See Also

- [Breaking & Line Wrapping](02-breaking.md) - Control where lines break
- [Indentation](04-indentation.md) - Control indentation behavior
- [Spacing](05-spacing.md) - Fine-tune whitespace
- [Full Style Options Reference](complete/clang-format-style-options.md)

---

[← Back to Index](index.md) | [CLI Usage](cli-usage.md) | [Next: Breaking →](02-breaking.md)
