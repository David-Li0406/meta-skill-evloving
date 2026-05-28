# Flamework Configuration Reference

Complete guide to setting up and configuring Flamework projects.

## Project Setup

### New Project from Template

```bash
# Create project folder
mkdir my-flamework-game
cd my-flamework-game

# Clone template
npx degit rbxts-flamework/template

# Install dependencies
npm install

# Update to latest
npm i rbxts-transformer-flamework@latest @flamework/core@latest
npm i @flamework/networking@latest @flamework/components@latest
npm i roblox-ts@latest @rbxts/types@latest @rbxts/compiler-types@latest
```

### Existing Project Setup

```bash
# Initialize roblox-ts project
npx rbxtsc init

# Install Flamework
npm i -D rbxts-transformer-flamework
npm i @flamework/core

# Optional modules
npm i @flamework/networking  # For RemoteEvents/RemoteFunctions
npm i @flamework/components  # For component system
```

## tsconfig.json Configuration

### Required Settings

```json
{
  "compilerOptions": {
    // REQUIRED: Enable decorators
    "experimentalDecorators": true,
    
    // REQUIRED: Add Flamework transformer
    "plugins": [
      {
        "transform": "rbxts-transformer-flamework"
      }
    ],
    
    // REQUIRED: Include Flamework types
    "typeRoots": [
      "node_modules/@rbxts",
      "node_modules/@flamework"
    ]
  }
}
```

### Complete Example

```json
{
  "compilerOptions": {
    "outDir": "out",
    "rootDir": "src",
    "baseUrl": "src",
    "declaration": false,
    "module": "commonjs",
    "strict": true,
    "noLib": true,
    "downlevelIteration": true,
    "jsx": "react",
    "jsxFactory": "Roact.createElement",
    "jsxFragmentFactory": "Roact.Fragment",
    "moduleResolution": "Node",
    "resolveJsonModule": true,
    "forceConsistentCasingInFileNames": true,
    "moduleDetection": "force",
    "skipLibCheck": true,
    "allowSyntheticDefaultImports": true,
    
    // Flamework requirements
    "experimentalDecorators": true,
    "plugins": [
      {
        "transform": "rbxts-transformer-flamework",
        // Optional transformer config here
      }
    ],
    "typeRoots": [
      "node_modules/@rbxts",
      "node_modules/@flamework"
    ],
    
    "types": [
      "@rbxts/types",
      "@rbxts/compiler-types"
    ]
  },
  "include": ["src"]
}
```

## default.project.json Configuration

### Required Settings

```json
{
  "name": "my-game",
  "tree": {
    "$className": "DataModel",
    
    "ReplicatedStorage": {
      "$className": "ReplicatedStorage",
      
      "node_modules": {
        "@rbxts": {
          "$path": "node_modules/@rbxts"
        },
        "@flamework": {
          "$path": "node_modules/@flamework"
        }
      }
    },
    
    "ServerScriptService": {
      "$className": "ServerScriptService",
      "TS": {
        "$path": "out/server"
      }
    },
    
    "StarterPlayer": {
      "$className": "StarterPlayer",
      "StarterPlayerScripts": {
        "$className": "StarterPlayerScripts",
        "TS": {
          "$path": "out/client"
        }
      }
    }
  }
}
```

## Transformer Configuration

Advanced options for Flamework's TypeScript transformer in tsconfig.json.

### noSemanticDiagnostics

Disable Flamework's type checking to improve compile times.

```json
{
  "plugins": [
    {
      "transform": "rbxts-transformer-flamework",
      "noSemanticDiagnostics": false  // default
    }
  ]
}
```

**Warning:** Disabling can cause instability if type errors exist.

### obfuscation

Enable ID obfuscation for production builds.

```json
{
  "plugins": [
    {
      "transform": "rbxts-transformer-flamework",
      "obfuscation": false  // default
    }
  ]
}
```

**When enabled:**
- Shortens and randomizes internal IDs
- Randomizes networking names
- Production security measure

### idGenerationMode

