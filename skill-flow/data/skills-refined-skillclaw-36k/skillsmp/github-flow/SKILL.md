---
name: github-flow
description: GitHub Flow 開發工作流程參考指南，適用於小團隊 + AI review 模式
---

# GitHub Flow 工作流程

輕量級、基於分支的工作流程，適合小團隊與持續部署。本指南假設 review 由 AI 自動完成。

官方參考：https://docs.github.com/en/get-started/using-github/github-flow

## 核心原則

- `main` 分支永遠保持可部署狀態
- 所有變更透過 feature branch + PR 進行
- AI 負責 code review，需等待回覆後處理意見
- 合併後立即部署

## 標準流程

### 1. 開始工作

```bash
git checkout main
git pull origin main
git checkout -b <branch-type>/<short-description>
```

**分支命名**：`feat/`、`fix/`、`refactor/`、`docs/` + 簡短描述

### 2. 開發與提交

```bash
git add <files>
git commit -m "<type>: <description>"
```

**Commit 類型**：feat, fix, refactor, docs, test, chore

每個 commit 應可獨立編譯/運行，訊息使用祈使句，主旨行 50 字元以內。

### 3. 推送與建立 PR

```bash
git push -u origin <branch-name>
gh pr create --fill
```

PR 標題清楚描述變更目的，描述包含變更內容與原因。

### 4. AI Review 循環

PR 建立後，AI reviewer 會自動分析並留下意見。

**等待時間**：
- 首次 review：約 2-3 分鐘
- 後續 review：約 1 分鐘 (需要回覆 `/gemini review` 指令來觸發)

**處理流程**：
1. 等待 AI review 完成
2. 查看 review 意見（GitHub UI 或 `gh pr view --comments`）
3. 評估建議：僅修復錯誤或重要改進，忽略風格偏好
4. 修改並推送
5. 重複直到通過

```bash
# 修改後
git add <files>
git commit -m "fix: address review feedback"
git push
```

### 5. 合併與清理

```bash
gh pr merge --squash

git checkout main
git pull origin main
git branch -d <branch-name>
```

## 常見情境

### 同步 main 的變更

```bash
git fetch origin main
git rebase origin/main
git push --force-with-lease
```

### 緊急修復

```bash
git checkout main && git pull
git checkout -b fix/critical-bug
# 修復、測試、提交、推送
gh pr create --fill
# 等待 AI review 通過後立即合併
```

## 檢查清單

開 PR 前：
- [ ] 程式碼可編譯/運行
- [ ] 測試通過
- [ ] Lint 通過

合併前：
- [ ] CI 全部通過
- [ ] AI review 意見已處理
- [ ] 分支已與 main 同步
