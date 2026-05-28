# 圖表生成工作流

生成日本債務利息負擔的視覺化 Dashboard。

## 執行步驟

### Step 1: 執行圖表生成腳本

**完整模式**（推薦，包含壓力測試）：
```bash
cd skills/analyze-japan-debt-service-tax-burden
python scripts/generate_charts.py --full --output-dir ../../output
```

**快速模式**：
```bash
python scripts/generate_charts.py --quick --output-dir ../../output
```

**從 JSON 檔案載入**：
```bash
python scripts/generate_charts.py --data-file data.json --output-dir ../../output
```

### Step 2: 確認輸出

輸出檔案：`output/japan_debt_dashboard_YYYYMMDD.png`

### Step 3: Dashboard 內容說明

生成的 Dashboard 包含四個區塊：

| 區塊 | 說明 |
|------|------|
| **風險儀表盤** (左上) | Interest/Tax Ratio 半圓儀表盤，顯示當前比例與風險區間 |
| **殖利率指標** (中上) | 10Y JGB 殖利率分位數指標，標示是否處於極端位置 |
| **財政摘要** (右上) | 稅收、利息支出、存量債務、隱含平均利率 |
| **壓力測試** (下方) | 多情境壓力測試結果條形圖，Year 1 vs Year 2 對比 |

### Step 4: 風險分級顏色

| 顏色 | 區間 | 含義 |
|------|------|------|
| 綠色 | < 25% | 財政彈性充足 |
| 黃色 | 25-40% | 彈性開始下降 |
| 橘色 | 40-55% | 政策空間受限 |
| 紅色 | > 55% | 接近危險區 |

## 進階選項

### 指定輸出檔名
```bash
python scripts/generate_charts.py --full --output-file my_dashboard.png
```

### 強制刷新數據
```bash
python scripts/generate_charts.py --full --refresh --output-dir ../../output
```

### 顯示圖表（不只存檔）
```bash
python scripts/generate_charts.py --full --show
```

## 輸出範例

Dashboard 範例輸出：

```
┌─────────────────┬─────────────────┬─────────────────┐
│  風險儀表盤     │  殖利率指標     │  財政摘要       │
│     15.0%       │  10Y: 2.06%     │  稅收: ¥70兆    │
│   ● GREEN       │  分位: 100%     │  利息: ¥10.5兆  │
└─────────────────┴─────────────────┴─────────────────┘
┌─────────────────────────────────────────────────────┐
│                 壓力測試情境比較                    │
│  +100bp baseline   ████████░░░░░░░  17.8% → 20.7%  │
│  +200bp baseline   ██████████░░░░░  20.7% → 26.4%  │
│  +200bp recession  ██████████░░░░░  21.8% → 27.7%  │
│  +300bp stress     █████████████░░  26.1% → 35.6%  │
└─────────────────────────────────────────────────────┘
```

## 常見問題

### 字體警告
如果出現中文字體警告，請確保系統安裝以下字體之一：
- Microsoft JhengHei
- PingFang TC
- Noto Sans CJK TC

### matplotlib 安裝
```bash
pip install matplotlib
```
