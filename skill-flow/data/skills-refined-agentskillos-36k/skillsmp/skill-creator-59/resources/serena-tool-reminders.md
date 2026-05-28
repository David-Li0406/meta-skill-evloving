# Serena Tool Reminders for Skills

Quick reference for using Serena tools in skills.

## Core Principle

**Use Serena for code operations, NOT bash commands**

| ❌ WRONG | ✅ CORRECT |
|---------|-----------|
| `bash: grep -r "pattern"` | `mcp__serena__search_for_pattern("pattern")` |
| `bash: find . -name "*.py"` | `mcp__serena__list_dir(".", recursive=true)` |
| `bash: cat file.py` + manual parsing | `mcp__serena__find_symbol("ClassName")` |
| `bash: sed/awk` edits | `mcp__serena__replace_symbol_body(...)` |

**Why:** Serena is symbol-aware, respects .gitignore, provides context, more reliable

## Essential Tools

### search_for_pattern (Search Code)

**Replace bash grep:**
```typescript
// ❌ Bad
bash: grep -r "API_KEY" .

// ✅ Good
results = mcp__serena__search_for_pattern(
  substring_pattern="API_KEY",
  output_mode="files_with_matches"
)
```

**With context lines:**
```typescript
results = mcp__serena__search_for_pattern(
  substring_pattern="def authenticate",
  context_lines_before=2,
  context_lines_after=2,
  output_mode="content"
)
```

**File filtering:**
```typescript
results = mcp__serena__search_for_pattern(
  substring_pattern="React.useState",
  paths_include_glob="**/*.tsx",
  restrict_search_to_code_files=true
)
```

**Multiline patterns:**
```typescript
results = mcp__serena__search_for_pattern(
  substring_pattern="class.*\\{[\\s\\S]*?authenticate",
  multiline=true
)
```

### list_dir (Find Files)

**Replace bash find:**
```typescript
// ❌ Bad
bash: find . -name "*.md" -type f

// ✅ Good
files = mcp__serena__list_dir(
  relative_path=".",
  recursive=true
)
// Then filter for .md in results
```

**Non-recursive:**
```typescript
files = mcp__serena__list_dir(
  relative_path="docs",
  recursive=false
)
```

**Skip ignored files:**
```typescript
files = mcp__serena__list_dir(
  relative_path=".",
  recursive=true,
  skip_ignored_files=true  // Respects .gitignore
)
```

### find_file (Exact File Match)

**Find by pattern:**
```typescript
files = mcp__serena__find_file(
  file_mask="*.md",
  relative_path="docs"
)
```

**Wildcards:**
```typescript
files = mcp__serena__find_file(
  file_mask="test_*.py",
  relative_path="tests"
)
```

### get_symbols_overview (Scan File)

**First step when exploring code:**
```typescript
// ❌ Bad: Read entire file
content = Read("backend/api/routes.py")

// ✅ Good: Get overview first
overview = mcp__serena__get_symbols_overview(
  relative_path="backend/api/routes.py"
)
// Shows: Classes, functions, imports (no bodies)
```

**Then read specific symbols:**
```typescript
// After seeing overview shows "class UserRouter"
symbol = mcp__serena__find_symbol(
  name_path="UserRouter",
  relative_path="backend/api/routes.py",
  include_body=true
)
```

### find_symbol (Locate Code)

**Find by name:**
```typescript
symbol = mcp__serena__find_symbol(
  name_path="authenticate",
  include_body=true
)
```

**Find in specific file:**
```typescript
symbol = mcp__serena__find_symbol(
  name_path="UserRouter",
  relative_path="backend/api/routes.py",
  include_body=true
)
```

**Find method in class:**
```typescript
method = mcp__serena__find_symbol(
  name_path="UserRouter/get_user",
  relative_path="backend/api/routes.py",
  include_body=true
)
```

**With descendants (get class + methods):**
```typescript
cls = mcp__serena__find_symbol(
  name_path="UserRouter",
  depth=1,  // Include direct children
  include_body=true
)
```

**Substring matching:**
```typescript
results = mcp__serena__find_symbol(
  name_path="user",
  substring_matching=true,
  include_body=false
)
// Finds: UserRouter, user_service, get_user, etc.
```

**Filter by kind:**
```typescript
classes = mcp__serena__find_symbol(
  name_path="User",
  include_kinds=[5],  // 5 = Class
  include_body=false
)
```

**LSP Symbol Kinds:**
```
1=file, 2=module, 3=namespace, 4=package, 5=class, 6=method,
7=property, 8=field, 9=constructor, 10=enum, 11=interface,
12=function, 13=variable, 14=constant, 15=string, 16=number,
17=boolean, 18=array, 19=object, 20=key, 21=null,
22=enum member, 23=struct, 24=event, 25=operator, 26=type parameter
```

### find_referencing_symbols (Find Usages)

