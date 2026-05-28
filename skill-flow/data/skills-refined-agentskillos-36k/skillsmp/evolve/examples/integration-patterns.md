# Integration Patterns

> 展示如何整合 Self-Evolving Agent 與其他工具和工作流程

## 與 Domain Skills 整合

Self-Evolving Agent 可自動識別任務關鍵詞並載入對應的領域知識。

### 自動領域識別流程

```
┌─────────────────────────────────────────────────────────────────┐
│  Domain Detection Pipeline                                       │
│                                                                 │
│  用戶輸入                                                        │
│  「分析台積電財報，評估投資價值」                                │
│         ↓                                                       │
│  關鍵詞提取                                                      │
│  [財報, 分析, 投資, 估值]                                        │
│         ↓                                                       │
│  Trigger 匹配                                                    │
│  finance/investment-analysis: [財報, 投資, 估值, ROE]           │
│         ↓                                                       │
│  載入 Domain Skill                                               │
│  - DCF 估值框架                                                  │
│  - 財務比率分析                                                  │
│  - 紅旗警示清單                                                  │
│         ↓                                                       │
│  應用專業知識執行任務                                            │
└─────────────────────────────────────────────────────────────────┘
```

### 多領域組合

當任務涉及多個領域時，可同時載入多個 skills：

```markdown
## 範例：規劃新產品發布

任務：「規劃新遊戲道具的發布活動，要有行銷策略和定價」

自動識別：
- business/product-management (產品發布)
- business/marketing (行銷策略)
- creative/game-design (遊戲道具)

載入後的能力增強：
- PRD 撰寫框架
- 行銷漏斗設計
- 遊戲經濟平衡
```

## 與 PAL MCP 整合

使用 PAL MCP 可增強複雜問題的解決能力。

### 深度分析模式

```python
# 當遇到複雜問題時，調用 thinkdeep
await mcp__pal__thinkdeep({
    "step": "分析為什麼用戶流失率突然上升",
    "step_number": 1,
    "total_steps": 3,
    "next_step_required": True,
    "findings": "初步觀察：上週更新後流失率從 5% 上升到 12%",
    "hypothesis": "新版本的 onboarding 流程變更可能是主因",
    "confidence": "medium",
    "model": "gemini-2.5-pro"
})
```

### 多模型共識

```python
# 重要決策時，使用多模型驗證
await mcp__pal__consensus({
    "step": "評估是否應該將後端從 Node.js 遷移到 Go",
    "step_number": 1,
    "total_steps": 3,
    "next_step_required": True,
    "findings": "當前效能瓶頸在 API 響應時間",
    "models": [
        {"model": "gpt-5.2", "stance": "for"},
        {"model": "gemini-2.5-pro", "stance": "against"}
    ]
})
```

## 與 CI/CD 整合

### GitHub Actions 自動觸發

```yaml
# .github/workflows/evolve-check.yml
name: Evolve Quality Check

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  evolve-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Claude Code
        run: npm install -g @anthropic-ai/claude-code

      - name: Run Evolve Analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude-code "/evolve 審查這個 PR 的程式碼品質和潛在問題"
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# 讓 evolve 審查即將提交的變更
staged_files=$(git diff --cached --name-only)

if [ -n "$staged_files" ]; then
    echo "Running evolve review on staged changes..."
    claude-code "/evolve 審查以下變更的程式碼品質: $staged_files"
fi
```

## 記憶系統整合模式

### 跨專案記憶共享

```
┌─────────────────────────────────────────────────────────────────┐
│  Cross-Project Memory Architecture                               │
│                                                                 │
│  Global Memory (~/.claude/memory/)                              │
│  ├── 通用學習經驗                                               │
│  ├── 跨專案適用的模式                                           │
│  └── 個人偏好設定                                               │
│                                                                 │
│  Project Memory (.claude/memory/)                               │
│  ├── 專案特定的決策                                             │
│  ├── 專案相關的失敗經驗                                         │
│  └── 專案架構知識                                               │
│                                                                 │
│  搜尋優先順序：                                                  │
│  1. Project Memory (最相關)                                     │
│  2. Global Memory (通用知識)                                    │
└─────────────────────────────────────────────────────────────────┘
```

