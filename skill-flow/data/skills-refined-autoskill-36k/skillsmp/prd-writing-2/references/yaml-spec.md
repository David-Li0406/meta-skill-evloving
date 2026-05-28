# For-AI YAML Specification

This file contains the complete YAML schema for the For-AI section of PRDs.

## Table of Contents

1. [Complete YAML Template](#complete-yaml-template)
2. [AI Instructions Block](#ai-instructions-block)
3. [Field Reference](#field-reference)

---

## Complete YAML Template

Replace the outline with this complete section in Phase 3:

```markdown
## For AI

> Machine-readable specification. High information density.
> Developers: paste this section to AI assistants for precise answers.

<ai_instructions>
You are reading a structured PRD specification. Follow these rules:

1. **Answer from spec**: Use the YAML data below to answer questions precisely. Cite specific fields (e.g., "per business_rules.RULE-001").

2. **Identify gaps**: If a question cannot be answered from the spec, say:
   "This is not specified in the PRD. You should clarify with the PM:
   - [specific question to ask]"

3. **Flag ambiguity**: If the spec is ambiguous or contradictory, say:
   "The PRD is unclear on this point:
   - [what's ambiguous]
   - Possible interpretations: A) ... B) ...
   - Recommend clarifying with PM before implementing."

4. **Check open_questions**: Before answering, check `notes.open_questions`. If the user's question relates to an open item, mention it.

5. **Respect scope**: If asked about something in `scope.out_of_scope`, remind the user it's explicitly excluded.

6. **Implementation guidance**: When asked "how to implement X":
   - Reference `system.architecture` for system design
   - Reference `system.apis` for interface contracts
   - Reference `business_rules` for logic
   - Reference `requirements.non_functional` for constraints
</ai_instructions>
```

---

## YAML Schema

```yaml
meta:
  feature_name: "feature-name"
  summary: "One sentence summary"
  status: draft | review | approved
  prd_version: "1.0"
  last_updated: "YYYY-MM-DD"

context:
  problem: "Precise problem statement"
  solution: "Solution approach"
  success_criteria:
    - metric: "metric name"
      target: "target value"
      measurement: "how to measure"

scope:
  systems_affected:
    - system: "system-name"
      impact: "what changes"
  out_of_scope:
    - "item"

user_flows:
  happy_path:
    - step: 1
      actor: "user | system"
      action: "what happens"
      result: "outcome"
  error_paths:
    - trigger: "error condition"
      behavior: "system response"
      user_message: "what user sees"

system:
  architecture: |
    [ASCII diagram or description]
    Client -> API Gateway -> Auth Service -> DB

  entities:
    - name: "EntityName"
      description: "what this entity represents"
      fields:
        - name: "field_name"
          type: "string | int | boolean | datetime | etc"
          required: true | false
          constraints: "validation rules"

  apis:
    - endpoint: "METHOD /path"
      description: "what this does"
      auth: "required | optional | none"
      input:
        field_name:
          type: "type"
          required: true | false
          validation: "rules"
      output:
        success:
          status: 200
          body:
            field: "type"
        errors:
          - status: 400
            code: "ERROR_CODE"
            message: "Error message"

  business_rules:
    - id: "RULE-001"
      name: "Rule Name"
      condition: "when this happens"
      action: "do this"
      exceptions: "unless..."

  requirements:
    functional:
      - id: "FR-001"
        description: "requirement"
        acceptance: "verification method"
        priority: "must | should | could"
    non_functional:
      - id: "NFR-001"
        type: "performance | security | reliability | scalability"
        description: "requirement"
        target: "measurable target"

notes:
  dependencies:
    - name: "dependency"
      type: "service | library | team"
      purpose: "why needed"
      owner: "who owns it"
  compliance:
    - "requirement"
  risks:
    - description: "risk"
      probability: "low | medium | high"
      impact: "low | medium | high"
      mitigation: "how to address"
  assumptions:
    - "assumption"
  timeline:
    - milestone: "milestone name"
      hard_deadline: true | false
      date: "YYYY-MM-DD or null"
  known_issues:
    - "issue"
  open_questions:
    - question: "question"
      owner: "who should answer"
      blocking: true | false
```

---

## Field Reference

### meta
| Field | Required | Description |
|-------|----------|-------------|
| feature_name | Yes | Lowercase with hyphens, e.g., "user-login" |
| summary | Yes | One sentence description |
| status | Yes | draft, review, or approved |
| prd_version | Yes | Semantic version, e.g., "1.0" |
| last_updated | Yes | ISO date format YYYY-MM-DD |

### context
| Field | Required | Description |
|-------|----------|-------------|
| problem | Yes | Clear problem statement |
| solution | Yes | High-level solution approach |
| success_criteria | Yes | Array of measurable metrics |

### scope
| Field | Required | Description |
|-------|----------|-------------|
| systems_affected | Yes | Systems that will be modified |
| out_of_scope | No | Explicitly excluded items |

### user_flows
| Field | Required | Description |
|-------|----------|-------------|
| happy_path | Yes | Primary success scenario steps |
| error_paths | No | Error scenarios and handling |

### system.entities
| Field | Required | Description |
|-------|----------|-------------|
| name | Yes | Entity name (PascalCase) |
| description | Yes | What this entity represents |
| fields | Yes | Array of field definitions |

### system.apis
| Field | Required | Description |
|-------|----------|-------------|
| endpoint | Yes | "METHOD /path" format |
| description | Yes | What the endpoint does |
| auth | Yes | required, optional, or none |
| input | No | Request parameters/body |
| output | Yes | Success and error responses |

### system.business_rules
| Field | Required | Description |
|-------|----------|-------------|
| id | Yes | Unique identifier, e.g., "RULE-001" |
| name | Yes | Human-readable name |
| condition | Yes | When this rule applies |
| action | Yes | What happens |
| exceptions | No | When rule doesn't apply |

### system.requirements
| Field | Required | Description |
|-------|----------|-------------|
| functional | Yes | Array of functional requirements |
| non_functional | No | Array of NFRs (performance, security, etc.) |

### notes
All fields in `notes` are optional. Include only what's relevant.
