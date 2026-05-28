# Quick Reference: Complete Configurations

[Back to Index](index.md) | [CLI Usage](cli-usage.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Ready-to-use complete clang-format configurations for common scenarios.

> **Note:** This reference is based on Clang v22 documentation. Some options may differ in earlier versions.

## How to Use

Copy the desired configuration to your project's `.clang-format` file:

```bash
# Copy configuration to your project
cat > .clang-format << 'EOF'
# Paste configuration here
EOF

# Test it
clang-format -i src/*.cpp include/*.h
```

## Google C++ Style (Modified)

```yaml
---
Language: Cpp
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 120

# Pointer and reference alignment
PointerAlignment: Left
ReferenceAlignment: Left
DerivePointerAlignment: false

# Line breaking
AllowShortFunctionsOnASingleLine: Inline
AllowShortIfStatementsOnASingleLine: WithoutElse
AllowShortLoopsOnASingleLine: false
AllowShortBlocksOnASingleLine: Empty
BreakBeforeBinaryOperators: None
BreakBeforeTernaryOperators: true

# Includes
SortIncludes: CaseSensitive
IncludeBlocks: Regroup
IncludeCategories:
  - Regex: '^".*\.h"'
    Priority: 1
  - Regex: '^".*'
    Priority: 2
  - Regex: '^<.*\.h>'
    Priority: 3
  - Regex: "^<.*"
    Priority: 4

# Braces
BreakBeforeBraces: Attach

# Indentation
IndentCaseLabels: true
IndentPPDirectives: AfterHash

# Spacing
SpaceBeforeParens: ControlStatements
SpacesBeforeTrailingComments: 2

# Comments
ReflowComments: true
FixNamespaceComments: true

# Empty lines
MaxEmptyLinesToKeep: 1
KeepEmptyLinesAtTheStartOfBlocks: false
```

## Linux Kernel Style

```yaml
---
Language: Cpp
BasedOnStyle: LLVM

# Use tabs
IndentWidth: 8
UseTab: Always
TabWidth: 8
ContinuationIndentWidth: 8

# Column limit
ColumnLimit: 80

# Braces
BreakBeforeBraces: Linux

# Indentation
IndentCaseLabels: false
IndentGotoLabels: false
AccessModifierOffset: -8

# Line breaking
AllowShortFunctionsOnASingleLine: None
AllowShortIfStatementsOnASingleLine: Never
AllowShortLoopsOnASingleLine: false
AllowShortBlocksOnASingleLine: Never
BreakBeforeBinaryOperators: None

# Pointer alignment
PointerAlignment: Right

# Spacing
SpaceBeforeParens: ControlStatements
SpacesInParentheses: false

# Comments
ReflowComments: false
FixNamespaceComments: false

# Alignment
AlignConsecutiveMacros: false
AlignConsecutiveAssignments: false
AlignConsecutiveDeclarations: false
AlignTrailingComments: false

# Empty lines
MaxEmptyLinesToKeep: 1

# Preprocessor
IndentPPDirectives: None
```

## Microsoft/Visual Studio Style

```yaml
---
Language: Cpp
BasedOnStyle: Microsoft
IndentWidth: 4
ColumnLimit: 120

# Braces
BreakBeforeBraces: Allman
BraceWrapping:
  AfterFunction: true
  AfterControlStatement: Always
  AfterClass: true
  AfterStruct: true
  AfterEnum: true
  BeforeElse: true
  BeforeCatch: true

# Pointer alignment
PointerAlignment: Left
ReferenceAlignment: Left

# Indentation
IndentCaseLabels: false
IndentAccessModifiers: false
AccessModifierOffset: -4

# Line breaking
AllowShortFunctionsOnASingleLine: None
AllowShortIfStatementsOnASingleLine: Never
AllowShortLoopsOnASingleLine: false
BreakBeforeBinaryOperators: None

# Spacing
SpaceBeforeParens: ControlStatements
SpacesBeforeTrailingComments: 1

# Includes
SortIncludes: CaseSensitive
IncludeBlocks: Preserve

# Comments
ReflowComments: true
FixNamespaceComments: true

# Alignment
AlignConsecutiveAssignments: false
AlignConsecutiveDeclarations: false
AlignTrailingComments: true

# Empty lines
MaxEmptyLinesToKeep: 1
```

## Modern C++17/20 Style

```yaml
---
Language: Cpp
BasedOnStyle: LLVM
Standard: c++20

IndentWidth: 2
ColumnLimit: 100

# Pointer alignment
PointerAlignment: Left
ReferenceAlignment: Left
DerivePointerAlignment: false

# Braces
BreakBeforeBraces: Attach
Cpp11BracedListStyle: true

# Breaking
AllowShortFunctionsOnASingleLine: InlineOnly
AllowShortLambdasOnASingleLine: All
AllowShortIfStatementsOnASingleLine: WithoutElse
AlwaysBreakTemplateDeclarations: Yes
BreakConstructorInitializers: BeforeColon
BreakInheritanceList: BeforeColon

# Indentation
IndentCaseLabels: true
IndentPPDirectives: AfterHash
IndentRequiresClause: true
IndentWrappedFunctionNames: false

# Spacing
SpaceBeforeParens: ControlStatements
SpaceBeforeCpp11BracedList: false
SpacesBeforeTrailingComments: 2

# Includes
SortIncludes: CaseSensitive
IncludeBlocks: Regroup
IncludeCategories:
  - Regex: '^<.*\.h>$'
    Priority: 1
  - Regex: "^<.*>$"
    Priority: 2
  - Regex: ".*"
    Priority: 3

# Alignment
AlignConsecutiveMacros: true
AlignConsecutiveAssignments: false
AlignConsecutiveDeclarations: false
AlignOperands: Align
AlignTrailingComments: true

# Comments
ReflowComments: true
FixNamespaceComments: true

# Empty lines
MaxEmptyLinesToKeep: 1
KeepEmptyLinesAtTheStartOfBlocks: false
```

## Compact/Dense Style (Minimal Whitespace)

```yaml
---
Language: Cpp
BasedOnStyle: Google
IndentWidth: 2
ColumnLimit: 120

# Braces
BreakBeforeBraces: Attach
AllowShortFunctionsOnASingleLine: All
AllowShortIfStatementsOnASingleLine: AllIfsAndElse
AllowShortLoopsOnASingleLine: true
AllowShortBlocksOnASingleLine: Always
AllowShortEnumsOnASingleLine: true

# Pointer alignment
PointerAlignment: Left

# Breaking
BinPackArguments: true
BinPackParameters: BinPack
BreakBeforeBinaryOperators: None
AllowAllArgumentsOnNextLine: true
AllowAllParametersOfDeclarationOnNextLine: true

# Spacing
SpaceInEmptyBraces: Never
SpaceBeforeParens: Never
SpacesInParentheses: false
SpacesBeforeTrailingComments: 1

# Indentation
IndentCaseLabels: true
CompactNamespaces: true

# Empty lines
MaxEmptyLinesToKeep: 1
KeepEmptyLinesAtTheStartOfBlocks: false

# Alignment
AlignConsecutiveAssignments: false
AlignConsecutiveDeclarations: false
AlignConsecutiveMacros: false
AlignTrailingComments: false
AlignOperands: DontAlign
```

## Readable/Spacious Style

```yaml
---
Language: Cpp
BasedOnStyle: LLVM
IndentWidth: 4
ColumnLimit: 100

# Braces
BreakBeforeBraces: Stroustrup

# Pointer alignment
PointerAlignment: Left

# Breaking
AllowShortFunctionsOnASingleLine: None
AllowShortIfStatementsOnASingleLine: Never
AllowShortLoopsOnASingleLine: false
AllowShortBlocksOnASingleLine: Never
BinPackArguments: false
BinPackParameters: OnePerLine
BreakBeforeBinaryOperators: NonAssignment

# Spacing
SpaceInEmptyBraces: Block
SpaceAfterCStyleCast: true
SpaceBeforeParens: ControlStatements
SpacesBeforeTrailingComments: 3
MaxEmptyLinesToKeep: 2
KeepEmptyLinesAtTheStartOfBlocks: true

# Indentation
IndentCaseLabels: true
IndentPPDirectives: AfterHash
IndentWrappedFunctionNames: true

# Alignment
AlignConsecutiveMacros:
  Enabled: true
  AcrossEmptyLines: true
AlignConsecutiveAssignments:
  Enabled: true
AlignConsecutiveDeclarations:
  Enabled: true
AlignOperands: Align
AlignTrailingComments:
  Kind: Always
  OverEmptyLines: 1

# Includes
SortIncludes: CaseSensitive
IncludeBlocks: Regroup

# Comments
ReflowComments: true
FixNamespaceComments: true

# Empty lines
EmptyLineBeforeAccessModifier: Always
EmptyLineAfterAccessModifier: Always
```

## Multi-Language Configuration

```yaml
---
# C++ Configuration
Language: Cpp
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
PointerAlignment: Left
BreakBeforeBraces: Attach
SortIncludes: CaseSensitive
---
# JavaScript/TypeScript Configuration
Language: JavaScript
BasedOnStyle: Google
IndentWidth: 2
ColumnLimit: 100
JavaScriptQuotes: Single
JavaScriptWrapImports: true
SpacesInContainerLiterals: true
---
# JSON Configuration
Language: Json
IndentWidth: 2
BreakArrays: true
---
# Protocol Buffers Configuration
Language: Proto
BasedOnStyle: Google
IndentWidth: 2
---
# Java Configuration
Language: Java
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 120
JavaImportGroups:
  - com.mycompany
  - com
  - org
  - java
  - javax
---
```

## Testing Your Configuration

After creating your `.clang-format` file:

```bash
# Test on a single file
clang-format --dry-run file.cpp

# See what would change
clang-format file.cpp | diff - file.cpp

# Apply formatting
clang-format -i file.cpp

# Format entire project
find src include -name '*.cpp' -o -name '*.h' | xargs clang-format -i

# Check in CI
clang-format --dry-run --Werror src/**/*.{cpp,h}
```

## Configuration Tips

1. **Start with a Base Style**

   - Choose a predefined style closest to your preferences
   - Only override specific options that differ

2. **Customize Incrementally**

   - Apply to a small test file first
   - Gradually expand to entire codebase
   - Test on representative code samples

3. **Document Your Choices**

   - Add comments explaining non-obvious settings
   - Maintain a style guide alongside configuration

4. **Version Control**

   - Commit `.clang-format` to repository root
   - Consider `.clang-format-ignore` for third-party code

5. **Team Adoption**
   - Get team consensus before major changes
   - Set up editor integration for everyone
   - Add pre-commit hooks for enforcement

## Troubleshooting

**Configuration not applied:**

```bash
# Check if clang-format finds your config
clang-format --dump-config file.cpp
```

**Unexpected formatting:**

```bash
# Test with explicit style
clang-format --style=file:/path/to/.clang-format file.cpp
```

**Unknown options (version mismatch):**

```bash
# Allow unknown options
clang-format --Wno-error=unknown -i file.cpp

# Check your version
clang-format --version
```

## See Also

- [Index](index.md) - Main documentation hub
- [CLI Usage](cli-usage.md) - Command-line options
- [All Style Options](index.md#style-options-by-category) - Detailed option documentation
- [Full Style Options Reference](complete/clang-format-style-options.md)
- [Full CLI Reference](complete/clang-format-cli.md)

---

[Back to Index](index.md) | [CLI Usage](cli-usage.md)
