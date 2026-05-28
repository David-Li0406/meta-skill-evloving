# Collect-UI 测试用例生成指南

> ⚠️ **重要**：在生成任何测试用例之前，必须先阅读并遵循本指南的所有规则。

## 🔴 生成测试用例时的绝对禁止事项

### 禁止1：JSON 键名缺少引号
```json
// ❌ 绝对禁止
{"rules": [{type: "email", "message": "邮箱"}]}
{"danger": true}

// ✅ 必须这样写
{"rules": [{"type": "email", "message": "邮箱"}]}
{"danger": true}
```

### 禁止2：React children 是对象而不是数组
```json
// ❌ 绝对禁止
{"tag": "col", "children": {"tag": "div"}}
{"tag": "form-item", "children": {"tag": "input"}}
{"tag": "dropdown", "children": {"tag": "button"}}

// ✅ 必须这样写
{"tag": "col", "children": [{"tag": "div"}]}
{"tag": "form-item", "children": [{"tag": "input"}]}
{"tag": "dropdown", "children": [{"tag": "button"}]}
```

### 禁止3：模板变量混合文本未包裹
```json
// ❌ 绝对禁止
{"children": "当前页: ${page}, 共 ${total} 条"}

// ✅ 必须这样写
{"children": "${'当前页: '+page+', 共: '+total+' 条'}"}
```

---

## 🟢 生成测试用例的标准流程

### 生成前检查
```
在编写任何 JSON 之前，必须确认：
1. 所有键都有双引号吗？
2. children 是数组吗？（除了纯文本）
3. 混合文本在 ${...} 内吗？
```

### 生成后验证
```bash
# 生成后必须立即运行
npx jsonlint demo/data/test/xxx-demo.json

# 验证不通过不能提交
```

---

## 📋 生成测试用例自检清单

### JSON 格式检查
- [ ] **所有键都有双引号**
  - `{type: "email"}` → `{"type": "email"}`
  - `{min: 6}` → `{"min": 6}`
  - `{danger}` → `{"danger": true}`

### React children 检查
- [ ] **children 是数组或字符串**
  - `{"children": "文本"}` ✅
  - `{"children": [{"tag": "span"}]}` ✅
  - `{"children": {"tag": "span"}}` ❌

- [ ] **需要数组的场景**
  - `col` 组件的 children
  - `row` 组件的 children
  - `form-item` 组件的 children
  - `dropdown` 组件的 children
  - 任何包含组件对象的 children

### 模板变量检查
- [ ] **混合文本在 ${...} 内**
  - `❌ "当前页: ${page}"`
  - `✅ "${'当前页: '+page}"`

---

## 🚫 常见错误模式（必须避免）

### 错误1：键名缺少引号
```json
// ❌
{"rules": [{type: "email"}]}
{"children": {"tag": "button"}}

// ✅
{"rules": [{"type": "email"}]}
{"children": [{"tag": "button"}]}
```

### 错误2：children 是对象
```json
// ❌
{"tag": "form-item", "children": {"tag": "input"}}

// ✅
{"tag": "form-item", "children": [{"tag": "input"}]}
```

### 错误3：模板变量混合文本
```json
// ❌
{"children": "当前页: ${page}"}

// ✅
{"children": "${'当前页: '+page}"}
```

---

## ✅ 正确示例集合

### 示例1：完整表单测试用例
```json
{
  "tag": "app",
  "children": [
    {
      "tag": "layout-fit",
      "initStore": {},
      "children": [
        {
          "tag": "div",
          "style": {"padding": "20px"},
          "children": [
            {"tag": "h3", "children": "表单测试"},
            {
              "tag": "form",
              "name": "testForm",
              "children": [
                {
                  "tag": "form-item",
                  "name": "username",
                  "label": "用户名",
                  "rules": [{"required": true, "message": "请输入用户名"}],
                  "children": [{"tag": "input", "placeholder": "请输入用户名"}]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### 示例2：完整布局测试用例
```json
{
  "tag": "layout-fit",
  "initStore": {},
  "children": [
    {
      "tag": "div",
      "style": {"padding": "20px"},
      "children": [
        {
          "tag": "row",
          "gutter": 16,
          "children": [
            {"tag": "col", "span": 12, "children": [{"tag": "div", "style": {"background": "#0092ff", "padding": "24px", "color": "#fff"}, "children": "col-12"}]},
            {"tag": "col", "span": 12, "children": [{"tag": "div", "style": {"background": "#0092ff", "padding": "24px", "color": "#fff"}, "children": "col-12"}]}
          ]
        }
      ]
    }
  ]
}
```

---

## 🔄 快速检查三步法

```
生成 JSON 时快速检查：

