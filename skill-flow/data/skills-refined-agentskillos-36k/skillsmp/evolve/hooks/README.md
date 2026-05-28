# Hooks 配置說明

本專案有兩種 hooks 機制，服務不同場景：

## 1. Claude Code Plugin Hooks（本目錄）

位置：`hooks/*.json` + `hooks/*.sh`

用於 Claude Code Plugin 自動載入，透過 `additionalContext` 提供提醒。

| 檔案 | 觸發時機 | 功能 |
|------|----------|------|
| `checkpoint-reminder.json` | Edit/Write | 提醒 CP1.5、CP2 檢查點 |
| `memory-sync.json` | Write to .claude/memory/ | 提醒 CP3.5 同步 index.md |

## 2. evolve-hooks.sh（scripts 目錄）

位置：`scripts/evolve-hooks.sh`

更完整的提醒腳本，包含：
- TDD 流程提醒
- Memory 同步提醒
- 版本發布檢查
- 彩色輸出格式

### 手動配置方式

在 `~/.claude/settings.json` 中添加：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/scripts/evolve-hooks.sh post $TOOL_NAME $EXIT_CODE $FILE_PATH"
          }
        ]
      }
    ]
  }
}
```

## 選擇建議

- **使用 Plugin**：自動載入 `hooks/` 目錄配置
- **自訂需求**：使用 `scripts/evolve-hooks.sh` 手動配置
