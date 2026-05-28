# Emergence Mechanisms (涌現機制)

> 讓 Self-Evolving Agent 從「會做」進化到「會教自己怎麼做」

## 概述

涌現（Emergence）不是「突然變聰明」，而是系統透過回饋迴路長出偏好：
- 哪種技能 + 哪種策略 + 哪種任務類型 → 成功率更高

本文檔描述三個關鍵機制，讓系統真正能夠自我進化。

## 機制 A: 多階技能路由

### 從關鍵字匹配升級到可控多階路由

```
┌─────────────────────────────────────────────────────────────────┐
│  Multi-Stage Skill Routing                                       │
│                                                                 │
│  輸入: 「分析財報並生成投資報告 PPT」                           │
│                                                                 │
│  第一層: 粗分類 (Domain Classification)                          │
│  ├─ Domain Skills (Business, Finance, Creative...)             │
│  ├─ Software Skills (code, tools, frameworks...)               │
│  └─ Workflow Skills (processes, pipelines...)                  │
│           ↓                                                     │
│  第二層: Top-K 候選 (Candidate Selection)                        │
│  候選 1: finance/investment-analysis (score: 0.92)             │
│  候選 2: business/product-management (score: 0.65)             │
│  候選 3: creative/storytelling (score: 0.58)                   │
│           ↓                                                     │
│  第三層: 組合策略 (Composition Strategy)                         │
│  ├─ 單技能解: 只用最高分的 skill                               │
│  ├─ 管線組合: skill_a → skill_b → skill_c                      │
│  └─ 並行組合: skill_a + skill_b 同時應用                       │
│                                                                 │
│  規則:                                                          │
│  • 預設只載入 1 個技能                                         │
│  • 偵測到卡住（連續失敗/缺能力）才擴展到 2~3 個                │
│  • 技能庫越大越需要精準路由，避免混亂                          │
└─────────────────────────────────────────────────────────────────┘
```

### 路由決策邏輯

```python
def multi_stage_routing(task_description):
    # Stage 1: 粗分類
    domain = classify_domain(task_description)
    # 返回: "finance", "creative", "software", etc.

    # Stage 2: Top-K 候選
    candidates = get_top_k_skills(
        query=task_description,
        domain=domain,
        k=3
    )

    # Stage 3: 組合策略選擇
    if task_is_simple(task_description):
        # 單技能解
        return [candidates[0]]

    elif task_is_pipeline(task_description):
        # 管線組合：分析 → 報告 → 呈現
        return compose_pipeline(candidates)

    else:
        # 預設：從最高分開始，卡住再擴展
        return [candidates[0]], fallback=candidates[1:]
```

### 卡住偵測與擴展

```markdown
## 卡住信號

| 信號 | 定義 | 行動 |
|------|------|------|
| 連續失敗 | 同一任務連續 2 次失敗 | 擴展到候選 #2 |
| 能力缺口 | 評估發現缺少關鍵能力 | 載入補充 skill |
| 策略耗盡 | 策略池中所有策略都試過 | 搜尋新 skill |
| 超時 | 迭代超過上限仍未完成 | 詢問用戶或載入更多 skill |

## 擴展規則

1. 第一次卡住 → 載入候選 #2
2. 第二次卡住 → 載入候選 #3
3. 仍然卡住 → 搜尋新 skill 或詢問用戶
4. 成功後 → 記錄有效組合到 skill-metrics
```

## 機制 B: 技能效果記分板

### Skill Metrics 結構

在 `.claude/memory/skill-metrics/` 建立效果追蹤：

```
.claude/memory/skill-metrics/
├── index.md                    # 總覽和排行榜
├── by-task-type/               # 按任務類型
│   ├── code-refactoring.md
│   ├── data-analysis.md
│   └── report-generation.md
├── by-skill/                   # 按技能
│   ├── investment-analysis.md
│   └── storytelling.md
└── combinations/               # 技能組合效果
    └── analysis-to-report.md
```

### 記錄格式

