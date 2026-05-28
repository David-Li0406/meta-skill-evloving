# 客戶端工具函數指南

用於格式化、驗證、轉換和解析的純函數（pure functions）。

## 快速參考

| 類別     | 範例                                          |
| -------- | --------------------------------------------- |
| 格式化器 | `formatCurrency`、`formatDate`、`formatBytes` |
| 驗證器   | `isValidEmail`、`isValidUrl`、`isValidPhone`  |
| 轉換器   | `slugify`、`truncate`、`capitalize`           |
| 解析器   | `parseQuery`、`parseJSON`、`parseDate`        |

## 基本原則

**純函數特性：**

- 相同輸入 → 相同輸出
- 無副作用
- 不修改外部狀態
- 不進行 API 呼叫、不使用 refs、不使用響應式

**何時不該使用 utils：**

- 有狀態邏輯 → 使用 composables
- Vue 特定功能 → 使用 composables
- 組件邏輯 → 保留在組件內
- API 呼叫 → 使用 queries

## 基本結構

```ts
// utils/formatters.ts
export function formatCurrency(amount: number, currency = 'USD'): string {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount)
}

export function formatRelativeTime(date: Date): string {
  const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' })
  const diff = date.getTime() - Date.now()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  return rtf.format(days, 'day')
}
```

**命名規範：** 使用描述性動詞（`formatCurrency`、`validateEmail`、`parseQuery`）  
**組織方式：** 依類別分組（`formatters.ts`、`validators.ts`）  
**匯出方式：** 僅使用具名匯出（named exports）

## 依類別分類的範例

**格式化器：**

```ts
// utils/formatters.ts
export function formatBytes(bytes: number): string { ... }
export function formatPhone(phone: string): string { ... }
```

**驗證器：**

```ts
// utils/validators.ts
export function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@][^\s.@]*\.[^\s@]+$/.test(email)
}

export function isValidUrl(url: string): boolean {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}
```

**轉換器：**

```ts
// utils/transformers.ts
export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, '-')
}

export function truncate(text: string, length: number): string {
  return text.length > length ? `${text.slice(0, length)}...` : text
}
```

**解析器：**

```ts
// utils/parsers.ts
export function parseQuery(search: string): Record<string, string> {
  return Object.fromEntries(new URLSearchParams(search))
}

export function parseJSON<T>(json: string, fallback: T): T {
  try {
    return JSON.parse(json)
  } catch {
    return fallback
  }
}
```

## 常見錯誤

**產生副作用（非純函數）：**

```ts
// ❌ 錯誤 - 修改外部狀態
let count = 0
export function increment() {
  count++
  return count
}

// ✅ 正確 - 純函數
export function add(a: number, b: number): number {
  return a + b
}
```

**將有狀態邏輯放在 utils：**

```ts
// ❌ 錯誤 - 應該是 composable
export function useCounter() { ... }

// ✅ 正確 - 純轉換函數
export function formatCount(count: number): string { ... }
```

## 檔案組織

**小型專案採用扁平結構：**

```
utils/
├── formatters.ts
├── validators.ts
└── transformers.ts
```

**大型專案採用巢狀結構：**

```
utils/
├── formatters/
│   ├── date.ts
│   ├── currency.ts
│   └── index.ts
└── validators/
    ├── email.ts
    └── index.ts
```
