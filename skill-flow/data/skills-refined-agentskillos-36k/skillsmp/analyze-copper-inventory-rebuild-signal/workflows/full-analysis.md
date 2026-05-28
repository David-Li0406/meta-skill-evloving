<required_reading>
- references/data-sources.md（數據來源與快取策略）
- references/methodology.md（方法論詳解）
- references/historical-episodes.md（歷史案例）
</required_reading>

<objective>
執行完整的銅庫存回補訊號分析，包括歷史回測驗證與詳細報告。
</objective>

<process>

**Step 1: 強制更新數據（SHFE + COMEX + 價格）**

```bash
cd skills/analyze-copper-inventory-rebuild-signal/scripts
python fetch_copper_data.py --force-refresh
```

**Step 2: 執行完整分析**

```bash
python inventory_signal_analyzer.py --full
```

**Step 3: 生成視覺化圖表**

```bash
python visualize_inventory_signal.py
```

輸出：`output/copper_inventory_signal.png`

**Step 4: 檢視完整報告**

分析結果包含：

1. **最新狀態**
   - SHFE 庫存量與分位數
   - SHFE 回補速度 z-score
   - COMEX 庫存量與分位數
   - COMEX 回補速度 z-score
   - 總庫存（SHFE + COMEX）
   - 銅價與分位數

2. **短期判斷**
   - near_term_signal（主要看 SHFE）
   - 訊號原因
   - 歷史驗證命中率

3. **長期判斷**
   - 價格歷史分位數
   - long_term_view

4. **歷史回測**
   - 訊號觸發次數
   - 命中次數與命中率

</process>

<parameter_tuning>
**可調參數**

| 參數 | 預設值 | 說明 |
|------|--------|------|
| fast_rebuild_window_weeks | 4 | 回補觀察窗口（週） |
| fast_rebuild_z | 1.5 | z-score 門檻 |
| z_baseline_weeks | 156 | z-score 滾動基準（3年） |
| high_inventory_percentile | 0.85 | 庫存偏高門檻 |
| peak_match_window_weeks | 2 | 局部高點匹配窗口 |
| long_term_window_years | 10 | 長期歷史窗口 |
| cheap_percentile | 0.35 | 便宜門檻 |
| rich_percentile | 0.65 | 昂貴門檻 |

**修改方式**：

編輯 `scripts/inventory_signal_analyzer.py` 中的 `DEFAULT_CONFIG`。
</parameter_tuning>

<output_format>
完整分析輸出格式參考：
- Markdown：`templates/output-markdown.md`
- JSON：`templates/output-json.md`
</output_format>

<success_criteria>
- [x] 數據成功更新
- [x] 完整分析報告生成
- [x] Bloomberg 風格圖表輸出
- [x] 歷史回測結果可驗證
- [x] 訊號邏輯與方法論一致
</success_criteria>
