# Quality Assurance

## Confidence Check (before each phase)

| Phase | Questions |
|-------|-----------|
| Pre-Spec | Problem validated? Market gap? Target audience? |
| Pre-Design | Requirements clear? AC testable? No contradictions? |
| Pre-Task | Architecture decided? No duplicates? Dependencies mapped? |
| Pre-Impl | Task clear? Approach decided? No blockers? |

**Threshold:** ≥90% proceed, 70-89% clarify, <70% stop

## Hallucination Prevention (before marking done)

1. Tests passing? → Show actual output
2. Requirements met? → List each with evidence
3. No assumptions? → Show documentation
4. Evidence exists? → Provide test results, code changes

## Reflexion Learning (after completion)

- Success → Store pattern in `~/.sdd/memory/patterns_learned.jsonl`
- Failure → Store error + solution in `~/.sdd/memory/mistakes_learned.jsonl`
