# Hexo 模板參考

## 目錄

- [模板類型與備援機制](#模板類型與備援機制)
- [支援的模板引擎](#支援的模板引擎)
- [佈局 (Layout)](#佈局-layout)
- [局部模板 (Partials)](#局部模板-partials)
- [片段快取 (Fragment Cache)](#片段快取-fragment-cache)
- [各模板檔案範例](#各模板檔案範例)

## 模板類型與備援機制

Hexo 使用模板備援機制，當特定模板不存在時會使用備援模板：

```text
index    (必需，無備援)
post     → index
page     → index
archive  → index
category → archive → index
tag      → archive → index
```

## 支援的模板引擎

| 引擎     | 副檔名              | 安裝方式                          |
| -------- | ------------------- | --------------------------------- |
| Nunjucks | `.njk`, `.nunjucks` | 內建                              |
| EJS      | `.ejs`              | `npm install hexo-renderer-ejs`   |
| Pug      | `.pug`              | `npm install hexo-renderer-pug`   |

## 佈局 (Layout)

### 基本佈局結構

```ejs
<!-- layout/layout.ejs -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title><%= config.title %></title>
  <%- css('css/style') %>
</head>
<body>
  <%- partial('_partial/header') %>
  <main><%- body %></main>
  <%- partial('_partial/footer') %>
  <%- js('js/script') %>
</body>
</html>
```

### 禁用佈局

在 front-matter 中設定：

```yaml
---
title: 無佈局頁面
layout: false
---
```

### 指定特定佈局

```yaml
---
title: 自訂佈局
layout: custom
---
```

## 局部模板 (Partials)

### 基本用法

```ejs
<%- partial('_partial/header') %>
```

### 傳遞變數

```ejs
<%- partial('_partial/article', {
  item: post,
  index: true
}) %>
```

### 局部模板範例

```ejs
<!-- layout/_partial/article.ejs -->
<article class="<%= item.layout %>">
  <header>
    <h2><a href="<%- url_for(item.path) %>"><%= item.title %></a></h2>
    <time><%= date(item.date, 'YYYY-MM-DD') %></time>
  </header>
  <% if (index && item.excerpt) { %>
    <%- item.excerpt %>
  <% } else { %>
    <%- item.content %>
  <% } %>
</article>
```

## 片段快取 (Fragment Cache)

用於快取跨頁面不變的內容，提升生成效能：

### 使用 fragment_cache

```ejs
<%- fragment_cache('sidebar', function(){
  return partial('_partial/sidebar');
}) %>
```

### 使用 partial 的 cache 選項

```ejs
<%- partial('_partial/header', {}, {cache: true}) %>
```

**注意**：僅用於跨頁面完全相同的內容，如固定的導覽列。

## 各模板檔案範例

### index.ejs

```ejs
<% page.posts.each(function(post){ %>
  <%- partial('_partial/article', {item: post, index: true}) %>
<% }) %>
<%- paginator({
  prev_text: '&laquo; 上一頁',
  next_text: '下一頁 &raquo;'
}) %>
```

### post.ejs

```ejs
<%- partial('_partial/article', {item: page, index: false}) %>
<% if (page.comments) { %>
  <%- partial('_partial/comments') %>
<% } %>
```

### archive.ejs

```ejs
<% page.posts.each(function(post){ %>
<article>
  <h3><a href="<%- url_for(post.path) %>"><%= post.title %></a></h3>
  <time><%= date(post.date, 'YYYY-MM-DD') %></time>
</article>
<% }) %>
<%- paginator() %>
```

### page.ejs

```ejs
<article class="page">
  <h1><%= page.title %></h1>
  <%- page.content %>
</article>
```

### category.ejs / tag.ejs

```ejs
<h1><%= page.category || page.tag %></h1>
<% page.posts.each(function(post){ %>
  <%- partial('_partial/article-item', {item: post}) %>
<% }) %>
<%- paginator() %>
```
