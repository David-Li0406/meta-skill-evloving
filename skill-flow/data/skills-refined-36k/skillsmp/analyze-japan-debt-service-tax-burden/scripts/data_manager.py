#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Japan Debt Data Manager
協調多數據源抓取、緩存管理與數據驗證

用法:
    python data_manager.py --fetch-all
    python data_manager.py --refresh

或作為模組:
    from data_manager import JapanDebtDataManager
    manager = JapanDebtDataManager()
    data = manager.get_all_data()
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 本地模組導入
try:
    from fetch_jgb_yields import JGBYieldFetcher
    from fetch_tic_holdings import TICHoldingsFetcher
except ImportError:
    # 當作為獨立腳本運行時
    import sys

    sys.path.insert(0, str(Path(__file__).parent))
    from fetch_jgb_yields import JGBYieldFetcher
    from fetch_tic_holdings import TICHoldingsFetcher


# 驗證規則
VALIDATION_RULES = {
    "jgb_10y": {"min": -0.5, "max": 5.0, "unit": "%"},
    "tax_revenue_jpy": {"min": 50e12, "max": 100e12, "unit": "yen"},
    "interest_payments_jpy": {"min": 5e12, "max": 35e12, "unit": "yen"},
    "debt_stock_jpy": {"min": 800e12, "max": 1500e12, "unit": "yen"},
    "ust_holdings_usd": {"min": 500e9, "max": 2000e9, "unit": "usd"},
}

# 硬編碼的最終 Fallback 數據
FALLBACK_DATA = {
    "jgb_10y": {
        "latest": 1.23,
        "history": [0.8, 0.9, 1.0, 1.1, 1.15, 1.2, 1.23],
        "source": "fallback",
    },
    "fiscal": {
        "tax_revenue_jpy": 72_000_000_000_000,
        "interest_payments_jpy": 10_000_000_000_000,
        "debt_service_jpy": 27_000_000_000_000,
        "debt_stock_jpy": 1_286_000_000_000_000,
        "fiscal_year": "FY2024",
        "source": "fallback",
    },
    "us_assets": {
        "ust_holdings_usd": 1_100_000_000_000,
        "source": "fallback",
    },
}


