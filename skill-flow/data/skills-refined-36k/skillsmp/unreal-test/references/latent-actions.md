# Latent Actions

## 目录
- [概述](#概述)
- [FExecute](#fexecute)
- [FWaitUntil](#fwaituntil)
- [FWaitDelay](#fwaitdelay)
- [FRunSequence](#frunsequence)
- [TestCommandBuilder](#testcommandbuilder)

## 概述
CQTest支持Latent Actions（异步操作），允许测试跨越多个帧执行。每个Latent Action完成后才会执行下一个。如果在Latent Action中触发断言失败，不会执行后续的Latent Actions，但仍会调用AFTER_EACH方法。

## FExecute

### 功能
执行一次性的操作，是最基础的Latent Action。

### 使用场景
- 初始化操作
- 触发事件
- 设置测试状态
- 执行清理逻辑

### 示例
```cpp
TEST_CLASS(LatentActionTest, "Game.Latent")
{
    int32 CallCount = 0;

    TEST_METHOD(BasicExecute_ShouldRunOnce)
    {
        CallCount = 0;

        // 添加一次性执行命令
        AddCommand(new FExecute([&]() {
            CallCount++;
        }));

        ASSERT_THAT(AreEqual(1, CallCount));
    }

    TEST_METHOD(MultipleExecute_ShouldRunInOrder)
    {
        TArray<int32> ExecutionOrder;

        AddCommand(new FExecute([&]() {
            ExecutionOrder.Add(1);
        }));

        AddCommand(new FExecute([&]() {
            ExecutionOrder.Add(2);
        }));

        AddCommand(new FExecute([&]() {
            ExecutionOrder.Add(3);
        }));

        ASSERT_THAT(AreEqual(1, ExecutionOrder[0]));
        ASSERT_THAT(AreEqual(2, ExecutionOrder[1]));
        ASSERT_THAT(AreEqual(3, ExecutionOrder[2]));
    }

    TEST_METHOD(ExecuteWithAssertion_ShouldFailOnError)
    {
        AddCommand(new FExecute([&]() {
            ASSERT_THAT(IsTrue(false)); // 这个断言会失败
        }));

        AddCommand(new FExecute([&]() {
            CallCount++; // 这行不会执行
        }));

        // CallCount应该仍然是0，因为第二个FExecute没有执行
        ASSERT_THAT(AreEqual(0, CallCount));
    }
};
```

### 在Setup/Teardown中使用
```cpp
TEST_CLASS(ExecuteInSetupTeardown, "Game.Latent")
{
    int32 SetupCount = 0;
    int32 TeardownCount = 0;

    BEFORE_EACH()
    {
        SetupCount = 0;
        TeardownCount = 0;

        // Setup中的Latent Action
        AddCommand(new FExecute([&]() {
            SetupCount++;
        }));
    }

    AFTER_EACH()
    {
        // Teardown中的Latent Action（测试完成后执行）
        AddCommand(new FExecute([&]() {
            TeardownCount++;
        }));

        // 注意：AFTER_EACH中的Latent Action在测试之后执行
        ASSERT_THAT(AreEqual(2, TeardownCount)); // Setup的1 + 测试的1
    }

    TEST_METHOD(TestExecution)
    {
        ASSERT_THAT(AreEqual(1, SetupCount)); // Setup已执行

        AddCommand(new FExecute([&]() {
            TeardownCount++; // 这个会在AFTER_EACH之前执行
        }));
    }
};
```

## FWaitUntil

### 功能
跨越多个帧持续执行，直到条件满足或超过超时时间。如果超时仍未满足条件，测试失败。

### 使用场景
- 等待Actor生成或销毁
- 等待动画播放完成
- 等待网络复制同步
- 等待状态机转换
- 等待异步操作完成

### 基本用法
```cpp
TEST_CLASS(WaitUntilTest, "Game.Latent")
{
    bool OperationComplete = false;

    TEST_METHOD(WaitUntil_ConditionMet_ShouldPass)
    {
        OperationComplete = false;

        // 启动异步操作
        AsyncTask(ENamedThreads::GameThread, [&]() {
            // 模拟异步工作（1秒后完成）
            FPlatformProcess::Sleep(1.0f);
            OperationComplete = true;
        });

        // 等待条件满足，超时5秒
        AddCommand(new FWaitUntil([&]() {
            return OperationComplete;
        }, 5.0f));

        ASSERT_THAT(IsTrue(OperationComplete));
    }

    TEST_METHOD(WaitUntil_Timeout_ShouldFail)
    {
        OperationComplete = false;

        // 不设置OperationComplete为true

        // 等待超时（0.5秒）
        AddCommand(new FWaitUntil([&]() {
            return OperationComplete;
        }, 0.5f));

        // 这行不会执行，因为上面的WaitUntil会超时失败
        ASSERT_THAT(IsTrue(false));
    }
};
```

### 实际应用示例

#### 等待Actor生成
```cpp
TEST_METHOD(SpawnActor_WaitUntilReady_ShouldSucceed)
{
    AMyActor* SpawnedActor = nullptr;

    // 异步生成Actor
    AsyncTask(ENamedThreads::GameThread, [&]() {
        SpawnedActor = GetWorld()->SpawnActor<AMyActor>(FVector::ZeroVector);
    });

    // 等待Actor生成
    AddCommand(new FWaitUntil([&]() {
        return SpawnedActor != nullptr && SpawnedActor->IsValidLowLevel();
    }, 2.0f));

    ASSERT_THAT(IsNotNull(SpawnedActor));
}
```

#### 等待动画完成
```cpp
TEST_METHOD(Animation_Complete_ShouldWaitUntilFinished)
{
    UAnimMontage* Montage = LoadObj<UAnimMontage>(TEXT("/Game/Animations/Attack"));

    // 播放动画
    AnimInstance->Montage_Play(Montage);

    // 等待动画播放完成
    AddCommand(new FWaitUntil([&]() {
        return AnimInstance->Montage_GetIsStopped(Montage);
    }, 5.0f));

    // 验证动画已完成
    ASSERT_THAT(IsTrue(AnimInstance->Montage_GetIsStopped(Montage)));
}
```

#### 等待网络复制
```cpp
TEST_METHOD(Network_Replication_ShouldSync)
{
    ServerActor->SetReplicatedValue(42);

    // 等待值复制到客户端
    AddCommand(new FWaitUntil([&]() {
        return ClientActor->GetReplicatedValue() == 42;
    }, 3.0f));

    ASSERT_THAT(AreEqual(42, ClientActor->GetReplicatedValue()));
}
```

### 注意事项
- 优先使用 `FWaitUntil` 而非 `FWaitDelay`，提高测试稳定性
- 设置合理的超时时间，避免测试过慢或误判
- Lambda应该快速返回，避免阻塞
- 条件应该在某一帧变为true并保持

## FWaitDelay

### 功能
等待指定的持续时间后继续执行。

### 使用场景
- **不推荐使用**：固定延迟会引入测试不稳定性
- 仅在确实需要等待固定时间时使用
- 用于测试基于时间的逻辑

### 示例
```cpp
TEST_METHOD(WaitDelay_Basic_ShouldPass)
{
    float StartTime = GetWorld()->GetTimeSeconds();

    // 等待1秒
    AddCommand(new FWaitDelay(1.0f));

    float CurrentTime = GetWorld()->GetTimeSeconds();
    ASSERT_THAT(IsTrue(CurrentTime - StartTime >= 1.0f));
}
```

### 警告
⚠️ **FWaitDelay不稳定性**：
- 固定延迟可能因性能波动导致测试不可靠
- 在慢速机器上测试可能超时失败
- 在快速机器上测试可能等待时间过长

### 推荐替代方案
使用 `FWaitUntil` 替代大多数固定延迟：

```cpp
// ❌ 不推荐：使用固定延迟
AddCommand(new FWaitDelay(2.0f));
ASSERT_THAT(IsTrue(OperationComplete));

// ✅ 推荐：等待条件满足
AddCommand(new FWaitUntil([&]() {
    return OperationComplete;
}, 2.0f));
ASSERT_THAT(IsTrue(OperationComplete));
```

## FRunSequence

### 功能
确保一组Latent Actions按顺序执行，且仅在所有之前的操作完成后才执行下一个。

### 使用场景
- 需要严格按顺序执行多个异步操作
- 确保操作之间的依赖关系
- 需要在多个步骤中共享状态

### 示例
```cpp
TEST_CLASS(RunSequenceTest, "Game.Latent")
{
    TArray<int32> ExecutionOrder;
    bool Step1Complete = false;
    bool Step2Complete = false;
    bool Step3Complete = false;

    TEST_METHOD(Sequence_ShouldExecuteInOrder)
    {
        // 创建序列
        AddCommand(new FRunSequence({
            new FExecute([&]() {
                ExecutionOrder.Add(1);
                Step1Complete = true;
            }),
            new FWaitUntil([&]() {
                return Step1Complete;
            }),
            new FExecute([&]() {
                ExecutionOrder.Add(2);
                Step2Complete = true;
            }),
            new FWaitUntil([&]() {
                return Step2Complete;
            }),
            new FExecute([&]() {
                ExecutionOrder.Add(3);
                Step3Complete = true;
            })
        }));

        // 验证执行顺序
        ASSERT_THAT(AreEqual(3, ExecutionOrder.Num()));
        ASSERT_THAT(AreEqual(1, ExecutionOrder[0]));
        ASSERT_THAT(AreEqual(2, ExecutionOrder[1]));
        ASSERT_THAT(AreEqual(3, ExecutionOrder[2]));
    }

    TEST_METHOD(Sequence_WithOperations_ShouldCompleteAll)
    {
        AActor* Actor = nullptr;
        bool Initialized = false;
        bool Positioned = false;
        bool Activated = false;

        AddCommand(new FRunSequence({
            new FExecute([&]() {
                Actor = GetWorld()->SpawnActor<AActor>(FVector::ZeroVector);
            }),
            new FWaitUntil([&]() {
                return Actor != nullptr && Actor->IsValidLowLevel();
            }),
            new FExecute([&]() {
                Actor->SetActorLocation(FVector(100, 0, 0));
                Initialized = true;
            }),
            new FWaitUntil([&]() {
                return Actor->GetActorLocation().X > 50;
            }),
            new FExecute([&]() {
                Actor->Activate();
                Activated = true;
            })
        }));

        ASSERT_THAT(IsTrue(Initialized));
        ASSERT_THAT(IsTrue(Activated));
    }
};
```

### 注意事项
- 序列中的任何步骤失败都会停止序列执行
- 使用序列可以提高代码可读性，但并非必需
- 简单场景可以直接链式AddCommand

## TestCommandBuilder

### 功能
提供流畅的命令构建器API，用于链式创建和配置Latent Actions。

### 可用命令

| 命令                  | 功能                         |
| --------------------- | ---------------------------- |
| `Do(lambda)`          | 添加FExecute命令             |
| `Then(lambda)`        | 添加FExecute命令（语义化）   |
| `Until(lambda)`       | 添加FWaitUntil命令           |
| `WaitDelay(seconds)`  | 添加FWaitDelay命令（不推荐） |
| `OnTearDown(lambda)`  | 在测试结束时执行的清理命令   |
| `CleanUpWith(lambda)` | 与OnTearDown相同             |

### 基本用法

#### 简单链式调用
```cpp
TEST_METHOD(CommandBuilder_BasicChain_ShouldExecute)
{
    int32 Step1Called = false;
    int32 Step2Called = false;
    int32 Step3Called = false;

    TestCommandBuilder
        .Do([&]() {
            Step1Called = true;
        })
        .Then([&]() {
            ASSERT_THAT(IsTrue(Step1Called)); // Step1已执行
            Step2Called = true;
        })
        .Until([&]() {
            ASSERT_THAT(IsTrue(Step2Called)); // Step2已执行
            Step3Called = true;
            return true;
        });

    ASSERT_THAT(IsTrue(Step1Called));
    ASSERT_THAT(IsTrue(Step2Called));
    ASSERT_THAT(IsTrue(Step3Called));
}
```

#### 使用Until等待条件
```cpp
TEST_METHOD(CommandBuilder_WaitUntil_ShouldPass)
{
    AMyActor* Actor = nullptr;
    bool ActorReady = false;

    TestCommandBuilder
        .Do([&]() {
            Actor = GetWorld()->SpawnActor<AMyActor>(FVector::ZeroVector);
        })
        .Until([&]() {
            if (Actor && Actor->IsValidLowLevel())
            {
                ActorReady = true;
                return true;
            }
            return false;
        }, 2.0f); // 2秒超时

    ASSERT_THAT(IsTrue(ActorReady));
}
```

#### 复杂工作流
```cpp
TEST_METHOD(CommandBuilder_ComplexWorkflow_ShouldSucceed)
{
    ACharacter* Player = nullptr;
    UAnimMontage* Montage = nullptr;
    bool AnimationStarted = false;
    bool AnimationCompleted = false;

    TestCommandBuilder
        // 1. 生成角色
        .Do([&]() {
            Player = GetWorld()->SpawnActor<ACharacter>(FVector::ZeroVector);
        })
        // 2. 等待角色就绪
        .Until([&]() {
            return Player != nullptr && Player->IsValidLowLevel();
        }, 2.0f)
        // 3. 播放动画
        .Do([&]() {
            Montage = LoadObj<UAnimMontage>(TEXT("/Game/Animations/Attack"));
            Player->PlayAnimMontage(Montage);
            AnimationStarted = true;
        })
        // 4. 等待动画开始
        .Until([&]() {
            return AnimationStarted && Player->GetMesh()->GetAnimInstance()->IsAnyMontagePlaying();
        }, 1.0f)
        // 5. 等待动画完成
        .Until([&]() {
            AnimationCompleted = !Player->GetMesh()->GetAnimInstance()->IsAnyMontagePlaying();
            return AnimationCompleted;
        }, 5.0f)
        // 6. 验证状态
        .Then([&]() {
            ASSERT_THAT(IsTrue(AnimationCompleted));
        });
}
```

### 清理命令

#### OnTearDown
在测试结束时执行清理，适合资源释放：

```cpp
TEST_METHOD(CommandBuilder_OnTearDown_ShouldCleanup)
{
    AActor* TempActor = nullptr;
    bool CleanupCalled = false;

    TestCommandBuilder
        .Do([&]() {
            TempActor = GetWorld()->SpawnActor<AActor>(FVector::ZeroVector);
        })
        .OnTearDown([&]() {
            if (TempActor)
            {
                TempActor->Destroy();
                CleanupCalled = true;
            }
        })
        .Then([&]() {
            ASSERT_THAT(IsNotNull(TempActor));
        });

    // 测试结束后，OnTearDown中的代码会自动执行
    ASSERT_THAT(IsTrue(CleanupCalled));
}
```

#### 多个清理命令
```cpp
TEST_METHOD(CommandBuilder_MultipleCleanup_ShouldExecuteInReverseOrder)
{
    int32 CleanupOrder = 0;
    TArray<int32> ExecutionOrder;

    TestCommandBuilder
        .Do([&]() {
            // 测试逻辑
        })
        .OnTearDown([&]() {
            ExecutionOrder.Add(1);
            CleanupOrder++;
        })
        .OnTearDown([&]() {
            ExecutionOrder.Add(2);
            CleanupOrder++;
        })
        .OnTearDown([&]() {
            ExecutionOrder.Add(3);
            CleanupOrder++;
        });

    // 清理命令按相反顺序执行（3, 2, 1）
    ASSERT_THAT(AreEqual(3, ExecutionOrder.Num()));
    ASSERT_THAT(AreEqual(3, ExecutionOrder[0])); // 最后添加的先执行
    ASSERT_THAT(AreEqual(2, ExecutionOrder[1]));
    ASSERT_THAT(AreEqual(1, ExecutionOrder[2]));
}
```

### TestCommandBuilder vs 手动AddCommand

| 特性     | TestCommandBuilder | 手动AddCommand     |
| -------- | ------------------ | ------------------ |
| 可读性   | 高（链式调用）     | 中等               |
| 灵活性   | 中等               | 高                 |
| 适用场景 | 简单到中等复杂度   | 复杂场景、条件分支 |

```cpp
// 使用TestCommandBuilder（推荐用于简单场景）
TestCommandBuilder
    .Do([&]() { Step1(); })
    .Then([&]() { Step2(); })
    .Until([&]() { return Step3Complete(); });

// 使用手动AddCommand（更灵活）
if (ConditionA)
{
    AddCommand(new FExecute([&]() { StepA1(); }));
    AddCommand(new FWaitUntil([&]() { return StepA1Complete(); }));
}
else if (ConditionB)
{
    AddCommand(new FExecute([&]() { StepB1(); }));
    AddCommand(new FWaitUntil([&]() { return StepB1Complete(); }));
}
AddCommand(new FExecute([&]() { FinalStep(); }));
```

### 最佳实践
1. **优先使用FWaitUntil**：避免固定延迟，提高测试稳定性
2. **合理设置超时**：根据操作实际耗时设置超时时间
3. **使用TestCommandBuilder**：提高可读性，适用于顺序操作
4. **利用OnTearDown**：确保资源清理，即使测试失败也会执行
5. **保持Lambda简洁**：避免在Lambda中执行复杂逻辑
6. **避免嵌套Latent Actions**：框架不支持在Latent Action中添加新的Latent Actions

## 综合示例

### 完整的游戏循环测试
```cpp
TEST_CLASS(GameplayFlowTest, "Game.Gameplay")
{
    ACharacter* Player = nullptr;
    AEnemy* Enemy = nullptr;
    UAnimMontage* AttackMontage = nullptr;
    bool PlayerSpawned = false;
    bool EnemySpawned = false;
    bool AttackStarted = false;
    bool AttackCompleted = false;
    bool EnemyDamaged = false;

    BEFORE_EACH()
    {
        // 加载资源
        AttackMontage = LoadObj<UAnimMontage>(TEXT("/Game/Animations/Attack"));
    }

    TEST_METHOD(CompleteGameplayFlow_ShouldSucceed)
    {
        TestCommandBuilder
            // 步骤1：生成玩家
            .Do([&]() {
                Player = GetWorld()->SpawnActor<ACharacter>(FVector::ZeroVector);
            })
            // 步骤2：等待玩家就绪
            .Until([&]() {
                if (Player && Player->IsValidLowLevel())
                {
                    PlayerSpawned = true;
                    return true;
                }
                return false;
            }, 2.0f)
            // 步骤3：生成敌人
            .Do([&]() {
                Enemy = GetWorld()->SpawnActor<AEnemy>(FVector(200, 0, 0));
            })
            // 步骤4：等待敌人就绪
            .Until([&]() {
                if (Enemy && Enemy->IsValidLowLevel())
                {
                    EnemySpawned = true;
                    return true;
                }
                return false;
            }, 2.0f)
            // 步骤5：玩家攻击
            .Do([&]() {
                Player->PlayAnimMontage(AttackMontage);
                AttackStarted = true;
            })
            // 步骤6：等待动画开始
            .Until([&]() {
                return AttackStarted && Player->GetMesh()->GetAnimInstance()->IsAnyMontagePlaying();
            }, 1.0f)
            // 步骤7：等待攻击命中敌人
            .Until([&]() {
                if (Enemy && Enemy->GetHealth() < 100.0f)
                {
                    EnemyDamaged = true;
                    return true;
                }
                return false;
            }, 2.0f)
            // 步骤8：等待动画完成
            .Until([&]() {
                AttackCompleted = !Player->GetMesh()->GetAnimInstance()->IsAnyMontagePlaying();
                return AttackCompleted;
            }, 3.0f)
            // 步骤9：验证结果
            .Then([&]() {
                ASSERT_THAT(IsTrue(PlayerSpawned));
                ASSERT_THAT(IsTrue(EnemySpawned));
                ASSERT_THAT(IsTrue(AttackStarted));
                ASSERT_THAT(IsTrue(AttackCompleted));
                ASSERT_THAT(IsTrue(EnemyDamaged));
                ASSERT_THAT(IsTrue(Enemy->GetHealth() < 100.0f));
            })
            // 清理
            .OnTearDown([&]() {
                if (Player) Player->Destroy();
                if (Enemy) Enemy->Destroy();
            });
    }
};
```