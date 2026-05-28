#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Japan Debt Service Tax Burden - Chart Generator

生成視覺化圖表：
1. Interest/Tax Ratio 風險儀表盤
2. 壓力測試情境比較
3. 殖利率分位數指標

Usage:
    python generate_charts.py --output-dir ../../output
    python generate_charts.py --quick  # 使用快速檢查數據
    python generate_charts.py --full   # 使用完整分析數據
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 設置非交互式後端（必須在導入 pyplot 之前）
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Wedge, Rectangle
import numpy as np

# 設定中文字體（Windows/Mac/Linux 兼容）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'PingFang TC', 'Noto Sans CJK TC', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 嘗試導入本地模組
try:
    from japan_debt_analyzer import run_quick_check, run_full_analysis, get_risk_band, get_risk_band_emoji
    HAS_ANALYZER = True
except ImportError:
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from japan_debt_analyzer import run_quick_check, run_full_analysis, get_risk_band, get_risk_band_emoji
        HAS_ANALYZER = True
    except ImportError:
        HAS_ANALYZER = False


# ============================================================================
# 顏色配置
# ============================================================================

COLORS = {
    "green": "#22c55e",
    "yellow": "#eab308",
    "orange": "#f97316",
    "red": "#ef4444",
    "background": "#1a1a2e",
    "text": "#e8e8e8",
    "grid": "#333355",
    "accent": "#4f46e5",
}

RISK_BAND_COLORS = {
    "green": COLORS["green"],
    "yellow": COLORS["yellow"],
    "orange": COLORS["orange"],
    "red": COLORS["red"],
}


# ============================================================================
# 儀表盤繪製函數
# ============================================================================

def draw_gauge(ax, value: float, title: str = "Interest/Tax Ratio"):
    """
    繪製半圓風險儀表盤

    Args:
        ax: matplotlib axes
        value: 當前 ratio (0-1 範圍，如 0.15 表示 15%)
        title: 標題
    """
    # 風險區間閾值
    thresholds = [0, 0.25, 0.40, 0.55, 0.70]
    colors = [COLORS["green"], COLORS["yellow"], COLORS["orange"], COLORS["red"]]

    # 繪製背景扇形
    start_angle = 180
    for i, (start, end) in enumerate(zip(thresholds[:-1], thresholds[1:])):
        # 將 ratio 映射到角度 (180° 到 0°)
        angle_start = 180 - (start / 0.70) * 180
        angle_end = 180 - (end / 0.70) * 180
        wedge = Wedge(
            center=(0.5, 0),
            r=0.4,
            theta1=angle_end,
            theta2=angle_start,
            width=0.15,
            facecolor=colors[i],
            edgecolor='white',
            linewidth=1,
            alpha=0.8
        )
        ax.add_patch(wedge)

    # 計算指針角度
    clamped_value = min(max(value, 0), 0.70)
    needle_angle = 180 - (clamped_value / 0.70) * 180
    needle_rad = np.radians(needle_angle)

    # 繪製指針
    needle_length = 0.35
    needle_x = 0.5 + needle_length * np.cos(needle_rad)
    needle_y = needle_length * np.sin(needle_rad)
    ax.plot([0.5, needle_x], [0, needle_y], color='white', linewidth=3, solid_capstyle='round')
    ax.plot(0.5, 0, 'o', color='white', markersize=10)

    # 標籤
    labels = ['0%', '25%', '40%', '55%', '70%']
    for i, (thresh, label) in enumerate(zip(thresholds, labels)):
        angle = 180 - (thresh / 0.70) * 180
        rad = np.radians(angle)
        x = 0.5 + 0.48 * np.cos(rad)
        y = 0.48 * np.sin(rad)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, color=COLORS["text"])

    # 當前值
    band = get_risk_band(value) if HAS_ANALYZER else "green"
    ax.text(0.5, -0.15, f"{value:.1%}", ha='center', va='center',
            fontsize=28, fontweight='bold', color=RISK_BAND_COLORS.get(band, "white"))
    ax.text(0.5, -0.28, title, ha='center', va='center',
            fontsize=12, color=COLORS["text"])

    # 風險等級標籤 (使用文字符號替代 emoji)
    band_symbol = {"green": "●", "yellow": "●", "orange": "●", "red": "●"}.get(band, "○")
    ax.text(0.5, -0.40, f"{band_symbol} {band.upper()}", ha='center', va='center',
            fontsize=14, fontweight='bold', color=RISK_BAND_COLORS.get(band, "white"))

    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, 0.55)
    ax.set_aspect('equal')
    ax.axis('off')


