# 03-memory

> Git-based 記憶系統：版本控制、可追溯、可協作

## 本模組包含

| 文件 | 用途 | 建議閱讀順序 |
|------|------|-------------|
| [structure.md](./_base/structure.md) | 目錄結構說明 | 1️⃣ |
| [operations.md](./_base/operations.md) | 搜尋、儲存操作 | 2️⃣ |
| [lifecycle.md](./_base/lifecycle.md) | 生命週期管理 | 3️⃣ |

## 記憶結構

```
.claude/memory/
├── index.md          # 快速索引（必須維護）
├── learnings/        # 成功經驗
├── failures/         # 失敗教訓
├── decisions/        # 決策記錄 (ADR)
├── patterns/         # 推理模式
├── strategies/       # 策略記錄
├── discoveries/      # 涌現發現
└── skill-metrics/    # 技能效果追蹤
```

## 關鍵操作

```python
# 搜尋
Grep(pattern="關鍵字", path=".claude/memory/")

# 儲存後必須同步 index.md（CP3.5）
Write(...) → Edit(index.md) → Verify
```

## 社群貢獻

