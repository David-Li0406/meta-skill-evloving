# Hook 钩子示例

针对常见使用场景的完整、经过测试的钩子配置。

## 日志记录钩子

### 记录所有 Bash 命令

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"\\(.tool_input.command) - \\(.tool_input.description // \"无描述\")\"' >> ~/.claude/bash-command-log.txt"
          }
        ]
      }
    ]
  }
}
```

### 记录所有文件编辑

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"[\\(now | strftime(\"%Y-%m-%d %H:%M:%S\"))] \\(.tool_name): \\(.tool_input.file_path)\"' >> ~/.claude/edit-log.txt"
          }
        ]
      }
    ]
  }
}
```

## 自动格式化钩子

### 格式化 TypeScript 文件

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read file_path; if echo \"$file_path\" | grep -q '\\.tsx\\?$'; then npx prettier --write \"$file_path\" 2>/dev/null; fi; }"
          }
        ]
      }
    ]
  }
}
```

### 使用 Black 格式化 Python 文件

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read f; [[ \"$f\" == *.py ]] && black \"$f\" 2>/dev/null; }"
          }
        ]
      }
    ]
  }
}
```

### 格式化 Go 文件

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read f; [[ \"$f\" == *.go ]] && gofmt -w \"$f\"; }"
          }
        ]
      }
    ]
  }
}
```

## 文件保护钩子

### 阻止编辑敏感文件

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json, sys; data=json.load(sys.stdin); path=data.get('tool_input',{}).get('file_path',''); blocked=['.env', 'package-lock.json', '.git/', 'secrets']; sys.exit(2 if any(p in path for p in blocked) else 0)\""
          }
        ]
      }
    ]
  }
}
```

### 阻止修改生产目录

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write|Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input | .file_path // .command // \"\"' | grep -q '/prod/' && echo 'BLOCKED: 无法修改生产文件' && exit 2 || exit 0"
          }
        ]
      }
    ]
  }
}
```

## 通知钩子

### macOS 桌面通知

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.message' | xargs -I{} osascript -e 'display notification \"{}\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```

### Linux 桌面通知

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.message' | xargs -I{} notify-send 'Claude Code' '{}'"
          }
        ]
      }
    ]
  }
}
```

### 声音通知 (macOS)

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Glass.aiff"
          }
        ]
      }
    ]
  }
}
```

## 验证钩子

### 写入前验证 JSON

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -e '.tool_input | select(.file_path | endswith(\".json\")) | .content' | jq . > /dev/null 2>&1 || { echo 'JSON 内容无效'; exit 2; }"
          }
        ]
      }
    ]
  }
}
```

### 提交前检查 TypeScript 代码规范

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' | grep -q 'git commit' && npx eslint . --max-warnings 0 || exit 0"
          }
        ]
      }
    ]
  }
}
```

## 会话钩子

### 会话开始时初始化环境

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "[ -f .claude-env ] && source .claude-env"
          }
        ]
      }
    ]
  }
}
```

### 会话结束时清理

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "rm -f /tmp/claude-session-* 2>/dev/null; exit 0"
          }
        ]
      }
    ]
  }
}
```

## 多钩子示例

在一个配置中组合多个钩子：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"import json,sys; p=json.load(sys.stdin).get('tool_input',{}).get('file_path',''); sys.exit(2 if '.env' in p else 0)\""
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | { read f; [[ \"$f\" == *.ts ]] && npx prettier --write \"$f\" 2>/dev/null; exit 0; }"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "afplay /System/Library/Sounds/Glass.aiff"
          }
        ]
      }
    ]
  }
}
```