#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
銅價依賴度分析圖表

生成三面板綜合分析圖表：
1. 銅價 + 趨勢狀態 + 關卡線
2. 滾動 β 係數 + 歷史分位數帶
3. 股市韌性評分

輸出路徑：根目錄 output/ 或指定路徑
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

# 添加腳本目錄到路徑
sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_copper, fetch_equity, fetch_china_10y_yield, align_monthly

# 使用非交互式後端
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from matplotlib.ticker import FuncFormatter

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# Bloomberg 風格配色
COLORS = {
    "background": "#1a1a2e",
    "panel_bg": "#16213e",
    "grid": "#2d2d44",
    "text": "#ffffff",
    "text_dim": "#888888",
    "copper": "#ff6b35",
    "sma": "#ffaa00",
    "level_line": "#666666",
    "beta_line": "#00d4ff",
    "beta_fill_pos": "#00ff88",
    "beta_fill_neg": "#ff4444",
    "resilience": "#ff8c00",
    "resilience_high": "#00ff88",
    "resilience_low": "#ff4444",
    "trend_up": "#00ff8822",
    "trend_down": "#ff444422",
}


def calculate_rolling_beta(copper, equity, yield_series, window=24):
    """計算滾動 β 係數"""
    ret = pd.DataFrame({
        "dcopper": copper.pct_change(),
        "dequity": equity.pct_change(),
        "dyield": yield_series.diff()
    }).dropna()

    betas = []
    for i in range(window, len(ret) + 1):
        window_data = ret.iloc[i - window:i]
        y = window_data["dcopper"].values
        X = np.column_stack([
            np.ones(len(y)),
            window_data["dequity"].values,
            window_data["dyield"].values
        ])
        try:
            coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
            betas.append({
                "date": ret.index[i - 1],
                "beta_equity": coeffs[1],
                "beta_yield": coeffs[2],
            })
        except Exception:
            betas.append({
                "date": ret.index[i - 1],
                "beta_equity": np.nan,
                "beta_yield": np.nan,
            })

    return pd.DataFrame(betas).set_index("date")


def calculate_trend_state(prices, ma_window=60):
    """計算趨勢狀態"""
    df = pd.DataFrame({"price": prices})
    df["sma"] = df["price"].rolling(ma_window, min_periods=1).mean()
    df["sma_slope"] = df["sma"].diff()

    conditions = [
        (df["price"] > df["sma"]) & (df["sma_slope"] > 0),
        (df["price"] < df["sma"]) & (df["sma_slope"] < 0)
    ]
    choices = ["up", "down"]
    df["trend"] = np.select(conditions, choices, default="range")

    return df


def calculate_resilience_score(equity, sma_period=12, drawdown_period=3):
    """計算股市韌性評分"""
    df = pd.DataFrame({"equity": equity})
    df["return_12m"] = df["equity"].pct_change(12)
    df["momentum_score"] = df["return_12m"].rank(pct=True) * 100
    df["sma"] = df["equity"].rolling(sma_period, min_periods=1).mean()
    df["above_sma"] = (df["equity"] > df["sma"]).astype(int) * 100
    df["rolling_max"] = df["equity"].rolling(drawdown_period, min_periods=1).max()
    df["drawdown"] = (df["rolling_max"] - df["equity"]) / df["rolling_max"]
    df["drawdown_score"] = (1 - np.clip(df["drawdown"] / 0.15, 0, 1)) * 100

    df["resilience_score"] = (
        0.4 * df["momentum_score"] +
        0.4 * df["above_sma"] +
        0.2 * df["drawdown_score"]
    )
    return df["resilience_score"]


