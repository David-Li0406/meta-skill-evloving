# Hexo 輔助函數參考

Hexo 輔助函數只能在模板中使用，不能在原始檔案中使用。

## 目錄

- [URL 輔助函數](#url-輔助函數)
- [HTML 標籤輔助函數](#html-標籤輔助函數)
- [條件判斷輔助函數](#條件判斷輔助函數)
- [字串處理輔助函數](#字串處理輔助函數)
- [日期時間輔助函數](#日期時間輔助函數)
- [列表輔助函數](#列表輔助函數)
- [其他輔助函數](#其他輔助函數)

## URL 輔助函數

### url_for(path)

回傳含根路徑的 URL，自動編碼。

```ejs
<%- url_for('/about') %>
<!-- /root/about -->
```

### relative_url(from, to)

計算兩個路徑間的相對路徑。

```ejs
<%- relative_url('foo/bar/', 'css/style.css') %>
<!-- ../../css/style.css -->
```

### full_url_for(path)

回傳含 `config.url` 的完整 URL。

```ejs
<%- full_url_for('/about') %>
<!-- https://example.com/about -->
```

### gravatar(email, [size])

產生 Gravatar 圖片 URL。

```ejs
<%- gravatar('email@example.com') %>
<%- gravatar('email@example.com', 200) %>
```

## HTML 標籤輔助函數

### css(path)

載入 CSS 檔案，自動加上 `.css` 副檔名。

```ejs
<%- css('style') %>
<!-- <link rel="stylesheet" href="/style.css"> -->

<%- css(['style', 'custom']) %>
<!-- 載入多個 CSS -->

<%- css({href: 'style', integrity: 'sha384-xxx'}) %>
<!-- 帶屬性的 CSS -->
```

### js(path)

載入 JavaScript 檔案。

```ejs
<%- js('script') %>
<!-- <script src="/script.js"></script> -->

<%- js(['jquery', 'app']) %>
<!-- 載入多個 JS -->
```

### link_to(path, [text], [options])

建立超連結。

```ejs
<%- link_to('https://hexo.io', 'Hexo') %>
<!-- <a href="https://hexo.io">Hexo</a> -->

<%- link_to('https://hexo.io', 'Hexo', {external: true}) %>
<!-- <a href="https://hexo.io" target="_blank" rel="noopener">Hexo</a> -->

<%- link_to('https://hexo.io', 'Hexo', {class: 'btn'}) %>
<!-- <a href="https://hexo.io" class="btn">Hexo</a> -->
```

### mail_to(email, [text], [options])

建立郵件連結。

```ejs
<%- mail_to('info@example.com') %>
<%- mail_to('info@example.com', 'Contact', {subject: 'Hello'}) %>
```

**選項**：`subject`, `cc`, `bcc`, `body`

### image_tag(path, [options])

插入圖片標籤。

```ejs
<%- image_tag('image.jpg') %>
<%- image_tag('image.jpg', {alt: '描述', class: 'thumbnail'}) %>
```

### favicon_tag(path)

插入 favicon 連結。

```ejs
<%- favicon_tag('favicon.ico') %>
```

### feed_tag(path, [options])

插入 feed 連結。

```ejs
<%- feed_tag('atom.xml') %>
<%- feed_tag('rss.xml', {title: 'RSS Feed', type: 'rss'}) %>
```

## 條件判斷輔助函數

### is_current(path, [strict])

檢查路徑是否為當前頁面。

```ejs
<%- is_current('/about') %>
```

### is_home() / is_home_first_page()

檢查是否為首頁。

```ejs
<% if (is_home()) { %>首頁<% } %>
<% if (is_home_first_page()) { %>首頁第一頁<% } %>
```

### is_post()

檢查是否為文章頁面。

### is_page()

檢查是否為獨立頁面。

### is_archive()

檢查是否為歸檔頁面。

### is_year() / is_month()

檢查是否為年度/月份歸檔頁面。

### is_category()

檢查是否為分類頁面，可選傳入分類名稱。

```ejs
<% if (is_category()) { %>分類頁<% } %>
<% if (is_category('生活')) { %>生活分類<% } %>
```

### is_tag()

檢查是否為標籤頁面，可選傳入標籤名稱。

## 字串處理輔助函數

### trim(string)

移除首尾空白。

```ejs
<%- trim('  hello  ') %>
<!-- hello -->
```

### strip_html(string)

移除 HTML 標籤。

```ejs
<%- strip_html('<p>Hello</p>') %>
<!-- Hello -->
```

### titlecase(string)

轉換為標題格式。

```ejs
<%- titlecase('hello world') %>
<!-- Hello World -->
```

### markdown(str)

將 Markdown 轉換為 HTML。

```ejs
<%- markdown('## 標題') %>
<!-- <h2>標題</h2> -->
```

### word_wrap(str, [length])

將文字依指定長度換行（預設 80）。

```ejs
<%- word_wrap('Very long text...', 40) %>
```

### truncate(text, length)

截斷文字到指定長度（預設 30）。

```ejs
<%- truncate('Hello World', 5) %>
<!-- Hello... -->

<%- truncate('Hello World', {length: 5, separator: ' '}) %>
<!-- Hello... -->
```

### escape_html(str)

轉義 HTML 實體。

```ejs
<%- escape_html('<div>') %>
<!-- &lt;div&gt; -->
```

## 日期時間輔助函數

### date(date, [format])

格式化日期，使用 Moment.js 格式。

```ejs
<%- date(Date.now()) %>
<!-- 2024-01-15 -->

<%- date(page.date, 'YYYY年MM月DD日') %>
<!-- 2024年01月15日 -->

<%- date(page.date, 'MMM D, YYYY') %>
<!-- Jan 15, 2024 -->
```

### date_xml(date)

輸出 ISO 8601 格式日期（用於 feed）。

```ejs
<%- date_xml(page.date) %>
<!-- 2024-01-15T10:30:00.000Z -->
```

### time(date, [format])

格式化時間。

```ejs
<%- time(Date.now(), 'HH:mm:ss') %>
<!-- 10:30:00 -->
```

### full_date(date, [format])

格式化完整日期時間。

```ejs
<%- full_date(page.date) %>
<!-- 2024-01-15 10:30:00 -->
```

### relative_date(date)

顯示相對時間。

```ejs
<%- relative_date(page.date) %>
<!-- 3 天前 -->
```

### time_tag(date, [format])

插入 `<time>` 標籤。

```ejs
<%- time_tag(page.date) %>
<!-- <time datetime="2024-01-15T10:30:00.000Z">2024-01-15</time> -->
```

## 列表輔助函數

### list_categories([options])

產生分類列表。

```ejs
<%- list_categories() %>
<%- list_categories(site.categories, {
  orderby: 'name',
  order: 1,
  show_count: true,
  depth: 2,
  class: 'category',
  separator: ', '
}) %>
```

**選項**：

| 選項         | 預設值     | 說明                      |
| ------------ | ---------- | ------------------------- |
| `orderby`    | `name`     | 排序依據                  |
| `order`      | `1`        | 排序方式，1 升序，-1 降序 |
| `show_count` | `true`     | 顯示文章數量              |
| `depth`      | `0`        | 分類深度，0 表示全部      |
| `class`      | `category` | CSS class                 |
| `separator`  | `,`        | 分隔符                    |

### list_tags([options])

產生標籤列表。

```ejs
<%- list_tags() %>
<%- list_tags({
  orderby: 'count',
  order: -1,
  show_count: true,
  class: 'tag',
  amount: 10
}) %>
```

### list_archives([options])

產生歸檔列表。

```ejs
<%- list_archives() %>
<%- list_archives({
  type: 'monthly',
  order: -1,
  show_count: true,
  format: 'YYYY年MM月'
}) %>
```

### list_posts([options])

產生文章列表。

```ejs
<%- list_posts({amount: 5}) %>
```

### tagcloud([tags], [options])

產生標籤雲。

```ejs
<%- tagcloud() %>
<%- tagcloud({
  min_font: 12,
  max_font: 24,
  amount: 50,
  color: true,
  start_color: '#ccc',
  end_color: '#111'
}) %>
```

## 其他輔助函數

### paginator(options)

產生分頁導覽。

```ejs
<%- paginator() %>
<%- paginator({
  prev_text: '← 上一頁',
  next_text: '下一頁 →',
  mid_size: 2,
  end_size: 1,
  show_all: false
}) %>
```

### search_form(options)

嵌入 Google 搜尋表單。

```ejs
<%- search_form({
  class: 'search-form',
  text: '搜尋',
  button: true
}) %>
```

### number_format(number, [options])

格式化數字。

```ejs
<%- number_format(1234567) %>
<!-- 1,234,567 -->

<%- number_format(1234.567, {precision: 2}) %>
<!-- 1,234.57 -->
```

### meta_generator()

輸出 Hexo 生成器 meta 標籤。

```ejs
<%- meta_generator() %>
<!-- <meta name="generator" content="Hexo 6.3.0"> -->
```

### open_graph([options])

產生 Open Graph 標籤（用於社群分享）。

```ejs
<%- open_graph() %>
<%- open_graph({
  title: page.title,
  description: page.description,
  image: page.thumbnail,
  twitter_card: 'summary_large_image',
  twitter_site: '@username'
}) %>
```

### toc(str, [options])

解析標題產生目錄。

```ejs
<%- toc(page.content) %>
<%- toc(page.content, {
  class: 'toc',
  list_number: true,
  max_depth: 3,
  min_depth: 1
}) %>
```