1. 看所有键 → 有双引号吗？
2. 看所有 children → 是数组或字符串吗？
3. 看所有模板变量 → 混合文本在 ${...} 内吗？

完成后 → 运行 npx jsonlint 验证
```

---

## 🎯 测试用例质量标准

生成的测试用例必须满足：
1. ✅ JSON 格式验证通过
2. ✅ 没有 React children 错误
3. ✅ 没有模板变量错误
4. ✅ 浏览器控制台无错误

**不满足以上标准的测试用例不能提交！**

---

## 📚 参考资源

- `AGENTS.md` - 项目开发指南
- `demo/data/` - 正确示例集合
- `npx jsonlint <file>` - JSON 验证

---

#### Tabs 组件最佳实践
**问题**：Tabs 内容高度为 0 或显示不全，标签页切换不明显
**分析**：
- **上层封装** (`src/components/tabs/tabs.tsx`): 支持 `activeKey` 自动绑定状态，无需手动设置 action
- **底层 API** (Ant Design Tabs): `type="line"` 提供更好的视觉反馈，`flex` 布局确保内容填充高度

**修复方案**：
```json
{
  "tag": "tabs",
  "activeKey": "${activeTab}",
  "type": "line",
  "size": "large",
  "style": {
    "flex": 1,
    "display": "flex", 
    "flexDirection": "column",
    "background": "#fff",
    "padding": "20px",
    "borderRadius": "8px",
    "margin": "20px"
  },
  "items": [
    {
      "key": "tab1",
      "label": "标签页 1",
      "children": [
        {
          "tag": "div",
          "children": "内容",
          "style": {
            "padding": "20px",
            "background": "#fff",
            "borderRadius": "6px",
            "color": "#333",
            "height": "100%"
          }
        }
      ]
    }
  ]
}
```
**要点**：
- 使用 `activeKey` 实现自动状态绑定
- 添加 `flex` 样式确保高度填充
- `type="line"` 比 `card` 提供更清晰的激活状态
- 内容区域使用白色背景和 `height: "100%"` 实现全高显示
- 无需额外 action，组件自动处理状态更新

---

## 🔧 常见错误诊断与解决方案

### 错误1：`keyField is required` (listview)
**症状**：控制台报错 "listview 中 keyField is required"，列表不显示
**原因**：listview 组件缺少必需的 `keyField` 属性
**修复**：
```json
{
  "tag": "listview",
  "keyField": "id",
  "itemData": "${dataList}",
  "itemAttr": {...}
}
```
**原则**：
- listview 必须设置 `keyField` 指定数据唯一标识字段
- 如果数据没有唯一字段，组件会自动回退使用 `id` 或生成 UUID
- 推荐显式设置 `keyField` 以提高性能和可预测性

---

### 错误2：JSON 解析失败
**症状**：`[plugin:vite:json] Failed to parse JSON file, invalid JSON syntax`
**原因**：JSON 格式错误，常见于：
- 缺少逗号或多余逗号
- 括号不匹配
- 缩进错误导致结构混乱
- **键名缺少引号（最常见！）**
**修复**：
1. 使用 JSON 验证工具检查：`npx jsonlint <file>`
2. 在线验证：https://jsonlint.com/
3. IDE 插件验证（VS Code 自动检测）

### 错误2.1：JSON 键名缺少引号
**症状**：`invalid JSON syntax found at position XXX`
**原因**：JSON 中所有的键必须是带引号的字符串

**错误示例**：
```json
// ❌ 错误：键名缺少引号
{
  "rules": [
    {type: "email", "message": "请输入邮箱"},
    {len: 11, "message": "手机号必须是11位"},
    {min: 6, "message": "密码至少6个字符"}
  ]
}
```

**正确示例**：
```json
// ✅ 正确：所有键都有引号
{
  "rules": [
    {"type": "email", "message": "请输入邮箱"},
    {"len": 11, "message": "手机号必须是11位"},
    {"min": 6, "message": "密码至少6个字符"}
  ]
}
```

**关键点**：
- JSON 中**所有键**都必须用双引号包围
- JavaScript 对象字面量可以省略键的引号，但 JSON 不行
- 验证规则中的 `type`、`len`、`min`、`max`、`pattern` 等都需要引号
- 编写完成后务必运行 `npx jsonlint <file>` 验证

**预防**：
- 编写 JSON 后立即验证
- 参考 `demo/data/` 中的示例配置
- 使用 VS Code 等支持 JSON 语法的编辑器

---

### 错误2.2：React children 不能是对象
**症状**：`Objects are not valid as a React child (found: object with keys {tag, style, children})`
**原因**：`children` 属性包含一个对象而不是数组或字符串

**错误示例**：
```json
// ❌ 错误：children 是对象
{
  "tag": "col",
  "span": 6,
  "children": {"tag": "div", "style": {...}, "children": "内容"}
}
```

**正确示例**：
```json
// ✅ 正确：children 是数组
{
  "tag": "col",
  "span": 6,
  "children": [{"tag": "div", "style": {...}, "children": "内容"}]
}
```

**关键点**：
- React 的 `children` 必须是字符串、数字、数组或 null
- 不能直接传递组件对象作为 children
- 需要将组件对象包装在数组中：`[{"tag": "div", ...}]`
- 多层嵌套时每一层都需要是数组

**常见场景**：
- `col` 组件的 children
- `row` 组件的 children
- 任何需要嵌套组件的地方

**预防**：
- 使用 jsonlint 验证 JSON 格式
- 参考 `demo/data/layout-demo.json` 中的正确用法
- 注意 `children` 应该是 `[...]` 而不是 `{...}`

---

### 错误3：数据嵌套层级过深
**症状**：`itemData` 或 `rowData` 无法正确渲染
**原因**：不必要的嵌套结构如 `{ "data": { "list": [...] } }`
**修复**：
```json
// ❌ 错误：多余嵌套
{
  "initStore": {
    "tableData": {
      "list": [...]
    }
  },
  "rowData": "${tableData.list}"
}

