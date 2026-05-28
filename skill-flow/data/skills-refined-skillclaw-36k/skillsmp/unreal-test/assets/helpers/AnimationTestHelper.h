#pragma once

#include "CoreMinimal.h"
#include "Animation/AnimInstance.h"
#include "Animation/AnimMontage.h"
#include "Delegates/DelegateCombinations.h"

// 前向声明
class UAnimInstance;

/**
 * AnimationTestHelper
 * 辅助类，用于简化和测试动画系统操作
 */
class AnimationTestHelper
{
public:
    /**
     * 构造函数
     * @param InAnimInstance 目标动画实例
     */
    AnimationTestHelper(UAnimInstance* InAnimInstance);
    ~AnimationTestHelper();

    /**
     * 播放蒙太奇
     * @param Montage 要播放的蒙太奇
     * @param PlayRate 播放速率
     * @return 是否成功开始播放
     */
    bool PlayMontage(UAnimMontage* Montage, float PlayRate = 1.0f);

    /**
     * 停止当前蒙太奇
     */
    void StopMontage();

    /**
     * 停止指定的蒙太奇
     * @param Montage 要停止的蒙太奇
     */
    void StopMontage(UAnimMontage* Montage);

    /**
     * 暂停当前蒙太奇
     */
    void PauseMontage();

    /**
     * 恢复当前蒙太奇
     */
    void ResumeMontage();

    /**
     * 检查是否有蒙太奇正在播放
     * @return 是否正在播放
     */
    bool IsMontagePlaying() const;

    /**
     * 检查指定的蒙太奇是否正在播放
     * @param Montage 要检查的蒙太奇
     * @return 是否正在播放
     */
    bool IsMontagePlaying(UAnimMontage* Montage) const;

    /**
     * 获取当前播放的蒙太奇
     * @return 当前蒙太奇指针
     */
    UAnimMontage* GetCurrentMontage() const;

    /**
     * 获取当前蒙太奇的播放位置
     * @return 播放位置（秒）
     */
    float GetCurrentMontagePosition() const;

    /**
     * 设置当前蒙太奇的播放位置
     * @param Position 目标位置（秒）
     */
    void SetCurrentMontagePosition(float Position);

    /**
     * 设置当前蒙太奇的播放速率
     * @param PlayRate 播放速率
     */
    void SetCurrentMontagePlayRate(float PlayRate);

    /**
     * 等待蒙太奇完成
     * @param Timeout 超时时间（秒）
     * @return 是否成功完成
     */
    bool WaitForMontageComplete(float Timeout = 5.0f);

    /**
     * 等待蒙太奇播放到指定位置
     * @param TargetPosition 目标位置（秒）
     * @param Timeout 超时时间（秒）
     * @return 是否到达目标位置
     */
    bool WaitForMontagePosition(float TargetPosition, float Timeout = 5.0f);

    /**
     * 获取当前动画状态
     * @return 状态名称
     */
    FName GetCurrentState() const;

    /**
     * 设置动画状态
     * @param StateName 状态名称
     * @return 是否成功
     */
    bool SetAnimationState(FName StateName);

    /**
     * 获取当前动画播放速度
     * @return 播放速度
     */
    float GetPlaybackSpeed() const;

    /**
     * 设置动画播放速度
     * @param Speed 播放速度
     */
    void SetPlaybackSpeed(float Speed);

    // 委托
    /** 蒙太奇开始混合时触发 */
    FOnMontageBlendingOutStarted OnMontageBlendingOutStarted;

    /** 蒙太奇结束时触发 */
    FOnMontageEnded OnMontageEnded;

    /** 动画通知触发 */
    FOnMontageNotifyBegin OnNotifyBegin;
    FOnMontageNotifyEnd OnNotifyEnd;

private:
    UAnimInstance* AnimInstance;
    UAnimMontage* CurrentMontage;
    bool bInitialized;

    /**
     * 内部初始化
     */
    void InternalInitialize();

    /**
     * 内部清理
     */
    void InternalCleanup();
};
