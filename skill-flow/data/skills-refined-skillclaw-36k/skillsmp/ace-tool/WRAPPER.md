# Ace 命令包装器

## 概述

`ace` 是一个包装脚本，提供了更简洁的命令行接口来调用 ace-tool 功能。

## 位置

- **包装器路径**: `/usr/local/bin/ace`
- **目标脚本**: `~/.pi/agent/skills/ace-tool/client.ts`

## 原理

`ace` 是一个 Bash 包装脚本，它：
1. 解析命令行参数
2. 验证输入
3. 调用 `bun` 执行实际的 `client.ts` 脚本

## 支持的命令

```bash
# 语义搜索
ace search "<query>"
ace s "<query>"              # 简写

# 提示增强
ace enhance "<prompt>"
ace e "<prompt>"             # 简写
```

## 实现代码

```bash
#!/usr/bin/env bash
SCRIPT_PATH="$HOME/.pi/agent/skills/ace-tool/client.ts"

case "$1" in
    search|s)
        bun "$SCRIPT_PATH" search "$@"
        ;;
    enhance|e)
        bun "$SCRIPT_PATH" enhance "$@"
        ;;
    *)
        echo "Error: Unknown command"
        ;;
esac
```

## 优势

1. **简洁性**: `ace search` vs `bun ~/.pi/agent/skills/ace-tool/client.ts search`
2. **可读性**: 更易记忆和使用
3. **参数验证**: 提前验证命令参数

## 安装/更新

如果 `ace` 命令不可用，需要创建包装器：

```bash
sudo tee /usr/local/bin/ace > /dev/null << 'EOF'
#!/usr/bin/env bash
SCRIPT_PATH="$HOME/.pi/agent/skills/ace-tool/client.ts"

if [ $# -lt 1 ]; then
    echo "Usage: ace <command> [args]"
    echo ""
    echo "Commands:"
    echo "  search <query>   - Search codebase semantically"
    echo "  enhance <prompt> - Enhance prompt with codebase context"
    echo ""
    echo "Examples:"
    echo '  ace search "Where is authentication handled?"'
    echo '  ace enhance "Add login page"'
    exit 1
fi

COMMAND="$1"
shift

case "$COMMAND" in
    search|s)
        if [ $# -lt 1 ]; then
            echo "Error: search requires a query"
            echo "Usage: ace search <query>"
            exit 1
        fi
        bun "$SCRIPT_PATH" search "$@"
        ;;
    enhance|e)
        if [ $# -lt 1 ]; then
            echo "Error: enhance requires a prompt"
            echo "Usage: ace enhance <prompt>"
            exit 1
        fi
        bun "$SCRIPT_PATH" enhance "$@"
        ;;
    *)
        echo "Error: Unknown command '$COMMAND'"
        echo "Usage: ace <search|enhance> [args]"
        exit 1
        ;;
esac
EOF

sudo chmod +x /usr/local/bin/ace
```

## 验证

```bash
# 检查 ace 命令是否存在
which ace

# 查看帮助
ace

# 测试搜索
ace search "test query"
```
