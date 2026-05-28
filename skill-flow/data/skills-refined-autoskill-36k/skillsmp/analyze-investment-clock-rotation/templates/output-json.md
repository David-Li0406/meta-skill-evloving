# JSON 輸出模板 (Output JSON Template)

## 完整輸出結構

```json
{
  "skill": "analyze-investment-clock-rotation",
  "version": "0.1.0",
  "as_of": "2026-01-19",

  "market": "US_EQUITY",

  "window": {
    "start_date": "2022-10-01",
    "end_date": "2026-01-19",
    "freq": "weekly"
  },

  "axis_mapping_used": {
    "x": "financial_conditions",
    "y": "earnings_growth"
  },

  "current_state": {
    "clock_hour": 10,
    "quadrant": "Q1_ideal",
    "quadrant_name": "理想象限",
    "x_value": -0.35,
    "y_value": 0.052,
    "interpretation": "獲利成長為正，金融環境偏支持，屬於風險資產相對順風的象限；需監控是否開始往金融環境轉緊或獲利轉弱的方向漂移。"
  },

  "rotation_summary": {
    "from_hour": 2,
    "to_hour": 10,
    "from_quadrant": "Q2_mixed",
    "to_quadrant": "Q1_ideal",
    "direction": "clockwise",
    "magnitude_degrees": 240,
    "full_rotations": 0,
    "magnitude_note": "本輪旋轉幅度中等（240°），屬於典型景氣循環轉換。"
  },

  "quadrant_time_distribution": {
    "Q1_ideal": {
      "periods": 45,
      "percentage": 35.4
    },
    "Q2_mixed": {
      "periods": 30,
      "percentage": 23.6
    },
    "Q3_recovery": {
      "periods": 25,
      "percentage": 19.7
    },
    "Q4_worst": {
      "periods": 27,
      "percentage": 21.3
    }
  },

  "cycle_comparison": {
    "enabled": true,
    "previous_cycle": {
      "period": {
        "start": "2020-01-01",
        "end": "2022-12-31"
      },
      "rotation_magnitude": 540,
      "rotation_character": "large_rotation_after_shock_recovery",
      "note": "屬於「先大幅衰退、再劇烈修復」的路徑，和一般循環的平緩漂移不完全同質。"
    },
    "comparison": {
      "rotation_ratio": 0.44,
      "similar_direction": true,
      "homogeneity": "heterogeneous",
      "interpretation": "當前循環旋轉幅度約為前一輪的 44%，兩者路徑特徵不同，不宜直接套用上一輪經驗。"
    }
  },

  "path_characteristics": {
    "volatility": 1.85,
    "smoothness": "moderate",
    "dominant_trend": "clockwise_drift",
    "reversal_count": 2,
    "max_consecutive_direction": 35
  },

  "implications": {
    "current_quadrant_implication": "偏多風險資產、順風配置",
    "rotation_implication": "順時針旋轉中，可能朝向 Q2（好壞混合）移動",
    "risk_factors": [
      "若金融環境轉緊（X 軸右移），將進入 Q2 估值壓力區",
      "若獲利成長轉負（Y 軸下移），將進入 Q3 修復過渡區"
    ],
    "monitoring_points": [
      "NFCI 是否持續為負",
      "企業利潤季報是否維持正成長"
    ]
  },

  "time_series": {
    "available": true,
    "columns": ["date", "x", "y", "hour", "quadrant", "earnings_growth_raw", "fci_raw"],
    "sample": [
      {
        "date": "2026-01-10",
        "x": -0.32,
        "y": 0.048,
        "hour": 10,
        "quadrant": "Q1_ideal"
      },
      {
        "date": "2026-01-17",
        "x": -0.35,
        "y": 0.052,
        "hour": 10,
        "quadrant": "Q1_ideal"
      }
    ]
  },

  "data_sources": {
    "earnings": {
      "series_id": "CP",
      "name": "Corporate Profits After Tax",
      "latest_date": "2025-09-30",
      "latest_value": 3250.5,
      "growth_method": "yoy"
    },
    "financial_conditions": {
      "series_id": "NFCI",
      "name": "Chicago Fed NFCI",
      "latest_date": "2026-01-17",
      "latest_value": -0.35,
      "transform": "inverse"
    }
  },

  "metadata": {
    "generated_at": "2026-01-19T10:30:00Z",
    "execution_time_ms": 1234,
    "skill_version": "0.1.0",
    "notes": [
      "獲利數據有 1 季延遲（最新為 2025-Q3）",
      "NFCI 週度更新，延遲約 1 週"
    ]
  }
}
```

