# Roblox-TS Setup Reference

Complete guide to installing, configuring, and structuring roblox-ts projects.

## Installation

### Prerequisites

- **Node.js** 18+ and npm
- **Roblox Studio**
- **Git** (recommended)

### Global Installation

```bash
# Install roblox-ts compiler globally
npm install -g roblox-ts

# Verify installation
rbxtsc --version
```

### Project Installation

```bash
# Create new project directory
mkdir my-roblox-game
cd my-roblox-game

# Initialize roblox-ts project
npx rbxtsc init

# Install dependencies
npm install
```

## Project Structure

### Default Structure

```
my-roblox-game/
├── src/
│   ├── server/
│   │   └── main.server.ts      # Server entry point
│   ├── client/
│   │   └── main.client.ts      # Client entry point
│   └── shared/
│       └── module.ts            # Shared code
├── out/                         # Compiled Luau (gitignored)
├── include/                     # Static assets
├── node_modules/                # Dependencies
├── default.project.json         # Rojo project file
├── tsconfig.json               # TypeScript config
└── package.json                # npm config
```

### Recommended Structure (Feature-Based)

```
src/
├── server/
│   ├── main.server.ts
│   ├── services/               # Server singletons
│   │   ├── player-service.ts
│   │   └── data-service.ts
│   └── features/
│       └── combat/
│           ├── combat-manager.ts
│           └── weapons.ts
├── client/
│   ├── main.client.ts
│   ├── controllers/            # Client singletons
│   │   ├── ui-controller.ts
│   │   └── input-controller.ts
│   └── features/
│       └── inventory/
│           ├── inventory-ui.tsx
│           └── inventory-manager.ts
└── shared/
    ├── types.ts                # Shared type definitions
    ├── constants.ts            # Game constants
    ├── remotes.ts              # Remote definitions
    └── utils/
        └── math-utils.ts
```

## Configuration Files

### tsconfig.json

Complete configuration with comments:

```json
{
  "compilerOptions": {
    // Output
    "outDir": "out",
    "rootDir": "src",
    
    // Module resolution
    "module": "commonjs",
    "moduleResolution": "Node",
    "resolveJsonModule": true,
    
    // Type checking
    "strict": true,
    "noLib": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    
    // Language features
    "downlevelIteration": true,
    "jsx": "react",
    "jsxFactory": "Roact.createElement",
    "jsxFragmentFactory": "Roact.Fragment",
    
    // Types
    "types": [
      "@rbxts/types",
      "@rbxts/compiler-types"
    ],
    "typeRoots": [
      "node_modules/@rbxts"
    ],
    
    // Advanced
    "declaration": false,
    "allowSyntheticDefaultImports": true,
    "moduleDetection": "force"
  },
  
  "include": ["src"],
  "exclude": ["node_modules", "out"]
}
```

### Configuration Options Explained

**outDir / rootDir:**
- `outDir`: Where compiled Luau files are written
- `rootDir`: Where TypeScript source files are located

**module / moduleResolution:**
- `module: "commonjs"`: Use CommonJS module system
- `moduleResolution: "Node"`: Resolve modules like Node.js

**strict:**
- Enables all strict type checking options
- Highly recommended for type safety

**noLib:**
- Don't include standard TypeScript libraries
- Required for roblox-ts (Roblox API instead)

**downlevelIteration:**
- Enables for-of loops and spread operators
- Required for array iteration

**jsx:**
- `jsx: "react"`: Enable JSX syntax
- `jsxFactory`: Function to transform JSX (Roact)
- `jsxFragmentFactory`: Function for fragments

**types / typeRoots:**
- `types`: Explicitly include type packages
- `typeRoots`: Where to find type definitions

### default.project.json (Rojo)

Basic Rojo configuration:

```json
{
  "name": "MyGame",
  "tree": {
    "$className": "DataModel",
    
    "ReplicatedStorage": {
      "$className": "ReplicatedStorage",
      
      "rbxts_include": {
        "$path": "include",
        "node_modules": {
          "$path": "node_modules/@rbxts"
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

### Advanced Rojo Configuration

With shared code and StarterGui:

```json
{
  "name": "MyGame",
  "tree": {
    "$className": "DataModel",
    
    "ReplicatedStorage": {
      "$className": "ReplicatedStorage",
      
      "rbxts_include": {
        "$path": "include",
        "node_modules": {
          "$path": "node_modules/@rbxts"
        }
      },
      
      "TS": {
        "$path": "out/shared"
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
    },
    
    "StarterGui": {
      "$className": "StarterGui",
      "$path": "place-file/StarterGui"
    }
  }
}
```

### package.json

Essential configuration:

```json
{
  "name": "my-roblox-game",
  "version": "1.0.0",
  "description": "A Roblox game written in TypeScript",
  "main": "out/init.lua",
  "scripts": {
    "build": "rbxtsc",
    "watch": "rbxtsc -w",
    "dev": "rbxtsc -w --verbose"
  },
  "keywords": ["roblox", "roblox-ts"],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@rbxts/compiler-types": "^2.0.0",
    "@rbxts/types": "^1.0.0",
    "roblox-ts": "^2.0.0"
  },
  "dependencies": {
    "@rbxts/services": "^1.5.1"
  }
}
```

## Essential Packages

### Core Packages

```bash
# Type definitions (required)
npm install @rbxts/types @rbxts/compiler-types

