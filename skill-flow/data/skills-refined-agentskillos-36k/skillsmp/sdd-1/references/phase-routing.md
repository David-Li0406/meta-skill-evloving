# Phase Routing Reference

## Purpose

Define how user intent maps to SDD phases and how prerequisites are validated.

---

## Intent Detection Patterns

### Pattern Matching Rules

```
Intent_Patterns := {
  foundation: [
    "define product", "/define-product", "product definition",
    "what does this product do", "who are the users"
  ],

  constitution: [
    "constitution", "technical principles", "/generate-constitution",
    "derive principles", "create guidelines"
  ],

  feature: [
    "create feature", "new feature", "build", "I want to",
    "/feature", "add functionality", "implement new"
  ],

  clarify: [
    "clarify", "unclear", "ambiguous", "/clarify",
    "what do you mean", "need more details"
  ],

  planning: [
    "plan", "how to implement", "architecture", "/plan",
    "design", "technical approach"
  ],

  audit: [
    "audit", "validate", "check consistency", "/audit",
    "verify", "review spec"
  ],

  implementation: [
    "implement", "code", "develop", "/implement",
    "start coding", "build it", "make it work"
  ],

  status: [
    "status", "progress", "what's next", "SDD status",
    "where am I", "workflow status", "next step"
  ]
}
```

---

## Detection Algorithm

```python
def detect_intent(user_message: str) -> str:
    """Detect SDD intent from user message."""
    message_lower = user_message.lower()

    # Check each pattern category
    for intent, patterns in Intent_Patterns.items():
        for pattern in patterns:
            if pattern in message_lower:
                return intent

    # No SDD intent detected
    return None

def route_to_phase(intent: str, context: dict) -> int:
    """Route detected intent to appropriate phase."""
    intent_to_phase = {
        "foundation": 1,
        "constitution": 2,
        "feature": 3,  # May trigger 0 first if complex
        "clarify": 4,
        "planning": 5,
        "audit": 7,
        "implementation": 8,
        "status": -1  # Special: report status
    }
    return intent_to_phase.get(intent, -1)
```

---

## Prerequisite Matrix

| Target Phase | Required Artifacts | Missing? Action |
|--------------|-------------------|-----------------|
| 1 (Product) | Repository | N/A - always available |
| 2 (Constitution) | memory/product.md | "Run /define-product first" |
| 3 (Feature) | (optional) product.md, constitution.md | Proceed with warning |
| 4 (Clarify) | spec.md with [NEEDS CLARIFICATION] | "No clarifications needed" |
| 5 (Plan) | spec.md (clarified) | "Run /feature first" |
| 6 (Tasks) | plan.md | Auto-invoked after Phase 5 |
| 7 (Audit) | spec.md, plan.md, tasks.md | "Missing: [list]" |
| 8 (Implement) | audit-report.md with PASS | "Audit failed. Fix: [issues]" |

---

## Prerequisite Check Logic

```python
def check_prerequisites(phase: int, feature_dir: str) -> dict:
    """Check if prerequisites are met for target phase."""
    result = {"pass": True, "missing": [], "message": ""}

    checks = {
        2: [("memory/product.md", "Run /define-product first")],
        4: [("spec.md", "No spec found. Run /feature first")],
        5: [("spec.md", "Run /feature first")],
        7: [
            ("spec.md", "Missing specification"),
            ("plan.md", "Missing plan"),
            ("tasks.md", "Missing tasks")
        ],
        8: [("audit-report.md", "Run /audit first")]
    }

    if phase in checks:
        for file, message in checks[phase]:
            path = f"{feature_dir}/{file}" if "/" not in file else file
            if not exists(path):
                result["pass"] = False
                result["missing"].append(file)
                result["message"] = message

    # Special check for Phase 8: audit must PASS
    if phase == 8 and result["pass"]:
        audit = read_file(f"{feature_dir}/audit-report.md")
        if "Result: **FAIL**" in audit:
            result["pass"] = False
            result["message"] = "Audit failed. Fix issues and re-run /audit"

    # Special check for Phase 4: must have markers
    if phase == 4 and result["pass"]:
        spec = read_file(f"{feature_dir}/spec.md")
        if "[NEEDS CLARIFICATION]" not in spec:
            result["pass"] = False
            result["message"] = "No clarifications needed. Proceed to /plan"

    return result
```

---

## Phase Transitions

### Normal Flow
```
1 → 2 → 3 → 5 → 6 → 7 → 8
              ↓
              4 (if markers present)
              ↓
              5 → ...
```

### Complex Feature Flow
```
User request → Complexity Detection → Phase 0
                                        ↓
                                    3 → 5 → 6 → 7 → 8
```

### Skip Allowed
- Phase 1 (product.md): Can start at Phase 3 without
- Phase 2 (constitution.md): Can start at Phase 3 without
- Phase 4 (clarify): Skipped if no markers

### Skip NOT Allowed
- Phase 5 before Phase 3: Must have spec.md
- Phase 7 before Phase 5: Must have plan.md
- Phase 8 before Phase 7: Must have audit PASS

---

## Auto-Chain Rules

| From Phase | To Phase | Condition |
|------------|----------|-----------|
| 3 (Feature) | 5 (Plan) | spec.md has no [NEEDS CLARIFICATION] |
| 3 (Feature) | 4 (Clarify) | spec.md has [NEEDS CLARIFICATION] |
| 4 (Clarify) | 5 (Plan) | All markers resolved |
| 5 (Plan) | 6 (Tasks) | plan.md complete |
| 6 (Tasks) | 7 (Audit) | tasks.md complete |
| 7 (Audit) | 8 (Implement) | audit PASS (manual trigger) |

---

## Status Report Format

**When intent = "status":**

```markdown
## SDD Workflow Status

**Working Directory**: {cwd}
**Active Feature**: {detected_feature or "None"}

### Artifact Status

| Artifact | Path | Status | Last Modified |
|----------|------|--------|---------------|
| Product Definition | memory/product.md | ✅/❌ | {date} |
| Constitution | memory/constitution.md | ✅/❌ | {date} |
| Specification | specs/$FEATURE/spec.md | ✅/❌ | {date} |
| Plan | specs/$FEATURE/plan.md | ✅/❌ | {date} |
| Tasks | specs/$FEATURE/tasks.md | ✅/❌ | {date} |
| Audit Report | specs/$FEATURE/audit-report.md | ✅/❌ | {date} |

### Current Phase: {phase_number} - {phase_name}

### Next Step
{recommended_action}

### Blockers
{blockers_if_any}
```

---

## Error Messages

| Error Code | Message | Resolution |
|------------|---------|------------|
| E001 | "No spec.md found" | Run /feature first |
| E002 | "Audit failed" | Fix issues in audit-report.md |
| E003 | "[NEEDS CLARIFICATION] markers present" | Run /clarify |
| E004 | "Missing plan.md" | Run /plan |
| E005 | "Missing tasks.md" | Run /tasks |
| E006 | "product.md not found" | Run /define-product (optional) |

---

## Version

**Version**: 1.0.0
**Last Updated**: 2025-12-30
