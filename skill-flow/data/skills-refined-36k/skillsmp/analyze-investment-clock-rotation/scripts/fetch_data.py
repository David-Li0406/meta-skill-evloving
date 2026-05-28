#!/usr/bin/env python3
"""
Investment Clock - Data Fetcher
從 FRED 抓取獲利成長與金融環境數據
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, Optional

import pandas as pd
import requests


# ============================================================================
# FRED 資料抓取
# ============================================================================


def fetch_fred_csv(
    series_id: str,
    start_date: str,
    end_date: str,
) -> pd.Series:
    """
    從 FRED 抓取 CSV 資料

    Args:
        series_id: FRED 系列 ID
        start_date: 起始日期 (YYYY-MM-DD)
        end_date: 結束日期 (YYYY-MM-DD)

    Returns:
        時間序列 Series
    """
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv"
    params = {
        "id": series_id,
        "cosd": start_date,
        "coed": end_date,
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        # 解析 CSV
        from io import StringIO

        df = pd.read_csv(
            StringIO(response.text), parse_dates=["DATE"], index_col="DATE"
        )

        # 處理缺失值標記
        df = df.replace(".", pd.NA)
        df = df.astype(float)

        series = df.iloc[:, 0]
        series.name = series_id

        return series

    except requests.RequestException as e:
        print(f"Error fetching {series_id}: {e}", file=sys.stderr)
        return pd.Series(dtype=float, name=series_id)


def fetch_all_data(
    start_date: str,
    end_date: str,
    earnings_id: str = "CP",
    fci_id: str = "NFCI",
) -> Dict[str, pd.Series]:
    """
    抓取所有需要的數據

    Args:
        start_date: 起始日期
        end_date: 結束日期
        earnings_id: 獲利指標 FRED ID
        fci_id: 金融環境指標 FRED ID

    Returns:
        包含各序列的字典
    """
    print(f"Fetching {earnings_id}...", file=sys.stderr)
    earnings = fetch_fred_csv(earnings_id, start_date, end_date)

    print(f"Fetching {fci_id}...", file=sys.stderr)
    fci = fetch_fred_csv(fci_id, start_date, end_date)

    return {
        "earnings": earnings,
        "fci": fci,
    }


# ============================================================================
# 主入口
# ============================================================================


def main():
    parser = argparse.ArgumentParser(
        description="Fetch data for Investment Clock analysis"
    )
    parser.add_argument(
        "--earnings",
        type=str,
        default="CP",
        help="FRED series ID for earnings (default: CP)",
    )
    parser.add_argument(
        "--fci",
        type=str,
        default="NFCI",
        help="FRED series ID for financial conditions (default: NFCI)",
    )
    parser.add_argument(
        "--start",
        type=str,
        default="2020-01-01",
        help="Start date (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--end",
        type=str,
        default=None,
        help="End date (YYYY-MM-DD), defaults to today",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file path (JSON)",
    )

    args = parser.parse_args()

    end_date = args.end or datetime.now().strftime("%Y-%m-%d")

    # 抓取數據
    data = fetch_all_data(
        start_date=args.start,
        end_date=end_date,
        earnings_id=args.earnings,
        fci_id=args.fci,
    )

    # 轉換為可序列化格式
    output = {
        "metadata": {
            "start_date": args.start,
            "end_date": end_date,
            "earnings_series": args.earnings,
            "fci_series": args.fci,
            "fetched_at": datetime.now().isoformat(),
        },
        "data": {
            "earnings": {
                "dates": [str(d.date()) for d in data["earnings"].index],
                "values": data["earnings"].tolist(),
            },
            "fci": {
                "dates": [str(d.date()) for d in data["fci"].index],
                "values": data["fci"].tolist(),
            },
        },
    }

    # 輸出
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, default=str)
        print(f"Data saved to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(output, indent=2, default=str))


if __name__ == "__main__":
    main()
