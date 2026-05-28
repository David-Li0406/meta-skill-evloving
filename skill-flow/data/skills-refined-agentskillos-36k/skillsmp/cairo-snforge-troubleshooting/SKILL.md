---
name: cairo-snforge-troubleshooting
description: Diagnose and fix common snforge test errors including Sierra compilation failures, cost computation cycles, and version mismatches; use when tests fail with cryptic errors even though `scarb build` succeeds.
---

# Cairo snforge Troubleshooting

## Overview
Guide debugging snforge test failures, particularly Sierra compilation errors that occur after successful Cairo compilation.

## Quick Use
- Read `references/common-errors.md` before diagnosing.
- Check `Scarb.toml` settings first - `enable-gas = false` causes many issues.
- Verify toolchain version compatibility (snforge, universal-sierra-compiler, Cairo).
- Generic implementations need proper trait bounds.

## Response Checklist
- If error mentions "cycle during cost computation": check `enable-gas` setting.
- If error mentions "universal-sierra-compiler": check version compatibility.
- If generic code fails: ensure `+Drop<T>`, `+Copy<T>` bounds and struct derives.
- If `scarb build` passes but `scarb test` fails: issue is test-specific compilation.

## Common Error Patterns

### "unexpected cycle during cost computation"
**Cause**: `enable-gas = false` in `[cairo]` section of `Scarb.toml`
**Fix**: Remove `enable-gas = false` or set to `true`

### "Error while compiling Sierra"
**Cause**: Version mismatch between Cairo and universal-sierra-compiler
**Fix**: Run `snfoundryup` to update toolchain

### Generic impl compilation issues
**Cause**: Missing trait bounds on generic implementations
**Fix**: Add `+Drop<T>`, `+Copy<T>` to impl and `#[derive(Drop, Copy)]` to structs

## Example Requests
- "My tests fail with 'unexpected cycle during cost computation'"
- "snforge test fails but scarb build works"
- "universal-sierra-compiler error after Cairo upgrade"
