# Workflow: 完整背離分析

<required_reading>
**執行前請先閱讀：**
1. references/input-schema.md - 完整參數定義
2. references/methodology.md - 背離偵測方法論
3. references/data-sources.md - 數據來源與抓取方式
</required_reading>

<process>

## Step 1: 確認參數

檢查用戶提供的參數，補充預設值：

```python
params = {
    "etf_ticker": "SLV",              # ETF 代碼（必填）
    "commodity_price_symbol": "XAGUSD",  # 商品價格代碼（必填）
    "start_date": None,               # 預設 10 年前
    "end_date": "today",              # 分析結束日
    "inventory_field": "auto",        # 庫存欄位（自動偵測）
    "decade_low_window_days": 3650,   # 十年低點視窗
    "divergence_window_days": 180,    # 背離計算視窗
    "min_price_return_pct": 0.15,     # 價格上漲門檻
    "min_inventory_drawdown_pct": 0.10,  # 庫存下滑門檻
}
```

若用戶有指定參數，覆蓋上述預設值。

## Step 2: 抓取價格數據

使用 `scripts/fetch_prices.py` 抓取商品價格：

```bash
python scripts/fetch_prices.py \
  --symbol {commodity_price_symbol} \
  --start {start_date} \
  --end {end_date} \
  --output prices.csv
```

或使用 Python API：

```python
from scripts.fetch_prices import fetch_price_series

price = fetch_price_series(
    symbol=params["commodity_price_symbol"],
    start_date=params["start_date"],
    end_date=params["end_date"]
)
```

## Step 3: 抓取 ETF 庫存數據

使用 `scripts/fetch_etf_holdings.py` 抓取 ETF 持倉：

```bash
python scripts/fetch_etf_holdings.py \
  --etf {etf_ticker} \
  --start {start_date} \
  --end {end_date} \
  --output holdings.csv
```

**注意**：此腳本使用 Selenium 模擬瀏覽器行為，需要：
- Chrome 瀏覽器已安裝
- webdriver-manager 自動管理 ChromeDriver
- 隨機延遲與 User-Agent 輪換（防偵測）

或使用 Python API：

```python
from scripts.fetch_etf_holdings import fetch_etf_inventory_series

inventory = fetch_etf_inventory_series(
    etf_ticker=params["etf_ticker"],
    start_date=params["start_date"],
    end_date=params["end_date"]
)
```

## Step 4: 對齊與清洗數據

```python
import pandas as pd

# 合併價格與庫存
df = pd.concat({"price": price, "inv": inventory}, axis=1).sort_index()

# 庫存前向填充（庫存不是每日更新）
df["inv"] = df["inv"].ffill()

# 移除缺失值
df = df.dropna(subset=["price", "inv"])
```

## Step 5: 計算背離特徵

```python
w = params["divergence_window_days"]

# 視窗期變化率
df["price_ret"] = df["price"].pct_change(w)
df["inv_chg"] = df["inv"].pct_change(w)

# 十年低點判定
df["inv_decade_min"] = df["inv"].rolling(
    params["decade_low_window_days"],
    min_periods=252
).min()
df["decade_low_flag"] = df["inv"] <= df["inv_decade_min"] * 1.001

# 庫存/價格比值 Z 分數
df["ratio"] = df["inv"] / df["price"]
ratio_mean = df["ratio"].rolling(params["decade_low_window_days"], min_periods=252).mean()
ratio_std = df["ratio"].rolling(params["decade_low_window_days"], min_periods=252).std()
df["ratio_z"] = (df["ratio"] - ratio_mean) / ratio_std

# 背離判定
df["divergence"] = (
    (df["price_ret"] >= params["min_price_return_pct"]) &
    (df["inv_chg"] <= -params["min_inventory_drawdown_pct"])
)
```

## Step 6: 計算壓力分數

```python
latest = df.iloc[-1]

# 背離嚴重度
divergence_severity = max(0, latest["price_ret"]) * max(0, -latest["inv_chg"])

# 十年低點加成
decade_low_bonus = 1.0 if latest["decade_low_flag"] else 0.0

# 比值極端加成
ratio_extreme_bonus = 1.0 if latest["ratio_z"] < -2 else 0.0

# 壓力分數
stress_score = 100 * min(1.0,
    0.6 * divergence_severity +
    0.2 * decade_low_bonus +
    0.2 * ratio_extreme_bonus
)
```

## Step 7: 產生雙重假設解釋

根據背離狀態產生兩種對立假設：

```python
interpretations = [
    {
        "name": "Physical Tightness Hypothesis",
        "when_supported": "若交易所/金庫庫存同步下降、期貨 backwardation 變強、lease rates 上升、零售溢價擴大",
        "note": "這才比較接近社群敘事所說的「實物吃緊/被抽走」。"
    },
    {
        "name": "ETF Flow / Redemption Hypothesis",
        "when_supported": "若其他實物緊張指標不跟，較可能是投資人資金外流或贖回機制所致",
        "note": "ETF 持倉下降不必然等同「銀行搶銀條」。"
    }
]
```

## Step 8: 產生下一步檢查建議

```python
next_checks = [
    f"拉 {params['etf_ticker']} 官方 holdings/bar list 歷史，確認是否真為十年低點",
    "比對 COMEX registered/eligible 是否同步下降",
    "檢查期貨曲線是否 backwardation 加劇",
    "觀察零售銀條/銀幣 premium 是否擴大"
]
```

## Step 9: 輸出結果

依據 `output_format` 參數產出結果：

- JSON 格式：參考 `templates/output-json.md`
- Markdown 格式：參考 `templates/output-markdown.md`

```bash
python scripts/divergence_detector.py \
  --etf {etf_ticker} \
  --commodity {commodity_price_symbol} \
  --start {start_date} \
  --end {end_date} \
  --output result.json
```

## Step 10: 生成視覺化報告（可選）

使用 `visualize_divergence.py` 生成完整的圖表報告：

```bash
python scripts/visualize_divergence.py \
  --result result.json \
  --output ../../../output/
```

**輸出內容**：
- PNG 圖表（高解析度 300 DPI）
- PDF 報告
- 包含：價格-庫存時間序列、壓力分數儀表盤、關鍵指標表格

**檔名格式**：`{ETF}_divergence_report_{YYYYMMDD}.png`

</process>

<success_criteria>
分析完成時應產出：

- [ ] 背離狀態判定（divergence: true/false）
- [ ] 價格變化率與庫存變化率
- [ ] 十年低點判定
- [ ] 庫存/價格比值 Z 分數
- [ ] 壓力分數（0-100）
- [ ] 兩種對立假設解釋
- [ ] 下一步驗證建議清單
- [ ] 結果輸出為指定格式
- [ ] **視覺化報告**（PNG + PDF）
</success_criteria>
