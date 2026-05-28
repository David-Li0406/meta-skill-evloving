# Workspace 初始化流程

**用途**: 本文档定义 DocSmith workspace 的验证和数据源管理流程

---

## 一、目录结构

用户在项目根目录执行 `/doc-smith`，workspace 创建在 `.aigne/doc-smith/` 目录：

```
my-project/                        # 用户的项目目录（cwd）
├── .aigne/
│   └── doc-smith/                 # DocSmith workspace
│       ├── config.yaml            # 配置文件
│       ├── intent/                # 意图文件
│       │   └── user-intent.md
│       ├── planning/              # 规划文件
│       │   └── document-structure.yaml
│       ├── docs/                  # 生成的文档
│       ├── assets/                # 生成的图片资源
│       └── cache/                 # 缓存数据
│           └── task_plan.md
├── src/                           # 项目源代码（数据源）
├── README.md
└── ...
```

**数据源**：项目本身

---

## 二、Workspace 检测流程

### 步骤 1: 检查 workspace 是否已存在

```bash
ls .aigne/doc-smith/config.yaml
```

### 步骤 2: 根据检测结果处理

| 检测结果 | 处理方式 |
|---------|---------|
| config.yaml 存在 | 直接使用，验证配置完整性 |
| config.yaml 不存在 | 初始化 workspace |

---

## 三、初始化 Workspace

当 `.aigne/doc-smith/config.yaml` 不存在时执行：

### 步骤 1: 创建目录结构

```bash
mkdir -p .aigne/doc-smith/{intent,planning,docs,assets,cache}
```

### 步骤 2: 在 workspace 中初始化 git

```bash
cd .aigne/doc-smith
git init
```

### 步骤 3: 创建 .gitignore

在 `.aigne/doc-smith/.gitignore` 中写入：

```
# Ignore temporary files
.tmp/
.temp/
temp/
```

### 步骤 4: 获取项目 git 信息

```bash
# 回到项目根目录
cd ../..

# 获取远程 URL
git remote get-url origin

# 获取当前分支
git branch --show-current

# 获取当前 commit
git rev-parse --short HEAD
```

### 步骤 5: 创建 config.yaml

在 `.aigne/doc-smith/config.yaml` 中写入：

```yaml
# Workspace metadata
workspaceVersion: "1.0"
createdAt: "<current-timestamp>"  # ISO 8601 格式

# Project information (待分析后填充)
projectName: ""
projectDesc: ""
locale: ""

# Documentation settings
projectLogo: ""
translateLanguages: []

# 数据源配置
sources:
  - type: local-path
    path: "../../"
    url: "<git-remote-url>"      # 如果有
    branch: "<current-branch>"
    commit: "<current-commit>"
```

### 步骤 6: 创建初始提交

```bash
cd .aigne/doc-smith
git add .
git commit -m "Initial commit: doc-smith workspace"
```

---

## 四、Config.yaml Schema

```yaml
# Workspace metadata
workspaceVersion: "1.0"        # 固定版本号
createdAt: "2025-01-13T10:00:00Z"

# Project information
projectName: "my-project"      # 项目名称
projectDesc: "项目描述"         # 项目描述
locale: "zh"                   # 输出语言代码

# Documentation settings
projectLogo: ""                # 项目 Logo 路径
translateLanguages: []         # 翻译目标语言列表

# 数据源配置
sources:
  - type: local-path
    path: "../../"             # 相对于 workspace 的路径
    url: "https://..."         # 可选，git 远程 URL
    branch: "main"             # 可选，当前分支
    commit: "a1b2c3d"          # 可选，当前 commit
```

---

## 五、收集必要信息

在 workspace 初始化或检测后，检查并收集以下信息：

### 5.1 输出语言 (locale)

**检查条件**：config.yaml 中 `locale` 为空

**处理逻辑**：
- 如果用户在请求中已指定语言（如"生成中文文档"）→ 直接使用
- 否则询问用户选择

**询问用户**：
```
请选择文档输出语言:
1. 简体中文 (zh)
2. English (en)
3. 繁體中文 (zh-TW)
4. 日本語 (ja)
5. 其他 (请输入语言代码)
```

### 5.2 项目信息

**检查条件**：`projectName` 或 `projectDesc` 为空

**处理逻辑**：
1. 分析数据源（README、package.json 等）
2. 推断项目名称和描述
3. 使用 `locale` 指定的语言生成描述
4. 保存到 config.yaml

---

## 六、验证 Workspace 完整性

### 6.1 配置完整性检查

读取 config.yaml，验证必要字段：

**必须存在**：
- `workspaceVersion`
- `sources`（至少一个数据源）

**可为空但需收集**：
- `projectName`
- `projectDesc`
- `locale`

---

## 七、路径映射

| 概念 | 实际路径 |
|------|---------|
| workspace 根目录 | `.aigne/doc-smith/` |
| config.yaml | `.aigne/doc-smith/config.yaml` |
| 文档目录 | `.aigne/doc-smith/docs/` |
| 资源目录 | `.aigne/doc-smith/assets/` |
| 数据源根目录 | `./`（项目根目录） |
| 数据源中的文件 | 相对于项目根目录的路径 |

---

## 八、错误处理

### 错误 1: config.yaml 格式错误

```
错误: config.yaml 格式不正确

请检查 YAML 语法，或删除 .aigne/doc-smith/config.yaml 重新初始化。
```

---

## 九、完整流程示意图

```
用户执行 /doc-smith
  ↓
检查 .aigne/doc-smith/config.yaml
  ├─ 存在 → 验证配置完整性
  └─ 不存在 → 初始化 workspace
  ↓
收集必要信息 (locale, projectName, projectDesc)
  ↓
验证数据源有效性
  ↓
进入文档生成流程
```