class JapanDebtDataManager:
    """
    日本債務數據管理器
    協調 JGB 殖利率、財政數據、TIC 持有數據
    """

    def __init__(self, cache_dir: Optional[str] = None, config_dir: Optional[str] = None):
        """
        初始化數據管理器

        Args:
            cache_dir: 緩存目錄路徑
            config_dir: 配置目錄路徑
        """
        base_dir = Path(__file__).parent.parent

        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = base_dir / "data" / "cache"

        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = base_dir / "config"

        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # 初始化抓取器
        self.jgb_fetcher = JGBYieldFetcher(cache_dir=str(self.cache_dir))
        self.tic_fetcher = TICHoldingsFetcher(cache_dir=str(self.cache_dir))

        # 追蹤錯誤與數據源
        self.fetch_errors: List[str] = []
        self.data_sources: Dict[str, str] = {}

    def _validate_value(self, key: str, value: Any) -> bool:
        """驗證數值是否在合理範圍內"""
        if key not in VALIDATION_RULES:
            return True
        if value is None:
            return False

        rule = VALIDATION_RULES[key]
        return rule["min"] <= value <= rule["max"]

    def _load_fiscal_config(self) -> Optional[Dict[str, Any]]:
        """載入財政數據配置"""
        config_path = self.config_dir / "fiscal_data.json"
        if not config_path.exists():
            return None

        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config
        except (json.JSONDecodeError, IOError) as e:
            self.fetch_errors.append(f"載入財政配置失敗: {e}")
            return None

    def get_fiscal_data(
        self,
        fiscal_year: Optional[str] = None,
        use_debt_service: bool = False,
    ) -> Dict[str, Any]:
        """
        取得財政數據

        Args:
            fiscal_year: 財政年度（如 FY2025），預設使用最新
            use_debt_service: 是否使用國債費（含本金）而非純利息

        Returns:
            財政數據字典
        """
        config = self._load_fiscal_config()

        if config:
            fy = fiscal_year or config.get("latest_fy", "FY2025")
            fy_data = config.get("data", {}).get(fy)

            if fy_data:
                interest_key = "debt_service_jpy" if use_debt_service else "interest_payments_jpy"
                interest_value = fy_data.get(interest_key, fy_data.get("interest_payments_jpy"))

                result = {
                    "tax_revenue_jpy": fy_data["tax_revenue_jpy"],
                    "interest_payments_jpy": interest_value,
                    "debt_stock_jpy": fy_data["debt_stock_jpy"],
                    "fiscal_year": fy,
                    "tax_revenue_series": "general_account_tax",
                    "interest_payment_series": "debt_service" if use_debt_service else "interest_only",
                    "source": fy_data.get("source", f"config/{fy}"),
                }

                # 驗證
                for key in ["tax_revenue_jpy", "interest_payments_jpy", "debt_stock_jpy"]:
                    if not self._validate_value(key, result.get(key)):
                        self.fetch_errors.append(f"財政數據 {key} 超出合理範圍")

                self.data_sources["fiscal"] = result["source"]
                return result

        # Fallback
        self.fetch_errors.append("使用 fallback 財政數據")
        self.data_sources["fiscal"] = "fallback"
        return FALLBACK_DATA["fiscal"].copy()

    def get_jgb_yields(
        self,
        tenor: str = "10Y",
        force_refresh: bool = False,
    ) -> Dict[str, Any]:
        """
        取得 JGB 殖利率數據

        Args:
            tenor: 期限
            force_refresh: 強制刷新

        Returns:
            殖利率數據字典
        """
        result = self.jgb_fetcher.fetch_yield(
            tenor=tenor,
            force_refresh=force_refresh,
        )

        # 驗證
        if result.get("latest") is not None:
            if not self._validate_value("jgb_10y", result["latest"]):
                self.fetch_errors.append(f"JGB {tenor} 殖利率 {result['latest']} 超出合理範圍")
            self.data_sources[f"jgb_{tenor.lower()}"] = result.get("source", "unknown")
        else:
            # Fallback
            self.fetch_errors.append(f"JGB {tenor} 數據獲取失敗，使用 fallback")
            self.data_sources[f"jgb_{tenor.lower()}"] = "fallback"
            return {
                "latest": FALLBACK_DATA["jgb_10y"]["latest"],
                "history": FALLBACK_DATA["jgb_10y"]["history"],
                "source": "fallback",
                "cached": False,
            }

        return result

    def get_tic_holdings(self, force_refresh: bool = False) -> Dict[str, Any]:
        """
        取得 TIC 日本持有美債數據

        Args:
            force_refresh: 強制刷新

        Returns:
            TIC 數據字典
        """
        result = self.tic_fetcher.fetch_japan_holdings(force_refresh=force_refresh)

        # 驗證
        if result.get("ust_holdings_usd") is not None:
            if not self._validate_value("ust_holdings_usd", result["ust_holdings_usd"]):
                self.fetch_errors.append(
                    f"TIC 持有量 {result['ust_holdings_usd']/1e9:.0f}B 超出合理範圍"
                )
            self.data_sources["tic"] = result.get("source", "unknown")
        else:
            # Fallback
            self.fetch_errors.append("TIC 數據獲取失敗，使用 fallback")
            self.data_sources["tic"] = "fallback"
            return {
                "ust_holdings_usd": FALLBACK_DATA["us_assets"]["ust_holdings_usd"],
                "source": "fallback",
                "cached": False,
            }

        return result

    def get_all_data(
        self,
        force_refresh: bool = False,
        include_tic: bool = True,
        use_debt_service: bool = False,
    ) -> Dict[str, Any]:
        """
        取得所有數據

        Args:
            force_refresh: 強制刷新所有數據源
            include_tic: 是否包含 TIC 數據
            use_debt_service: 是否使用國債費（含本金）而非純利息

        Returns:
            {
                "jgb_10y": {...},
                "fiscal": {...},
                "us_assets": {...},  # 如果 include_tic
                "data_sources": {...},
                "fetch_errors": [...],
                "fetch_time": "..."
            }
        """
        # 重置追蹤
        self.fetch_errors = []
        self.data_sources = {}

        print("=" * 60)
        print("Japan Debt Data Manager - 數據抓取")
        print("=" * 60)

        # 抓取 JGB 殖利率
        jgb_data = self.get_jgb_yields(tenor="10Y", force_refresh=force_refresh)

        # 取得財政數據
        fiscal_data = self.get_fiscal_data(use_debt_service=use_debt_service)

        result = {
            "jgb_10y": jgb_data,
            "fiscal": fiscal_data,
            "data_sources": self.data_sources.copy(),
            "fetch_errors": self.fetch_errors.copy() if self.fetch_errors else None,
            "fetch_time": datetime.now().isoformat(),
        }

        # TIC 數據（可選）
        if include_tic:
            tic_data = self.get_tic_holdings(force_refresh=force_refresh)
            result["us_assets"] = {
                "ust_holdings_usd": tic_data.get("ust_holdings_usd"),
                "total_usd": tic_data.get("ust_holdings_usd"),  # 簡化估計
                "as_of": tic_data.get("as_of"),
                "source": tic_data.get("source"),
            }

        print("\n" + "=" * 60)
        print("數據源摘要:")
        for key, source in self.data_sources.items():
            print(f"  - {key}: {source}")
        if self.fetch_errors:
            print("\n警告:")
            for err in self.fetch_errors:
                print(f"  ! {err}")
        print("=" * 60)

        return result


def main():
    """命令列介面"""
    import argparse

    parser = argparse.ArgumentParser(description="Japan Debt Data Manager")
    parser.add_argument("--fetch-all", action="store_true", help="抓取所有數據")
    parser.add_argument("--refresh", action="store_true", help="強制刷新（忽略緩存）")
    parser.add_argument("--cache-dir", type=str, help="緩存目錄")
    parser.add_argument("--output", type=str, help="輸出 JSON 檔案")
    parser.add_argument(
        "--use-debt-service",
        action="store_true",
        help="使用國債費（含本金）而非純利息",
    )

    args = parser.parse_args()

    manager = JapanDebtDataManager(cache_dir=args.cache_dir)

    if args.fetch_all or True:  # 預設抓取所有
        data = manager.get_all_data(
            force_refresh=args.refresh,
            use_debt_service=args.use_debt_service,
        )

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            print(f"\n資料已儲存至: {args.output}")
        else:
            print("\n完整數據:")
            print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
