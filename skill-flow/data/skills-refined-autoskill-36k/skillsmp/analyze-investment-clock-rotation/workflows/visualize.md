# Workflow: 視覺化

<required_reading>
**執行前請先閱讀：**
1. workflows/analyze.md - 了解如何產生分析數據
</required_reading>

<process>

## Step 1: 準備分析數據

先執行完整分析以取得時間序列數據：

```bash
python scripts/investment_clock.py \
  --start 2022-01-01 \
  --end 2026-01-19 \
  --output analysis.json
```

## Step 2: 執行視覺化

```bash
python scripts/visualize.py \
  -i analysis.json \
  -o output/investment_clock.png \
  --style dark  # 或 light
```

## Step 3: 視覺化腳本說明

```python
# scripts/visualize.py 主要功能

import matplotlib.pyplot as plt
import numpy as np
import json

def plot_investment_clock(data, output_path, style='dark'):
    """
    生成投資時鐘視覺化圖表

    圖表包含：
    1. 極座標時鐘圖（主圖）
    2. 時間序列軌跡
    3. 象限標註
    4. 當前位置標記
    """

    fig = plt.figure(figsize=(14, 10))

    # Panel 1: 極座標時鐘圖
    ax1 = fig.add_subplot(221, projection='polar')
    plot_clock_face(ax1, data)

    # Panel 2: X-Y 散佈圖（笛卡爾座標）
    ax2 = fig.add_subplot(222)
    plot_xy_scatter(ax2, data)

    # Panel 3: 時間序列 - 獲利成長
    ax3 = fig.add_subplot(223)
    plot_earnings_series(ax3, data)

    # Panel 4: 時間序列 - 金融環境
    ax4 = fig.add_subplot(224)
    plot_fci_series(ax4, data)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()


def plot_clock_face(ax, data):
    """繪製極座標時鐘圖"""

    # 繪製時鐘刻度
    for hour in range(1, 13):
        angle = (90 - hour * 30) * np.pi / 180
        ax.annotate(str(hour), xy=(angle, 1.1), ha='center', va='center')

    # 繪製象限背景
    quadrant_colors = {
        'Q1': '#90EE90',  # 淺綠（理想）
        'Q2': '#FFD700',  # 金色（混合）
        'Q3': '#87CEEB',  # 天藍（修復）
        'Q4': '#FFA07A'   # 淺橘（最差）
    }

    # 繪製軌跡
    angles = data['time_series']['angles']
    radii = data['time_series']['radii']
    ax.plot(angles, radii, 'b-', alpha=0.6, linewidth=1)

    # 標記起點和終點
    ax.scatter(angles[0], radii[0], c='green', s=100, marker='o', label='Start')
    ax.scatter(angles[-1], radii[-1], c='red', s=100, marker='*', label='Current')

    ax.set_title('Investment Clock')
    ax.legend(loc='upper right')


def plot_xy_scatter(ax, data):
    """繪製 X-Y 散佈圖"""

    x = data['time_series']['x']
    y = data['time_series']['y']

    # 繪製象限背景
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.axvline(x=0, color='gray', linestyle='--', alpha=0.5)

    # 填充象限顏色
    ax.fill_between([-3, 0], 0, 3, alpha=0.2, color='lightblue', label='Q3 Recovery')
    ax.fill_between([0, 3], 0, 3, alpha=0.2, color='lightgreen', label='Q1 Ideal')
    ax.fill_between([-3, 0], -3, 0, alpha=0.2, color='lightsalmon', label='Q4 Worst')
    ax.fill_between([0, 3], -3, 0, alpha=0.2, color='khaki', label='Q2 Mixed')

    # 繪製軌跡
    ax.plot(x, y, 'b-', alpha=0.6, linewidth=1)

    # 標記起點和終點
    ax.scatter(x[0], y[0], c='green', s=100, marker='o', zorder=5)
    ax.scatter(x[-1], y[-1], c='red', s=100, marker='*', zorder=5)

    # 標註箭頭顯示方向
    for i in range(0, len(x)-1, max(1, len(x)//10)):
        ax.annotate('', xy=(x[i+1], y[i+1]), xytext=(x[i], y[i]),
                    arrowprops=dict(arrowstyle='->', color='blue', alpha=0.3))

    ax.set_xlabel('Financial Conditions (Z-score)\n← Loose | Tight →')
    ax.set_ylabel('Earnings Growth\n← Negative | Positive →')
    ax.set_title('Investment Clock Path')
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-0.3, 0.3)


def plot_earnings_series(ax, data):
    """繪製獲利成長時間序列"""

    dates = data['time_series']['dates']
    y = data['time_series']['y']

    ax.plot(dates, y, 'b-', linewidth=1.5)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.fill_between(dates, y, 0, where=[v > 0 for v in y], alpha=0.3, color='green')
    ax.fill_between(dates, y, 0, where=[v < 0 for v in y], alpha=0.3, color='red')

    ax.set_xlabel('Date')
    ax.set_ylabel('Earnings Growth (YoY)')
    ax.set_title('Earnings Growth Over Time')


def plot_fci_series(ax, data):
    """繪製金融環境時間序列"""

    dates = data['time_series']['dates']
    x = data['time_series']['x']

    ax.plot(dates, x, 'purple', linewidth=1.5)
    ax.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
    ax.fill_between(dates, x, 0, where=[v < 0 for v in x], alpha=0.3, color='green', label='Loose')
    ax.fill_between(dates, x, 0, where=[v > 0 for v in x], alpha=0.3, color='red', label='Tight')

    ax.set_xlabel('Date')
    ax.set_ylabel('Financial Conditions (Z-score)')
    ax.set_title('Financial Conditions Over Time')
    ax.legend()
```

## Step 4: 輸出格式選項

```bash
# PNG（預設）
python scripts/visualize.py -i analysis.json -o chart.png

# SVG（向量格式）
python scripts/visualize.py -i analysis.json -o chart.svg

# HTML（互動式，使用 Plotly）
python scripts/visualize.py -i analysis.json -o chart.html --interactive
```

## Step 5: 自訂樣式

```python
# 可用樣式參數
styles = {
    'dark': {
        'bg_color': '#1a1a2e',
        'text_color': 'white',
        'grid_color': '#444',
        'quadrant_alpha': 0.3
    },
    'light': {
        'bg_color': 'white',
        'text_color': 'black',
        'grid_color': '#ccc',
        'quadrant_alpha': 0.2
    },
    'print': {
        'bg_color': 'white',
        'text_color': 'black',
        'grid_color': 'gray',
        'quadrant_alpha': 0.1
    }
}
```

</process>

<success_criteria>
視覺化完成時應產出：

- [ ] 投資時鐘極座標圖（含軌跡、起終點）
- [ ] X-Y 散佈圖（含象限背景、方向箭頭）
- [ ] 獲利成長時間序列
- [ ] 金融環境時間序列
- [ ] 圖表標題與圖例
- [ ] 輸出檔案（PNG/SVG/HTML）
</success_criteria>
