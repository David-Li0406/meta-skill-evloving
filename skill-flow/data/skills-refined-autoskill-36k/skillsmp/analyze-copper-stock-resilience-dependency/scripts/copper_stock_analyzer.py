#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
銅價股市韌性依賴分析器

分析銅價與股市韌性的依賴關係、關卡狀態與回補機率。
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import numpy as np
import pandas as pd

# 添加腳本目錄到路徑
sys.path.insert(0, str(Path(__file__).parent))
from fetch_data import fetch_copper, fetch_equity, fetch_china_10y_yield, align_monthly


# 預設參數
DEFAULT_MA_WINDOW = 60
DEFAULT_ROLLING_WINDOW = 24
DEFAULT_ROUND_LEVELS = [10000, 13000]
DEFAULT_BACKFILL_MAX_DRAWDOWN = 0.25
DEFAULT_LEVEL_THRESHOLD = 0.05
DEFAULT_RESILIENCE_WEIGHTS = {
    "momentum": 0.4,
    "sma": 0.4,
    "drawdown": 0.2
}


def calculate_trend_state(
    prices: pd.Series,
    ma_window: int = DEFAULT_MA_WINDOW
) -> pd.DataFrame:
    """
    計算趨勢狀態

    Parameters
    ----------
    prices : pd.Series
        價格序列
    ma_window : int
        移動平均視窗

    Returns
    -------
    pd.DataFrame
        包含 sma, sma_slope, trend 的 DataFrame
    """
    df = pd.DataFrame({"price": prices})

    # 計算 SMA
    df["sma"] = df["price"].rolling(ma_window, min_periods=1).mean()

    # 計算斜率
    df["sma_slope"] = df["sma"].diff()

    # 定義趨勢
    conditions = [
        (df["price"] > df["sma"]) & (df["sma_slope"] > 0),
        (df["price"] < df["sma"]) & (df["sma_slope"] < 0)
    ]
    choices = ["up", "down"]
    df["trend"] = np.select(conditions, choices, default="range")

    return df


def detect_round_levels(
    price: float,
    levels: List[float],
    threshold: float = DEFAULT_LEVEL_THRESHOLD
) -> Dict[str, List[float]]:
    """
    判斷價格接近哪些關卡

    Parameters
    ----------
    price : float
        當前價格
    levels : list
        關卡列表
    threshold : float
        容忍範圍

    Returns
    -------
    dict
        {"near_resistance": [...], "near_support": [...]}
    """
    near_resistance = []
    near_support = []

    for level in levels:
        distance = abs(price - level) / level
        if distance < threshold:
            if price < level:
                near_resistance.append(level)
            else:
                near_support.append(level)

    return {
        "near_resistance": sorted(near_resistance),
        "near_support": sorted(near_support, reverse=True)
    }


def calculate_equity_resilience_score(
    equity: pd.Series,
    weights: Dict[str, float] = DEFAULT_RESILIENCE_WEIGHTS,
    sma_period: int = 12,
    drawdown_period: int = 3
) -> pd.Series:
    """
    計算股市韌性評分

    Parameters
    ----------
    equity : pd.Series
        股市價格序列
    weights : dict
        權重設定
    sma_period : int
        均線期數
    drawdown_period : int
        回撤計算期數

    Returns
    -------
    pd.Series
        韌性評分（0-100）
    """
    df = pd.DataFrame({"equity": equity})

    # 12 個月動能
    df["return_12m"] = df["equity"].pct_change(12)

    # 分位數排名（轉為 0-100）
    df["momentum_score"] = df["return_12m"].rank(pct=True) * 100

    # 是否站上均線
    df["sma"] = df["equity"].rolling(sma_period, min_periods=1).mean()
    df["above_sma"] = (df["equity"] > df["sma"]).astype(int) * 100

    # 近期回撤
    df["rolling_max"] = df["equity"].rolling(drawdown_period, min_periods=1).max()
    df["drawdown"] = (df["rolling_max"] - df["equity"]) / df["rolling_max"]
    # 回撤越小越好，用 15% 作為標準化基準
    df["drawdown_score"] = (1 - np.clip(df["drawdown"] / 0.15, 0, 1)) * 100

    # 加權計算
    df["resilience_score"] = (
        weights["momentum"] * df["momentum_score"] +
        weights["sma"] * df["above_sma"] +
        weights["drawdown"] * df["drawdown_score"]
    )

    return df["resilience_score"]


