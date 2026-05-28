---
name: pke-query
description: "PKE (Promethean Knowledge Engine) query patterns and memory framework integration. Use for: (1) Structured knowledge retrieval, (2) Context package assembly, (3) Course spec lookups, (4) Terminology and formatting rules, (5) Semantic anchoring. Triggers: PKE, knowledge engine, memory, context, retrieval, query, lookup, course spec, terminology."
---

# PKE Query Skill

## Purpose

Define query patterns and integration approaches for the Promethean Knowledge Engine (PKE). This skill prepares the framework for PKE implementation and establishes patterns for knowledge retrieval operations.

**Current Status:** PKE is PLACEHOLDER - `core/pke/__init__.py` not yet implemented.

This skill documents the intended architecture and query patterns to guide implementation.

## PKE in the Memory Framework

### Memory Layer 3

PKE operates at **Layer 3** of the Prometheus Memory Framework:

```
Layer 1: Constitution & Architecture (Immutable Authority)
Layer 2: Context Packages (Task-specific anchoring)
Layer 3: PKE Retrieval (Structured long-term knowledge)  ← THIS LAYER
Layer 4: Logs & Trace History (Temporal grounding)
Layer 5: Local State (Ephemeral)
```

### PKE Responsibilities

PKE provides:
- Structured course specifications
- Lesson templates
- Terminology rules
- Formatting models
- Institutional knowledge
- Semantic anchors

### PKE Constraints

- **PKE is NOT autonomous** - It only retrieves and aligns information
- **All logic remains governed by Sarah and the Orchestrator**
- **PKE does not make decisions** - It surfaces knowledge for decision-makers

## Query Types

### 1. Course Specification Query

**Purpose:** Retrieve full course structure

```python
# Proposed API
response = pke.query(
    type="course_spec",
    course_id="COURSE-001",
    include=["clos", "topics", "lessons", "prerequisites"]
)

# Response structure
{
    "course": {
        "id": "COURSE-001",
        "title": "Security Operations",
        "duration_hours": 40,
        "level": "Intermediate"
    },
    "clos": [...],
    "topics": [...],
    "lessons": [...]
}
```

### 2. Terminology Query

**Purpose:** Retrieve approved terminology for a domain

```python
response = pke.query(
    type="terminology",
    domain="security",
    context="training_material"
)

# Response structure
{
    "terms": [
        {
            "term": "operational security",
            "definition": "...",
            "abbreviation": "OPSEC",
            "usage_context": "...",
            "avoid_terms": ["op sec", "ops security"]
        }
    ]
}
```

### 3. Template Query

**Purpose:** Retrieve document templates

```python
response = pke.query(
    type="template",
    template_type="lesson_plan",
    format="docx"
)

# Response structure
{
    "template_id": "LP-001",
    "template_path": "core/templates/docx/lesson_plan_template.docx",
    "placeholders": ["{{COURSE_TITLE}}", "{{LESSON_REF}}", ...],
    "styling_rules": {...}
}
```

### 4. Formatting Rules Query

**Purpose:** Retrieve formatting standards for output type

```python
response = pke.query(
    type="formatting_rules",
    output_type="presentation",
    audience="trainees"
)

# Response structure
{
    "fonts": {
        "title": {"family": "Candara", "size": "36pt"},
        "body": {"family": "Candara", "size": "20pt"}
    },
    "colors": {
        "accent": "#FF6600",
        "text": "#333333"
    },
    "guidelines": [
        "6x6 rule: max 6 bullets, 6 words per bullet",
        "One idea per slide"
    ]
}
```

### 5. Bloom's Taxonomy Query

**Purpose:** Validate or suggest verbs for cognitive levels

```python
response = pke.query(
    type="blooms_taxonomy",
    cognitive_level=4,  # Analyse
    context="learning_objective"
)

# Response structure
{
    "level": 4,
    "level_name": "Analyse",
    "definition": "Break material into constituent parts and determine relationships",
    "valid_verbs": ["analyse", "compare", "contrast", "differentiate", ...],
    "invalid_verbs": ["know", "understand", "appreciate"],
    "assessment_methods": ["case studies", "data analysis tasks"]
}
```

### 6. Prior Decision Query

**Purpose:** Retrieve relevant architectural or design decisions

```python
response = pke.query(
    type="prior_decision",
    topic="ui_coordinate_system",
    component="navigation"
)

# Response structure
{
    "decisions": [
        {
            "id": "DEC-UI-001",
            "date": "2025-12-17",
            "topic": "Implementation Viewport Baseline",
            "decision": "1890×940 pixels",
            "rationale": "Founder's display configuration",
            "authority": "Matthew",
            "reference": "UI_DOCTRINE.md"
        }
    ]
}
```

### 7. Semantic Anchor Query

**Purpose:** Ground concepts in authoritative definitions

```python
response = pke.query(
    type="semantic_anchor",
    concept="SAT",
    depth="full"
)

# Response structure
{
    "concept": "SAT",
    "full_name": "Systems Approach to Training",
    "definition": "A systematic methodology for designing, developing, and delivering training",
    "components": ["Analysis", "Design", "Development", "Implementation", "Evaluation"],
    "related_concepts": ["ADDIE", "ISD"],
    "prometheus_usage": "Core methodology for courseware generation"
}
```

