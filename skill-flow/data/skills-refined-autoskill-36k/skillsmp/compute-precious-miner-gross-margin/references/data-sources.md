# 數據來源指南

## 金屬價格數據

### 黃金價格

| 來源                | 類型       | URL / API                               | 頻率 | 備註             |
|---------------------|------------|-----------------------------------------|------|------------------|
| **LBMA Gold Price** | 現貨指標價 | https://www.lbma.org.uk/prices-and-data | 日   | 最權威的現貨基準 |
| **COMEX GC**        | 期貨近月   | yfinance `GC=F`                         | 日   | 流動性最佳       |
| **Yahoo Finance**   | 現貨       | yfinance `GC=F` 或 `GOLD`               | 日   | 免費、方便       |
| **FRED**            | 歷史       | fred `GOLDAMGBD228NLBM`                 | 日   | 長期歷史         |

**建議**：使用 **yfinance `GC=F`**（COMEX 近月期貨），因：
- 免費且無需 API key
- 覆蓋足夠歷史
- 與礦業實際結算價接近

**Python 範例**：
```python
import yfinance as yf

gold = yf.download("GC=F", start="2010-01-01")
gold_price = gold['Close']
```

### 白銀價格

| 來源                  | 類型       | URL / API                               | 頻率 | 備註     |
|-----------------------|------------|-----------------------------------------|------|----------|
| **LBMA Silver Price** | 現貨指標價 | https://www.lbma.org.uk/prices-and-data | 日   | 最權威   |
| **COMEX SI**          | 期貨近月   | yfinance `SI=F`                         | 日   | 流動性佳 |

**Python 範例**：
```python
silver = yf.download("SI=F", start="2010-01-01")
silver_price = silver['Close']
```

---

## 礦業成本數據

### AISC 數據來源

成本數據是本 skill 的**核心難點**，因無單一公開資料庫，需從多來源收集：

#### 1. 公司投資人簡報 (Investor Presentation)

**優點**：
- 通常有 AISC 摘要表格
- 格式較結構化
- 每季更新

**缺點**：
- PDF 格式需解析
- 各公司格式不一

**範例來源**：
| 公司               | IR 頁面                                                 |
|--------------------|---------------------------------------------------------|
| Newmont (NEM)      | https://www.newmont.com/investors/presentations/        |
| Barrick (GOLD)     | https://www.barrick.com/investors/presentations/        |
| Agnico Eagle (AEM) | https://www.agnicoeagle.com/investors/presentations/    |
| Coeur (CDE)        | https://www.coeur.com/investors/presentations/          |
| Hecla (HL)         | https://www.hecla.com/investors/investor-presentations/ |

#### 2. 季報新聞稿 (Earnings Release)

**優點**：
- 純文字，易解析
- 發布最快
- 通常在開頭摘要

**缺點**：
- 格式不固定
- 需正則表達式匹配

**解析範例**：
```python
import re

def extract_aisc(text):
    patterns = [
        r'AISC\s*(?:of|was|:)?\s*\$?([\d,]+(?:\.\d+)?)\s*(?:per|/)\s*(?:oz|ounce)',
        r'all-in sustaining cost[s]?\s*(?:of|was|:)?\s*\$?([\d,]+(?:\.\d+)?)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1).replace(',', ''))
    return None
```

#### 3. SEC 10-Q / 10-K (MD&A)

**優點**：
- 最完整
- 標準化格式
- 可透過 EDGAR API 取得

**缺點**：
- 發布較慢
- 需解析複雜文件

**EDGAR API 範例**：
```python
import requests

def get_sec_filings(ticker, filing_type='10-Q'):
    # 透過 SEC EDGAR API
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    # ... 實作
```

#### 4. 第三方彙整

| 來源               | URL                     | 說明           |
|--------------------|-------------------------|----------------|
| Mining.com         | https://www.mining.com/ | 偶有彙整報導   |
| Kitco              | https://www.kitco.com/  | 有成本追蹤報導 |
| World Gold Council | https://www.gold.org/   | 產業報告       |

---

## 產量數據

