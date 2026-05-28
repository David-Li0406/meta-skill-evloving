#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Japan Debt Spiral Simulation - Visual Chart Generator

模擬債務螺旋上升情境：
- 多年累積效應視覺化
- 不同壓力情境比較
- 風險區間標示

Usage:
    python generate_spiral_chart.py --output-dir ../../output
    python generate_spiral_chart.py --years 10 --scenarios all
    python generate_spiral_chart.py --stress 200  # 單一情境
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# 設置非交互式後端（必須在導入 pyplot 之前）
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
import numpy as np

# 設定中文字體（Windows/Mac/Linux 兼容）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'PingFang TC', 'Noto Sans CJK TC', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 嘗試導入本地模組
try:
    from japan_debt_analyzer import get_risk_band, get_risk_band_emoji
    from data_manager import JapanDebtDataManager
    HAS_ANALYZER = True
except ImportError:
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from japan_debt_analyzer import get_risk_band, get_risk_band_emoji
        from data_manager import JapanDebtDataManager
        HAS_ANALYZER = True
    except ImportError:
        HAS_ANALYZER = False
        def get_risk_band(ratio):
            if ratio < 0.25: return "green"
            elif ratio < 0.40: return "yellow"
            elif ratio < 0.55: return "orange"
            else: return "red"


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
    "baseline": "#60a5fa",
    "stress_200": "#f97316",
    "stress_200_recession": "#ef4444",
    "stress_300": "#dc2626",
}

RISK_BAND_COLORS = {
    "green": COLORS["green"],
    "yellow": COLORS["yellow"],
    "orange": COLORS["orange"],
    "red": COLORS["red"],
}


# ============================================================================
# 債務螺旋模擬核心
# ============================================================================

def simulate_debt_spiral(
    initial_interest: float,
    initial_tax: float,
    debt_stock: float,
    delta_yield_bp: int,
    pass_through_annual: float = 0.15,
    tax_growth_annual: float = 0.0,
    years: int = 10,
) -> List[Dict[str, Any]]:
    """
    模擬債務螺旋多年演變

    Args:
        initial_interest: 初始利息支出（兆日圓）
        initial_tax: 初始稅收（兆日圓）
        debt_stock: 債務存量（兆日圓）
        delta_yield_bp: 殖利率上升幅度（bp）
        pass_through_annual: 年度再定價比例
        tax_growth_annual: 稅收年增率（負值表示衰退）
        years: 模擬年數

    Returns:
        各年的模擬結果列表
    """
    delta_yield = delta_yield_bp / 10000.0  # bp 轉小數
    results = []

    interest = initial_interest
    tax = initial_tax
    cumulative_pass_through = 0.0

    # Year 0: 基準狀態
    results.append({
        "year": 0,
        "interest": interest,
        "tax": tax,
        "ratio": interest / tax,
        "cumulative_pass_through": 0.0,
        "additional_interest": 0.0,
        "risk_band": get_risk_band(interest / tax),
    })

    for y in range(1, years + 1):
        # 累積再定價比例
        cumulative_pass_through = min(cumulative_pass_through + pass_through_annual, 1.0)

        # 新增利息 = 存量 × 累積再定價 × 利率上升
        additional_interest = debt_stock * cumulative_pass_through * delta_yield
        interest = initial_interest + additional_interest

        # 稅收變化
        tax = initial_tax * ((1.0 + tax_growth_annual) ** y)

        ratio = interest / tax if tax > 0 else float('inf')

        results.append({
            "year": y,
            "interest": interest,
            "tax": tax,
            "ratio": ratio,
            "cumulative_pass_through": cumulative_pass_through,
            "additional_interest": additional_interest,
            "risk_band": get_risk_band(ratio),
        })

    return results


