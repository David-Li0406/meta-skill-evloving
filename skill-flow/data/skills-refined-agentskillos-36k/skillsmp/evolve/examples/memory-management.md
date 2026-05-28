# Memory Management Examples

> 展示如何使用 Git-based Memory 系統記錄和檢索經驗

## Memory 目錄結構

```
.claude/memory/
├── index.md              # 快速索引（必須維護）
├── learnings/            # 成功經驗
│   └── 2026-01-07-comfyui-rembg.md
├── failures/             # 失敗教訓
│   └── 2026-01-07-vram-issue.md
├── patterns/             # 推理模式
│   └── debug-node-loading.md
├── decisions/            # 架構決策 (ADR)
│   └── 001-use-typescript.md
└── strategies/           # 策略記錄
    └── image-generation.md
```

## Example 1: 儲存學習經驗

當成功解決一個問題後，記錄經驗：

```markdown
# .claude/memory/learnings/2026-01-07-comfyui-rembg.md

---
date: 2026-01-07
tags: [comfyui, rembg, 透明背景, 遊戲素材]
task: 生成透明背景遊戲道具
status: resolved
---

# ComfyUI 生成透明背景圖片

## 情境
需要批量生成遊戲道具圖片，要求 PNG 透明背景

## 問題
預設輸出有白色背景，不適合遊戲使用

## 解決方案
1. 安裝 ComfyUI-Manager
2. 搜尋並安裝 RemBG 節點
3. 在工作流程最後加入 RemBG 節點
4. 輸出格式設為 PNG

## 驗證
✅ 成功生成透明背景圖片

## 注意事項
- 需要 4GB+ GPU 記憶體
- 處理速度約 2秒/張

## 相關檔案
- `workflows/game-assets.json`
```

## Example 2: 記錄失敗經驗

失敗也是寶貴的經驗，記錄以避免重蹈覆轍：

```markdown
# .claude/memory/failures/2026-01-07-vram-issue.md

---
date: 2026-01-07
tags: [comfyui, gpu, vram, batch]
task: 批量生成圖片
status: unresolved
---

# ComfyUI 批量生成 VRAM 不足

## 症狀
批量生成到第 4-5 張圖片時 GPU 記憶體耗盡

## 嘗試過的方案
1. ❌ 降低解析度 → 只延後問題發生
2. ❌ 使用 fp16 → 仍然洩漏
3. ⏳ 每張圖後重啟 → 待測試

## 根本原因
ComfyUI 節點沒有正確釋放中間張量

## 臨時解決方案
改用雲端 API (Stable Diffusion API)

## 待研究
- [ ] ComfyUI --lowvram 參數
- [ ] 手動清理 VRAM 的方法
```

## Example 3: 建立推理模式

將可複用的問題解決模式記錄下來：

```markdown
# .claude/memory/patterns/debug-api-timeout.md

---
category: debugging
name: API 超時診斷模式
applicable_to: [api, network, timeout]
success_rate: 85%
---

# API 超時診斷模式

## 觸發條件
當遇到 API 請求超時、連線失敗等錯誤時

## 診斷步驟

### Step 1: 確認網路連通性
```bash
curl -I https://api.example.com/health
```

### Step 2: 檢查超時設定
- 預設超時是否太短？
- 是否有重試機制？

### Step 3: 檢查請求大小
- 請求 payload 是否過大？
- 是否需要分批處理？

### Step 4: 檢查 API 限流
- 是否觸發了 rate limit？
- 檢查 X-RateLimit-* headers

### Step 5: 檢查伺服器狀態
- API 是否在維護中？
- 是否有已知的服務中斷？

## 常見解決方案

| 問題 | 解決方案 |
|------|----------|
| 超時太短 | 增加 timeout 設定 |
| 請求太大 | 分批處理、壓縮 |
| Rate limit | 加入 retry with backoff |
| 伺服器問題 | 等待或切換備援 |
```

## Example 4: 記錄策略池

為特定任務類型維護策略列表：

