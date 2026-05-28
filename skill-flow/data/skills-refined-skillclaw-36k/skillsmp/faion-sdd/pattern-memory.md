---
id: pattern-memory
name: "Pattern Memory"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Pattern Memory

## Overview

Pattern Memory is the SDD system for capturing, storing, and retrieving successful patterns learned during development. It creates an evolving knowledge base that improves over time, enabling consistent application of proven solutions and faster problem-solving.

## When to Use

- Documenting successful solutions for reuse
- Finding applicable patterns for current tasks
- Building team knowledge base
- Onboarding new developers
- Standardizing best practices
- Improving consistency across codebase

## Process/Steps

### 1. Pattern Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Pattern Memory System                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Capture   │ →  │   Storage   │ →  │  Retrieval  │    │
│  │   Layer     │    │   Layer     │    │   Layer     │    │
│  └─────────────┘    └─────────────┘    └─────────────┘    │
│        │                  │                  │             │
│        ▼                  ▼                  ▼             │
│  Pattern         patterns_learned      Query by:          │
│  Recognition     .jsonl               - Category          │
│  & Extraction                         - Context           │
│                                       - Similarity        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Storage Location:**
```
~/.sdd/memory/
├── patterns_learned.jsonl       # Main pattern storage
├── patterns_index.json          # Quick lookup index
├── patterns_archive/            # Historical versions
│   └── patterns_2024_01.jsonl
└── patterns_stats.json          # Usage analytics
```

### 2. Pattern Schema

**Full Pattern Record:**
```json
{
  "id": "PAT_2024_001",
  "version": 1,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T15:45:00Z",

  "metadata": {
    "category": "coding",
    "subcategory": "error-handling",
    "language": "typescript",
    "framework": "react",
    "tags": ["async", "error-boundary", "user-experience"]
  },

  "pattern": {
    "name": "Async Operation Error Boundary",
    "summary": "Graceful error handling for async operations with user feedback",

    "problem": {
      "description": "Async operations can fail, causing poor UX or app crashes",
      "symptoms": [
        "Unhandled promise rejections",
        "Blank screens on errors",
        "No user feedback on failures"
      ],
      "contexts": [
        "API calls in React components",
        "Data fetching with useEffect",
        "Form submissions"
      ]
    },

    "solution": {
      "description": "Wrap async operations with try-catch and manage error/loading states",
      "approach": [
        "Create error and loading state variables",
        "Wrap async code in try-catch-finally",
        "Set loading true before, false in finally",
        "Set error in catch block",
        "Display appropriate UI for each state"
      ],
      "code_example": "function useAsyncOperation<T>(asyncFn: () => Promise<T>) {\n  const [data, setData] = useState<T | null>(null);\n  const [error, setError] = useState<Error | null>(null);\n  const [loading, setLoading] = useState(false);\n\n  const execute = useCallback(async () => {\n    try {\n      setLoading(true);\n      setError(null);\n      const result = await asyncFn();\n      setData(result);\n      return result;\n    } catch (e) {\n      setError(e instanceof Error ? e : new Error(String(e)));\n      throw e;\n    } finally {\n      setLoading(false);\n    }\n  }, [asyncFn]);\n\n  return { data, error, loading, execute };\n}"
    },

    "benefits": [
      "Prevents unhandled errors",
      "Provides user feedback",
      "Enables graceful degradation",
      "Simplifies debugging"
    ],

    "trade_offs": [
      "Additional state management",
      "Need to design error UI",
      "Slight code overhead"
    ],

    "related_patterns": ["PAT_2024_015", "PAT_2024_022"],
    "supersedes": null,
    "superseded_by": null
  },

  "validation": {
    "confidence": 0.92,
    "usage_count": 15,
    "success_rate": 0.93,
    "last_used": "2024-01-20T14:30:00Z",
    "failure_notes": [
      "Less effective for SSR hydration errors"
    ]
  },

  "provenance": {
    "discovered_in": "TASK_042",
    "verified_in": ["TASK_055", "TASK_067", "TASK_089"],
    "contributors": ["claude-agent", "human-review"],
    "sources": [
      "https://react.dev/reference/react/use"
    ]
  }
}
```

### 3. Pattern Categories

