# 資源管理和生命週期

## 🎯 資源生命週期管理

CloudFormation 管理資源的整個生命週期：創建、更新、刪除。理解每個階段的行為至關重要。

---

## 🛡️ DeletionPolicy

### 三種策略

**Delete**（默認）：
```yaml
MyResource:
  Type: AWS::S3::Bucket
  DeletionPolicy: Delete  # Stack 刪除時，資源也刪除
```

**Retain**（保留）：
```yaml
MyTable:
  Type: AWS::DynamoDB::Table
  DeletionPolicy: Retain  # Stack 刪除時，資源保留
```

**Snapshot**（快照）：
```yaml
MyDatabase:
  Type: AWS::RDS::DBInstance
  DeletionPolicy: Snapshot  # 刪除前創建快照
```

### 何時使用 Retain

**應該使用**：
- ✅ DynamoDB 表（包含用戶數據）
- ✅ S3 bucket（包含上傳文件）
- ✅ CloudWatch Logs（審計需求）
- ✅ RDS 數據庫（關鍵數據）

**避免使用**：
- ❌ 開發/測試資源
- ❌ 可重新生成的資源
- ❌ Lambda 函數（代碼在 Git 中）
- ❌ EventBridge rules（配置在 template 中）

### Retain 的後果

**問題**：
```yaml
# 舊 stack 使用 Retain
OldStack:
  MyTable:
    DeletionPolicy: Retain

# 刪除舊 stack 後，table 仍存在
# 新 stack 無法創建同名 table
NewStack:
  MyTable:  # ❌ 錯誤：Resource already exists
```

**解決方案**：
```yaml
# 選項 1: 新 stack 使用不同名稱
TableName: !Sub '${AWS::StackName}-users-v2'

# 選項 2: 引用現有 table（不創建）
Environment:
  Variables:
    TABLE_NAME: 'existing-table-name'  # 固定值

# 選項 3: 手動刪除舊 table 後重新部署
```

---

## 🔄 UpdateReplacePolicy

**與 DeletionPolicy 的區別**：
- DeletionPolicy：Stack 刪除時
- UpdateReplacePolicy：資源**更新需要替換**時

**範例**：
```yaml
MyTable:
  Type: AWS::DynamoDB::Table
  DeletionPolicy: Retain  # Stack 刪除時保留
  UpdateReplacePolicy: Retain  # 更新替換時也保留
```

**何時觸發替換**：
- 改變 DynamoDB table 的 AttributeDefinitions
- 改變 S3 bucket 的 BucketName
- 其他不可變屬性的修改

---

## 🏷️ 資源標記（Tagging）

### 標準標記策略

**必須的標記**：
```yaml
Tags:
  - Key: Project
    Value: AgentCoreNexus
  - Key: Component
    Value: ai-processor
  - Key: Environment
    Value: !Ref Environment
  - Key: ManagedBy
    Value: SAM
  - Key: CostCenter
    Value: Engineering
```

### 標記的好處

**成本分配**：
- 按 Project 追蹤成本
- 按 Component 細分費用
- 按 Environment 區分開發/生產成本

**資源發現**：
```bash
# 找出所有 ai-processor 資源
aws resourcegroupstaggingapi get-resources \
  --tag-filters Key=Component,Values=ai-processor

# 找出所有專案資源
aws resourcegroupstaggingapi get-resources \
  --tag-filters Key=Project,Values=AgentCoreNexus
```

**合規性**：
- 自動化合規掃描
- 審計追蹤
- 組織策略執行

---

## 🔍 Stack Drift 檢測

### 什麼是 Drift

**Drift = 實際配置 ≠ Template 定義**

**常見原因**：
- 手動修改資源（違反 IaC）
- Console 操作
- 其他自動化工具修改

### 檢測 Drift

