// Animation测试头文件模板

#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "Animation/AnimMontage.h"

// 引入Helper类
#include "Helpers/AnimationTestHelper.h"

/**
 * AnimationTestHelper
 * 辅助类，用于简化动画测试操作
 */
class AnimationTestHelper
{
public:
    AnimationTestHelper(UAnimInstance* InAnimInstance);
    ~AnimationTestHelper();

    // 播放蒙太奇
    bool PlayMontage(UAnimMontage* Montage);

    // 停止当前蒙太奇
    void StopMontage();

    // 检查蒙太奇是否正在播放
    bool IsMontagePlaying() const;

    // 检查特定蒙太奇是否正在播放
    bool IsMontagePlaying(UAnimMontage* Montage) const;

    // 等待蒙太奇完成（返回是否成功）
    bool WaitForMontageComplete(float Timeout = 5.0f);

    // 获取当前动画状态
    FName GetCurrentState() const;

    // 设置动画状态
    void SetAnimationState(FName StateName);

    // 事件回调
    FOnMontageBlendingOutStarted OnMontageBlendingOutStarted;
    FOnMontageEnded OnMontageEnded;

private:
    UAnimInstance* AnimInstance;
    UAnimMontage* CurrentMontage;
};
