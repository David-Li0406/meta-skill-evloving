// Actor测试头文件模板

#pragma once

#include "CoreMinimal.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"

// 引入Helper类
#include "Helpers/ActorTestHelper.h"

/**
 * YourTestActorTest
 * 测试类，用于验证YourActor的功能
 */
class YourTestActorTest
{
public:
    YourTestActorTest();
    ~YourTestActorTest();

    // 初始化测试环境
    bool Initialize();

    // 清理测试环境
    void Cleanup();

    // 生成测试Actor
    template<typename T>
    T* SpawnTestActor(const FVector& Location = FVector::ZeroVector);

    // 销毁所有测试Actor
    void DestroyAllTestActors();

private:
    // 测试世界
    UWorld* TestWorld;

    // 生成的Actor列表
    TArray<AActor*> SpawnedActors;

    // 是否已初始化
    bool bInitialized;
};
