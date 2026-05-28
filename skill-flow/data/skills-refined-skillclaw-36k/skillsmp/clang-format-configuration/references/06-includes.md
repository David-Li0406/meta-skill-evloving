# Include Organization Options

[← Prev: Spacing](05-spacing.md) | [Back to Index](index.md) | [Next: Languages →](07-languages.md)

**Navigation:** [Alignment](01-alignment.md) | [Breaking](02-breaking.md) | [Braces](03-braces.md) | [Indentation](04-indentation.md) | [Spacing](05-spacing.md) | [Includes](06-includes.md) | [Languages](07-languages.md) | [Comments](08-comments.md) | [Advanced](09-advanced.md)

Organize and sort include directives automatically.

## Migration Note

**Important:** In Clang v22, `SortIncludes` has changed from a simple enum to a nested configuration structure:

- Old syntax (deprecated): `SortIncludes: Never|CaseSensitive|CaseInsensitive`
- New syntax:
  ```yaml
  SortIncludes:
    Enabled: true/false
    IgnoreCase: true/false
    IgnoreExtension: true/false
  ```

**Migration Guide:**

- `SortIncludes: Never` → `SortIncludes: { Enabled: false }`
- `SortIncludes: CaseSensitive` → `SortIncludes: { Enabled: true, IgnoreCase: false }`
- `SortIncludes: CaseInsensitive` → `SortIncludes: { Enabled: true, IgnoreCase: true }`

The old values are deprecated but still supported for backward compatibility.

## Enable Include Sorting

### SortIncludes

Controls if and how clang-format will sort `#includes`.

**Type:** `SortIncludesOptions` (nested configuration) **Suboptions:**

- `Enabled` (bool) - If `true`, includes are sorted based on other suboptions. Replaces deprecated `Never` value (use `Enabled: false` instead).
- `IgnoreCase` (bool) - Whether includes are sorted case-insensitively. Replaces deprecated `CaseSensitive` and `CaseInsensitive` values (use `IgnoreCase: false` and `IgnoreCase: true` respectively).
- `IgnoreExtension` (bool) - When sorting includes in each block, only take file extensions into account if two includes compare equal otherwise.

**Example:**

`IgnoreCase: false` (replaces `CaseSensitive`):

```cpp
#include "A/B.h"
#include "A/b.h"
#include "B/A.h"
#include "B/a.h"
#include "a/b.h"
```

`IgnoreCase: true` (replaces `CaseInsensitive`):

```cpp
#include "A/B.h"
#include "A/b.h"
#include "a/b.h"
#include "B/A.h"
#include "B/a.h"
```

`IgnoreExtension: true`:

```cpp
# include "A.h"
# include "A.inc"
# include "A-util.h"
```

`IgnoreExtension: false`:

```cpp
# include "A-util.h"
# include "A.h"
# include "A.inc"
```

**Configuration:**

```yaml
SortIncludes:
  Enabled: true
  IgnoreCase: false
  IgnoreExtension: false
```

## Include Blocks

### IncludeBlocks

How to organize include blocks.

**Type:** `IncludeBlocksStyle` **Values:**

- `Preserve` - Keep existing blocks
- `Merge` - Merge all includes into one block
- `Regroup` - Separate into blocks by category

**Examples:**

`Preserve`:

```cpp
#include "b.h"

#include "a.h"
#include <lib/main.h>
```

`Merge`:

```cpp
#include "a.h"
#include "b.h"
#include <lib/main.h>
```

`Regroup`:

```cpp
#include "a.h"
#include "b.h"

#include <lib/main.h>
```

## Include Categories

### IncludeCategories

Define categories for organizing includes.

**Type:** `List of IncludeCategories`

**Structure:**

```yaml
IncludeCategories:
  - Regex: "<[[:alnum:]]+>"
    Priority: 1
  - Regex: "<.*>"
    Priority: 2
  - Regex: ".*"
    Priority: 3
```

**Fields:**

- `Regex` - Regular expression to match include path
- `Priority` - Sort priority (lower numbers first)
- `SortPriority` - Optional separate sort priority
- `CaseSensitive` - Optional case sensitivity flag

**Example Configuration:**

```yaml
IncludeBlocks: Regroup
IncludeCategories:
  # Main header (for .cpp files)
  - Regex: '^".*\.h"$'
    Priority: 1
    SortPriority: 1
  # Project headers
  - Regex: '^".*"$'
    Priority: 2
    SortPriority: 2
  # System headers
  - Regex: '^<.*\.h>$'
    Priority: 3
    SortPriority: 3
  # C++ standard library
  - Regex: "^<.*>$"
    Priority: 4
    SortPriority: 4
```

