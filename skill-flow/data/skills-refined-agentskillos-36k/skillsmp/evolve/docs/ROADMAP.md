# Self-Evolving Agent Roadmap

> 版本: 2026-01-12 | 基於競品分析與專案審查制定

## 當前狀態 (v4.2.0)

### 已完成

- [x] 原子化架構重構 (00-05 + 99 模組)
- [x] PDCA 執行循環
- [x] Git-based Memory 系統
- [x] 4 層涌現機制
- [x] CP1-CP5 強制檢查點
- [x] Fallback 降級機制 (4 層)
- [x] 基礎測試框架
- [x] Makefile 自動化
- [x] 競品分析報告

### 待改善

- [x] ~~Memory 系統有結構但缺乏實際數據~~ → 已有 9 筆 learnings
- [x] ~~涌現指標全為零~~ → emergence-metrics.yaml 已有數據
- [ ] 缺乏視覺化工具
- [ ] CP5 尚未被自然觸發（需要真實失敗情境）

---

## Phase 1: 基礎強化 (0-1 月)

> 目標: 「吃自己的狗糧」- 讓系統產生真實數據

### P0 - 立即執行

| 任務 | 狀態 | 說明 |
|------|------|------|
| 創建 lessons/ 目錄 | ✅ 完成 | 支援 CP5 結構化教訓 |
| 整合 CP5 到 SKILL.md | ✅ 完成 | 失敗後驗屍機制 |
| 提交未暫存變更 | ✅ 完成 | v4.2.0 發布 |

### P1 - 本週目標

| 任務 | 優先級 | 預期產出 | 狀態 |
|------|--------|----------|------|
| 用 /evolve 完成真實任務 | 高 | 產生經驗記錄 | ✅ 完成 (changelog, Makefile) |
| 填充 emergence-metrics.yaml | 高 | 基線數據 | ✅ 完成 |
| 填充 skill-metrics/index.md | 中 | 技能效果追蹤 | ✅ 完成 |
| 記錄首個 ADR 決策 | 中 | decisions/001-*.md | ✅ 完成 |

---

## Phase 2: 可視化 (1-3 月)

> 目標: 讓學習過程可見、可追蹤

### MVP 儀表板

```
需求:
- Memory 統計總覽 (learnings/failures/patterns 數量)
- 涌現等級分布圖
- 最近活動時間線
- 技能效果排行榜

技術選型建議:
- 靜態 HTML + Chart.js (最簡單)
- 或 Streamlit (快速原型)
- 或 VS Code Webview (整合度高)
```

### Benchmark 套件

```
需要測量的指標:
- 任務完成率
- 平均迭代次數
- CP5 觸發頻率
- Lesson 泛化率 (applicable_to > 1)
- 重複失敗率
```

---

## Phase 3: 生態整合 (3-6 月)

> 目標: 與主流工具無縫整合

### 整合優先級

| 工具 | 優先級 | 整合方式 |
|------|--------|----------|
| VS Code | P0 | 擴展: Memory 瀏覽器 + 涌現提示 |
| Cursor | P1 | .cursorrules 相容層 |
| Agent SDK | P1 | 導出為獨立 Agent |
| Copilot | P2 | .github/copilot/ 整合 |

### Agent SDK 導出

```
目標: 將 Skill 打包為可獨立部署的 Agent

需要:
- 提取核心邏輯為 Python/TS 模組
- MCP Server 封裝
- 配置檔標準化
```

---

## Phase 4: 智能提升 (6-12 月)

> 目標: 從「能學習」到「會創造」

### GEPA 整合

參考 OpenAI 的 Genetic Pareto 框架:
- 評估 → 反思 → 修訂 → 迭代
- 應用於 Prompt 自動優化
- 整合到知識蒸餾流程

### Multi-Agent 支援

```
場景:
- 主 Agent (規劃) + 執行 Agent (實作)
- 專家 Agent 諮詢 (PAL MCP)
- 跨 Agent Memory 共享

挑戰:
- 記憶衝突解決
- 責任邊界定義
```

### 跨 Agent 記憶共享

```
方案探索:
- Git remote 同步 (最簡單)
- 中央 Memory Server
- P2P 記憶交換協議
```

---

## 成功指標

### Phase 1 完成標準
- [x] Memory 系統有 ≥5 筆真實記錄 (非範例) → ✅ 9 筆 learnings
- [ ] CP5 至少觸發過 2 次 → ⏳ 待自然失敗觸發
- [x] emergence-metrics.yaml 有非零數據 → ✅ 已有基線數據

### Phase 2 完成標準
- [ ] 儀表板 MVP 可運行
- [ ] Benchmark 套件覆蓋 3+ 指標
- [ ] 有文檔說明如何解讀數據

### Phase 3 完成標準
- [ ] VS Code 擴展可安裝使用
- [ ] Agent SDK 導出成功並可執行
- [ ] Cursor 相容性驗證通過

### Phase 4 完成標準
- [ ] GEPA 自動優化展示 case
- [ ] Multi-Agent 協作 demo
- [ ] 記憶共享 POC

---

## 參考資源

- [競品分析報告](./competitor-analysis-2026-01.md)
- [GEPA Paper](https://arxiv.org/abs/xxx)
- [Andrew Ng - Agentic Design Patterns](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-2-reflection/)
- [OpenAI Self-Evolving Agents Cookbook](https://cookbook.openai.com/examples/partners/self_evolving_agents/autonomous_agent_retraining)

---

## 變更記錄

| 日期 | 變更 |
|------|------|
| 2026-01-12 | 初始版本，基於 P0/P1/P2 分析制定 |
| 2026-01-12 | 更新 P1 任務狀態；更新 Phase 1 完成標準進度 |
