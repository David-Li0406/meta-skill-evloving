---
name: skill-improvement
description: Propose PR-style improvements to advisor skills based on session feedback. Use at end of advisor flow or when friction/corrections occur.
---

# Skill Improvement PR Suggestor (Learning Loop)

Propose PR-style improvements to the skill set based on interaction evidence.

## Triggers

- End of stack selection and planning flow
- Repeated friction or corrections during process
- User provides feedback on skill effectiveness
- Gap in skill coverage identified

## Evidence Types

| Type | Description |
|------|-------------|
| **User Corrections** | Times user corrected an output |
| **Missing Information** | Questions skill couldn't answer |
| **Process Friction** | Steps that took too long |
| **Outdated Content** | Pricing/services that changed |
| **User Feedback** | Explicit feedback provided |

## Improvement Categories

| Category | Description | Priority |
|----------|-------------|----------|
| **Bug Fix** | Incorrect output | High |
| **Enhancement** | Could do more/better | Medium |
| **New Content** | Missing info/options | Medium |
| **Clarification** | Instructions unclear | Low |
| **Deprecation** | No longer relevant | Low |

## Output Contract

```yaml
pr_suggestions:
  session_id: "<session id>"
  generated_at: "<ISO timestamp>"

  suggestions:
    - id: "<PR-XXX>"
      title: "<short title>"
      type: "<bug_fix|enhancement|new_content|clarification|deprecation>"
      priority: "<high|medium|low>"

      motivation: |
        <Why is this change needed?>

      evidence:
        - type: "<evidence type>"
          description: "<what happened>"
          context: "<session context>"

      affected_skills:
        - skill: "<skill name>"
          file: "<file path>"

      proposed_changes:
        - file: "<file path>"
          section: "<section>"
          change_type: "<add|modify|remove>"
          current: |
            <current content>
          proposed: |
            <proposed content>
          rationale: "<why>"

      acceptance_criteria:
        - "<how to verify>"

      breaking_changes: false
```

## Example: Missing Cloud Provider

```yaml
- id: "PR-001"
  title: "Add DigitalOcean as cloud provider option"
  type: "new_content"
  priority: "medium"

  motivation: |
    User asked about DigitalOcean App Platform but skill
    doesn't include it as candidate or have cost evaluator.

  evidence:
    - type: "missing_info"
      description: "User requested DigitalOcean evaluation"

  affected_skills:
    - skill: "stack-evaluation"
      file: ".claude/skills/advisor/stack-evaluation/SKILL.md"

  proposed_changes:
    - file: ".claude/skills/advisor/stack-evaluation/cost-evaluators/digitalocean.md"
      change_type: "add"
      proposed: |
        # DigitalOcean Cost Evaluator
        ...
```

## Example: Outdated Pricing

```yaml
- id: "PR-002"
  title: "Update Vercel Pro pricing"
  type: "bug_fix"
  priority: "high"

  motivation: |
    Vercel pricing changed, current info is incorrect.

  evidence:
    - type: "outdated"
      description: "User corrected pricing"

  proposed_changes:
    - file: ".claude/skills/advisor/stack-evaluation/cost-evaluators/vercel.md"
      section: "Pro Tier"
      change_type: "modify"
      current: "Pro tier cost"
      proposed: "Pro: $20/user/month (verify at vercel.com/pricing)"
```

## Presentation Format

---

## Suggested Skill Improvements

Based on this session, I've identified **X** improvements:

### High Priority

#### PR-001: [Title]
**Type**: [Type] | **Affects**: [Skill]

[Brief description]

**Proposed**: [Summary of change]

---

### Would you like me to:
1. Generate detailed PR descriptions?
2. Create draft changes?
3. Prioritize differently?

---

## Metrics to Track

- User corrections per session
- Time to complete full flow
- Custom combination usage frequency
- Questions that couldn't be answered