def calculate_rolling_betas(
    copper: pd.Series,
    equity: pd.Series,
    yield_series: pd.Series,
    window: int = DEFAULT_ROLLING_WINDOW
) -> pd.DataFrame:
    """
    計算滾動迴歸貝塔係數

    Parameters
    ----------
    copper : pd.Series
        銅價序列
    equity : pd.Series
        股市序列
    yield_series : pd.Series
        殖利率序列
    window : int
        滾動視窗

    Returns
    -------
    pd.DataFrame
        包含 beta_equity, beta_yield, r_squared 的 DataFrame
    """
    # 計算報酬率/變化
    ret = pd.DataFrame({
        "dcopper": copper.pct_change(),
        "dequity": equity.pct_change(),
        "dyield": yield_series.diff()
    }).dropna()

    # 滾動迴歸
    betas = []
    for i in range(window, len(ret) + 1):
        window_data = ret.iloc[i - window:i]

        # 簡單 OLS
        y = window_data["dcopper"].values
        X = np.column_stack([
            np.ones(len(y)),
            window_data["dequity"].values,
            window_data["dyield"].values
        ])

        try:
            coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
            y_pred = X @ coeffs
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - y.mean()) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

            betas.append({
                "date": ret.index[i - 1],
                "beta_equity": coeffs[1],
                "beta_yield": coeffs[2],
                "r_squared": r_squared
            })
        except Exception:
            betas.append({
                "date": ret.index[i - 1],
                "beta_equity": np.nan,
                "beta_yield": np.nan,
                "r_squared": np.nan
            })

    result = pd.DataFrame(betas).set_index("date")
    return result


def detect_backfill_events(
    df: pd.DataFrame,
    level_hi: float = 13000,
    level_lo: float = 10000,
    lookforward: int = 12,
    resilience_col: str = "resilience_score"
) -> pd.DataFrame:
    """
    偵測回補事件

    Parameters
    ----------
    df : pd.DataFrame
        包含銅價和韌性評分的 DataFrame
    level_hi : float
        高關卡
    level_lo : float
        低關卡
    lookforward : int
        觀察期（月）
    resilience_col : str
        韌性評分欄位名

    Returns
    -------
    pd.DataFrame
        回補事件記錄
    """
    events = []
    touched_indices = set()

    for i, (idx, row) in enumerate(df.iterrows()):
        if idx in touched_indices:
            continue

        if row["copper"] >= level_hi * 0.98:
            # 標記為已處理（避免連續觸及重複計算）
            for j in range(i, min(i + 3, len(df))):
                touched_indices.add(df.index[j])

            # 觀察未來期間
            future_start = i + 1
            future_end = min(i + 1 + lookforward, len(df))
            future = df.iloc[future_start:future_end]

            if len(future) > 0:
                trough_price = future["copper"].min()
                backfill = trough_price <= level_lo * 1.02

                events.append({
                    "touch_date": idx,
                    "touch_price": row["copper"],
                    "trough_price": trough_price,
                    "backfill": backfill,
                    "equity_resilience_at_touch": row.get(resilience_col, np.nan)
                })

    return pd.DataFrame(events)


def calculate_backfill_probabilities(
    events_df: pd.DataFrame,
    high_threshold: float = 70,
    low_threshold: float = 30
) -> Dict[str, float]:
    """
    計算回補機率

    Parameters
    ----------
    events_df : pd.DataFrame
        回補事件 DataFrame
    high_threshold : float
        高韌性門檻
    low_threshold : float
        低韌性門檻

    Returns
    -------
    dict
        回補機率統計
    """
    if len(events_df) == 0:
        return {
            "overall": None,
            "equity_resilience_high": None,
            "equity_resilience_low": None
        }

    overall = events_df["backfill"].mean()

    high_resilience = events_df[events_df["equity_resilience_at_touch"] >= high_threshold]
    low_resilience = events_df[events_df["equity_resilience_at_touch"] <= low_threshold]

    return {
        "overall": round(overall, 3) if not np.isnan(overall) else None,
        "equity_resilience_high": round(high_resilience["backfill"].mean(), 3) if len(high_resilience) > 0 else None,
        "equity_resilience_low": round(low_resilience["backfill"].mean(), 3) if len(low_resilience) > 0 else None
    }