## Context Package Integration

PKE queries are assembled into **Context Packages** for task execution:

```yaml
# Context Package Schema
task_id: "TASK-2025-001"
task_description: "Generate lesson plan for Security Operations 1.1.1.A"

pke_queries:
  - type: course_spec
    course_id: COURSE-001
  - type: template
    template_type: lesson_plan
  - type: formatting_rules
    output_type: document
  - type: blooms_taxonomy
    cognitive_level: 3

contextual_documents:
  - prometheus-constitution.md
  - sat-courseware/SKILL.md

constraints:
  - "Bloom's verb validation required"
  - "Duration must match course spec"

acceptance_criteria:
  - "Lesson plan generated in DOCX format"
  - "All placeholders populated"
  - "Speaker notes included"
```

## Implementation Patterns

### Query Interface (Proposed)

```python
# core/pke/query.py

class PKEQuery:
    """PKE Query Interface"""

    def __init__(self, knowledge_base_path: str):
        self.kb = self._load_knowledge_base(knowledge_base_path)

    def query(self, query_type: str, **params) -> dict:
        """Execute a PKE query"""
        handler = self._get_handler(query_type)
        return handler(**params)

    def _get_handler(self, query_type: str):
        handlers = {
            "course_spec": self._query_course_spec,
            "terminology": self._query_terminology,
            "template": self._query_template,
            "formatting_rules": self._query_formatting_rules,
            "blooms_taxonomy": self._query_blooms,
            "prior_decision": self._query_decisions,
            "semantic_anchor": self._query_anchors
        }
        return handlers.get(query_type, self._unknown_query)

    def _query_course_spec(self, course_id: str, include: list = None) -> dict:
        """Retrieve course specification"""
        # Implementation TBD
        pass

    def _query_blooms(self, cognitive_level: int, context: str = None) -> dict:
        """Retrieve Bloom's taxonomy guidance"""
        # Can leverage sat-courseware/references/blooms-taxonomy.md
        pass
```

### Knowledge Base Structure (Proposed)

```
core/pke/
├── __init__.py
├── query.py              # Query interface
├── knowledge_base/
│   ├── courses/          # Course specifications
│   │   └── COURSE-001.json
│   ├── terminology/      # Domain terminology
│   │   └── security.json
│   ├── templates/        # Template metadata
│   │   └── templates.json
│   ├── decisions/        # Prior decisions
│   │   └── decisions.json
│   └── anchors/          # Semantic anchors
│       └── anchors.json
└── validators/
    └── blooms_validator.py
```

## Integration with Other Skills

### With /sat-courseware
- PKE provides Bloom's taxonomy data
- SAT skill validates CLO structure
- PKE stores validated course specs

### With /docx-gen and /pptx-gen
- PKE provides template metadata
- PKE provides formatting rules
- Generation skills apply the rules

### With /prometheus-testing
- PKE queries can be tested for correctness
- Integration tests verify PKE responses

## Validation Rules

### Query Validation

Before PKE returns data:
1. Verify query type is supported
2. Validate required parameters present
3. Check data freshness (if applicable)
4. Apply access controls (if implemented)

### Response Validation

Before returning to caller:
1. Ensure response matches expected schema
2. Flag any missing optional fields
3. Include metadata (query_time, source_version)

## Error Handling

```python
class PKEError(Exception):
    """Base PKE error"""
    pass

class PKEQueryNotFound(PKEError):
    """Query type not supported"""
    pass

class PKEDataNotFound(PKEError):
    """Requested data not in knowledge base"""
    pass

class PKEValidationError(PKEError):
    """Response failed validation"""
    pass
```

## Usage in Claude Code

When CC needs PKE data (once implemented):

```python
# Example: Generating a lesson plan
from core.pke import PKEQuery

pke = PKEQuery("core/pke/knowledge_base")

# Get course spec
course = pke.query("course_spec", course_id="COURSE-001")

# Get Bloom's guidance for CLO level
blooms = pke.query("blooms_taxonomy", cognitive_level=course["clos"][0]["cognitive_level"])

# Get template
template = pke.query("template", template_type="lesson_plan")

# Generate using /docx-gen patterns
generate_lesson_plan(course, blooms, template)
```

## Implementation Priority

| Component | Priority | Dependencies |
|-----------|----------|--------------|
| Query interface | HIGH | None |
| Bloom's taxonomy queries | HIGH | sat-courseware data |
| Course spec storage | HIGH | Course JSON schema |
| Template metadata | MEDIUM | docx-gen, pptx-gen |
| Terminology database | MEDIUM | Domain knowledge |
| Prior decisions store | LOW | Governance docs |
| Semantic anchors | LOW | Constitution, Architecture |

## See Also

- `docs/memory-framework.md` - Full memory architecture
- `/sat-courseware` - SAT methodology and Bloom's data
- `/docx-gen`, `/pptx-gen` - Document generation consumers
- `docs/prometheus-constitution.md` - Governance principles
