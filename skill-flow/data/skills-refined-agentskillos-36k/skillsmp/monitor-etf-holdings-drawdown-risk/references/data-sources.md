# 數據來源 (Data Sources)

本技能使用公開數據來源，部分需要 Selenium 模擬瀏覽器行為。

## ETF 持倉數據（主要來源）

### iShares Silver Trust (SLV)

**官網**：https://www.ishares.com/us/products/239855/ishares-silver-trust-fund

**持倉欄位**：
| 欄位 | 說明 | 單位 |
|------|------|------|
| Total Ounces of Silver | 總白銀盎司 | troy oz |
| NAV per Share | 每股淨值 | USD |
| Shares Outstanding | 流通股數 | shares |

**抓取方式**：Selenium + BeautifulSoup
- 需要等待 JavaScript 渲染完成
- 使用 `WebDriverWait` 等待持倉數據載入
- 典型選擇器：`div.fund-header-content`

**歷史數據**：
- iShares 官網提供近期數據
- 歷史數據可從 ETF.com 或 Bloomberg 取得
- 建議建立本地快取避免重複抓取

### Sprott Physical Silver Trust (PSLV)

**官網**：https://sprott.com/investment-strategies/physical-bullion-trusts/silver/

**持倉欄位**：
| 欄位 | 說明 | 單位 |
|------|------|------|
| Silver Held | 白銀持倉量 | troy oz |
| Net Asset Value | 淨資產值 | USD |
| Premium/Discount | 溢價/折價 | % |

**特點**：
- PSLV 為封閉式基金，溢價/折價資訊有額外參考價值
- 持倉存放於加拿大皇家鑄幣廠，非 LBMA 體系

### SPDR Gold Shares (GLD)

**官網**：https://www.spdrgoldshares.com/

**持倉欄位**：
| 欄位 | 說明 | 單位 |
|------|------|------|
| Gold Holdings | 黃金持倉量 | troy oz |
| Tonnes | 噸數 | metric tonnes |
| NAV | 淨資產值 | USD |

### Sprott Physical Gold Trust (PHYS)

**官網**：https://sprott.com/investment-strategies/physical-bullion-trusts/gold/

## 商品價格數據

### Yahoo Finance（yfinance 套件）

**存取方式**：Python `yfinance` 套件

```python
import yfinance as yf

def fetch_price_series(symbol, start_date, end_date):
    """從 Yahoo Finance 抓取價格數據"""
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start_date, end=end_date)
    return data["Close"]
```

**可用代碼**：

| 代碼 | 名稱 | 說明 | 狀態 |
|------|------|------|------|
| ~~XAGUSD=X~~ | ~~白銀現貨~~ | ~~Silver Spot~~ | ❌ 已失效 |
| ~~XAUUSD=X~~ | ~~黃金現貨~~ | ~~Gold Spot~~ | ❌ 已失效 |
| **SI=F** | **白銀期貨近月** | Silver Futures Front Month | ✅ 推薦使用 |
| **GC=F** | **黃金期貨近月** | Gold Futures Front Month | ✅ 推薦使用 |
| SLV | SLV ETF | iShares Silver Trust | ✅ 可用 |
| GLD | GLD ETF | SPDR Gold Shares | ✅ 可用 |

**注意事項**：
- **2026-01 更新**：Yahoo Finance 的現貨代碼（XAGUSD=X, XAUUSD=X）已失效，改用期貨代碼（SI=F, GC=F）
- 使用 `Close`（收盤價）
- 週末與假日無數據
- 期貨價格與現貨價格高度相關，適合用於背離分析

## 交叉驗證數據源

### COMEX 庫存

**來源**：CME Group
**URL**：https://www.cmegroup.com/clearing/operations-and-deliveries/nymex-delivery-notices.html

**庫存類型**：
| 類型 | 說明 |
|------|------|
| Registered | 已註冊可交割庫存 |
| Eligible | 符合交割規格但未註冊 |
| Total | Registered + Eligible |

