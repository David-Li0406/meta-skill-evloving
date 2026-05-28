# 生命周期与事件

## 目录
- [生命周期函数](#生命周期函数)
- [委托与事件](#委托与事件)

## 生命周期函数

### BeginPlay
```angelscript
UFUNCTION(BlueprintOverride)
void BeginPlay()
{
    // Actor 进入游戏时调用
    // 初始化逻辑
    ScriptOnlyMethod();
    NewOverridableMethod();
}
```

### Tick
```angelscript
UFUNCTION(BlueprintOverride)
void Tick(float DeltaSeconds)
{
    // 每帧调用
    // DeltaSeconds 表示自上一帧以来的时间（秒）

    // 示例：格式化打印
    Print(f"DeltaSeconds = {DeltaSeconds:.0f}");
}
```

### ConstructionScript
```angelscript
UFUNCTION(BlueprintOverride)
void ConstructionScript()
{
    // 在编辑器中构造 Actor 时调用
    // 动态创建组件
    Billboard = UBillboardComponent::Create(this, n"Billboard");
    Billboard.SetHiddenInGame(false);

    // 计算派生属性
    Product = ValueA * ValueB;
}
```

### 完整示例
```angelscript
class AExampleConstructionScript : AActor
{
    UPROPERTY(NotVisible)
    UBillboardComponent Billboard;

    UPROPERTY(Category = "Calculation")
    int ValueA = 3;

    UPROPERTY(Category = "Calculation")
    int ValueB = 3;

    UPROPERTY(BlueprintReadOnly, NotEditable, Category = "Calculation")
    int Product;

    UFUNCTION(BlueprintOverride)
    void ConstructionScript()
    {
        Billboard = UBillboardComponent::Create(this, n"Billboard");
        Billboard.SetHiddenInGame(false);
        Product = ValueA * ValueB;
    }
};
```

## 委托与事件

### 委托定义
```angelscript
// 声明委托类型
delegate void FExampleDelegateSignature(UObject Object, float Value);

UFUNCTION()
void ExecuteExampleDelegate(FExampleDelegateSignature InDelegate)
{
    // 检查委托是否绑定
    if (!InDelegate.IsBound())
    {
        Log("Input delegate was not bound.");
        return;
    }

    // 执行委托（未绑定会报错）
    InDelegate.Execute(nullptr, 5.4);

    // 安全执行委托（未绑定不报错）
    InDelegate.ExecuteIfBound(nullptr, 1.0);
}
```

### 事件定义
```angelscript
// 声明事件类型
event void FExampleEventSignature(UObject Object, float Value);

class AExampleEventActor : AActor
{
    // 声明为 UPROPERTY 可让蓝图绑定
    UPROPERTY(Category = "Example Events")
    FExampleEventSignature ExampleEvent;

    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        // 广播事件（无需检查 IsBound）
        ExampleEvent.Broadcast(nullptr, 100.0);
    }
};
```

### 绑定委托和事件
```angelscript
class AExampleEventActor : AActor
{
    UPROPERTY(Category = "Example Events")
    FExampleEventSignature ExampleEvent;

    UFUNCTION()
    void ExampleFunction(UObject InObject, float InValue)
    {
        Log("ExampleFunction: " + InValue);
    }

    UFUNCTION()
    void BindExampleDelegates()
    {
        // 绑定函数到事件
        // 注意 n"" 前缀表示 FName 字面量（编译时解析）
        ExampleEvent.AddUFunction(this, n"ExampleFunction");

        // 广播事件
        ExampleEvent.Broadcast(nullptr, 12.5);

        // 创建并绑定本地委托
        FExampleDelegateSignature ExampleLocalDelegate;
        ExampleLocalDelegate.BindUFunction(this, n"ExampleFunction");

        // 传递委托给函数
        ExecuteExampleDelegate(ExampleLocalDelegate);
    }
};
```

### 输出参数
```angelscript
UFUNCTION(Category = "Example Functions")
void ExampleFunctionWithOutputParameter(FVector&out OutPosition)
{
    OutPosition = FVector(1.0, 1.0, 0.0);
}
```

### 蓝图事件
```angelscript
class AExampleActorType : AActor
{
    // 蓝图可重写的事件
    UFUNCTION(BlueprintEvent)
    void NewOverridableMethod()
    {
        Log("Blueprint did not override this event.");
    }

    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        // 调用可重写事件
        NewOverridableMethod();
    }
};
```

## 注意事项
- `BeginPlay`、`Tick`、`ConstructionScript` 等生命周期函数必须标记为 `UFUNCTION(BlueprintOverride)`
- 委托和事件绑定的函数必须标记为 `UFUNCTION()`
- `FName` 字面量使用 `n""` 前缀（如 `n"FunctionName"`），编译时解析，性能更好
- `delegate` 和 `event` 的区别：
  - `delegate` 可以作为函数参数传递
  - `event` 可以作为 `UPROPERTY` 声明，供蓝图绑定
  - `event` 广播使用 `.Broadcast()`，不需要检查 `IsBound()`
- 输出参数使用 `&out` 标记，在蓝图中显示为输出引脚
- `BlueprintEvent` 创建的事件可以被蓝图重写，默认执行脚本实现