---
name: analyze-julia-compiler-pr
description: Analyze a Julia compiler PR for downstream impact, secondary effects, and changelog generation. Use when asked to analyze a PR number, when working with compiler_prs.json data, or when the user asks about Julia compiler changes and their effects on downstream packages like Turing.jl, Enzyme.jl, GPUCompiler, JET, IRTools, or Cassette.
---

# Julia Compiler PR Analysis Skill

Analyze Julia compiler PRs to generate structured changelog entries for downstream package maintainers (Turing.jl, Enzyme.jl, GPUCompiler, JET, etc.).

## Data Location

- PR cache: `pr-archive/JuliaLang_julia/`
- Compiler PRs list: `pr-archive/JuliaLang_julia/compiler_prs.json`
- Analysis output: `analyses/pr_{number}.yaml` (per-PR file)
- Schema: `references/analysis-schema.json`

## Setup: Clone Julia Repository

**IMPORTANT:** Before analyzing PRs, clone the Julia repository to examine full code context (not just diffs):

```bash
# Clone Julia repo if not present
if [ ! -d "julia" ]; then
  git clone --depth 100 https://github.com/JuliaLang/julia.git julia
fi

# Checkout the merge commit for a specific PR
cd julia
git fetch origin pull/{PR_NUMBER}/merge:pr-{PR_NUMBER}
git checkout pr-{PR_NUMBER}
```

This enables:
- Reading full file context around changed lines
- Tracing function call sites and callers
- Understanding data structures being modified
- Finding secondary effects not visible in the diff alone

## Compiler Pipeline (how changes propagate)

```
JuliaSyntax parser/tokenizer
  -> AST shape & token kinds
  -> Macro expansion + hygiene
  -> JuliaLowering desugaring + scope analysis
  -> Linear IR / closure conversion
  -> CodeInfo / SSA IR
  -> Abstract interpretation + type inference
  -> Effects & escape analysis
  -> Inlining & optimization passes
  -> Codegen / runtime behavior
  -> Interpreter fallback + debugging tools
```

Changes early in the pipeline (JuliaSyntax/JuliaLowering) tend to amplify downstream.

## Analysis Framework

For each PR, investigate and document:

### A. PR Metadata & Intent
- Title, labels, linked issues, merge date
- Stated intent vs observed changes

### B. Pipeline Localization
Map touched files to stages:
- `JuliaSyntax/` -> Parsing, tokenization
- `JuliaLowering/` -> Lowering, scope analysis, closure conversion
- `Compiler/src/abstractinterpretation.jl` -> Type inference
- `Compiler/src/ssair/` -> SSA IR, inlining, optimization passes
- `Compiler/src/tfuncs.jl` -> Type functions
- `src/interpreter.c` -> Interpreter

### C. Change Taxonomy
- Semantic vs performance vs diagnostics vs refactor-only
- Compile-time vs runtime behavior
- Internal API changes vs implementation-only

### D. Direct Behavior Deltas
- New/changed AST or IR forms
- New invariants or removed passes
- Altered heuristics

### E. Secondary Propagation Analysis (CRITICAL)
Trace how changes ripple through:
- Inference <-> Inlining feedback loops
- Macro expansion <-> Lowering interactions
- Effects inference -> Optimization decisions
- Type lattice changes -> Specialization behavior

### F. Downstream Package Impact
Check for effects on:
- **OpaqueClosure** - creation, inference, optimization
- **Generated functions** - `@generated` execution
- **World age / invalidation** - method tables, caches
- **Internal API consumers** - IRTools, Cassette, JET, GPUCompiler, Enzyme
- **Effect flags** - `:consistent`, `:effect_free`, `:nothrow`, etc.

### G. Evidence & Confidence
- Test changes and assertions
- Risk level: low/medium/high

## Output Schema (YAML)

```yaml
schema_version: "1.0"
pr:
  number: int
  title: string
  url: uri
  author: string
  labels: [string]
  merged_at: datetime
scope:
  files_touched: [string]
  components: [JuliaSyntax|JuliaLowering|Compiler.*|Interpreter]
  pipeline_stages: [Parsing|Lowering|TypeInference|Inlining|...]
analysis:
  intent:
    summary: string
    issue_links: [string]
  direct_changes:
    - summary: string
      component: string
      evidence: [{source, path, loc, snippet}]
  secondary_effects:
    - effect: string
      mechanism: string
      downstream_surfaces: [string]
      likelihood: low|medium|high
      impact: low|medium|high
  compatibility:
    internal_api: [impact_item]
    behavioral: [impact_item]
  performance:
    compile_time: [impact_item]
    runtime: [impact_item]
  risk:
    level: low|medium|high
    rationale: [string]
  open_questions: [string]
  recommendations: [string]
```

## How to Use

1. **Analyze a specific PR:**
   ```
   Analyze PR 59413 from the compiler PRs
   ```

