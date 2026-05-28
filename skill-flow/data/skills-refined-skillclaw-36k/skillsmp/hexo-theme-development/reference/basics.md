# Hexo 基礎參考

開發 Hexo 主題前需要了解的基礎知識。

## 目錄

- [配置檔案](#配置檔案)
- [指令](#指令)
- [Front-matter](#front-matter)
- [標籤外掛](#標籤外掛)
- [資料檔案](#資料檔案)

## 配置檔案

Hexo 使用 `_config.yml` 作為主要配置檔案。

### 網站設定

| 設定          | 說明                                 |
| ------------- | ------------------------------------ |
| `title`       | 網站標題                             |
| `subtitle`    | 網站副標題                           |
| `description` | 網站描述（用於 SEO）                 |
| `keywords`    | 網站關鍵字                           |
| `author`      | 作者名稱                             |
| `language`    | 語言（ISO-639-1 代碼，如 `zh-tw`）   |
| `timezone`    | 時區（如 `Asia/Taipei`）             |

### URL 設定

| 設定                         | 預設值                      | 說明                                             |
| ---------------------------- | --------------------------- | ------------------------------------------------ |
| `url`                        | -                           | 網站網址（必須以 `http://` 或 `https://` 開頭）  |
| `root`                       | `/`                         | 網站根目錄                                       |
| `permalink`                  | `:year/:month/:day/:title/` | 文章永久連結格式                                 |
| `pretty_urls.trailing_index` | `true`                      | 是否保留結尾的 `index.html`                      |
| `pretty_urls.trailing_html`  | `true`                      | 是否保留結尾的 `.html`                           |

### 永久連結變數

| 變數          | 說明                                 |
| ------------- | ------------------------------------ |
| `:year`       | 4 位數年份                           |
| `:month`      | 2 位數月份                           |
| `:day`        | 2 位數日期                           |
| `:title`      | 檔案名稱（小寫，空格替換為連字號）   |
| `:post_title` | 文章標題                             |
| `:id`         | 文章 ID                              |
| `:category`   | 分類（若無則為 `default_category`）  |

### 目錄設定

| 設定           | 預設值       | 說明                         |
| -------------- | ------------ | ---------------------------- |
| `source_dir`   | `source`     | 原始檔案目錄                 |
| `public_dir`   | `public`     | 產生的靜態檔案目錄           |
| `tag_dir`      | `tags`       | 標籤目錄                     |
| `archive_dir`  | `archives`   | 歸檔目錄                     |
| `category_dir` | `categories` | 分類目錄                     |
| `skip_render`  | -            | 跳過渲染的檔案（支援 glob）  |

### 寫作設定

| 設定                   | 預設值      | 說明                 |
| ---------------------- | ----------- | -------------------- |
| `new_post_name`        | `:title.md` | 新文章檔名格式       |
| `default_layout`       | `post`      | 預設佈局             |
| `auto_spacing`         | `false`     | 中英文間自動加空格   |
| `titlecase`            | `false`     | 標題轉換為標題格式   |
| `external_link.enable` | `true`      | 外部連結開新分頁     |
| `post_asset_folder`    | `false`     | 啟用文章資源資料夾   |
| `relative_link`        | `false`     | 使用相對連結         |
| `future`               | `true`      | 顯示未來文章         |

### 分頁設定

| 設定             | 預設值 | 說明                     |
| ---------------- | ------ | ------------------------ |
| `per_page`       | `10`   | 每頁文章數（0 停用分頁） |
| `pagination_dir` | `page` | 分頁目錄                 |

### 主題設定

```yaml
# 指定主題
theme: landscape

# 主題配置（會與主題 _config.yml 合併）
theme_config:
  menu:
    home: /
    archives: /archives
```

### 替代配置檔

```bash
# 使用替代配置檔
hexo generate --config custom.yml

# 合併多個配置檔（後者優先）
hexo generate --config _config.yml,_config.theme.yml
```

## 指令

### 核心指令

```bash
# 建立新網站
hexo init [folder]

# 建立新文章/頁面/草稿
hexo new [layout] <title>
hexo new post "My Post"
hexo new page "about"
hexo new draft "Draft Post"

# 產生靜態檔案
hexo generate
hexo g              # 簡寫
hexo g --watch      # 監視檔案變化
hexo g --deploy     # 產生後部署
hexo g --force      # 強制重新產生

# 啟動本地伺服器
hexo server
hexo s              # 簡寫
hexo s -p 5000      # 指定埠號
hexo s --draft      # 顯示草稿

# 發布草稿
hexo publish <filename>

# 部署網站
hexo deploy
hexo d              # 簡寫
hexo d --generate   # 產生後部署

# 清除快取和已產生檔案
hexo clean

# 顯示路由清單
hexo list <type>    # type: page, post, route, tag, category
```

### 全域選項

| 選項              | 說明                 |
| ----------------- | -------------------- |
| `--safe`          | 安全模式（停用插件） |
| `--debug`         | 除錯模式             |
| `--silent`        | 靜默模式             |
| `--config <path>` | 指定配置檔           |
| `--draft`         | 顯示草稿             |
| `--cwd <path>`    | 指定工作目錄         |

## Front-matter

Front-matter 是檔案開頭的 YAML 或 JSON 區塊，用於設定文章屬性。

### 格式

```yaml
---
title: 文章標題
date: 2024-01-15 10:30:00
tags:
  - Tag1
  - Tag2
categories:
  - Category1
---
文章內容...
```

### 可用屬性

| 屬性         | 說明           | 預設值             |
| ------------ | -------------- | ------------------ |
| `title`      | 標題           | 檔案名稱           |
| `date`       | 建立日期       | 檔案建立日期       |
| `updated`    | 更新日期       | 檔案修改日期       |
| `layout`     | 佈局           | `post` 或 `page`   |
| `comments`   | 開啟評論       | `true`             |
| `tags`       | 標籤（僅文章） | -                  |
| `categories` | 分類（僅文章） | -                  |
| `permalink`  | 自訂永久連結   | -                  |
| `excerpt`    | 摘要（純文字） | -                  |
| `published`  | 是否發布       | `true`             |
| `lang`       | 語言           | 繼承 `_config.yml` |

### 分類與標籤

```yaml
# 標籤（同一層級）
tags:
  - JavaScript
  - Node.js

# 分類（階層結構）
categories:
  - Programming
  - Web Development

# 多重分類階層
categories:
  - [Programming, JavaScript]
  - [Tutorial]
```

### 自訂屬性

可以自訂任意屬性，在模板中透過 `page.xxx` 存取：

```yaml
---
title: My Post
thumbnail: /images/thumb.jpg
featured: true
---
```

```ejs
<% if (page.featured) { %>
  <img src="<%= page.thumbnail %>">
<% } %>
```

## 標籤外掛

標籤外掛用於在文章中插入特定內容，格式為 `{% tag_name args %}`。

### 程式碼區塊

```markdown
{% codeblock [title] [lang:language] [url] [link text] [line_number:false] [highlight:true] [first_line:1] [mark:#,#-#] %}
code snippet
{% endcodeblock %}

<!-- 範例 -->
{% codeblock Array.map lang:javascript %}
const doubled = [1, 2, 3].map(n => n * 2);
{% endcodeblock %}
```

### 引用區塊

```markdown
{% blockquote [author[, source]] [link] [source_link_title] %}
quote content
{% endblockquote %}

<!-- 範例 -->
{% blockquote David Levithan, Wide Awake %}
Do not just seek happiness for yourself.
{% endblockquote %}
```

### Pull Quote

```markdown
{% pullquote [class] %}
content
{% endpullquote %}
```

### 嵌入內容

```markdown
<!-- iframe -->
{% iframe url [width] [height] %}

<!-- 圖片 -->
{% img [class names] /path/to/image [width] [height] "title text 'alt text'" %}

<!-- 連結 -->
{% link text url [external] [title] %}
```

### 引入程式碼檔案

```markdown
<!-- 從 source/downloads/code 引入 -->
{% include_code [title] [lang:language] [from:line] [to:line] path/to/file %}

<!-- 範例 -->
{% include_code lang:javascript test.js %}
```

### 文章連結

```markdown
<!-- 取得文章路徑 -->
{% post_path filename %}

<!-- 建立文章連結 -->
{% post_link filename [title] [escape] %}

<!-- 範例 -->
{% post_link my-post '點擊這裡' %}
```

### 資源標籤

需啟用 `post_asset_folder: true`：

```markdown
<!-- 資源路徑 -->
{% asset_path filename %}

<!-- 資源圖片 -->
{% asset_img [class names] filename [width] [height] [title text [alt text]] %}

<!-- 資源連結 -->
{% asset_link filename [title] [escape] %}
```

### URL 標籤

```markdown
{% url_for path %}
{% full_url_for path %}
```

### Raw 標籤

防止內容被解析：

```markdown
{% raw %}
content that should not be parsed
{% endraw %}
```

### 文章摘要

在文章中插入 `<!-- more -->` 分隔摘要：

```markdown
這是摘要內容

<!-- more -->

這是完整內容
```

## 資料檔案

資料檔案用於儲存可重複使用的資料。

### 建立資料檔案

在 `source/_data/` 目錄建立 YAML 或 JSON 檔案：

```yaml
# source/_data/menu.yml
home: /
archives: /archives
about: /about
```

```yaml
# source/_data/friends.yml
- name: Friend 1
  url: https://friend1.com
  description: A great blog

- name: Friend 2
  url: https://friend2.com
  description: Another great blog
```

### 在模板中使用

透過 `site.data` 存取：

```ejs
<!-- 導覽選單 -->
<nav>
  <% for (var name in site.data.menu) { %>
    <a href="<%= site.data.menu[name] %>"><%= name %></a>
  <% } %>
</nav>

<!-- 友情連結 -->
<% if (site.data.friends) { %>
  <ul class="friends">
    <% site.data.friends.forEach(function(friend){ %>
      <li>
        <a href="<%= friend.url %>"><%= friend.name %></a>
        <span><%= friend.description %></span>
      </li>
    <% }) %>
  </ul>
<% } %>
```

### 用途範例

- 導覽選單配置
- 社群連結
- 友情連結
- 網站公告
- 贊助商資訊
- 任何需要重複使用的結構化資料
