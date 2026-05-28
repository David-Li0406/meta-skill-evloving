---
name: design-view-hierarchy
description: Design views with proper parent context and neighboring elements. Include C1/C2/C3 hierarchy, include patterns, and view organization into folders.
---

# Design View Hierarchy

Use this skill when creating or modifying visualization views in system-model.c4.

**Prerequisite:** Read `design-view-includes-neighbors` for advanced include patterns.

## Core Principles

### 1. Always Include Parent/Surrounding Context

**Every view MUST explicitly include the parent/surrounding element for context:**

| View Type | Shows | Must Include |
|-----------|-------|------------------|
| C3 Component | Internal modules | Parent Container |
| C2 Container | System building blocks | Parent System |
| C1 Context | System in landscape | External Systems |

This ensures every view answers: "What is this IN? What surrounds it?"

### 2. Use Shared Spec for Elements & Styling

**When designing views, always prefer shared specification:**
- Use element kinds defined in `shared/spec-*.c4`
- Use colors defined in `shared/spec-global.c4`
- Don't create custom kinds, colors, or styles in view-specific files
- If something is needed:
  1. Check shared spec first
  2. Ask permission from user
  3. Contribute to shared spec instead
  4. Then use the spec definition

This ensures consistency and maintainability across all views and projects.

## View Organization Hierarchy

**Organize views into subfolders using the `views 'FolderName'` syntax:**

```likec4
// Root views (no subfolder) - architectural hierarchy
views {
  view c1_context { ... }      // System context with actors
  view c2_internals { ... }    // System internals and containers
  view c3_upload_service { ... } // Component deep-dives
  view c3_retrieval_service { ... }
}
```

### Root Folder: C1 Context View

Shows system boundary and external actors/systems:

```likec4
views {
  view c1_context {
    title 'C1 / System Name'
    include customer
    include browser
    include vault
    include externalService
  }
}
```

**✓ MUST include system boundary** - Always show what is INSIDE vs. OUTSIDE the system.

### Root Folder: C2 Containers View (Single "Internals" Overview)

Overview of all major containers/services inside a system:

```likec4
views {
  view c2_internals {
    title 'C2 / System Internals'
    include customer
    include browser
    include vault.*          // All containers
    include externalService
  }
}
```

**✓ TYPICALLY ONE VIEW per system** - Shows all containers together as "System Internals"  
**✓ MUST include system for container context** - Always show containers WITHIN the system boundary

### Root Folder: Multiple C3 Component Deep-Dives

Internal modules within specific containers (one view per major service):

```likec4
views {
  view c3_upload_service {
    title 'C3 / Upload Service'
    include vault.uploadService.*    // Components inside container
    include vault.uploadService      // Container itself
    include customer                 // Parent system actors
    include browser
    include vault.minio.*            // Related services
    include externalService
  }
  
  view c3_retrieval_service {
    title 'C3 / Retrieval Service'
    include vault.retrievalService.*
    include vault.retrievalService
    include customer
    include browser
    include vault.minio.*
    include externalService
  }
}
```

**Naming pattern:**
- View ID: `c3_<service_name>` → Title: `C3 / <Service Name>`
- Examples: `c3_upload_service` → "C3 / Upload Service"

**✓ MUST include parent container for context** - Always show container boundary with components inside

### Index View (MANDATORY)

Entry point for architecture exploration:

```likec4
views {
  view index extends c1_context {
    title 'Architecture Overview'
    description 'Navigate to detailed views for deeper exploration'
  }
}
```

**✓ MUST extend c1_context** - Inherits system context by default

## Include Patterns

### Basic Pattern: Focus + Parent

```likec4
view c3_service {
  // Focus: the container and its components
  include vault.uploadService.*
  include vault.uploadService
}
```

### Parent + Focus + Neighbors

```likec4
view c3_upload {
  include customer
  include vault.uploadService.*
  include vault.uploadService
  include vault.minio.*
}
```

### Showing Relationships (Next Skill)

For advanced include patterns showing callers and dependencies, see `design-view-includes-neighbors`.

## File Organization Best Practice

```
project/
  system-model.c4           # ← Elements, containers, components
  system-views.c4           # ← views { } → C1, C2, C3 hierarchy
  system-sequences.c4       # ← views 'Use Cases' { } → workflows
  deployment.c4             # ← Deployment nodes and VMs
  deployment-views.c4       # ← views 'Deployment' { } → infrastructure
  operations.c4             # ← Operations infrastructure
  operations-views.c4       # ← views 'Operations' { } → monitoring/DR
```

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| C3 view without parent container | Always include parent container | Provides context |
| C2 view without system | Always include system | Shows system boundary |
| C1 view missing external systems | Include all external integrations | Complete ecosystem view |
| Multiple C2 views per system | One C2 overview per system | Simplifies navigation |
| Custom colors/shapes in view | Use shared spec definitions | Maintains consistency |

## Related Skills

- `design-view-includes-neighbors` - Advanced include patterns (callers, dependencies, relationships)
- `navigate-views` - View-to-view navigation and linking
