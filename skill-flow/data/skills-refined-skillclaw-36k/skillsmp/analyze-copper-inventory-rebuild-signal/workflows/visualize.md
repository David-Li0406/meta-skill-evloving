<required_reading>
- references/data-sources.md（確認數據已抓取）
</required_reading>

<objective>
生成 Bloomberg 風格的銅庫存回補訊號視覺化圖表。
</objective>

<process>

**Step 1: 確認數據存在**

```bash
ls cache/shfe_inventory.csv cache/comex_inventory.csv cache/copper_price.csv
```

若不存在，先執行：
```bash
python fetch_copper_data.py
```

**Step 2: 生成圖表**

```bash
cd skills/analyze-copper-inventory-rebuild-signal/scripts
python visualize_inventory_signal.py
```

**Step 3: 指定輸出路徑（可選）**

```bash
python visualize_inventory_signal.py --output path/to/custom_output.png
```

</process>

<chart_components>
**圖表包含多個子圖**

1. **上圖：價格與庫存**
   - 左軸：銅期貨價格（USD/lb）
   - 右軸：SHFE 和 COMEX 庫存（噸）
   - 標記：CAUTION 訊號點

2. **中圖：回補速度 Z-Score**
   - 顯示 SHFE 和 COMEX z-score 時序
   - 標記 ±1.5 和 ±2.0 門檻線
   - CAUTION 區域（z > 1.5）著色

3. **下圖：庫存分位數熱力條**
   - 顯示庫存在歷史分布中的位置
   - 綠色（低位）→ 紅色（高位）

**配色方案（Bloomberg 深色主題）**

| 元素 | 顏色 |
|------|------|
| 背景 | #1a1a2e |
| 銅價 | #ffa500（橙色） |
| SHFE 庫存 | #00bfff（天藍） |
| COMEX 庫存 | #00ff88（綠色） |
| CAUTION 標記 | #ff6b35（紅橙） |
| SUPPORTIVE 標記 | #00d4aa（青綠） |
| 門檻線 | #666666（灰色） |
</chart_components>

<output>
**預設輸出路徑**：`output/copper_inventory_signal.png`

**圖表尺寸**：1600 x 1200 像素

**字體**：等寬字體（Consolas / Monaco / monospace）
</output>

<success_criteria>
- [x] 圖表成功生成
- [x] 三個子圖完整顯示
- [x] CAUTION 訊號點正確標記
- [x] 配色符合 Bloomberg 風格
</success_criteria>
