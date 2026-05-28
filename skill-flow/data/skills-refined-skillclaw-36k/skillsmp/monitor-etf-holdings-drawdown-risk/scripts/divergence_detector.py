#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
divergence_detector.py - ETF 持倉-價格背離偵測器

偵測「商品價格上漲、但對應實物 ETF/信託持倉卻下滑」的背離現象。
計算壓力分數，提供雙重假設解釋。
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

import pandas as pd
import numpy as np

from fetch_prices import fetch_price_series
from fetch_etf_holdings import fetch_etf_inventory_series, ETF_CONFIG


def detect_divergence(
    etf_ticker: str,
    commodity_symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    decade_low_window_days: int = 3650,
    divergence_window_days: int = 180,
    min_price_return_pct: float = 0.15,
    min_inventory_drawdown_pct: float = 0.10
) -> Dict[str, Any]:
    """
    偵測 ETF 持倉與商品價格的背離

    Parameters
    ----------
    etf_ticker : str
        ETF 代碼（如 SLV）
    commodity_symbol : str
        商品價格代碼（如 XAGUSD=X）
    start_date : str, optional
        起始日期
    end_date : str, optional
        結束日期
    decade_low_window_days : int
        十年低點視窗（天）
    divergence_window_days : int
        背離計算視窗（天）
    min_price_return_pct : float
        價格上漲門檻
    min_inventory_drawdown_pct : float
        庫存下滑門檻

    Returns
    -------
    dict
        背離分析結果
    """
    # 1. 抓取數據
    print(f"抓取 {commodity_symbol} 價格數據...")
    price = fetch_price_series(commodity_symbol, start_date, end_date)

    print(f"抓取 {etf_ticker} 持倉數據...")
    inventory = fetch_etf_inventory_series(etf_ticker, start_date, end_date)

    # 2. 對齊與清洗
    df = pd.concat({"price": price, "inv": inventory}, axis=1).sort_index()
    df["inv"] = df["inv"].ffill()  # 庫存前向填充
    df = df.dropna(subset=["price", "inv"])

    if len(df) < divergence_window_days:
        raise ValueError(f"數據不足：需要至少 {divergence_window_days} 天，實際只有 {len(df)} 天")

    # 3. 計算特徵
    w = divergence_window_days

    # 視窗期變化率
    df["price_ret"] = df["price"].pct_change(w)
    df["inv_chg"] = df["inv"].pct_change(w)

    # 十年低點判定
    df["inv_decade_min"] = df["inv"].rolling(decade_low_window_days, min_periods=252).min()
    df["decade_low_flag"] = df["inv"] <= df["inv_decade_min"] * 1.001  # epsilon

    # 庫存/價格比值
    df["ratio"] = df["inv"] / df["price"]
    ratio_mean = df["ratio"].rolling(decade_low_window_days, min_periods=252).mean()
    ratio_std = df["ratio"].rolling(decade_low_window_days, min_periods=252).std()
    df["ratio_z"] = (df["ratio"] - ratio_mean) / ratio_std

    # 4. 背離判定
    df["divergence"] = (
        (df["price_ret"] >= min_price_return_pct) &
        (df["inv_chg"] <= -min_inventory_drawdown_pct)
    )

    # 5. 計算壓力分數
    latest = df.iloc[-1]

    # 背離嚴重度 = 價格漲幅 × 庫存跌幅
    divergence_severity = max(0, latest["price_ret"]) * max(0, -latest["inv_chg"])

    # 十年低點加成
    decade_low_bonus = 1.0 if latest["decade_low_flag"] else 0.0

    # 比值極端加成
    ratio_extreme_bonus = 1.0 if latest["ratio_z"] < -2 else 0.0

    # 壓力分數
    stress_score = 100 * min(1.0,
        0.6 * divergence_severity +
        0.2 * decade_low_bonus +
        0.2 * ratio_extreme_bonus
    )

    # 壓力等級
    if stress_score >= 80:
        stress_level = "CRITICAL"
    elif stress_score >= 60:
        stress_level = "HIGH"
    elif stress_score >= 30:
        stress_level = "MEDIUM"
    else:
        stress_level = "LOW"

    # 6. 產生結果
    result = {
        "skill": "monitor-etf-holdings-drawdown-risk",
        "version": "0.1.0",
        "asof": str(df.index[-1].date()),

        "inputs": {
            "etf_ticker": etf_ticker,
            "commodity_price_symbol": commodity_symbol,
            "divergence_window_days": divergence_window_days,
            "decade_low_window_days": decade_low_window_days,
            "min_price_return_pct": min_price_return_pct,
            "min_inventory_drawdown_pct": min_inventory_drawdown_pct
        },

        "result": {
            "divergence": bool(latest["divergence"]),
            "price_return_window": float(latest["price_ret"]) if not np.isnan(latest["price_ret"]) else None,
            "inventory_change_window": float(latest["inv_chg"]) if not np.isnan(latest["inv_chg"]) else None,
            "inventory_decade_low": bool(latest["decade_low_flag"]),
            "inventory_to_price_ratio_z": float(latest["ratio_z"]) if not np.isnan(latest["ratio_z"]) else None,
            "stress_score_0_100": float(stress_score),
            "stress_level": stress_level
        },

        "latest_values": {
            "price": float(latest["price"]),
            "price_date": str(df.index[-1].date()),
            "inventory_oz": float(latest["inv"]),
            "inventory_tonnes": float(latest["inv"]) * 31.1035 / 1000000,
            "inventory_date": str(df.index[-1].date()),
            "ratio": float(latest["ratio"])
        },

        "historical_context": {
            "inventory_decade_min": float(df["inv"].min()),
            "inventory_decade_max": float(df["inv"].max()),
            "inventory_percentile": float((latest["inv"] - df["inv"].min()) / (df["inv"].max() - df["inv"].min()) * 100) if df["inv"].max() != df["inv"].min() else 50.0,
            "ratio_mean": float(ratio_mean.iloc[-1]) if not np.isnan(ratio_mean.iloc[-1]) else None,
            "ratio_std": float(ratio_std.iloc[-1]) if not np.isnan(ratio_std.iloc[-1]) else None
        },

        "interpretations": [
            {
                "name": "Physical Tightness Hypothesis",
                "when_supported": "若交易所/金庫庫存同步下降、期貨 backwardation 變強、lease rates 上升、零售溢價擴大",
                "note": "這才比較接近社群敘事所說的「實物吃緊/被抽走」。"
            },
            {
                "name": "ETF Flow / Redemption Hypothesis",
                "when_supported": "若其他實物緊張指標不跟，較可能是投資人資金外流或贖回機制所致",
                "note": "ETF 持倉下降不必然等同「銀行搶銀條」。"
            }
        ],

        "cross_validation": {
            "performed": False,
            "signals_checked": [],
            "physical_tightness_score": None,
            "etf_flow_score": None,
            "dominant_hypothesis": None
        },

        "next_checks": [
            f"核對 {etf_ticker} 官方持倉時間序列是否真為 10 年低點（避免圖表來源/口徑問題）",
            "交叉比對 COMEX registered/eligible 是否同步下降",
            "檢查期貨曲線是否 backwardation 加劇",
            "觀察零售銀條/銀幣 premium 是否擴大"
        ],

        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "data_points": len(df),
            "data_freshness": {
                "price_data": str(df.index[-1].date()),
                "inventory_data": str(df.index[-1].date())
            }
        }
    }

    return result


