#!/bin/bash
# CheckPoint 提醒 Hook
# 輸出 JSON 格式，讓 Claude 透過 additionalContext 看到提醒

cat << 'EOF'
{
  "additionalContext": "🔍 CheckPoint 提醒：\n• CP1.5: 確認已檢查現有實作、專案慣例\n• CP2: 記得執行編譯+測試驗證"
}
EOF