def generate_diagnosis(
    latest: Dict[str, Any],
    backfill_probs: Dict[str, float],
    beta_percentiles: Dict[str, float]
) -> Dict[str, str]:
    """
    生成情境判讀

    Parameters
    ----------
    latest : dict
        最新狀態
    backfill_probs : dict
        回補機率
    beta_percentiles : dict
        貝塔分位數

    Returns
    -------
    dict
        診斷結果
    """
    diagnosis = {}

    # 趨勢狀態
    trend = latest.get("copper_trend", "range")
    if trend == "up":
        diagnosis["trend_status"] = "上升趨勢中，銅價高於長期均線且均線斜率為正"
    elif trend == "down":
        diagnosis["trend_status"] = "下降趨勢中，銅價低於長期均線且均線斜率為負"
    else:
        diagnosis["trend_status"] = "區間整理中，趨勢不明確"

    # 關卡狀態
    near_res = latest.get("near_resistance_levels", [])
    near_sup = latest.get("near_support_levels", [])
    if near_res:
        diagnosis["level_status"] = f"接近 {near_res[0]:,.0f} 關卡，為重要阻力位"
    elif near_sup:
        diagnosis["level_status"] = f"接近 {near_sup[0]:,.0f} 關卡，為重要支撐位"
    else:
        diagnosis["level_status"] = "距離關卡較遠，處於中間區域"

    # 韌性狀態
    resilience = latest.get("equity_resilience_score", 50)
    if resilience >= 70:
        diagnosis["resilience_status"] = f"股市韌性評分 {resilience:.0f}，處於高韌性區間"
    elif resilience <= 30:
        diagnosis["resilience_status"] = f"股市韌性評分 {resilience:.0f}，處於低韌性區間"
    else:
        diagnosis["resilience_status"] = f"股市韌性評分 {resilience:.0f}，處於中性區間"

    # 依賴狀態
    beta_pct = beta_percentiles.get("beta_equity_percentile", 50)
    beta_equity = latest.get("rolling_beta_equity_24m", 0) or 0

    if beta_equity < 0:
        diagnosis["dependency_status"] = f"滾動 β 為負值 ({beta_equity:.2f})，銅與股市呈反向關係，脫離傳統風險資產模式"
    elif beta_pct >= 75:
        diagnosis["dependency_status"] = "滾動 β 位於歷史高分位，銅正被當作風險資產交易"
    elif beta_pct <= 25:
        diagnosis["dependency_status"] = "滾動 β 位於歷史低分位，銅有自身獨立邏輯"
    else:
        diagnosis["dependency_status"] = "滾動 β 處於中性水平，依賴度一般"

    # 綜合敘述
    parts = []
    parts.append(f"銅價{diagnosis['trend_status'].split('，')[0]}")
    if near_res:
        parts.append(f"接近 {near_res[0]:,.0f} 關卡")
    parts.append(f"股市韌性{'高檔' if resilience >= 70 else '低檔' if resilience <= 30 else '中性'}")

    if trend == "up" and near_res and resilience >= 70:
        scenario = "續航機率較高"
        backfill_ref = backfill_probs.get("equity_resilience_high")
        parts.append(f"歷史高韌性情境回補率約 {backfill_ref*100:.0f}%" if backfill_ref else "")
    elif trend == "up" and near_res and resilience < 50:
        scenario = "回補風險上升"
        backfill_ref = backfill_probs.get("equity_resilience_low")
        parts.append(f"歷史低韌性情境回補率約 {backfill_ref*100:.0f}%" if backfill_ref else "")
    else:
        scenario = "需持續觀察"

    diagnosis["narrative"] = "，".join([p for p in parts if p]) + "。"
    diagnosis["scenario"] = scenario

    return diagnosis


