---
name: aristotle
description: Run Aristotle automated theorem prover on Lean files to fill sorry placeholders. Use when you have a file with sorries that needs automated proof search. Handles API setup, HIT detection, and result verification.
---

# Aristotle Automated Theorem Prover

Run [Aristotle](https://aristotle.harmonic.fun) to automatically fill `sorry` placeholders in Lean 4 files.

## Workflow

1. **Validate file**: Check for `sorry` in the target file
2. **Check for HIT imports**: Aristotle may fail on files importing HIT axioms
3. **Run Aristotle**: Submit file for proof search
4. **Apply results**: Replace sorries with generated proofs
5. **Verify**: Run `lake build` to confirm

## HIT Detection

Check for imports that may cause issues:

```bash
grep -E "import.*Path\.HIT\.|import.*Circle|import.*Torus|import.*Sphere" "path/to/file.lean"
```

If HIT imports are found, consider:
- Moving the proof to a separate file
- Using manual proof instead

## Usage Notes

- Aristotle works best on pure computational proofs
- May struggle with axiom-heavy HIT modules
- Always verify generated proofs compile
