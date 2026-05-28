#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
計算貴金屬礦業毛利率 (Precious Miner Gross Margin Calculator)

計算黃金/白銀礦業的毛利率代理值，並判斷歷史分位數位置。

Usage:
    python margin_calculator.py --quick --metal gold
    python margin_calculator.py --metal silver --miners CDE,HL,AG --frequency quarterly
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

try:
    import yfinance as yf
except ImportError:
    yf = None
    print("Warning: yfinance not installed. Run: pip install yfinance")

# =============================================================================
# 常數定義
# =============================================================================

# 預設礦業籃子
DEFAULT_BASKETS = {
    "gold": ["NEM", "GOLD", "AEM", "KGC", "AU"],
    "silver": ["CDE", "HL", "AG", "PAAS", "MAG"],
}

# 期貨代碼
METAL_TICKERS = {
    "gold": "GC=F",
    "silver": "SI=F",
}

# 範例成本數據（實際使用時應從外部載入或爬取）
# 格式：{miner: {quarter: {"aisc": float, "production": int}}}
SAMPLE_COST_DATA = {
    "gold": {
        "NEM": {
            "2024-Q4": {"aisc": 1350, "production": 1600000},
            "2024-Q3": {"aisc": 1380, "production": 1550000},
            "2024-Q2": {"aisc": 1320, "production": 1480000},
            "2024-Q1": {"aisc": 1290, "production": 1420000},
        },
        "GOLD": {
            "2024-Q4": {"aisc": 1290, "production": 1200000},
            "2024-Q3": {"aisc": 1310, "production": 1180000},
            "2024-Q2": {"aisc": 1280, "production": 1150000},
            "2024-Q1": {"aisc": 1250, "production": 1100000},
        },
        "AEM": {
            "2024-Q4": {"aisc": 1310, "production": 900000},
            "2024-Q3": {"aisc": 1340, "production": 880000},
            "2024-Q2": {"aisc": 1300, "production": 850000},
            "2024-Q1": {"aisc": 1270, "production": 820000},
        },
    },
    "silver": {
        "CDE": {
            "2024-Q4": {"aisc": 18.50, "production": 2800000},
            "2024-Q3": {"aisc": 19.20, "production": 2650000},
            "2024-Q2": {"aisc": 18.80, "production": 2500000},
            "2024-Q1": {"aisc": 19.50, "production": 2400000},
        },
        "HL": {
            "2024-Q4": {"aisc": 17.80, "production": 3500000},
            "2024-Q3": {"aisc": 18.10, "production": 3400000},
            "2024-Q2": {"aisc": 17.50, "production": 3300000},
            "2024-Q1": {"aisc": 17.90, "production": 3200000},
        },
        "AG": {
            "2024-Q4": {"aisc": 19.20, "production": 5000000},
            "2024-Q3": {"aisc": 19.80, "production": 4800000},
            "2024-Q2": {"aisc": 19.50, "production": 4600000},
            "2024-Q1": {"aisc": 20.10, "production": 4400000},
        },
    },
}


# =============================================================================
# 核心計算函數
# =============================================================================


def margin_proxy(price: float, unit_cost: float) -> float:
    """計算毛利率代理值

    Args:
        price: 金屬價格 (USD/oz)
        unit_cost: 單位成本 (USD/oz)

    Returns:
        毛利率代理值 (0-1)
    """
    if price <= 0:
        return 0.0
    return max(0.0, (price - unit_cost) / price)


def get_metal_price(
    metal: str,
    start_date: str,
    end_date: str,
    frequency: str = "quarterly",
) -> pd.Series:
    """取得金屬價格序列

    Args:
        metal: 金屬類型 ("gold" / "silver")
        start_date: 起始日期 (YYYY-MM-DD)
        end_date: 結束日期 (YYYY-MM-DD)
        frequency: 頻率 ("daily" / "weekly" / "monthly" / "quarterly")

    Returns:
        價格序列 (pd.Series)
    """
    if yf is None:
        raise ImportError("yfinance is required. Run: pip install yfinance")

    ticker = METAL_TICKERS.get(metal)
    if not ticker:
        raise ValueError(f"Unknown metal: {metal}")

    # 下載數據
    df = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if df.empty:
        raise ValueError(f"No price data found for {ticker}")

    # 取收盤價
    if isinstance(df.columns, pd.MultiIndex):
        price = df["Close"][ticker]
    else:
        price = df["Close"]

    # 重採樣
    freq_map = {
        "daily": "D",
        "weekly": "W",
        "monthly": "M",
        "quarterly": "Q",
    }
    resample_freq = freq_map.get(frequency, "Q")
    price_resampled = price.resample(resample_freq).mean()

    return price_resampled.dropna()


