#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
視覺化工具 - Bloomberg 風格

生成銅價股市韌性依賴分析的視覺化圖表，模仿 Bloomberg Intelligence 風格。

圖表特點：
- 深色背景
- 多軸疊加（銅價右軸 R1，全球市值左軸 L2，中國10Y債券價格 左軸 L1）
- 銅價用線圖 + SMA60
- 全球市值用橙色面積圖
- 中國10Y債券價格 用黃線
- 關鍵數值標註
- 全中文標籤
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

import numpy as np
import pandas as pd

# 添加腳本目錄到路徑
sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_copper, fetch_world_market_cap, fetch_china_10y_yield, align_monthly

# 使用非交互式後端
import matplotlib
matplotlib.use('Agg')

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.ticker import FuncFormatter

    # 設定中文字體
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("請安裝 matplotlib: pip install matplotlib")


# Bloomberg 風格配色
BLOOMBERG_COLORS = {
    "background": "#1a1a2e",
    "grid": "#2d2d44",
    "text": "#ffffff",
    "text_dim": "#888888",
    "copper": "#ff6b35",       # 橙紅色（銅價線）
    "copper_candle_up": "#00ff88",
    "copper_candle_down": "#ff4444",
    "sma": "#ffaa00",          # 橙黃色（SMA）
    "world_mktcap": "#ff8c00", # 橙色面積圖
    "world_mktcap_alpha": 0.4,
    "china_bond": "#ffff00",   # 黃色（中國債券價格）
    "level_line": "#666666",
    "annotation": "#ffffff",
}


def yield_to_bond_price(yield_pct: pd.Series, maturity: int = 10) -> pd.Series:
    """
    將殖利率轉換為債券價格（假設面額 100）

    公式: Price = 100 / (1 + yield/100)^maturity

    Parameters
    ----------
    yield_pct : pd.Series
        殖利率（百分比，如 2.5 表示 2.5%）
    maturity : int
        到期年限（預設 10 年）

    Returns
    -------
    pd.Series
        債券價格
    """
    return 100 / ((1 + yield_pct / 100) ** maturity)


def format_price(x, pos):
    """格式化價格標籤"""
    if x >= 1000:
        return f'{x/1000:.1f}K'
    return f'{x:.0f}'


def format_trillion(x, pos):
    """格式化兆美元標籤"""
    return f'{x:.0f}'


def format_percent(x, pos):
    """格式化百分比標籤"""
    return f'{x:.1f}%'


