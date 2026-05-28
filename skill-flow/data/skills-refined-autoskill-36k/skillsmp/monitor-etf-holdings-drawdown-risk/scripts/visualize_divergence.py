#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
visualize_divergence.py - ETF 持倉-價格背離視覺化

生成完整的背離分析報告圖表，包含：
1. 價格與庫存時間序列（雙 Y 軸）
2. 壓力分數儀表盤
3. 關鍵指標統計表
4. 歷史背離事件標記
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# 設定非交互式後端（避免 Segmentation fault）
import matplotlib
matplotlib.use('Agg')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def plot_gauge(ax, score: float, title: str = "壓力分數"):
    """
    繪製壓力分數儀表盤

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        繪圖軸
    score : float
        壓力分數（0-100）
    title : str
        標題
    """
    # 顏色分級
    if score >= 80:
        color = '#d32f2f'  # 紅色 - CRITICAL
        level = 'CRITICAL'
    elif score >= 60:
        color = '#f57c00'  # 橙色 - HIGH
        level = 'HIGH'
    elif score >= 30:
        color = '#fbc02d'  # 黃色 - MEDIUM
        level = 'MEDIUM'
    else:
        color = '#388e3c'  # 綠色 - LOW
        level = 'LOW'

    # 清空軸
    ax.clear()
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.2, 1.2)
    ax.axis('off')

    # 繪製背景圓弧（180度）
    theta = np.linspace(0, np.pi, 100)

    # 四個區間的背景
    zones = [
        (0, 30, '#c8e6c9'),      # 綠色區
        (30, 60, '#fff9c4'),     # 黃色區
        (60, 80, '#ffe0b2'),     # 橙色區
        (80, 100, '#ffcdd2')     # 紅色區
    ]

    for start, end, bg_color in zones:
        theta_zone = np.linspace(
            np.pi * (1 - start/100),
            np.pi * (1 - end/100),
            50
        )
        x_zone = 0.9 * np.cos(theta_zone)
        y_zone = 0.9 * np.sin(theta_zone)
        ax.fill_between(
            np.concatenate([[0], x_zone, [0]]),
            np.concatenate([[0], y_zone, [0]]),
            color=bg_color,
            alpha=0.3
        )

    # 繪製指針
    angle = np.pi * (1 - score/100)
    x_needle = [0, 0.8 * np.cos(angle)]
    y_needle = [0, 0.8 * np.sin(angle)]
    ax.plot(x_needle, y_needle, color=color, linewidth=4, zorder=10)
    ax.scatter([0], [0], s=200, color=color, zorder=11, edgecolors='white', linewidths=2)

    # 標記刻度
    for val in [0, 30, 60, 80, 100]:
        theta_tick = np.pi * (1 - val/100)
        x_tick = 1.0 * np.cos(theta_tick)
        y_tick = 1.0 * np.sin(theta_tick)
        ax.text(x_tick, y_tick, str(val), ha='center', va='center', fontsize=9)

    # 顯示分數與等級
    ax.text(0, -0.15, f'{score:.1f}', ha='center', va='top',
            fontsize=32, fontweight='bold', color=color)
    ax.text(0, 0.5, title, ha='center', va='center',
            fontsize=14, fontweight='bold')
    ax.text(0, 0.35, level, ha='center', va='center',
            fontsize=12, color=color, fontweight='bold')


