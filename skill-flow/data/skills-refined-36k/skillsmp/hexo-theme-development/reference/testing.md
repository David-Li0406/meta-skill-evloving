# Hexo 主題測試參考

本文檔參考 Hexo 官方核心的測試實踐，提供通用的主題測試指南，適用於 EJS、Nunjucks、Pug 等模板引擎。

## 目錄

- [測試架構概覽](#測試架構概覽)
- [專案設置](#專案設置)
- [單元測試](#單元測試)
- [配置檔驗證](#配置檔驗證)
- [程式碼品質檢查](#程式碼品質檢查)
- [GitHub Actions CI/CD](#github-actions-cicd)
- [功能測試](#功能測試)

## 測試架構概覽

完整的主題測試包含以下層面：

| 類型        | 工具                  | 用途                   |
| ----------- | --------------------- | ---------------------- |
| 單元測試    | Mocha + Chai          | 測試輔助函數、標籤外掛 |
| 配置驗證    | js-yaml               | 驗證 YAML 檔案格式     |
| JS Linting  | ESLint                | JavaScript 程式碼品質  |
| CSS Linting | Stylelint             | 樣式表程式碼品質       |
| 覆蓋率      | c8                    | 程式碼覆蓋率報告       |
| 功能測試    | hexo-theme-unit-test  | 主題功能完整性         |
| CI/CD       | GitHub Actions        | 自動化測試流程         |

## 專案設置

### package.json

```json
{
  "name": "hexo-theme-mytheme",
  "version": "1.0.0",
  "scripts": {
    "eslint": "eslint scripts/ source/js/ test/",
    "stylelint": "stylelint \"source/css/**/*.css\"",
    "test": "mocha test/index.js",
    "test:cov": "c8 --reporter=lcov npm test",
    "lint": "npm run eslint && npm run stylelint"
  },
  "devDependencies": {
    "chai": "^5.0.0",
    "c8": "^10.0.0",
    "eslint": "^9.0.0",
    "hexo": "^7.0.0",
    "js-yaml": "^4.0.0",
    "mocha": "^10.0.0",
    "sinon": "^17.0.0",
    "stylelint": "^16.0.0",
    "stylelint-config-standard": "^36.0.0"
  }
}
```

### 目錄結構

```text
themes/mytheme/
├── test/
│   ├── index.js           # 測試入口
│   ├── helpers/           # 輔助函數測試
│   │   ├── index.js
│   │   └── url-helper.js
│   ├── tags/              # 標籤外掛測試
│   │   └── index.js
│   └── validate/          # 配置驗證測試
│       └── index.js
├── .github/
│   └── workflows/
│       └── ci.yml
├── eslint.config.js
├── .stylelintrc.json
└── package.json
```

## 單元測試

### 測試入口 (test/index.js)

```javascript
'use strict';

require('chai').should();

describe('MyTheme', () => {
  require('./helpers');
  require('./tags');
  require('./validate');
});
```

### 輔助函數測試

#### 基本結構 (test/helpers/index.js)

```javascript
'use strict';

describe('Helpers', () => {
  require('./url-helper');
  // 加入更多輔助函數測試
});
```

#### URL 輔助函數測試 (test/helpers/url-helper.js)

參考 Hexo 官方 `url_for` 測試方式：

```javascript
'use strict';

const Hexo = require('hexo');

describe('url-helper', () => {
  const hexo = new Hexo(__dirname, { silent: true });

  before(() => hexo.init());

  // 載入自訂輔助函數
  require('../../scripts/helpers/url-helper')(hexo);

  const urlHelper = hexo.extend.helper.get('my_url').bind(hexo);

  it('should encode path', () => {
    urlHelper('fôo.html').should.equal('/f%C3%B4o.html');
  });

  it('should handle absolute URL', () => {
    urlHelper('https://example.com/').should.equal('https://example.com/');
  });

  it('should handle hash link', () => {
    urlHelper('#section').should.equal('#section');
  });

  it('should prepend root path', () => {
    hexo.config.root = '/blog/';
    urlHelper('about/').should.equal('/blog/about/');
    hexo.config.root = '/';
  });
});
```

#### 通用輔助函數測試範例

```javascript
'use strict';

const Hexo = require('hexo');

describe('reading-time', () => {
  const hexo = new Hexo(__dirname, { silent: true });

  before(() => hexo.init());

  require('../../scripts/helpers/reading-time')(hexo);

  const readingTime = hexo.extend.helper.get('reading_time').bind(hexo);

  it('should calculate reading time', () => {
    const content = 'word '.repeat(200); // 200 字
    readingTime(content).should.equal('1 min');
  });

  it('should handle empty content', () => {
    readingTime('').should.equal('0 min');
  });

  it('should strip HTML tags', () => {
    const content = '<p>' + 'word '.repeat(400) + '</p>';
    readingTime(content).should.equal('2 min');
  });
});
```

### 標籤外掛測試

#### 結構 (test/tags/index.js)

```javascript
'use strict';

describe('Tags', () => {
  require('./note-tag');
});
```

#### 標籤測試範例 (test/tags/note-tag.js)

```javascript
'use strict';

const Hexo = require('hexo');

describe('note tag', () => {
  const hexo = new Hexo(__dirname, { silent: true });

  before(() => hexo.init());

  // 註冊標籤
  require('../../scripts/tags/note')(hexo);

  it('should render note with default style', async () => {
    const result = await hexo.post.render(null, {
      content: '{% note %}This is a note{% endnote %}',
      engine: 'markdown'
    });
    result.content.should.include('<div class="note">');
    result.content.should.include('This is a note');
  });

  it('should render note with warning style', async () => {
    const result = await hexo.post.render(null, {
      content: '{% note warning %}Warning message{% endnote %}',
      engine: 'markdown'
    });
    result.content.should.include('class="note warning"');
  });

  it('should handle empty content', async () => {
    const result = await hexo.post.render(null, {
      content: '{% note %}{% endnote %}',
      engine: 'markdown'
    });
    result.content.should.include('<div class="note">');
  });
});
```

## 配置檔驗證

### 驗證測試 (test/validate/index.js)

```javascript
'use strict';

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

describe('Validate', () => {
  const themeDir = path.resolve(__dirname, '../..');

  describe('Theme Config', () => {
    it('_config.yml should be valid YAML', () => {
      const configPath = path.join(themeDir, '_config.yml');
      const content = fs.readFileSync(configPath, 'utf8');

      (() => {
        yaml.load(content);
      }).should.not.throw();
    });
  });

  describe('Language Files', () => {
    const langDir = path.join(themeDir, 'languages');

    if (!fs.existsSync(langDir)) return;

    const files = fs.readdirSync(langDir).filter(f => f.endsWith('.yml'));

    files.forEach(file => {
      it(`${file} should be valid YAML`, () => {
        const filePath = path.join(langDir, file);
        const content = fs.readFileSync(filePath, 'utf8');

        (() => {
          yaml.load(content);
        }).should.not.throw();
      });
    });
  });

  describe('Language Consistency', () => {
    const langDir = path.join(themeDir, 'languages');

    if (!fs.existsSync(langDir)) return;

    const files = fs.readdirSync(langDir).filter(f => f.endsWith('.yml'));
    if (files.length < 2) return;

    const defaultLang = yaml.load(
      fs.readFileSync(path.join(langDir, files[0]), 'utf8')
    );
    const defaultKeys = Object.keys(flattenObject(defaultLang)).sort();

    files.slice(1).forEach(file => {
      it(`${file} should have same keys as ${files[0]}`, () => {
        const lang = yaml.load(
          fs.readFileSync(path.join(langDir, file), 'utf8')
        );
        const keys = Object.keys(flattenObject(lang)).sort();

        keys.should.deep.equal(defaultKeys);
      });
    });
  });
});

// 扁平化巢狀物件
function flattenObject(obj, prefix = '') {
  const result = {};
  for (const key in obj) {
    const newKey = prefix ? `${prefix}.${key}` : key;
    if (typeof obj[key] === 'object' && obj[key] !== null) {
      Object.assign(result, flattenObject(obj[key], newKey));
    } else {
      result[newKey] = obj[key];
    }
  }
  return result;
}
```

## 程式碼品質檢查

### ESLint 配置 (eslint.config.js)

```javascript
import js from '@eslint/js';

export default [
  js.configs.recommended,
  {
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: 'module',
      globals: {
        // Browser
        window: 'readonly',
        document: 'readonly',
        // Node
        require: 'readonly',
        module: 'readonly',
        __dirname: 'readonly',
        process: 'readonly',
        // Hexo
        hexo: 'readonly',
        // Test
        describe: 'readonly',
        it: 'readonly',
        before: 'readonly',
        after: 'readonly',
        beforeEach: 'readonly',
        afterEach: 'readonly'
      }
    },
    rules: {
      'indent': ['error', 2],
      'quotes': ['error', 'single'],
      'semi': ['error', 'always'],
      'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      'no-console': 'off'
    }
  },
  {
    ignores: ['node_modules/', 'public/', '.deploy_git/']
  }
];
```

### Stylelint 配置 (.stylelintrc.json)

#### CSS/SCSS 專案

```json
{
  "extends": ["stylelint-config-standard"],
  "rules": {
    "indentation": 2,
    "string-quotes": "single",
    "no-duplicate-selectors": true,
    "selector-class-pattern": "^[a-z][a-z0-9-]*$",
    "declaration-block-no-duplicate-properties": true
  }
}
```

#### Stylus 專案

```json
{
  "plugins": ["stylelint-stylus"],
  "extends": ["stylelint-stylus/standard"],
  "rules": {
    "stylus/semicolon": "always",
    "stylus/declaration-colon": "always"
  }
}
```

## GitHub Actions CI/CD

### 完整 CI 工作流程 (.github/workflows/ci.yml)

```yaml
name: CI

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run eslint

      - name: Run Stylelint
        run: npm run stylelint

  test:
    needs: lint
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Run tests with coverage
        run: npm run test:cov

  build:
    needs: test
    runs-on: ${{ matrix.os }}

    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        node-version: ['18', '20', '22']

    steps:
      - name: Checkout hexo-starter
        uses: actions/checkout@v4
        with:
          repository: hexojs/hexo-starter
          submodules: true

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install Hexo dependencies
        run: npm install

      - name: Checkout theme
        uses: actions/checkout@v4
        with:
          path: themes/mytheme

      - name: Configure theme
        run: echo "theme: mytheme" >> _config.yml

      - name: Generate site
        run: npx hexo generate

      - name: Check for errors
        run: |
          if [ -f "debug.log" ]; then
            cat debug.log
            exit 1
          fi
        shell: bash
```

### 簡化版工作流程

如果不需要多平台測試：

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout hexo-starter
        uses: actions/checkout@v4
        with:
          repository: hexojs/hexo-starter

      - uses: actions/setup-node@v4
        with:
          node-version: '20'

      - run: npm install

      - name: Checkout theme
        uses: actions/checkout@v4
        with:
          path: themes/mytheme

      - run: |
          echo "theme: mytheme" >> _config.yml
          npx hexo generate
```

## 功能測試

### 使用 hexo-theme-unit-test

官方提供的測試環境，包含各種測試情境的文章：

```bash
# 1. 複製測試儲存庫
git clone https://github.com/hexojs/hexo-theme-unit-test.git
cd hexo-theme-unit-test

# 2. 安裝依賴
npm install

# 3. 安裝你的主題
git clone https://github.com/your/theme.git themes/mytheme

# 4. 設定主題
echo "theme: mytheme" >> _config.yml

# 5. 啟動伺服器測試
npx hexo server
```

### 功能測試清單

#### Head 區塊

- [ ] DOCTYPE 宣告正確（推薦 `<!DOCTYPE html>`）
- [ ] charset 設為 UTF-8
- [ ] 頁面標題正確顯示
- [ ] favicon 正常載入
- [ ] meta generator 標籤存在

#### 首頁

- [ ] 文章列表顯示正確
- [ ] 只顯示摘要（非全文）
- [ ] 分頁功能正常
- [ ] 日期格式正確

#### 文章頁

- [ ] 標題顯示正確
- [ ] 內容渲染正確
- [ ] 分類和標籤顯示
- [ ] 上一篇/下一篇導覽
- [ ] 評論區塊（如啟用）
- [ ] 程式碼高亮正常
- [ ] 圖片正常載入

#### 歸檔頁

- [ ] 文章按時間排序
- [ ] 年月分組正確
- [ ] 分頁功能正常

#### 特殊情況

- [ ] 無標題文章可存取
- [ ] 長標題不破版
- [ ] 特殊字元正確顯示
- [ ] 外部連結開新分頁（`target="_blank"`）
- [ ] 外部連結有 `rel="noopener"`

#### 效能

- [ ] 使用片段快取 (`fragment_cache`)
- [ ] 靜態資源壓縮

#### 響應式設計

- [ ] 桌面版正常顯示
- [ ] 平板版正常顯示
- [ ] 手機版正常顯示
- [ ] 導覽選單可用

#### 可選功能

- [ ] 國際化 (i18n)
- [ ] SEO 優化
- [ ] RSS 自動發現

### 自動化建置測試

```javascript
// test/build.js
'use strict';

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

describe('Build', function() {
  this.timeout(60000);

  const publicDir = path.resolve(__dirname, '../public');

  before(() => {
    execSync('npx hexo clean && npx hexo generate', {
      cwd: path.resolve(__dirname, '..'),
      stdio: 'inherit'
    });
  });

  it('should generate public directory', () => {
    fs.existsSync(publicDir).should.be.true;
  });

  it('should generate index.html', () => {
    const indexPath = path.join(publicDir, 'index.html');
    fs.existsSync(indexPath).should.be.true;
  });

  it('should include DOCTYPE', () => {
    const indexPath = path.join(publicDir, 'index.html');
    const content = fs.readFileSync(indexPath, 'utf8');
    content.should.match(/<!DOCTYPE html>/i);
  });

  it('should include charset meta', () => {
    const indexPath = path.join(publicDir, 'index.html');
    const content = fs.readFileSync(indexPath, 'utf8');
    content.should.match(/charset=["']?utf-8["']?/i);
  });

  it('should generate archives page', () => {
    const archivePath = path.join(publicDir, 'archives/index.html');
    fs.existsSync(archivePath).should.be.true;
  });

  it('should generate CSS files', () => {
    const cssDir = path.join(publicDir, 'css');
    fs.existsSync(cssDir).should.be.true;
    fs.readdirSync(cssDir).length.should.be.above(0);
  });
});
```

## 測試執行命令

```bash
# 執行所有測試
npm test

# 執行測試並產生覆蓋率報告
npm run test:cov

# 只執行 lint
npm run lint

# 執行 ESLint
npm run eslint

# 執行 Stylelint
npm run stylelint

# 監視模式執行測試
npx mocha --watch test/index.js

# 執行特定測試檔案
npx mocha test/helpers/url-helper.js
```

## 測試最佳實踐

### 1. 測試命名清晰

```javascript
// 好的命名
it('should encode special characters in URL', () => {});
it('should return empty string when input is null', () => {});

// 不好的命名
it('test1', () => {});
it('works', () => {});
```

### 2. 每個測試獨立

```javascript
describe('helper', () => {
  let hexo;

  beforeEach(() => {
    // 每個測試前重新初始化
    hexo = new Hexo(__dirname, { silent: true });
  });

  afterEach(() => {
    // 清理
    hexo = null;
  });
});
```

### 3. 測試邊界情況

```javascript
describe('truncate', () => {
  it('should handle normal input', () => {});
  it('should handle empty string', () => {});
  it('should handle null', () => {});
  it('should handle very long string', () => {});
  it('should handle special characters', () => {});
});
```

### 4. 使用 fixtures

```text
test/
└── fixtures/
    ├── sample-post.md
    ├── config.yml
    └── expected-output.html
```

```javascript
const fs = require('fs');
const path = require('path');

const fixture = (name) => {
  return fs.readFileSync(
    path.join(__dirname, 'fixtures', name),
    'utf8'
  );
};

it('should render post correctly', () => {
  const input = fixture('sample-post.md');
  const expected = fixture('expected-output.html');
  // ...
});
```
