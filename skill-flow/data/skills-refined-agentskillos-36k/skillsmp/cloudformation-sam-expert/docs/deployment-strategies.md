# 部署策略指南

## 🎯 SAM 部署基礎

### 標準部署流程

```bash
# 1. Build
cd component-directory
sam build

# 2. Deploy
sam deploy \
  --stack-name agentcore-component-name \
  --region us-west-2 \
  --capabilities CAPABILITY_IAM \
  --resolve-s3

# 3. 驗證
aws cloudformation describe-stacks \
  --stack-name agentcore-component-name \
  --query 'Stacks[0].StackStatus'
```

---

## 🔄 部署模式

### 1. 標準部署（All-at-Once）

**特點**：
- 最簡單直接
- 短暫停機時間
- 適合開發環境

**配置**：
```yaml
# template.yaml
MyFunction:
  Type: AWS::Serverless::Function
  Properties:
    AutoPublishAlias: live  # 自動發布別名
    DeploymentPreference:
      Type: AllAtOnce  # 一次性部署
```

### 2. 金絲雀部署（Canary）

**特點**：
- 漸進式發布
- 降低風險
- 適合生產環境

**配置**：
```yaml
MyFunction:
  Type: AWS::Serverless::Function
  Properties:
    AutoPublishAlias: live
    DeploymentPreference:
      Type: Canary10Percent5Minutes  # 10% 流量持續 5 分鐘
      Alarms:
        - !Ref ErrorAlarm  # 錯誤時自動回滾
      Hooks:
        PreTraffic: !Ref PreTrafficHook  # 部署前驗證
        PostTraffic: !Ref PostTrafficHook  # 部署後驗證
```

**可用模式**：
- Canary10Percent30Minutes
- Canary10Percent5Minutes
- Canary10Percent10Minutes
- Linear10PercentEvery10Minutes
- Linear10PercentEvery1Minute

### 3. 藍綠部署

**概念**：
- 藍色環境：當前生產
- 綠色環境：新版本
- 驗證後切換

**實施**：
```yaml
# 使用 Lambda 別名
ProductionAlias:
  Type: AWS::Lambda::Alias
  Properties:
    FunctionName: !Ref MyFunction
    FunctionVersion: !GetAtt MyFunctionVersion.Version
    Name: prod
    RoutingConfig:
      AdditionalVersionWeights:
        - FunctionVersion: !GetAtt NewVersion.Version
          FunctionWeight: 0.1  # 10% 流量到新版本
```

---

## 🚀 部署最佳實踐

### 變更集審查

**為什麼**：
- 預覽將要發生的變更
- 避免意外修改
- 團隊審查機會

**流程**：
```bash
# 1. 創建變更集（不執行）
sam deploy --stack-name STACK --no-execute-changeset

# 2. 審查變更
aws cloudformation describe-change-set \
  --change-set-name CHANGESET \
  --stack-name STACK

# 3. 如果安全，執行
aws cloudformation execute-change-set \
  --change-set-name CHANGESET
```

### 環境隔離

**多環境策略**：
```yaml
Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]
    Default: dev

Mappings:
  EnvironmentConfig:
    dev:
      MemorySize: 256
      Timeout: 30
      LogRetention: 7
    staging:
      MemorySize: 512
      Timeout: 60
      LogRetention: 14
    prod:
      MemorySize: 1024
      Timeout: 300
      LogRetention: 30

Resources:
  MyFunction:
    Properties:
      MemorySize: !FindInMap [EnvironmentConfig, !Ref Environment, MemorySize]
      Timeout: !FindInMap [EnvironmentConfig, !Ref Environment, Timeout]
```

---

## 📦 多 Stack 部署順序

### 依賴圖範例

```
1. agentcore-telegram-adapter  # 提供 EventBus
   ↓
2. agentcore-ai-processor      # 使用 EventBus
   ↓
3. agentcore-web-adapter       # 使用 EventBus
```

### 部署腳本

```bash
#!/bin/bash
set -e

# 部署順序關鍵
echo "部署 telegram-adapter..."
cd telegram-adapter
sam build && sam deploy --stack-name agentcore-telegram-adapter --region us-west-2

echo "部署 ai-processor..."
cd ../ai-processor
sam build && sam deploy --stack-name agentcore-ai-processor --region us-west-2

echo "部署 web-adapter..."
cd ../web-adapter/infrastructure
sam build && sam deploy --stack-name agentcore-web-adapter --region us-west-2

echo "✅ 所有 stacks 部署完成"
```

---

## 🔄 更新策略

### 小型更新（配置變更）

```bash
# 快速部署（跳過確認）
sam deploy --stack-name STACK --no-confirm-changeset
```

### 大型更新（架構變更）

```bash
# 1. 審查變更集
sam deploy --stack-name STACK --no-execute-changeset

# 2. 通知團隊

# 3. 執行部署

# 4. 監控指標

# 5. 準備回滾方案
```

---

## 🎯 部署驗證

### 自動驗證腳本

```bash
#!/bin/bash
STACK_NAME=$1

echo "驗證 Stack: $STACK_NAME"

# 1. 檢查 stack 狀態
STATUS=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --query 'Stacks[0].StackStatus' \
  --output text)

if [ "$STATUS" != "CREATE_COMPLETE" ] && [ "$STATUS" != "UPDATE_COMPLETE" ]; then
  echo "❌ Stack 狀態異常: $STATUS"
  exit 1
fi

# 2. 檢查 Lambda 函數
FUNCTIONS=$(aws cloudformation describe-stack-resources \
  --stack-name $STACK_NAME \
  --query 'StackResources[?ResourceType==`AWS::Lambda::Function`].PhysicalResourceId' \
  --output text)

for func in $FUNCTIONS; do
  STATE=$(aws lambda get-function \
    --function-name $func \
    --query 'Configuration.State' \
    --output text)
  
  if [ "$STATE" != "Active" ]; then
    echo "❌ Lambda $func 狀態異常: $STATE"
    exit 1
  fi
done

echo "✅ 驗證通過"
```

---

## 💡 高級技巧

### 並行部署

```bash
# 無依賴的 stacks 可以並行
cd telegram-adapter && sam deploy &
PID1=$!

cd web-adapter && sam deploy &
PID2=$!

# 等待兩者完成
wait $PID1 && wait $PID2
```

### 條件部署

```yaml
# 只在特定條件下創建資源
Conditions:
  IsProduction: !Equals [!Ref Environment, 'prod']
  IsDevelopment: !Equals [!Ref Environment, 'dev']

Resources:
  ProdOnlyAlarm:
    Type: AWS::CloudWatch::Alarm
    Condition: IsProduction
  
  DevOnlyLogGroup:
    Type: AWS::Logs::LogGroup
    Condition: IsDevelopment
    Properties:
      RetentionInDays: 3  # Dev 只保留 3 天
```

---

## 🔗 相關資源

- [SKILL.md](../SKILL.md) - 返回主文檔
- [故障排除](troubleshooting.md)
- [資源管理](resource-management.md)