**Result:**

```cpp
#include "myclass.h"

#include "project/helper.h"
#include "project/utils.h"

#include <stdio.h>
#include <stdlib.h>

#include <algorithm>
#include <vector>
```

## Main Include Detection

### IncludeIsMainRegex

Regex to identify main include file.

**Type:** `String` **Default:** `([-_](test|unittest))?$`

Used to ensure the main header for a .cpp file sorts first.

**Example:**

For `foo.cpp`, these would be detected as main includes:

- `foo.h`
- `foo_test.h`
- `foo-unittest.h`

```yaml
IncludeIsMainRegex: "([-_](test|unittest))?$"
```

### IncludeIsMainSourceRegex

Additional regex for detecting source files.

**Type:** `String`

**Example:**

```yaml
IncludeIsMainSourceRegex: "(_test)?$"
```

This helps clang-format recognize test files as valid source files.

## Common Configurations

### C++ with Standard Library Priority

```yaml
SortIncludes:
  Enabled: true
  IgnoreCase: false
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
IncludeIsMainRegex: "([-_](test|unittest))?$"
```

**Result:**

```cpp
// main.cpp
#include "main.h"

#include "project/module.h"

#include <sys/types.h>

#include <iostream>
#include <vector>
```

### Google C++ Style

```yaml
SortIncludes:
  Enabled: true
  IgnoreCase: false
IncludeBlocks: Regroup
IncludeCategories:
  - Regex: '^<ext/.*\.h>'
    Priority: 2
    SortPriority: 0
  - Regex: '^<.*\.h>'
    Priority: 1
    SortPriority: 1
  - Regex: "^<.*"
    Priority: 2
    SortPriority: 2
  - Regex: ".*"
    Priority: 3
    SortPriority: 3
IncludeIsMainRegex: "([-_](test|unittest))?$"
```

### LLVM Style

```yaml
SortIncludes:
  Enabled: true
  IgnoreCase: false
IncludeBlocks: Regroup
IncludeCategories:
  - Regex: '^"(llvm|llvm-c|clang|clang-c)/'
    Priority: 2
    SortPriority: 0
  - Regex: '^(<|"(gtest|gmock|isl|json)/)'
    Priority: 3
  - Regex: ".*"
    Priority: 1
IncludeIsMainRegex: "(Test)?$"
IncludeIsMainSourceRegex: ""
```

### Mozilla Style

```yaml
SortIncludes:
  Enabled: true
  IgnoreCase: true
IncludeBlocks: Regroup
IncludeCategories:
  - Regex: '^".*\.h"'
    Priority: 1
  - Regex: '^<.*\.h>'
    Priority: 2
  - Regex: "^<.*"
    Priority: 3
  - Regex: ".*"
    Priority: 4
```

### Simple Three-Tier

```yaml
SortIncludes:
  Enabled: true
  IgnoreCase: false
IncludeBlocks: Regroup
IncludeCategories:
  # Local headers
  - Regex: '^"'
    Priority: 1
  # System headers
  - Regex: '^<.*\.h>'
    Priority: 2
  # C++ standard library
  - Regex: "^<"
    Priority: 3
```

**Result:**

```cpp
#include "local.h"

#include <stdlib.h>
#include <sys/types.h>

#include <iostream>
#include <string>
```

## Tips

1. **Test Thoroughly**: Include sorting can be tricky; test on your entire codebase
2. **Main Header First**: Configure `IncludeIsMainRegex` to match your naming conventions
3. **Category Priority**: Lower priority numbers sort first
4. **Regex Matching**: Test your regex patterns carefully; they must match the full include path
5. **Case Sensitivity**: Match your filesystem's case sensitivity
6. **Block Separation**: Use `Regroup` for visual organization
7. **Gradual Adoption**: Consider `Preserve` initially, then migrate to `Regroup`

## Disabling Sorting

To disable include sorting for specific sections:

```cpp
// clang-format off
#include "z.h"
#include "a.h"
// clang-format on
```

Or globally:

```yaml
SortIncludes:
  Enabled: false
```

Note: `SortIncludes: Never` is deprecated, use `Enabled: false` instead.

## See Also

- [CLI Usage](cli-usage.md) - Command-line options including `--sort-includes`
- [Comments & Misc](08-comments.md) - Comment-related options
- [Languages](07-languages.md) - Language-specific settings
- [Full Style Options Reference](complete/clang-format-style-options.md)

---

[← Prev: Spacing](05-spacing.md) | [Back to Index](index.md) | [Next: Languages →](07-languages.md)
