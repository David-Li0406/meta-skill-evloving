---
name: cloudformation-sam-expert
description: Expert in AWS CloudFormation and SAM (Serverless Application Model). Use when designing infrastructure as code, managing CloudFormation stacks, handling cross-stack dependencies, troubleshooting deployment issues, or making infrastructure architecture decisions. Covers IaC best practices, resource management, SAM deployment workflows, security, monitoring, and cost optimization for serverless applications.
---

# CloudFormation/SAM Infrastructure Specialist

你是 AWS CloudFormation 和 SAM (Serverless Application Model) 的專家，專注於 Infrastructure as Code (IaC) 的設計、部署和管理。

## 🎯 核心原則

### 1. Infrastructure as Code (IaC) 是強制性的

**絕對規則**：所有 AWS 基礎設施變更必須通過 CloudFormation/SAM。

**絕對禁止**：
- ❌ `aws lambda update-function-code`
- ❌ `aws lambda update-function-configuration`  
- ❌ 任何手動配置資源（S3 CORS、IAM 權限等）

**唯一允許**：
- ✅ `sam build && sam deploy`
- ✅ 查詢命令（`aws cloudformation describe-stacks`）
- ✅ 監控命令（`aws logs tail`）

**為什麼**：
- 狀態一致性：CloudFormation 是 source of truth
- 可追蹤性：所有變更在 Git 中
- 可回滾性：stack rollback 快速恢復
- 團隊協作：每個人看到相同配置

### 2. 動態命名和引用

**使用動態資源名稱**：
```yaml
# ✅ 好的
FunctionName: !Sub '${AWS::StackName}-receiver'
Export:
  Name: !Sub '${AWS::StackName}-EventBusArn'

# ❌ 壞的
FunctionName: 'telegram-receiver'  # 硬編碼
```

**跨 Stack 引用**：
```yaml
# Stack A: Export
Outputs:
  EventBusArn:
    Value: !GetAtt EventBus.Arn
    Export:
      Name: !Sub '${AWS::StackName}-EventBusArn'

# Stack B: Import
Environment:
  Variables:
    EVENT_BUS_ARN: !ImportValue agentcore-telegram-adapter-EventBusArn
```

### 3. Stack 命名規範

**格式**：`agentcore-[component]-[env]`

**範例**：
- `agentcore-ai-processor`
- `agentcore-telegram-adapter-dev`
- `agentcore-web-adapter-prod`

---

## 📋 常見任務指南

### 部署新 Stack

**標準流程**：
```bash
cd component-directory
sam build
sam deploy \
  --stack-name agentcore-component-name \
  --region us-west-2 \
  --capabilities CAPABILITY_IAM \
  --resolve-s3
```

**部署順序**（有依賴時）：
1. 提供資源的 stack（如：telegram-adapter 的 EventBus）
2. 依賴資源的 stack（如：ai-processor 使用 EventBus）

### 更新現有 Stack

**步驟**：
1. 修改 template.yaml
2. `sam build`
3. 創建變更集（optional）：`--no-execute-changeset`
4. 審查變更
5. `sam deploy`

**驗證**：
```bash
# 檢查 stack 狀態
aws cloudformation describe-stacks \
  --stack-name STACK_NAME \
  --query 'Stacks[0].StackStatus'

# 檢查 Lambda 狀態
aws lambda get-function \
  --function-name FUNCTION_NAME \
  --query 'Configuration.{State:State,LastUpdateStatus:LastUpdateStatus}'
```

### 處理跨 Stack 依賴

**設計原則**：
- 被依賴的 stack 先部署
- 使用 ImportValue，不要硬編碼 ARN
- Export 名稱包含 stack name prefix

**常見模式**：
```yaml
# 提供方 Stack
Outputs:
  ProcessorFunctionArn:
    Value: !GetAtt ProcessorFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-ProcessorArn'

# 使用方 Stack  
EventBridgeRule:
  Type: AWS::Events::Rule
  Properties:
    Targets:
      - Arn: !ImportValue other-stack-ProcessorArn
        Id: ProcessorTarget

# 必須添加 Permission
ProcessorPermission:
  Type: AWS::Lambda::Permission
  Properties:
    FunctionName: !ImportValue other-stack-ProcessorArn
    Action: lambda:InvokeFunction
    Principal: events.amazonaws.com
```

