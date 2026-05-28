# {Bounded Context Name}

## Purpose

{Business domain description extracted from module analysis and YAML definitions}

## Modules

| Module | Responsibility |
|--------|----------------|
| {module-name} | {Responsibility inferred from aggregate and field analysis} |

## Key Business Rules

{Rules discovered from code analysis: guards, validators, domain invariants}
- Rule 1: {From guard/validator}
- Rule 2: {From domain constraint}
- Rule 3: {From value object}

## Main Flows

{Flows extracted from command/query handlers}
1. **{Flow Name}**: {Description from handler analysis}
2. **{Flow Name}**: {Description from handler analysis}

## Dependencies

- **Uses**: {Contexts imported by this bounded context}
- **Used by**: {Contexts that import from this bounded context}

## Technical Notes

{Implementation observations from code exploration}
- Aggregate roots: {List}
- Event patterns: {If found}
- Integration points: {External systems}
- Special considerations: {From code analysis}
