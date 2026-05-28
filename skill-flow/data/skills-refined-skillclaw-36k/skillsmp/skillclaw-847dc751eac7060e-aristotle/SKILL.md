---
name: aristotle
description: Use this skill when you have a Lean 4 file with `sorry` placeholders that needs automated proof search using the Aristotle theorem prover.
---

# Aristotle Automated Theorem Prover

This skill runs [Aristotle](https://aristotle.harmonic.fun) to automatically fill `sorry` placeholders in Lean 4 files.

## Quick Usage

```
/aristotle path/to/file.lean
```

## Workflow

When the user invokes `/aristotle`, follow these steps:

### Step 1: Validate the Target File

1. **Check file exists**: Verify the specified `.lean` file exists.
2. **Check for sorries**: Grep for `sorry` in the file - if none, inform the user.
3. **Check for HIT imports**: Search for imports that may cause Aristotle to fail.

```bash
grep -n "sorry" "path/to/file.lean"
grep -E "import.*Path\.HIT\.|import.*Circle|import.*Torus|import.*Sphere" "path/to/file.lean"
```

If HIT imports are found, warn the user:
```
WARNING: This file imports HIT modules. Aristotle may reject it due to axiom detection.

Options:
1. Factor out non-HIT dependent proofs into a separate file.
2. Use `admit` for HIT-dependent sorries and run Aristotle on the rest.
3. Proceed anyway (will likely fail).
```

### Step 2: Run Aristotle

```bash
export ARISTOTLE_API_KEY='your_api_key_here'
uvx --from aristotlelib aristotle.exe prove-from-file "path/to/file.lean" \
  --output-file "path/to/file_aristotle.lean"
```

**Important**: The command may take several minutes. Aristotle queues jobs and polls for completion.

### Step 3: Report Results

After Aristotle completes, read the output file header to see what was proved:

```lean
/-
This file was edited by Aristotle.
...
The following was proved by Aristotle:
- theorem foo : ...
- theorem bar : ...
-/
```

Report to the user:
- Number of theorems attempted
- Number successfully proved
- Any that failed or were skipped
- Any counterexamples found

### Step 4: Verify Output

Offer to verify the output compiles:

```bash
lake build ModuleName_aristotle
```

If `exact?` tactics are present, the build will show suggestions.

## Command Variations

### Basic Usage
```
/aristotle path/to/file.lean
```

### With Custom Output
```
/aristotle path/to/file.lean --output custom_output.lean
```

## Notes

- Aristotle works best on pure computational proofs.
- It may struggle with axiom-heavy HIT modules.
- Always verify that generated proofs compile.