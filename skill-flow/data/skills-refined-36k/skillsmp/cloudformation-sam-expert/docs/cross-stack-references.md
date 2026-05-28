# 跨 Stack 引用詳解

## 🎯 為什麼需要跨 Stack 引用

在微服務和多組件架構中，不同的 CloudFormation stacks 需要共享資源：
- EventBridge bus 被多個 Lambda 使用
- DynamoDB 表被多個服務訪問
- API Gateway 整合多個 Lambda 函數

**錯誤方式**：硬編碼 ARN
**正確方式**：Export/ImportValue

---

## 📋 Export 最佳實踐

### 命名規範

**格式**：`${StackName}-[ResourceType]`

```yaml
Outputs:
  EventBusName:
    Description: EventBridge bus name
    Value: !Ref EventBus
    Export:
      Name: !Sub '${AWS::StackName}-EventBusName'
  
  EventBusArn:
    Description: EventBridge bus ARN
    Value: !GetAtt EventBus.Arn
    Export:
      Name: !Sub '${AWS::StackName}-EventBusArn'
  
  ProcessorFunctionArn:
    Description: Processor Lambda ARN
    Value: !GetAtt ProcessorFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-ProcessorArn'
```

**為什麼使用 stack name**：
- ✅ 避免命名衝突（每個 stack 唯一）
- ✅ 清楚來源（知道 export 來自哪個 stack）
- ✅ 支持多環境（dev/staging/prod 可以並存）

### Export 什麼

**常見 Export 項目**：
- ARN（最常見）：用於權限和引用
- Name：用於 API 調用
- URL：用於 HTTP 端點
- Configuration values：跨 stack 配置

**範例**：
```yaml
Outputs:
  # Lambda Function
  FunctionName:
    Value: !Ref MyFunction
    Export:
      Name: !Sub '${AWS::StackName}-FunctionName'
  
  FunctionArn:
    Value: !GetAtt MyFunction.Arn
    Export:
      Name: !Sub '${AWS::StackName}-FunctionArn'
  
  # API Gateway
  ApiUrl:
    Value: !Sub 'https://${Api}.execute-api.${AWS::Region}.amazonaws.com/Prod'
    Export:
      Name: !Sub '${AWS::StackName}-ApiUrl'
  
  # DynamoDB Table
  TableName:
    Value: !Ref MyTable
    Export:
      Name: !Sub '${AWS::StackName}-TableName'
  
  TableArn:
    Value: !GetAtt MyTable.Arn
    Export:
      Name: !Sub '${AWS::StackName}-TableArn'
```

---

## 📥 Import 最佳實踐

### 基本使用

```yaml
Resources:
  MyFunction:
    Type: AWS::Serverless::Function
    Properties:
      Environment:
        Variables:
          # Import name
          EVENT_BUS_NAME: !ImportValue agentcore-telegram-adapter-EventBusName
          # Import ARN
          EVENT_BUS_ARN: !ImportValue agentcore-telegram-adapter-EventBusArn
      
      Policies:
        - Statement:
            - Effect: Allow
              Action: events:PutEvents
              Resource: !ImportValue agentcore-telegram-adapter-EventBusArn
```

### EventBridge Integration

**完整範例**：
```yaml
Resources:
  # EventBridge Rule（在使用方 Stack）
  MessageReceivedRule:
    Type: AWS::Events::Rule
    Properties:
      EventBusName: !ImportValue agentcore-telegram-adapter-EventBusName
      EventPattern:
        source:
          - agentcore.telegram
        detail-type:
          - message.received
      Targets:
        - Arn: !GetAtt ProcessorFunction.Arn
          Id: ProcessorTarget
  
  # Lambda Permission（必須）
  ProcessorPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !Ref ProcessorFunction
      Action: lambda:InvokeFunction
      Principal: events.amazonaws.com
      SourceArn: !GetAtt MessageReceivedRule.Arn
```

---

## ⚠️ 常見問題

### 問題 1: Import 的 Stack 還不存在

**錯誤**：
```
Export STACK-NAME-Resource does not exist
```

**解決**：
- 確保提供 export 的 stack 已部署
- 檢查 export 名稱拼寫
- 驗證 region 匹配

### 問題 2: 無法刪除有 Export 的 Stack

**錯誤**：
```
Export cannot be deleted as it is in use by STACK_NAME
```

**解決順序**：
1. 先刪除 import 的 stack（依賴方）
2. 再刪除 export 的 stack（提供方）

### 問題 3: 硬編碼 ARN 失敗

**錯誤**：
```
AWS::EarlyValidation::ResourceExistenceCheck failed
```

**原因**：CloudFormation 驗證資源存在時失敗

**解決**：使用 ImportValue 而非硬編碼 ARN

---

## 🔄 循環依賴處理

### 識別循環依賴

**症狀**：
```
Circular dependency between resources
```

**常見場景**：
- Stack A export 給 Stack B
- Stack B export 給 Stack A

### 解決策略

**1. 重新設計架構**（推薦）：
- 提取共享資源到第三個 stack
- Stack C export 給 A 和 B

**2. 使用條件資源**：
- 第一次部署時不創建依賴資源
- 第二次部署時添加

**3. 拆分功能**：
- 減少跨 stack 依賴
- 增加組件自包含性

---

## 📊 Export 依賴圖

### 本專案範例

```
agentcore-telegram-adapter (提供方)
├── Exports:
│   ├── EventBusName
│   └── EventBusArn
│
└── 被使用於:
    ├── agentcore-ai-processor
    └── agentcore-web-adapter
```

### 依賴管理

**部署順序**：
1. telegram-adapter（提供 EventBus）
2. ai-processor（使用 EventBus）
3. web-adapter（使用 EventBus）

**刪除順序**（反向）：
1. web-adapter
2. ai-processor
3. telegram-adapter

---

## 💡 高級模式

### 條件 Export

```yaml
Conditions:
  IsProduction: !Equals [!Ref Environment, 'prod']

Outputs:
  ApiUrl:
    Condition: IsProduction  # 只在 prod 環境 export
    Value: !Sub 'https://${Api}.execute-api.${AWS::Region}.amazonaws.com'
    Export:
      Name: !Sub '${AWS::StackName}-ApiUrl'
```

### 多值 Export

```yaml
# Export JSON 字符串
Outputs:
  DatabaseConfig:
    Value: !Sub |
      {
        "host": "${Database.Endpoint.Address}",
        "port": "${Database.Endpoint.Port}",
        "name": "${DatabaseName}"
      }
    Export:
      Name: !Sub '${AWS::StackName}-DatabaseConfig'
```

---

## ✅ 檢查清單

**創建 Export 時**：
- [ ] 名稱包含 `${AWS::StackName}` prefix
- [ ] Description 清楚說明用途
- [ ] 考慮是否需要同時 export ARN 和 Name
- [ ] 文檔記錄 export 的使用方式

**使用 Import 時**：
- [ ] 確認 export 的 stack 已部署
- [ ] Import 名稱完全匹配（大小寫敏感）
- [ ] 添加必要的 Permission（EventBridge, API Gateway）
- [ ] 考慮部署順序和刪除順序

---

## 🔗 相關資源

- [CloudFormation Outputs](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html)
- [Cross-Stack References](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/walkthrough-crossstackref.html)
- 本專案：`.clinerules/deployment/stack-management-best-practices.md`