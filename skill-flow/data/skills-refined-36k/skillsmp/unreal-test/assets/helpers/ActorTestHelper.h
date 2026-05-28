#pragma once

#include "CoreMinimal.h"
#include "Engine/World.h"
#include "GameFramework/Actor.h"

/**
 * ActorTestHelper
 * 辅助类，用于简化Actor测试操作
 */
class ActorTestHelper
{
public:
    /**
     * 在指定世界生成Actor
     * @tparam T Actor类型
     * @param World 目标世界
     * @param Location 生成位置
     * @param Rotation 生成旋转
     * @return 生成的Actor指针
     */
    template<typename T>
    static T* SpawnActor(UWorld* World, const FVector& Location = FVector::ZeroVector, const FRotator& Rotation = FRotator::ZeroRotator);

    /**
     * 初始化Actor
     * @param Actor 要初始化的Actor
     * @return 是否成功
     */
    static bool InitializeActor(AActor* Actor);

    /**
     * 设置Actor属性
     * @param Actor 目标Actor
     * @param PropertyName 属性名
     * @param Value 属性值
     * @return 是否成功
     */
    static bool SetActorProperty(AActor* Actor, const FName& PropertyName, const FVariant& Value);

    /**
     * 获取Actor属性
     * @param Actor 目标Actor
     * @param PropertyName 属性名
     * @return 属性值
     */
    static FVariant GetActorProperty(AActor* Actor, const FName& PropertyName);

    /**
     * 验证Actor是否有效
     * @param Actor 要验证的Actor
     * @return 是否有效
     */
    static bool IsActorValid(AActor* Actor);

    /**
     * 销毁Actor
     * @param Actor 要销毁的Actor
     * @return 是否成功
     */
    static bool DestroyActor(AActor* Actor);

    /**
     * 批量销毁Actor
     * @param Actors 要销毁的Actor数组
     * @return 成功销毁的数量
     */
    static int32 DestroyActors(TArray<AActor*>& Actors);
};

/**
 * ActorTestSpawner
 * 管理测试世界和Actor生成/销毁
 */
class ActorTestSpawner
{
public:
    ActorTestSpawner();
    ~ActorTestSpawner();

    /**
     * 初始化测试世界
     * @return 是否成功
     */
    bool InitializeWorld();

    /**
     * 销毁测试世界
     */
    void DestroyWorld();

    /**
     * 在测试世界中生成Actor
     * @tparam T Actor类型
     * @param Location 生成位置
     * @param Rotation 生成旋转
     * @return 生成的Actor指针
     */
    template<typename T>
    T* SpawnActor(const FVector& Location = FVector::ZeroVector, const FRotator& Rotation = FRotator::ZeroRotator);

    /**
     * 销毁所有生成的Actor
     */
    void DestroyAllSpawnedActors();

    /**
     * 获取测试世界
     * @return 测试世界指针
     */
    UWorld* GetTestWorld() const;

    /**
     * 获取生成的Actor数量
     * @return Actor数量
     */
    int32 GetSpawnedActorCount() const;

private:
    UWorld* TestWorld;
    TArray<AActor*> SpawnedActors;
    bool bWorldInitialized;
};

// 模板实现
template<typename T>
T* ActorTestHelper::SpawnActor(UWorld* World, const FVector& Location, const FRotator& Rotation)
{
    if (!World)
    {
        return nullptr;
    }

    return World->SpawnActor<T>(Location, Rotation);
}

template<typename T>
T* ActorTestSpawner::SpawnActor(const FVector& Location, const FRotator& Rotation)
{
    if (!TestWorld || !bWorldInitialized)
    {
        return nullptr;
    }

    T* Actor = ActorTestHelper::SpawnActor<T>(TestWorld, Location, Rotation);
    if (Actor)
    {
        SpawnedActors.Add(Actor);
    }

    return Actor;
}
