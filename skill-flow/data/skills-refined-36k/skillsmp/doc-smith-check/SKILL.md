---
name: doc-smith-check
description: Validate the structure and content integrity of Doc-Smith documentation. Use this skill to verify document structure YAML, check document content, and validate links and image paths. Can also be invoked by other doc-smith skills for validation.
---

# Doc-Smith 文档检查

检查 Doc-Smith 文档的结构和内容完整性。

## Usage

```bash
# 运行所有检查（结构 + 内容）
/doc-smith-check

# 只检查结构（document-structure.yaml）
/doc-smith-check --structure
/doc-smith-check -s

# 只检查内容（文档文件、链接、图片）
/doc-smith-check --content
/doc-smith-check -c

# 只检查指定文档的内容
/doc-smith-check --content --path /api/overview
/doc-smith-check -c -p /api/overview

# 检查多个指定文档
/doc-smith-check --content --path /api/overview --path /guides/start

# 检查内容并验证 AFS image slot 已替换
/doc-smith-check --content --check-slots
/doc-smith-check -c --check-slots
```

## Options

| Option | Alias | Description |
|--------|-------|-------------|
| `--structure` | `-s` | 只运行结构检查 |
| `--content` | `-c` | 只运行内容检查 |
| `--path <docPath>` | `-p` | 指定要检查的文档路径（可多次使用，仅与 `--content` 配合） |
| `--check-slots` | - | 检查 AFS image slot 已替换（仅与 `--content` 配合） |

## 检查项目

### 结构检查 (--structure)

校验 `planning/document-structure.yaml` 文件：

| 检查项 | 说明 |
|--------|------|
| YAML 格式 | 语法是否正确 |
| 必需字段 | title, path, description 是否存在 |
| path 格式 | 是否以 `/` 开头 |
| sourcePaths | 格式是否正确 |

**执行脚本：**
```bash
node skills/doc-smith-check/scripts/check-structure.mjs
```

### 内容检查 (--content)

检查已生成文档的完整性：

| 检查项 | 说明 |
|--------|------|
| 文档文件 | 是否存在 |
| .meta.yaml | 元数据文件是否存在 |
| 内部链接 | 是否有效 |
| 图片路径 | 是否正确 |
| AFS image slot | 格式是否正确 |

**执行脚本：**
```bash
# 检查所有文档
node skills/doc-smith-check/scripts/check-content.mjs

# 只检查指定文档
node skills/doc-smith-check/scripts/check-content.mjs --path /overview
node skills/doc-smith-check/scripts/check-content.mjs -p /api/auth -p /guides/start
```

### AFS Image Slot 检查 (--check-slots)

当启用 `--check-slots` 时，执行以下额外检查：

| 检查项 | 说明 |
|--------|------|
| slot 已替换 | 文档中不应存在 `<!-- afs:image ... -->` 占位符（排除代码块中的示例） |
| 路径正确 | 图片引用路径相对于文档位置的层级正确（需考虑语言文件层级） |
| 文件存在 | 对应的图片文件确实存在于 assets 目录 |

**执行脚本：**
```bash
# 检查所有文档的 slot 是否已替换
node skills/doc-smith-check/scripts/check-content.mjs --check-slots

# 检查指定文档的 slot
node skills/doc-smith-check/scripts/check-content.mjs --path /overview --check-slots
```

**错误报告示例：**
```
❌ FAIL: 文档内容存在错误

统计信息:
  总文档数: 5
  已检查: 5
  未替换的 slot: 2
  路径层级错误: 1
  缺失的图片: 1

致命错误（必须修复）:

1. AFS image slot 未替换: architecture-overview
   文档: /overview
   语言文件: zh.md
   Slot ID: architecture-overview
   操作: 请使用 generate-slot-image 生成图片

2. 图片路径层级错误: ../assets/setup/images/zh.png
   文档: /guides/start
   语言文件: zh.md
   图片: ../assets/setup/images/zh.png
   期望路径: ../../../assets/setup/images/zh.png
   操作: 修正相对路径层级
```

## 返回结果

```json
{
  "valid": true,
  "structure": { "valid": true, "errors": [] },
  "content": { "valid": true, "errors": [] }
}
```

失败时返回错误列表和修复建议：

```json
{
  "valid": false,
  "structure": {
    "valid": false,
    "errors": [
      { "type": "missing_field", "path": "/docs/intro", "field": "description", "suggestion": "添加 description 字段" }
    ]
  }
}
```

## 错误处理

### 依赖未安装

如果执行脚本时出现模块找不到的错误（如 `Cannot find module 'yaml'`），需要先安装依赖：

```bash
cd skills/doc-smith-check/scripts && npm install
```

### 结构检查失败

1. 分析错误报告，理解问题所在
2. 根据修复建议修正 `document-structure.yaml`
3. 重新执行结构检查
4. 如果连续 3 次失败，向用户报告

### 内容检查失败

1. 分析问题列表
2. 根据问题类型采取行动：
   - 文档缺失：生成缺失的文档
   - 链接错误：修正链接路径
   - 图片问题：提供图片或修正路径
3. 重新执行内容检查

## 被其他 Skill 调用

在 doc-smith 主流程中：
- 生成 document-structure.yaml 后：`/doc-smith-check --structure`
- 生成文档内容后：`/doc-smith-check --content`
- 图片生成后校验 slot 已替换：`/doc-smith-check --content --check-slots`
- 结束前进行最终校验：`/doc-smith-check`