### 記憶同步腳本

```bash
#!/bin/bash
# sync-memory.sh - 同步重要學習到全域記憶

PROJECT_MEMORY=".claude/memory"
GLOBAL_MEMORY="$HOME/.claude/memory"

# 同步標記為 global: true 的學習
grep -l "global: true" $PROJECT_MEMORY/learnings/*.md | while read file; do
    cp "$file" "$GLOBAL_MEMORY/learnings/"
    echo "Synced: $file"
done
```

## 與 Skill Package 整合

### 自動 Skill 發現和安裝

```python
# 任務開始時自動搜尋相關 skills
async def auto_discover_skills(task_description):
    # 1. 搜尋推薦
    result = await mcp__skillpkg__recommend_skill({
        "query": task_description,
        "criteria": "popular"
    })

    # 2. 如果找到匹配的 skill，詢問是否安裝
    if result["recommendation"]:
        skill = result["recommendation"]
        print(f"發現相關 skill: {skill['name']}")
        print(f"描述: {skill['description']}")

        # 3. 安裝並載入
        await mcp__skillpkg__install_skill({
            "source": f"github:{skill['source']}"
        })
        await mcp__skillpkg__load_skill({
            "id": skill["name"]
        })
```

### Skill 鏈式調用

```markdown
## 複雜任務的 Skill 組合

任務：「開發一個投資組合追蹤 App」

Skill 調用順序：
1. finance/investment-analysis → 了解投資指標
2. business/product-management → 撰寫 PRD
3. creative/ui-ux-design → 設計介面
4. (技術實作)
5. business/marketing → 推廣策略
```

## 與外部 API 整合

### 數據來源整合

```python
# 結合外部數據執行 evolve 任務
async def evolve_with_data(goal, data_sources):
    """
    範例：分析股票時自動獲取財報數據
    """
    # 1. 獲取外部數據
    data = {}
    for source in data_sources:
        data[source.name] = await source.fetch()

    # 2. 將數據納入任務上下文
    enhanced_goal = f"""
    {goal}

    可用數據：
    {json.dumps(data, indent=2)}
    """

    # 3. 執行 evolve 流程
    return await evolve(enhanced_goal)
```

### Webhook 通知整合

```python
# 任務完成後發送通知
async def notify_completion(task_result, webhook_url):
    """
    支援 Slack, Discord, Teams 等 webhook
    """
    payload = {
        "text": f"✅ 任務完成",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*任務*: {task_result['goal']}\n*狀態*: {task_result['status']}\n*學習數*: {len(task_result['learnings'])}"
                }
            }
        ]
    }

    await http_post(webhook_url, payload)
```

## 最佳實踐

### 1. 漸進式整合

```markdown
## 整合階段

Stage 1: 基礎使用
- 直接使用 /evolve 命令
- 手動查看記憶

Stage 2: 自動化
- 設定 CI/CD 整合
- 配置 pre-commit hooks

Stage 3: 進階整合
- PAL MCP 深度分析
- 多專案記憶同步
- 自動 Skill 發現
```

### 2. 監控和日誌

```bash
# 記錄 evolve 執行歷史
# .claude/logs/evolve-history.jsonl

{"timestamp": "2026-01-07T10:30:00Z", "goal": "優化效能", "iterations": 3, "status": "success"}
{"timestamp": "2026-01-07T14:15:00Z", "goal": "修復登入bug", "iterations": 2, "status": "success"}
```

### 3. 失敗處理策略

```markdown
## 整合失敗處理

| 失敗類型 | 處理策略 |
|----------|----------|
| Skill 載入失敗 | 回退到基礎模式 |
| PAL 服務不可用 | 使用本地推理 |
| 記憶搜尋超時 | 跳過記憶，直接執行 |
| API 限流 | 延遲重試 + 通知用戶 |
```

## 相關文檔

- [基本使用](./basic-usage.md)
- [自動領域識別](./auto-domain-detection.md)
- [失敗處理](./failure-handling.md)
- [記憶管理](./memory-management.md)
