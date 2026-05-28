# KISS Checklist (Keep It Simple, Stupid)

> 在设计与实现前，必须通过此检查。

## 1. 复杂度奥卡姆剃刀

- [ ] **是否真的需要新目录？**
  - 如果只有 1 个组件，放在 `components/ui` 或 `features/shared` 即可。
  - 不要为了 future proofing 而过度分层。

- [ ] **状态是否放置正确？**
  - 能用 URL 参数解决的，不用 State。
  - 能用 React Query 解决的，不用 Zustand。
  - 能用 Local State (useState) 解决的，不用 Global。

- [ ] **依赖最小化**
  - 不要为了一个简单的 `formatDate` 引入 `date-fns` (如果只用一次)。
  - 不要为了简单的动画引入 `framer-motion` (CSS Transition 优先)。

## 2. 代码量警报

- [ ] **单个文件 < 300 行**
  - 超过则拆分，但不要为了拆分而拆分（保持逻辑内聚）。

- [ ] **单个函数 < 50 行**
  - 提取子逻辑为 pure functions。

## 3. 认知负担

- [ ] **命名即文档**
  - 变量名应描述内容，动词+名词。
  - 避免 `handle1`, `data2` 这种命名。
  - 复杂逻辑必须有 `JSDoc` 或行内注释。
