# Hexo 基本主題範例

本範例展示如何建立一個簡單但完整的 Hexo 主題。

## 目錄

- [目錄結構](#目錄結構)
- [主題配置](#主題配置)
- [佈局檔案](#佈局檔案)
- [頁面模板](#頁面模板)
- [語言檔案](#語言檔案)
- [基本樣式](#基本樣式)

## 目錄結構

```text
themes/simple/
├── _config.yml
├── languages/
│   ├── en.yml
│   └── zh-tw.yml
├── layout/
│   ├── _partial/
│   │   ├── head.ejs
│   │   ├── header.ejs
│   │   ├── footer.ejs
│   │   ├── article.ejs
│   │   └── pagination.ejs
│   ├── layout.ejs
│   ├── index.ejs
│   ├── post.ejs
│   ├── page.ejs
│   └── archive.ejs
└── source/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

## 主題配置

```yaml
# themes/simple/_config.yml
menu:
  home: /
  archives: /archives
  about: /about

# 社群連結
social:
  github: https://github.com/username
  twitter: https://twitter.com/username

# 頁尾資訊
footer:
  since: 2024
```

## 佈局檔案

### layout.ejs（主佈局）

```ejs
<!DOCTYPE html>
<html lang="<%= config.language %>">
<head>
  <%- partial('_partial/head') %>
</head>
<body>
  <%- partial('_partial/header') %>

  <main class="container">
    <%- body %>
  </main>

  <%- partial('_partial/footer') %>

  <%- js('js/script') %>
</body>
</html>
```

### _partial/head.ejs

```ejs
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title><%= page.title ? page.title + ' | ' + config.title : config.title %></title>
<meta name="description" content="<%= page.description || config.description %>">

<%- css('css/style') %>
<%- meta_generator() %>
<%- open_graph() %>

<% if (config.favicon) { %>
  <%- favicon_tag(config.favicon) %>
<% } %>
```

### _partial/header.ejs

```ejs
<header class="site-header">
  <div class="container">
    <a href="<%- url_for('/') %>" class="site-title">
      <%= config.title %>
    </a>

    <nav class="main-nav">
      <% for (var name in theme.menu) { %>
        <a href="<%- url_for(theme.menu[name]) %>"
           class="<%= is_current(theme.menu[name]) ? 'active' : '' %>">
          <%= __('menu.' + name) %>
        </a>
      <% } %>
    </nav>
  </div>
</header>
```

### _partial/footer.ejs

```ejs
<footer class="site-footer">
  <div class="container">
    <p>&copy; <%= theme.footer.since %>-<%= new Date().getFullYear() %> <%= config.author %></p>
    <p><%= __('powered_by', 'Hexo') %></p>

    <% if (theme.social) { %>
    <div class="social-links">
      <% for (var name in theme.social) { %>
        <a href="<%= theme.social[name] %>" target="_blank" rel="noopener">
          <%= name %>
        </a>
      <% } %>
    </div>
    <% } %>
  </div>
</footer>
```

### _partial/article.ejs

```ejs
<article class="post <%= item.layout %>">
  <header class="post-header">
    <% if (index) { %>
      <h2 class="post-title">
        <a href="<%- url_for(item.path) %>"><%= item.title %></a>
      </h2>
    <% } else { %>
      <h1 class="post-title"><%= item.title %></h1>
    <% } %>

    <div class="post-meta">
      <time datetime="<%- date_xml(item.date) %>">
        <%= date(item.date, 'YYYY-MM-DD') %>
      </time>

      <% if (item.categories && item.categories.length) { %>
        <span class="post-categories">
          <% item.categories.each(function(cat){ %>
            <a href="<%- url_for(cat.path) %>"><%= cat.name %></a>
          <% }) %>
        </span>
      <% } %>
    </div>
  </header>

  <div class="post-content">
    <% if (index && item.excerpt) { %>
      <%- item.excerpt %>
      <a href="<%- url_for(item.path) %>" class="read-more">
        <%= __('post.read_more') %>
      </a>
    <% } else { %>
      <%- item.content %>
    <% } %>
  </div>

  <% if (!index && item.tags && item.tags.length) { %>
  <footer class="post-footer">
    <div class="post-tags">
      <% item.tags.each(function(tag){ %>
        <a href="<%- url_for(tag.path) %>">#<%= tag.name %></a>
      <% }) %>
    </div>
  </footer>
  <% } %>
</article>
```

### _partial/pagination.ejs

```ejs
<% if (page.total > 1) { %>
<nav class="pagination">
  <%- paginator({
    prev_text: __('pagination.prev'),
    next_text: __('pagination.next'),
    mid_size: 1
  }) %>
</nav>
<% } %>
```

## 頁面模板

### index.ejs

```ejs
<div class="posts">
  <% page.posts.each(function(post){ %>
    <%- partial('_partial/article', {item: post, index: true}) %>
  <% }) %>
</div>

<%- partial('_partial/pagination') %>
```

### post.ejs

```ejs
<%- partial('_partial/article', {item: page, index: false}) %>

<% if (page.prev || page.next) { %>
<nav class="post-nav">
  <% if (page.prev) { %>
    <a href="<%- url_for(page.prev.path) %>" class="prev">
      ← <%= page.prev.title %>
    </a>
  <% } %>
  <% if (page.next) { %>
    <a href="<%- url_for(page.next.path) %>" class="next">
      <%= page.next.title %> →
    </a>
  <% } %>
</nav>
<% } %>

<% if (page.comments) { %>
<section class="comments">
  <!-- 評論系統佔位 -->
</section>
<% } %>
```

### page.ejs

```ejs
<article class="page">
  <h1 class="page-title"><%= page.title %></h1>
  <div class="page-content">
    <%- page.content %>
  </div>
</article>
```

### archive.ejs

```ejs
<h1 class="archive-title">
  <% if (page.category) { %>
    <%= __('category') %>: <%= page.category %>
  <% } else if (page.tag) { %>
    <%= __('tag') %>: <%= page.tag %>
  <% } else { %>
    <%= __('archive') %>
  <% } %>
</h1>

<div class="archive-posts">
  <% var year; %>
  <% page.posts.each(function(post){ %>
    <% var postYear = date(post.date, 'YYYY'); %>
    <% if (postYear !== year) { %>
      <% year = postYear; %>
      <h2 class="archive-year"><%= year %></h2>
    <% } %>
    <article class="archive-post">
      <time><%= date(post.date, 'MM-DD') %></time>
      <a href="<%- url_for(post.path) %>"><%= post.title %></a>
    </article>
  <% }) %>
</div>

<%- partial('_partial/pagination') %>
```

## 語言檔案

### languages/zh-tw.yml

```yaml
menu:
  home: 首頁
  archives: 歸檔
  about: 關於

post:
  read_more: 繼續閱讀

pagination:
  prev: ← 較新
  next: 較舊 →

archive: 文章歸檔
category: 分類
tag: 標籤

powered_by: 由 %s 驅動
```

### languages/en.yml

```yaml
menu:
  home: Home
  archives: Archives
  about: About

post:
  read_more: Read More

pagination:
  prev: ← Newer
  next: Older →

archive: Archives
category: Category
tag: Tag

powered_by: Powered by %s
```

## 基本樣式

```css
/* source/css/style.css */

/* 重置與基礎 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.6;
  color: #333;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 頁首 */
.site-header {
  padding: 20px 0;
  border-bottom: 1px solid #eee;
}

.site-title {
  font-size: 1.5rem;
  text-decoration: none;
  color: #333;
}

.main-nav a {
  margin-left: 20px;
  text-decoration: none;
  color: #666;
}

.main-nav a.active {
  color: #333;
  font-weight: bold;
}

/* 文章 */
.post {
  padding: 40px 0;
  border-bottom: 1px solid #eee;
}

.post-title {
  margin-bottom: 10px;
}

.post-title a {
  text-decoration: none;
  color: #333;
}

.post-meta {
  color: #999;
  font-size: 0.9rem;
}

.post-content {
  margin-top: 20px;
}

/* 分頁 */
.pagination {
  padding: 40px 0;
  text-align: center;
}

.pagination a {
  padding: 5px 15px;
  margin: 0 5px;
  text-decoration: none;
}

/* 頁尾 */
.site-footer {
  padding: 40px 0;
  text-align: center;
  color: #999;
  font-size: 0.9rem;
}
```
