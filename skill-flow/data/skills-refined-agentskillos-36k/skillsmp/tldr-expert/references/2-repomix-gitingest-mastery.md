# Reference: Repomix & Gitingest Mastery

## 📦 Tool 1: Repomix
Repomix is the primary tool for creating "Context Snapshots."

### Recommended Configuration (`repomix.config.json`)
```json
{
  "output": {
    "filePath": "repomix-output.xml",
    "style": "xml",
    "removeComments": true,
    "removeEmptyLines": true,
    "showLineNumbers": true
  },
  "include": ["src/**/*"],
  "ignore": {
    "customPatterns": ["**/*.test.ts", "**/dist/**", "**/docs/**"]
  }
}
```

### ⚡ Power Command: Signatures Only
Use this to understand a huge module without hitting token limits.
`repomix --include "src/huge-module/**" --no-code-bodies`

---

## 🍯 Tool 2: Gitingest
Gitingest is best for "Quick Forensics" on remote repositories or local sub-directories.

### Key Use Cases:
1.  **Dependency Discovery:** Point Gitingest at a library's GitHub URL to understand its API.
2.  **Architecture Review:** Use Gitingest's summary output to get a tree view and file-size breakdown.

### The "Squaads Digest" Command
`gitingest . --exclude "node_modules,dist,build" --max-size 1mb --output digest.txt`

---

## 🛠️ Tool 3: Tree-sitter Signatures
The TLDR Expert uses Tree-sitter (often via `llm-tldr`) to extract just the "Shape" of the code.

```typescript
// Example Tree-sitter extraction (Conceptual)
export function calculateTax(amount: number): number;
export class TaxEngine {
  constructor(config: Config);
  process(item: Item): Result;
}
```
*Note: This gives the AI the "What" without the "How", saving thousands of tokens.*
