# Failure Handling Examples

> 展示 Self-Evolving Agent 如何診斷失敗並自動恢復

## 失敗類型分類

Agent 會自動將失敗分為 5 種類型，並針對性處理：

| 類型 | 症狀 | 處方 |
|------|------|------|
| **A: 知識缺口** | 不知道怎麼做 | 搜尋 skill → 安裝 → 學習 |
| **B: 執行錯誤** | 知道但做錯 | 重新檢查參數、語法 |
| **C: 環境問題** | 依賴缺失/版本問題 | 修復環境、安裝依賴 |
| **D: 策略錯誤** | 方法不適合情境 | 切換策略池其他策略 |
| **E: 資源限制** | 記憶體/API 限制 | 優化/分批/換輕量方案 |

---

## Example 1: 知識缺口自動填補

```
User: /evolve 用 ComfyUI 生成遊戲道具，要透明背景

Agent:
📋 Goal Analysis Complete

Goal: 生成透明背景遊戲道具圖片
Acceptance criteria:
- PNG 格式，透明背景
- 512x512 解析度
- 一致的美術風格

---
🔄 Attempt #1: 基本 ComfyUI 生成

Plan: 使用 KSampler + VAEDecode 生成
Do: [執行工作流程...]
Check: ❌ 失敗 - 輸出有白色背景

📝 Failure Diagnosis
Type: A - 知識缺口
→ 不知道如何生成透明背景

---
🔍 Knowledge Acquisition

Grep(pattern="透明背景", path=".claude/memory/")
→ 無相關經驗

recommend_skill({ query: "ComfyUI transparent background" })
→ Found: comfyui-rembg-workflow

install_skill({ source: "comfyui-rembg-workflow" })
→ ✅ 已安裝

load_skill({ id: "comfyui-rembg-workflow" })
→ 學到：使用 RemBG 節點移除背景

---
🔄 Attempt #2: 加入 RemBG 節點

Plan: KSampler → VAEDecode → RemBG → SaveImage(PNG)
Do: [執行更新後的工作流程...]
Check: ✅ 成功 - 透明背景 PNG

💾 Save to memory
Write(.claude/memory/learnings/2026-01-07-comfyui-transparent.md)
```

---

## Example 2: 環境問題自動修復

```
User: /evolve 執行 pytest 測試套件

Agent:
📋 Goal Analysis Complete

Goal: 執行測試套件並確保通過

---
🔄 Attempt #1: 直接執行

Plan: pytest tests/
Do: [執行測試...]
Check: ❌ 失敗

錯誤訊息：
ModuleNotFoundError: No module named 'pytest'

📝 Failure Diagnosis
Type: C - 環境問題
→ pytest 未安裝

---
🔧 Environment Fix

Bash: pip install pytest
→ ✅ 安裝成功

---
🔄 Attempt #2: 重新執行

Do: [執行 pytest tests/...]
Check: ❌ 失敗

錯誤訊息：
ImportError: No module named 'requests'

📝 Failure Diagnosis
Type: C - 環境問題（連鎖依賴）
→ 測試需要 requests 套件

---
🔧 Environment Fix

Bash: pip install -r requirements.txt
→ ✅ 所有依賴安裝成功

---
🔄 Attempt #3: 重新執行

Do: [執行 pytest tests/...]
Check: ✅ 成功 - 15 tests passed

💾 Save experience
Write(.claude/memory/learnings/2026-01-07-pytest-setup.md)
```

---

## Example 3: 多策略切換

```
User: /evolve 生成 10 張產品圖片

Agent:
📋 Goal Analysis Complete

Goal: 批量生成 10 張產品圖片

📂 Loading strategy pool
Read(.claude/memory/strategies/image-generation.md)

Available strategies:
- S1: Local ComfyUI (priority: 1)
- S2: Stable Diffusion API (priority: 2)
- S3: DALL-E API (priority: 3)

---
🔄 Strategy S1: Local ComfyUI

Plan: 使用本地 ComfyUI 批量生成
Do: [生成第 1-3 張成功...]
Check: ❌ 失敗 - 第 4 張時 GPU 記憶體耗盡

📝 Failure Diagnosis
Type: E - 資源限制
→ GPU VRAM 不足

Strategy S1 marked as: failed
do_not_retry_until: "GPU 記憶體問題解決"

---
🔄 Strategy S2: Stable Diffusion API

Plan: 改用 SD API 雲端生成
Do: [API 呼叫生成 10 張...]
Check: ✅ 成功

💾 Update strategy stats
- S1: 成功率 30% (3/10)
- S2: 成功率 100% (10/10)

💡 Insight saved:
「批量生成時，雲端 API 比本地更穩定」
```

---

## Example 4: 執行錯誤自我修正

```
User: /evolve 建立 React component

Agent:
🔄 Attempt #1

Plan: 建立 UserCard.tsx
Do: [寫入程式碼...]

export const UserCard = ({ user }) => {
  return (
    <div className="card">
      <h2>{user.name}<h2>  // ← 錯誤：標籤未閉合
      <p>{user.email}</p>
    </div>
  );
};

Check: ❌ 失敗

錯誤訊息：
SyntaxError: Unexpected token

📝 Failure Diagnosis
Type: B - 執行錯誤
→ JSX 語法錯誤，標籤未正確閉合

---
🔄 Attempt #2: 修正語法

Do: [修正並重新寫入...]

export const UserCard = ({ user }) => {
  return (
    <div className="card">
      <h2>{user.name}</h2>  // ← 修正
      <p>{user.email}</p>
    </div>
  );
};

Check: ✅ 編譯成功
```

---

## 最大重試次數

```
┌─────────────────────────────────────────────────────────────────┐
│  停止條件                                                        │
│                                                                 │
│  ✅ 成功：目標達成，驗收標準通過                                │
│                                                                 │
│  ❌ 停止重試：                                                   │
│     • 達到最大迭代次數（預設 10 次）                            │
│     • 連續 3 次相同錯誤                                         │
│     • 所有策略都已嘗試且失敗                                    │
│     • 用戶手動中止                                              │
│                                                                 │
│  ⚠️ 暫停詢問：                                                   │
│     • 需要用戶決策                                              │
│     • 需要外部資源（API key 等）                                │
│     • 風險操作需確認                                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 失敗記憶格式

成功處理失敗後，經驗會被記錄：

```markdown
# .claude/memory/failures/2026-01-07-comfyui-vram.md

---
date: 2026-01-07
tags: [comfyui, gpu, vram, batch-generation]
task: 批量生成圖片
status: resolved
---

# ComfyUI 批量生成 VRAM 不足

## 症狀
批量生成到第 4 張圖片時 GPU 記憶體耗盡

## 根本原因
ComfyUI 未在批次間清理 VRAM

## 解決方案
1. ✅ 改用雲端 API（推薦）
2. 使用 --lowvram 參數
3. 每張圖後重啟 ComfyUI

## 驗證
使用 S2 (SD API) 策略成功生成 10 張
```

---

## Tips

1. **觀察失敗模式** - Agent 會記錄失敗，下次遇到相似問題會更快解決
2. **策略池會進化** - 成功率高的策略會被優先選擇
3. **經驗可搜尋** - 使用 `Grep` 搜尋 `.claude/memory/` 查找過去經驗