def generate_flags(latest: Dict[str, Any], beta_percentiles: Dict[str, float]) -> List[Dict[str, str]]:
    """
    生成警報旗標

    Parameters
    ----------
    latest : dict
        最新狀態
    beta_percentiles : dict
        貝塔分位數

    Returns
    -------
    list
        警報旗標列表
    """
    flags = []

    # 關卡旗標
    if latest.get("near_resistance_levels"):
        flags.append({
            "flag": "APPROACHING_RESISTANCE",
            "level": "active",
            "condition": f"copper within 5% of {latest['near_resistance_levels'][0]}",
            "meaning": "接近重要阻力位，關注能否突破"
        })

    if latest.get("near_support_levels"):
        flags.append({
            "flag": "APPROACHING_SUPPORT",
            "level": "active",
            "condition": f"copper within 5% of {latest['near_support_levels'][0]}",
            "meaning": "接近重要支撐位，關注是否跌破"
        })

    # 韌性旗標
    resilience = latest.get("equity_resilience_score", 50)
    if resilience >= 70:
        flags.append({
            "flag": "HIGH_RESILIENCE",
            "level": "active",
            "condition": "equity_resilience_score >= 70",
            "meaning": "股市韌性高，支持風險資產"
        })
    elif resilience <= 30:
        flags.append({
            "flag": "LOW_RESILIENCE",
            "level": "active",
            "condition": "equity_resilience_score <= 30",
            "meaning": "股市韌性低，回補風險上升"
        })

    # 依賴旗標
    beta_pct = beta_percentiles.get("beta_equity_percentile", 50)
    beta_equity = latest.get("rolling_beta_equity_24m", 0) or 0

    if beta_equity < 0:
        flags.append({
            "flag": "NEGATIVE_BETA_REGIME",
            "level": "active",
            "condition": f"beta_equity = {beta_equity:.2f} < 0",
            "meaning": "銅與股市呈反向關係，脫離傳統風險資產模式，可能受避險/供給因素驅動"
        })

    if beta_pct is not None and beta_pct <= 10:
        flags.append({
            "flag": "LOW_BETA_ANOMALY",
            "level": "warning",
            "condition": f"beta_equity at {beta_pct}th percentile (historical extreme)",
            "meaning": "β 處於歷史極端低位，銅正展現獨立於股市的上漲邏輯"
        })

    if beta_pct is not None and beta_pct >= 75:
        flags.append({
            "flag": "HIGH_BETA_REGIME",
            "level": "active",
            "condition": "beta_equity >= 75th percentile",
            "meaning": "銅與股市高度連動，注意股市風險"
        })

    # 警戒旗標
    if resilience < 50 and latest.get("near_resistance_levels"):
        flags.append({
            "flag": "WATCH_EQUITY_RESILIENCE",
            "level": "warning",
            "condition": "equity_resilience_score < 50 AND near resistance",
            "meaning": "回補風險顯著上升，需警惕回踩"
        })

    return flags


