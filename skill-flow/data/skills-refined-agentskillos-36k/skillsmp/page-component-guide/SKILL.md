---
name: page-component-guide
description: 開發前端頁面時，優先使用 Component 組合，避免在 Page 自行切版
---

# Page Component Guide

開發前端頁面時，**能用 Component 就不自己切版**，Page 只負責 Layout 與 Component 組合。

## 觸發時機

- 使用者提到要開發「頁面」、「page」相關功能時
- 新增或修改 `pages/` 目錄下的檔案時
- 頁面需要 loading 狀態、錯誤訊息、表單區塊等常見 UI 時

## 核心原則

1. **Page 只處理 Layout**：使用 layout component 或簡單的容器結構
2. **能用 Component 就用 Component**：不要自己切版
3. **Page 不應有樣式檔**：沒有 `.css` / `.scss` 檔案

## 檢查清單

### ❌ 需要改進的模式

| 模式 | 問題 | 正確做法 |
|------|------|----------|
| 頁面有 `.component.css` 檔案 | Page 不應有自己的樣式 | 刪除 CSS，用 component 或 utility class |
| `<div class="min-h-screen ...">` | 自己處理頁面容器 | 使用 layout component |
| `<main class="mx-auto max-w-md ...">` | 自己切內容區域 | 使用 layout component |
| `<div class="flex justify-center py-8">` + loading 文字 | 自己切 loading 狀態 | 使用 `fm-loading` 或封裝 component |
| `<p class="text-red-500">錯誤訊息</p>` | 自己切錯誤訊息 | 使用 `fm-alert` |
| `<div class="border-t pt-6">` 區塊 | 自己切區塊分隔 | 封裝成 component |
| 複雜的巢狀 div 結構 | 自己切複雜 layout | 拆成多個 component |

### ✅ 可接受的樣式

| 模式 | 說明 |
|------|------|
| `class="space-y-4"` | 簡單的間距 utility |
| `class="pt-2"` | 微調用的 padding/margin |
| `class="flex flex-col gap-3"` | 按鈕群組的簡單排列 |
| Tailwind utility 用於微調 | 不構成「切版」的輔助樣式 |

## 好例子 vs 壞例子

### ✅ 好例子：register.component.html

```html
<fm-auth-page-layout>                    <!-- Layout component -->
  <ng-container main>
    <fm-auth-header title="註冊帳號">     <!-- Header component -->
      <a routerLink="/login">登入現有帳號</a>
    </fm-auth-header>

    @if (errorMessage) {
      <fm-alert [message]="errorMessage" type="error" />  <!-- Alert component -->
    }

    <form class="space-y-4" ...>         <!-- 只有簡單的間距 -->
      <fm-labeled-input ... />            <!-- Input component -->
      <fm-button ...>註冊</fm-button>     <!-- Button component -->
    </form>
  </ng-container>

  <ng-container footer>
    <fm-divider label="或使用其他方式" />  <!-- Divider component -->
    <fm-social-login-row ... />           <!-- Social login component -->
  </ng-container>
</fm-auth-page-layout>
```

**特點：**
- 沒有 `.css` 檔案
- 使用 `fm-auth-page-layout` 處理整體佈局
- 所有 UI 元素都用 component
- 只有 `space-y-4`, `pt-2` 等微調 utility

### ❌ 壞例子：需要改進的模式

```html
<div class="min-h-screen pb-6">           <!-- 自己切頁面容器 -->
  <fm-page-header title="設定" />

  <main class="mx-auto w-full max-w-md px-4 pt-4">  <!-- 自己切內容區域 -->
    @if (isLoading()) {
      <div class="flex justify-center py-8">        <!-- 自己切 loading -->
        <span class="text-slate-400">載入中...</span>
      </div>
    }

    @if (errorMessage()) {
      <p class="text-sm text-red-500">{{ errorMessage() }}</p>  <!-- 自己切錯誤 -->
    }

    <div class="mt-8 border-t border-slate-200 pt-6">  <!-- 自己切區塊 -->
      <h3>危險區域</h3>
      <p class="mb-4 text-sm text-slate-500">說明文字</p>
    </div>
  </main>
</div>
```

## 開發步驟

1. **確認是否有對應的 Layout Component**
   - 認證相關頁面：`fm-auth-page-layout`
   - 一般頁面：考慮是否需要建立新的 layout component

2. **盤點頁面需要的 UI 區塊**
   - Loading 狀態 → 使用現有 component 或建立
   - 錯誤訊息 → `fm-alert`
   - 表單 → `fm-labeled-input`, `fm-button` 等
   - 區塊標題 → `fm-section-heading`

3. **檢查是否有重複的切版模式**
   - 如果同樣的 HTML 結構在多處出現 → 封裝成 component
   - 如果區塊有明確的職責 → 封裝成 component

4. **最終檢查**
   - Page 沒有 `.css` 檔案
   - Page 的 HTML 主要是 component 組合
   - 自己寫的 class 只有間距微調

## 可用的 @flashmind/ui Components

| Category | Components |
|----------|------------|
| Layout | `FmAuthPageLayoutComponent`, `FmPageHeaderComponent` |
| Button | `FmButtonComponent`, `FmIconButtonComponent`, `FmFabComponent` |
| Form | `FmLabeledInputComponent`, `FmTextareaComponent`, `FmNumberInputRowComponent`, `FmSearchInputComponent` |
| Feedback | `FmAlertComponent`, `FmEmptyStateComponent`, `FmProgressBarComponent` |
| Display | `FmBadgeComponent`, `FmDividerComponent`, `FmSectionHeadingComponent` |
| Auth | `FmAuthHeaderComponent`, `FmSocialLoginRowComponent` |

## 何時建立新的 Component

當以下情況發生時，應該建立新的 component：

1. **重複使用**：同樣的 HTML 結構出現 2 次以上
2. **複雜區塊**：超過 10 行的 HTML 區塊有明確職責
3. **獨立狀態**：區塊有自己的狀態邏輯
4. **可測試性**：區塊需要獨立測試

**新 component 放置位置：**
- 只在單一頁面使用 → `pages/{page}/components/`
- 跨頁面共用 → `@flashmind/ui` library

## 參考

- `apps/web/src/app/pages/register/`（好的範例）
- ADR-012：前端元件按領域分組與共置原則
