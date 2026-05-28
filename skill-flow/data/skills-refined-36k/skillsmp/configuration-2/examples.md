# Configuration Examples

> **Note**: See `SKILL.md` for the basic structure. This file contains detailed field references and validation examples.

## Configuration Field Reference

### Required Fields

#### application_name
- **Type**: string
- **Pattern**: `^[a-z0-9]+(-[a-z0-9]+)*$` (kebab-case)
- **Description**: The name of your application in kebab-case
- **Examples**: `"omni-inventory-manager-web"`, `"my-awesome-app"`

#### project_scope
- **Type**: string
- **Pattern**: `^@[a-z0-9-]+$` (npm scope format)
- **Description**: Your NPM scope/organization
- **Examples**: `"@pdl-fulfillment-omni"`, `"@myorg"`

#### router_base_path
- **Type**: string
- **Pattern**: `^/[a-z0-9-/]*$` (path format)
- **Description**: Base path for the Vue Router
- **Examples**: `"/omni-inventory-manager"`, `"/app"`, `"/"`

#### api_base_path
- **Type**: string
- **Pattern**: `^/[a-z0-9-/]*$` (path format)
- **Description**: Base API path for backend service proxying
- **Examples**: `"/omni-access-manager"`, `"/api"`, `"/backend"`

#### default_port
- **Type**: integer
- **Range**: 1024-65535
- **Description**: Port for the development server
- **Examples**: `8089`, `3000`, `8080`

#### application_type
- **Type**: string
- **Enum**: `["micro-frontend", "standalone"]`
- **Description**: Type of application
  - `"micro-frontend"`: Single-spa with SystemJS
  - `"standalone"`: Traditional SPA with ES modules
- **Default**: `"micro-frontend"`

#### test_framework
- **Type**: string
- **Enum**: `["jest", "vitest"]`
- **Description**: Testing framework to use
- **Default**: `"jest"`

#### state_management
- **Type**: string
- **Enum**: `["vuex", "pinia"]`
- **Description**: State management library to use
- **Default**: `"vuex"`

### Optional Fields

#### node_version
- **Type**: string
- **Pattern**: `^v?[0-9]+\.[0-9]+\.[0-9]+$`
- **Default**: `"v22.16.0"`
- **Examples**: `"v22.16.0"`, `"22.16.0"`

#### vue_version
- **Type**: string
- **Pattern**: `^\^?[0-9]+\.[0-9]+\.[0-9]+$`
- **Default**: `"^3.5.13"`
- **Examples**: `"^3.5.13"`, `"3.5.13"`

#### vite_version
- **Type**: string
- **Pattern**: `^\^?[0-9]+\.[0-9]+\.[0-9]+$`
- **Default**: `"^6.3.5"`
- **Examples**: `"^6.3.5"`, `"6.3.5"`

#### typescript_version
- **Type**: string
- **Pattern**: `^\^?[0-9]+\.[0-9]+$`
- **Default**: `"^5.7.3"`
- **Examples**: `"^5.7.3"`, `"5.7.3"`

#### enable_single_spa
- **Type**: boolean
- **Default**: `true`
- **Description**: Enable single-spa micro frontend integration
- **Note**: Should be false for standalone applications

#### enable_datadog
- **Type**: boolean
- **Default**: `true`
- **Description**: Enable Datadog RUM monitoring

#### component_library
- **Type**: string
- **Default**: `"@royalaholddelhaize/pdl-spectrum-component-library-web"`
- **Description**: Component library to use (leave empty to skip)
- **Examples**: `"@royalaholddelhaize/pdl-spectrum-component-library-web"`, `"@myorg/component-library"`, `""`

#### component_library_version
- **Type**: string
- **Default**: `"^1.0.3"`
- **Description**: Version of the component library
- **Examples**: `"^1.0.3"`, `"1.2.0"`

---

## Example 1: Minimal Modern Stack (config.json)

