#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TIC（美國財政部國際資本）資料抓取模組
抓取日本持有美國國債數據

用法:
    python fetch_tic_holdings.py
    python fetch_tic_holdings.py --refresh

或作為模組:
    from fetch_tic_holdings import TICHoldingsFetcher
    fetcher = TICHoldingsFetcher()
    data = fetcher.fetch_japan_holdings()
"""

import json
import random
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import requests

# TIC 數據 URL
TIC_MFH_URL = "https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents/mfh.txt"


class TICHoldingsFetcher:
    """
    TIC 美債持有數據抓取器
    從美國財政部抓取主要外國持有者數據
    """

    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    ]

    # 緩存過期時間（秒）- 7 天
    CACHE_EXPIRY_SECONDS = 7 * 86400

    def __init__(self, cache_dir: Optional[str] = None):
        """
        初始化 TIC 抓取器

        Args:
            cache_dir: 緩存目錄路徑，預設為 scripts 目錄下的 ../data/cache
        """
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(__file__).parent.parent / "data" / "cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _random_delay(self, min_sec: float = 0.5, max_sec: float = 1.5):
        """模擬人類行為的隨機延遲"""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def _get_headers(self) -> Dict[str, str]:
        """取得隨機 headers"""
        return {
            "User-Agent": random.choice(self.USER_AGENTS),
            "Accept": "text/plain,text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }

    def _get_cache_path(self) -> Path:
        """取得緩存檔案路徑"""
        return self.cache_dir / "tic_japan_holdings.json"

    def _load_from_cache(self) -> Optional[Dict[str, Any]]:
        """從緩存載入資料"""
        cache_path = self._get_cache_path()
        if cache_path.exists():
            cache_age = time.time() - cache_path.stat().st_mtime
            if cache_age < self.CACHE_EXPIRY_SECONDS:
                try:
                    with open(cache_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        data["cached"] = True
                        data["cache_age_days"] = round(cache_age / 86400, 1)
                        return data
                except (json.JSONDecodeError, KeyError):
                    pass
        return None

    def _save_to_cache(self, data: Dict[str, Any]):
        """儲存資料到緩存"""
        cache_path = self._get_cache_path()
        cache_data = {
            "ust_holdings_usd": data.get("ust_holdings_usd"),
            "as_of": data.get("as_of"),
            "history": data.get("history", []),
            "source": data.get("source"),
            "fetch_time": datetime.now().isoformat(),
        }
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)

    def _parse_mfh_text(self, text: str) -> Optional[Dict[str, Any]]:
        """
        解析 TIC MFH 固定寬度文本檔案

        Args:
            text: mfh.txt 文件內容

        Returns:
            解析後的日本持有數據
        """
        lines = text.strip().split("\n")

        # 找到標題行（包含月份）
        header_line = None
        data_start = 0
        for i, line in enumerate(lines):
            # 標題行通常以月份名開頭或包含年份
            if re.search(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", line):
                header_line = line
                data_start = i + 1
                break

        if not header_line:
            print("  ! 無法找到標題行")
            return None

        # 解析月份標題
        # 格式類似: "          Jan    Feb    Mar   ... "
        months = re.findall(
            r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*(\d{2,4})?",
            header_line,
        )

        # 找到 Japan 行
        japan_data = None
        for line in lines[data_start:]:
            if line.strip().startswith("Japan"):
                japan_data = line
                break

        if not japan_data:
            print("  ! 無法找到 Japan 數據行")
            return None

        # 解析 Japan 數據
        # 格式類似: "Japan        1087.0  1079.3 ..."
        numbers = re.findall(r"[\d.]+", japan_data)

        if not numbers:
            print("  ! 無法解析 Japan 數據")
            return None

        # 取最新值（通常是最後一個非空數據）
        history = []
        for n in numbers:
            try:
                val = float(n)
                history.append(val)
            except ValueError:
                continue

        if not history:
            return None

        # 最新持有量（十億美元）
        latest = history[-1]

        # 嘗試確定日期（從月份列表）
        as_of = "unknown"
        if months:
            last_month = months[-1] if months else None
            if last_month:
                month_name = last_month[0]
                year = last_month[1] if len(last_month) > 1 and last_month[1] else str(
                    datetime.now().year
                )
                if len(year) == 2:
                    year = "20" + year
                as_of = f"{year}-{month_name}"

        return {
            "ust_holdings_usd": latest * 1e9,  # 轉換為實際美元金額
            "ust_holdings_billions": latest,
            "as_of": as_of,
            "history": history,
            "source": "US Treasury TIC",
            "cached": False,
        }

    def fetch_japan_holdings(
        self,
        use_cache: bool = True,
        force_refresh: bool = False,
    ) -> Dict[str, Any]:
        """
        抓取日本持有美國國債數據

        Args:
            use_cache: 是否使用緩存
            force_refresh: 強制刷新（忽略緩存）

        Returns:
            {
                "ust_holdings_usd": 1100000000000,  # 美元
                "ust_holdings_billions": 1100.0,   # 十億美元
                "as_of": "2025-Nov",
                "history": [1087.0, 1079.3, ...],
                "source": "US Treasury TIC",
                "cached": False
            }
        """
        print("\n抓取 TIC 日本美債持有數據...")

        # 嘗試從緩存載入
        if use_cache and not force_refresh:
            cached_data = self._load_from_cache()
            if cached_data:
                print(f"  + 從緩存載入（{cached_data.get('cache_age_days', 0):.1f} 天前）")
                return cached_data

        # 從 TIC 網站抓取
        self._random_delay()

        try:
            response = requests.get(TIC_MFH_URL, headers=self._get_headers(), timeout=30)
            response.raise_for_status()

            result = self._parse_mfh_text(response.text)

            if result:
                print(
                    f"  + TIC: Japan 持有 ${result['ust_holdings_billions']:.1f}B 美債 "
                    f"(as of {result['as_of']})"
                )
                self._save_to_cache(result)
                return result

        except requests.RequestException as e:
            print(f"  ! TIC 請求失敗: {e}")
        except Exception as e:
            print(f"  ! TIC 解析失敗: {e}")

        # 嘗試過期緩存
        print("  ! TIC 抓取失敗，嘗試過期緩存...")
        cache_path = self._get_cache_path()
        if cache_path.exists():
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    result = json.load(f)
                    result["cached"] = True
                    result["stale"] = True
                    print("  + 使用過期緩存")
                    return result
            except:
                pass

        # 完全失敗
        return {
            "ust_holdings_usd": None,
            "ust_holdings_billions": None,
            "as_of": None,
            "history": [],
            "source": "unavailable",
            "cached": False,
            "error": "無法獲取 TIC 數據",
        }


def main():
    """命令列介面"""
    import argparse

    parser = argparse.ArgumentParser(description="TIC 日本美債持有數據抓取工具")
    parser.add_argument("--refresh", action="store_true", help="強制刷新（忽略緩存）")
    parser.add_argument("--cache-dir", type=str, help="緩存目錄")
    parser.add_argument("--output", type=str, help="輸出 JSON 檔案")

    args = parser.parse_args()

    fetcher = TICHoldingsFetcher(cache_dir=args.cache_dir)
    result = fetcher.fetch_japan_holdings(force_refresh=args.refresh)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n資料已儲存至: {args.output}")
    else:
        print(f"\n結果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
