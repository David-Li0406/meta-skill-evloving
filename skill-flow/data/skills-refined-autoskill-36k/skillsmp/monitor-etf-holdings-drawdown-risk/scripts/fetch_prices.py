#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
fetch_prices.py - 抓取商品價格數據

從 Yahoo Finance 抓取商品現貨或期貨價格。
"""

import argparse
import json
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

try:
    import yfinance as yf
except ImportError:
    print("請安裝 yfinance: pip install yfinance")
    raise


def fetch_price_series(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.Series:
    """
    從 Yahoo Finance 抓取價格序列

    Parameters
    ----------
    symbol : str
        Yahoo Finance 代碼（如 XAGUSD=X, SI=F）
    start_date : str, optional
        起始日期 (YYYY-MM-DD)，預設 10 年前
    end_date : str, optional
        結束日期 (YYYY-MM-DD)，預設今天

    Returns
    -------
    pd.Series
        價格序列，index 為日期
    """
    # 預設日期範圍
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    if start_date is None:
        start_dt = datetime.now() - timedelta(days=3650)  # 10 年
        start_date = start_dt.strftime("%Y-%m-%d")

    # 抓取數據
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start_date, end=end_date)

    if data.empty:
        raise ValueError(f"無法取得 {symbol} 的價格數據")

    # 使用收盤價
    price = data["Close"]
    price.name = symbol
    price.index = pd.to_datetime(price.index).date
    price.index = pd.DatetimeIndex(price.index)

    return price


def main():
    parser = argparse.ArgumentParser(
        description="抓取商品價格數據"
    )
    parser.add_argument(
        "--symbol", "-s",
        required=True,
        help="Yahoo Finance 代碼（如 XAGUSD=X, SI=F）"
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
        "--output", "-o",
        help="輸出檔案路徑（CSV 或 JSON）"
    )

    args = parser.parse_args()

    # 抓取價格
    price = fetch_price_series(
        symbol=args.symbol,
        start_date=args.start,
        end_date=args.end
    )

    # 輸出
    if args.output:
        if args.output.endswith(".json"):
            result = {
                "symbol": args.symbol,
                "start": str(price.index[0].date()),
                "end": str(price.index[-1].date()),
                "count": len(price),
                "data": {
                    str(k.date()): v for k, v in price.items()
                }
            }
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
        else:
            df = price.to_frame()
            df.to_csv(args.output)
        print(f"已輸出至 {args.output}")
    else:
        print(f"Symbol: {args.symbol}")
        print(f"Period: {price.index[0].date()} to {price.index[-1].date()}")
        print(f"Count: {len(price)}")
        print(f"Latest: {price.iloc[-1]:.4f}")
        print()
        print(price.tail(10).to_string())


if __name__ == "__main__":
    main()
