---
name: analyze-julia-compiler-pr
description: Use this skill when analyzing a Julia compiler PR for downstream impact, secondary effects, and changelog generation.
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
- Semantic vs performance vs diagnostics