// ✅ 正确：扁平结构
{
  "initStore": {
    "dataList": [...]
  },
  "rowData": "${dataList}"
}
```
**原则**：
- 数据直接用数组，不要嵌套
- 参考 `demo/data/demo.json` 中的数据结构
- 保持简单直接，减少引用路径

---

### 错误4：listview 属性名错误
**症状**：列表项不显示或渲染异常
**原因**：使用了错误的属性名
**修复**：
```json
// ❌ 错误：使用 renderItem
{
  "tag": "listview",
  "renderItem": {...}
}

// ✅ 正确：使用 itemAttr
{
  "tag": "listview",
  "keyField": "id",
  "itemData": "${dataList}",
  "itemAttr": {...}
}
```
**原则**：
- listview 使用 `itemAttr` 定义项模板，不是 `renderItem`
- table 使用 `columnDefs` 定义列，不是 `columns`
- 参考 `readme/components/listview.md` 文档

---

### 错误5：模板变量引用错误
**症状**：模板变量显示为 `${...}` 原始字符串或 undefined
**原因**：变量名或引用格式错误
**修复**：
```json
// ❌ 错误：使用 item
{
  "itemAttr": {
    "children": "${item.title}"
  }
}

// ✅ 正确：使用 row
{
  "itemAttr": {
    "children": "${row.title}"
  }
}
```
**原则**：
- listview 项模板中使用 `${row.field}` 访问数据
- table 列中使用 `${data.field}` 或 `${value}`
- form 中使用 `${form.getFieldValue('field')}`
- 参考对应组件文档中的变量说明

---

### 错误6：table API 空引用
**症状**：`Cannot read properties of null (reading 'api')`
**原因**：ag-grid API 在组件未初始化时就被访问
**修复** (`src/components/table/table.tsx`)：
```typescript
// 添加空值检查
if (gridRef.current && gridRef.current.api) {
  gridRef.current.api.resetColumnState();
  gridRef.current.api.sizeColumnsToFit();
}
```
**原则**：
- 异步操作前检查引用有效性
- resize 事件中使用延迟确保 DOM 就绪

---

### 错误7：Tabs 内容高度为 0
**症状**：标签页切换后内容区域空白
**原因**：缺少 flex 布局样式
**修复**：
```json
{
  "tag": "tabs",
  "type": "line",
  "style": {
    "flex": 1,
    "display": "flex",
    "flexDirection": "column"
  }
}
```
**原则**：
- Tabs 组件需要 flex 容器确保内容填充
- 父容器也要设置高度
- 使用 `type="line"` 比 `card` 视觉更清晰

---

### 错误8：不必要的 card 包裹
**症状**：布局过于嵌套，样式复杂
**原因**：所有组件都用 card 包裹
**修复**：
```json
// ❌ 过度嵌套
{
  "tag": "card",
  "children": [{
    "tag": "listview",
    ...
  }]
}

