#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
銅庫存回補訊號分析器

核心功能：
1. 計算 SHFE 和 COMEX 庫存回補速度 z-score
2. 判斷短期訊號（CAUTION / NEUTRAL / SUPPORTIVE）
3. 計算長期價格分位數
4. 執行歷史回測驗證

Usage:
    python inventory_signal_analyzer.py --quick
    python inventory_signal_analyzer.py --full
    python inventory_signal_analyzer.py --long-term
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import numpy as np
import pandas as pd

# ========== 配置區域 ==========
DEFAULT_CONFIG = {
    # 時間範圍
    "start_date": "2015-01-01",
    "end_date": None,  # None = today

    # 價格參數
    "price_ticker": "HG=F",  # COMEX 銅期貨
    "price_freq": "weekly",

    # 回補速度參數
    "fast_rebuild_window_weeks": 4,
    "fast_rebuild_z": 1.5,
    "z_baseline_weeks": 156,  # 3 年滾動

    # 庫存水位參數
    "high_inventory_mode": "percentile",  # absolute 或 percentile
    "high_inventory_percentile": 0.85,
    "high_inventory_absolute": 250000,  # 噸

    # 回測參數
    "peak_match_window_weeks": 2,

    # 長期分位數參數
    "long_term_window_years": 10,
    "cheap_percentile": 0.35,
    "rich_percentile": 0.65,
}
# ==============================