產量數據用於 production_weighted 聚合：

### 來源

| 來源     | 說明                  |
|----------|-----------------------|
| 公司季報 | 與 AISC 同一來源      |
| 年報摘要 | 全年產量指引          |
| 產業報告 | WGC、Silver Institute |

### 單位轉換

```python
# 噸 (tonnes) → 盎司 (troy oz)
oz = tonnes * 32150.7465

# 千盎司 (koz) → 盎司
oz = koz * 1000

# 銀等量 (AgEq oz) = 實際銀 + 副產品折算
# 通常使用固定比率（如 80:1 金銀比）
```

---

## 數據更新頻率

| 數據類型 | 披露頻率 | 滯後     | 更新建議   |
|----------|----------|----------|------------|
| 金銀價格 | 日       | 即時     | 日更新     |
| AISC     | 季度     | 1-2 個月 | 季報發布後 |
| 產量     | 季度     | 1-2 個月 | 同 AISC    |
| 年度指引 | 年初     | -        | 年初一次   |

**建議更新排程**：
- 價格：每日自動更新
- 成本/產量：每季度手動更新（可搭配爬蟲）

---

## 預設礦業籃子

### 黃金礦業

| 代碼 | 公司              | 2024 產量估 | 說明       |
|------|-------------------|-------------|------------|
| NEM  | Newmont           | ~6M oz      | 全球最大   |
| GOLD | Barrick Gold      | ~4M oz      | 全球第二   |
| AEM  | Agnico Eagle      | ~3.5M oz    | 加拿大為主 |
| KGC  | Kinross Gold      | ~2M oz      | 美洲/西非  |
| AU   | AngloGold Ashanti | ~2.5M oz    | 非洲/美洲  |

**串流公司（不含在成本分析）**：
- FNV (Franco-Nevada)
- WPM (Wheaton Precious Metals)

### 白銀礦業

| 代碼 | 公司                | 2024 產量估  | 說明           |
|------|---------------------|--------------|----------------|
| CDE  | Coeur Mining        | ~10M oz Ag   | 美國為主       |
| HL   | Hecla Mining        | ~15M oz Ag   | 美國最大銀礦業 |
| AG   | First Majestic      | ~20M oz AgEq | 墨西哥         |
| PAAS | Pan American Silver | ~20M oz Ag   | 拉美           |
| MAG  | MAG Silver          | ~5M oz Ag    | 墨西哥         |

---

## 估算方法（缺乏數據時）

若無法取得某礦業的 AISC，可使用以下估算：

### 方法 1：營業成本推算

```python
# 使用財報數據
estimated_unit_cost = cost_of_revenue / gold_sold_oz
```

**注意**：此方法會混入副產品、會計差異，僅作參考。

### 方法 2：同業參照

```python
# 使用同類型礦業的 AISC 平均值
peer_aisc = similar_miners_aisc.mean()
```

### 方法 3：成本曲線參照

參考 WGC 或產業報告的成本曲線：
- 低成本生產商：$900-1,100/oz
- 中等成本：$1,100-1,300/oz
- 高成本生產商：$1,300-1,600/oz

---

## 爬蟲設計指引

詳細爬蟲設計請參考：
- `thoughts/shared/guide/design-human-like-crawler.md`
- `workflows/data-research.md`

### 關鍵要點

1. **使用 Selenium**：公司 IR 網站多為動態載入
2. **防偵測**：隨機 UA、延遲、禁用自動化標記
3. **多層選擇器**：網站可能改版
4. **驗證機制**：抓取後人工驗證

---

## 資料儲存格式

建議使用 JSON 格式儲存：

```json
{
  "metadata": {
    "updated_at": "2025-01-15T10:00:00Z",
    "source_version": "v1.0"
  },
  "gold": {
    "NEM": {
      "2024-Q4": {
        "aisc_usd_oz": 1350,
        "cash_cost_usd_oz": 980,
        "production_oz": 1600000,
        "source": "Q4 2024 Earnings Release",
        "source_url": "https://..."
      }
    }
  },
  "silver": {
    "CDE": {
      ...
    }
  }
}
```
