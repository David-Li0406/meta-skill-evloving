---
name: api-update
description: "Parse routes and handlers from the current project, generate/update API documentation to the spec repository."
---

# /api-update - 更新 API 文档

解析当前项目的路由和 handler，生成/更新 API 文档到规范仓库。

## 使用方式

```bash
/api-update              # 更新所有 API
/api-update auth         # 只更新 auth 模块
```

## 前置条件

- 项目已执行 `/api-init`，存在 `.api-spec.yaml` 配置文件
- `inspirai-api-specs` 仓库已 clone 到本地

## 执行步骤

### Step 1: 读取配置

```bash
# 读取 .api-spec.yaml
if [ ! -f ".api-spec.yaml" ]; then
    echo "错误：未找到 .api-spec.yaml，请先执行 /api-init"
    exit 1
fi
```

### Step 2: 解析路由文件

根据项目类型解析路由：

**Go 项目：**
- 解析 `routes.go` 中的 `mux.HandleFunc` 和 `mux.Handle` 调用
- 提取 HTTP 方法、路径、handler 函数名
- 读取对应的 handler 文件，提取请求/响应结构体

**Node.js 项目：**
- 解析 `router.get/post/put/delete` 调用
- 提取路由和 handler

**Python 项目：**
- 解析 `urlpatterns` 或 Flask/FastAPI 路由装饰器

### Step 3: 生成 API 文档

为每个 API 生成 YAML 文件：

```
{spec_repo}/{project_name}/
├── meta.yaml           # 项目索引
├── auth/
│   ├── sms-send.yaml
│   └── sms-login.yaml
├── user/
│   └── get-profile.yaml
└── ...
```

**meta.yaml 格式：**
```yaml
project: {project_name}
description: {description}
base_url: {base_url}
updated_at: {timestamp}
apis:
  - path: auth/sms-send
    method: POST
    endpoint: /api/v1/auth/sms/send
    auth: false
    summary: 发送短信验证码
  ...
```

**单个 API 文件格式：**
```yaml
endpoint: /api/v1/auth/sms/login
method: POST
summary: 短信验证码登录
auth: false
description: 使用手机号和短信验证码登录

request:
  content_type: application/json
  fields:
    - name: phone
      type: string
      required: true
      description: 手机号
    ...

response:
  success:
    status: 200
    fields:
      - name: token
        type: string
        description: JWT token
      ...
  errors:
    - status: 400
      error: invalid_code
      description: 验证码错误
```

### Step 4: 更新全局索引

更新 `{spec_repo}/meta.yaml`：

```yaml
projects:
  {project_name}:
    description: {description}
    base_url: {base_url}
    api_count: {count}
    updated_at: {timestamp}
```

### Step 5: 提交并推送

```bash
cd {spec_repo}
git add -A
git commit -m "docs: 更新 {project_name} API 文档"
git push origin main
```

## 输出

- 更新 `inspirai-api-specs/{project_name}/` 目录下的所有 API 文档
- 自动 commit 并 push 到远程仓库
- 显示更新摘要（新增/修改/删除的 API 数量）
