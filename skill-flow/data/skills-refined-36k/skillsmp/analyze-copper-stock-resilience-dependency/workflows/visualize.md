# Workflow: 視覺化圖表（Bloomberg 風格）

<required_reading>
**執行前請閱讀：**
1. references/data-sources.md - 確認資料來源
</required_reading>

<process>

## Step 1: 生成 Bloomberg 風格圖表

### 1.1 快速生成（預設 2015-今）

```bash
cd skills/analyze-copper-stock-resilience-dependency
python scripts/visualize.py
```

輸出檔案會自動命名為 `output/copper_resilience_YYYY-MM-DD.png`

### 1.2 自訂參數

```bash
python scripts/visualize.py \
    --start 2015-01-01 \
    --end 2026-01-22 \
    -o output/copper_resilience_2026-01-22.png \
    --figsize 14,8 \
    --dpi 150 \
    --levels 10000,13000
```

## Step 2: 圖表元素說明

圖表模仿 Bloomberg Intelligence 風格，包含：

| 元素                 | 軸位   | 顏色   | 說明                       |
|----------------------|--------|--------|----------------------------|
| 銅價 (HG=F)          | R1 右軸 | 橙紅色 | 月線圖，轉換為 USD/ton     |
| SMA(60)              | R1 右軸 | 橙黃色 | 60 月移動平均線            |
| 全球股市市值         | L2 左軸 | 橙色   | 面積圖（VT 作為代理）      |
| 中國 10Y 殖利率      | L1 左軸 | 黃色   | 折線圖                     |
| 關卡線               | R1 右軸 | 灰色   | 10,000 / 13,000 整數位     |

### 數值標註

圖表右側會標註各序列的最新數值：
- 銅價（粗體）
- SMA60
- 全球市值（兆美元）
- 中國 10Y（%）

## Step 3: 配置選項

### 可用參數

| 參數          | 預設值         | 說明               |
|---------------|----------------|--------------------|
| `--start`     | 2015-01-01     | 起始日期           |
| `--end`       | 今天           | 結束日期           |
| `-o/--output` | 自動生成       | 輸出路徑           |
| `--figsize`   | 14,8           | 圖表尺寸（寬,高）  |
| `--dpi`       | 150            | 解析度             |
| `--levels`    | 10000,13000    | 關卡位置（逗號分隔）|
| `--ma-window` | 60             | SMA 視窗           |

### 輸出路徑規範

建議輸出至專案根目錄的 `output/` 資料夾：

```
output/
├── copper_resilience_2026-01-22.png
├── copper_resilience_2026-01-21.png
└── ...
```

## Step 4: 從分析腳本生成

也可以在完整分析後直接生成圖表：

```bash
# 完整分析 + 圖表
python scripts/copper_stock_analyzer.py \
    --start 2015-01-01 \
    --end 2026-01-22 \
    --output data/result.json

# 單獨生成圖表
python scripts/visualize.py \
    --start 2015-01-01 \
    --end 2026-01-22 \
    -o output/copper_resilience_2026-01-22.png
```

</process>

<success_criteria>
視覺化成功時應產出：

- [ ] Bloomberg 風格深色背景圖表
- [ ] 多軸疊加（銅價 R1 + 市值 L2 + 殖利率 L1）
- [ ] 銅價線 + SMA60 線
- [ ] 全球市值橙色面積圖
- [ ] 中國 10Y 黃色折線
- [ ] 關卡位置標記（10,000 / 13,000）
- [ ] 數值標註（最新值）
- [ ] 圖例、來源、日期標註
- [ ] 圖表儲存至 `output/` 目錄
</success_criteria>

<troubleshooting>

### 常見問題

**1. 找不到 mplfinance 模組**
```bash
pip install mplfinance
```

**2. 中國殖利率爬取失敗**
會自動使用模擬數據，不影響圖表生成。

**3. 圖表中文亂碼**
```python
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
```

**4. 數據時間範圍不一致**
腳本會自動對齊到共同的時間區間。

</troubleshooting>
