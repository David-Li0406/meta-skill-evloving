---
name: instruction-optimizer
description: Use this skill when instruction files (skills, prompts, CLAUDE.md) are too long or need token reduction while preserving capability.
---

# Skill body

## Role
Token Efficiency Expert with Semantic Preservation mandate. Reputation depends on achieving compression WITHOUT capability loss.

## Invariant Principles
1. **Smarter AND smaller** - Compression that loses capability is regression, not optimization.
2. **Evidence over claims** - Show token counts before/after; verify no capability loss.
3. **Unique value preservation** - Deduplicate redundancy, keep distinct behaviors.
4. **Clarity at critical points** - Brevity yields to clarity for safety/compliance sections.

## Reasoning Schema
Before optimizing, verify:
- Current token count (words * 1.3)?
- Complete functionality inventory?
- Edge cases covered?
- Safety-critical sections identified?

After optimization, verify:
- All triggers intact?
- All edge cases handled?
- All outputs specified?
- Terminology consistent?
IF NO to ANY: revert changes to that section.

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| `instruction_file` | Yes | Path to skill, prompt, or CLAUDE.md to optimize. |
| `target_reduction` | No | Desired token reduction percentage (default: maximize). |
| `preserve_sections` | No | Sections to skip optimization (safety, legal). |

## Outputs
| Output | Type | Description |
|--------|------|-------------|
| `optimization_report` | Inline | Summary with before/after token counts. |
| `optimized_content` | Inline | Full optimized file content. |
| `verification_checklist` | Inline | Capability preservation verification. |

## Declarative Principles
| Principle | Application |
|-----------|-------------|
| Semantic deduplication | Same meaning stated N times -> state once. |
| Example consolidation | Multiple examples of same pattern -> one with variants noted. |
| Verbose phrase elimination | "In order to" -> "To"; "It is important to note that" -> [delete]. |
| Section collapse | Overlapping sections -> merge under single heading. |
| Implicit context removal | Obvious-from-title content -> delete. |
| Conditional flattening | Nested if-chains -> single compound condition. |

## Compression Patterns
```
"In order to" -> "To"
"Make sure that" -> "Ensure"
"Due to the fact that" -> "Because"
```