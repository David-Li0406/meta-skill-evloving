# Conditional Generation Examples

> **Note**: See `SKILL.md` for the basic logic. This file contains detailed examples for different application types.

## Example 1: Micro-Frontend Application

### Configuration
```json
{
  "application_name": "omni-inventory-manager-web",
  "application_type": "micro-frontend",
  "enable_single_spa": true
}
```

### Conditional Checks
```javascript
userConfig.is_microfrontend = true;
userConfig.is_standalone = false;
userConfig.vite_build_format = 'system';
```

### Files Generated

**✅ .env.standalone**
```bash
VITE_LAUNCHER_APP_URL=http://localhost:8088
```

**✅ main.ts (with single-spa lifecycle)**
```typescript
import { h, createApp } from 'vue';
import singleSpaVue from 'single-spa-vue';
import App from './App.vue';
import router from './router';
import store from './store';

const vueLifecycles = singleSpaVue({
  createApp,
  appOptions: {
    render() {
      return h(App);
    },
  },
  handleInstance: (app) => {
    app.use(router);
    app.use(store);
  }
});

export const bootstrap = vueLifecycles.bootstrap;
export const mount = vueLifecycles.mount;
export const unmount = vueLifecycles.unmount;
```

**✅ EnvConsts.ts (with launcherAppUrl)**
```typescript
export const baseUrl = import.meta.env.VITE_ACCESS_MANAGEMENT_BASE_URL;
export const launcherAppUrl = import.meta.env.VITE_LAUNCHER_APP_URL;
export const datadogEnv = import.meta.env.VITE_DATADOG_ENV;
```

**✅ index.html**
```html
<div id="single-spa-application:omni-inventory-manager"></div>
```

**✅ package.json**
```json
{
  "scripts": {
    "serve": "npm-run-all --parallel build:watch dev lint:init:watch",
    "dev": "vite preview --port 8091",
    "build:watch": "vite build --watch"
  },
  "dependencies": {
    "vue": "^3.5.13",
    "single-spa-vue": "^3.0.2"
  }
}
```

**✅ vite.config.ts**
```typescript
export default defineConfig({
  build: {
    lib: {
      formats: ['system']
    }
  }
});
```

---

## Example 2: Standalone Application

### Configuration
```json
{
  "application_name": "customer-portal-web",
  "application_type": "standalone",
  "enable_single_spa": false
}
```

### Conditional Checks
```javascript
userConfig.is_standalone = true;
userConfig.is_microfrontend = false;
userConfig.vite_build_format = 'es';
```

### Files Generated

**❌ .env.standalone (SKIPPED)**
- File not created for standalone apps

**✅ main.ts (simple mount)**
```typescript
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';

const app = createApp(App);

app.use(router);
app.use(store);

app.mount('#app');
```

**✅ EnvConsts.ts (without launcherAppUrl)**
```typescript
export const baseUrl = import.meta.env.VITE_ACCESS_MANAGEMENT_BASE_URL;
export const datadogEnv = import.meta.env.VITE_DATADOG_ENV;
```

**✅ index.html**
```html
<div id="app"></div>
```

**✅ package.json**
```json
{
  "scripts": {
    "serve": "vite serve --port 8090 --mode standalone",
    "dev": "vite preview --port 8090",
    "build": "vite build"
  },
  "dependencies": {
    "vue": "^3.5.13"
  }
}
```

**✅ vite.config.ts**
```typescript
export default defineConfig({
  build: {
    lib: {
      formats: ['es']
    }
  }
});
```

---

## Example 3: Auto-Correction (Standalone with enable_single_spa = true)

### Configuration
```json
{
  "application_type": "standalone",
  "enable_single_spa": true
}
```

### Agent Auto-Correction

**Console Output:**
```
⚠️  Warning: Standalone apps typically do not use single-spa.
   Auto-correcting: enable_single_spa = false

─────────────────────────────────────────────────────────────
  CONDITIONAL FILE GENERATION
─────────────────────────────────────────────────────────────
Application Type:  standalone
Build Format:      es
Single-SPA:        Disabled

Standalone App Files:
  ✗ .env.standalone (skipped)
  ✓ main.ts (simple mount)
  ✓ EnvConsts.ts (without launcherAppUrl)
  ✗ single-spa-vue (skipped)
─────────────────────────────────────────────────────────────
```

**Corrected Config:**
```javascript
{
  "application_type": "standalone",
  "enable_single_spa": false  // ✓ Auto-corrected
}
```

---

## Example 4: Auto-Correction (Micro-Frontend with enable_single_spa = false)

### Configuration
```json
{
  "application_type": "micro-frontend",
  "enable_single_spa": false
}
```