```markdown
# .claude/memory/strategies/code-optimization.md

---
task_type: 程式碼優化
last_updated: 2026-01-07
---

# 程式碼優化策略池

## 策略 S1: 演算法優化 (優先)
- **適用**: 時間複雜度問題
- **方法**: 分析 Big-O，選擇更優演算法
- **成功率**: 90%
- **風險**: 可能增加程式碼複雜度

## 策略 S2: 快取優化
- **適用**: 重複計算、頻繁 I/O
- **方法**: 加入 memoization、cache layer
- **成功率**: 85%
- **風險**: 記憶體增加、cache invalidation

## 策略 S3: 並行處理
- **適用**: CPU-bound、可並行的任務
- **方法**: 使用 worker threads、async/await
- **成功率**: 75%
- **風險**: race condition、複雜度增加

## 策略 S4: 延遲載入
- **適用**: 啟動時間過長
- **方法**: lazy loading、code splitting
- **成功率**: 80%
- **風險**: 首次使用時延遲

## 選擇邏輯
1. 先用 profiler 找出瓶頸
2. 根據瓶頸類型選擇策略
3. 優先嘗試 S1（改演算法）
4. S1 不適用再考慮 S2-S4
```

## Example 5: 搜尋記憶

使用 Grep 搜尋過去的經驗：

```python
# 搜尋所有 ComfyUI 相關經驗
Grep(
    pattern="ComfyUI|comfyui",
    path=".claude/memory/",
    output_mode="files_with_matches"
)
# → learnings/2026-01-07-comfyui-rembg.md
# → failures/2026-01-07-vram-issue.md

# 搜尋特定標籤
Grep(
    pattern="tags:.*gpu",
    path=".claude/memory/",
    output_mode="content",
    C=3
)

# 搜尋未解決的問題
Grep(
    pattern="status: unresolved",
    path=".claude/memory/failures/",
    output_mode="files_with_matches"
)
```

## Example 6: 維護索引

定期更新 index.md 保持快速查找：

```markdown
# .claude/memory/index.md

# 專案記憶索引

> Last curated: 2026-01-07
> Total entries: 15
> Next review: 2026-01-14

## 最近學習
<!-- LEARNINGS_START -->
- [ComfyUI 透明背景](learnings/2026-01-07-comfyui-rembg.md) - comfyui, rembg
- [TypeScript 嚴格模式](learnings/2026-01-05-ts-strict.md) - typescript, strict
- [React 效能優化](learnings/2026-01-03-react-perf.md) - react, performance
<!-- LEARNINGS_END -->

## 重要決策
<!-- DECISIONS_START -->
- [001 使用 TypeScript](decisions/001-use-typescript.md)
- [002 選擇 Vitest](decisions/002-use-vitest.md)
<!-- DECISIONS_END -->

## 待解決問題
<!-- FAILURES_START -->
- [VRAM 不足問題](failures/2026-01-07-vram-issue.md) - unresolved
<!-- FAILURES_END -->

## 標籤索引
<!-- TAGS_START -->
- `comfyui`: 2 entries
- `typescript`: 3 entries
- `react`: 5 entries
- `performance`: 4 entries
<!-- TAGS_END -->
```

## Memory 生命週期

```
┌─────────────────────────────────────────────────────────────────┐
│  Memory 生命週期管理                                             │
│                                                                 │
│  新增 → 使用 → 評估 → 處理                                      │
│                        ↓                                        │
│              ┌────────────────────┐                             │
│              │ 仍然相關？         │                             │
│              │ ├─ Yes → 保留      │                             │
│              │ ├─ 部分 → 合併/更新│                             │
│              │ └─ No → 標註過時   │                             │
│              └────────────────────┘                             │
│                                                                 │
│  定期清理：                                                      │
│  • 合併重複項目                                                  │
│  • 標註過時內容                                                  │
│  • 刪除無價值記錄                                                │
│  • 更新 index.md                                                │
└─────────────────────────────────────────────────────────────────┘
```

## Tips

1. **及時記錄** - 解決問題後立即記錄，避免遺忘細節
2. **標籤一致** - 使用一致的標籤方便搜尋
3. **定期清理** - 每週檢視一次，移除過時內容
4. **搜尋優先** - 執行任務前先搜尋是否有相關經驗
5. **結構化格式** - 使用 frontmatter 方便程式化處理
