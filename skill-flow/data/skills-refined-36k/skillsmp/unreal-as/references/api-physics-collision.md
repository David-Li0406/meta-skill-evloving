# 物理与碰撞

## 目录
- [Actor 重叠检测](#actor-重叠检测)
- [组件重叠检测](#组件重叠检测)
- [位置控制](#位置控制)

## Actor 重叠检测

### 重叠事件
```angelscript
class AOverlapExampleActor : AActor
{
    // 覆盖开始重叠
    UFUNCTION(BlueprintOverride)
    void ActorBeginOverlap(AActor OtherActor)
    {
        Print("Overlapping with: " + OtherActor.Name);
    }

    // 覆盖结束重叠
    UFUNCTION(BlueprintOverride)
    void ActorEndOverlap(AActor OtherActor)
    {
        Print("No longer overlapping with: " + OtherActor.Name);
    }
};
```

### 完整示例
```angelscript
class AOverlapExampleActor : AActor
{
    UFUNCTION(BlueprintOverride)
    void ActorBeginOverlap(AActor OtherActor)
    {
        Print("Overlapping with: " + OtherActor.Name);
    }

    UFUNCTION(BlueprintOverride)
    void ActorEndOverlap(AActor OtherActor)
    {
        Print("No longer overlapping with: " + OtherActor.Name);
    }
};
```

## 组件重叠检测

### 绑定重叠事件
```angelscript
class UOverlapExampleComponent : UPrimitiveComponent
{
    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        // 绑定组件重叠事件
        // 绑定的函数必须是 UFUNCTION()
        OnComponentBeginOverlap.AddUFunction(this, n"TriggeredOnBeginOverlap");
        OnComponentEndOverlap.AddUFunction(this, n"TriggeredOnEndOverlap");
    }
};
```

### 处理函数
```angelscript
// 开始重叠处理
UFUNCTION()
void TriggeredOnBeginOverlap(
    UPrimitiveComponent OverlappedComponent, AActor OtherActor,
    UPrimitiveComponent OtherComponent, int OtherBodyIndex,
    bool bFromSweep, const FHitResult&in Hit)
{
    Print("Overlapping with component: " + OtherComponent.Name);
}

// 结束重叠处理
UFUNCTION()
void TriggeredOnEndOverlap(
    UPrimitiveComponent OverlappedComponent, AActor OtherActor,
    UPrimitiveComponent OtherComponent, int OtherBodyIndex)
{
    Print("No longer overlapping with component: " + OtherComponent.Name);
}
```

### 完整示例
```angelscript
class UOverlapExampleComponent : UPrimitiveComponent
{
    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        OnComponentBeginOverlap.AddUFunction(this, n"TriggeredOnBeginOverlap");
        OnComponentEndOverlap.AddUFunction(this, n"TriggeredOnEndOverlap");
    }

    UFUNCTION()
    void TriggeredOnBeginOverlap(
        UPrimitiveComponent OverlappedComponent, AActor OtherActor,
        UPrimitiveComponent OtherComponent, int OtherBodyIndex,
        bool bFromSweep, const FHitResult&in Hit)
    {
        Print("Overlapping with component: " + OtherComponent.Name);
    }

    UFUNCTION()
    void TriggeredOnEndOverlap(
        UPrimitiveComponent OverlappedComponent, AActor OtherActor,
        UPrimitiveComponent OtherComponent, int OtherBodyIndex)
    {
        Print("No longer overlapping with component: " + OtherComponent.Name);
    }
};
```

## 位置控制

### 获取和设置位置
```angelscript
class AExampleMovingObject : AActor
{
    UPROPERTY()
    float MovementPerSecond = 100.0;

    UPROPERTY(NotEditable, BlueprintReadOnly)
    FVector OriginalPosition;

    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        // 记录原始位置
        OriginalPosition = GetActorLocation();
    }

    UFUNCTION(BlueprintOverride)
    void Tick(float DeltaSeconds)
    {
        FVector NewLocation = GetActorLocation();
        NewLocation += FVector(DeltaSeconds * MovementPerSecond, 0, 0);

        // 设置位置
        // bTeleport: true = 传送（不碰撞检测），false = 物理移动（碰撞检测）
        // bSweep: false = 不碰撞检测，true = 碰撞检测并返回结果
        FHitResult SweepResult;
        SetActorLocation(NewLocation, bTeleport = true, bSweep = false, SweepHitResult = SweepResult);
    }
};
```

### 移动逻辑示例
```angelscript
class AExampleMovingObject : AActor
{
    UPROPERTY(DefaultComponent, RootComponent)
    UStaticMeshComponent Mesh;

    default Mesh.RelativeLocation = FVector(0.0, 0.0, 0.0);

    UPROPERTY()
    float MovementPerSecond = 100.0;

    UPROPERTY(NotEditable, BlueprintReadOnly)
    FVector OriginalPosition;

    bool bHeadingBack = false;

    UFUNCTION(BlueprintOverride)
    void BeginPlay()
    {
        OriginalPosition = GetActorLocation();
    }

    UFUNCTION(BlueprintOverride)
    void Tick(float DeltaSeconds)
    {
        FVector NewLocation = GetActorLocation();

        if (bHeadingBack)
        {
            NewLocation -= FVector(DeltaSeconds * MovementPerSecond, 0, 0);

            // 向左移动一定距离后转向
            if (NewLocation.X < OriginalPosition.X - 100)
                bHeadingBack = false;
        }
        else
        {
            NewLocation += FVector(DeltaSeconds * MovementPerSecond, 0, 0);

            // 向右移动一定距离后转向
            if (NewLocation.X > OriginalPosition.X + 100)
                bHeadingBack = true;
        }

        FHitResult SweepResult;
        SetActorLocation(NewLocation, bTeleport = true, bSweep = false, SweepHitResult = SweepResult);
    }
};
```

## 注意事项
- Actor 重叠事件需要继承 `AActor` 并覆盖对应函数
- 组件重叠事件需要绑定 `OnComponentBeginOverlap` 和 `OnComponentEndOverlap` 事件
- 处理函数必须标记为 `UFUNCTION()`
- `SetActorLocation()` 的 `bTeleport` 参数：
  - `true` - 传送（不进行碰撞检测）
  - `false` - 物理移动（会进行碰撞检测）
- `SetActorLocation()` 的 `bSweep` 参数：
  - `false` - 不进行碰撞检测
  - `true` - 进行碰撞检测并将结果写入 `SweepHitResult`
- 组件重叠事件比 Actor 重叠事件更复杂，但可以区分具体哪个组件重叠
- `OtherActor.Name` 返回 Actor 名称
- `OtherComponent.Name` 返回组件名称