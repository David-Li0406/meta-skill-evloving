# Complexity Detection Reference

## Purpose

Determine when to trigger Phase 0 (System Understanding) before feature specification.

---

## Complexity Indicators

### Keyword Detection

| Category | Keywords | Weight |
|----------|----------|--------|
| Architectural | "refactor", "migrate", "redesign", "overhaul" | +3 |
| Integration | "integrate", "connect", "API", "webhook" | +2 |
| Cross-cutting | "auth", "security", "logging", "caching" | +2 |
| Data | "database", "schema", "migration", "model" | +2 |
| Multi-component | "system", "platform", "full-stack" | +2 |
| Simple | "button", "fix", "tweak", "small" | -2 |

**Threshold**: Score ≥ 4 → Trigger Phase 0

---

## Component Count Detection

```python
def estimate_components(user_request: str, codebase_intel: dict) -> int:
    """Estimate number of components affected by feature."""

    # Search for related files
    related_files = project_intel_search(user_request)

    # Group by module/directory
    modules = set()
    for file in related_files:
        module = file.split("/")[0]  # Top-level directory
        modules.add(module)

    # Each unique module = 1 component
    return len(modules)
```

| Component Count | Complexity | Action |
|-----------------|------------|--------|
| ≤ 3 | Simple | Skip Phase 0 |
| 4-6 | Moderate | Optional Phase 0 |
| > 6 | Complex | Required Phase 0 |

---

## File Touch Estimation

```python
def estimate_file_touches(user_request: str) -> int:
    """Estimate files that will be created/modified."""

    # Feature type patterns
    patterns = {
        "new_endpoint": 4,  # route, service, model, test
        "new_model": 3,     # model, repo, migration
        "integration": 6,   # client, service, config, handler, model, test
        "refactor": 8,      # Depends on scope
        "bug_fix": 2,       # Fix file, test file
        "ui_component": 3,  # Component, styles, test
    }

    # Detect feature type from keywords
    for feature_type, count in patterns.items():
        if feature_type_detected(user_request, feature_type):
            return count

    return 5  # Default estimate
```

| File Touch Estimate | Complexity | Action |
|---------------------|------------|--------|
| ≤ 5 | Simple | Skip Phase 0 |
| 6-10 | Moderate | Optional Phase 0 |
| > 10 | Complex | Required Phase 0 |

---

## First Feature Detection

```bash
# Check if this is the first feature in the project
if [ -z "$(ls -d specs/[0-9]* 2>/dev/null)" ]; then
    echo "First feature - Phase 0 recommended"
fi
```

**Rationale**: First feature benefits from codebase understanding to establish patterns.

---

## Explicit Triggers

| User Phrase | Action |
|-------------|--------|
| "analyze system" | Trigger Phase 0 |
| "understand codebase" | Trigger Phase 0 |
| "map architecture" | Trigger Phase 0 |
| "how does X work" | Trigger Phase 0 (focused on X) |
| "show me the structure" | Trigger Phase 0 (overview mode) |

---

## Scoring Algorithm

```python
def calculate_complexity_score(user_request: str, codebase: dict) -> dict:
    """Calculate complexity score and recommendation."""

    score = 0
    reasons = []

    # 1. Keyword scoring
    keyword_score = calculate_keyword_score(user_request)
    score += keyword_score
    if keyword_score >= 3:
        reasons.append(f"Architectural keywords detected (+{keyword_score})")

    # 2. Component count
    component_count = estimate_components(user_request, codebase)
    if component_count > 6:
        score += 3
        reasons.append(f"High component count: {component_count} (+3)")
    elif component_count > 3:
        score += 1
        reasons.append(f"Moderate component count: {component_count} (+1)")

    # 3. File touch estimate
    file_estimate = estimate_file_touches(user_request)
    if file_estimate > 10:
        score += 3
        reasons.append(f"Many files affected: ~{file_estimate} (+3)")
    elif file_estimate > 5:
        score += 1
        reasons.append(f"Moderate files affected: ~{file_estimate} (+1)")

    # 4. First feature bonus
    if is_first_feature():
        score += 2
        reasons.append("First feature in project (+2)")

    # 5. Explicit trigger
    if explicit_analysis_requested(user_request):
        score += 5
        reasons.append("Explicit analysis requested (+5)")

    # Determine action
    if score >= 6:
        action = "REQUIRED"
    elif score >= 4:
        action = "RECOMMENDED"
    else:
        action = "SKIP"

    return {
        "score": score,
        "action": action,
        "reasons": reasons,
        "components": component_count,
        "files": file_estimate
    }
```

---

## Complexity Classification

| Score | Classification | Phase 0 Action |
|-------|----------------|----------------|
| 0-3 | Simple | Skip |
| 4-5 | Moderate | Optional (ask user) |
| 6+ | Complex | Required |

---

## Decision Output

```markdown
## Complexity Assessment

**Feature**: [User request summary]
**Score**: X/15

### Indicators
- [ ] Architectural keywords: {detected/none}
- [ ] Component count: {N} ({simple/moderate/complex})
- [ ] File estimate: ~{N} files
- [ ] First feature: {yes/no}
- [ ] Explicit request: {yes/no}

### Classification: {Simple/Moderate/Complex}

### Recommendation
{SKIP Phase 0 / OPTIONAL Phase 0 / REQUIRED Phase 0}

### Reasons
1. {reason 1}
2. {reason 2}
```

---

## Override Rules

**User can always override:**

| User Says | Action |
|-----------|--------|
| "skip analysis" | Skip Phase 0 regardless of score |
| "analyze first" | Run Phase 0 regardless of score |
| "just do it" | Skip Phase 0, proceed to Phase 3 |

---

## Integration with Phase Routing

```python
def route_feature_request(user_request: str) -> int:
    """Route feature request to appropriate starting phase."""

    complexity = calculate_complexity_score(user_request, get_codebase())

    if complexity["action"] == "REQUIRED":
        return 0  # Phase 0: System Understanding
    elif complexity["action"] == "RECOMMENDED":
        # Ask user
        response = ask_user(
            "This feature appears moderately complex. "
            "Would you like me to analyze the system first?",
            options=["Yes, analyze first", "No, proceed to spec"]
        )
        return 0 if "Yes" in response else 3
    else:
        return 3  # Phase 3: Specification
```

---

## Version

**Version**: 1.0.0
**Last Updated**: 2025-12-30
