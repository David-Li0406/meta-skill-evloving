# Ralph Loop 提示詞範本

> 複製貼上即可使用，根據需求選擇對應的涌現等級

## 快速選擇指南

| 情境 | 推薦範本 | 涌現等級 |
|------|----------|----------|
| 日常任務、明確目標 | 範本 A | Level 0-1 |
| 專案改進、品質提升 | 範本 B | Level 1 |
| 跨專案優化、生態系整合 | 範本 C | Level 2 |
| 探索創新、自主進化 | 範本 D | Level 3 |

---

## 範本 A: 精確執行 (Level 0)

適用：有明確目標、不需要探索的任務

```
/evolve [具體任務描述]

--max-iterations 5
--completion-promise done
```

範例：
```
/evolve 修復 README.md 中的錯字和格式問題

--max-iterations 3
--completion-promise done
```

---

## 範本 B: 標準改進 (Level 1)

適用：專案改進、品質提升

```
使用 /evolve skill，針對以下專案進行系統性改進：

專案：{專案路徑}

目標：
1. [具體目標 1]
2. [具體目標 2]
3. [具體目標 3]

指導原則：
- 每次改進後驗證有效性
- 記錄學習到 .claude/memory/learnings/
- 完成主任務後可探索相關改進

--max-iterations 10
--completion-promise done
```

範例：
```
使用 /evolve skill，針對以下專案進行系統性改進：

專案：/Users/user/Workspace/self-evolving-agent

目標：
1. 提升 SKILL.md 的可讀性和結構
2. 補充缺少的範例
3. 優化使用者體驗

指導原則：
- 每次改進後驗證有效性
- 記錄學習到 .claude/memory/learnings/
- 完成主任務後可探索相關改進

--max-iterations 10
--completion-promise done
```

---

## 範本 C: 跨領域探索 (Level 2) - 推薦

適用：多專案優化、生態系整合

```
使用 /evolve skill，讓這個生態系統變得更智能：

專案範圍：
- /Users/user/Workspace/self-evolving-agent
- /Users/user/Workspace/claude-domain-skills
- /Users/user/Workspace/claude-software-skills
- /Users/user/Workspace/claude-starter-kit

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

---

## 範本 D: 最大涌現 (Level 3)

適用：探索創新、追求系統性突破

```
使用 /evolve skill，自主進化這個生態系統：

專案範圍：
- /Users/user/Workspace/self-evolving-agent - /evolve 核心技能
- /Users/user/Workspace/claude-domain-skills - 領域知識技能
- /Users/user/Workspace/claude-software-skills - 軟體工程技能
- /Users/user/Workspace/claude-starter-kit - CLI 腳手架工具

核心問題：
「如何讓這個系統真正地自我進化，而不只是執行指令？」

自主權限：
- 可以自主決定改進方向
- 可以探索非預期的連結
- 可以提出我沒想到的改進
- 可以調整計劃基於發現
- 可以將發現轉化為新能力

約束：
- 不破壞現有功能
- 不刪除重要內容
- 保持向後相容

涌現目標：
- 讓系統長出「偏好」- 哪種做法更有效
- 讓系統累積「經驗」- 可重用的模式
- 讓系統產生「直覺」- 快速判斷方向

記錄要求：
- 每次發現寫入 .claude/memory/discoveries/
- 標記 confidence (high/medium/low) 和 type (connection/pattern/insight/hypothesis)
- 追蹤後續驗證狀態

--autonomous --emergence --explore
--max-iterations 20
--completion-promise done
```

---

## 進階用法

### 指定涌現等級的 Flags

```bash
# 探索模式 - 允許自主選擇方向
--explore

# 涌現模式 - 啟用跨領域連結探索
--emergence

# 自主模式 - 完全自主，追求系統性創新
--autonomous

# 組合使用（推薦）
--explore --emergence --max-iterations 15
```

### 涌現觸發關鍵詞

在提示詞中加入以下詞彙可以提高涌現機率：

| 類型 | 關鍵詞 | 效果 |
|------|--------|------|
| 開放性 | 更好、改進、優化 | 允許自主判斷 |
| 探索性 | 探索、發現、嘗試 | 鼓勵多方向探索 |
| 連結性 | 整合、連結、組合 | 促進跨域連結 |
| 自主性 | 自主、自動、智能 | 提高決策權 |
| 創新性 | 創新、突破、非預期 | 鼓勵非常規思路 |

### 特定情境範本

#### 修復 Bug
```
/evolve 修復 [bug 描述]

診斷後記錄失敗原因到 .claude/memory/failures/

--max-iterations 5
--completion-promise done
```

#### 新功能開發
```
使用 /evolve skill，實現以下功能：

功能：[功能描述]

需求：
1. [需求 1]
2. [需求 2]

驗收標準：
- [標準 1]
- [標準 2]

--max-iterations 10
--completion-promise done
```

#### 重構優化
```
使用 /evolve skill，重構以下程式碼：

目標檔案：[檔案路徑]

重構目標：
1. 提升可讀性
2. 減少重複程式碼
3. 改善效能

約束：
- 保持 API 相容性
- 測試必須通過

--max-iterations 8
--completion-promise done
```

---

## 相關文檔

- [SKILL.md - 涌現觸發條件](../SKILL.md#涌現觸發條件-emergence-triggers)
- [EMERGENCE.md - 涌現機制設計](EMERGENCE.md)
- [涌現指標](../.claude/memory/emergence-metrics.yaml)
