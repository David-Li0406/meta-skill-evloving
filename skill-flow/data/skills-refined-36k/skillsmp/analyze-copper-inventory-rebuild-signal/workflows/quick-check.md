<required_reading>
- references/data-sources.md（數據來源與快取策略）
</required_reading>

<objective>
快速檢查當前銅庫存回補訊號狀態，產出簡短的訊號判讀。
</objective>

<process>

**Step 1: 執行數據抓取（SHFE + COMEX + 價格）**

```bash
cd skills/analyze-copper-inventory-rebuild-signal/scripts
python fetch_copper_data.py
```

若快取有效（12 小時內），會直接使用快取數據。

**Step 2: 執行分析**

```bash
python inventory_signal_analyzer.py
```

**Step 3: 查看結果**

分析結果會輸出到控制台，並儲存到：
- `cache/analysis_result.json`

**Step 4: 解讀訊號**

| near_term_signal | 解讀 |
|------------------|------|
| CAUTION | 短線謹慎，回補速度異常快且庫存偏高 |
| NEUTRAL | 無明顯訊號 |
| SUPPORTIVE | 庫存偏低或去化快，短線有支撐 |

| long_term_view | 解讀 |
|----------------|------|
| CHEAP | 長期偏便宜（價格分位數 ≤ 35%） |
| FAIR | 長期中性 |
| RICH | 長期偏貴（價格分位數 ≥ 65%） |

</process>

<output_format>
快速檢查的輸出應包含：

```
銅庫存回補訊號快速檢查
========================
數據日期：{asof}
SHFE 庫存：{shfe_inventory_tonnes:,} 噸
SHFE 回補速度 z-score：{shfe_rebuild_z:+.2f}
COMEX 庫存：{comex_inventory_tonnes:,} 噸
COMEX 回補速度 z-score：{comex_rebuild_z:+.2f}
總庫存：{total_inventory_tonnes:,} 噸
銅價：{copper_price:.2f} USD/lb

短期訊號：{signal_emoji} {near_term_signal}
長期判讀：{view_emoji} {long_term_view}
```
</output_format>

<success_criteria>
- [x] 數據成功抓取或使用有效快取
- [x] 分析完成並輸出訊號
- [x] 訊號解讀清晰明確
</success_criteria>
