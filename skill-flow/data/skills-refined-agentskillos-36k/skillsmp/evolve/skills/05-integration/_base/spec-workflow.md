# spec-workflow 整合

> 使用 spec-workflow MCP 進行結構化需求到實作的轉換

## 工作流程

```
需求文件 (Requirements)
         ↓
設計文件 (Design)
         ↓
任務分解 (Tasks)
         ↓
實作執行 (Implementation)
```

## 核心工具

| 工具 | 用途 |
|------|------|
| `spec-workflow-guide` | 載入工作流程指南 |
| `spec-status` | 查看 spec 進度 |
| `approvals` | 管理審批請求 |
| `log-implementation` | 記錄實作詳情 |

## 使用範例

### 啟動新 Spec

```python
# 1. 載入工作流程指南
mcp__spec-workflow__spec-workflow-guide()

# 2. 創建需求文件
Write(
    file_path="specs/feature-name/requirements.md",
    content="..."
)

# 3. 請求審批
mcp__spec-workflow__approvals({
    "action": "request",
    "category": "spec",
    "categoryName": "feature-name",
    "filePath": "specs/feature-name/requirements.md",
    "title": "Feature Requirements Review",
    "type": "document"
})
```

### 查看進度

```python
mcp__spec-workflow__spec-status({
    "specName": "feature-name"
})
```

### 記錄實作

```python
mcp__spec-workflow__log-implementation({
    "specName": "feature-name",
    "taskId": "2.1",
    "summary": "Implemented user authentication API",
    "filesModified": ["src/auth/handler.ts"],
    "filesCreated": ["src/auth/middleware.ts"],
    "statistics": {"linesAdded": 150, "linesRemoved": 20},
    "artifacts": {
        "apiEndpoints": [{
            "method": "POST",
            "path": "/api/auth/login",
            "purpose": "User login endpoint"
        }]
    }
})
```

## 整合到 evolve

### 從 Spec 執行

```bash
# 從 spec-workflow 的 tasks.md 執行
/evolve --from-spec feature-name
```

### 執行流程

```
1. 讀取 specs/{name}/tasks.md
2. 解析待執行任務
3. 對每個任務執行 PDCA
4. 完成後記錄 implementation log
5. 更新任務狀態
```

## Spec 目錄結構

```
specs/
└── feature-name/
    ├── requirements.md     # 需求文件
    ├── design.md           # 設計文件
    ├── tasks.md            # 任務分解
    └── implementation-log/ # 實作記錄
        └── entries.json
```

## 最佳實踐

1. **先規劃再實作**: 完成 requirements → design → tasks 再開始寫程式
2. **審批門檻**: 重要決策需要人工審批
3. **詳細記錄**: 實作完成後記錄 artifacts，方便未來 AI 搜尋
