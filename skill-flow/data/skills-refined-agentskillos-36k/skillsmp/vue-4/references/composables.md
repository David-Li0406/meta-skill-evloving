# Vue Composables 開發指南

使用 Composition API 封裝可重用狀態邏輯的函數。

## 核心原則

1. **優先使用 VueUse** - 撰寫自訂 composable 前，先查詢 [vueuse.org](https://vueuse.org)
2. **避免 async composables** - 被 await 時會失去生命週期上下文
3. **僅頂層呼叫** - 絕不在事件處理器、條件式或迴圈中呼叫
4. **使用 readonly() 匯出** - 保護內部狀態免於外部修改
5. **SSR 使用 useState()** - Nuxt 專案使用 `useState()` 而非全域 refs

## 快速參考

| 模式     | 範例                                             |
| -------- | ------------------------------------------------ |
| 命名     | `useAuth`、`useCounter`、`useDebounce`           |
| 狀態     | `const count = ref(0)`                           |
| 計算屬性 | `const double = computed(() => count.value * 2)` |
| 生命週期 | `onMounted(() => ...)`、`onUnmounted(() => ...)` |
| 回傳值   | `return { count, increment }`                    |

## 基本結構

```ts
// composables/useCounter.ts
import { readonly, ref } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)

  function increment() {
    count.value++
  }
  function decrement() {
    count.value--
  }
  function reset() {
    count.value = initialValue
  }

  return {
    count: readonly(count), // 若不應被修改，使用 readonly
    increment,
    decrement,
    reset,
  }
}
```

## 命名規範

**永遠以 `use` 開頭：** `useAuth`、`useLocalStorage`、`useDebounce`

**檔案名稱 = 函數名稱：** `useAuth.ts` 匯出 `useAuth`

## 最佳實踐

**應該做的事：**

- 回傳物件與具名屬性（方便解構）
- 接受選項物件作為配置參數
- 使用 `readonly()` 保護不應修改的狀態
- 妥善處理清理工作（`onUnmounted`、`onScopeDispose`）
- 為複雜函數添加 JSDoc 註解

## 生命週期處理

hooks 在組件上下文中執行：

```ts
export function useEventListener(target: EventTarget, event: string, handler: Function) {
  onMounted(() => target.addEventListener(event, handler))
  onUnmounted(() => target.removeEventListener(event, handler))
}
```

**Watcher 清理（Vue 3.5+）：**

```ts
import { watch, onWatcherCleanup } from 'vue'

export function usePolling(url: Ref<string>) {
  watch(url, newUrl => {
    const interval = setInterval(() => {
      fetch(newUrl).then(/* ... */)
    }, 1000)

    // watcher 重新執行或停止時清理
    onWatcherCleanup(() => {
      clearInterval(interval)
    })
  })
}
```

**`onWatcherCleanup()` 的優勢：**

- 比回傳清理函數更簡潔
- 支援非同步 watchers
- 可在同一個 watcher 中多次呼叫

## 非同步處理模式

```ts
export function useAsyncData<T>(fetcher: () => Promise<T>) {
  const data = ref<T | null>(null)
  const error = ref<Error | null>(null)
  const loading = ref(false)

  async function execute() {
    loading.value = true
    error.value = null
    try {
      data.value = await fetcher()
    } catch (e) {
      error.value = e as Error
    } finally {
      loading.value = false
    }
  }

  execute()
  return { data, error, loading, refetch: execute }
}
```

**資料獲取：** 建議使用 Pinia Colada queries 而非自訂 composables。

## VueUse 整合

> 若需 VueUse composable 參考，請使用 `vueuse` skill。

撰寫自訂 composables 前先查詢 VueUse - 大多數模式已有現成實作。

> **Nuxt 專屬 composables**（useFetch、useRequestURL）：請參閱 `nuxt` skill 的 nuxt-composables.md

## 進階模式

### Singleton Composable

在所有使用同一 composable 的組件間共享狀態：

```ts
import { createSharedComposable } from '@vueuse/core'

function useMapControlsBase() {
  const mapInstance = ref<Map | null>(null)
  const flyTo = (coords: [number, number]) => mapInstance.value?.flyTo(coords)
  return { mapInstance, flyTo }
}

export const useMapControls = createSharedComposable(useMapControlsBase)
```

### 可取消的 Fetch（搭配 AbortController）

```ts
export function useSearch() {
  let abortController: AbortController | null = null

  watch(query, async newQuery => {
    abortController?.abort()
    abortController = new AbortController()

    try {
      const data = await $fetch('/api/search', {
        query: { q: newQuery },
        signal: abortController.signal,
      })
    } catch (e) {
      if (e.name !== 'AbortError') throw e
    }
  })
}
```

### 步驟式狀態機

```ts
export function useSendFlow() {
  const step = ref<'input' | 'confirm' | 'success'>('input')
  const amount = ref('')

  const next = () => {
    if (step.value === 'input') step.value = 'confirm'
    else if (step.value === 'confirm') step.value = 'success'
  }

  return { step, amount, next }
}
```

### 僅客戶端執行守衛

```ts
export function useUserLocation() {
  const location = ref<GeolocationPosition | null>(null)

  if (import.meta.client) {
    navigator.geolocation.getCurrentPosition(pos => (location.value = pos))
  }

  return { location }
}
```

### Custom Element Composables（Vue 3.5+）

適用於自訂元素組件的內建輔助函數：

```ts
import { useHost, useShadowRoot } from 'vue'

export function useCustomElement() {
  const host = useHost() // 宿主元素引用
  const shadowRoot = useShadowRoot() // Shadow DOM 根節點

  onMounted(() => {
    console.log('Host:', host)
    console.log('Shadow:', shadowRoot)
  })

  return { host, shadowRoot }
}
```

**可用於：**

- 使用 `<script setup>` 的 custom elements 組件
- Options API 透過 `this.$host` 存取

### 自動儲存搭配防抖

```ts
export function useAutoSave(content: Ref<string>) {
  const hasChanges = ref(false)

  const save = useDebounceFn(async () => {
    if (!hasChanges.value) return
    await $fetch('/api/save', { method: 'POST', body: { content: content.value } })
    hasChanges.value = false
  }, 1000)

  watch(content, () => {
    hasChanges.value = true
    save()
  })

  return { hasChanges }
}
```

### 標籤化日誌記錄

```ts
import { consola } from 'consola'

export function useSearch() {
  const logger = consola.withTag('search')

  watch(query, q => {
    logger.info('Query changed:', q)
  })
}
```

## 常見錯誤

**未使用 `readonly()` 保護內部狀態：**

```ts
// ❌ 錯誤 - 暴露可修改的 ref
return { count }

// ✅ 正確 - 防止外部修改
return { count: readonly(count) }
```

**遺漏清理工作：**

```ts
// ❌ 錯誤 - 監聽器永不移除
onMounted(() => target.addEventListener('click', handler))

// ✅ 正確 - 卸載時清理
onMounted(() => target.addEventListener('click', handler))
onUnmounted(() => target.removeEventListener('click', handler))
```
