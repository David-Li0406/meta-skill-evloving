# Skill 整合（Plugin 方式）

> 使用 Claude Code Plugin 系統搜尋、安裝、載入 skills

## 「Skill 庫」優先搜尋

**重要：搜尋 skill 時必須優先檢查以下兩個 repo：**

| 優先順序 | Repo | 連結 |
|---------|------|------|
| 🥇 1 | claude-software-skills | https://github.com/miles990/claude-software-skills |
| 🥈 2 | claude-domain-skills | https://github.com/miles990/claude-domain-skills |

只有在這兩個 repo 都確認沒有合適的 skill 後，才詢問用戶是否透過其他管道尋找。

## 智能安裝流程

在習得新 skill 前，先檢查現有安裝狀態和版本：

```
Step 0: 檢查已安裝狀態
        Read("~/.claude/plugins/installed_plugins.json")
        Read("~/.claude/plugins/known_marketplaces.json")
               ↓
Step 1: 版本檢查（若已安裝）
        比對 installed version vs marketplace latest version
               ↓
        已安裝且最新 → 直接使用
        已安裝但過期 → /plugin update ...
        未安裝但有 marketplace → /plugin install ...
        無 marketplace → /plugin marketplace add ...
```

### 已安裝狀態檢查

```python
# 讀取已安裝 plugins
installed = Read("~/.claude/plugins/installed_plugins.json")
# 結構: { "plugins": { "name@marketplace": [{ "version": "x.y.z", ... }] } }

# 讀取已添加 marketplaces
marketplaces = Read("~/.claude/plugins/known_marketplaces.json")
# 結構: { "marketplace-name": { "source": {...}, "installLocation": "..." } }
```

### 版本檢查

```python
# 已安裝版本
installed_version = installed["plugins"]["name@marketplace"][0]["version"]

# 最新版本（從 marketplace 讀取）
marketplace_path = marketplaces["marketplace-name"]["installLocation"]
# 方式 1: 從 plugin.json 讀取
latest = Read(f"{marketplace_path}/{plugin-name}/.claude-plugin/plugin.json")
latest_version = latest["version"]

# 方式 2: 從 marketplace.json 讀取
marketplace_json = Read(f"{marketplace_path}/.claude-plugin/marketplace.json")
latest_version = next(p["version"] for p in marketplace_json["plugins"] if p["name"] == plugin_name)

# 比對
if installed_version != latest_version:
    print(f"⚠️ 有新版本可用: {installed_version} → {latest_version}")
    # /plugin update {plugin-name}
```

### 智能決策

| 狀態 | 行動 |
|------|------|
| Plugin 已安裝且最新 | 直接使用 `Skill({ skill: "..." })` |
| Plugin 已安裝但過期 | `/plugin update {name}` 後使用 |
| Marketplace 已添加但 plugin 未安裝 | `/plugin install {name}@{marketplace}` |
| Marketplace 未添加 | 先 `/plugin marketplace add ...` 再安裝 |
| 找不到適合的 skill | WebSearch 搜尋或降級執行 |

### 推薦 Marketplaces

| Marketplace | 用途 | 添加指令 |
|-------------|------|----------|
| `claude-plugins-official` | 官方工具 | 預設已添加 |
| `miles990/claude-software-skills` | 軟體開發 | `/plugin marketplace add miles990/claude-software-skills` |
| `miles990/claude-domain-skills` | 領域知識 | `/plugin marketplace add miles990/claude-domain-skills` |
| `miles990/self-evolving-agent` | 自我進化 | `/plugin marketplace add miles990/self-evolving-agent` |

## 基本操作

### 搜尋 Skill

```bash
# 在 Claude Code 中使用
/plugin
# → 選擇 Discover tab 瀏覽可用 skills

# 或使用 WebSearch 工具
WebSearch({ query: "Claude Code skill [關鍵字]" })
```

### 安裝 Skill

