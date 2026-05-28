---
name: testid-guide
description: 開發前端頁面時，為可互動元素添加 testId 以支援 E2E 測試
---

# testId Guide

開發前端頁面元件時，**為所有可互動元素添加 testId**，確保 E2E 測試的穩定性。

## 觸發時機

- 使用者提到要開發「頁面」、「元件」、「UI」等相關功能時
- 新增或修改 `.component.html` 檔案時
- 涉及按鈕、表單輸入、連結等可互動元素時

## 開發指南

### 必須添加 testId 的元素

| 元素類型 | 說明 | 範例 |
|----------|------|------|
| UI 元件 | `fm-button`、`fm-icon-button`、`fm-labeled-input`、`fm-toggle`、`fm-search-input`、`fm-textarea`、`fm-number-input`、`fm-alert`、`fm-fab` | `testId="login-submit"` |
| 表單元素 | `input`、`textarea`、`select`、`button` | `data-testid="login-email"` |
| 導航連結 | 帶有 `routerLink` 的元素 | `data-testid="nav-home"` |
| 可點擊元素 | 帶有 `(click)` 事件的元素 | `data-testid="deck-item-123"` |

### 可省略 testId 的元素

- 純裝飾性元素（icon、分隔線）
- 靜態文字內容（標題、說明文字）
- `ng-container`、`ng-template` 等結構性元素

## testId 命名規範

**格式：`{page/context}-{element}[-{qualifier}]`**

- **page/context**：從檔案路徑取得頁面名稱（如 `deck-detail`、`login`）
- **element**：元素用途（如 `submit`、`back`、`search`、`email`）
- **qualifier**：可選，用於區分相似元素

### 命名對照表

| 元素類型 | 命名方式 | 範例 |
|----------|----------|------|
| 提交按鈕 | `{page}-submit` | `login-submit` |
| 取消按鈕 | `{page}-cancel` | `deck-form-cancel` |
| 返回按鈕 | `{page}-back` | `deck-detail-back` |
| 設定按鈕 | `{page}-settings` | `deck-detail-settings` |
| 輸入欄位 | `{page}-{field}` | `login-email` |
| 搜尋框 | `{page}-search` | `deck-list-search` |
| 錯誤訊息 | `{page}-error` | `login-error` |
| 列表項目 | `{item}-item-{id}` | `deck-item-{id}` |
| FAB 按鈕 | `{page}-{action}` | `deck-detail-add-card` |

## 使用方式

```html
<!-- UI 元件使用 testId 屬性 -->
<fm-button testId="login-submit">登入</fm-button>
<fm-labeled-input testId="login-email" ... />
<fm-icon-button testId="deck-detail-back" ... />

<!-- 原生元素使用 data-testid 屬性 -->
<div data-testid="deck-list-empty">尚無牌組</div>
<button data-testid="card-delete">刪除</button>
```

## 開發步驟

1. **辨識頁面中的可互動元素**（按鈕、輸入框、連結等）
2. **根據命名規範決定 testId 名稱**
3. **UI 元件使用 `testId` 屬性，原生元素使用 `data-testid`**
4. **確保同一頁面內 testId 不重複**

## 參考

- ADR-019：前端 testId 規範
- AGENTS.md：E2E 測試選擇器規範
