# 测试类型详解

## 目录
- [概述](#概述)
- [基础测试](#基础测试)
- [结构化测试（TEST_CLASS）](#结构化测试test_class)
- [Actor测试](#actor测试)
- [Animation测试](#animation测试)
- [Input测试](#input测试)
- [Network测试](#network测试)
- [Map测试](#map测试)

## 概述
CQTest支持多种类型的测试，从简单的逻辑验证到复杂的游戏系统集成测试。选择合适的测试类型可以提高测试效率和可维护性。

## 基础测试

### 使用场景
- 简单的逻辑验证
- 独立的功能测试
- 不需要Setup/Teardown的测试
- 单次执行的验证

### 模板和示例
```cpp
#include "CQTest.h"

TEST(MathUtilsTest, "Game.Math")
{
    // 测试数学工具函数
    const float Result = FMath::Max(10.0f, 20.0f);
    ASSERT_THAT(AreEqual(20.0f, Result));
}

TEST(StringManipulationTest, "Game.String")
{
    // 测试字符串处理
    FString TestString = TEXT("Hello World");
    TestString = TestString.ToUpper();

    ASSERT_THAT(AreEqual(TEXT("HELLO WORLD"), TestString));
}

TEST(InventoryValidationTest, "Game.Inventory")
{
    // 验证背包系统逻辑（无需Actor）
    const int32 MaxCapacity = 100;
    const int32 CurrentLoad = 50;
    const bool CanAddItem = (CurrentLoad < MaxCapacity);

    ASSERT_THAT(IsTrue(CanAddItem));
}
```

### 最佳实践
- 保持测试简单和专注
- 每个测试只验证一个逻辑点
- 使用清晰的测试名称描述预期行为
- 避免在基础测试中进行复杂设置

## 结构化测试（TEST_CLASS）

### 使用场景
- 需要Setup/Teardown的测试
- 多个测试共享相同的设置
- 需要维护测试间状态
- 测试场景相关的功能组

### 模板和示例
```cpp
#include "CQTest.h"

TEST_CLASS(PlayerHealthTest, "Game.Character.Health")
{
    APlayerCharacter* TestPlayer = nullptr;
    float InitialHealth = 100.0f;

    BEFORE_EACH()
    {
        // 每个测试前初始化
        TestPlayer = NewObject<APlayerCharacter>();
        TestPlayer->SetHealth(InitialHealth);
    }

    AFTER_EACH()
    {
        // 每个测试后清理
        if (TestPlayer)
        {
            TestPlayer->MarkPendingKill();
        }
    }

    TEST_METHOD(Damage_ShouldReduceHealth)
    {
        const float DamageAmount = 20.0f;
        TestPlayer->TakeDamage(DamageAmount, FDamageEvent(), nullptr, nullptr);

        ASSERT_THAT(AreEqual(80.0f, TestPlayer->GetHealth()));
    }

    TEST_METHOD(Heal_ShouldNotExceedMaxHealth)
    {
        TestPlayer->TakeDamage(50.0f, FDamageEvent(), nullptr, nullptr);
        TestPlayer->Heal(100.0f);

        ASSERT_THAT(AreEqual(100.0f, TestPlayer->GetHealth()));
    }

    TEST_METHOD(Death_ShouldTriggerEvent)
    {
        bool DeathEventTriggered = false;
        TestPlayer->OnDeath.AddLambda([&]() { DeathEventTriggered = true; });

        TestPlayer->TakeDamage(150.0f, FDamageEvent(), nullptr, nullptr);

        ASSERT_THAT(IsTrue(DeathEventTriggered));
    }
};
```

### 最佳实践
- 使用BEFORE_EACH/AFTER_EACH确保测试独立性
- 将相关测试组织在同一个TEST_CLASS中
- 避免在不同测试之间共享可变状态
- 使用protected辅助方法减少重复代码

## Actor测试

### 使用场景
- 测试Actor的生命周期和行为
- 验证Actor之间的交互
- 测试组件和子对象
- 模拟游戏场景中的Actor

### 模板和示例
```cpp
#include "CQTest.h"
#include "Helpers/ActorTestHelper.h"

TEST_CLASS(WeaponSystemTest, "Game.Weapon")
{
    ActorTestSpawner Spawner;
    AWeaponActor* TestWeapon = nullptr;
    ACharacter* TestCharacter = nullptr;

    BEFORE_EACH()
    {
        Spawner.InitializeWorld();
        TestCharacter = Spawner.SpawnActor<ACharacter>(FVector::ZeroVector);
        TestWeapon = Spawner.SpawnActor<AWeaponActor>(FVector(100, 0, 0));
    }

    AFTER_EACH()
    {
        Spawner.DestroyAllSpawnedActors();
    }

    TEST_METHOD(EquipWeapon_ShouldAttachToCharacter)
    {
        TestCharacter->EquipWeapon(TestWeapon);

        ASSERT_THAT(IsTrue(TestWeapon->IsAttachedTo(TestCharacter)));
        ASSERT_THAT(AreEqual(TestCharacter, TestWeapon->GetOwner()));
    }

    TEST_METHOD(FireWeapon_ShouldReduceAmmo)
    {
        const int32 InitialAmmo = TestWeapon->GetCurrentAmmo();
        TestWeapon->Fire();

        ASSERT_THAT(AreEqual(InitialAmmo - 1, TestWeapon->GetCurrentAmmo()));
    }

    TEST_METHOD(Reload_WithFullAmmo_ShouldFail)
    {
        TestWeapon->SetAmmo(TestWeapon->GetMaxAmmo());
        const bool ReloadResult = TestWeapon->Reload();

        ASSERT_THAT(IsFalse(ReloadResult));
    }

    TEST_METHOD(WeaponDestroy_Character_ShouldUnequip)
    {
        TestCharacter->EquipWeapon(TestWeapon);
        TestWeapon->Destroy();

        ASSERT_THAT(IsNull(TestCharacter->GetCurrentWeapon()));
    }
};
```

### 使用ActorTestHelper
ActorTestHelper提供了简化的API用于常见操作：

```cpp
#include "Helpers/ActorTestHelper.h"

TEST_CLASS(AdvancedActorTest, "Game.Actor")
{
    AMyActor* TestActor = nullptr;

    TEST_METHOD(SpawnAndInitialize_UsingHelper)
    {
        // 使用Helper简化Actor创建
        TestActor = ActorTestHelper::SpawnActor<AMyActor>(
            FVector::ZeroVector,
            FRotator::ZeroRotator
        );

        ASSERT_THAT(IsNotNull(TestActor));
        ASSERT_THAT(IsTrue(ActorTestHelper::InitializeActor(TestActor)));
    }

    TEST_METHOD(SetActorProperty_UsingHelper)
    {
        TestActor = ActorTestHelper::SpawnActor<AMyActor>(FVector::ZeroVector);

        // 使用Helper设置属性
        ActorTestHelper::SetActorProperty(TestActor, "Health", 100.0f);

        ASSERT_THAT(AreEqual(100.0f, TestActor->GetHealth()));
    }
};
```

### 最佳实践
- 总是使用ActorTestSpawner管理Actor生命周期
- 确保在AFTER_EACH中清理所有生成的Actor
- 使用AFTER_EACH清理，即使测试失败也会执行
- 避免在测试中依赖特定的Actor ID或索引

## Animation测试

### 使用场景
- 测试动画播放和混合
- 验证动画状态机转换
- 测试动画通知事件
- 验证动画序列和蒙太奇

### 模板和示例
```cpp
#include "CQTest.h"
#include "Helpers/AnimationTestHelper.h"

TEST_CLASS(AnimationSystemTest, "Game.Animation")
{
    ACharacter* TestCharacter = nullptr;
    UAnimInstance* AnimInstance = nullptr;
    AnimationTestHelper* AnimHelper = nullptr;

    BEFORE_EACH()
    {
        TestCharacter = NewObject<ACharacter>();
        AnimInstance = TestCharacter->GetMesh()->GetAnimInstance();
        AnimHelper = new AnimationTestHelper(AnimInstance);
    }

    AFTER_EACH()
    {
        delete AnimHelper;
    }

    TEST_METHOD(PlayMontage_ShouldStartSuccessfully)
    {
        UAnimMontage* TestMontage = LoadObj<UAnimMontage>(TEXT("/Game/Animations/TestMontage"));

        const bool PlayResult = AnimHelper->PlayMontage(TestMontage);

        ASSERT_THAT(IsTrue(PlayResult));
        ASSERT_THAT(IsTrue(AnimHelper->IsMontagePlaying()));
    }

    TEST_METHOD(MontageComplete_ShouldTriggerEvent)
    {
        UAnimMontage* TestMontage = LoadObj<UAnimMontage>(TEXT("/Game/Animations/TestMontage"));
        bool MontageCompleted = false;

        AnimHelper->OnMontageCompleted.AddLambda([&]() {
            MontageCompleted = true;
        });

        AnimHelper->PlayMontage(TestMontage);

        // 等待蒙太奇完成
        AddCommand(new FWaitUntil([&]() {
            return MontageCompleted;
        }, 5.0f)); // 5秒超时

        ASSERT_THAT(IsTrue(MontageCompleted));
    }

    TEST_METHOD(StateMachine_Transition_ShouldSucceed)
    {
        // 设置初始状态
        AnimInstance->TrySetAnimationState(EAnimationState::Idle);

        // 触发状态转换
        AnimInstance->SetMovementSpeed(100.0f);

        // 等待状态转换
        AddCommand(new FWaitUntil([&]() {
            return AnimInstance->GetCurrentState() == EAnimationState::Running;
        }, 2.0f));

        ASSERT_THAT(AreEqual(EAnimationState::Running, AnimInstance->GetCurrentState()));
    }
};
```

### 最佳实践
- 使用 `FWaitUntil` 等待动画完成，避免使用固定延迟
- 测试动画通知事件时注册回调并等待触发
- 动画是异步的，确保测试有足够的等待时间
- 测试状态机转换时验证中间状态和最终状态

## Input测试

### 使用场景
- 验证输入动作触发
- 测试输入响应逻辑
- 测试按键绑定
- 验证轴输入处理

### 模板和示例
```cpp
#include "CQTest.h"
#include "Helpers/InputTestHelper.h"

TEST_CLASS(InputSystemTest, "Game.Input")
{
    AMyCharacter* TestCharacter = nullptr;
    ActorTestSpawner Spawner;

    BEFORE_EACH()
    {
        Spawner.InitializeWorld();
        TestCharacter = Spawner.SpawnActor<AMyCharacter>(FVector::ZeroVector);
        TestCharacter->AutoPossessPlayer = EAutoReceiveInput::Player0;
        InputTestHelper::Initialize(TestCharacter);
    }

    AFTER_EACH()
    {
        Spawner.DestroyAllSpawnedActors();
    }

    TEST_METHOD(JumpAction_ShouldTriggerJump)
    {
        const float InitialZ = TestCharacter->GetActorLocation().Z;

        // 触发Jump输入
        InputTestHelper::TriggerAction(TEXT("Jump"));

        // 等待角色跳跃
        AddCommand(new FWaitUntil([&]() {
            return TestCharacter->GetActorLocation().Z > InitialZ;
        }, 1.0f));

        ASSERT_THAT(IsTrue(TestCharacter->IsJumping()));
    }

    TEST_METHOD(MovementInput_ShouldMoveCharacter)
    {
        const FVector InitialLocation = TestCharacter->GetActorLocation();

        // 持续移动输入
        InputTestHelper::SetAxisValue(TEXT("MoveForward"), 1.0f);

        // 等待移动发生
        AddCommand(new FWaitUntil([&]() {
            const float Distance = FVector::Distance(
                InitialLocation,
                TestCharacter->GetActorLocation()
            );
            return Distance > 100.0f;
        }, 2.0f));

        // 停止移动
        InputTestHelper::SetAxisValue(TEXT("MoveForward"), 0.0f);

        const FVector FinalLocation = TestCharacter->GetActorLocation();
        const float DistanceMoved = FVector::Distance(InitialLocation, FinalLocation);

        ASSERT_THAT(IsTrue(DistanceMoved > 100.0f));
    }

    TEST_METHOD(FireAction_ShouldDecreaseAmmo)
    {
        const int32 InitialAmmo = TestCharacter->GetWeaponAmmo();

        // 触发射击动作
        InputTestHelper::TriggerAction(TEXT("Fire"));

        // 等待射击逻辑执行
        AddCommand(new FWaitDelay(0.1f));

        ASSERT_THAT(AreEqual(InitialAmmo - 1, TestCharacter->GetWeaponAmmo()));
    }
};
```

### 最佳实践
- 确保输入动作名称与项目输入映射配置一致
- 使用FWaitUntil等待输入结果，而非固定延迟
- 测试结束后重置所有输入状态
- 对于持续输入（如移动），测试完成后停止输入

## Network测试

### 使用场景
- 测试网络复制变量同步
- 验证RPC调用
- 测试多客户端场景
- 测试网络条件下的游戏逻辑

### 模板和示例
```cpp
#include "CQTest.h"
#include "Helpers/NetworkTestHelper.h"

TEST_CLASS(NetworkReplicationTest, "Game.Network")
    , public EAutomationTestFlags::EditorContext
{
    PIENetworkComponent NetworkComponent;
    AMyNetworkActor* ServerActor = nullptr;

    BEFORE_EACH()
    {
        // 初始化网络：1服务器，2客户端
        NetworkComponent.Initialize(1, 2);

        // 在服务器上创建Actor
        ServerActor = NetworkComponent.GetServerWorld()
            ->SpawnActor<AMyNetworkActor>(FVector::ZeroVector);
    }

    AFTER_EACH()
    {
        NetworkComponent.Shutdown();
    }

    TEST_METHOD(ReplicatedVariable_ShouldSyncToClients)
    {
        const int32 TestValue = 42;
        ServerActor->SetReplicatedValue(TestValue);

        // 等待复制到客户端0
        AddCommand(new FWaitUntil([&]() {
            AMyNetworkActor* ClientActor = NetworkComponent.GetClientActor<AMyNetworkActor>(0);
            return ClientActor && ClientActor->GetReplicatedValue() == TestValue;
        }, 5.0f));

        // 等待复制到客户端1
        AddCommand(new FWaitUntil([&]() {
            AMyNetworkActor* ClientActor = NetworkComponent.GetClientActor<AMyNetworkActor>(1);
            return ClientActor && ClientActor->GetReplicatedValue() == TestValue;
        }, 5.0f));

        AMyNetworkActor* Client0Actor = NetworkComponent.GetClientActor<AMyNetworkActor>(0);
        AMyNetworkActor* Client1Actor = NetworkComponent.GetClientActor<AMyNetworkActor>(1);

        ASSERT_THAT(AreEqual(TestValue, Client0Actor->GetReplicatedValue()));
        ASSERT_THAT(AreEqual(TestValue, Client1Actor->GetReplicatedValue()));
    }

    TEST_METHOD(ServerRPC_ShouldExecuteOnServer)
    {
        bool RPCExecuted = false;
        ServerActor->OnServerRPCCalled.AddLambda([&]() { RPCExecuted = true; });

        // 从客户端调用服务器RPC
        AMyNetworkActor* ClientActor = NetworkComponent.GetClientActor<AMyNetworkActor>(0);
        ClientActor->Server_ExecuteRPC();

        // 等待RPC执行
        AddCommand(new FWaitUntil([&]() {
            return RPCExecuted;
        }, 2.0f));

        ASSERT_THAT(IsTrue(RPCExecuted));
    }

    TEST_METHOD(ClientRPC_ShouldExecuteOnClient)
    {
        bool RPCExecuted = false;
        AMyNetworkActor* ClientActor = NetworkComponent.GetClientActor<AMyNetworkActor>(0);
        ClientActor->OnClientRPCCalled.AddLambda([&]() { RPCExecuted = true; });

        // 从服务器调用客户端RPC
        ServerActor->Client_ExecuteRPC(ClientActor);

        // 等待RPC执行
        AddCommand(new FWaitUntil([&]() {
            return RPCExecuted;
        }, 2.0f));

        ASSERT_THAT(IsTrue(RPCExecuted));
    }
};
```

### AsyncMessageTestActor使用
AsyncMessageTestActor用于测试异步网络消息：

```cpp
TEST_CLASS(AsyncNetworkTest, "Game.Network.Async")
    , public EAutomationTestFlags::EditorContext
{
    AAsyncMessageTestActor* TestActor = nullptr;

    TEST_METHOD(AsyncMessage_ShouldBeReceived)
    {
        // 创建异步消息测试Actor
        TestActor = GetWorld()->SpawnActor<AAsyncMessageTestActor>();

        // 发送异步消息
        TestActor->SendAsyncMessage(TEXT("TestMessage"));

        // 等待消息接收
        AddCommand(new FWaitUntil([&]() {
            return TestActor->HasReceivedMessage(TEXT("TestMessage"));
        }, 3.0f));

        ASSERT_THAT(IsTrue(TestActor->HasReceivedMessage(TEXT("TestMessage"))));
    }
};
```

### 最佳实践
- **必须**指定 `EAutomationTestFlags::EditorContext` 标志
- 网络复制是异步的，使用 `FWaitUntil` 等待
- 测试多客户端场景时，验证每个客户端的状态
- RPC测试时，验证调用端和执行端的行为
- 测试完成后调用 `Shutdown()` 清理网络环境

## Map测试

### 使用场景
- 在特定关卡中测试功能
- 验证关卡加载和卸载
- 测试场景特定的逻辑
- 测试关卡中的Actor交互

### 模板和示例
```cpp
#include "CQTest.h"

TEST_CLASS(MapLoadingTest, "Game.Map")
    , public EAutomationTestFlags::EditorContext
{
    MapTestSpawner MapSpawner;

    BEFORE_EACH()
    {
        // 加载测试关卡
        const bool LoadResult = MapSpawner.LoadMap(TEXT("/Game/Maps/TestLevel"));
        ASSERT_THAT(IsTrue(LoadResult));
    }

    AFTER_EACH()
    {
        MapSpawner.UnloadMap();
    }

    TEST_METHOD(SpawnActorInMap_Success)
    {
        UWorld* World = MapSpawner.GetCurrentWorld();
        ASSERT_THAT(IsNotNull(World));

        AMyActor* Actor = World->SpawnActor<AMyActor>(FVector::ZeroVector);

        ASSERT_THAT(IsNotNull(Actor));
        ASSERT_THAT(IsTrue(Actor->IsValidLowLevel()));
    }

    TEST_METHOD(LevelActors_ShouldBePresent)
    {
        UWorld* World = MapSpawner.GetCurrentWorld();
        TArray<AActor*> FoundActors;
        UGameplayStatics::GetAllActorsOfClass(World, AMyLevelActor::StaticClass(), FoundActors);

        ASSERT_THAT(IsTrue(FoundActors.Num() > 0));
    }

    TEST_METHOD(GameMode_ShouldBeCorrectType)
    {
        UWorld* World = MapSpawner.GetCurrentWorld();
        AGameModeBase* GameMode = World->GetAuthGameMode();

        ASSERT_THAT(IsNotNull(GameMode));
        ASSERT_THAT(IsTrue(GameMode->IsA(AMyGameMode::StaticClass())));
    }
};
```

### 使用MapTestSpawner的高级功能

```cpp
TEST_METHOD(SpawnAtSpecificLocation_ShouldSucceed)
{
    UWorld* World = MapSpawner.GetCurrentWorld();
    const FVector SpawnLocation = FVector(100, 200, 300);

    AMyActor* Actor = World->SpawnActor<AMyActor>(
        SpawnLocation,
        FRotator::ZeroRotator
    );

    ASSERT_THAT(AreEqual(SpawnLocation, Actor->GetActorLocation()));
}

TEST_METHOD(UnloadMap_ShouldCleanUpActors)
{
    UWorld* World = MapSpawner.GetCurrentWorld();
    World->SpawnActor<AMyActor>(FVector::ZeroVector);

    MapSpawner.UnloadMap();

    // 验证关卡已卸载
    ASSERT_THAT(IsNull(MapSpawner.GetCurrentWorld()));
}
```

### 最佳实践
- 加载大型关卡会影响性能，使用小型测试关卡
- 关卡加载是异步的，使用Latent Actions等待
- 测试后始终卸载关卡，避免内存泄漏
- 验证关卡中的Actor和GameMode是否符合预期
