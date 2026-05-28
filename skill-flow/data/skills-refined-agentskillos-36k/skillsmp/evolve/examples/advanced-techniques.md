# Advanced Techniques

> 進階使用技巧和最佳實踐

## 客製化執行策略

### 策略池配置

為特定類型的任務預定義策略池：

```markdown
# .claude/memory/strategies/code-refactoring.md

---
task_type: 程式碼重構
last_updated: 2026-01-07
---

# 程式碼重構策略池

## 策略 S1: 漸進式重構 (推薦)
- **優先級**: 1
- **適用**: 大型專案、需要持續部署
- **方法**: 小步快跑，每次只改一小塊
- **成功率**: 95%
- **風險**: 時間較長

## 策略 S2: 平行重寫
- **優先級**: 2
- **適用**: 小型模組、有完整測試
- **方法**: 新舊並行，逐步切換
- **成功率**: 85%
- **風險**: 可能有功能差異

## 策略 S3: 大爆炸重構
- **優先級**: 3
- **適用**: 技術債過重、團隊一致同意
- **方法**: 一次性全部重寫
- **成功率**: 60%
- **風險**: 高，需要充分測試

## 選擇邏輯
if 測試覆蓋率 > 80% && 模組獨立:
    嘗試 S2
elif 專案規模 < 5000 行:
    嘗試 S3
else:
    使用 S1
```

### 動態策略選擇

```python
# 策略選擇偽代碼
def select_strategy(task, context):
    # 1. 搜尋相關策略
    strategies = grep(f".claude/memory/strategies/{task.type}.md")

    # 2. 過濾已失敗的策略
    available = [s for s in strategies if s.status != "failed"]

    # 3. 按成功率排序
    sorted_strategies = sorted(available, key=lambda s: s.success_rate, reverse=True)

    # 4. 考慮上下文約束
    for strategy in sorted_strategies:
        if strategy.requirements_met(context):
            return strategy

    # 5. 無可用策略 → 搜尋新策略
    return search_new_strategy(task)
```

## 記憶優化

### 記憶索引維護

定期維護索引以提升搜尋效率：

```bash
#!/bin/bash
# scripts/maintain-memory.sh

MEMORY_DIR=".claude/memory"
INDEX_FILE="$MEMORY_DIR/index.md"

echo "# 專案記憶索引" > $INDEX_FILE
echo "" >> $INDEX_FILE
echo "> 自動生成於 $(date)" >> $INDEX_FILE
echo "" >> $INDEX_FILE

# 統計
echo "## 統計" >> $INDEX_FILE
echo "- 學習記錄: $(ls $MEMORY_DIR/learnings/*.md 2>/dev/null | wc -l)" >> $INDEX_FILE
echo "- 失敗經驗: $(ls $MEMORY_DIR/failures/*.md 2>/dev/null | wc -l)" >> $INDEX_FILE
echo "- 推理模式: $(ls $MEMORY_DIR/patterns/*.md 2>/dev/null | wc -l)" >> $INDEX_FILE
echo "" >> $INDEX_FILE

# 最近學習
echo "## 最近學習" >> $INDEX_FILE
for file in $(ls -t $MEMORY_DIR/learnings/*.md 2>/dev/null | head -10); do
    title=$(head -1 "$file" | sed 's/^# //')
    echo "- [$title]($file)" >> $INDEX_FILE
done
echo "" >> $INDEX_FILE

# 未解決問題
echo "## 未解決問題" >> $INDEX_FILE
grep -l "status: unresolved" $MEMORY_DIR/failures/*.md 2>/dev/null | while read file; do
    title=$(head -1 "$file" | sed 's/^# //')
    echo "- [$title]($file)" >> $INDEX_FILE
done

echo "索引更新完成: $INDEX_FILE"
```

### 記憶去重和合併

```markdown
## 記憶清理流程

### 識別重複
1. 搜尋相似標籤的記錄
2. 比較內容相似度
3. 標記重複項目

### 合併策略
- 保留最新的記錄
- 合併獨特的見解
- 更新相關連結

### 歸檔舊記錄
- 超過 6 個月未引用 → 移至 archive/
- 技術已過時 → 標記 deprecated
```