```bash
# 啟動 drift 檢測
aws cloudformation detect-stack-drift --stack-name STACK_NAME

# 查看結果
aws cloudformation describe-stack-resource-drifts \
  --stack-name STACK_NAME \
  --stack-resource-drift-status-filters MODIFIED DELETED
```

### 修復 Drift

**步驟**：
1. 識別 drift 的資源
2. 決定保留哪個：
   - Template（理想狀態）→ 重新部署
   - 實際配置（需要的變更）→ 更新 template
3. 執行修復
4. 再次檢測驗證

---

## 📦 資源依賴管理

### 自動依賴

CloudFormation 自動推斷大部分依賴：
```yaml
MyFunction:
  Properties:
    Environment:
      Variables:
        TABLE_NAME: !Ref MyTable  # 自動依賴 MyTable
```

### 明確依賴（DependsOn）

**何時需要**：
- CloudFormation 無法推斷依賴
- 需要特定創建順序
- 自定義資源依賴

```yaml
MyFunction:
  Type: AWS::Serverless::Function
  DependsOn:
    - MyTable
    - MySecret
```

### 隱式依賴

**通過 !Ref 或 !GetAtt**：
```yaml
# 自動創建依賴關係
Resource: !GetAtt MyTable.Arn
FunctionName: !Ref MyFunction
```

---

## 🔐 資源配置最佳實踐

### Lambda 配置

**內存和超時**：
```yaml
ProcessorFunction:
  Type: AWS::Serverless::Function
  Properties:
    MemorySize: 1024  # 基於實際需求
    Timeout: 300  # AI 處理需要較長時間
    ReservedConcurrentExecutions: 10  # 成本控制
```

**環境變數**：
```yaml
Environment:
  Variables:
    # 必要配置
    EVENT_BUS_NAME: !ImportValue stack-EventBusName
    BEDROCK_MODEL_ID: anthropic.claude-3-5-sonnet-20241022-v2:0
    LOG_LEVEL: INFO
    
    # 功能開關
    BROWSER_ENABLED: 'true'
    MEMORY_ENABLED: 'true'
```

### DynamoDB 配置

**點播 vs 預配置**：
```yaml
# 流量不可預測 → 點播
MyTable:
  Type: AWS::DynamoDB::Table
  Properties:
    BillingMode: PAY_PER_REQUEST

# 流量穩定 → 預配置（更便宜）
MyTable:
  Type: AWS::DynamoDB::Table
  Properties:
    BillingMode: PROVISIONED
    ProvisionedThroughput:
      ReadCapacityUnits: 5
      WriteCapacityUnits: 5
```

**Point-in-Time Recovery**：
```yaml
# 重要表必須啟用
PointInTimeRecoverySpecification:
  PointInTimeRecoveryEnabled: true
```

### S3 配置

**加密**：
```yaml
BucketEncryption:
  ServerSideEncryptionConfiguration:
    - ServerSideEncryptionByDefault:
        SSEAlgorithm: AES256
```

**版本控制**：
```yaml
VersioningConfiguration:
  Status: Enabled  # 重要數據必須
```

**CORS（Web 應用）**：
```yaml
CorsConfiguration:
  CorsRules:
    - AllowedOrigins: ['*']
      AllowedMethods: [PUT, POST, GET, HEAD]
      AllowedHeaders: ['*']
      ExposedHeaders: [ETag]
      MaxAge: 3000
```

---

## 🔄 資源更新策略

### 無停機時間更新

**Lambda 代碼**：
- ✅ 無停機（藍綠部署）
- 新版本創建，流量切換

**Lambda 配置**：
- ✅ 無停機（環境變數）
- ⚠️ 短暫停機（memory/timeout）

**API Gateway**：
- ⚠️ 可能短暫停機
- 使用 canary 部署減輕影響

### 有風險的更新

**需要替換的變更**：
- ❌ DynamoDB table schema（AttributeDefinitions）
- ❌ S3 bucket name
- ❌ IAM role name（如果硬編碼）

