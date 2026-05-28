# CQTest框架核心概念

## 目录
- [概述](#概述)
- [测试宏](#测试宏)
- [断言](#断言)
- [Setup和Teardown](#setup和teardown)
- [命名空间和分类](#命名空间和分类)
- [异常处理](#异常处理)

## 概述
CQTest（Code Quality Test）是Unreal Engine FAutomationTestBase的扩展，提供了测试夹具和通用自动化测试命令。CQTest的目标是简化新测试的编写，并支持测试前后的自动操作来重置状态。

### 核心特性
- 简化的测试宏和语法
- 自动化的Setup和Teardown机制
- 支持Latent Actions（多帧操作）
- 组件化设计，易于扩展

## 测试宏

### TEST - 基础测试宏
用于创建简单的测试对象，适合不需要共享状态的独立测试。

```cpp
#include "CQTest.h"

TEST(MinimalTest, "Game.MyGame")
{
    ASSERT_THAT(IsTrue(true));
}
```

**参数说明：**
- 第一个参数：测试名称（必须是有效的C++标识符）
- 第二个参数：测试分类/命名空间（字符串，使用点号分隔层级）

### TEST_CLASS - 结构化测试宏
用于需要Setup、Teardown、共享状态和测试分组的测试对象。

```cpp
#include "CQTest.h"

TEST_CLASS(MyTest, "Game.MyGame")
{
    bool SetupCalled = false;
    uint32 SomeNumber = 0;

    BEFORE_EACH()
    {
        SetupCalled = true;
        SomeNumber++;
    }

    AFTER_EACH()
    {
        // 清理资源
    }

    TEST_METHOD(TestMethod)
    {
        ASSERT_THAT(IsTrue(SetupCalled));
    }
};
```

**可用的生命周期方法：**
- `BEFORE_ALL()`：在所有测试之前执行一次（静态方法）
- `BEFORE_EACH()`：在每个测试之前执行
- `AFTER_EACH()`：在每个测试之后执行
- `AFTER_ALL()`：在所有测试之后执行一次（静态方法）

### 其他测试宏变体

| 宏名称                         | 用途                                 |
| ------------------------------ | ------------------------------------ |
| TEST_CLASS_WITH_ASSERTS        | 使用自定义断言器的测试对象           |
| TEST_CLASS_WITH_BASE           | 继承自不同测试对象的测试对象         |
| TEST_CLASS_WITH_FLAGS          | 使用不同自动化测试标志的测试对象     |
| TEST_CLASS_WITH_BASE_AND_FLAGS | 可继承基类且使用自定义标志的测试对象 |

## 断言

### 基础断言宏
所有断言都使用 `ASSERT_THAT` 宏包装。

```cpp
// 布尔断言
ASSERT_THAT(IsTrue(true));
ASSERT_THAT(IsFalse(false));

// 相等性断言
ASSERT_THAT(AreEqual(ExpectedValue, ActualValue));

// 不等断言
ASSERT_THAT(AreNotEqual(UnexpectedValue, ActualValue));

// 数值比较（如果定义了比较运算符）
ASSERT_THAT(IsLessThan(ActualValue, ExpectedValue));
```

### 自定义类型断言
要为自定义类型使用断言，需要定义 `==`、`!=` 运算符和 `ToString()` 方法：

```cpp
struct MyCustomType
{
    int32 Value;

    bool operator==(const MyCustomType& other) const
    {
        return Value == other.Value;
    }

    bool operator!=(const MyCustomType& other) const
    {
        return !(*this == other);
    }

    FString ToString() const
    {
        return FString::Printf(TEXT("%d"), Value);
    }
};

// 使用自定义类型
TEST_METHOD(CustomTypeTest)
{
    MyCustomType A{42};
    MyCustomType B{42};
    ASSERT_THAT(AreEqual(A, B));
}
```

### 枚举类型断言
```cpp
enum struct MyCustomEnum
{
    Red, Green, Blue
};

template<>
FString CQTestConvert::ToString(const MyCustomEnum& Enum)
{
    switch (Enum)
    {
        case MyCustomEnum::Red: return TEXT("Red");
        case MyCustomEnum::Green: return TEXT("Green");
        case MyCustomEnum::Blue: return TEXT("Blue");
        default: return TEXT("Unknown");
    }
}

TEST_METHOD(EnumTest)
{
    ASSERT_THAT(AreEqual(MyCustomEnum::Red, MyCustomEnum::Red));
}
```

## Setup和Teardown

### BEFORE_EACH 和 AFTER_EACH
在每个测试方法执行前后自动调用：

```cpp
TEST_CLASS(ActorLifecycleTest, "Game.Actor")
{
    AMyActor* TestActor = nullptr;

    BEFORE_EACH()
    {
        // 在每个测试前创建Actor
        TestActor = NewObject<AMyActor>();
        TestActor->Initialize();
    }

    AFTER_EACH()
    {
        // 在每个测试后清理Actor
        if (TestActor)
        {
            TestActor->Destroy();
        }
    }

    TEST_METHOD(Actor_Initialization_IsSuccessful)
    {
        ASSERT_THAT(IsTrue(TestActor->IsInitialized()));
    }
};
```

### BEFORE_ALL 和 AFTER_ALL
在所有测试的开始和结束仅执行一次：

```cpp
TEST_CLASS(ResourceTest, "Game.Resource")
{
    static UResourceManager* ResourceManager;

    BEFORE_ALL()
    {
        // 加载共享资源（如关卡、配置等）
        ResourceManager = UResourceManager::Get();
        ResourceManager->LoadAllResources();
    }

    AFTER_ALL()
    {
        // 清理共享资源
        if (ResourceManager)
        {
            ResourceManager->UnloadAllResources();
        }
    }

    TEST_METHOD(Resource_Access_ShouldSucceed)
    {
        ASSERT_THAT(IsNotNull(ResourceManager));
    }
};
```

### Setup/Teardown注意事项
- BEFORE_EACH/AFTER_EACH：非静态方法，可以访问实例成员
- BEFORE_ALL/AFTER_ALL：静态方法，只能访问静态成员或通过静态资源管理
- 数据成员在每个测试之间会重置为初始值
- AFTER_EACH即使测试失败也会执行，确保资源清理

## 命名空间和分类

### 测试命名约定
测试分类使用点号分隔的字符串，建议遵循以下规范：
```
<模块>.<子系统>.<功能>.<场景>
```

**示例：**
```
"Game.Weapon.Fire.Reload"
"Game.Character.Movement.Jump"
"Game.UI.HUD.Display"
```

### 测试发现和运行
在Unreal Editor中：
1. 打开 Tools → Sessions Frontend
2. 测试按命名空间分组显示
3. 可以按命名空间过滤和运行测试

## 异常处理

### 异常支持
并非所有平台都支持异常，因此CQTest提供了多种处理方式：

#### 选项1：使用异常（仅支持异常的平台）
```cpp
TEST_METHOD(ExceptionExample)
{
    if (!Condition)
    {
        throw std::runtime_error("Condition failed");
    }
}
```

#### 选项2：返回[[nodiscard]] bool（默认推荐）
```cpp
[[nodiscard]] bool ValidateCondition()
{
    return ExpectedValue == ActualValue;
}

TEST_METHOD(ValidateTest)
{
    ASSERT_THAT(ValidateCondition());
}
```

#### 选项3：使用ASSERT_THAT宏进行早期返回
```cpp
TEST_METHOD(MultiStepTest)
{
    ASSERT_THAT(AreEqual(Step1Result, Expected));
    ASSERT_THAT(AreEqual(Step2Result, Expected));
    ASSERT_THAT(AreEqual(Step3Result, Expected));
}
```

### 异常处理最佳实践
- 优先使用 `ASSERT_THAT` 宏，它会自动处理早期返回
- Helper函数返回 `[[nodiscard]] bool` 以鼓励调用方检查
- 在支持异常的平台可以使用throw，但会降低跨平台兼容性
- 默认实现使用 `[[nodiscard]] bool`，配合 `ASSERT_THAT` 使用