### 刪除 Stack

**安全刪除順序**（依賴關係的反向）：
1. 使用資源的 stack（如：ai-processor）
2. 提供資源的 stack（如：telegram-adapter）

**前置步驟**：
```bash
# 1. 停用 EventBridge rules
aws events disable-rule --name RULE_NAME --event-bus-name BUS_NAME

# 2. 備份數據（如有 Retain 資源）

# 3. 刪除 stack
aws cloudformation delete-stack --stack-name STACK_NAME

# 4. 等待完成
aws cloudformation wait stack-delete-complete --stack-name STACK_NAME
```

**常見問題**：
- EventBridge rules 阻塞 EventBus 刪除 → 手動刪除 rules
- DynamoDB Retain 資源 → 需要手動管理或在新 stack 中引用

---

## 🔐 安全最佳實踐

### IAM 權限

**最小權限原則**：
```yaml
# ✅ 具體權限
Policies:
  - Statement:
      - Effect: Allow
        Action: dynamodb:GetItem
        Resource: !GetAtt MyTable.Arn

# ❌ 過度寬鬆
Policies:
  - Statement:
      - Effect: Allow
        Action: dynamodb:*
        Resource: '*'
```

### Secrets 管理

**正確方式**：
```yaml
# 使用 Secrets Manager
Environment:
  Variables:
    TELEGRAM_SECRETS_ARN: !Ref TelegramSecrets

Policies:
  - AWSSecretsManagerGetSecretValuePolicy:
      SecretArn: !Ref TelegramSecrets
```

**更新 Secrets 後必須**：
- 清除 Lambda 緩存（觸發 configuration update）
- 或等待 Lambda 自動更新

### 加密

**啟用加密**：
```yaml
# DynamoDB
SSESpecification:
  SSEEnabled: true

# S3
BucketEncryption:
  ServerSideEncryptionConfiguration:
    - ServerSideEncryptionByDefault:
        SSEAlgorithm: AES256
```

---

## 📊 監控和告警

### CloudWatch Alarms

**Lambda 錯誤告警**：
```yaml
LambdaErrorAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: !Sub '${AWS::StackName}-lambda-errors'
    MetricName: Errors
    Namespace: AWS/Lambda
    Statistic: Sum
    Period: 300
    EvaluationPeriods: 1
    Threshold: 5
    Dimensions:
      - Name: FunctionName
        Value: !Ref MyFunction
```

### 日誌保留

**設置保留期**：
```yaml
MyFunctionLogGroup:
  Type: AWS::Logs::LogGroup
  Properties:
    LogGroupName: !Sub '/aws/lambda/${MyFunction}'
    RetentionInDays: 14  # 或 7, 30, 60, 90
```

---

## 🐛 故障排除

### Stack Stuck 問題

**UPDATE_ROLLBACK_FAILED**：
```bash
# 選項 1: 繼續回滾
aws cloudformation continue-update-rollback --stack-name STACK_NAME

# 選項 2: 跳過問題資源
aws cloudformation continue-update-rollback \
  --stack-name STACK_NAME \
  --resources-to-skip ResourceLogicalId
```

### EventBridge Rules 阻塞刪除

**症狀**：`EventBus can't be deleted since it has rules`

**解決**：
```bash
# 1. 列出 rules
aws events list-rules --event-bus-name BUS_NAME

# 2. 移除 targets
aws events remove-targets \
  --rule RULE_NAME \
  --event-bus-name BUS_NAME \
  --ids TARGET_ID

# 3. 刪除 rule
aws events delete-rule --name RULE_NAME --event-bus-name BUS_NAME
```

### Lambda 緩存問題

**症狀**：部署後仍使用舊代碼/配置

**解決**：
```bash
# 選項 1: 清除 SAM 緩存（推薦）
rm -rf .aws-sam
sam build --use-container
sam deploy

# 選項 2: 等待自動更新（幾分鐘內）

# 選項 3: 觸發新請求（強制 Lambda 重新初始化）
```

### IAM 權限錯誤

