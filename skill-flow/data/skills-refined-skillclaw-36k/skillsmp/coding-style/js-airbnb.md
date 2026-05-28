---
name: JavaScript Airbnb 規範
description: 最流行的 JavaScript 編碼規範
---

# Airbnb JavaScript Style Guide

## 基本規則

### 縮排與格式
- 縮排：2 空格
- 引號：單引號 `'`
- 分號：必須
- 行寬：100 字元

### 變數宣告

```javascript
// ✅ 使用 const
const foo = 1;

// ✅ 需要重新賦值時使用 let
let bar = 1;
bar = 2;

// ❌ 禁止使用 var
var baz = 1;
```

### 物件

```javascript
// ✅ 使用簡寫
const name = 'John';
const user = { name };

// ✅ 使用解構
const { name, age } = user;

// ✅ 尾逗號
const obj = {
  a: 1,
  b: 2,
};
```

### 函式

```javascript
// ✅ 使用箭頭函式作為回呼
const arr = [1, 2, 3].map((x) => x * 2);

// ✅ 使用預設參數
function greet(name = 'Guest') {
  return `Hello, ${name}`;
}

// ✅ 使用展開運算子
function sum(...numbers) {
  return numbers.reduce((a, b) => a + b, 0);
}
```

### 模組

```javascript
// ✅ 使用 import/export
import { foo } from './module';
export { bar };

// ❌ 不使用 require
const foo = require('./module');
```

---

## ESLint 設定

```json
{
  "extends": ["airbnb", "airbnb/hooks"],
  "rules": {
    "react/jsx-filename-extension": [1, { "extensions": [".jsx", ".tsx"] }]
  }
}
```

## 安裝

```bash
npm install -D eslint eslint-config-airbnb eslint-plugin-import eslint-plugin-react eslint-plugin-react-hooks eslint-plugin-jsx-a11y
```
