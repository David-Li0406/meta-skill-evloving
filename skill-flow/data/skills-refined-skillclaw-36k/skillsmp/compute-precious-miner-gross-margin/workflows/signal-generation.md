# Workflow: 訊號生成

<required_reading>
**執行前請先閱讀：**
1. references/methodology.md - 理解毛利率代理值的含義
2. workflows/analyze.md - 確保已完成基礎計算
</required_reading>

<process>

## Step 1: 確認訊號生成目標

訊號可用於：

| 目標       | 訊號類型     | 適用場景               |
|------------|--------------|------------------------|
| 礦業股擇時 | 極端區間標記 | 配置 GDX/GDXJ/SIL/SILJ |
| 個股選擇   | 相對毛利排名 | 選股因子               |
| 事件研究   | 極端事件日期 | 回測前瞻報酬           |
| 風險預警   | 均值回歸訊號 | 風險管理               |

## Step 2: 極端區間訊號

生成基於歷史分位數的區間訊號：

```python
def generate_regime_signal(margin_series, percentile_series):
    """生成區間訊號"""
    signals = []

    for date in margin_series.index:
        pct = percentile_series.loc[date]
        margin = margin_series.loc[date]

        if pct >= 0.9:
            signal = {
                "date": date,
                "signal": "EXTREME_HIGH",
                "strength": (pct - 0.9) / 0.1,  # 0-1
                "margin": margin,
                "percentile": pct,
                "interpretation": "毛利極端高，均值回歸風險升高",
                "suggested_action": "減持礦業股或觀望"
            }
        elif pct <= 0.1:
            signal = {
                "date": date,
                "signal": "EXTREME_LOW",
                "strength": (0.1 - pct) / 0.1,
                "margin": margin,
                "percentile": pct,
                "interpretation": "毛利極端低，可能接近成本支撐",
                "suggested_action": "關注金價反彈潛力"
            }
        else:
            signal = {
                "date": date,
                "signal": "NEUTRAL",
                "margin": margin,
                "percentile": pct
            }

        signals.append(signal)

    return pd.DataFrame(signals)
```

## Step 3: 驅動拆解訊號

區分價格驅動與成本驅動的毛利變化：

```python
def generate_driver_signal(price_series, cost_series, margin_series, lookback=3):
    """生成驅動拆解訊號"""
    signals = []

    for i in range(lookback, len(margin_series)):
        date = margin_series.index[i]

        price_change = (price_series.iloc[i] / price_series.iloc[i-lookback]) - 1
        cost_change = (cost_series.iloc[i] / cost_series.iloc[i-lookback]) - 1
        margin_change = margin_series.iloc[i] - margin_series.iloc[i-lookback]

        # 判斷主要驅動因素
        if margin_change > 0.05:  # 毛利率提升超過 5 個百分點
            if price_change > 0.1 and cost_change < 0.05:
                driver = "PRICE_RALLY"
                quality = "HIGH"  # 價格驅動的毛利較可持續
            elif cost_change < -0.05:
                driver = "COST_DECLINE"
                quality = "MEDIUM"  # 成本下降可能是暫時的
            else:
                driver = "MIXED_IMPROVEMENT"
                quality = "MEDIUM"
        elif margin_change < -0.05:
            if price_change < -0.1:
                driver = "PRICE_DROP"
                quality = "LOW"
            elif cost_change > 0.1:
                driver = "COST_INFLATION"
                quality = "LOW"
            else:
                driver = "MIXED_DETERIORATION"
                quality = "LOW"
        else:
            driver = "STABLE"
            quality = "NEUTRAL"

        signals.append({
            "date": date,
            "margin_change": margin_change,
            "price_change": price_change,
            "cost_change": cost_change,
            "driver": driver,
            "quality": quality
        })

    return pd.DataFrame(signals)
```

## Step 4: 事件研究訊號

標記極端事件並計算前瞻報酬：

```python
import yfinance as yf

def event_study(extreme_dates: list, etf_ticker: str = "GDX",
                horizons: list = [63, 126, 252]):
    """極端毛利事件的前瞻報酬研究"""

    # 取得 ETF 價格
    etf = yf.download(etf_ticker, start="2010-01-01")['Adj Close']

    results = []
    for event_date in extreme_dates:
        if event_date not in etf.index:
            continue

        event_idx = etf.index.get_loc(event_date)
        event_price = etf.iloc[event_idx]

        forward_returns = {}
        for h in horizons:
            if event_idx + h < len(etf):
                future_price = etf.iloc[event_idx + h]
                forward_returns[f"{h}d_return"] = (future_price / event_price) - 1

        results.append({
            "event_date": event_date,
            **forward_returns
        })

    df = pd.DataFrame(results)

    # 彙總統計
    summary = {
        "n_events": len(df),
        "avg_returns": {
            col: df[col].mean() for col in df.columns if col != "event_date"
        },
        "median_returns": {
            col: df[col].median() for col in df.columns if col != "event_date"
        },
        "win_rate": {
            col: (df[col] > 0).mean() for col in df.columns if col != "event_date"
        }
    }

    return df, summary
```

## Step 5: 相對強弱訊號

比較不同礦業的毛利率表現：

