// Network测试实现文件模板
// 注意：必须指定 EAutomationTestFlags::EditorContext 标志

#include "CQTest.h"
#include "GameFramework/Actor.h"
#include "GameFramework/Character.h"
#include "NetworkTestHelper.h"

TEST_CLASS(NetworkReplicationTest, "Game.Network")
    , public EAutomationTestFlags::EditorContext
{
    // 数据成员
    NetworkTestHelper* NetworkHelper = nullptr;
    AMyNetworkActor* ServerActor = nullptr;
    AMyNetworkActor* Client0Actor = nullptr;
    AMyNetworkActor* Client1Actor = nullptr;

    // 在每个测试之前执行
    BEFORE_EACH()
    {
        // 初始化网络：1服务器，2客户端
        NetworkHelper = new NetworkTestHelper();
        const bool InitResult = NetworkHelper->Initialize(2);
        ASSERT_THAT(IsTrue(InitResult));

        // 在服务器上生成Actor
        ServerActor = NetworkHelper->GetServerWorld()->SpawnActor<AMyNetworkActor>(FVector::ZeroVector);
        ASSERT_THAT(IsNotNull(ServerActor));
    }

    // 在每个测试之后执行
    AFTER_EACH()
    {
        // 清理网络环境
        if (NetworkHelper)
        {
            NetworkHelper->Shutdown();
            delete NetworkHelper;
            NetworkHelper = nullptr;
        }
    }

    // 测试复制变量同步
    TEST_METHOD(ReplicatedVariable_ShouldSyncToClients)
    {
        const int32 TestValue = 42;
        ServerActor->SetReplicatedValue(TestValue);

        // 等待复制到客户端0
        AddCommand(new FWaitUntil([&]() {
            Client0Actor = NetworkHelper->GetClientActor<AMyNetworkActor>(0);
            return Client0Actor && Client0Actor->GetReplicatedValue() == TestValue;
        }, 5.0f));

        // 等待复制到客户端1
        AddCommand(new FWaitUntil([&]() {
            Client1Actor = NetworkHelper->GetClientActor<AMyNetworkActor>(1);
            return Client1Actor && Client1Actor->GetReplicatedValue() == TestValue;
        }, 5.0f));

        ASSERT_THAT(AreEqual(TestValue, Client0Actor->GetReplicatedValue()));
        ASSERT_THAT(AreEqual(TestValue, Client1Actor->GetReplicatedValue()));
    }

    // 测试多个复制变量
    TEST_METHOD(MultipleReplicatedVariables_ShouldAllSync)
    {
        const int32 IntValue = 100;
        const float FloatValue = 3.14f;
        const FString StringValue = TEXT("TestString");

        ServerActor->SetReplicatedInt(IntValue);
        ServerActor->SetReplicatedFloat(FloatValue);
        ServerActor->SetReplicatedString(StringValue);

        // 等待所有变量复制
        AddCommand(new FWaitUntil([&]() {
            AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(0);
            return ClientActor &&
                   ClientActor->GetReplicatedInt() == IntValue &&
                   FMath::IsNearlyEqual(ClientActor->GetReplicatedFloat(), FloatValue, 0.001f) &&
                   ClientActor->GetReplicatedString() == StringValue;
        }, 5.0f));

        AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(0);
        ASSERT_THAT(AreEqual(IntValue, ClientActor->GetReplicatedInt()));
        ASSERT_THAT(IsTrue(FMath::IsNearlyEqual(FloatValue, ClientActor->GetReplicatedFloat(), 0.001f)));
        ASSERT_THAT(AreEqual(StringValue, ClientActor->GetReplicatedString()));
    }

    // 测试服务器RPC
    TEST_METHOD(ServerRPC_ShouldExecuteOnServer)
    {
        bool ServerRPCExecuted = false;
        ServerActor->OnServerRPCCalled.AddLambda([&]() {
            ServerRPCExecuted = true;
        });

        // 从客户端0调用服务器RPC
        AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(0);
        if (ClientActor)
        {
            ClientActor->Server_ExecuteRPC();
        }

        // 等待RPC执行
        AddCommand(new FWaitUntil([&]() {
            return ServerRPCExecuted;
        }, 3.0f));

        ASSERT_THAT(IsTrue(ServerRPCExecuted));
    }

    // 测试客户端RPC
    TEST_METHOD(ClientRPC_ShouldExecuteOnClient)
    {
        bool ClientRPCExecuted = false;
        AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(0);

        if (ClientActor)
        {
            ClientActor->OnClientRPCCalled.AddLambda([&]() {
                ClientRPCExecuted = true;
            });

            // 从服务器调用客户端RPC
            ServerActor->Client_ExecuteRPC(ClientActor);

            // 等待RPC执行
            AddCommand(new FWaitUntil([&]() {
                return ClientRPCExecuted;
            }, 3.0f));
        }

        ASSERT_THAT(IsTrue(ClientRPCExecuted));
    }

    // 测试多客户端RPC
    TEST_METHOD(MulticastRPC_ShouldExecuteOnAllClients)
    {
        int32 ExecutedCount = 0;
        const int32 ExpectedCount = 2; // 2个客户端

        // 注册所有客户端的回调
        for (int32 i = 0; i < ExpectedCount; i++)
        {
            AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(i);
            if (ClientActor)
            {
                ClientActor->OnMulticastRPCCalled.AddLambda([&]() {
                    ExecutedCount++;
                });
            }
        }

        // 从服务器调用Multicast RPC
        ServerActor->Multicast_ExecuteRPC();

        // 等待所有客户端执行
        AddCommand(new FWaitUntil([&]() {
            return ExecutedCount == ExpectedCount;
        }, 5.0f));

        ASSERT_THAT(AreEqual(ExpectedCount, ExecutedCount));
    }

    // 测试网络复制延迟
    TEST_METHOD(ReplicationDelay_ShouldBeAcceptable)
    {
        const int32 TestValue = 42;
        double ReplicationStartTime = 0.0;
        bool ReplicationStarted = false;

        ServerActor->OnVariableReplicated.AddLambda([&]() {
            if (!ReplicationStarted)
            {
                ReplicationStarted = true;
                ReplicationStartTime = FPlatformTime::Seconds();
            }
        });

        ServerActor->SetReplicatedValue(TestValue);

        // 等待复制完成
        AddCommand(new FWaitUntil([&]() {
            AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(0);
            return ClientActor && ClientActor->GetReplicatedValue() == TestValue;
        }, 5.0f));

        double ReplicationTime = FPlatformTime::Seconds() - ReplicationStartTime;

        // 验证复制延迟在合理范围内（<500ms）
        ASSERT_THAT(IsTrue(ReplicationTime < 0.5));
    }

    // 测试网络条件下的Actor生成
    TEST_METHOD(SpawnActor_ShouldReplicateToClients)
    {
        const FVector SpawnLocation = FVector(100, 0, 0);

        // 在服务器上生成新Actor
        AMyNetworkActor* NewActor = NetworkHelper->GetServerWorld()->SpawnActor<AMyNetworkActor>(SpawnLocation);

        // 等待Actor复制到客户端
        AddCommand(new FWaitUntil([&]() {
            for (int32 i = 0; i < 2; i++)
            {
                AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(i);
                if (!ClientActor || ClientActor->GetActorLocation() != SpawnLocation)
                {
                    return false;
                }
            }
            return true;
        }, 5.0f));

        // 验证所有客户端都有该Actor
        for (int32 i = 0; i < 2; i++)
        {
            AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(i);
            ASSERT_THAT(IsNotNull(ClientActor));
            ASSERT_THAT(AreEqual(SpawnLocation, ClientActor->GetActorLocation()));
        }
    }

    // 测试Actor销毁复制
    TEST_METHOD(ActorDestroy_ShouldReplicateToClients)
    {
        // 等待Actor复制到客户端
        AddCommand(new FWaitUntil([&]() {
            for (int32 i = 0; i < 2; i++)
            {
                AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(i);
                if (!ClientActor)
                {
                    return false;
                }
            }
            return true;
        }, 5.0f));

        // 在服务器上销毁Actor
        ServerActor->Destroy();

        // 等待Actor在客户端上销毁
        AddCommand(new FWaitUntil([&]() {
            for (int32 i = 0; i < 2; i++)
            {
                AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(i);
                if (ClientActor)
                {
                    return false;
                }
            }
            return true;
        }, 5.0f));

        // 验证所有客户端上Actor都已销毁
        for (int32 i = 0; i < 2; i++)
        {
            AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(i);
            ASSERT_THAT(IsNull(ClientActor));
        }
    }

    // 使用Command Builder测试网络流程
    TEST_METHOD(NetworkWorkflow_UsingCommandBuilder)
    {
        const int32 TestValue = 100;
        bool ValueReplicated = false;
        bool ServerRPCExecuted = false;
        bool ClientRPCExecuted = false;

        ServerActor->OnVariableReplicated.AddLambda([&]() {
            ValueReplicated = true;
        });

        ServerActor->OnServerRPCCalled.AddLambda([&]() {
            ServerRPCExecuted = true;
        });

        AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(0);
        if (ClientActor)
        {
            ClientActor->OnClientRPCCalled.AddLambda([&]() {
                ClientRPCExecuted = true;
            });
        }

        TestCommandBuilder
            // 设置复制变量
            .Do([&]() {
                ServerActor->SetReplicatedValue(TestValue);
            })
            // 等待复制
            .Until([&]() {
                AMyNetworkActor* ClientActor = NetworkHelper->GetClientActor<AMyNetworkActor>(0);
                return ClientActor && ClientActor->GetReplicatedValue() == TestValue;
            }, 5.0f)
            // 验证复制
            .Then([&]() {
                ASSERT_THAT(IsTrue(ValueReplicated));
            })
            // 调用服务器RPC
            .Do([&]() {
                if (ClientActor)
                {
                    ClientActor->Server_ExecuteRPC();
                }
            })
            // 等待RPC执行
            .Until([&]() {
                return ServerRPCExecuted;
            }, 3.0f)
            // 调用客户端RPC
            .Do([&]() {
                ServerActor->Client_ExecuteRPC(ClientActor);
            })
            // 等待RPC执行
            .Until([&]() {
                return ClientRPCExecuted;
            }, 3.0f)
            // 验证所有操作
            .Then([&]() {
                ASSERT_THAT(IsTrue(ServerRPCExecuted));
                ASSERT_THAT(IsTrue(ClientRPCExecuted));
            });
    }
};
