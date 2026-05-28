#!/usr/bin/env python3
"""
Japan Debt Service Tax Burden Analyzer

量化日本「利息吃掉稅收」敘事，提供現況核對、壓力測試與風險分級。

Usage:
    python japan_debt_analyzer.py --quick           # 快速檢查
    python japan_debt_analyzer.py --full            # 完整分析
    python japan_debt_analyzer.py --stress 200      # 壓測 +200bp
    python japan_debt_analyzer.py --quick --refresh # 強制刷新數據
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

import numpy as np
import pandas as pd

# 嘗試導入數據管理器
try:
    from data_manager import JapanDebtDataManager
    HAS_DATA_MANAGER = True
except ImportError:
    try:
        # 嘗試相對導入
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from data_manager import JapanDebtDataManager
        HAS_DATA_MANAGER = True
    except ImportError:
        HAS_DATA_MANAGER = False


# ============================================================================
# 常數與預設值
# ============================================================================

DEFAULT_YIELD_TENORS = ["2Y", "10Y", "30Y"]
DEFAULT_ANALYSIS_WINDOW = 504  # 約 2 年交易日
DEFAULT_PASS_THROUGH = 0.15  # 年度再定價比例

# 風險分級閾值
RISK_BANDS = {
    "green": (0.0, 0.25),
    "yellow": (0.25, 0.40),
    "orange": (0.40, 0.55),
    "red": (0.55, float("inf")),
}

# 預設壓力測試情境
DEFAULT_SCENARIOS = [
    {
        "name": "+100bp baseline",
        "delta_yield_bp": 100,
        "pass_through_year1": 0.15,
        "pass_through_year2": 0.15,
        "tax_shock": 0.0,
    },
    {
        "name": "+200bp baseline",
        "delta_yield_bp": 200,
        "pass_through_year1": 0.15,
        "pass_through_year2": 0.15,
        "tax_shock": 0.0,
    },
    {
        "name": "+200bp + recession (-5% tax)",
        "delta_yield_bp": 200,
        "pass_through_year1": 0.15,
        "pass_through_year2": 0.15,
        "tax_shock": -0.05,
    },
    {
        "name": "+300bp severe stress",
        "delta_yield_bp": 300,
        "pass_through_year1": 0.15,
        "pass_through_year2": 0.15,
        "tax_shock": -0.10,
    },
]

# Fallback 靜態數據（當所有數據源都失敗時使用）
SAMPLE_DATA = {
    "jgb_10y": {
        "latest": 1.23,
        "history": [0.8, 0.9, 1.0, 1.1, 1.15, 1.2, 1.23],  # 簡化示例
    },
    "fiscal": {
        "tax_revenue_jpy": 72_000_000_000_000,  # 72 兆日圓
        "interest_payments_jpy": 24_000_000_000_000,  # 24 兆日圓
        "debt_stock_jpy": 1_200_000_000_000_000,  # 1200 兆日圓
        "fiscal_year": "FY2024",
        "tax_revenue_series": "general_account_tax",
        "interest_payment_series": "interest_only",
    },
    "us_assets": {
        "total_usd": 3_000_000_000_000,  # 約 3 兆美元
        "ust_holdings_usd": 1_100_000_000_000,  # 約 1.1 兆美元
    },
}


# ============================================================================
# 統計函數
# ============================================================================

def zscore(series: pd.Series) -> float:
    """計算最新值的 Z-score"""
    if len(series) < 2:
        return 0.0
    mean = series.mean()
    std = series.std(ddof=0)
    if std < 1e-12:
        return 0.0
    return float((series.iloc[-1] - mean) / std)


def percentile_rank(series: pd.Series) -> float:
    """計算最新值的百分位數"""
    if len(series) < 2:
        return 0.5
    x = series.iloc[-1]
    return float((series <= x).mean())


def get_risk_band(ratio: float) -> str:
    """根據 interest/tax ratio 判定風險分級"""
    for band, (low, high) in RISK_BANDS.items():
        if low <= ratio < high:
            return band
    return "red"


def get_risk_band_emoji(band: str) -> str:
    """取得風險分級的 emoji"""
    return {
        "green": "🟢",
        "yellow": "🟡",
        "orange": "🟠",
        "red": "🔴",
    }.get(band, "⚪")


# ============================================================================
# 核心計算函數
# ============================================================================

def calculate_interest_tax_ratio(
    interest_payments: float,
    tax_revenue: float,
) -> float:
    """計算利息/稅收比"""
    if tax_revenue < 1e-12:
        return float("inf")
    return interest_payments / tax_revenue


def stress_interest_tax_ratio(
    interest_payments: float,
    tax_revenue: float,
    debt_stock: float,
    delta_yield_bp: int,
    pass_through: float,
    tax_shock: float = 0.0,
) -> float:
    """
    計算壓力測試後的 interest/tax ratio

    Args:
        interest_payments: 當前利息支出
        tax_revenue: 當前稅收
        debt_stock: 債務存量
        delta_yield_bp: 殖利率上升幅度（bp）
        pass_through: 再定價/再融資比例
        tax_shock: 稅收衝擊（如 -0.05 表示下降 5%）

    Returns:
        壓測後的 interest/tax ratio
    """
    delta_yield = delta_yield_bp / 10000.0  # bp 轉小數
    additional_interest = debt_stock * pass_through * delta_yield
    stressed_tax = tax_revenue * (1.0 + tax_shock)

    if stressed_tax < 1e-12:
        return float("inf")

    return (interest_payments + additional_interest) / stressed_tax


def analyze_yield_stats(
    yield_history: List[float],
    tenor: str = "10Y",
    window_days: int = DEFAULT_ANALYSIS_WINDOW,
) -> Dict[str, Any]:
    """分析殖利率統計"""
    series = pd.Series(yield_history[-window_days:])
    latest = series.iloc[-1]

    return {
        "tenor": tenor,
        "latest": float(latest),
        "zscore": zscore(series),
        "percentile": percentile_rank(series),
        "window_days": len(series),
        "min": float(series.min()),
        "max": float(series.max()),
        "mean": float(series.mean()),
        "interpretation": _interpret_yield_percentile(percentile_rank(series)),
    }


def _interpret_yield_percentile(percentile: float) -> str:
    """解讀殖利率百分位數"""
    if percentile >= 0.95:
        return f"分位數 {percentile:.0%}，處於極端高位區"
    elif percentile >= 0.80:
        return f"分位數 {percentile:.0%}，處於偏高區"
    elif percentile >= 0.50:
        return f"分位數 {percentile:.0%}，處於中性區"
    elif percentile >= 0.20:
        return f"分位數 {percentile:.0%}，處於偏低區"
    else:
        return f"分位數 {percentile:.0%}，處於極端低位區"


def run_stress_tests(
    interest_payments: float,
    tax_revenue: float,
    debt_stock: float,
    scenarios: List[Dict],
) -> List[Dict]:
    """執行多情境壓力測試"""
    results = []

    for sc in scenarios:
        # Year 1
        ratio_y1 = stress_interest_tax_ratio(
            interest_payments,
            tax_revenue,
            debt_stock,
            delta_yield_bp=sc["delta_yield_bp"],
            pass_through=sc.get("pass_through_year1", DEFAULT_PASS_THROUGH),
            tax_shock=sc.get("tax_shock", 0.0),
        )

        # Year 2 (累積效應)
        cumulative_pass_through = (
            sc.get("pass_through_year1", DEFAULT_PASS_THROUGH) +
            sc.get("pass_through_year2", DEFAULT_PASS_THROUGH)
        )
        ratio_y2 = stress_interest_tax_ratio(
            interest_payments,
            tax_revenue,
            debt_stock,
            delta_yield_bp=sc["delta_yield_bp"],
            pass_through=cumulative_pass_through,
            tax_shock=sc.get("tax_shock", 0.0),
        )

        results.append({
            "name": sc["name"],
            "assumptions": {
                "delta_yield_bp": sc["delta_yield_bp"],
                "pass_through_year1": sc.get("pass_through_year1", DEFAULT_PASS_THROUGH),
                "pass_through_year2": sc.get("pass_through_year2", DEFAULT_PASS_THROUGH),
                "tax_shock": sc.get("tax_shock", 0.0),
            },
            "results": {
                "year1_interest_tax_ratio": round(ratio_y1, 4),
                "year2_interest_tax_ratio": round(ratio_y2, 4),
            },
            "risk_band_year1": get_risk_band(ratio_y1),
            "risk_band_year2": get_risk_band(ratio_y2),
        })

    return results


def analyze_spillover_channel(us_assets: Dict) -> Dict:
    """分析外溢通道（日本對美資產）"""
    return {
        "enabled": True,
        "us_assets_estimate_usd": us_assets.get("total_usd", 0),
        "ust_holdings_usd": us_assets.get("ust_holdings_usd", 0),
        "components": [
            "UST holdings (TIC)",
            "Agency securities",
            "Corporate bonds",
            "Equities",
        ],
        "note": (
            "僅標示潛在通道與量級；"
            "是否『會拋售』屬行為假設，需搭配資金流/政策約束判讀"
        ),
    }


# ============================================================================
# 主分析函數
# ============================================================================

def run_quick_check(
    data: Optional[Dict] = None,
    force_refresh: bool = False,
    cache_dir: Optional[str] = None,
) -> Dict:
    """
    快速檢查：返回當前狀態摘要

    Args:
        data: 預先獲取的數據（如果為 None，會自動抓取）
        force_refresh: 強制刷新數據
        cache_dir: 緩存目錄
    """
    data_sources = {}
    fetch_errors = []

    if data is None:
        # 使用數據管理器獲取實時數據
        if HAS_DATA_MANAGER:
            try:
                manager = JapanDebtDataManager(cache_dir=cache_dir)
                data = manager.get_all_data(
                    force_refresh=force_refresh,
                    include_tic=False,  # 快速檢查不需要 TIC 數據
                )
                data_sources = data.get("data_sources", {})
                fetch_errors = data.get("fetch_errors") or []
            except Exception as e:
                fetch_errors.append(f"數據管理器錯誤: {e}")
                data = SAMPLE_DATA
                data_sources = {"all": "fallback"}
        else:
            data = SAMPLE_DATA
            data_sources = {"all": "fallback (no data_manager)"}

    fiscal = data["fiscal"]
    ratio = calculate_interest_tax_ratio(
        fiscal["interest_payments_jpy"],
        fiscal["tax_revenue_jpy"],
    )
    band = get_risk_band(ratio)

    yield_stats = analyze_yield_stats(
        data["jgb_10y"]["history"],
        tenor="10Y",
    )

    result = {
        "mode": "quick_check",
        "as_of": datetime.now().strftime("%Y-%m-%d"),
        "yield_stats": {
            "tenor": yield_stats["tenor"],
            "latest": yield_stats["latest"],
            "percentile": round(yield_stats["percentile"], 2),
        },
        "fiscal": {
            "interest_tax_ratio": round(ratio, 3),
            "risk_band": band,
            "risk_band_emoji": get_risk_band_emoji(band),
        },
        "headline": (
            f"利息支出佔稅收 {ratio:.1%}，"
            f"處於{get_risk_band_emoji(band)} {band.upper()} 區"
        ),
        "data_sources": data_sources,
    }

    if fetch_errors:
        result["fetch_errors"] = fetch_errors

    return result


def run_full_analysis(
    data: Optional[Dict] = None,
    scenarios: Optional[List[Dict]] = None,
    include_spillover: bool = True,
    force_refresh: bool = False,
    cache_dir: Optional[str] = None,
) -> Dict:
    """
    完整分析：現況 + 壓測 + 外溢

    Args:
        data: 預先獲取的數據（如果為 None，會自動抓取）
        scenarios: 壓力測試情境
        include_spillover: 是否包含外溢通道分析
        force_refresh: 強制刷新數據
        cache_dir: 緩存目錄
    """
    data_sources = {}
    fetch_errors = []

    if data is None:
        # 使用數據管理器獲取實時數據
        if HAS_DATA_MANAGER:
            try:
                manager = JapanDebtDataManager(cache_dir=cache_dir)
                data = manager.get_all_data(
                    force_refresh=force_refresh,
                    include_tic=include_spillover,
                )
                data_sources = data.get("data_sources", {})
                fetch_errors = data.get("fetch_errors") or []
            except Exception as e:
                fetch_errors.append(f"數據管理器錯誤: {e}")
                data = SAMPLE_DATA
                data_sources = {"all": "fallback"}
        else:
            data = SAMPLE_DATA
            data_sources = {"all": "fallback (no data_manager)"}

    if scenarios is None:
        scenarios = DEFAULT_SCENARIOS

    fiscal = data["fiscal"]
    ratio = calculate_interest_tax_ratio(
        fiscal["interest_payments_jpy"],
        fiscal["tax_revenue_jpy"],
    )
    band = get_risk_band(ratio)

    # 殖利率分析
    yield_stats = analyze_yield_stats(
        data["jgb_10y"]["history"],
        tenor="10Y",
    )

    # 壓力測試
    stress_results = run_stress_tests(
        fiscal["interest_payments_jpy"],
        fiscal["tax_revenue_jpy"],
        fiscal["debt_stock_jpy"],
        scenarios,
    )

    result = {
        "skill": "analyze_japan_debt_service_tax_burden",
        "mode": "full_analysis",
        "as_of": datetime.now().strftime("%Y-%m-%d"),
        "yield_stats": yield_stats,
        "fiscal": {
            "tax_revenue_jpy": fiscal["tax_revenue_jpy"],
            "interest_payments_jpy": fiscal["interest_payments_jpy"],
            "debt_stock_jpy": fiscal["debt_stock_jpy"],
            "interest_tax_ratio": round(ratio, 4),
            "risk_band": band,
            "risk_band_emoji": get_risk_band_emoji(band),
            "definition": {
                "tax_revenue_series": fiscal.get("tax_revenue_series", "general_account_tax"),
                "interest_payment_series": fiscal.get("interest_payment_series", "interest_only"),
                "fiscal_year": fiscal.get("fiscal_year", "unknown"),
            },
        },
        "stress_tests": stress_results,
        "headline_takeaways": _generate_takeaways(ratio, band, yield_stats, stress_results),
        "data_sources": data_sources,
    }

    if fetch_errors:
        result["fetch_errors"] = fetch_errors

    # 外溢通道（可選）
    if include_spillover and "us_assets" in data:
        result["spillover_channel"] = analyze_spillover_channel(data["us_assets"])

    return result


def _generate_takeaways(
    ratio: float,
    band: str,
    yield_stats: Dict,
    stress_results: List[Dict],
) -> List[str]:
    """生成 headline takeaways"""
    takeaways = []

    # 現況
    takeaways.append(
        f"當前 interest/tax ratio 為 {ratio:.1%}，處於 {band.upper()} 區"
    )

    # 殖利率
    pct = yield_stats["percentile"]
    if pct >= 0.90:
        takeaways.append(
            f"10Y JGB 殖利率 {yield_stats['latest']:.2f}% 處於 {pct:.0%} 分位，接近近期極值"
        )

    # 壓測
    worst_y2 = max(s["results"]["year2_interest_tax_ratio"] for s in stress_results)
    worst_band = get_risk_band(worst_y2)
    if worst_band in ("orange", "red"):
        takeaways.append(
            f"最嚴重壓測情境下，兩年後 ratio 可能升至 {worst_y2:.1%}，進入 {worst_band.upper()} 區"
        )

    # 口徑提醒
    takeaways.append(
        "注意：不同口徑（國稅 vs 一般會計 vs 總收入）會產生不同數值，本分析已標示使用口徑"
    )

    return takeaways


# ============================================================================
# 輸出格式化
# ============================================================================

def format_markdown(result: Dict) -> str:
    """格式化為 Markdown 報告"""
    lines = []

    lines.append(f"# 分析日本債務利息負擔報告")
    lines.append(f"\n> 分析日期：{result.get('as_of', 'N/A')}")
    lines.append("")

    # 摘要
    if "headline" in result:
        lines.append(f"## 摘要\n")
        lines.append(f"**{result['headline']}**\n")

    # 殖利率
    if "yield_stats" in result:
        ys = result["yield_stats"]
        lines.append(f"## 殖利率狀態\n")
        lines.append(f"| 指標 | 數值 |")
        lines.append(f"|------|------|")
        lines.append(f"| {ys.get('tenor', '10Y')} 殖利率 | {ys.get('latest', 'N/A'):.2f}% |")
        if "percentile" in ys:
            lines.append(f"| 百分位數 | {ys['percentile']:.0%} |")
        if "interpretation" in ys:
            lines.append(f"\n{ys['interpretation']}\n")

    # 財政
    if "fiscal" in result:
        f = result["fiscal"]
        lines.append(f"## 財政利息負擔\n")
        lines.append(f"| 指標 | 數值 |")
        lines.append(f"|------|------|")
        if "tax_revenue_jpy" in f:
            lines.append(f"| 稅收 | ¥{f['tax_revenue_jpy']/1e12:.1f}兆 |")
        if "interest_payments_jpy" in f:
            lines.append(f"| 利息支出 | ¥{f['interest_payments_jpy']/1e12:.1f}兆 |")
        lines.append(f"| Interest/Tax Ratio | {f.get('interest_tax_ratio', 0):.1%} |")
        lines.append(f"| 風險分級 | {f.get('risk_band_emoji', '')} {f.get('risk_band', '').upper()} |")
        lines.append("")

    # 壓力測試
    if "stress_tests" in result:
        lines.append(f"## 壓力測試結果\n")
        lines.append(f"| 情境 | Year 1 Ratio | Year 2 Ratio | 風險分級 |")
        lines.append(f"|------|--------------|--------------|----------|")
        for s in result["stress_tests"]:
            r = s["results"]
            lines.append(
                f"| {s['name']} | {r['year1_interest_tax_ratio']:.1%} | "
                f"{r['year2_interest_tax_ratio']:.1%} | "
                f"{get_risk_band_emoji(s['risk_band_year2'])} {s['risk_band_year2'].upper()} |"
            )
        lines.append("")

    # 外溢通道
    if "spillover_channel" in result:
        sp = result["spillover_channel"]
        lines.append(f"## 外溢通道（日本對美資產）\n")
        lines.append(f"- 估計總規模：${sp.get('us_assets_estimate_usd', 0)/1e12:.1f}兆")
        lines.append(f"- 美債持有：${sp.get('ust_holdings_usd', 0)/1e12:.1f}兆")
        lines.append(f"\n> {sp.get('note', '')}\n")

    # Takeaways
    if "headline_takeaways" in result:
        lines.append(f"## 要點摘要\n")
        for t in result["headline_takeaways"]:
            lines.append(f"- {t}")
        lines.append("")

    return "\n".join(lines)


# ============================================================================
# CLI 入口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Japan Debt Service Tax Burden Analyzer"
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="快速檢查模式"
    )
    parser.add_argument(
        "--full", action="store_true",
        help="完整分析模式"
    )
    parser.add_argument(
        "--stress", type=int, metavar="BP",
        help="單一殖利率衝擊壓測（bp）"
    )
    parser.add_argument(
        "--format", choices=["json", "markdown"], default="markdown",
        help="輸出格式（預設 markdown）"
    )
    parser.add_argument(
        "--no-spillover", action="store_true",
        help="不包含外溢通道分析"
    )
    parser.add_argument(
        "--refresh", action="store_true",
        help="強制刷新數據（忽略緩存）"
    )
    parser.add_argument(
        "--cache-dir", type=str, metavar="DIR",
        help="指定緩存目錄"
    )

    args = parser.parse_args()

    # 預設為快速檢查
    if not any([args.quick, args.full, args.stress]):
        args.quick = True

    # 執行分析
    if args.quick:
        result = run_quick_check(
            force_refresh=args.refresh,
            cache_dir=args.cache_dir,
        )
    elif args.stress:
        # 單一壓測情境
        scenarios = [{
            "name": f"+{args.stress}bp custom",
            "delta_yield_bp": args.stress,
            "pass_through_year1": DEFAULT_PASS_THROUGH,
            "pass_through_year2": DEFAULT_PASS_THROUGH,
            "tax_shock": 0.0,
        }]
        result = run_full_analysis(
            scenarios=scenarios,
            include_spillover=not args.no_spillover,
            force_refresh=args.refresh,
            cache_dir=args.cache_dir,
        )
    else:  # args.full
        result = run_full_analysis(
            include_spillover=not args.no_spillover,
            force_refresh=args.refresh,
            cache_dir=args.cache_dir,
        )

    # 輸出
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_markdown(result))


if __name__ == "__main__":
    main()