2. **Batch analysis:**
   ```
   Analyze all JuliaLowering PRs and summarize closure-related changes
   ```

3. **Impact search:**
   ```
   Which PRs might affect OpaqueClosure behavior?
   ```

## Analysis Workflow

For each PR analysis, follow these steps:

### Step 1: Setup Julia repo and checkout PR
```bash
# Clone if needed (shallow clone for speed)
[ ! -d "julia" ] && git clone --depth 100 https://github.com/JuliaLang/julia.git julia

# Fetch and checkout the specific PR
cd julia
git fetch origin pull/60567/merge:pr-60567
git checkout pr-60567
```

### Step 2: Read cached PR metadata
```bash
cat pr-archive/JuliaLang_julia/pr_60567.json
```

### Step 3: Examine FULL code context (not just diff)
This is critical for finding secondary effects:
```bash
# Read complete modified files
cat julia/JuliaLowering/src/closure_conversion.jl

# Find all callers of a modified function
rg "analyze_lambda_vars" julia/

# Trace struct usage across codebase
rg "MethodMatchTarget" julia/Compiler/

# Check test files for expected behavior
cat julia/JuliaLowering/test/closures.jl
```

### Step 4: Write analysis to per-PR output file
```bash
# Output path: analyses/pr_{number}.yaml
# Per-PR files allow parallel analysis without merge conflicts
mkdir -p analyses
# Write YAML analysis to analyses/pr_60567.yaml
```

## Quality Requirements (CRITICAL)

### 1. Include ACTUAL code snippets, not descriptions

**BAD - vague description:**
```yaml
snippet: "analyze_def_and_use! ... mark them as is_always_defined=true"
```

**GOOD - actual code:**
```yaml
snippet: |
  function is_boxed(binfo::BindingInfo)
      defined_but_not_assigned = binfo.is_always_defined && !binfo.is_assigned
      single_assigned_never_undef = binfo.kind in (:local, :argument) &&
                                    binfo.is_always_defined && binfo.is_assigned_once
      return binfo.is_captured && !defined_but_not_assigned && !single_assigned_never_undef
  end
```

### 2. Show concrete before/after examples from tests

Include actual test code that demonstrates behavior changes:
```yaml
snippet: |
  # Assignment after if statement doesn't need Box
  function f_after_if(cond)
      if cond
          println("hello")
      end
      y = 1
      () -> y
  end
  # IR output shows: slots: [... slot₃/y(single_assign)]
  # Instead of Core.Box, uses direct: (new %₇ slot₃/y)
```

### 3. Trace code paths explicitly with call chains

For secondary effects, show the actual function call chain:
```yaml
mechanism: |
  analyze_def_and_use!() sets is_always_defined flag
    -> is_boxed() checks: binfo.is_always_defined && binfo.is_assigned_once
    -> closure_type_fields() uses is_boxed() to decide field types
    -> _opaque_closure handling emits unboxed capture
```

### 4. Include rg search results for callers

When a function is modified, search for all callers:
```bash
$ rg "is_boxed" julia/JuliaLowering/
src/closure_conversion.jl:304:function is_boxed(binfo::BindingInfo)
src/closure_conversion.jl:380:    if is_boxed(binfo)
src/closure_conversion.jl:525:    field_is_box = [is_boxed(b) for b in field_orig_bindings]
```

### 5. Verify claims against actual code

Don't speculate - read the code and quote it:
- If you say "X affects OpaqueClosure", show the specific code path
- If you say "changes IR shape", show actual IR output from tests
- If you say "affects downstream packages", explain which API they use

### 6. NO ellipses (...) in snippets

**BAD:**
```yaml
snippet: |
  function foo()
      ...
      bar()
  end
```

**GOOD:** Show complete, contiguous code blocks:
```yaml
snippet: |
  function foo()
      x = compute()
      bar()
  end
```

### 7. Include diff provenance

Every analysis must include:
```yaml
pr:
  merge_commit_sha: "abc123..."  # Actual commit SHA
  diff_url: "https://github.com/JuliaLang/julia/pull/60567.diff"
```

### 8. Trace call chains with evidence locations

**BAD - assertion without trace:**
```yaml
mechanism: "The new pass sets is_always_defined which affects boxing"
```

**GOOD - explicit call chain with file:line:**
```yaml
mechanism: |
  analyze_def_and_use!(ctx, ex)  [binding_analysis.jl:45]
    sets binfo.is_always_defined = true
  -> is_boxed(binfo)  [closure_conversion.jl:304]
    checks binfo.is_always_defined && binfo.is_assigned_once
  -> closure_type_fields(ctx, ex, binds)  [closure_conversion.jl:525]
    field_is_box = [is_boxed(b) for b in bindings]
  -> K"new_opaque_closure" emission  [closure_conversion.jl:540]
    emits unboxed capture: (new_opaque_closure ... slot₁/y)
```

