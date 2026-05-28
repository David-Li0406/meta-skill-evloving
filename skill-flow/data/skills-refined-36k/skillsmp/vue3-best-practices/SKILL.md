---
name: vue3-best-practices
description: Vue 3 开发最佳实践指南，涵盖 Composition API, Script Setup, Pinia, TypeScript 集成及性能优化。
---

# Vue 3 Best Practices

## 🌟 技能核心

本技能指导开发者编写 **模块化、类型安全、高性能** 的 Vue 3 应用。

**核心原则**：
- Composition API First
- 逻辑复用 (Composables)
- 类型推导优先
- 单一数据流

---

## 📁 推荐项目结构

```
src/
├── assets/              # 静态资源
├── components/          # 通用组件
│   ├── ui/              # 基础 UI 组件
│   └── business/        # 业务组件
├── composables/         # 组合式函数 (use*.ts)
├── stores/              # Pinia stores
├── views/               # 页面组件
├── router/              # 路由配置
├── types/               # TypeScript 类型定义
├── utils/               # 工具函数
├── api/                 # API 请求封装
└── App.vue
```

**命名规范**：
| 类型 | 规范 | 示例 |
|------|------|------|
| 组件 | PascalCase | `UserProfile.vue` |
| Composables | camelCase + use 前缀 | `useAuth.ts` |
| Stores | camelCase + Store 后缀 | `userStore.ts` |
| 工具函数 | camelCase | `formatDate.ts` |

---

## 🧠 核心原则

### 1. Script Setup 与 Composition API

```vue
<script setup lang="ts">
// ✅ 推荐：显式导入，利于代码阅读和依赖追踪
import { ref, computed, watch, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'

// 顶层 await 支持
const data = await fetchInitialData()

// 响应式状态
const count = ref(0)
const doubled = computed(() => count.value * 2)

// Store 使用
const userStore = useUserStore()
</script>
```

**要点**：
- 默认使用 `<script setup lang="ts">`，更简洁，运行时性能更好
- 支持顶层 `await`
- 显式导入 `ref`, `computed`, `watch` 等（而非依赖自动导入）

### 2. 响应式数据 (Reactivity)

| 场景 | 推荐 | 原因 |
|------|------|------|
| 基本类型 | `ref` | 清晰的 `.value` 访问 |
| 对象/数组（默认） | `reactive` | 更直观；解构需 `toRefs` |
| 需要整体替换/可空对象 | `ref` | 便于赋新对象与类型约束 |
| 深层嵌套大对象 | `reactive` | 仅当不解构时使用 |
| 大型外部实例 | `shallowRef` | 避免不必要的深度响应 |

```typescript
// ✅ 推荐
const user = ref<User | null>(null)
user.value = { name: 'John' }

// ⚠️ 谨慎使用 reactive
const state = reactive({ items: [] })
// 解构会丢失响应性！
const { items } = state // ❌ items 不再是响应式

// ✅ 使用 toRefs 解构
const { items } = toRefs(state)
```

### 3. 组件通信

#### Props 定义（带默认值）

```typescript
// Vue 3.5+ 推荐写法
const { title, count = 0 } = defineProps<{
  title: string
  count?: number
}>()

// Vue 3.4 及以下
const props = withDefaults(defineProps<{
  title: string
  count?: number
}>(), {
  count: 0
})
```

**注意**：解构式 props 需要 Vue 3.5+（或编译选项 `propsDestructure: true`）。否则解构结果非响应式，建议使用 `withDefaults` 或保留 `props.xxx` 访问。

#### Emits 定义

```typescript
const emit = defineEmits<{
  change: [id: number]
  update: [value: string]
}>()

// 使用
emit('change', 123)
```

#### v-model（Vue 3.4+）

```typescript
// 简化双向绑定
const modelValue = defineModel<string>()
const count = defineModel<number>('count', { default: 0 })
```

#### Slots 类型化

```typescript
defineSlots<{
  default: (props: { item: Item }) => any
  header: () => any
}>()
```

#### Expose

```typescript
// 暴露给父组件的方法/属性
defineExpose({
  focus: () => inputRef.value?.focus(),
  reset
})
```

### 4. 组件命名 (defineOptions)

递归组件、调试、DevTools 中必须显式命名：

```typescript
defineOptions({
  name: 'TreeNode',      // 递归组件必须
  inheritAttrs: false    // 禁用属性自动透传
})
```

**何时需要命名**：
| 场景 | 必要性 |
|------|--------|
| 递归组件 | ⭐ 必须 |
| DevTools 调试 | 推荐 |
| KeepAlive include/exclude | 必须 |
| Transition 组件 | 推荐 |

### 5. 属性透传 (inheritAttrs)

```vue
<script setup lang="ts">
defineOptions({ inheritAttrs: false })

// 获取透传的属性
const attrs = useAttrs()
</script>

<template>
  <!-- 手动绑定到内部元素 -->
  <div class="wrapper">
    <input v-bind="attrs" />
  </div>
</template>
```

### 6. 泛型组件（Vue 3.3+）

```vue
<script setup lang="ts" generic="T extends { id: number }">
defineProps<{
  items: T[]
  selected?: T
}>()

const emit = defineEmits<{
  select: [item: T]
}>()
</script>
```

---

## 🧩 逻辑复用 (Composables)

### 基本模式

```typescript
// composables/useCounter.ts
import { ref, computed } from 'vue'

export function useCounter(initial = 0) {
  const count = ref(initial)
  const doubled = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  function reset() {
    count.value = initial
  }

  return {
    count,
    doubled,
    increment,
    reset
  }
}
```

