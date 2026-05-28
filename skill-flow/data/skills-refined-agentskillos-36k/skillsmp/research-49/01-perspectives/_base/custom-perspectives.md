# Custom Perspectives

> 自訂視角指南：根據研究需求建立專屬視角

## 使用自訂視角

```bash
/multi-research --custom [主題]
```

系統會互動式引導你定義視角。

## 視角定義結構

每個視角需要定義：

```yaml
perspective:
  id: unique-id           # 唯一識別碼
  name: 視角名稱          # 顯示名稱
  role: 角色描述          # 這個視角扮演什麼角色
  focus:                  # 研究重點（3-5 項）
    - 重點 1
    - 重點 2
    - 重點 3
  method: deep | search   # 研究方法
  prompt_template: |      # Prompt 模板
    你是一位 {role}...
```

## 研究方法選擇

### deep（深度分析）

使用 Task API 進行深度思考，適用於：
- 理論分析
- 概念探索
- 系統設計
- 抽象推理

### search（網路搜尋）

使用 WebSearch 收集資訊，適用於：
- 市場調研
- 案例收集
- 工具比較
- 趨勢追蹤

## 自訂視角範例

### 安全專家視角

```yaml
perspective:
  id: security
  name: 安全專家
  role: 資訊安全專家，專注於威脅建模和防護策略
  focus:
    - 威脅識別
    - 攻擊向量分析
    - 防護措施
    - 合規要求
  method: deep
```

### 使用者體驗視角

```yaml
perspective:
  id: ux
  name: UX 設計師
  role: 使用者體驗設計師，專注於易用性和使用者旅程
  focus:
    - 使用者需求
    - 互動設計
    - 易用性評估
    - 情感設計
  method: deep
```

### 競品分析視角

```yaml
perspective:
  id: competitive
  name: 競品分析師
  role: 市場分析師，專注於競爭格局和差異化策略
  focus:
    - 競品功能比較
    - 市場定位
    - 差異化機會
    - 定價策略
  method: search
```

## 視角組合建議

### 產品開發

```
architecture + ux + competitive + industry
```

### 安全審計

```
architecture + security + workflow + industry
```

### 技術選型

```
architecture + workflow + industry
```

### 學術研究

```
cognitive + industry（學術文獻）
```

## 儲存自訂視角

自訂視角可以儲存到專案：

```
.claude/perspectives/
├── security.yaml
├── ux.yaml
└── competitive.yaml
```

下次使用：

```bash
/multi-research --perspectives security,ux,competitive 某主題
```

## 視角設計原則

1. **互補性**：視角之間應該互補，而非重疊
2. **聚焦性**：每個視角有明確的研究範圍
3. **可操作**：研究結果應該可以轉化為行動
4. **平衡性**：理論與實踐並重

## 視角數量建議

| 研究複雜度 | 建議視角數 | 說明 |
|-----------|-----------|------|
| 簡單 | 2-3 | 快速決策 |
| 中等 | 4 | 標準研究（預設）|
| 複雜 | 5-6 | 重大決策 |
| 深度 | 6+ | 學術級研究 |

> 視角過多會增加整合難度，建議不超過 6 個