def draw_yield_indicator(ax, latest: float, percentile: float, tenor: str = "10Y"):
    """
    繪製殖利率分位數指標

    Args:
        ax: matplotlib axes
        latest: 最新殖利率
        percentile: 百分位數 (0-1)
        tenor: 期限
    """
    # 繪製漸層條
    gradient = np.linspace(0, 1, 100).reshape(1, -1)
    ax.imshow(gradient, aspect='auto', cmap='RdYlGn_r', extent=[0, 1, 0, 0.3], alpha=0.8)

    # 當前位置標記
    marker_x = percentile
    ax.plot([marker_x, marker_x], [0, 0.3], color='white', linewidth=3)
    ax.plot(marker_x, 0.35, 'v', color='white', markersize=15)

    # 標籤
    ax.text(0.5, 0.55, f"{tenor} JGB 殖利率: {latest:.2f}%", ha='center', va='center',
            fontsize=14, fontweight='bold', color=COLORS["text"])
    ax.text(0.5, 0.75, f"百分位數: {percentile:.0%}", ha='center', va='center',
            fontsize=11, color=COLORS["text"])

    # 極端值警示 (使用文字符號替代 emoji)
    if percentile >= 0.95:
        ax.text(0.5, 0.92, "▲ 處於極端高位區", ha='center', va='center',
                fontsize=10, color=COLORS["red"])
    elif percentile <= 0.05:
        ax.text(0.5, 0.92, "▼ 處於極端低位區", ha='center', va='center',
                fontsize=10, color=COLORS["green"])

    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.1, 1.0)
    ax.axis('off')


def draw_stress_test_bars(ax, stress_results: List[Dict]):
    """
    繪製壓力測試結果條形圖

    Args:
        ax: matplotlib axes
        stress_results: 壓力測試結果列表
    """
    scenarios = [s["name"] for s in stress_results]
    y1_ratios = [s["results"]["year1_interest_tax_ratio"] for s in stress_results]
    y2_ratios = [s["results"]["year2_interest_tax_ratio"] for s in stress_results]

    y_pos = np.arange(len(scenarios))
    bar_height = 0.35

    # Year 1 條形
    bars1 = ax.barh(y_pos + bar_height/2, y1_ratios, bar_height,
                    label='Year 1', color=COLORS["accent"], alpha=0.8)
    # Year 2 條形
    bars2 = ax.barh(y_pos - bar_height/2, y2_ratios, bar_height,
                    label='Year 2', color='#818cf8', alpha=0.8)

    # 風險區間背景
    ax.axvspan(0, 0.25, alpha=0.1, color=COLORS["green"])
    ax.axvspan(0.25, 0.40, alpha=0.1, color=COLORS["yellow"])
    ax.axvspan(0.40, 0.55, alpha=0.1, color=COLORS["orange"])
    ax.axvspan(0.55, 0.70, alpha=0.1, color=COLORS["red"])

    # 風險閾值線
    for thresh, color in [(0.25, COLORS["yellow"]), (0.40, COLORS["orange"]), (0.55, COLORS["red"])]:
        ax.axvline(x=thresh, color=color, linestyle='--', linewidth=1, alpha=0.5)

    # 數值標籤
    for bar, ratio in zip(bars1, y1_ratios):
        band = get_risk_band(ratio) if HAS_ANALYZER else "green"
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f'{ratio:.1%}', va='center', fontsize=9, color=RISK_BAND_COLORS.get(band, "white"))

    for bar, ratio in zip(bars2, y2_ratios):
        band = get_risk_band(ratio) if HAS_ANALYZER else "green"
        ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                f'{ratio:.1%}', va='center', fontsize=9, color=RISK_BAND_COLORS.get(band, "white"))

    ax.set_yticks(y_pos)
    ax.set_yticklabels(scenarios, fontsize=10, color=COLORS["text"])
    ax.set_xlabel('Interest/Tax Ratio', fontsize=11, color=COLORS["text"])
    ax.set_title('壓力測試情境比較', fontsize=13, fontweight='bold', color=COLORS["text"], pad=10)
    ax.set_xlim(0, 0.50)
    ax.legend(loc='lower right', fontsize=9)
    ax.tick_params(colors=COLORS["text"])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(COLORS["grid"])
    ax.spines['left'].set_color(COLORS["grid"])


def draw_fiscal_summary(ax, fiscal: Dict):
    """
    繪製財政數據摘要

    Args:
        ax: matplotlib axes
        fiscal: 財政數據
    """
    ax.axis('off')

    # 標題
    ax.text(0.5, 0.95, '財政數據摘要', ha='center', va='top',
            fontsize=13, fontweight='bold', color=COLORS["text"])

    # 數據項目
    items = [
        ('稅收', f"¥{fiscal.get('tax_revenue_jpy', 0)/1e12:.1f}兆"),
        ('利息支出', f"¥{fiscal.get('interest_payments_jpy', 0)/1e12:.1f}兆"),
        ('存量債務', f"¥{fiscal.get('debt_stock_jpy', 0)/1e12:.0f}兆"),
        ('隱含平均利率', f"{fiscal.get('interest_payments_jpy', 0)/fiscal.get('debt_stock_jpy', 1)*100:.2f}%"),
    ]

    y_start = 0.75
    for i, (label, value) in enumerate(items):
        y = y_start - i * 0.18
        ax.text(0.1, y, label + ':', ha='left', va='center',
                fontsize=11, color=COLORS["text"])
        ax.text(0.9, y, value, ha='right', va='center',
                fontsize=11, fontweight='bold', color=COLORS["accent"])

    # 口徑說明
    definition = fiscal.get('definition', {})
    ax.text(0.5, 0.05, f"口徑: {definition.get('interest_payment_series', 'N/A')} / {definition.get('fiscal_year', 'N/A')}",
            ha='center', va='bottom', fontsize=9, color='#888888', style='italic')


