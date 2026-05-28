---
name: complexity-analysis
description: Use this skill when evaluating complexity in projects, planning features, or addressing concerns about over-engineering and simplicity.
---

# Skill body

## When to Use
- Planning features or architecture
- Choosing frameworks, libraries, or patterns
- Evaluating proposed solutions
- Detecting premature optimization or abstraction
- Making build vs buy decisions

**NOT for:** trivial tasks, clear requirements with validated complexity, or regulatory/compliance-mandated approaches.

## Phases
Track with TodoWrite when applying the framework to non-trivial proposals:

| Phase      | Trigger                       | activeForm                        |
|------------|-------------------------------|-----------------------------------|
| Identify   | Complexity smell detected     | "Identifying complexity smell"    |
| Alternative| Generating simpler options     | "Proposing simpler alternatives"  |
| Question   | Probing constraints           | "Questioning constraints"         |
| Document   | Recording decision            | "Documenting decision"            |

### TodoWrite format:
```text
- Identify { complexity type } smell
- Propose alternatives to { specific approach }
- Question { constraint/requirement }
- Document { decision/rationale }
```

## Workflow
- **Start:** Create Identify `in_progress` when a smell is detected.
- **Transition:** Mark current `completed`, add next `in_progress`.
- **Skip to Document** if complexity is validated immediately.
- **Optional phases:** Skip Alternative if obvious, skip Question if constraints are clear.

## Escalation
Adjust tone based on severity:

◇ **Alternative** (Minor complexity):
> "Interesting approach. Help me understand why X over the more common Y?"

◆ **Caution** (Moderate risk):
> "This pattern often leads to [specific problems]. Are we solving for something I'm not seeing?"

◆◆ **Hazard** (High risk):
> "This violates [principle] and will likely cause [specific issues]. I strongly recommend [alternative]. If we must proceed, we need to document the reasoning."

## Triggers
Common complexity smells to watch for:

**Build vs Buy:** Custom solution when proven libraries exist
- Custom auth system → Auth0, Clerk, BetterAuth
- Custom validation → Zod, Valibot, ArkType
- Custom state management → Zustand, Jotai, Nanostores
- Custom form handling → React Hook Form, Formik

**Indirect Solutions:** Solving problem A by first solving problems B, C, D
- Compiling TS→JS then using JS → Use TS directly in the build tool.