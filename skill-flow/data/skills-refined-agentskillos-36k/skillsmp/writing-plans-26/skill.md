---
name: writing-plans
description: 當你有規格或需求用於多步驟任務，在接觸程式碼之前使用
---

# 編寫計劃

## 概述

編寫全面的實作計劃，假設工程師對我們的程式碼庫沒有上下文且品味可疑。記錄他們需要知道的一切：每個任務要接觸哪些檔案、程式碼、測試、他們可能需要檢查的文件、如何測試。給他們整個計劃作為小任務。DRY。YAGNI。TDD。頻繁提交。

假設他們是熟練的開發者，但對我們的工具集或問題領域幾乎一無所知。假設他們不太了解好的測試設計。

**開始時宣布：** "我正在使用 writing-plans 技能來建立實作計劃。"

**上下文：** 這應該在專用工作樹中執行（由 brainstorming 技能建立）。

**將計劃儲存到：** `docs/plans/YYYY-MM-DD-<feature-name>.md`

## 小任務粒度

**每個步驟是一個動作（2-5 分鐘）：**
- "寫失敗的測試" - 步驟
- "執行它以確保它失敗" - 步驟
- "實作最少程式碼讓測試通過" - 步驟
- "執行測試並確保它們通過" - 步驟
- "提交" - 步驟

## 計劃文件標題

**每個計劃必須以此標題開始：**

```markdown
# [功能名稱] 實作計劃

> **給 Claude：** 必要子技能：使用 hi-skills:executing-plans 逐任務實作此計劃。

**目標：** [一句話描述這建置什麼]

**架構：** [2-3 句關於方法]

**技術棧：** [關鍵技術/程式庫]

---
```

## 風險評估

為每個任務標註風險等級：

| 等級 | 符號 | 定義 | 範例 |
|------|------|------|------|
| 🟢 Low | 純新增、不影響既有行為 | 新增獨立元件、新增測試檔案 |
| 🟡 Medium | 修改現有邏輯、需測試驗證 | 重構函數、修改 API 回傳格式 |
| 🔴 High | 涉及安全、資料、權限、破壞性變更 | 修改認證邏輯、變更資料庫 schema、刪除功能 |

## 任務結構

```markdown
### 任務 N：[組件名稱] 🟢/🟡/🔴

**檔案：**
- 建立：`exact/path/to/file.py`
- 修改：`exact/path/to/existing.py:123-145`
- 測試：`tests/exact/path/to/test.py`

**步驟 1：寫失敗的測試**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**步驟 2：執行測試驗證它失敗**

執行：`pytest tests/path/test.py::test_name -v`
預期：FAIL 帶有 "function not defined"

**步驟 3：寫最少實作**

```python
def function(input):
    return expected
```

**步驟 4：執行測試驗證它通過**

執行：`pytest tests/path/test.py::test_name -v`
預期：PASS

**步驟 5：提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## 記住
- 始終確切的檔案路徑
- 計劃中的完整程式碼（不是"添加驗證"）
- 確切的命令帶預期輸出
- 用 @ 語法引用相關技能
- DRY、YAGNI、TDD、頻繁提交

## 計劃提交

**計劃儲存後，立即進行 git 提交：**

```bash
git add docs/plans/YYYY-MM-DD-<feature-name>.md
git commit -m "docs: add implementation plan for <feature-name>"
```

這確保計劃文件被版本控制追蹤，方便團隊審查和歷史追溯。

## 執行交接

儲存計劃後，先完成 git 提交，再提供執行選擇：

**"計劃完成並儲存到 `docs/plans/<filename>.md`。執行選項：**

| 選項 | 速度 | 控制 | 說明 |
|-----|------|------|------|
| **A. 步步審查** | 最慢 | 最高 | 每個任務完成後確認 |
| **B. 階段審查** | 中 | 中 | 每個階段完成後確認 |
| **C. 全程執行** | 最快 | 低 | 全部完成後才審查 |
| **D. 獨立會話** | 最快 | 低 | 開新會話執行 |

**選擇哪個方法？"**

**如果選擇 A/B/C（此會話執行）：**
- **必要子技能：** 使用 hi-skills:executing-plans
- 留在此會話，保留對話上下文
- A: 每個任務後暫停確認
- B: 每個階段後暫停確認
- C: 全部完成後才報告

**如果選擇 D（獨立會話）：**
- 引導使用者開新會話
- 執行指令：`/hi-ace 執行 <plan-file>.md`
- **必要子技能：** 新會話使用 hi-skills:executing-plans

## 變更摘要（計劃結尾必填）

每個計劃必須以此結尾：

```markdown
---

## 變更摘要

**影響檔案：**
- `src/auth/middleware.ts` - 修改
- `src/models/user.ts` - 修改
- `src/services/avatar.ts` - 新增
- `tests/auth.test.ts` - 修改

**整體風險：** 🟢/🟡/🔴

**回滾策略：**
1. `git revert <commit-hash>` 還原所有變更
2. [若有資料庫變更] 執行 rollback 指令
3. [若有快取] 清除相關快取

**驗收條件：**
- [ ] 所有測試通過
- [ ] 手動測試核心流程
- [ ] 無 console 錯誤
```