// ✅ 简洁结构
{
  "tag": "listview",
  "className": "padding10",
  ...
}
```
**原则**：
- 简单展示不需要 card 包裹
- 使用 `className: "padding10"` 提供间距
- 只在需要卡片视觉效果时使用 card

---

## 📋 开发检查清单

### 编写 JSON 配置前
- [ ] 参考 `demo/frontend/page_data/data/` 中的生产示例
- [ ] 阅读 `readme/components/[组件名].md` 文档
- [ ] 确认组件必需属性（listview 需 keyField）

### JSON 编写时
- [ ] 扁平化数据结构，避免 `xxx.list` 嵌套
- [ ] 使用正确的属性名（itemAttr 不是 renderItem）
- [ ] 使用正确的变量引用（row 不是 item）

### 完成后
- [ ] 运行 `npx jsonlint <file>` 验证 JSON 格式
- [ ] 在浏览器中测试组件功能
- [ ] 检查浏览器控制台错误

---

## 🧪 JSON 测试验证技能

### 技能：自动检测和修复 JSON 错误

**使用场景**：当 Vite 报 `Failed to parse JSON file` 错误时

**操作步骤**：
```
1. 读取 dev.log 获取错误信息
2. 定位错误文件和位置
3. 修复 JSON 语法错误
4. 运行 npx jsonlint <file> 验证
```

### 常见 JSON 错误速查表

| 错误类型 | 错误示例 | 正确写法 |
|----------|----------|----------|
| 键名缺少引号 | `{type: "email"}` | `{"type": "email"}` |
| 键名缺少引号 | `{danger}` | `{"danger": true}` |
| 键名缺少引号 | `{min: 6}` | `{"min": 6}` |
| 括号不匹配 | `]}}` | `}]}` |
| 逗号错误 | `},]` | `}]` |
| 多余逗号 | `[1, 2, 3,]` | `[1, 2, 3]` |

### 验证脚本

```bash
#!/bin/bash
# validate-all-tests.sh - 验证所有测试 JSON 文件

cd /data/react/collect-ui/demo/data/test

for file in *.json; do
  echo "Checking $file..."
  if npx jsonlint "$file" > /dev/null 2>&1; then
    echo "  ✅ $file - 验证通过"
  else
    echo "  ❌ $file - 验证失败"
    npx jsonlint "$file" 2>&1 | head -5
  fi
done
```

### 从 dev.log 提取错误并修复

```bash
# 1. 查看 dev.log 中的错误
tail -50 /data/react/collect-ui/dev.log | grep "Failed to parse"

# 2. 定位错误文件
# 错误信息格式: File: /path/to/file.json:行:列

