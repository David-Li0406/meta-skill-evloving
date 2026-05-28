// Actor测试实现文件模板

#include "CQTest.h"
#include "Helpers/ActorTestHelper.h"

// 如果有自定义测试类头文件
// #include "YourTestActorTest.h"

TEST_CLASS(YourActorTestClass, "Game.Actor")
{
    // 数据成员
    ActorTestSpawner Spawner;
    AYourActor* TestActor = nullptr;
    AOtherActor* OtherActor = nullptr;

    // 在每个测试之前执行
    BEFORE_EACH()
    {
        // 初始化测试世界
        Spawner.InitializeWorld();

        // 生成测试Actor
        TestActor = Spawner.SpawnActor<AYourActor>(FVector::ZeroVector);
        OtherActor = Spawner.SpawnActor<AOtherActor>(FVector(100, 0, 0));
    }

    // 在每个测试之后执行
    AFTER_EACH()
    {
        // 清理所有生成的Actor
        Spawner.DestroyAllSpawnedActors();
    }

    // 测试Actor生成
    TEST_METHOD(SpawnActor_ShouldSucceed)
    {
        ASSERT_THAT(IsNotNull(TestActor));
        ASSERT_THAT(IsTrue(TestActor->IsValidLowLevel()));
        ASSERT_THAT(AreEqual(FVector::ZeroVector, TestActor->GetActorLocation()));
    }

    // 测试Actor属性
    TEST_METHOD(ActorProperties_ShouldBeSetCorrectly)
    {
        const float ExpectedHealth = 100.0f;
        TestActor->SetHealth(ExpectedHealth);

        ASSERT_THAT(AreEqual(ExpectedHealth, TestActor->GetHealth()));
    }

    // 测试Actor行为
    TEST_METHOD(ActorAction_ShouldWork)
    {
        const int32 InitialValue = TestActor->GetValue();
        TestActor->PerformAction();

        ASSERT_THAT(AreEqual(InitialValue + 1, TestActor->GetValue()));
    }

    // 测试Actor交互
    TEST_METHOD(ActorInteraction_ShouldSucceed)
    {
        const bool InteractionResult = TestActor->InteractWith(OtherActor);

        ASSERT_THAT(IsTrue(InteractionResult));
        ASSERT_THAT(IsTrue(OtherActor->WasInteractedWith()));
    }

    // 测试Actor销毁
    TEST_METHOD(ActorDestroy_ShouldCleanup)
    {
        const bool DestroyResult = TestActor->Destroy();

        ASSERT_THAT(IsTrue(DestroyResult));
    }

    // 测试多个Actor
    TEST_METHOD(MultipleActors_ShouldAllSpawn)
    {
        TArray<AYourActor*> Actors;

        for (int32 i = 0; i < 5; i++)
        {
            AYourActor* Actor = Spawner.SpawnActor<AYourActor>(FVector(i * 100, 0, 0));
            Actors.Add(Actor);
            ASSERT_THAT(IsNotNull(Actor));
        }

        ASSERT_THAT(AreEqual(5, Actors.Num()));
    }

    // 使用Latent Actions测试异步操作
    TEST_METHOD(ActorAsyncOperation_ShouldComplete)
    {
        bool OperationComplete = false;

        // 触发异步操作
        TestActor->StartAsyncOperation();
        TestActor->OnOperationComplete.AddLambda([&]() {
            OperationComplete = true;
        });

        // 等待操作完成
        AddCommand(new FWaitUntil([&]() {
            return OperationComplete;
        }, 5.0f));

        ASSERT_THAT(IsTrue(OperationComplete));
    }

    // 使用Command Builder
    TEST_METHOD(ActorWorkflow_UsingCommandBuilder)
    {
        TestCommandBuilder
            .Do([&]() {
                TestActor->Initialize();
            })
            .Until([&]() {
                return TestActor->IsInitialized();
            }, 2.0f)
            .Do([&]() {
                TestActor->Activate();
            })
            .Until([&]() {
                return TestActor->IsActive();
            }, 2.0f)
            .Then([&]() {
                ASSERT_THAT(IsTrue(TestActor->IsInitialized()));
                ASSERT_THAT(IsTrue(TestActor->IsActive()));
            });
    }
};
