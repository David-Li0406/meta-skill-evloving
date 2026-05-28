# Latest Versions Reference

This file provides the structure for generating package.json with the latest versions from npm registry.

## Usage

Use this reference when:
- User requests "latest configuration"
- User wants "most recent versions"
- User specifies "use latest packages"
- Default for new projects

## How It Works

All versions are dynamically resolved from `../versions.json`:
1. Load versions.json configuration
2. For each package marked as `"latest"`, fetch current version from npm
3. For pinned versions, use as specified
4. Replace placeholders with resolved versions

## Package.json Structure with Latest Versions

```json
{
  "name": "{{project_scope}}/{{application_name}}",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite preview --port {{default_port}}",
    "build:watch": "vite build --watch",
    "serve": "{{serve_command}}",
    "build": "vite build",
    "test:unit": "{{test_framework}}",
    "test:unit:watch": "{{test_framework}} --watch",
    "lint:init:watch": "npm run lint && npm run lint:watch",
    "lint:watch": "chokidar \"src/**/*.{js,ts,vue}\" -i node_modules -i dist -i .git --debounce 500 --initial false -c \"npm run lint\"",
    "lint": "eslint --ext .js,.ts,.vue src",
    "prettier": "prettier --write .",
    "prettier-watch": "onchange \"**/*\" \"!dist/**\" \"!node_modules/**\" -- prettier --write {{changed}}",
    "prepare": "husky"
  },
  "dependencies": {
    "vue": "{{vue_version}}",
    "vue-router": "{{vue_router_version}}",
    "{{state_management_lib}}": "{{state_management_version}}",
    "axios": "{{axios_version}}",
    "core-js": "{{core_js_version}}",
    "date-fns": "{{date_fns_version}}",
    "date-fns-tz": "{{date_fns_tz_version}}",
    "{{component_library}}": "{{component_library_version}}",
    "@datadog/browser-rum": "{{datadog_rum_version}}"
  },
  "devDependencies": {
    "vite": "{{vite_version}}",
    "@vitejs/plugin-vue": "{{vitejs_plugin_vue_version}}",
    "vite-plugin-css-injected-by-js": "{{vite_plugin_css_injected_version}}",
    "vite-svg-loader": "{{vite_svg_loader_version}}",
    "typescript": "{{typescript_version}}",
    "@types/node": "{{types_node_version}}",
    "@types/jest": "{{types_jest_version}}",
    "@types/jsdom": "{{types_jsdom_version}}",
    "{{test_framework}}": "{{test_framework_version}}",
    "@vue/test-utils": "{{vue_test_utils_version}}",
    "ts-jest": "{{ts_jest_version}}",
    "@babel/core": "{{babel_core_version}}",
    "@babel/plugin-transform-runtime": "{{babel_plugin_transform_runtime_version}}",
    "@babel/preset-env": "{{babel_preset_env_version}}",
    "eslint": "{{eslint_version}}",
    "eslint-plugin-vue": "{{eslint_plugin_vue_version}}",
    "@typescript-eslint/eslint-plugin": "{{typescript_eslint_plugin_version}}",
    "@typescript-eslint/parser": "{{typescript_eslint_parser_version}}",
    "vue-eslint-parser": "{{vue_eslint_parser_version}}",
    "@vue/eslint-config-typescript": "{{vue_eslint_config_typescript_version}}",
    "eslint-config-prettier": "{{eslint_config_prettier_version}}",
    "eslint-plugin-prettier": "{{eslint_plugin_prettier_version}}",
    "@eslint/js": "{{eslint_js_version}}",
    "@eslint/eslintrc": "{{eslint_eslintrc_version}}",
    "prettier": "{{prettier_version}}",
    "sass": "{{sass_version}}",
    "sass-loader": "{{sass_loader_version}}",
    "stylelint": "{{stylelint_version}}",
    "stylelint-config-recommended-vue": "{{stylelint_config_recommended_vue_version}}",
    "stylelint-config-standard-scss": "{{stylelint_config_standard_scss_version}}",
    "husky": "{{husky_version}}",
    "lint-staged": "{{lint_staged_version}}",
    "npm-run-all": "{{npm_run_all_version}}",
    "chokidar-cli": "{{chokidar_cli_version}}",
    "onchange": "{{onchange_version}}"
  }
}
```

## Conditional Dependencies

### Serve Command Based on Application Type

The `serve` script differs based on application type:

**Standalone Application** (`application_type === "standalone"`):
```json
{
  "scripts": {
    "serve": "vite serve --port {{default_port}} --mode standalone"
  }
}
```

**Micro-Frontend Application** (`application_type === "micro-frontend"`):
```json
{
  "scripts": {
    "serve": "npm-run-all --parallel build:watch dev lint:init:watch"
  }
}
```

**Explanation**:
- **Standalone**: Uses Vite dev server directly for fast HMR and development
- **Micro-Frontend**: Uses build-watch + preview to serve the built SystemJS bundle, which is required for single-spa integration

### Single-spa (Micro-Frontend)
If `application_type === "micro-frontend"`:
```json
{
  "dependencies": {
    "single-spa-vue": "{{single_spa_vue_version}}"
  }
}
```

### State Management
If `state_management === "vuex"`:
```json
{
  "dependencies": {
    "vuex": "{{vuex_version}}"
  }
}
```

