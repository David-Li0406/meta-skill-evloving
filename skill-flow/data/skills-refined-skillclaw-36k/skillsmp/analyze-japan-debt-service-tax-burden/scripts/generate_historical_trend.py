#!/usr/bin/env python3
"""
Japan Debt Historical Trend Analyzer

分析 2015-2025 年日本債務利息支出佔稅收比例的歷史趨勢。

Usage:
    python generate_historical_trend.py --output-dir ../../output
    python generate_historical_trend.py --start-year 2015 --end-year 2025
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib
matplotlib.use('Agg')  # 使用非互動式後端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd


# ============================================================================
# 常數設定
# ============================================================================

RISK_BANDS = {
    "green": (0.0, 0.25, "#2ecc71"),
    "yellow": (0.25, 0.40, "#f1c40f"),
    "orange": (0.40, 0.55, "#e67e22"),
    "red": (0.55, float("inf"), "#e74c3c"),
}


# ============================================================================
# 載入財政數據
# ============================================================================

def load_fiscal_data(config_path: Path) -> Dict:
    """載入財政數據配置"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def prepare_historical_dataframe(fiscal_config: Dict, start_year: int, end_year: int) -> pd.DataFrame:
    """準備歷史時間序列 DataFrame"""

    data_records = []

    for year in range(start_year, end_year + 1):
        fy_key = f"FY{year}"

        if fy_key not in fiscal_config['data']:
            print(f"警告: {fy_key} 數據不存在，跳過")
            continue

        fy_data = fiscal_config['data'][fy_key]

        tax_revenue = fy_data['tax_revenue_jpy']
        interest_payments = fy_data['interest_payments_jpy']
        debt_service = fy_data['debt_service_jpy']
        debt_stock = fy_data['debt_stock_jpy']

        # 計算關鍵比率
        interest_tax_ratio = interest_payments / tax_revenue
        debt_service_tax_ratio = debt_service / tax_revenue
        implied_avg_rate = interest_payments / debt_stock

        # 風險分級
        risk_band = get_risk_band(interest_tax_ratio)

        data_records.append({
            'fiscal_year': year,
            'fy_label': fy_key,
            'tax_revenue_jpy': tax_revenue,
            'interest_payments_jpy': interest_payments,
            'debt_service_jpy': debt_service,
            'debt_stock_jpy': debt_stock,
            'interest_tax_ratio': interest_tax_ratio,
            'debt_service_tax_ratio': debt_service_tax_ratio,
            'implied_avg_rate': implied_avg_rate,
            'risk_band': risk_band,
        })

    df = pd.DataFrame(data_records)
    df = df.sort_values('fiscal_year')

    return df


def get_risk_band(ratio: float) -> str:
    """判斷風險分級"""
    for band, (lower, upper, _) in RISK_BANDS.items():
        if lower <= ratio < upper:
            return band
    return "red"


# ============================================================================
# 視覺化
# ============================================================================

def setup_chinese_font():
    """設置中文字體"""
    chinese_fonts = [
        'Microsoft JhengHei',
        'Microsoft YaHei',
        'PingFang TC',
        'Noto Sans CJK TC',
        'Arial Unicode MS',
    ]

    for font_name in chinese_fonts:
        try:
            plt.rcParams['font.sans-serif'] = [font_name]
            plt.rcParams['axes.unicode_minus'] = False
            return
        except:
            continue

    print("警告: 無法找到中文字體，可能無法正確顯示中文")


