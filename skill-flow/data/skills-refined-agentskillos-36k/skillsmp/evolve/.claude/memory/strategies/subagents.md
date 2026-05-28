---
task_type: subagent-strategies
last_updated: 2025-01-07
source: Boris Cherny Tips (Tip #8)
---

# Subagent 策略定義

> 來源：Boris Cherny (Claude Code 創作者) 的使用技巧

## 策略列表

### verify-app

**用途**：驗證應用程式正確運作

```yaml
trigger: "功能實作完成"
priority: 1
commands:
  - "npm test"
  - "npm run build"
  - "npm start & sleep 3 && curl -f http://localhost:3000/health || exit 1"
success_criteria: "所有命令回傳 0"
fail_action: "阻止進入下一步，報告錯誤"
```

**使用時機**：
- 每次功能實作完成後
- 重大重構後
- 合併分支前

---

### code-simplifier

**用途**：簡化複雜或冗長的程式碼

```yaml
trigger: "檔案超過 200 行 或 函數超過 50 行"
priority: 2
focus:
  - "重複程式碼 → 提取共用函數"
  - "深層巢狀 → 早期返回"
  - "過長函數 → 拆分職責"
  - "複雜條件 → 提取命名變數"
constraint: "不改變外部行為（相同輸入 → 相同輸出）"
verification: "執行測試確認行為不變"
```

**使用時機**：
- 程式碼審查時發現複雜度過高
- 新增功能後檔案變得難以維護
- 準備重構時

---

### build-validator

**用途**：驗證構建流程正確

```yaml
trigger: "程式碼變更"
priority: 1
commands:
  - "npm run build"
  - "npm run lint"
  - "npm run typecheck"  # 或 tsc --noEmit
success_criteria: "所有命令回傳 0，無警告"
fail_action: "阻止進入下一步"
```

**使用時機**：
- 每次程式碼變更後
- 提交前
- CI/CD 流程中

---

## 策略選擇邏輯

```
程式碼變更
    ↓
┌─────────────────────────────────────┐
│  1. build-validator                 │  ← 優先：確保能編譯
│     通過 → 繼續                      │
│     失敗 → 停止，修復錯誤            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  2. verify-app                      │  ← 次要：確保功能正確
│     通過 → 繼續                      │
│     失敗 → 停止，修復錯誤            │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  3. code-simplifier（可選）          │  ← 最後：優化程式碼
│     觸發條件符合 → 執行簡化          │
│     條件不符 → 跳過                  │
└─────────────────────────────────────┘
    ↓
  完成
```

## 自訂 Subagent

可以根據專案需求新增自訂 subagent：

```yaml
# 範例：security-checker
security-checker:
  trigger: "涉及認證、授權、資料處理"
  commands:
    - "npm audit"
    - "npx eslint --config .eslintrc.security.json"
  focus:
    - "SQL injection"
    - "XSS vulnerabilities"
    - "Sensitive data exposure"
  fail_action: "警告並建議修復"
```