**Category Taxonomy:**
```yaml
pattern_categories:
  coding:
    error_handling:
      - exception_patterns
      - fallback_strategies
      - retry_mechanisms

    data_management:
      - state_management
      - caching_patterns
      - data_transformation

    api_design:
      - endpoint_structure
      - response_formats
      - versioning

    testing:
      - unit_test_patterns
      - mock_strategies
      - test_data_management

  architecture:
    structural:
      - component_organization
      - module_boundaries
      - layer_separation

    behavioral:
      - event_handling
      - pub_sub_patterns
      - command_patterns

    integration:
      - api_integration
      - service_communication
      - data_sync

  process:
    planning:
      - estimation_techniques
      - decomposition_strategies
      - risk_assessment

    execution:
      - implementation_order
      - debugging_approaches
      - review_practices

    communication:
      - documentation_patterns
      - handoff_practices
      - escalation_protocols

  devops:
    ci_cd:
      - pipeline_patterns
      - deployment_strategies
      - rollback_procedures

    monitoring:
      - logging_patterns
      - alerting_strategies
      - debugging_in_production

    infrastructure:
      - scaling_patterns
      - resource_management
      - security_practices
```

### 4. Pattern Capture

**Capture Triggers:**
```yaml
capture_triggers:
  explicit:
    - "User marks solution as pattern"
    - "Code review identifies reusable solution"
    - "Retrospective highlights best practice"

  implicit:
    - "Similar solution used 3+ times"
    - "Solution resolves recurring issue"
    - "High-quality code review feedback"

  ai_detected:
    - "Agent recognizes successful pattern"
    - "Similarity to existing patterns detected"
    - "Performance/quality metrics exceeded"
```

**Capture Process:**
```python
def capture_pattern(task_id: str, solution: dict) -> Pattern:
    """Capture a new pattern from successful task execution"""

    # 1. Extract pattern components
    pattern = Pattern(
        id=generate_pattern_id(),
        metadata=extract_metadata(solution),
        problem=identify_problem(task_id),
        solution=document_solution(solution),
        provenance=create_provenance(task_id)
    )

    # 2. Check for duplicates/similar
    similar = find_similar_patterns(pattern)
    if similar:
        return merge_or_link_patterns(pattern, similar)

    # 3. Initial validation
    pattern.validation = ValidationData(
        confidence=0.5,  # Start at medium confidence
        usage_count=1,
        success_rate=1.0,
        last_used=datetime.now()
    )

    # 4. Store pattern
    store_pattern(pattern)

    # 5. Update index
    update_pattern_index(pattern)

    return pattern
```

### 5. Pattern Retrieval

**Query Interface:**
```python
def query_patterns(
    category: str = None,
    tags: List[str] = None,
    context: str = None,
    min_confidence: float = 0.7,
    limit: int = 5
) -> List[Pattern]:
    """Query patterns matching criteria"""

    patterns = load_patterns()

    # Filter by category
    if category:
        patterns = [p for p in patterns
                   if p.metadata.category == category]

    # Filter by tags
    if tags:
        patterns = [p for p in patterns
                   if any(t in p.metadata.tags for t in tags)]

    # Filter by confidence
    patterns = [p for p in patterns
               if p.validation.confidence >= min_confidence]

    # Rank by relevance
    if context:
        patterns = rank_by_context_similarity(patterns, context)
    else:
        patterns = rank_by_usage_and_confidence(patterns)

    return patterns[:limit]
```

**Context-Based Retrieval:**
```python
def get_patterns_for_task(task: Task) -> List[Pattern]:
    """Get relevant patterns for a task"""

    # Extract task characteristics
    task_type = task.metadata.type
    tech_stack = task.metadata.technologies
    domain = task.metadata.domain
    problem_keywords = extract_keywords(task.description)

    # Query patterns
    patterns = query_patterns(
        category=map_task_type_to_category(task_type),
        tags=tech_stack + [domain],
        context=task.description,
        min_confidence=0.6
    )

    # Also check for problem-specific patterns
    problem_patterns = find_patterns_by_problem(problem_keywords)
    patterns.extend(problem_patterns)

    # Deduplicate and rank
    unique_patterns = deduplicate(patterns)
    ranked = rank_by_relevance(unique_patterns, task)

    return ranked[:5]
```

### 6. Pattern Validation

**Validation Workflow:**
```yaml
validation_workflow:
  initial_capture:
    confidence: 0.5
    requirements:
      - "Successful in original context"
      - "Basic documentation"

  early_validation:
    confidence: 0.6-0.7
    requirements:
      - "Used successfully 2-3 times"
      - "Works in similar contexts"
      - "No critical failures"

  established:
    confidence: 0.8-0.9
    requirements:
      - "Used successfully 5+ times"
      - "Verified across different contexts"
      - "Documented trade-offs"
      - "Peer reviewed"

  proven:
    confidence: 0.9+
    requirements:
      - "Used successfully 10+ times"
      - "Adopted as team standard"
      - "Full documentation"
      - "Training material available"
```

