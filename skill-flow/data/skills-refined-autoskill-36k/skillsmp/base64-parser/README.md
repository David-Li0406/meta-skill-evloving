# Base64 编解码技能

一个功能完整的 Base64 编解码工具，支持文本、JSON、二进制文件的处理。

## 功能特性

- **双向转换**：支持编码和解码
- **格式自动检测**：自动识别 JSON、文本、图片、PDF 等格式
- **二进制支持**：处理图片、PDF 等二进制文件
- **URL 安全**：支持 URL 安全的 Base64 格式
- **批量处理**：一次处理多个 Base64 字符串

## 快速开始

```bash
# 解码
python3 scripts/base64_tool.py decode "SGVsbG8gV29ybGQ="
# 输出: {"success": true, "type": "text", "content": "Hello World", ...}

# 编码
python3 scripts/base64_tool.py encode "Hello World"
# 输出: {"success": true, "encoded": "SGVsbG8gV29ybGQ=", ...}

# 检测类型
python3 scripts/base64_tool.py detect "eyJ0ZXN0IjogMX0="
# 输出: {"type": "json", "content": {"test": 1}, ...}
```

## 命令详解

### decode - 解码

```bash
# 基本解码
python3 scripts/base64_tool.py decode "SGVsbG8="

# 从文件读取
python3 scripts/base64_tool.py decode --file encoded.txt

# 保存到文件
python3 scripts/base64_tool.py decode "iVBORw0KGgo..." --output image.png

# 强制二进制模式
python3 scripts/base64_tool.py decode "..." --binary
```

### encode - 编码

```bash
# 编码文本
python3 scripts/base64_tool.py encode "Hello World"

# 编码文件
python3 scripts/base64_tool.py encode --file document.pdf

# URL 安全编码
python3 scripts/base64_tool.py encode "Hello+World" --url-safe
```

### detect - 类型检测

```bash
# 检测内容类型
python3 scripts/base64_tool.py detect "eyJ0ZXN0IjogMX0="
```

支持检测的类型：
- `json` - JSON 数据
- `text` - 纯文本
- `image/png`, `image/jpeg`, `image/gif` - 图片
- `application/pdf` - PDF 文档
- `application/zip` - ZIP 压缩包
- `application/gzip` - Gzip 压缩
- `binary` - 其他二进制

### batch - 批量处理

```bash
# 批量解码（每行一个 Base64）
python3 scripts/base64_tool.py batch --file list.txt

# 批量解码并保存到目录
python3 scripts/base64_tool.py batch --file list.txt --output-dir ./decoded/
```

## 输出格式

所有命令输出 JSON 格式：

```json
{
  "success": true,
  "operation": "decode",
  "type": "json",
  "mime_type": "application/json",
  "content": {"key": "value"},
  "raw_size": 16,
  "message": "Successfully decoded as JSON"
}
```

## 使用场景

| 场景 | 命令 |
|------|------|
| 解析 JWT Token | `decode <jwt_payload>` |
| 查看 K8s Secret | `decode <secret_data>` |
| 编码配置文件 | `encode --file config.json` |
| 提取 Data URI 图片 | `decode <base64_part> --output image.png` |
| 批量处理日志 | `batch --file logs.txt` |

## 技术实现

- 使用 Python 3 标准库 `base64` 模块
- 通过 magic bytes 检测二进制文件类型
- 自动处理 URL 安全格式（`-_` 转换为 `+/`）
- 自动补齐 Base64 padding

## 文件结构

```
base64-parser/
├── SKILL.md              # 技能定义
├── README.md             # 本文档
└── scripts/
    └── base64_tool.py    # 主程序
```