### 9. Specific API/field names for compatibility

**BAD:**
```yaml
internal_api: "Downstream tooling may need to account for changes"
```

**GOOD:**
```yaml
internal_api:
  - field: "BindingInfo.is_always_defined"
    change: "Now reset to false for arguments, then recomputed by analyze_def_and_use!"
    affected_tools: ["JET (reads binding flags)", "IRTools (inspects closure fields)"]
```

### 10. Quantify or bound performance claims

**BAD:**
```yaml
compile_time: "Slight extra work"
```

**GOOD:**
```yaml
compile_time: |
  O(n) tree walk per lambda body where n = AST nodes
  One additional pass after analyze_variables!, before closure_conversion
  ESTIMATED: <5% increase in lowering time for typical functions
```

Label claims as `ESTIMATED` or `MEASURED` (with benchmark link).

### 11. Add line-linked URLs to evidence

Every evidence item should include a direct GitHub URL to the exact lines:

```yaml
evidence:
  - source: "code"
    path: "JuliaLowering/src/closure_conversion.jl"
    loc: "304-316"
    url: "https://github.com/JuliaLang/julia/blob/8ca9bc66ed/JuliaLowering/src/closure_conversion.jl#L304-L316"
    snippet: |
      function is_boxed(binfo::BindingInfo)
          ...
      end
```

Build URL from: `https://github.com/JuliaLang/julia/blob/{merge_commit_sha}/{path}#L{start}-L{end}`

### 12. Annotate IR snippets to highlight key behavior

In test IR output, add comments showing what to look for:

```yaml
snippet: |
  # IR showing NO Box - direct slot capture:
  slots: [slot₁/#self#(!read) slot₂/cond slot₃/y(single_assign)]  # <-- single_assign = no box
  4   (= slot₃/y 1)
  8   (new %₇ slot₃/y)  # <-- captures slot directly, not Core.Box
```

### 13. Cite actual tooling usage sites

**BAD:**
```yaml
affected_tools: ["JET", "IRTools"]
```

**GOOD:**
```yaml
affected_tools:
  - tool: "JET"
    usage: "JET.jl reads BindingInfo.is_captured in src/abstractinterpret/inferenceerrorreport.jl"
  - tool: "IRTools"
    usage: "IRTools inspects closure field layout in src/reflection/utils.jl"
```

## Key Questions Per PR

1. **Intent:** What does the PR claim to fix/improve?
2. **Stage:** Which compiler stage(s) are touched?
3. **Semantic change:** Could user code behave differently?
4. **Inference:** Does it change lattice operations, tfuncs, or heuristics?
5. **Optimization:** Does it change inlining thresholds, escape analysis, effect inference?
6. **OpaqueClosure / generated functions:** Any changes to closure representation or `@generated`?
7. **World age / invalidation:** Are method tables or caches affected?
8. **Compiler API surface:** Any struct/field changes that break Core.Compiler users?
9. **Non-obvious downstream:** Performance characteristics or allocation behavior changes?
10. **Tests:** What behavior do added tests lock in?

## Pre-Submission Checklist

Before writing the analysis file, verify:

- [ ] Julia repo cloned and PR checked out
- [ ] Read full source files, not just diff
- [ ] All evidence snippets contain ACTUAL code (multi-line with `|`)
- [ ] NO ellipses (...) in any snippet - complete code only
- [ ] At least one concrete before/after example from tests
- [ ] Secondary effects traced with explicit call chains INCLUDING file:line
- [ ] rg search performed for modified functions to find callers
- [ ] Claims about downstream impact backed by specific code paths
- [ ] Line numbers in `loc` fields are accurate and verifiable
- [ ] merge_commit_sha included in PR metadata
- [ ] Compatibility section names specific fields/APIs, not vague warnings
- [ ] Performance claims labeled ESTIMATED or MEASURED
- [ ] Evidence includes line-linked GitHub URLs (blob/{sha}/path#L1-L10)
- [ ] IR snippets annotated with comments showing key behavior
- [ ] Tooling impact cites actual usage sites, not just tool names
- [ ] Output is valid YAML (validate before writing)

## Output Format

Write output as **valid YAML** to `analyses/pr_{number}.yaml`:

```bash
# Validate YAML before writing
python -c "import yaml; yaml.safe_load(open('analyses/pr_60567.yaml'))" && echo "Valid YAML"
```

YAML format requirements:
- Use `|` for multi-line code snippets (preserves newlines and indentation)
- Ensure proper indentation (2 spaces)
- Quote strings containing special characters (`:`, `#`, etc.)

Example multi-line snippet:
```yaml
snippet: |
  function is_boxed(binfo::BindingInfo)
      defined_but_not_assigned = binfo.is_always_defined && !binfo.is_assigned
      return binfo.is_captured && !defined_but_not_assigned
  end
```

