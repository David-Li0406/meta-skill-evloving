# JSON 輸出模板 (Output JSON Template)

## 完整輸出結構

```json
{
  "skill": "monitor-etf-holdings-drawdown-risk",
  "version": "0.1.0",
  "asof": "2026-01-16",

  "inputs": {
    "etf_ticker": "SLV",
    "commodity_price_symbol": "XAGUSD",
    "divergence_window_days": 180,
    "decade_low_window_days": 3650,
    "min_price_return_pct": 0.15,
    "min_inventory_drawdown_pct": 0.10
  },

  "result": {
    "divergence": true,
    "price_return_window": 0.32,
    "inventory_change_window": -0.18,
    "inventory_decade_low": true,
    "inventory_to_price_ratio_z": -2.4,
    "stress_score_0_100": 78.5,
    "stress_level": "HIGH"
  },

  "latest_values": {
    "price": 32.45,
    "price_date": "2026-01-16",
    "inventory_oz": 456789012,
    "inventory_tonnes": 14203.5,
    "inventory_date": "2026-01-15",
    "ratio": 14073589.2
  },

  "historical_context": {
    "inventory_decade_min": 445000000,
    "inventory_decade_max": 612000000,
    "inventory_percentile": 8.5,
    "ratio_mean": 18500000,
    "ratio_std": 2100000
  },

  "interpretations": [
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
  ],

  "cross_validation": {
    "performed": false,
    "signals_checked": [],
    "physical_tightness_score": null,
    "etf_flow_score": null,
    "dominant_hypothesis": null
  },

  "next_checks": [
    "核對 SLV 官方持倉時間序列是否真為 10 年低點（避免圖表來源/口徑問題）",
    "交叉比對 COMEX registered/eligible 是否同步下降",
    "檢查期貨曲線是否 backwardation 加劇",
    "觀察零售銀條/銀幣 premium 是否擴大"
  ],

  "time_series": {
    "available": true,
    "file": "time_series.csv",
    "columns": [
      "date",
      "price",
      "inventory",
      "price_return",
      "inventory_change",
      "ratio",
      "ratio_z",
      "divergence"
    ]
  },

  "metadata": {
    "generated_at": "2026-01-16T10:30:00Z",
    "execution_time_ms": 2345,
    "data_freshness": {
      "price_data": "2026-01-16",
      "inventory_data": "2026-01-15"
    },
    "warnings": []
  }
}
```

## 欄位說明

### result

| 欄位 | 類型 | 說明 |
|------|------|------|
| divergence | boolean | 是否偵測到背離 |
| price_return_window | float | 視窗期價格變化率 |
| inventory_change_window | float | 視窗期庫存變化率 |
| inventory_decade_low | boolean | 庫存是否處於十年低點 |
| inventory_to_price_ratio_z | float | 庫存/價格比值 Z 分數 |
| stress_score_0_100 | float | 壓力分數（0-100） |
| stress_level | string | 壓力等級（LOW/MEDIUM/HIGH/CRITICAL） |

### stress_level 定義

| 等級 | 分數範圍 | 說明 |
|------|----------|------|
| LOW | 0-30 | 正常，無明顯背離 |
| MEDIUM | 30-60 | 輕度背離，值得關注 |
| HIGH | 60-80 | 中度背離，建議深入驗證 |
| CRITICAL | 80-100 | 重度背離，高度警戒 |

### latest_values

| 欄位 | 類型 | 說明 |
|------|------|------|
| price | float | 最新價格 |
| price_date | string | 價格日期 |
| inventory_oz | int | 庫存（盎司） |
| inventory_tonnes | float | 庫存（噸） |
| inventory_date | string | 庫存日期 |
| ratio | float | 庫存/價格比值 |

### historical_context

| 欄位 | 類型 | 說明 |
|------|------|------|
| inventory_decade_min | int | 十年最低庫存 |
| inventory_decade_max | int | 十年最高庫存 |
| inventory_percentile | float | 當前庫存百分位數 |
| ratio_mean | float | 比值滾動平均 |
| ratio_std | float | 比值滾動標準差 |

### cross_validation（交叉驗證後填入）

| 欄位 | 類型 | 說明 |
|------|------|------|
| performed | boolean | 是否執行交叉驗證 |
| signals_checked | array | 已檢查的訊號清單 |
| physical_tightness_score | float | 實物緊張假設支持度 |
| etf_flow_score | float | ETF 資金流假設支持度 |
| dominant_hypothesis | string | 主導假設 |

## 精簡輸出（--quick 模式）

```json
{
  "skill": "monitor-etf-holdings-drawdown-risk",
  "asof": "2026-01-16",
  "etf_ticker": "SLV",
  "result": {
    "divergence": true,
    "price_return_window": 0.32,
    "inventory_change_window": -0.18,
    "inventory_decade_low": true,
    "stress_score_0_100": 78.5
  },
  "next_checks": [
    "核對 SLV 官方持倉時間序列是否真為 10 年低點",
    "交叉比對 COMEX registered/eligible 是否同步下降"
  ]
}
```

## 監控模式輸出

```json
{
  "skill": "monitor-etf-holdings-drawdown-risk",
  "mode": "monitor",
  "timestamp": "2026-01-16T10:30:00Z",

  "summary": {
    "total_monitored": 4,
    "critical_alerts": 1,
    "warning_alerts": 1,
    "normal": 2
  },

  "alerts": [
    {
      "etf": "SLV",
      "level": "CRITICAL",
      "stress_score": 78.5,
      "divergence": true,
      "message": "iShares Silver Trust: stress=78.5, divergence=true"
    },
    {
      "etf": "PSLV",
      "level": "WARNING",
      "stress_score": 52.3,
      "divergence": true,
      "message": "Sprott Physical Silver: stress=52.3, divergence=true"
    }
  ],

  "details": [
    {
      "etf_ticker": "SLV",
      "stress_score_0_100": 78.5,
      "divergence": true
    },
    {
      "etf_ticker": "PSLV",
      "stress_score_0_100": 52.3,
      "divergence": true
    },
    {
      "etf_ticker": "GLD",
      "stress_score_0_100": 15.2,
      "divergence": false
    },
    {
      "etf_ticker": "PHYS",
      "stress_score_0_100": 12.8,
      "divergence": false
    }
  ]
}
```

## 錯誤輸出

```json
{
  "skill": "monitor-etf-holdings-drawdown-risk",
  "error": true,
  "error_code": "DATA_FETCH_FAILED",
  "error_message": "無法抓取 SLV 持倉數據：選擇器失效，請檢查網站結構",
  "suggestions": [
    "確認 iShares 官網是否可正常訪問",
    "檢查 Selenium 爬蟲選擇器是否需要更新",
    "嘗試使用替代數據源"
  ],
  "metadata": {
    "generated_at": "2026-01-16T10:30:00Z",
    "failed_at_step": "fetch_etf_holdings"
  }
}
```
