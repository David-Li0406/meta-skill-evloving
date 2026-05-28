# /ohspec:init - 初始化权限配置

## 命令说明

首次使用 OHSpec 前运行此命令，配置权限以减少运行时确认提示。

## 使用方式

```bash
/ohspec:init
```

## 执行流程

### Step 1: 检查现有配置

```python
import os
import json

project_root = os.getcwd()
settings_path = f"{project_root}/.claude/settings.json"

if os.path.exists(settings_path):
    with open(settings_path, 'r') as f:
        existing = json.load(f)
    print(f"✅ 已存在配置文件: {settings_path}")
    print(f"   当前权限: {existing.get('permissions', {})}")

    # 询问是否覆盖
    # AskUserQuestion: 是否更新为 OHSpec 推荐配置？
else:
    print(f"⚠️ 配置文件不存在: {settings_path}")
    print("   将创建新配置文件")
```

### Step 2: 生成推荐配置

```python
ohspec_permissions = {
    "permissions": {
        "allow": [
            # 文件读取（代码扫描必需）
            "Read(*)",

            # 文件写入（RFC、findings、progress）
            "Write(*.md)",
            "Write(*.json)",
            "Edit(*.md)",
            "Edit(*.json)",

            # 文件搜索（代码扫描必需）
            "Glob(*)",
            "Grep(*)",
            "Bash(rg:*)",
            "Bash(ag:*)",
            "Bash(python3:*)",
            "Bash(python:*)",
            "Bash(py:*)",

            # 目录操作
            "Bash(mkdir:*)",
            "Bash(ls:*)",

            # MCP 工具（可选，根据项目配置）
            # "mcp__*"
        ],
        "deny": [
            # 禁止删除文件
            "Bash(rm:*)",
            "Bash(rmdir:*)",

            # 禁止写入临时目录（强制写入项目目录）
            "Write(/tmp/*)",

            # 禁止写入系统目录
            "Write(/etc/*)",
            "Write(/root/*)"
        ]
    },
    "_ohspec": {
        "version": "2.0",
        "initialized_at": "{{TIMESTAMP}}",
        "description": "OHSpec 权限配置，减少运行时确认提示"
    }
}
```

### Step 3: 写入配置文件

```python
import os
from datetime import datetime

# 确保目录存在
os.makedirs(f"{project_root}/.claude", exist_ok=True)

# 替换时间戳
ohspec_permissions["_ohspec"]["initialized_at"] = datetime.now().isoformat()

# 写入文件
with open(settings_path, 'w') as f:
    json.dump(ohspec_permissions, f, indent=2, ensure_ascii=False)

print(f"✅ 配置文件已创建: {settings_path}")
```

### Step 4: 验证配置

```python
# 重新读取验证
with open(settings_path, 'r') as f:
    saved = json.load(f)

allow_count = len(saved.get("permissions", {}).get("allow", []))
deny_count = len(saved.get("permissions", {}).get("deny", []))

print(f"""
✅ OHSpec 初始化完成

配置摘要:
- 允许的操作: {allow_count} 项
- 禁止的操作: {deny_count} 项
- 配置文件: {settings_path}

现在可以使用 OHSpec:
  /ohspec "你的需求描述"

运行时将自动跳过以下确认:
- 读取项目文件
- 写入 RFC/findings/progress
- 文件搜索操作
""")
```

## 输出示例

```
🔧 OHSpec 初始化

检查配置文件...
⚠️ 配置文件不存在: /home/user/project/.claude/settings.json

创建推荐配置...
✅ 配置文件已创建

配置摘要:
- 允许的操作: 8 项
- 禁止的操作: 4 项

现在可以使用 OHSpec:
  /ohspec "Add 3D sound effect toggle to audio service"
```

## 配置项说明

### 允许的操作 (allow)

| 权限 | 说明 | 必要性 |
|------|------|--------|
| `Read(*)` | 读取任何文件 | 必需（代码扫描） |
| `Write(*.md)` | 写入 Markdown 文件 | 必需（RFC 输出） |
| `Write(*.json)` | 写入 JSON 文件 | 必需（findings/progress） |
| `Edit(*.md)` | 编辑 Markdown 文件 | 必需（增量更新） |
| `Edit(*.json)` | 编辑 JSON 文件 | 必需（状态更新） |
| `Glob(*)` | 文件模式匹配 | 必需（查找文件） |
| `Grep(*)` | 内容搜索 | 必需（代码搜索） |
| `Bash(mkdir:*)` | 创建目录 | 推荐（RFC 目录） |

### 禁止的操作 (deny)

| 权限 | 说明 | 原因 |
|------|------|------|
| `Bash(rm:*)` | 删除文件 | 安全保护 |
| `Write(/tmp/*)` | 写入临时目录 | 强制写入项目目录 |
| `Write(/etc/*)` | 写入系统目录 | 安全保护 |

## 高级配置

### 添加 MCP 工具权限

如果项目使用 MCP 工具（如 context7、sequential-thinking），可以添加：

```json
{
  "permissions": {
    "allow": [
      "mcp__context7__*",
      "mcp__sequential-thinking__*"
    ]
  }
}
```

### 项目特定配置

可以在项目根目录创建 `.claude/settings.local.json`，覆盖全局配置：

```json
{
  "permissions": {
    "allow": [
      "Bash(npm:*)",
      "Bash(yarn:*)"
    ]
  }
}
```

## 故障排除

### 问题：仍然出现确认提示

**原因**：操作不在 allow 列表中

**解决**：
1. 查看提示中的操作名称
2. 添加到 `.claude/settings.json` 的 allow 列表
3. 或选择 "Allow always" 自动添加

### 问题：配置文件被覆盖

**原因**：其他工具或手动操作覆盖了配置

**解决**：
1. 重新运行 `/ohspec:init`
2. 或手动恢复配置

### 问题：权限过于宽松

**解决**：根据项目需求调整 allow/deny 列表，遵循最小权限原则。