Control how Flamework generates internal identifiers.

```json
{
  "plugins": [
    {
      "transform": "rbxts-transformer-flamework",
      "idGenerationMode": "full"  // or "obfuscated", "short", "tiny"
    }
  ]
}
```

**Options:**
- `full` (default without obfuscation) - Readable debug IDs
  - Game: `server/services/myService@MyService`
  - Package: `@rbxts/my-package:server/services/myService@MyService`
  
- `obfuscated` (default with obfuscation) - No debug info
  - Game: `aZx`
  - Package: `@rbxts/my-package:aZx`
  
- `short` - Partial debug info with uniqueness
  - Game: `myService@MyService{aZx}`
  - Package: `@rbxts/my-package:myService@MyService{aZx}`
  
- `tiny` - Minimal debug info
  - Game: `MyService{aZx}`
  - Package: `@rbxts/my-package:MyService{aZx}`

**Use case:** Use `full` in development, `obfuscated` in production.

### hashPrefix

Override package name prefix for ID generation.

```json
{
  "plugins": [
    {
      "transform": "rbxts-transformer-flamework",
      "hashPrefix": "my-custom-prefix"
    }
  ]
}
```

**Default:** Uses package name from package.json

## Runtime Configuration (flamework.json)

Optional runtime behavior configuration file in project root.

### Creating flamework.json

```json
{
  "profiling": true,
  "logLevel": "verbose",
  "disableDependencyWarnings": false
}
```

### profiling

Enable microprofiler tags and memory categories.

```json
{
  "profiling": true  // default in Studio, false in production
}
```

**What it does:**
- Adds microprofiler labels to lifecycle events
- Creates memory categories for debugging
- Helps identify performance bottlenecks

### logLevel

Control Flamework's logging verbosity.

```json
{
  "logLevel": "none"  // or "verbose"
}
```

**Options:**
- `none` (default) - No logging
- `verbose` - Detailed logging

### disableDependencyWarnings

Disable warnings when using Dependency<T>() before ignite.

```json
{
  "disableDependencyWarnings": false  // default
}
```

**Use case:** Set to `true` if you have legitimate pre-ignition dependency usage.

## Project Structure

### Recommended Layout

```
my-flamework-game/
├── src/
│   ├── server/
│   │   ├── runtime.server.ts    # Server entry point
│   │   ├── services/            # Server singletons
│   │   │   ├── player-service.ts
│   │   │   └── data-service.ts
│   │   └── components/          # Server components
│   │       └── npc-component.ts
│   ├── client/
│   │   ├── runtime.client.ts    # Client entry point
│   │   ├── controllers/         # Client singletons
│   │   │   ├── ui-controller.ts
│   │   │   └── input-controller.ts
│   │   └── components/          # Client components
│   │       └── camera-component.ts
│   └── shared/
│       ├── networking.ts        # Shared networking definitions
│       └── types.ts             # Shared types
├── tsconfig.json
├── default.project.json
├── flamework.json              # Optional
└── package.json
```

### Runtime Entry Points

#### runtime.server.ts

```typescript
import { Flamework } from "@flamework/core";

// Preload server code
Flamework.addPaths("src/server/services/");
Flamework.addPaths("src/server/components/");

// Start framework
Flamework.ignite();
```

#### runtime.client.ts

```typescript
import { Flamework } from "@flamework/core";

// Preload client code
Flamework.addPaths("src/client/controllers/");
Flamework.addPaths("src/client/components/");

// Start framework
Flamework.ignite();
```

## Build Scripts

### package.json

```json
{
  "name": "my-flamework-game",
  "version": "1.0.0",
  "scripts": {
    "build": "rbxtsc",
    "watch": "rbxtsc -w",
    "dev": "rbxtsc -w --verbose"
  },
  "devDependencies": {
    "@rbxts/compiler-types": "latest",
    "@rbxts/types": "latest",
    "roblox-ts": "latest",
    "rbxts-transformer-flamework": "latest"
  },
  "dependencies": {
    "@flamework/core": "latest",
    "@flamework/networking": "latest",
    "@flamework/components": "latest"
  }
}
```

