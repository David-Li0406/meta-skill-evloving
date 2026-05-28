# Design: Boris Tips Integration

## 架構決策

### AD-1: 文檔位置

| 項目 | 位置 | 理由 |
|------|------|------|
| Permissions 配置 | `skills/00-getting-started/_base/psb-setup.md` | 屬於環境設定的一部分 |
| Large Codebase | `skills/06-scaling/_base/large-codebase.md` | 新增專門的 scaling 模組 |

### AD-2: 新增 06-scaling 模組

```
skills/
├── ...
├── 05-integration/
├── 06-scaling/          # 新增
│   ├── README.md
│   └── _base/
│       └── large-codebase.md
└── 99-evolution/
```

**理由：**
- Large codebase 優化是獨立的關注點
- 未來可擴展其他 scaling 相關主題（平行執行、資源管理等）
- 保持原子化架構的一致性

## 技術設計

### P0: Permissions 配置

在 `psb-setup.md` 的 Setup 階段添加新步驟：

```markdown
│  □ 8. Claude Code 權限配置（可選）                             │
│     - 使用 /permissions 精細管理                               │
│     - 預先允許安全的常用命令                                   │
```

**配置範例：**

```json
// .claude/settings.local.json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git status)",
      "Bash(git diff*)",
      "Bash(git log*)",
      "Bash(make *)",
      "Read(*)",
      "Glob(*)",
      "Grep(*)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force*)"
    ]
  }
}
```

### P1: Large Codebase 優化

**文檔結構：**

```markdown
# Large Codebase 優化

## 問題診斷
- 何時需要此優化
- 預設行為說明

## 解決方案
- fileSuggestion 配置
- 自訂索引腳本

## 實作步驟
1. 建立索引腳本
2. 配置 settings.json
3. 驗證效果

## 適用場景
- 大型 monorepo
- 檔案數 > 10,000
```

**fileSuggestion 配置：**

```json
// settings.json
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

**索引腳本模板：**

```bash
#!/bin/bash
# file-suggestion.sh - 快速檔案索引
# 使用 fd 或 find 配合快取提升效能

CACHE_FILE="${HOME}/.claude/file-index-cache"
CACHE_TTL=300  # 5 分鐘

# 檢查快取
if [[ -f "$CACHE_FILE" ]]; then
  age=$(($(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE")))
  if [[ $age -lt $CACHE_TTL ]]; then
    cat "$CACHE_FILE"
    exit 0
  fi
fi

# 重建索引
if command -v fd &>/dev/null; then
  fd --type f --hidden --exclude .git > "$CACHE_FILE"
else
  find . -type f -not -path '*/.git/*' > "$CACHE_FILE"
fi

cat "$CACHE_FILE"
```

## 整合點

### SKILL.md 更新

在目錄結構中添加：

```markdown
| **06-scaling** | 大規模專案優化 | [→](./06-scaling/) |
```

### 快速導覽更新

```markdown
## 快速導覽

| 模組 | 用途 | 路徑 |
|------|------|------|
| ... |
| **06-scaling** | 大規模專案優化 | [→](./06-scaling/) |
```

## 驗證計劃

1. **P0 驗證**：執行 `/permissions` 確認配置生效
2. **P1 驗證**：在大型專案中測試檔案搜尋速度
