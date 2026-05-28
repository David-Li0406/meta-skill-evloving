# Nim

**Category**: languages
**Description**: Nim programming language - efficient, expressive, statically typed language that compiles to C, C++, or JavaScript
**Homepage**: https://nim-lang.org

## Package Detection

### NIMBLE
- `nimble`
- `nim`

## Configuration Files

- `*.nimble`
- `nim.cfg`
- `config.nims`
- `.nim.cfg`
- `nimsuggest.nim`
- `*.nims` (NimScript)

## File Extensions

- `.nim`
- `.nims` (NimScript)
- `.nimble`

## Import Detection

### Nim
**Pattern**: `^import\s+\w+`
- Import statement
- Example: `import strutils, sequtils`

**Pattern**: `^from\s+\w+\s+import`
- From import
- Example: `from strutils import split`

**Pattern**: `^include\s+\w+`
- Include statement
- Example: `include utils`

**Pattern**: `^proc\s+\w+`
- Procedure declaration
- Example: `proc greet(name: string): string =`

**Pattern**: `^func\s+\w+`
- Function declaration (no side effects)
- Example: `func add(a, b: int): int =`

**Pattern**: `^type\s*$`
- Type section
- Example: `type User = object`

**Pattern**: `^template\s+\w+`
- Template declaration
- Example: `template debug(x: untyped) =`

**Pattern**: `^macro\s+\w+`
- Macro declaration
- Example: `macro dumpTree(body: untyped): untyped =`

## Environment Variables

- `NIM_HOME`
- `NIMBLE_DIR`
- `NIM_PATH`

## Version Indicators

- Nim 2.0 (current major release)
- Nim 1.6 (LTS)

## Detection Notes

- Look for `.nim` files in repository
- .nimble file indicates Nimble package
- nim.cfg for project configuration
- Compiles to C, C++, JavaScript, or LLVM
- Check for `nimble install` in CI/CD

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **.nimble Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
