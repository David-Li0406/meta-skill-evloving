# test-planner 視角

> 測試規劃師：規劃測試任務，確保 TDD 先行

## 視角定義

```yaml
id: test-planner
name: 測試規劃師
role: 規劃測試任務，確保測試覆蓋和 TDD 順序
method: TDD 規劃 + 邊界分析

focus:
  - 單元測試規劃
  - 整合測試規劃
  - 邊界案例識別
  - TDD 順序確保

output:
  tasks:
    prefix: "TEST-"
```

## 執行順序

**Phase 2: 並行執行**

在 dependency-analyst 完成後，與 task-decomposer、risk-preventor 並行執行。

## 輸入

```yaml
from_dependency_analyst:
  - dependency-graph.md  # 元件清單和依賴關係

from_plan:
  - implementation-plan.md  # 技術方案
```

## TDD 原則

### 測試優先順序

```yaml
tdd_order:
  principle: "測試任務應在對應功能任務之前或同時"

  dependencies:
    - TEST-001 blocks T-F-001  # 測試先於實作
    - TEST-001 blocked_by []   # 測試無前置依賴
```

### 測試類型

| 類型 | 說明 | 命名 |
|------|------|------|
| 單元測試 | 單一函數/類別 | TEST-001 |
| 整合測試 | 多模組協作 | TEST-INT-001 |
| E2E 測試 | 端到端流程 | TEST-E2E-001 |

## 規劃步驟

### Step 1: 識別測試目標

從 implementation-plan.md 識別：

- 需要測試的函數/類別
- 公開 API 端點
- 關鍵業務邏輯

### Step 2: 設計測試案例

對每個測試目標：

```yaml
test_case_design:
  happy_path:
    - "正常輸入，預期結果"

  edge_cases:
    - "空輸入"
    - "最大值"
    - "最小值"
    - "特殊字元"

  error_cases:
    - "無效輸入"
    - "權限不足"
    - "資源不存在"
```

### Step 3: 確保 TDD 順序

```yaml
dependency_check:
  for_each_feature_task:
    - find_related_test_task
    - ensure: "TEST-* blocks T-F-*"
```

### Step 4: 識別邊界條件

```yaml
boundary_analysis:
  numeric:
    - "0"
    - "負數"
    - "MAX_INT"

  string:
    - "空字串"
    - "超長字串"
    - "特殊字元"
    - "Unicode"

  collection:
    - "空集合"
    - "單一元素"
    - "大量元素"
```

## 輸出格式

### 單元測試任務

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
    - scenario: "空 payload"
      expected: "拋出 InvalidPayloadError"

  priority: P0

  dependencies:
    blocked_by: []
    blocks: [T-F-001]  # TDD: 測試先於實作

  acceptance_criteria:
    - "tests/auth/jwt.test.ts 存在"
    - "覆蓋率 > 80%"
    - "邊界案例全部覆蓋"

  estimate:
    duration: "20m"
    complexity: S

  status: pending
```

### 整合測試任務

```yaml
- id: TEST-INT-001
  type: test
  milestone: M2
  name: "認證流程整合測試"
  related_task: T-F-003

  test_cases:
    - scenario: "完整登入流程"
      expected: "返回有效 token"
    - scenario: "使用 token 訪問保護資源"
      expected: "正常訪問"
    - scenario: "使用過期 token"
      expected: "401 Unauthorized"
    - scenario: "並發登入請求"
      expected: "所有請求正常處理"

  priority: P0

  dependencies:
    blocked_by: [T-F-001, T-F-002]
    blocks: [T-F-003]

  acceptance_criteria:
    - "tests/integration/auth.test.ts 存在"
    - "CI 中執行通過"

  estimate:
    duration: "30m"
    complexity: M

  status: pending
```

## 覆蓋率要求

```yaml
coverage_requirements:
  unit_tests:
    line: ">= 80%"
    branch: ">= 70%"
    function: ">= 90%"

  integration_tests:
    api_endpoints: "100%"
    critical_paths: "100%"
```

## 品質檢查

### 必須通過

- [ ] 所有任務 ID 格式正確（TEST-NNN）
- [ ] 所有功能任務都有對應的測試任務
- [ ] TDD 順序正確（TEST 在 T-F 之前或同時）
- [ ] test_cases 完整

### 建議通過

- [ ] 覆蓋率目標已定義
- [ ] 邊界案例已識別
- [ ] 錯誤案例已覆蓋
