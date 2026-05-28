# 项目规则: needs-connect-app

## 🏗 架构与模式 (Architecture & Patterns)
- **Composable/Hook Pattern**: Logic reuse via Vue 3 Composition API. Naming: use{FeatureName}. Return: Object containing refs, computed, and functions.
- **API Hooks**: Data fetching logic encapsulated in use{Resource}Api hooks.
- **Modal Management**: Modal state and logic in use{Feature}Modal.

## 🎨 编码规范 (Coding Standards)
- **Imports**: Use @/ for project root alias.
- **Language**: TypeScript with explicit types.

## 🚫 红线 (Blockers)
- **No Chinese Comments**: Strict adherence to English/Japanese comments.
- **No console.log**: Remove debug logs.
- **No any**: Avoid any type, use specific interfaces.