def load_cost_data(
    metal: str,
    miners: List[str],
    cost_metric: str = "AISC",
) -> Tuple[Dict[str, pd.Series], Dict[str, pd.Series]]:
    """載入成本數據

    Args:
        metal: 金屬類型
        miners: 礦業清單
        cost_metric: 成本口徑

    Returns:
        (成本字典, 產量字典)
    """
    # 使用範例數據（實際應從外部載入）
    sample_data = SAMPLE_COST_DATA.get(metal, {})

    costs = {}
    productions = {}

    for miner in miners:
        if miner not in sample_data:
            print(f"Warning: No cost data for {miner}")
            continue

        miner_data = sample_data[miner]
        dates = []
        aisc_values = []
        prod_values = []

        for quarter, values in miner_data.items():
            # 解析季度為日期
            year, q = quarter.split("-Q")
            month = int(q) * 3
            date = pd.Timestamp(year=int(year), month=month, day=1)
            dates.append(date)
            aisc_values.append(values.get("aisc", 0))
            prod_values.append(values.get("production", 0))

        if dates:
            costs[miner] = pd.Series(aisc_values, index=dates).sort_index()
            productions[miner] = pd.Series(prod_values, index=dates).sort_index()

    return costs, productions


def align_cost_to_price_index(
    cost_series: pd.Series,
    price_index: pd.DatetimeIndex,
) -> pd.Series:
    """對齊成本到價格索引

    Args:
        cost_series: 成本序列
        price_index: 價格索引

    Returns:
        對齊後的成本序列
    """
    return cost_series.reindex(price_index, method="ffill")


def aggregate_margins(
    margins_df: pd.DataFrame,
    weights_df: Optional[pd.DataFrame] = None,
    mode: str = "production_weighted",
) -> pd.Series:
    """聚合毛利率

    Args:
        margins_df: 各礦業毛利率 DataFrame
        weights_df: 權重 DataFrame (可選)
        mode: 聚合模式

    Returns:
        籃子毛利率序列
    """
    if mode == "equal_weight" or weights_df is None:
        return margins_df.mean(axis=1)

    # 正規化權重
    w = weights_df.div(weights_df.sum(axis=1), axis=0).fillna(0.0)
    return (margins_df * w).sum(axis=1)


def compute_percentile_rank(
    series: pd.Series,
    window_years: int = 20,
) -> pd.Series:
    """計算滾動歷史分位數

    Args:
        series: 輸入序列
        window_years: 視窗年數

    Returns:
        分位數排名序列
    """
    window = window_years * 4  # 季度

    def rank_func(x):
        if len(x) < 2:
            return np.nan
        return (x.iloc[-1] > x.iloc[:-1]).mean()

    ranks = series.rolling(window, min_periods=4).apply(rank_func, raw=False)
    return ranks


def regime_label(percentile: float) -> str:
    """區間標記

    Args:
        percentile: 分位數 (0-1)

    Returns:
        區間標籤
    """
    if np.isnan(percentile):
        return "unknown"
    if percentile >= 0.9:
        return "extreme_high_margin"
    elif percentile >= 0.7:
        return "high_margin"
    elif percentile >= 0.3:
        return "neutral"
    elif percentile >= 0.1:
        return "low_margin"
    else:
        return "extreme_low_margin"


def decompose_driver(
    price_series: pd.Series,
    cost_series: pd.Series,
    lookback: int = 3,
) -> Dict:
    """驅動拆解

    Args:
        price_series: 價格序列
        cost_series: 成本序列
        lookback: 回顧期數

    Returns:
        驅動分析結果
    """
    if len(price_series) < lookback + 1 or len(cost_series) < lookback + 1:
        return {"driver": "insufficient_data"}

    price_change = (price_series.iloc[-1] / price_series.iloc[-lookback - 1]) - 1
    cost_change = (cost_series.iloc[-1] / cost_series.iloc[-lookback - 1]) - 1

    if abs(price_change) > abs(cost_change) * 2:
        driver = "mostly_price_" + ("up" if price_change > 0 else "down")
    elif abs(cost_change) > abs(price_change) * 2:
        driver = "mostly_cost_" + ("down" if cost_change < 0 else "up")
    else:
        driver = "mixed"

    return {
        "lookback_quarters": lookback,
        "price_change_pct": round(price_change, 4),
        "cost_change_pct": round(cost_change, 4),
        "driver": driver,
    }


def winsorize(series: pd.Series, lower: float = 0.01, upper: float = 0.99) -> pd.Series:
    """Winsorize 離群值

    Args:
        series: 輸入序列
        lower: 下分位數
        upper: 上分位數

    Returns:
        處理後的序列
    """
    low = series.quantile(lower)
    high = series.quantile(upper)
    return series.clip(low, high)


