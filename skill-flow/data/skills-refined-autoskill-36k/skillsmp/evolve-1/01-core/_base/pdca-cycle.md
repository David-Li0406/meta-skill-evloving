# PDCA 執行循環

> Plan → Do → Check → Act 的迭代執行
>
> 🔗 **v5.9 Superpowers 整合**：
> - **Plan**: Level 2 使用 `superpowers:writing-plans`
> - **Do**: 強制使用 `superpowers:test-driven-development`
> - **Check**: 強制使用 `superpowers:verification-before-completion`
> - 詳見：[05-integration/_base/superpowers-integration.md](../../05-integration/_base/superpowers-integration.md)

## 流程

### Plan（規劃）
- 制定具體執行計劃、預測可能問題、準備備選方案
- 架構設計（依等級觸發，見下方）

### Do（執行）
- 按計劃執行、記錄過程、收集中間結果

🔗 **強制使用 TDD（不可跳過）**：

```
宣告：「我正在使用 superpowers:test-driven-development skill。」

RED → GREEN → REFACTOR 循環：
1. 先寫測試（RED）
2. 看測試失敗（驗證 RED）
3. 寫最小實作（GREEN）
4. 看測試通過（驗證 GREEN）
5. 重構（REFACTOR）
6. 循環
```

**鐵律**：
```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

如果先寫了程式碼再寫測試 → 刪除程式碼，從測試開始

### Check（評估）
- 結果是否符合預期？失敗則分析原因
- 評估：完全成功 / 部分成功 / 失敗

🔑 **Boris Tip #13**: 給 Claude 驗證工作的方式，品質提升 2-3 倍

🔗 **強制使用 verification-before-completion（不可跳過）**：

```
宣告：「我正在使用 superpowers:verification-before-completion skill。」

鐵律：NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

**自動化驗證策略**：
- [ ] 執行測試：`npm test` / `pytest` / `go test`
- [ ] 執行構建：`npm run build` / `tsc` / `cargo build`
- [ ] Lint 檢查：`eslint` / `prettier --check`
- [ ] 型別檢查：`tsc --noEmit`

**禁止用語**：
- ❌ "should work now"
- ❌ "probably fixed"
- ❌ "looks correct"

**正確做法**：
```
✅ [執行測試命令] [看到: 34/34 pass] "所有測試通過"
```

**驗證失敗 → 不進入下一步，先修復**

### Act（改進）

**成功時**：記錄到 `.claude/memory/learnings/` → 更新 index.md → 下一子目標

**失敗時**：反思 → 學習 → 搜索 → 更新策略 → 記錄到 `.claude/memory/failures/` → 重試

## Plan 階段：架構設計指引

根據 Goal Analysis 階段標記的 `architecture_level`，決定 Plan 階段的深度：

### Level 0: 直接執行

不需要架構考量，直接制定執行計劃。

### Level 1: 輕量架構思考

💡 **Level 1 快速檢查（1-2 分鐘）**
- [ ] 錯誤處理：這個功能可能失敗嗎？如何處理？
- [ ] 命名：函數/變數名稱是否清晰表達意圖？
- [ ] 位置：程式碼應該放在哪個檔案/目錄？
- [ ] 測試：需要寫測試嗎？測什麼？

### Level 2: 完整架構設計

🔗 **強制使用 writing-plans**：

```
宣告：「我正在使用 superpowers:writing-plans skill 來撰寫實作計畫。」
```

計畫產出：`docs/plans/YYYY-MM-DD-<feature-name>.md`

🏗️ **Level 2 架構設計流程**

**Step 1: 可靠性考量**
- [ ] 錯誤處理策略：可能遇到哪些錯誤？使用統一處理方式
- [ ] 重試機制：需要重試嗎？指數退避？固定間隔？
- [ ] 降級策略：核心失敗有備選方案嗎？需要 circuit breaker？

**Step 2: 可擴展性考量**
- [ ] 介面設計：足夠抽象？容易新增變體？
- [ ] 依賴方向：符合分層？有逆向依賴？
- [ ] 變化點識別：未來最可能變化的部分？需預留擴展點？

**Step 3: 可維護性考量**
- [ ] 分層與職責：模組職責單一？符合分層架構？
- [ ] 設計模式：需使用專案已採用的模式？避免過度設計（YAGNI）
- [ ] 測試策略：單元測試覆蓋哪些場景？需整合測試？

**Step 4: 輸出設計決策**
- 記錄關鍵決策，供 CP1.5 Phase 2 驗證

### 設計決策記錄模板

完成 Level 2 架構設計後，記錄關鍵決策：

```yaml
architecture_decisions:
  task: "建立用戶通知系統"

  reliability:
    error_handling: "使用 NotificationError 類別，繼承 AppError"
    retry_strategy: "外部服務失敗時重試 3 次，指數退避"
    fallback: "Email 失敗時降級為 in-app 通知"

  scalability:
    interface: "NotificationChannel 抽象介面，支援多種通道"
    patterns: "Strategy Pattern 處理不同通知類型"
    extension_points: "新通道只需實作 NotificationChannel"

  maintainability:
    location: "src/notifications/ 新模組"
    layer: "Service 層，依賴 Repository 層"
    testing: "每個 Channel 獨立單元測試"
```

### 架構設計與後續流程的關係

| 階段 | 動作 | 輸出 |
|------|------|------|
| Goal Analysis | 判斷架構等級 | `architecture_level: 2` |
| PDCA Plan | 做設計決策 | 設計決策記錄 |
| CP1.5 Phase 2 | 驗證實作 | 確認符合設計 |

→ 設計 → 實作 → 驗證 閉環

---

## 失敗模式診斷

失敗時先分類，再針對性處理：

| 類型 | 症狀 | 處方 |
|------|------|------|
| **A: 知識缺口** | 不知道怎麼做 | recommend_skill → install → learn |
| **B: 執行錯誤** | 知道但做錯了 | 重新閱讀文檔、檢查參數 |
| **C: 環境問題** | 依賴缺失、版本不符 | 修復環境、安裝依賴 |
| **D: 策略錯誤** | 方法正確但不適合情境 | 切換到其他策略 |
| **E: 資源限制** | 記憶體不足、API 限制 | 優化資源、分批處理 |

## 多策略機制

不重複嘗試同一個失敗策略：

```
策略選擇邏輯：
1. 從 available_strategies 按 priority 排序
2. 跳過 status = "failed" 的策略
3. 選擇第一個可行的策略
4. 如果所有策略都失敗 → 詢問用戶或搜尋新策略
```

## 反思流程（Reflexion）

每次失敗後：

1. **失敗分析**
   - 錯誤類型是什麼？
   - 根本原因是什麼？

2. **知識補充**
   - 需要學習什麼？
   - 搜索相關資料

3. **策略調整**
   - 原策略哪裡有問題？
   - 新策略是什麼？

4. **記憶更新**
   - 寫入 .claude/memory/
   - 格式：[情境] → [錯誤] → [解決方案]
