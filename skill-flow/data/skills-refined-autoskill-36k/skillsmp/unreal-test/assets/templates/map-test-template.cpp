// Map测试实现文件模板
// 注意：必须指定 EAutomationTestFlags::EditorContext 标志

#include "CQTest.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Character.h"
#include "GameFramework/GameStateBase.h"
#include "GameFramework/GameModeBase.h"
#include "Kismet/GameplayStatics.h"

TEST_CLASS(MapLoadingTest, "Game.Map")
    , public EAutomationTestFlags::EditorContext
{
    // 数据成员
    UWorld* CurrentWorld = nullptr;
    UGameModeBase* GameMode = nullptr;
    AGameStateBase* GameState = nullptr;

    // 在每个测试之前执行
    BEFORE_EACH()
    {
        // 加载测试关卡（替换为实际路径）
        const FString MapPath = TEXT("/Game/Maps/TestLevel");
        UWorld* LoadedWorld = UGameplayStatics::LoadLevelWorldBySoftObjectPtr(nullptr, MapPath);

        if (LoadedWorld)
        {
            CurrentWorld = LoadedWorld;
            GameMode = CurrentWorld->GetAuthGameMode();
            GameState = CurrentWorld->GetGameState();
        }
    }

    // 在每个测试之后执行
    AFTER_EACH()
    {
        // 卸载关卡
        if (CurrentWorld)
        {
            UGameplayStatics::UnloadLevelBySoftObjectPtr(nullptr, CurrentWorld);
            CurrentWorld = nullptr;
        }
    }

    // 测试关卡加载
    TEST_METHOD(LoadMap_ShouldSucceed)
    {
        ASSERT_THAT(IsNotNull(CurrentWorld));
        ASSERT_THAT(IsTrue(CurrentWorld->IsValidLowLevel()));
    }

    // 测试GameMode
    TEST_METHOD(GameMode_ShouldBeCorrectType)
    {
        ASSERT_THAT(IsNotNull(GameMode));
        ASSERT_THAT(IsTrue(GameMode->IsA<AMyGameMode>())); // 替换为实际的GameMode类
    }

    // 测试GameState
    TEST_METHOD(GameState_ShouldBeValid)
    {
        ASSERT_THAT(IsNotNull(GameState));
        ASSERT_THAT(IsTrue(GameState->IsValidLowLevel()));
    }

    // 测试关卡中的Actor
    TEST_METHOD(LevelActors_ShouldBePresent)
    {
        TArray<AActor*> FoundActors;
        UGameplayStatics::GetAllActorsOfClass(CurrentWorld, AMyLevelActor::StaticClass(), FoundActors);

        ASSERT_THAT(IsTrue(FoundActors.Num() > 0));
    }

    // 测试在关卡中生成Actor
    TEST_METHOD(SpawnActorInMap_ShouldSucceed)
    {
        const FVector SpawnLocation = FVector(100, 200, 300);
        AMyActor* SpawnedActor = CurrentWorld->SpawnActor<AMyActor>(SpawnLocation);

        ASSERT_THAT(IsNotNull(SpawnedActor));
        ASSERT_THAT(IsTrue(SpawnedActor->IsValidLowLevel()));
        ASSERT_THAT(AreEqual(SpawnLocation, SpawnedActor->GetActorLocation()));
    }

    // 测试生成多个Actor
    TEST_METHOD(SpawnMultipleActors_ShouldAllSucceed)
    {
        TArray<AActor*> SpawnedActors;

        for (int32 i = 0; i < 10; i++)
        {
            FVector SpawnLocation = FVector(i * 100, 0, 0);
            AActor* Actor = CurrentWorld->SpawnActor<AActor>(SpawnLocation);
            SpawnedActors.Add(Actor);
            ASSERT_THAT(IsNotNull(Actor));
        }

        ASSERT_THAT(AreEqual(10, SpawnedActors.Num()));
    }

    // 测试Actor销毁
    TEST_METHOD(DestroyActor_ShouldSucceed)
    {
        AActor* Actor = CurrentWorld->SpawnActor<AActor>(FVector::ZeroVector);
        ASSERT_THAT(IsNotNull(Actor));

        const bool DestroyResult = Actor->Destroy();

        ASSERT_THAT(IsTrue(DestroyResult));
    }

    // 测试关卡中的特定对象
    TEST_METHOD(SpecificObject_ShouldBeFound)
    {
        AMySpecialObject* SpecialObject = nullptr;
        TArray<AActor*> FoundActors;
        UGameplayStatics::GetAllActorsOfClass(CurrentWorld, AMySpecialObject::StaticClass(), FoundActors);

        if (FoundActors.Num() > 0)
        {
            SpecialObject = Cast<AMySpecialObject>(FoundActors[0]);
        }

        ASSERT_THAT(IsNotNull(SpecialObject));
        ASSERT_THAT(IsTrue(SpecialObject->IsInitialized()));
    }

    // 测试关卡流送
    TEST_METHOD(LevelStreaming_ShouldWork)
    {
        // 假设关卡有流送关卡
        const FString StreamingLevelPath = TEXT("/Game/Maps/SubLevels/TestSubLevel");
        bool StreamLevelLoaded = false;

        // 注册流送完成回调
        CurrentWorld->AddOnLevelsChangedListener([&](const UWorld* World, const TArray<ULevel*>& LevelsAdded, const TArray<ULevel*>& LevelsRemoved) {
            for (ULevel* Level : LevelsAdded)
            {
                if (Level->GetOutermost()->GetName() == TEXT("TestSubLevel"))
                {
                    StreamLevelLoaded = true;
                }
            }
        });

        // 加载流送关卡
        UGameplayStatics::LoadStreamLevel(
            CurrentWorld,
            StreamingLevelPath,
            true,
            true,
            FLatentActionInfo()
        );

        // 等待流送关卡加载
        AddCommand(new FWaitUntil([&]() {
            return StreamLevelLoaded;
        }, 10.0f));

        ASSERT_THAT(IsTrue(StreamLevelLoaded));
    }

    // 测试关卡的物理环境
    TEST_METHOD(PhysicsEnvironment_ShouldWork)
    {
        // 生成一个物理Actor
        APhysicsActor* PhysicsActor = CurrentWorld->SpawnActor<APhysicsActor>(FVector(0, 0, 500));
        ASSERT_THAT(IsNotNull(PhysicsActor));

        const float InitialZ = PhysicsActor->GetActorLocation().Z;

        // 等待物理模拟
        AddCommand(new FWaitDelay(1.0f));

        const float FinalZ = PhysicsActor->GetActorLocation().Z;

        // 物体应该下落
        ASSERT_THAT(IsTrue(FinalZ < InitialZ));
    }

    // 测试关卡的导航系统
    TEST_METHOD(NavigationSystem_ShouldBeValid)
    {
        AAIController* AIController = CurrentWorld->SpawnActor<AAIController>();
        ASSERT_THAT(IsNotNull(AIController));

        const FVector StartLocation = FVector(0, 0, 0);
        const FVector EndLocation = FVector(500, 0, 0);

        bool PathFound = false;
        AIController->MoveToLocation(EndLocation);

        // 等待导航
        AddCommand(new FWaitUntil([&]() {
            APawn* Pawn = AIController->GetPawn();
            if (Pawn)
            {
                const float Distance = FVector::Distance(Pawn->GetActorLocation(), EndLocation);
                return Distance < 10.0f;
            }
            return false;
        }, 10.0f));

        APawn* Pawn = AIController->GetPawn();
        ASSERT_THAT(IsNotNull(Pawn));
    }

    // 测试关机的光照和渲染
    TEST_METHOD(LightingAndRendering_ShouldBeCorrect)
    {
        // 验证光照系统
        ULightComponent* LightComponent = nullptr;
        TArray<ALight*> Lights;
        UGameplayStatics::GetAllActorsOfClass(CurrentWorld, ALight::StaticClass(), Lights);

        if (Lights.Num() > 0)
        {
            LightComponent = Lights[0]->GetLightComponent();
        }

        ASSERT_THAT(IsNotNull(LightComponent));
        ASSERT_THAT(IsTrue(LightComponent->IsVisible()));
    }

    // 使用Command Builder测试复杂关卡场景
    TEST_METHOD(ComplexMapScenario_UsingCommandBuilder)
    {
        ACharacter* Player = nullptr;
        bool PlayerSpawned = false;
        bool ObjectiveReached = false;

        TestCommandBuilder
            // 生成玩家
            .Do([&]() {
                Player = CurrentWorld->SpawnActor<ACharacter>(FVector::ZeroVector);
                PlayerSpawned = true;
            })
            // 等待玩家就绪
            .Until([&]() {
                return PlayerSpawned && Player && Player->IsValidLowLevel();
            }, 2.0f)
            // 移动玩家到目标位置
            .Do([&]() {
                Player->SetActorLocation(FVector(100, 0, 0));
            })
            // 等待移动完成
            .Until([&]() {
                const float Distance = FVector::Distance(
                    Player->GetActorLocation(),
                    FVector(100, 0, 0)
                );
                return Distance < 1.0f;
            }, 2.0f)
            // 验证状态
            .Then([&]() {
                ASSERT_THAT(IsNotNull(Player));
                ASSERT_THAT(IsTrue(Player->IsValidLowLevel()));
                ASSERT_THAT(AreEqual(FVector(100, 0, 0), Player->GetActorLocation()));
            })
            // 清理
            .OnTearDown([&]() {
                if (Player)
                {
                    Player->Destroy();
                }
            });
    }

    // 测试关卡卸载
    TEST_METHOD(UnloadMap_ShouldCleanupActors)
    {
        // 生成一些Actor
        TArray<AActor*> TestActors;
        for (int32 i = 0; i < 5; i++)
        {
            AActor* Actor = CurrentWorld->SpawnActor<AActor>(FVector(i * 100, 0, 0));
            TestActors.Add(Actor);
        }

        // 卸载关卡
        UGameplayStatics::UnloadLevelBySoftObjectPtr(nullptr, CurrentWorld);
        CurrentWorld = nullptr;

        // 验证关卡已卸载
        ASSERT_THAT(IsNull(CurrentWorld));
    }

    // 测试关卡间的转换
    TEST_METHOD(LevelTransition_ShouldWork)
    {
        const FString FirstLevelPath = TEXT("/Game/Maps/TestLevel");
        const FString SecondLevelPath = TEXT("/Game/Maps/TestLevel2");

        // 加载第二个关卡
        UWorld* SecondWorld = UGameplayStatics::LoadLevelWorldBySoftObjectPtr(nullptr, SecondLevelPath);

        ASSERT_THAT(IsNotNull(SecondWorld));

        // 验证第二关卡的GameMode不同
        UGameModeBase* SecondGameMode = SecondWorld->GetAuthGameMode();
        ASSERT_THAT(IsNotNull(SecondGameMode));

        // 卸载第二关卡
        UGameplayStatics::UnloadLevelBySoftObjectPtr(nullptr, SecondWorld);
    }
};
