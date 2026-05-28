# Language-Specific Options

[← Prev: Includes](06-includes.md) | [Back to Index](index.md) | [Next: Comments →](08-comments.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Options that apply to specific programming languages.

## Language Selection

### Language

Specify the language for formatting.

**Type:** `LanguageKind` **Values:**

- `None` - Do not use
- `C` - C
- `Cpp` - C++
- `CSharp` - C#
- `Java` - Java
- `JavaScript` - JavaScript
- `Json` - JSON
- `ObjC` - Objective-C, Objective-C++
- `Proto` - Protocol Buffers
- `TableGen` - LLVM TableGen
- `TextProto` - Text format Protocol Buffers
- `Verilog` - Verilog/SystemVerilog

**Note:** For `.h` files, specify the language explicitly with a comment:

```cpp
// clang-format Language: Cpp
```

**Usage:**

In `.clang-format`:

```yaml
---
Language: Cpp
# C++ options
---
Language: JavaScript
# JavaScript options
---
```

## JavaScript/TypeScript

### JavaScriptQuotes

Quote style for JavaScript strings.

**Type:** `JavaScriptQuoteStyle` **Values:**

- `Leave` - Keep existing quotes
- `Single` - Use single quotes
- `Double` - Use double quotes

**Example:**

`Single`:

```javascript
import { a } from "foo";
let x = "hello";
```

`Double`:

```javascript
import { a } from "foo";
let x = "hello";
```

### JavaScriptWrapImports

Wrap ES6 import/export statements.

**Type:** `Boolean`

**Example:**

`true`:

```javascript
import { VeryLongImportsAreAnnoying, VeryLongImportsAreAnnoying, VeryLongImportsAreAnnoying } from "some/module.js";
```

`false`:

```javascript
import { VeryLongImportsAreAnnoying, VeryLongImportsAreAnnoying, VeryLongImportsAreAnnoying } from "some/module.js";
```

### BreakArrays

Break after JSON array opening bracket `[`.

**Type:** `Boolean`

**Note:** This is currently only for formatting JSON. When `true`, clang-format will always break after a JSON array `[`. When `false`, it will scan until the closing `]` to determine if it should add newlines between elements (prettier compatible).

**Example:**

`true`:

```json
[1, 2, 3, 4]
```

`false`:

```json
[1, 2, 3, 4]
```

## Java

### JavaImportGroups

Define Java import groups.

**Type:** `List of Strings`

**Example:**

```yaml
JavaImportGroups:
  - com.mycompany
  - com
  - org
```

**Result:**

```java
import com.mycompany.Foo;
import com.mycompany.Bar;

import com.otherlibrary.Baz;

import org.apache.Something;
```

### BreakAfterJavaFieldAnnotations

Break after field annotations in Java.

**Type:** `Boolean`

**Example:**

`true`:

```java
@Annotation
private int myField;
```

`false`:

```java
@Annotation private int myField;
```

### SortJavaStaticImport

Control placement of static imports relative to non-static imports.

**Type:** `SortJavaStaticImportOptions` **Values:**

- `Before` - Static imports are placed before non-static imports (default)
- `After` - Static imports are placed after non-static imports

**Example:**

`Before`:

```java
import static org.example.function1;

import org.example.ClassA;
```

`After`:

```java
import org.example.ClassA;

import static org.example.function1;
```

**Note:** This option works in conjunction with `JavaImportGroups` to control Java import organization.

## C

C# uses the `CSharp` language setting and shares most options with other C-family languages.

## Protocol Buffers

Protocol buffer files use the `Proto` or `TextProto` language settings.

**Example Configuration:**

```yaml
---
Language: Proto
BasedOnStyle: Google
IndentWidth: 2
---
Language: TextProto
BasedOnStyle: Google
---
```

## TableGen (LLVM)

TableGen has specific alignment options (see [Alignment](01-alignment.md)):

- `AlignConsecutiveTableGenBreakingDAGArgColons`
- `AlignConsecutiveTableGenCondOperatorColons`
- `AlignConsecutiveTableGenDefinitionColons`

## Objective-C

### ObjCBinPackProtocolList

Pack Objective-C protocol list.

**Type:** `BinPackStyle` **Values:**

- `Auto`, `Always`, `Never`

**Example:**

`Never`:

```objc
@interface ccccccccccccc () <
  ccccccccccccc,
  ccccccccccccc,
  ccccccccccccc,
  ccccccccccccc>
```

`Always`:

```objc
@interface ccccccccccccc () <ccccccccccccc, ccccccccccccc, ccccccccccccc, ccccccccccccc>
```

### ObjCBlockIndentWidth

Indent width for ObjC blocks.

**Type:** `Unsigned`

### ObjCBreakBeforeNestedBlockParam

Break before nested block parameters.

**Type:** `Boolean`

### ObjCPropertyAttributeOrder

Order of Objective-C property attributes.

**Type:** `List of Strings`

**Example:**

```yaml
ObjCPropertyAttributeOrder:
  [
    class,
    direct,
    atomic,
    nonatomic,
    assign,
    retain,
    strong,
    copy,
    weak,
    unsafe_unretained,
    readonly,
    readwrite,
    getter,
    setter,
    nullable,
    nonnull,
    null_resettable,
    null_unspecified,
  ]
```

**Warning:** Using this option could lead to incorrect code formatting due to clang-format's lack of complete semantic information. Extra care should be taken to review code changes.

### ObjCSpaceAfterProperty

Add space after @property.

**Type:** `Boolean`

**Example:**

`true`:

```objc
@property (readonly) int a;
```

`false`:

```objc
@property(readonly) int a;
```

### ObjCSpaceBeforeProtocolList

Add space before protocol list.

**Type:** `Boolean`

**Example:**

`true`:

```objc
Foo <Protocol> *foo;
```

`false`:

```objc
Foo<Protocol> *foo;
```

## Verilog/SystemVerilog

### VerilogBreakBetweenInstancePorts

Break between instance ports.

**Type:** `Boolean`

## Multi-Language Configuration

Use separate sections for different languages:

```yaml
---
# C++ configuration
Language: Cpp
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100
---
# JavaScript configuration
Language: JavaScript
BasedOnStyle: Google
IndentWidth: 2
JavaScriptQuotes: Single
JavaScriptWrapImports: true
---
# JSON configuration
Language: Json
IndentWidth: 2
BreakArrays: true
---
# Java configuration
Language: Java
BasedOnStyle: Google
JavaImportGroups:
  - com.mycompany
  - com
  - org
---
```

## Language Detection

clang-format detects language from file extension:

- `.c` → C
- `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp` → Cpp
- `.cs` → CSharp
- `.java` → Java
- `.js`, `.mjs`, `.ts` → JavaScript
- `.json`, `.ipynb` → Json
- `.m`, `.mm` → ObjC
- `.proto` → Proto
- `.td` → TableGen
- `.txtpb`, `.textproto` → TextProto
- `.sv`, `.v`, `.vh` → Verilog

**Note:** For `.h` files that could be C, C++, or Objective-C, add a language comment at the top of the file to ensure correct detection.

Override with `--assume-filename`:

```bash
cat file.txt | clang-format --assume-filename=file.cpp
```

## Common Patterns

### JavaScript/TypeScript Project

```yaml
---
Language: JavaScript
BasedOnStyle: Google
IndentWidth: 2
ColumnLimit: 100
JavaScriptQuotes: Single
JavaScriptWrapImports: true
SpacesInContainerLiterals: true
---
```

### Java Enterprise Project

```yaml
---
Language: Java
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 120
JavaImportGroups:
  - com.company.product
  - com.company
  - java
  - javax
BreakAfterJavaFieldAnnotations: true
---
```

### Multi-Language Monorepo

```yaml
---
Language: Cpp
BasedOnStyle: Google
IndentWidth: 2
---
Language: JavaScript
BasedOnStyle: Google
IndentWidth: 2
JavaScriptQuotes: Single
---
Language: Json
IndentWidth: 2
---
Language: Proto
BasedOnStyle: Google
IndentWidth: 2
---
```

## Tips

1. **Separate Configs**: Use multiple `---` sections for different languages
2. **Shared Base**: Start each language with same `BasedOnStyle` for consistency
3. **Language Detection**: Verify correct language is detected with `--dump-config`
4. **Import Organization**: Configure Java imports and include sorting consistently
5. **Quote Style**: Match JavaScript quotes to your linter/prettier settings
6. **JSON Formatting**: Consider separate JSON formatter for complex configuration files

## See Also

- [Include Organization](06-includes.md) - Organize imports/includes
- [Comments & Misc](08-comments.md) - Comment formatting
- [CLI Usage](cli-usage.md) - Language detection and override
- [Full Style Options Reference](complete/clang-format-style-options.md)

---

[← Prev: Includes](06-includes.md) | [Back to Index](index.md) | [Next: Comments →](08-comments.md)
