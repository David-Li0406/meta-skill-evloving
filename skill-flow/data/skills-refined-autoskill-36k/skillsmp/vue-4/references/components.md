# Vue 組件開發指南

使用 Composition API 搭配 `<script setup>` 的 Vue 3 組件開發模式。

## 快速參考

| 模式            | 語法                                                            |
| --------------- | --------------------------------------------------------------- |
| Props（解構式） | `const { name = 'default' } = defineProps<{ name?: string }>()` |
| Props（僅模板） | `defineProps<{ name: string }>()`                               |
| 事件發送        | `const emit = defineEmits<{ click: [id: number] }>()`           |
| 雙向綁定        | `const model = defineModel<string>()`                           |
| Slots 簡寫      | `<template #header>` 而非 `<template v-slot:header>`            |

## 命名規範

**檔案命名：** PascalCase（`UserProfile.vue`）或 kebab-case（`user-profile.vue`）- 保持一致即可

**程式碼中的組件名稱：** 一律使用 PascalCase

**組件命名順序：** 從通用到具體：`SearchButtonClear.vue` 而非 `ClearSearchButton.vue`

## Props 屬性定義

**解構式寫法搭配預設值（Vue 3.5+）** - 當需要在 script 中使用或設定預設值時：

```ts
const { count = 0, message = 'Hello' } = defineProps<{
  count?: number
  message?: string
  required: boolean
}>()

// 直接使用 - 保持響應性
console.log(count + 1)

// ⚠️ 傳入 watch 或函數時，需包裝成 getter：
watch(() => count, (newVal) => { ... }) // ✅ 正確
watch(count, (newVal) => { ... })        // ❌ 無法運作
```

**非解構式寫法** - 僅當 props 只在模板中使用時：

```ts
defineProps<{ count: number }>()
// 模板中使用：{{ count }}
```

**同名簡寫（Vue 3.4+）：** `:count` 取代 `:count="count"`

```vue
<MyComponent :count :user :items />
<!-- 等同於：:count="count" :user="user" :items="items" -->
```

[Reactive destructuring 官方文件](https://vuejs.org/guide/components/props#reactive-props-destructure)

## Emits 事件定義

型別安全的事件定義方式：

```ts
const emit = defineEmits<{
  update: [id: number, value: string] // 多個參數
  close: [] // 無參數
}>()

// 使用方式
emit('update', 123, 'new value')
emit('close')
```

**模板語法：** kebab-case（`@update-item`）對應 script 中的 camelCase（`updateItem`）

## Slots 插槽

**永遠使用簡寫：** `<template #header>` 而非 `<template v-slot:header>`

**所有 slot 都明確使用 `<template>` 標籤**

```vue
<template>
  <Card>
    <template #header>
      <h2>標題</h2>
    </template>
    <template #default> 內容區塊 </template>
  </Card>
</template>
```

## defineModel() - 雙向綁定

取代手動的 `modelValue` prop + `update:modelValue` emit 模式。

### 基礎用法

```vue
<script setup lang="ts">
const title = defineModel<string>()
</script>

<template>
  <input v-model="title" />
</template>
```

### 進階選項

```vue
<script setup lang="ts">
const [title, modifiers] = defineModel<string>({
  default: 'default value',
  required: true,
  get: value => value.trim(),
  set: value => {
    if (modifiers.capitalize) {
      return value.charAt(0).toUpperCase() + value.slice(1)
    }
    return value
  },
})
</script>
```

**⚠️ 注意：** 使用 `default` 但父組件未提供值時，父子組件可能不同步（父為 `undefined`，子有預設值）。建議在父組件也提供對應的預設值，或將 prop 設為 required。

### 多個 Model

預設使用 `modelValue` prop。若需多個綁定，使用明確的名稱：

```vue
<script setup lang="ts">
const firstName = defineModel<string>('firstName')
const age = defineModel<number>('age')
</script>

<!-- 使用方式 -->
<UserForm v-model:first-name="user.firstName" v-model:age="user.age" />
```

[v-model modifiers 官方文件](https://vuejs.org/guide/components/v-model#handling-v-model-modifiers)

## 可重用模板

在組件內建立型別安全、有作用域的模板片段：

```vue
<script setup lang="ts">
import { createReusableTemplate } from '@vueuse/core'

const [DefineItem, UseItem] = createReusableTemplate<{
  item: SearchItem
  icon: string
  color?: 'red' | 'green' | 'blue'
}>()
</script>

<template>
  <DefineItem v-slot="{ item, icon, color }">
    <div :class="color">
      <Icon :name="icon" />
      {{ item.name }}
    </div>
  </DefineItem>

  <!-- 多次重複使用 -->
  <UseItem v-for="item in items" :key="item.id" :item :icon="getIcon(item)" />
</template>
```

## Template Refs（Vue 3.5+）

使用 `useTemplateRef()` 獲得型別安全的模板引用，並享有完整的 IDE 支援：

```vue
<script setup lang="ts">
import { useTemplateRef, onMounted } from 'vue'

const input = useTemplateRef<HTMLInputElement>('my-input')

onMounted(() => {
  input.value?.focus()
})
</script>

<template>
  <input ref="my-input" />
</template>
```

**相較於 `ref()` 的優勢：**

- 泛型提供型別安全
- 更好的 IDE 自動完成和重構支援
- 明確的 ref 名稱（字串字面量）

**動態 refs：**

```vue
<script setup lang="ts">
const items = ref(['a', 'b', 'c'])
const itemRefs = useTemplateRef<HTMLElement>('item')

// 掛載後存取 refs
onMounted(() => {
  console.log(itemRefs.value) // 元素陣列
})
</script>

<template>
  <div v-for="item in items" :key="item" ref="item">
    {{ item }}
  </div>
</template>
```

## SSR Hydration（Vue 3.5+）

**抑制 hydration 不匹配警告** - 適用於伺服器/客戶端值不同的情況：

```vue
<template>
  <!-- 僅客戶端的值 -->
  <span data-allow-mismatch>{{ new Date().toLocaleString() }}</span>

  <!-- 指定不匹配類型 -->
  <span data-allow-mismatch="text">{{ timestamp }}</span>
  <span data-allow-mismatch="children">
    <ClientOnly>...</ClientOnly>
  </span>
  <span data-allow-mismatch="style">...</span>
  <span data-allow-mismatch="class">...</span>
  <span data-allow-mismatch="attribute">...</span>
</template>
```

**產生 SSR 穩定的 ID：**

```vue
<script setup lang="ts">
import { useId } from 'vue'

const id = useId() // 伺服器/客戶端渲染時保持一致
</script>

<template>
  <label :for="id">姓名</label>
  <input :id="id" />
</template>
```

## Deferred Teleport（Vue 3.5+）

傳送到同一週期中稍後才渲染的元素：

```vue
<template>
  <!-- 先渲染這個 -->
  <Teleport defer to="#late-div">
    <span>延遲傳送的內容</span>
  </Teleport>

  <!-- 後渲染，但 Teleport 會等待 -->
  <div id="late-div"></div>
</template>
```

若不使用 `defer`，傳送到 `#late-div` 會失敗，因為該元素尚未存在。

## 常見錯誤

**使用 `const props =` 搭配解構：**

```ts
// ❌ 錯誤
const props = defineProps<{ count: number }>()
const { count } = props // 失去響應性
```

**忘記 TypeScript 型別：**

```ts
// ❌ 錯誤
const emit = defineEmits(['update'])

// ✅ 正確
const emit = defineEmits<{ update: [id: number] }>()
```

**組件超過 300 行：** 應拆分成更小的組件，或將邏輯抽取到 composables