## 失敗診斷進階

### 自動根因分析

```markdown
## 失敗診斷決策樹

開始
│
├─ 錯誤訊息包含 "not found"?
│   ├─ Yes → 類型: 環境問題
│   │         處方: 檢查依賴、路徑、版本
│   └─ No  → 繼續
│
├─ 錯誤訊息包含 "permission"?
│   ├─ Yes → 類型: 權限問題
│   │         處方: 檢查檔案權限、用戶權限
│   └─ No  → 繼續
│
├─ 錯誤訊息包含 "timeout"?
│   ├─ Yes → 類型: 資源限制
│   │         處方: 增加超時、優化效能、分批處理
│   └─ No  → 繼續
│
├─ 錯誤訊息包含 "syntax" or "parse"?
│   ├─ Yes → 類型: 執行錯誤
│   │         處方: 檢查語法、參數格式
│   └─ No  → 繼續
│
└─ 預設 → 類型: 需要進一步診斷
          處方: 搜尋相關經驗、查閱文檔、嘗試備選方案
```

### 失敗模式學習

```python
# 記錄失敗並學習
def record_and_learn(failure):
    # 1. 分類失敗類型
    failure_type = classify_failure(failure.error_message)

    # 2. 搜尋類似經驗
    similar = grep(failure_type, ".claude/memory/failures/")

    # 3. 如果是新類型，記錄
    if not similar:
        save_failure(failure)

    # 4. 更新策略成功率
    update_strategy_stats(failure.strategy, success=False)

    # 5. 建議下一步
    if similar:
        return f"找到類似失敗經驗，建議參考: {similar[0]}"
    else:
        return "新類型失敗，已記錄。建議搜尋外部資源。"
```

## 能力邊界擴展

### Skill 習得最佳實踐

```markdown
## Skill 習得流程優化

### 1. 預習得驗證
安裝前先驗證 skill 是否適用：
- 檢查 skill 的 triggers 和 keywords
- 閱讀 skill 的 description
- 確認 skill 的版本和更新日期

### 2. 漸進式學習
- 先用簡單任務測試
- 逐步增加複雜度
- 記錄每次使用的經驗

### 3. 知識內化
成功使用 skill 後：
- 記錄關鍵步驟到 learnings/
- 提取可複用的模式到 patterns/
- 更新策略池

### 4. 分享回饋
- 發現 skill 問題 → 提交 issue
- 有改進建議 → 提交 PR
- 成功案例 → 寫成範例分享
```

### 自動 Skill 推薦

```
┌─────────────────────────────────────────────────────────────────┐
│  Skill 推薦邏輯                                                 │
│                                                                 │
│  輸入: 任務描述                                                 │
│         ↓                                                       │
│  Step 1: 關鍵詞提取                                            │
│  「用 React 開發一個財務儀表板」                                │
│  → [React, 財務, 儀表板, 開發]                                  │
│         ↓                                                       │
│  Step 2: 已有經驗匹配                                          │
│  搜尋 .claude/memory/ 中的相關記錄                             │
│         ↓                                                       │
│  Step 3: Skill 匹配                                            │
│  - investment-analysis (財務 → 匹配)                           │
│  - ui-ux-design (儀表板 → 匹配)                                │
│         ↓                                                       │
│  Step 4: 排序推薦                                               │
│  按相關度和評分排序，返回 top 3                                │
└─────────────────────────────────────────────────────────────────┘
```

## 迭代優化

### PDCA 迭代追蹤

```markdown
## 迭代記錄模板

### 迭代 #1
- **Plan**: 使用 ComfyUI 生成遊戲道具
- **Do**: 安裝環境，建立基本工作流程
- **Check**: ❌ 輸出有白色背景
- **Act**: 研究透明背景解決方案

### 迭代 #2
- **Plan**: 加入 RemBG 節點去背景
- **Do**: 安裝 ComfyUI-Manager，加入節點
- **Check**: ✅ 成功生成透明背景
- **Act**: 記錄經驗，進入下一子目標

### 學到的經驗
- ComfyUI 預設不支援透明輸出
- RemBG 節點需要額外 GPU 記憶體
- 建議每 5 張圖重啟節點避免記憶體洩漏
```

