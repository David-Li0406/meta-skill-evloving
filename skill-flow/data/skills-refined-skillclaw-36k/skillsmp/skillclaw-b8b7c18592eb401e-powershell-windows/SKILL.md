---
name: powershell-windows
description: Use this skill when you need to understand critical patterns and pitfalls in Windows PowerShell scripting, including operator syntax, error handling, and best practices.
---

# PowerShell Windows Patterns

> Critical patterns and pitfalls for Windows PowerShell.

## 1. Operator Syntax Rules

### CRITICAL: Parentheses Required

| ❌ Wrong                               | ✅ Correct                                 |
| -------------------------------------- | ------------------------------------------ |
| `if (Test-Path "a" -or Test-Path "b")` | `if ((Test-Path "a") -or (Test-Path "b"))` |
| `if (Get-Item $x -and $y -eq 5)`       | `if ((Get-Item $x) -and ($y -eq 5))`       |

**Rule:** Each cmdlet call MUST be in parentheses when using logical operators.

## 2. Unicode/Emoji Restriction

### CRITICAL: No Unicode in Scripts

| Purpose  | ❌ Don't Use | ✅ Use     |
| -------- | ------------ | ---------- |
| Success  | ✅ ✓         | [OK] [+]   |
| Error    | ❌ ✗ 🔴      | [!] [X]    |
| Warning  | ⚠️ 🟡        | [*] [WARN] |
| Info     | ℹ️ 🔵        | [i] [INFO] |
| Progress | ⏳           | [...]      |

**Rule:** Use ASCII characters only in PowerShell scripts.

## 3. Null Check Patterns

### Always Check Before Access

| ❌ Wrong             | ✅ Correct                       |
| -------------------- | -------------------------------- |
| `$array.Count -gt 0` | `$array -and $array.Count -gt 0` |
| `$text.Length`       | `if ($text) { $text.Length }`    |

## 4. String Interpolation

### Complex Expressions

| ❌ Wrong                    | ✅ Correct              |
| --------------------------- | ----------------------- |
| `"Value: $($obj.prop.sub)"` | Store in variable first |

**Pattern:**

```powershell
$value = $obj.prop.sub
Write-Output "Value: $value"
```

## 5. Error Handling

### ErrorActionPreference

| Value            | Use                     |
| ---------------- | ----------------------- |
| Stop             | Development (fail fast) |
| Continue         | Production scripts      |
| SilentlyContinue | When errors expected    |

### Try/Catch Pattern

- Don't return inside try block
- Use finally for cleanup
- Return after try/catch

## 6. File Paths

### Windows Path Rules

| Pattern       | Use                                     |
| ------------- | --------------------------------------- |
| Literal path  | `C:\Users\User\file.txt`                |
| Variable path | `Join-Path $env:USERPROFILE "file.txt"` |
| Relative      | `Join-Path $ScriptDir "data"`          |

**Rule:** Use Join-Path for cross-platform safety.

## 7. Array Operations

### Correct Patterns

| Operation      | Syntax                      |
|----------------|-----------------------------|
| Empty array    | `$array = @()`              |
| Add item       | `$array += $item`           |
| ArrayList add  | `$list.Add($item) | Out-Null` |

## 8. JSON Operations

### CRITICAL: Depth Parameter

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| `ConvertTo-Json` | `ConvertTo-Json -Depth 10` |

**Rule:** Always specify `-Depth` for nested objects.