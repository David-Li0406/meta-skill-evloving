---
name: HSM Fuzz Testing
description: Run fuzz tests to find crashes and edge cases
version: 1.0.0
tags: [hsm, fuzzing, testing]
---

# HSM Fuzz Testing

Fuzz testing orchestration for HSM modules.

## Usage

```
/hsm-fuzz <module-number> [iterations]
```

Default iterations: 1,000,000

## What You Do

1. **List Fuzz Targets:**
   ```bash
   cd crates/<module>
   cargo fuzz list
   ```

2. **Run Fuzz Tests:**
   For each target:
   ```bash
   cargo fuzz run <target> -- -runs=<iterations>
   ```

3. **Monitor Progress:**
   Show real-time stats:
   - Runs completed / total
   - Crashes found
   - Hangs detected
   - Coverage achieved

4. **Handle Crashes:**
   If crash found:
   ```bash
   # Minimize corpus
   cargo fuzz cmin <target>

   # Minimize crash
   cargo fuzz tmin <target> crash-<hash>
   ```

5. **Report Results:**
   ```
   Target: fuzz_ed25519_verify
   Runs: 1,000,000
   Status: PASS ✅
   Crashes: 0
   Coverage: 94%
   ```

## Common Fuzz Targets

- **Crypto Engine:** sign/verify, encrypt/decrypt
- **gRPC API:** request parsing
- **Audit:** event serialization
- **Storage:** encryption/compression