```json
{
  "application_name": "my-app-web",
  "project_scope": "@myorg",
  "router_base_path": "/my-app",
  "api_base_path": "/api",
  "default_port": 8080,
  "application_type": "standalone",
  "test_framework": "vitest",
  "state_management": "pinia"
}
```

**Result**:
- Uses Vite + Vitest + Pinia (modern stack)
- Standalone SPA (no single-spa)
- No component library
- All optional fields use defaults

---

## Example 2: Micro-Frontend with Component Library

```json
{
  "application_name": "omni-inventory-manager-web",
  "project_scope": "@pdl-fulfillment-omni",
  "router_base_path": "/omni-inventory-manager",
  "api_base_path": "/omni-access-manager",
  "default_port": 8089,
  "application_type": "micro-frontend",
  "test_framework": "jest",
  "state_management": "vuex",
  "component_library": "@royalaholddelhaize/pdl-spectrum-component-library-web",
  "component_library_version": "^1.0.3"
}
```

**Result**:
- Uses Jest + Vuex (legacy stack)
- Micro-frontend with single-spa
- Includes component library
- Creates .npmrc

---

## Example 3: Hybrid Approach (Partial config.json)

```json
{
  "application_name": "reporting-dashboard-web",
  "project_scope": "@analytics",
  "application_type": "standalone",
  "test_framework": "vitest",
  "state_management": "pinia"
}
```

**Agent will prompt for**:
- `router_base_path`
- `api_base_path`
- `default_port`

**Agent will use defaults for**:
- `node_version`: `"v22.16.0"`
- `vue_version`: `"^3.5.13"`
- `vite_version`: `"^6.3.5"`
- Other optional fields

---

## Example 4: No config.json (Full Interactive)

**User runs agent without config.json**

**Agent prompts**:
```
? Application name (kebab-case): my-awesome-app-web
? NPM scope (e.g., @myorg): @mycompany
? Router base path (e.g., /my-app): /my-awesome-app
? API base path (e.g., /api): /api
? Development server port: 3000
? Application type: 
  ❯ standalone
    micro-frontend
? Test framework:
  ❯ vitest
    jest
? State management:
  ❯ pinia
    vuex
? Save this configuration to config.json for future use? Yes
```

**Result**: All values from prompts, defaults for optional fields

**Agent then saves**:
```
✓ Configuration saved to config.json
   You can manually add it to config.json if needed (it will be gitignored)
✓ Added config.json to .gitignore
```

**Generated config.json**:
```json
{
  "application_name": "my-awesome-app-web",
  "project_scope": "@mycompany",
  "router_base_path": "/my-awesome-app",
  "api_base_path": "/api",
  "default_port": 3000,
  "application_type": "standalone",
  "test_framework": "vitest",
  "state_management": "pinia",
  "node_version": "v22.16.0",
  "vue_version": "^3.5.13",
  "vite_version": "^6.3.5",
  "typescript_version": "^5.7.3",
  "enable_single_spa": false,
  "enable_datadog": true,
  "component_library": "@royalaholddelhaize/pdl-spectrum-component-library-web",
  "component_library_version": "^1.0.3"
}
```

---

## Example 4b: Interactive Prompts - User Declines to Save

**Console Output:**
```
? Application name (kebab-case): my-app-web
? NPM scope (e.g., @myorg): @mycompany
...
? Save this configuration to config.json for future use? No
```

**Result**: 
- Configuration used for generation
- No config.json file created
- User can generate config.json later if needed

---

## Example 5: Standalone Without Component Library

```json
{
  "application_name": "customer-portal-web",
  "project_scope": "@customer-services",
  "router_base_path": "/portal",
  "api_base_path": "/customer-api",
  "default_port": 5000,
  "application_type": "standalone",
  "test_framework": "vitest",
  "state_management": "pinia",
  "component_library": "",
  "enable_single_spa": false,
  "enable_datadog": false
}
```

