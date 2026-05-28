# Custom Perspectives

> 根據專案需求自訂規劃視角

## 自訂視角流程

使用 `--custom` 時的互動流程：

```bash
/multi-plan --custom 建立支付系統
```

```
> 請選擇或自訂視角（預設使用 4 個）：

預設視角：
1. ☑ architect    - 系統架構師
2. ☑ risk-analyst - 風險分析師
3. ☑ estimator    - 估算專家
4. ☑ ux-advocate  - UX 倡導者

額外視角：
5. ☐ security     - 安全專家
6. ☐ ops          - 維運專家
7. ☐ data         - 資料專家
8. ☐ compliance   - 合規專家

> 輸入數字切換選擇，或輸入 'c' 創建新視角
> 完成後輸入 'done'
```

## 額外視角定義

### security - 安全專家

```yaml
id: security
name: 安全專家
focus:
  - 認證授權設計
  - 資料保護
  - OWASP 風險
  - 安全合規
  - 威脅建模
prompt: |
  你是一位安全專家。針對「{feature}」功能，請進行安全規劃：

  1. **認證授權**：需要什麼樣的認證和授權機制？
  2. **資料保護**：敏感資料如何保護？
  3. **威脅建模**：可能的攻擊向量有哪些？
  4. **安全控制**：需要實施哪些安全控制？
  5. **合規要求**：有哪些安全合規需求？
```

### ops - 維運專家

```yaml
id: ops
name: 維運專家
focus:
  - 部署策略
  - 監控告警
  - 擴展策略
  - 災難復原
  - 維護計劃
prompt: |
  你是一位維運專家。針對「{feature}」功能，請進行維運規劃：

  1. **部署策略**：如何部署此功能？
  2. **監控設計**：需要監控什麼指標？
  3. **擴展策略**：如何應對流量增長？
  4. **災難復原**：備援和恢復策略
  5. **維護計劃**：日常維護需求
```

### data - 資料專家

```yaml
id: data
name: 資料專家
focus:
  - 資料模型
  - 儲存策略
  - 資料遷移
  - 效能優化
  - 資料一致性
prompt: |
  你是一位資料專家。針對「{feature}」功能，請進行資料規劃：

  1. **資料模型**：需要什麼資料結構？
  2. **儲存選擇**：使用什麼資料庫？為什麼？
  3. **遷移策略**：現有資料如何遷移？
  4. **效能考量**：查詢效能如何優化？
  5. **一致性**：如何保證資料一致性？
```

### compliance - 合規專家

```yaml
id: compliance
name: 合規專家
focus:
  - 法規要求
  - 隱私保護
  - 審計追蹤
  - 資料留存
  - 合規文檔
prompt: |
  你是一位合規專家。針對「{feature}」功能，請進行合規規劃：

  1. **法規要求**：需要遵守哪些法規？
  2. **隱私保護**：GDPR/個資法合規需求
  3. **審計追蹤**：需要記錄什麼操作？
  4. **資料留存**：資料保留和刪除政策
  5. **文檔需求**：需要準備哪些合規文檔？
```

## 創建自訂視角

選擇 'c' 進入創建模式：

```
> 創建新視角

請輸入視角 ID（英文小寫）：
> mobile-expert

請輸入視角名稱：
> 移動端專家

請輸入聚焦領域（逗號分隔）：
> 行動 App 體驗, 離線支援, 推播通知, 效能優化

請輸入 Prompt 模板（輸入 'END' 結束）：
> 你是一位移動端專家...
> END

✅ 視角 'mobile-expert' 已創建
```

## 視角組合範例

### 金融支付專案

```bash
/multi-plan --custom
# 選擇：architect, security, compliance, estimator
```

### 高流量系統

```bash
/multi-plan --custom
# 選擇：architect, ops, data, risk-analyst
```

### 用戶導向產品

```bash
/multi-plan --custom
# 選擇：ux-advocate, architect, estimator, data
```

## 保存視角配置

自訂視角配置會保存在：

```
.claude/memory/plans/perspectives/
├── custom-{id}.yaml    # 自訂視角定義
└── presets/
    ├── fintech.yaml    # 金融科技預設
    └── high-traffic.yaml
```

## 視角選擇原則

| 專案類型 | 推薦視角 |
|----------|----------|
| 核心業務 | architect, risk-analyst, security |
| 快速原型 | architect, ux-advocate |
| 資料密集 | architect, data, ops |
| 合規敏感 | security, compliance, risk-analyst |
| 高可用 | architect, ops, risk-analyst |
