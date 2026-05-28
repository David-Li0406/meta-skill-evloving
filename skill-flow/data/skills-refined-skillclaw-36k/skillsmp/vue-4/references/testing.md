# Vue 測試指南

Vue 3 組件、composables 和工具函數的測試模式。

## 快速參考

| 測試類型   | 模式                                 |
| ---------- | ------------------------------------ |
| 組件測試   | `mount(Component, { props, slots })` |
| 使用者互動 | `await wrapper.trigger('click')`     |
| 事件發送   | `wrapper.emitted('update')`          |
| Composable | 直接呼叫，測試回傳值                 |
| Utils      | 純函數測試（最簡單）                 |

## 測試技術棧

- **Vitest** - 測試執行器
- **@vue/test-utils** - 組件掛載、互動
- **@testing-library/vue** - 以使用者為中心的替代方案
- **happy-dom / jsdom** - DOM 環境

## 檔案位置

測試與代碼放在一起（colocation）：

```
Button.vue → Button.spec.ts
useAuth.ts → useAuth.spec.ts
formatters.ts → formatters.spec.ts
```

## 組件測試

### 基礎測試

```ts
import { mount } from '@vue/test-utils'
import Button from './Button.vue'

it('渲染 slot 內容', () => {
  const wrapper = mount(Button, {
    slots: { default: '點我' },
  })
  expect(wrapper.text()).toBe('點我')
})

it('點擊時發送事件', async () => {
  const wrapper = mount(Button)
  await wrapper.trigger('click')
  expect(wrapper.emitted('click')).toHaveLength(1)
})
```

### Props 測試

```ts
it('套用 variant class', () => {
  const wrapper = mount(Button, {
    props: { variant: 'primary' },
  })
  expect(wrapper.classes()).toContain('btn-primary')
})
```

### Emits 測試

```ts
it('發送包含資料的 update 事件', async () => {
  const wrapper = mount(Input)
  await wrapper.find('input').setValue('new value')
  expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['new value'])
})
```

### Slots 測試

```ts
it('渲染具名 slots', () => {
  const wrapper = mount(Card, {
    slots: {
      header: '<h1>標題</h1>',
      default: '<p>內容</p>',
    },
  })
  expect(wrapper.html()).toContain('<h1>標題</h1>')
})
```

## Composable 測試

直接呼叫即可，無需掛載：

```ts
import { useCounter } from './useCounter'

it('遞增計數', () => {
  const { count, increment } = useCounter(0)
  expect(count.value).toBe(0)
  increment()
  expect(count.value).toBe(1)
})

it('重置到初始值', () => {
  const { count, increment, reset } = useCounter(5)
  increment()
  increment()
  expect(count.value).toBe(7)
  reset()
  expect(count.value).toBe(5)
})
```

## Utils 測試

最簡單 - 純函數測試：

```ts
import { formatCurrency, slugify } from './formatters'

describe('formatCurrency', () => {
  it('格式化美金', () => {
    expect(formatCurrency(10.5)).toBe('$10.50')
  })
})

describe('slugify', () => {
  it('轉換為小寫', () => {
    expect(slugify('Hello World')).toBe('hello-world')
  })

  it('移除特殊字元', () => {
    expect(slugify('Hello! World?')).toBe('hello-world')
  })
})
```

## Mocking 模擬

**Composables 模擬：**

```ts
import { vi } from 'vitest'

vi.mock('./useAuth', () => ({
  useAuth: vi.fn(() => ({
    user: { id: 1, name: 'Test' },
    isAuthenticated: true,
  })),
}))
```

**API 呼叫模擬：**

```ts
global.fetch = vi.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({ data: [] }),
  })
)
```

## 最佳實踐

**應該做的事：**

- 測試行為（使用者看到/做的事），而非實作細節
- 使用 Arrange-Act-Assert 結構
- 每個測試一個斷言
- 描述性的測試名稱
- 模擬外部依賴

**不應該做的事：**

- 測試 Vue 內部機制（響應性）
- 測試第三方函式庫
- 測試瑣碎的 getters/setters
- 測試實作細節

## 測試範圍

**應該測試：**

- 使用者互動（點擊、輸入）
- 條件式渲染
- Props 驗證、事件發送
- 計算屬性、業務邏輯

**可跳過測試：**

- Vue 內部機制、第三方函式庫
- 瑣碎的 getters/setters
- 實作細節

## 執行測試

```bash
pnpm test                          # 全部測試
pnpm exec vitest Button.spec.ts   # 特定檔案
pnpm exec vitest --watch           # 監視模式
pnpm test --coverage               # 測試覆蓋率
```

**官方文件：** [vitest.dev](https://vitest.dev/) · [test-utils.vuejs.org](https://test-utils.vuejs.org/)
