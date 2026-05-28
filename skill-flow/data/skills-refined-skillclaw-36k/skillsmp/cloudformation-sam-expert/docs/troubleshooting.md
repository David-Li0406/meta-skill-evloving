# CloudFormation/SAM 故障排除手冊

## 🚨 常見部署問題

### 1. Stack Stuck in UPDATE_ROLLBACK_FAILED

**症狀**：Stack 更新失敗，回滾也失敗，卡住無法操作

**解決方案**：

```bash
# 選項 1: 繼續回滾
aws cloudformation continue-update-rollback \
  --stack-name STACK_NAME \
  --region us-west-2

# 選項 2: 跳過問題資源
aws cloudformation continue-update-rollback \
  --stack-name STACK_NAME \
  --resources-to-skip ResourceLogicalId \
  --region us-west-2

# 選項 3: 取消更新（回到之前狀態）
aws cloudformation cancel-update-stack \
  --stack-name STACK_NAME \
  --region us-west-2
```

---

### 2. EventBridge Rules 阻塞 EventBus 刪除

**症狀**：
```
EventBus can't be deleted since it has rules
```

**原因**：EventBridge bus 上有未刪除的 rules

**解決**：
```bash
# 1. 列出所有 rules
aws events list-rules \
  --event-bus-name agentcore-telegram-adapter-events \
  --region us-west-2

# 2. 查看每個 rule 的 targets
aws events list-targets-by-rule \
  --rule RULE_NAME \
  --event-bus-name BUS_NAME \
  --region us-west-2

# 3. 移除 targets
aws events remove-targets \
  --rule RULE_NAME \
  --event-bus-name BUS_NAME \
  --ids TARGET_ID \
  --region us-west-2

# 4. 刪除 rule
aws events delete-rule \
  --name RULE_NAME \
  --event-bus-name BUS_NAME \
  --region us-west-2

# 5. 重試 stack 刪除
aws cloudformation delete-stack --stack-name STACK_NAME
```

---

### 3. Lambda 緩存問題

**症狀**：
- SAM deploy 成功
- Lambda 仍執行舊代碼
- 環境變數未更新

**原因**：Lambda 緩存執行環境

**解決方案**：

```bash
# 方法 1: 清除 SAM 緩存（推薦）
rm -rf .aws-sam
sam build --use-container
sam deploy --stack-name STACK_NAME --region us-west-2

# 方法 2: 等待自動更新（2-5 分鐘）
aws lambda wait function-updated \
  --function-name FUNCTION_NAME \
  --region us-west-2

# 方法 3: 觸發新請求（強制重新初始化）
```

---

### 4. IAM 權限錯誤

**症狀**：
```
User/Role is not authorized to perform: ACTION on resource: ARN
AccessDeniedException
```

**診斷流程**：

```bash
# 1. 確認 Lambda 執行角色
aws lambda get-function \
  --function-name FUNCTION_NAME \
  --query 'Configuration.Role'

# 2. 查看角色策略
ROLE_NAME=$(echo $ROLE_ARN | cut -d'/' -f2)
aws iam list-role-policies --role-name $ROLE_NAME

# 3. 查看策略詳情
aws iam get-role-policy \
  --role-name $ROLE_NAME \
  --policy-name POLICY_NAME
```

**常見遺漏權限**：
```yaml
Policies:
  - Statement:
      # EventBridge
      - Effect: Allow
        Action: events:PutEvents
        Resource: '*'
      
      # Bedrock
      - Effect: Allow
        Action:
          - bedrock:InvokeModel
          - bedrock:InvokeModelWithResponseStream
        Resource: '*'
      
      # Browser Sandbox
      - Effect: Allow
        Action:
          - bedrock-agentcore:StartBrowserSession
          - bedrock-agentcore:StopBrowserSession
          - bedrock-agentcore:GetBrowserSession
        Resource: '*'
```

---

### 5. 空參數導致 IAM 錯誤

**症狀**：
```
Resource must be in ARN format or "*"
```

**原因**：
```yaml
Parameters:
  EventBusArn:
    Default: ''  # ❌ 空字符串

Policies:
  - Statement:
      Resource: !Ref EventBusArn  # ❌ 空 ARN
```

**解決**：
```yaml
# 選項 1: 使用通配符
Resource: '*'

# 選項 2: 條件判斷
Conditions:
  HasEventBusArn: !Not [!Equals [!Ref EventBusArn, '']]

Policies:
  - Statement:
      Resource: !If [HasEventBusArn, !Ref EventBusArn, '*']
```

---

### 6. Lambda 更新後仍有問題