### Building

```bash
# One-time build
npm run build

# Watch mode (rebuilds on file change)
npm run watch

# Development mode with verbose output
npm run dev
```

## VSCode Integration

### Recommended Extensions

- **roblox-ts** - Official roblox-ts extension with IntelliSense
- **ESLint** - Linting TypeScript code
- **Prettier** - Code formatting

### .vscode/extensions.json

```json
{
  "recommendations": [
    "roblox-ts.vscode-roblox-ts",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode"
  ]
}
```

### .vscode/settings.json

```json
{
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  }
}
```

## Path Configuration

### Absolute Paths

```typescript
// Relative to project root
Flamework.addPaths("src/server/services/");
Flamework.addPaths("src/client/controllers/");
```

### Relative Paths

```typescript
// Relative to current file (must start with ./)
Flamework.addPaths("./services/");
Flamework.addPaths("../shared/components/");
```

### Glob Patterns

```typescript
// Match all services folders (directories must end with /)
Flamework.addPaths("src/*/services/");

// Deep match
Flamework.addPaths("src/**/services/");

// Using addPathsGlob for files
Flamework.addPathsGlob("src/**/*.service.ts");
```

**Important:** Globs disable relative paths.

## Development Workflow

### 1. Initial Setup
```bash
npm install
npm run build
```

### 2. Development
```bash
# Start watch mode
npm run watch

# Open Roblox Studio
# File > Advanced > Open in Script Editor
# Navigate to your .rbxl file
```

### 3. Testing in Studio
- Watch mode compiles on save
- Refresh place in Studio to see changes
- Use `print()` and Studio output for debugging

### 4. Production Build
```bash
# Enable obfuscation in tsconfig.json
{
  "plugins": [
    {
      "transform": "rbxts-transformer-flamework",
      "obfuscation": true
    }
  ]
}

# Build
npm run build
```

## Migration from Old Versions

### Flamework v1.0+ Migration

If upgrading from pre-v1.0:

1. **Update packages:**
```bash
npm i rbxts-transformer-flamework@latest @flamework/core@latest
npm i @flamework/networking@latest @flamework/components@latest
```

2. **Update addPaths calls:**
```typescript
// Old (v0.x)
Flamework.addPaths({ glob: "directory" }, "path");

// New (v1.0+)
Flamework.addPathsGlob("path/");  // Note trailing slash for directories
```

3. **Update networking:**
```typescript
// Old
const Events = GlobalEvents.server;
const Events = GlobalEvents.client;

// New
const Events = GlobalEvents.createServer({ /* config */ });
const Events = GlobalEvents.createClient({ /* config */ });
```

4. **Remove config from ignite:**
```typescript
// Old
Flamework.ignite({ ... });

// New
Flamework.ignite();  // Config now in flamework.json
```

See [Migration Guide](https://flamework.fireboltofdeath.dev/docs/migration/) for full details.

## Common Issues

**"experimentalDecorators" not enabled**
- Add to tsconfig.json compilerOptions
- Restart VSCode/editor

**"Cannot find module @flamework"**
- Add to typeRoots in tsconfig.json
- Add to default.project.json node_modules
- Run `npm install`

**Transform not running**
- Verify plugin in tsconfig.json
- Delete `out/` directory and rebuild
- Restart watch mode

**Singletons not loading**
- Check Flamework.addPaths() includes directory
- Ensure decorators applied correctly
- Verify no TypeScript errors

**Build performance issues**
- Enable noSemanticDiagnostics (with caution)
- Use incremental compilation
- Exclude test files from build

## Best Practices

1. **Use template** for new projects
2. **Keep flamework.json minimal** - only override what you need
3. **Enable obfuscation** for production builds
4. **Use watch mode** during development
5. **Structure by feature** not by type
6. **Test in Studio** frequently
7. **Version lock** dependencies for stability
8. **Document custom config** in your project README