# Roblox services (highly recommended)
npm install @rbxts/services
```

### Recommended Packages

```bash
# UI framework
npm install @rbxts/roact @rbxts/roact-hooked

# Type validation
npm install @rbxts/t

# Remote events
npm install @rbxts/remo
# or
npm install @rbxts/net

# Utilities
npm install @rbxts/object-utils
npm install @rbxts/string-utils
```

## Development Workflow

### Build Commands

```bash
# Build once
npx rbxtsc

# Watch mode (recommended for development)
npx rbxtsc -w

# Verbose output (for debugging)
npx rbxtsc -w --verbose

# Type checking only (no emit)
npx rbxtsc --noEmit

# Production build
npx rbxtsc --production
```

### Watch Mode

Watch mode automatically rebuilds when files change:

```bash
# Start watch mode
npx rbxtsc -w

# Output:
# [12:00:00 PM] Starting compilation in watch mode...
# [12:00:02 PM] Found 0 errors. Watching for file changes.
```

### Using with Rojo

```bash
# Terminal 1: TypeScript compiler
npx rbxtsc -w

# Terminal 2: Rojo serve
rojo serve default.project.json

# In Roblox Studio:
# Plugins -> Rojo -> Connect
```

### VSCode Integration

**.vscode/settings.json:**
```json
{
  "typescript.tsdk": "node_modules/typescript/lib",
  "typescript.enablePromptUseWorkspaceTsdk": true,
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true
  },
  "files.exclude": {
    "**/*.lua": true,
    "out/": true
  }
}
```

**.vscode/tasks.json:**
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Watch",
      "type": "shell",
      "command": "npx rbxtsc -w",
      "problemMatcher": "$tsc-watch",
      "isBackground": true,
      "group": {
        "kind": "build",
        "isDefault": true
      }
    }
  ]
}
```

### Recommended VSCode Extensions

```json
{
  "recommendations": [
    "roblox-ts.vscode-roblox-ts",
    "evaera.vscode-rojo",
    "sumneko.lua",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode"
  ]
}
```

## Project Templates

### Template from GitHub

```bash
# Use roblox-ts game template
npx degit roblox-ts/template my-game
cd my-game
npm install
```

### Custom Template Structure

Create your own template:

```
my-template/
├── src/
│   ├── server/
│   │   ├── main.server.ts
│   │   └── services/
│   ├── client/
│   │   ├── main.client.ts
│   │   └── controllers/
│   └── shared/
│       ├── types.ts
│       └── remotes.ts
├── .vscode/
│   ├── settings.json
│   ├── extensions.json
│   └── tasks.json
├── .gitignore
├── default.project.json
├── tsconfig.json
└── package.json
```

## Git Configuration

**.gitignore:**
```
# roblox-ts
out/
*.lua

# Node
node_modules/
npm-debug.log*

# Roblox
*.rbxl.lock
*.rbxlx.lock

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/settings.json
.idea/
```

## Environment Setup

### Multiple Environments

**tsconfig.development.json:**
```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "sourceMap": true
  }
}
```

**tsconfig.production.json:**
```json
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "removeComments": true,
    "declaration": false
  }
}
```

**Build scripts:**
```json
{
  "scripts": {
    "build:dev": "rbxtsc -p tsconfig.development.json",
    "build:prod": "rbxtsc -p tsconfig.production.json",
    "watch": "rbxtsc -w -p tsconfig.development.json"
  }
}
```

## Troubleshooting Setup

**rbxtsc not found:**
- Install globally: `npm install -g roblox-ts`
- Or use npx: `npx rbxtsc`

**Module resolution errors:**
- Check `moduleResolution: "Node"` in tsconfig.json
- Verify `node_modules/@rbxts` exists
- Run `npm install`

**Types not found:**
- Install: `npm install @rbxts/types @rbxts/compiler-types`
- Check `types` array in tsconfig.json

**Rojo not syncing compiled files:**
- Check `outDir` in tsconfig.json matches Rojo paths
- Verify Rojo is serving correct project file
- Restart Rojo serve

**Watch mode not detecting changes:**
- Check file is inside `rootDir`
- Restart watch mode
- Check file isn't in `exclude` array

## Best Practices

1. **Use watch mode** during development for instant feedback
2. **Structure by feature** not by file type
3. **Keep tsconfig strict** - don't disable type checking
4. **Use npm scripts** for consistent commands
5. **Version control** - commit package-lock.json
6. **Separate environments** - different configs for dev/prod
7. **Document setup** - README.md with setup instructions
8. **Use templates** - Create project templates for consistency
