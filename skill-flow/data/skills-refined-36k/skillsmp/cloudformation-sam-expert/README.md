# CloudFormation/SAM Expert Skill

## 📖 關於這個 Skill

這是 AgentCoreNexus 專案的第一個 Cline Skill，整合了專案在 AWS CloudFormation 和 SAM 開發中累積的專業知識和最佳實踐。

**創建日期**：2026-01-23  
**狀態**：試驗期（3 個月評估）  
**版本**：1.0.0

---

## 🎯 Skill 涵蓋範圍

### 核心知識領域
- Infrastructure as Code (IaC) 強制執行原則
- CloudFormation/SAM stack 管理
- 跨 stack 依賴和引用
- 部署策略（標準、金絲雀、藍綠）
- 故障排除和診斷
- 安全和權限配置
- 成本優化策略

### 知識來源
整合自專案的實戰文檔：
- `.clinerules/deployment/stack-management-best-practices.md`
- `.clinerules/deployment/IaC-enforcement-summary.md`
- `docs/deployment-guide.md`
- `docs/STACK_MANAGEMENT.md`
- 多個 dev-reports/ 中的教訓

---

## 🚀 如何使用

### 自動激活

當你的請求符合以下場景，Cline 會自動激活這個 Skill：

**觸發關鍵詞**：
- "設計 infrastructure"、"創建 stack"
- "跨 stack"、"cross-stack"、"ImportValue"
- "部署失敗"、"troubleshoot deployment"
- "CloudFormation"、"SAM"、"template.yaml"
- "IAM policy"、"permissions"、"security"
- "EventBridge"、"Lambda"、"DynamoDB"

**範例請求**：
```
"如何設計一個新的 Lambda stack？"
"跨 stack 引用 EventBus 的最佳方式？"
"Stack 部署失敗，如何診斷？"
"Lambda 需要什麼 IAM 權限訪問 DynamoDB？"
```

### 手動激活（如需要）

如果 Skill 沒有自動激活，可以明確指示：
```
"使用 cloudformation-sam-expert skill 幫我..."
```

---

## 📚 Skill 結構

```
cloudformation-sam-expert/
├── SKILL.md                           # 主要指令和知識
├── README.md                          # 本文件
├── docs/
│   ├── cross-stack-references.md      # 跨 stack 引用詳解
│   ├── resource-management.md         # 資源生命週期管理
│   ├── deployment-strategies.md       # 部署策略和模式
│   ├── troubleshooting.md             # 故障排除手冊
│   └── security-best-practices.md     # 安全配置指南
└── templates/
    ├── basic-lambda-stack.yaml        # 基礎 stack 範例
    ├── multi-stack-example.yaml       # 多 stack 整合範例
    └── eventbridge-integration.yaml   # EventBridge 整合範例
```

---

## 🧪 測試計劃

### Week 1-2：初期測試

**目標**：驗證 Skill 正確激活

**測試場景**：
1. **Stack 設計請求**
   - "我要創建一個新的 Lambda stack"
   - 預期：Skill 激活，提供設計指導

2. **跨 stack 問題**
   - "如何讓 ai-processor 使用 telegram-adapter 的 EventBus？"
   - 預期：Skill 激活，提供 Export/Import 指導

3. **部署問題**
   - "Stack 卡在 UPDATE_ROLLBACK_FAILED"
   - 預期：Skill 激活，提供故障排除步驟

4. **不應激活場景**（負面測試）
   - "如何測試 Python 代碼？"
   - 預期：Skill 不激活（這是測試相關，不是 IaC）

**記錄指標**：
- 激活次數
- 激活準確性（該激活時激活，不該激活時不激活）
- 提供資訊的有用性

### Week 3-4：實際使用

**真實場景測試**：
- 實際創建新 stack 時使用
- 遇到部署問題時使用
- 需要架構決策時使用

**記錄**：
- 使用頻率
- 解決問題的效果
- vs 直接查閱文檔的比較

---

## 📊 評估標準（3 個月後）

### 定量指標

1. **使用頻率**
   - 目標：> 5 次/月被激活
   - 測量：檢查 Cline 日誌

2. **激活準確性**
   - 目標：誤觸發率 < 10%
   - 測量：記錄不適當的激活

3. **觸發率**
   - 目標：該激活時的觸發率 > 80%
   - 測量：記錄應該激活但沒有的情況

### 定性評估