def plot_metrics_table(ax, result: Dict[str, Any]):
    """
    繪製關鍵指標統計表

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        繪圖軸
    result : dict
        分析結果
    """
    ax.axis('off')

    # 準備表格數據
    metrics = [
        ['指標', '數值', '說明'],
        ['─' * 20, '─' * 15, '─' * 30],
        ['背離狀態',
         '是' if result['result']['divergence'] else '否',
         '價漲庫跌同時發生'],
        ['價格變化 (180天)',
         f"{result['result']['price_return_window']*100:+.1f}%",
         '視窗期價格變化率'],
        ['庫存變化 (180天)',
         f"{result['result']['inventory_change_window']*100:+.1f}%",
         '視窗期庫存變化率'],
        ['庫存十年低點',
         '是' if result['result']['inventory_decade_low'] else '否',
         '是否處於十年最低'],
        ['庫存百分位',
         f"{result['historical_context']['inventory_percentile']:.1f}%",
         '十年歷史中的位置'],
        ['庫存/價格 Z 分數',
         f"{result['result']['inventory_to_price_ratio_z']:.2f}",
         '標準化相對水平'],
    ]

    # 繪製表格
    table = ax.table(
        cellText=metrics,
        cellLoc='left',
        loc='center',
        bbox=[0, 0, 1, 1]
    )

    # 設定樣式
    table.auto_set_font_size(False)
    table.set_fontsize(9)

    # 標題行樣式
    for i in range(3):
        cell = table[(0, i)]
        cell.set_facecolor('#e3f2fd')
        cell.set_text_props(weight='bold')

    # 調整列寬
    table.auto_set_column_width([0, 1, 2])


