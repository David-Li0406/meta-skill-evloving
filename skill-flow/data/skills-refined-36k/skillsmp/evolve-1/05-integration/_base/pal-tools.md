# PAL 工具整合

> 使用 PAL MCP 進行多模型協作和深度分析

## PAL 工具概覽

| 工具 | 用途 | 使用場景 |
|------|------|----------|
| `chat` | 一般對話 | 腦力激盪、第二意見 |
| `thinkdeep` | 深度分析 | 複雜問題、架構決策 |
| `debug` | 系統性除錯 | 難以定位的 bug |
| `codereview` | 程式碼審查 | PR 審查、品質檢查 |
| `consensus` | 多模型共識 | 重要決策 |
| `analyze` | 程式碼分析 | 架構理解、效能分析 |

## 使用範例

### 深度思考 (thinkdeep)

```python
mcp__pal__thinkdeep({
    "step": "分析這個系統的架構瓶頸",
    "step_number": 1,
    "total_steps": 3,
    "next_step_required": True,
    "findings": "初步觀察...",
    "model": "gemini-2.5-pro",
    "relevant_files": ["/path/to/file.py"]
})
```

### 多模型共識 (consensus)

```python
mcp__pal__consensus({
    "step": "評估是否應該採用微服務架構",
    "step_number": 1,
    "total_steps": 4,
    "next_step_required": True,
    "findings": "目前架構分析...",
    "models": [
        {"model": "gemini-2.5-pro", "stance": "for"},
        {"model": "gpt-5.2", "stance": "against"}
    ]
})
```

### 系統性除錯 (debug)

```python
mcp__pal__debug({
    "step": "調查記憶體洩漏問題",
    "step_number": 1,
    "total_steps": 3,
    "next_step_required": True,
    "findings": "症狀描述...",
    "hypothesis": "可能是未釋放的事件監聽器",
    "model": "gemini-2.5-pro",
    "relevant_files": ["/path/to/suspect.ts"]
})
```

## 整合到 PDCA

### Plan 階段

使用 `thinkdeep` 或 `consensus` 協助規劃：

```
目標複雜度高 → thinkdeep 分析可行性
有多個方案 → consensus 建立共識
```

### Check 階段

使用 `codereview` 進行品質檢查：

```
程式碼變更後 → codereview 審查
發現問題 → debug 深入調查
```

## 模型選擇建議

| 任務類型 | 推薦模型 |
|----------|----------|
| 複雜推理 | gemini-2.5-pro, gpt-5.2 |
| 程式碼生成 | gpt-5.1-codex |
| 快速回應 | gemini-2.5-flash |
| 創意任務 | claude-opus-4 |

## 注意事項

1. **成本考量**: 多模型共識會消耗較多 token
2. **延遲**: thinkdeep 可能需要較長時間
3. **適度使用**: 不是每個任務都需要多模型
