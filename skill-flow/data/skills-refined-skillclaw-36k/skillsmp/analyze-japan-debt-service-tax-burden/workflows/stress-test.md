# 情境壓力測試工作流

自定義殖利率衝擊情境，評估對利息負擔的影響。

## 基本壓測

### 單一利率衝擊

```bash
# +100bp 衝擊
python scripts/japan_debt_analyzer.py --stress 100

# +200bp 衝擊
python scripts/japan_debt_analyzer.py --stress 200

# +300bp 嚴重衝擊
python scripts/japan_debt_analyzer.py --stress 300
```

## 進階壓測（修改腳本）

### Step 1: 自定義情境

編輯 `scripts/japan_debt_analyzer.py` 中的 `DEFAULT_SCENARIOS`：

```python
CUSTOM_SCENARIOS = [
    {
        "name": "+150bp with 20% pass-through",
        "delta_yield_bp": 150,
        "pass_through_year1": 0.20,  # 較高再定價速度
        "pass_through_year2": 0.20,
        "tax_shock": 0.0,
    },
    {
        "name": "+200bp + stagflation",
        "delta_yield_bp": 200,
        "pass_through_year1": 0.15,
        "pass_through_year2": 0.15,
        "tax_shock": -0.10,  # 稅收下降 10%
    },
    {
        "name": "+250bp + fiscal consolidation",
        "delta_yield_bp": 250,
        "pass_through_year1": 0.15,
        "pass_through_year2": 0.15,
        "tax_shock": 0.05,  # 稅收增加 5%（增稅）
    },
]
```

### Step 2: 理解壓測公式

```
additional_interest = debt_stock × pass_through × delta_yield
stressed_ratio = (interest + additional_interest) / (tax × (1 + tax_shock))
```

**關鍵參數**：

| 參數 | 說明 | 預設值 |
|------|------|--------|
| delta_yield_bp | 殖利率上升幅度（bp） | - |
| pass_through_year1 | Year 1 再定價比例 | 0.15 |
| pass_through_year2 | Year 2 再定價比例 | 0.15 |
| tax_shock | 稅收衝擊（負=下降） | 0.0 |

### Step 3: 解讀結果

| Year 2 Ratio | 風險分級 | 含義 |
|--------------|----------|------|
| < 0.40 | 🟡 YELLOW | 可控壓力 |
| 0.40–0.55 | 🟠 ORANGE | 需政策調整 |
| > 0.55 | 🔴 RED | 財政彈性極度受限 |

## 情境設計建議

### 保守情境
- delta_yield_bp: 100–150
- tax_shock: 0
- 用途：基準風險評估

### 中性情境
- delta_yield_bp: 200
- tax_shock: 0 或 -0.03
- 用途：合理壓力測試

### 嚴重情境
- delta_yield_bp: 300+
- tax_shock: -0.10
- 用途：尾部風險評估

### 反向情境（稅收增加）
- delta_yield_bp: 200
- tax_shock: +0.05（增稅）
- 用途：政策調整效果評估
