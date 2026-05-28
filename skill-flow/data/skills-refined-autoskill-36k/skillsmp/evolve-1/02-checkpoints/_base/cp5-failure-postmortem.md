# Checkpoint 5: 失敗後驗屍（Failure Post-Mortem）

> 🚨 **強制檢查點** - PDCA Check 失敗時觸發
>
> 靈感來源：SAGE (Self-Attributing) + GEPA (Reflective Evaluation)
>
> 🔗 **v5.9 整合**：強制使用 `superpowers:systematic-debugging`
> — 詳見：[05-integration/_base/superpowers-integration.md](../../05-integration/_base/superpowers-integration.md)

## 觸發條件

| 條件 | 行為 |
|------|------|
| PDCA Check 失敗 | 立即執行 Post-Mortem |
| 測試/構建失敗 | 立即執行 Post-Mortem |
| 連續 2 次嘗試失敗 | 強制深度 Post-Mortem |
| 用戶反饋「不對」 | 立即執行 Post-Mortem |

## 強制輸出格式

每次觸發 CP5 後，**必須**生成結構化 Lesson 並存入 `.claude/memory/lessons/`：

```yaml
---
date: "YYYY-MM-DD"
task: "[任務描述]"
failure_id: "[YYYYMMDD-HHMM-簡短描述]"

classification:
  type: "A|B|C|D|E"  # 見下方類型說明
  confidence: "high|medium|low"

diagnosis:
  symptom: "[具體錯誤現象]"
  error_message: "[錯誤訊息原文]"
  root_cause: "[根本原因分析 - 5 Whys]"

lesson:
  principle: "[一句話通用原則，可在其他場景重用]"
  applicable_to:
    - "[適用場景 1]"
    - "[適用場景 2]"
  not_applicable_when: "[不適用情境]"

correction:
  action_taken: "[採取的修正措施]"
  outcome: "success|partial|failed"
  time_to_fix: "[修復耗時]"

tags: [tag1, tag2, tag3]
---

## 失敗背景

[詳細描述失敗發生的上下文]

## 診斷過程

[記錄分析過程，包括排除的假設]

## 關鍵洞察

[最重要的發現，未來應該記住的事]
```

## 失敗類型分類（Type A-E）

| Type | 名稱 | 描述 | 典型修正 |
|------|------|------|----------|
| A | Knowledge Gap | 缺乏領域知識 | 習得新 Skill、查文檔 |
| B | Execution Error | 知道怎麼做但執行出錯 | 重試、微調參數 |
| C | Environment Issue | 依賴/配置/權限問題 | 修復環境、提示用戶 |
| D | Strategy Error | 方向錯誤、方法不適用 | 切換策略 |
| E | Resource Limit | 超時/額度/記憶體限制 | 分解任務、降級 |

## Superpowers 整合：Systematic Debugging

🔗 **強制使用 systematic-debugging（不可跳過）**：

```
宣告：「我正在使用 superpowers:systematic-debugging skill。」

鐵律：NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

### 四階段流程（不可跳過任何階段）

```
Phase 1: 根因調查（修復前必完成）
├─ 仔細閱讀錯誤訊息（不要跳過）
├─ 穩定重現問題（怎麼觸發？每次都發生？）
├─ 檢查近期變更（git diff、最近 commits）
└─ 收集證據（多組件系統要追蹤每層）

Phase 2: 模式分析
├─ 找到運作中的類似程式碼
├─ 與參考實作比較（完整閱讀，不要略讀）
└─ 識別差異

Phase 3: 假設與測試
├─ 形成單一假設（明確寫下）
├─ 最小化測試（一次只改一個變數）
└─ 驗證後才繼續

Phase 4: 實作
├─ 建立失敗測試案例（使用 TDD）
├─ 實作單一修復
└─ 驗證修復
```

### 紅旗清單（如果你在想以下內容，立即停止）

| 想法 | 現實 | 行動 |
|------|------|------|
| 「先快速修復，之後再調查」 | 隨機修復浪費時間 | 回到 Phase 1 |
| 「試著改改 X 看會不會好」 | 不理解 = 新 bug | 回到 Phase 1 |
| 「同時改多處，跑測試」 | 無法隔離問題 | 回到 Phase 3 |
| 「再試一次」（已試 2+ 次）| 3+ 次失敗 = 架構問題 | 質疑架構 |

### 3+ 次修復失敗：質疑架構

如果已嘗試 3 次以上修復仍然失敗：

```
STOP - 不要嘗試第 4 次修復

詢問：
- 這個模式是否根本有問題？
- 我們是否「因為慣性而堅持」？
- 應該重構架構還是繼續修症狀？