**Who calls this function?**
```typescript
refs = mcp__serena__find_referencing_symbols(
  name_path="authenticate",
  relative_path="backend/auth/service.py"
)
// Returns: List of symbols that call authenticate()
```

**Filter references:**
```typescript
refs = mcp__serena__find_referencing_symbols(
  name_path="UserRouter",
  relative_path="backend/api/routes.py",
  include_kinds=[6, 12]  // Only methods and functions
)
```

### replace_symbol_body (Edit Code)

**Replace entire symbol:**
```typescript
// ❌ Bad: Read + Edit with regex
content = Read("file.py")
Edit("file.py", old_string="...", new_string="...")

// ✅ Good: Replace symbol directly
mcp__serena__replace_symbol_body(
  name_path="authenticate",
  relative_path="backend/auth/service.py",
  body="def authenticate(token: str) -> User:\n    # New implementation\n    ..."
)
```

**Note:** Body includes signature line

### insert_after_symbol (Add Code)

**Add new function after existing:**
```typescript
mcp__serena__insert_after_symbol(
  name_path="authenticate",
  relative_path="backend/auth/service.py",
  body="\n\ndef logout(user: User) -> None:\n    # Logout implementation\n    ...\n"
)
```

**Add at end of file:**
```typescript
// Find last symbol first
overview = mcp__serena__get_symbols_overview("file.py")
last_symbol = overview[-1]

mcp__serena__insert_after_symbol(
  name_path=last_symbol.name,
  relative_path="file.py",
  body="\n\n# New code here\n"
)
```

### insert_before_symbol (Add Code Before)

**Add import at top:**
```typescript
// Find first symbol
overview = mcp__serena__get_symbols_overview("file.py")
first_symbol = overview[0]

mcp__serena__insert_before_symbol(
  name_path=first_symbol.name,
  relative_path="file.py",
  body="from typing import Optional\n\n"
)
```

### rename_symbol (Refactor)

**Rename across codebase:**
```typescript
mcp__serena__rename_symbol(
  name_path="old_function_name",
  relative_path="backend/utils.py",
  new_name="new_function_name"
)
// Updates all references automatically
```

## Usage Patterns by Skill Type

### Workflow Skills (Discovery Heavy)

**Pattern: Search → Read → Edit**

```typescript
// 1. Search for pattern
files = mcp__serena__search_for_pattern(
  substring_pattern="TODO:",
  output_mode="files_with_matches"
)

// 2. Get overview of each file
for file in files:
  overview = mcp__serena__get_symbols_overview(file)

// 3. Read specific symbols
symbol = mcp__serena__find_symbol(
  name_path="problematic_function",
  include_body=true
)

// 4. Edit if needed
mcp__serena__replace_symbol_body(...)
```

**Example: fix-pr-feedback skill**
```typescript
### 1. Find Deleted File References
refs = mcp__serena__search_for_pattern(
  substring_pattern="github_projects.py",
  output_mode="content",
  context_lines_before=2,
  context_lines_after=2
)

### 2. For Each Reference
for ref in refs:
  // Get symbol context
  overview = mcp__serena__get_symbols_overview(ref.file)

  // Find function that has the reference
  func = mcp__serena__find_symbol(
    name_path=ref.symbol_name,
    relative_path=ref.file,
    include_body=true
  )

  // Replace with updated code
  mcp__serena__replace_symbol_body(
    name_path=ref.symbol_name,
    relative_path=ref.file,
    body=updated_body
  )
```

### Specialist Skills (Code Generation)

**Pattern: Analyze → Generate → Insert**

```typescript
// 1. Analyze existing code
files = mcp__serena__list_dir("backend/api", recursive=true)
overview = mcp__serena__get_symbols_overview("backend/api/routes.py")

// 2. Find where to insert
existing_routes = mcp__serena__find_symbol(
  name_path="APIRouter",
  include_body=false
)

// 3. Generate new code
new_route = "router.post('/endpoint')\ndef new_endpoint():\n    ..."

// 4. Insert after last route
mcp__serena__insert_after_symbol(
  name_path="last_route_name",
  relative_path="backend/api/routes.py",
  body=new_route
)
```

### Meta Skills (Read Only)

**Pattern: Scan → Analyze → Report**

```typescript
// 1. Scan all skills
skill_files = mcp__serena__list_dir(
  relative_path=".claude/skills",
  recursive=true
)

// 2. Analyze each
for skill_file in skill_files:
  overview = mcp__serena__get_symbols_overview(skill_file)

  // Check for patterns
  has_beads = mcp__serena__search_for_pattern(
    substring_pattern="mcp__plugin_beads_beads__",
    relative_path=skill_file,
    output_mode="count"
  )
```

## Token Efficiency

### Progressive Reading

**❌ Bad: Read everything**
```typescript
// Reads 500 lines
content = Read("backend/api/routes.py")
// Parse manually to find UserRouter
```

