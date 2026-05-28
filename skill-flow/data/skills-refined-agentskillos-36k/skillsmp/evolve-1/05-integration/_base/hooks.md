# Claude Code Hooks 整合

> 使用 Hooks 自動化觸發驗證和記錄
>
> 🔗 **v5.9 更新**：整合 Superpowers 工作流強制執行
> — 詳見：[superpowers-integration.md](./superpowers-integration.md)

## Hook 類型

| Hook | 時機 | 用途 |
|------|------|------|
| **PreToolUse** | 工具執行前 | 版本偵測、前置檢查、CP0/CP1/CP1.5 |
| **PostToolUse** | 工具執行後 | 自動格式化、驗證、CP2/CP3.5 |
| **Stop** | 會話結束時 | 提醒記錄學習、CP3/CP4/CP5/CP6 |

## Checkpoint 與 Hook 對照

| Checkpoint | Hook 類型 | 觸發條件 | 強制內容 |
|------------|-----------|----------|----------|
| CP0 北極星錨定 | PreToolUse | Task 啟動 | 檢查 north-star 文件 |
| CP1 Memory 搜尋 | PreToolUse | Task 啟動 | 提醒搜尋 Memory |
| CP1.5 一致性 | PreToolUse | Edit/Write | 提醒檢查專案慣例 |
| CP2 PDCA 驗證 | PostToolUse | Bash (test) | 驗證測試結果 |
| CP3 方向確認 | Stop | Milestone | 確認目標對齊 |
| CP3.5 Index 同步 | PostToolUse | Edit Memory | 提醒更新 index.md |
| CP4 涌現檢查 | Stop | 迭代完成 | 檢查涌現機會 |
| CP5 失敗後驗屍 | PostToolUse | Bash 失敗 | 🔗 systematic-debugging |
| CP6 經驗記錄 | Stop | 任務完成 | 記錄學習經驗 |

## Superpowers 整合 Hooks

| 觸發時機 | Superpowers Skill | 強制提醒 |
|----------|-------------------|----------|
| Edit/Write 程式碼 | TDD | RED → GREEN → REFACTOR |
| Bash 測試命令 | verification | 驗證證據要求 |
| Bash 失敗 | systematic-debugging | 四階段流程 |
| Task 啟動 | brainstorming | 深度訪談 (Level 1+) |

## 配置方式

在 `.claude/settings.local.json` 配置：

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "echo '📝 File modified - remember to verify changes'"
      }
    ],
    "Stop": [
      {
        "command": "echo '💡 Session ended - consider recording learnings to .claude/memory/'"
      }
    ]
  }
}
```

## PostToolUse Hook

### 自動格式化

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "npx prettier --write $FILE"
      }
    ]
  }
}
```

### Lint 檢查

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "npx eslint $FILE --fix"
      }
    ]
  }
}
```

## Stop Hook

### 完成驗證

```json
{
  "hooks": {
    "Stop": [
      {
        "command": "npm test && npm run build"
      }
    ]
  }
}
```

### 學習提醒

```json
{
  "hooks": {
    "Stop": [
      {
        "command": "echo '💡 記得將本次學習記錄到 .claude/memory/'"
      }
    ]
  }
}
```

## evolve v5.9 完整 Hooks 配置

> 🔗 使用 `scripts/evolve-hooks.sh` 統一管理所有提醒

### 方式一：使用腳本（推薦）

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Task",
        "command": "./scripts/evolve-hooks.sh pre-task-start"
      },
      {
        "matcher": "Edit|Write",
        "command": "./scripts/evolve-hooks.sh pre-code-write"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "./scripts/evolve-hooks.sh post-edit-write $TOOL_NAME $EXIT_CODE $FILE_PATH"
      },
      {
        "matcher": "Bash",
        "condition": "exit_code != 0",
        "command": "./scripts/evolve-hooks.sh post-bash-failed $TOOL_NAME $EXIT_CODE"
      },
      {
        "matcher": "Bash",
        "condition": "command =~ '(npm test|pytest|go test|bun test|vitest|jest)'",
        "command": "./scripts/evolve-hooks.sh post-bash-test $TOOL_NAME $EXIT_CODE"
      }
    ],
    "Stop": [
      {
        "command": "./scripts/evolve-hooks.sh stop-verification"
      },
      {
        "command": "./scripts/evolve-hooks.sh stop-memory"
      }
    ]
  }
}
```