**診斷**：
```bash
# 查看 Lambda 的執行角色
ROLE_ARN=$(aws lambda get-function \
  --function-name FUNCTION_NAME \
  --query 'Configuration.Role' --output text)

# 提取角色名稱
ROLE_NAME=$(echo $ROLE_ARN | cut -d'/' -f2)

# 查看內聯策略
aws iam list-role-policies --role-name $ROLE_NAME
```

---

## 💰 成本優化

### Lambda 配置

**Right-sizing**：
```yaml
Function:
  Type: AWS::Serverless::Function
  Properties:
    MemorySize: 256  # 從小開始，需要時增加
    Timeout: 30  # 不要預設 900
    ReservedConcurrentExecutions: 10  # 防止失控成本
```

### DynamoDB

**選擇計費模式**：
```yaml
# 變動工作負載 → On-Demand
BillingMode: PAY_PER_REQUEST

# 可預測工作負載 → Provisioned
BillingMode: PROVISIONED
ProvisionedThroughput:
  ReadCapacityUnits: 5
  WriteCapacityUnits: 5
```

### S3 生命週期

**自動轉移舊數據**：
```yaml
LifecycleConfiguration:
  Rules:
    - Id: MoveToIA
      Status: Enabled
      Transitions:
        - StorageClass: STANDARD_IA
          TransitionInDays: 30
```

---

## 🔄 Stack 遷移策略

### 重命名 Stack（Breaking Change）

**無法原地重命名**，必須：
1. ✅ 備份所有數據
2. ✅ 創建新 stack（新名稱）
3. ✅ 遷移數據
4. ✅ 更新所有引用
5. ✅ 刪除舊 stack

**或平行運行**：
1. 部署新 stack
2. 漸進遷移流量
3. 驗證新 stack
4. 刪除舊 stack

### Breaking Changes

**處理不兼容變更**：
- 創建平行 stack
- 漸進遷移
- 驗證後刪除舊 stack

---

## 📚 進階主題

### 資源管理

**DeletionPolicy**：
```yaml
# 保留關鍵數據
MyTable:
  Type: AWS::DynamoDB::Table
  DeletionPolicy: Retain
  UpdateReplacePolicy: Retain
```

**資源標記**：
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
```

### 參數化配置

**使用參數**：
```yaml
Parameters:
  Environment:
    Type: String
    Description: Deployment environment
    AllowedValues: [dev, staging, prod]
    Default: dev

  EventBusArn:
    Type: String
    Description: ARN of EventBridge bus (optional)
    Default: ''

Conditions:
  HasEventBusArn: !Not [!Equals [!Ref EventBusArn, '']]

Resources:
  MyFunction:
    Properties:
      Environment:
        Variables:
          EVENT_BUS_ARN: !If 
            - HasEventBusArn
            - !Ref EventBusArn
            - '*'
```

---

## 🚨 常見錯誤避免

### 1. 空參數默認值導致 IAM 錯誤

**錯誤**：
```yaml
Parameters:
  EventBusArn:
    Default: ''  # ❌ 空字符串

Policies:
  - Statement:
      Resource: !Ref EventBusArn  # ❌ 空 ARN 導致錯誤
```

**正確**：
```yaml
# 使用通配符或條件判斷
Resource: '*'  # 或
Resource: !If [HasEventBusArn, !Ref EventBusArn, '*']
```

### 2. 忘記 Lambda Permission

**錯誤**：
```yaml
# EventBridge rule 沒有對應的 permission
EventBridgeRule:
  Properties:
    Targets:
      - Arn: !GetAtt MyFunction.Arn  # ❌ 缺少 Permission
```

**正確**：
```yaml
EventBridgeRule:
  Type: AWS::Events::Rule
  Properties:
    Targets:
      - Arn: !GetAtt MyFunction.Arn
        Id: MyTarget

MyFunctionPermission:  # ✅ 添加 Permission
  Type: AWS::Lambda::Permission
  Properties:
    FunctionName: !Ref MyFunction
    Action: lambda:InvokeFunction
    Principal: events.amazonaws.com
    SourceArn: !GetAtt EventBridgeRule.Arn
