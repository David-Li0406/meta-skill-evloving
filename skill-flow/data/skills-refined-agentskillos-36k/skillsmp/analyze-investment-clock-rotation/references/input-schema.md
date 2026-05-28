# 輸入參數定義

## 完整輸入 Schema

```json
{
  "market": "US_EQUITY",
  "start_date": "2022-01-01",
  "end_date": "2026-01-19",

  "earnings_series": {
    "source": "fred",
    "series_id": "CP",
    "field": "value",
    "growth_method": "yoy"
  },

  "financial_conditions_series": {
    "source": "fred",
    "series_id": "NFCI",
    "transform": "inverse"
  },

  "freq": "weekly",
  "z_window": 52,

  "smoothing": {
    "method": "moving_average",
    "window": 4
  },

  "axis_mapping": {
    "x": "financial_conditions",
    "y": "earnings_growth"
  },

  "clock_convention": {
    "financial_loose_is_left": true,
    "supportive_is_up": true
  },

  "compare_cycle": {
    "enabled": false,
    "cycle_start": null,
    "cycle_end": null
  }
}
```

---

## 核心參數

### market

| 屬性 | 值 |
|------|-----|
| 類型 | string |
| 必要 | 是 |
| 預設值 | `"US_EQUITY"` |
| 可選值 | `US_EQUITY`, `GLOBAL`, `EU`, `EM` |

分析標的或市場區域。影響資料來源選擇。

### start_date / end_date

| 屬性 | 值 |
|------|-----|
| 類型 | string (ISO 8601 date) |
| 必要 | 是 |
| 格式 | `YYYY-MM-DD` |

分析時間區間。

---

## 獲利成長參數 (earnings_series)

### source

| 屬性 | 值 |
|------|-----|
| 類型 | string |
| 必要 | 是 |
| 可選值 | `fred`, `api`, `csv`, `manual` |

資料來源類型。

### series_id

| 屬性 | 值 |
|------|-----|
| 類型 | string |
| 必要 | 若 source 為 fred/api |
| 範例 | `"CP"`, `"GDPC1"`, `"INDPRO"` |

資料序列 ID。

### growth_method

| 屬性 | 值 |
|------|-----|
| 類型 | string |
| 必要 | 是 |
| 預設值 | `"yoy"` |
| 可選值 | `yoy`, `qoq_annualized`, `rolling_4q_yoy` |

成長率計算方法。

| 方法 | 說明 | 公式 |
|------|------|------|
| `yoy` | 年對年 | `(E[t] / E[t-1y]) - 1` |
| `qoq_annualized` | 季對季年化 | `((E[t] / E[t-1q]) ** 4) - 1` |
| `rolling_4q_yoy` | 滾動四季同比 | `(sum(E[t-3:t]) / sum(E[t-7:t-4])) - 1` |

---

## 金融環境參數 (financial_conditions_series)

### source

| 屬性 | 值 |
|------|-----|
| 類型 | string |
| 必要 | 是 |
| 可選值 | `fred`, `api`, `csv`, `manual` |

### series_id

| 屬性 | 值 |
|------|-----|
| 類型 | string |
| 必要 | 若 source 為 fred/api |
| 範例 | `"NFCI"`, `"STLFSI4"`, `"ANFCI"` |

### transform

| 屬性 | 值 |
|------|-----|
| 類型 | string |
| 必要 | 否 |
| 預設值 | `"level"` |
| 可選值 | `level`, `zscore`, `inverse` |

轉換方式。

| 轉換 | 說明 | 使用時機 |
|------|------|----------|
| `level` | 原始值 | 已標準化的指標 |
| `zscore` | 滾動 Z-score | 未標準化的原始數據 |
| `inverse` | 反轉方向 | 原始定義與預期相反 |

---

## 頻率與平滑參數

### freq

| 屬性 | 值 |
|------|-----|
| 類型 | string |
| 必要 | 否 |
| 預設值 | `"weekly"` |
| 可選值 | `weekly`, `monthly` |

分析頻率。影響 Z-score 視窗單位。

### z_window

