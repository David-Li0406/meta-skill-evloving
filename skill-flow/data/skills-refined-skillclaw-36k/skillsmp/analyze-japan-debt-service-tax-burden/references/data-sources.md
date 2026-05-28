# 資料來源說明

本 Skill 使用的資料來源與 API 端點。

## 優先使用：官方/公開資料

### 1. JGB 殖利率

#### 日本財務省 (MOF)
- **網站**: https://www.mof.go.jp/jgbs/reference/interest_rate/
- **資料**: 日本國債殖利率時間序列
- **格式**: CSV/Excel 可下載
- **期限**: 1Y, 2Y, 3Y, 5Y, 10Y, 20Y, 30Y, 40Y

#### 日本銀行 (BOJ) 統計
- **網站**: https://www.stat-search.boj.or.jp/
- **資料**: 金融市場統計
- **格式**: CSV

#### FRED（替代方案）
- **端點**: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=IRLTLT01JPM156N`
- **系列**:
  - `IRLTLT01JPM156N` - 日本長期利率（10Y 近似）
  - `INTGSTJPM193N` - 日本短期利率

```python
# 無需 API key 的 FRED CSV 抓取
import pandas as pd
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=IRLTLT01JPM156N"
df = pd.read_csv(url, parse_dates=["DATE"])
```

### 2. 財政數據（稅收、利息支出、債務）

#### 日本財務省 預算/決算
- **網站**: https://www.mof.go.jp/policy/budget/
- **資料**:
  - 一般會計歲入歲出（稅收）
  - 國債費（利息+本金償還）
  - 國債殘高（債務存量）
- **頻率**: 年度

#### 日本財務省 國債統計
- **網站**: https://www.mof.go.jp/jgbs/reference/gbb/
- **資料**: 國債發行殘高、到期結構
- **用途**: 計算 pass_through 再定價比例

#### IMF / OECD（跨國比較用）
- **IMF IFS**: General government interest payments / revenue
- **OECD**: Government debt interest payments
- **注意**: 口徑可能與日本國內統計不同

### 3. 外溢通道（日本對美資產）

#### US Treasury TIC
- **網站**: https://ticdata.treasury.gov/
- **資料**: 外國持有美國證券
- **系列**: Major Foreign Holders of Treasury Securities
- **日本數據**: 月度更新

```python
# TIC 日本持有美債
url = "https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents/mfh.txt"
```

#### 日本 IIP（國際投資頭寸）
- **來源**: 日本銀行
- **資料**: 對外資產負債表
- **用途**: 估算對美資產總規模

### 4. GDP 數據（用於計算 debt_to_gdp 和 debt_in_us_terms）

#### 美國 GDP (FRED)
- **系列**: `GDP`（季度名目 GDP）
- **端點**: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDP`
- **單位**: 十億美元
- **更新頻率**: 季度
- **用途**: 計算「debt_in_us_terms」（若美國有相同債務/GDP比例）

```python
# 抓取美國 GDP（由 data_manager.py 自動執行）
import pandas as pd
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=GDP"
df = pd.read_csv(url, parse_dates=["DATE"])
us_gdp_usd = df["GDP"].iloc[-1] * 1e9  # 十億美元 → 美元
```

#### 日本 GDP (FRED)
- **系列**: `JPNNGDP`（日本名目 GDP，美元計）
- **端點**: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=JPNNGDP`
- **單位**: 十億美元
- **更新頻率**: 年度
- **用途**: 驗證配置中的 `japan_gdp_jpy` 合理性

```python
# 抓取日本 GDP（由 data_manager.py 自動執行）
url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=JPNNGDP"
df = pd.read_csv(url, parse_dates=["DATE"])
japan_gdp_usd = df["JPNNGDP"].iloc[-1] * 1e9
```

#### 日本 GDP（日圓計，配置維護）
- **來源**: `config/fiscal_data.json` 中的 `japan_gdp_jpy`
- **用途**: 計算 `debt_to_gdp = debt_stock_jpy / japan_gdp_jpy`
- **注意**: 此值需手動維護，與財政數據同步更新

## 資料口徑說明

### 稅收口徑

| 口徑 | 說明 | 數值量級 |
|------|------|----------|
| `national_tax` | 國稅（所得稅+法人稅+消費稅等） | ~60-65 兆 |
| `general_account_tax` | 一般會計稅收 | ~70-75 兆 |
| `total_revenue` | 總收入（含非稅收入） | ~100+ 兆 |

### 利息口徑

| 口徑 | 說明 | 數值量級 |
|------|------|----------|
| `interest_only` | 純利息支出 | ~8-10 兆 |
| `debt_service` | 國債費（利息+本金償還） | ~25-28 兆 |

**重要**：媒體敘事「1/3」通常使用 `debt_service / general_account_tax`。

## 資料更新頻率

| 資料類型 | 更新頻率 | 滯後 |
|----------|----------|------|
| JGB 殖利率 | 每日 | T+0 |
| 稅收/利息 | 年度 | 1-2 年 |
| 債務存量 | 季度/年度 | 1 季度 |
| TIC 持有 | 月度 | 2 個月 |

## 資料品質警示

1. **殖利率 vs 財政資料時間不同步**：殖利率為即時，財政為歷史
2. **會計年度差異**：日本財政年度為 4 月～3 月
3. **口徑混用風險**：不同來源可能使用不同定義
4. **預算 vs 決算**：預算數與實際執行數可能有差異

## 緩存策略

本 Skill 使用多層數據抓取與緩存機制：

### 數據源優先級

| 數據類型 | 優先級 1 | 優先級 2 | Fallback |
|----------|----------|----------|----------|
| JGB 殖利率 | FRED CSV | yfinance | 本地緩存/靜態 |
| 財政數據 | config/fiscal_data.json | - | 硬編碼 fallback |
| GDP 數據 | FRED CSV | - | 硬編碼 fallback |
| TIC 持有 | TIC mfh.txt | - | 本地緩存/靜態 |

### 緩存過期時間

| 數據類型 | 緩存位置 | 過期時間 |
|----------|----------|----------|
| JGB 殖利率 | `data/cache/jgb_*.json` | 24 小時 |
| GDP 數據 | `data/cache/gdp_data.json` | 7 天 |
| TIC 持有 | `data/cache/tic_*.json` | 7 天 |
| 財政數據 | `config/fiscal_data.json` | 手動更新 |

### 驗證規則

數據抓取後會進行範圍驗證：

| 數據 | 最小值 | 最大值 |
|------|--------|--------|
| JGB 10Y | -0.5% | 5.0% |
| 稅收 | 50 兆 | 100 兆 |
| 利息支出 | 5 兆 | 35 兆 |
| 債務存量 | 800 兆 | 1500 兆 |
| US GDP | $20T | $40T |
| Japan GDP | $3T | $8T |
| UST 持有 | $500B | $2000B |

### 強制刷新

使用 `--refresh` 參數可忽略緩存強制抓取最新數據：

```bash
python scripts/japan_debt_analyzer.py --quick --refresh
```
