# Hexo API 參考

Hexo API 用於開發插件和深度自訂主題功能。

## 目錄

- [初始化與生命週期](#初始化與生命週期)
- [事件系統](#事件系統)
- [區域變數 (Locals)](#區域變數-locals)
- [擴展 API](#擴展-api)
  - [Filter 過濾器](#filter-過濾器)
  - [Helper 輔助函數](#helper-輔助函數)
  - [Generator 產生器](#generator-產生器)
  - [Tag 標籤](#tag-標籤)
  - [Renderer 渲染器](#renderer-渲染器)
  - [Injector 注入器](#injector-注入器)
  - [Console 控制台](#console-控制台)

## 初始化與生命週期

### 建立 Hexo 實例

```javascript
const Hexo = require('hexo');
const hexo = new Hexo(process.cwd(), {});

// 初始化
hexo.init().then(() => {
  // 載入來源檔案
  return hexo.load();
}).then(() => {
  // 執行指令
  return hexo.call('generate');
}).then(() => {
  // 結束
  return hexo.exit();
}).catch(err => {
  return hexo.exit(err);
});
```

### 主要方法

| 方法                    | 說明                   |
| ----------------------- | ---------------------- |
| `hexo.init()`           | 初始化，載入配置和插件 |
| `hexo.load()`           | 載入來源檔案           |
| `hexo.watch()`          | 監視檔案變化           |
| `hexo.call(name, args)` | 執行控制台指令         |
| `hexo.exit(err)`        | 結束並儲存資料庫       |

## 事件系統

Hexo 繼承自 Node.js 的 EventEmitter。

### 可用事件

| 事件             | 說明             | 回傳資料          |
| ---------------- | ---------------- | ----------------- |
| `deployBefore`   | 部署前觸發       | -                 |
| `deployAfter`    | 部署後觸發       | -                 |
| `generateBefore` | 產生前觸發       | -                 |
| `generateAfter`  | 產生後觸發       | -                 |
| `processBefore`  | 處理前觸發       | Box 根目錄路徑    |
| `processAfter`   | 處理後觸發       | Box 根目錄路徑    |
| `new`            | 建立文章時觸發   | `{path, content}` |
| `exit`           | 結束前觸發       | -                 |
| `ready`          | 初始化完成時觸發 | -                 |

### 使用範例

```javascript
hexo.on('generateBefore', () => {
  console.log('開始產生網站...');
});

hexo.on('new', (post) => {
  console.log(`新文章: ${post.path}`);
});
```

## 區域變數 (Locals)

區域變數用於模板渲染，對應模板中的 `site` 變數。

### 預設變數

- `posts` - 所有文章
- `pages` - 所有頁面
- `categories` - 所有分類
- `tags` - 所有標籤

### 操作方法

```javascript
// 取得變數
hexo.locals.get('posts');

// 設定變數
hexo.locals.set('posts', function() {
  return this.database.model('Post').find({});
});

// 移除變數
hexo.locals.remove('posts');

// 取得所有變數
hexo.locals.toObject();

// 清除快取
hexo.locals.invalidate();
```

## 擴展 API

### Filter 過濾器

過濾器用於修改特定資料，依優先順序執行（數字越小越先執行）。

#### 註冊過濾器

```javascript
hexo.extend.filter.register('before_post_render', function(data) {
  // 修改文章資料
  data.title = data.title.toUpperCase();
  return data;
}, 10); // 優先順序
```

#### 可用過濾器類型

##### 文章處理

| 類型                 | 說明       | 參數   |
| -------------------- | ---------- | ------ |
| `before_post_render` | 文章渲染前 | `data` |
| `after_post_render`  | 文章渲染後 | `data` |

##### 生命週期

| 類型              | 說明     |
| ----------------- | -------- |
| `after_init`      | 初始化後 |
| `before_exit`     | 結束前   |
| `before_generate` | 產生前   |
| `after_generate`  | 產生後   |
| `after_clean`     | 清理後   |

##### 內容與路由

| 類型              | 說明             |
| ----------------- | ---------------- |
| `post_permalink`  | 決定文章永久連結 |
| `new_post_path`   | 決定新文章路徑   |
| `template_locals` | 修改模板區域變數 |

##### 渲染與伺服器

| 類型                | 說明               |
| ------------------- | ------------------ |
| `after_render:html` | HTML 渲染後        |
| `after_render:css`  | CSS 渲染後         |
| `server_middleware` | 新增伺服器中介軟體 |

#### 實用範例

```javascript
// 為外部連結新增 target="_blank"
hexo.extend.filter.register('after_post_render', function(data) {
  data.content = data.content.replace(
    /<a href="(https?:\/\/[^"]+)">/g,
    '<a href="$1" target="_blank" rel="noopener">'
  );
  return data;
});

// 修改模板變數
hexo.extend.filter.register('template_locals', function(locals) {
  locals.now = Date.now();
  return locals;
});
```

### Helper 輔助函數

輔助函數用於在模板中快速插入程式碼片段。

#### 註冊輔助函數

```javascript
hexo.extend.helper.register('greeting', function(name) {
  return `Hello, ${name}!`;
});
```

#### 在模板中使用

```ejs
<%= greeting('World') %>
<!-- 輸出: Hello, World! -->
```

#### 存取其他輔助函數

```javascript
hexo.extend.helper.register('my_link', function(path, text) {
  // 使用內建的 url_for 輔助函數
  return `<a href="${this.url_for(path)}">${text}</a>`;
});
```

#### 在插件中取得輔助函數

```javascript
const helper = hexo.extend.helper.get('url_for').bind(hexo);
const url = helper('/about');
```

### Generator 產生器

產生器根據處理後的檔案建立路由。

#### 註冊產生器

```javascript
hexo.extend.generator.register('my_generator', function(locals) {
  return {
    path: 'about/index.html',
    data: { title: 'About' },
    layout: ['page', 'index']
  };
});
```

#### 回傳格式

| 屬性     | 說明                       |
| -------- | -------------------------- |
| `path`   | 路由路徑（不含開頭 `/`）   |
| `data`   | 要渲染的資料               |
| `layout` | 使用的佈局（陣列或字串）   |

#### Generator 範例

```javascript
// 產生文章頁面
hexo.extend.generator.register('post', function(locals) {
  return locals.posts.map(function(post) {
    return {
      path: post.path,
      data: post,
      layout: ['post', 'index']
    };
  });
});

// 產生分頁
const pagination = require('hexo-pagination');

hexo.extend.generator.register('archive', function(locals) {
  return pagination('archives/index.html', locals.posts, {
    perPage: 10,
    layout: ['archive', 'index'],
    data: {}
  });
});

// 複製檔案
hexo.extend.generator.register('asset', function(locals) {
  return {
    path: 'file.txt',
    data: function() {
      return fs.createReadStream('path/to/file.txt');
    }
  };
});
```

### Tag 標籤

標籤外掛用於在文章中插入特定內容。

#### 基本註冊

```javascript
// 簡單標籤
hexo.extend.tag.register('youtube', function(args) {
  const id = args[0];
  return `<iframe src="https://www.youtube.com/embed/${id}"></iframe>`;
});
```

#### 帶結束標籤

```javascript
hexo.extend.tag.register('pullquote', function(args, content) {
  const className = args.join(' ');
  return `<blockquote class="${className}">${content}</blockquote>`;
}, { ends: true });
```

#### 非同步標籤

```javascript
hexo.extend.tag.register('include', function(args) {
  const filename = args[0];
  return fs.readFile(filename, 'utf8');
}, { async: true });
```

#### 使用方式（在文章中）

```markdown
{% youtube dQw4w9WgXcQ %}

{% pullquote center %}
這是引用文字
{% endpullquote %}
```

#### 取消註冊

```javascript
hexo.extend.tag.unregister('youtube');
```

### Renderer 渲染器

渲染器用於轉換內容格式。

#### 註冊渲染器

```javascript
// 非同步渲染器
hexo.extend.renderer.register('scss', 'css', function(data, options) {
  return sass.render({
    file: data.path,
    data: data.text
  }).then(result => result.css);
});

// 同步渲染器
hexo.extend.renderer.register('ejs', 'html', function(data, options) {
  return ejs.render(data.text, options);
}, true);
```

#### 參數說明

| 參數       | 說明                         |
| ---------- | ---------------------------- |
| `name`     | 輸入副檔名（小寫，不含 `.`） |
| `output`   | 輸出副檔名                   |
| `function` | 渲染函數                     |
| `sync`     | 是否同步（預設 `false`）     |

#### 停用 Nunjucks 處理

```javascript
function renderer(data, options) {
  // ...
}
renderer.disableNunjucks = true;

hexo.extend.renderer.register('html', 'html', renderer);
```

### Injector 注入器

注入器用於在 HTML 特定位置插入靜態程式碼。

#### 基本用法

```javascript
hexo.extend.injector.register(entry, value, to);
```

#### Entry 注入點

| 值           | 說明         |
| ------------ | ------------ |
| `head_begin` | `<head>` 後  |
| `head_end`   | `</head>` 前 |
| `body_begin` | `<body>` 後  |
| `body_end`   | `</body>` 前 |

#### To 目標頁面

| 值         | 說明     |
| ---------- | -------- |
| `default`  | 所有頁面 |
| `home`     | 首頁     |
| `post`     | 文章頁   |
| `page`     | 獨立頁面 |
| `archive`  | 歸檔頁   |
| `category` | 分類頁   |
| `tag`      | 標籤頁   |

#### Injector 範例

```javascript
// 注入 CSS
hexo.extend.injector.register('head_end', '<link rel="stylesheet" href="/custom.css">', 'default');

// 注入 JS（僅文章頁）
hexo.extend.injector.register('body_end', '<script src="/post.js"></script>', 'post');

// 使用函數動態產生
hexo.extend.injector.register('head_end', () => {
  return `<meta name="generator" content="Hexo ${hexo.version}">`;
}, 'default');
```

### Console 控制台

控制台是 Hexo 與使用者溝通的橋樑。

#### 註冊指令

```javascript
hexo.extend.console.register('hello', '打招呼指令', {
  usage: '[name]',
  arguments: [
    { name: 'name', desc: '你的名字' }
  ],
  options: [
    { name: '-u, --uppercase', desc: '使用大寫' }
  ]
}, function(args) {
  const name = args._[0] || 'World';
  let greeting = `Hello, ${name}!`;

  if (args.uppercase) {
    greeting = greeting.toUpperCase();
  }

  console.log(greeting);
});
```

#### 使用指令

```bash
hexo hello Ray
# 輸出: Hello, Ray!

hexo hello Ray -u
# 輸出: HELLO, RAY!
```

## 配置存取

在擴展中可存取配置：

```javascript
// 網站配置
hexo.config.title

// 主題配置
hexo.theme.config.menu

// 合併後的配置（Hexo 5+）
hexo.theme.config  // 已合併主題和網站配置
```

## 腳本檔案位置

自訂腳本可放置於：

- 專案根目錄 `scripts/` 資料夾
- 主題 `themes/<name>/scripts/` 資料夾

Hexo 初始化時會自動載入這些腳本。
