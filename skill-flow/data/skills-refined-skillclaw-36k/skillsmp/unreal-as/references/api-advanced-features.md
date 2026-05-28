# 高级特性

## 目录
- [Mixin 方法](#mixin-方法)
- [组件系统](#组件系统)
- [默认值设置](#默认值设置)
- [调试输出](#调试输出)

## Mixin 方法

### 定义 Mixin 方法
```angelscript
// Mixin 方法只能作为方法调用
// 第一个参数是该方法可以使用的对象类型
mixin void ExampleMixinActorMethod(AActor Self, FVector Location)
{
    Self.ActorLocation = Location;
}
```

### 使用 Mixin 方法
```angelscript
void Example_MixinMethod()
{
    AActor ActorReference;
    // 直接在对象上调用 Mixin 方法
    ActorReference.ExampleMixinActorMethod(FVector(0.0, 0.0, 100.0));
}
```

### 完整示例
```angelscript
/**
 * Global functions declared with the 'mixin' keyword can only be called as methods.
 * The first paramater will be the type of object the method can be used on.
 *
 * The module must still be imported for the mixin method to be usable.
 *
 * This behaves similar to the ScriptMixin meta tag for C++ function libraries.
 */
mixin void ExampleMixinActorMethod(AActor Self, FVector Location)
{
    Self.ActorLocation = Location;
}

void Example_MixinMethod()
{
    AActor ActorReference;
    ActorReference.ExampleMixinActorMethod(FVector(0.0, 0.0, 100.0));
}
```

## 组件系统

### 动态创建组件
```angelscript
class AExampleConstructionScript : AActor
{
    UPROPERTY(NotVisible)
    UBillboardComponent Billboard;

    UFUNCTION(BlueprintOverride)
    void ConstructionScript()
    {
        // 动态创建组件
        Billboard = UBillboardComponent::Create(this, n"Billboard");
        Billboard.SetHiddenInGame(false);
    }
};
```

### 设置组件可见性
```angelscript
// 设置游戏中是否可见
Billboard.SetHiddenInGame(false);  // false = 可见，true = 不可见
```

### 组件属性
```angelscript
class AExampleActorType : AActor
{
    // 自动创建组件
    UPROPERTY(DefaultComponent, RootComponent)
    UStaticMeshComponent Mesh;

    // 设置组件默认属性
    default Mesh.RelativeLocation = FVector(0.0, 0.0, 0.0);

    // 附加组件
    UPROPERTY(DefaultComponent, Attach = Mesh)
    UBillboardComponent Billboard;
    default Billboard.SetHiddenInGame(false);
};
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

## 默认值设置

### 使用 default 关键字
```angelscript
class AExampleActorType : AActor
{
    UPROPERTY()
    int ExampleValue = 15;

    // 使用 default 覆盖父类属性
    default bReplicates = true;

    // 添加标签
    default Tags.Add(n"ExampleTag");

    // 设置组件默认属性
    UPROPERTY(DefaultComponent, RootComponent)
    UStaticMeshComponent Mesh;

    default Mesh.RelativeLocation = FVector(0.0, 0.0, 0.0);
};
```

### 完整示例
```angelscript
class AExampleMovingObject : AActor
{
    UPROPERTY(DefaultComponent, RootComponent)
    UStaticMeshComponent Mesh;

    default Mesh.RelativeLocation = FVector(0.0, 0.0, 0.0);

    default bReplicates = true;

    UPROPERTY(DefaultComponent, Attach = Mesh)
    UBillboardComponent Billboard;

    default Billboard.SetHiddenInGame(false);

    UPROPERTY()
    float MovementPerSecond = 100.0;

    UPROPERTY(NotEditable, BlueprintReadOnly)
    FVector OriginalPosition;

    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        OriginalPosition = GetActorLocation();
    }

    UFUNCTION(BlueprintOverride)
    void Tick(float DeltaSeconds)
    {
        FVector NewLocation = GetActorLocation();
        NewLocation += FVector(DeltaSeconds * MovementPerSecond, 0, 0);

        FHitResult SweepResult;
        SetActorLocation(NewLocation, bTeleport = true, bSweep = false, SweepHitResult = SweepResult);
    }
};
```

## 调试输出

### 日志输出
```angelscript
void ScriptOnlyMethod()
{
    Log("ScriptOnlyMethod Called");
}
```

### 屏幕打印
```angelscript
// 打印到屏幕
Print("Printed on screen");

// 设置显示时长（秒）
Print("Jump was pressed!", Duration=5.0);

// 格式化打印
Print(f"Called from actor {GetName()} at location {ActorLocation}");
```

### 完整示例
```angelscript
UFUNCTION()
void ExecuteExampleFunction(AActor InputActor)
{
    Print("Printed on screen");
    InputActor.ActorHiddenInGame = true;
}

class AExampleActorType : AActor
{
    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        ScriptOnlyMethod();
    }

    void ScriptOnlyMethod()
    {
        Log("ScriptOnlyMethod Called");
    }
};
```

## 注意事项

### Mixin 方法
- `mixin` 关键字定义的方法只能作为方法调用，不能作为函数调用
- Mixin 方法的第一个参数是该方法可以使用的对象类型
- 使用 Mixin 方法需要导入对应的模块
- Mixin 方法类似于 C++ 的 `ScriptMixin` meta tag

### 组件系统
- `DefaultComponent` 会自动创建组件，无需手动实例化
- `Create(owner, name)` 用于在 ConstructionScript 中动态创建组件
- `SetHiddenInGame(false)` 设置组件在游戏中可见
- 组件层级通过 `Attach` 和 `RootComponent` 修饰符设置

### 默认值设置
- `default` 关键字用于设置父类属性或组件的默认值
- `default` 语句等价于在 C++ 构造函数中设置属性
- 使用 `n""` 前缀表示 FName 字面量（编译时解析）
- `Tags.Add(n"TagName")` 用于添加标签

### 调试输出
- `Log()` 输出到日志窗口，适合调试和追踪
- `Print()` 输出到屏幕，适合临时调试和视觉反馈
- `Print(message, Duration=X)` 控制显示时长（秒）
- 格式化字符串支持 `f"..."` 语法和格式化选项
- 使用 `check(condition)` 进行断言检查