**Confidence Update Logic:**
```python
def update_pattern_validation(pattern: Pattern, usage_outcome: str):
    """Update pattern validation based on usage outcome"""

    v = pattern.validation

    # Update usage count
    v.usage_count += 1
    v.last_used = datetime.now()

    # Update success rate
    if usage_outcome == "success":
        v.success_rate = (v.success_rate * (v.usage_count - 1) + 1) / v.usage_count
        v.confidence = min(0.95, v.confidence + 0.03)
    elif usage_outcome == "partial":
        v.success_rate = (v.success_rate * (v.usage_count - 1) + 0.5) / v.usage_count
        v.confidence = v.confidence * 0.98
    elif usage_outcome == "failure":
        v.success_rate = (v.success_rate * (v.usage_count - 1)) / v.usage_count
        v.confidence = max(0.3, v.confidence - 0.1)
        v.failure_notes.append(f"Failed on {datetime.now()}: {get_failure_context()}")

    # Apply recency weighting
    days_since_validated = (datetime.now() - v.last_successful_use).days
    if days_since_validated > 90:
        v.confidence *= 0.95  # Decay old patterns

    return pattern
```

### 7. Pattern Maintenance

**Maintenance Tasks:**
```yaml
maintenance_schedule:
  daily:
    - "Capture new patterns from completed tasks"
    - "Update validation metrics"

  weekly:
    - "Review low-confidence patterns"
    - "Merge similar patterns"
    - "Archive unused patterns"

  monthly:
    - "Full pattern review"
    - "Update documentation"
    - "Sync with team standards"
    - "Generate usage reports"

  quarterly:
    - "Comprehensive audit"
    - "Retire obsolete patterns"
    - "Identify gaps"
    - "Training material updates"
```

**Pattern Lifecycle:**
```
Draft → Active → Established → Proven → Deprecated → Archived
  │        │          │           │          │
  │        │          │           │          └── Kept for reference
  │        │          │           └── Replaced by better pattern
  │        │          └── Widely adopted
  │        └── Validated multiple times
  └── Initial capture
```

## Best Practices

### Pattern Quality
1. **Specific but generalizable** - Clear context, broad applicability
2. **Complete documentation** - Problem, solution, trade-offs
3. **Working examples** - Real code, not just theory
4. **Known limitations** - When NOT to use

### Memory Management
1. **Regular cleanup** - Archive unused patterns
2. **Merge duplicates** - Avoid fragmentation
3. **Version control** - Track pattern evolution
4. **Index optimization** - Fast retrieval

### Team Integration
1. **Shared ownership** - Everyone can contribute
2. **Review process** - Quality control for patterns
3. **Documentation** - Patterns in team wiki
4. **Training** - Onboard with key patterns

## Templates/Examples

### Quick Pattern Capture

```markdown
## New Pattern: [Name]

**Category:** [coding|architecture|process|devops] / [subcategory]
**Tags:** [tag1, tag2, tag3]

**Problem:**
[What problem does this solve?]

**Solution:**
[Brief description of the approach]

**Code Example:**
```[language]
[Minimal working example]
```

**When to Use:**
- [Context 1]
- [Context 2]

**When NOT to Use:**
- [Anti-context 1]

**Discovered In:** TASK_XXX
```

### Pattern Usage Report

```yaml
pattern_usage_report:
  period: "2024-01"

  most_used:
    - id: PAT_2024_001
      name: "Async Error Boundary"
      usage_count: 15
      success_rate: 93%

    - id: PAT_2024_015
      name: "API Response Normalization"
      usage_count: 12
      success_rate: 100%

  newly_established:
    - id: PAT_2024_042
      name: "Form Validation Pattern"
      confidence_increase: 0.5 → 0.8

  needs_attention:
    - id: PAT_2024_008
      name: "Legacy Cache Pattern"
      reason: "3 failures this month"
      action: "Review and update or deprecate"

  gap_analysis:
    missing_patterns:
      - "Database transaction handling"
      - "File upload chunking"
```

## References

- [reflexion-learning: Reflexion Learning](./reflexion-learning_reflexion_learning.md)
- [mistake-memory: Mistake Memory](./mistake-memory_mistake_memory.md)
- [Design Patterns (GoF)](https://www.oreilly.com/library/view/design-patterns-elements/0201633612/)
- [Patterns of Enterprise Application Architecture](https://martinfowler.com/eaaCatalog/)
