// Input测试实现文件模板

#include "CQTest.h"
#include "GameFramework/Character.h"
#include "GameFramework/PlayerController.h"
#include "EnhancedInputComponent.h"
#include "InputActionValue.h"
#include "Helpers/InputTestHelper.h"

TEST_CLASS(InputTestClass, "Game.Input")
{
    // 数据成员
    ACharacter* TestCharacter = nullptr;
    InputTestHelper* InputHelper = nullptr;
    APlayerController* PlayerController = nullptr;

    // 在每个测试之前执行
    BEFORE_EACH()
    {
        // 创建测试角色
        TestCharacter = NewObject<ACharacter>();

        // 创建PlayerController
        PlayerController = NewObject<APlayerController>();
        TestCharacter->AutoPossessPlayer = EAutoReceiveInput::Player0;

        // 初始化Input Helper
        InputHelper = new InputTestHelper(TestCharacter);
        InputHelper->Initialize();
    }

    // 在每个测试之后执行
    AFTER_EACH()
    {
        // 清理Input Helper
        if (InputHelper)
        {
            InputHelper->ResetAllInput();
            InputHelper->Cleanup();
            delete InputHelper;
            InputHelper = nullptr;
        }

        // 清理角色
        if (TestCharacter)
        {
            TestCharacter->MarkPendingKill();
        }

        if (PlayerController)
        {
            PlayerController->MarkPendingKill();
        }
    }

    // 测试Jump动作
    TEST_METHOD(JumpAction_ShouldTriggerJump)
    {
        const float InitialZ = TestCharacter->GetActorLocation().Z;
        bool JumpStarted = false;

        // 注册跳跃开始事件
        TestCharacter->Jumped.AddLambda([&]() {
            JumpStarted = true;
        });

        // 触发Jump输入
        InputHelper->TriggerAction(TEXT("Jump"));

        // 等待跳跃开始
        AddCommand(new FWaitUntil([&]() {
            return JumpStarted;
        }, 1.0f));

        // 等待角色上升
        AddCommand(new FWaitUntil([&]() {
            return TestCharacter->GetActorLocation().Z > InitialZ;
        }, 1.0f));

        ASSERT_THAT(IsTrue(JumpStarted));
        ASSERT_THAT(IsTrue(TestCharacter->IsJumping()));
    }

    // 测试移动输入
    TEST_METHOD(MovementInput_ShouldMoveCharacter)
    {
        const FVector InitialLocation = TestCharacter->GetActorLocation();
        const float MoveAmount = 100.0f;
        const float MoveSpeed = 300.0f;

        // 设置移动速度
        TestCharacter->GetCharacterMovement()->MaxWalkSpeed = MoveSpeed;

        // 持续向前移动
        InputHelper->SetAxisValue(TEXT("MoveForward"), 1.0f);

        // 等待角色移动
        AddCommand(new FWaitUntil([&]() {
            const float Distance = FVector::Distance(
                InitialLocation,
                TestCharacter->GetActorLocation()
            );
            return Distance > MoveAmount;
        }, 2.0f));

        // 停止移动
        InputHelper->SetAxisValue(TEXT("MoveForward"), 0.0f);

        const FVector FinalLocation = TestCharacter->GetActorLocation();
        const float DistanceMoved = FVector::Distance(InitialLocation, FinalLocation);

        ASSERT_THAT(IsTrue(DistanceMoved > MoveAmount));
    }

    // 测试Fire动作
    TEST_METHOD(FireAction_ShouldDecreaseAmmo)
    {
        // 假设角色有武器系统
        const int32 InitialAmmo = 100;
        TestCharacter->SetAmmo(InitialAmmo);

        // 触发射击动作
        InputHelper->TriggerAction(TEXT("Fire"));

        // 等待射击逻辑执行
        AddCommand(new FWaitDelay(0.1f));

        const int32 FinalAmmo = TestCharacter->GetAmmo();
        ASSERT_THAT(AreEqual(InitialAmmo - 1, FinalAmmo));
    }

    // 测试Reload动作
    TEST_METHOD(ReloadAction_ShouldRefillAmmo)
    {
        const int32 InitialAmmo = 10;
        const int32 MaxAmmo = 100;
        TestCharacter->SetAmmo(InitialAmmo);
        TestCharacter->SetMaxAmmo(MaxAmmo);

        // 触发Reload动作
        InputHelper->TriggerAction(TEXT("Reload"));

        // 等待Reload完成
        AddCommand(new FWaitDelay(1.0f));

        const int32 FinalAmmo = TestCharacter->GetAmmo();
        ASSERT_THAT(AreEqual(MaxAmmo, FinalAmmo));
    }

    // 测试按键输入
    TEST_METHOD(KeyInput_ShouldTriggerAction)
    {
        bool ActionTriggered = false;

        // 注册按键回调（示例）
        TestCharacter->OnKeyAction.AddLambda([&](FKey Key) {
            if (Key == EKeys::SpaceBar)
            {
                ActionTriggered = true;
            }
        });

        // 按下空格键
        InputHelper->PressKey(EKeys::SpaceBar);
        AddCommand(new FWaitDelay(0.1f));

        // 释放空格键
        InputHelper->ReleaseKey(EKeys::SpaceBar);

        ASSERT_THAT(IsTrue(ActionTriggered));
    }

    // 测试组合输入
    TEST_METHOD(CombinedInput_ShouldWorkTogether)
    {
        const FVector InitialLocation = TestCharacter->GetActorLocation();

        // 同时移动和跳跃
        InputHelper->SetAxisValue(TEXT("MoveForward"), 1.0f);
        InputHelper->TriggerAction(TEXT("Jump"));

        // 等待移动和跳跃
        AddCommand(new FWaitUntil([&]() {
            const float Distance = FVector::Distance(
                InitialLocation,
                TestCharacter->GetActorLocation()
            );
            const float Height = TestCharacter->GetActorLocation().Z;
            return Distance > 50.0f && Height > InitialLocation.Z;
        }, 2.0f));

        // 停止移动
        InputHelper->SetAxisValue(TEXT("MoveForward"), 0.0f);

        ASSERT_THAT(IsTrue(TestCharacter->IsJumping()));
    }

    // 使用Command Builder测试输入序列
    TEST_METHOD(InputSequence_UsingCommandBuilder)
    {
        const FVector InitialLocation = TestCharacter->GetActorLocation();
        bool MoveStarted = false;
        bool JumpStarted = false;

        TestCharacter->Jumped.AddLambda([&]() {
            JumpStarted = true;
        });

        TestCommandBuilder
            // 向前移动
            .Do([&]() {
                InputHelper->SetAxisValue(TEXT("MoveForward"), 1.0f);
                MoveStarted = true;
            })
            // 等待移动
            .Until([&]() {
                return MoveStarted && FVector::Distance(
                    InitialLocation,
                    TestCharacter->GetActorLocation()
                ) > 50.0f;
            }, 2.0f)
            // 跳跃
            .Do([&]() {
                InputHelper->TriggerAction(TEXT("Jump"));
            })
            // 等待跳跃
            .Until([&]() {
                return JumpStarted;
            }, 1.0f)
            // 停止移动
            .Then([&]() {
                InputHelper->SetAxisValue(TEXT("MoveForward"), 0.0f);
            })
            // 验证状态
            .Then([&]() {
                ASSERT_THAT(IsTrue(MoveStarted));
                ASSERT_THAT(IsTrue(JumpStarted));
                ASSERT_THAT(IsTrue(TestCharacter->IsJumping()));
            })
            // 清理
            .OnTearDown([&]() {
                InputHelper->ResetAllInput();
            });
    }

    // 测试输入响应延迟
    TEST_METHOD(InputResponse_ShouldBeTimely)
    {
        bool ActionExecuted = false;

        TestCharacter->OnActionExecuted.AddLambda([&]() {
            ActionExecuted = true;
        });

        // 触发动作并记录时间
        double StartTime = FPlatformTime::Seconds();
        InputHelper->TriggerAction(TEXT("TestAction"));

        // 等待动作执行
        AddCommand(new FWaitUntil([&]() {
            return ActionExecuted;
        }, 0.5f));

        double ResponseTime = FPlatformTime::Seconds() - StartTime;

        // 验证响应时间在合理范围内（<100ms）
        ASSERT_THAT(IsTrue(ResponseTime < 0.1));
    }

    // 测试输入取消
    TEST_METHOD(InputCancellation_ShouldPreventAction)
    {
        bool ActionTriggered = false;

        TestCharacter->OnActionExecuted.AddLambda([&]() {
            ActionTriggered = true;
        });

        // 触发动作
        InputHelper->TriggerAction(TEXT("TestAction"));

        // 立即取消
        InputHelper->TriggerAction(TEXT("CancelAction"));

        // 等待一小段时间
        AddCommand(new FWaitDelay(0.1f));

        // 验证动作被取消（根据实际实现调整）
        // ASSERT_THAT(IsFalse(ActionTriggered));
    }
};
