---
name: aristotle
description: Use this skill to run the Aristotle automated theorem prover on Lean files to fill `sorry` placeholders. It handles API setup, HIT detection, and result verification.
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
2. **Check for sorries**: Grep for `sorry` in the file; if none, inform the user.
3. **Check for HIT imports**: Search for imports that may cause Aristotle to fail.

```bash
grep -n "sorry" "path/to/file.lean"
grep -E "import.*Path\.HIT\.|import.*Circle|import.*Torus|import.*Sphere" "path/to/file.lean"
```

If HIT imports are found, warn the user:
```
WARNING: This file imports HIT modules. Aristotle will likely reject it due to axiom detection.

Options:
1. Factor out non-HIT dependent proofs into a separate file.
2. Use `admit` for HIT-dependent sorries and run Aristotle on the rest.
3. Proceed anyway (will likely fail).
```

### Step 2: Run Aristotle

```bash
export ARISTOTLE_API_KEY='arstl_hCSoWHQ4OwTccQbXeuRXOHF-UqIH8RtVMUjS2B_vIpI'
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

### With Additional Context
```
/aristotle path/to/file.lean --context path/to/context.lean
```

## Interpreting Aristotle Output

### Success Indicators

```lean
/-
The following was proved by Aristotle:
- theorem my_theorem : ...
-/
```

### Common Proof Tactics

| Tactic | Meaning |
|--------|---------|
| `exact?` | Found matching lemma (build to see suggestion) |
| `grind` | Automation solved it |
| `simp` | Simplification worked |
| `rfl` | Reflexivity |
| `omega` | Linear arithmetic |
| `decide` | Decidable proposition |

### Failure Indicators

```lean
/- Aristotle failed to load this code into its environment. -/
```
**Cause**: Syntax issues or import problems.

```lean
Aristotle encountered an error while processing imports for this file.
Error: Axioms were added during init_sorries: [...]
```
**Cause**: File imports HIT axioms.

### Counterexamples

If Aristotle proves the negation:
```lean
/-
Aristotle found this block to be false.
Here is a proof of the negation:
...
-/
```
**Action**: Review the theorem statement - it may be incorrectly formalized.

## Environment Setup

The API key should be set in `~/.bashrc`:
```bash
export ARISTOTLE_API_KEY='arstl_hCSoWHQ4OwTccQbXeuRXOHF-UqIH8RtVMUjS2B_vIpI'
```

If not set, the skill should set it for the session:
```bash
export ARISTOTLE_API_KEY='arstl_hCSoWHQ4OwTccQbXeuRXOHF-UqIH8RtVMUjS2B_vIpI'
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Axioms were added" | File imports HITs - factor out non-HIT code. |
| "already been declared" | Rename theorem to avoid conflict. |
| Timeout/stuck | Use `--no-wait`, check dashboard later. |
| `exact?` in output | Run `lake build` to see suggestions. |
| API key error | Check `ARISTOTLE_API_KEY` is set. |

## Example Session

User: `/aristotle path/to/file.lean`

Claude:
1. Reads file, finds 2 sorries.
2. Checks imports - no HITs, safe to proceed.
3. Runs Aristotle (waits ~3-5 minutes).
4. Reports: "Aristotle proved 2/2 theorems."
5. Offers: "Want me to verify the output compiles?"
6. Builds, reports success.
7. Offers: "Want me to show the diff or replace the original file?"