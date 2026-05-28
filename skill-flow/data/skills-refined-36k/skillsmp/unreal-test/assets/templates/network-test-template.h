// Network测试头文件模板

#pragma once

#include "CoreMinimal.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"

/**
 * NetworkTestHelper
 * 辅助类，用于简化和管理网络测试环境
 */
class NetworkTestHelper
{
public:
    NetworkTestHelper();
    ~NetworkTestHelper();

    // 初始化网络环境（服务器+客户端）
    bool Initialize(int32 NumClients = 1);

    // 清理网络环境
    void Shutdown();

    // 获取服务器世界
    UWorld* GetServerWorld() const;

    // 获取客户端世界
    UWorld* GetClientWorld(int32 ClientIndex) const;

    // 在服务器上生成Actor
    template<typename T>
    T* SpawnServerActor(const FVector& Location = FVector::ZeroVector);

    // 获取服务器上的Actor
    template<typename T>
    T* GetServerActor();

    // 获取客户端上的Actor
    template<typename T>
    T* GetClientActor(int32 ClientIndex);

private:
    // 网络组件
    PIENetworkComponent* NetworkComponent;

    // 是否已初始化
    bool bInitialized;
};