### 带异步请求的 Composable

```typescript
// composables/useFetch.ts
import { ref, shallowRef, watchEffect, toValue, type MaybeRefOrGetter } from 'vue'

export function useFetch<T>(url: MaybeRefOrGetter<string>) {
  const data = shallowRef<T | null>(null)
  const error = shallowRef<Error | null>(null)
  const loading = ref(false)

  async function execute() {
    loading.value = true
    error.value = null
    try {
      const res = await fetch(toValue(url))
      data.value = await res.json()
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  watchEffect(() => {
    execute()
  })

  return { data, error, loading, refresh: execute }
}
```

**注意**：`MaybeRefOrGetter`/`toValue` 需要 Vue 3.3+。低版本可用 `unref` 或改为仅接收 `Ref`。

**最佳实践**：
- ✅ 以 `use` 开头命名
- ✅ 返回对象包含响应式状态和方法
- ✅ 优先使用 [VueUse](https://vueuse.org/) 已有工具
- ❌ 不要在 Composable 中使用 `this`

---

## 📦 状态管理 (Pinia)

### Setup Store（推荐）

```typescript
// stores/userStore.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref('')

  // Getters
  const isLoggedIn = computed(() => !!token.value)
  const displayName = computed(() => user.value?.name ?? 'Guest')

  // Actions
  async function login(credentials: LoginDTO) {
    const res = await api.login(credentials)
    user.value = res.user
    token.value = res.token
  }

  function logout() {
    user.value = null
    token.value = ''
  }

  return {
    user,
    token,
    isLoggedIn,
    displayName,
    login,
    logout
  }
})
```

**要点**：
- 优先使用 Setup Store，与组件写法一致
- State 保持扁平化
- Getters = computed
- Actions 处理同步/异步逻辑

---

## 🚫 反模式对照表

| ❌ 错误做法 | ✅ 正确做法 |
|-------------|-------------|
| 使用 Mixins | 使用 Composables |
| `const { prop } = props` 解构 | `props.prop` 或 `toRefs(props)` |
| 在 setup 中写 `created` 逻辑 | 直接写在 setup 顶层 |
| 忘记 `.value` | 始终在 script 中使用 `.value` |
| `reactive` 后解构 | 使用 `ref` 或 `toRefs` |
| Options API 混用 | 统一使用 Composition API |

---

## ⚡ 性能优化

| 技术 | 场景 | 示例 |
|------|------|------|
| `v-memo` | 大型列表/表格 | `v-memo="[item.id, item.selected]"` |
| `shallowRef` | 大型外部实例 | 地图、图表实例 |
| `KeepAlive` | 缓存组件 | 标签页切换 |
| 路由懒加载 | 所有路由 | `() => import('./Page.vue')` |
| `defineAsyncComponent` | 条件渲染组件 | 模态框、抽屉 |

```typescript
// 路由懒加载
const routes = [
  {
    path: '/dashboard',
    component: () => import('@/views/Dashboard.vue')
  }
]

// 异步组件
const HeavyModal = defineAsyncComponent(() => 
  import('./HeavyModal.vue')
)
```

---

## 🛠️ 技术栈推荐

| 分类 | 推荐 |
|------|------|
| 构建工具 | Vite |
| 路由 | Vue Router 4 |
| 状态管理 | Pinia |
| UI 组件库 | Element Plus / Naive UI / Ant Design Vue |
| 样式方案 | UnoCSS / Tailwind CSS |
| 测试 | Vitest + Vue Test Utils |
| 工具库 | VueUse |

---

## 🔄 迁移指南：Options → Composition

| Options API | Composition API |
|-------------|-----------------|
| `data()` | `ref()` / `reactive()` |
| `computed: {}` | `computed()` |
| `methods: {}` | 普通函数 |
| `watch: {}` | `watch()` / `watchEffect()` |
| `created` | `<script setup>` 顶层代码 |
| `mounted` | `onMounted()` |
| `this.xxx` | 直接访问变量 |

---

## 🐛 常见错误排查

| 问题 | 原因 | 解决 |
|------|------|------|
| 数据不更新 | 忘记 `.value` | 检查 ref 访问 |
| 解构后不响应 | reactive 解构 | 使用 `toRefs()` |
| computed 不执行 | 未访问 `.value` | 确保访问响应式依赖 |
| watch 不触发 | 监听了原始值 | 使用 getter 函数 |
| Props 类型错误 | 缺少类型定义 | 添加泛型类型 |

---

## 📂 示例文件

本技能包含以下完整示例，位于 `examples/` 目录：

| 文件 | 说明 |
|------|------|
| [component-example.vue](./examples/component-example.vue) | 递归树形组件，展示 defineOptions 命名、插槽透传 |
| [composable-example.ts](./examples/composable-example.ts) | usePagination 分页逻辑封装 |
| [store-example.ts](./examples/store-example.ts) | Pinia Setup Store 完整示例 |

---

## 🎨 常用指令示例

```bash
# 生成 Composable
/vue-coder 提取这段逻辑为一个名为 usePagination 的 Composable 函数。

# 转换 Options API
/vue-coder 将这个 Options API 组件重构为 <script setup lang="ts"> 写法。

# 优化响应式
/vue-coder 检查这段代码中 reactive 的使用是否合理，建议改为 ref。

# 添加类型
/vue-coder 为这个组件的 props 和 emits 添加完整的 TypeScript 类型。

# 性能优化
/vue-coder 分析这个列表组件的性能问题，建议优化方案。
```