```python
def relative_margin_ranking(margins_df: pd.DataFrame):
    """生成相對毛利率排名訊號"""

    # 最新排名
    latest = margins_df.iloc[-1].sort_values(ascending=False)

    # 過去 4 季變化
    change_4q = margins_df.iloc[-1] - margins_df.iloc[-4]

    rankings = []
    for miner in latest.index:
        rankings.append({
            "miner": miner,
            "current_margin": latest[miner],
            "rank": list(latest.index).index(miner) + 1,
            "margin_change_4q": change_4q[miner],
            "signal": "OUTPERFORM" if change_4q[miner] > 0.05 else (
                "UNDERPERFORM" if change_4q[miner] < -0.05 else "NEUTRAL"
            )
        })

    return pd.DataFrame(rankings)
```

## Step 6: 資本週期訊號

結合毛利率與資本開支趨勢：

```python
def capital_cycle_signal(margin_series, capex_series=None):
    """
    資本週期訊號

    邏輯：
    1. 高毛利 + 低資本開支 → 早期擴張（看多）
    2. 高毛利 + 高資本開支 → 週期高峰（謹慎）
    3. 低毛利 + 高資本開支 → 產能過剩（看空）
    4. 低毛利 + 低資本開支 → 觸底（潛在機會）
    """

    margin_pct = margin_series.rank(pct=True).iloc[-1]

    # 若無資本開支數據，僅用毛利率判斷
    if capex_series is None:
        if margin_pct > 0.8:
            return {
                "phase": "LATE_CYCLE_WARNING",
                "description": "毛利極高，通常引發資本開支週期，注意均值回歸"
            }
        elif margin_pct < 0.2:
            return {
                "phase": "POTENTIAL_BOTTOM",
                "description": "毛利極低，可能接近成本支撐，關注價格反彈"
            }
        else:
            return {
                "phase": "MID_CYCLE",
                "description": "毛利中等，無明顯週期訊號"
            }

    # 有資本開支數據時的完整判斷
    capex_pct = capex_series.rank(pct=True).iloc[-1]

    if margin_pct > 0.7 and capex_pct < 0.3:
        return {"phase": "EARLY_EXPANSION", "signal": "BULLISH"}
    elif margin_pct > 0.7 and capex_pct > 0.7:
        return {"phase": "CYCLE_PEAK", "signal": "CAUTIOUS"}
    elif margin_pct < 0.3 and capex_pct > 0.7:
        return {"phase": "OVERCAPACITY", "signal": "BEARISH"}
    elif margin_pct < 0.3 and capex_pct < 0.3:
        return {"phase": "CYCLE_TROUGH", "signal": "WATCH_FOR_TURN"}
    else:
        return {"phase": "MID_CYCLE", "signal": "NEUTRAL"}
```

## Step 7: 輸出訊號報告

```python
def generate_signal_report(metal: str, basket_margin: pd.Series,
                           percentile_series: pd.Series,
                           miner_margins: pd.DataFrame = None):
    """生成完整訊號報告"""

    report = {
        "skill": "compute_precious_miner_margin_proxy",
        "metal": metal,
        "generated_at": datetime.now().isoformat(),

        "regime_signal": generate_regime_signal(
            basket_margin, percentile_series
        ).iloc[-1].to_dict(),

        "capital_cycle": capital_cycle_signal(basket_margin),

        "recommended_actions": []
    }

    # 根據訊號生成建議
    regime = report["regime_signal"]["signal"]
    if regime == "EXTREME_HIGH":
        report["recommended_actions"].extend([
            "檢視 GDX/GDXJ 相對 GLD 的強弱",
            "監控資本開支公告與併購活動",
            "考慮減持或對沖礦業股曝險"
        ])
    elif regime == "EXTREME_LOW":
        report["recommended_actions"].extend([
            "關注金價是否觸及成本支撐",
            "監控邊際礦業減產公告",
            "考慮逆勢佈局機會"
        ])

    if miner_margins is not None:
        report["relative_ranking"] = relative_margin_ranking(miner_margins).to_dict('records')

    return report
```

## Step 8: 整合執行

完整訊號生成流程：

```bash
python scripts/margin_calculator.py \
  --metal gold \
  --generate-signals \
  --event-study \
  --output signals.json
```

</process>

<success_criteria>
訊號生成完成時應產出：

- [ ] 極端區間訊號（EXTREME_HIGH / EXTREME_LOW）
- [ ] 驅動拆解訊號（PRICE_RALLY / COST_DECLINE 等）
- [ ] 事件研究結果（極端事件的前瞻報酬統計）
- [ ] 相對強弱排名（若有多個礦業）
- [ ] 資本週期訊號
- [ ] 綜合建議行動
- [ ] JSON 格式的訊號報告
</success_criteria>

<risk_notes>
**訊號使用注意事項**：

1. **滯後性**：成本數據滯後 1-2 個月，短期訊號可能失真
2. **樣本偏誤**：極端事件樣本小，前瞻報酬統計可能不穩健
3. **結構變化**：成本結構可能因技術/併購而改變，歷史分位數需定期校驗
4. **非充分條件**：毛利率僅為諸多因子之一，需結合其他分析
</risk_notes>
