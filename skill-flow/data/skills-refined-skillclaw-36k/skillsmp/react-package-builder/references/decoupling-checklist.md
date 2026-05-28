# Decoupling Checklist

Before extracting a component into a package, verify these constraints.

## Package Must NOT

| Constraint | Why |
|------------|-----|
| Fetch data | Parent provides data via props |
| Talk to Supabase | No backend coupling |
| Depend on Auth | Parent handles auth context |
| Persist state | Parent saves progress/preferences |
| Manage routing | Parent controls navigation |
| Import from `apps/` | Only peer dependencies allowed |

## Package MAY

| Allowed | Notes |
|---------|-------|
| Manage transient UI state | Panels, dragging, timers |
| Use animation libraries | GSAP, framer-motion as dependencies |
| Emit callbacks | Parent decides what to do |
| Accept refs for imperative API | Optional, prefer callbacks |

## Props Contract Review

- [ ] All data comes via props (no fetching)
- [ ] All side effects use callbacks (no direct mutations)
- [ ] Types are generic (no app-specific structures)
- [ ] Controlled/uncontrolled both supported for stateful props
- [ ] Default values documented

## Adapter Layer (in app)

The consuming app creates an adapter that:

1. Loads data (verses, media, preferences)
2. Maps app types → package types
3. Handles callbacks (save progress, play audio)
4. Manages routing/navigation

Example location:
```
apps/<app-name>/src/features/<feature>/
  <Component>Screen.tsx      # Wrapper component
  use<Component>Adapter.ts   # Data/state adapter hook
```
