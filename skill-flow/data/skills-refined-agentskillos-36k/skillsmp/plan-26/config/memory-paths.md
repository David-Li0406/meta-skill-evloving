# Memory Paths Configuration

> plan skill 的 Memory 存儲路徑配置

## 基礎路徑

```yaml
base_path: .claude/memory/plans/
```

## 記錄結構

```
.claude/memory/plans/
├── index.md                      # 規劃索引
└── [feature-id]/                 # 單個規劃記錄
    ├── meta.yaml                 # 元數據
    ├── overview.md               # 一頁概述
    ├── perspectives/             # 視角報告
    │   ├── architect.md
    │   ├── risk-analyst.md
    │   ├── estimator.md
    │   └── ux-advocate.md
    ├── synthesis.md              # 共識設計
    ├── implementation-plan.md    # 實作計劃（主輸出）
    ├── milestones.md             # 里程碑
    └── risk-mitigation.md        # 風險緩解
```

## 文件命名規則

### feature-id 生成

```
規則：{feature-name-kebab-case}
範例：
- "用戶認證系統" → user-auth-system
- "購物車功能" → shopping-cart
- "API 重構" → api-refactoring
```

### 重複處理

```
如已存在相同 feature-id：
- 詢問是否復用
- 或添加日期後綴：user-auth-system-20250124
```

## meta.yaml 格式

```yaml
id: user-auth-system
feature: 用戶認證系統
skill: plan
date: 2025-01-24
duration: 35min

config:
  mode: normal        # quick | normal | deep
  perspectives:
    - architect
    - risk-analyst
    - estimator
    - ux-advocate

results:
  consensus_points: 8
  conflicts_resolved: 2
  milestones: 5
  estimated_effort: "5 天"

related:
  research:
    - auth-patterns     # 相關研究記錄
  plan: []
  implementation: []

status: completed       # in_progress | completed | partial

tags:
  - authentication
  - security
  - user-management
```

## 索引更新規則

### index.md 格式

```markdown
# Plans Memory Index

## 規劃列表

| ID | 功能 | 日期 | 視角數 | 狀態 |
|----|------|------|--------|------|
| user-auth-system | 用戶認證系統 | 2025-01-24 | 4 | ✅ |
| shopping-cart | 購物車功能 | 2025-01-23 | 4 | ✅ |

## 按標籤分類

### authentication
- [user-auth-system](./user-auth-system/overview.md)

### api
- [api-refactoring](./api-refactoring/overview.md)

## 最近規劃

1. user-auth-system (2025-01-24)
2. shopping-cart (2025-01-23)
```

### 更新時機

每次規劃完成（Phase 7）時：
1. 添加新記錄到「規劃列表」
2. 更新「按標籤分類」
3. 更新「最近規劃」（保留最近 10 個）

## 與 research 的關聯

### 載入研究結果

```
--from-research {research-id}
```

會自動：
1. 讀取 `.claude/memory/research/{research-id}/synthesis.md`
2. 提取關鍵發現作為規劃輸入
3. 在 meta.yaml 中記錄關聯

### 關聯記錄

```yaml
# plan 的 meta.yaml
related:
  research:
    - microservice-patterns
```

```yaml
# research 的 meta.yaml（反向更新）
related:
  plan:
    - api-refactoring
```

## 共用模組參考

- Memory 系統通用規範：[shared/integration/memory-system.md](../../../shared/integration/memory-system.md)
- Checkpoint 對應：[shared/integration/evolve-checkpoints.md](../../../shared/integration/evolve-checkpoints.md)