def get_fiscal_data() -> Dict[str, float]:
    """獲取財政數據"""
    if HAS_ANALYZER:
        try:
            manager = JapanDebtDataManager()
            data = manager.get_all_data(include_tic=False)
            fiscal = data["fiscal"]
            return {
                "interest": fiscal["interest_payments_jpy"] / 1e12,  # 轉換為兆
                "tax": fiscal["tax_revenue_jpy"] / 1e12,
                "debt_stock": fiscal["debt_stock_jpy"] / 1e12,
            }
        except Exception:
            pass

    # Fallback
    return {
        "interest": 10.5,  # 兆日圓
        "tax": 70.0,
        "debt_stock": 1324.0,
    }


# ============================================================================
# 視覺化函數
# ============================================================================

def draw_spiral_comparison(
    ax,
    scenarios: List[Dict[str, Any]],
    years: int = 10,
):
    """
    繪製多情境螺旋比較圖

    Args:
        ax: matplotlib axes
        scenarios: 情境列表，每個包含 name, results, color
        years: 模擬年數
    """
    # 風險區間背景
    ax.axhspan(0, 0.25, alpha=0.15, color=COLORS["green"], label='_nolegend_')
    ax.axhspan(0.25, 0.40, alpha=0.15, color=COLORS["yellow"], label='_nolegend_')
    ax.axhspan(0.40, 0.55, alpha=0.15, color=COLORS["orange"], label='_nolegend_')
    ax.axhspan(0.55, 0.70, alpha=0.15, color=COLORS["red"], label='_nolegend_')

    # 風險閾值線
    for thresh, color, label in [
        (0.25, COLORS["yellow"], "25% (GREEN→YELLOW)"),
        (0.40, COLORS["orange"], "40% (YELLOW→ORANGE)"),
        (0.55, COLORS["red"], "55% (ORANGE→RED)"),
    ]:
        ax.axhline(y=thresh, color=color, linestyle='--', linewidth=1.5, alpha=0.7)

    # 繪製各情境曲線
    for scenario in scenarios:
        results = scenario["results"]
        x = [r["year"] for r in results]
        y = [r["ratio"] for r in results]

        line, = ax.plot(x, y,
                        color=scenario["color"],
                        linewidth=2.5,
                        marker='o',
                        markersize=6,
                        label=scenario["name"])

        # 終點標註
        final_ratio = y[-1]
        final_band = get_risk_band(final_ratio)
        ax.annotate(
            f'{final_ratio:.1%}',
            xy=(x[-1], y[-1]),
            xytext=(8, 0),
            textcoords='offset points',
            fontsize=10,
            fontweight='bold',
            color=RISK_BAND_COLORS.get(final_band, scenario["color"]),
            va='center',
        )

    # 設定
    ax.set_xlim(-0.5, years + 1.5)
    ax.set_ylim(0, 0.75)
    ax.set_xlabel('年數', fontsize=12, color=COLORS["text"])
    ax.set_ylabel('Interest / Tax Ratio', fontsize=12, color=COLORS["text"])
    ax.set_title('債務螺旋情境模擬：Interest/Tax Ratio 多年演變',
                 fontsize=14, fontweight='bold', color=COLORS["text"], pad=15)

    ax.set_xticks(range(0, years + 1, 2 if years > 5 else 1))
    ax.tick_params(colors=COLORS["text"])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(COLORS["grid"])
    ax.spines['left'].set_color(COLORS["grid"])
    ax.set_facecolor(COLORS["background"])

    # 圖例
    ax.legend(loc='upper left', fontsize=10, framealpha=0.8)


def draw_interest_breakdown(
    ax,
    scenario: Dict[str, Any],
):
    """
    繪製利息分解堆疊圖

    Args:
        ax: matplotlib axes
        scenario: 單一情境結果
    """
    results = scenario["results"]
    years = [r["year"] for r in results]
    base_interest = results[0]["interest"]
    additional = [r["additional_interest"] for r in results]

    # 堆疊柱狀圖
    width = 0.6
    ax.bar(years, [base_interest] * len(years), width,
           label='原始利息支出', color=COLORS["accent"], alpha=0.8)
    ax.bar(years, additional, width, bottom=[base_interest] * len(years),
           label='新增利息負擔', color=COLORS["stress_200"], alpha=0.8)

    # 標註
    for i, r in enumerate(results):
        if r["year"] > 0:
            total = r["interest"]
            ax.text(r["year"], total + 0.5, f'¥{total:.1f}兆',
                   ha='center', va='bottom', fontsize=9, color=COLORS["text"])

    ax.set_xlabel('年數', fontsize=11, color=COLORS["text"])
    ax.set_ylabel('利息支出（兆日圓）', fontsize=11, color=COLORS["text"])
    ax.set_title(f'利息支出分解：{scenario["name"]}',
                fontsize=12, fontweight='bold', color=COLORS["text"], pad=10)

    ax.tick_params(colors=COLORS["text"])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(COLORS["grid"])
    ax.spines['left'].set_color(COLORS["grid"])
    ax.set_facecolor(COLORS["background"])
    ax.legend(loc='upper left', fontsize=9)