### 方式二：內嵌命令

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Task",
        "command": "echo '🌟 [CP0] 北極星檢查 - 確認任務對齊目標' && echo '📚 [CP1] 記得搜尋 Memory'"
      },
      {
        "matcher": "Edit|Write",
        "command": "echo '⚠️ [CP1.5] 寫程式碼前：1.搜尋現有實作 2.檢查專案慣例' && echo '🧪 [TDD] 記得先寫測試！'"
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "echo '🧪 [superpowers:TDD] RED → GREEN → REFACTOR' && echo '   鐵律: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST'"
      },
      {
        "matcher": "Bash",
        "condition": "exit_code != 0",
        "command": "echo '🔧 [superpowers:systematic-debugging] 命令失敗！' && echo '   鐵律: NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST' && echo '   四階段：根因調查 → 模式分析 → 假設測試 → 實作修復'"
      },
      {
        "matcher": "Bash",
        "condition": "command =~ '(npm test|pytest|go test)'",
        "command": "[ $EXIT_CODE -eq 0 ] && echo '✅ 測試通過' || echo '🛑 測試失敗 - 不可宣告完成！'"
      }
    ],
    "Stop": [
      {
        "command": "echo '✅ [superpowers:verification] 完成前確認：測試通過？Build 成功？Lint 無警告？' && echo '   禁止用語: should work / probably fixed / looks correct'"
      },
      {
        "command": "echo '📝 [CP6] 記得記錄學習經驗到 .claude/memory/'"
      }
    ]
  }
}
```

### 三條鐵律提醒

Hooks 會強制提醒以下核心紀律：

| 鐵律 | 觸發時機 | Hook |
|------|----------|------|
| NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST | Edit/Write 程式碼 | PostToolUse |
| NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST | Bash 失敗 | PostToolUse |
| NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE | 會話結束 | Stop |
| NO RELEASE WITHOUT VERSION CONSISTENCY CHECK | 發布前 | PreToolUse |

## Release Hooks（版本發布）

### 版本發布強制檢查

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "condition": "file_path =~ '(SKILL\\.md|plugin\\.json|marketplace\\.json|CHANGELOG\\.md)'",
        "command": "./scripts/evolve-hooks.sh post-version-update"
      },
      {
        "matcher": "Bash",
        "condition": "command =~ 'git tag'",
        "command": "./scripts/evolve-hooks.sh post-git-tag"
      }
    ]
  }
}
```

### Release Hooks 類型

| Hook | 觸發時機 | 提醒內容 |
|------|----------|----------|
| `post-version-update` | 修改版本相關文件後 | 執行 check-version.sh |
| `post-git-tag` | 建立 git tag 後 | 推送 tag、建立 release |
| `pre-release` | 發布前手動調用 | 完整發布檢查清單 |

### 手動調用發布檢查

```bash
# 發布前顯示完整檢查清單
./scripts/evolve-hooks.sh pre-release
```

輸出：
```
🚀 [Release] 發布前強制檢查清單

   發布前檢查：
   [ ] git status 工作區乾淨
   [ ] ./scripts/check-version.sh 版本一致
   [ ] CHANGELOG.md 已更新
   [ ] ./scripts/check-env.sh 環境正常

   發布流程：
   1. ./scripts/update-version.sh X.Y.Z
   2. 更新 CHANGELOG.md
   3. git commit
   4. git tag vX.Y.Z
   5. git push && git push --tags
   6. gh release create vX.Y.Z

   鐵律: NO RELEASE WITHOUT VERSION CONSISTENCY CHECK
```

## Boris Tip 整合

### Tip #9: PostToolUse 自動格式化

> 讓 Claude 專注於邏輯，格式化交給工具

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "command": "npx prettier --write $FILE && npx eslint $FILE --fix"
      }
    ]
  }
}
```

### Tip #12: Stop Hook 完成驗證

> 確保長時間任務完成時驗證結果

```json
{
  "hooks": {
    "Stop": [
      {
        "command": "npm test && npm run build && echo '✅ All checks passed'"
      }
    ]
  }
}
```

## 注意事項

1. **Hook 命令要快** - 避免阻塞
2. **錯誤處理** - Hook 失敗不應阻止繼續
3. **環境依賴** - 確保命令在專案目錄可執行
