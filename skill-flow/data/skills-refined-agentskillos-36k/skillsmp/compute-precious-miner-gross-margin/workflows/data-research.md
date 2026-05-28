# Workflow: 數據源研究與爬蟲設計

<required_reading>
**執行前請先閱讀：**
1. references/data-sources.md - 數據來源詳情
2. thoughts/shared/guide/design-human-like-crawler.md - 爬蟲設計指南
</required_reading>

<process>

## Step 1: 識別目標礦業

根據分析需求識別需要獲取數據的礦業：

**黃金礦業**：
| 代碼 | 公司名稱          | IR 網站                                     |
|------|-------------------|---------------------------------------------|
| NEM  | Newmont           | https://www.newmont.com/investors/          |
| GOLD | Barrick Gold      | https://www.barrick.com/investors/          |
| AEM  | Agnico Eagle      | https://www.agnicoeagle.com/investors/      |
| KGC  | Kinross Gold      | https://www.kinross.com/investors/          |
| AU   | AngloGold Ashanti | https://www.anglogoldashanti.com/investors/ |

**白銀礦業**：
| 代碼 | 公司名稱            | IR 網站                                      |
|------|---------------------|----------------------------------------------|
| CDE  | Coeur Mining        | https://www.coeur.com/investors/             |
| HL   | Hecla Mining        | https://www.hecla.com/investors/             |
| AG   | First Majestic      | https://www.firstmajestic.com/investors/     |
| PAAS | Pan American Silver | https://www.panamericansilver.com/investors/ |
| MAG  | MAG Silver          | https://www.magsilver.com/investors/         |

## Step 2: 了解數據披露模式

**AISC 披露特點**：
- **頻率**：季度（部分公司半年）
- **位置**：
  - 季報新聞稿（最快取得）
  - 投資人簡報 PDF（有表格）
  - 10-Q / 10-K MD&A（最完整）
- **單位**：USD/oz（黃金）、USD/oz AgEq（白銀）
- **滯後**：財報發布約在季末後 1-2 個月

**典型披露格式**：
```
Production: 1,500,000 oz Au
AISC: $1,320/oz
Cash Cost: $980/oz
```

## Step 3: 選擇數據獲取策略

根據需求選擇策略：

| 策略         | 優點             | 缺點       | 適用場景             |
|--------------|------------------|------------|----------------------|
| 手動收集     | 準確、無技術門檻 | 耗時       | 少量公司、一次性分析 |
| 新聞稿爬蟲   | 結構化好         | 需維護     | 定期更新             |
| PDF 表格抽取 | 資料完整         | 技術難度高 | 歷史回填             |
| 第三方服務   | 省時             | 可能付費   | 生產環境             |

**建議**：新聞稿爬蟲 + 手動驗證

## Step 4: 爬蟲架構設計

遵循 `design-human-like-crawler.md` 的指引：

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import time

# 防偵測配置
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ...',
]

class MinerAISCCrawler:
    def __init__(self, miner_code: str):
        self.miner_code = miner_code
        self.ir_url = MINER_IR_URLS[miner_code]

    async def fetch_quarterly_reports(self):
        """抓取季報連結"""
        # 隨機延遲
        await asyncio.sleep(random.uniform(1.0, 3.0))
        # ... 實作

    def parse_aisc_from_news(self, html: str) -> dict:
        """從新聞稿解析 AISC"""
        soup = BeautifulSoup(html, 'lxml')
        # 多層備用選擇器
        selectors = [
            r'AISC[:\s]+\$?([\d,]+)',
            r'All-in sustaining cost[s]?[:\s]+\$?([\d,]+)',
        ]
        # ... 實作
```

## Step 5: 解析策略設計

**新聞稿解析**：
```python
import re

def extract_aisc_from_text(text: str) -> dict:
    """從文字中提取 AISC 數據"""
    patterns = {
        'aisc': [
            r'AISC\s*(?:of|was|:)?\s*\$?([\d,]+(?:\.\d+)?)\s*(?:per|/)\s*(?:oz|ounce)',
            r'all-in sustaining cost[s]?\s*(?:of|was|:)?\s*\$?([\d,]+(?:\.\d+)?)',
        ],
        'production': [
            r'(?:gold )?production\s*(?:of|was|:)?\s*([\d,]+(?:\.\d+)?)\s*(?:thousand\s)?(?:oz|ounces)',
            r'produced\s*([\d,]+(?:\.\d+)?)\s*(?:thousand\s)?(?:oz|ounces)',
        ],
        'cash_cost': [
            r'cash cost[s]?\s*(?:of|was|:)?\s*\$?([\d,]+(?:\.\d+)?)',
        ]
    }

    result = {}
    for key, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                result[key] = float(match.group(1).replace(',', ''))
                break

    return result
```

## Step 6: PDF 表格抽取（進階）

若需要歷史數據回填，可使用 PDF 解析：

```python
# 選用：tabula-py 或 camelot
import tabula

def extract_tables_from_pdf(pdf_path: str):
    """從 PDF 抽取表格"""
    tables = tabula.read_pdf(pdf_path, pages='all')

    for table in tables:
        # 尋找含 AISC 的表格
        if 'AISC' in table.to_string():
            return table

    return None
```

**注意**：PDF 抽取不穩定，建議：
- 優先使用新聞稿
- PDF 僅作備用
- 抽取後人工驗證

## Step 7: 數據儲存格式

設計標準化的儲存格式：

```python
# data/miner_costs.json
{
    "NEM": {
        "2024-Q4": {
            "aisc_usd_oz": 1350,
            "cash_cost_usd_oz": 980,
            "production_oz": 1600000,
            "source": "Q4 2024 Earnings Release",
            "source_url": "https://...",
            "scraped_at": "2025-01-15T10:30:00Z"
        },
        "2024-Q3": {
            ...
        }
    },
    "GOLD": {
        ...
    }
}
```

## Step 8: 建立更新排程

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = AsyncIOScheduler()

# 每月 15 日檢查（多數公司在季末後 45 天內發布）
scheduler.add_job(
    update_quarterly_costs,
    CronTrigger(day=15, hour=6),
    id='quarterly_cost_update'
)
```

## Step 9: 驗證與品質控制

```python
def validate_cost_data(data: dict) -> list:
    """驗證成本數據品質"""
    issues = []

    for miner, quarters in data.items():
        for q, values in quarters.items():
            # 合理範圍檢查
            aisc = values.get('aisc_usd_oz', 0)
            if aisc < 500 or aisc > 2500:
                issues.append(f"{miner} {q}: AISC {aisc} 超出合理範圍")

            # 連續性檢查
            # ... 實作

    return issues
```

</process>

<success_criteria>
數據研究完成時應有：

- [ ] 目標礦業清單與 IR 網站
- [ ] 數據披露模式理解（頻率、位置、格式）
- [ ] 爬蟲架構設計（遵循防偵測指引）
- [ ] 解析規則（正則表達式或選擇器）
- [ ] 標準化儲存格式定義
- [ ] 更新排程規劃
- [ ] 品質驗證規則
</success_criteria>

<output_artifacts>
完成本 workflow 後產出：
- `scripts/crawler/miner_cost_crawler.py` - 爬蟲核心
- `data/miner_costs.json` - 成本數據
- `data/crawl_log.json` - 爬取記錄
</output_artifacts>
