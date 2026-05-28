---
name: aristotle
description: Run Aristotle automated theorem prover on Lean files to fill sorry placeholders. Use when you have a file with sorries that needs automated proof search. Handles API setup, HIT detection, and result verification.
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

1. **Check file exists**: Verify the specified `.lean` file exists
2. **Check for sorries**: Grep for `sorry` in the file - if none, inform user
3. **Check for HIT imports**: Search for imports from `Path/HIT/` or HIT axiom files

```bash
# Check for HIT imports that will cause Aristotle to fail
grep -E "import.*Path\.HIT\.|import.*Circle|import.*Torus|import.*Sphere|import.*Klein|import.*Projective|import.*Orientable|import.*NonOrientable|import.*Pushout|import.*Cylinder|import.*Mobius" "path/to/file.lean"
```

If HIT imports found, **warn the user**:
```
WARNING: This file imports HIT modules. Aristotle will likely reject it due to axiom detection.

Options:
1. Factor out non-HIT dependent proofs into a separate file
2. Use `admit` for HIT-dependent sorries and run Aristotle on the rest
3. Proceed anyway (will likely fail)

Do you want to proceed?
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

Report to user:
- Number of theorems attempted
- Number successfully proved
- Any that failed or were skipped
- Any counterexamples found

### Step 4: Verify Output (Optional)

Offer to verify the output compiles:

```bash
lake build ModuleName_aristotle
```

If `exact?` tactics are present, the build will show suggestions:
```
info: path/to/file_aristotle.lean:41:2: Try this: exact rfl
```

## Command Variations

### Basic Usage
```
/aristotle ComputationalPaths/Path/MyFile.lean
```

### With Custom Output
```
/aristotle ComputationalPaths/Path/MyFile.lean --output MyFile_proved.lean
```

### With Additional Context
```
/aristotle ComputationalPaths/Path/MyFile.lean --context ComputationalPaths/Path/Basic
```

## HIT Axiom Limitation

**Critical**: Aristotle rejects files that import modules containing axioms.

### Files That Work
- `Path/Basic/*` - Core definitions
- `Path/Rewrite/*` - Rewrite system (except ConfluenceConstructiveAxiom)
- `Path/Groupoid.lean` - Category theory
- `Path/Bicategory.lean` - 2-category theory

### Files That Don't Work
- `Path/HIT/*` - All HIT definitions
- Any file importing HITs transitively
- Files with `*Axiom.lean` imports

### Workaround Strategy

If a file has both HIT-dependent and pure theorems:

1. **Factor out pure proofs** into a separate file
2. **Run Aristotle** on the pure file
3. **Manually prove** HIT-dependent theorems

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
/- Aristotle failed to load this code into its environment.
   `theorem_name` has already been declared -/
```
**Cause**: Theorem name conflicts with imported module.

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

## Providing Proof Hints

For complex theorems, add `PROVIDED SOLUTION` in the docstring:

```lean
/--
Prove that loops on S² are trivial.

PROVIDED SOLUTION
Use the encode-decode method. The key insight is that the universal cover
of S² is contractible, so all loops lift to paths between the same point,
hence are homotopic to the constant loop.
-/
theorem sphere_loops_trivial : ... := by
  sorry
```

## Environment Setup

The API key should be set in `~/.bashrc`:
```bash
export ARISTOTLE_API_KEY='arstl_hCSoWHQ4OwTccQbXeuRXOHF-UqIH8RtVMUjS2B_vIpI'
```

If not set, the skill should set it for the session:
```bash
export ARISTOTLE_API_KEY='arstl_hCSoWHQ4OwTccQbXeuRXOHF-UqIH8RtVMUjS2B_vIpI'
```

## Version Compatibility

- **Lean**: `leanprover/lean4:v4.24.0`
- **Mathlib**: `v4.24.0`
- **Aristotle**: `aristotlelib 0.6.0+`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Axioms were added" | File imports HITs - factor out non-HIT code |
| "already been declared" | Rename theorem to avoid conflict |
| Timeout/stuck | Use `--no-wait`, check dashboard later |
| `exact?` in output | Run `lake build` to see suggestions |
| API key error | Check `ARISTOTLE_API_KEY` is set |

## Example Session

User: `/aristotle ComputationalPaths/Path/Basic/NewLemmas.lean`

Claude:
1. Reads file, finds 3 sorries
2. Checks imports - no HITs, safe to proceed
3. Runs Aristotle (waits ~3-5 minutes)
4. Reports: "Aristotle proved 3/3 theorems"
5. Offers: "Want me to verify the output compiles?"
6. Builds, reports success
7. Offers: "Want me to show the diff or replace the original file?"
