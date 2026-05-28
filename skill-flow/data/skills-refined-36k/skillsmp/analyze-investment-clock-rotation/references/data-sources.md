# 資料來源

## FRED 資料來源

本 skill 主要使用 FRED（Federal Reserve Economic Data）公開資料，無需 API key。

### 獲取方式

**CSV Endpoint（推薦）**：
```
https://fred.stlouisfed.org/graph/fredgraph.csv?id={SERIES_ID}&cosd={START}&coed={END}
```

範例：
```bash
# 抓取 NFCI 從 2020-01-01 到 2026-01-01
curl "https://fred.stlouisfed.org/graph/fredgraph.csv?id=NFCI&cosd=2020-01-01&coed=2026-01-01"
```

---

## 金融環境指標

### NFCI - Chicago Fed National Financial Conditions Index

| 屬性 | 值 |
|------|-----|
| FRED ID | `NFCI` |
| 頻率 | 週度（Weekly） |
| 單位 | Index |
| 原始定義 | 正值 = 緊縮，負值 = 寬鬆 |
| 歷史起點 | 1971-01-08 |

**說明**：
- 綜合 105 項金融市場指標
- 涵蓋風險、信用、槓桿三個子指數
- 0 代表歷史平均水平
- 適合週度分析

**使用方式**：
```python
# 反轉方向讓正值代表「支持性」
fci_support = -nfci
```

### STLFSI4 - St. Louis Fed Financial Stress Index

| 屬性 | 值 |
|------|-----|
| FRED ID | `STLFSI4` |
| 頻率 | 週度（Weekly） |
| 單位 | Index |
| 原始定義 | 正值 = 壓力高，負值 = 壓力低 |
| 歷史起點 | 1993-12-31 |

**說明**：
- 聚焦於金融壓力/風險
- 適合危機預警
- 與 NFCI 方向一致

### ANFCI - Adjusted National Financial Conditions Index

| 屬性 | 值 |
|------|-----|
| FRED ID | `ANFCI` |
| 頻率 | 週度（Weekly） |
| 單位 | Index |
| 原始定義 | 正值 = 緊縮 |
| 歷史起點 | 1971-01-08 |

**說明**：
- 調整過的 NFCI
- 移除經濟週期影響
- 更純粹反映金融條件

---

## 獲利成長指標

### CP - Corporate Profits After Tax

| 屬性 | 值 |
|------|-----|
| FRED ID | `CP` |
| 頻率 | 季度（Quarterly） |
| 單位 | Billions of Dollars |
| 季節調整 | Seasonally Adjusted Annual Rate |
| 歷史起點 | 1947-01-01 |

**說明**：
- 最直接的企業獲利指標
- 涵蓋所有美國企業
- 適合計算 YoY 成長率

**計算 YoY**：
```python
# 季度數據，用 4 期計算 YoY
earnings_yoy = (cp / cp.shift(4)) - 1
```

### A261RX1Q020SBEA - Real GDP per Capita

| 屬性 | 值 |
|------|-----|
| FRED ID | `A261RX1Q020SBEA` |
| 頻率 | 季度（Quarterly） |
| 單位 | Chained 2017 Dollars |
| 歷史起點 | 1947-01-01 |

**說明**：
- 實質 GDP 人均
- 可作為獲利成長的代理變數
- 較為平滑

### INDPRO - Industrial Production Index

| 屬性 | 值 |
|------|-----|
| FRED ID | `INDPRO` |
| 頻率 | 月度（Monthly） |
| 單位 | Index 2017=100 |
| 歷史起點 | 1919-01-01 |

**說明**：
- 製造業獲利的代理
- 月度頻率較高
- 與企業利潤高度相關

---

## 資料頻率對齊

### 週度 ↔ 季度對齊

**方法 A：將週度降採樣到季度**

```python
# 取季度最後一個觀測值
nfci_quarterly = nfci.resample('Q').last()

# 或取季度平均
nfci_quarterly = nfci.resample('Q').mean()
```

**方法 B：將季度升採樣到週度**

```python
# 前向填充
earnings_weekly = earnings.resample('W').ffill()
```

### 建議做法

| 分析目的 | 建議頻率 | 對齊方法 |
|----------|----------|----------|
| 長期趨勢 | 季度 | 週度降採樣 |
| 短期監控 | 週度 | 季度升採樣（ffill） |
| 回測 | 月度 | 折衷方案 |

---

## 替代資料來源

### MacroMicro 財經 M 平方

若需要更多指標或視覺化，可參考 MacroMicro：

| 圖表 | URL | 說明 |
|------|-----|------|
| 美國金融狀況 | `/charts/xxx` | 綜合金融狀況圖 |
| 企業利潤 | `/charts/xxx` | 企業利潤趨勢 |

**注意**：MacroMicro 需要使用 Selenium 爬蟲，詳見 `thoughts/shared/guide/macromicro-highcharts-crawler.md`。

### Bloomberg / Refinitiv

若有付費訂閱，可使用：
- Bloomberg: `NFCI Index`
- Refinitiv: 對應代碼

---

## 資料品質檢查

### 必要檢查項目

```python
def validate_data(df):
    checks = {
        "no_nulls": df.isnull().sum().sum() == 0,
        "no_duplicates": not df.index.duplicated().any(),
        "sorted_index": df.index.is_monotonic_increasing,
        "reasonable_range": {
            "nfci": df["nfci"].between(-5, 5).all(),
            "earnings_yoy": df["earnings_yoy"].between(-0.5, 0.5).all()
        }
    }
    return checks
```

### 缺失值處理

| 情況 | 建議處理 |
|------|----------|
| 單一缺失 | 線性內插 |
| 連續缺失 < 4 期 | 前向填充 |
| 連續缺失 >= 4 期 | 標記為無效區間 |

---

## 快速抓取範例

```python
import pandas as pd

def fetch_fred_csv(series_id, start_date, end_date):
    """從 FRED 抓取 CSV 資料"""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv"
    params = {
        "id": series_id,
        "cosd": start_date,
        "coed": end_date
    }
    query = "&".join(f"{k}={v}" for k, v in params.items())
    full_url = f"{url}?{query}"

    df = pd.read_csv(full_url, parse_dates=["DATE"], index_col="DATE")
    df.columns = [series_id]
    return df

# 使用範例
nfci = fetch_fred_csv("NFCI", "2020-01-01", "2026-01-19")
cp = fetch_fred_csv("CP", "2020-01-01", "2026-01-19")
```
