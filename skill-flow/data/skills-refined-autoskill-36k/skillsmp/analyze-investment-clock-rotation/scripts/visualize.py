#!/usr/bin/env python3
"""
Investment Clock Visualizer
投資時鐘視覺化工具
"""

import argparse
import json
import sys
from typing import Any, Dict

import numpy as np

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("Warning: matplotlib not installed. Visualization disabled.", file=sys.stderr)


# ============================================================================
# 視覺化函數
# ============================================================================


def plot_investment_clock(
    data: Dict[str, Any],
    output_path: str,
    style: str = "light",
) -> None:
    """
    生成投資時鐘視覺化圖表

    Args:
        data: 分析結果數據
        output_path: 輸出檔案路徑
        style: 風格（light/dark）
    """
    if not HAS_MATPLOTLIB:
        print("Error: matplotlib required for visualization", file=sys.stderr)
        return

    # 設定風格
    if style == "dark":
        plt.style.use("dark_background")
        bg_color = "#1a1a2e"
        text_color = "white"
        grid_alpha = 0.3
    else:
        plt.style.use("default")
        bg_color = "white"
        text_color = "black"
        grid_alpha = 0.5

    # 建立圖表
    fig = plt.figure(figsize=(14, 10))
    fig.patch.set_facecolor(bg_color)

    # Panel 1: X-Y 散佈圖（主圖）
    ax1 = fig.add_subplot(221)
    plot_xy_scatter(ax1, data, text_color, grid_alpha)

    # Panel 2: 極座標時鐘圖
    ax2 = fig.add_subplot(222, projection="polar")
    plot_clock_face(ax2, data, text_color)

    # Panel 3: 獲利成長時間序列
    ax3 = fig.add_subplot(223)
    plot_earnings_series(ax3, data, text_color, grid_alpha)

    # Panel 4: 金融環境時間序列
    ax4 = fig.add_subplot(224)
    plot_fci_series(ax4, data, text_color, grid_alpha)

    # 標題
    fig.suptitle(
        f"Investment Clock Analysis - {data.get('as_of', 'N/A')}",
        fontsize=14,
        color=text_color,
        fontweight="bold",
    )

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=bg_color)
    plt.close()

    print(f"Chart saved to {output_path}", file=sys.stderr)