def plot_dependency_analysis(
    df,
    output_path,
    round_levels=[10000, 13000],
    figsize=(14, 12),
    dpi=150
):
    """
    繪製三面板依賴度分析圖表

    Parameters
    ----------
    df : pd.DataFrame
        包含 copper, sma, trend, beta_equity, resilience_score 的 DataFrame
    output_path : str
        輸出路徑
    round_levels : list
        關卡位置
    figsize : tuple
        圖表尺寸
    dpi : int
        解析度
    """
    plt.style.use('dark_background')

    fig, axes = plt.subplots(3, 1, figsize=figsize, facecolor=COLORS["background"],
                             gridspec_kw={'height_ratios': [3, 2, 1.5], 'hspace': 0.08})

    for ax in axes:
        ax.set_facecolor(COLORS["panel_bg"])
        ax.grid(True, color=COLORS["grid"], alpha=0.3, linestyle='-', linewidth=0.5)
        ax.tick_params(colors=COLORS["text_dim"])

    # ===== 面板 1: 銅價 + 趨勢 + 關卡 =====
    ax1 = axes[0]

    # 繪製趨勢背景色帶
    trend_changes = df["trend"].ne(df["trend"].shift()).cumsum()
    for _, group in df.groupby(trend_changes):
        if len(group) < 2:
            continue
        trend = group["trend"].iloc[0]
        if trend == "up":
            ax1.axvspan(group.index[0], group.index[-1], color=COLORS["trend_up"], zorder=0)
        elif trend == "down":
            ax1.axvspan(group.index[0], group.index[-1], color=COLORS["trend_down"], zorder=0)

    # 繪製銅價
    ax1.plot(df.index, df["copper"], color=COLORS["copper"], linewidth=2, label="銅價 (USD/ton)", zorder=3)

    # 繪製 SMA
    ax1.plot(df.index, df["sma"], color=COLORS["sma"], linewidth=1.5, linestyle="--", label="SMA(60)", zorder=2)

    # 繪製關卡線
    for level in round_levels:
        ax1.axhline(y=level, color=COLORS["level_line"], linestyle=":", alpha=0.7, zorder=1)
        ax1.text(df.index[-1], level, f" {level:,.0f}", va="center", ha="left",
                 color=COLORS["text_dim"], fontsize=9)

    # 標註當前價格
    latest_copper = df["copper"].iloc[-1]
    latest_sma = df["sma"].iloc[-1]
    ax1.annotate(f'{latest_copper:,.0f}', xy=(df.index[-1], latest_copper),
                 xytext=(10, 0), textcoords='offset points',
                 color=COLORS["copper"], fontsize=11, fontweight='bold', va='center')
    ax1.annotate(f'{latest_sma:,.0f}', xy=(df.index[-1], latest_sma),
                 xytext=(10, 0), textcoords='offset points',
                 color=COLORS["sma"], fontsize=9, va='center')

    ax1.set_ylabel("銅價 (USD/ton)", color=COLORS["text"], fontsize=10)
    ax1.legend(loc="upper left", fontsize=8, facecolor=COLORS["panel_bg"],
               edgecolor=COLORS["grid"], labelcolor=COLORS["text"])
    ax1.set_title("銅價依賴度分析", color=COLORS["text"], fontsize=14, fontweight="bold", pad=15)

    # 添加趨勢圖例
    legend_text = "■ 上升趨勢  ■ 下降趨勢  □ 區間整理"
    ax1.text(0.98, 0.02, legend_text, transform=ax1.transAxes, ha="right", va="bottom",
             fontsize=8, color=COLORS["text_dim"])

    # ===== 面板 2: 滾動 β 係數 =====
    ax2 = axes[1]

    beta = df["beta_equity"].dropna()
    if len(beta) > 0:
        # 計算歷史分位數
        beta_mean = beta.mean()
        beta_std = beta.std()
        beta_p25 = beta.quantile(0.25)
        beta_p75 = beta.quantile(0.75)

        # 繪製 ±1σ 範圍
        ax2.fill_between(beta.index, beta_mean - beta_std, beta_mean + beta_std,
                         color="#4a4a6a", alpha=0.3, label="±1σ 範圍")

        # 繪製 β 線
        ax2.plot(beta.index, beta.values, color=COLORS["beta_line"], linewidth=1.5, label="β (股市)")

        # 填充正負區域
        ax2.fill_between(beta.index, 0, beta.values,
                         where=beta.values >= 0, color=COLORS["beta_fill_pos"], alpha=0.3)
        ax2.fill_between(beta.index, 0, beta.values,
                         where=beta.values < 0, color=COLORS["beta_fill_neg"], alpha=0.3)

        # 零線
        ax2.axhline(y=0, color=COLORS["text_dim"], linestyle="-", linewidth=1, alpha=0.5)

        # 歷史均值線
        ax2.axhline(y=beta_mean, color="#888888", linestyle="--", linewidth=1, alpha=0.7)
        ax2.text(beta.index[0], beta_mean, f" 均值: {beta_mean:.2f}", va="center",
                 color=COLORS["text_dim"], fontsize=8)

        # 標註當前值
        latest_beta = beta.iloc[-1]
        beta_pct = (beta <= latest_beta).mean() * 100
        ax2.annotate(f'{latest_beta:.2f}\n({beta_pct:.0f}%分位)',
                     xy=(beta.index[-1], latest_beta),
                     xytext=(10, 0), textcoords='offset points',
                     color=COLORS["beta_line"], fontsize=10, fontweight='bold', va='center')

        # 標記極端區域
        if latest_beta < 0:
            ax2.text(0.5, 0.95, "[!] β < 0：銅與股市呈反向關係", transform=ax2.transAxes,
                     ha="center", va="top", fontsize=10, color=COLORS["beta_fill_neg"],
                     fontweight="bold", bbox=dict(boxstyle="round", fc=COLORS["panel_bg"], ec=COLORS["beta_fill_neg"]))

    ax2.set_ylabel("滾動 β 係數 (24M)", color=COLORS["text"], fontsize=10)
    ax2.legend(loc="upper left", fontsize=8, facecolor=COLORS["panel_bg"],
               edgecolor=COLORS["grid"], labelcolor=COLORS["text"])

    # ===== 面板 3: 股市韌性評分 =====
    ax3 = axes[2]

    resilience = df["resilience_score"].dropna()
    if len(resilience) > 0:
        # 繪製韌性評分
        ax3.fill_between(resilience.index, 0, resilience.values,
                         color=COLORS["resilience"], alpha=0.4)
        ax3.plot(resilience.index, resilience.values, color=COLORS["resilience"], linewidth=1.5)

        # 繪製閾值線
        ax3.axhline(y=70, color=COLORS["resilience_high"], linestyle="--", linewidth=1, alpha=0.7)
        ax3.axhline(y=30, color=COLORS["resilience_low"], linestyle="--", linewidth=1, alpha=0.7)

        ax3.text(resilience.index[0], 70, " 高韌性 (70)", va="center",
                 color=COLORS["resilience_high"], fontsize=8)
        ax3.text(resilience.index[0], 30, " 低韌性 (30)", va="center",
                 color=COLORS["resilience_low"], fontsize=8)

        # 標註當前值
        latest_resilience = resilience.iloc[-1]
        color = COLORS["resilience_high"] if latest_resilience >= 70 else (
            COLORS["resilience_low"] if latest_resilience <= 30 else COLORS["resilience"])
        ax3.annotate(f'{latest_resilience:.0f}',
                     xy=(resilience.index[-1], latest_resilience),
                     xytext=(10, 0), textcoords='offset points',
                     color=color, fontsize=11, fontweight='bold', va='center')

    ax3.set_ylabel("韌性評分", color=COLORS["text"], fontsize=10)
    ax3.set_ylim(0, 100)

    # X 軸格式
    for ax in axes:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        ax.xaxis.set_major_locator(mdates.YearLocator())

    # 只在最下方顯示 X 軸標籤
    for ax in axes[:-1]:
        ax.tick_params(labelbottom=False)

    # 來源與日期標註
    fig.text(0.02, 0.01, "資料來源: Yahoo Finance, MacroMicro",
             color=COLORS["text_dim"], fontsize=8, ha="left")
    fig.text(0.98, 0.01, f"截至: {df.index[-1].strftime('%Y-%m-%d')}",
             color=COLORS["text_dim"], fontsize=8, ha="right")

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.05)

    # 儲存
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight', facecolor=COLORS["background"])
    plt.close()

    print(f"圖表已儲存: {output_path}")
    return str(output_path)


