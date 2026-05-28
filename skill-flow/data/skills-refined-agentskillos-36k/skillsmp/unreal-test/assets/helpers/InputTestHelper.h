#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Pawn.h"
#include "InputActionValue.h"
#include "EnhancedInputComponent.h"
#include "Input/Keys.h"

// 前向声明
class APawn;
class UEnhancedInputComponent;
struct FInputActionValue;

/**
 * InputTestHelper
 * 辅助类，用于简化和模拟输入操作
 */
class InputTestHelper
{
public:
    /**
     * 构造函数
     * @param InPawn 目标Pawn
     */
    InputTestHelper(APawn* InPawn);
    ~InputTestHelper();

    /**
     * 初始化输入系统
     * @return 是否成功
     */
    bool Initialize();

    /**
     * 清理输入系统
     */
    void Cleanup();

    /**
     * 触发输入动作
     * @param ActionName 动作名称
     * @param Value 输入值
     */
    void TriggerAction(const FName& ActionName, const FInputActionValue& Value = FInputActionValue(1.0f));

    /**
     * 触发输入动作（带布尔值）
     * @param ActionName 动作名称
     * @param Value 布尔值
     */
    void TriggerAction(const FName& ActionName, bool Value);

    /**
     * 触发输入动作（带轴值）
     * @param ActionName 动作名称
     * @param AxisValue 轴值
     */
    void TriggerAction(const FName& ActionName, float AxisValue);

    /**
     * 模拟按键按下
     * @param Key 要按下的键
     */
    void PressKey(FKey Key);

    /**
     * 模拟按键释放
     * @param Key 要释放的键
     */
    void ReleaseKey(FKey Key);

    /**
     * 模拟按键点击
     * @param Key 要点击的键
     */
    void PressAndReleaseKey(FKey Key);

    /**
     * 设置轴输入值
     * @param AxisName 轴名称
     * @param Value 轴值
     */
    void SetAxisValue(const FName& AxisName, float Value);

    /**
     * 获取当前轴值
     * @param AxisName 轴名称
     * @return 当前轴值
     */
    float GetAxisValue(const FName& AxisName) const;

    /**
     * 模拟鼠标移动
     * @param DeltaX X轴移动量
     * @param DeltaY Y轴移动量
     */
    void SimulateMouseMovement(float DeltaX, float DeltaY);

    /**
     * 模拟鼠标滚轮
     * @param DeltaValue 滚轮增量
     */
    void SimulateMouseWheel(float DeltaValue);

    /**
     * 模拟鼠标点击
     * @param MouseButton 鼠标按键
     */
    void SimulateMouseClick(FKey MouseButton);

    /**
     * 重置所有输入
     */
    void ResetAllInput();

    /**
     * 重置特定动作
     * @param ActionName 动作名称
     */
    void ResetAction(const FName& ActionName);

    /**
     * 重置特定轴
     * @param AxisName 轴名称
     */
    void ResetAxis(const FName& AxisName);

    /**
     * 获取输入组件
     * @return 输入组件指针
     */
    UEnhancedInputComponent* GetInputComponent() const;

    /**
     * 获取目标Pawn
     * @return 目标Pawn指针
     */
    APawn* GetTargetPawn() const;

    /**
     * 检查是否已初始化
     * @return 是否已初始化
     */
    bool IsInitialized() const;

private:
    APawn* TargetPawn;
    UEnhancedInputComponent* InputComponent;
    bool bInitialized;

    /**
     * 内部初始化
     */
    void InternalInitialize();

    /**
     * 内部清理
     */
    void InternalCleanup();

    /**
     * 验证输入组件
     * @return 输入组件是否有效
     */
    bool ValidateInputComponent() const;
};
