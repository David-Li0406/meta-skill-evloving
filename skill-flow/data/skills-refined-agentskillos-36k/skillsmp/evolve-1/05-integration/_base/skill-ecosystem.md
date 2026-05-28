# 智能 Skill 生態系整合

> 自動發現、推薦、組合最適合的 Skill

## 「Skill 庫」定義

**重要：當用戶提到「skill 庫」時，專指以下兩個官方 repo：**

| 優先順序 | Repo | 領域 | 連結 |
|---------|------|------|------|
| 🥇 1 | **claude-software-skills** | 軟體開發 | https://github.com/miles990/claude-software-skills |
| 🥈 2 | **claude-domain-skills** | 專業領域 | https://github.com/miles990/claude-domain-skills |

### 搜尋規則

```
┌─────────────────────────────────────────────────────────────────┐
│  Skill 搜尋優先順序（不可跳過）                                  │
│                                                                 │
│  1. 🔴 必須先搜尋 Skill 庫                                      │
│     ├─ miles990/claude-software-skills                         │
│     └─ miles990/claude-domain-skills                           │
│                                                                 │
│  2. 評估結果                                                    │
│     ├─ 找到合適 → 安裝使用                                      │
│     └─ 確認沒找到 → 步驟 3                                      │
│                                                                 │
│  3. 🟡 詢問用戶其他管道（僅在 skill 庫找不到時）                │
│     「在 skill 庫中未找到相關 skill，是否要透過其他方式尋找？」 │
│     - WebSearch 搜尋                                            │
│     - 其他 marketplace                                          │
│     - 使用現有知識嘗試                                          │
└─────────────────────────────────────────────────────────────────┘
```

> ⚠️ **禁止**：未先搜尋 skill 庫就直接使用其他管道尋找 skill

## 概覽

智能 Skill 生態系讓 AI 能夠：
1. **自動發現** - 從 GitHub repos 同步 skill 索引
2. **智能推薦** - 根據任務自動推薦相關 skill
3. **經驗共享** - 跨專案學習和分享

```
┌─────────────────────────────────────────────────────────────┐
│                    智能 Skill 生態系                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   GitHub Repos                    sqlite-memory             │
│   ┌──────────────────┐           ┌──────────────────┐      │
│   │ software-skills  │ ──sync──► │ skill:*          │      │
│   │   (54 skills)    │           │ (78 skills 索引) │      │
│   └──────────────────┘           └────────┬─────────┘      │
│   ┌──────────────────┐                    │                │
│   │  domain-skills   │ ──sync──►          │                │
│   │   (24 skills)    │                    │                │
│   └──────────────────┘                    │                │
│                                           ↓                │
│                              ┌────────────────────┐        │
│                              │   evolve CP1       │        │
│                              │   memory_search()  │        │
│                              │   → 推薦相關 skill │        │
│                              └────────────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 支援的 Skill Repos

| Repo | Skills | 領域 |
|------|--------|------|
| [claude-software-skills](https://github.com/miles990/claude-software-skills) | 54 | 軟體開發 |
| [claude-domain-skills](https://github.com/miles990/claude-domain-skills) | 24 | 專業領域 |

### Software Skills 分類

| 分類 | Skills | 範例 |
|------|--------|------|
| software-design | 6 | architecture-patterns, api-design |
| software-engineering | 8 | testing-strategies, devops-cicd |
| development-stacks | 8 | frontend, backend, database |
| tools-integrations | 8 | git-workflows, automation-scripts |
| domain-applications | 12 | e-commerce, game-development |
| programming-languages | 12 | python, typescript, rust |

### Domain Skills 分類

| 分類 | Skills | 範例 |
|------|--------|------|
| business | 5 | marketing, product-management |
| finance | 3 | quant-trading, investment-analysis |
| creative | 8 | game-design, storytelling |
| professional | 2 | research-analysis |
| lifestyle | 2 | personal-growth |
| methodology | 4 | knowledge-acquisition-4c |

## 同步 Skill 索引

### 手動同步

```bash
# 同步所有 repos
./scripts/sync-skills.sh

# 只同步 software skills
./scripts/sync-skills.sh --software

# 只同步 domain skills
./scripts/sync-skills.sh --domain

# 列出已索引的 skills
./scripts/sync-skills.sh --list

# 清除索引
./scripts/sync-skills.sh --clear
```

### 自動同步（建議）

可以設定 cron job 定期同步：

```bash
# 每天早上 9 點同步
0 9 * * * /path/to/self-evolving-agent/scripts/sync-skills.sh
```

或在 evolve 啟動時檢查：

```python
# 檢查上次同步時間，超過 7 天則自動同步
last_sync = memory_search({"query": "skill:sync:timestamp"})
if days_since(last_sync) > 7:
    run("./scripts/sync-skills.sh")
```

## 搜尋 Skill

### 使用 memory_search

```python
# 搜尋量化交易相關 skill
memory_search({
    "query": "skill:* quant trading",
    "limit": 5
})

# 搜尋遊戲開發相關 skill
memory_search({
    "query": "skill:* game design",
    "limit": 5
})

# 搜尋 Python 相關 skill
memory_search({
    "query": "skill:* python",
    "limit": 5
})
```

### 搜尋結果格式

```json
{
  "key": "skill:claude-domain-skills:finance:quant-trading",
  "content": "name: quant-trading\nrepo: github:miles990/claude-domain-skills\npath: finance/quant-trading\ncategory: finance\ntriggers: 量化, 交易, 回測",
  "tags": ["skill", "finance", "claude-domain-skills"],
  "scope": "global"
}
```

## CP1 整合

在 evolve CP1 中自動執行：

```python
# 1. 分析任務關鍵字
task = "建立量化交易系統"
keywords = extract_keywords(task)  # ["量化", "交易", "系統"]

# 2. 搜尋相關經驗
memory_search({"query": " ".join(keywords)})

# 3. 搜尋失敗經驗
failure_search({"query": " ".join(keywords)})

# 4. 搜尋相關 skill（新增）
skill_results = memory_search({
    "query": f"skill:* {' '.join(keywords)}",
    "limit": 5
})

# 5. 顯示推薦
if skill_results:
    print("🎯 發現相關 Skill:")
    for skill in skill_results:
        print(f"  - {skill['key']}")
```

## Scope 判斷

記錄經驗時自動判斷 scope：

```python
# 詳見 03-memory/_base/scope-detection.md

# 通用經驗 → global（跨專案共享）
memory_write({
    "key": "learning:2026-01-16:ts-pattern",
    "content": "TypeScript 技巧...",
    "scope": "global"
})

# 專案專屬 → project:xxx
memory_write({
    "key": "learning:2026-01-16:quant-bot-strategy",
    "content": "quant-bot 專屬交易策略...",
    "scope": "project:quant-bot"
})
```

## 未來擴展

### Phase 2: 智能組合

根據任務自動組合多個 skill：

```
任務: "建立量化交易 Web 應用"
       ↓
推薦組合:
  Primary: quant-trading + frontend
  Supporting: testing-strategies + security-practices
```

### Phase 3: 自動安裝

缺少的 skill 自動下載安裝：

```bash
# 偵測到需要但未安裝的 skill
skill install github:miles990/claude-domain-skills#finance/quant-trading
```

### Phase 4: 協作執行

多 skill 共享 context 協同工作：

```python
# skill A 設定 context
context_set(session_id, "api_schema", {...})

# skill B 讀取 context
schema = context_get(session_id, "api_schema")
```
