# 完整分析工作流

執行完整的分析日本債務利息負擔，包含現況核對、壓力測試與外溢通道評估。

## 執行步驟

### Step 1: 安裝依賴

```bash
cd skills/analyze-japan-debt-service-tax-burden
pip install pandas numpy requests
```

### Step 2: 執行完整分析

```bash
python scripts/japan_debt_analyzer.py --full
```

或指定 JSON 輸出：
```bash
python scripts/japan_debt_analyzer.py --full --format json
```

### Step 3: 解讀各區塊結果

#### 3.1 殖利率狀態 (yield_stats)

```json
{
  "tenor": "10Y",
  "latest": 1.23,
  "zscore": 2.10,
  "percentile": 0.97,
  "interpretation": "分位數 97%，處於極端高位區"
}
```

**核對敘事**：
- 若 percentile > 0.95 且 zscore > 2.0 → 接近極值，敘事「創高」可能成立
- 若 percentile < 0.80 → 敘事可能誇大

#### 3.2 財政利息負擔 (fiscal)

```json
{
  "interest_tax_ratio": 0.333,
  "risk_band": "yellow",
  "definition": {
    "tax_revenue_series": "general_account_tax",
    "interest_payment_series": "interest_only",
    "fiscal_year": "FY2024"
  }
}
```

**核對敘事**：
- 0.333 ≈ 1/3，敘事「利息吃掉 1/3 稅收」可驗證
- 注意口徑：若用 total_revenue（含非稅收入），ratio 會較低

#### 3.3 壓力測試 (stress_tests)

```json
{
  "name": "+200bp baseline",
  "results": {
    "year1_interest_tax_ratio": 0.383,
    "year2_interest_tax_ratio": 0.433
  },
  "risk_band_year2": "orange"
}
```

**敏感度分析**：
- 主要驅動因子：債務存量 × 再定價速度 × 利率衝擊
- Year 2 累積效應：兩年再定價約 30% 存量債務

#### 3.4 外溢通道 (spillover_channel)

```json
{
  "us_assets_estimate_usd": 3000000000000,
  "ust_holdings_usd": 1100000000000,
  "note": "僅標示通道與量級，不做行為預測"
}
```

**謹慎解讀**：
- 「持有」≠「會拋售」
- 實際拋售受制於：政策約束、匯率影響、市場深度

### Step 4: 輸出報告

完整 Markdown 報告會包含：
1. 摘要 headline
2. 殖利率狀態表
3. 財政負擔表
4. 壓力測試結果表
5. 外溢通道說明
6. 要點摘要列表

## 自定義分析

若需調整參數，編輯腳本或使用 `--stress` 單一壓測：

```bash
# 壓測 +150bp
python scripts/japan_debt_analyzer.py --stress 150

# 不含外溢分析
python scripts/japan_debt_analyzer.py --full --no-spillover
```