# =============================================================================
# 主計算流程
# =============================================================================


def calculate_margin_analysis(
    metal: str,
    miners: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    frequency: str = "quarterly",
    cost_metric: str = "AISC",
    aggregation: str = "production_weighted",
    history_window_years: int = 20,
    outlier_rule: str = "winsorize_1_99",
) -> Dict:
    """執行完整毛利率分析

    Args:
        metal: 金屬類型
        miners: 礦業清單
        start_date: 起始日期
        end_date: 結束日期
        frequency: 頻率
        cost_metric: 成本口徑
        aggregation: 聚合方式
        history_window_years: 歷史視窗
        outlier_rule: 離群處理

    Returns:
        分析結果字典
    """
    # 預設值
    if miners is None:
        miners = DEFAULT_BASKETS.get(metal, [])[:3]  # 使用前 3 個
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if start_date is None:
        start_date = (datetime.now() - timedelta(days=365 * 10)).strftime("%Y-%m-%d")

    # 1. 取得價格
    try:
        price_series = get_metal_price(metal, start_date, end_date, frequency)
    except Exception as e:
        return {"error": f"Failed to get price data: {e}"}

    # 2. 載入成本
    costs, productions = load_cost_data(metal, miners, cost_metric)
    if not costs:
        return {"error": "No cost data available"}

    # 3. 計算各礦業毛利率
    margins = {}
    aligned_costs = {}
    for miner in costs:
        aligned_cost = align_cost_to_price_index(costs[miner], price_series.index)
        aligned_costs[miner] = aligned_cost
        margins[miner] = pd.Series(
            [margin_proxy(p, c) for p, c in zip(price_series, aligned_cost)],
            index=price_series.index,
        )

    margins_df = pd.DataFrame(margins)
    productions_df = pd.DataFrame(
        {m: align_cost_to_price_index(productions[m], price_series.index) for m in productions}
    )

    # 4. 離群處理
    if outlier_rule == "winsorize_1_99":
        for col in margins_df.columns:
            margins_df[col] = winsorize(margins_df[col], 0.01, 0.99)

    # 5. 聚合籃子毛利率
    basket_margin = aggregate_margins(margins_df, productions_df, aggregation)

    # 6. 計算加權成本
    aligned_costs_df = pd.DataFrame(aligned_costs)
    if aggregation == "production_weighted" and not productions_df.empty:
        w = productions_df.div(productions_df.sum(axis=1), axis=0).fillna(0)
        weighted_cost = (aligned_costs_df * w).sum(axis=1)
    else:
        weighted_cost = aligned_costs_df.mean(axis=1)

    # 7. 歷史分位數
    percentile_series = compute_percentile_rank(basket_margin, history_window_years)

    # 8. 最新數據
    latest_idx = basket_margin.dropna().index[-1] if not basket_margin.dropna().empty else None
    if latest_idx is None:
        return {"error": "No valid margin data"}

    latest_margin = basket_margin.loc[latest_idx]
    latest_percentile = percentile_series.loc[latest_idx] if latest_idx in percentile_series.index else np.nan
    latest_price = price_series.loc[latest_idx] if latest_idx in price_series.index else np.nan
    latest_cost = weighted_cost.loc[latest_idx] if latest_idx in weighted_cost.index else np.nan

    # 9. 驅動拆解
    decomposition = decompose_driver(price_series.dropna(), weighted_cost.dropna(), lookback=3)

    # 10. 礦業詳情
    miner_details = []
    for miner in margins_df.columns:
        if latest_idx in margins_df.index:
            miner_margin = margins_df.loc[latest_idx, miner]
            miner_cost = aligned_costs_df.loc[latest_idx, miner] if latest_idx in aligned_costs_df.index else np.nan
            miner_prod = productions_df.loc[latest_idx, miner] if latest_idx in productions_df.index else np.nan
            miner_details.append(
                {
                    "ticker": miner,
                    "aisc_usd_oz": round(miner_cost, 2) if not np.isnan(miner_cost) else None,
                    "production_oz": int(miner_prod) if not np.isnan(miner_prod) else None,
                    "margin_proxy": round(miner_margin, 4) if not np.isnan(miner_margin) else None,
                    "margin_vs_basket": round(miner_margin - latest_margin, 4)
                    if not np.isnan(miner_margin)
                    else None,
                }
            )

    # 計算權重
    if aggregation == "production_weighted" and latest_idx in productions_df.index:
        total_prod = productions_df.loc[latest_idx].sum()
        weights = {m: round(productions_df.loc[latest_idx, m] / total_prod, 3) for m in productions_df.columns}
    else:
        weights = {m: round(1.0 / len(miners), 3) for m in miners if m in margins_df.columns}

    # 組裝結果
    result = {
        "skill": "compute_precious_miner_margin_proxy",
        "generated_at": datetime.now().isoformat() + "Z",
        "version": "0.1.0",
        "parameters": {
            "metal": metal,
            "miners": miners,
            "start_date": start_date,
            "end_date": end_date,
            "frequency": frequency,
            "cost_metric": cost_metric,
            "aggregation": aggregation,
            "history_window_years": history_window_years,
        },
        "basket": {
            "miners": list(margins_df.columns),
            "aggregation": aggregation,
            "weights": weights,
        },
        "latest": {
            "date": latest_idx.strftime("%Y-Q%q").replace("Q1", "Q1").replace("Q2", "Q2").replace("Q3", "Q3").replace(
                "Q4", "Q4"
            )
            if hasattr(latest_idx, "quarter")
            else latest_idx.strftime("%Y-%m"),
            "metal_price_usd_oz": round(latest_price, 2) if not np.isnan(latest_price) else None,
            "unit_cost_proxy_usd_oz": round(latest_cost, 2) if not np.isnan(latest_cost) else None,
            "gross_margin_proxy": round(latest_margin, 4),
            "history_percentile": round(latest_percentile, 2) if not np.isnan(latest_percentile) else None,
            "regime_label": regime_label(latest_percentile),
        },
        "miner_details": miner_details,
        "decomposition": decomposition,
        "notes": [
            "gross_margin_proxy 使用 (price - AISC)/price 作為近似；不等同會計報表的毛利率口徑。",
            f"成本為{frequency}資料，已對齊至價格索引。",
            f"歷史分位數基於 {history_window_years} 年滾動視窗計算。",
        ],
        "recommended_next_checks": [
            "用同一套 margin proxy 對照 GDX/GDXJ 或個股的 3/6/12 個月前瞻報酬（事件研究）",
            "檢查是否出現資本開支/併購升溫",
            "監控成本通膨壓力（柴油/工資/試劑）",
        ],
    }

    return result


