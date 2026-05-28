#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
數據抓取工具

抓取銅價、股市代理、中國10Y殖利率等數據。

數據來源：
- 銅價：Yahoo Finance (HG=F)
- 全球股市市值：Yahoo Finance (VT)
- 中國10Y殖利率：MacroMicro (https://en.macromicro.me/charts/133362/China-10Year-Government-Bond-Yield)
"""

import json
import random
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List

import pandas as pd
import yfinance as yf

# 快取目錄
CACHE_DIR = Path(__file__).parent.parent / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# 單位換算係數
POUNDS_PER_TON = 2204.62262

# MacroMicro 配置
MACROMICRO_CHINA_10Y_URL = "https://en.macromicro.me/charts/133362/China-10Year-Government-Bond-Yield"
MACROMICRO_CHART_WAIT_SECONDS = 35
MACROMICRO_MAX_RETRIES = 3

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
]

# Highcharts 數據提取 JavaScript
EXTRACT_HIGHCHARTS_JS = '''
// 檢查 Highcharts 是否存在
if (typeof Highcharts === 'undefined') {
    return {error: 'Highcharts not loaded', retry: true};
}

// 獲取所有有效的圖表
var charts = Highcharts.charts.filter(c => c !== undefined && c !== null);
if (charts.length === 0) {
    return {error: 'No charts found', totalCharts: Highcharts.charts.length, retry: true};
}

// 提取每個圖表的數據
var result = [];
for (var i = 0; i < charts.length; i++) {
    var chart = charts[i];
    var chartInfo = {
        title: chart.title ? chart.title.textStr : 'Chart ' + i,
        series: []
    };

    for (var j = 0; j < chart.series.length; j++) {
        var s = chart.series[j];
        var seriesData = {
            name: s.name,
            type: s.type,
            dataLength: s.data.length,
            data: s.data.map(function(point) {
                return {
                    x: point.x,
                    y: point.y,
                    date: point.x ? new Date(point.x).toISOString().split('T')[0] : null
                };
            })
        };
        chartInfo.series.push(seriesData);
    }
    result.push(chartInfo);
}

return result;
'''


def fetch_copper(
    series: str = "HG=F",
    start_date: str = "2020-01-01",
    end_date: Optional[str] = None,
    freq: str = "1mo",
    convert_to_ton: bool = True,
    use_cache: bool = True,
    cache_hours: int = 12
) -> pd.Series:
    """
    抓取銅價數據

    Parameters
    ----------
    series : str
        銅價序列代碼（預設 HG=F）
    start_date : str
        起始日期
    end_date : str
        結束日期（預設今天）
    freq : str
        頻率（1mo, 1wk, 1d）
    convert_to_ton : bool
        是否轉換為 USD/ton（預設 True）
    use_cache : bool
        是否使用快取
    cache_hours : int
        快取有效時間（小時）

    Returns
    -------
    pd.Series
        銅價時間序列
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    cache_file = CACHE_DIR / f"copper_{series}_{start_date}_{end_date}_{freq}.json"

    # 檢查快取
    if use_cache and cache_file.exists():
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if datetime.now() - mtime < timedelta(hours=cache_hours):
            with open(cache_file, "r") as f:
                data = json.load(f)
            series_data = pd.Series(data["values"], index=pd.to_datetime(data["index"]))
            series_data.name = "copper"
            return series_data

    # 抓取數據
    print(f"正在抓取銅價數據: {series}")
    df = yf.download(series, start=start_date, end=end_date, interval=freq, progress=False)

    if df.empty:
        raise ValueError(f"無法取得 {series} 的數據")

    # 取收盤價
    copper = df["Close"].squeeze()

    # 單位換算
    if convert_to_ton and series == "HG=F":
        copper = copper * POUNDS_PER_TON
        print(f"已將 {series} 從 USD/lb 轉換為 USD/ton")

    copper.name = "copper"

    # 儲存快取
    cache_data = {
        "index": copper.index.strftime("%Y-%m-%d").tolist(),
        "values": copper.tolist(),
        "series": series,
        "converted_to_ton": convert_to_ton
    }
    with open(cache_file, "w") as f:
        json.dump(cache_data, f)

    return copper


def fetch_equity(
    series: str = "ACWI",
    start_date: str = "2020-01-01",
    end_date: Optional[str] = None,
    freq: str = "1mo",
    use_cache: bool = True,
    cache_hours: int = 12
) -> pd.Series:
    """
    抓取股市代理數據

    Parameters
    ----------
    series : str
        股市序列代碼（預設 ACWI）
    start_date : str
        起始日期
    end_date : str
        結束日期
    freq : str
        頻率
    use_cache : bool
        是否使用快取
    cache_hours : int
        快取有效時間

    Returns
    -------
    pd.Series
        股市時間序列
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    cache_file = CACHE_DIR / f"equity_{series}_{start_date}_{end_date}_{freq}.json"

    # 檢查快取
    if use_cache and cache_file.exists():
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if datetime.now() - mtime < timedelta(hours=cache_hours):
            with open(cache_file, "r") as f:
                data = json.load(f)
            series_data = pd.Series(data["values"], index=pd.to_datetime(data["index"]))
            series_data.name = "equity"
            return series_data

    # 抓取數據
    print(f"正在抓取股市數據: {series}")
    df = yf.download(series, start=start_date, end=end_date, interval=freq, progress=False)

    if df.empty:
        raise ValueError(f"無法取得 {series} 的數據")

    equity = df["Close"].squeeze()
    equity.name = "equity"

    # 儲存快取
    cache_data = {
        "index": equity.index.strftime("%Y-%m-%d").tolist(),
        "values": equity.tolist(),
        "series": series
    }
    with open(cache_file, "w") as f:
        json.dump(cache_data, f)

    return equity


def fetch_world_market_cap(
    start_date: str = "2015-01-01",
    end_date: Optional[str] = None,
    freq: str = "1mo",
    use_cache: bool = True,
    cache_hours: int = 12
) -> pd.Series:
    """
    抓取全球股市市值代理數據

    使用 VT (Vanguard Total World Stock ETF) 作為全球市值代理

    Parameters
    ----------
    start_date : str
        起始日期
    end_date : str
        結束日期
    freq : str
        頻率
    use_cache : bool
        是否使用快取
    cache_hours : int
        快取有效時間

    Returns
    -------
    pd.Series
        全球市值代理序列（單位：兆美元）
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    cache_file = CACHE_DIR / f"world_mktcap_{start_date}_{end_date}_{freq}.json"

    # 檢查快取
    if use_cache and cache_file.exists():
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if datetime.now() - mtime < timedelta(hours=cache_hours):
            with open(cache_file, "r") as f:
                data = json.load(f)
            series_data = pd.Series(data["values"], index=pd.to_datetime(data["index"]))
            series_data.name = "world_mktcap"
            return series_data

    # 抓取 VT 數據
    print(f"正在抓取全球股市市值代理數據: VT")
    df = yf.download("VT", start=start_date, end=end_date, interval=freq, progress=False)

    if df.empty:
        # 備用：使用 ACWI
        print("VT 數據不可用，改用 ACWI")
        df = yf.download("ACWI", start=start_date, end=end_date, interval=freq, progress=False)

    if df.empty:
        raise ValueError("無法取得全球市值代理數據")

    price = df["Close"].squeeze()

    # 將 ETF 價格轉換為估算市值（兆美元）
    # 基準：2024 年全球市值約 110 兆美元，對應 VT 約 110
    BASE_MKTCAP = 110  # 兆美元
    BASE_PRICE = 110   # VT 價格基準
    world_mktcap = price * (BASE_MKTCAP / BASE_PRICE)
    world_mktcap.name = "world_mktcap"

    # 儲存快取
    cache_data = {
        "index": world_mktcap.index.strftime("%Y-%m-%d").tolist(),
        "values": world_mktcap.tolist(),
        "source": "VT proxy"
    }
    with open(cache_file, "w") as f:
        json.dump(cache_data, f)

    return world_mktcap


def _fetch_china_yield_macromicro() -> Optional[pd.Series]:
    """
    使用 Selenium 從 MacroMicro 抓取中國10Y殖利率歷史數據

    數據來源：https://en.macromicro.me/charts/133362/China-10Year-Government-Bond-Yield

    Returns
    -------
    pd.Series or None
        殖利率時間序列，或 None 如果失敗
    """
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print("Selenium 未安裝，請執行: pip install selenium webdriver-manager")
        return None

    driver = None

    try:
        # 1. 隨機延遲（模擬人類）
        delay = random.uniform(1.0, 2.0)
        print(f"請求前延遲 {delay:.2f} 秒...")
        time.sleep(delay)

        # 2. 配置 Chrome
        chrome_options = Options()
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(120)

        # 3. 載入頁面
        print(f"正在抓取中國10Y殖利率: {MACROMICRO_CHINA_10Y_URL}")
        driver.get(MACROMICRO_CHINA_10Y_URL)

        # 4. 初步等待頁面載入
        print("等待頁面載入...")
        time.sleep(5)

        # 5. 滾動到頁面頂部
        driver.execute_script('window.scrollTo(0, 0);')
        time.sleep(3)

        # 6. 等待圖表區域出現
        print("等待圖表區域...")
        chart_selectors = [
            '.chart-area',
            '.chart-wrapper',
            '.mm-chart-wrapper',
            '#chartArea',
            '.highcharts-container',
            '[data-highcharts-chart]'
        ]

        for selector in chart_selectors:
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                print(f"找到圖表區域: {selector}")
                break
            except:
                continue

        # 7. 🔴 長時間等待 Highcharts 渲染完成
        print(f"等待圖表完全渲染 ({MACROMICRO_CHART_WAIT_SECONDS}秒)...")
        time.sleep(MACROMICRO_CHART_WAIT_SECONDS)

        # 8. 確保頁面穩定
        driver.execute_script('window.scrollTo(0, 0);')
        time.sleep(2)

        # 9. 執行 JavaScript 提取數據（帶重試）
        print("從 Highcharts 圖表中提取數據...")
        chart_data = None

        for retry in range(MACROMICRO_MAX_RETRIES):
            chart_data = driver.execute_script(EXTRACT_HIGHCHARTS_JS)

            # 檢查是否需要重試
            if isinstance(chart_data, dict) and chart_data.get('retry'):
                print(f"重試 {retry + 1}/{MACROMICRO_MAX_RETRIES}，等待 10 秒...")
                time.sleep(10)
                driver.execute_script(
                    'window.scrollTo(0, 100); '
                    'setTimeout(() => window.scrollTo(0, 0), 500);'
                )
                continue
            else:
                break

        # 10. 檢查結果
        if isinstance(chart_data, dict) and 'error' in chart_data:
            print(f"提取圖表數據失敗: {chart_data['error']}")
            return None

        if not chart_data:
            print("未找到圖表數據")
            return None

        print(f"成功獲取 {len(chart_data)} 個圖表的數據!")

        # 11. 找到中國10Y殖利率 series
        # 可能的關鍵字：'China', '10-Year', 'Yield', '中國'
        target_series = None
        for chart in chart_data:
            for series in chart.get('series', []):
                series_name = series.get('name', '')
                # 尋找包含 China 或 Yield 或 10 的 series
                if any(kw in series_name.lower() for kw in ['china', 'yield', '10', '中國', '殖利率']):
                    if series.get('dataLength', 0) > 0:
                        target_series = series
                        print(f"找到目標 Series: {series_name}, 數據點: {series['dataLength']}")
                        break
            if target_series:
                break

        # 如果沒找到，使用第一個有數據的 series
        if not target_series:
            for chart in chart_data:
                for series in chart.get('series', []):
                    if series.get('dataLength', 0) > 0:
                        target_series = series
                        print(f"使用第一個 Series: {series.get('name')}, 數據點: {series['dataLength']}")
                        break
                if target_series:
                    break

        if not target_series:
            print("未找到有效的數據 series")
            # 列出所有 series 供除錯
            all_series = [
                f"{s.get('name')} ({s.get('dataLength')} points)"
                for c in chart_data
                for s in c.get('series', [])
            ]
            print(f"可用 series: {all_series}")
            return None

        # 12. 轉換為 Pandas Series
        points = target_series['data']
        df = pd.DataFrame(points)
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        df = df.sort_index()
        df = df.dropna(subset=['y'])

        result = df['y']
        result.name = "cny10y"

        print(f"成功獲取 {len(result)} 筆中國10Y殖利率數據")
        print(f"  日期範圍: {result.index.min()} ~ {result.index.max()}")
        print(f"  數值範圍: {result.min():.2f}% ~ {result.max():.2f}%")

        return result

    except Exception as e:
        print(f"MacroMicro 爬取失敗: {e}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        if driver:
            driver.quit()
            print("瀏覽器已關閉")


def fetch_china_10y_yield(
    start_date: str = "2015-01-01",
    end_date: Optional[str] = None,
    use_cache: bool = True,
    cache_hours: int = 12
) -> pd.Series:
    """
    抓取中國10Y殖利率數據

    數據來源：MacroMicro (https://en.macromicro.me/charts/133362/China-10Year-Government-Bond-Yield)

    Parameters
    ----------
    start_date : str
        起始日期
    end_date : str
        結束日期
    use_cache : bool
        是否使用快取
    cache_hours : int
        快取有效時間

    Returns
    -------
    pd.Series
        中國10Y殖利率時間序列
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    cache_file = CACHE_DIR / f"china_10y_macromicro.json"

    # 檢查快取
    if use_cache and cache_file.exists():
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if datetime.now() - mtime < timedelta(hours=cache_hours):
            print(f"使用快取的中國10Y殖利率數據 (快取時間: {mtime.strftime('%Y-%m-%d %H:%M')})")
            with open(cache_file, "r") as f:
                data = json.load(f)
            series_data = pd.Series(data["values"], index=pd.to_datetime(data["index"]))
            series_data.name = "cny10y"

            # 過濾日期範圍
            mask = (series_data.index >= start_date) & (series_data.index <= end_date)
            return series_data[mask]

    # 從 MacroMicro 抓取
    yield_data = _fetch_china_yield_macromicro()

    if yield_data is not None and len(yield_data) > 0:
        # 儲存快取
        cache_data = {
            "index": yield_data.index.strftime("%Y-%m-%d").tolist(),
            "values": yield_data.tolist(),
            "source": "MacroMicro",
            "url": MACROMICRO_CHINA_10Y_URL,
            "fetched_at": datetime.now().isoformat()
        }
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        print(f"已儲存快取: {cache_file}")

        # 過濾日期範圍
        mask = (yield_data.index >= start_date) & (yield_data.index <= end_date)
        return yield_data[mask]

    # 如果爬取失敗，嘗試使用舊的快取（即使過期）
    if cache_file.exists():
        print("爬取失敗，使用過期的快取數據")
        with open(cache_file, "r") as f:
            data = json.load(f)
        series_data = pd.Series(data["values"], index=pd.to_datetime(data["index"]))
        series_data.name = "cny10y"
        mask = (series_data.index >= start_date) & (series_data.index <= end_date)
        return series_data[mask]

    # 最後手段：拋出錯誤
    raise ValueError(
        "無法取得中國10Y殖利率數據。\n"
        "請確保：\n"
        "1. 已安裝 selenium: pip install selenium webdriver-manager\n"
        "2. 網路連接正常\n"
        "3. Chrome 瀏覽器已安裝"
    )


def align_monthly(data_dict: Dict[str, pd.Series]) -> pd.DataFrame:
    """
    將多條序列對齊到月底

    Parameters
    ----------
    data_dict : dict
        {"copper": series1, "equity": series2, "cny10y": series3}

    Returns
    -------
    pd.DataFrame
        對齊後的 DataFrame
    """
    df = pd.DataFrame(data_dict)

    # 確保索引為日期
    df.index = pd.to_datetime(df.index)

    # 重採樣到月底
    df = df.resample('ME').last()

    # 前向填補（處理少量缺值）
    df = df.ffill()

    # 丟掉仍有缺值的行
    df = df.dropna()

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="數據抓取工具")
    parser.add_argument("--series", type=str, required=True, help="序列代碼（逗號分隔）")
    parser.add_argument("--start", type=str, default="2015-01-01", help="起始日期")
    parser.add_argument("--end", type=str, default=None, help="結束日期")
    parser.add_argument("--freq", type=str, default="1mo", help="頻率")
    parser.add_argument("--no-cache", action="store_true", help="不使用快取")

    args = parser.parse_args()

    series_list = args.series.split(",")

    for s in series_list:
        s = s.strip()
        if s in ["HG=F"]:
            data = fetch_copper(s, args.start, args.end, args.freq, use_cache=not args.no_cache)
        elif s in ["ACWI", "VT", "URTH"]:
            data = fetch_equity(s, args.start, args.end, args.freq, use_cache=not args.no_cache)
        elif s == "cny10y":
            data = fetch_china_10y_yield(args.start, args.end, use_cache=not args.no_cache)
        else:
            print(f"未知序列: {s}")
            continue

        print(f"\n{s}:")
        print(data.tail())
