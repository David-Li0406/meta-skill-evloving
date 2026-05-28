# Workflow: 快速檢查

<required_reading>
**執行前快速瀏覽：**
1. references/data-sources.md - 確認資料來源可用
</required_reading>

<process>

## Step 1: 執行快速檢查腳本

```bash
cd skills/analyze-copper-stock-resilience-dependency
python scripts/copper_stock_analyzer.py --quick
```

此命令會：
1. 抓取最近 3 年數據（使用快取優先）
2. 計算當前狀態（趨勢、關卡、韌性評分）
3. 輸出簡要摘要

## Step 2: 解讀輸出

### 輸出範例

```json
{
  "as_of": "2026-01-20",
  "quick_check": true,
  "latest_state": {
    "copper_price_usd_per_ton": 12700,
    "copper_sma_60": 9261,
    "copper_trend": "up",
    "near_resistance": [13000],
    "near_support": [],
    "equity_resilience_score": 78,
    "rolling_beta_equity_24m": 0.62
  },
  "quick_diagnosis": "上升趨勢中，接近 13,000 關卡，股市韌性高（78），支持續航",
  "flags": ["APPROACHING_RESISTANCE"]
}
```

### 欄位解讀

| 欄位 | 含義 |
|------|------|
| copper_trend | 趨勢狀態：up/down/range |
| near_resistance | 接近的上方關卡（阻力） |
| near_support | 接近的下方關卡（支撐） |
| equity_resilience_score | 股市韌性：70+ 高、30- 低 |
| rolling_beta_equity_24m | 銅對股市的依賴度 |
| flags | 警報旗標（見下方說明） |

### 常見 Flags

| Flag | 條件 | 建議動作 |
|------|------|----------|
| `APPROACHING_RESISTANCE` | 接近關卡上方 | 關注是否能突破 |
| `APPROACHING_SUPPORT` | 接近關卡下方 | 關注是否會跌破 |
| `WATCH_EQUITY_RESILIENCE` | 韌性 < 50 且接近關卡 | 回補風險上升 |
| `HIGH_BETA_REGIME` | β_equity 位於高分位 | 銅正被當風險資產交易 |

## Step 3: 判斷是否需要完整分析

如果快速檢查顯示以下情況，建議執行完整分析：

1. **接近關卡** (near_resistance 或 near_support 非空)
2. **韌性邊界** (equity_resilience_score 在 45-55 之間)
3. **趨勢轉換** (copper_trend = "range")

完整分析命令：
```bash
python scripts/copper_stock_analyzer.py \
    --start 2020-01-01 \
    --end 2026-01-20 \
    --output result.json
```

</process>

<success_criteria>
快速檢查成功時應產出：

- [ ] 當前銅價（USD/ton）
- [ ] 趨勢狀態
- [ ] 關卡接近判定
- [ ] 股市韌性評分
- [ ] 滾動貝塔（最近值）
- [ ] 快速診斷摘要
- [ ] 警報旗標（如有）
</success_criteria>