### Agent Auto-Correction

**Console Output:**
```
⚠️  Warning: Micro-frontend apps require single-spa.
   Auto-correcting: enable_single_spa = true

─────────────────────────────────────────────────────────────
  CONDITIONAL FILE GENERATION
─────────────────────────────────────────────────────────────
Application Type:  micro-frontend
Build Format:      system
Single-SPA:        Enabled

Micro-Frontend Files:
  ✓ .env.standalone
  ✓ main.ts (single-spa lifecycle)
  ✓ EnvConsts.ts (with launcherAppUrl)
  ✓ Dependencies: single-spa-vue
─────────────────────────────────────────────────────────────
```

**Corrected Config:**
```javascript
{
  "application_type": "micro-frontend",
  "enable_single_spa": true  // ✓ Auto-corrected
}
```

---

## Example 5: Template Selection Logic

```javascript
// Helper function to select templates
function getTemplate(filename, config) {
  const templates = {
    'main.ts': config.is_microfrontend 
      ? 'skills/main-entry/main-microfrontend.ts' 
      : 'skills/main-entry/main-standalone.ts',
      
    'EnvConsts.ts': config.is_microfrontend
      ? 'skills/env-constants/EnvConsts-microfrontend.ts'
      : 'skills/env-constants/EnvConsts-standalone.ts',
      
    'index.html': config.is_microfrontend
      ? 'skills/index-html/index-microfrontend.html'
      : 'skills/index-html/index-standalone.html'
  };
  
  return templates[filename] || null;
}

// Usage
const mainTemplate = getTemplate('main.ts', userConfig);
console.log(`Using template: ${mainTemplate}`);
// Micro-frontend: "skills/main-entry/main-microfrontend.ts"
// Standalone: "skills/main-entry/main-standalone.ts"
```

---

## Example 6: File Generation Logic

```javascript
// Determine which files to generate
function shouldGenerateFile(filename, config) {
  const conditionalFiles = {
    '.env.standalone': config.is_microfrontend
  };
  
  if (filename in conditionalFiles) {
    return conditionalFiles[filename];
  }
  
  return true;  // Generate by default
}

// Usage examples
console.log(shouldGenerateFile('.env.standalone', { is_microfrontend: true }));
// Output: true

console.log(shouldGenerateFile('.env.standalone', { is_standalone: true }));
// Output: false (because is_microfrontend would be false)

console.log(shouldGenerateFile('package.json', { is_standalone: true }));
// Output: true (not conditional)
```

---

## Example 7: Dependency Selection Logic

```javascript
// Determine which dependencies to include
function shouldIncludeDependency(dependencyName, config) {
  const conditionalDependencies = {
    'single-spa-vue': config.is_microfrontend
  };
  
  if (dependencyName in conditionalDependencies) {
    return conditionalDependencies[dependencyName];
  }
  
  return true;  // Include by default
}

// Build dependencies object
function buildDependencies(config) {
  const allDependencies = {
    'vue': '^3.5.13',
    'vue-router': '^4.5.0',
    'vuex': '^4.1.0',
    'axios': '^1.7.9',
    'single-spa-vue': '^3.0.2'  // Conditional
  };
  
  const dependencies = {};
  
  for (const [name, version] of Object.entries(allDependencies)) {
    if (shouldIncludeDependency(name, config)) {
      dependencies[name] = version;
    }
  }
  
  return dependencies;
}

// Usage
const microFrontendDeps = buildDependencies({ is_microfrontend: true });
console.log(microFrontendDeps);
// { vue: '^3.5.13', 'vue-router': '^4.5.0', vuex: '^4.1.0', axios: '^1.7.9', 'single-spa-vue': '^3.0.2' }

const standaloneDeps = buildDependencies({ is_standalone: true, is_microfrontend: false });
console.log(standaloneDeps);
// { vue: '^3.5.13', 'vue-router': '^4.5.0', vuex: '^4.1.0', axios: '^1.7.9' }
// Notice: 'single-spa-vue' is excluded
```

---

## Example 8: Environment Variable Selection