def plot_bloomberg_style(
    copper: pd.Series,
    copper_ohlc: Optional[pd.DataFrame],
    sma: pd.Series,
    world_mktcap: pd.Series,
    china_yield: pd.Series,
    output_path: str,
    title: str = "銅價 vs. 股市韌性",
    figsize: Tuple[int, int] = (14, 8),
    dpi: int = 150,
    round_levels: list = [10000, 13000],
    source: str = "資料來源: Yahoo Finance, MacroMicro"
) -> None:
    """
    繪製 Bloomberg 風格的多軸疊加圖表（中文版）

    Parameters
    ----------
    copper : pd.Series
        銅價序列（USD/ton）
    copper_ohlc : pd.DataFrame, optional
        銅價 OHLC 數據（用於蠟燭圖）
    sma : pd.Series
        銅價 SMA60
    world_mktcap : pd.Series
        全球股市市值（兆美元）
    china_yield : pd.Series
        中國10Y殖利率（%）- 會自動轉換為債券價格
    output_path : str
        輸出路徑
    title : str
        圖表標題
    figsize : tuple
        圖表尺寸
    dpi : int
        解析度
    round_levels : list
        關卡位置
    source : str
        數據來源標註
    """
    if not HAS_MATPLOTLIB:
        print("請安裝 matplotlib: pip install matplotlib")
        return

    # 設定深色背景
    plt.style.use('dark_background')

    fig, ax1 = plt.subplots(figsize=figsize, facecolor=BLOOMBERG_COLORS["background"])
    ax1.set_facecolor(BLOOMBERG_COLORS["background"])

    # 對齊所有序列到共同索引
    common_idx = copper.index.intersection(world_mktcap.index).intersection(china_yield.index)
    copper = copper.loc[common_idx]
    sma = sma.loc[sma.index.intersection(common_idx)]
    world_mktcap = world_mktcap.loc[common_idx]
    china_yield = china_yield.loc[common_idx]

    # 將殖利率轉換為債券價格
    china_bond_price = yield_to_bond_price(china_yield)

    # === 左軸 L2: 全球市值（面積圖）===
    ax_mktcap = ax1
    ax_mktcap.fill_between(
        world_mktcap.index,
        0,
        world_mktcap.values,
        color=BLOOMBERG_COLORS["world_mktcap"],
        alpha=BLOOMBERG_COLORS["world_mktcap_alpha"],
        label="全球股市總市值 (L2)",
        zorder=1
    )
    ax_mktcap.set_ylabel("全球市值 (兆美元)", color=BLOOMBERG_COLORS["text_dim"], fontsize=10)
    ax_mktcap.tick_params(axis='y', labelcolor=BLOOMBERG_COLORS["text_dim"])
    ax_mktcap.yaxis.set_major_formatter(FuncFormatter(format_trillion))
    ax_mktcap.set_ylim(0, world_mktcap.max() * 1.3)

    # === 左軸 L1: 中國10Y債券價格 ===
    ax_bond = ax1.twinx()
    ax_bond.spines['left'].set_position(('outward', 60))
    ax_bond.yaxis.set_label_position('left')
    ax_bond.yaxis.set_ticks_position('left')

    ax_bond.plot(
        china_bond_price.index,
        china_bond_price.values,
        color=BLOOMBERG_COLORS["china_bond"],
        linewidth=1.5,
        label="中國10年期國債價格 (L1)",
        zorder=3
    )
    ax_bond.set_ylabel("中國10Y債券價格", color=BLOOMBERG_COLORS["china_bond"], fontsize=10)
    ax_bond.tick_params(axis='y', labelcolor=BLOOMBERG_COLORS["china_bond"])
    bond_range = china_bond_price.max() - china_bond_price.min()
    ax_bond.set_ylim(china_bond_price.min() - bond_range * 0.2, china_bond_price.max() + bond_range * 0.2)

    # === 右軸 R1: 銅價 ===
    ax_copper = ax1.twinx()

    # 繪製銅價線
    line_copper, = ax_copper.plot(
        copper.index,
        copper.values,
        color=BLOOMBERG_COLORS["copper"],
        linewidth=2,
        label="銅期貨 LME 月線 (R1)",
        zorder=5
    )

    # 繪製 SMA
    if len(sma) > 0:
        line_sma, = ax_copper.plot(
            sma.index,
            sma.values,
            color=BLOOMBERG_COLORS["sma"],
            linewidth=1.5,
            linestyle='--',
            label=f"SMA(60) 收盤均線 (P1)",
            zorder=4
        )

    # 繪製關卡線
    for level in round_levels:
        ax_copper.axhline(
            y=level,
            color=BLOOMBERG_COLORS["level_line"],
            linestyle=':',
            alpha=0.7,
            zorder=2
        )

    ax_copper.set_ylabel("銅價 (美元/噸)", color=BLOOMBERG_COLORS["copper"], fontsize=10)
    ax_copper.tick_params(axis='y', labelcolor=BLOOMBERG_COLORS["copper"])
    ax_copper.yaxis.set_major_formatter(FuncFormatter(format_price))

    # 設定銅價軸範圍
    copper_min = min(copper.min(), min(round_levels) * 0.8)
    copper_max = max(copper.max(), max(round_levels) * 1.1)
    ax_copper.set_ylim(copper_min, copper_max)

    # === 標註當前數值 ===
    latest_date = copper.index[-1]
    latest_copper = copper.iloc[-1]
    latest_sma = sma.iloc[-1] if len(sma) > 0 else None
    latest_mktcap = world_mktcap.iloc[-1]
    latest_bond_price = china_bond_price.iloc[-1]

    # 銅價標註
    ax_copper.annotate(
        f'{latest_copper:,.0f}',
        xy=(latest_date, latest_copper),
        xytext=(10, 0),
        textcoords='offset points',
        color=BLOOMBERG_COLORS["copper"],
        fontsize=11,
        fontweight='bold',
        va='center'
    )

    # SMA 標註
    if latest_sma:
        ax_copper.annotate(
            f'{latest_sma:,.0f}',
            xy=(latest_date, latest_sma),
            xytext=(10, 0),
            textcoords='offset points',
            color=BLOOMBERG_COLORS["sma"],
            fontsize=9,
            va='center'
        )

    # 市值標註
    ax_mktcap.annotate(
        f'{latest_mktcap:.0f}',
        xy=(latest_date, latest_mktcap),
        xytext=(10, 0),
        textcoords='offset points',
        color=BLOOMBERG_COLORS["world_mktcap"],
        fontsize=9,
        va='center'
    )

    # 債券價格標註
    ax_bond.annotate(
        f'{latest_bond_price:.2f}',
        xy=(latest_date, latest_bond_price),
        xytext=(10, 0),
        textcoords='offset points',
        color=BLOOMBERG_COLORS["china_bond"],
        fontsize=9,
        va='center'
    )

    # === 格式化 X 軸 ===
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax1.xaxis.set_major_locator(mdates.YearLocator())
    ax1.tick_params(axis='x', colors=BLOOMBERG_COLORS["text_dim"])

    # 設定網格
    ax1.grid(True, color=BLOOMBERG_COLORS["grid"], alpha=0.3, linestyle='-', linewidth=0.5)
    ax1.set_axisbelow(True)

    # === 標題與圖例 ===
    fig.suptitle(
        title,
        color=BLOOMBERG_COLORS["text"],
        fontsize=14,
        fontweight='bold',
        y=0.98
    )

    # 創建圖例（中文）
    legend_elements = [
        plt.Line2D([0], [0], color=BLOOMBERG_COLORS["copper"], linewidth=2, label='銅期貨 LME 月線 (R1)'),
        plt.Line2D([0], [0], color=BLOOMBERG_COLORS["sma"], linewidth=1.5, linestyle='--', label=f'SMA(60) 收盤均線 (P1)  {latest_sma:,.0f}' if latest_sma else 'SMA(60) 收盤均線'),
        plt.Rectangle((0, 0), 1, 1, fc=BLOOMBERG_COLORS["world_mktcap"], alpha=BLOOMBERG_COLORS["world_mktcap_alpha"], label='全球股市總市值 (L2)'),
        plt.Line2D([0], [0], color=BLOOMBERG_COLORS["china_bond"], linewidth=1.5, label='中國10年期國債價格 (L1)'),
    ]

    ax1.legend(
        handles=legend_elements,
        loc='upper left',
        fontsize=8,
        facecolor=BLOOMBERG_COLORS["background"],
        edgecolor=BLOOMBERG_COLORS["grid"],
        labelcolor=BLOOMBERG_COLORS["text"]
    )

    # 來源標註
    fig.text(
        0.02, 0.02,
        source,
        color=BLOOMBERG_COLORS["text_dim"],
        fontsize=8,
        ha='left'
    )

    # 日期標註
    fig.text(
        0.98, 0.02,
        f'截至: {latest_date.strftime("%Y-%m-%d")}',
        color=BLOOMBERG_COLORS["text_dim"],
        fontsize=8,
        ha='right'
    )

    plt.tight_layout()
    plt.subplots_adjust(top=0.93, bottom=0.08)

    # 儲存
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor=BLOOMBERG_COLORS["background"])
    plt.close()

    print(f"圖表已儲存: {output_path}")


