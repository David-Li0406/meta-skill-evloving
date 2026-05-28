# TypeScript

**Category**: languages
**Description**: TypeScript programming language - JavaScript with static typing, developed by Microsoft
**Homepage**: https://www.typescriptlang.org

---

## TIER 1: Quick Detection (SBOM-based)

These patterns are used during quick scans that only analyze the SBOM.

### Package Detection

#### NPM
- `typescript` - TypeScript compiler
- `ts-node` - TypeScript execution for Node.js
- `tsx` - TypeScript execute (esbuild-based)
- `@types/node` - Node.js type definitions
- `@typescript-eslint/parser` - TypeScript ESLint parser
- `@typescript-eslint/eslint-plugin` - TypeScript ESLint rules
- `ts-loader` - TypeScript loader for webpack
- `ts-jest` - TypeScript Jest transformer
- `tslib` - TypeScript runtime helpers
- `ttypescript` - Transformer-enabled TypeScript compiler

---

## TIER 2: Deep Detection (File-based)

These patterns require scanning repository files and take longer to run.

### File Extensions
*Presence of these extensions indicates TypeScript usage*

- `.ts` - TypeScript source files
- `.tsx` - TypeScript React (JSX) files
- `.mts` - TypeScript ES module files
- `.cts` - TypeScript CommonJS files
- `.d.ts` - TypeScript declaration files
- `.d.mts` - ES module declaration files
- `.d.cts` - CommonJS declaration files

### Configuration Files
*Known configuration files that indicate TypeScript*

- `tsconfig.json` - Main TypeScript configuration (strong indicator)
- `tsconfig.*.json` - Extended TypeScript configurations
- `tsconfig.build.json` - Build-specific configuration
- `tsconfig.node.json` - Node-specific configuration
- `tsconfig.app.json` - Application configuration
- `tsconfig.spec.json` - Test configuration
- `.ts-node` - ts-node configuration directory

### Import Patterns

#### TypeScript
Extensions: `.ts`, `.tsx`, `.mts`, `.cts`

**Pattern**: `import\s+.*\s+from\s+['"]`
- ES module import
- Example: `import { Component } from '@angular/core';`

**Pattern**: `import\s+type\s+\{`
- Type-only named import
- Example: `import type { User } from './types';`

**Pattern**: `import\s+type\s+\w+\s+from`
- Type-only default import
- Example: `import type User from './types';`

**Pattern**: `export\s+type\s+\{`
- Type-only export
- Example: `export type { User, Post };`

**Pattern**: `export\s+type\s+\w+\s*=`
- Type alias export
- Example: `export type ID = string | number;`

### Code Patterns
*TypeScript-specific code patterns*

**Pattern**: `:\s*(string|number|boolean|object|any|void|never|unknown|null|undefined|bigint|symbol)\b`
- Primitive type annotations
- Example: `function greet(name: string): void {}`

**Pattern**: `:\s*\w+(\[\]|\<[^>]+\>)`
- Generic or array type annotations
- Example: `const items: string[] = [];`

**Pattern**: `interface\s+\w+`
- Interface declaration
- Example: `interface User { name: string; }`

**Pattern**: `type\s+\w+\s*=`
- Type alias declaration
- Example: `type ID = string | number;`

**Pattern**: `<[A-Z]\w*>`
- Generic type parameter
- Example: `function identity<T>(arg: T): T {}`

**Pattern**: `as\s+const\b`
- Const assertion
- Example: `const colors = ['red', 'blue'] as const;`

**Pattern**: `as\s+\w+`
- Type assertion
- Example: `const element = document.getElementById('app') as HTMLDivElement;`

**Pattern**: `!\s*[;,\)]`
- Non-null assertion
- Example: `const value = maybeNull!;`

**Pattern**: `\?\s*:`
- Optional property/parameter
- Example: `function greet(name?: string) {}`

**Pattern**: `readonly\s+\w+`
- Readonly modifier
- Example: `readonly name: string;`

**Pattern**: `private\s+\w+|protected\s+\w+|public\s+\w+`
- Access modifiers
- Example: `private count: number;`

**Pattern**: `abstract\s+(class|method)`
- Abstract declaration
- Example: `abstract class Animal {}`

**Pattern**: `implements\s+\w+`
- Interface implementation
- Example: `class Dog implements Animal {}`

**Pattern**: `enum\s+\w+`
- Enum declaration
- Example: `enum Color { Red, Green, Blue }`

**Pattern**: `namespace\s+\w+`
- Namespace declaration
- Example: `namespace MyAPI {}`

**Pattern**: `declare\s+(const|let|var|function|class|module|namespace)`
- Ambient declaration
- Example: `declare const process: NodeJS.Process;`

---

## Environment Variables

- `TS_NODE_PROJECT` - Custom tsconfig for ts-node
- `TS_NODE_COMPILER_OPTIONS` - Compiler options for ts-node
- `TS_NODE_TRANSPILE_ONLY` - Skip type checking
- `TS_NODE_FILES` - Load files from tsconfig
- `TS_NODE_IGNORE` - Regex patterns to skip
- `TSC_COMPILE_ON_ERROR` - Continue on errors (CRA)

## Detection Notes

- `tsconfig.json` is the strongest indicator of TypeScript usage
- `.ts` and `.tsx` file extensions are definitive
- `@types/*` packages indicate TypeScript type definitions
- Type annotations (`: Type`) are unique to TypeScript
- Interfaces and type aliases are TypeScript constructs
- Modern React projects often use TypeScript (`.tsx`)
- Can be detected alongside JavaScript in same project
