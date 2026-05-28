---
name: skill-marketplace
description: "從技能平台搜尋、瀏覽、安裝 Claude Code 技能。支援中文搜尋、技能詳情諮詢、一鍵安裝到全域目錄。"
---

# 技能市集

從線上平台搜尋並安裝 Claude Code 技能到全域目錄。

## 何時使用此技能

當使用者明確要**從網路平台搜尋新技能**時使用：

- 「幫我**從平台找** XX 的 skill」
- 「**網路上有沒有** XX 技能」
- 「**下載/安裝**一個 XX 技能」
- 「去 **AgentSkillsIndex** 找 XX」

**不要使用此技能的情況：**
- 使用者說「用 XX skill」→ 直接調用本地技能
- 使用者說「有沒有 XX skill」→ 先查本地 `~/.claude/skills/`
- 使用者想執行已安裝的技能 → 用 Skill 工具調用

## 流程

### 階段 1：翻譯與確認關鍵字

1. 接收使用者的中文需求描述
2. 翻譯成 2-3 個英文搜尋關鍵字
3. 詢問使用者確認：

「我打算用這些關鍵字搜尋：
- {keyword1}
- {keyword2}
- {keyword3}

可以嗎？或要調整/補充？」

### 階段 2：搜尋平台

對每個關鍵字執行：

```
WebFetch("https://agentskillsindex.com/en?q={keyword}")
prompt: "從搜尋結果提取技能列表，包含：名稱、描述、來源倉庫、詳情頁 URL"
```

整理結果並顯示：

| # | 技能名稱 | 描述 | 來源 |
|---|---------|------|------|
| 1 | skill-name | 簡短描述... | owner/repo |

> 註：不顯示星數，因為平台顯示的是整個倉庫的星數，非單一技能的熱門度。

詢問：「想了解哪個技能的詳情？或直接安裝？」

### 階段 3：互動諮詢（可選）

當使用者詢問技能詳情時：

1. **「這個在幹嘛？」** - 取得技能詳情
   - WebFetch 詳情頁 URL
   - 提取 skillMdRaw 或完整描述
   - 翻譯成繁體中文說明

2. **「適合 XX 情境嗎？」** - 情境分析
   - 根據技能內容分析適用性
   - 給出建議和理由

範例回應：
「**Strategy Canvas** 是用來做商業策略規劃的工具，主要功能包含：
- SWOT 分析框架
- 競爭對手分析
- 年度目標設定

適合用於：年度規劃、策略檢討、創業計劃書」

### 階段 4：確認安裝

當使用者選擇安裝時：

「確定要安裝 **{skill-name}** 到 `~/.claude/skills/` 嗎？」

### 階段 5：下載與安裝

1. **取得原始 Markdown**
   - WebFetch 詳情頁
   - 提取 skillMdRaw 欄位（原始 Markdown 內容）

2. **翻譯成繁體中文**
   - 保留 YAML frontmatter 格式
   - 翻譯所有說明文字
   - 保留程式碼區塊不翻譯

3. **寫入檔案**
   ```
   Write 工具
   路徑：~/.claude/skills/{skill-name}/SKILL.md
   內容：翻譯後的 Markdown
   ```

4. **回報結果**
   「✅ 已安裝 **{skill-name}**！

   使用方式：`/{skill-name}`
   檔案位置：`~/.claude/skills/{skill-name}/SKILL.md`」

### 階段 6：更新索引

1. **更新 README.md**
   - 讀取 `~/.claude/skills/README.md`
   - 在適當分類表格中新增該技能
   - 格式：`| **{skill-name}** | {description} |`

2. **更新技能索引**
   - 執行 `/hi-update-skills-index`
   - 確保 Claude 能識別新技能

3. **完成通知**
   「索引已更新！新技能已可使用。」

## 支援平台

| 平台 | 狀態 | 說明 |
|------|------|------|
| AgentSkillsIndex | ✅ 可用 | 44,000+ 技能 |
| SkillsMP | 🔮 未來 | 目前有防爬限制 |

## 擴充新平台

如需支援新平台，需提供：
1. 搜尋 URL 格式
2. 結果頁面解析方式
3. 詳情頁 Markdown 取得方式