class CopperInventorySignalAnalyzer:
    """銅庫存回補訊號分析器"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.shfe_df: Optional[pd.DataFrame] = None
        self.comex_df: Optional[pd.DataFrame] = None
        self.price_df: Optional[pd.DataFrame] = None
        self.merged_df: Optional[pd.DataFrame] = None

    def load_inventory(self, cache_dir: str = "cache", source: str = "both") -> Dict[str, pd.DataFrame]:
        """
        載入庫存數據

        Parameters
        ----------
        cache_dir : str
            快取目錄
        source : str
            要載入的數據源：'shfe', 'comex', 或 'both'

        Returns
        -------
        Dict[str, pd.DataFrame]
            包含各數據源 DataFrame 的字典
        """
        cache_path = Path(cache_dir)
        result = {}

        if source in ["shfe", "both"]:
            shfe_path = cache_path / "shfe_inventory.csv"
            if shfe_path.exists():
                df = pd.read_csv(shfe_path)
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                self.shfe_df = df
                result['shfe'] = df
                print(f"[Data] 載入 {len(df)} 筆 SHFE 庫存數據")
            else:
                print(f"[Warning] 找不到 SHFE 庫存數據: {shfe_path}")

        if source in ["comex", "both"]:
            comex_path = cache_path / "comex_inventory.csv"
            if comex_path.exists():
                df = pd.read_csv(comex_path)
                df['date'] = pd.to_datetime(df['date'])
                df = df.sort_values('date').reset_index(drop=True)
                self.comex_df = df
                result['comex'] = df
                print(f"[Data] 載入 {len(df)} 筆 COMEX 庫存數據")
            else:
                print(f"[Warning] 找不到 COMEX 庫存數據: {comex_path}")

        if not result:
            raise FileNotFoundError(
                f"找不到庫存數據文件\n"
                "請先執行: python fetch_copper_data.py"
            )

        return result

    def load_price(self, cache_dir: str = "cache") -> pd.DataFrame:
        """載入銅價數據"""
        price_path = Path(cache_dir) / "copper_price.csv"

        if not price_path.exists():
            raise FileNotFoundError(
                f"找不到價格數據: {price_path}\n"
                "請先執行: python fetch_copper_data.py"
            )

        df = pd.read_csv(price_path)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)

        self.price_df = df
        print(f"[Data] 載入 {len(df)} 筆銅價數據")
        return df

    def to_weekly(self, df: pd.DataFrame, value_col: str) -> pd.DataFrame:
        """轉換為週頻數據"""
        df = df.copy()
        df['week'] = df['date'].dt.to_period('W').dt.start_time
        weekly = df.groupby('week').agg({value_col: 'last'}).reset_index()
        weekly.columns = ['date', value_col]
        return weekly

    def merge_data(self, cache_dir: str = "cache") -> pd.DataFrame:
        """合併所有數據"""
        # 載入數據
        if self.shfe_df is None or self.comex_df is None:
            self.load_inventory(cache_dir, source="both")
        if self.price_df is None:
            self.load_price(cache_dir)

        # 轉換為週頻
        dataframes = []

        if self.shfe_df is not None:
            shfe_weekly = self.to_weekly(self.shfe_df, 'inventory_tonnes')
            shfe_weekly = shfe_weekly.rename(columns={'inventory_tonnes': 'shfe_inventory'})
            dataframes.append(shfe_weekly)

        if self.comex_df is not None:
            comex_weekly = self.to_weekly(self.comex_df, 'inventory_tonnes')
            comex_weekly = comex_weekly.rename(columns={'inventory_tonnes': 'comex_inventory'})
            dataframes.append(comex_weekly)

        if self.price_df is not None:
            price_weekly = self.to_weekly(self.price_df, 'close')
            dataframes.append(price_weekly)

        # 合併
        merged = dataframes[0]
        for df in dataframes[1:]:
            merged = pd.merge(merged, df, on='date', how='outer')

        merged = merged.sort_values('date').reset_index(drop=True)

        # 計算總庫存
        if 'shfe_inventory' in merged.columns and 'comex_inventory' in merged.columns:
            merged['total_inventory'] = merged['shfe_inventory'].fillna(0) + merged['comex_inventory'].fillna(0)

        self.merged_df = merged
        print(f"[Data] 合併後 {len(merged)} 筆週頻數據")
        return merged

    def compute_rebuild_zscore(self, df: Optional[pd.DataFrame] = None, source: str = "shfe") -> pd.DataFrame:
        """
        計算回補速度 z-score

        Parameters
        ----------
        df : pd.DataFrame
            數據框架
        source : str
            'shfe', 'comex', 或 'total'
        """
        if df is None:
            df = self.merged_df if self.merged_df is not None else self.merge_data()

        df = df.copy()
        W = self.config["fast_rebuild_window_weeks"]
        baseline_weeks = self.config["z_baseline_weeks"]

        col_map = {
            'shfe': 'shfe_inventory',
            'comex': 'comex_inventory',
            'total': 'total_inventory'
        }

        inv_col = col_map.get(source, 'shfe_inventory')

        if inv_col not in df.columns:
            print(f"[Warning] 缺少 {inv_col} 欄位")
            return df

        # 計算 W 週回補量
        rebuild_col = f'{source}_rebuild_W'
        z_col = f'{source}_rebuild_z'

        df[rebuild_col] = df[inv_col] - df[inv_col].shift(W)

        # 計算滾動 z-score
        mu = df[rebuild_col].rolling(baseline_weeks, min_periods=52).mean()
        sigma = df[rebuild_col].rolling(baseline_weeks, min_periods=52).std()
        df[z_col] = (df[rebuild_col] - mu) / sigma

        return df

    def compute_inventory_percentile(self, df: Optional[pd.DataFrame] = None, source: str = "shfe") -> pd.DataFrame:
        """計算庫存水位分位數"""
        if df is None:
            df = self.merged_df if self.merged_df is not None else self.merge_data()

        df = df.copy()
        lookback_weeks = self.config["long_term_window_years"] * 52

        col_map = {
            'shfe': 'shfe_inventory',
            'comex': 'comex_inventory',
            'total': 'total_inventory'
        }

        inv_col = col_map.get(source, 'shfe_inventory')
        pct_col = f'{source}_inventory_percentile'

        if inv_col not in df.columns:
            return df

        df[pct_col] = df[inv_col].rolling(
            lookback_weeks, min_periods=52
        ).apply(lambda x: (x.iloc[-1] - x.min()) / (x.max() - x.min()) if x.max() > x.min() else 0.5)

        return df

    def compute_price_percentile(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        """計算價格分位數"""
        if df is None:
            df = self.merged_df if self.merged_df is not None else self.merge_data()

        df = df.copy()
        lookback_weeks = self.config["long_term_window_years"] * 52

        if 'close' not in df.columns:
            return df

        df['price_percentile'] = df['close'].rolling(
            lookback_weeks, min_periods=52
        ).apply(lambda x: (x.iloc[-1] - x.min()) / (x.max() - x.min()) if x.max() > x.min() else 0.5)

        return df

    def generate_signals(self, df: Optional[pd.DataFrame] = None, cache_dir: str = "cache") -> pd.DataFrame:
        """生成訊號"""
        if df is None:
            df = self.merge_data(cache_dir)

        # 計算 SHFE 指標
        df = self.compute_rebuild_zscore(df, source="shfe")
        df = self.compute_inventory_percentile(df, source="shfe")

        # 計算 COMEX 指標
        df = self.compute_rebuild_zscore(df, source="comex")
        df = self.compute_inventory_percentile(df, source="comex")

        # 計算總庫存指標
        if 'total_inventory' in df.columns:
            df = self.compute_rebuild_zscore(df, source="total")
            df = self.compute_inventory_percentile(df, source="total")

        # 計算價格分位數
        df = self.compute_price_percentile(df)

        z_threshold = self.config["fast_rebuild_z"]

        # 判定 SHFE 高庫存
        if 'shfe_inventory_percentile' in df.columns:
            if self.config["high_inventory_mode"] == "absolute":
                df['shfe_high_inventory'] = df['shfe_inventory'] >= self.config["high_inventory_absolute"]
            else:
                df['shfe_high_inventory'] = df['shfe_inventory_percentile'] >= self.config["high_inventory_percentile"]

            # 判定 SHFE 快速回補
            if 'shfe_rebuild_z' in df.columns:
                df['shfe_fast_rebuild'] = df['shfe_rebuild_z'] >= z_threshold

        # 判定 COMEX 高庫存
        if 'comex_inventory_percentile' in df.columns:
            df['comex_high_inventory'] = df['comex_inventory_percentile'] >= self.config["high_inventory_percentile"]

            if 'comex_rebuild_z' in df.columns:
                df['comex_fast_rebuild'] = df['comex_rebuild_z'] >= z_threshold

        # 生成短期訊號（主要看 SHFE，COMEX 作為輔助）
        df['near_term_signal'] = 'NEUTRAL'

        # SHFE 觸發條件
        shfe_caution = False
        if 'shfe_high_inventory' in df.columns and 'shfe_fast_rebuild' in df.columns:
            shfe_caution = df['shfe_high_inventory'] & df['shfe_fast_rebuild']
            df.loc[shfe_caution, 'near_term_signal'] = 'CAUTION'

        # SHFE 去庫存快 → SUPPORTIVE
        if 'shfe_rebuild_z' in df.columns:
            shfe_supportive = df['shfe_rebuild_z'] < -z_threshold
            df.loc[shfe_supportive, 'near_term_signal'] = 'SUPPORTIVE'

        # 生成長期訊號
        cheap = self.config["cheap_percentile"]
        rich = self.config["rich_percentile"]
        df['long_term_view'] = 'FAIR'

        if 'price_percentile' in df.columns:
            df.loc[df['price_percentile'] <= cheap, 'long_term_view'] = 'CHEAP'
            df.loc[df['price_percentile'] >= rich, 'long_term_view'] = 'RICH'

        return df

    def backtest_signals(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """回測訊號命中率"""
        if df is None:
            df = self.generate_signals()

        N = self.config["peak_match_window_weeks"]

        # 找出訊號週
        signal_mask = df['near_term_signal'] == 'CAUTION'
        signal_indices = df[signal_mask].index.tolist()

        if len(signal_indices) == 0:
            return {
                "signal_count": 0,
                "hit_count": 0,
                "hit_rate": 0.0,
                "message": "無訊號觸發記錄"
            }

        hits = 0
        for idx in signal_indices:
            # 找 ±N 週的窗口
            start_idx = max(0, idx - N)
            end_idx = min(len(df) - 1, idx + N)

            window = df.iloc[start_idx:end_idx + 1]
            if len(window) == 0 or 'close' not in window.columns:
                continue

            # 檢查當前週是否為局部高點
            current_price = df.loc[idx, 'close']
            if pd.isna(current_price):
                continue

            max_price = window['close'].max()

            if current_price >= max_price * 0.99:  # 容許 1% 誤差
                hits += 1

        hit_rate = hits / len(signal_indices) if signal_indices else 0

        return {
            "signal_count": len(signal_indices),
            "hit_count": hits,
            "hit_rate": hit_rate,
            "peak_window_weeks": N
        }

    def get_latest_status(self, df: Optional[pd.DataFrame] = None) -> Dict[str, Any]:
        """取得最新狀態"""
        if df is None:
            df = self.generate_signals()

        # 取最後一筆有效數據
        latest = df.dropna(subset=['close']).iloc[-1] if 'close' in df.columns else df.iloc[-1]

        result = {
            "asof": latest['date'].strftime('%Y-%m-%d') if pd.notna(latest['date']) else None,
            "copper_price": float(latest['close']) if pd.notna(latest.get('close')) else None,
            "price_percentile": float(latest['price_percentile']) if pd.notna(latest.get('price_percentile')) else None,
            "near_term_signal": latest.get('near_term_signal', 'NEUTRAL'),
            "long_term_view": latest.get('long_term_view', 'FAIR'),
        }

        # SHFE 數據
        if 'shfe_inventory' in latest.index:
            result["shfe_inventory_tonnes"] = float(latest['shfe_inventory']) if pd.notna(latest['shfe_inventory']) else None
            result["shfe_rebuild_z"] = float(latest['shfe_rebuild_z']) if pd.notna(latest.get('shfe_rebuild_z')) else None
            result["shfe_inventory_percentile"] = float(latest['shfe_inventory_percentile']) if pd.notna(latest.get('shfe_inventory_percentile')) else None
            result["shfe_high_inventory"] = bool(latest['shfe_high_inventory']) if pd.notna(latest.get('shfe_high_inventory')) else False
            result["shfe_fast_rebuild"] = bool(latest['shfe_fast_rebuild']) if pd.notna(latest.get('shfe_fast_rebuild')) else False

        # COMEX 數據
        if 'comex_inventory' in latest.index:
            result["comex_inventory_tonnes"] = float(latest['comex_inventory']) if pd.notna(latest['comex_inventory']) else None
            result["comex_rebuild_z"] = float(latest['comex_rebuild_z']) if pd.notna(latest.get('comex_rebuild_z')) else None
            result["comex_inventory_percentile"] = float(latest['comex_inventory_percentile']) if pd.notna(latest.get('comex_inventory_percentile')) else None

        # 總庫存
        if 'total_inventory' in latest.index:
            result["total_inventory_tonnes"] = float(latest['total_inventory']) if pd.notna(latest['total_inventory']) else None

        return result

    def analyze(self, mode: str = "quick", cache_dir: str = "cache") -> Dict[str, Any]:
        """執行分析"""
        print(f"\n{'='*60}")
        print("銅庫存回補訊號分析")
        print(f"{'='*60}\n")

        # 載入並生成訊號
        df = self.generate_signals(cache_dir=cache_dir)

        result = {
            "mode": mode,
            "config": self.config,
            "latest": self.get_latest_status(df),
            "analyzed_at": datetime.now().isoformat()
        }

        if mode in ["full", "backtest"]:
            result["backtest"] = self.backtest_signals(df)

        return result


def format_output_markdown(result: Dict[str, Any]) -> str:
    """格式化 Markdown 輸出"""
    latest = result["latest"]

    output = []
    output.append("# 銅：庫存回補訊號（SHFE / COMEX）\n")

    output.append("## 最新狀態")
    output.append(f"- 數據日期：{latest.get('asof', 'N/A')}")

    # SHFE 庫存
    if latest.get('shfe_inventory_tonnes'):
        output.append(f"- SHFE 庫存：{latest['shfe_inventory_tonnes']:,.0f} 噸")
        z_score = latest.get('shfe_rebuild_z')
        if z_score is not None:
            z_label = "異常快" if z_score >= 1.5 else ("異常慢" if z_score <= -1.5 else "正常")
            output.append(f"- SHFE 4 週回補速度 z-score：{z_score:+.2f}（{z_label}）")

    # COMEX 庫存
    if latest.get('comex_inventory_tonnes'):
        output.append(f"- COMEX 庫存：{latest['comex_inventory_tonnes']:,.0f} 噸")
        z_score = latest.get('comex_rebuild_z')
        if z_score is not None:
            z_label = "異常快" if z_score >= 1.5 else ("異常慢" if z_score <= -1.5 else "正常")
            output.append(f"- COMEX 4 週回補速度 z-score：{z_score:+.2f}（{z_label}）")

    # 總庫存
    if latest.get('total_inventory_tonnes'):
        output.append(f"- 總庫存（SHFE + COMEX）：{latest['total_inventory_tonnes']:,.0f} 噸")

    # 銅價
    if latest.get('copper_price'):
        output.append(f"- 銅期貨價格：{latest['copper_price']:.2f} USD/lb\n")

    output.append("## 短期判斷（是否「有點超前」）")
    signal = latest.get('near_term_signal', 'NEUTRAL')
    signal_emoji = {"CAUTION": "⚠️", "NEUTRAL": "➖", "SUPPORTIVE": "✅"}.get(signal, "")
    output.append(f"- 訊號：**{signal_emoji} {signal}**")

    if signal == "CAUTION":
        reasons = []
        if latest.get('shfe_high_inventory') and latest.get('shfe_fast_rebuild'):
            reasons.append("SHFE 庫存「水位偏高」且「回補速度異常快」")
        output.append(f"- 原因：{'; '.join(reasons) if reasons else 'N/A'}")
    elif signal == "SUPPORTIVE":
        output.append("- 原因：庫存去化速度快，短線有支撐")
    else:
        output.append("- 原因：庫存水位與回補速度均在正常範圍")

    if "backtest" in result:
        bt = result["backtest"]
        if bt["signal_count"] > 0:
            output.append(f"- 歷史驗證：過去同類訊號在 ±{bt['peak_window_weeks']} 週內對應局部高點的命中率約 **{bt['hit_rate']:.0%}**")
            output.append(f"- 樣本數：{bt['signal_count']} 次訊號\n")

    output.append("\n## 長期判斷（是否仍「偏便宜」）")
    pct = latest.get('price_percentile')
    if pct is not None:
        output.append(f"- 銅價 10 年歷史分位數：{pct:.2f}")

    view = latest.get('long_term_view', 'FAIR')
    view_emoji = {"CHEAP": "💚", "FAIR": "➖", "RICH": "🔴"}.get(view, "")
    view_desc = {"CHEAP": "長期偏便宜", "FAIR": "長期中性", "RICH": "長期偏貴"}.get(view, view)
    output.append(f"- 結論：**{view_emoji} {view_desc}**")

    output.append("\n---")
    output.append("### 數據來源")
    output.append("- SHFE 庫存：MacroMicro (CDP)")
    output.append("- COMEX 庫存：MacroMicro (CDP)")
    output.append("- 銅價：Yahoo Finance (HG=F)")

    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description="銅庫存回補訊號分析"
    )
    parser.add_argument(
        "--quick", "-q",
        action="store_true",
        help="快速檢查當前狀態"
    )
    parser.add_argument(
        "--full", "-f",
        action="store_true",
        help="完整分析（含歷史回測）"
    )
    parser.add_argument(
        "--long-term", "-l",
        action="store_true",
        help="長期分位數分析"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="輸出 JSON 格式"
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default="cache",
        help="快取目錄"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="輸出文件路徑"
    )

    args = parser.parse_args()

    # 決定分析模式
    if args.full:
        mode = "full"
    elif args.long_term:
        mode = "long-term"
    else:
        mode = "quick"

    try:
        analyzer = CopperInventorySignalAnalyzer()
        result = analyzer.analyze(mode=mode, cache_dir=args.cache_dir)

        if args.json:
            output = json.dumps(result, indent=2, ensure_ascii=False, default=str)
        else:
            output = format_output_markdown(result)

        print(output)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n[Saved] {args.output}")

        return 0

    except Exception as e:
        print(f"\n[Error] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
