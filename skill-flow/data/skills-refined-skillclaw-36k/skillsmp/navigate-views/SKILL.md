---
name: navigate-views
description: View-to-view navigation (navigateTo, drill-down), external links, and view metadata. Preserves parent context.
---

# Navigate Views

Use this skill for view-to-view navigation, external links, and view metadata.

**Prerequisite:** Read `style-view-elements` first for basic styling.

## Core Principle: Preserve Context

When designing navigation:
- Never hide parent container/system/zone boundaries
- Never exclude outer context when drilling down
- Use navigation to add detail, not to isolate
- Parent context helps users understand relationships

## View-to-View Navigation

Enable drill-down from parent to child view:

```likec4
view systemOverview {
  title "System Overview"
  include *
  
  // Clicking on backend opens backendDetails view
  include cloud.backend with {
    navigateTo backendDetails
  }
}

view backendDetails of cloud.backend {
  title "Backend Details"
  include *
  include cloud.backend.api with { navigateTo apiServices }
}

view apiServices of cloud.backend.api {
  title "API Microservices"
  include *
}
```

**Pattern:** Context → Container → Component (drill-down hierarchy)

## Navigation Use Cases

### Drill-Down (Hierarchical)
```likec4
view systemView {
  include *
  include system with { navigateTo containerView }
}

view containerView of system {
  include *
  include system.api with { navigateTo componentView }
}

view componentView of system.api {
  include *
}
```

### Hub & Spoke (Central Index)
```likec4
view architectureIndex {
  title "Architecture Index"
  include *
  include system.api with { navigateTo apiServices }
  include system.storage with { navigateTo dataArchitecture }
  include system.worker with { navigateTo asyncProcessing }
}

view apiServices {
  title "API Services"
  include *
}

view dataArchitecture {
  title "Data Architecture"
  include *
}

view asyncProcessing {
  title "Async Processing"
  include *
}
```

### Related Views
```likec4
view deployment {
  title "Deployment Architecture"
  include deployment.*
}

view operations {
  title "Operations & Monitoring"
  include deployment.monitoring.*
  include deployment.logging.*
}
```

## External Documentation Links

Link to external resources (JIRA, documentation, specifications):

```likec4
view epic12 {
  title "System Changes - Epic 12"
  
  description """
    Implementation details.
    See linked resources.
  """
  
  link https://my.jira/epic/12 'Epic-12'
  link https://docs.internal/spec 'Specification'
  link https://github.com/org/repo/issues/42 'GitHub Issue'
  
  include *
}
```

**Format:** `link {URL} '{DisplayText}'`
- URLs must be HTTPS
- Display text should be descriptive
- Use markdown links in descriptions too

## View Metadata

Add metadata to views for organization and filtering:

```likec4
view myView {
  title "Clear, Descriptive Title"
  
  description """
    This view shows:
    - **Component A**: Handles requests
    - **Component B**: Processes data
    - **Component C**: Stores results
    
    See [deployment guide](https://docs.internal/deploy).
  """
  
  // Tags for filtering/searching
  #production, #deployment, #critical
  
  include *
}
```

## View Organization with Folders

Group related views into folders:

```likec4
views 'Architecture' {
  view contextView { ... }
  view containerView { ... }
}

views 'Deployment' {
  view productionDeploy { ... }
  view stagingDeploy { ... }
}

views 'Operations' {
  view monitoring { ... }
  view scaling { ... }
}
```

## Navigation Checklist

- [ ] Navigation targets reference valid view IDs
- [ ] Drill-down maintains parent context
- [ ] Hub & spoke index has clear central view
- [ ] Related views use meaningful names
- [ ] External links use HTTPS with descriptive text
- [ ] View titles are unique and descriptive

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| navigateTo nonexistent view | Target valid existing view | Navigation must work |
| Exclude parent container in child view | Include parent context | Users need orientation |
| Unclear view titles | "System Architecture" or "Backend Microservices" | Users must understand purpose |
| Dead links in descriptions | Verify all links work | Broken docs undermine credibility |

## Related Skills

- `style-view-elements` - Styling and coloring views
- `design-view` - Basic view includes and excludes
