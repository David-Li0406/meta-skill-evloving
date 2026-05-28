---
name: Coding Style 技能
description: JavaScript、TypeScript、PHP、Python、CSS 程式碼規範
---

# 📝 Coding Style 技能

## 規範索引

| 語言 | 規範 | 說明 |
|-----|------|-----|
| [JavaScript - Airbnb](js-airbnb.md) | 最流行、嚴格 |
| [JavaScript - Standard](js-standard.md) | 無分號風格 |
| [TypeScript](ts.md) | TypeScript 特定規範 |
| [PHP - PSR-12](php-psr12.md) | PHP 官方標準 |
| [PHP - Laravel](php-laravel.md) | Laravel 風格 |
| [Python - PEP8](py-pep8.md) | Python 官方標準 |
| [CSS - BEM](css-bem.md) | 命名規範 |

---

## 共通原則

### 命名規範

| 類型 | JavaScript | PHP | Python |
|-----|-----------|-----|--------|
| 變數 | camelCase | $camelCase | snake_case |
| 函式 | camelCase | camelCase | snake_case |
| 類別 | PascalCase | PascalCase | PascalCase |
| 常數 | UPPER_SNAKE | UPPER_SNAKE | UPPER_SNAKE |

### 格式化

| 項目 | 建議 |
|-----|------|
| 縮排 | 2 或 4 空格（依語言）|
| 行寬 | 80-120 字元 |
| 檔案結尾 | 保留空行 |
| 引號 | 統一使用單引號或雙引號 |

---

## 工具設定

### ESLint + Prettier (JS/TS)

```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser"
}
```

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

### EditorConfig

```ini
# .editorconfig
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.{php,py}]
indent_size = 4
```

---

## Git Hooks

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{js,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.css": ["stylelint --fix"]
  }
}
```

---

## 選擇精靈

不確定用什麼規範？使用 [Coding Style 精靈](../wizard/code.md)
