# JSON 輸出模板

## 完整輸出結構

```json
{
  "skill": "analyze-copper-stock-resilience-dependency",
  "version": "0.1.0",
  "as_of": "2026-01-20",

  "inputs": {
    "start_date": "2020-01-01",
    "end_date": "2026-01-20",
    "freq": "1mo",
    "copper_series": "HG=F (converted to USD/ton)",
    "equity_proxy_series": "ACWI",
    "china_10y_yield_series": "TradingEconomics: China 10Y",
    "ma_window": 60,
    "rolling_window": 24,
    "round_levels": [10000, 13000]
  },

  "data_summary": {
    "total_periods": 72,
    "copper_range": {
      "min": 5800,
      "max": 13200,
      "latest": 12700
    },
    "equity_range": {
      "min": 65.2,
      "max": 120.5,
      "latest": 115.3
    },
    "yield_range": {
      "min": 2.1,
      "max": 3.8,
      "latest": 2.45
    }
  },

  "latest_state": {
    "date": "2026-01-20",
    "copper_price_usd_per_ton": 12700,
    "copper_sma_60": 9261,
    "copper_sma_slope": 42.5,
    "copper_trend": "up",
    "near_resistance_levels": [13000],
    "near_support_levels": [],
    "distance_to_resistance_pct": 2.36,
    "distance_to_support_pct": null,
    "equity_price": 115.3,
    "equity_12m_return": 0.082,
    "equity_above_sma12": true,
    "equity_drawdown_3m": 0.025,
    "equity_resilience_score": 78,
    "china_10y_yield": 2.45,
    "china_yield_zscore_5y": -0.35,
    "china_yield_change_12m": -0.42,
    "rolling_beta_equity_24m": 0.62,
    "rolling_beta_yield_24m": -0.18,
    "rolling_r_squared_24m": 0.45
  },

  "historical_betas": {
    "beta_equity_percentile": 75,
    "beta_equity_mean": 0.48,
    "beta_equity_std": 0.21,
    "beta_yield_percentile": 40,
    "beta_yield_mean": -0.12,
    "beta_yield_std": 0.15
  },

  "backfill_analysis": {
    "events_detected": 8,
    "backfill_events": 3,
    "backfill_probability_12m": {
      "overall": 0.375,
      "equity_resilience_high": 0.20,
      "equity_resilience_low": 0.60
    },
    "events_detail": [
      {
        "touch_date": "2022-03-31",
        "touch_price": 13050,
        "trough_price": 9800,
        "backfill": true,
        "equity_resilience_at_touch": 45
      },
      {
        "touch_date": "2024-05-31",
        "touch_price": 12980,
        "trough_price": 11200,
        "backfill": false,
        "equity_resilience_at_touch": 72
      }
    ]
  },

  "diagnosis": {
    "trend_status": "上升趨勢中，銅價高於 60 月均線且均線斜率為正",
    "level_status": "接近 13,000 關卡（距離 2.36%），為重要阻力位",
    "resilience_status": "股市韌性評分 78，處於高韌性區間",
    "dependency_status": "滾動 β_equity = 0.62，位於歷史 75 分位，銅正被當作風險資產交易",
    "yield_interpretation": "中國10Y殖利率下行（-0.42%），但股市韌性高，偏向寬鬆/流動性敘事",
    "narrative": "銅價接近 13,000 關卡，趨勢仍偏上行，但是否能續航高度依賴股市韌性。當前股市韌性高檔（78），歷史上類似情境的回補機率約 20%。若股市韌性轉弱跌破 50，回補至 10,000 附近的風險將顯著上升。",
    "scenario": "續航機率較高"
  },

  "actionable_flags": [
    {
      "flag": "APPROACHING_RESISTANCE",
      "level": "active",
      "condition": "copper within 5% of 13000",
      "meaning": "接近重要阻力位，關注能否突破"
    },
    {
      "flag": "HIGH_RESILIENCE",
      "level": "active",
      "condition": "equity_resilience_score >= 70",
      "meaning": "股市韌性高，支持突破"
    },
    {
      "flag": "HIGH_BETA_REGIME",
      "level": "active",
      "condition": "beta_equity >= 75th percentile",
      "meaning": "銅正被當作風險資產交易，與股市高度連動"
    }
  ],

  "watch_conditions": [
    {
      "condition": "equity_resilience_score drops below 50",
      "trigger": "WATCH_EQUITY_RESILIENCE",
      "action": "回補風險上升，考慮減碼或設定停損"
    },
    {
      "condition": "copper breaks above 13000 with volume",
      "trigger": "BREAKOUT_CONFIRMATION",
      "action": "突破確認，可考慮追進"
    },
    {
      "condition": "copper drops below 10000",
      "trigger": "SUPPORT_BREACH",
      "action": "支撐跌破，重新評估趨勢"
    }
  ],

  "metadata": {
    "generated_at": "2026-01-20T14:30:00Z",
    "execution_time_seconds": 12.5,
    "data_sources": {
      "copper": "yfinance:HG=F",
      "equity": "yfinance:ACWI",
      "yield": "tradingeconomics:scrape"
    },
    "cache_used": {
      "copper": false,
      "equity": false,
      "yield": true
    }
  }
}
```

