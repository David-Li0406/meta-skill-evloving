# AILANG Error Catalog

Complete reference of AILANG error messages with causes and fixes.

## Parse Errors

### PAR_UNEXPECTED_TOKEN

**Message:** `expected next token to be X, got Y instead`

**Common cases:**

| Expected | Got | Cause | Fix |
|----------|-----|-------|-----|
| `}` | `let` | Missing semicolon | Add `;` between statements |
| `}` | `IDENT` | No loops in AILANG | Use recursion instead |
| `)` | `,` | Wrong function call syntax | Check argument count |

**Example fix:**
```ailang
-- WRONG: missing semicolons
{
  let x = 10
  let y = 20
  x + y
}

-- CORRECT
{
  let x = 10;
  let y = 20;
  x + y
}
```

### PAR_NO_PREFIX_PARSE

**Message:** `unexpected token in expression: X`

**Common triggers:**
- `for` - AILANG has no for loops
- `while` - AILANG has no while loops
- `in` - No `for x in xs` syntax
- `}` - Unmatched braces

**Fix:** Use recursion and pattern matching instead of loops.

```ailang
-- Instead of: for i in range(5) { ... }
export func loop(n: int) -> () ! {IO} {
  if n <= 0 then () else {
    print(show(n));
    loop(n - 1)
  }
}
```

## Type Errors

### Undefined Variable

**Message:** `undefined variable: X at file.ail:line:col`

**Common cases:**

| Variable | Module | Import |
|----------|--------|--------|
| `print` | std/io | Auto-imported in entry modules |
| `println` | N/A | **Does not exist** - use `print` |
| `map` | std/list | `import std/list (map)` |
| `filter` | std/list | `import std/list (filter)` |
| `fold` | std/list | `import std/list (fold)` |
| `show` | builtin | Auto-imported |
| `readFile` | std/fs | `import std/fs (readFile)` |
| `writeFile` | std/fs | `import std/fs (writeFile)` |
| `httpGet` | std/net | `import std/net (httpGet)` |
| `httpPost` | std/net | `import std/net (httpPost)` |
| `now` | std/clock | `import std/clock (now)` |
| `decode` | std/json | `import std/json (decode)` |
| `encode` | std/json | `import std/json (encode)` |

**Find what module has a function:**
```bash
ailang builtins list | grep functionName
ailang builtins list --by-module
```

### No Instance for Num[string]

**Message:** `No instance for Num[string] in scope`

**Cause:** Passing a number where a string is expected.

```ailang
-- WRONG: print expects string
print(42)

-- CORRECT: convert with show()
print(show(42))
```

### Type Mismatch

**Message:** `type mismatch: expected X, got Y`

**Common cases:**

| Expected | Got | Fix |
|----------|-----|-----|
| `string` | `int` | Use `show(intValue)` |
| `int` | `float` | Use `floatToInt(floatValue)` |
| `float` | `int` | Use `intToFloat(intValue)` |
| `[a]` | `a` | Wrap in list: `[value]` |

## Module Errors

### MOD010 - Module Path Mismatch

**Message:** `module 'X' does not match canonical path 'Y'`

**Cause:** Module declaration doesn't match file path.

**Fixes:**
1. Rename module to match path
2. Use `--relax-modules` flag
3. Set `AILANG_RELAX_MODULES=1`

```bash
# For prototyping, relax module matching
ailang run --relax-modules --caps IO --entry main file.ail

# Or set environment variable
export AILANG_RELAX_MODULES=1
```

**Note:** Files in `/tmp` auto-relax this check.

## Effect Errors

### Missing Capability

**Message:** `effect X not in allowed set`

**Fix:** Add capability to `--caps` flag:

```bash
# WRONG: missing IO capability
ailang run --entry main file.ail

# CORRECT
ailang run --caps IO --entry main file.ail

# Multiple capabilities
ailang run --caps IO,FS,Net --entry main file.ail
```

**Capability reference:**

| Capability | Enables |
|------------|---------|
| `IO` | `print`, `readLine`, `readInt` |
| `FS` | `readFile`, `writeFile`, `listDir` |
| `Net` | `httpGet`, `httpPost`, `httpRequest` |
| `Clock` | `now`, `sleep` |
| `AI` | `AI.call(prompt)` |

## Runtime Errors

### Pattern Match Failure

**Message:** `non-exhaustive pattern match`

**Cause:** Match expression doesn't cover all cases.

```ailang
-- WRONG: missing None case
match opt {
  Some(x) => x
}

-- CORRECT: handle all cases
match opt {
  Some(x) => x,
  None => defaultValue
}
```

### Division by Zero

**Message:** `division by zero`

**Fix:** Check divisor before dividing:

```ailang
export func safeDivide(a: int, b: int) -> Option[int] {
  if b == 0 then None else Some(a / b)
}
```

## CLI Errors

### Flags After Filename

**Symptom:** Flags appear to be ignored.

**Cause:** Flags must come BEFORE the filename.

```bash
# WRONG: --caps is ignored!
ailang run file.ail --caps IO

# CORRECT
ailang run --caps IO --entry main file.ail
```

### Entry Point Not Found

**Message:** `entry point 'main' not found`

**Fixes:**
1. Add `export` to your main function
2. Specify different entry point with `--entry`

```ailang
-- WRONG: not exported
func main() -> () ! {IO} { ... }

-- CORRECT: exported
export func main() -> () ! {IO} { ... }
```

## Debugging Commands

```bash
# Type-check without running
ailang check file.ail

# Interactive REPL
ailang repl

# In REPL:
> :type expression    -- Show type
> :help               -- Show commands
> :load file.ail      -- Load file

# List all builtins
ailang builtins list --by-module

# Search for a builtin
ailang builtins list | grep functionName

# Watch for changes
ailang watch file.ail

# Trace execution
ailang run --trace --caps IO --entry main file.ail
```
