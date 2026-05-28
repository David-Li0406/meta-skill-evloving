// 基础测试模板 - 使用TEST宏
// 用于简单的逻辑验证和独立测试

#include "CQTest.h"

TEST(YourTestName, "Game.YourModule")
{
    // 测试逻辑
    // 1. 准备测试数据
    const int32 ExpectedValue = 42;
    const int32 ActualValue = CalculateValue();

    // 2. 验证结果
    ASSERT_THAT(AreEqual(ExpectedValue, ActualValue));
}

// 更多测试示例...

TEST(BooleanTest, "Game.Math")
{
    const bool Condition = true;
    ASSERT_THAT(IsTrue(Condition));
}

TEST(StringTest, "Game.String")
{
    const FString Expected = TEXT("Hello");
    const FString Actual = TEXT("Hello");
    ASSERT_THAT(AreEqual(Expected, Actual));
}

TEST(NullPointerTest, "Game.Memory")
{
    UObject* Object = NewObject<UObject>();
    ASSERT_THAT(IsNotNull(Object));

    Object = nullptr;
    ASSERT_THAT(IsNull(Object));
}
