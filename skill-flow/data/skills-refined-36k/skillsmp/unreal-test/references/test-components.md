# 测试组件说明

## 目录
- [概述](#概述)
- [SpawnHelper](#spawnhelper)
- [ActorTestSpawner](#actortestspawner)
- [MapTestSpawner](#maptestspawner)
- [PIENetworkComponent](#pienetworkcomponent)
- [InputTestActions](#inputtestactions)
- [CQTestSlateComponent](#cqtestslatecomponent)
- [CQTestAssetHelper](#cqtestassethelper)
- [FAssetBuilder](#fassetbuilder)

## 概述
CQTest框架采用组合优于继承的设计理念。创建新组件是扩展框架的推荐默认机制。

## SpawnHelper

### 功能
简化Actor和其他对象的生成，提供一致的生成接口。

### 实现方式
- ActorTestSpawner：创建最小UWorld用于测试Actor，并管理它们的销毁
- MapTestSpawner：创建临时地图或打开指定关卡

### 使用示例
```cpp
#include "CQTest.h"

TEST_CLASS(SpawnTest, "Game.Spawn")
{
    // SpawnHelper通过具体实现类使用
    TEST_METHOD(SpawnActor_InValidWorld_Succeeds)
    {
        // 使用ActorTestSpawner
        // 见ActorTestSpawner章节
    }
};
```

## ActorTestSpawner

### 功能
为测试创建最小的UWorld，管理Actor的生成和自动销毁。

### 主要方法
```cpp
// 创建测试世界并初始化
void InitializeWorld();

// 在测试世界中生成Actor
template<typename T>
T* SpawnActor(const FVector& Location, const FRotator& Rotation = FRotator::ZeroRotator);

// 销毁所有生成的Actor
void DestroyAllSpawnedActors();

// 获取测试世界
UWorld* GetTestWorld();
```

### 使用示例
```cpp
TEST_CLASS(ActorSpawnTest, "Game.Actor.Spawn")
{
    ActorTestSpawner Spawner;
    AMyCharacter* TestCharacter = nullptr;

    BEFORE_EACH()
    {
        Spawner.InitializeWorld();
    }

    AFTER_EACH()
    {
        Spawner.DestroyAllSpawnedActors();
    }

    TEST_METHOD(SpawnCharacter_AtOrigin_Success)
    {
        TestCharacter = Spawner.SpawnActor<AMyCharacter>(
            FVector::ZeroVector,
            FRotator::ZeroRotator
        );

        ASSERT_THAT(IsNotNull(TestCharacter));
        ASSERT_THAT(IsTrue(TestCharacter->IsValidLowLevel()));
    }

    TEST_METHOD(SpawnMultipleActors_AllValid)
    {
        AMyActor* Actor1 = Spawner.SpawnActor<AMyActor>(FVector(100, 0, 0));
        AMyActor* Actor2 = Spawner.SpawnActor<AMyActor>(FVector(200, 0, 0));

        ASSERT_THAT(IsNotNull(Actor1));
        ASSERT_THAT(IsNotNull(Actor2));
    }
};
```

### 注意事项
- 必须先调用 `InitializeWorld()` 才能生成Actor
- 测试结束后调用 `DestroyAllSpawnedActors()` 清理
- 生成的Actor会自动注册到测试世界
- 测试世界与游戏世界隔离，不影响游戏逻辑

## MapTestSpawner

### 功能
创建临时地图或加载指定关卡，用于在特定关卡中测试。

### 主要方法
```cpp
// 创建临时测试地图
bool CreateTempMap();

// 加载指定关卡
bool LoadMap(const FString& MapPath);

// 获取当前加载的地图
UWorld* GetCurrentWorld();

// 卸载当前地图
bool UnloadMap();
```

### 使用示例
```cpp
TEST_CLASS(MapTest, "Game.Map")
{
    MapTestSpawner MapSpawner;

    BEFORE_EACH()
    {
        // 创建临时地图或加载特定关卡
        ASSERT_THAT(IsTrue(MapSpawner.LoadMap(TEXT("/Game/Maps/TestMap"))));
    }

    AFTER_EACH()
    {
        MapSpawner.UnloadMap();
    }

    TEST_METHOD(SpawnActorInMap_Success)
    {
        UWorld* World = MapSpawner.GetCurrentWorld();
        ASSERT_THAT(IsNotNull(World));

        // 在加载的关卡中生成Actor
        AMyActor* Actor = World->SpawnActor<AMyActor>(FVector::ZeroVector);
        ASSERT_THAT(IsNotNull(Actor));
    }
};
```

### 注意事项
- 加载关卡是异步操作，可能需要使用Latent Actions
- 加载大型关卡可能影响测试性能
- 必须在测试后卸载地图，避免内存泄漏
- 仅在Editor上下文中有效，需指定 `EAutomationTestFlags::EditorContext`

## PIENetworkComponent

### 功能
创建服务器和多个客户端，用于测试网络复制和同步。PIEN（Play In Editor）网络测试专用。

### 主要特性
- 自动设置服务器和客户端PIE实例
- 模拟网络延迟和丢包（可选）
- 支持多客户端场景

### 使用示例
```cpp
#include "CQTest.h"

TEST_CLASS(NetworkReplicationTest, "Game.Network")
    , public EAutomationTestFlags::EditorContext
{
    PIENetworkComponent NetworkComponent;

    BEFORE_EACH()
    {
        // 初始化网络：1个服务器，2个客户端
        NetworkComponent.Initialize(1, 2);
    }

    AFTER_EACH()
    {
        NetworkComponent.Shutdown();
    }

    TEST_METHOD(ReplicatedVariable_ShouldSyncToClient)
    {
        AMyNetworkActor* ServerActor = NetworkComponent.GetServerWorld()
            ->SpawnActor<AMyNetworkActor>(FVector::ZeroVector);

        const int32 TestValue = 100;
        ServerActor->SetReplicatedValue(TestValue);

        // 等待复制到客户端
        AddCommand(new FWaitUntil([&]() {
            AMyNetworkActor* ClientActor = NetworkComponent.GetClientActor<AMyNetworkActor>(0);
            return ClientActor && ClientActor->GetReplicatedValue() == TestValue;
        }));

        AMyNetworkActor* ClientActor = NetworkComponent.GetClientActor<AMyNetworkActor>(0);
        ASSERT_THAT(AreEqual(TestValue, ClientActor->GetReplicatedValue()));
    }
};
```

### 注意事项
- **必须指定** `EAutomationTestFlags::EditorContext` 标志
- 仅在Editor上下文中可用
- 网络复制是异步的，使用 `FWaitUntil` 而非 `FWaitDelay`
- 测试完成后必须调用 `Shutdown()` 清理

## InputTestActions

### 功能
向Pawn注入InputActions，用于测试输入系统和输入响应。

### 主要方法
```cpp
// 触发输入动作
void TriggerInputAction(UObject* Target, const FName& ActionName, const FInputActionValue& Value);

// 模拟按键按下
void PressKey(UObject* Target, FKey Key);

// 模拟按键释放
void ReleaseKey(UObject* Target, FKey Key);

// 模拟轴输入
void SetAxisValue(UObject* Target, FName AxisName, float Value);
```

### 使用示例
```cpp
#include "CQTest.h"

TEST_CLASS(InputTest, "Game.Input")
{
    AMyCharacter* TestCharacter = nullptr;
    ActorTestSpawner Spawner;

    BEFORE_EACH()
    {
        Spawner.InitializeWorld();
        TestCharacter = Spawner.SpawnActor<AMyCharacter>(FVector::ZeroVector);
        TestCharacter->AutoPossessPlayer = EAutoReceiveInput::Player0;
    }

    AFTER_EACH()
    {
        Spawner.DestroyAllSpawnedActors();
    }

    TEST_METHOD(JumpAction_ShouldTriggerJump)
    {
        const float InitialZ = TestCharacter->GetActorLocation().Z;

        // 触发Jump输入动作
        InputTestActions::TriggerInputAction(
            TestCharacter,
            TEXT("Jump"),
            FInputActionValue(1.0f)
        );

        // 等待跳跃发生
        AddCommand(new FWaitUntil([&]() {
            const float CurrentZ = TestCharacter->GetActorLocation().Z;
            return CurrentZ > InitialZ;
        }));

        ASSERT_THAT(IsTrue(TestCharacter->IsJumping()));
    }
};
```

### 注意事项
- 目标Pawn必须配置好输入映射
- 输入动作名称必须与项目配置一致
- 物理模拟需要时间，使用 `FWaitUntil` 等待结果
- 测试前确保PlayerController已正确关联

## CQTestSlateComponent

### 功能
通知当前测试UI已更新，用于测试Slate/UMG界面。

### 主要方法
```cpp
// 注册UI更新回调
void RegisterOnUIUpdated(TFunction<void()> Callback);

// 触发UI更新通知
void NotifyUIUpdated();
```

### 使用示例
```cpp
TEST_CLASS(UITest, "Game.UI")
{
    UMyUserWidget* TestWidget = nullptr;
    CQTestSlateComponent SlateComponent;
    bool UIUpdated = false;

    BEFORE_EACH()
    {
        SlateComponent.RegisterOnUIUpdated([&]() {
            UIUpdated = true;
        });
    }

    TEST_METHOD(WidgetVisibilityChange_ShouldNotifyUI)
    {
        UIUpdated = false;
        TestWidget->SetVisibility(ESlateVisibility::Hidden);

        // 等待UI更新通知
        AddCommand(new FWaitUntil([&]() {
            return UIUpdated;
        }));

        ASSERT_THAT(IsTrue(UIUpdated));
    }
};
```

### 注意事项
- UI更新是异步的，需要使用Latent Actions等待
- 确保Slate组件在测试期间保持有效
- 避免在回调中执行复杂逻辑

## CQTestAssetHelper

### 功能
命名空间，提供辅助方法用于搜索和过滤资产。

### 主要方法
```cpp
// 按包路径搜索资产
TArray<FAssetData> FindAssetsByPackagePath(const FString& PackagePath);

// 按名称搜索Blueprint
TArray<FAssetData> FindBlueprintsByName(const FString& BlueprintName);

// 使用过滤器构建器搜索资产
TArray<FAssetData> FindAssets(const FAssetFilterBuilder& FilterBuilder);
```

### 使用示例
```cpp
TEST_CLASS(AssetTest, "Game.Asset")
    , public EAutomationTestFlags::EditorContext
{
    TEST_METHOD(FindBlueprint_ByName_ShouldSucceed)
    {
        const FString BlueprintName = TEXT("BP_TestCharacter");

        TArray<FAssetData> FoundAssets = CQTestAssetHelper::FindBlueprintsByName(BlueprintName);

        ASSERT_THAT(IsTrue(FoundAssets.Num() > 0));
        ASSERT_THAT(AreEqual(BlueprintName, FoundAssets[0].AssetName.ToString()));
    }

    TEST_METHOD(FindAssets_InGamePath_ShouldFindAssets)
    {
        FAssetFilterBuilder FilterBuilder;
        FilterBuilder.PackagePath = TEXT("/Game");

        TArray<FAssetData> FoundAssets = CQTestAssetHelper::FindAssets(FilterBuilder);

        ASSERT_THAT(IsTrue(FoundAssets.Num() > 0));
    }
};
```

### 注意事项
- 仅在Editor上下文中可用，需指定 `EAutomationTestFlags::EditorContext`
- Blueprint资产加载较慢，建议使用Latent Actions
- 搜索结果可能包含多个资产，注意验证

## FAssetBuilder

### 功能
创建资产过滤器，用于搜索AssetRegistry。

### 主要属性和方法
```cpp
struct FAssetFilterBuilder
{
    FString PackagePath;           // 包路径（如"/Game"）
    FString ClassName;             // 类名
    FString AssetName;             // 资产名称
    bool Recursive;                // 是否递归搜索

    FAssetFilterBuilder& SetPackagePath(const FString& Path);
    FAssetFilterBuilder& SetClassName(const FString& Class);
    FAssetFilterBuilder& SetAssetName(const FString& Name);
    FAssetFilterBuilder& SetRecursive(bool bInRecursive);
};
```

### 使用示例
```cpp
TEST_METHOD(AssetFilter_CustomSearch_ShouldSucceed)
{
    FAssetFilterBuilder FilterBuilder;
    FilterBuilder.SetPackagePath(TEXT("/Game/Blueprints"))
                .SetClassName(TEXT("Blueprint"))
                .SetRecursive(true);

    TArray<FAssetData> Assets = CQTestAssetHelper::FindAssets(FilterBuilder);

    ASSERT_THAT(IsTrue(Assets.Num() > 0));
}
```

### 注意事项
- 过滤器可以链式调用
- 包路径必须以"/"开头
- 递归搜索会影响性能，尽量缩小搜索范围