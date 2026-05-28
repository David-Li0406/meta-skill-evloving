# 安全最佳實踐

## 🔐 IAM 權限管理

### 最小權限原則

**核心概念**：只給予完成任務所需的最小權限

**錯誤範例**：
```yaml
# ❌ 過度寬鬆
Policies:
  - Statement:
      - Effect: Allow
        Action: '*'  # 所有操作
        Resource: '*'  # 所有資源
```

**正確範例**：
```yaml
# ✅ 具體且限制
Policies:
  - Statement:
      # 具體操作
      - Effect: Allow
        Action:
          - dynamodb:GetItem
          - dynamodb:PutItem
          - dynamodb:Query
        Resource: !GetAtt MyTable.Arn  # 具體資源
      
      # EventBridge（通常需要 *）
      - Effect: Allow
        Action: events:PutEvents
        Resource: '*'  # 可接受
```

### SAM Policy Templates

**使用內建策略**（推薦）：
```yaml
Policies:
  # DynamoDB
  - DynamoDBReadPolicy:
      TableName: !Ref MyTable
  - DynamoDBWritePolicy:
      TableName: !Ref MyTable
  
  # S3
  - S3ReadPolicy:
      BucketName: !Ref MyBucket
  - S3WritePolicy:
      BucketName: !Ref MyBucket
  
  # Secrets Manager
  - AWSSecretsManagerGetSecretValuePolicy:
      SecretArn: !Ref MySecret
```

### 跨服務權限

**Lambda 調用 Lambda**：
```yaml
# 調用方需要權限
CallerFunction:
  Policies:
    - Statement:
        - Effect: Allow
          Action: lambda:InvokeFunction
          Resource: !GetAtt TargetFunction.Arn

# 被調用方不需要額外配置
```

**EventBridge 調用 Lambda**：
```yaml
# Lambda Permission 必須
MyFunctionPermission:
  Type: AWS::Lambda::Permission
  Properties:
    FunctionName: !Ref MyFunction
    Action: lambda:InvokeFunction
    Principal: events.amazonaws.com
    SourceArn: !GetAtt MyRule.Arn
```

---

## 🔒 Secrets 管理

### 使用 Secrets Manager

**創建 Secret**：
```yaml
MySecret:
  Type: AWS::SecretsManager::Secret
  Properties:
    Description: Bot credentials
    SecretString: !Sub |
      {
        "bot_token": "${BotToken}",
        "api_key": "${ApiKey}"
      }
```

**在 Lambda 中使用**：
```yaml
MyFunction:
  Type: AWS::Serverless::Function
  Properties:
    Environment:
      Variables:
        SECRET_ARN: !Ref MySecret  # 傳遞 ARN
    
    Policies:
      - AWSSecretsManagerGetSecretValuePolicy:
          SecretArn: !Ref MySecret
```

**代碼中讀取**：
```python
import boto3
import json

secrets_client = boto3.client('secretsmanager')

def get_secret(secret_arn):
    response = secrets_client.get_secret_value(SecretId=secret_arn)
    return json.loads(response['SecretString'])
```

### 避免的做法

**❌ 環境變數中明文密碼**：
```yaml
Environment:
  Variables:
    BOT_TOKEN: '1234567890:ABCDEF...'  # ❌ 絕不這樣做
```

**❌ Template 中硬編碼**：
```yaml
Parameters:
  ApiKey:
    Type: String
    Default: 'sk-abc123...'  # ❌ 不要放在 template
```

---

## 🔐 加密配置

### 資料靜態加密

**DynamoDB**：
```yaml
MyTable:
  Type: AWS::DynamoDB::Table
  Properties:
    SSESpecification:
      SSEEnabled: true  # 使用 AWS 管理的金鑰
```

**S3**：
```yaml
MyBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketEncryption:
      ServerSideEncryptionConfiguration:
        - ServerSideEncryptionByDefault:
            SSEAlgorithm: AES256  # 或 aws:kms
```

**Secrets Manager**：
- 自動加密（無需配置）
- 使用 KMS 金鑰

### 資料傳輸加密

**API Gateway**：
- 強制 HTTPS（default）
- 禁用 HTTP

**Lambda 環境變數**：
- 自動加密（使用 AWS 管理的金鑰）

---

## 🌐 網路安全

### VPC 配置

