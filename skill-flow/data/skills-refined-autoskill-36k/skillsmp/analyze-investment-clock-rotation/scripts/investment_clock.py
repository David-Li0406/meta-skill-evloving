#!/usr/bin/env python3
"""
Investment Clock Analyzer - Main Script
投資時鐘分析主腳本

把「獲利成長 × 財務狀況（金融環境）」映射成「投資時鐘」，
判斷目前落在哪個象限、近期是順時針還是逆時針旋轉、
以及相對於上一輪循環的位置差異。
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from fetch_data import fetch_all_data


# ============================================================================
# 常數定義
# ============================================================================

QUADRANT_NAMES = {
    "Q1_ideal": "理想象限",
    "Q2_mixed": "好壞混合",
    "Q3_recovery": "修復過渡",
    "Q4_worst": "最差象限",
}

QUADRANT_IMPLICATIONS = {
    "Q1_ideal": "偏多風險資產、順風配置",
    "Q2_mixed": "配置波動管理、估值敏感度提高",
    "Q3_recovery": "謹慎配置、避免誤判為全面牛市",
    "Q4_worst": "優先風險控管、降低槓桿與高 beta 曝險",
}

QUADRANT_DESCRIPTIONS = {
    "Q1_ideal": "獲利成長為正，金融環境偏支持，屬於風險資產相對順風的象限；需監控是否開始往金融環境轉緊或獲利轉弱的方向漂移。",
    "Q2_mixed": "獲利成長為正但金融環境不支持，面臨估值壓力與波動風險；配置上需關注估值敏感度。",
    "Q3_recovery": "金融環境支持但獲利尚未回升，通常代表「寬鬆救市」但基本面未回；避免把它誤判成全面牛市。",
    "Q4_worst": "獲利下滑且金融環境不支持，風險資產易受傷；應優先風險控管、降低槓桿。",
}


# ============================================================================
# 數據處理函數
# ============================================================================


def yoy_growth(series: pd.Series, periods: int = 4) -> pd.Series:
    """
    計算同比成長率

    Args:
        series: 原始序列
        periods: 期數（季度=4, 月度=12, 週度=52）

    Returns:
        成長率序列
    """
    return series.pct_change(periods=periods)


def zscore(series: pd.Series, window: int = 52) -> pd.Series:
    """
    計算滾動 Z-score

    Args:
        series: 原始序列
        window: 滾動視窗

    Returns:
        Z-score 序列
    """
    mean = series.rolling(window=window, min_periods=window // 2).mean()
    std = series.rolling(window=window, min_periods=window // 2).std()
    return (series - mean) / std


def align_series(
    earnings: pd.Series,
    fci: pd.Series,
    method: str = "ffill",
) -> pd.DataFrame:
    """
    對齊兩個不同頻率的序列

    Args:
        earnings: 獲利序列（可能是季度）
        fci: 金融環境序列（可能是週度）
        method: 對齊方法（ffill/bfill/interpolate）

    Returns:
        對齊後的 DataFrame
    """
    # 合併
    df = pd.DataFrame({"earnings": earnings, "fci": fci})

    # 前向填充缺失值
    if method == "ffill":
        df = df.ffill()
    elif method == "bfill":
        df = df.bfill()
    elif method == "interpolate":
        df = df.interpolate(method="time")

    return df.dropna()


# ============================================================================
# 座標與象限計算
# ============================================================================


def calculate_quadrant(x: float, y: float) -> str:
    """
    根據 X/Y 值判定象限

    Args:
        x: X 軸值（金融環境，負=支持/寬鬆）
        y: Y 軸值（獲利成長，正=成長）

    Returns:
        象限代碼
    """
    # 注意：X 軸負值代表金融環境支持（寬鬆）
    # 所以 x < 0 時金融環境是 supportive

    if y >= 0 and x <= 0:
        return "Q1_ideal"  # 獲利↑ & 金融支持↑
    elif y >= 0 and x > 0:
        return "Q2_mixed"  # 獲利↑ & 金融不支持↓
    elif y < 0 and x <= 0:
        return "Q3_recovery"  # 獲利↓ & 金融支持↑
    else:
        return "Q4_worst"  # 獲利↓ & 金融不支持↓


def clock_hour_from_angle(theta_rad: float) -> int:
    """
    將角度（弧度）轉換為 12 小時制時鐘點位

    Args:
        theta_rad: 角度（弧度，atan2 結果）

    Returns:
        時鐘點位（1-12）
    """
    # atan2 返回 -π 到 π
    # 轉換為「從 12 點開始順時針」
    # 12 點在正上方（y 最大，x=0），即 θ = π/2

    # 將角度轉換為從正上方（12點）開始的順時針角度
    theta = (np.pi / 2 - theta_rad) % (2 * np.pi)

    # 轉換為小時
    hour = int((theta / (2 * np.pi)) * 12) or 12

    return hour


def angle_from_coordinates(x: float, y: float) -> float:
    """
    從座標計算角度（弧度）

    Args:
        x: X 座標
        y: Y 座標

    Returns:
        角度（弧度）
    """
    return np.arctan2(y, x)


# ============================================================================
# 旋轉分析
# ============================================================================


def analyze_rotation(
    angles: List[float],
) -> Dict[str, Any]:
    """
    分析旋轉方向與幅度

    Args:
        angles: 角度序列（弧度）

    Returns:
        旋轉分析結果
    """
    if len(angles) < 2:
        return {
            "from_hour": None,
            "to_hour": None,
            "direction": None,
            "magnitude_degrees": 0,
            "full_rotations": 0,
        }

    # 計算累積旋轉（處理角度跳躍）
    unwrapped = np.unwrap(angles)
    total_rotation = unwrapped[-1] - unwrapped[0]

    # 轉換為度數
    magnitude_degrees = abs(np.degrees(total_rotation))

    # 判斷方向
    # 順時針在我們的座標系中是負角度變化
    direction = "clockwise" if total_rotation < 0 else "counter_clockwise"

    # 計算完整圈數
    full_rotations = int(magnitude_degrees // 360)

    # 起終點時鐘點位
    from_hour = clock_hour_from_angle(angles[0])
    to_hour = clock_hour_from_angle(angles[-1])

    return {
        "from_hour": from_hour,
        "to_hour": to_hour,
        "direction": direction,
        "magnitude_degrees": round(magnitude_degrees, 1),
        "full_rotations": full_rotations,
        "net_degrees": round(magnitude_degrees % 360, 1),
    }


def get_magnitude_note(degrees: float) -> str:
    """
    根據旋轉幅度生成說明文字

    Args:
        degrees: 旋轉度數

    Returns:
        說明文字
    """
    if degrees < 90:
        return f"微幅漂移（{degrees:.0f}°），趨勢不明確"
    elif degrees < 270:
        return f"中等旋轉（{degrees:.0f}°），屬於典型景氣循環轉換"
    elif degrees < 360:
        return f"大幅旋轉（{degrees:.0f}°），接近完整景氣循環"
    else:
        return f"極端旋轉（{degrees:.0f}°），可能經歷劇烈衝擊與復甦"


# ============================================================================
# 主分析函數
# ============================================================================


def analyze_investment_clock(
    data: Dict[str, pd.Series],
    start_date: str,
    end_date: str,
    earnings_growth_method: str = "yoy",
    earnings_periods: int = 4,
    z_window: int = 52,
    invert_fci: bool = True,
    smoothing_window: Optional[int] = None,
) -> Dict[str, Any]:
    """
    執行投資時鐘分析

    Args:
        data: 包含 earnings 和 fci 序列的字典
        start_date: 分析起始日期
        end_date: 分析結束日期
        earnings_growth_method: 獲利成長計算方法
        earnings_periods: 獲利成長計算期數
        z_window: Z-score 視窗
        invert_fci: 是否反轉 FCI（讓負值=支持性）
        smoothing_window: 平滑視窗（None 表示不平滑）

    Returns:
        分析結果字典
    """
    earnings = data["earnings"].copy()
    fci = data["fci"].copy()

    # 計算獲利成長
    if earnings_growth_method == "yoy":
        earnings_growth = yoy_growth(earnings, periods=earnings_periods)
    else:
        earnings_growth = yoy_growth(earnings, periods=earnings_periods)

    # 計算金融環境 Z-score
    fci_z = zscore(fci, window=z_window)

    # 反轉金融環境（若需要）
    if invert_fci:
        fci_z = -fci_z

    # 對齊序列
    df = align_series(earnings_growth, fci_z)

    # 篩選日期範圍
    df = df.loc[start_date:end_date]

    if df.empty:
        return {"error": "No data in specified date range"}

    # 平滑（可選）
    if smoothing_window:
        df["earnings"] = df["earnings"].rolling(smoothing_window).mean()
        df["fci"] = df["fci"].rolling(smoothing_window).mean()
        df = df.dropna()

    # 計算座標、角度、象限
    x_values = df["fci"].values
    y_values = df["earnings"].values
    dates = df.index

    angles = [angle_from_coordinates(x, y) for x, y in zip(x_values, y_values)]
    hours = [clock_hour_from_angle(a) for a in angles]
    quadrants = [calculate_quadrant(x, y) for x, y in zip(x_values, y_values)]

    # 分析旋轉
    rotation = analyze_rotation(angles)

    # 當前狀態
    current_x = float(x_values[-1])
    current_y = float(y_values[-1])
    current_hour = hours[-1]
    current_quadrant = quadrants[-1]

    # 象限時間分布
    quadrant_counts = pd.Series(quadrants).value_counts()
    total_periods = len(quadrants)
    quadrant_distribution = {
        q: {
            "periods": int(quadrant_counts.get(q, 0)),
            "percentage": round(quadrant_counts.get(q, 0) / total_periods * 100, 1),
        }
        for q in ["Q1_ideal", "Q2_mixed", "Q3_recovery", "Q4_worst"]
    }

    return {
        "skill": "analyze-investment-clock-rotation",
        "version": "0.1.0",
        "as_of": str(dates[-1].date()),
        "market": "US_EQUITY",
        "window": {
            "start_date": str(dates[0].date()),
            "end_date": str(dates[-1].date()),
            "freq": "weekly" if len(df) > 100 else "monthly",
            "total_periods": total_periods,
        },
        "axis_mapping_used": {
            "x": "financial_conditions",
            "y": "earnings_growth",
        },
        "current_state": {
            "clock_hour": current_hour,
            "quadrant": current_quadrant,
            "quadrant_name": QUADRANT_NAMES[current_quadrant],
            "x_value": round(current_x, 4),
            "y_value": round(current_y, 4),
            "interpretation": QUADRANT_DESCRIPTIONS[current_quadrant],
        },
        "rotation_summary": {
            "from_hour": rotation["from_hour"],
            "to_hour": rotation["to_hour"],
            "from_quadrant": quadrants[0],
            "to_quadrant": current_quadrant,
            "direction": rotation["direction"],
            "direction_cn": "順時針" if rotation["direction"] == "clockwise" else "逆時針",
            "magnitude_degrees": rotation["magnitude_degrees"],
            "full_rotations": rotation["full_rotations"],
            "magnitude_note": get_magnitude_note(rotation["magnitude_degrees"]),
        },
        "quadrant_time_distribution": quadrant_distribution,
        "implications": {
            "current_quadrant_implication": QUADRANT_IMPLICATIONS[current_quadrant],
            "rotation_implication": f"{'順時針' if rotation['direction'] == 'clockwise' else '逆時針'}旋轉中",
        },
        "time_series": {
            "dates": [str(d.date()) for d in dates],
            "x": [round(v, 4) for v in x_values],
            "y": [round(v, 4) for v in y_values],
            "hours": hours,
            "quadrants": quadrants,
        },
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "parameters": {
                "earnings_growth_method": earnings_growth_method,
                "z_window": z_window,
                "invert_fci": invert_fci,
                "smoothing_window": smoothing_window,
            },
        },
    }


def get_quick_status(
    data: Dict[str, pd.Series],
    z_window: int = 52,
    invert_fci: bool = True,
) -> Dict[str, Any]:
    """
    快速檢查當前狀態

    Args:
        data: 數據字典
        z_window: Z-score 視窗
        invert_fci: 是否反轉 FCI

    Returns:
        快速狀態
    """
    earnings = data["earnings"]
    fci = data["fci"]

    # 計算獲利成長（假設季度數據）
    earnings_growth = yoy_growth(earnings, periods=4)

    # 計算金融環境 Z-score
    fci_z = zscore(fci, window=z_window)
    if invert_fci:
        fci_z = -fci_z

    # 對齊並取最新值
    df = align_series(earnings_growth, fci_z).dropna()

    if df.empty:
        return {"error": "No data available"}

    latest = df.iloc[-1]
    current_x = float(latest["fci"])
    current_y = float(latest["earnings"])
    angle = angle_from_coordinates(current_x, current_y)
    hour = clock_hour_from_angle(angle)
    quadrant = calculate_quadrant(current_x, current_y)

    return {
        "skill": "analyze-investment-clock-rotation",
        "as_of": str(df.index[-1].date()),
        "current_position": {
            "clock_hour": hour,
            "quadrant": quadrant,
            "quadrant_name": QUADRANT_NAMES[quadrant],
            "earnings_growth": round(current_y, 4),
            "financial_conditions_zscore": round(current_x, 4),
        },
        "interpretation": f"{QUADRANT_NAMES[quadrant]}，{QUADRANT_IMPLICATIONS[quadrant]}",
    }


# ============================================================================
# 主入口
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Investment Clock Analyzer - 投資時鐘分析"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick check: show current position only",
    )
    parser.add_argument(
        "--start",
        type=str,
        default="2022-01-01",
        help="Analysis start date",
    )
    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="Analysis end date",
    )
    parser.add_argument(
        "--earnings",
        type=str,
        default="CP",
        help="FRED series ID for earnings",
    )
    parser.add_argument(
        "--fci",
        type=str,
        default="NFCI",
        help="FRED series ID for financial conditions",
    )
    parser.add_argument(
        "--z-window",
        type=int,
        default=52,
        help="Z-score rolling window",
    )
    parser.add_argument(
        "--no-invert-fci",
        action="store_true",
        help="Do not invert FCI (default: invert so negative = supportive)",
    )
    parser.add_argument(
        "--smoothing",
        type=int,
        default=None,
        help="Smoothing window (optional)",
    )
    parser.add_argument(
        "--compare-cycle",
        type=str,
        nargs=2,
        metavar=("START", "END"),
        default=None,
        help="Compare with previous cycle (START END)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path",
    )

    args = parser.parse_args()

    end_date = args.end or datetime.now().strftime("%Y-%m-%d")
    invert_fci = not args.no_invert_fci

    # 抓取數據（需要較長的歷史以計算 Z-score）
    data_start = "2010-01-01"  # 確保有足夠歷史數據
    print("Fetching data...", file=sys.stderr)
    data = fetch_all_data(
        start_date=data_start,
        end_date=end_date,
        earnings_id=args.earnings,
        fci_id=args.fci,
    )

    if args.quick:
        # 快速模式
        result = get_quick_status(data, z_window=args.z_window, invert_fci=invert_fci)
    else:
        # 完整分析
        print("Analyzing investment clock...", file=sys.stderr)
        result = analyze_investment_clock(
            data=data,
            start_date=args.start,
            end_date=end_date,
            z_window=args.z_window,
            invert_fci=invert_fci,
            smoothing_window=args.smoothing,
        )

        # 循環比較（若有指定）
        if args.compare_cycle:
            prev_start, prev_end = args.compare_cycle
            print(f"Comparing with cycle {prev_start} to {prev_end}...", file=sys.stderr)
            prev_result = analyze_investment_clock(
                data=data,
                start_date=prev_start,
                end_date=prev_end,
                z_window=args.z_window,
                invert_fci=invert_fci,
                smoothing_window=args.smoothing,
            )

            # 加入比較結果
            result["cycle_comparison"] = {
                "enabled": True,
                "previous_cycle": {
                    "period": {
                        "start": prev_start,
                        "end": prev_end,
                    },
                    "rotation_magnitude": prev_result["rotation_summary"]["magnitude_degrees"],
                    "direction": prev_result["rotation_summary"]["direction"],
                    "from_hour": prev_result["rotation_summary"]["from_hour"],
                    "to_hour": prev_result["rotation_summary"]["to_hour"],
                },
                "comparison": {
                    "rotation_ratio": round(
                        result["rotation_summary"]["magnitude_degrees"]
                        / max(prev_result["rotation_summary"]["magnitude_degrees"], 1),
                        2,
                    ),
                    "similar_direction": (
                        result["rotation_summary"]["direction"]
                        == prev_result["rotation_summary"]["direction"]
                    ),
                },
            }

    # 輸出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        print(f"Result saved to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
