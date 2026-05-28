# Workflow: 循環比較

<required_reading>
**執行前請先閱讀：**
1. references/methodology.md - 循環比較的意義
2. references/data-sources.md - 確保數據覆蓋所需區間
</required_reading>

<process>

## Step 1: 定義比較區間

```python
# 當前循環
current_cycle = {
    "start": "2022-10-01",
    "end": "2026-01-19",
    "name": "current"
}

# 前一輪循環（如 2020 疫情後復甦）
previous_cycle = {
    "start": "2020-01-01",
    "end": "2022-12-31",
    "name": "covid_recovery"
}
```

## Step 2: 分別計算兩個循環的數據

```python
from scripts.investment_clock import analyze_cycle

# 當前循環
current = analyze_cycle(
    start_date=current_cycle["start"],
    end_date=current_cycle["end"],
    earnings_id="CP",
    fci_id="NFCI"
)

# 前一輪循環
previous = analyze_cycle(
    start_date=previous_cycle["start"],
    end_date=previous_cycle["end"],
    earnings_id="CP",
    fci_id="NFCI"
)
```

## Step 3: 計算循環特徵

```python
from scripts.investment_clock import extract_cycle_features

def extract_cycle_features(cycle_data):
    """提取循環特徵"""
    return {
        # 起終點
        "start_hour": cycle_data["hours"][0],
        "end_hour": cycle_data["hours"][-1],
        "start_quadrant": cycle_data["quadrants"][0],
        "end_quadrant": cycle_data["quadrants"][-1],

        # 旋轉特徵
        "total_rotation_degrees": cycle_data["rotation"]["net_degrees"],
        "direction": cycle_data["rotation"]["direction"],
        "full_rotations": cycle_data["rotation"]["full_rotations"],

        # 極端值
        "max_earnings_growth": max(cycle_data["y"]),
        "min_earnings_growth": min(cycle_data["y"]),
        "max_fci_z": max(cycle_data["x"]),
        "min_fci_z": min(cycle_data["x"]),

        # 象限分布
        "time_in_q1": sum(1 for q in cycle_data["quadrants"] if q == "Q1_ideal"),
        "time_in_q2": sum(1 for q in cycle_data["quadrants"] if q == "Q2_mixed"),
        "time_in_q3": sum(1 for q in cycle_data["quadrants"] if q == "Q3_recovery"),
        "time_in_q4": sum(1 for q in cycle_data["quadrants"] if q == "Q4_worst"),

        # 路徑特徵
        "path_volatility": np.std(cycle_data["hours"]),
        "dominant_direction": "clockwise" if net_rotation > 0 else "counter_clockwise"
    }

current_features = extract_cycle_features(current)
previous_features = extract_cycle_features(previous)
```

## Step 4: 比較分析

```python
def compare_cycles(current_feat, previous_feat):
    """比較兩個循環"""
    comparison = {
        # 旋轉幅度比較
        "rotation_comparison": {
            "current_degrees": current_feat["total_rotation_degrees"],
            "previous_degrees": previous_feat["total_rotation_degrees"],
            "ratio": current_feat["total_rotation_degrees"] / max(previous_feat["total_rotation_degrees"], 1),
            "interpretation": interpret_rotation_difference(
                current_feat["total_rotation_degrees"],
                previous_feat["total_rotation_degrees"]
            )
        },

        # 起終點比較
        "position_comparison": {
            "current_start": current_feat["start_hour"],
            "previous_start": previous_feat["start_hour"],
            "current_end": current_feat["end_hour"],
            "previous_end": previous_feat["end_hour"],
            "similar_endpoint": abs(current_feat["end_hour"] - previous_feat["end_hour"]) <= 2
        },

        # 極端值比較
        "extremes_comparison": {
            "earnings_range_current": current_feat["max_earnings_growth"] - current_feat["min_earnings_growth"],
            "earnings_range_previous": previous_feat["max_earnings_growth"] - previous_feat["min_earnings_growth"],
            "fci_range_current": current_feat["max_fci_z"] - current_feat["min_fci_z"],
            "fci_range_previous": previous_feat["max_fci_z"] - previous_feat["min_fci_z"]
        },

        # 象限時間分布
        "quadrant_distribution": {
            "current": {
                "Q1": current_feat["time_in_q1"],
                "Q2": current_feat["time_in_q2"],
                "Q3": current_feat["time_in_q3"],
                "Q4": current_feat["time_in_q4"]
            },
            "previous": {
                "Q1": previous_feat["time_in_q1"],
                "Q2": previous_feat["time_in_q2"],
                "Q3": previous_feat["time_in_q3"],
                "Q4": previous_feat["time_in_q4"]
            }
        },

        # 同質性判斷
        "homogeneity": {
            "similar_magnitude": abs(current_feat["total_rotation_degrees"] - previous_feat["total_rotation_degrees"]) < 180,
            "similar_direction": current_feat["dominant_direction"] == previous_feat["dominant_direction"],
            "similar_volatility": abs(current_feat["path_volatility"] - previous_feat["path_volatility"]) < 1.0,
            "overall": "homogeneous" if all([...]) else "heterogeneous"
        }
    }

    return comparison

comparison = compare_cycles(current_features, previous_features)
```

## Step 5: 生成比較報告

```json
{
  "skill": "analyze-investment-clock-rotation",
  "mode": "cycle_comparison",
  "as_of": "2026-01-19",

  "cycles": {
    "current": {
      "name": "current",
      "period": {"start": "2022-10-01", "end": "2026-01-19"},
      "features": {
        "start_hour": 2,
        "end_hour": 10,
        "total_rotation": 240,
        "direction": "clockwise",
        "path_character": "moderate_drift"
      }
    },
    "previous": {
      "name": "covid_recovery",
      "period": {"start": "2020-01-01", "end": "2022-12-31"},
      "features": {
        "start_hour": 6,
        "end_hour": 12,
        "total_rotation": 540,
        "direction": "clockwise",
        "path_character": "extreme_swing"
      }
    }
  },

  "comparison": {
    "rotation_comparison": {
      "current_degrees": 240,
      "previous_degrees": 540,
      "ratio": 0.44,
      "interpretation": "當前循環旋轉幅度約為前一輪的一半，屬於較溫和的漂移"
    },
    "homogeneity": {
      "similar_magnitude": false,
      "similar_direction": true,
      "overall": "heterogeneous",
      "note": "兩輪循環不完全同質，前一輪為極端衝擊後的劇烈復甦，當前循環較為平緩"
    }
  },

  "implications": [
    "當前循環與 2020-2022 循環的路徑特徵不同，不宜直接套用上一輪經驗",
    "前一輪因疫情衝擊出現極端旋轉，當前循環更接近典型景氣漂移",
    "若要類比，可參考 2015-2019 的溫和循環特徵"
  ],

  "caveats": [
    "循環比較假設相同的資料來源和計算方法",
    "不同循環的外部環境（政策、事件）可能導致不可比性"
  ]
}
```

## Step 6: 執行比較

```bash
python scripts/investment_clock.py \
  --start 2022-10-01 \
  --end 2026-01-19 \
  --compare-cycle 2020-01-01 2022-12-31 \
  --output comparison.json
```

</process>

<success_criteria>
循環比較完成時應產出：

- [ ] 兩個循環的完整特徵摘要
- [ ] 旋轉幅度比較（度數、比率）
- [ ] 起終點位置比較
- [ ] 極端值範圍比較
- [ ] 象限時間分布比較
- [ ] 同質性判斷（是否可類比）
- [ ] 配置含義與注意事項
- [ ] 不可比的警示（若有）
</success_criteria>
