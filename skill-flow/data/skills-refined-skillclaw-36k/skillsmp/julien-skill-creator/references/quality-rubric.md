# Quality Assessment Rubric

Score each dimension from 1-5, then calculate average.

## Scoring Table

| Dimension | 1 (Poor) | 3 (Good) | 5 (Excellent) |
|-----------|----------|----------|---------------|
| **Clarity** | Vague, ambiguous instructions | Clear workflow, some details missing | Crystal clear, no ambiguity |
| **Completeness** | Missing critical steps/resources | Covers main use cases | Handles edge cases, errors |
| **Discoverability** | Hard to know when to use skill | Description mentions key scenarios | Name + description trigger appropriately |
| **Context Efficiency** | Bloated SKILL.md (>500 lines) | Reasonable length, some verbosity | Lean SKILL.md (<500 lines), refs for details |
| **Actionability** | Theoretical, no concrete steps | Step-by-step workflow provided | Checklist-style, copy-paste ready |
| **Resource Organization** | Missing bundled resources or all in SKILL.md | Good separation scripts/refs/assets | Optimal progressive disclosure |
| **Examples** | No examples or only abstract ones | 1-2 concrete examples | Multiple examples covering scenarios |
| **Skill Chaining** | No relationship to other skills documented | Mentions related skills | Full Input/Output/Dependencies documented |
| **Error Handling** | No guidance on failures | Basic troubleshooting | Comprehensive error scenarios |

## Score Interpretation

- **1.0-2.4**: Skill needs major rework before use
- **2.5-3.4**: Functional but significant improvements needed
- **3.5-4.4**: Good skill, minor refinements recommended
- **4.5-5.0**: Excellent skill, ready for production

## Example Iteration Plan

After initial assessment showing:
- Clarity: 4/5
- Completeness: 3/5 (missing error handling)
- Discoverability: 2/5 (poor description)
- Context Efficiency: 4/5
- Actionability: 3/5 (lacks checklists)
- Resource Organization: 5/5
- Examples: 2/5 (no concrete examples)
- Skill Chaining: 1/5 (not documented)
- Error Handling: 2/5 (minimal)
- **Average: 2.9/5** (Functional but needs improvement)

### Iteration 1 - Critical Fix: Discoverability (2/5 → 5/5)
- **Problem**: Description too generic
- **Fix**: Rewrite to be specific with triggers and use cases
- **Result**: Score improved to 5/5

### Iteration 2 - High Impact: Skill Chaining (1/5 → 5/5)
- **Problem**: No documentation of relationships
- **Fix**: Add comprehensive Skill Chaining section
- **Result**: Score improved to 5/5

### Iteration 3 - Medium Impact: Examples (2/5 → 4/5)
- **Problem**: Only abstract descriptions
- **Fix**: Add 3 real-world examples with exact commands
- **Result**: Score improved to 4/5

### Iteration 4 - Medium Impact: Error Handling (2/5 → 4/5)
- **Problem**: Missing error scenarios
- **Fix**: Add Troubleshooting section
- **Result**: Score improved to 4/5

## Common Improvement Areas by Iteration

**First iteration typically addresses:**
- Discoverability (name/description triggers)
- Critical missing steps

**Second iteration typically addresses:**
- Skill chaining documentation
- Resource organization

**Third iteration typically addresses:**
- Concrete examples
- Error handling

**Fourth+ iterations address:**
- Edge cases
- Performance optimizations
- Polish