# ============================================================================
# 主圖表生成函數
# ============================================================================

def generate_dashboard(
    data: Dict[str, Any],
    output_path: Optional[str] = None,
    show: bool = False,
) -> str:
    """
    生成完整的 Dashboard 圖表

    Args:
        data: 分析結果數據
        output_path: 輸出檔案路徑
        show: 是否顯示圖表

    Returns:
        輸出檔案路徑
    """
    # 設定圖表
    fig = plt.figure(figsize=(14, 10), facecolor=COLORS["background"])
    fig.suptitle('日本債務利息負擔分析 Dashboard', fontsize=18, fontweight='bold',
                 color=COLORS["text"], y=0.97)

    # 子圖佈局
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3,
                          left=0.05, right=0.95, top=0.90, bottom=0.08)

    # 1. 風險儀表盤 (左上)
    ax_gauge = fig.add_subplot(gs[0, 0])
    ax_gauge.set_facecolor(COLORS["background"])
    ratio = data.get("fiscal", {}).get("interest_tax_ratio", 0.15)
    draw_gauge(ax_gauge, ratio)

    # 2. 殖利率指標 (中上)
    ax_yield = fig.add_subplot(gs[0, 1])
    ax_yield.set_facecolor(COLORS["background"])
    yield_stats = data.get("yield_stats", {})
    draw_yield_indicator(
        ax_yield,
        latest=yield_stats.get("latest", 1.0),
        percentile=yield_stats.get("percentile", 0.5),
        tenor=yield_stats.get("tenor", "10Y")
    )

    # 3. 財政摘要 (右上)
    ax_fiscal = fig.add_subplot(gs[0, 2])
    ax_fiscal.set_facecolor(COLORS["background"])
    draw_fiscal_summary(ax_fiscal, data.get("fiscal", {}))

    # 4. 壓力測試 (下方跨全寬)
    ax_stress = fig.add_subplot(gs[1, :])
    ax_stress.set_facecolor(COLORS["background"])
    if "stress_tests" in data:
        draw_stress_test_bars(ax_stress, data["stress_tests"])
    else:
        ax_stress.text(0.5, 0.5, "執行 --full 模式以查看壓力測試結果",
                      ha='center', va='center', fontsize=14, color=COLORS["text"])
        ax_stress.axis('off')

    # 底部資訊
    as_of = data.get("as_of", datetime.now().strftime("%Y-%m-%d"))
    sources = data.get("data_sources", {})
    source_text = ", ".join([f"{k}: {v}" for k, v in sources.items()]) if sources else "N/A"
    fig.text(0.5, 0.02, f"分析日期: {as_of} | 數據來源: {source_text}",
             ha='center', fontsize=9, color='#666666')

    # 輸出
    if output_path is None:
        output_dir = Path(__file__).parent.parent.parent.parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"japan_debt_dashboard_{datetime.now().strftime('%Y%m%d')}.png"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.savefig(output_path, dpi=150, facecolor=COLORS["background"],
                edgecolor='none', bbox_inches='tight')

    if show:
        plt.show()
    else:
        plt.close()

    return str(output_path)


# ============================================================================
# CLI 入口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Japan Debt Chart Generator")
    parser.add_argument("--quick", action="store_true", help="使用快速檢查數據")
    parser.add_argument("--full", action="store_true", help="使用完整分析數據")
    parser.add_argument("--data-file", type=str, help="從 JSON 檔案載入數據")
    parser.add_argument("--output-dir", type=str, help="輸出目錄")
    parser.add_argument("--output-file", type=str, help="輸出檔案名稱")
    parser.add_argument("--show", action="store_true", help="顯示圖表")
    parser.add_argument("--refresh", action="store_true", help="強制刷新數據")

    args = parser.parse_args()

    # 取得數據
    data = None

    if args.data_file:
        with open(args.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    elif HAS_ANALYZER:
        if args.full:
            print("執行完整分析...")
            data = run_full_analysis(force_refresh=args.refresh)
        else:
            print("執行快速檢查...")
            quick_data = run_quick_check(force_refresh=args.refresh)
            # 為了顯示壓力測試，也執行完整分析
            print("取得壓力測試數據...")
            full_data = run_full_analysis(force_refresh=False)
            data = {**quick_data, "stress_tests": full_data.get("stress_tests")}
    else:
        print("Error: 無法載入分析器模組，請提供 --data-file 參數")
        return

    # 決定輸出路徑
    if args.output_file:
        output_path = args.output_file
    elif args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"japan_debt_dashboard_{datetime.now().strftime('%Y%m%d')}.png"
    else:
        output_path = None  # 使用預設

    # 生成圖表
    result_path = generate_dashboard(data, output_path=output_path, show=args.show)
    print(f"\n圖表已生成: {result_path}")


if __name__ == "__main__":
    main()
