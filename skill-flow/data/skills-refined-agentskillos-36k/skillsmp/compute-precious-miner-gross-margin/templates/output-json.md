# JSON 輸出模板

## 完整輸出結構

```json
{
  "skill": "compute_precious_miner_margin_proxy",
  "generated_at": "2025-01-15T10:30:00Z",
  "version": "0.1.0",

  "parameters": {
    "metal": "gold",
    "miners": ["NEM", "GOLD", "AEM"],
    "start_date": "2015-01-01",
    "end_date": "2025-01-15",
    "frequency": "quarterly",
    "cost_metric": "AISC",
    "aggregation": "production_weighted",
    "price_series": "spot",
    "history_window_years": 20
  },

  "data_sources": {
    "metal_price": {
      "source": "Yahoo Finance (GC=F)",
      "last_update": "2025-01-15"
    },
    "miner_costs": {
      "source": "Company IR / Earnings Releases",
      "last_update": "2025-01-10",
      "coverage": {
        "NEM": "2015-Q1 to 2024-Q4",
        "GOLD": "2015-Q1 to 2024-Q4",
        "AEM": "2015-Q1 to 2024-Q4"
      }
    }
  },

  "basket": {
    "miners": ["NEM", "GOLD", "AEM"],
    "aggregation": "production_weighted",
    "weights": {
      "NEM": 0.45,
      "GOLD": 0.35,
      "AEM": 0.20
    }
  },

  "latest": {
    "date": "2024-Q4",
    "metal_price_usd_oz": 2650.0,
    "unit_cost_proxy_usd_oz": 1320.0,
    "gross_margin_proxy": 0.502,
    "history_percentile": 0.78,
    "regime_label": "high_margin"
  },

  "miner_details": [
    {
      "ticker": "NEM",
      "name": "Newmont",
      "latest_quarter": "2024-Q4",
      "aisc_usd_oz": 1350.0,
      "production_oz": 1600000,
      "margin_proxy": 0.491,
      "margin_vs_basket": -0.011
    },
    {
      "ticker": "GOLD",
      "name": "Barrick Gold",
      "latest_quarter": "2024-Q4",
      "aisc_usd_oz": 1290.0,
      "production_oz": 1200000,
      "margin_proxy": 0.513,
      "margin_vs_basket": 0.011
    },
    {
      "ticker": "AEM",
      "name": "Agnico Eagle",
      "latest_quarter": "2024-Q4",
      "aisc_usd_oz": 1310.0,
      "production_oz": 900000,
      "margin_proxy": 0.506,
      "margin_vs_basket": 0.004
    }
  ],

  "history": {
    "summary": {
      "min_margin": 0.15,
      "max_margin": 0.65,
      "mean_margin": 0.38,
      "median_margin": 0.40,
      "std_margin": 0.12,
      "current_zscore": 1.02
    },
    "time_series": [
      {"date": "2015-Q1", "margin": 0.22, "percentile": 0.15},
      {"date": "2015-Q2", "margin": 0.25, "percentile": 0.20}
    ]
  },

  "decomposition": {
    "lookback_quarters": 3,
    "price_change_pct": 0.12,
    "cost_change_pct": -0.03,
    "margin_change_pct": 0.08,
    "driver": "mostly_price_up",
    "interpretation": "毛利改善主要由金價上漲驅動（+12%），成本小幅下降（-3%）"
  },

  "regime_analysis": {
    "current_regime": "high_margin",
    "percentile_rank": 0.78,
    "time_in_current_regime": "3 quarters",
    "regime_transitions": [
      {"date": "2024-Q2", "from": "neutral", "to": "high_margin"}
    ],
    "historical_avg_duration": {
      "extreme_high_margin": "2.5 quarters",
      "high_margin": "4 quarters",
      "neutral": "6 quarters",
      "low_margin": "3 quarters",
      "extreme_low_margin": "2 quarters"
    }
  },

  "signals": {
    "regime_signal": {
      "signal": "HIGH_MARGIN",
      "strength": 0.56,
      "interpretation": "毛利處於歷史高檔（78 百分位），但未達極端"
    },
    "driver_signal": {
      "signal": "PRICE_DRIVEN_RALLY",
      "quality": "MEDIUM",
      "interpretation": "毛利改善依賴金價，需關注價格回調風險"
    },
    "capital_cycle_signal": {
      "phase": "MID_EXPANSION",
      "interpretation": "毛利較高，資本開支可能升溫"
    }
  },

  "notes": [
    "gross_margin_proxy 使用 (price - AISC)/price 作為近似；不等同會計報表的毛利率口徑。",
    "成本為季度資料，已以同季均價對齊。",
    "歷史分位數基於 20 年滾動視窗計算。"
  ],

  "recommended_next_checks": [
    "用同一套 margin proxy 對照 GDX/GDXJ 的 3/6/12 個月前瞻報酬（事件研究）",
    "檢查是否出現資本開支/併購升溫",
    "監控成本通膨壓力（柴油/工資/試劑）",
    "比較個別礦業的相對毛利強弱"
  ],

  "disclaimers": [
    "本分析僅供研究參考，不構成投資建議。",
    "毛利率代理值為估算值，與會計報表數字可能存在差異。",
    "成本數據基於公開資料，可能存在滯後或不完整。"
  ]
}
```

