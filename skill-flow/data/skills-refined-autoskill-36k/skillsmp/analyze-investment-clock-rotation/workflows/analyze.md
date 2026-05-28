# Workflow: 完整分析

<required_reading>
**執行前請先閱讀：**
1. references/methodology.md - 投資時鐘模型邏輯
2. references/data-sources.md - 各指標的經濟意義
3. references/input-schema.md - 參數配置
</required_reading>

<process>

## Step 1: 抓取數據

```bash
python scripts/fetch_data.py \
  --earnings CP \
  --fci NFCI \
  --start 2022-01-01 \
  --end 2026-01-19 \
  --output data.json
```

或使用 Python：

```python
from scripts.fetch_data import fetch_fred_series, fetch_all_data

# 抓取所有需要的數據
data = fetch_all_data(
    start_date="2022-01-01",
    end_date="2026-01-19",
    earnings_id="CP",
    fci_id="NFCI"
)
```

## Step 2: 計算獲利成長

```python
from scripts.investment_clock import yoy_growth

# 計算同比成長率
# periods 依據頻率：週頻=52, 月頻=12, 季頻=4
earnings_growth = yoy_growth(data["earnings"], periods=4)  # 季度數據用 4
```

獲利成長計算方法選擇：

| 方法 | 說明 | 適用場景 |
|------|------|----------|
| `yoy` | 年對年成長 | 消除季節性，最常用 |
| `qoq_annualized` | 季對季年化 | 捕捉短期動量 |
| `rolling_4q_yoy` | 滾動四季同比 | 平滑雜訊 |

## Step 3: 計算金融環境 Z-score

```python
from scripts.investment_clock import zscore

# 計算滾動 Z-score
# NFCI 原始定義：正值=緊縮，負值=寬鬆
fci_z = zscore(data["fci"], window=52)  # 52 週視窗

# 若需要反轉方向（讓正值=支持性）
fci_support = -fci_z
```

**方向統一規則**：

| 原始指標 | 原始定義 | transform 設定 |
|----------|----------|----------------|
| NFCI | 正=緊縮 | `inverse=True` 讓正=寬鬆 |
| STLFSI4 | 正=壓力高 | `inverse=True` |
| 自建 FCI | 依定義 | 檢查後設定 |

## Step 4: 對齊頻率

```python
import pandas as pd

# 獲利通常是季度，金融環境是週度
# 需要對齊到共同頻率

# 方法 A：將週度數據重採樣到季度
fci_quarterly = fci_z.resample('Q').last()

# 方法 B：將季度數據擴展到週度（前向填充）
earnings_weekly = earnings_growth.resample('W').ffill()

# 合併
df = pd.DataFrame({
    'earnings_growth': earnings_growth,
    'fci_z': fci_z
}).dropna()
```

## Step 5: 建立座標

```python
from scripts.investment_clock import build_coordinates

# 依據 axis_mapping 建立座標
# 預設：X = financial_conditions, Y = earnings_growth
coords = build_coordinates(
    df,
    x_col='fci_z',
    y_col='earnings_growth',
    invert_x=True  # 若 financial_loose_is_left=True
)

# coords 結構：
# {
#   'x': [...],
#   'y': [...],
#   'dates': [...]
# }
```

## Step 6: 計算象限與時鐘點位

```python
from scripts.investment_clock import calculate_quadrant, clock_hour_from_angle
import numpy as np

# 計算角度
angle = np.arctan2(coords['y'][-1], coords['x'][-1])

# 轉換為時鐘點位
hour = clock_hour_from_angle(angle)

# 判定象限
quadrant = calculate_quadrant(coords['x'][-1], coords['y'][-1])

# quadrant 可能的值：
# - 'Q1_ideal': 獲利↑ & 支持↑
# - 'Q2_mixed': 獲利↑ & 支持↓
# - 'Q3_recovery': 獲利↓ & 支持↑
# - 'Q4_worst': 獲利↓ & 支持↓
```

## Step 7: 計算旋轉方向與幅度

```python
from scripts.investment_clock import analyze_rotation

rotation = analyze_rotation(
    start_angle=angles[0],
    end_angle=angles[-1],
    intermediate_angles=angles[1:-1]
)

# rotation 結構：
# {
#   'from_hour': 2,
#   'to_hour': 10,
#   'direction': 'clockwise',  # 或 'counter_clockwise'
#   'magnitude_degrees': 240,
#   'full_rotations': 0,  # 完整圈數
#   'net_degrees': 240
# }
```

## Step 8: 生成分析報告

```python
result = {
    "skill": "analyze-investment-clock-rotation",
    "as_of": str(df.index[-1].date()),
    "market": "US_EQUITY",
    "window": {
        "start_date": start_date,
        "end_date": end_date,
        "freq": freq
    },
    "axis_mapping_used": {
        "x": "financial_conditions",
        "y": "earnings_growth"
    },
    "current_state": {
        "clock_hour": hour,
        "quadrant": quadrant,
        "quadrant_name": QUADRANT_NAMES[quadrant],
        "x_value": float(coords['x'][-1]),
        "y_value": float(coords['y'][-1]),
        "interpretation": get_quadrant_interpretation(quadrant)
    },
    "rotation_summary": {
        "from_hour": rotation['from_hour'],
        "to_hour": rotation['to_hour'],
        "direction": rotation['direction'],
        "magnitude_degrees": rotation['magnitude_degrees'],
        "magnitude_note": get_magnitude_note(rotation['magnitude_degrees'])
    },
    "time_series": {
        "dates": [str(d.date()) for d in df.index],
        "x": coords['x'].tolist(),
        "y": coords['y'].tolist(),
        "hours": hours.tolist(),
        "quadrants": quadrants
    },
    "metadata": {
        "generated_at": datetime.now().isoformat(),
        "data_sources": {
            "earnings": earnings_series_id,
            "financial_conditions": fci_series_id
        }
    }
}
```

## Step 9: 輸出

```bash
# 輸出到檔案
python scripts/investment_clock.py \
  --start 2022-01-01 \
  --end 2026-01-19 \
  --output result.json

# 或直接輸出到 stdout
python scripts/investment_clock.py --start 2022-01-01 --end 2026-01-19
```

</process>

<success_criteria>
完整分析完成時應產出：

- [ ] 當前時鐘點位（1-12 點）
- [ ] 當前象限與名稱
- [ ] X/Y 軸數值（金融環境 Z-score 與獲利成長）
- [ ] 旋轉方向（順時針/逆時針）
- [ ] 旋轉幅度（度數）
- [ ] 配置建議（依象限解讀）
- [ ] 完整時間序列（若需要視覺化）
- [ ] 資料來源與元數據
</success_criteria>