def plot_xy_scatter(
    ax: plt.Axes,
    data: Dict[str, Any],
    text_color: str,
    grid_alpha: float,
) -> None:
    """繪製 X-Y 散佈圖"""
    ts = data.get("time_series", {})
    x = ts.get("x", [])
    y = ts.get("y", [])

    if not x or not y:
        ax.text(
            0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes
        )
        return

    # 繪製象限背景
    ax.axhline(y=0, color="gray", linestyle="--", alpha=grid_alpha)
    ax.axvline(x=0, color="gray", linestyle="--", alpha=grid_alpha)

    # 填充象限顏色
    xlim = max(abs(min(x)), abs(max(x))) * 1.2
    ylim = max(abs(min(y)), abs(max(y))) * 1.2

    ax.fill_between(
        [-xlim, 0], 0, ylim, alpha=0.15, color="lightgreen", label="Q1 Ideal"
    )
    ax.fill_between(
        [0, xlim], 0, ylim, alpha=0.15, color="khaki", label="Q2 Mixed"
    )
    ax.fill_between(
        [-xlim, 0], -ylim, 0, alpha=0.15, color="lightblue", label="Q3 Recovery"
    )
    ax.fill_between(
        [0, xlim], -ylim, 0, alpha=0.15, color="lightsalmon", label="Q4 Worst"
    )

    # 繪製軌跡
    ax.plot(x, y, "b-", alpha=0.6, linewidth=1.5)

    # 標記起點和終點
    ax.scatter(x[0], y[0], c="green", s=100, marker="o", zorder=5, label="Start")
    ax.scatter(x[-1], y[-1], c="red", s=150, marker="*", zorder=5, label="Current")

    # 繪製方向箭頭
    step = max(1, len(x) // 8)
    for i in range(0, len(x) - step, step):
        ax.annotate(
            "",
            xy=(x[i + step], y[i + step]),
            xytext=(x[i], y[i]),
            arrowprops=dict(arrowstyle="->", color="blue", alpha=0.4),
        )

    ax.set_xlabel(
        "Financial Conditions (Z-score)\n← Loose (Supportive) | Tight (Not Supportive) →",
        color=text_color,
    )
    ax.set_ylabel(
        "Earnings Growth\n← Negative | Positive →",
        color=text_color,
    )
    ax.set_title("Investment Clock Path", color=text_color, fontweight="bold")
    ax.set_xlim(-xlim, xlim)
    ax.set_ylim(-ylim, ylim)
    ax.legend(loc="upper right", fontsize=8)
    ax.tick_params(colors=text_color)

    # 標註象限名稱
    ax.text(
        -xlim * 0.5, ylim * 0.7, "Q1\n理想象限", ha="center", fontsize=9, color="darkgreen"
    )
    ax.text(
        xlim * 0.5, ylim * 0.7, "Q2\n好壞混合", ha="center", fontsize=9, color="darkgoldenrod"
    )
    ax.text(
        -xlim * 0.5, -ylim * 0.7, "Q3\n修復過渡", ha="center", fontsize=9, color="darkblue"
    )
    ax.text(
        xlim * 0.5, -ylim * 0.7, "Q4\n最差象限", ha="center", fontsize=9, color="darkred"
    )


def plot_clock_face(
    ax: plt.Axes,
    data: Dict[str, Any],
    text_color: str,
) -> None:
    """繪製極座標時鐘圖"""
    ts = data.get("time_series", {})
    x = ts.get("x", [])
    y = ts.get("y", [])

    if not x or not y:
        return

    # 計算角度和半徑
    angles = [np.arctan2(yi, xi) for xi, yi in zip(x, y)]
    radii = [np.sqrt(xi**2 + yi**2) for xi, yi in zip(x, y)]

    # 標準化半徑
    max_r = max(radii) if radii else 1
    radii = [r / max_r for r in radii]

    # 繪製時鐘刻度
    for hour in range(1, 13):
        # 將小時轉換為角度（12點在正上方）
        angle = np.pi / 2 - (hour / 12) * 2 * np.pi
        ax.annotate(
            str(hour),
            xy=(angle, 1.15),
            ha="center",
            va="center",
            fontsize=10,
            color=text_color,
        )

    # 繪製軌跡
    ax.plot(angles, radii, "b-", alpha=0.6, linewidth=1.5)

    # 標記起點和終點
    ax.scatter(angles[0], radii[0], c="green", s=100, marker="o", zorder=5)
    ax.scatter(angles[-1], radii[-1], c="red", s=150, marker="*", zorder=5)

    ax.set_ylim(0, 1.3)
    ax.set_title("Clock View", color=text_color, fontweight="bold", pad=20)
    ax.tick_params(colors=text_color)


def plot_earnings_series(
    ax: plt.Axes,
    data: Dict[str, Any],
    text_color: str,
    grid_alpha: float,
) -> None:
    """繪製獲利成長時間序列"""
    ts = data.get("time_series", {})
    dates = ts.get("dates", [])
    y = ts.get("y", [])

    if not dates or not y:
        ax.text(
            0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes
        )
        return

    # 轉換日期
    import pandas as pd

    dates = pd.to_datetime(dates)

    ax.plot(dates, y, "b-", linewidth=1.5)
    ax.axhline(y=0, color="gray", linestyle="--", alpha=grid_alpha)

    # 填充正負區域
    ax.fill_between(
        dates, y, 0, where=[v >= 0 for v in y], alpha=0.3, color="green", label="Positive"
    )
    ax.fill_between(
        dates, y, 0, where=[v < 0 for v in y], alpha=0.3, color="red", label="Negative"
    )

    ax.set_xlabel("Date", color=text_color)
    ax.set_ylabel("Earnings Growth (YoY)", color=text_color)
    ax.set_title("Earnings Growth Over Time", color=text_color, fontweight="bold")
    ax.tick_params(colors=text_color)
    ax.legend(loc="upper right", fontsize=8)


def plot_fci_series(
    ax: plt.Axes,
    data: Dict[str, Any],
    text_color: str,
    grid_alpha: float,
) -> None:
    """繪製金融環境時間序列"""
    ts = data.get("time_series", {})
    dates = ts.get("dates", [])
    x = ts.get("x", [])

    if not dates or not x:
        ax.text(
            0.5, 0.5, "No data", ha="center", va="center", transform=ax.transAxes
        )
        return

    # 轉換日期
    import pandas as pd

    dates = pd.to_datetime(dates)

    ax.plot(dates, x, "purple", linewidth=1.5)
    ax.axhline(y=0, color="gray", linestyle="--", alpha=grid_alpha)

    # 填充正負區域（負值=支持性/寬鬆）
    ax.fill_between(
        dates, x, 0, where=[v <= 0 for v in x], alpha=0.3, color="green", label="Loose (Supportive)"
    )
    ax.fill_between(
        dates, x, 0, where=[v > 0 for v in x], alpha=0.3, color="red", label="Tight"
    )

    ax.set_xlabel("Date", color=text_color)
    ax.set_ylabel("Financial Conditions (Z-score)", color=text_color)
    ax.set_title("Financial Conditions Over Time", color=text_color, fontweight="bold")
    ax.tick_params(colors=text_color)
    ax.legend(loc="upper right", fontsize=8)


# ============================================================================
# 主入口
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Investment Clock Visualizer - 投資時鐘視覺化"
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="Input JSON file (analysis result)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="Output image file path",
    )
    parser.add_argument(
        "--style",
        type=str,
        default="light",
        choices=["light", "dark"],
        help="Visual style",
    )

    args = parser.parse_args()

    if not HAS_MATPLOTLIB:
        print("Error: matplotlib is required for visualization", file=sys.stderr)
        print("Install with: pip install matplotlib", file=sys.stderr)
        sys.exit(1)

    # 讀取數據
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 生成圖表
    plot_investment_clock(data, args.output, style=args.style)


if __name__ == "__main__":
    main()
