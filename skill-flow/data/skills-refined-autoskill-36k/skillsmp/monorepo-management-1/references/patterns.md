# Monorepo Management

## Patterns

### **Turborepo Setup**
  #### **Description**
Turborepo with pnpm
  #### **Example**
    // turbo.json
    {
      "$schema": "https://turbo.build/schema.json",
      "tasks": {
        "build": {
          "dependsOn": ["^build"],
          "outputs": ["dist/**", ".next/**"]
        },
        "dev": {
          "cache": false,
          "persistent": true
        },
        "lint": {
          "dependsOn": ["^build"]
        },
        "test": {
          "dependsOn": ["build"]
        }
      }
    }
    
    // pnpm-workspace.yaml
    packages:
      - "apps/*"
      - "packages/*"
    
    // package.json (root)
    {
      "name": "monorepo",
      "scripts": {
        "build": "turbo build",
        "dev": "turbo dev",
        "lint": "turbo lint",
        "test": "turbo test"
      },
      "devDependencies": {
        "turbo": "^2.0.0"
      }
    }
    
### **Package Structure**
  #### **Description**
Monorepo package organization
  #### **Example**
    monorepo/
      apps/
        web/                 # Next.js app
          package.json
        api/                 # API server
          package.json
      packages/
        ui/                  # Shared UI components
          package.json
          src/
            Button.tsx
            index.ts
        config-eslint/       # Shared ESLint config
          package.json
        config-typescript/   # Shared tsconfig
          package.json
        database/            # Database client/schema
          package.json
      turbo.json
      pnpm-workspace.yaml
      package.json
    
### **Shared Package**
  #### **Description**
Creating shared packages
  #### **Example**
    // packages/ui/package.json
    {
      "name": "@repo/ui",
      "version": "0.0.0",
      "private": true,
      "main": "./src/index.ts",
      "types": "./src/index.ts",
      "exports": {
        ".": "./src/index.ts",
        "./button": "./src/Button.tsx"
      },
      "scripts": {
        "build": "tsc",
        "lint": "eslint src/"
      },
      "peerDependencies": {
        "react": "^18.0.0"
      },
      "devDependencies": {
        "@repo/config-typescript": "workspace:*",
        "typescript": "^5.0.0"
      }
    }
    
    // packages/ui/src/index.ts
    export { Button } from "./Button";
    export { Card } from "./Card";
    
    // apps/web/package.json
    {
      "dependencies": {
        "@repo/ui": "workspace:*"
      }
    }
    
    // apps/web/src/app/page.tsx
    import { Button } from "@repo/ui";
    
### **Remote Caching**
  #### **Description**
Turborepo remote caching
  #### **Example**
    // Enable Vercel Remote Cache
    npx turbo login
    npx turbo link
    
    // Or self-hosted with turbo-remote-cache
    // turbo.json
    {
      "remoteCache": {
        "signature": true
      }
    }
    
    // CI environment
    TURBO_TOKEN=xxx
    TURBO_TEAM=your-team
    

## Anti-Patterns

### **Circular Deps**
  #### **Description**
Circular dependencies between packages
  #### **Wrong**
Package A imports B, B imports A
  #### **Right**
Extract shared code to package C
### **Version Mismatch**
  #### **Description**
Different versions of same dependency
  #### **Wrong**
React 18 in app, React 17 in package
  #### **Right**
Single version in root, workspace:* for internal
### **No Caching**
  #### **Description**
Not using task caching
  #### **Wrong**
Rebuilding everything on every CI run
  #### **Right**
Configure outputs, use remote cache