### 效能指標追蹤

```markdown
## 執行效能指標

### 任務完成統計
| 指標 | 本週 | 上週 | 趨勢 |
|------|------|------|------|
| 完成任務數 | 15 | 12 | ↑ |
| 平均迭代次數 | 2.3 | 3.1 | ↓ (改善) |
| 首次成功率 | 65% | 52% | ↑ |
| 新學習記錄 | 8 | 5 | ↑ |

### 失敗類型分布
| 類型 | 次數 | 佔比 |
|------|------|------|
| 知識缺口 | 3 | 30% |
| 執行錯誤 | 2 | 20% |
| 環境問題 | 4 | 40% |
| 策略錯誤 | 1 | 10% |

### 改進方向
- 環境問題佔比高 → 建立環境檢查清單
- 首次成功率待提升 → 加強能力評估
```

## 多專案協作

### 跨專案記憶同步

```bash
#!/bin/bash
# scripts/sync-cross-project.sh

# 定義專案列表
PROJECTS=(
    "/path/to/project-a"
    "/path/to/project-b"
    "/path/to/project-c"
)

GLOBAL_MEMORY="$HOME/.claude/memory"

# 同步標記為全域的學習
for project in "${PROJECTS[@]}"; do
    local_memory="$project/.claude/memory"

    # 找出標記 global: true 的檔案
    grep -l "global: true" "$local_memory/learnings/"*.md 2>/dev/null | while read file; do
        filename=$(basename "$file")

        # 如果全域還沒有這個檔案，複製過去
        if [ ! -f "$GLOBAL_MEMORY/learnings/$filename" ]; then
            cp "$file" "$GLOBAL_MEMORY/learnings/"
            echo "Synced: $file → global"
        fi
    done
done
```

### 專案特定 vs 全域知識

```markdown
## 知識分類指南

### 放在專案記憶 (.claude/memory/)
- 專案特定的架構決策
- 專案相關的 bug 修復經驗
- 專案特定的配置和設定
- 團隊約定的規範

### 放在全域記憶 (~/.claude/memory/)
- 通用的程式設計技巧
- 跨專案適用的設計模式
- 工具使用經驗（Git, Docker 等）
- 個人偏好和習慣

### 標記方式
在 frontmatter 中加入：
- `global: true` - 同步到全域
- `project_specific: true` - 僅限本專案
```

## 除錯和疑難排解

### 常見問題診斷

| 問題 | 可能原因 | 解決方案 |
|------|----------|----------|
| 記憶搜尋無結果 | 關鍵詞不匹配 | 嘗試同義詞、模糊搜尋 |
| Skill 載入失敗 | 格式錯誤、依賴缺失 | 檢查 SKILL.md 格式 |
| 迭代超過上限 | 目標過於模糊 | 重新定義更具體的目標 |
| 策略重複失敗 | 策略不適用 | 強制切換到下一策略 |

### 除錯日誌

```markdown
## 開啟詳細日誌

在執行 evolve 時加入 --verbose 可以看到：
- 能力評估過程
- 策略選擇邏輯
- 記憶搜尋結果
- 每次迭代的詳細狀態

## 日誌範例

[INFO] 開始任務: 優化 UserList 效能
[DEBUG] 能力評估:
  - React 效能優化: 熟練
  - Profiler 使用: 基本
  - 需要習得: React.memo 進階用法
[DEBUG] 搜尋記憶: "React 效能" → 找到 2 筆
[DEBUG] 選擇策略: S1-memoization (成功率 85%)
[INFO] 開始 PDCA 迭代 #1
...
```

## 相關文檔

- [基本使用](./basic-usage.md)
- [失敗處理](./failure-handling.md)
- [記憶管理](./memory-management.md)
- [整合模式](./integration-patterns.md)