def generate_dependency_chart(
    start_date="2015-01-01",
    end_date=None,
    output_path=None,
    figsize=(14, 12),
    dpi=150,
    round_levels=[10000, 13000],
    ma_window=60,
    rolling_window=24
):
    """
    生成依賴度分析圖表

    Parameters
    ----------
    start_date : str
        起始日期
    end_date : str
        結束日期
    output_path : str
        輸出路徑
    figsize : tuple
        圖表尺寸
    dpi : int
        解析度
    round_levels : list
        關卡位置
    ma_window : int
        SMA 視窗
    rolling_window : int
        滾動迴歸視窗

    Returns
    -------
    str
        輸出檔案路徑
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    if output_path is None:
        today = datetime.now().strftime("%Y-%m-%d")
        # 預設輸出到專案根目錄的 output/
        output_path = Path(__file__).parent.parent.parent.parent.parent / "output" / f"copper-dependency-analysis-{today}.png"

    print("=" * 60)
    print("生成銅價依賴度分析圖表")
    print("=" * 60)

    # 1. 抓取數據
    print("\n[1/5] 抓取數據...")
    copper = fetch_copper("HG=F", start_date, end_date, freq="1mo")
    equity = fetch_equity("ACWI", start_date, end_date, freq="1mo")
    cny10y = fetch_china_10y_yield(start_date, end_date)

    # 2. 對齊數據
    print("\n[2/5] 對齊數據...")
    df = align_monthly({
        "copper": copper,
        "equity": equity,
        "cny10y": cny10y
    })
    print(f"  共 {len(df)} 筆月資料")

    # 3. 計算趨勢狀態
    print("\n[3/5] 計算趨勢狀態...")
    trend_df = calculate_trend_state(df["copper"], ma_window)
    df = df.join(trend_df[["sma", "trend"]])

    # 4. 計算滾動 β
    print("\n[4/5] 計算滾動 β...")
    betas = calculate_rolling_beta(df["copper"], df["equity"], df["cny10y"], rolling_window)
    df = df.join(betas)

    # 5. 計算韌性評分
    print("\n[5/5] 計算韌性評分...")
    df["resilience_score"] = calculate_resilience_score(df["equity"])

    # 繪製圖表
    print("\n繪製圖表...")
    result_path = plot_dependency_analysis(
        df,
        output_path,
        round_levels=round_levels,
        figsize=figsize,
        dpi=dpi
    )

    print("\n" + "=" * 60)
    print(f"完成！圖表已儲存至: {result_path}")
    print("=" * 60)

    return result_path


def main():
    parser = argparse.ArgumentParser(
        description="生成銅價依賴度分析圖表"
    )
    parser.add_argument("--start", type=str, default="2015-01-01", help="起始日期")
    parser.add_argument("--end", type=str, default=None, help="結束日期")
    parser.add_argument("-o", "--output", type=str, default=None, help="輸出路徑")
    parser.add_argument("--figsize", type=str, default="14,12", help="圖表尺寸")
    parser.add_argument("--dpi", type=int, default=150, help="解析度")
    parser.add_argument("--levels", type=str, default="10000,13000", help="關卡位置")
    parser.add_argument("--ma-window", type=int, default=60, help="SMA 視窗")
    parser.add_argument("--rolling-window", type=int, default=24, help="滾動迴歸視窗")

    args = parser.parse_args()

    # 解析參數
    figsize = tuple(map(int, args.figsize.split(",")))
    round_levels = [float(x.strip()) for x in args.levels.split(",")]

    # 生成圖表
    generate_dependency_chart(
        start_date=args.start,
        end_date=args.end,
        output_path=args.output,
        figsize=figsize,
        dpi=args.dpi,
        round_levels=round_levels,
        ma_window=args.ma_window,
        rolling_window=args.rolling_window
    )


if __name__ == "__main__":
    main()
