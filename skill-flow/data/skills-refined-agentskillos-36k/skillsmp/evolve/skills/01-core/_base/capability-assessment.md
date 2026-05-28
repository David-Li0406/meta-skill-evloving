# 能力評估 (Capability Assessment)

> 在執行任務前，先評估自己是否具備所需能力

## 評估流程

```
任務分析 → 能力清單 → 差距識別 → 習得/降級決策
```

## 能力維度

| 維度 | 說明 | 範例 |
|------|------|------|
| **領域知識** | 特定領域的專業知識 | 量化交易、遊戲設計、UI/UX |
| **技術能力** | 程式語言、框架、工具 | Python, ComfyUI, PostgreSQL |
| **環境需求** | 本地環境、API、硬體 | GPU, API Key, 特定版本 |

## 評估模板

```yaml
task: [任務描述]
required_capabilities:
  domain_knowledge:
    - [領域 1]
    - [領域 2]
  technical_skills:
    - [技術 1]
    - [技術 2]
  environment:
    - [環境需求 1]

self_assessment:
  have:
    - [具備的能力]
  gap:
    - [缺少的能力]

decision: acquire | delegate | simplify | abort
```

## 決策選項

| 決策 | 條件 | 行動 |
|------|------|------|
| **acquire** | 差距可透過 skill 習得填補 | 搜尋並載入相關 skill |
| **delegate** | 需要外部專家或工具 | 提示用戶尋求專業協助 |
| **simplify** | 可降低目標複雜度 | 與用戶確認簡化版本 |
| **abort** | 完全超出能力範圍 | 誠實說明限制 |

## 搜尋記憶

在評估前，先搜尋是否有相關經驗：

```python
# 搜尋過去類似任務的經驗
Grep(
    pattern="[任務關鍵字]",
    path=".claude/memory/",
    output_mode="files_with_matches"
)
```

## 習得 Skill

若有能力差距，先檢查已安裝狀態和版本再習得：

```python
# Step 1: 檢查已安裝 plugins
installed = Read("~/.claude/plugins/installed_plugins.json")
# 結構: { "plugins": { "name@marketplace": [{ "version": "x.y.z" }] } }

# Step 2: 檢查已添加 marketplaces
marketplaces = Read("~/.claude/plugins/known_marketplaces.json")
# 常用: claude-software-skills, claude-domain-skills

# Step 3: 版本檢查（若已安裝）
if skill_installed:
    installed_ver = installed["plugins"]["name@marketplace"][0]["version"]
    marketplace_path = marketplaces["marketplace"]["installLocation"]
    latest = Read(f"{marketplace_path}/{plugin}/.claude-plugin/plugin.json")
    if installed_ver != latest["version"]:
        # /plugin update {plugin}  # 更新到最新版
    Skill({ skill: "skill-name" })

# Step 4: 智能決策
elif marketplace_exists:
    # /plugin install {skill}@{marketplace}
else:
    # /plugin marketplace add miles990/{marketplace}
    # /plugin install {skill}@{marketplace}
```

### 快速參考

| 需求類型 | Marketplace | 安裝/更新指令 |
|----------|-------------|---------------|
| 軟體開發 | `claude-software-skills` | `/plugin install {category}@claude-software-skills` |
| 領域知識 | `claude-domain-skills` | `/plugin install {category}@claude-domain-skills` |
| 官方工具 | `claude-plugins-official` | `/plugin install {plugin}@claude-plugins-official` |
| 更新 | - | `/plugin update {plugin-name}` |
