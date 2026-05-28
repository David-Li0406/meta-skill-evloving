#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
銅庫存回補訊號視覺化

生成 Bloomberg 風格的銅庫存回補訊號分析圖表。
支持 SHFE + COMEX 雙數據源。

Usage:
    python visualize_inventory_signal.py
    python visualize_inventory_signal.py --output path/to/output.png
"""

import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

import matplotlib
matplotlib.use('Agg')  # 非交互式後端，必須在 import pyplot 前設定

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd

from inventory_signal_analyzer import CopperInventorySignalAnalyzer


# ========== Bloomberg 風格配色（依據 bloomberg-style-chart-guide.md）==========
COLORS = {
    # 背景與網格
    "background": "#1a1a2e",
    "grid": "#2d2d44",

    # 文字
    "text": "#ffffff",
    "text_dim": "#888888",

    # 主要數據線
    "primary": "#00bfff",       # 淺藍色（銅價）
    "secondary": "#ff8c00",     # 橘色（SHFE 庫存）
    "tertiary": "#cc5500",      # 深橘色（COMEX 庫存）
    "total_inv": "#666666",     # 淡灰色（總庫存）

    # 訊號配色
    "caution": "#ff4444",       # 紅色（CAUTION 訊號）
    "supportive": "#00ff88",    # 綠色（SUPPORTIVE）
    "neutral": "#888888",       # 灰色（中性）

    # z-score 配色
    "z_positive": "#ff6b6b",    # 回補（紅色系）
    "z_negative": "#4ecdc4",    # 去庫存（青色系）

    # 面積圖
    "area_fill": "#ff8c00",
    "area_alpha": 0.4,

    # 輔助元素
    "level_line": "#666666",
}

# 中文字體設定
plt.rcParams['font.sans-serif'] = [
    'Microsoft JhengHei',  # Windows 正黑體
    'SimHei',              # Windows 黑體
    'Microsoft YaHei',     # Windows 微軟雅黑
    'PingFang TC',         # macOS 蘋方
    'Noto Sans CJK TC',    # Linux/通用
    'DejaVu Sans'          # 備用
]
plt.rcParams['axes.unicode_minus'] = False


def setup_bloomberg_style():
    """設定 Bloomberg 風格"""
    plt.style.use('dark_background')
    plt.rcParams.update({
        'figure.facecolor': COLORS['background'],
        'axes.facecolor': COLORS['background'],
        'axes.edgecolor': COLORS['grid'],
        'axes.labelcolor': COLORS['text'],
        'axes.grid': True,
        'grid.color': COLORS['grid'],
        'grid.alpha': 0.3,
        'grid.linestyle': '-',
        'grid.linewidth': 0.5,
        'text.color': COLORS['text'],
        'xtick.color': COLORS['text_dim'],
        'ytick.color': COLORS['text_dim'],
        'legend.facecolor': COLORS['background'],
        'legend.edgecolor': COLORS['grid'],
        'legend.labelcolor': COLORS['text'],
        'font.size': 10,
    })


def format_inventory(x, pos):
    """庫存格式化（K 表示千噸）"""
    if x >= 1000:
        return f'{x/1000:.0f}K'
    return f'{x:.0f}'


def create_signal_chart(
    df: pd.DataFrame,
    latest_status: Dict[str, Any],
    output_path: Optional[str] = None,
    title: str = "銅庫存回補訊號分析"
) -> None:
    """
    創建銅庫存回補訊號分析圖表（Bloomberg 風格）

    Parameters
    ----------
    df : pd.DataFrame
        包含 date, shfe_inventory, comex_inventory, close, 各類 z-score 等欄位
    latest_status : Dict[str, Any]
        最新狀態字典
    output_path : str, optional
        輸出路徑
    title : str
        圖表標題
    """
    setup_bloomberg_style()

    # 過濾有效數據（取最近 5 年）
    df = df.copy()
    df = df[df['date'] >= df['date'].max() - pd.Timedelta(days=5*365)]
    df = df.dropna(subset=['close'])

    fig, axes = plt.subplots(3, 1, figsize=(14, 10),
                              gridspec_kw={'height_ratios': [2, 1, 1]})
    fig.set_facecolor(COLORS['background'])

    # ========== 圖 1: 銅價 + 總庫存對照（雙軸）==========
    ax1 = axes[0]
    ax1.set_facecolor(COLORS['background'])

    # R1 右軸：銅價（主要指標）
    ax1.plot(df['date'], df['close'],
             color=COLORS['primary'], linewidth=2, label='銅價 (R1)', zorder=5)
    ax1.set_ylabel('銅價 (USD/lb)', color=COLORS['primary'], fontsize=10)
    ax1.tick_params(axis='y', labelcolor=COLORS['primary'])

    # L2 左軸：庫存面積圖（底層）
    ax1_twin = ax1.twinx()
    ax1_twin.spines['right'].set_position(('outward', 0))

    # 庫存數據檢查
    has_comex = 'comex_inventory' in df.columns and df['comex_inventory'].notna().any()
    has_shfe = 'shfe_inventory' in df.columns and df['shfe_inventory'].notna().any()

    if has_shfe and has_comex:
        # 計算總庫存
        total_inv = df['shfe_inventory'].fillna(0) + df['comex_inventory'].fillna(0)

        # 總庫存面積圖 + 虛線（最底層，淡灰色）
        ax1_twin.fill_between(df['date'], total_inv / 1000, 0,
                              color=COLORS['total_inv'], alpha=0.15, label='總庫存', zorder=1)
        ax1_twin.plot(df['date'], total_inv / 1000,
                      color=COLORS['total_inv'], linewidth=1.5, linestyle='--', alpha=0.7, zorder=2)

        # SHFE 庫存線（橘色實線）
        ax1_twin.plot(df['date'], df['shfe_inventory'].fillna(0) / 1000,
                      color=COLORS['secondary'], linewidth=1.5, label='SHFE', zorder=3)

        # COMEX 庫存線（深橘色實線）
        ax1_twin.plot(df['date'], df['comex_inventory'].fillna(0) / 1000,
                      color=COLORS['tertiary'], linewidth=1.5, label='COMEX', zorder=3)

    elif has_shfe:
        ax1_twin.fill_between(df['date'], df['shfe_inventory'] / 1000, 0,
                              color=COLORS['secondary'], alpha=0.3, label='SHFE 庫存', zorder=1)
        ax1_twin.plot(df['date'], df['shfe_inventory'] / 1000,
                      color=COLORS['secondary'], linewidth=1.5, zorder=2)
    elif has_comex:
        ax1_twin.fill_between(df['date'], df['comex_inventory'] / 1000, 0,
                              color=COLORS['tertiary'], alpha=0.3, label='COMEX 庫存', zorder=1)
        ax1_twin.plot(df['date'], df['comex_inventory'] / 1000,
                      color=COLORS['tertiary'], linewidth=1.5, zorder=2)

    ax1_twin.set_ylabel('庫存 (千噸)', color=COLORS['secondary'], fontsize=10)
    ax1_twin.tick_params(axis='y', labelcolor=COLORS['secondary'])
    ax1_twin.yaxis.set_major_formatter(FuncFormatter(format_inventory))

    # 標記 CAUTION 訊號觸發點
    if 'near_term_signal' in df.columns:
        caution_df = df[df['near_term_signal'] == 'CAUTION']
        if len(caution_df) > 0:
            ax1.scatter(caution_df['date'], caution_df['close'],
                        color=COLORS['caution'], s=60, marker='v',
                        label='CAUTION', zorder=6, edgecolors='white', linewidth=0.5)

    # 最新值標註
    if len(df) > 0:
        latest_date = df['date'].iloc[-1]
        latest_price = df['close'].iloc[-1]
        ax1.annotate(f'{latest_price:.2f}',
                     xy=(latest_date, latest_price),
                     xytext=(10, 0), textcoords='offset points',
                     color=COLORS['primary'], fontsize=11, fontweight='bold', va='center')

    # 圖例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax1_twin.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2,
               loc='upper left', fontsize=8, facecolor=COLORS['background'],
               edgecolor=COLORS['grid'])

    ax1.set_title('銅價 vs 庫存（SHFE + COMEX）', fontsize=11, color=COLORS['text'], pad=5)
    ax1.grid(True, color=COLORS['grid'], alpha=0.3, linewidth=0.5)
    ax1.set_axisbelow(True)

    # ========== 圖 2: SHFE 回補速度 z-score ==========
    ax2 = axes[1]
    ax2.set_facecolor(COLORS['background'])

    if 'shfe_rebuild_z' in df.columns:
        shfe_z = df['shfe_rebuild_z'].fillna(0)
        z_positive = shfe_z.clip(lower=0)
        z_negative = shfe_z.clip(upper=0)

        ax2.fill_between(df['date'], z_positive, 0,
                         color=COLORS['z_positive'], alpha=0.4, label='回補')
        ax2.fill_between(df['date'], z_negative, 0,
                         color=COLORS['z_negative'], alpha=0.4, label='去庫存')
        ax2.plot(df['date'], shfe_z, color=COLORS['secondary'], linewidth=1.2)

    # 門檻線
    ax2.axhline(y=1.5, color=COLORS['caution'], linestyle='--', linewidth=1, alpha=0.7)
    ax2.axhline(y=2.0, color=COLORS['caution'], linestyle='-', linewidth=1.5, alpha=0.5)
    ax2.axhline(y=-1.5, color=COLORS['supportive'], linestyle='--', linewidth=1, alpha=0.7)
    ax2.axhline(y=0, color=COLORS['text_dim'], linestyle='-', linewidth=0.5, alpha=0.5)

    ax2.set_ylabel('z-score', fontsize=10)
    ax2.set_ylim(-4, 4)
    ax2.legend(loc='upper right', fontsize=8, ncol=2,
               facecolor=COLORS['background'], edgecolor=COLORS['grid'])
    ax2.set_title('SHFE 回補情況', fontsize=11, color=COLORS['secondary'], pad=5)
    ax2.grid(True, color=COLORS['grid'], alpha=0.3, linewidth=0.5)
    ax2.set_axisbelow(True)

    # ========== 圖 3: COMEX 回補速度 z-score ==========
    ax3 = axes[2]
    ax3.set_facecolor(COLORS['background'])

    if 'comex_rebuild_z' in df.columns and df['comex_rebuild_z'].notna().any():
        comex_z = df['comex_rebuild_z'].fillna(0)
        z_positive = comex_z.clip(lower=0)
        z_negative = comex_z.clip(upper=0)

        ax3.fill_between(df['date'], z_positive, 0,
                         color=COLORS['z_positive'], alpha=0.4, label='回補')
        ax3.fill_between(df['date'], z_negative, 0,
                         color=COLORS['z_negative'], alpha=0.4, label='去庫存')
        ax3.plot(df['date'], comex_z, color=COLORS['tertiary'], linewidth=1.2)

    # 門檻線
    ax3.axhline(y=1.5, color=COLORS['caution'], linestyle='--', linewidth=1, alpha=0.7)
    ax3.axhline(y=2.0, color=COLORS['caution'], linestyle='-', linewidth=1.5, alpha=0.5)
    ax3.axhline(y=-1.5, color=COLORS['supportive'], linestyle='--', linewidth=1, alpha=0.7)
    ax3.axhline(y=0, color=COLORS['text_dim'], linestyle='-', linewidth=0.5, alpha=0.5)

    ax3.set_ylabel('z-score', fontsize=10)
    ax3.set_ylim(-4, 4)
    ax3.legend(loc='upper right', fontsize=8, ncol=2,
               facecolor=COLORS['background'], edgecolor=COLORS['grid'])
    ax3.set_title('COMEX 回補情況', fontsize=11, color=COLORS['tertiary'], pad=5)
    ax3.grid(True, color=COLORS['grid'], alpha=0.3, linewidth=0.5)
    ax3.set_axisbelow(True)

    # ========== 格式化 X 軸 ==========
    for ax in axes:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=0)

    # ========== 標題 ==========
    fig.suptitle(title, color=COLORS['text'], fontsize=14, fontweight='bold', y=0.995)

    # ========== 輸出 ==========
    plt.tight_layout()
    plt.subplots_adjust(top=0.92, bottom=0.04, hspace=0.35)

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=150, facecolor=COLORS['background'],
                    edgecolor='none', bbox_inches='tight')
        print(f"[Chart] 已保存到: {output_path}")
    else:
        plt.show()

    plt.close()


def main():
    parser = argparse.ArgumentParser(
        description="生成銅庫存回補訊號視覺化圖表（Bloomberg 風格）"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="輸出路徑（預設: output/copper_inventory_signal_YYYY-MM-DD.png）"
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default="cache",
        help="快取目錄"
    )
    parser.add_argument(
        "--root-output",
        action="store_true",
        default=True,
        help="輸出到根目錄 output/（預設）"
    )

    args = parser.parse_args()

    try:
        print("\n" + "=" * 60)
        print("銅庫存回補訊號視覺化")
        print("=" * 60 + "\n")

        # 載入並分析數據
        analyzer = CopperInventorySignalAnalyzer()
        df = analyzer.generate_signals(cache_dir=args.cache_dir)
        latest_status = analyzer.get_latest_status(df)

        # 決定輸出路徑
        if args.output:
            output_path = args.output
        else:
            # 預設輸出到根目錄 output/，檔名包含日期
            today = datetime.now().strftime('%Y-%m-%d')

            # 找到專案根目錄（向上找到 .claude 目錄的父目錄）
            current_dir = Path(__file__).resolve().parent
            root_dir = current_dir
            while root_dir.parent != root_dir:
                if (root_dir / '.claude').exists() or (root_dir / 'output').exists():
                    break
                root_dir = root_dir.parent

            # 如果在 skill 目錄內，向上找到專案根目錄
            if '.claude' in str(current_dir):
                # 從 .claude/skills/xxx/scripts 向上找
                root_dir = current_dir
                for _ in range(5):  # 最多向上 5 層
                    if (root_dir / 'output').exists() or root_dir.name == 'macro-skills':
                        break
                    root_dir = root_dir.parent

            output_path = root_dir / 'output' / f'copper_inventory_signal_{today}.png'

        # 生成圖表
        create_signal_chart(df, latest_status, output_path=str(output_path))

        return 0

    except Exception as e:
        print(f"\n[Error] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
