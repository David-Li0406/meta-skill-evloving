# 輸入參數定義 (Input Schema)

## 核心參數

### metal (string) - **必填**

目標金屬類型。

| 值       | 說明         |
|----------|--------------|
| `gold`   | 黃金（預設） |
| `silver` | 白銀         |

**範例**：
```bash
--metal gold
```

---

### miners (list[string]) - 選填

礦業或礦業股代號清單。

**預設值**：
- 黃金：`["NEM", "GOLD", "AEM", "KGC", "AU"]`
- 白銀：`["CDE", "HL", "AG", "PAAS", "MAG"]`

**範例**：
```bash
--miners NEM,GOLD,AEM
--miners "CDE,HL,AG"
```

**注意**：
- 使用逗號分隔
- 需確保有對應的成本數據

---

### start_date (string, YYYY-MM-DD) - **必填**

計算起始日期。

**範例**：
```bash
--start-date 2015-01-01
```

**建議**：
- 黃金：2013 年後（AISC 標準化後）
- 至少 10 年以計算有意義的歷史分位數

---

### end_date (string, YYYY-MM-DD) - 選填

計算結束日期。

**預設值**：今天

**範例**：
```bash
--end-date 2025-12-31
```

---

### frequency (string) - **必填**

數據頻率。

| 值          | 說明         | 建議場景                       |
|-------------|--------------|--------------------------------|
| `daily`     | 日頻         | 短期交易訊號（需內插成本）     |
| `weekly`    | 週頻         | 短期分析（需內插成本）         |
| `monthly`   | 月頻         | 一般分析                       |
| `quarterly` | 季頻（預設） | **建議**（與成本披露頻率一致） |

**範例**：
```bash
--frequency quarterly
```

---

### cost_metric (string) - **必填**

成本口徑。

| 值             | 說明                           | 典型值 (Gold)   |
|----------------|--------------------------------|-----------------|
| `AISC`         | All-In Sustaining Cost（預設） | $1,100-1,500/oz |
| `cash_cost_C1` | 現金成本                       | $800-1,200/oz   |
| `all_in_cost`  | 全成本（含成長資本開支）       | $1,300-1,800/oz |

**範例**：
```bash
--cost-metric AISC
```

**建議**：優先使用 `AISC`，因其可比性最佳。

---

### aggregation (string) - 選填

籃子聚合方式。

| 值                    | 說明             | 適用場景                   |
|-----------------------|------------------|----------------------------|
| `equal_weight`        | 等權重平均       | 關注「典型礦業」           |
| `production_weighted` | 產量加權（預設） | **建議**，反映「產業毛利」 |
| `marketcap_weighted`  | 市值加權         | 與 GDX 曝險結構接近        |

**範例**：
```bash
--aggregation production_weighted
```

---

## 進階參數

### price_series (string) - 選填

價格口徑。

| 值                  | 說明                                |
|---------------------|-------------------------------------|
| `spot`              | 現貨價（預設，LBMA 或近月期貨代理） |
| `front_futures`     | 期貨近月合約                        |
| `realized_estimate` | 公司實際銷售價估算（需額外數據）    |

**預設值**：`spot`

---

### fx_mode (string) - 選填

匯率處理方式。

| 值             | 說明                             |
|----------------|----------------------------------|
| `none`         | 不處理（預設，假設成本已為 USD） |
| `local_to_usd` | 將本地幣別成本轉為 USD           |

**預設值**：`none`

**說明**：多數礦業以 USD 報告 AISC，通常不需匯率轉換。

---

### outlier_rule (string) - 選填

離群值處理規則。

| 值               | 說明                         |
|------------------|------------------------------|
| `winsorize_1_99` | 縮尾至 1-99 分位數（預設）   |
| `winsorize_5_95` | 縮尾至 5-95 分位數（更激進） |
| `median_filter`  | 中位數濾波                   |
| `none`           | 不處理                       |

**預設值**：`winsorize_1_99`

---

### history_window_years (int) - 選填

歷史分位數計算視窗（年）。

| 值 | 覆蓋週期          | 說明   |
|----|-------------------|--------|
| 10 | ~2 個週期         | 較敏感 |
| 15 | ~3 個週期         | 平衡   |
| 20 | ~4 個週期（預設） | 穩健   |

**預設值**：`20`

**範例**：
```bash
--history-window 15
```

---

## 輸出參數

### output (string) - 選填

輸出檔案路徑。

**範例**：
```bash
--output result.json
--output report.md
```

**格式判斷**：
- `.json` → JSON 格式
- `.md` → Markdown 報告

---

### format (string) - 選填

強制指定輸出格式。

| 值         | 說明              |
|------------|-------------------|
| `json`     | JSON 格式（預設） |
| `markdown` | Markdown 報告     |

---

## 訊號生成參數

### generate_signals (bool) - 選填

是否生成交易/研究訊號。

**預設值**：`false`

**範例**：
```bash
--generate-signals
```

---

### event_study (bool) - 選填

是否執行極端事件研究。

**預設值**：`false`

**範例**：
```bash
--event-study
```

---

### signal_horizons (list[int]) - 選填

事件研究的前瞻報酬天數。

**預設值**：`[63, 126, 252]`（約 3/6/12 個月）

---

## 完整範例

### 快速計算

```bash
python scripts/margin_calculator.py --quick --metal gold
```

### 完整分析

```bash
python scripts/margin_calculator.py \
  --metal silver \
  --miners CDE,HL,AG \
  --start-date 2015-01-01 \
  --frequency quarterly \
  --cost-metric AISC \
  --aggregation production_weighted \
  --history-window 15 \
  --output result.json
```

### 訊號生成

```bash
python scripts/margin_calculator.py \
  --metal gold \
  --generate-signals \
  --event-study \
  --signal-horizons 63,126,252 \
  --output signals.json
```

---

## 參數摘要表

| 參數                   | 類型   | 必填 | 預設值              | 說明     |
|------------------------|--------|------|---------------------|----------|
| `metal`                | string | ✅    | gold                | 目標金屬 |
| `miners`               | list   | ❌    | 預設籃子            | 礦業清單 |
| `start_date`           | string | ✅    | -                   | 起始日   |
| `end_date`             | string | ❌    | today               | 結束日   |
| `frequency`            | string | ✅    | quarterly           | 頻率     |
| `cost_metric`          | string | ✅    | AISC                | 成本口徑 |
| `aggregation`          | string | ❌    | production_weighted | 聚合方式 |
| `price_series`         | string | ❌    | spot                | 價格口徑 |
| `fx_mode`              | string | ❌    | none                | 匯率處理 |
| `outlier_rule`         | string | ❌    | winsorize_1_99      | 離群處理 |
| `history_window_years` | int    | ❌    | 20                  | 歷史視窗 |
| `output`               | string | ❌    | stdout              | 輸出路徑 |
| `format`               | string | ❌    | json                | 輸出格式 |
| `generate_signals`     | bool   | ❌    | false               | 生成訊號 |
| `event_study`          | bool   | ❌    | false               | 事件研究 |