# 3. 修复后验证
npx jsonlint /path/to/file.json
```

### JSON 编写黄金法则

1. **所有键必须用双引号** - JSON 不是 JavaScript 对象
2. **所有字符串必须用双引号** - 包括 `"true"`, `"false"`, `"null"`
3. **数组/对象后无逗号** - 最后一个元素后不要加逗号
4. **使用 jsonlint 验证** - 编写完成后立即运行验证

### 自动化测试 CI

```yaml
# .github/workflows/validate-json.yml
name: Validate JSON
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install jsonlint
        run: npm install -g jsonlint
      - name: Validate all test files
        run: |
          for f in demo/data/test/*.json; do
            jsonlint "$f" || exit 1
          done
```

---

## 📚 参考资源

### 文档目录
- `readme/components/` - 所有组件详细文档
- `demo/data/` - 演示配置
- `demo/frontend/page_data/data/` - 生产配置示例
- `AGENTS.md` - 项目开发指南

### 常用组件文档
- `readme/components/listview.md` - 列表视图
- `readme/components/table.md` - 表格组件
- `readme/components/tabs.md` - 标签页
- `readme/components/form.md` - 表单

---

## 🎯 新增测试用例速查

### 基础组件测试
| 测试文件 | 组件 | 关键特性 |
|----------|------|----------|
| `breadcrumb-divider-demo.json` | Breadcrumb, Divider | 面包屑导航、分割线样式 |
| `button-demo.json` | Button | 按钮类型、危险按钮、图标按钮 |
| `icon-demo.json` | Icon | 图标使用、动态图标 |
| `badge-demo.json` | Badge | 徽章状态、计数显示 |
| `space-title-text-demo.json` | Space, Title, Div, Span | 间距控制、标题层级、文本标签 |
| `pagination-step-dropdown-demo.json` | Pagination, Step, Dropdown | 分页导航、步骤条、下拉菜单 |

### 表单组件测试
| 测试文件 | 组件 | 关键特性 |
|----------|------|----------|
| `input-demo.json` | Input | 基本输入、密码框、文本域 |
| `input-full-demo.json` | Input | 前置/后置图标、搜索框、字数统计 |
| `select-demo.json` | Select | 下拉选择、单选/多选 |
| `select-full-demo.json` | Select | 分组选项、搜索过滤、虚拟滚动 |
| `form-controls-demo.json` | Checkbox, Radio, Switch | 表单控件基础 |
| `form-controls-advanced-demo.json` | Checkbox, Radio, Switch | 复选框组、单选组、开关状态 |
| `date-progress-tag-demo.json` | Date, Progress, Tag, Tooltip | 日期选择、进度条、标签、提示 |
| `cascader-demo.json` | Cascader | 级联选择、动态加载 |
| `upload-demo.json` | Upload | 文件上传、拖拽上传、图片预览 |
| `form-validation-demo.json` | Form | 表单验证规则、动态验证 |

### 表格和列表组件测试
| 测试文件 | 组件 | 关键特性 |
|----------|------|----------|
| `table-demo.json` | Table | 基本表格、列配置 |
| `table-full-demo.json` | Table | 完整功能、分页、排序、筛选 |
| `listview-demo.json` | ListView | 列表渲染、点击事件 |
| `tree-demo.json` | Tree | 树形数据、展开/折叠 |

### 布局组件测试
| 测试文件 | 组件 | 关键特性 |
|----------|------|----------|
| `tabs-demo.json` | Tabs | 基本标签页 |
| `tabs-full-demo.json` | Tabs | 完整功能、图标、尺寸变化 |
| `card-demo.json` | Card | 卡片容器、标题、操作按钮 |
| `layout-demo.json` | Layout, Row, Col | 基础布局、栅格系统 |
| `layout-advanced-demo.json` | Layout, Row, Col, Flex | 高级布局、响应式栅格 |
| `dialog-demo.json` | Dialog | 对话框、确认框 |

### Actions 测试
| 测试文件 | Action | 关键特性 |
|----------|--------|----------|
| `actions-demo.json` | message, confirm, dialog, drawer, ajax | 消息提示、确认框、弹窗、抽屉、HTTP请求 |

---

## 📝 测试用例编写技能

### 技能：创建新的测试用例

**使用场景**：为新组件或现有组件添加测试用例

**操作步骤**：
```
1. 在 demo/data/test/ 创建 [组件名]-demo.json
2. 使用 app 标签包装（需要 message 等功能时）
3. 使用 layout-fit 管理布局
4. 添加 initStore 定义测试数据
5. 验证 JSON 格式：npx jsonlint <file>
6. 在 App.tsx 注册测试用例
```

### 测试用例模板

```json
{
  "tag": "app",
  "children": [
    {
      "tag": "layout-fit",
      "initStore": {
        "testData": []
      },
      "children": [
        {
          "tag": "div",
          "style": {"padding": "20px"},
          "children": [
            {"tag": "h3", "style": {"marginBottom": "16px"}, "children": "组件名称"},
            {"tag": "div", "style": {"marginBottom": "24px", "color": "#666"}, "children": "组件功能描述"},
            {
              "tag": "组件名",
              "属性": "值",
              "children": [...]
            }
          ]
        }
      ]
    }
  ]
}
```

### 测试用例命名规范

| 类型 | 命名格式 | 示例 |
|------|----------|------|
| 基础演示 | `[组件名]-demo.json` | `button-demo.json` |
| 完整功能 | `[组件名]-full-demo.json` | `select-full-demo.json` |
| 组合测试 | `[功能名]-test.json` | `form-validation-demo.json` |

### 测试用例注册流程

```typescript
// 1. 在 demo/App.tsx 添加 import
import testXxxConfig from "./data/test/xxx-demo.json"

// 2. 在 testCases 数组注册
{ 
  key: 'test/xxx-demo', 
  name: '组件名称', 
  description: '测试描述', 
  category: 'basic', 
  tags: ['组件', '标签'] 
}

// 3. 在 testConfigs 对象添加映射
'test/xxx-demo': testXxxConfig,
```

### 测试用例验证命令

```bash
# 验证单个文件
npx jsonlint demo/data/test/xxx-demo.json

# 批量验证所有测试文件
cd demo/data/test
for f in *.json; do npx jsonlint "$f"; done

# 检查 dev.log 中的错误
tail -100 /data/react/collect-ui/dev.log | grep "Failed to parse"
```

### 测试用例质量检查清单

- [ ] JSON 格式验证通过
- [ ] 使用 `app` 标签包装（需要 Actions 功能时）
- [ ] 使用 `layout-fit` 管理布局
- [ ] `initStore` 中包含必要的测试数据
- [ ] 组件属性名称正确（参考组件文档）
- [ ] 模板变量引用正确（使用 `row` 而不是 `item`）
- [ ] 在 App.tsx 正确注册
- [ ] 浏览器中测试通过
- [ ] 控制台无错误信息

### 常用组件测试模式

#### Input 组件测试
```json
{
  "tag": "input",
  "placeholder": "请输入...",
  "allowClear": true,
  "disabled": false,
  "maxLength": 100
}
```

#### Select 组件测试
```json
{
  "tag": "select",
  "value": "${selectedValue}",
  "options": [
    {"value": "A", "label": "选项 A"},
    {"value": "B", "label": "选项 B"}
  ],
  "mode": "multiple"
}
```

#### Table 组件测试
```json
{
  "tag": "table",
  "rowData": "${tableData}",
  "columnDefs": [
    {"field": "name", "headerName": "姓名"},
    {"field": "age", "headerName": "年龄"}
  ],
  "pagination": {"pageSize": 10}
}
```

#### ListView 组件测试
```json
{
  "tag": "listview",
  "keyField": "id",
  "itemData": "${listData}",
  "itemAttr": {
    "tag": "div",
    "children": "${row.name}"
  }
}
```

### 错误处理测试

#### 测试消息提示
```json
{
  "tag": "button",
  "children": "显示消息",
  "action": [
    {"tag": "message", "type": "success", "content": "操作成功"}
  ]
}
```

#### 测试确认对话框
```json
{
  "tag": "button",
  "danger": true,
  "children": "删除",
  "action": [
    {
      "tag": "confirm",
      "title": "确认删除",
      "content": "确定要删除吗？",
      "onOk": [{"tag": "message", "type": "success", "content": "已删除"}]
    }
  ]
}
```

### 性能测试建议

1. **数据量测试**：使用 100+ 条数据测试列表性能
2. **分页测试**：验证分页切换是否正常
3. **虚拟滚动**：大量数据时验证滚动性能
4. **并发操作**：测试快速点击/输入时的响应

### 测试用例目录结构

```
demo/data/test/
├── hello-world.json              # 入门示例
├── button-demo.json              # 按钮
├── input-demo.json               # 输入框
├── select-demo.json              # 选择器
├── table-demo.json               # 表格
├── listview-demo.json            # 列表
├── tabs-demo.json                # 标签页
├── card-demo.json                # 卡片
├── form-validation-demo.json     # 表单验证
├── actions-demo.json             # Actions
└── ...                           # 更多测试
```

### 持续集成测试

```yaml
# .github/workflows/test-validation.yml
name: Test Case Validation
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - name: Install jsonlint
        run: npm install -g jsonlint
      - name: Validate all test files
        run: |
          for f in demo/data/test/*.json; do
            echo "Validating $f..."
            jsonlint "$f" || { echo "Error in $f"; exit 1; }
          done
      - name: Check dev.log for errors
        run: |
          if grep -q "Failed to parse" dev.log 2>/dev/null; then
            echo "JSON parse errors found in dev.log"
            grep "Failed to parse" dev.log | head -5
            exit 1
          fi
          echo "No JSON parse errors in dev.log"
```

---

## 🐛 调试经验总结

### 案例1：DatePicker 组件调试

#### 问题症状
- 日期选择后输入框立即清空
- 但 store 中值已正确保存
- 独立使用和表单中使用表现不一致

#### 调试过程

**步骤1：添加组件日志**
```typescript
// 在组件入口添加
console.log('[DatePicker] props.value:', props.value)
console.log('[DatePicker] props.valueType:', typeof props.value)

// 在解析函数添加
function parseToDayjs(dateInput: any, format: string | undefined) {
  console.log('[DatePicker] parseToDayjs input:', dateInput, 'type:', typeof dateInput)
  // ...
}
```

**步骤2：发现根本原因**
```
[DatePicker] props.value: ${dateValue}      ← 模板变量未被解析
[DatePicker] After transferProp, newProps.value: undefined  ← transferProp 返回 undefined
```

**步骤3：定位问题代码**
```typescript
// 问题代码：value 被解构，没有传给 transferProp
const { value, valueFormat, action, ...rest } = props
let newProps = transferProp(rest, "date")  // value 不在 rest 中！
```

**步骤4：修复方案**
```typescript
// 修复：手动解析 value 模板变量
const { value, valueFormat, action, store, namespace, ...rest } = props
const _target = genTarget(props)

let parsedValue = value
if (typeof value === 'string' && value.includes('${')) {
  parsedValue = varValue(value, store, _target)
}
```

#### 教训总结

1. **组件解构要谨慎**
   - 从 props 解构的属性不会传给 transferProp
   - 如果属性包含模板变量，需要先手动解析

2. **日志是最好的朋友**
   - 从组件入口开始，逐步追踪值的变化
   - 关注 props.value 的类型变化

3. **关注组件渲染时序**
   - store 更新后组件重新渲染
   - 新渲染时 props.value 应该已被解析

---

### 案例2：DateRangePicker 只能选一个日期

#### 问题症状
- 日期范围选择器只能选择开始日期
- 选择第二个日期后弹窗关闭

#### 调试过程

**步骤1：检查 range 属性**
```json
{
  "tag": "date",
  "range": true  // ✓ 属性已设置
}
```

**步骤2：检查组件实现**
```typescript
// 问题代码：始终使用 DatePicker
return (
  <DatePicker
    {...newProps}
    value={dayjsValue}
  />
)
```

**步骤3：修复方案**
```typescript
// 根据 range 属性选择组件
const Component = range ? DatePicker.RangePicker : DatePicker

return (
  <Component
    locale={zhCN}
    {...newProps}
    value={dayjsValue}
  />
)
```

#### 教训总结

1. **Ant Design 组件差异**
   - DatePicker 单日期选择
   - RangePicker 范围选择
   - 需要根据 mode/range 属性选择正确的组件

2. **数据格式差异**
   - 单日期：dateString 是字符串
   - 范围选择：dateString 是数组 `["2026-01-01", "2026-01-15"]`

---

### 案例3：Form 组件高度异常

#### 问题症状
- form 组件占用满屏高度
- inline 布局显示不紧凑

#### 调试过程

**步骤1：检查 DOM 结构**
```tsx
// 问题代码
<div onKeyDown={handleKeyDown} className="h100">
  <Form {...rest}>
    {props.children}
  </Form>
</div>
```

**步骤2：修复方案**
```tsx
// 移除 h100 class
<div onKeyDown={handleKeyDown}>
  <Form {...rest}>
    {props.children}
  </Form>
</div>
```

#### 教训总结

1. **CSS 类名影响布局**
   - `h100` 设置 height: 100%
   - 导致组件撑满父容器

2. **Form 组件使用建议**
   - 简单场景使用 `layout: "inline"`
   - 避免不必要的 wrapper div

---

## 🔧 调试工具箱

### 常用调试命令

```bash
# 1. 查看 dev.log 错误
tail -100 /data/react/collect-ui/dev.log | grep "Failed to parse"

# 2. 验证 JSON 格式
npx jsonlint demo/data/test/xxx.json

# 3. 批量验证所有测试文件
cd demo/data/test
for f in *.json; do npx jsonlint "$f"; done

# 4. 查找特定错误
grep -r "Objects are not valid as a React child" .
grep -r "Invalid Date" .
```

### 调试日志模板

```typescript
// 组件入口日志
console.log('[ComponentName] ============ Render ============')
console.log('[ComponentName] props:', props)

// 解析函数日志
function parseValue(input: any) {
  console.log('[ComponentName] parseValue input:', input, 'type:', typeof input)
  // ... 处理逻辑
  console.log('[ComponentName] parseValue result:', result)
  return result
}

// 事件处理日志
const onChange = useCallback((value: any) => {
  console.log('[ComponentName] onChange:', value)
  // ... 处理逻辑
}, [])
```

### 常见问题快速定位

| 症状 | 可能原因 | 排查方向 |
|------|----------|----------|
| 模板变量显示为 `${...}` | 变量未被解析 | 检查 transferProp 调用 |
| 组件值立即清空 | props 未正确传递 | 检查 props 解构 |
| 组件不显示 | JSON 格式错误 | 运行 jsonlint |
| React 渲染错误 | children 类型错误 | 检查 children 是数组 |
| Invalid Date | 日期格式问题 | 检查 valueFormat |

---

## 📚 参考资料

### 关键文件
- `src/components/date/date.tsx` - DatePicker 组件实现
- `src/utils/transferProp.tsx` - 属性传递与变量解析
- `src/utils/varValue.tsx` - 模板变量解析
- `src/components/form/form.tsx` - Form 组件实现

### 调试技巧
1. 从组件入口开始，逐步追踪
2. 关注 props.value 的变化
3. 注意组件解构对 props 的影响
4. 使用 console.log 添加关键节点日志
5. 对比正常和异常场景的差异

---

### 案例4：Checkbox Group 和 Radio Group 不显示

#### 问题症状
- Checkbox Group 和 Radio Group 组件不显示
- 无报错但页面空白

#### 调试过程

**步骤1：检查控制台**
- 无 React 错误
- 无组件渲染日志

**步骤2：检查组件文件**
```
src/components/checkbox/checkbox.tsx  ← 存在
src/components/radio/radio.tsx        ← 存在
```

**步骤3：检查标签名称**
```json
// ❌ 错误：使用了不存在的标签
{"tag": "checkbox-group", ...}
{"tag": "radio-group", ...}
```

**步骤4：修复方案**
```json
// ✅ 正确：使用组件名 + group 属性
{"tag": "checkbox", "group": true, ...}
{"tag": "radio", "group": true, ...}
```

#### 教训总结

1. **组件标签规则**
   - 标签对应 `src/components/[组件名]/[组件名].tsx`
   - `checkbox-group` 没有对应的组件文件
   - 应该使用 `checkbox` 并设置 `group: true`

2. **组件属性规则**
   - Checkbox.Group = `checkbox` + `group: true`
   - Radio.Group = `radio` + `group: true`

3. **常见组件映射**
   | 错误标签 | 正确标签 | 正确属性 |
   |----------|----------|----------|
   | `checkbox-group` | `checkbox` | `group: true` |
   | `radio-group` | `radio` | `group: true` |
   | `date-picker` | `date` | - |
   | `input-number` | `input` | `type: "number"` |

---

### 案例5：Radio Group 和 Checkbox Group 只显示一个选项且无 label

#### 问题症状
- Radio Group 只显示一个选项
- Checkbox Group 只显示一个选项
- label 标签不显示

#### 调试过程

**步骤1：检查 JSON 配置**
```json
{
  "tag": "radio",
  "group": true,
  "options": [
    {"label": "男", "value": "male"},
    {"label": "女", "value": "female"}
  ]
}
```

**步骤2：检查组件实现**
```typescript
// 问题代码：直接传递 options 给 Group
if(isGroup){
  return (
    <Radio.Group {...newProps}>
      {/* options 没有被渲染！ */}
    </Radio.Group>
  )
}
```

**步骤3：修复方案**
```typescript
// 正确：遍历 options 渲染 Radio 组件
if(isGroup){
  return (
    <Radio.Group {...newProps}>
      {options && options.map((opt: any, index: number) => (
        <Radio key={index} value={opt.value}>{opt.label}</Radio>
      ))}
    </Radio.Group>
  )
}
```

#### 教训总结

1. **Ant Design Group 组件**
   - Radio.Group 和 Checkbox.Group 需要显式渲染子组件
   - 不能只传递 `options` 属性，需要遍历渲染

2. **正确写法**
   ```json
   // Radio Group 正确写法
   {
     "tag": "radio",
     "group": true,
     "options": [
       {"label": "男", "value": "male"},
       {"label": "女", "value": "female"}
     ]
   }
   ```

3. **组件内部实现**
   - 需要遍历 `options` 数组
   - 为每个 option 创建 Radio/Checkbox 组件
   - 设置 `value` 和 `children`(label)