```javascript
// Determine which environment variables to include
function buildEnvVars(config) {
  const allEnvVars = {
    'VITE_ACCESS_MANAGEMENT_BASE_URL': 'http://localhost:8080',
    'VITE_LAUNCHER_APP_URL': 'http://localhost:8088',  // Conditional
    'VITE_DATADOG_ENV': 'local',
    'VITE_DATADOG_APPLICATION_ID': '',
    'VITE_DATADOG_CLIENT_TOKEN': '',
    'VITE_APP_VERSION': '0.1.0'
  };
  
  const envVars = {};
  
  for (const [name, value] of Object.entries(allEnvVars)) {
    // Skip VITE_LAUNCHER_APP_URL for standalone
    if (name === 'VITE_LAUNCHER_APP_URL' && !config.is_microfrontend) {
      continue;
    }
    
    envVars[name] = value;
  }
  
  return envVars;
}

// Usage
const microEnvVars = buildEnvVars({ is_microfrontend: true });
console.log(microEnvVars);
// Includes VITE_LAUNCHER_APP_URL

const standaloneEnvVars = buildEnvVars({ is_standalone: true, is_microfrontend: false });
console.log(standaloneEnvVars);
// Excludes VITE_LAUNCHER_APP_URL
```

---

## Example 9: Validation Function

```javascript
function validateConditionalGeneration(config) {
  const issues = [];
  
  // Check 1: Standalone should not have single-spa
  if (config.is_standalone && config.enable_single_spa) {
    issues.push('Standalone apps should not use single-spa');
    config.enable_single_spa = false;
  }
  
  // Check 2: Micro-frontend requires single-spa
  if (config.is_microfrontend && !config.enable_single_spa) {
    issues.push('Micro-frontend apps require single-spa');
    config.enable_single_spa = true;
  }
  
  // Check 3: Build format matches app type
  if (config.is_microfrontend && config.vite_build_format !== 'system') {
    issues.push('Micro-frontend should use "system" build format');
    config.vite_build_format = 'system';
  }
  
  if (config.is_standalone && config.vite_build_format !== 'es') {
    issues.push('Standalone should use "es" build format');
    config.vite_build_format = 'es';
  }
  
  // Display issues
  if (issues.length > 0) {
    console.warn('\n⚠️  Configuration Auto-Corrections:');
    issues.forEach(issue => console.warn(`   - ${issue}`));
    console.warn('');
  }
  
  return config;
}

// Test Case 1: Invalid standalone config
let config1 = {
  is_standalone: true,
  is_microfrontend: false,
  enable_single_spa: true,
  vite_build_format: 'system'
};

config1 = validateConditionalGeneration(config1);
// Output:
// ⚠️  Configuration Auto-Corrections:
//    - Standalone apps should not use single-spa
//    - Standalone should use "es" build format

console.log(config1);
// { enable_single_spa: false, vite_build_format: 'es', ... }
```

---

## Example 10: Complete Generation Flow

```javascript
async function generateApp(userConfig) {
  // Step 1: Validate and auto-correct
  userConfig = validateConditionalGeneration(userConfig);
  
  // Step 2: Display summary
  console.log('\n' + '─'.repeat(60));
  console.log('  CONDITIONAL FILE GENERATION');
  console.log('─'.repeat(60));
  console.log(`Application Type:  ${userConfig.application_type}`);
  console.log(`Build Format:      ${userConfig.vite_build_format}`);
  console.log(`Single-SPA:        ${userConfig.enable_single_spa ? 'Enabled' : 'Disabled'}`);
  
  // Step 3: Generate files conditionally
  if (shouldGenerateFile('.env.standalone', userConfig)) {
    await generateEnvStandalone(userConfig);
    console.log('  ✓ .env.standalone');
  } else {
    console.log('  ✗ .env.standalone (skipped)');
  }
  
  // Step 4: Generate main.ts with appropriate template
  const mainTemplate = getTemplate('main.ts', userConfig);
  await generateMainEntry(userConfig, mainTemplate);
  console.log(`  ✓ main.ts (${userConfig.is_microfrontend ? 'single-spa' : 'standalone'})`);
  
  // Step 5: Generate package.json with conditional dependencies
  const dependencies = buildDependencies(userConfig);
  await generatePackageJson(userConfig, dependencies);
  console.log('  ✓ package.json');
  
  console.log('─'.repeat(60) + '\n');
}
```

---

## Testing Scenarios

### Test 1: Pure Micro-Frontend
```javascript
const config = {
  application_type: 'micro-frontend',
  enable_single_spa: true
};

// Expected: All micro-frontend files generated
```

### Test 2: Pure Standalone
```javascript
const config = {
  application_type: 'standalone',
  enable_single_spa: false
};

// Expected: No micro-frontend specific files
```

### Test 3: Inconsistent Config (Standalone + single-spa)
```javascript
const config = {
  application_type: 'standalone',
  enable_single_spa: true  // Inconsistent!
};

// Expected: Auto-corrected to enable_single_spa = false
```

### Test 4: Inconsistent Config (Micro-frontend without single-spa)
```javascript
const config = {
  application_type: 'micro-frontend',
  enable_single_spa: false  // Inconsistent!
};

// Expected: Auto-corrected to enable_single_spa = true
```