def analyze(
    start_date: str,
    end_date: str,
    copper_series: str = "HG=F",
    equity_series: str = "ACWI",
    ma_window: int = DEFAULT_MA_WINDOW,
    rolling_window: int = DEFAULT_ROLLING_WINDOW,
    round_levels: List[float] = DEFAULT_ROUND_LEVELS,
    quick: bool = False
) -> Dict[str, Any]:
    """
    執行完整分析

    Parameters
    ----------
    start_date : str
        起始日期
    end_date : str
        結束日期
    copper_series : str
        銅價序列
    equity_series : str
        股市序列
    ma_window : int
        MA 視窗
    rolling_window : int
        滾動視窗
    round_levels : list
        關卡列表
    quick : bool
        是否快速模式

    Returns
    -------
    dict
        分析結果
    """
    # 1. 抓取數據
    print("Step 1: 抓取數據...")
    copper = fetch_copper(copper_series, start_date, end_date)
    equity = fetch_equity(equity_series, start_date, end_date)
    cny10y = fetch_china_10y_yield(start_date, end_date)

    # 2. 對齊數據
    print("Step 2: 對齊數據...")
    df = align_monthly({
        "copper": copper,
        "equity": equity,
        "cny10y": cny10y
    })
    print(f"  共 {len(df)} 筆資料")

    # 3. 計算趨勢
    print("Step 3: 計算趨勢狀態...")
    trend_df = calculate_trend_state(df["copper"], ma_window)
    df = df.join(trend_df[["sma", "sma_slope", "trend"]])

    # 4. 計算股市韌性
    print("Step 4: 計算股市韌性評分...")
    df["resilience_score"] = calculate_equity_resilience_score(df["equity"])

    # 5. 計算滾動貝塔
    print("Step 5: 計算滾動貝塔...")
    betas = calculate_rolling_betas(df["copper"], df["equity"], df["cny10y"], rolling_window)
    df = df.join(betas)

    # 6. 偵測回補事件
    print("Step 6: 偵測回補事件...")
    events_df = detect_backfill_events(df, level_hi=max(round_levels), level_lo=min(round_levels))
    backfill_probs = calculate_backfill_probabilities(events_df)

    # 7. 計算最新狀態
    print("Step 7: 生成報告...")
    latest_row = df.iloc[-1]
    level_status = detect_round_levels(latest_row["copper"], round_levels)

    # 計算貝塔分位數
    beta_percentiles = {
        "beta_equity_percentile": int(df["beta_equity"].rank(pct=True).iloc[-1] * 100) if not pd.isna(latest_row.get("beta_equity")) else None,
        "beta_yield_percentile": int(df["beta_yield"].rank(pct=True).iloc[-1] * 100) if not pd.isna(latest_row.get("beta_yield")) else None,
    }

    latest_state = {
        "date": latest_row.name.strftime("%Y-%m-%d"),
        "copper_price_usd_per_ton": round(latest_row["copper"], 2),
        "copper_sma_60": round(latest_row["sma"], 2) if not pd.isna(latest_row["sma"]) else None,
        "copper_sma_slope": round(latest_row["sma_slope"], 2) if not pd.isna(latest_row["sma_slope"]) else None,
        "copper_trend": latest_row["trend"],
        "near_resistance_levels": level_status["near_resistance"],
        "near_support_levels": level_status["near_support"],
        "equity_resilience_score": round(latest_row["resilience_score"], 1) if not pd.isna(latest_row["resilience_score"]) else None,
        "rolling_beta_equity_24m": round(latest_row["beta_equity"], 3) if not pd.isna(latest_row.get("beta_equity")) else None,
        "rolling_beta_yield_24m": round(latest_row["beta_yield"], 3) if not pd.isna(latest_row.get("beta_yield")) else None,
    }

    # 生成診斷
    diagnosis = generate_diagnosis(latest_state, backfill_probs, beta_percentiles)

    # 生成旗標
    flags = generate_flags(latest_state, beta_percentiles)

    # 構建輸出
    result = {
        "skill": "analyze-copper-stock-resilience-dependency",
        "version": "0.1.0",
        "as_of": end_date,
        "quick_check": quick,
        "inputs": {
            "start_date": start_date,
            "end_date": end_date,
            "copper_series": f"{copper_series} (converted to USD/ton)",
            "equity_proxy_series": equity_series,
            "ma_window": ma_window,
            "rolling_window": rolling_window,
            "round_levels": round_levels
        },
        "latest_state": latest_state,
        "diagnosis": diagnosis,
        "actionable_flags": flags
    }

    # 完整模式添加更多資訊
    if not quick:
        result["backfill_analysis"] = {
            "events_detected": len(events_df),
            "backfill_events": int(events_df["backfill"].sum()) if len(events_df) > 0 else 0,
            "backfill_probability_12m": backfill_probs
        }
        result["historical_betas"] = {
            "beta_equity_percentile": beta_percentiles["beta_equity_percentile"],
            "beta_equity_mean": round(df["beta_equity"].mean(), 3) if not df["beta_equity"].isna().all() else None,
            "beta_equity_std": round(df["beta_equity"].std(), 3) if not df["beta_equity"].isna().all() else None,
        }
        result["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "data_points": len(df)
        }

    return result


def main():
    parser = argparse.ArgumentParser(
        description="銅價股市韌性依賴分析器"
    )
    parser.add_argument("--start", type=str, help="起始日期 (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, help="結束日期 (YYYY-MM-DD)")
    parser.add_argument("--copper", type=str, default="HG=F", help="銅價序列")
    parser.add_argument("--equity", type=str, default="ACWI", help="股市序列")
    parser.add_argument("--ma-window", type=int, default=DEFAULT_MA_WINDOW, help="MA 視窗")
    parser.add_argument("--rolling-window", type=int, default=DEFAULT_ROLLING_WINDOW, help="滾動視窗")
    parser.add_argument("--levels", type=str, default="10000,13000", help="關卡位置（逗號分隔）")
    parser.add_argument("--output", type=str, help="輸出檔案路徑")
    parser.add_argument("--quick", action="store_true", help="快速模式")

    args = parser.parse_args()

    # 處理日期
    if args.quick:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=365 * 3)).strftime("%Y-%m-%d")
    else:
        start_date = args.start or "2020-01-01"
        end_date = args.end or datetime.now().strftime("%Y-%m-%d")

    # 處理關卡
    round_levels = [float(x.strip()) for x in args.levels.split(",")]

    # 執行分析
    result = analyze(
        start_date=start_date,
        end_date=end_date,
        copper_series=args.copper,
        equity_series=args.equity,
        ma_window=args.ma_window,
        rolling_window=args.rolling_window,
        round_levels=round_levels,
        quick=args.quick
    )

    # 輸出
    output_json = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output_json)
        print(f"\n結果已儲存至: {output_path}")
    else:
        print("\n" + "=" * 60)
        print(output_json)


if __name__ == "__main__":
    main()
