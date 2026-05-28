---
name: style-view-elements
description: Color, shape, and icon styling for views using shared spec definitions and style predicates. No custom colors or shapes.
---

# Style View Elements

Use this skill for styling views with colors, shapes, and icons from shared specifications.

**Prerequisite:** Read `design-view` first for basic view organization.

## Core Principle: Shared Spec Only

**IMPORTANT:** Use colors and shapes from shared spec, never create custom styles.

### Shared Spec Sources

All styling comes from `shared/spec-*.c4` files:
- **Colors** → Defined in `shared/spec-global.c4`
- **Shapes** → Derived from element kinds in spec files
- **Icons** → Tech providers in spec files

**If styling needs something not in spec:**
1. Check shared spec first
2. Ask permission to contribute
3. Add to shared spec
4. Then use the shared definition

## Available Colors

Use only colors defined in `shared/spec-global.c4`:
- `primary` - Primary brand color
- `secondary` - Secondary color  
- `success` - Success/positive state
- `warning` - Warning state
- `danger` - Error/danger state
- `muted` - Muted/inactive state

**Query shared spec to see the full list:**
```likec4
// In spec-global.c4, you'll find:
const color_primary = #2563EB
const color_secondary = #7C3AED
const color_success = #10B981
const color_warning = #F59E0B
const color_danger = #EF4444
const color_muted = #9CA3AF
```

## Available Shapes

Shapes come from element kinds defined in spec:
- `rectangle` - Standard box
- `storage` - Database symbol
- `cylinder` - Storage/cache
- `browser` - Web interface
- `mobile` - Mobile app
- `person` - User/actor
- `queue` - Message queue
- `bucket` - Object storage
- `document` - File/document

**DO NOT** define custom shapes. Use available kinds or contribute new ones to spec.

## View-Level Style Overrides

Override styles for specific elements:

```likec4
view myView {
  include cloud.backend with {
    title 'Backend Services'
    color primary              // From shared spec
    shape database             // From kind definition
    icon tech:java
  }
  
  include cloud.cache with {
    color secondary
    icon tech:redis
  }
}
```

## Style Predicates

Use predicates to apply styles to groups of elements:

### By Tag
```likec4
view apiView {
  include *
  
  // Muted deprecated services
  style element.tag = #deprecated { 
    color muted
    opacity 50%
  }
  
  // Highlight production services
  style element.tag = #production { 
    color primary
    opacity 100%
  }
}
```

### By Kind
```likec4
view architectureView {
  include *
  
  // Dim all databases
  style element.kind = 'database' {
    color secondary
  }
  
  // Highlight API gateways
  style element.kind = 'api-gateway' {
    color success
  }
}
```

### By Name Pattern
```likec4
view systemView {
  include *
  
  // Dim external services
  style external.* {
    color muted
    opacity 70%
  }
  
  // Highlight core domain
  style core.* {
    color primary
  }
}
```

### Exclude Elements
```likec4
view focusedView {
  include *
  
  // Dim everything except focus area
  style * { 
    color muted
    opacity 30%
  }
  
  // Highlight focus area
  style focus.* {
    color primary
    opacity 100%
  }
}
```

## Global Style Groups

Define reusable style groups:

```likec4
global {
  styleGroup theme_production {
    style * { color primary }
    style element.tag = #external { color muted }
    style element.tag = #deprecated { opacity 50% }
  }
  
  styleGroup theme_development {
    style * { color secondary }
    style element.tag = #wip { color warning }
  }
}

views {
  view prodOverview {
    global style theme_production
    include *
  }
  
  view devOverview {
    global style theme_development
    include *
  }
}
```

## Icon Styling

Apply technology icons to elements:

```likec4
view microservices {
  include *
  
  include system.api with { icon tech:java }
  include system.cache with { icon tech:redis }
  include system.database with { icon tech:mongodb }
  
  // Apply icons by pattern
  style element.technology *= 'Node' { icon tech:nodejs }
  style element.technology *= 'Python' { icon tech:python }
}
```

## Color Accessibility

- **Primary/Secondary:** Use for contrast and focus
- **Success/Warning/Danger:** Use for state indication (red = problems)
- **Muted:** Use for less important elements
- **Avoid:** Pure black/white - use primary/secondary/muted instead

## Styling Checklist

- [ ] All colors from `shared/spec-global.c4`
- [ ] All shapes from defined element kinds
- [ ] Style predicates use `element.tag = #name` or `element.kind = 'kind'`
- [ ] No conflicting color styles on same element
- [ ] Opacity used sparingly (not to hide important context)
- [ ] Icons match technology property

## Common Mistakes

| ❌ Don't | ✅ Do | Why |
|---|---|---|
| Custom color `#FF5733` | Use `primary` from spec | Maintains consistency |
| Custom shape `hexagon` | Use kind from spec | Standard shapes only |
| Hide parent containers with opacity | Keep parent visible | Context is important |
| Multiple conflicting colors | One color per element | Prevents visual confusion |

## Related Skills

- `design-view` - Basic view organization and includes
- `navigate-views` - Navigation and view linking
