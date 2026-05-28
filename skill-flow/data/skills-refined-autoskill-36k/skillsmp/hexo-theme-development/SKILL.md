---
name: hexo-theme-development
description: Provides Hexo blog theme development guidance covering templates, variables, helpers, and i18n. Use when creating or modifying Hexo themes, working with EJS/Nunjucks templates, using Hexo variables or helper functions, or developing Hexo plugins and extensions.
---

# Hexo 主題開發

## 目錄

- [Hexo 基礎](#hexo-基礎)
- [主題結構](#主題結構)
- [模板系統](#模板系統)
- [變數系統](#變數系統)
- [輔助函數](#輔助函數)
- [國際化](#國際化)
- [擴展 API](#擴展-api)
- [測試](#測試)
- [發布主題](#發布主題)

## Hexo 基礎

開發主題前需了解的 Hexo 基礎知識。

### 配置檔案

主要配置在 `_config.yml`：

```yaml
# 網站設定
title: My Blog
author: Author Name
language: zh-tw

# URL 設定
url: https://example.com
permalink: :year/:month/:day/:title/

# 目錄設定
source_dir: source
public_dir: public

# 主題設定
theme: my-theme
```

### 常用指令

```bash
hexo new post "標題"    # 新建文章
hexo new page "about"   # 新建頁面
hexo generate           # 產生靜態檔案
hexo server             # 啟動本地伺服器
hexo clean              # 清除快取
```

### Front-matter

文章開頭的 YAML 區塊：

```yaml
---
title: 文章標題
date: 2024-01-15
tags: [Tag1, Tag2]
categories: [Category]
---
```

### 資料檔案

在 `source/_data/` 放置 YAML/JSON，透過 `site.data` 存取：

```yaml
# source/_data/menu.yml
home: /
archives: /archives
```

詳細基礎參考：[reference/basics.md](reference/basics.md)

## 主題結構

Hexo 主題遵循標準化目錄結構：

```text
.
├── _config.yml    # 主題配置檔
├── languages/     # 國際化語言檔案
├── layout/        # 模板檔案
├── scripts/       # JavaScript 擴展腳本
└── source/        # 靜態資源 (CSS, JS, 圖片)
```

**各目錄說明**：

| 目錄/檔案      | 說明                                 |
| -------------- | ------------------------------------ |
| `_config.yml`  | 主題配置，修改後自動生效無需重啟     |
| `languages/`   | 存放 YAML/JSON 語言檔案              |
| `layout/`      | 模板檔案，支援 EJS、Nunjucks、Pug    |
| `scripts/`     | 初始化時自動載入的 JS 腳本           |
| `source/`      | 靜態資源，`_` 開頭和隱藏檔案會被忽略 |

## 模板系統

### 六種核心模板

| 模板       | 說明         | 備援      |
| ---------- | ------------ | --------- |
| `index`    | 首頁（必需） | -         |
| `post`     | 文章頁面     | `index`   |
| `page`     | 獨立分頁     | `index`   |
| `archive`  | 歸檔頁面     | `index`   |
| `category` | 分類歸檔     | `archive` |
| `tag`      | 標籤歸檔     | `archive` |

### 佈局機制

佈局檔案需包含 `body` 變數以顯示模板內容：

```ejs
<!-- layout.ejs -->
<!DOCTYPE html>
<html>
  <head><title><%= page.title %></title></head>
  <body><%- body %></body>
</html>
```

在 front-matter 指定或禁用佈局：

```yaml
---
layout: false  # 禁用佈局
---
```

### 局部模板

使用 `partial()` 引入共用元件：

```ejs
<%- partial('partial/header') %>
<%- partial('partial/sidebar', {active: 'home'}) %>
```

**片段快取**（用於跨頁面不變的內容）：

```ejs
<%- fragment_cache('header', function(){ return '<header>...</header>'; }) %>
<%- partial('partial/header', {}, {cache: true}) %>
```

## 變數系統

### 全域變數

| 變數     | 說明             |
| -------- | ---------------- |
| `site`   | 網站資訊         |
| `page`   | 當前頁面資訊     |
| `config` | 網站配置         |
| `theme`  | 主題配置         |
| `path`   | 當前頁面路徑     |
| `url`    | 當前頁面完整網址 |

詳細變數參考：[reference/variables.md](reference/variables.md)

## 輔助函數

Hexo 提供豐富的內建輔助函數：

- **URL 類**：`url_for()`, `relative_url()`, `full_url_for()`
- **HTML 標籤類**：`css()`, `js()`, `link_to()`, `image_tag()`
- **條件判斷類**：`is_home()`, `is_post()`, `is_archive()`
- **字串處理類**：`trim()`, `strip_html()`, `truncate()`
- **日期時間類**：`date()`, `time()`, `relative_date()`
- **列表類**：`list_categories()`, `list_tags()`, `paginator()`

詳細函數參考：[reference/helpers.md](reference/helpers.md)

## 國際化

### 配置語言

在 `_config.yml` 設定：

```yaml
language: zh-tw
# 或多語言
language:
  - zh-tw
  - en
```

### 語言檔案

在 `languages/` 建立 YAML 檔案：

```yaml
# languages/zh-tw.yml
Home: 首頁
Archive: 歸檔
Search: 搜尋
```

### 模板中使用

```ejs
<%= __('Home') %>
<%= _p('posts', 5) %>  <!-- 複數形式 -->
```

詳細說明：[reference/i18n.md](reference/i18n.md)

## 擴展 API

Hexo 提供強大的擴展 API，用於開發插件和自訂功能。

### 主要擴展點

| API       | 說明     | 用途                         |
| --------- | -------- | ---------------------------- |
| Filter    | 過濾器   | 修改處理中的資料             |
| Helper    | 輔助函數 | 在模板中插入程式碼片段       |
| Generator | 產生器   | 根據檔案建立路由             |
| Tag       | 標籤     | 在文章中插入自訂內容         |
| Renderer  | 渲染器   | 轉換內容格式                 |
| Injector  | 注入器   | 在 HTML 特定位置插入程式碼   |
| Console   | 控制台   | 建立自訂指令                 |

### 快速範例

```javascript
// scripts/my-plugin.js

// 自訂輔助函數
hexo.extend.helper.register('greeting', function(name) {
  return `Hello, ${name}!`;
});

// 文章渲染後處理
hexo.extend.filter.register('after_post_render', function(data) {
  // 修改文章內容
  return data;
});

// 自訂標籤
hexo.extend.tag.register('note', function(args, content) {
  return `<div class="note">${content}</div>`;
}, { ends: true });
```

詳細 API 參考：[reference/api.md](reference/api.md)

## 測試

完整的主題測試包含多個層面。

### 測試工具

| 類型 | 工具 | 用途 |
| ---- | ---- | ---- |
| 單元測試 | Mocha + Chai | 測試輔助函數、標籤 |
| 配置驗證 | js-yaml | 驗證 YAML 格式 |
| JS Linting | ESLint | JavaScript 品質 |
| CSS Linting | Stylelint | 樣式表品質 |
| 功能測試 | hexo-theme-unit-test | 主題完整性 |
| CI/CD | GitHub Actions | 自動化測試 |

### 基本設置

```json
{
  "scripts": {
    "test": "mocha test/index.js",
    "lint": "eslint scripts/ source/js/"
  },
  "devDependencies": {
    "chai": "^5.0.0",
    "eslint": "^9.0.0",
    "mocha": "^10.0.0"
  }
}
```

### 輔助函數測試範例

```javascript
// test/helpers/my-helper.js
const Hexo = require('hexo');

describe('my-helper', () => {
  const hexo = new Hexo(__dirname, { silent: true });
  before(() => hexo.init());

  const helper = hexo.extend.helper.get('my_helper').bind(hexo);

  it('should return formatted text', () => {
    helper('hello').should.equal('<span>hello</span>');
  });
});
```

### 功能測試清單

- [ ] DOCTYPE 和 charset 正確
- [ ] 首頁文章列表和分頁
- [ ] 文章頁標題、內容、標籤
- [ ] 歸檔頁按時間排序
- [ ] 響應式設計正常

詳細測試參考：[reference/testing.md](reference/testing.md)

## 發布主題

1. 執行測試確保品質
2. Fork [hexojs/site](https://github.com/hexojs/site) 儲存庫
3. 在 `themes.yml` 新增主題資訊
4. 提供 800×500px PNG 截圖

## 參考資料

- **基礎參考**：[reference/basics.md](reference/basics.md)
- **模板參考**：[reference/templates.md](reference/templates.md)
- **變數參考**：[reference/variables.md](reference/variables.md)
- **輔助函數參考**：[reference/helpers.md](reference/helpers.md)
- **國際化參考**：[reference/i18n.md](reference/i18n.md)
- **API 參考**：[reference/api.md](reference/api.md)
- **測試參考**：[reference/testing.md](reference/testing.md)
- **基本範例**：[examples/basic-theme.md](examples/basic-theme.md)
- **進階用法**：[examples/advanced-usage.md](examples/advanced-usage.md)
