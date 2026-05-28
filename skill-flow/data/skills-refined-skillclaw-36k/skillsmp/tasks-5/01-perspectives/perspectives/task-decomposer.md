# task-decomposer 視角

> 任務分解師：將計劃分解為可執行的功能任務

## 視角定義

```yaml
id: task-decomposer
name: 任務分解師
role: 將技術方案分解為 10-60 分鐘可完成的功能任務
method: 分解估算 + INVEST 原則

focus:
  - 功能任務分解
  - 工作量估算
  - 驗收標準定義
  - 檔案影響識別

output:
  tasks:
    - prefix: "T-F-"  # 功能任務
    - prefix: "T-R-"  # 重構任務
```

## 執行順序

**Phase 2: 並行執行**

在 dependency-analyst 完成後，與 test-planner、risk-preventor 並行執行。

## 輸入

```yaml
from_dependency_analyst:
  - dependency-graph.md  # 元件清單和依賴關係

from_plan:
  - implementation-plan.md  # 技術方案
  - milestones.md           # 里程碑定義
```

## 分解原則

### INVEST 原則

| 原則 | 說明 | 檢查問題 |
|------|------|----------|
| **I**ndependent | 獨立可測 | 這個任務可以單獨驗收嗎？ |
| **N**egotiable | 可協商 | 有明確的成功標準嗎？ |
| **V**aluable | 有價值 | 完成後有明確產出嗎？ |
| **E**stimable | 可估算 | 能估算工作量嗎？ |
| **S**mall | 足夠小 | 在 10-60 分鐘內可完成嗎？ |
| **T**estable | 可測試 | 如何驗證完成了？ |

### 粒度標準

```yaml
granularity:
  target: "10-60 分鐘"

  too_small:
    threshold: "< 10 分鐘"
    action: "合併相關任務"

  too_large:
    threshold: "> 60 分鐘"
    action: "進一步拆分"

  exceptions:
    - "環境設置類：可達 2 小時"
    - "簡單配置類：可少於 10 分鐘"
```

## 分解步驟

### Step 1: 識別功能單元

從 implementation-plan.md 識別：

- 需要實作的函數/類別
- 需要建立的模組
- 需要修改的現有程式碼

### Step 2: 拆分任務

對每個功能單元：

1. 識別子步驟
2. 評估每個步驟的工作量
3. 超過 60 分鐘的繼續拆分
4. 少於 10 分鐘的考慮合併

### Step 3: 定義驗收標準

每個任務必須有：

- 明確的完成條件
- 可執行的驗證命令
- 預期的產出檔案

### Step 4: 識別檔案影響

```yaml
files:
  create:
    - "新建的檔案路徑"
  modify:
    - "需修改的現有檔案"
```

## 輸出格式

### 任務定義

```yaml
- id: T-F-001
  type: feature
  milestone: M1
  name: "實作 JWT token 生成函數"
  description: |
    建立 JWT token 生成與驗證的核心函數。
    使用 HS256 演算法，token 有效期 24 小時。

  estimate:
    duration: "30m"
    complexity: M  # XS/S/M/L/XL

  priority: P0  # P0 必做 / P1 應做 / P2 可延

  dependencies:
    blocked_by: []
    blocks: [T-F-002, T-F-003]

  acceptance_criteria:
    - "src/auth/jwt.ts 檔案存在"
    - "導出 generateToken() 和 verifyToken() 函數"
    - "npm test -- --grep 'JWT' 通過"

  files:
    create: [src/auth/jwt.ts]
    modify: []

  supervision_hints:
    tdd: "先寫測試：過期 token、無效簽名"
    security: "檢查 secret 是否硬編碼"

  status: pending
```

### 重構任務

```yaml
- id: T-R-001
  type: refactor
  milestone: M2
  name: "重構認證中介軟體"
  description: |
    將認證邏輯從路由層抽離到獨立中介軟體。

  estimate:
    duration: "45m"
    complexity: M

  priority: P1

  dependencies:
    blocked_by: [T-F-001, T-F-002]
    blocks: []

  acceptance_criteria:
    - "認證邏輯在 middleware/auth.ts"
    - "原有測試全部通過"
    - "無重複程式碼"

  files:
    create: [src/middleware/auth.ts]
    modify: [src/routes/api.ts]

  status: pending
```

## 複雜度定義

| 等級 | 說明 | 典型時長 |
|------|------|----------|
| **XS** | 極簡單，配置級 | < 10m |
| **S** | 簡單，單一功能 | 10-20m |
| **M** | 中等，多步驟 | 20-45m |
| **L** | 複雜，涉及多模組 | 45-90m |
| **XL** | 極複雜，需拆分 | > 90m |

## 品質檢查

### 必須通過

- [ ] 所有任務 ID 格式正確（T-F-NNN 或 T-R-NNN）
- [ ] 所有任務有明確的驗收標準
- [ ] 所有任務粒度在 10-60 分鐘範圍
- [ ] 所有任務有優先級標記

### 建議通過

- [ ] supervision_hints 已填寫
- [ ] files 欄位完整
- [ ] 依賴關係與 dependency-graph 一致
