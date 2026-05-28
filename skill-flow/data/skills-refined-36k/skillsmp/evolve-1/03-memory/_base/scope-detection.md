# Scope 自動判斷指南

> 決定記憶應該是 `global`（跨專案共享）還是 `project:xxx`（專案專屬）

## 核心原則

**寧可多分享，不要過度隔離** — 預設使用 `global`，除非明確是專案專屬資訊。

## 判斷流程

```
                    ┌─────────────────────┐
                    │   分析記憶內容       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ↓                │                ↓
    ┌─────────────────┐        │      ┌─────────────────┐
    │ 專案專屬信號？   │        │      │ 通用經驗信號？   │
    │                 │        │      │                 │
    │ • 專案名稱提及   │        │      │ • 語言/框架技巧  │
    │ • API keys      │        │      │ • 工具使用方法   │
    │ • 特定配置      │        │      │ • 設計模式       │
    │ • 業務邏輯規則   │        │      │ • 錯誤處理經驗   │
    └────────┬────────┘        │      └────────┬────────┘
             │                 │               │
             ↓                 ↓               ↓
    scope: "project:xxx"   不確定        scope: "global"
                               │
                               ↓
                      預設: "global"
```

## 專案專屬信號（使用 project:xxx）

### 強信號（必定專案專屬）

| 信號類型 | 範例 | 說明 |
|----------|------|------|
| **敏感資訊** | API keys, 密碼, tokens | 絕不可跨專案 |
| **專案名稱** | "quant-bot 的交易策略" | 明確提及專案 |
| **特定 URL** | `api.mycompany.com/v1` | 專案特定端點 |
| **業務規則** | "用戶等級 3+ 才能..." | 專案業務邏輯 |

### 弱信號（需結合判斷）

| 信號類型 | 範例 | 處理方式 |
|----------|------|----------|
| 特定配置值 | port: 3001 | 如果通用配置 → global |
| 目錄結構 | `src/services/` | 如果是通用架構 → global |
| 依賴版本 | `"react": "18.2.0"` | 通常 → global |

## 通用經驗信號（使用 global）

### 強信號（必定跨專案共享）

| 信號類型 | 範例 | 說明 |
|----------|------|------|
| **語言技巧** | "TypeScript 的 discriminated union" | 通用技術 |
| **工具使用** | "如何配置 ESLint" | 跨專案適用 |
| **設計模式** | "Repository 模式的實作" | 通用架構 |
| **錯誤解法** | "TypeError: Cannot read property" | 常見問題 |
| **最佳實踐** | "React useEffect 的清理" | 框架知識 |

### 弱信號（通常跨專案）

| 信號類型 | 範例 | 處理方式 |
|----------|------|----------|
| 效能優化 | "減少 re-render 的方法" | 通常 → global |
| 測試方法 | "Jest mock 的使用" | 通常 → global |
| 除錯技巧 | "Chrome DevTools 技巧" | 通常 → global |

## 實作判斷邏輯

### 在 CP3.5 記錄經驗時使用

```python
def determine_scope(content: str, project_path: str) -> str:
    """
    自動判斷記憶的 scope

    Args:
        content: 記憶內容
        project_path: 當前專案路徑

    Returns:
        "global" 或 "project:{project_name}"
    """
    project_name = os.path.basename(project_path)

    # 強信號：專案專屬
    project_specific_patterns = [
        r'api[_-]?key',
        r'secret',
        r'password',
        r'token',
        rf'\b{project_name}\b',  # 專案名稱
        r'(my|our)\s+(api|endpoint|server)',
        r'https?://[^/]+\.(internal|local|company)',
    ]

    for pattern in project_specific_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return f"project:{project_name}"

    # 強信號：通用經驗
    global_patterns = [
        r'(typescript|javascript|python|rust|go)\s+(技巧|tip|pattern)',
        r'(設計模式|design pattern)',
        r'(最佳實踐|best practice)',
        r'(如何|how to)\s+(配置|setup|install)',
        r'(錯誤|error|exception|bug)\s+(解法|fix|solution)',
        r'(框架|framework|library)\s+(使用|usage)',
    ]

    for pattern in global_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return "global"

    # 預設：global（寧可多分享）
    return "global"
```

### 使用範例

```python
# 在 CP3.5 記錄經驗時
content = "學到了 TypeScript discriminated union 的用法..."
project_path = "/Users/user/Workspace/quant-bot"

scope = determine_scope(content, project_path)
# → "global"（通用 TypeScript 技巧）

# 記錄到 sqlite-memory
memory_write({
    "key": "learning:2026-01-16:ts-discriminated-union",
    "content": content,
    "scope": scope,  # "global"
    "tags": ["typescript", "pattern"]
})
```

```python
# 專案專屬範例
content = "quant-bot 的交易策略：當 RSI > 70 時賣出..."
scope = determine_scope(content, project_path)
# → "project:quant-bot"（包含專案名稱 + 業務邏輯）
```

## 搜尋時的 Scope 行為

```python
# 搜尋所有記憶（包括 global + 當前專案）
memory_search({"query": "TypeScript pattern"})
# → 返回所有 global + project:當前專案 的結果

# 只搜尋 global
memory_search({"query": "TypeScript pattern", "scope": "global"})

# 只搜尋特定專案
memory_search({"query": "交易策略", "scope": "project:quant-bot"})
```

## 特殊情況處理

### 1. 從專案經驗中提取通用知識

如果專案專屬經驗中包含可通用的知識，建議：

```python
# 原始專案經驗
memory_write({
    "key": "learning:2026-01-16:quant-bot-backtest-fix",
    "content": "修復 quant-bot 回測時的資料對齊問題...",
    "scope": "project:quant-bot"
})

# 提取通用知識另存
memory_write({
    "key": "learning:2026-01-16:backtest-data-alignment",
    "content": "回測時的資料對齊技巧：確保時間戳一致...",
    "scope": "global"  # 通用化後跨專案共享
})
```

### 2. 敏感資訊遮罩

如果內容包含敏感資訊但經驗本身有價值：

```python
# 遮罩敏感資訊後存為 global
original = "使用 API key sk-abc123 連接 OpenAI..."
sanitized = "使用 API key [REDACTED] 連接 OpenAI..."

memory_write({
    "key": "learning:2026-01-16:openai-connection",
    "content": sanitized,
    "scope": "global"
})
```

## 標籤建議

配合 scope 使用標籤增強搜尋：

| Scope | 建議標籤 | 用途 |
|-------|----------|------|
| global | `["typescript", "pattern"]` | 技術領域 |
| global | `["tool", "eslint", "config"]` | 工具類型 |
| project:xxx | `["business", "trading"]` | 業務領域 |
| project:xxx | `["config", "internal"]` | 配置類型 |

## 與 evolve 整合

在 CP3.5 自動應用此邏輯：

1. 分析要儲存的經驗內容
2. 呼叫 `determine_scope()` 判斷
3. 使用判斷結果設定 scope
4. 如果不確定，詢問用戶確認

```
[CP3.5] 記錄經驗

內容: "TypeScript discriminated union 的用法..."
自動判斷: scope = "global" (通用技術技巧)

確認儲存？ [Y/n]
```
