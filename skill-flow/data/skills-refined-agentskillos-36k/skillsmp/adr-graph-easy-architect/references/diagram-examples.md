# Diagram Examples by ADR Type

This reference provides diagram patterns for different ADR types. Every ADR requires **two diagrams**:

1. **Before/After** — Shows state change (Context section)
2. **Architecture** — Shows component relationships (Architecture section)

## Feature ADR

### Before/After Diagram

Shows what capability is being added:

```
graph { flow: east; }
[ Before ] { label: "Manual Process\n(No Automation)"; }
[ After ] { label: "Automated Pipeline\n(CI/CD)"; }
[ Before ] --> [ After ]
```

### Architecture Diagram

Shows new components and integrations:

```
graph { flow: south; }
[ User ] -> [ API Gateway ]
[ API Gateway ] -> [ New Service ]
[ New Service ] -> [ Database ]
[ New Service ] -> [ External API ]
```

## Bug Fix ADR

### Before/After Diagram

Shows incorrect vs correct behavior:

```
graph { flow: east; }
[ Before ] { label: "Race Condition\n(Data Loss)"; border: bold; }
[ After ] { label: "Mutex Lock\n(Data Safe)"; }
[ Before ] --> [ After ]
```

### Architecture Diagram

Shows where the fix was applied:

```
graph { flow: south; }
[ Request Handler ] -> [ Mutex ] { label: "NEW"; }
[ Mutex ] -> [ Shared State ]
```

## Refactor ADR

### Before/After Diagram

Shows structural change:

```
graph { flow: east; }
[ Before ] { label: "Monolith\n(Single Service)"; }
[ After ] { label: "Microservices\n(3 Services)"; }
[ Before ] --> [ After ]
```

### Architecture Diagram

Shows new structure:

```
graph { flow: south; }
[ API Gateway ] -> [ Auth Service ]
[ API Gateway ] -> [ User Service ]
[ API Gateway ] -> [ Data Service ]
[ Auth Service ] -> [ Shared DB ]
[ User Service ] -> [ Shared DB ]
[ Data Service ] -> [ Shared DB ]
```

## Documentation ADR

### Before/After Diagram

Shows documentation coverage change:

```
graph { flow: east; }
[ Before ] { label: "Scattered Docs\n(README only)"; }
[ After ] { label: "Structured Docs\n(ADR + Specs)"; }
[ Before ] --> [ After ]
```

### Architecture Diagram

Shows documentation structure:

```
graph { flow: south; }
[ docs/ ] -> [ adr/ ]
[ docs/ ] -> [ design/ ]
[ docs/ ] -> [ api/ ]
[ adr/ ] -> [ YYYY-MM-DD-slug.md ]
[ design/ ] -> [ YYYY-MM-DD-slug/spec.md ]
```

## Performance ADR

### Before/After Diagram

Shows performance improvement:

```
graph { flow: east; }
[ Before ] { label: "500ms Response\n(No Cache)"; border: bold; }
[ After ] { label: "50ms Response\n(Redis Cache)"; }
[ Before ] --> [ After ]
```

### Architecture Diagram

Shows caching layer:

```
graph { flow: east; }
[ Client ] -> [ API ]
[ API ] -> [ Redis Cache ] { label: "check"; }
[ Redis Cache ] -> [ Database ] { label: "miss"; }
[ Redis Cache ] -> [ API ] { label: "hit"; }
```

## Tips for Effective Diagrams

1. **Keep it simple** — 3-6 nodes maximum per diagram
2. **Use labels** — Annotate edges and nodes with context
3. **Show contrast** — Before/After should have clear visual difference
4. **Be specific** — Use actual component names, not generic boxes
5. **Flow direction** — Use `east` for before/after, `south` for architecture