---

## 欄位說明

### 頂層欄位

| 欄位 | 類型 | 說明 |
|------|------|------|
| `skill` | string | 技能名稱 |
| `version` | string | 技能版本 |
| `as_of` | string | 分析截止日期 |

### inputs

輸入參數的回顯，便於重現分析。

### data_summary

資料摘要，包含各序列的範圍與最新值。

### latest_state

**核心輸出**，當前狀態的完整資訊：

| 欄位 | 說明 |
|------|------|
| `copper_price_usd_per_ton` | 銅價（USD/ton） |
| `copper_trend` | 趨勢狀態（up/down/range） |
| `near_resistance_levels` | 接近的阻力位列表 |
| `equity_resilience_score` | 股市韌性評分（0-100） |
| `rolling_beta_equity_24m` | 滾動 β 係數（股市） |
| `rolling_beta_yield_24m` | 滾動 β 係數（殖利率） |

### backfill_analysis

回補機率分析：

| 欄位 | 說明 |
|------|------|
| `events_detected` | 偵測到的觸及高關卡事件數 |
| `backfill_probability_12m.overall` | 整體回補機率 |
| `backfill_probability_12m.equity_resilience_high` | 高韌性情境回補機率 |
| `backfill_probability_12m.equity_resilience_low` | 低韌性情境回補機率 |

### diagnosis

**情境判讀**，以自然語言呈現分析結論。

### actionable_flags

**可執行警報旗標**，用於程式化監控：

| Flag | 觸發條件 |
|------|----------|
| `APPROACHING_RESISTANCE` | 接近阻力位 |
| `APPROACHING_SUPPORT` | 接近支撐位 |
| `HIGH_RESILIENCE` | 韌性 >= 70 |
| `LOW_RESILIENCE` | 韌性 <= 30 |
| `HIGH_BETA_REGIME` | β_equity >= 75 分位 |
| `NEGATIVE_BETA_REGIME` | β_equity < 0（銅與股市呈反向關係） |
| `LOW_BETA_ANOMALY` | β_equity <= 10 分位（歷史極端低位） |
| `WATCH_EQUITY_RESILIENCE` | 韌性 < 50 且接近關卡 |

### watch_conditions

後續監控條件，可用於設定警報。

---

## 快速檢查模式輸出（簡化版）

```json
{
  "skill": "analyze-copper-stock-resilience-dependency",
  "as_of": "2026-01-20",
  "quick_check": true,
  "latest_state": {
    "copper_price_usd_per_ton": 12700,
    "copper_trend": "up",
    "near_resistance": [13000],
    "equity_resilience_score": 78,
    "rolling_beta_equity_24m": 0.62
  },
  "quick_diagnosis": "上升趨勢中，接近 13,000 關卡，股市韌性高（78），支持續航",
  "flags": ["APPROACHING_RESISTANCE", "HIGH_RESILIENCE"]
}
```