```bash
# 從已添加的 Marketplace 安裝
/plugin install {plugin-name}@{marketplace-name}

# 範例：安裝 software-design
/plugin install software-design@claude-software-skills

# 範例：安裝 finance（需要先添加 marketplace）
/plugin marketplace add miles990/claude-domain-skills
/plugin install finance@claude-domain-skills
```

### 載入 Skill

Skills 安裝後會自動載入。只需在對話中提及 skill 名稱，Claude 會自動識別並載入。

```bash
# 使用 Skill 工具載入
Skill({ skill: "skill-name" })
```

### 更新 Plugin

```bash
# 更新特定 plugin
/plugin update {plugin-name}

# 更新所有 marketplaces
claude plugin marketplace update
```

## 自動領域識別流程

```
用戶任務：「幫我建立一個量化交易回測系統」
                    ↓
Step 0: 🔴 優先搜尋 Skill 庫
        分析任務關鍵詞：量化、交易、回測
        → 先搜尋 miles990/claude-software-skills
        → 再搜尋 miles990/claude-domain-skills
        → 找到 finance/quant-trading ✓
                    ↓
Step 1: 檢查已安裝狀態
        Read("~/.claude/plugins/installed_plugins.json")
        → 檢查是否有 finance@claude-domain-skills
                    ↓
Step 2: 版本檢查（若已安裝）
        比對 installed.version vs marketplace latest version
        → 過期則 /plugin update finance
                    ↓
Step 3: 若未安裝，檢查 marketplace
        Read("~/.claude/plugins/known_marketplaces.json")
        → 檢查是否有 claude-domain-skills
                    ↓
Step 4: 安裝（若需要）
        /plugin marketplace add miles990/claude-domain-skills  # 若無
        /plugin install finance@claude-domain-skills
                    ↓
Step 5: 使用 Skill
        Skill({ skill: "quant-trading" })
                    ↓
Step 6: 帶著領域知識執行任務

---

用戶任務：「幫我建立區塊鏈智能合約審計工具」
                    ↓
Step 0: 🔴 優先搜尋 Skill 庫
        分析任務關鍵詞：區塊鏈、智能合約、審計
        → 搜尋 claude-software-skills... 無直接匹配
        → 搜尋 claude-domain-skills... 無直接匹配
                    ↓
Step 1: 🟡 Skill 庫未找到，詢問用戶
        「在 skill 庫中未找到『區塊鏈智能合約審計』相關的 skill，
         是否要透過其他方式尋找？」
        1. WebSearch 搜尋其他 Claude Code skill
        2. 嘗試用 security-practices skill 作為基礎
        3. 直接使用我現有的知識開始嘗試
```

## 研究模式

當整體信心度 < 50% 時，自動進入研究模式：

```
overall_confidence: 0.35 (< 0.5 閾值)
research_mode: true
research_suggestions:
  • WebSearch 搜尋 skill 或最佳實踐
  • Context7 查詢技術文檔
  • 詢問用戶澄清具體需求

→ 不盲目執行，先補充知識再繼續
```

## SKILL.md 格式

```yaml
---
name: skill-name
version: "1.0.0"
description: 技能描述
triggers: [觸發詞1, 觸發詞2]
keywords: [關鍵字1, 關鍵字2]
---

# Skill 標題

## 說明
[技能內容...]
```

## 與 evolve 整合

技能習得流程：

1. **識別缺口** - 「我無法完成 X 因為我不知道 Y」
2. **搜尋記憶** - `Grep(pattern="Y", path=".claude/memory/")`
3. **搜尋 Skill** - WebSearch 或 `/plugin` Discover tab
4. **安裝** - `/plugin install {skill}@{marketplace}`
5. **載入** - `Skill({ skill: "..." })` 或直接提及 skill 名稱
6. **驗證** - 用簡單任務測試
7. **記錄** - 寫入 .claude/memory/learnings/
