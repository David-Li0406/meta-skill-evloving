# Workflow: 交叉驗證背離訊號

<required_reading>
**執行前請先閱讀：**
1. references/methodology.md - 雙重假設驗證框架
2. references/data-sources.md - 交叉驗證數據來源
</required_reading>

<process>

## Step 1: 確認需要驗證的背離訊號

確認已有背離分析結果：

```python
# 假設已執行 analyze.md 工作流
# 或直接讀取先前的分析結果
import json

with open("result.json") as f:
    divergence_result = json.load(f)

# 確認存在背離
if not divergence_result.get("divergence"):
    print("未偵測到背離，無需交叉驗證")
    exit()
```

## Step 2: 定義驗證指標

```python
validation_signals = {
    "supports_physical_tightness": [
        {
            "name": "comex_inventory",
            "description": "COMEX registered/eligible 庫存下降",
            "weight": 0.25
        },
        {
            "name": "futures_backwardation",
            "description": "期貨曲線從 contango 轉為 backwardation",
            "weight": 0.25
        },
        {
            "name": "lease_rates",
            "description": "白銀/黃金 lease rates 上升",
            "weight": 0.20
        },
        {
            "name": "retail_premiums",
            "description": "零售銀條/銀幣溢價擴大",
            "weight": 0.15
        },
        {
            "name": "lbma_vault",
            "description": "LBMA 金庫存量下降",
            "weight": 0.15
        }
    ],
    "supports_etf_flow": [
        {
            "name": "comex_stable",
            "description": "COMEX 庫存穩定或上升",
            "weight": 0.25
        },
        {
            "name": "futures_contango",
            "description": "期貨曲線維持 contango",
            "weight": 0.25
        },
        {
            "name": "retail_premiums_stable",
            "description": "零售溢價平穩",
            "weight": 0.25
        },
        {
            "name": "fund_flows_negative",
            "description": "ETF 資金流數據顯示淨流出",
            "weight": 0.25
        }
    ]
}
```

## Step 3: 檢查 COMEX 庫存

抓取 COMEX registered/eligible 庫存數據：

```python
# COMEX 庫存數據通常需要從 CME 網站抓取
# 或使用第三方彙總數據

def check_comex_inventory():
    """
    檢查 COMEX 白銀/黃金庫存變化
    返回：'declining', 'stable', 'increasing'
    """
    # 實作：抓取 COMEX daily stocks report
    # https://www.cmegroup.com/clearing/operations-and-deliveries/nymex-delivery-notices.html

    # 簡化範例：手動輸入或抓取
    comex_change = -0.05  # 假設下降 5%

    if comex_change < -0.03:
        return "declining"
    elif comex_change > 0.03:
        return "increasing"
    else:
        return "stable"
```

## Step 4: 檢查期貨曲線結構

```python
import yfinance as yf

def check_futures_curve(commodity="SI"):
    """
    檢查期貨曲線是 contango 還是 backwardation
    SI = 白銀, GC = 黃金
    """
    # 抓取近月與遠月期貨
    front_month = yf.Ticker(f"{commodity}=F")
    back_month = yf.Ticker(f"{commodity}H25.CME")  # 需要動態計算

    front_price = front_month.history(period="1d")["Close"].iloc[-1]
    back_price = back_month.history(period="1d")["Close"].iloc[-1]

    spread = (back_price - front_price) / front_price

    if spread < -0.005:  # 遠月低於近月超過 0.5%
        return "backwardation"
    elif spread > 0.005:
        return "contango"
    else:
        return "flat"
```

## Step 5: 檢查零售溢價

```python
def check_retail_premiums():
    """
    檢查零售銀條/銀幣相對現貨的溢價
    通常需要從 APMEX、JM Bullion 等零售商抓取
    """
    # 簡化範例：使用固定值或手動輸入
    # 正常溢價約 3-5%，緊張時可達 10-20%

    current_premium = 0.08  # 假設 8%
    normal_premium = 0.05   # 正常水準 5%

    if current_premium > normal_premium * 1.5:
        return "elevated"
    else:
        return "normal"
```

## Step 6: 計算驗證分數

```python
def calculate_validation_scores(signals_status):
    """
    計算兩種假設的支持度
    """
    physical_score = 0
    etf_flow_score = 0

    # Physical Tightness 假設
    for signal in validation_signals["supports_physical_tightness"]:
        status = signals_status.get(signal["name"])
        if status == "supports":
            physical_score += signal["weight"]

    # ETF Flow 假設
    for signal in validation_signals["supports_etf_flow"]:
        status = signals_status.get(signal["name"])
        if status == "supports":
            etf_flow_score += signal["weight"]

    return {
        "physical_tightness_score": physical_score,
        "etf_flow_score": etf_flow_score,
        "dominant_hypothesis": "physical_tightness" if physical_score > etf_flow_score else "etf_flow"
    }
```

## Step 7: 執行完整驗證

```python
# 收集所有訊號狀態
signals_status = {}

# COMEX 庫存
comex = check_comex_inventory()
if comex == "declining":
    signals_status["comex_inventory"] = "supports"
    signals_status["comex_stable"] = "contradicts"
elif comex == "stable":
    signals_status["comex_inventory"] = "contradicts"
    signals_status["comex_stable"] = "supports"

# 期貨曲線
curve = check_futures_curve()
if curve == "backwardation":
    signals_status["futures_backwardation"] = "supports"
    signals_status["futures_contango"] = "contradicts"
elif curve == "contango":
    signals_status["futures_backwardation"] = "contradicts"
    signals_status["futures_contango"] = "supports"

# 零售溢價
premium = check_retail_premiums()
if premium == "elevated":
    signals_status["retail_premiums"] = "supports"
    signals_status["retail_premiums_stable"] = "contradicts"
else:
    signals_status["retail_premiums"] = "contradicts"
    signals_status["retail_premiums_stable"] = "supports"

# 計算分數
validation_result = calculate_validation_scores(signals_status)
```

## Step 8: 產出驗證報告

```python
cross_validation_report = {
    "original_divergence": divergence_result,
    "validation_signals": signals_status,
    "scores": validation_result,
    "conclusion": {
        "dominant_hypothesis": validation_result["dominant_hypothesis"],
        "confidence": max(
            validation_result["physical_tightness_score"],
            validation_result["etf_flow_score"]
        ),
        "recommendation": get_recommendation(validation_result)
    }
}

def get_recommendation(result):
    if result["physical_tightness_score"] > 0.6:
        return "多重指標支持實物緊張假設，建議密切關注供需動態"
    elif result["etf_flow_score"] > 0.6:
        return "較可能是 ETF 資金流動所致，非實物短缺"
    else:
        return "訊號混合，建議繼續監控等待更多數據"
```

</process>

<success_criteria>
交叉驗證完成時應產出：

- [ ] 已檢查 COMEX 庫存狀態
- [ ] 已檢查期貨曲線結構
- [ ] 已檢查零售溢價水準
- [ ] 計算兩種假設的支持分數
- [ ] 判定主導假設
- [ ] 提供信心水準與建議
- [ ] 產出完整驗證報告
</success_criteria>