```yaml
# .claude/memory/skill-metrics/by-task-type/financial-analysis.yaml

task_type: "財務分析"
total_attempts: 45
success_rate: 82%
last_updated: 2026-01-07

skill_performance:
  - skill: "finance/investment-analysis"
    attempts: 30
    success_rate: 90%
    avg_iterations: 2.1
    avg_time_minutes: 15
    failure_types:
      knowledge_gap: 2
      execution_error: 1

  - skill: "business/product-management"
    attempts: 10
    success_rate: 60%
    avg_iterations: 3.5
    avg_time_minutes: 25
    note: "適合產品財務，不適合純投資分析"

strategy_performance:
  - strategy: "DCF估值優先"
    success_rate: 95%
    best_with: ["finance/investment-analysis"]

  - strategy: "比較分析優先"
    success_rate: 75%
    note: "需要可比公司數據"

recommended_combination:
  primary: "finance/investment-analysis"
  support: ["research-analysis"]
  pipeline: "分析 → 整理 → 報告"
```

### 動態路由規則

```python
def smart_skill_routing(task):
    # 1. 分類任務類型
    task_type = classify_task(task.description)

    # 2. 查詢歷史效果
    metrics = load_metrics(f"by-task-type/{task_type}.yaml")

    if metrics and metrics.total_attempts > 10:
        # 有足夠歷史數據，使用推薦組合
        return metrics.recommended_combination

    else:
        # 數據不足，使用預設路由
        return default_routing(task)


def update_metrics(task, result):
    """任務完成後更新記分板"""
    metrics_file = f"by-task-type/{task.type}.yaml"
    metrics = load_metrics(metrics_file)

    metrics.total_attempts += 1
    if result.success:
        metrics.success_count += 1

    # 更新技能效果
    for skill in result.skills_used:
        skill_stats = metrics.skill_performance.get(skill, default_stats())
        skill_stats.attempts += 1
        skill_stats.success_rate = calculate_rate(skill_stats)

    # 更新策略效果
    strategy_stats = metrics.strategy_performance.get(result.strategy)
    strategy_stats.attempts += 1
    strategy_stats.success_rate = calculate_rate(strategy_stats)

    # 如果成功，考慮更新推薦組合
    if result.success and is_better_combination(result, metrics):
        metrics.recommended_combination = result.combination

    save_metrics(metrics_file, metrics)
```

### 效果排行榜

```markdown
# .claude/memory/skill-metrics/index.md

# 技能效果排行榜

> 自動更新，根據實際使用效果排序

## 最有效的技能組合 (Top 10)

| 排名 | 任務類型 | 技能組合 | 成功率 | 樣本數 |
|------|----------|----------|--------|--------|
| 1 | 財務分析 | investment-analysis | 90% | 30 |
| 2 | UI 設計 | ui-ux-design | 88% | 25 |
| 3 | 報告生成 | research + storytelling | 85% | 20 |
| 4 | 市場調研 | research-analysis | 82% | 18 |
| 5 | 產品規劃 | product-management | 80% | 15 |

## 需要改進的領域

| 任務類型 | 當前成功率 | 主要失敗原因 | 建議 |
|----------|------------|--------------|------|
| 複雜重構 | 55% | 策略錯誤 | 嘗試漸進式策略 |
| 跨領域整合 | 60% | 技能組合不當 | 建立管線模板 |

## 最近趨勢

- 本週成功率: 78% (↑ 5%)
- 平均迭代次數: 2.4 (↓ 0.3)
- 新學習記錄: 12 條
```

## 機制 C: 知識蒸餾

### 從經驗到可重用技能

```
┌─────────────────────────────────────────────────────────────────┐
│  Knowledge Distillation Pipeline                                 │
│                                                                 │
│  成功經驗 (memory/learnings/)                                   │
│         ↓                                                       │
│  模式識別 (多次成功的共同點)                                    │
│         ↓                                                       │
│  蒸餾為:                                                        │
│  ├─ 新的 SKILL.md (小而深)                                     │
│  │   例: "comfyui-game-assets" skill                           │
│  │                                                              │
│  ├─ 既有 skill 的增補                                          │
│  │   - Examples 區塊                                           │
│  │   - Pitfalls 區塊                                           │
│  │   - Checklist 區塊                                          │
│  │                                                              │
│  └─ 策略池更新                                                  │
│      - 新策略加入                                               │
│      - 成功率數據                                               │
│                                                                 │
│  發版和同步:                                                    │
│  • skillpkg 版本管理                                           │
│  • 依賴解決                                                     │
│  • 跨專案同步                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 自動蒸餾觸發條件

```markdown
## 觸發蒸餾的條件

### 新 Skill 創建
當以下條件滿足時，建議創建新 skill：
- 同一任務類型成功 5+ 次
- 形成了可複用的模式
- 現有 skill 都不完全匹配

