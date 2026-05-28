# 涌現等級 (Emergence Levels)

> 不同等級的自主性和探索深度

## 等級定義

| Level | 名稱 | 行為 | 觸發方式 |
|-------|------|------|----------|
| 0 | 基礎 | 嚴格執行指定任務 | 預設模式 |
| 1 | 探索 | 完成後探索相關改進 | `--explore` 或連續成功 |
| 2 | 涌現 | 主動尋找跨領域連結 | `--emergence` 或發現連結 |
| 3 | 自主 | 自主發現和追求創新 | `--autonomous` |

```
Level 0          Level 1          Level 2          Level 3
基礎模式         探索模式         涌現模式         自主模式
   │                │                │                │
   ▼                ▼                ▼                ▼
執行任務    →   探索相關    →   跨域連結    →   自主創新
   │                │                │                │
   └── 逐步提升 ──→├── 信號觸發 ──→├── 累積經驗 ──→┘
```

## 自動觸發信號

當以下情況發生時，系統自動提升涌現等級：

| 信號 | 行為 | 範例 |
|------|------|------|
| 連續成功 3+ 次 | 嘗試更高難度的變體 | 「都成功了，試試更有挑戰的目標？」 |
| 發現 skill 之間的連結 | 記錄並嘗試組合 | 「marketing + game-design = 遊戲化行銷？」 |
| 完成任務後有剩餘迭代 | 探索「還能做什麼」 | 「還有 3 次迭代，探索一下？」 |
| 用戶給予開放性目標 | 主動提出多個方向 | 「讓它變得更好」→ 提出 3 個具體方向 |
| 發現可重用模式 | 提議抽象化 | 「這個模式出現 3 次了，要不要變成 skill？」 |

## 手動觸發（Flags）

```bash
# 探索模式 - 允許自主選擇方向
/evolve [目標] --explore

# 涌現模式 - 啟用跨領域連結探索
/evolve [目標] --emergence

# 自主模式 - 完全自主，追求系統性創新
/evolve [目標] --autonomous

# 組合使用
/evolve 改進專案架構 --explore --emergence --max-iterations 10
```

## 涌現觸發關鍵詞

特定詞彙會提高涌現發生的機率：

| 關鍵詞類型 | 範例 | 觸發行為 |
|------------|------|----------|
| 開放性 | 「更好」「改進」「優化」 | 允許自主判斷方向 |
| 探索性 | 「探索」「發現」「嘗試」 | 鼓勵多方向探索 |
| 連結性 | 「整合」「連結」「組合」 | 促進跨領域連結 |
| 自主性 | 「自主」「自動」「智能」 | 提高自主決策權 |
| 創新性 | 「創新」「突破」「非預期」 | 鼓勵非常規思路 |

## 涌現記錄格式

發現值得記錄的涌現時，寫入 `.claude/memory/discoveries/`：

```yaml
# .claude/memory/discoveries/YYYY-MM-DD-discovery-name.md
---
date: 2024-01-15
type: connection | pattern | insight | hypothesis
confidence: high | medium | low
related_skills: [skill-a, skill-b]
---

## 發現

[描述發現的內容]

## 觸發情境

[什麼情況下發現的]

## 潛在應用

[可能的應用方向]

## 後續行動

- [ ] 驗證假設
- [ ] 建立新 skill
- [ ] 整合到現有機制
```

## 涌現指標追蹤

在 `.claude/memory/emergence-metrics.yaml` 追蹤涌現效果：

```yaml
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

recommended_settings:
  default_level: 1
  for_exploration: 2
  for_innovation: 3
  note: "Level 2+ 需要較多迭代次數才能發揮效果"
```