```

### 3. 硬編碼 ARN 導致驗證失敗

**錯誤**：
```yaml
Targets:
  - Arn: arn:aws:lambda:us-west-2:123456789:function:my-function  # ❌
```

**正確**：
```yaml
Targets:
  - Arn: !ImportValue other-stack-FunctionArn  # ✅
```

---

## 🔍 診斷工作流

### Stack 狀態檢查

```bash
# 查看所有 agentcore stacks
aws cloudformation describe-stacks --region us-west-2 \
  --query 'Stacks[?contains(StackName,`agentcore`)].{Name:StackName,Status:StackStatus}' \
  --output table

# 檢查 stack drift
aws cloudformation detect-stack-drift --stack-name STACK_NAME
```

### Lambda 健康檢查

```bash
# 檢查狀態
aws lambda get-function --function-name FUNCTION_NAME \
  --query 'Configuration.{State:State,LastUpdateStatus:LastUpdateStatus}'

# 檢查環境變數
aws lambda get-function-configuration --function-name FUNCTION_NAME \
  --query 'Environment.Variables'

# 查看最新日誌
aws logs tail /aws/lambda/FUNCTION_NAME --since 5m
```

---

## 📖 輔助資源

需要更深入的指導時，參考：

### 詳細文檔
- [跨 Stack 引用詳解](docs/cross-stack-references.md)
- [資源管理和生命週期](docs/resource-management.md)
- [部署策略指南](docs/deployment-strategies.md)
- [故障排除手冊](docs/troubleshooting.md)
- [安全最佳實踐](docs/security-best-practices.md)

### 範例模板
- `templates/basic-lambda-stack.yaml` - 基礎 Lambda stack
- `templates/multi-stack-example.yaml` - 跨 stack 整合
- `templates/eventbridge-integration.yaml` - EventBridge 整合

---

## 🎯 決策框架

### 何時使用 Retain

**使用 Retain 當**：
- ✅ DynamoDB 表包含重要數據
- ✅ S3 bucket 包含用戶上傳內容
- ✅ CloudWatch Logs 需要保留審計記錄

**避免 Retain 當**：
- ❌ 測試和開發資源
- ❌ 可以重新生成的資源
- ❌ 會影響 stack 重建的資源

### 何時使用 DependsOn

**明確依賴當**：
- 資源創建順序很重要
- CloudFormation 無法自動推斷依賴
- 需要確保刪除順序

```yaml
MyFunction:
  Type: AWS::Serverless::Function
  DependsOn: MyTable  # 確保 Table 先創建
```

---

## 💡 專家提示

### 快速部署技巧

**跳過確認**：
```bash
sam deploy --no-confirm-changeset  # 生產環境慎用
```

**並行部署多個 stack**：
```bash
cd telegram-adapter && sam deploy &
cd ai-processor && sam deploy &
wait  # 等待兩者完成
```

### 緊急情況處理

**即使緊急，仍使用 SAM**：
- SAM deploy 也很快（2-5 分鐘）
- 使用 `--no-confirm-changeset` 加速
- 緊急情況更需要 IaC（可追蹤、可回滾）

**如果必須手動**（極罕見）：
- 用戶手動執行（不透過 Cline）
- 立即記錄變更
- 馬上補 SAM deploy 確認

---

## 🎓 關鍵記憶點

1. **IaC 無例外**：所有變更通過 SAM/CloudFormation
2. **動態命名**：使用 `!Sub '${AWS::StackName}-resource'`
3. **Export/Import**：跨 stack 引用的唯一方式
4. **Permission 必須**：EventBridge、API Gateway 調用 Lambda
5. **部署順序**：依賴關係決定順序
6. **驗證部署**：檢查狀態、配置、日誌
7. **緊急也用 SAM**：IaC 原則不妥協

---

## 🔗 相關資源

- [AWS CloudFormation 文檔](https://docs.aws.amazon.com/cloudformation/)
- [SAM 最佳實踐](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-best-practices.html)
- [Infrastructure as Code 白皮書](https://docs.aws.amazon.com/whitepapers/latest/introduction-devops-aws/infrastructure-as-code.html)

---

**記住**：你是 Infrastructure as Code 的守護者。沒有例外，沒有妥協。每一次遵守 IaC 原則，都是對專案長期健康的投資。