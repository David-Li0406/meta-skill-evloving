# Architecture Anti-Patterns (架构反模式)

> 严禁触犯以下红线。

## 1. 状态管理反模式

### ❌ 手动同步 Server State 到 Client Store
```typescript
// BAD
const { data } = useQuery(...)
useEffect(() => {
  setStoreData(data) // ❌ 多余的同步，导致双重真理来源
}, [data])

// GOOD
const { data } = useQuery(...) // ✅ 直接使用 data
```

### ❌ Store 解构
```typescript
// BAD - 任何 state 变化都会触发重渲染
const { count, inc } = useStore()

// GOOD -只监听 count 变化
const count = useStore(s => s.count)
const inc = useStore(s => s.inc)
```

## 2. API 与异步反模式

### ❌ 裸奔的 Fetch
没有 Zod 校验的 API 调用是类型不安全的源头。
**必须**使用 `YourSchema.parse(response)` 确保运行时安全。

### ❌ `catch (error: any)`
TypeScript 4.4+ 默认 error 为 unknown。
**必须**检查类型或断言：
```typescript
if (error instanceof Error) { ... }
```

## 3. 结构反模式

### ❌ 循环依赖 (Circular Dependency)
Feature A 引用 Feature B，Feature B 引用 Feature A。
**解法**: 提取公共部分到 `src/features/shared` 或 `src/lib`。

### ❌ 深度穿透 (Prop Drilling) > 3 层
超过 3 层的 Prop 传递。
**解法**: 使用 Context 或 Composition (Slot pattern)。
