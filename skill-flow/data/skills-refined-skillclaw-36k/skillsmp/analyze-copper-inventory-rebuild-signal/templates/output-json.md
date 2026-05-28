<overview>
銅庫存回補訊號分析的 JSON 輸出格式規範。
</overview>

<schema>

```json
{
  "asof": "YYYY-MM-DD",
  "status": "success | partial | error",
  "confidence": 0.0-1.0,

  "latest": {
    "shfe_inventory_tonnes": 235000,
    "shfe_rebuild_z": 1.9,
    "shfe_inventory_percentile": 0.87,
    "copper_price": 4.52,
    "price_percentile": 0.32,
    "near_term_signal": "CAUTION | NEUTRAL | SUPPORTIVE",
    "long_term_view": "CHEAP | FAIR | RICH",
    "high_inventory": true,
    "fast_rebuild": true
  },

  "backtest": {
    "peak_match_window_weeks": 2,
    "signal_count": 21,
    "hit_count": 13,
    "signal_to_local_peak_hit_rate": 0.62
  },

  "drivers": {
    "shfe_inventory_tonnes": 235000,
    "shfe_rebuild_window_weeks": 4,
    "shfe_rebuild_z": 1.9,
    "high_inventory_rule": "percentile>=0.85"
  },

  "long_term": {
    "window_years": 10,
    "price_percentile": 0.32,
    "cheap_threshold": 0.35,
    "rich_threshold": 0.65,
    "long_term_view": "CHEAP"
  },

  "metadata": {
    "data_sources": {
      "shfe_inventory": "MacroMicro (CDP)",
      "copper_price": "Yahoo Finance (HG=F)"
    },
    "shfe_data_range": {
      "start": "2015-01-01",
      "end": "2026-01-26"
    },
    "price_data_range": {
      "start": "2015-01-01",
      "end": "2026-01-26"
    },
    "analyzed_at": "2026-01-26T10:30:00Z"
  },

  "config": {
    "fast_rebuild_window_weeks": 4,
    "fast_rebuild_z": 1.5,
    "z_baseline_weeks": 156,
    "high_inventory_mode": "percentile",
    "high_inventory_percentile": 0.85,
    "peak_match_window_weeks": 2,
    "long_term_window_years": 10,
    "cheap_percentile": 0.35,
    "rich_percentile": 0.65
  },

  "reasons": [
    "SHFE 庫存 235,000 噸，處於 87% 分位數（偏高）",
    "4 週回補速度 z-score +1.9，超過 1.5 門檻（異常快）",
    "歷史同類訊號命中率 62%",
    "銅價 10 年分位數 32%，處於「偏便宜」區間"
  ],

  "artifacts": [
    {
      "type": "chart",
      "path": "output/copper_inventory_signal.png",
      "description": "Bloomberg 風格銅庫存回補訊號圖表"
    },
    {
      "type": "data",
      "path": "cache/shfe_inventory.csv",
      "description": "SHFE 庫存時序數據"
    }
  ]
}
```

</schema>

<field_descriptions>

**頂層欄位**

| 欄位 | 類型 | 說明 |
|------|------|------|
| asof | string | 數據截止日期 |
| status | enum | 執行狀態：success, partial, error |
| confidence | float | 信心水準（0-1） |

**latest 區塊**

| 欄位 | 類型 | 說明 |
|------|------|------|
| shfe_inventory_tonnes | number | SHFE 庫存量（噸） |
| shfe_rebuild_z | number | 回補速度 z-score |
| shfe_inventory_percentile | number | 庫存水位分位數（0-1） |
| copper_price | number | 銅價（USD/lb） |
| price_percentile | number | 價格分位數（0-1） |
| near_term_signal | enum | 短期訊號 |
| long_term_view | enum | 長期判讀 |
| high_inventory | boolean | 是否庫存偏高 |
| fast_rebuild | boolean | 是否快速回補 |

**backtest 區塊**

| 欄位 | 類型 | 說明 |
|------|------|------|
| peak_match_window_weeks | number | 局部高點匹配窗口（週） |
| signal_count | number | 歷史訊號觸發次數 |
| hit_count | number | 命中次數 |
| signal_to_local_peak_hit_rate | number | 命中率 |

**reasons 陣列**

人類可讀的結論依據清單，用於快速理解分析結論。

**artifacts 陣列**

分析產出的檔案清單，包含圖表和數據檔案。

</field_descriptions>

<example>

```json
{
  "asof": "2026-01-26",
  "status": "success",
  "confidence": 0.75,
  "latest": {
    "shfe_inventory_tonnes": 235000,
    "shfe_rebuild_z": 1.9,
    "shfe_inventory_percentile": 0.87,
    "copper_price": 4.52,
    "price_percentile": 0.32,
    "near_term_signal": "CAUTION",
    "long_term_view": "CHEAP",
    "high_inventory": true,
    "fast_rebuild": true
  },
  "backtest": {
    "peak_match_window_weeks": 2,
    "signal_count": 21,
    "hit_count": 13,
    "signal_to_local_peak_hit_rate": 0.62
  },
  "drivers": {
    "shfe_inventory_tonnes": 235000,
    "shfe_rebuild_window_weeks": 4,
    "shfe_rebuild_z": 1.9,
    "high_inventory_rule": "percentile>=0.85"
  },
  "long_term": {
    "window_years": 10,
    "price_percentile": 0.32,
    "long_term_view": "CHEAP"
  },
  "reasons": [
    "SHFE 庫存 235,000 噸，處於 87% 分位數（偏高）",
    "4 週回補速度 z-score +1.9，超過 1.5 門檻（異常快）",
    "歷史同類訊號命中率 62%",
    "銅價 10 年分位數 32%，處於「偏便宜」區間"
  ]
}
```

</example>
