---
name: component-refactoring
description: Use this skill to refactor high-complexity React components in the Dify frontend when complexity metrics indicate the need for improvement.
---

# Dify Component Refactoring Skill

Refactor high-complexity React components in the Dify frontend codebase with the patterns and workflow below.

> **Complexity Threshold**: Components with complexity > 50 (measured by `pnpm analyze-component`) should be refactored before testing.

## Quick Reference

### Commands (run from `web/`)

Use paths relative to `web/` (e.g., `app/components/...`). Use `refactor-component` for refactoring prompts and `analyze-component` for testing prompts and metrics.

```bash
cd web

# Generate refactoring prompt
pnpm refactor-component <path>

# Output refactoring analysis as JSON
pnpm refactor-component <path> --json

# Generate testing prompt (after refactoring)
pnpm analyze-component <path>

# Output testing analysis as JSON
pnpm analyze-component <path> --json
```

### Complexity Analysis

```bash
# Analyze component complexity
pnpm analyze-component <path> --json

# Key metrics to check:
# - complexity: normalized score 0-100 (target < 50)
# - maxComplexity: highest single function complexity
# - lineCount: total lines (target < 300)
```

### Complexity Score Interpretation

| Score  | Level           | Action                      |
| ------ | --------------- | --------------------------- |
| 0-25   | 🟢 Simple       | Ready for testing           |
| 26-50  | 🟡 Medium       | Consider minor refactoring  |
| 51-75  | 🟠 Complex      | **Refactor before testing** |
| 76-100 | 🔴 Very Complex | **Must refactor**           |

## Core Refactoring Patterns

### Pattern 1: Extract Custom Hooks

**When**: Component has complex state management, multiple `useState`/`useEffect`, or business logic mixed with UI.

**Dify Convention**: Place hooks in a `hooks/` subdirectory or alongside the component as `use-<feature>.ts`.

```typescript
// ❌ Before: Complex state logic in component
const Configuration: FC = () => {
  const [modelConfig, setModelConfig] = useState<ModelConfig>(...)
  const [datasetConfigs, setDatasetConfigs] = useState<DatasetConfigs>(...)
  const [completionParams, setCompletionParams] = useState<FormValue>({})
  
  // 50+ lines of state management logic...
  
  // Refactor this logic into custom hooks
}
```