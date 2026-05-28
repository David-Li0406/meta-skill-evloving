#!/bin/bash
# Memory 同步提醒 Hook
# 只在寫入 .claude/memory/ 目錄時觸發

FILE="$CLAUDE_TOOL_ARG_FILE_PATH"

if [[ "$FILE" == *".claude/memory/"* ]]; then
  cat << 'EOF'
{
  "additionalContext": "CP3.5: 已創建 Memory 文件，記得同步 index.md"
}
EOF
fi