def generate_trend_chart(df: pd.DataFrame, output_path: Path):
    """生成歷史趨勢圖表"""

    setup_chinese_font()

    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

    # ========== 圖1: Interest/Tax Ratio 歷史趨勢 ==========
    ax1 = fig.add_subplot(gs[0, :])

    # 繪製風險區間背景
    for band, (lower, upper, color) in RISK_BANDS.items():
        if upper == float("inf"):
            upper = 1.0
        ax1.axhspan(lower, upper, alpha=0.15, color=color, zorder=0)

    # 繪製主線
    ax1.plot(df['fiscal_year'], df['interest_tax_ratio'],
             marker='o', linewidth=2.5, markersize=8,
             color='#2c3e50', label='利息/稅收比', zorder=3)

    # 標註數值
    for _, row in df.iterrows():
        ax1.text(row['fiscal_year'], row['interest_tax_ratio'] + 0.005,
                f"{row['interest_tax_ratio']:.1%}",
                ha='center', va='bottom', fontsize=9, color='#34495e')

    ax1.set_xlabel('財政年度', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Interest / Tax Ratio', fontsize=12, fontweight='bold')
    ax1.set_title('日本債務利息支出佔稅收比例歷史趨勢 (2015-2025)',
                  fontsize=14, fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_ylim(0, 0.20)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0%}'))
    ax1.legend(loc='upper right', fontsize=10)

    # ========== 圖2: 稅收與利息支出趨勢 ==========
    ax2 = fig.add_subplot(gs[1, 0])

    x = df['fiscal_year']
    width = 0.35

    ax2.bar(x - width/2, df['tax_revenue_jpy'] / 1e12, width,
            label='稅收', color='#3498db', alpha=0.8)
    ax2.bar(x + width/2, df['interest_payments_jpy'] / 1e12, width,
            label='利息支出', color='#e74c3c', alpha=0.8)

    ax2.set_xlabel('財政年度', fontsize=11, fontweight='bold')
    ax2.set_ylabel('金額（兆日圓）', fontsize=11, fontweight='bold')
    ax2.set_title('稅收 vs 利息支出', fontsize=12, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=9)
    ax2.grid(True, alpha=0.3, axis='y', linestyle='--')

    # ========== 圖3: 債務存量趨勢 ==========
    ax3 = fig.add_subplot(gs[1, 1])

    ax3.fill_between(df['fiscal_year'], 0, df['debt_stock_jpy'] / 1e12,
                     alpha=0.6, color='#95a5a6')
    ax3.plot(df['fiscal_year'], df['debt_stock_jpy'] / 1e12,
             marker='s', linewidth=2, markersize=6, color='#2c3e50')

    ax3.set_xlabel('財政年度', fontsize=11, fontweight='bold')
    ax3.set_ylabel('債務存量（兆日圓）', fontsize=11, fontweight='bold')
    ax3.set_title('政府債務存量趨勢', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3, linestyle='--')

    # ========== 圖4: 隱含平均利率趨勢 ==========
    ax4 = fig.add_subplot(gs[2, 0])

    ax4.plot(df['fiscal_year'], df['implied_avg_rate'] * 100,
             marker='D', linewidth=2.5, markersize=7,
             color='#8e44ad', label='隱含平均利率')

    for _, row in df.iterrows():
        ax4.text(row['fiscal_year'], row['implied_avg_rate'] * 100 + 0.02,
                f"{row['implied_avg_rate']:.2%}",
                ha='center', va='bottom', fontsize=8, color='#6c3483')

    ax4.set_xlabel('財政年度', fontsize=11, fontweight='bold')
    ax4.set_ylabel('隱含平均利率 (%)', fontsize=11, fontweight='bold')
    ax4.set_title('債務隱含平均利率 (利息支出/債務存量)', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3, linestyle='--')
    ax4.legend(loc='upper left', fontsize=9)

    # ========== 圖5: 風險分級分布 ==========
    ax5 = fig.add_subplot(gs[2, 1])

    risk_counts = df['risk_band'].value_counts()
    risk_colors = [RISK_BANDS[band][2] for band in risk_counts.index]

    ax5.bar(range(len(risk_counts)), risk_counts.values,
            color=risk_colors, alpha=0.7)
    ax5.set_xticks(range(len(risk_counts)))
    ax5.set_xticklabels([band.upper() for band in risk_counts.index],
                        fontsize=10, fontweight='bold')
    ax5.set_ylabel('年度數量', fontsize=11, fontweight='bold')
    ax5.set_title('風險分級分布 (2015-2025)', fontsize=12, fontweight='bold')
    ax5.grid(True, alpha=0.3, axis='y', linestyle='--')

    # 加入圖表底部說明
    fig.text(0.5, 0.02,
             f'數據來源: 日本財務省 | 生成時間: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             ha='center', fontsize=9, color='#7f8c8d', style='italic')

    # 儲存圖表
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\n✓ 圖表已儲存至: {output_path}")

    plt.close()


def print_summary_table(df: pd.DataFrame):
    """列印摘要表格"""

    print("\n" + "="*80)
    print("日本債務利息負擔歷史趨勢摘要 (2015-2025)")
    print("="*80)
    print(f"\n{'年度':<8} {'稅收(兆)':<12} {'利息(兆)':<12} {'債務(兆)':<12} {'比率':<10} {'風險':<8}")
    print("-"*80)

    for _, row in df.iterrows():
        print(f"{row['fy_label']:<8} "
              f"{row['tax_revenue_jpy']/1e12:>10.2f}   "
              f"{row['interest_payments_jpy']/1e12:>10.2f}   "
              f"{row['debt_stock_jpy']/1e12:>10.0f}   "
              f"{row['interest_tax_ratio']:>8.1%}  "
              f"{row['risk_band'].upper():<8}")

    print("="*80)

    # 關鍵統計
    print("\n關鍵統計:")
    print(f"  - 比率範圍: {df['interest_tax_ratio'].min():.1%} ~ {df['interest_tax_ratio'].max():.1%}")
    print(f"  - 平均比率: {df['interest_tax_ratio'].mean():.1%}")
    print(f"  - 當前比率 (FY2025): {df.iloc[-1]['interest_tax_ratio']:.1%}")
    print(f"  - 趨勢: ", end="")

    if df.iloc[-1]['interest_tax_ratio'] > df.iloc[0]['interest_tax_ratio']:
        print(f"上升 ({df.iloc[0]['interest_tax_ratio']:.1%} → {df.iloc[-1]['interest_tax_ratio']:.1%})")
    else:
        print(f"下降 ({df.iloc[0]['interest_tax_ratio']:.1%} → {df.iloc[-1]['interest_tax_ratio']:.1%})")

    print("\n風險分級分布:")
    risk_dist = df['risk_band'].value_counts().sort_index()
    for band, count in risk_dist.items():
        print(f"  - {band.upper()}: {count} 年度")

    print("\n")


# ============================================================================
# 主程式
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='分析日本債務利息負擔歷史趨勢 (2015-2025)'
    )
    parser.add_argument('--start-year', type=int, default=2015,
                      help='起始年度 (預設: 2015)')
    parser.add_argument('--end-year', type=int, default=2025,
                      help='結束年度 (預設: 2025)')
    parser.add_argument('--output-dir', type=str, default='../../output',
                      help='輸出目錄 (預設: ../../output)')
    parser.add_argument('--output-file', type=str,
                      default=f'japan_debt_trend_{datetime.now().strftime("%Y%m%d")}.png',
                      help='輸出檔名')

    args = parser.parse_args()

    # 設定路徑
    script_dir = Path(__file__).parent
    config_path = script_dir.parent / 'config' / 'fiscal_data.json'
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / args.output_file

    # 載入數據
    print(f"\n載入財政數據: {config_path}")
    fiscal_config = load_fiscal_data(config_path)

    # 準備時間序列
    print(f"準備 {args.start_year}-{args.end_year} 年度數據...")
    df = prepare_historical_dataframe(fiscal_config, args.start_year, args.end_year)

    if df.empty:
        print("錯誤: 沒有可用的數據")
        sys.exit(1)

    # 列印摘要
    print_summary_table(df)

    # 生成圖表
    print("\n生成趨勢圖表...")
    generate_trend_chart(df, output_path)

    print("\n✓ 完成！")


if __name__ == '__main__':
    main()
