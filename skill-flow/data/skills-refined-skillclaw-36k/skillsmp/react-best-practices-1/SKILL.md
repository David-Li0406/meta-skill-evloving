---
name: react-best-practices
description: React 开发最佳实践指南，涵盖组件设计、Hooks 使用、状态管理及性能优化。
---

# React Best Practices

## 🌟 技能核心：编写可维护的 React 代码
本技能旨在指导开发者编写**清晰、高性能、可扩展**的 React 应用。
**核心原则**：声明式编程、组件化思维、单一职责、不可变性。

## 🧠 Core Principles (核心原则)

### 1. 组件设计 (Component Design)
- **Small & Focused**: 每个组件只做一件事。如果组件超过 200 行，考虑拆分。
- **Composition**: 优先使用组合（Composition）而非继承。使用 `children` prop 或 render props 来复用逻辑。
- **Presentational vs Container**: 区分展示组件（只负责 UI）和容器组件（负责数据和逻辑），尽管 Hooks 让界限模糊，但分离关注点依然重要。

### 2. Hooks 最佳实践
- **Rules of Hooks**: 只在顶层调用 Hooks，不要在循环、条件或嵌套函数中调用。
- **Custom Hooks**: 将复杂的逻辑抽取为自定义 Hook (e.g., `useWindowSize`, `useAuth`)，保持组件整洁。
- **Dependency Arrays**: 诚实地填写 `useEffect` 和 `useCallback` 的依赖数组。如果依赖项导致无限循环，解决依赖问题而不是撒谎（例如使用 `useRef` 或重构逻辑）。

### 3. 状态管理 (State Management)
- **Lift State Up**: 将状态提升到最近的共同祖先。
- **Server State vs Client State**: 使用 React Query (TanStack Query) 或 SWR 管理服务端数据，不要用 Redux/Context 存 API 数据。
- **Context API**: 仅用于低频更新的全局数据（如主题、用户信息），避免高频更新导致全树重渲染。
- **Global State**: 对于复杂的客户端状态，推荐使用 Zustand 或 Jotai，比 Redux 更轻量且 boilerplate 更少。

## 🚫 反模式 (Anti-Patterns)
- ❌ **Prop Drilling**: 层层传递 props 超过 3 层。解决方案：Context 或组合 (Component Composition)。
- ❌ **Effect for Derived State**: 在 `useEffect` 中根据 props 更新 state。解决方案：直接在渲染期间计算，或使用 `useMemo`。
- ❌ **Index as Key**: 在列表渲染中使用数组索引作为 `key`（除非列表是静态且不重排的）。
- ❌ **Huge useEffect**: 一个 `useEffect` 处理多个不相关的逻辑。解决方案：拆分为多个单一职责的 `useEffect`。
- ❌ **Stale Closures**: 在 `useEffect` 或 `useCallback` 中引用了旧的 state/props，通常是因为依赖数组不完整。

## ⚡ 性能优化 (Performance)
- **Code Splitting**: 使用 `React.lazy` and `Suspense` 对路由或大型组件进行懒加载。
- **Memoization**: 使用 `React.memo` 避免不必要的子组件重渲染（仅当 props 引用变化时）。使用 `useMemo` 缓存昂贵的计算。
- **Virtualization**: 对于长列表，使用 `react-window` 或 `react-virtuoso` 进行虚拟滚动。

## 🛠️ 技术栈与工具推荐
- **Framework**: Next.js (App Router) 或 Vite.
- **Styling**: Tailwind CSS (推荐), CSS Modules, 或 Styled Components.
- **State**: Zustand (Client), React Query (Server).
- **Form**: React Hook Form + Zod (Validation).
- **Testing**: Vitest + React Testing Library.

## 🎨 常用指令示例
```bash
# 优化组件性能
/react-coder 优化这个组件的渲染性能，检查是否有不必要的重渲染，并应用 useMemo 或 React.memo。

# 重构为自定义 Hook
/react-coder 将这个组件中的数据获取和表单逻辑提取为单独的自定义 Hooks。

# 审查代码质量
/react-coder 检查这段代码是否违反了 React 最佳实践，特别是 useEffect 的依赖和状态管理方面。
```