### 既有 Skill 增補
當以下條件滿足時，增補現有 skill：
- 發現新的 pitfall（已記錄 3+ 次）
- 發現更好的方法（成功率顯著提升）
- 有具體的範例值得記錄

### 策略池更新
當以下條件滿足時，更新策略池：
- 新策略成功 3+ 次
- 現有策略成功率下降
- 發現策略適用條件需要調整
```

### 蒸餾模板

```markdown
# 知識蒸餾記錄

## 來源
- 學習記錄: learnings/2026-01-07-comfyui-rembg.md
- 學習記錄: learnings/2026-01-05-comfyui-batch.md
- 失敗記錄: failures/2026-01-04-vram-issue.md

## 模式識別
成功的共同點：
1. 使用 RemBG 節點處理透明背景
2. 每 5 張圖重啟避免記憶體問題
3. 輸出格式統一使用 PNG

## 蒸餾結果

### 新 Skill: comfyui-game-assets
```yaml
name: comfyui-game-assets
version: 1.0.0
description: 使用 ComfyUI 生成遊戲素材的最佳實踐
triggers: [comfyui, game-assets, 遊戲素材, 道具圖, 透明背景]
```

### 核心內容
- 工作流程模板
- 節點配置建議
- 常見問題解決方案
- 效能優化技巧

## 版本發布
- [ ] 創建 SKILL.md
- [ ] 測試驗證
- [ ] skillpkg 發版
- [ ] 同步到全域
```

## 預期涌現能力

基於這三個機制，系統最容易自然長出的能力：

### 1. 跨領域任務管線
```
投資分析 (domain skill)
    ↓
寫報告 (creative/storytelling)
    ↓
落地成腳本/表格 (software skill)
```

### 2. 自動補洞
```
做一半發現缺知識
    ↓
自動搜尋 skill
    ↓
安裝並驗證
    ↓
繼續任務
```

### 3. 越做越不重複犯同樣錯
```
強制檢查點 + 變更後測試 + milestone 確認
    ↓
行為穩定
    ↓
「突然成熟」的感覺
```

---

## 機制 D: 提示詞層級涌現設計

### 涌現觸發的提示詞框架

提示詞的設計直接影響涌現發生的機率。以下是經過設計的提示詞範本：

### 涌現等級與對應提示詞

```markdown
┌─────────────────────────────────────────────────────────────────┐
│  涌現等級 (Emergence Levels)                                    │
│                                                                 │
│  Level 0: 基礎執行                                              │
│  提示詞：「完成 X 任務」                                        │
│  行為：嚴格執行指定任務，不主動探索                             │
│                                                                 │
│  Level 1: 探索模式                                              │
│  提示詞：「改進這個專案，完成後如果有想法可以探索」             │
│  行為：完成主任務後，主動探索相關改進                           │
│                                                                 │
│  Level 2: 涌現模式                                              │
│  提示詞：「讓這個生態系變得更好，尋找跨領域連結」               │
│  行為：主動尋找 skill 之間的連結，嘗試組合創新                  │
│                                                                 │
│  Level 3: 自主模式                                              │
│  提示詞：「自主進化，追求系統性創新，發現我沒想到的可能性」     │
│  行為：完全自主，追求非預期的創新發現                           │
└─────────────────────────────────────────────────────────────────┘
```

### 涌現觸發關鍵詞

特定詞彙會提高涌現發生的機率：

| 關鍵詞類型 | 範例 | 觸發行為 |
|------------|------|----------|
| 開放性 | 「更好」「改進」「優化」 | 允許自主判斷方向 |
| 探索性 | 「探索」「發現」「嘗試」 | 鼓勵多方向探索 |
| 連結性 | 「整合」「連結」「組合」 | 促進跨領域連結 |
| 自主性 | 「自主」「自動」「智能」 | 提高自主決策權 |
| 創新性 | 「創新」「突破」「非預期」 | 鼓勵非常規思路 |

### 範本提示詞集

#### 範本 A: 標準改進 (Level 1)

```
使用 /evolve skill，針對以下專案進行系統性改進：

專案：
- {project_1}
- {project_2}
- {project_3}

目標：
1. 提升可用性和一致性
2. 增強文檔完整度
3. 優化使用者體驗

指導原則：
- 每次改進後驗證有效性
- 記錄學習和發現
- 完成主任務後可探索相關改進

--max-iterations 10
--completion-promise done
```

#### 範本 B: 跨領域探索 (Level 2)

```
使用 /evolve skill，讓這個生態系統變得更智能：

