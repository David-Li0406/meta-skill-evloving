---
name: use-research
description: Find relevant research and guide implementation based on it. Use when implementing features, fixing bugs, or exploring techniques where existing research in docs/research/ may provide guidance. Trigger phrases include "apply research", "use research", "based on the research", "implement from paper", or "find relevant research for [task]".
---

# Use Research Knowledge

Apply knowledge from research documents in `docs/research/` to guide implementation of current tasks.

## Workflow

### Phase 1: Discovery

Find research documents relevant to the current task.

1. **List available research**
   ```
   Glob: docs/research/*.md
   ```

2. **Quick scan each document** by reading the title (first H1) and overview/abstract section to build an index of available research:

   | Document | Topic |
   |----------|-------|
   | `type-inference.md` | HM type inference, Algorithm W/J/M, unification |
   | `grokking-the-sequent-calculus.md` | λμμ̃-calculus, producers/consumers, IR design |
   | `malgo.md`, `anma.md` | Related language implementations |
   | `thesis_2024.md` | Project background and design decisions |
   | etc. | |

3. **Match to current task** by identifying keywords:
   - Type system tasks → `type-inference.md`, `ziku-type-inference-design.md`
   - IR/evaluation tasks → `grokking-the-sequent-calculus.md`
   - Parser/syntax tasks → `arrow-syntax-alternatives.md`
   - Testing tasks → `golden-test.md`, `lake-test.md`

4. **If no relevant research exists**:
   - Inform user no prior research was found for this task
   - Ask if they want to proceed without research or run `/research` first
   - If proceeding, consider creating research doc post-implementation

### Phase 2: Analysis

Deep-read the relevant research document(s).

1. **Read the full document**
   ```
   Read: docs/research/<relevant-doc>.md
   ```

2. **Extract key sections**:
   - **Key Contributions / Features** - What this research provides
   - **Implementation Details** - Code patterns, algorithms, data structures
   - **Core Concepts** - Definitions and terminology
   - **Examples** - Code snippets showing usage

3. **Identify applicable patterns**:
   - Translation rules (e.g., Surface → IR mappings)
   - Evaluation rules (e.g., μ/μ̃-reduction)
   - Type rules (e.g., inference algorithms)
   - Design patterns (e.g., data/codata duality)

### Phase 3: Application

Apply research patterns to the current task.

1. **Map concepts to codebase**:
   ```
   Research Concept → Ziku Implementation
   ──────────────────────────────────────
   Producer         → Ziku/IR/Syntax.lean (Producer type)
   Consumer         → Ziku/IR/Syntax.lean (Consumer type)
   μ-reduction      → Ziku/IR/Eval.lean (eval function)
   Translation ⟦−⟧  → Ziku/Translate.lean
   Type inference   → Ziku/Infer.lean
   ```

2. **Provide implementation guidance**:
   - Reference specific research sections for context
   - Show how patterns translate to Lean 4 code
   - Note any adaptations needed for Ziku's design

3. **Cite sources** when referencing research:
   - Link to specific sections in research docs
   - Quote relevant rules or definitions

## Example Usage

### Task: "Implement let-polymorphism"

**Discovery**: Match "polymorphism" → `type-inference.md`

**Analysis**: From `docs/research/type-inference.md`:
- Section "Let-Polymorphism" explains the restriction
- Section "Key Operations" covers `gen()` and `inst()`
- Code pattern:
  ```
  W(Γ, let x = e₁ in e₂) =
    let (S₁, τ₁) = W(Γ, e₁)
        σ = gen(S₁(Γ), τ₁)
        (S₂, τ₂) = W(S₁(Γ)[x↦σ], e₂)
    in (S₂ ∘ S₁, τ₂)
  ```

**Application**: Apply to `Ziku/Infer.lean`:
- Implement `generalize` function
- Add `Scheme` type for polymorphic types
- Update `infer` for `let_` case

### Task: "Add label/goto control flow"

**Discovery**: Match "label", "goto", "control" → `grokking-the-sequent-calculus.md`

**Analysis**: From `docs/research/grokking-the-sequent-calculus.md`:
- Section "Translation from Fun to Core" shows:
  ```
  ⟦label α {t}⟧  = μα.⟨⟦t⟧ | α⟩
  ⟦goto(t; α)⟧   = μβ.⟨⟦t⟧ | α⟩  (β fresh)
  ```
- Section "Key Insights" explains let/label duality

**Application**: Apply to `Ziku/Translate.lean`:
- Add `label` case using `Producer.mu`
- Add `goto` case with fresh continuation

## Tips

- Research documents contain both theory and implementation details
- The "Implementation" or "Implementation in Ziku" sections are most directly applicable
- Cross-reference multiple research docs when tasks span areas
- The "Sources" section in each doc links to original papers for deeper understanding
- If implementation diverges from research, note why and consider updating the research doc