def quick_check(
    etf_ticker: str,
    commodity_symbol: str
) -> Dict[str, Any]:
    """
    快速檢查背離狀態（精簡輸出）
    """
    result = detect_divergence(
        etf_ticker=etf_ticker,
        commodity_symbol=commodity_symbol
    )

    # 精簡輸出
    quick_result = {
        "skill": "monitor-etf-holdings-drawdown-risk",
        "asof": result["asof"],
        "etf_ticker": etf_ticker,
        "result": {
            "divergence": result["result"]["divergence"],
            "price_return_window": result["result"]["price_return_window"],
            "inventory_change_window": result["result"]["inventory_change_window"],
            "inventory_decade_low": result["result"]["inventory_decade_low"],
            "stress_score_0_100": result["result"]["stress_score_0_100"]
        },
        "next_checks": result["next_checks"][:2]  # 只顯示前兩個
    }

    return quick_result


# 商品代碼對照表
# 註：XAGUSD=X 已失效，改用 SI=F（白銀期貨）
COMMODITY_MAPPING = {
    "SLV": "SI=F",      # 白銀期貨（XAGUSD=X 已失效）
    "PSLV": "SI=F",     # 白銀期貨
    "GLD": "GC=F",      # 黃金期貨
    "PHYS": "GC=F",     # 黃金期貨
    "IAU": "GC=F",      # 黃金期貨
    "SIVR": "SI=F"      # 白銀期貨
}


def main():
    parser = argparse.ArgumentParser(
        description="ETF 持倉-價格背離偵測器"
    )
    parser.add_argument(
        "--etf", "-e",
        required=True,
        help=f"ETF 代碼，支援: {list(ETF_CONFIG.keys())}"
    )
    parser.add_argument(
        "--commodity", "-c",
        help="商品價格代碼（如 XAGUSD=X），不指定則自動配對"
    )
    parser.add_argument(
        "--start",
        help="起始日期 (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end",
        help="結束日期 (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--divergence-window",
        type=int,
        default=180,
        help="背離計算視窗（天），預設 180"
    )
    parser.add_argument(
        "--decade-window",
        type=int,
        default=3650,
        help="十年低點視窗（天），預設 3650"
    )
    parser.add_argument(
        "--price-threshold",
        type=float,
        default=0.15,
        help="價格上漲門檻，預設 0.15 (15%%)"
    )
    parser.add_argument(
        "--inventory-threshold",
        type=float,
        default=0.10,
        help="庫存下滑門檻，預設 0.10 (10%%)"
    )
    parser.add_argument(
        "--output", "-o",
        help="輸出檔案路徑（JSON）"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="快速檢查模式（精簡輸出）"
    )

    args = parser.parse_args()

    # 自動配對商品代碼
    commodity = args.commodity
    if not commodity:
        commodity = COMMODITY_MAPPING.get(args.etf)
        if not commodity:
            print(f"錯誤：未指定商品代碼，且無法自動配對 {args.etf}")
            print(f"請使用 --commodity 參數指定")
            return

    # 執行偵測
    if args.quick:
        result = quick_check(
            etf_ticker=args.etf,
            commodity_symbol=commodity
        )
    else:
        result = detect_divergence(
            etf_ticker=args.etf,
            commodity_symbol=commodity,
            start_date=args.start,
            end_date=args.end,
            decade_low_window_days=args.decade_window,
            divergence_window_days=args.divergence_window,
            min_price_return_pct=args.price_threshold,
            min_inventory_drawdown_pct=args.inventory_threshold
        )

    # 輸出
    output_json = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"已輸出至 {args.output}")
    else:
        print(output_json)

    # 簡要摘要
    print("\n" + "=" * 50)
    print(f"ETF: {args.etf}")
    print(f"背離: {'是' if result['result']['divergence'] else '否'}")
    print(f"壓力分數: {result['result']['stress_score_0_100']:.1f}/100")
    if 'stress_level' in result['result']:
        print(f"壓力等級: {result['result']['stress_level']}")
    print("=" * 50)


if __name__ == "__main__":
    main()
