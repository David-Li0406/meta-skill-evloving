---
name: configure-project-includes
description: Manage likec4.config.json includes and image aliases. Ensures relative paths and preserves existing configuration. Support multi-file organization (system-model + system-views + deployment + operations).
---

# Manage LikeC4 Project Includes

Use this skill when configuring project dependencies in likec4.config.json.

## Single vs. Multi-File Organization

### Small Projects (Single File)
For simple systems, one model file works:
```
project/
  system.c4              # All elements, relationships, and views
```

### Large Projects (Multi-File Recommended)
For complex systems, split into focused files:
```
project/
  system-model.c4        # ← Elements and relationships only
  system-views.c4        # ← Architectural views (C1, C2, C3)
  system-sequences.c4    # ← Use case workflows (dynamic views)
  deployment.c4          # ← Deployment definition (infrastructure)
  deployment-views.c4    # ← Deployment visualizations
  operations.c4          # ← Operations infrastructure (monitoring, backup)
  operations-views.c4    # ← Operations visualizations
```

**Benefits:**
- **Collaboration:** Multiple developers edit different files without conflicts
- **Maintainability:** 150-200 line files are easier to navigate than 2000-line files
- **Clarity:** File names indicate content type and purpose
- **Scaling:** Easy to add new model files as system grows

### File Organization Convention

- **Model files:** Define structure → `system-model.c4`, `deployment.c4`, `operations.c4`
- **View files:** Define visualizations → `system-views.c4`, `deployment-views.c4`, `operations-views.c4`
- **Sequences:** Temporal flows → `system-sequences.c4` (separate from system-views)
- **Config:** Project settings → `likec4.config.json`

## Rules

1. **Relative paths:** Use `../shared` not absolute paths
2. **Preserve defaults:** Keep existing includes when adding new ones
3. **Image aliases:** Maintain `"@": "../shared/images"` for icon consistency
4. **Multiple specs:** Append to `paths` array, don't replace

## Example

```json
{
  "name": "my-project",
  "title": "My Project",
  "include": {
    "paths": ["../shared", "../common"]
  },
  "imageAliases": {
    "@": "../shared/images"
  }
}
```