def draw_risk_timeline(
    ax,
    scenario: Dict[str, Any],
):
    """
    繪製風險區間時間軸

    Args:
        ax: matplotlib axes
        scenario: 單一情境結果
    """
    results = scenario["results"]

    for r in results:
        band = r["risk_band"]
        color = RISK_BAND_COLORS.get(band, "#888888")
        rect = Rectangle((r["year"] - 0.4, 0), 0.8, 1,
                         facecolor=color, alpha=0.8, edgecolor='white', linewidth=1)
        ax.add_patch(rect)

        # 年份標籤
        ax.text(r["year"], -0.15, f'Y{r["year"]}', ha='center', va='top',
               fontsize=9, color=COLORS["text"])

        # Ratio 標籤
        ax.text(r["year"], 0.5, f'{r["ratio"]:.0%}', ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')

    ax.set_xlim(-0.8, len(results) - 0.2)
    ax.set_ylim(-0.4, 1.2)
    ax.set_title(f'風險區間演變：{scenario["name"]}',
                fontsize=12, fontweight='bold', color=COLORS["text"], pad=10)
    ax.axis('off')
    ax.set_facecolor(COLORS["background"])

    # 圖例
    legend_elements = [
        mpatches.Patch(facecolor=COLORS["green"], label='GREEN (<25%)'),
        mpatches.Patch(facecolor=COLORS["yellow"], label='YELLOW (25-40%)'),
        mpatches.Patch(facecolor=COLORS["orange"], label='ORANGE (40-55%)'),
        mpatches.Patch(facecolor=COLORS["red"], label='RED (>55%)'),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8, framealpha=0.8)


def draw_summary_stats(
    ax,
    scenarios: List[Dict[str, Any]],
    fiscal_data: Dict[str, float],
):
    """
    繪製摘要統計

    Args:
        ax: matplotlib axes
        scenarios: 情境列表
        fiscal_data: 財政數據
    """
    ax.axis('off')
    ax.set_facecolor(COLORS["background"])

    # 標題
    ax.text(0.5, 0.95, '模擬參數與結果摘要', ha='center', va='top',
           fontsize=13, fontweight='bold', color=COLORS["text"])

    # 基礎數據
    lines = [
        f"初始利息：¥{fiscal_data['interest']:.1f}兆",
        f"初始稅收：¥{fiscal_data['tax']:.1f}兆",
        f"債務存量：¥{fiscal_data['debt_stock']:.0f}兆",
        f"初始 Ratio：{fiscal_data['interest']/fiscal_data['tax']:.1%}",
        "",
        "各情境 Year 10 結果：",
    ]

    for sc in scenarios:
        final = sc["results"][-1]
        band = final["risk_band"]
        emoji = {"green": "●", "yellow": "●", "orange": "●", "red": "●"}.get(band, "○")
        lines.append(f"  {emoji} {sc['name']}: {final['ratio']:.1%}")

    y = 0.80
    for line in lines:
        ax.text(0.05, y, line, ha='left', va='top',
               fontsize=10, color=COLORS["text"])
        y -= 0.085


# ============================================================================
# 主圖表生成函數
# ============================================================================

def generate_spiral_dashboard(
    output_path: Optional[str] = None,
    years: int = 10,
    custom_scenarios: Optional[List[Dict]] = None,
    show: bool = False,
) -> str:
    """
    生成債務螺旋模擬 Dashboard

    Args:
        output_path: 輸出檔案路徑
        years: 模擬年數
        custom_scenarios: 自定義情境（如果為 None，使用預設情境）
        show: 是否顯示圖表

    Returns:
        輸出檔案路徑
    """
    # 獲取財政數據
    fiscal = get_fiscal_data()

    # 定義情境
    if custom_scenarios is None:
        scenario_configs = [
            {
                "name": "基準（維持現狀）",
                "delta_yield_bp": 0,
                "tax_growth": 0.0,
                "color": COLORS["baseline"],
            },
            {
                "name": "+200bp（利率正常化）",
                "delta_yield_bp": 200,
                "tax_growth": 0.02,  # 假設經濟成長 2%
                "color": COLORS["stress_200"],
            },
            {
                "name": "+200bp + 衰退（稅收-3%/年）",
                "delta_yield_bp": 200,
                "tax_growth": -0.03,
                "color": COLORS["stress_200_recession"],
            },
            {
                "name": "+300bp 嚴重衝擊",
                "delta_yield_bp": 300,
                "tax_growth": -0.05,
                "color": COLORS["stress_300"],
            },
        ]
    else:
        scenario_configs = custom_scenarios

    # 執行模擬
    scenarios = []
    for config in scenario_configs:
        results = simulate_debt_spiral(
            initial_interest=fiscal["interest"],
            initial_tax=fiscal["tax"],
            debt_stock=fiscal["debt_stock"],
            delta_yield_bp=config["delta_yield_bp"],
            tax_growth_annual=config.get("tax_growth", 0.0),
            years=years,
        )
        scenarios.append({
            "name": config["name"],
            "results": results,
            "color": config.get("color", COLORS["accent"]),
            "config": config,
        })

    # 設定圖表
    fig = plt.figure(figsize=(16, 12), facecolor=COLORS["background"])
    fig.suptitle('日本債務螺旋模擬分析', fontsize=20, fontweight='bold',
                color=COLORS["text"], y=0.97)

    # 子圖佈局
    gs = fig.add_gridspec(2, 2, hspace=0.25, wspace=0.20,
                          left=0.06, right=0.94, top=0.90, bottom=0.08)

    # 1. 螺旋比較圖（左上，主圖）
    ax_spiral = fig.add_subplot(gs[0, :])
    draw_spiral_comparison(ax_spiral, scenarios, years)

    # 2. 利息分解圖（左下）
    ax_breakdown = fig.add_subplot(gs[1, 0])
    # 選擇 +200bp 情境作為展示
    target_scenario = next((s for s in scenarios if "+200bp" in s["name"] and "衰退" not in s["name"]), scenarios[1])
    draw_interest_breakdown(ax_breakdown, target_scenario)

    # 3. 摘要統計（右下）
    ax_summary = fig.add_subplot(gs[1, 1])
    draw_summary_stats(ax_summary, scenarios, fiscal)

    # 底部資訊
    as_of = datetime.now().strftime("%Y-%m-%d")
    fig.text(0.5, 0.02,
             f"模擬日期: {as_of} | 假設: 年度再定價 15% | 數據來源: MOF FY2025 Budget",
             ha='center', fontsize=9, color='#666666')

    # 輸出
    if output_path is None:
        output_dir = Path(__file__).parent.parent.parent.parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"japan_debt_spiral_{datetime.now().strftime('%Y-%m-%d')}.png"
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


def generate_single_stress_chart(
    delta_yield_bp: int,
    output_path: Optional[str] = None,
    years: int = 10,
    show: bool = False,
) -> str:
    """
    生成單一壓力情境的詳細圖表

    Args:
        delta_yield_bp: 殖利率衝擊（bp）
        output_path: 輸出路徑
        years: 模擬年數
        show: 是否顯示

    Returns:
        輸出檔案路徑
    """
    fiscal = get_fiscal_data()

    # 基準 vs 壓力情境
    scenarios = [
        {
            "name": "基準（維持現狀）",
            "results": simulate_debt_spiral(
                fiscal["interest"], fiscal["tax"], fiscal["debt_stock"],
                delta_yield_bp=0, years=years
            ),
            "color": COLORS["baseline"],
        },
        {
            "name": f"+{delta_yield_bp}bp 衝擊",
            "results": simulate_debt_spiral(
                fiscal["interest"], fiscal["tax"], fiscal["debt_stock"],
                delta_yield_bp=delta_yield_bp, years=years
            ),
            "color": COLORS["stress_200"],
        },
        {
            "name": f"+{delta_yield_bp}bp + 衰退",
            "results": simulate_debt_spiral(
                fiscal["interest"], fiscal["tax"], fiscal["debt_stock"],
                delta_yield_bp=delta_yield_bp, tax_growth_annual=-0.03, years=years
            ),
            "color": COLORS["stress_200_recession"],
        },
    ]

    # 設定圖表
    fig = plt.figure(figsize=(14, 10), facecolor=COLORS["background"])
    fig.suptitle(f'日本債務壓力測試：+{delta_yield_bp}bp 情境分析',
                fontsize=18, fontweight='bold', color=COLORS["text"], y=0.96)

    gs = fig.add_gridspec(2, 2, hspace=0.28, wspace=0.20,
                          left=0.07, right=0.93, top=0.88, bottom=0.08)

    # 1. 螺旋比較
    ax1 = fig.add_subplot(gs[0, :])
    draw_spiral_comparison(ax1, scenarios, years)

    # 2. 風險時間軸
    ax2 = fig.add_subplot(gs[1, 0])
    draw_risk_timeline(ax2, scenarios[1])  # +bp 情境

    # 3. 利息分解
    ax3 = fig.add_subplot(gs[1, 1])
    draw_interest_breakdown(ax3, scenarios[1])

    # 底部資訊
    as_of = datetime.now().strftime("%Y-%m-%d")
    fig.text(0.5, 0.02,
             f"模擬日期: {as_of} | 年度再定價: 15% | 數據: MOF FY2025",
             ha='center', fontsize=9, color='#666666')

    # 輸出
    if output_path is None:
        output_dir = Path(__file__).parent.parent.parent.parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"japan_debt_stress_{delta_yield_bp}bp_{datetime.now().strftime('%Y-%m-%d')}.png"
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
    parser = argparse.ArgumentParser(description="Japan Debt Spiral Chart Generator")
    parser.add_argument("--output-dir", type=str, help="輸出目錄")
    parser.add_argument("--output-file", type=str, help="輸出檔案名稱")
    parser.add_argument("--years", type=int, default=10, help="模擬年數（預設 10）")
    parser.add_argument("--stress", type=int, metavar="BP", help="單一壓力情境（bp）")
    parser.add_argument("--all", action="store_true", help="生成完整 Dashboard")
    parser.add_argument("--show", action="store_true", help="顯示圖表")

    args = parser.parse_args()

    # 決定輸出目錄
    if args.output_dir:
        output_dir = Path(args.output_dir)
    else:
        output_dir = Path(__file__).parent.parent.parent.parent.parent / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.stress:
        # 單一壓力情境
        if args.output_file:
            output_path = output_dir / args.output_file
        else:
            output_path = output_dir / f"japan_debt_stress_{args.stress}bp_{datetime.now().strftime('%Y-%m-%d')}.png"

        result_path = generate_single_stress_chart(
            delta_yield_bp=args.stress,
            output_path=str(output_path),
            years=args.years,
            show=args.show,
        )
        print(f"壓力測試圖表已生成: {result_path}")
    else:
        # 完整 Dashboard
        if args.output_file:
            output_path = output_dir / args.output_file
        else:
            output_path = output_dir / f"japan_debt_spiral_{datetime.now().strftime('%Y-%m-%d')}.png"

        result_path = generate_spiral_dashboard(
            output_path=str(output_path),
            years=args.years,
            show=args.show,
        )
        print(f"螺旋模擬 Dashboard 已生成: {result_path}")


if __name__ == "__main__":
    main()
