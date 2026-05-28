---
name: customize-view
description: Advanced view features: styling (colors, shapes, style predicates), layout control (autoLayout, rank hints), and navigation (navigateTo, links).
---

# Customize View

Use this skill for advanced view features: styling, layout, and navigation.

## Core Principles

### 1. Prefer Shared Spec Over Custom Styling

**Before customizing colors, shapes, or styles:**
1. **Check shared spec first** - Use specs from `shared/spec-*.c4` files
2. **Use defined colors** - Refer to `spec-global.c4` color definitions
3. **Avoid custom colors** - Don't create new hex colors for styling
4. **Avoid custom shapes** - Use kinds from shared spec, not custom shape definitions
5. **If needed, ask & contribute** - If styling really needs something new:
   - Ask user permission first
   - Suggest adding it to shared spec
   - Contribute to spec instead of one-off customization
   - This keeps styling consistent across all projects

**Why:** Shared specs ensure consistency, maintainability, and avoid proliferation of custom styles.

### 2. Respect Parent Context

When customizing views, always preserve the parent/surrounding element context:
- Never hide parent container/system/zone boundaries
- Never exclude the outer context when styling inner elements
- Use styling to emphasize, not to isolate elements from their context
- Apply opacity changes carefully to avoid losing context

## View Organization

For folder organization of views, use the `views 'FolderName'` syntax:

```likec4
views 'Deployment' {
  view my_view { ... }
}
```

See the **design-view** skill for full organization patterns and parent context requirements.

## Visual Styling

**IMPORTANT:** Use colors and shapes from shared spec (`shared/spec-*.c4`), not custom definitions.

### Available Colors (From Shared Spec)

Use only colors defined in `shared/spec-global.c4`:
- `primary` - Primary brand color
- `secondary` - Secondary color
- `success` - Success/positive state
- `warning` - Warning state
- `danger` - Error/danger state
- `muted` - Muted/inactive
- (Check spec-global.c4 for complete list)

**DO NOT:** Create new hex color definitions. If you need a color not in the spec:
1. Check `spec-global.c4` first
2. If missing, ask permission and contribute to shared spec
3. Then use the spec color

### Available Shapes (From Element Kinds)

Shapes come from element kinds defined in `spec-*.c4` files:
- Each kind has a predefined shape (box, cylinder, etc.)
- Use the kind's shape, don't override with custom shapes

**DO NOT:** Define custom shapes. If a shape is needed:
1. Check if a kind exists with that shape
2. If not, contribute new kind to shared spec
3. Then use that kind

### View-Level Style Overrides (Shared Spec Only)

```likec4
view myView {
  include cloud.backend with {
    title 'Backend Services'
    color primary              // From shared spec
    shape database             // From kind definition
    icon tech:java
  }
}
```

### Style Predicates (Shared Spec Colors Only)

```likec4
view apiView {
  include *
  
  style * { color muted; opacity 10% }           // spec-global color
  style api.*, gateway.* { color primary; opacity 100% }  // spec-global color
  style element.tag = #deprecated { color muted }         // spec-global color
  style element.tag != #production { color secondary }    // spec-global color
}
```

### Global Style Groups

```likec4
global {
  styleGroup theme_production {
    style * { color primary }
    style element.tag = #external { color muted }
  }
}

views {
  global style theme_production
  
  view myView {
    include *
  }
}
```

**Style Properties:**  
Elements: color, shape, icon, opacity, border, size, textSize, multiple  
Colors: primary, secondary, muted, amber, gray, green, indigo, red  
Shapes: rectangle, storage, cylinder, browser, mobile, person, queue, bucket, document  
Icons: tech:*, aws:*, gcp:*, azure:*

## Layout Control

### Auto-Layout Direction

```likec4
view layered {
  include *
  autoLayout TopBottom  // or LeftRight
}
```

### Rank Hints

```likec4
view requestFlow {
  include *
  
  include client with { rank source }           // Entry point
  include service1, service2 with { rank same } // Parallel
  include database with { rank sink }           // Endpoint
  
  autoLayout TopBottom
}
```

### Directed Includes

```likec4
view dataFlow {
  include frontend, backend, database
  include frontend -> backend ->  // Direction hints
  include -> database
  
  autoLayout LeftRight
}
```

### Common Layout Patterns

**Layered (TopBottom):**
```likec4
view layered {
  include *
  include presentation.* with { rank source }
  include data.* with { rank sink }
  autoLayout TopBottom
}
```

**Request Flow (LeftRight):**
```likec4
view flow {
  include *
  include client with { rank source }
  include external.* with { rank sink }
  autoLayout LeftRight
}
```

**Load Balanced:**
```likec4
view balanced {
  include *
  include loadBalancer with { rank source }
  include backend1, backend2, backend3 with { rank same }
  include database with { rank sink }
  autoLayout TopBottom
}
```

### Layout Troubleshooting

- **Overlapping elements:** Add rank hints to separate layers
- **Wrong flow direction:** Use directed includes or change autoLayout
- **Elements spread out:** Group related elements with `rank same`

## Navigation

### View-to-View Navigation

```likec4
view systemOverview {
  include *
  
  include cloud.backend with {
    navigateTo backendDetails
  }
}

view backendDetails of cloud.backend {
  include *
}
```

### Navigation Patterns

**Drill-down:** Context → Container → Component (navigateTo on parent elements)
```likec4
view contextView {
  include *
  include cloud with { navigateTo cloudContainers }
}

view cloudContainers of cloud {
  include *
  include cloud.backend with { navigateTo backendComponents }
}
```

**Hub-spoke:** Central index with links to specialized views
```likec4
view index {
  title "Architecture Index"
  include *
  include cloud.api with { navigateTo apiServices }
  include cloud.storage with { navigateTo dataArchitecture }
}
```

### External Documentation Links

```likec4
view epic12 {
  title "System Changes - Epic 12"
  
  description """
    Implementation details.
    See linked resources.
  """
  
  link https://my.jira/epic/12 'Epic-12'
  link https://docs.internal/spec 'Specification'
  
  include *
}
```

### View Metadata

```likec4
view myView {
  title "Clear, Descriptive Title"
  
  description """
    This view shows:
    - **Component A**: Handles requests
    - **Component B**: Processes data
    
    See [deployment guide](https://docs.internal/deploy).
  """
  
  #production, #deployment
  
  include *
}
```

## Validation

- [ ] Style predicates use `element.tag = #name` syntax
- [ ] AutoLayout direction matches flow (TopBottom for layers, LeftRight for sequences)
- [ ] Source rank = entry points, Sink rank = endpoints
- [ ] No conflicting rank hints (can't be both source and sink)
- [ ] Navigation targets reference valid view IDs
- [ ] External links use HTTPS with descriptive text
- [ ] View titles unique and descriptive

**MCP:** Use `open-view` to preview layout and navigation interactively

**Context7:** Query `/likec4/likec4` for syntax validation if uncertain

## Output

Polished views with appropriate styling, logical layout, and clear navigation paths.