**問題清單**：
1. **是否真的更有幫助**？
   - Skill 提供的指導 vs 直接說"參考 stack-management-best-practices.md"
   - 哪個更快解決問題？

2. **維護成本是否合理**？
   - 文檔更新時同步 Skill 的時間成本
   - 是否值得持續投入？

3. **是否應該擴展**？
   - 如果這個 Skill 有效，是否創建更多？
   - 如果無效，是否刪除並回到文檔引用？

### 決策矩陣

| 指標 | 通過 | 失敗 | 下一步 |
|------|------|------|--------|
| 使用頻率 > 5/月 | ✅ | ❌ | → 評估有用性 |
| 激活準確性 > 90% | ✅ | ❌ | → 調整描述 |
| 真的更有幫助 | ✅ | ❌ | → 評估維護成本 |
| 維護成本可接受 | ✅ | ❌ | → 考慮刪除 |

**結論**：
- **全部 ✅** → 擴展更多 Skills（優先級 #2: Lambda+EventBridge 架構）
- **部分 ✅** → 調整和優化當前 Skill
- **全部 ❌** → 刪除 Skill，回到文檔引用方式

---

## 🔧 維護指南

### 何時需要更新 Skill

**觸發事件**：
1. `.clinerules/deployment/` 文檔更新
2. `docs/STACK_MANAGEMENT.md` 或 `deployment-guide.md` 更新
3. 發現新的 CloudFormation 最佳實踐
4. 專案累積新的實戰經驗
5. AWS 發布新的 SAM 功能

**更新頻率估計**：每月 1-2 次

### 更新流程

1. **識別變更**
   - 哪個源文檔更新了？
   - 影響 Skill 的哪個部分？

2. **更新 Skill**
   - 更新 SKILL.md（如果核心原則變更）
   - 更新對應的 docs/（如果細節變更）
   - 更新 templates/（如果範例需要調整）

3. **測試驗證**
   - 確認 Skill 仍能正確激活
   - 驗證新知識被正確整合

4. **記錄變更**
   - 在 Git commit 中記錄
   - 更新 README.md 的版本號

### 同步檢查清單

**月度檢查**（每月第一個週五）：
- [ ] 檢查 `.clinerules/deployment/` 是否有更新
- [ ] 檢查 `docs/` 相關文件是否有更新
- [ ] 審查最近的 dev-reports/
- [ ] 如有更新，同步到 Skill
- [ ] 測試 Skill 激活

---

## 📈 成功案例（待記錄）

**使用此區域記錄 Skill 的成功應用**：

### 範例格式

**日期**：2026-XX-XX  
**場景**：創建新的 Lambda stack  
**Skill 貢獻**：
- 自動激活 ✅
- 提供完整的 template 結構
- 避免了常見的 Permission 錯誤
**節省時間**：估計 30 分鐘

---

## 🚫 失敗案例（待記錄）

**使用此區域記錄 Skill 的問題**：

### 範例格式

**日期**：2026-XX-XX  
**問題**：應該激活但沒有  
**原因**：描述不夠匹配用戶的用語  
**解決**：調整 description 添加關鍵詞

---

## 🔗 相關資源

### 專案內部
- `.clinerules/README.md` - Cline 配置總覽
- `.clinerules/workflows/deploy-lambda.md` - 部署 workflow
- `.clinerules/rules/deployment-iac.md` - IaC 強制規則

### Cline 官方
- [Skills 文檔](https://docs.cline.bot/features/skills)
- [Skills 最佳實踐](https://docs.cline.bot/features/skills#best-practices)

### AWS 官方
- [CloudFormation User Guide](https://docs.aws.amazon.com/cloudformation/)
- [SAM Developer Guide](https://docs.aws.amazon.com/serverless-application-model/)

---

## 💡 給未來維護者的提醒

1. **保持簡單**
   - 不要過度複雜化
   - 如果文檔引用就足夠，不要強行使用 Skill

2. **定期評估**
   - 3 個月後認真評估價值
   - 如果沒有帶來顯著好處，考慮刪除

3. **文檔優先**
   - Skill 是輔助，文檔才是 source of truth
   - 保持 `.clinerules/deployment/` 和 `docs/` 完整

4. **記錄使用**
   - 記錄成功和失敗案例
   - 這些數據對評估至關重要

---

**版本歷史**：
- v1.0.0 (2026-01-23) - 初始創建，試驗期開始