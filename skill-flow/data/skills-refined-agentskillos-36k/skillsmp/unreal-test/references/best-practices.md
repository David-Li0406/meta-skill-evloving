# 测试最佳实践

## 目录
- [概述](#概述)
- [测试命名](#测试命名)
- [测试独立性](#测试独立性)
- [断言使用](#断言使用)
- [资源管理](#资源管理)
- [性能优化](#性能优化)
- [可维护性](#可维护性)
- [常见陷阱](#常见陷阱)

## 概述
编写高质量的测试不仅需要理解CQTest框架，还需要遵循最佳实践。良好的测试习惯可以提高测试的可维护性、稳定性和可读性。

## 测试命名

### 基本原则
测试名称应该清晰描述被测试的功能和预期行为。

### 命名格式
推荐格式：`测试场景_预期行为` 或 `被测试对象_动作_预期结果`

### 命名示例

#### ✅ 好的命名
```cpp
TEST_METHOD(FireWeapon_ShouldReduceAmmo)                    // 清晰描述场景和结果
TEST_METHOD(Character_Jump_ShouldReachTargetHeight)          // 明确的动词和预期
TEST_METHOD(Inventory_AddItem_WhenFull_ShouldFail)           // 包含条件和结果
TEST_METHOD(Network_Replication_ShouldSyncToAllClients)      // 描述技术细节

TEST_CLASS(PlayerHealthTests, "Game.Character.Health")         // 复数形式表示测试类
```

#### ❌ 不好的命名
```cpp
TEST_METHOD(Test1)                                            // 无意义的名称
TEST_METHOD(HealthTest)                                        // 缺少行为描述
TEST_METHOD(DoSomething)                                       // 过于模糊
TEST_METHOD(MyTest)                                             // 不提供任何信息

TEST_CLASS(Tests, "Game")                                       // 过于宽泛的分类
```

### 测试分类命名
测试分类字符串应遵循层次结构：

```
<模块>.<子系统>.<功能>.<场景>
```

**示例：**
```cpp
// 武器系统测试
TEST(WeaponFire, "Game.Weapon.Fire")
TEST(WeaponReload, "Game.Weapon.Reload")

// 角色移动测试
TEST(CharacterWalk, "Game.Character.Movement.Walk")
TEST(CharacterRun, "Game.Character.Movement.Run")

// UI系统测试
TEST(HealthBarUpdate, "Game.UI.HUD.HealthBar")
TEST(MinimapRender, "Game.UI.Minimap")
```

### 命名约定检查清单
- [ ] 测试名称清晰描述被测试的功能
- [ ] 测试名称明确说明预期行为
- [ ] 测试名称是有效的C++标识符（TEST宏）
- [ ] 测试分类使用点号分隔层级
- [ ] 测试名称避免使用"Test"等冗余词汇
- [ ] 避免使用数字序号（Test1, Test2等）

## 测试独立性

### 基本原则
每个测试应该是独立的，不依赖于其他测试的执行顺序或状态。

### 独立性示例

#### ✅ 独立的测试
```cpp
TEST_CLASS(InventoryTests, "Game.Inventory")
{
    UInventoryComponent* Inventory = nullptr;

    BEFORE_EACH()
    {
        // 每个测试都创建新的Inventory
        Inventory = NewObject<UInventoryComponent>();
        Inventory->Initialize();
    }

    AFTER_EACH()
    {
        // 每个测试后清理
        if (Inventory)
        {
            Inventory->Cleanup();
        }
    }

    TEST_METHOD(AddItem_WithSpace_ShouldSucceed)
    {
        const int32 InitialCount = Inventory->GetItemCount();
        Inventory->AddItem(ItemData);
        ASSERT_THAT(AreEqual(InitialCount + 1, Inventory->GetItemCount()));
    }

    TEST_METHOD(RemoveItem_ExistingItem_ShouldSucceed)
    {
        Inventory->AddItem(ItemData); // 独立添加物品
        const int32 InitialCount = Inventory->GetItemCount();
        Inventory->RemoveItem(ItemData);
        ASSERT_THAT(AreEqual(InitialCount - 1, Inventory->GetItemCount()));
    }
};
```

#### ❌ 不独立的测试
```cpp
TEST_CLASS(InventoryTests, "Game.Inventory")
{
    UInventoryComponent* Inventory = nullptr;
    bool SetupCalled = false;

    BEFORE_ALL()  // ❌ 在所有测试前只执行一次
    {
        Inventory = NewObject<UInventoryComponent>();
        Inventory->Initialize();
        SetupCalled = true;
    }

    TEST_METHOD(AddItem_ShouldSucceed)
    {
        ASSERT_THAT(IsTrue(SetupCalled));
        Inventory->AddItem(ItemData);
        ASSERT_THAT(AreEqual(1, Inventory->GetItemCount()));
    }

    TEST_METHOD(RemoveItem_ShouldSucceed)
    {
        // ❌ 依赖于AddItem测试的执行结果
        ASSERT_THAT(AreEqual(1, Inventory->GetItemCount()));
        Inventory->RemoveItem(ItemData);
        ASSERT_THAT(AreEqual(0, Inventory->GetItemCount()));
    }
};
```

### 状态重置
确保每个测试开始时状态一致：

```cpp
TEST_CLASS(PlayerStateTests, "Game.Player")
{
    APlayerController* Player = nullptr;
    int32 TestNumber = 0;  // ❌ 这个变量会在测试间保留

    BEFORE_EACH()
    {
        Player = NewObject<APlayerController>();
        Player->PlayerState = NewObject<APlayerState>();
        TestNumber = 0;  // ✅ 显式重置
    }

    TEST_METHOD(Test1)
    {
        TestNumber++;
        ASSERT_THAT(AreEqual(1, TestNumber));
    }

    TEST_METHOD(Test2)
    {
        // 如果没有重置，TestNumber可能是1
        ASSERT_THAT(AreEqual(0, TestNumber));
    }
};
```

### 独立性检查清单
- [ ] 每个测试都可以独立运行
- [ ] 测试不依赖于其他测试的执行顺序
- [ ] 使用BEFORE_EACH而非BEFORE_ALL（除非确实需要）
- [ ] 所有共享状态在BEFORE_EACH中重置
- [ ] 测试不依赖于外部状态（如全局变量）
- [ ] 随机顺序执行测试也能通过

## 断言使用

### 断言选择原则
使用最符合意图的断言类型。

### 断言类型

#### 布尔断言
```cpp
// 简单的真值判断
ASSERT_THAT(IsTrue(Value > 0));
ASSERT_THAT(IsFalse(Value == 0));

// 非空判断
ASSERT_THAT(IsNotNull(Actor));
ASSERT_THAT(IsNull(DestroyedActor));
```

#### 相等性断言
```cpp
// 数值比较
ASSERT_THAT(AreEqual(ExpectedValue, ActualValue));

// 字符串比较
ASSERT_THAT(AreEqual(ExpectedString, ActualString));

// 自定义类型（需要实现operator==）
MyCustomType A{42};
MyCustomType B{42};
ASSERT_THAT(AreEqual(A, B));
```

### 断言最佳实践

#### ✅ 好的断言使用
```cpp
TEST_METHOD(HealthCalculation_ShouldBeCorrect)
{
    const float Damage = 25.0f;
    const float InitialHealth = 100.0f;
    const float ExpectedHealth = 75.0f;

    Player->TakeDamage(Damage, FDamageEvent(), nullptr, nullptr);

    // ✅ 明确的期望值和实际值比较
    ASSERT_THAT(AreEqual(ExpectedHealth, Player->GetHealth()));
}

TEST_METHOD(InventoryCapacity_ShouldBeRespected)
{
    const int32 MaxCapacity = 100;
    const int32 InitialLoad = 90;
    const int32 ItemWeight = 15;

    Inventory->SetMaxCapacity(MaxCapacity);
    Inventory->SetCurrentLoad(InitialLoad);

    // ✅ 使用布尔断言检查条件
    ASSERT_THAT(IsFalse(Inventory->CanAddItem(ItemWeight)));
}
```

#### ❌ 不好的断言使用
```cpp
TEST_METHOD(HealthCalculation)
{
    Player->TakeDamage(25.0f, FDamageEvent(), nullptr, nullptr);

    // ❌ 断言意图不明确
    ASSERT_THAT(IsTrue(Player->GetHealth() < 100.0f));

    // ❌ 使用魔法数字
    ASSERT_THAT(AreEqual(75.0f, Player->GetHealth()));

    // ❌ 过于复杂的表达式
    ASSERT_THAT(IsTrue(Player->GetHealth() > 0 && Player->GetHealth() < 100 && Player->IsAlive()));
}
```

### 断言消息
提供清晰的失败信息：

```cpp
TEST_METHOD(PlayerSpawn_ShouldSucceed)
{
    // ❌ 没有上下文信息
    ASSERT_THAT(IsNotNull(Player));

    // ✅ 使用有意义的变量名和上下文
    APlayerController* SpawnedPlayer = UGameplayStatics::SpawnPlayerController(
        GetWorld(),
        0
    );
    ASSERT_THAT(IsNotNull(SpawnedPlayer));
}
```

### 断言检查清单
- [ ] 使用最合适的断言类型
- [ ] 断言包含清晰的期望值
- [ ] 避免在断言中使用复杂的表达式
- [ ] 断言失败时能快速定位问题
- [ ] 每个测试至少有一个断言
- [ ] 断言数量适当（不是越多越好）

## 资源管理

### 基本原则
所有分配的资源都应该在测试后正确释放，即使测试失败。

### 资源管理示例

#### ✅ 正确的资源管理
```cpp
TEST_CLASS(ActorLifecycleTest, "Game.Actor")
{
    TArray<AActor*> SpawnedActors;

    BEFORE_EACH()
    {
        SpawnedActors.Empty();
    }

    AFTER_EACH()
    {
        // ✅ 确保所有Actor都被销毁
        for (AActor* Actor : SpawnedActors)
        {
            if (Actor && Actor->IsValidLowLevel())
            {
                Actor->Destroy();
            }
        }
        SpawnedActors.Empty();
    }

    TEST_METHOD(SpawnMultipleActors_ShouldCleanup)
    {
        for (int32 i = 0; i < 10; i++)
        {
            AActor* Actor = GetWorld()->SpawnActor<AActor>(FVector(i * 100, 0, 0));
            SpawnedActors.Add(Actor);
            ASSERT_THAT(IsNotNull(Actor));
        }
    }
};
```

#### 使用Latent Actions清理
```cpp
TEST_METHOD(LatentCleanup_ShouldSucceed)
{
    AActor* Actor = GetWorld()->SpawnActor<AActor>(FVector::ZeroVector);

    TestCommandBuilder
        .Do([&]() {
            // 测试逻辑
        })
        .OnTearDown([&]() {
            // ✅ 确保Actor被销毁
            if (Actor && Actor->IsValidLowLevel())
            {
                Actor->Destroy();
            }
        });
}
```

#### 使用智能指针
```cpp
TEST_METHOD(SmartPointer_ShouldAutoCleanup)
{
    // ✅ 使用TSharedPtr自动管理资源
    TSharedPtr<MyCustomObject> Object = MakeShared<MyCustomObject>();
    Object->Initialize();

    ASSERT_THAT(IsTrue(Object->IsInitialized()));
    // 超出作用域时自动释放
}
```

### 资源管理检查清单
- [ ] 所有分配的内存都有对应的释放
- [ ] 使用AFTER_EACH或OnTearDown清理资源
- [ ] 即使测试失败也会执行清理
- [ ] 考虑使用智能指针管理资源
- [ ] 避免内存泄漏（通过测试工具验证）
- [ ] 验证资源清理的正确性

## 性能优化

### 基本原则
测试应该快速执行，同时保持可靠性。

### 性能优化技巧

#### 1. 使用FWaitUntil而非FWaitDelay
```cpp
// ❌ 慢速：固定延迟
AddCommand(new FWaitDelay(2.0f));
ASSERT_THAT(IsTrue(OperationComplete));

// ✅ 快速：条件等待
AddCommand(new FWaitUntil([&]() {
    return OperationComplete;
}, 2.0f));
ASSERT_THAT(IsTrue(OperationComplete));
```

#### 2. 减少资源加载
```cpp
TEST_CLASS(ResourceLoadingTest, "Game.Resource")
{
    static UDataTable* CachedDataTable;  // ✅ 缓存资源

    BEFORE_ALL()
    {
        // 只加载一次
        CachedDataTable = LoadObj<UDataTable>(TEXT("/Game/Data/TestData"));
    }

    TEST_METHOD(DataLookup_ShouldSucceed)
    {
        // ✅ 使用缓存的数据
        FTestRow* Row = CachedDataTable->FindRow<FTestRow>(TEXT("Row1"), TEXT(""));
        ASSERT_THAT(IsNotNull(Row));
    }
};
```

#### 3. 避免不必要的Actor生成
```cpp
TEST_METHOD(ActorTest_ShouldReuseActor)
{
    // ❌ 每次测试都生成新Actor
    AActor* Actor1 = GetWorld()->SpawnActor<AActor>(FVector::ZeroVector);
    ASSERT_THAT(IsNotNull(Actor1));
    Actor1->Destroy();

    AActor* Actor2 = GetWorld()->SpawnActor<AActor>(FVector::ZeroVector);
    ASSERT_THAT(IsNotNull(Actor2));
    Actor2->Destroy();

    // ✅ 重用Actor
    AActor* Actor = GetWorld()->SpawnActor<AActor>(FVector::ZeroVector);
    ASSERT_THAT(IsNotNull(Actor));

    // 执行多个测试...
    ASSERT_THAT(IsTrue(Actor->IsValidLowLevel()));
    ASSERT_THAT(AreEqual(FVector::ZeroVector, Actor->GetActorLocation()));

    Actor->Destroy();
}
```

#### 4. 限制测试范围
```cpp
TEST_METHOD(NetworkTest_ShouldUseMinimalClients)
{
    // ❌ 测试所有客户端
    NetworkComponent.Initialize(1, 10);  // 10个客户端，慢

    // ✅ 只测试必要数量
    NetworkComponent.Initialize(1, 2);   // 2个客户端，快
}
```

### 性能检查清单
- [ ] 测试执行时间在合理范围内（通常<5秒）
- [ ] 避免不必要的固定延迟
- [ ] 复用资源而非重复加载
- [ ] 限制测试规模（客户端数量、Actor数量等）
- [ ] 使用轻量级测试资产
- [ ] 考虑将慢速测试移到单独的测试套件

## 可维护性

### 基本原则
测试应该易于理解、修改和扩展。

### 可维护性技巧

#### 1. 使用辅助方法
```cpp
TEST_CLASS(PlayerMovementTest, "Game.Character")
{
    ACharacter* Player = nullptr;

    BEFORE_EACH()
    {
        Player = NewObject<ACharacter>();
    }

    // ✅ 提取公共逻辑
    bool MovePlayerTo(const FVector& Location)
    {
        Player->SetActorLocation(Location);
        return Player->GetActorLocation().Equals(Location, 0.1f);
    }

    TEST_METHOD(MoveForward_ShouldSucceed)
    {
        ASSERT_THAT(IsTrue(MovePlayerTo(FVector(100, 0, 0))));
    }

    TEST_METHOD(MoveRight_ShouldSucceed)
    {
        ASSERT_THAT(IsTrue(MovePlayerTo(FVector(0, 100, 0))));
    }
};
```

#### 2. 使用清晰的变量名
```cpp
TEST_METHOD(WeaponSystem_ShouldCalculateCorrectly)
{
    // ❌ 不清晰的变量名
    float a = 100.0f;
    float b = 25.0f;
    float c = a - b;

    // ✅ 清晰的变量名
    const float InitialAmmo = 100.0f;
    const float AmmoConsumed = 25.0f;
    const float RemainingAmmo = InitialAmmo - AmmoConsumed;

    ASSERT_THAT(AreEqual(RemainingAmmo, Weapon->GetAmmo()));
}
```

#### 3. 组织相关测试
```cpp
// ✅ 按功能组织
TEST_CLASS(WeaponFireTests, "Game.Weapon.Fire") { /* ... */ };
TEST_CLASS(WeaponReloadTests, "Game.Weapon.Reload") { /* ... */ };
TEST_CLASS(WeaponUpgradeTests, "Game.Weapon.Upgrade") { /* ... */ };

// ✅ 按测试类型组织
TEST_CLASS(UnitTests, "Game.Math")
{
    TEST_METHOD(Addition_ShouldBeCorrect) { /* ... */ }
    TEST_METHOD(Multiplication_ShouldBeCorrect) { /* ... */ }
};

TEST_CLASS(IntegrationTests, "Game.Character")
{
    TEST_METHOD(CombatFlow_ShouldWork) { /* ... */ }
    TEST_METHOD(LevelUp_ShouldAwardXP) { /* ... */ }
};
```

#### 4. 添加注释说明复杂逻辑
```cpp
TEST_METHOD(ComplexLogic_ShouldBeCorrect)
{
    // 测试装备系统：
    // 1. 玩家装备武器
    // 2. 验证武器属性应用到角色
    // 3. 验证旧武器被卸载
    // 4. 验证背包空间更新

    const int32 ExpectedDamage = 100;
    const int32 ExpectedInventorySpace = 5;

    Player->EquipWeapon(Weapon);

    ASSERT_THAT(AreEqual(ExpectedDamage, Player->GetTotalDamage()));
    ASSERT_THAT(IsNull(Player->GetPreviousWeapon()));
    ASSERT_THAT(AreEqual(ExpectedInventorySpace, Inventory->GetAvailableSpace()));
}
```

### 可维护性检查清单
- [ ] 测试代码清晰易懂
- [ ] 使用有意义的变量和函数名
- [ ] 提取公共逻辑到辅助方法
- [ ] 添加必要的注释
- [ ] 相关测试组织在一起
- [ ] 避免重复代码

## 常见陷阱

### 陷阱1：依赖测试执行顺序
```cpp
// ❌ 错误：Test2依赖于Test1
TEST_METHOD(Test1) { Value = 42; }
TEST_METHOD(Test2) { ASSERT_THAT(AreEqual(42, Value)); }

// ✅ 正确：每个测试独立
TEST_METHOD(Test1)
{
    const int32 TestValue = 42;
    ASSERT_THAT(AreEqual(42, TestValue));
}
```

### 陷阱2：忘记清理资源
```cpp
// ❌ 错误：Actor没有被销毁
TEST_METHOD(ActorTest)
{
    AActor* Actor = GetWorld()->SpawnActor<AActor>(FVector::ZeroVector);
    // 忘记销毁Actor
}

// ✅ 正确：确保清理
TEST_METHOD(ActorTest)
{
    AActor* Actor = GetWorld()->SpawnActor<AActor>(FVector::ZeroVector);
    // 测试逻辑...

    Actor->Destroy();
}
```

### 陷阱3：使用固定延迟
```cpp
// ❌ 错误：使用FWaitDelay
AddCommand(new FWaitDelay(2.0f));
ASSERT_THAT(IsTrue(OperationComplete));

// ✅ 正确：使用FWaitUntil
AddCommand(new FWaitUntil([&]() {
    return OperationComplete;
}, 2.0f));
```

### 陷阱4：过度使用BEFORE_ALL
```cpp
// ❌ 错误：过度使用BEFORE_ALL导致状态污染
BEFORE_ALL()
{
    Player = NewObject<ACharacter>();
    Player->SetHealth(50);  // 测试间保留状态
}

// ✅ 正确：使用BEFORE_EACH
BEFORE_EACH()
{
    Player = NewObject<ACharacter>();
    Player->SetHealth(100);  // 每个测试都是初始状态
}
```

### 陷阱5：忽略测试失败
```cpp
// ❌ 错误：忽略可能的失败
bool Result = Player->TryPerformAction();
// 没有验证Result

// ✅ 正确：验证结果
bool Result = Player->TryPerformAction();
ASSERT_THAT(IsTrue(Result));
```

### 陷阱检查清单
- [ ] 测试不依赖于执行顺序
- [ ] 所有资源都被正确清理
- [ ] 避免使用固定延迟
- [ ] 正确使用BEFORE_EACH而非BEFORE_ALL
- [ ] 验证所有可能失败的操作
- [ ] 避免在测试中使用随机数

## 总结

编写高质量测试的关键点：
1. **清晰的命名**：让测试意图一目了然
2. **独立性**：每个测试都可以独立运行
3. **适当的断言**：使用最合适的断言类型
4. **资源管理**：确保资源正确释放
5. **性能优化**：快速且可靠的测试
6. **可维护性**：易于理解和修改的代码
7. **避免陷阱**：了解常见错误并避免

遵循这些最佳实践，可以编写出可靠、快速且易于维护的测试代码。