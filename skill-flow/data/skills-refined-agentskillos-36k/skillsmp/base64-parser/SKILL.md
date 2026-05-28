---
name: base64-parser
description: Base64 编解码工具，支持编码/解码文本、JSON、二进制文件，自动检测格式，支持批量处理
allowed-tools:
  - Read
  - Write
  - Bash
version: 2.0.0
user-invocable: true
---

# Base64 编解码技能

## 功能

| 操作 | 说明 |
|------|------|
| **decode** | 解码 Base64 字符串为文本/JSON/二进制 |
| **encode** | 将文本/文件编码为 Base64 |
| **detect** | 自动检测 Base64 内容类型（JSON/文本/图片/PDF等） |
| **batch** | 批量解码多个 Base64 字符串 |

## 使用方法

**重要**：始终使用 `-p` 参数获得人类友好的输出格式！

### 1. 解码 Base64

```bash
# 解码并显示完整内容（推荐）
python3 .blade/skills/base64-parser/scripts/base64_tool.py -p decode "SGVsbG8gV29ybGQ="

# 解码并保存到文件
python3 .blade/skills/base64-parser/scripts/base64_tool.py -p decode "..." --output result.txt

# 解码二进制（如图片）并保存
python3 .blade/skills/base64-parser/scripts/base64_tool.py -p decode "iVBORw0KGgo..." --output image.png --binary
```

### 2. 编码为 Base64

```bash
# 编码文本
python3 .blade/skills/base64-parser/scripts/base64_tool.py -p encode "Hello World"

# 编码文件
python3 .blade/skills/base64-parser/scripts/base64_tool.py -p encode --file image.png

# URL 安全编码
python3 .blade/skills/base64-parser/scripts/base64_tool.py -p encode "Hello World" --url-safe
```

### 3. 检测类型

```bash
# 自动检测 Base64 内容类型并显示内容
python3 .blade/skills/base64-parser/scripts/base64_tool.py -p detect "eyJ0ZXN0IjogMX0="
```

### 4. 批量处理

```bash
# 从文件批量解码（每行一个 Base64）
python3 .blade/skills/base64-parser/scripts/base64_tool.py -p batch --file input.txt --output-dir ./decoded/
```

## 输出格式说明

- **`-p` (pretty)**: 人类友好格式，带 emoji 图标，显示完整解码内容
- **不加 `-p`**: JSON 格式，适合程序处理

示例输出（使用 `-p`）：

```
✅ Successfully decoded as JSON

📊 类型: json (application/json)
📏 大小: 35 bytes

📄 解码内容:
--------------------------------------------------
{
  "name": "Blade",
  "version": "2.0"
}
--------------------------------------------------
```

## 支持格式

| 格式 | 自动检测 | 说明 |
|------|---------|------|
| JSON | ✅ | 自动解析并格式化输出 |
| 纯文本 | ✅ | UTF-8 文本 |
| PNG/JPEG/GIF | ✅ | 通过 magic bytes 检测 |
| PDF | ✅ | 通过 %PDF 头检测 |
| 其他二进制 | ✅ | 显示十六进制预览 |

## 常见场景

1. **解析 JWT Token**：JWT 的 payload 是 Base64 编码的 JSON
2. **查看 API 响应**：某些 API 返回 Base64 编码的数据
3. **处理配置文件**：Kubernetes Secrets 等使用 Base64
4. **图片 Data URI**：`data:image/png;base64,...` 格式
5. **调试加密数据**：查看加密前的原始内容