# =============================================================================
# CLI 入口
# =============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="計算貴金屬礦業毛利率",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("--quick", action="store_true", help="快速計算（使用預設參數）")
    parser.add_argument("--metal", type=str, default="gold", choices=["gold", "silver"], help="目標金屬")
    parser.add_argument("--miners", type=str, help="礦業清單（逗號分隔）")
    parser.add_argument("--start-date", type=str, help="起始日期 (YYYY-MM-DD)")
    parser.add_argument("--end-date", type=str, help="結束日期 (YYYY-MM-DD)")
    parser.add_argument(
        "--frequency",
        type=str,
        default="quarterly",
        choices=["daily", "weekly", "monthly", "quarterly"],
        help="頻率",
    )
    parser.add_argument(
        "--cost-metric",
        type=str,
        default="AISC",
        choices=["AISC", "cash_cost_C1", "all_in_cost"],
        help="成本口徑",
    )
    parser.add_argument(
        "--aggregation",
        type=str,
        default="production_weighted",
        choices=["equal_weight", "production_weighted", "marketcap_weighted"],
        help="聚合方式",
    )
    parser.add_argument("--history-window", type=int, default=20, help="歷史視窗（年）")
    parser.add_argument("--output", type=str, help="輸出檔案路徑")
    parser.add_argument("--generate-signals", action="store_true", help="生成訊號")
    parser.add_argument("--compact", action="store_true", help="精簡輸出")

    args = parser.parse_args()

    # 解析參數
    miners = args.miners.split(",") if args.miners else None

    # 執行計算
    result = calculate_margin_analysis(
        metal=args.metal,
        miners=miners,
        start_date=args.start_date,
        end_date=args.end_date,
        frequency=args.frequency,
        cost_metric=args.cost_metric,
        aggregation=args.aggregation,
        history_window_years=args.history_window,
    )

    # 精簡輸出
    if args.compact and "latest" in result:
        result = {
            "skill": result["skill"],
            "metal": result["parameters"]["metal"],
            "date": result["latest"]["date"],
            "basket_margin": result["latest"]["gross_margin_proxy"],
            "percentile": result["latest"]["history_percentile"],
            "regime": result["latest"]["regime_label"],
            "driver": result.get("decomposition", {}).get("driver", "unknown"),
        }

    # 輸出
    output_str = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_str)
        print(f"Results saved to: {args.output}")
    else:
        print(output_str)


if __name__ == "__main__":
    main()
