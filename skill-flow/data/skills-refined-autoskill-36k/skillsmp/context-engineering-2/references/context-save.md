# Context Save

Intelligent context capture, serialization, and preservation for cross-session continuity.

## Overview

Context Save captures comprehensive project state for:
- Multi-session collaboration continuity
- Agent workflow handoffs
- Knowledge preservation and transfer
- Audit trails and decision tracking

## Context Types

| Type          | Captured Content                      | Size   |
| ------------- | ------------------------------------- | ------ |
| Minimal       | Project name, current task, blockers  | ~500   |
| Standard      | + Decisions, files modified, progress | ~2000  |
| Comprehensive | + Full context, rationale, history    | ~5000+ |

## Context Extraction

```python
def extract_project_context(project_root, context_type='standard'):
    """Extract context with semantic awareness."""
    context = {
        'project_metadata': extract_project_metadata(project_root),
        'architectural_decisions': analyze_architecture(project_root),
        'dependency_graph': build_dependency_graph(project_root),
        'semantic_tags': generate_semantic_tags(project_root),
        'files_modified': get_recent_modifications(project_root),
        'current_state': summarize_current_state()
    }

    if context_type == 'minimal':
        return filter_minimal(context)
    elif context_type == 'comprehensive':
        context['full_history'] = get_conversation_history()
        context['decision_rationale'] = extract_rationales()

    return context
```

## Context Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "project_name": {"type": "string"},
    "version": {"type": "string"},
    "context_fingerprint": {"type": "string"},
    "captured_at": {"type": "string", "format": "date-time"},
    "session_intent": {
      "type": "object",
      "properties": {
        "original_goal": {"type": "string"},
        "current_objective": {"type": "string"}
      }
    },
    "files_modified": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "path": {"type": "string"},
          "changes": {"type": "string"},
          "impact": {"type": "string"}
        }
      }
    },
    "architectural_decisions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "decision_type": {"type": "string"},
          "rationale": {"type": "string"},
          "alternatives_considered": {"type": "array"},
          "impact_score": {"type": "number"}
        }
      }
    },
    "current_state": {
      "type": "object",
      "properties": {
        "progress": {"type": "string"},
        "blockers": {"type": "array"},
        "next_steps": {"type": "array"}
      }
    }
  }
}
```

## Anchored Iterative Summary Template

```markdown
## Session Intent
Original goal: [preserved from session start]
Current objective: [updated each save]

## Files Modified
- `path/to/file.ts`: [what changed]
- `path/to/other.ts`: [what changed]

## Decisions Made
- **[Decision]**: [rationale] (alternatives: [list])

## Current State
[Progress summary]

## Blockers
- [Active blockers if any]

## Next Steps
1. [Immediate next action]
2. [Following action]
```

## Compression Strategies

```python
def compress_context(context, compression_level='standard'):
    """Compress context while preserving critical information."""
    strategies = {
        'minimal': remove_redundant_tokens,
        'standard': semantic_compression,
        'comprehensive': advanced_vector_compression
    }
    compressor = strategies.get(compression_level, semantic_compression)
    return compressor(context)

def semantic_compression(context):
    """Preserve semantics, reduce tokens."""
    compressed = {
        'intent': context['session_intent'],
        'artifacts': summarize_files(context['files_modified']),
        'decisions': extract_key_decisions(context['architectural_decisions']),
        'state': context['current_state']['progress'],
        'next': context['current_state']['next_steps'][:3]
    }
    return compressed
```

## Vector Database Integration

```python
def save_to_vector_store(context, project_id):
    """Store context with semantic embeddings."""
    # Generate embedding for the context
    embedding = embed_context(context)

    # Store with metadata
    vector_store.upsert({
        'id': generate_context_id(project_id, context['captured_at']),
        'embedding': embedding,
        'metadata': {
            'project': project_id,
            'timestamp': context['captured_at'],
            'type': context.get('context_type', 'standard'),
            'fingerprint': context['context_fingerprint']
        },
        'content': serialize_context(context)
    })
```

## Storage Formats

| Format           | Pros                        | Cons                  |
| ---------------- | --------------------------- | --------------------- |
| JSON             | Portable, readable          | Verbose               |
| Markdown         | Human-readable, git-friendly| Less structured       |
| Protocol Buffers | Compact, typed              | Requires schema       |
| MessagePack      | Fast, compact               | Binary, less readable |

## Workflow: Project Onboarding

1. Analyze project structure
2. Extract architectural decisions
3. Generate semantic embeddings
4. Store in vector database
5. Create markdown summary

## Guidelines

1. Save context at natural breakpoints (task completion, decisions)
2. Use anchored iterative format for continuity
3. Preserve explicit artifact tracking (file list)
4. Include decision rationale for future reference
5. Generate fingerprint for change detection
6. Compress for storage, expand for retrieval
7. Version contexts for rollback capability

## Related

- [Context Restore](./context-restore.md)
- [Context Compression](./context-compression.md)
- [Memory Systems](./memory-systems.md)
