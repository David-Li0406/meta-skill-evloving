// Animation测试实现文件模板

#include "CQTest.h"
#include "Animation/AnimInstance.h"
#include "Animation/AnimMontage.h"
#include "GameFramework/Character.h"
#include "Helpers/AnimationTestHelper.h"

TEST_CLASS(AnimationTestClass, "Game.Animation")
{
    // 数据成员
    ACharacter* TestCharacter = nullptr;
    UAnimInstance* AnimInstance = nullptr;
    AnimationTestHelper* AnimHelper = nullptr;
    UAnimMontage* TestMontage = nullptr;

    // 在每个测试之前执行
    BEFORE_EACH()
    {
        // 创建测试角色
        TestCharacter = NewObject<ACharacter>();
        TestCharacter->CreateDefaultSubobject<USkeletalMeshComponent>(TEXT("Mesh"));
        AnimInstance = TestCharacter->GetMesh()->GetAnimInstance();

        // 创建Helper
        AnimHelper = new AnimationTestHelper(AnimInstance);

        // 加载测试蒙太奇（替换为实际路径）
        TestMontage = LoadObject<UAnimMontage>(
            nullptr,
            TEXT("/Game/Animations/TestMontage")
        );
    }

    // 在每个测试之后执行
    AFTER_EACH()
    {
        // 清理Helper
        if (AnimHelper)
        {
            delete AnimHelper;
            AnimHelper = nullptr;
        }

        // 清理角色
        if (TestCharacter)
        {
            TestCharacter->MarkPendingKill();
        }
    }

    // 测试蒙太奇播放
    TEST_METHOD(PlayMontage_ShouldStartSuccessfully)
    {
        if (!TestMontage)
        {
            return; // 蒙太奇未加载，跳过测试
        }

        const bool PlayResult = AnimHelper->PlayMontage(TestMontage);

        ASSERT_THAT(IsTrue(PlayResult));
        ASSERT_THAT(IsTrue(AnimHelper->IsMontagePlaying()));
    }

    // 测试蒙太奇停止
    TEST_METHOD(StopMontage_ShouldStopPlayback)
    {
        if (!TestMontage)
        {
            return;
        }

        AnimHelper->PlayMontage(TestMontage);
        ASSERT_THAT(IsTrue(AnimHelper->IsMontagePlaying()));

        AnimHelper->StopMontage();
        ASSERT_THAT(IsFalse(AnimHelper->IsMontagePlaying()));
    }

    // 测试蒙太奇完成
    TEST_METHOD(MontageComplete_ShouldTriggerEvent)
    {
        if (!TestMontage)
        {
            return;
        }

        bool MontageCompleted = false;

        // 注册蒙太奇完成回调
        AnimHelper->OnMontageEnded.AddLambda([&](UAnimMontage* EndedMontage, bool bInterrupted) {
            if (EndedMontage == TestMontage)
            {
                MontageCompleted = true;
            }
        });

        // 播放蒙太奇
        AnimHelper->PlayMontage(TestMontage);

        // 等待蒙太奇完成
        AddCommand(new FWaitUntil([&]() {
            return MontageCompleted;
        }, 10.0f));

        ASSERT_THAT(IsTrue(MontageCompleted));
    }

    // 测试动画状态机
    TEST_METHOD(StateMachine_Transition_ShouldSucceed)
    {
        // 假设角色有Idle和Run状态
        const FName IdleState = TEXT("Idle");
        const FName RunState = TEXT("Run");

        // 设置初始状态
        AnimHelper->SetAnimationState(IdleState);
        ASSERT_THAT(AreEqual(IdleState, AnimHelper->GetCurrentState()));

        // 触发状态转换（如增加移动速度）
        TestCharacter->GetCharacterMovement()->MaxWalkSpeed = 600.0f;

        // 等待状态转换
        AddCommand(new FWaitUntil([&]() {
            return AnimHelper->GetCurrentState() == RunState;
        }, 2.0f));

        ASSERT_THAT(AreEqual(RunState, AnimHelper->GetCurrentState()));
    }

    // 测试混合空间
    TEST_METHOD(BlendSpace_ShouldBlendCorrectly)
    {
        const float MoveSpeed = 300.0f;
        TestCharacter->GetCharacterMovement()->MaxWalkSpeed = MoveSpeed;

        // 触发移动
        TestCharacter->AddMovementInput(FVector(1, 0, 0), 1.0f);

        // 等待动画系统更新
        AddCommand(new FWaitDelay(0.1f));

        // 验证动画是否正确混合（根据具体实现调整）
        const float CurrentPlaybackSpeed = AnimInstance->GetCurrentActiveMontage()->GetPosition();
        ASSERT_THAT(IsTrue(CurrentPlaybackSpeed > 0.0f));
    }

    // 测试动画通知
    TEST_METHOD(AnimNotify_ShouldBeTriggered)
    {
        bool NotifyTriggered = false;

        // 注册动画通知回调
        AnimInstance->OnPlayMontageNotifyBegin.AddLambda([&](FName NotifyName, const FBranchingPointNotifyPayload& Payload) {
            if (NotifyName == TEXT("TestNotify"))
            {
                NotifyTriggered = true;
            }
        });

        if (!TestMontage)
        {
            return;
        }

        // 播放包含通知的蒙太奇
        AnimHelper->PlayMontage(TestMontage);

        // 等待通知触发
        AddCommand(new FWaitUntil([&]() {
            return NotifyTriggered;
        }, 5.0f));

        ASSERT_THAT(IsTrue(NotifyTriggered));
    }

    // 使用Command Builder测试复杂动画流程
    TEST_METHOD(AnimationWorkflow_UsingCommandBuilder)
    {
        if (!TestMontage)
        {
            return;
        }

        bool AnimationStarted = false;
        bool AnimationCompleted = false;

        AnimHelper->OnMontageBlendingOutStarted.AddLambda([&](UAnimMontage* Montage, bool bInterrupted) {
            AnimationStarted = true;
        });

        AnimHelper->OnMontageEnded.AddLambda([&](UAnimMontage* Montage, bool bInterrupted) {
            if (Montage == TestMontage)
            {
                AnimationCompleted = true;
            }
        });

        TestCommandBuilder
            // 播放动画
            .Do([&]() {
                AnimHelper->PlayMontage(TestMontage);
            })
            // 等待动画开始
            .Until([&]() {
                return AnimationStarted;
            }, 1.0f)
            // 验证动画正在播放
            .Then([&]() {
                ASSERT_THAT(IsTrue(AnimHelper->IsMontagePlaying()));
            })
            // 等待动画完成
            .Until([&]() {
                return AnimationCompleted;
            }, 10.0f)
            // 验证动画已停止
            .Then([&]() {
                ASSERT_THAT(IsFalse(AnimHelper->IsMontagePlaying()));
            });
    }

    // 测试多个蒙太奇队列
    TEST_METHOD(MontageQueue_ShouldPlaySequentially)
    {
        if (!TestMontage)
        {
            return;
        }

        TArray<UAnimMontage*> Montages;
        Montages.Add(TestMontage);
        Montages.Add(TestMontage); // 可以使用不同的蒙太奇

        int32 CurrentIndex = 0;
        int32 CompletedMontages = 0;

        AnimHelper->OnMontageEnded.AddLambda([&](UAnimMontage* Montage, bool bInterrupted) {
            if (Montage == Montages[CurrentIndex])
            {
                CompletedMontages++;
                CurrentIndex++;

                if (CurrentIndex < Montages.Num())
                {
                    // 播放下一个蒙太奇
                    AnimHelper->PlayMontage(Montages[CurrentIndex]);
                }
            }
        });

        // 开始播放第一个蒙太奇
        AnimHelper->PlayMontage(Montages[0]);

        // 等待所有蒙太奇完成
        AddCommand(new FWaitUntil([&]() {
            return CompletedMontages == Montages.Num();
        }, 20.0f));

        ASSERT_THAT(AreEqual(Montages.Num(), CompletedMontages));
    }
};