## 欄位說明

### 頂層欄位

| 欄位                      | 類型   | 說明                     |
|---------------------------|--------|--------------------------|
| `skill`                   | string | 技能識別符               |
| `generated_at`            | string | 報告生成時間（ISO 8601） |
| `version`                 | string | 技能版本號               |
| `parameters`              | object | 輸入參數                 |
| `data_sources`            | object | 數據來源資訊             |
| `basket`                  | object | 籃子定義                 |
| `latest`                  | object | 最新數據摘要             |
| `miner_details`           | array  | 各礦業詳情               |
| `history`                 | object | 歷史統計                 |
| `decomposition`           | object | 驅動拆解                 |
| `regime_analysis`         | object | 區間分析                 |
| `signals`                 | object | 生成的訊號               |
| `notes`                   | array  | 備註說明                 |
| `recommended_next_checks` | array  | 後續建議                 |
| `disclaimers`             | array  | 免責聲明                 |

### latest 欄位

| 欄位                     | 類型   | 說明                     |
|--------------------------|--------|--------------------------|
| `date`                   | string | 最新數據日期（季度格式） |
| `metal_price_usd_oz`     | number | 金屬價格（USD/oz）       |
| `unit_cost_proxy_usd_oz` | number | 加權平均成本（USD/oz）   |
| `gross_margin_proxy`     | number | 毛利率代理值（0-1）      |
| `history_percentile`     | number | 歷史分位數（0-1）        |
| `regime_label`           | string | 區間標記                 |

### regime_label 可能值

| 值                    | 分位數範圍 | 說明       |
|-----------------------|------------|------------|
| `extreme_high_margin` | ≥ 0.9      | 極端高毛利 |
| `high_margin`         | 0.7 - 0.9  | 高毛利     |
| `neutral`             | 0.3 - 0.7  | 中等       |
| `low_margin`          | 0.1 - 0.3  | 低毛利     |
| `extreme_low_margin`  | < 0.1      | 極端低毛利 |

### decomposition.driver 可能值

| 值                  | 說明               |
|---------------------|--------------------|
| `mostly_price_up`   | 主要由價格上漲驅動 |
| `mostly_price_down` | 主要由價格下跌驅動 |
| `mostly_cost_down`  | 主要由成本下降驅動 |
| `mostly_cost_up`    | 主要由成本上升驅動 |
| `mixed`             | 價格與成本同時變化 |

---

## 精簡輸出

若只需核心數據，可使用 `--compact` 參數：

```json
{
  "skill": "compute_precious_miner_margin_proxy",
  "metal": "gold",
  "date": "2024-Q4",
  "basket_margin": 0.502,
  "percentile": 0.78,
  "regime": "high_margin",
  "driver": "mostly_price_up"
}
```