**策略**：
1. 評估影響
2. 創建平行資源
3. 遷移數據
4. 切換流量
5. 刪除舊資源

---

## 📊 資源監控

### CloudWatch Metrics

**Lambda 關鍵指標**：
- Invocations（調用次數）
- Errors（錯誤次數）
- Duration（執行時間）
- Throttles（限流次數）
- ConcurrentExecutions（並發執行）

**DynamoDB 關鍵指標**：
- ConsumedReadCapacityUnits
- ConsumedWriteCapacityUnits
- UserErrors
- SystemErrors

### 告警設置

**Lambda 錯誤率**：
```yaml
ErrorRateAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    MetricName: Errors
    Namespace: AWS/Lambda
    Statistic: Sum
    Period: 300
    EvaluationPeriods: 2
    Threshold: 10
    ComparisonOperator: GreaterThanThreshold
```

---

## 🧹 資源清理

### 定期審查

**月度檢查**：
- [ ] 識別未使用資源
- [ ] 檢查 CloudWatch Logs 保留期
- [ ] 審查 S3 生命週期規則
- [ ] 驗證 Lambda 併發限制

### 自動清理

**Lambda Logs**：
```yaml
# 自動刪除舊日誌
LogGroup:
  Properties:
    RetentionInDays: 14
```

**S3 舊對象**：
```yaml
# 自動轉移或刪除
LifecycleConfiguration:
  Rules:
    - Id: DeleteOldObjects
      Status: Enabled
      ExpirationInDays: 90
```

---

## 💡 專家提示

### 1. 使用 Parameters 處理環境差異

```yaml
Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]
  
  LambdaMemory:
    Type: Number
    Description: Lambda memory (MB)
    Default: 256

Mappings:
  EnvironmentConfig:
    dev:
      LogRetention: 7
    prod:
      LogRetention: 30

Resources:
  MyFunction:
    Properties:
      MemorySize: !Ref LambdaMemory
  
  LogGroup:
    Properties:
      RetentionInDays: !FindInMap
        - EnvironmentConfig
        - !Ref Environment
        - LogRetention
```

### 2. 使用 Conditions 控制資源創建

```yaml
Conditions:
  CreateProdResources: !Equals [!Ref Environment, 'prod']

Resources:
  ProductionAlarm:
    Type: AWS::CloudWatch::Alarm
    Condition: CreateProdResources  # 只在 prod 創建
```

### 3. 資源命名策略

```yaml
# ✅ 動態命名
TableName: !Sub '${AWS::StackName}-users'
BucketName: !Sub '${AWS::StackName}-attachments-${AWS::AccountId}'

# ❌ 靜態命名（部署失敗風險）
TableName: 'users'
```

---

## ⚠️ 常見陷阱

### 1. 忘記設置 DeletionPolicy

**風險**：重要數據意外刪除

**解決**：關鍵資源必須明確設置
```yaml
UserDataTable:
  DeletionPolicy: Retain
  UpdateReplacePolicy: Retain
```

### 2. 過度使用 Retain

**問題**：
- Stack 刪除後資源孤立
- 重新部署時名稱衝突
- 資源管理混亂

**平衡**：
- 只對真正重要的數據使用 Retain
- 記錄哪些資源使用了 Retain
- 定期審查 orphaned 資源

### 3. 忽略資源限制

**AWS 限制**：
- 每個 region 的 stack 數量
- 每個 stack 的資源數量（500）
- Export 名稱長度（255 字符）

**監控**：
```bash
# 檢查 stack 資源數量
aws cloudformation describe-stack-resources \
  --stack-name STACK_NAME \
  --query 'length(StackResources)'
```

---

## 🔗 相關文檔

- [SKILL.md](../SKILL.md) - 返回主文檔
- [跨 Stack 引用](cross-stack-references.md)
- [部署策略](deployment-strategies.md)