專案範圍：
- {project_1} - {description_1}
- {project_2} - {description_2}
- {project_3} - {description_3}

期望行為：
1. 尋找專案之間的協同可能性
2. 發現 skill 之間可以組合的機會
3. 提出非顯而易見的改進方向
4. 記錄意外發現到 .claude/memory/discoveries/

開放性指導：
- 如果發現有趣的連結，值得追蹤
- 允許調整優先序基於發現
- 鼓勵「如果...會怎樣」的思考

--explore --emergence
--max-iterations 15
--completion-promise done
```

#### 範本 C: 最大涌現 (Level 3)

```
使用 /evolve skill，自主進化這個生態系統：

專案範圍：
{列出所有相關專案}

核心問題：
「如何讓這個系統真正地自我進化，而不只是執行指令？」

自主權限：
✅ 可以自主決定改進方向
✅ 可以探索非預期的連結
✅ 可以提出我沒想到的改進
✅ 可以調整計劃基於發現
✅ 可以將發現轉化為新能力

約束：
❌ 不破壞現有功能
❌ 不刪除重要內容
❌ 保持向後相容

涌現目標：
- 讓系統長出「偏好」- 哪種做法更有效
- 讓系統累積「經驗」- 可重用的模式
- 讓系統產生「直覺」- 快速判斷方向

記錄格式：
- 每次發現寫入 .claude/memory/discoveries/
- 標記 confidence 和 type
- 追蹤後續驗證狀態

--autonomous --emergence --explore
--max-iterations 20
--completion-promise done
```

### 涌現反饋迴路

```
┌─────────────────────────────────────────────────────────────────┐
│  Emergence Feedback Loop                                         │
│                                                                 │
│  提示詞輸入                                                      │
│       ↓                                                         │
│  涌現等級判定 ←─────────────────────────┐                       │
│       ↓                                 │                       │
│  執行任務                               │                       │
│       ↓                                 │                       │
│  Checkpoint 4: 涌現機會檢查             │                       │
│       ↓                                 │                       │
│  發現記錄 ──→ 累積經驗                  │                       │
│       ↓           ↓                     │                       │
│  模式識別 ←─── 效果追蹤                 │                       │
│       ↓                                 │                       │
│  自動調整涌現等級 ──────────────────────┘                       │
│       ↓                                                         │
│  下一次迭代                                                      │
└─────────────────────────────────────────────────────────────────┘
```

### 涌現指標追蹤

在 `.claude/memory/emergence-metrics.yaml` 追蹤涌現效果：

```yaml
# .claude/memory/emergence-metrics.yaml

emergence_stats:
  total_sessions: 50
  discoveries_recorded: 23
  patterns_identified: 8
  skills_created_from_emergence: 3

by_level:
  level_0:
    sessions: 20
    discoveries: 2
    emergence_rate: 10%
  level_1:
    sessions: 15
    discoveries: 7
    emergence_rate: 47%
  level_2:
    sessions: 10
    discoveries: 9
    emergence_rate: 90%
  level_3:
    sessions: 5
    discoveries: 5
    emergence_rate: 100%

most_valuable_discoveries:
  - discovery: "marketing + game-design = gamification patterns"
    date: 2026-01-05
    led_to: "new skill: gamification"
  - discovery: "memory patterns applicable across all skills"
    date: 2026-01-03
    led_to: "standardized memory format"

recommended_settings:
  default_level: 1
  for_exploration: 2
  for_innovation: 3
  note: "Level 2+ 需要較多迭代次數才能發揮效果"
```

---

## 實施路線圖

### Phase 1: 基礎設施 (當前)
- [x] Memory 系統
- [x] 策略池機制
- [x] 失敗診斷分類
- [ ] skill-metrics 目錄結構

### Phase 2: 多階路由
- [ ] 粗分類器
- [ ] Top-K 候選選擇
- [ ] 卡住偵測邏輯
- [ ] 動態擴展機制

### Phase 3: 效果記分板
- [ ] 記錄格式定義
- [ ] 自動更新機制
- [ ] 排行榜生成
- [ ] 智能路由集成

### Phase 4: 知識蒸餾
- [ ] 觸發條件偵測
- [ ] 蒸餾模板
- [ ] skillpkg 集成
- [ ] 跨專案同步

## 相關文檔

- [進階技巧](../examples/advanced-techniques.md)
- [記憶管理](../examples/memory-management.md)
- [整合模式](../examples/integration-patterns.md)
