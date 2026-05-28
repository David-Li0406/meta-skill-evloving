# Framework Detection Algorithm

Detection patterns for identifying source frameworks in migration projects.

## Detection Priority

1. **package.json analysis** (primary)
2. **Configuration files** (secondary)
3. **File extension patterns** (tertiary)
4. **Import statement analysis** (quaternary)

## Detection Rules

### Vue.js

```yaml
vue:
  package_json:
    - "vue": "*"
    - "@vue/cli-service": "*"
  config_files:
    - vue.config.js
    - vue.config.ts
    - vite.config.ts (with @vitejs/plugin-vue)
  file_patterns:
    - "**/*.vue"
  version_detection:
    vue2: '"vue": "^2.'
    vue3: '"vue": "^3.'
```

### React CRA

```yaml
react_cra:
  package_json:
    - "react-scripts": "*"
  file_patterns:
    - src/index.js
    - src/index.tsx
```

### React Vite

```yaml
react_vite:
  package_json:
    - "@vitejs/plugin-react": "*"
  config_files:
    - vite.config.js
    - vite.config.ts
```

### Angular

```yaml
angular:
  package_json:
    - "@angular/core": "*"
  config_files:
    - angular.json
  file_patterns:
    - "**/*.component.ts"
    - "**/*.module.ts"
```

### Svelte

```yaml
svelte:
  package_json:
    - "svelte": "*"
  config_files:
    - svelte.config.js
  file_patterns:
    - "**/*.svelte"
```

## Detection Logic

```python
def detect_framework(project_path):
    """Detect source framework from project structure."""

    # 1. Check package.json
    pkg = load_json(f"{project_path}/package.json")
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

    # Priority order
    if "react-scripts" in deps:
        return "react_cra", get_version(deps.get("react"))

    if "@angular/core" in deps:
        return "angular", get_version(deps.get("@angular/core"))

    if "vue" in deps:
        version = "3" if deps["vue"].startswith("^3") else "2"
        return f"vue{version}", get_version(deps.get("vue"))

    if "svelte" in deps:
        return "svelte", get_version(deps.get("svelte"))

    if "@vitejs/plugin-react" in deps:
        return "react_vite", get_version(deps.get("react"))

    # 2. Fall back to config file detection
    if exists(f"{project_path}/angular.json"):
        return "angular", "unknown"

    if exists(f"{project_path}/vue.config.js"):
        return "vue2", "unknown"

    if exists(f"{project_path}/svelte.config.js"):
        return "svelte", "unknown"

    # 3. Fall back to file pattern detection
    if glob(f"{project_path}/**/*.vue"):
        return "vue", "unknown"

    if glob(f"{project_path}/**/*.svelte"):
        return "svelte", "unknown"

    return "unknown", "unknown"
```

---

Version: 2.1.0
Source: jikime-migration-to-nextjs SKILL.md
