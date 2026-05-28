# Theory Verification Workflow

Systematic verification of performance theories using profiling tools.

## Core Principles

- **Code analysis finds potential issues. Tools prove which issues actually matter.**
- **Work iteratively** - verify the most critical theory first, fix it, then continue
- **Trust the tools** - tool output is authoritative for data
- **Stay flexible** - adapt when new evidence emerges

## Phase 1: Select Theory to Verify

**Objective**: Choose the highest-impact unverified theory

### Process

1. Review the theory list from `generating-performance-theories`
2. Select the highest-severity unverified theory
3. Note the theory's verification plan (which tools are needed)

If one theory is verified, proceed to `implementing-performance-fixes` for the verified theory.

## Phase 2: Prepare for Verification

**Objective**: Understand what you're looking for before running tools

### Process

1. **Load tool documentation** - Use the relevant tool skills to understand:
   - What commands to run
   - What output to expect
   - How to interpret results

2. **Form expectations** (Fermi estimation) - Before running tools, estimate:
   - Approximate magnitude of expected output
   - What would confirm the theory
   - What would contradict the theory

This prevents garbage-in-garbage-out from misconfigured tools.

## Phase 3: Execute Tools

**Objective**: Collect quantitative evidence

### Process

Run the tools specified in the theory's verification plan. For each tool:

1. **Smoke test** (if first time using this tool) - Run on trivial input to verify tool works
2. **Execute** on the actual benchmark
3. **Validate output** - Does magnitude match expectations?
   - Within ~1 order of magnitude → proceed with analysis
   - Wildly different or unexpected zero → diagnose before trusting

Save outputs to `tool-outputs/` for later reference.

### Direct Implementation as Verification (for small fixes)

If the proposed fix is small (<10 lines of code), you can verify the theory empirically:

1. Implement the fix
2. Build the project
3. Run the benchmark and compare against baseline
4. Significant improvement → theory VERIFIED
5. No improvement → theory FALSIFIED or requires further investigation

This approach provides direct empirical evidence and is often faster than extensive profiling for simple changes.

### Handling Unexpected Results

If tool output doesn't match expectations:
- Check tool configuration and command syntax
- Verify benchmark is running correctly
- Consider whether your expectation was wrong (update mental model)

## Phase 4: Handle Emergent Issues

**Objective**: Respond appropriately when tools reveal unexpected problems

While running tools, you may discover issues not in your theory list (e.g., a deoptimization loop, compilation failure, unexpected allocation pattern).

### When This Happens

1. **Assess the new issue's severity** - Is it Critical, High, Medium, or Low?
2. **Compare to current theory** - Which has greater performance impact?

### Decision

- **New issue is MORE critical** → **Pivot**: Stop current verification, investigate the new issue. The original theory remains unverified for now.

- **New issue is LESS critical** → **Note it**: Record as "Future Work" in your findings, continue with current theory.

Use your judgment. The goal is to fix the most impactful issues first.

## Phase 5: Synthesize Evidence

**Objective**: Determine if the theory is proven, disproven, or unclear

### Evaluate Tool Results

Consider all evidence collected:
- Do multiple tools agree?
- Is there quantitative data (frequencies, percentages, counts)?
- Does the evidence support or contradict the theory?

### Reach a Verdict

- **VERIFIED** - Evidence confirms the theory with quantitative data
- **FALSIFIED** - Evidence contradicts the theory
- **INCONCLUSIVE** - Insufficient or conflicting data

For verified theories, characterize:
- Root cause (from tool evidence)
- Quantified impact (frequency, time%, allocations)
- Affected code locations

## Phase 6: Next Steps

### If VERIFIED

1. Update theory status to `verified` in PERFORMANCE_THEORIES.md
2. **Stop verification** - proceed to `implementing-performance-fixes` skill
3. The fix skill will handle implementation, validation, and iteration

### If FALSIFIED

1. Document why the theory was wrong (learning for future)
2. Proceed immediately to next highest-priority theory

### If INCONCLUSIVE

1. Note which tools worked and which didn't
2. Proceed to next theory (may revisit after other fixes clear the signal)

### If PIVOTED to Emergent Issue

1. Add the new issue to your theory list with appropriate severity
2. Complete verification of the emergent issue
3. Original theory may be revisited later

## Guidelines for Judgment Calls

### When to Pivot vs Continue

Pivot if the emergent issue:
- Is causing deoptimization loops in hot paths
- Is blocking compilation of core functions
- Would make current theory's impact negligible by comparison

Continue if the emergent issue:
- Affects cold paths only
- Is a minor optimization opportunity
- Can wait until after the current fix

### When to Trust vs Question Tool Output

Trust when:
- Output matches rough expectations
- Multiple tools corroborate
- Tool executed without errors

Question when:
- Output is zero or unexpectedly empty
- Values are orders of magnitude off from estimates
- Tool reported warnings or errors

### How Many Tools Are Enough

- Minimum: The tools specified in the theory's verification plan
- Add more if: Evidence is conflicting or insufficient
- Stop when: You have confident quantitative evidence for a verdict

## Integration Notes

**Inputs**: Theories from `generating-performance-theories` skill

**Tool Skills**: Use as needed based on theory type:
- `profiling-with-cpu-sampler` - where time is spent
- `tracing-execution-counts` - how often code runs
- `detecting-performance-warnings` - optimization barriers
- `tracing-compilation-events` - compilation behavior
- `tracing-inlining-decisions` - inlining analysis
- `detecting-deoptimizations` - type stability issues
- `profiling-memory-allocations` - allocation patterns
- `analyzing-compiler-graphs` - deep IR analysis

**Output**: Verified theories ready for `implementing-performance-fixes`
