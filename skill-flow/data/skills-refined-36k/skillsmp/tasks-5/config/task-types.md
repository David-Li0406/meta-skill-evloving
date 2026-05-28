# 任務類型定義

> 定義 TASKS skill 產出的任務類型和格式

## 任務類型總覽

| 前綴 | 類型 | 來源視角 | 說明 |
|------|------|----------|------|
| `T-F-` | feature | task-decomposer | 功能實作任務 |
| `T-R-` | refactor | task-decomposer | 重構任務 |
| `TEST-` | test | test-planner | 測試任務 |
| `RISK-` | prevention/rollback/monitoring | risk-preventor | 風險相關任務 |

## 功能任務 (T-F-*)

### 定義

功能實作任務，由 `task-decomposer` 視角產出。

### 格式

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
    complexity: M

  priority: P0

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

---

## 重構任務 (T-R-*)

### 定義

程式碼重構任務，由 `task-decomposer` 視角產出。

### 格式

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

---

## 測試任務 (TEST-*)

### 定義

測試任務，由 `test-planner` 視角產出。遵循 TDD 原則，測試任務應排在對應功能任務之前或同時。

### 格式

```yaml
- id: TEST-001
  type: test
  milestone: M1
  name: "JWT 函數單元測試"
  related_task: T-F-001

  test_cases:
    - scenario: "生成有效 token"
      expected: "返回 JWT 字串"
    - scenario: "驗證有效 token"
      expected: "返回 payload"
    - scenario: "驗證過期 token"
      expected: "拋出 TokenExpiredError"
    - scenario: "驗證無效簽名"
      expected: "拋出 InvalidSignatureError"

  priority: P0

  dependencies:
    blocked_by: []
    blocks: [T-F-001]  # TDD: 測試先於實作

  acceptance_criteria:
    - "tests/auth/jwt.test.ts 存在"
    - "覆蓋率 > 80%"
    - "邊界案例全部覆蓋"

  status: pending
```

---

## 風險任務 (RISK-*)

### 定義

風險預防相關任務，由 `risk-preventor` 視角產出。

### 子類型

| 子類型 | 說明 |
|--------|------|
| prevention | 預防措施 |
| rollback | 回退計劃 |
| monitoring | 監控設置 |

### 格式：預防任務

```yaml
- id: RISK-001
  type: prevention
  milestone: M1
  name: "設定認證服務監控"
  related_risk: "R-002 認證效能問題"

  trigger: "部署後"

  steps:
    - "設定登入延遲告警 (> 2s)"
    - "設定失敗率告警 (> 5%)"
    - "建立 dashboard"

  priority: P1

  dependencies:
    blocked_by: [T-F-002]
    blocks: []

  acceptance_criteria:
    - "監控 dashboard 已建立"
    - "告警規則已配置"

  status: pending
```

### 格式：回退任務

```yaml
- id: RISK-002
  type: rollback
  milestone: M2
  name: "認證系統回退計劃"
  related_risk: "R-001 認證系統故障"

  trigger: "登入失敗率 > 10%"

  steps:
    - "切換到舊版認證端點"
    - "通知維運團隊"
    - "保留日誌供分析"

  priority: P0

  dependencies:
    blocked_by: [T-F-003]
    blocks: []

  status: pending
```

### 格式：監控任務

```yaml
- id: RISK-003
  type: monitoring
  milestone: M3
  name: "設置效能基準監控"

  metrics:
    - name: "登入延遲"
      threshold: "< 500ms"
    - name: "Token 驗證延遲"
      threshold: "< 50ms"

  priority: P1

  dependencies:
    blocked_by: [T-F-001, T-F-002]
    blocks: []

  status: pending
```

---

## 優先級定義

| 等級 | 名稱 | 說明 | 行動 |
|------|------|------|------|
| **P0** | 必做 | 核心功能，不可跳過 | 必須在此迭代完成 |
| **P1** | 應做 | 重要功能，強烈建議完成 | 應在此迭代完成 |
| **P2** | 可延 | 優化功能，可延後處理 | 可延後到下個迭代 |

---

## 任務粒度標準

### 目標粒度

**10-60 分鐘可完成**

### 判斷標準

| 情況 | 判斷 | 建議動作 |
|------|------|----------|
| < 10 分鐘 | 太細 | 合併相關任務 |
| 10-60 分鐘 | 適中 | 保持 |
| > 60 分鐘 | 太粗 | 進一步拆分 |
| > 3 個獨立步驟 | 可能太粗 | 考慮拆分 |

### 例外情況

- 環境設置類任務可達 2 小時
- 簡單配置類任務可少於 10 分鐘

---

## 複雜度定義

| 等級 | 說明 | 典型時長 |
|------|------|----------|
| **XS** | 極簡單，配置級 | < 10m |
| **S** | 簡單，單一功能 | 10-20m |
| **M** | 中等，多步驟 | 20-45m |
| **L** | 複雜，涉及多模組 | 45-90m |
| **XL** | 極複雜，需拆分 | > 90m |

> 注意：XL 複雜度的任務應該進一步拆分
