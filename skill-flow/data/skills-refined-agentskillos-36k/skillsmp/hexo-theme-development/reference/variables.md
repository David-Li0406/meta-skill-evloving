# Hexo 變數參考

## 目錄

- [全域變數](#全域變數)
- [Site 變數](#site-變數)
- [Page 變數](#page-變數)
- [Config 變數](#config-變數)
- [Theme 變數](#theme-變數)
- [模板使用範例](#模板使用範例)

## 全域變數

| 變數     | 類型   | 說明                             |
| -------- | ------ | -------------------------------- |
| `site`   | Object | 網站資料                         |
| `page`   | Object | 當前頁面資料及 front-matter 變數 |
| `config` | Object | 網站配置 (`_config.yml`)         |
| `theme`  | Object | 主題配置，繼承自網站配置         |
| `path`   | String | 當前頁面路徑（不含根路徑）       |
| `url`    | String | 當前頁面完整 URL                 |
| `env`    | Object | 環境變數                         |

> **注意**：Lodash 已從 Hexo 5.0.0 版本的全域變數中移除。

## Site 變數

透過 `site` 物件存取網站範圍的資料集合：

| 變數              | 類型  | 說明         |
| ----------------- | ----- | ------------ |
| `site.posts`      | Query | 所有文章     |
| `site.pages`      | Query | 所有獨立頁面 |
| `site.categories` | Query | 所有分類     |
| `site.tags`       | Query | 所有標籤     |

### 使用範例

```ejs
<!-- 取得文章總數 -->
<%= site.posts.length %>

<!-- 遍歷所有文章 -->
<% site.posts.each(function(post){ %>
  <a href="<%- url_for(post.path) %>"><%= post.title %></a>
<% }) %>

<!-- 取得所有標籤 -->
<% site.tags.each(function(tag){ %>
  <span><%= tag.name %> (<%= tag.posts.length %>)</span>
<% }) %>
```

## Page 變數

### 通用頁面變數

| 變數               | 類型    | 說明                     |
| ------------------ | ------- | ------------------------ |
| `page.title`       | String  | 頁面標題                 |
| `page.date`        | Moment  | 建立日期                 |
| `page.updated`     | Moment  | 更新日期                 |
| `page.comments`    | Boolean | 是否開啟評論             |
| `page.layout`      | String  | 佈局名稱                 |
| `page.content`     | String  | 完整內容                 |
| `page.excerpt`     | String  | 摘要                     |
| `page.more`        | String  | 摘要以外的內容           |
| `page.source`      | String  | 原始檔路徑               |
| `page.full_source` | String  | 原始檔完整路徑           |
| `page.path`        | String  | 頁面 URL（不含根路徑）   |
| `page.permalink`   | String  | 頁面完整 URL             |
| `page.prev`        | Object  | 上一篇文章               |
| `page.next`        | Object  | 下一篇文章               |
| `page.raw`         | String  | 原始內容                 |
| `page.photos`      | Array   | 文章照片                 |
| `page.link`        | String  | 外部連結                 |

### 文章特有變數

| 變數              | 類型    | 說明       |
| ----------------- | ------- | ---------- |
| `page.published`  | Boolean | 是否已發布 |
| `page.categories` | Array   | 分類陣列   |
| `page.tags`       | Array   | 標籤陣列   |

### 首頁特有變數

| 變數               | 類型   | 說明             |
| ------------------ | ------ | ---------------- |
| `page.per_page`    | Number | 每頁文章數       |
| `page.total`       | Number | 總頁數           |
| `page.current`     | Number | 當前頁碼         |
| `page.current_url` | String | 當前頁面 URL     |
| `page.posts`       | Query  | 當前頁面的文章   |
| `page.prev`        | Number | 上一頁頁碼       |
| `page.prev_link`   | String | 上一頁連結       |
| `page.next`        | Number | 下一頁頁碼       |
| `page.next_link`   | String | 下一頁連結       |

### 歸檔頁面特有變數

| 變數           | 類型    | 說明         |
| -------------- | ------- | ------------ |
| `page.archive` | Boolean | 是否為歸檔頁 |
| `page.year`    | Number  | 年份         |
| `page.month`   | Number  | 月份         |

### 分類/標籤頁面特有變數

| 變數            | 說明         |
| --------------- | ------------ |
| `page.category` | 當前分類名稱 |
| `page.tag`      | 當前標籤名稱 |

## Config 變數

存取 `_config.yml` 中的設定：

```ejs
<!-- 網站標題 -->
<%= config.title %>

<!-- 網站描述 -->
<%= config.description %>

<!-- 網站 URL -->
<%= config.url %>

<!-- 語言設定 -->
<%= config.language %>
```

## Theme 變數

存取主題 `_config.yml` 中的設定：

```ejs
<!-- 主題設定的 menu -->
<% for (var name in theme.menu) { %>
  <a href="<%- url_for(theme.menu[name]) %>"><%= name %></a>
<% } %>
```

## 模板使用範例

### 判斷頁面類型

```ejs
<% if (is_home()) { %>
  <!-- 首頁內容 -->
<% } else if (is_post()) { %>
  <!-- 文章內容 -->
<% } else if (is_archive()) { %>
  <!-- 歸檔內容 -->
<% } %>
```

### 顯示文章標籤

```ejs
<% if (page.tags && page.tags.length) { %>
  <div class="tags">
    <% page.tags.each(function(tag){ %>
      <a href="<%- url_for(tag.path) %>">#<%= tag.name %></a>
    <% }) %>
  </div>
<% } %>
```

### 顯示分頁導覽

```ejs
<% if (page.prev || page.next) { %>
  <nav class="post-nav">
    <% if (page.prev) { %>
      <a href="<%- url_for(page.prev.path) %>">← <%= page.prev.title %></a>
    <% } %>
    <% if (page.next) { %>
      <a href="<%- url_for(page.next.path) %>"><%= page.next.title %> →</a>
    <% } %>
  </nav>
<% } %>
```