If `state_management === "pinia"`:
```json
{
  "dependencies": {
    "pinia": "{{pinia_version}}"
  }
}
```

### Testing Framework
If `test_framework === "jest"`:
```json
{
  "devDependencies": {
    "jest": "{{jest_version}}",
    "@vue/vue3-jest": "{{vue3_jest_version}}",
    "babel-jest": "{{babel_jest_version}}",
    "ts-jest": "{{ts_jest_version}}"
  }
}
```

If `test_framework === "vitest"`:
```json
{
  "devDependencies": {
    "vitest": "{{vitest_version}}",
    "@vitest/ui": "{{vitest_ui_version}}",
    "@vitest/coverage-v8": "{{vitest_coverage_v8_version}}",
    "jsdom": "{{jsdom_version}}"
  }
}
```

**CRITICAL VITEST DEPENDENCIES**:
- `vitest` - The test framework itself
- `@vitest/ui` - Optional UI for test visualization
- `@vitest/coverage-v8` - **REQUIRED** Coverage provider (used in vitest.config.ts)
- `jsdom` - **REQUIRED** DOM environment for Vue component testing (used in vitest.config.ts)

**Why these are required**:
- Without `jsdom`: Tests will fail with "jsdom environment not found" error
- Without `@vitest/coverage-v8`: Coverage reports will fail to generate
- These packages are referenced in `vitest.config.ts` configuration

### Component Library
If `component_library` is specified:
```json
{
  "dependencies": {
    "{{component_library}}": "{{component_library_version}}"
  }
}
```

## Version Resolution Process

### Step 1: Load versions.json
```javascript
const versionsConfig = require('../versions.json');
```

### Step 2: Resolve Each Package
```javascript
// Example for Vue
const vueVersionSpec = versionsConfig.core.vue;

if (vueVersionSpec === 'latest') {
  // Fetch from npm
  const latestVersion = await fetchLatestVersion('vue');
  config.vue_version = `^${latestVersion}`;
} else {
  // Use specified version
  config.vue_version = vueVersionSpec;
}
```

### Step 3: Apply to Template
Replace all `{{placeholder}}` values with resolved versions.

## Version Mapping

| Placeholder | versions.json Path | Example Result |
|-------------|-------------------|----------------|
| `{{vue_version}}` | `core.vue` | `^3.5.13` |
| `{{vite_version}}` | `core.vite` | `^6.3.5` |
| `{{typescript_version}}` | `core.typescript` | `^5.7.3` |
| `{{vue_router_version}}` | `dependencies.vue-router` | `^4.6.3` |
| `{{vuex_version}}` | `dependencies.vuex` | `^4.1.0` |
| `{{pinia_version}}` | `dependencies.pinia` | `^2.3.0` |
| `{{axios_version}}` | `dependencies.axios` | `^1.7.9` |
| `{{eslint_version}}` | `devDependencies.eslint` | `^9.30.1` |
| `{{prettier_version}}` | `devDependencies.prettier` | `^3.6.2` |
| `{{jest_version}}` | `devDependencies.jest` | `^30.2.0` |
| `{{vitest_version}}` | `devDependencies.vitest` | `^3.0.0` |

## Example: Complete Resolution

### Input (versions.json)
```json
{
  "core": {
    "vue": "latest",
    "vite": "latest",
    "typescript": "latest"
  },
  "dependencies": {
    "vue-router": "latest",
    "vuex": "latest"
  },
  "devDependencies": {
    "eslint": "latest",
    "prettier": "latest"
  }
}
```

### Process
1. Fetch latest versions from npm:
   - `npm view vue version` → `3.5.13`
   - `npm view vite version` → `6.3.5`
   - `npm view typescript version` → `5.7.3`
   - etc.

2. Apply caret prefix for compatibility:
   - `3.5.13` → `^3.5.13`
   - `6.3.5` → `^6.3.5`

3. Replace placeholders in template

### Output (Generated package.json)
```json
{
  "name": "@myorg/my-app",
  "version": "0.1.0",
  "dependencies": {
    "vue": "^3.5.13",
    "vue-router": "^4.6.3",
    "vuex": "^4.1.0"
  },
  "devDependencies": {
    "vite": "^6.3.5",
    "typescript": "^5.7.3",
    "eslint": "^9.30.1",
    "prettier": "^3.6.2"
  }
}
```

## Error Handling

### Network Error
If npm fetch fails:
1. Log warning
2. Fall back to default version
3. Continue generation

```javascript
try {
  const version = await fetchLatestVersion('vue');
  config.vue_version = `^${version}`;
} catch (error) {
  console.warn('Failed to fetch vue version, using default');
  config.vue_version = '^3.5.13'; // Fallback
}
```

### Package Not Found
If package doesn't exist on npm:
1. Log error
2. Skip package or use specified version
3. Continue generation

## Best Practices

1. **Always validate** resolved versions before generating
2. **Cache results** during single generation run
3. **Log versions** being used for debugging
4. **Fallback gracefully** if network unavailable
5. **Document versions** in generated README

## See Also

- `../versions.json` - Version configuration
- `jest-vuex.md` - Jest + Vuex reference
- `vitest-pinia.md` - Vitest + Pinia reference