**✅ Good: Progressive disclosure**
```typescript
// Step 1: Overview (50 lines)
overview = mcp__serena__get_symbols_overview("backend/api/routes.py")
// See: UserRouter exists

// Step 2: Read only UserRouter (50 lines)
symbol = mcp__serena__find_symbol(
  name_path="UserRouter",
  include_body=true
)
// Total: 100 lines vs 500 lines
```

### Targeted Search

**❌ Bad: Broad search**
```typescript
// Returns 1000 matches
results = mcp__serena__search_for_pattern(
  substring_pattern="user"
)
```

**✅ Good: Filtered search**
```typescript
// Returns 50 matches
results = mcp__serena__search_for_pattern(
  substring_pattern="class.*User.*Router",
  paths_include_glob="backend/api/**/*.py",
  restrict_search_to_code_files=true,
  head_limit=10
)
```

## Common Patterns

### Find and Replace Pattern

```typescript
// 1. Find all occurrences
matches = mcp__serena__search_for_pattern(
  substring_pattern="old_api_call",
  output_mode="content"
)

// 2. For each match
for match in matches:
  // Get symbol containing match
  symbol = mcp__serena__find_symbol(
    name_path=match.symbol_name,
    relative_path=match.file,
    include_body=true
  )

  // Replace symbol with updated version
  updated_body = symbol.body.replace("old_api_call", "new_api_call")

  mcp__serena__replace_symbol_body(
    name_path=match.symbol_name,
    relative_path=match.file,
    body=updated_body
  )
```

### Add Import Pattern

```typescript
// 1. Get first symbol
overview = mcp__serena__get_symbols_overview("file.py")
first = overview[0]

// 2. Check if import exists
has_import = mcp__serena__search_for_pattern(
  substring_pattern="from typing import Optional",
  relative_path="file.py",
  output_mode="count"
)

// 3. Add if missing
if (has_import == 0) {
  mcp__serena__insert_before_symbol(
    name_path=first.name,
    relative_path="file.py",
    body="from typing import Optional\n"
  )
}
```

### Explore Codebase Pattern

```typescript
// 1. List directories
dirs = mcp__serena__list_dir("backend", recursive=false)

// 2. For interesting dirs
for dir in ["api", "services", "models"]:
  files = mcp__serena__list_dir(f"backend/{dir}", recursive=true)

  // 3. Get overviews
  for file in files:
    if file.endswith(".py"):
      overview = mcp__serena__get_symbols_overview(file)
      // Analyze structure
```

## Error Handling

### Symbol Not Found

```typescript
try {
  symbol = mcp__serena__find_symbol(
    name_path="MissingClass",
    include_body=true
  )
} catch {
  // Try substring matching
  results = mcp__serena__find_symbol(
    name_path="Missing",
    substring_matching=true,
    include_body=false
  )

  if (results.length > 0) {
    // Found similar symbols
  } else {
    // Truly doesn't exist
  }
}
```

### Output Too Large

```typescript
// Symptom: "Max answer chars exceeded"

// Fix: Add head_limit
results = mcp__serena__search_for_pattern(
  substring_pattern="pattern",
  head_limit=50  // Limit to first 50 results
)
```

### Multiline Pattern Issues

```typescript
// Symptom: Pattern not matching across lines

// Fix: Enable multiline mode
results = mcp__serena__search_for_pattern(
  substring_pattern="class.*\\{[\\s\\S]*?method",
  multiline=true  // . matches newlines
)
```

## Best Practices

### Do

✅ Use get_symbols_overview before reading files
✅ Use find_symbol for targeted reads
✅ Use search_for_pattern instead of bash grep
✅ Use list_dir instead of bash find
✅ Use replace_symbol_body for symbol-level edits
✅ Filter searches (glob, kinds, head_limit)
✅ Use progressive disclosure (overview → symbol)

### Don't

❌ Use bash grep/find for code operations
❌ Read entire files when you need one symbol
❌ Use Read + Edit for symbol replacement
❌ Search without filters (too many results)
❌ Forget multiline flag for cross-line patterns
❌ Ignore output_mode options (files_with_matches vs content)

## Tool Selection Guide

| Task | Tool | Why |
|------|------|-----|
| Search for text | search_for_pattern | .gitignore-aware, context lines |
| Find files | list_dir or find_file | Better metadata than bash find |
| Explore file | get_symbols_overview | See structure without reading all |
| Read function | find_symbol | Targeted, symbol-aware |
| Find usages | find_referencing_symbols | Cross-reference analysis |
| Edit function | replace_symbol_body | Symbol-level, robust |
| Add code | insert_after/before_symbol | Position-aware |
| Rename | rename_symbol | Cross-codebase refactor |

---

**Related:**
- https://github.com/oraios/serena - Official docs
- resources/v3-philosophy.md - Token efficiency
- CLAUDE.md - Tool usage policies