**抓取方式**：
- 每日發布 stocks report
- PDF 或 Excel 格式
- 需要解析表格

**替代來源**：
- 第三方彙總網站（如 goldchartsrus.com）
- 付費數據服務

### LBMA 金庫存量

**來源**：London Bullion Market Association
**URL**：https://www.lbma.org.uk/prices-and-data/london-vault-holdings

**可用數據**：
- London Gold Holdings（每月）
- London Silver Holdings（每月）

**注意**：
- 僅為 LBMA 成員金庫彙總
- 不包含 ETF 專屬金庫
- 發布延遲約 2 週

### 期貨曲線結構

**判斷方式**：比較近月與遠月期貨價格

```python
def check_curve_structure(commodity):
    """
    檢查期貨曲線結構
    commodity: 'SI' for Silver, 'GC' for Gold
    """
    import yfinance as yf

    # 近月期貨
    front = yf.Ticker(f"{commodity}=F")
    front_price = front.history(period="1d")["Close"].iloc[-1]

    # 需要動態計算下個月合約代碼
    # 例如：SIH25.CME (2025年3月白銀期貨)

    # 簡化：使用價差判斷
    # backwardation: 近月 > 遠月
    # contango: 近月 < 遠月
```

### 零售溢價指標

**來源**：主要零售商網站
- APMEX: https://www.apmex.com/
- JM Bullion: https://www.jmbullion.com/
- SD Bullion: https://sdbullion.com/

**計算方式**：
```
Premium = (零售價格 - 現貨價格) / 現貨價格 × 100%
```

**正常水準**：
| 商品 | 正常溢價 | 緊張時溢價 |
|------|----------|------------|
| 銀幣 (American Eagle) | 8-12% | 20-50% |
| 銀條 (1 oz bar) | 3-5% | 10-20% |
| 金幣 (American Eagle) | 5-8% | 10-15% |
| 金條 (1 oz bar) | 2-4% | 5-10% |

## 反偵測策略（Selenium 爬蟲）

### User-Agent 輪換

```python
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
]
```

### Chrome 選項配置

```python
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
```

### 隨機延遲

```python
import random
import time

# 請求前隨機延遲
delay = random.uniform(1.0, 3.0)
time.sleep(delay)
```

### 定時任務 Jitter

```python
from apscheduler.triggers.interval import IntervalTrigger

# 每 24 小時執行，±30 分鐘隨機偏移
trigger = IntervalTrigger(hours=24, jitter=30*60)
```

## 數據對齊

### 頻率對齊

所有數據統一對齊到**日頻（D）**：
- ETF 持倉：前向填充（ffill），因為不是每日更新
- 價格數據：直接使用
- 交易日對齊

### 時區處理

- 統一使用 **UTC** 或 **America/New_York**
- ETF 持倉以美東時間為準
- Yahoo Finance 價格以交易所時區為準

### 缺值處理

```python
# ETF 持倉前向填充
df["holdings"] = df["holdings"].ffill()

# 價格不填充，保留 NaN
# 最後移除同時缺失的列
df = df.dropna(subset=["price", "holdings"])
```

## 程式碼範例

### 抓取 SLV 持倉（Selenium）

```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import random
import time

def fetch_slv_holdings():
    """從 iShares 官網抓取 SLV 持倉"""
    url = "https://www.ishares.com/us/products/239855/ishares-silver-trust-fund"

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    user_agent = random.choice(USER_AGENTS)
    chrome_options.add_argument(f'user-agent={user_agent}')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # 隨機延遲
        time.sleep(random.uniform(1.0, 2.0))

        driver.get(url)

        # 等待頁面載入
        wait = WebDriverWait(driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "fund-header-content")))

        # 額外等待 JS 執行
        time.sleep(3)

        # 解析
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # 提取持倉數據（選擇器需根據實際頁面調整）
        # ...

        return holdings_data

    finally:
        driver.quit()
```
