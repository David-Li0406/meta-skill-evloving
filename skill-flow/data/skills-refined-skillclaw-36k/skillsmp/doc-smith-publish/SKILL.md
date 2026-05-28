---
name: doc-smith-publish
description: Publish Doc-Smith generated documentation to online platforms. Use this skill when the user requests to publish, deploy, or release documentation.
---

# Doc-Smith 文档发布

将生成的文档发布到在线平台。

## Usage

```bash
# 发布到上次使用的目标（从 config.yaml 读取 appUrl）
/doc-smith-publish

# 指定发布目标 URL
/doc-smith-publish --url https://example.com/docs
/doc-smith-publish -u https://example.com/docs

# 创建新网站并发布
/doc-smith-publish --new-website
```

## Options

| Option | Alias | Description |
|--------|-------|-------------|
| `--url <url>` | `-u` | 发布目标 URL（默认使用 config.yaml 中的 appUrl） |
| `--new-website` | | 创建新网站并发布（付费服务） |

## 工作流程

### 1. 检测 Workspace

检查当前目录是否为有效的 Doc-Smith workspace（存在 `.aigne/doc-smith/config.yaml` 文件）。

### 2. 检查发布条件

调用 `doc-smith-check` skill 确保文档完整。如果检查失败，提示用户先修复问题后再发布。

### 3. 确定发布方式

如果用户指定了 `--url` 或 `--new-website` 参数，直接使用对应方式。

否则，读取 `config.yaml` 中的 `appUrl` 配置：
- **存在 appUrl**：直接使用该 URL 发布
- **不存在 appUrl**：使用 AskUserQuestion 向用户询问发布方式

**询问用户时提供以下选项**：
1. **DocSmith Cloud** - 免费托管，文档公开访问，适合开源项目
2. **现有网站** - 发布到用户已有的网站（需要用户提供 URL）
3. **新建网站** - 付费服务，创建全新网站

根据用户选择：
- 选择 DocSmith Cloud：使用默认 URL `https://docsmith.aigne.io`
- 选择现有网站：追问用户输入网站 URL，然后使用 `--url` 参数
- 选择新建网站：使用 `--new-website` 参数

### 4. 翻译 Meta 信息

读取 `config.yaml` 中的配置：
- `projectName`: 项目名称
- `projectDesc`: 项目描述
- `locale`: 主语言
- `translateLanguages`: 翻译目标语言列表

如果存在多个目标语言，直接翻译项目名称和描述到所有目标语言。

**翻译要求**：
- 描述翻译必须控制在 100 字符以内
- 保持原意的同时确保语言流畅自然
- 将翻译结果保存到 `.aigne/doc-smith/cache/translation-cache.yaml`

**Meta 信息格式**（translation-cache.yaml）：
```yaml
title:
  en: Project Name
  zh: 项目名称
desc:
  en: Project description in English
  zh: 项目中文描述
```

### 5. 执行发布

根据确定的发布方式调用发布脚本：

```bash
# 发布到指定 URL
node skills/doc-smith-publish/scripts/publish-docs.mjs --appUrl https://example.com

# 创建新网站并发布
node skills/doc-smith-publish/scripts/publish-docs.mjs --newWebsite
```

发布脚本会处理以下步骤：
- 读取翻译缓存文件（如不存在会报错提示先翻译）
- 检查并获取站点授权
- 上传文档到目标站点

**注意**：发布脚本内部会处理授权流程，如果没有授权会引导用户完成。

### 6. 返回结果

返回发布结果：
- 发布状态（成功/失败）
- 在线访问 URL

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| 依赖未安装 | 在 scripts 目录执行 `npm install` 安装依赖 |
| 翻译文件不存在 | 先完成步骤 4（翻译 Meta 信息）再执行发布 |
| 授权失败 | 引导用户重新授权 |
| 网络错误 | 提示重试 |
| 文档不完整 | 提示先运行 `/doc-smith-check` 并修复问题 |

### 依赖未安装

如果执行脚本时出现模块找不到的错误（如 `Cannot find module 'xxx'`），需要先安装依赖：

```bash
cd skills/doc-smith-publish/scripts && npm install
```
