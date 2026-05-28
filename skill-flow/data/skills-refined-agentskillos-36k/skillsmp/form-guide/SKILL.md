---
name: form-guide
description: 開發前端表單時，使用 Angular Signal Forms 的正確模式
---

# Form Guide

開發含有表單的前端頁面時，**優先使用 Angular Signal Forms 模式**。

## 觸發時機

- 使用者提到要開發「表單」、「form」、「登入」、「註冊」等相關功能時
- 新增含有 `<form>` 元素的頁面時
- 需要處理表單驗證或表單提交時

## 開發指南

### 1. 表單提交事件綁定

**問題**：使用 `(ngSubmit)` 搭配 async `onSubmit()` 會導致瀏覽器預設提交行為觸發，造成頁面重載。

```html
<!-- ❌ 錯誤寫法 -->
<form (ngSubmit)="onSubmit()">

<!-- ✅ 正確寫法 -->
<form (submit)="$event.preventDefault(); onSubmit()">
```

**檢查步驟**：
1. 找到所有 `<form>` 元素
2. 檢查是否使用 `(ngSubmit)`
3. 若 `onSubmit()` 是 async 函數，應改用 `(submit)="$event.preventDefault(); onSubmit()"`

### 2. Signal Forms import

**檢查 TypeScript 是否正確 import**：

```typescript
// ✅ 正確 import
import { form, FormField, required, email, minLength, validate, submit } from '@angular/forms/signals';
```

**常用 API**：
- `form()` - 建立表單
- `FormField` - Directive，用於 template 綁定
- `submit()` - 提交表單，會先執行驗證
- `required()`, `email()`, `minLength()`, `maxLength()` - 內建驗證器
- `validate()` - 自訂驗證器

### 3. 表單模型定義

**檢查表單模型是否使用 signal**：

```typescript
// ✅ 正確寫法
readonly formModel = signal<LoginFormData>({
  email: '',
  password: ''
});

readonly loginForm = form(this.formModel, (f) => {
  required(f.email, { message: '請輸入 Email' });
  email(f.email, { message: '請輸入有效的 Email 格式' });
  required(f.password, { message: '請輸入密碼' });
});
```

### 4. Template 綁定

**檢查輸入元件是否使用 `[formField]` 綁定**：

```html
<!-- ✅ 正確寫法 -->
<fm-labeled-input
  [formField]="loginForm.email"
  label="Email"
  placeholder="請輸入 Email"
/>

<!-- ❌ 不要混用 Reactive Forms 的 formControlName -->
<input formControlName="email" />
```

### 5. Submit 處理

**檢查 submit 函數的使用方式**：

```typescript
// ✅ 正確寫法
async onSubmit(): Promise<void> {
  await submit(this.loginForm, async () => {
    // 驗證通過後執行
    const { email, password } = this.formModel();
    await this.authService.login(email, password);
  });
}
```

## 開發步驟

1. **定義表單介面與 signal model**
2. **使用 `form()` 建立表單並設定驗證器**
3. **在 template 使用 `[formField]` 綁定輸入元件**
4. **使用 `(submit)="$event.preventDefault(); onSubmit()"` 處理提交**
5. **在 `onSubmit()` 中使用 `submit()` 函數執行驗證與提交**

## Reactive Forms 轉換對照

| Reactive Forms | Signal Forms |
|----------------|--------------|
| `(ngSubmit)="onSubmit()"` | `(submit)="$event.preventDefault(); onSubmit()"` |
| `formControlName="email"` | `[formField]="form.email"` |
| `[formGroup]="form"` | 移除，Signal Forms 不需要 |
| `this.form.value` | `this.formModel()` |
| `this.form.valid` | `this.loginForm.valid()` |

## 參考

- ADR-012：前端元件按領域分組與共置原則（Form 層範例）
- `apps/docs-viewer/src/content/docs/agentSelfFeedback/angular-signal-forms-submit.md`
- `apps/web/src/app/pages/register/register.component.ts`（參考實作）