與用戶討論後再行動
```

## Post-Mortem 引導問題

執行 CP5 時，依序回答以下問題：

### 1. 現象確認
- 發生了什麼？（具體錯誤）
- 預期行為是什麼？
- 實際行為是什麼？

### 2. 根因分析（5 Whys）
- Why 1: 為什麼失敗？
- Why 2: 為什麼會這樣？
- Why 3: 為什麼沒有預防？
- Why 4: 為什麼沒有偵測到？
- Why 5: 根本原因是什麼？

### 3. 通用化
- 這個教訓可以泛化到什麼場景？
- 什麼情況下這個教訓不適用？
- 用一句話總結核心原則

### 4. 預防措施
- 如何避免再次發生？
- 需要更新哪些 Skill？
- 需要添加什麼檢查？

## 範例

```yaml
---
date: "2026-01-12"
task: "建立 React 元件測試"
failure_id: "20260112-1430-jest-config-missing"

classification:
  type: "C"
  confidence: "high"

diagnosis:
  symptom: "執行 npm test 時報錯 'Cannot find module jest'"
  error_message: "Error: Cannot find module 'jest' from '/project'"
  root_cause: "專案使用 Vitest 而非 Jest，沒有先檢查測試框架配置"

lesson:
  principle: "執行測試前，先檢查 package.json 的 test script 確認測試框架"
  applicable_to:
    - "任何 JavaScript/TypeScript 專案的測試"
    - "CI/CD 配置"
  not_applicable_when: "已知專案測試框架的情況"

correction:
  action_taken: "改用 npm run test (實際執行 vitest)"
  outcome: "success"
  time_to_fix: "2 分鐘"

tags: [testing, javascript, environment, vitest, jest]
---

## 失敗背景

用戶要求為 React 元件添加測試。直接假設使用 Jest 並執行 `npx jest`。

## 診斷過程

1. 首先懷疑 Jest 未安裝 → 檢查 devDependencies，沒有 jest
2. 檢查 package.json scripts → 發現 `"test": "vitest"`
3. 確認使用 Vitest 而非 Jest

## 關鍵洞察

**不要假設測試框架**。JavaScript 生態有多種選擇（Jest、Vitest、Mocha、Jasmine）。
始終先檢查 `package.json` 的 `scripts.test` 欄位。
```

## 整合點

### 與 PDCA 的整合

```
Plan → Do → Check
              ↓ (失敗)
           CP5 觸發
              ↓
         生成 Lesson
              ↓
         存入 lessons/
              ↓
           Act (修正)
              ↓
         下一輪 Plan (自動載入相關 Lessons)
```

### 與 Plan 階段的整合

在 Plan 階段開始時，除了搜尋 Memory，還要：

```bash
# 搜尋相關 Lessons
Grep pattern="[任務關鍵字]" path=".claude/memory/lessons/"
```

Plan 階段應考慮：
1. 過去類似任務的 Lessons
2. 高頻失敗類型的預防措施
3. 最近的 Lessons（可能揭示系統性問題）

## 指標追蹤

建議追蹤以下指標評估 CP5 效果：

| 指標 | 計算方式 | 目標 |
|------|----------|------|
| Lesson 覆蓋率 | lessons 數 / failures 數 | > 80% |
| Lesson 可泛化率 | applicable_to 數量 > 1 的比例 | > 60% |
| 重複失敗率 | 相同 root_cause 的失敗 / 總失敗 | < 10% |
| 修復成功率 | outcome=success 的比例 | > 90% |

## Memory MCP 整合

除了存入 `.claude/memory/lessons/`，也同步到 Memory MCP 以加速搜尋：

```python
# 記錄失敗到 SQLite（供跨專案搜尋）
failure_record({
    "error_pattern": "[錯誤類型，如 TypeError: Cannot read properties]",
    "error_message": "[完整錯誤訊息]",
    "solution": "[採取的解決方案]",
    "skill_name": "evolve",
    "project_path": "/path/to/project"
})
```

**效益**：
- 下次遇到類似錯誤時，CP1 的 `failure_search` 可快速找到解法
- 跨專案共享失敗經驗，避免在不同專案重複踩坑
- FTS5 搜尋比 Grep 快 5-6x，Token 節省 91%

## 護欄

- ❌ 不可跳過 CP5（失敗後必須執行）
- ❌ 不可省略 `lesson.principle`（必須提煉通用教訓）
- ❌ 不可重複相同 root_cause 超過 3 次（必須系統性解決）
- ✅ 每個 Lesson 必須有 tags 方便搜尋
- ✅ 每個 Lesson 必須記錄 time_to_fix 用於效率分析
- ✅ 同步到 Memory MCP 以加速跨專案搜尋（若可用）
