# AI 系统

## 目录
- [Behavior Tree Decorator](#behavior-tree-decorator)
- [Behavior Tree Service](#behavior-tree-service)
- [Behavior Tree Task](#behavior-tree-task)

## Behavior Tree Decorator

### 基础结构
```angelscript
class UBTDecorator_ExampleDecorator : UBTDecorator_BlueprintBase
{
    default NodeName = "Example Decorator";

    UPROPERTY(Category=ExampleDecorator)
    bool bShouldExecute = false;
};
```

### 条件检查
```angelscript
// 执行条件检查
UFUNCTION(BlueprintOverride)
bool PerformConditionCheckAI(AAIController OwnerController, APawn ControlledPawn)
{
    Print("Performing condition check for Example Decorator!");
    return bShouldExecute;  // true = 执行子节点，false = 跳过子节点
}
```

### Tick 更新
```angelscript
// 每帧更新
UFUNCTION(BlueprintOverride)
void TickAI(AAIController OwnerController, APawn ControlledPawn, float DeltaSeconds)
{
    Print("Ticking Example Decorator!");
}
```

### 完整示例
```angelscript
class UBTDecorator_ExampleDecorator : UBTDecorator_BlueprintBase
{
    default NodeName = "Example Decorator";

    UPROPERTY(Category=ExampleDecorator)
    bool bShouldExecute = false;

    UFUNCTION(BlueprintOverride)
    bool PerformConditionCheckAI(AAIController OwnerController, APawn ControlledPawn)
    {
        Print("Performing condition check for Example Decorator!");
        return bShouldExecute;
    }

    UFUNCTION(BlueprintOverride)
    void TickAI(AAIController OwnerController, APawn ControlledPawn, float DeltaSeconds)
    {
        Print("Ticking Example Decorator!");
    }
};
```

## Behavior Tree Service

### 基础结构
```angelscript
class UBTService_ExampleService : UBTService_BlueprintBase
{
    default NodeName = "Example Service";

    UPROPERTY(Category=ExampleService)
    float SomeValue = 50.0;
};
```

### 激活事件
```angelscript
// 服务激活时调用
UFUNCTION(BlueprintOverride)
void ActivationAI(AAIController OwnerController, APawn ControlledPawn)
{
    Print("Activating Example Service!");
}
```

### Tick 更新
```angelscript
// 每帧更新
UFUNCTION(BlueprintOverride)
void TickAI(AAIController OwnerController, APawn ControlledPawn, float DeltaSeconds)
{
    Print("Ticking Example Service!");
}
```

### 完整示例
```angelscript
class UBTService_ExampleService : UBTService_BlueprintBase
{
    default NodeName = "Example Service";

    UPROPERTY(Category=ExampleService)
    float SomeValue = 50.0;

    UFUNCTION(BlueprintOverride)
    void ActivationAI(AAIController OwnerController, APawn ControlledPawn)
    {
        Print("Activating Example Service!");
    }

    UFUNCTION(BlueprintOverride)
    void TickAI(AAIController OwnerController, APawn ControlledPawn, float DeltaSeconds)
    {
        Print("Ticking Example Service!");
    }
};
```

## Behavior Tree Task

### 基础结构
```angelscript
class UBTTask_ExampleTask : UBTTask_BlueprintBase
{
    default NodeName = "Example Task";

    UPROPERTY(Category=ExampleTask)
    float SomeValue = 50.0;
};
```

### 执行任务
```angelscript
// 任务首次执行时调用
UFUNCTION(BlueprintOverride)
void ExecuteAI(AAIController OwnerController, APawn ControlledPawn)
{
    Print("Executing Example Task!");
    FinishExecute(true);  // true = 成功，false = 失败
}
```

### Tick 更新
```angelscript
// 任务执行期间每帧调用
UFUNCTION(BlueprintOverride)
void TickAI(AAIController OwnerController, APawn ControlledPawn, float DeltaSeconds)
{
    Print("Ticking Example Task!");
}
```

### 中止任务
```angelscript
// 行为树中止任务时调用
UFUNCTION(BlueprintOverride)
void AbortAI(AAIController OwnerController, APawn ControlledPawn)
{
    Print("Aborting Example Task!");
}
```

### 完整示例
```angelscript
class UBTTask_ExampleTask : UBTTask_BlueprintBase
{
    default NodeName = "Example Task";

    UPROPERTY(Category=ExampleTask)
    float SomeValue = 50.0;

    UFUNCTION(BlueprintOverride)
    void ExecuteAI(AAIController OwnerController, APawn ControlledPawn)
    {
        Print("Executing Example Task!");
        FinishExecute(true);
    }

    UFUNCTION(BlueprintOverride)
    void TickAI(AAIController OwnerController, APawn ControlledPawn, float DeltaSeconds)
    {
        Print("Ticking Example Task!");
    }

    UFUNCTION(BlueprintOverride)
    void AbortAI(AAIController OwnerController, APawn ControlledPawn)
    {
        Print("Aborting Example Task!");
    }
};
```

## 节点类型对比

| 类型      | 基类                         | 主要用途                       | 关键函数                         |
| --------- | ---------------------------- | ------------------------------ | -------------------------------- |
| Decorator | `UBTDecorator_BlueprintBase` | 条件判断，决定是否执行子节点   | `PerformConditionCheckAI()`      |
| Service   | `UBTService_BlueprintBase`   | 定期更新 AI 状态，修改黑板变量 | `ActivationAI()`, `TickAI()`     |
| Task      | `UBTTask_BlueprintBase`      | 执行具体行动，如移动、攻击等   | `ExecuteAI()`, `FinishExecute()` |

## 注意事项
- 所有 Behavior Tree 节点都需要设置 `default NodeName`
- 使用 `UPROPERTY()` 暴露的参数可以在行为树编辑器中设置
- `PerformConditionCheckAI()` 返回 `true` 表示条件满足，`false` 表示不满足
- `ExecuteAI()` 必须调用 `FinishExecute()` 通知行为树任务完成
- `FinishExecute(true)` 表示成功，`FinishExecute(false)` 表示失败
- `TickAI()` 在节点活跃期间每帧调用
- `AbortAI()` 在行为树中断任务时调用（如条件不再满足、节点被跳过等）
- `ActivationAI()` 在服务首次激活时调用（Service 专用）
- 节点参数可以使用 `UPROPERTY()` 声明，并通过行为树编辑器可视化配置