def generate_chart(
    start_date: str = "2015-01-01",
    end_date: str = None,
    output_path: str = None,
    figsize: Tuple[int, int] = (14, 8),
    dpi: int = 150,
    round_levels: list = [10000, 13000],
    ma_window: int = 60
) -> str:
    """
    生成完整的 Bloomberg 風格圖表

    Parameters
    ----------
    start_date : str
        起始日期
    end_date : str
        結束日期
    output_path : str
        輸出路徑（若無則自動生成）
    figsize : tuple
        圖表尺寸
    dpi : int
        解析度
    round_levels : list
        關卡位置
    ma_window : int
        SMA 視窗

    Returns
    -------
    str
        輸出檔案路徑
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    if output_path is None:
        today = datetime.now().strftime("%Y-%m-%d")
        output_path = f"output/copper_resilience_{today}.png"

    print("=" * 60)
    print("生成 Bloomberg 風格銅價股市韌性圖表")
    print("=" * 60)

    # 1. 抓取數據
    print("\n[1/4] 抓取數據...")
    copper = fetch_copper("HG=F", start_date, end_date, freq="1mo")
    world_mktcap = fetch_world_market_cap(start_date, end_date, freq="1mo")
    china_yield = fetch_china_10y_yield(start_date, end_date)

    # 2. 對齊數據
    print("\n[2/4] 對齊數據...")
    df = align_monthly({
        "copper": copper,
        "world_mktcap": world_mktcap,
        "china_yield": china_yield
    })
    print(f"  共 {len(df)} 筆月資料")

    # 3. 計算 SMA
    print("\n[3/4] 計算技術指標...")
    df["sma"] = df["copper"].rolling(ma_window, min_periods=1).mean()

    # 4. 繪製圖表
    print("\n[4/4] 繪製圖表...")
    plot_bloomberg_style(
        copper=df["copper"],
        copper_ohlc=None,
        sma=df["sma"],
        world_mktcap=df["world_mktcap"],
        china_yield=df["china_yield"],
        output_path=output_path,
        figsize=figsize,
        dpi=dpi,
        round_levels=round_levels
    )

    print("\n" + "=" * 60)
    print(f"完成！圖表已儲存至: {output_path}")
    print("=" * 60)

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="生成 Bloomberg 風格銅價股市韌性圖表"
    )
    parser.add_argument("--start", type=str, default="2015-01-01", help="起始日期")
    parser.add_argument("--end", type=str, default=None, help="結束日期")
    parser.add_argument("-o", "--output", type=str, default=None, help="輸出路徑")
    parser.add_argument("--figsize", type=str, default="14,8", help="圖表尺寸")
    parser.add_argument("--dpi", type=int, default=150, help="解析度")
    parser.add_argument("--levels", type=str, default="10000,13000", help="關卡位置")
    parser.add_argument("--ma-window", type=int, default=60, help="SMA 視窗")

    args = parser.parse_args()

    # 解析參數
    figsize = tuple(map(int, args.figsize.split(",")))
    round_levels = [float(x.strip()) for x in args.levels.split(",")]

    # 生成圖表
    generate_chart(
        start_date=args.start,
        end_date=args.end,
        output_path=args.output,
        figsize=figsize,
        dpi=args.dpi,
        round_levels=round_levels,
        ma_window=args.ma_window
    )


if __name__ == "__main__":
    main()
