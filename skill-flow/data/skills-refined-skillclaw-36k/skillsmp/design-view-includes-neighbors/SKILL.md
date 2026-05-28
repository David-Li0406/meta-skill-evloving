---
name: design-view-includes-neighbors
description: Include neighboring elements in views (callers and dependencies). Show focused element with elements that use it and what it depends on.
---

# Design View: Include Neighboring Elements

Use this skill for focused C2 or C3 views showing interaction context.

**Prerequisite:** Read `design-view-hierarchy` for basic view organization.

## Core Principle

**Focused views MUST show neighboring elements to provide interaction context:**
- Include all elements that have relationships WITH the focused element(s)
- Shows incoming relationships: What calls/uses this?
- Shows outgoing relationships: What does this call/depend on?
- Provides complete interaction context

This ensures every focused view answers: "What uses this? What does it use?"

## Why Show Neighbors?

Without neighboring elements:
- ❌ View shows isolated container/component
- ❌ Unclear how it fits in larger system
- ❌ Missing interaction context

With neighboring elements:
- ✓ View shows focused element + related elements
- ✓ Clear what uses it and what it uses
- ✓ Complete interaction context

## Include Syntax for Relationships

### Include Direct Callers (Incoming)

```likec4
view c3_upload {
  // Add all elements that have relationships TO this component
  include -> vault.uploadService
}
```

### Include Dependencies (Outgoing)

```likec4
view c3_upload {
  // Add all elements that this component depends on
  include vault.uploadService ->
}
```

### Include Related Child Components

```likec4
view c3_upload {
  // Include related nested services/components
  include vault.uploadService.*
  include vault.minio.*  // What it depends on
}
```

## Complete Examples with Neighboring Elements

### Focused C3 View: Upload Service

```likec4
view c3_upload_service {
  title 'C3 / Upload Service'
  
  // What calls this? (incoming)
  include -> vault.uploadService
  
  // Focus: container and its components
  include vault.uploadService.*
  include vault.uploadService
  
  // What does this call? (outgoing)
  include vault.uploadService ->
  
  // Additional context: parent and external actors
  include customer
  include browser
}
```

### Focused C2 View: Upload Subsystem

For a focused C2 view on a specific subsystem:

```likec4
view c2_upload_subsystem {
  title 'C2 / Upload Subsystem'
  
  // Callers: What systems use this?
  include -> vault.uploadService
  include -> vault.jobs
  
  // Focus: main containers in subsystem
  include vault.uploadService
  include vault.jobs
  include vault.minio
  
  // Dependencies: What external systems does this need?
  include vault.uploadService ->
  include vault.minio ->
  
  // Actors for context
  include customer
  include browser
}
```

### Multi-Container C3 View: Processing Workflow

```likec4
view c3_processing_workflow {
  title 'C3 / Async Processing Workflow'
  
  // Show all components in processing containers
  include vault.jobs.*           // Queue components
  include vault.jobs
  include vault.worker.*         // Worker components
  include vault.worker
  include vault.resultNotifier.* // Notification components
  include vault.resultNotifier
  
  // Show what triggers this workflow
  include -> vault.jobs
  
  // Show what this workflow depends on
  include vault.jobs ->
  include vault.worker ->
  include vault.resultNotifier ->
}
```

## Include Patterns Reference

| Pattern | Result | Use Case |
|---------|--------|----------|
| `Element.*` | Element + all nested content (components/properties) | Show component internals |
| `-> Element` | All elements with relationships TO this element | Show callers/consumers |
| `Element ->` | All elements this element has relationships TO | Show dependencies |
| `-> Element ->` | Bidirectional: callers AND dependencies | Show complete interaction |
| `System.*` | System + all direct children (containers) | Show system containers |

## Common Include Patterns

### Pattern 1: Focused Element + Neighbors

```likec4
view c3_validator {
  // Callers
  include -> vault.fileValidator
  
  // Focus
  include vault.fileValidator
  include vault.fileValidator.*
  
  // Dependencies
  include vault.fileValidator ->
}
```

### Pattern 2: Multi-Level Interaction

```likec4
view c3_complex {
  // Incoming: who calls this?
  include -> vault.uploadService
  include browser
  
  // Focus: the component and its internals
  include vault.uploadService.*
  include vault.uploadService
  
  // Outgoing: what does it use?
  include vault.uploadService ->
  
  // Show downstream: what do those dependencies use?
  include vault.minio.*
  include vault.jobs.*
}
```

### Pattern 3: Isolated Focus (No Neighbors)

Sometimes you want NO neighbors (rare):

```likec4
view c3_validator_isolated {
  // Only the component internals, no incoming/outgoing
  include vault.fileValidator
  include vault.fileValidator.*
}
```

## Checking Relationship Context

**Before creating a focused view, ask:**
1. What elements call this container/component?
2. What does this container/component depend on?
3. Should both incoming and outgoing be shown?
4. Should child components be shown?

**Use the answers to structure the view:**
```likec4
view c3_service {
  // Include answers to question 1 (callers)
  include -> vault.uploadService
  
  // Include answer to question 2 (dependencies)
  include vault.uploadService ->
  
  // Include the service itself
  include vault.uploadService
  
  // Include child components if question 4 = yes
  include vault.uploadService.*
}
```

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| Focused view without context | Include -> and -> neighbors | Shows how element fits |
| Show only callers | Show callers AND dependencies | Incomplete interaction picture |
| Nested `include ->` (include -> -> ) | Single direction per statement | Cleaner syntax |
| Mix focused element with unrelated services | Show only related neighbors | Focused view, not full system |

## Related Skills

- `design-view-hierarchy` - Basic view organization and parent context
- `navigate-views` - View-to-view navigation and linking
