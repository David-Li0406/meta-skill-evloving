#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JGB 殖利率資料抓取模組
使用 FRED CSV endpoint（無需 API key），支援 yfinance 作為備用

用法:
    python fetch_jgb_yields.py --tenor 10Y
    python fetch_jgb_yields.py --tenor 10Y --start 2020-01-01

或作為模組:
    from fetch_jgb_yields import JGBYieldFetcher
    fetcher = JGBYieldFetcher()
    data = fetcher.fetch_yield('10Y')
"""

import json
import random
import time
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
import requests

# FRED 系列代碼對照表
FRED_JGB_SERIES = {
    "10Y": "IRLTLT01JPM156N",  # 日本長期利率（10Y 月度）
    "short": "INTGSTJPM193N",  # 日本短期利率
}

# yfinance 代理標的（用於即時數據）
YFINANCE_PROXIES = {
    "10Y": "^TNX",  # 美國 10Y 作為參考（需調整）
}


class JGBYieldFetcher:
    """
    JGB 殖利率抓取器
    優先級：FRED > yfinance > 本地緩存
    """

    FRED_BASE_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv"

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    ]

    # 緩存過期時間（秒）
    CACHE_EXPIRY_SECONDS = 86400  # 24 小時

    def __init__(self, cache_dir: Optional[str] = None):
        """
        初始化 JGB 殖利率抓取器

        Args:
            cache_dir: 緩存目錄路徑，預設為 scripts 目錄下的 ../data/cache
        """
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(__file__).parent.parent / "data" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _random_delay(self, min_sec: float = 0.3, max_sec: float = 1.0):
        """模擬人類行為的隨機延遲"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def _get_headers(self) -> Dict[str, str]:
        """取得隨機 headers"""
        return {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "text/csv,text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    def _get_cache_path(self, tenor: str) -> Path:
        """取得緩存檔案路徑"""
        return self.cache_dir / f"jgb_{tenor}_yield.json"

    def _load_from_cache(self, tenor: str) -> Optional[Dict[str, Any]]:
        """從緩存載入資料"""
        cache_path = self._get_cache_path(tenor)
        if cache_path.exists():
            cache_age = time.time() - cache_path.stat().st_mtime
            if cache_age < self.CACHE_EXPIRY_SECONDS:
                try:
                    with open(cache_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        data["cached"] = True
                        data["cache_age_hours"] = round(cache_age / 3600, 1)
                        return data
                except (json.JSONDecodeError, KeyError):
                    pass
        return None

    def _save_to_cache(self, tenor: str, data: Dict[str, Any]):
        """儲存資料到緩存"""
        cache_path = self._get_cache_path(tenor)
        cache_data = {
            "tenor": tenor,
            "latest": data.get("latest"),
            "history": data.get("history", []),
            "dates": data.get("dates", []),
            "source": data.get("source"),
            "fetch_time": datetime.now().isoformat(),
        }
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

    def _fetch_from_fred(
        self,
        tenor: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """從 FRED 抓取 JGB 殖利率"""
        series_id = FRED_JGB_SERIES.get(tenor)
        if not series_id:
            print(f"  ! 不支援的期限: {tenor}")
            return None

        # 預設抓取近 5 年數據
        if not start_date:
            start_date = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")

        params = {"id": series_id, "cosd": start_date, "coed": end_date}
        url = f"{self.FRED_BASE_URL}?{'&'.join(f'{k}={v}' for k, v in params.items())}"

        self._random_delay()

        try:
            response = requests.get(url, headers=self._get_headers(), timeout=30)
            response.raise_for_status()

            df = pd.read_csv(
                StringIO(response.text),
                index_col=0,
                parse_dates=True,
                na_values=["."],
            )

            if df.empty:
                print(f"  ! FRED {series_id}: 無資料")
                return None

            series = df.iloc[:, 0].dropna()
            if series.empty:
                return None

            result = {
                "tenor": tenor,
                "latest": float(series.iloc[-1]),
                "history": series.values.tolist(),
                "dates": series.index.strftime("%Y-%m-%d").tolist(),
                "source": f"FRED/{series_id}",
                "cached": False,
            }

            print(f"  + FRED {series_id}: 獲取 {len(series)} 筆資料，最新 {result['latest']:.2f}%")
            return result

        except requests.RequestException as e:
            print(f"  ! FRED 請求失敗: {e}")
            return None
        except Exception as e:
            print(f"  ! FRED 解析失敗: {e}")
            return None

    def _fetch_from_yfinance(self, tenor: str) -> Optional[Dict[str, Any]]:
        """從 yfinance 抓取備用數據"""
        try:
            import yfinance as yf
        except ImportError:
            print("  ! yfinance 未安裝，跳過備用數據源")
            return None

        ticker = YFINANCE_PROXIES.get(tenor)
        if not ticker:
            return None

        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="2y")

            if hist.empty:
                return None

            # 使用收盤價作為殖利率代理
            series = hist["Close"].dropna()

            result = {
                "tenor": tenor,
                "latest": float(series.iloc[-1]),
                "history": series.values.tolist(),
                "dates": series.index.strftime("%Y-%m-%d").tolist(),
                "source": f"yfinance/{ticker}",
                "cached": False,
                "note": "使用美國 10Y 作為代理，僅供參考",
            }

            print(f"  + yfinance {ticker}: 獲取 {len(series)} 筆資料")
            return result

        except Exception as e:
            print(f"  ! yfinance 抓取失敗: {e}")
            return None

    def fetch_yield(
        self,
        tenor: str = "10Y",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        use_cache: bool = True,
        force_refresh: bool = False,
    ) -> Dict[str, Any]:
        """
        抓取 JGB 殖利率

        Args:
            tenor: 期限（10Y, short）
            start_date: 起始日期（YYYY-MM-DD）
            end_date: 結束日期（YYYY-MM-DD）
            use_cache: 是否使用緩存
            force_refresh: 強制刷新（忽略緩存）

        Returns:
            {
                "tenor": "10Y",
                "latest": 1.23,
                "history": [0.8, 0.9, ...],
                "dates": ["2023-01-01", ...],
                "source": "FRED/IRLTLT01JPM156N",
                "cached": False
            }
        """
        print(f"\n抓取 JGB {tenor} 殖利率...")

        # 嘗試從緩存載入
        if use_cache and not force_refresh:
            cached_data = self._load_from_cache(tenor)
            if cached_data:
                print(f"  + 從緩存載入（{cached_data.get('cache_age_hours', 0):.1f} 小時前）")
                return cached_data

        # 嘗試 FRED
        result = self._fetch_from_fred(tenor, start_date, end_date)

        # 嘗試 yfinance 作為備用
        if result is None:
            print("  ! FRED 失敗，嘗試 yfinance...")
            result = self._fetch_from_yfinance(tenor)

        # 最後嘗試緩存（即使過期）
        if result is None:
            print("  ! 所有數據源失敗，嘗試過期緩存...")
            cache_path = self._get_cache_path(tenor)
            if cache_path.exists():
                try:
                    with open(cache_path, "r", encoding="utf-8") as f:
                        result = json.load(f)
                        result["cached"] = True
                        result["stale"] = True
                        print(f"  + 使用過期緩存")
                except:
                    pass

        # 完全失敗
        if result is None:
            result = {
                "tenor": tenor,
                "latest": None,
                "history": [],
                "dates": [],
                "source": "unavailable",
                "cached": False,
                "error": "所有數據源均無法獲取",
            }

        # 儲存到緩存
        if result.get("latest") is not None and not result.get("stale"):
            self._save_to_cache(tenor, result)

        return result


def main():
    """命令列介面"""
    import argparse

    parser = argparse.ArgumentParser(description="JGB 殖利率抓取工具")
    parser.add_argument("--tenor", type=str, default="10Y", help="期限（10Y, short）")
    parser.add_argument("--start", type=str, help="起始日期（YYYY-MM-DD）")
    parser.add_argument("--end", type=str, help="結束日期（YYYY-MM-DD）")
    parser.add_argument("--refresh", action="store_true", help="強制刷新（忽略緩存）")
    parser.add_argument("--cache-dir", type=str, help="緩存目錄")
    parser.add_argument("--output", type=str, help="輸出 JSON 檔案")

    args = parser.parse_args()

    fetcher = JGBYieldFetcher(cache_dir=args.cache_dir)
    result = fetcher.fetch_yield(
        tenor=args.tenor,
        start_date=args.start,
        end_date=args.end,
        force_refresh=args.refresh,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n資料已儲存至: {args.output}")
    else:
        print(f"\n結果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
