// 结构化测试模板 - 使用TEST_CLASS宏
// 用于需要Setup/Teardown、共享状态的测试

#include "CQTest.h"

TEST_CLASS(YourTestClass, "Game.YourModule")
{
    // 数据成员
    int32 TestValue = 0;
    bool SetupCalled = false;

    // 可选：在所有测试之前执行一次（静态方法）
    BEFORE_ALL()
    {
        // 执行全局初始化，如加载资源、配置系统等
    }

    // 在每个测试之前执行
    BEFORE_EACH()
    {
        // 初始化测试状态
        TestValue = 0;
        SetupCalled = true;
    }

    // 在每个测试之后执行
    AFTER_EACH()
    {
        // 清理测试资源
        TestValue = 0;
    }

    // 可选：在所有测试之后执行一次（静态方法）
    AFTER_ALL()
    {
        // 执行全局清理，如卸载资源等
    }

protected:
    // 辅助方法（protected，供测试方法使用）
    bool HelperMethod() const
    {
        return TestValue > 0;
    }

    void IncreaseValue(int32 Amount)
    {
        TestValue += Amount;
    }

public:
    // 测试方法
    TEST_METHOD(Setup_ShouldBeCalled)
    {
        ASSERT_THAT(IsTrue(SetupCalled));
    }

    TEST_METHOD(HelperMethod_ShouldWork)
    {
        TestValue = 10;
        ASSERT_THAT(IsTrue(HelperMethod()));
    }

    TEST_METHOD(ValueModification_ShouldPersistInTest)
    {
        const int32 InitialValue = TestValue;
        IncreaseValue(5);

        ASSERT_THAT(AreEqual(InitialValue + 5, TestValue));
    }

    TEST_METHOD(Value_ShouldResetBetweenTests)
    {
        // 每个测试TestValue都会重置为0
        ASSERT_THAT(AreEqual(0, TestValue));
    }
};