| 屬性 | 值 |
|------|-----|
| 類型 | integer |
| 必要 | 否 |
| 預設值 | `52`（週頻）或 `12`（月頻） |
| 建議範圍 | 36-104（週），12-60（月） |

Z-score 滾動視窗長度。

### smoothing

| 屬性 | 值 |
|------|-----|
| 類型 | object |
| 必要 | 否 |

#### smoothing.method

| 可選值 | 說明 |
|--------|------|
| `none` | 不平滑 |
| `moving_average` | 移動平均 |
| `ema` | 指數移動平均 |

#### smoothing.window

| 屬性 | 值 |
|------|-----|
| 類型 | integer |
| 預設值 | `4` |
| 建議範圍 | 2-8 |

---

## 軸向參數 (axis_mapping)

### x / y

| 屬性 | 值 |
|------|-----|
| 類型 | string |
| 可選值 | `earnings_growth`, `financial_conditions` |

指定 X 軸和 Y 軸分別代表什麼變數。

**預設**：
- `x`: `financial_conditions`
- `y`: `earnings_growth`

**注意**：不同來源的圖表可能有不同定義，請確認後調整。

---

## 時鐘約定 (clock_convention)

### financial_loose_is_left

| 屬性 | 值 |
|------|-----|
| 類型 | boolean |
| 預設值 | `true` |

是否將金融環境「寬鬆」放在左側（負 X）。

### supportive_is_up

| 屬性 | 值 |
|------|-----|
| 類型 | boolean |
| 預設值 | `true` |

是否將「支持性更高」放在上方。

**組合效果**：

| loose_is_left | supportive_is_up | 象限配置 |
|---------------|------------------|----------|
| true | true | Q3 左上, Q1 右上, Q4 左下, Q2 右下 |
| false | true | Q1 左上, Q3 右上, Q2 左下, Q4 右下 |

---

## 循環比較參數 (compare_cycle)

### enabled

| 屬性 | 值 |
|------|-----|
| 類型 | boolean |
| 預設值 | `false` |

是否啟用前一輪循環比較。

### cycle_start / cycle_end

| 屬性 | 值 |
|------|-----|
| 類型 | string (ISO 8601 date) |
| 必要 | 若 enabled=true |

前一輪循環的起止日期。

---

## 參數驗證規則

```python
def validate_params(params):
    errors = []

    # 日期驗證
    if params["start_date"] >= params["end_date"]:
        errors.append("start_date must be before end_date")

    # 成長方法驗證
    valid_growth_methods = ["yoy", "qoq_annualized", "rolling_4q_yoy"]
    if params["earnings_series"]["growth_method"] not in valid_growth_methods:
        errors.append(f"Invalid growth_method: {params['earnings_series']['growth_method']}")

    # 軸向驗證
    valid_axes = ["earnings_growth", "financial_conditions"]
    if params["axis_mapping"]["x"] not in valid_axes:
        errors.append(f"Invalid x axis: {params['axis_mapping']['x']}")
    if params["axis_mapping"]["y"] not in valid_axes:
        errors.append(f"Invalid y axis: {params['axis_mapping']['y']}")
    if params["axis_mapping"]["x"] == params["axis_mapping"]["y"]:
        errors.append("x and y axes must be different")

    # Z-window 驗證
    if params["z_window"] < 12:
        errors.append("z_window should be at least 12 for meaningful standardization")

    return errors
```

---

## 預設配置範例

### 美股週度分析

```json
{
  "market": "US_EQUITY",
  "earnings_series": {
    "source": "fred",
    "series_id": "CP",
    "growth_method": "yoy"
  },
  "financial_conditions_series": {
    "source": "fred",
    "series_id": "NFCI",
    "transform": "inverse"
  },
  "freq": "weekly",
  "z_window": 52
}
```

### 月度長期分析

```json
{
  "market": "US_EQUITY",
  "earnings_series": {
    "source": "fred",
    "series_id": "CP",
    "growth_method": "yoy"
  },
  "financial_conditions_series": {
    "source": "fred",
    "series_id": "NFCI",
    "transform": "inverse"
  },
  "freq": "monthly",
  "z_window": 36,
  "smoothing": {
    "method": "moving_average",
    "window": 3
  }
}
```