**Result**:
- Standalone app with no micro-frontend features
- No component library
- No Datadog monitoring
- Minimal configuration

---

## Example 6: Override All Defaults

```json
{
  "application_name": "legacy-system-web",
  "project_scope": "@legacy",
  "router_base_path": "/legacy",
  "api_base_path": "/api/v1",
  "default_port": 3000,
  "application_type": "micro-frontend",
  "test_framework": "jest",
  "state_management": "vuex",
  "node_version": "v22.16.0",
  "vue_version": "^3.5.13",
  "vite_version": "^6.3.5",
  "typescript_version": "^5.7.3",
  "enable_single_spa": true,
  "enable_datadog": true,
  "component_library": "@custom/component-lib",
  "component_library_version": "^2.5.0",
}
```

**Result**:
- All fields explicitly set
- No defaults used
- Full control over configuration

---

## Auto-Derived Values Examples

### Input:
```json
{
  "application_name": "omni-inventory-manager-web"
}
```

### Auto-Derived:
```javascript
{
  "main_component_name": "OmniInventoryManagerWeb",  // PascalCase
  "application_id": "omni-inventory-manager-web",    // Same as name
  "service_name": "omni-inventory-manager-web",      // Same as name
  "is_standalone": false,                            // From application_type
  "is_microfrontend": true,                          // From application_type
  "vite_build_format": "system"                      // From application_type
}
```

---

## Package Reference Selection

Based on `test_framework` and `state_management`:

### Jest + Vuex
```json
{
  "test_framework": "jest",
  "state_management": "vuex"
}
```
**Uses**: `skills/package-json/reference/jest-vuex.md`

### Jest + Pinia
```json
{
  "test_framework": "jest",
  "state_management": "pinia"
}
```
**Uses**: `skills/package-json/reference/jest-pinia.md`

### Vitest + Vuex
```json
{
  "test_framework": "vitest",
  "state_management": "vuex"
}
```
**Uses**: `skills/package-json/reference/vitest-vuex.md`

### Vitest + Pinia
```json
{
  "test_framework": "vitest",
  "state_management": "pinia"
}
```
**Uses**: `skills/package-json/reference/vitest-pinia.md`

---

## Validation Examples

### ✅ Valid Configuration
```json
{
  "application_name": "my-app-web",
  "project_scope": "@myorg",
  "router_base_path": "/my-app",
  "api_base_path": "/api",
  "default_port": 8080,
  "application_type": "standalone"
}
```

### ❌ Invalid: application_name not kebab-case
```json
{
  "application_name": "MyAppWeb"  // Should be "my-app-web"
}
```

### ❌ Invalid: project_scope missing @
```json
{
  "project_scope": "myorg"  // Should be "@myorg"
}
```

### ❌ Invalid: router_base_path missing /
```json
{
  "router_base_path": "my-app"  // Should be "/my-app"
}
```

### ❌ Invalid: default_port out of range
```json
{
  "default_port": 80  // Should be 1024-65535
}
```

### ❌ Invalid: application_type unknown
```json
{
  "application_type": "spa"  // Should be "standalone" or "micro-frontend"
}
```

---

## Configuration Summary Output

```
════════════════════════════════════════════════════════════
  CONFIGURATION SUMMARY
════════════════════════════════════════════════════════════
Application:       omni-inventory-manager-web
Scope:             @pdl-fulfillment-omni
Type:              micro-frontend
Router Base:       /omni-inventory-manager
API Base:          /omni-access-manager
Port:              8089
Test Framework:    jest
State Management:  vuex
Component Library: @royalaholddelhaize/pdl-spectrum-component-library-web
════════════════════════════════════════════════════════════
```

---

## Security Note

⚠️ **Never commit config.json with sensitive data**

```bash
# Add to .gitignore
echo "config.json" >> .gitignore
```

**Safe to commit**:
- None (all config files are user-specific or archived)

**Never commit**:
- `config.json`
