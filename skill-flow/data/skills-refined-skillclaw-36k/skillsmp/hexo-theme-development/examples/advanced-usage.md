# Hexo 進階用法範例

## 目錄

- [自訂輔助函數](#自訂輔助函數)
- [自訂過濾器](#自訂過濾器)
- [自訂標籤](#自訂標籤)
- [進階模板技巧](#進階模板技巧)
- [效能優化](#效能優化)
- [資料檔案使用](#資料檔案使用)
- [多語言進階設定](#多語言進階設定)
- [SEO 優化](#seo-優化)
- [暗色模式](#暗色模式)

## 自訂輔助函數

在 `scripts/` 目錄建立自訂輔助函數：

```javascript
// scripts/helpers.js

// 閱讀時間估算
hexo.extend.helper.register('reading_time', function(content) {
  const wordsPerMinute = 200;
  const words = content.replace(/<[^>]*>/g, '').length;
  const minutes = Math.ceil(words / wordsPerMinute);
  return minutes + ' min read';
});

// 文章字數統計
hexo.extend.helper.register('word_count', function(content) {
  const text = content.replace(/<[^>]*>/g, '');
  return text.length;
});

// 隨機文章
hexo.extend.helper.register('random_posts', function(count) {
  const posts = this.site.posts.toArray();
  const shuffled = posts.sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
});
```

使用方式：

```ejs
<span><%= reading_time(page.content) %></span>
<span><%= word_count(page.content) %> 字</span>

<% random_posts(5).forEach(function(post){ %>
  <a href="<%- url_for(post.path) %>"><%= post.title %></a>
<% }) %>
```

## 自訂過濾器

```javascript
// scripts/filters.js

// 為外部連結添加 target="_blank"
hexo.extend.filter.register('after_post_render', function(data) {
  data.content = data.content.replace(
    /<a href="(https?:\/\/[^"]+)">/g,
    '<a href="$1" target="_blank" rel="noopener">'
  );
  return data;
});

// 圖片懶載入
hexo.extend.filter.register('after_post_render', function(data) {
  data.content = data.content.replace(
    /<img([^>]*)src="([^"]*)"([^>]*)>/g,
    '<img$1src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" data-src="$2"$3 loading="lazy">'
  );
  return data;
});
```

## 自訂標籤

```javascript
// scripts/tags.js

// 提示框標籤
hexo.extend.tag.register('note', function(args, content) {
  const type = args[0] || 'info';
  const md = hexo.render.renderSync({ text: content, engine: 'markdown' });
  return `<div class="note note-${type}">${md}</div>`;
}, { ends: true });

// 程式碼群組標籤
hexo.extend.tag.register('codegroup', function(args, content) {
  const tabs = content.split('---').map((block, i) => {
    const lines = block.trim().split('\n');
    const title = lines[0].replace('# ', '');
    const code = lines.slice(1).join('\n');
    return { title, code, active: i === 0 };
  });

  let html = '<div class="code-group">';
  html += '<div class="code-tabs">';
  tabs.forEach((tab, i) => {
    html += `<button class="${tab.active ? 'active' : ''}" data-tab="${i}">${tab.title}</button>`;
  });
  html += '</div>';
  tabs.forEach((tab, i) => {
    html += `<div class="code-panel ${tab.active ? 'active' : ''}" data-panel="${i}">${tab.code}</div>`;
  });
  html += '</div>';
  return html;
}, { ends: true });
```

使用方式：

```markdown
{% note warning %}
這是一個警告提示框
{% endnote %}

{% codegroup %}
# JavaScript
console.log('Hello');
---
# Python
print('Hello')
{% endcodegroup %}
```

## 進階模板技巧

### 條件式載入資源

```ejs
<% if (is_post()) { %>
  <%- css('css/prism') %>
  <%- js('js/prism') %>
<% } %>

<% if (page.photos && page.photos.length) { %>
  <%- css('css/lightbox') %>
  <%- js('js/lightbox') %>
<% } %>

<% if (page.mathjax) { %>
  <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<% } %>
```

### 自動產生目錄

```ejs
<% if (page.toc !== false && toc(page.content).length > 0) { %>
<aside class="post-toc">
  <h3>目錄</h3>
  <%- toc(page.content, {
    class: 'toc',
    list_number: false,
    max_depth: 3
  }) %>
</aside>
<% } %>
```

### 相關文章

```ejs
<%
var relatedPosts = site.posts.filter(function(post) {
  if (post.path === page.path) return false;
  var hasSameCat = page.categories.some(function(cat) {
    return post.categories.some(function(c) { return c.name === cat.name; });
  });
  var hasSameTag = page.tags.some(function(tag) {
    return post.tags.some(function(t) { return t.name === tag.name; });
  });
  return hasSameCat || hasSameTag;
}).slice(0, 5);
%>

<% if (relatedPosts.length) { %>
<section class="related-posts">
  <h3>相關文章</h3>
  <ul>
    <% relatedPosts.each(function(post){ %>
      <li><a href="<%- url_for(post.path) %>"><%= post.title %></a></li>
    <% }) %>
  </ul>
</section>
<% } %>
```

### 麵包屑導覽

```ejs
<nav class="breadcrumb">
  <a href="<%- url_for('/') %>"><%= __('menu.home') %></a>

  <% if (is_archive()) { %>
    <span>›</span>
    <a href="<%- url_for('/archives') %>"><%= __('archive') %></a>
    <% if (page.year) { %>
      <span>›</span>
      <span><%= page.year %></span>
    <% } %>
  <% } else if (is_category()) { %>
    <span>›</span>
    <span><%= page.category %></span>
  <% } else if (is_tag()) { %>
    <span>›</span>
    <span><%= page.tag %></span>
  <% } else if (is_post()) { %>
    <% if (page.categories && page.categories.length) { %>
      <% var cat = page.categories.toArray()[0]; %>
      <span>›</span>
      <a href="<%- url_for(cat.path) %>"><%= cat.name %></a>
    <% } %>
    <span>›</span>
    <span><%= page.title %></span>
  <% } %>
</nav>
```

## 效能優化

### 片段快取使用

```ejs
<!-- 固定內容使用快取 -->
<%- fragment_cache('header', function(){
  return partial('_partial/header');
}) %>

<!-- 或使用 partial 的 cache 選項 -->
<%- partial('_partial/sidebar', {}, {cache: true}) %>
```

### 條件式渲染

```ejs
<!-- 僅在需要時渲染 -->
<% if (theme.sidebar && theme.sidebar.display !== 'none') { %>
  <%- partial('_partial/sidebar') %>
<% } %>

<!-- 使用 only 選項限制變數傳遞 -->
<%- partial('_partial/article', {item: post}, {only: true}) %>
```

## 資料檔案使用

### 建立資料檔案

```yaml
# source/_data/links.yml
- name: Hexo
  url: https://hexo.io
  description: 快速、簡潔的部落格框架

- name: GitHub
  url: https://github.com
  description: 程式碼託管平台
```

### 在模板中使用

```ejs
<% if (site.data.links) { %>
<div class="friend-links">
  <h3>友情連結</h3>
  <ul>
    <% site.data.links.forEach(function(link){ %>
      <li>
        <a href="<%= link.url %>" target="_blank" rel="noopener">
          <%= link.name %>
        </a>
        <span><%= link.description %></span>
      </li>
    <% }) %>
  </ul>
</div>
<% } %>
```

## 多語言進階設定

### 語言切換器

```ejs
<%
var languages = ['zh-tw', 'en', 'ja'];
var currentLang = page.lang || config.language;
var currentPath = page.path.replace(/^(zh-tw|en|ja)\//, '');
%>

<div class="language-switcher">
  <% languages.forEach(function(lang){ %>
    <% var langPath = lang === config.language ? currentPath : lang + '/' + currentPath; %>
    <a href="<%- url_for(langPath) %>"
       class="<%= lang === currentLang ? 'active' : '' %>">
      <%= lang.toUpperCase() %>
    </a>
  <% }) %>
</div>
```

### 語言特定配置

```yaml
# _config.yml
language:
  - zh-tw
  - en

# 各語言的 per_page 設定
per_page_i18n:
  zh-tw: 10
  en: 5
```

## SEO 優化

### 結構化資料

```ejs
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "<%= is_post() ? 'BlogPosting' : 'WebPage' %>",
  "headline": "<%= page.title %>",
  "datePublished": "<%= date_xml(page.date) %>",
  <% if (page.updated) { %>
  "dateModified": "<%= date_xml(page.updated) %>",
  <% } %>
  "author": {
    "@type": "Person",
    "name": "<%= config.author %>"
  },
  "publisher": {
    "@type": "Organization",
    "name": "<%= config.title %>"
  }
}
</script>
```

### Sitemap 標頭

```ejs
<% if (page.prev) { %>
  <link rel="prev" href="<%- full_url_for(page.prev.path) %>">
<% } %>
<% if (page.next) { %>
  <link rel="next" href="<%- full_url_for(page.next.path) %>">
<% } %>
<link rel="canonical" href="<%- full_url_for(page.path) %>">
```

## 暗色模式

### JavaScript 切換

```javascript
// source/js/darkmode.js
const toggle = document.querySelector('.darkmode-toggle');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');

function setTheme(dark) {
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light');
  localStorage.setItem('theme', dark ? 'dark' : 'light');
}

// 初始化
const saved = localStorage.getItem('theme');
if (saved) {
  setTheme(saved === 'dark');
} else {
  setTheme(prefersDark.matches);
}

toggle.addEventListener('click', () => {
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  setTheme(!isDark);
});
```

### CSS 變數

```css
:root {
  --bg-color: #fff;
  --text-color: #333;
  --border-color: #eee;
}

[data-theme="dark"] {
  --bg-color: #1a1a1a;
  --text-color: #e0e0e0;
  --border-color: #333;
}

body {
  background: var(--bg-color);
  color: var(--text-color);
}
```
