# Default Perspectives

> 預設 4 視角配置：監督式實作的品質守護框架

## 視角總覽

```
┌─────────────────────────────────────────────────────────┐
│                    主 Agent 實作                         │
├─────────────────────────────────────────────────────────┤
│  品質層                          安全層                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│  │ TDD      │  │ 效能     │  │ 安全     │  │ 維護性   ││
│  │ 守護者   │  │ 優化師   │  │ 審計員   │  │ 專家     ││
│  │          │  │          │  │          │  │          ││
│  │ 測試先行 │  │ 複雜度   │  │ OWASP    │  │ 可讀性   ││
│  │ 覆蓋率   │  │ 記憶體   │  │ 輸入驗證 │  │ 文檔     ││
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘│
│        ↓              ↓              ↓              ↓   │
│                    即時回饋到主 Agent                    │
└─────────────────────────────────────────────────────────┘
```

## 視角 1: TDD 守護者 (tdd-enforcer)

### 角色定位

測試驅動開發專家，確保測試優先

### 監督重點

- 測試先行（紅綠重構）
- 測試覆蓋率
- 邊界案例
- Mock 使用
- 測試品質

### 回饋模板

```
TDD 守護者審查：

對於 {code_block}：

測試覆蓋：
  ✅ 有單元測試
  ❌ 缺少 {function_name} 的測試

邊界案例：
  ⚠️ 未測試空輸入
  ⚠️ 未測試最大值

建議：
  💡 添加 test_{function_name}_empty_input()
  💡 添加 test_{function_name}_max_value()
```

### 阻擋條件

```yaml
block_if:
  - new_function_without_test: true
  - coverage_below: 80%
  - critical_path_untested: true
```

## 視角 2: 效能優化師 (performance-optimizer)

### 角色定位

效能專家，識別效能問題

### 監督重點

- 時間複雜度
- 空間複雜度
- 記憶體使用
- 快取機會
- 資料庫查詢

### 回饋模板

```
效能優化師審查：

對於 {code_block}：

複雜度分析：
  時間：O(n²) ⚠️
  空間：O(n) ✅

效能問題：
  ⚠️ 巢狀迴圈可優化為 O(n log n)
  ⚠️ 可考慮 memoization

建議：
  💡 使用 hash map 優化查找
  💡 考慮批次處理
```

### 阻擋條件

```yaml
block_if:
  - complexity_above: "O(n³)"
  - memory_leak_detected: true
  - n_plus_1_query: true
```

## 視角 3: 安全審計員 (security-auditor)

### 角色定位

安全專家，識別安全漏洞

### 監督重點

- OWASP Top 10
- 輸入驗證
- 認證授權
- 資料保護
- 安全編碼

### 回饋模板

```
安全審計員審查：

對於 {code_block}：

安全檢查：
  ❌ 用戶輸入未驗證
  ⚠️ 缺少 CSRF 保護

OWASP 風險：
  A1 - Injection：❌ 風險
  A7 - XSS：✅ 無風險

建議：
  💡 使用 sanitize(input) 處理輸入
  💡 添加 @csrf_protect 裝飾器
```

### 阻擋條件

```yaml
block_if:
  - sql_injection_possible: true
  - xss_vulnerability: true
  - hardcoded_secret: true
  - insecure_auth: true
```

## 視角 4: 維護性專家 (maintainer)

### 角色定位

可維護性專家，確保程式碼易於維護

### 監督重點

- 命名清晰度
- 函數長度
- 程式碼重複
- 文檔完整
- 重構友善

### 回饋模板

```
維護性專家審查：

對於 {code_block}：

可讀性：
  ✅ 命名清晰
  ⚠️ 函數過長（120 行）

程式碼品質：
  ⚠️ 發現重複邏輯
  ✅ 無魔術數字

建議：
  💡 拆分為 process_input() 和 validate_output()
  💡 提取重複邏輯為 helper 函數
```

### 阻擋條件

```yaml
block_if:
  - function_lines_above: 200
  - cyclomatic_complexity_above: 20
  - duplicate_code_ratio_above: 0.3
```

## 視角協作

### 回饋整合

```
┌─────────────────────────────────────────────┐
│ 綜合回饋（4 視角整合）                       │
├─────────────────────────────────────────────┤
│ 阻擋項（必須修正）：                         │
│   ❌ [Security] 輸入未驗證                   │
│   ❌ [TDD] login() 缺少測試                  │
│                                              │
│ 警告項（建議修正）：                         │
│   ⚠️ [Performance] O(n²) 可優化             │
│   ⚠️ [Maintainer] 函數過長                  │
│                                              │
│ 建議項（可選改進）：                         │
│   💡 [TDD] 添加邊界案例                      │
│   💡 [Performance] 考慮快取                  │
└─────────────────────────────────────────────┘
```

### 優先順序

1. Security 阻擋 > 其他阻擋
2. TDD 阻擋 > Performance 阻擋
3. 多視角共識 > 單視角意見

## 深度模式額外視角

當使用 `--deep` 時，可添加：

| ID | 名稱 | 聚焦領域 |
|----|------|----------|
| `a11y` | 可訪問性專家 | WCAG、螢幕閱讀器 |
| `i18n` | 國際化專家 | 多語言、本地化 |

## 自訂視角

詳見 [custom-perspectives.md](./custom-perspectives.md)