**Lambda in VPC**（需要時）：
```yaml
MyFunction:
  Type: AWS::Serverless::Function
  Properties:
    VpcConfig:
      SecurityGroupIds:
        - !Ref LambdaSecurityGroup
      SubnetIds:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
```

**注意事項**：
- VPC Lambda 需要 NAT Gateway 訪問公網
- 冷啟動時間增加
- 需要 VPC endpoints（訪問 AWS 服務）

### Security Groups

```yaml
LambdaSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupDescription: Lambda security group
    VpcId: !Ref VPC
    SecurityGroupEgress:
      # 最小出站規則
      - IpProtocol: tcp
        FromPort: 443
        ToPort: 443
        CidrIp: 0.0.0.0/0  # HTTPS
```

---

## 🛡️ 訪問控制

### API Gateway Authorization

**IAM Authorization**：
```yaml
MyApi:
  Type: AWS::Serverless::Api
  Properties:
    Auth:
      DefaultAuthorizer: AWS_IAM
      InvokeRole: NONE
```

**Lambda Authorizer**：
```yaml
MyApi:
  Type: AWS::Serverless::Api
  Properties:
    Auth:
      DefaultAuthorizer: MyLambdaAuthorizer
      Authorizers:
        MyLambdaAuthorizer:
          FunctionArn: !GetAtt AuthFunction.Arn
```

### Resource-Based Policies

**S3 Bucket Policy**：
```yaml
MyBucketPolicy:
  Type: AWS::S3::BucketPolicy
  Properties:
    Bucket: !Ref MyBucket
    PolicyDocument:
      Statement:
        - Sid: AllowCloudFrontAccess
          Effect: Allow
          Principal:
            Service: cloudfront.amazonaws.com
          Action: s3:GetObject
          Resource: !Sub '${MyBucket.Arn}/*'
```

---

## 📊 審計和合規

### CloudTrail 整合

**記錄 API 調用**：
```yaml
MyTrail:
  Type: AWS::CloudTrail::Trail
  Properties:
    IsLogging: true
    S3BucketName: !Ref AuditBucket
    IncludeGlobalServiceEvents: true
    EventSelectors:
      - ReadWriteType: All
        IncludeManagementEvents: true
```

### AWS Config 規則

**合規檢查**：
```yaml
# 檢查加密是否啟用
EncryptionRule:
  Type: AWS::Config::ConfigRule
  Properties:
    ConfigRuleName: s3-bucket-encryption-enabled
    Source:
      Owner: AWS
      SourceIdentifier: S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED
```

---

## 🔍 安全掃描

### 部署前檢查

**Checklist**：
- [ ] 無硬編碼密碼或 API keys
- [ ] IAM 權限使用最小原則
- [ ] 所有敏感數據使用 Secrets Manager
- [ ] 加密啟用（S3、DynamoDB）
- [ ] 日誌不包含敏感資訊
- [ ] Public access 限制（S3、API）

### 工具

**cfn-lint**：
```bash
# 檢查 template 問題
pip install cfn-lint
cfn-lint template.yaml
```

**AWS Security Hub**：
- 自動檢測安全問題
- 提供修復建議

---

## 🚨 安全事件響應

### Lambda 被入侵

**立即行動**：
1. 停用 Lambda（設置併發為 0）
2. 審查 CloudTrail 日誌
3. 輪換所有 secrets
4. 審查代碼和依賴
5. 重新部署乾淨版本

### Secret 洩漏

**立即行動**：
1. 輪換 secret
2. 審查訪問日誌
3. 更新所有使用該 secret 的服務
4. 監控異常使用

---

## 💡 安全檢查清單

### 部署前

- [ ] 所有 secrets 在 Secrets Manager
- [ ] IAM 權限最小化
- [ ] 資源加密啟用
- [ ] 日誌記錄配置
- [ ] 網路訪問限制
- [ ] 無公開敏感端點

### 部署後

- [ ] 驗證權限正確
- [ ] 測試 secrets 可訪問
- [ ] 檢查日誌無敏感資料
- [ ] 掃描安全漏洞
- [ ] 審查 public access

### 定期審查

- [ ] 審查 IAM 權限（每月）
- [ ] 輪換 secrets（按策略）
- [ ] 檢查未使用資源
- [ ] 更新依賴版本
- [ ] 審查日誌存取

---

## 🔗 相關資源

- [SKILL.md](../SKILL.md) - 返回主文檔
- [AWS Security Best Practices](https://docs.aws.amazon.com/security/)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)