def visualize_divergence(result_json_path: str, output_dir: Optional[str] = None):
    """
    生成完整的背離分析視覺化報告

    Parameters
    ----------
    result_json_path : str
        divergence_detector.py 生成的 JSON 結果路徑
    output_dir : str, optional
        輸出目錄，預設為項目根目錄的 output/
    """
    # 讀取結果
    with open(result_json_path, 'r', encoding='utf-8') as f:
        result = json.load(f)

    etf_ticker = result['inputs']['etf_ticker']
    commodity = result['inputs']['commodity_price_symbol']
    asof_date = result['asof']

    # 重新加載完整時間序列數據
    from fetch_prices import fetch_price_series
    from fetch_etf_holdings import fetch_etf_inventory_series

    print(f"重新加載 {commodity} 價格數據...")
    price = fetch_price_series(commodity, end_date=asof_date)

    print(f"重新加載 {etf_ticker} 持倉數據...")
    inventory = fetch_etf_inventory_series(etf_ticker, end_date=asof_date)

    # 對齊數據
    df = pd.concat({"price": price, "inv": inventory}, axis=1).sort_index()
    df["inv"] = df["inv"].ffill()
    df = df.dropna(subset=["price", "inv"])

    # 計算特徵（用於繪圖）
    w = result['inputs']['divergence_window_days']
    df["price_ret"] = df["price"].pct_change(w)
    df["inv_chg"] = df["inv"].pct_change(w)

    # 背離判定
    df["divergence"] = (
        (df["price_ret"] >= result['inputs']['min_price_return_pct']) &
        (df["inv_chg"] <= -result['inputs']['min_inventory_drawdown_pct'])
    )

    # 十年低點
    df["inv_decade_min"] = df["inv"].rolling(
        result['inputs']['decade_low_window_days'],
        min_periods=252
    ).min()
    df["decade_low_flag"] = df["inv"] <= df["inv_decade_min"] * 1.001

    # 創建圖表
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)

    # === 1. 主要時間序列圖（跨越整個上半部） ===
    ax1 = fig.add_subplot(gs[0:2, :])

    # 雙 Y 軸
    ax1_price = ax1
    ax1_inv = ax1.twinx()

    # 繪製價格
    line1 = ax1_price.plot(df.index, df['price'],
                            color='#1976d2', linewidth=1.5,
                            label=f'{commodity} 價格', zorder=3)
    ax1_price.set_ylabel('價格 (USD)', color='#1976d2', fontsize=11, fontweight='bold')
    ax1_price.tick_params(axis='y', labelcolor='#1976d2')
    ax1_price.grid(True, alpha=0.3, linestyle='--')

    # 繪製庫存
    line2 = ax1_inv.plot(df.index, df['inv'] / 1e6,  # 轉換為百萬盎司
                          color='#d32f2f', linewidth=1.5,
                          label=f'{etf_ticker} 持倉', zorder=2)
    ax1_inv.set_ylabel('持倉 (百萬盎司)', color='#d32f2f', fontsize=11, fontweight='bold')
    ax1_inv.tick_params(axis='y', labelcolor='#d32f2f')

    # 標記背離事件
    divergence_dates = df[df['divergence']].index
    if len(divergence_dates) > 0:
        for date in divergence_dates:
            ax1_price.axvline(date, color='orange', alpha=0.3, linewidth=2, zorder=1)

    # 標記十年低點
    decade_low_dates = df[df['decade_low_flag']].index
    if len(decade_low_dates) > 0:
        ax1_inv.scatter(decade_low_dates,
                        df.loc[decade_low_dates, 'inv'] / 1e6,
                        color='red', s=30, marker='v',
                        label='十年低點', zorder=4, alpha=0.6)

    # 標記當前位置
    latest_date = df.index[-1]
    ax1_price.scatter([latest_date], [df['price'].iloc[-1]],
                      color='blue', s=100, marker='o',
                      zorder=5, edgecolors='white', linewidths=2)
    ax1_inv.scatter([latest_date], [df['inv'].iloc[-1] / 1e6],
                    color='red', s=100, marker='o',
                    zorder=5, edgecolors='white', linewidths=2)

    # 圖例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    if len(decade_low_dates) > 0:
        lines.append(ax1_inv.collections[0])
        labels.append('十年低點')
    ax1_price.legend(lines, labels, loc='upper left', fontsize=10)

    # 標題
    divergence_status = "背離" if result['result']['divergence'] else "正常"
    ax1_price.set_title(
        f"{etf_ticker} 持倉-價格分析 | 狀態: {divergence_status} | 截至: {asof_date}",
        fontsize=14, fontweight='bold', pad=15
    )

    # 格式化 x 軸
    ax1_price.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1_price.xaxis.set_major_locator(mdates.YearLocator())
    plt.setp(ax1_price.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # === 2. 壓力分數儀表盤 ===
    ax2 = fig.add_subplot(gs[2, 0])
    plot_gauge(ax2, result['result']['stress_score_0_100'])

    # === 3. 關鍵指標表格 ===
    ax3 = fig.add_subplot(gs[2, 1:])
    plot_metrics_table(ax3, result)

    # 調整佈局
    plt.tight_layout()

    # 輸出
    if output_dir is None:
        # 預設為項目根目錄的 output/
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent.parent.parent
        output_dir = Path(project_root) / "output"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True, parents=True)

    # 檔名包含日期
    today = datetime.now().strftime("%Y%m%d")
    output_file = Path(output_dir) / f"{etf_ticker}_divergence_report_{today}.png"

    plt.savefig(str(output_file), dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ 報告已生成: {output_file}")

    # 同時生成 PDF
    output_file_pdf = Path(output_dir) / f"{etf_ticker}_divergence_report_{today}.pdf"
    plt.savefig(str(output_file_pdf), bbox_inches='tight', facecolor='white')
    print(f"✓ PDF 已生成: {output_file_pdf}")

    plt.close()

    return str(output_file)


def main():
    parser = argparse.ArgumentParser(
        description="ETF 持倉-價格背離視覺化"
    )
    parser.add_argument(
        "--result", "-r",
        required=True,
        help="divergence_detector.py 生成的 JSON 結果檔案路徑"
    )
    parser.add_argument(
        "--output", "-o",
        help="輸出目錄（預設為項目根目錄的 output/）"
    )

    args = parser.parse_args()

    # 生成視覺化
    output_file = visualize_divergence(
        result_json_path=args.result,
        output_dir=args.output
    )

    print(f"\n完成！圖表已儲存至: {output_file}")


if __name__ == "__main__":
    main()
