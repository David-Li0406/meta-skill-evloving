---
name: api-init
description: "Initialize API documentation config for a backend project. Creates .api-spec.yaml with project metadata and routes file location."
---

# /api-init - 初始化项目 API 文档配置

初始化当前后端项目的 API 文档配置，生成 `.api-spec.yaml` 文件。

## 使用方式

```bash
/api-init
```

## 执行步骤

### Step 1: 检测项目类型

检查项目结构，识别后端框架：

```bash
# Go 项目
if [ -f "go.mod" ]; then
    PROJECT_TYPE="go"
    # 查找路由文件
    ROUTES_FILE=$(find . -name "routes.go" -o -name "router.go" | head -1)
fi

# Node.js 项目
if [ -f "package.json" ]; then
    PROJECT_TYPE="node"
    ROUTES_FILE=$(find . -name "routes.ts" -o -name "routes.js" -o -name "router.ts" | head -1)
fi

# Python 项目
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    PROJECT_TYPE="python"
    ROUTES_FILE=$(find . -name "urls.py" -o -name "routes.py" | head -1)
fi
```

### Step 2: 收集项目信息

询问用户以下信息（如果无法自动检测）：

1. **项目名称** - 用于在 API 规范仓库中创建目录
2. **Base URL** - 生产环境的 API 地址
3. **路由文件位置** - 如果自动检测不准确

### Step 3: 生成配置文件

在项目根目录创建 `.api-spec.yaml`：

```yaml
# API 规范配置
project_name: {project_name}
description: {description}
base_url: {base_url}

# API 规范仓库位置
spec_repo: ~/.inspirai/apilookup

# 路由文件位置（用于解析 API）
routes_file: {routes_file}

# 项目类型
project_type: {go|node|python}
```

### Step 4: 确认配置

显示生成的配置文件内容，询问用户确认。

## 输出

- 在项目根目录创建 `.api-spec.yaml` 文件
- 将 `.api-spec.yaml` 添加到 `.gitignore`（可选）

## 注意事项

- 如果 `.api-spec.yaml` 已存在，询问是否覆盖
- spec_repo 默认为 `~/.inspirai/apilookup`
- 需确保 inspirai-api-specs 仓库已 clone 到该目录
