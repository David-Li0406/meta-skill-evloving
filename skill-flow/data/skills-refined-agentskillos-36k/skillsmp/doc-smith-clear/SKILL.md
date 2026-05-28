---
name: doc-smith-clear
description: Clear Doc-Smith site authorization and deployment configuration. Use this skill when the user requests to clear authorization, reset configuration, or remove deployment settings.
---

# Doc-Smith 清除配置

清除 Doc-Smith 的站点授权和部署配置。

## 触发场景

- 用户要求清除授权 token
- 用户要求清除部署配置
- 用户说"清除配置"、"重置"、"清除授权"

## 存储说明

**授权信息 (authTokens)**：
- 存储在系统 keyring（如 macOS Keychain）中
- 服务名：`aigne-doc-smith-publish`
- 按站点 hostname 组织，支持多站点授权
- 如果系统不支持 keyring，回退到 `~/.aigne/doc-smith-connected.yaml`

**部署配置 (deploymentConfig)**：
- `appUrl` 字段存储在 workspace 的 `.aigne/doc-smith/config.yaml` 中

## 可清除的内容

| 目标 | 说明 |
|------|------|
| authTokens | 站点授权信息（存储在系统 keyring 中） |
| deploymentConfig | 部署配置（config.yaml 中的 appUrl 字段） |

## 工作流程

### 1. 确认清除内容

根据用户输入确定要清除的内容：

**情况一：用户明确指定了清除目标**

例如用户说：
- "清除授权" → 清除 authTokens
- "清除部署配置" → 清除 deploymentConfig
- "清除所有配置" → 清除全部

直接执行清除操作。

**情况二：用户未明确指定**

使用 AskUserQuestion 工具询问用户：

```
请选择要清除的内容：

选项：
1. 站点授权 (authTokens) - 清除后需要重新授权才能发布
2. 部署配置 (deploymentConfig) - 清除后需要重新指定发布目标
3. 全部清除
```

### 2. 清除站点授权

如果用户选择清除授权：

**Step 1: 获取已授权站点列表**

```bash
node skills/doc-smith-clear/scripts/list-auth.mjs
```

输出格式：
```json
{"sites": ["site1.arcblock.io", "site2.arcblock.io"]}
```

如果没有授权信息，返回 `{"sites": []}`。

**Step 2: 确认要清除的站点**

如果有多个站点，使用 AskUserQuestion 询问用户要清除哪些：

```
发现以下已授权的站点：
- site1.arcblock.io
- site2.arcblock.io

请选择要清除授权的站点：

选项：
1. site1.arcblock.io
2. site2.arcblock.io
3. 清除全部站点授权
```

如果只有一个站点，直接询问是否清除该站点的授权。

**Step 3: 执行清除**

```bash
# 清除指定站点
node skills/doc-smith-clear/scripts/clear-auth.mjs --site=site1.arcblock.io

# 清除全部站点
node skills/doc-smith-clear/scripts/clear-auth.mjs --all
```

### 3. 清除部署配置

如果用户选择清除部署配置：

**Step 1: 检查配置文件是否存在**

```bash
ls .aigne/doc-smith/config.yaml
```

如果不存在，提示用户："当前目录没有 Doc-Smith 部署配置，无需清除。"

**Step 2: 执行清除**

```bash
node skills/doc-smith-clear/scripts/clear-deployment-config.mjs
```

### 4. 返回结果

显示清除结果：
- 已清除的站点授权列表（如果清除了授权）
- 是否清除了部署配置
- 后续提示（如"需要重新授权才能发布"）

## 脚本说明

### list-auth.mjs

列出所有已授权的站点 hostname。

**输出**：JSON 格式，包含 sites 数组

### clear-auth.mjs

清除站点授权信息。

**参数**：
- `--site=<hostname>`: 清除指定站点的授权
- `--all`: 清除所有站点的授权

**输出**：JSON 格式，包含清除结果

### clear-deployment-config.mjs

清除 config.yaml 中的 appUrl 字段。

**输出**：JSON 格式，包含清除结果

## 错误处理

- **配置文件不存在**：返回提示信息，不视为错误
- **无授权信息可清除**：返回提示信息，不视为错误
- **无效的站点名称**：提示用户正确的站点名称

## 注意事项

- 清除操作不可恢复，执行前确保用户已确认
- 清除站点授权后需要重新授权才能发布到该站点
- 清除部署配置后下次发布需要重新指定目标 URL
- 站点授权是全局的（存储在用户目录），不依赖于当前 workspace
