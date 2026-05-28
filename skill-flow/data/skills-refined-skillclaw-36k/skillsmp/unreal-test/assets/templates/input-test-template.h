// Input测试头文件模板

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "InputAction.h"
#include "EnhancedInputComponent.h"

// 引入Helper类
#include "Helpers/InputTestHelper.h"

/**
 * InputTestHelper
 * 辅助类，用于简化和模拟输入操作
 */
class InputTestHelper
{
public:
    InputTestHelper(APawn* InPawn);
    ~InputTestHelper();

    // 初始化输入系统
    bool Initialize();

    // 清理输入系统
    void Cleanup();

    // 触发输入动作
    void TriggerAction(const FName& ActionName, const FInputActionValue& Value = FInputActionValue(1.0f));

    // 模拟按键按下
    void PressKey(FKey Key);

    // 模拟按键释放
    void ReleaseKey(FKey Key);

    // 设置轴输入值
    void SetAxisValue(const FName& AxisName, float Value);

    // 重置所有输入
    void ResetAllInput();

private:
    APawn* TargetPawn;
    UEnhancedInputComponent* InputComponent;
    bool bInitialized;
};
