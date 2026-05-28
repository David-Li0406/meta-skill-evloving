#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
銅數據統一爬蟲（全自動 CDP + yfinance）

從 MacroMicro 提取 SHFE 和 COMEX 銅庫存數據，從 Yahoo Finance 提取銅期貨價格。
自動啟動 Chrome、等待頁面載入、提取數據、關閉 Chrome。

數據來源：
- SHFE 銅庫存: https://en.macromicro.me/series/8743/copper-shfe-warehouse-stock
- COMEX 銅庫存: https://www.macromicro.me/series/8742/copper-comex-warehouse-stock
- 銅期貨價格: Yahoo Finance (HG=F)

Usage:
    python fetch_copper_data.py                    # 抓取所有數據
    python fetch_copper_data.py --force-refresh    # 強制更新
    python fetch_copper_data.py --source shfe      # 只抓 SHFE
    python fetch_copper_data.py --source comex     # 只抓 COMEX
    python fetch_copper_data.py --source price     # 只抓價格
"""

import argparse
import json
import subprocess
import time
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List

import pandas as pd

try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False
    print("[Warning] yfinance 未安裝，無法抓取銅價。請執行: pip install yfinance")

# ========== 配置區域 ==========
# MacroMicro URLs
SHFE_INVENTORY_URL = "https://en.macromicro.me/series/8743/copper-shfe-warehouse-stock"
COMEX_INVENTORY_URL = "https://www.macromicro.me/series/8742/copper-comex-warehouse-stock"

# Yahoo Finance
COPPER_TICKER = "HG=F"  # COMEX Copper Futures 連續近月

# CDP 配置
CDP_PORT = 9222
CACHE_MAX_AGE_HOURS = 12
PAGE_LOAD_WAIT_SECONDS = 40  # 等待頁面載入的時間

# Chrome 路徑（按優先順序嘗試）
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
]
# ==============================

# Highcharts 數據提取 JavaScript
EXTRACT_HIGHCHARTS_JS = '''
(function() {
    if (typeof Highcharts === 'undefined' || !Highcharts.charts) {
        return JSON.stringify({error: 'Highcharts not found'});
    }

    var charts = Highcharts.charts.filter(c => c !== undefined && c !== null);
    if (charts.length === 0) {
        return JSON.stringify({error: 'No charts found'});
    }

    var result = [];
    for (var i = 0; i < charts.length; i++) {
        var chart = charts[i];
        var chartInfo = {
            title: chart.title ? chart.title.textStr : 'Chart ' + i,
            series: []
        };

        for (var j = 0; j < chart.series.length; j++) {
            var s = chart.series[j];
            var seriesData = [];

            if (s.xData && s.xData.length > 0) {
                for (var k = 0; k < s.xData.length; k++) {
                    seriesData.push({
                        x: s.xData[k],
                        y: s.yData[k],
                        date: new Date(s.xData[k]).toISOString().split('T')[0]
                    });
                }
            } else if (s.data && s.data.length > 0) {
                seriesData = s.data.map(function(point) {
                    return {
                        x: point.x,
                        y: point.y,
                        date: point.x ? new Date(point.x).toISOString().split('T')[0] : null
                    };
                });
            }

            chartInfo.series.push({
                name: s.name,
                type: s.type,
                dataLength: seriesData.length,
                data: seriesData
            });
        }
        result.push(chartInfo);
    }
    return JSON.stringify(result);
})()
'''


# ==================== Chrome 自動化管理 ====================

def find_chrome_path() -> Optional[str]:
    """尋找 Chrome 可執行檔路徑"""
    for path in CHROME_PATHS:
        if Path(path).exists():
            return path
    return None


def is_chrome_debug_running(port: int = CDP_PORT) -> bool:
    """檢查 Chrome 調試端口是否已開啟"""
    import requests
    try:
        resp = requests.get(f'http://127.0.0.1:{port}/json', timeout=2)
        return resp.status_code == 200
    except Exception:
        return False


def start_chrome_debug(url: str, port: int = CDP_PORT) -> Optional[subprocess.Popen]:
    """
    自動啟動 Chrome 調試模式

    Returns
    -------
    subprocess.Popen or None
        Chrome 進程句柄，失敗返回 None
    """
    chrome_path = find_chrome_path()
    if not chrome_path:
        print("[Error] 找不到 Chrome，請確認已安裝 Google Chrome")
        return None

    # 用戶數據目錄（避免與現有 Chrome 衝突）
    user_data_dir = Path.home() / ".chrome-cdp-profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        chrome_path,
        f"--remote-debugging-port={port}",
        "--remote-allow-origins=*",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        url
    ]

    print(f"[Chrome] 啟動 Chrome (port {port})...")

    # Windows 使用 CREATE_NEW_PROCESS_GROUP 避免繼承控制台
    if sys.platform == 'win32':
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    return proc


def wait_for_chrome_ready(port: int = CDP_PORT, timeout: int = 30) -> bool:
    """等待 Chrome 調試端口準備好"""
    import requests

    start = time.time()
    while time.time() - start < timeout:
        try:
            resp = requests.get(f'http://127.0.0.1:{port}/json', timeout=2)
            if resp.status_code == 200 and len(resp.json()) > 0:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def close_chrome_debug(proc: subprocess.Popen):
    """關閉 Chrome 進程"""
    if proc:
        try:
            proc.terminate()
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


def navigate_to_url(port: int, url: str) -> bool:
    """導航到指定 URL"""
    import requests
    import websocket

    try:
        # 獲取當前頁面
        resp = requests.get(f'http://127.0.0.1:{port}/json', timeout=5)
        pages = resp.json()
        if not pages:
            return False

        ws_url = pages[0].get('webSocketDebuggerUrl')
        if not ws_url:
            return False

        # 導航
        ws = websocket.create_connection(ws_url, timeout=30)
        cmd = {
            "id": 1,
            "method": "Page.navigate",
            "params": {"url": url}
        }
        ws.send(json.dumps(cmd))
        ws.recv()
        ws.close()
        return True

    except Exception as e:
        print(f"[CDP] 導航失敗: {e}")
        return False


# ==================== CDP 數據抓取 ====================

def get_cdp_ws_url(port: int = CDP_PORT, url_keyword: str = 'macromicro') -> Optional[str]:
    """取得目標頁面的 WebSocket URL"""
    import requests

    try:
        resp = requests.get(f'http://127.0.0.1:{port}/json', timeout=5)
        pages = resp.json()

        for page in pages:
            if url_keyword.lower() in page.get('url', '').lower():
                return page.get('webSocketDebuggerUrl')

        return pages[0].get('webSocketDebuggerUrl') if pages else None

    except Exception as e:
        print(f"[CDP] 無法連接到 Chrome (port {port}): {e}")
        return None


def cdp_execute_js(ws_url: str, js_code: str, timeout: int = 30) -> Any:
    """透過 CDP 執行 JavaScript"""
    import websocket

    ws = websocket.create_connection(ws_url, timeout=timeout)

    cmd = {
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": js_code,
            "returnByValue": True
        }
    }
    ws.send(json.dumps(cmd))
    result = json.loads(ws.recv())
    ws.close()

    return result


def fetch_inventory_via_cdp(
    url: str,
    source_name: str,
    port: int = CDP_PORT,
    wait_seconds: int = PAGE_LOAD_WAIT_SECONDS,
    chrome_proc: Optional[subprocess.Popen] = None,
    we_started_chrome: bool = False
) -> Dict[str, Any]:
    """
    透過 CDP 抓取庫存數據

    Parameters
    ----------
    url : str
        MacroMicro 頁面 URL
    source_name : str
        數據源名稱 (SHFE / COMEX)
    port : int
        CDP 端口
    wait_seconds : int
        等待頁面載入秒數
    chrome_proc : subprocess.Popen
        已存在的 Chrome 進程（可選）
    we_started_chrome : bool
        是否由本函數啟動 Chrome

    Returns
    -------
    Dict[str, Any]
        包含圖表數據的字典
    """
    try:
        # 檢查是否已有 Chrome 調試實例
        if not is_chrome_debug_running(port):
            if chrome_proc is None:
                # 啟動 Chrome
                chrome_proc = start_chrome_debug(url, port)
                if not chrome_proc:
                    raise RuntimeError("無法啟動 Chrome")
                we_started_chrome = True

                # 等待 Chrome 準備好
                print("[CDP] 等待 Chrome 啟動...")
                if not wait_for_chrome_ready(port, timeout=30):
                    raise RuntimeError("Chrome 啟動超時")
        else:
            # 已有 Chrome，導航到目標 URL
            print(f"[CDP] 發現已運行的 Chrome，導航到 {source_name} 頁面...")
            navigate_to_url(port, url)

        # 等待頁面載入（Highcharts 渲染需要時間）
        print(f"[CDP] 等待 {source_name} 頁面載入 ({wait_seconds} 秒)...")
        time.sleep(wait_seconds)

        # 連接並提取數據
        ws_url = get_cdp_ws_url(port)
        if not ws_url:
            raise RuntimeError("無法取得 WebSocket URL")

        print(f"[CDP] 提取 {source_name} Highcharts 數據...")
        result = cdp_execute_js(ws_url, EXTRACT_HIGHCHARTS_JS)

        value = result.get('result', {}).get('result', {}).get('value')
        if not value:
            raise ValueError(f"無法取得數據: {result}")

        data = json.loads(value)

        if isinstance(data, dict) and 'error' in data:
            raise ValueError(f"提取失敗: {data['error']}")

        print(f"[CDP] 成功提取 {source_name} 數據，共 {len(data)} 個圖表!")

        return {
            "source": f"MacroMicro (CDP Auto) - {source_name}",
            "url": url,
            "charts": data,
            "fetched_at": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"[CDP] {source_name} 數據抓取失敗: {e}")
        raise


def fetch_all_inventories(
    fetch_shfe: bool = True,
    fetch_comex: bool = True,
    port: int = CDP_PORT,
    wait_seconds: int = PAGE_LOAD_WAIT_SECONDS
) -> Dict[str, Dict[str, Any]]:
    """
    全自動抓取所有庫存數據

    Parameters
    ----------
    fetch_shfe : bool
        是否抓取 SHFE 數據
    fetch_comex : bool
        是否抓取 COMEX 數據

    Returns
    -------
    Dict[str, Dict[str, Any]]
        包含各數據源數據的字典
    """
    results = {}
    chrome_proc = None
    we_started_chrome = False

    try:
        # 確定第一個要抓取的 URL
        first_url = SHFE_INVENTORY_URL if fetch_shfe else COMEX_INVENTORY_URL

        # 檢查是否需要啟動 Chrome
        if not is_chrome_debug_running(port):
            chrome_proc = start_chrome_debug(first_url, port)
            if not chrome_proc:
                raise RuntimeError("無法啟動 Chrome")
            we_started_chrome = True

            print("[CDP] 等待 Chrome 啟動...")
            if not wait_for_chrome_ready(port, timeout=30):
                raise RuntimeError("Chrome 啟動超時")

        # 抓取 SHFE
        if fetch_shfe:
            try:
                results['shfe'] = fetch_inventory_via_cdp(
                    url=SHFE_INVENTORY_URL,
                    source_name="SHFE",
                    port=port,
                    wait_seconds=wait_seconds,
                    chrome_proc=chrome_proc,
                    we_started_chrome=we_started_chrome
                )
            except Exception as e:
                print(f"[Warning] SHFE 數據抓取失敗: {e}")
                results['shfe'] = None

        # 抓取 COMEX
        if fetch_comex:
            try:
                # 導航到 COMEX 頁面
                if fetch_shfe:
                    print("[CDP] 導航到 COMEX 頁面...")
                    navigate_to_url(port, COMEX_INVENTORY_URL)
                    time.sleep(wait_seconds)  # 等待新頁面載入

                results['comex'] = fetch_inventory_via_cdp(
                    url=COMEX_INVENTORY_URL,
                    source_name="COMEX",
                    port=port,
                    wait_seconds=wait_seconds if not fetch_shfe else 0,  # 如果已經等過了就不用再等
                    chrome_proc=chrome_proc,
                    we_started_chrome=we_started_chrome
                )
            except Exception as e:
                print(f"[Warning] COMEX 數據抓取失敗: {e}")
                results['comex'] = None

        return results

    finally:
        # 關閉我們啟動的 Chrome
        if we_started_chrome and chrome_proc:
            print("[Chrome] 關閉 Chrome...")
            close_chrome_debug(chrome_proc)


# ==================== 價格數據抓取 ====================

def fetch_copper_price(
    start_date: str = "2010-01-01",
    end_date: Optional[str] = None,
    ticker: str = COPPER_TICKER
) -> pd.DataFrame:
    """
    從 Yahoo Finance 抓取銅期貨價格

    Parameters
    ----------
    start_date : str
        起始日期 (YYYY-MM-DD)
    end_date : str, optional
        結束日期，預設為今天
    ticker : str
        Yahoo Finance ticker

    Returns
    -------
    pd.DataFrame
        columns: date, close, high, low, open, volume
    """
    if not HAS_YFINANCE:
        raise RuntimeError("yfinance 未安裝，請執行: pip install yfinance")

    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    print(f"[yfinance] 抓取 {ticker} 價格 ({start_date} ~ {end_date})...")

    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    if data.empty:
        raise ValueError(f"無法取得 {ticker} 數據")

    # 標準化欄位名稱
    df = data.reset_index()
    df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]

    # 確保有 date 欄位
    if 'date' not in df.columns:
        df = df.rename(columns={df.columns[0]: 'date'})

    df['date'] = pd.to_datetime(df['date'])

    print(f"[yfinance] 取得 {len(df)} 筆價格數據")
    print(f"[yfinance] 時間範圍: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")

    return df


# ==================== 數據處理 ====================

def extract_inventory_data(chart_data: Dict[str, Any], source_name: str) -> pd.DataFrame:
    """從圖表數據中提取庫存時間序列"""
    all_rows = []

    keywords = {
        'shfe': ['shfe', 'shanghai', '上海', 'warehouse stock'],
        'comex': ['comex', 'warehouse stock']
    }

    source_keywords = keywords.get(source_name.lower(), [source_name.lower()])

    for chart in chart_data.get('charts', []):
        for series in chart.get('series', []):
            series_name = series.get('name', 'Unknown')

            # 尋找相關 series
            if any(kw in series_name.lower() for kw in source_keywords):
                for point in series.get('data', []):
                    if point.get('y') is not None and point.get('date'):
                        all_rows.append({
                            'date': point['date'],
                            'inventory_tonnes': point['y'],
                            'series_name': series_name
                        })

    if not all_rows:
        # 如果沒找到特定關鍵字，取第一個有數據的 series
        for chart in chart_data.get('charts', []):
            for series in chart.get('series', []):
                if series.get('dataLength', 0) > 0:
                    for point in series.get('data', []):
                        if point.get('y') is not None and point.get('date'):
                            all_rows.append({
                                'date': point['date'],
                                'inventory_tonnes': point['y'],
                                'series_name': series.get('name', 'Unknown')
                            })
                    break
            if all_rows:
                break

    if not all_rows:
        raise ValueError(f"未能提取到任何 {source_name} 數據")

    df = pd.DataFrame(all_rows)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').drop_duplicates(subset=['date'], keep='last')
    df = df.reset_index(drop=True)

    print(f"[Data] 提取到 {len(df)} 筆 {source_name} 庫存數據")
    print(f"[Data] 時間範圍: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")

    return df


# ==================== 快取管理 ====================

class CopperDataCache:
    """銅數據快取管理"""

    def __init__(self, cache_dir: str = 'cache', max_age_hours: int = CACHE_MAX_AGE_HOURS):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.max_age = timedelta(hours=max_age_hours)

    def _cache_path(self, source: str) -> Path:
        return self.cache_dir / f"{source}_cache.json"

    def _csv_path(self, source: str) -> Path:
        return self.cache_dir / f"{source}.csv"

    def is_fresh(self, source: str) -> bool:
        cache_file = self._csv_path(source)
        if not cache_file.exists():
            return False
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        return (datetime.now() - mtime) < self.max_age

    def get_dataframe(self, source: str) -> Optional[pd.DataFrame]:
        if not self.is_fresh(source):
            return None
        try:
            df = pd.read_csv(self._csv_path(source))
            df['date'] = pd.to_datetime(df['date'])
            return df
        except Exception:
            return None

    def save_inventory(self, source: str, raw_data: Dict, df: pd.DataFrame):
        # 保存原始 JSON
        with open(self._cache_path(source), 'w', encoding='utf-8') as f:
            json.dump(raw_data, f, ensure_ascii=False, indent=2)

        # 保存 CSV
        df.to_csv(self._csv_path(source), index=False)
        print(f"[Cache] 已儲存 {source} 到 {self._csv_path(source)}")

    def save_price(self, df: pd.DataFrame):
        df.to_csv(self._csv_path('copper_price'), index=False)
        print(f"[Cache] 已儲存價格到 {self._csv_path('copper_price')}")


# ==================== 主要 API ====================

def fetch_copper_data(
    cache_dir: str = "cache",
    force_refresh: bool = False,
    fetch_shfe: bool = True,
    fetch_comex: bool = True,
    fetch_price: bool = True,
    price_start_date: str = "2010-01-01",
    cdp_port: int = CDP_PORT
) -> Dict[str, pd.DataFrame]:
    """
    獲取所有銅相關數據（全自動）

    Parameters
    ----------
    cache_dir : str
        快取目錄
    force_refresh : bool
        是否強制重新抓取
    fetch_shfe : bool
        是否抓取 SHFE 庫存
    fetch_comex : bool
        是否抓取 COMEX 庫存
    fetch_price : bool
        是否抓取銅價
    price_start_date : str
        價格數據起始日期
    cdp_port : int
        CDP 調試端口

    Returns
    -------
    Dict[str, pd.DataFrame]
        包含 'shfe_inventory', 'comex_inventory', 'copper_price' 的字典
    """
    cache = CopperDataCache(cache_dir)
    results = {}

    # 檢查快取
    need_fetch_shfe = fetch_shfe
    need_fetch_comex = fetch_comex
    need_fetch_price = fetch_price

    if not force_refresh:
        if fetch_shfe:
            cached = cache.get_dataframe('shfe_inventory')
            if cached is not None:
                print("[Cache] 使用 SHFE 快取數據")
                results['shfe_inventory'] = cached
                need_fetch_shfe = False

        if fetch_comex:
            cached = cache.get_dataframe('comex_inventory')
            if cached is not None:
                print("[Cache] 使用 COMEX 快取數據")
                results['comex_inventory'] = cached
                need_fetch_comex = False

        if fetch_price:
            cached = cache.get_dataframe('copper_price')
            if cached is not None:
                print("[Cache] 使用價格快取數據")
                results['copper_price'] = cached
                need_fetch_price = False

    # 抓取庫存數據
    if need_fetch_shfe or need_fetch_comex:
        print("[Fetch] 開始全自動抓取庫存數據...")
        inventory_data = fetch_all_inventories(
            fetch_shfe=need_fetch_shfe,
            fetch_comex=need_fetch_comex,
            port=cdp_port
        )

        if need_fetch_shfe and inventory_data.get('shfe'):
            df = extract_inventory_data(inventory_data['shfe'], 'SHFE')
            cache.save_inventory('shfe_inventory', inventory_data['shfe'], df)
            results['shfe_inventory'] = df

        if need_fetch_comex and inventory_data.get('comex'):
            df = extract_inventory_data(inventory_data['comex'], 'COMEX')
            cache.save_inventory('comex_inventory', inventory_data['comex'], df)
            results['comex_inventory'] = df

    # 抓取價格數據
    if need_fetch_price:
        try:
            price_df = fetch_copper_price(start_date=price_start_date)
            cache.save_price(price_df)
            results['copper_price'] = price_df
        except Exception as e:
            print(f"[Warning] 價格數據抓取失敗: {e}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="全自動抓取銅庫存與價格數據"
    )
    parser.add_argument(
        "--force-refresh", "-f",
        action="store_true",
        help="強制重新抓取，忽略快取"
    )
    parser.add_argument(
        "--source", "-s",
        type=str,
        choices=['all', 'shfe', 'comex', 'price'],
        default='all',
        help="要抓取的數據源 (預設: all)"
    )
    parser.add_argument(
        "--cache-dir",
        type=str,
        default="cache",
        help="快取目錄 (預設: cache)"
    )
    parser.add_argument(
        "--price-start",
        type=str,
        default="2010-01-01",
        help="價格數據起始日期 (預設: 2010-01-01)"
    )

    args = parser.parse_args()

    # 決定要抓取哪些數據
    fetch_shfe = args.source in ['all', 'shfe']
    fetch_comex = args.source in ['all', 'comex']
    fetch_price = args.source in ['all', 'price']

    try:
        data = fetch_copper_data(
            cache_dir=args.cache_dir,
            force_refresh=args.force_refresh,
            fetch_shfe=fetch_shfe,
            fetch_comex=fetch_comex,
            fetch_price=fetch_price,
            price_start_date=args.price_start
        )

        # 顯示摘要
        print("\n" + "=" * 60)
        print("銅數據摘要")
        print("=" * 60)

        if 'shfe_inventory' in data:
            df = data['shfe_inventory']
            print(f"\n[SHFE 庫存]")
            print(f"  數據筆數: {len(df)}")
            print(f"  時間範圍: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")
            print(f"  最新庫存: {df['inventory_tonnes'].iloc[-1]:,.0f} 噸")

        if 'comex_inventory' in data:
            df = data['comex_inventory']
            print(f"\n[COMEX 庫存]")
            print(f"  數據筆數: {len(df)}")
            print(f"  時間範圍: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")
            print(f"  最新庫存: {df['inventory_tonnes'].iloc[-1]:,.0f} 噸")

        if 'copper_price' in data:
            df = data['copper_price']
            print(f"\n[銅期貨價格 (HG=F)]")
            print(f"  數據筆數: {len(df)}")
            print(f"  時間範圍: {df['date'].min().strftime('%Y-%m-%d')} ~ {df['date'].max().strftime('%Y-%m-%d')}")
            print(f"  最新價格: {df['close'].iloc[-1]:.4f} USD/lb")

        return 0

    except Exception as e:
        print(f"\n[Error] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
