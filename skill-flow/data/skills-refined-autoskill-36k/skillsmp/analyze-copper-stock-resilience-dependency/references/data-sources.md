# 數據來源與爬蟲說明

## 數據來源總覽

| 數據 | 原始來源（封閉） | 公開替代 | 取得方式 |
|------|------------------|----------|----------|
| 銅期貨價格 | LME Copper | COMEX Copper (HG=F) | Yahoo Finance (yfinance) |
| 全球股市韌性 | Bloomberg World Mkt Cap | ACWI / VT | Yahoo Finance (yfinance) |
| 中國10Y殖利率 | Bloomberg Generic Yield | TradingEconomics | Selenium 爬蟲 |

---

## 1. 銅期貨價格 (COMEX Copper)

### 來源

**Yahoo Finance - HG=F**

```python
import yfinance as yf

# 抓取 COMEX Copper futures
copper = yf.download("HG=F", start="2020-01-01", end="2026-01-20", interval="1mo")
```

### 重要：單位換算

HG=F 報價單位為 **USD/lb（美元/磅）**，需轉換為 **USD/ton（美元/噸）**：

```python
# 換算係數：1 噸 = 2204.62262 磅
POUNDS_PER_TON = 2204.62262

copper_usd_per_ton = copper["Close"] * POUNDS_PER_TON
```

**對照範例：**
- HG=F = $4.50/lb → $4.50 × 2204.62 = **$9,921/ton**
- HG=F = $5.90/lb → $5.90 × 2204.62 = **$13,007/ton**

### 注意事項

- HG=F 為連續合約，可能有換月跳空
- 建議使用月底收盤價
- 數據延遲約 15 分鐘

---

## 2. 全球股市韌性代理 (ACWI)

### 來源

**Yahoo Finance - ACWI / VT**

```python
import yfinance as yf

# ACWI: iShares MSCI All Country World Index ETF
equity = yf.download("ACWI", start="2020-01-01", end="2026-01-20", interval="1mo")

# 或使用 VT: Vanguard Total World Stock ETF
# equity = yf.download("VT", start="2020-01-01", end="2026-01-20", interval="1mo")
```

### 可用代理比較

| 代碼 | 名稱 | 涵蓋範圍 | 費用率 |
|------|------|----------|--------|
| ACWI | iShares MSCI ACWI ETF | 全球已開發 + 新興 | 0.32% |
| VT | Vanguard Total World Stock | 全球 | 0.07% |
| URTH | iShares MSCI World ETF | 已開發市場 | 0.24% |

**建議使用 ACWI**，涵蓋範圍最接近「全球股市市值」概念。

### 與彭博全球市值的差異

- 彭博數據為總市值（market cap）
- ACWI 為指數價格（price return）
- 兩者高度相關，但非完全一致
- 本技能目的是捕捉「股市韌性」，價格指數已足夠

---

## 3. 中國10Y公債殖利率

### 來源

**TradingEconomics 爬蟲**

由於中國公債殖利率沒有方便的免費 API，需使用 Selenium 爬取。

### 爬蟲設計

遵循 `thoughts/shared/guide/design-human-like-crawler.md` 規範：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
中國10年期公債殖利率爬蟲
使用 Selenium 模擬瀏覽器行為
"""

import random
import time
from datetime import datetime
from typing import Optional, Dict

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# 配置
TARGET_URL = "https://tradingeconomics.com/china/government-bond-yield"

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
]


def get_china_10y_yield() -> Optional[Dict]:
    """抓取中國 10Y 殖利率"""
    driver = None

    try:
        # 隨機延遲
        time.sleep(random.uniform(1.0, 2.0))

        # Chrome 配置（防偵測）
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')

        # 啟動瀏覽器
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(60)

        # 載入頁面
        driver.get(TARGET_URL)

        # 等待表格載入
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "table"))
        )
        time.sleep(3)

        # 解析
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # 提取當前殖利率（需依實際頁面結構調整選擇器）
        yield_element = soup.select_one('#ticker')
        if yield_element:
            current_yield = float(yield_element.get_text(strip=True))
            return {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "china_10y_yield": current_yield,
                "source": "TradingEconomics"
            }

        return None

    except Exception as e:
        print(f"爬取失敗: {e}")
        return None

    finally:
        if driver:
            driver.quit()
```

### 快取策略

```python
import json
from pathlib import Path
from datetime import datetime, timedelta

CACHE_FILE = Path("data/cache/china_10y_yield.json")
CACHE_MAX_AGE_HOURS = 12

def get_cached_yield():
    """優先使用快取"""
    if CACHE_FILE.exists():
        mtime = datetime.fromtimestamp(CACHE_FILE.stat().st_mtime)
        if datetime.now() - mtime < timedelta(hours=CACHE_MAX_AGE_HOURS):
            with open(CACHE_FILE) as f:
                return json.load(f)

    # 快取過期，重新爬取
    data = get_china_10y_yield()
    if data:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(data, f)
    return data
```

### 替代來源

如果 TradingEconomics 不可用，可考慮：

| 來源 | 可行性 | 說明 |
|------|--------|------|
| Investing.com | 中 | 頁面結構複雜，反爬蟲較強 |
| MacroMicro | 中 | 需等待 Highcharts 渲染（見 macromicro-highcharts-crawler.md） |
| FRED | 低 | 無中國公債殖利率序列 |

---

## 4. 數據頻率與對齊

### 頻率選擇

本技能預設使用 **月頻（1mo）**：

- 對應研究報告圖中的 monthly candle
- 過濾短期雜訊
- 三條序列都能取得月頻數據

### 對齊方法

```python
import pandas as pd

def align_monthly(data_dict: dict) -> pd.DataFrame:
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
    df = df.resample('M').last()

    # 丟掉缺值（或用前值填補）
    df = df.dropna()

    return df
```

### 時區處理

- Yahoo Finance 預設為美東時間
- TradingEconomics 數據可能為 UTC
- 建議統一轉換為 UTC，再取月底

---

## 5. 依賴套件安裝

```bash
# 核心套件
pip install pandas numpy yfinance scipy statsmodels

# 爬蟲套件
pip install selenium webdriver-manager beautifulsoup4 lxml

# 視覺化（可選）
pip install matplotlib plotly
```

---

## 6. 完整資料抓取範例

```python
from scripts.fetch_data import fetch_copper, fetch_equity, fetch_china_yield
from scripts.copper_stock_analyzer import align_monthly

# 1. 抓取數據
copper = fetch_copper("HG=F", "2020-01-01", "2026-01-20")
equity = fetch_equity("ACWI", "2020-01-01", "2026-01-20")
cny10y = fetch_china_yield("2020-01-01", "2026-01-20")

# 2. 對齊
df = align_monthly({
    "copper": copper,
    "equity": equity,
    "cny10y": cny10y
})

print(f"資料筆數: {len(df)}")
print(df.tail())
```