---

## 欄位說明

### current_state

| 欄位 | 類型 | 說明 |
|------|------|------|
| clock_hour | int | 時鐘點位（1-12） |
| quadrant | string | 象限代碼 |
| quadrant_name | string | 象限中文名稱 |
| x_value | float | X 軸數值（金融環境 Z-score） |
| y_value | float | Y 軸數值（獲利成長率） |
| interpretation | string | 當前位置的解讀 |

### rotation_summary

| 欄位 | 類型 | 說明 |
|------|------|------|
| from_hour | int | 起始時鐘點位 |
| to_hour | int | 結束時鐘點位 |
| direction | string | 旋轉方向（clockwise/counter_clockwise） |
| magnitude_degrees | float | 旋轉度數（絕對值） |
| full_rotations | int | 完整圈數 |
| magnitude_note | string | 幅度說明 |

### quadrant 代碼對照

| 代碼 | 名稱 | 獲利 | 金融環境 |
|------|------|------|----------|
| Q1_ideal | 理想象限 | 正 | 支持 |
| Q2_mixed | 好壞混合 | 正 | 不支持 |
| Q3_recovery | 修復過渡 | 負 | 支持 |
| Q4_worst | 最差象限 | 負 | 不支持 |

### direction 代碼

| 代碼 | 說明 |
|------|------|
| clockwise | 順時針（典型景氣循環） |
| counter_clockwise | 逆時針（非典型/政策干預） |

---

## 精簡輸出（--quick 模式）

```json
{
  "skill": "analyze-investment-clock-rotation",
  "as_of": "2026-01-19",
  "current_position": {
    "clock_hour": 10,
    "quadrant": "Q1_ideal",
    "quadrant_name": "理想象限",
    "earnings_growth": 0.052,
    "financial_conditions_zscore": -0.35
  },
  "interpretation": "理想象限，風險資產相對順風"
}
```

---

## 循環比較輸出

當 `--compare-cycle` 啟用時，額外輸出：

```json
{
  "cycle_comparison": {
    "current_cycle": {
      "period": {"start": "2022-10-01", "end": "2026-01-19"},
      "start_hour": 2,
      "end_hour": 10,
      "rotation_degrees": 240,
      "character": "moderate_drift"
    },
    "previous_cycle": {
      "period": {"start": "2020-01-01", "end": "2022-12-31"},
      "start_hour": 6,
      "end_hour": 12,
      "rotation_degrees": 540,
      "character": "extreme_swing"
    },
    "comparison_summary": {
      "rotation_ratio": 0.44,
      "homogeneity": "heterogeneous",
      "can_apply_previous_experience": false,
      "reason": "前一輪為極端衝擊後的劇烈復甦，當前循環較為平緩"
    }
  }
}
```

---

## 錯誤輸出

```json
{
  "skill": "analyze-investment-clock-rotation",
  "error": true,
  "error_code": "DATA_FETCH_FAILED",
  "error_message": "Failed to fetch NFCI data from FRED",
  "details": {
    "series_id": "NFCI",
    "http_status": 500,
    "retry_count": 3
  },
  "metadata": {
    "generated_at": "2026-01-19T10:30:00Z"
  }
}
```

### 錯誤代碼

| 代碼 | 說明 |
|------|------|
| DATA_FETCH_FAILED | 資料抓取失敗 |
| INVALID_PARAMS | 參數驗證失敗 |
| INSUFFICIENT_DATA | 資料點數不足 |
| CALCULATION_ERROR | 計算錯誤 |