**症狀**：
- Deploy 成功
- Lambda 狀態顯示 Active
- 但功能不正常

**檢查清單**：

```bash
# 1. 驗證 Lambda 狀態
aws lambda get-function \
  --function-name FUNCTION_NAME \
  --query 'Configuration.{State:State,LastUpdateStatus:LastUpdateStatus}'

# 應該看到：
# State: Active
# LastUpdateStatus: Successful

# 2. 檢查環境變數
aws lambda get-function-configuration \
  --function-name FUNCTION_NAME \
  --query 'Environment.Variables'

# 3. 查看最新日誌
aws logs tail /aws/lambda/FUNCTION_NAME --since 5m --region us-west-2

# 4. 檢查是否有錯誤
aws logs tail /aws/lambda/FUNCTION_NAME --since 5m | grep ERROR
```

---

### 7. Secrets Manager 更新未生效

**症狀**：
- 更新了 secret 值
- Lambda 仍讀取舊值

**原因**：Lambda 緩存了 secret

**解決**：
```bash
# 1. 更新 secret
aws secretsmanager update-secret \
  --secret-id SECRET_ID \
  --secret-string '{"key":"new-value"}'

# 2. 強制 Lambda 清除緩存
aws lambda update-function-configuration \
  --function-name FUNCTION_NAME \
  --environment Variables={DUMMY=update} \
  --region us-west-2

# 3. 等待更新完成
aws lambda wait function-updated \
  --function-name FUNCTION_NAME
```

---

## 🔍 診斷工具

### Stack 事件查看

```bash
# 查看最近的 stack 事件
aws cloudformation describe-stack-events \
  --stack-name STACK_NAME \
  --max-items 20 \
  --query 'StackEvents[*].[Timestamp,ResourceStatus,ResourceType,LogicalResourceId,ResourceStatusReason]' \
  --output table

# 只看失敗事件
aws cloudformation describe-stack-events \
  --stack-name STACK_NAME \
  --query 'StackEvents[?ResourceStatus==`CREATE_FAILED` || ResourceStatus==`UPDATE_FAILED`]'
```

### 資源 Drift 檢測

```bash
# 啟動檢測
aws cloudformation detect-stack-drift --stack-name STACK_NAME

# 查看結果
aws cloudformation describe-stack-resource-drifts \
  --stack-name STACK_NAME \
  --stack-resource-drift-status-filters MODIFIED DELETED
```

---

## 🛠️ 緊急修復程序

### 快速回滾

```bash
# 如果最近更新導致問題
aws cloudformation cancel-update-stack --stack-name STACK_NAME

# 或回滾到之前版本
# 修改 template 回到工作版本
sam deploy --stack-name STACK_NAME
```

### 強制清理

```bash
# 如果 stack 刪除失敗且無法修復
# 1. 手動刪除問題資源（謹慎）
# 2. 繼續 stack 刪除並跳過該資源
aws cloudformation continue-update-rollback \
  --stack-name STACK_NAME \
  --resources-to-skip ProblematicResource
```

---

## 📋 故障排除檢查清單

**部署失敗時**：
- [ ] 檢查 stack events（最近 20 個）
- [ ] 查看失敗資源的 StatusReason
- [ ] 驗證所有 Parameters 正確
- [ ] 檢查 IAM 權限完整
- [ ] 確認跨 stack imports 存在
- [ ] 驗證資源限制未超過

**功能不正常時**：
- [ ] Lambda 狀態是 Active
- [ ] LastUpdateStatus 是 Successful
- [ ] 環境變數正確
- [ ] Secrets 已更新
- [ ] 日誌無錯誤
- [ ] 權限配置正確

---

## 💡 預防措施

### 1. 使用變更集審查

```bash
# 創建變更集但不執行
sam deploy --stack-name STACK_NAME --no-execute-changeset

# 審查變更
aws cloudformation describe-change-set \
  --change-set-name CHANGESET_NAME \
  --stack-name STACK_NAME

# 如果安全，執行
aws cloudformation execute-change-set \
  --change-set-name CHANGESET_NAME \
  --stack-name STACK_NAME
```

### 2. 測試環境先行

- 在 dev stack 先測試變更
- 驗證成功後部署到 staging
- 最後部署到 production

### 3. 備份關鍵數據

**部署前**：
- 備份 DynamoDB（On-Demand Backup）
- 記錄所有 Stack Outputs
- 保存 template.yaml 版本

---

## 🔗 相關資源

- [SKILL.md](../SKILL.md) - 返回主文檔
- [資源管理](resource-management.md)
- [部署策略](deployment-strategies.md)