# Google Test / Catch2 最佳实践

C/C++ 测试框架的配置和最佳实践指南。

## 目录

- [项目配置](#项目配置)
- [测试结构](#测试结构)
- [断言最佳实践](#断言最佳实践)
- [参数化测试](#参数化测试)
- [Mock 策略](#mock-策略)
- [Fixtures](#fixtures)
- [覆盖率配置](#覆盖率配置)

---

## 项目配置

### Google Test (CMake)

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.14)
project(MyProject)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 启用测试
enable_testing()

# 添加 Google Test
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG v1.14.0
)
FetchContent_MakeAvailable(googletest)

# 主库
add_library(mylib
    src/user_service.cpp
    src/user_repository.cpp
)
target_include_directories(mylib PUBLIC include)

# 测试可执行文件
add_executable(mylib_tests
    tests/user_service_test.cpp
    tests/user_repository_test.cpp
)
target_link_libraries(mylib_tests
    mylib
    GTest::gtest_main
    GTest::gmock_main
)

# 注册测试
include(GoogleTest)
gtest_discover_tests(mylib_tests)

# 覆盖率配置 (GCC/Clang)
option(ENABLE_COVERAGE "Enable coverage reporting" OFF)
if(ENABLE_COVERAGE)
    target_compile_options(mylib_tests PRIVATE --coverage -O0 -g)
    target_link_options(mylib_tests PRIVATE --coverage)
endif()
```

### Catch2 (CMake)

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.14)
project(MyProject)

set(CMAKE_CXX_STANDARD 17)

enable_testing()

# 添加 Catch2
include(FetchContent)
FetchContent_Declare(
    Catch2
    GIT_REPOSITORY https://github.com/catchorg/Catch2.git
    GIT_TAG v3.5.0
)
FetchContent_MakeAvailable(Catch2)

# 主库
add_library(mylib src/user_service.cpp)
target_include_directories(mylib PUBLIC include)

# 测试
add_executable(tests
    tests/user_service_test.cpp
)
target_link_libraries(tests
    mylib
    Catch2::Catch2WithMain
)

include(CTest)
include(Catch)
catch_discover_tests(tests)
```

### 目录结构

```
myproject/
├── include/
│   └── myproject/
│       ├── user_service.hpp
│       └── user_repository.hpp
├── src/
│   ├── user_service.cpp
│   └── user_repository.cpp
├── tests/
│   ├── user_service_test.cpp
│   ├── user_repository_test.cpp
│   ├── mocks/
│   │   └── mock_user_repository.hpp
│   └── fixtures/
│       └── test_fixtures.hpp
├── CMakeLists.txt
└── README.md
```

---

## 测试结构

### Google Test 基本结构

```cpp
#include <gtest/gtest.h>
#include "myproject/user_service.hpp"
#include "mocks/mock_user_repository.hpp"

namespace myproject {
namespace {

class UserServiceTest : public ::testing::Test {
protected:
    void SetUp() override {
        mock_repo_ = std::make_shared<MockUserRepository>();
        service_ = std::make_unique<UserService>(mock_repo_);
    }

    void TearDown() override {
        service_.reset();
        mock_repo_.reset();
    }

    std::shared_ptr<MockUserRepository> mock_repo_;
    std::unique_ptr<UserService> service_;
};

TEST_F(UserServiceTest, CreateUser_ShouldCreateUser_WhenInputIsValid) {
    // Arrange
    CreateUserRequest request{"test@example.com", "Test User"};
    EXPECT_CALL(*mock_repo_, ExistsByEmail("test@example.com"))
        .WillOnce(::testing::Return(false));
    EXPECT_CALL(*mock_repo_, Save(::testing::_))
        .WillOnce(::testing::Return(true));

    // Act
    auto result = service_->CreateUser(request);

    // Assert
    ASSERT_TRUE(result.has_value());
    EXPECT_EQ(result->email, "test@example.com");
    EXPECT_EQ(result->name, "Test User");
}

TEST_F(UserServiceTest, CreateUser_ShouldReturnError_WhenEmailExists) {
    // Arrange
    CreateUserRequest request{"existing@example.com", "New User"};
    EXPECT_CALL(*mock_repo_, ExistsByEmail("existing@example.com"))
        .WillOnce(::testing::Return(true));

    // Act
    auto result = service_->CreateUser(request);

    // Assert
    ASSERT_FALSE(result.has_value());
    EXPECT_EQ(result.error(), UserError::DuplicateEmail);
}

}  // namespace
}  // namespace myproject
```

### Catch2 基本结构

```cpp
#include <catch2/catch_test_macros.hpp>
#include "myproject/user_service.hpp"

namespace myproject {

TEST_CASE("UserService::CreateUser", "[user][service]") {
    auto mock_repo = std::make_shared<MockUserRepository>();
    UserService service(mock_repo);

    SECTION("should create user when input is valid") {
        // Arrange
        mock_repo->SetExistsByEmailResult(false);
        CreateUserRequest request{"test@example.com", "Test User"};

        // Act
        auto result = service.CreateUser(request);

        // Assert
        REQUIRE(result.has_value());
        CHECK(result->email == "test@example.com");
        CHECK(result->name == "Test User");
    }

    SECTION("should return error when email exists") {
        // Arrange
        mock_repo->SetExistsByEmailResult(true);
        CreateUserRequest request{"existing@example.com", "New User"};

        // Act
        auto result = service.CreateUser(request);

        // Assert
        REQUIRE_FALSE(result.has_value());
        CHECK(result.error() == UserError::DuplicateEmail);
    }
}

}  // namespace myproject
```

### 测试命名规范

```cpp
// ❌ 不好的命名
TEST(Test1, Test) {}
TEST(UserTest, Create) {}

// ✅ 好的命名 - Google Test
TEST(UserServiceTest, CreateUser_ShouldCreateUser_WhenInputIsValid) {}
TEST(UserServiceTest, CreateUser_ShouldReturnError_WhenEmailExists) {}

// ✅ 好的命名 - Catch2
TEST_CASE("UserService::CreateUser creates user when input is valid", "[user]") {}
TEST_CASE("UserService::CreateUser returns error when email exists", "[user]") {}
```

---

## 断言最佳实践

### Google Test 断言

```cpp
// 基本断言
EXPECT_EQ(expected, actual);      // 相等
EXPECT_NE(unexpected, actual);    // 不相等
EXPECT_LT(a, b);                  // a < b
EXPECT_LE(a, b);                  // a <= b
EXPECT_GT(a, b);                  // a > b
EXPECT_GE(a, b);                  // a >= b

// 布尔断言
EXPECT_TRUE(condition);
EXPECT_FALSE(condition);

// 字符串断言
EXPECT_STREQ(expected, actual);           // C 字符串相等
EXPECT_STRNE(unexpected, actual);         // C 字符串不相等
EXPECT_STRCASEEQ(expected, actual);       // 忽略大小写

// 浮点数断言
EXPECT_FLOAT_EQ(expected, actual);
EXPECT_DOUBLE_EQ(expected, actual);
EXPECT_NEAR(expected, actual, tolerance);

// 异常断言
EXPECT_THROW(statement, exception_type);
EXPECT_NO_THROW(statement);
EXPECT_ANY_THROW(statement);

// ASSERT vs EXPECT
// ASSERT_* - 失败时终止当前测试
// EXPECT_* - 失败时继续执行
ASSERT_NE(ptr, nullptr);  // 后续依赖 ptr 不为空
EXPECT_EQ(ptr->value, 42);
```

### Catch2 断言

```cpp
// 基本断言
REQUIRE(condition);        // 失败时终止
CHECK(condition);          // 失败时继续

REQUIRE(a == b);
CHECK(a != b);

// 比较
REQUIRE(a == b);
REQUIRE(a < b);
REQUIRE_THAT(str, Catch::Matchers::StartsWith("Hello"));

// 异常
REQUIRE_THROWS(expression);
REQUIRE_THROWS_AS(expression, exception_type);
REQUIRE_NOTHROW(expression);

// 浮点数
REQUIRE(a == Catch::Approx(b));
REQUIRE(a == Catch::Approx(b).epsilon(0.01));

// Matchers
using namespace Catch::Matchers;
REQUIRE_THAT(str, StartsWith("Hello") && EndsWith("World"));
REQUIRE_THAT(vec, Contains(42));
REQUIRE_THAT(vec, SizeIs(3));
```

### 禁止弱断言

```cpp
// ❌ 弱断言 - 几乎不验证任何东西
EXPECT_NE(result, nullptr);
EXPECT_TRUE(result.has_value());
EXPECT_FALSE(list.empty());

// ✅ 强断言 - 验证具体值
ASSERT_NE(result, nullptr);
EXPECT_EQ(result->status, Status::Success);
EXPECT_EQ(result->email, "test@example.com");

ASSERT_TRUE(result.has_value());
EXPECT_EQ(result->value, 42);

ASSERT_EQ(list.size(), 3);
EXPECT_EQ(list[0], "expected_item");
```

### 自定义匹配器

```cpp
// Google Test 自定义匹配器
MATCHER_P(HasEmail, email, "") {
    return arg.email == email;
}

TEST_F(UserServiceTest, CreateUser_WithMatcher) {
    // ...
    EXPECT_THAT(result.value(), HasEmail("test@example.com"));
}

// Catch2 自定义匹配器
class HasEmailMatcher : public Catch::Matchers::MatcherBase<User> {
    std::string expected_email_;
public:
    HasEmailMatcher(std::string email) : expected_email_(std::move(email)) {}

    bool match(const User& user) const override {
        return user.email == expected_email_;
    }

    std::string describe() const override {
        return "has email " + expected_email_;
    }
};

HasEmailMatcher HasEmail(std::string email) {
    return HasEmailMatcher(std::move(email));
}

TEST_CASE("User matcher") {
    User user{"test@example.com", "Test"};
    REQUIRE_THAT(user, HasEmail("test@example.com"));
}
```

---

## 参数化测试

### Google Test 参数化

```cpp
// 值参数化测试
class ValidateEmailTest : public ::testing::TestWithParam<std::pair<std::string, bool>> {};

TEST_P(ValidateEmailTest, ShouldReturnExpectedResult) {
    auto [email, expected] = GetParam();
    EXPECT_EQ(ValidateEmail(email), expected);
}

INSTANTIATE_TEST_SUITE_P(
    EmailValidation,
    ValidateEmailTest,
    ::testing::Values(
        std::make_pair("", false),
        std::make_pair(" ", false),
        std::make_pair("invalid", false),
        std::make_pair("test@", false),
        std::make_pair("test@example.com", true)
    )
);

// 类型参数化测试
template <typename T>
class ContainerTest : public ::testing::Test {
protected:
    T container_;
};

using ContainerTypes = ::testing::Types<std::vector<int>, std::list<int>, std::deque<int>>;
TYPED_TEST_SUITE(ContainerTest, ContainerTypes);

TYPED_TEST(ContainerTest, ShouldBeEmptyInitially) {
    EXPECT_TRUE(this->container_.empty());
}

TYPED_TEST(ContainerTest, ShouldNotBeEmptyAfterPush) {
    this->container_.push_back(42);
    EXPECT_FALSE(this->container_.empty());
}
```

### Catch2 参数化

```cpp
// 使用 GENERATE
TEST_CASE("ValidateEmail returns expected result", "[validation]") {
    auto [email, expected] = GENERATE(table<std::string, bool>({
        {"", false},
        {" ", false},
        {"invalid", false},
        {"test@", false},
        {"test@example.com", true}
    }));

    CAPTURE(email);  // 失败时显示参数值
    CHECK(ValidateEmail(email) == expected);
}

// 范围生成
TEST_CASE("Factorial", "[math]") {
    auto n = GENERATE(range(0, 10));

    CAPTURE(n);
    CHECK(Factorial(n) > 0);
}

// 组合生成
TEST_CASE("Calculator add", "[math]") {
    auto a = GENERATE(1, 2, 3);
    auto b = GENERATE(10, 20, 30);

    CAPTURE(a, b);
    CHECK(Add(a, b) == a + b);
}
```

---

## Mock 策略

### Google Mock

```cpp
// 定义 Mock 类
#include <gmock/gmock.h>

class MockUserRepository : public UserRepositoryInterface {
public:
    MOCK_METHOD(bool, Save, (const User& user), (override));
    MOCK_METHOD(std::optional<User>, FindById, (int id), (override));
    MOCK_METHOD(bool, ExistsByEmail, (const std::string& email), (override));
    MOCK_METHOD(void, Delete, (int id), (override));
};

// 使用 Mock
TEST_F(UserServiceTest, CreateUser_ShouldCallRepository) {
    using ::testing::_;
    using ::testing::Return;
    using ::testing::Invoke;

    // 设置期望
    EXPECT_CALL(*mock_repo_, ExistsByEmail("test@example.com"))
        .Times(1)
        .WillOnce(Return(false));

    EXPECT_CALL(*mock_repo_, Save(_))
        .Times(1)
        .WillOnce(Invoke([](const User& user) {
            EXPECT_EQ(user.email, "test@example.com");
            return true;
        }));

    // 执行
    auto result = service_->CreateUser({"test@example.com", "Test"});

    // Mock 期望会在测试结束时自动验证
}

// 参数匹配器
TEST_F(UserServiceTest, WithMatchers) {
    using namespace ::testing;

    EXPECT_CALL(*mock_repo_, Save(Field(&User::email, "test@example.com")));
    EXPECT_CALL(*mock_repo_, FindById(Gt(0)));
    EXPECT_CALL(*mock_repo_, ExistsByEmail(HasSubstr("@")));
}

// 调用顺序
TEST_F(UserServiceTest, CallOrder) {
    using namespace ::testing;

    InSequence seq;

    EXPECT_CALL(*mock_repo_, ExistsByEmail(_)).WillOnce(Return(false));
    EXPECT_CALL(*mock_repo_, Save(_)).WillOnce(Return(true));
}
```

### 手动 Mock (无框架)

```cpp
// 简单的手动 Mock
class MockUserRepository : public UserRepositoryInterface {
public:
    // 记录调用
    std::vector<User> saved_users;
    std::vector<int> find_by_id_calls;

    // 配置返回值
    bool exists_by_email_result = false;
    std::optional<User> find_by_id_result;

    bool Save(const User& user) override {
        saved_users.push_back(user);
        return true;
    }

    std::optional<User> FindById(int id) override {
        find_by_id_calls.push_back(id);
        return find_by_id_result;
    }

    bool ExistsByEmail(const std::string& email) override {
        return exists_by_email_result;
    }

    void Reset() {
        saved_users.clear();
        find_by_id_calls.clear();
        exists_by_email_result = false;
        find_by_id_result = std::nullopt;
    }
};

// 使用
TEST_F(UserServiceTest, CreateUser_ManualMock) {
    mock_repo_->exists_by_email_result = false;

    auto result = service_->CreateUser({"test@example.com", "Test"});

    ASSERT_EQ(mock_repo_->saved_users.size(), 1);
    EXPECT_EQ(mock_repo_->saved_users[0].email, "test@example.com");
}
```

---

## Fixtures

### Google Test Fixtures

```cpp
class UserServiceTest : public ::testing::Test {
protected:
    // 每个测试前执行
    void SetUp() override {
        mock_repo_ = std::make_shared<MockUserRepository>();
        service_ = std::make_unique<UserService>(mock_repo_);
    }

    // 每个测试后执行
    void TearDown() override {
        service_.reset();
        mock_repo_.reset();
    }

    // 共享成员
    std::shared_ptr<MockUserRepository> mock_repo_;
    std::unique_ptr<UserService> service_;

    // 辅助方法
    User CreateTestUser(const std::string& email = "test@example.com") {
        return User{1, email, "Test User"};
    }
};

// 测试套件级 Fixture
class DatabaseTest : public ::testing::Test {
protected:
    static void SetUpTestSuite() {
        // 所有测试前执行一次
        db_ = std::make_shared<TestDatabase>();
        db_->Migrate();
    }

    static void TearDownTestSuite() {
        // 所有测试后执行一次
        db_.reset();
    }

    void SetUp() override {
        // 每个测试前
        db_->BeginTransaction();
    }

    void TearDown() override {
        // 每个测试后
        db_->RollbackTransaction();
    }

    static std::shared_ptr<TestDatabase> db_;
};

std::shared_ptr<TestDatabase> DatabaseTest::db_;
```

### Catch2 Fixtures

```cpp
// 使用类作为 Fixture
class UserServiceFixture {
protected:
    std::shared_ptr<MockUserRepository> mock_repo =
        std::make_shared<MockUserRepository>();
    UserService service{mock_repo};

    User CreateTestUser(const std::string& email = "test@example.com") {
        return User{1, email, "Test User"};
    }
};

TEST_CASE_METHOD(UserServiceFixture, "UserService creates user", "[user]") {
    mock_repo->SetExistsByEmailResult(false);
    auto user = CreateTestUser();

    auto result = service.CreateUser({"test@example.com", "Test"});

    REQUIRE(result.has_value());
}

// 使用 SECTION 共享设置
TEST_CASE("UserService", "[user]") {
    auto mock_repo = std::make_shared<MockUserRepository>();
    UserService service(mock_repo);

    SECTION("CreateUser") {
        SECTION("creates user when input is valid") {
            mock_repo->SetExistsByEmailResult(false);
            auto result = service.CreateUser({"test@example.com", "Test"});
            REQUIRE(result.has_value());
        }

        SECTION("returns error when email exists") {
            mock_repo->SetExistsByEmailResult(true);
            auto result = service.CreateUser({"existing@example.com", "Test"});
            REQUIRE_FALSE(result.has_value());
        }
    }
}
```

---

## 覆盖率配置

### GCC/Clang 覆盖率

```cmake
# CMakeLists.txt
option(ENABLE_COVERAGE "Enable coverage" OFF)

if(ENABLE_COVERAGE)
    if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
        add_compile_options(--coverage -O0 -g)
        add_link_options(--coverage)
    endif()
endif()
```

### 使用 lcov

```bash
#!/bin/bash
# scripts/coverage.sh

# 清理旧数据
lcov --directory . --zerocounters

# 运行测试
./build/mylib_tests

# 收集覆盖率
lcov --directory . --capture --output-file coverage.info

# 过滤系统文件
lcov --remove coverage.info '/usr/*' '*/tests/*' --output-file coverage.info

# 生成 HTML 报告
genhtml coverage.info --output-directory coverage_report

# 检查覆盖率门禁
COVERAGE=$(lcov --summary coverage.info 2>&1 | grep "lines" | awk '{print $2}' | sed 's/%//')
if (( $(echo "$COVERAGE < 80" | bc -l) )); then
    echo "Coverage $COVERAGE% is below 80%"
    exit 1
fi
```

### 使用 gcovr

```bash
# 生成报告
gcovr --root . --exclude 'tests/*' --html --html-details -o coverage.html

# JSON 格式
gcovr --root . --exclude 'tests/*' --json coverage.json

# 检查门禁
gcovr --root . --exclude 'tests/*' --fail-under-line 80
```

### CI 配置

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y lcov

      - name: Configure
        run: cmake -B build -DENABLE_COVERAGE=ON

      - name: Build
        run: cmake --build build

      - name: Test
        run: ctest --test-dir build --output-on-failure

      - name: Coverage
        run: |
          lcov --directory . --capture --output-file coverage.info
          lcov --remove coverage.info '/usr/*' '*/tests/*' --output-file coverage.info
          lcov --summary coverage.info

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: coverage.info
```

---

## 常用命令

```bash
# CMake 构建和测试
cmake -B build
cmake --build build
ctest --test-dir build

# 运行特定测试 (Google Test)
./build/mylib_tests --gtest_filter=UserServiceTest.*
./build/mylib_tests --gtest_filter=*CreateUser*

# 运行特定测试 (Catch2)
./build/tests "[user]"
./build/tests "UserService*"

# 列出所有测试
./build/mylib_tests --gtest_list_tests
./build/tests --list-tests

# 详细输出
./build/mylib_tests --gtest_print_time=1
./build/tests -s  # Catch2 显示成功的测试

# 重复运行 (检查稳定性)
./build/mylib_tests --gtest_repeat=10

# 打乱顺序
./build/mylib_tests --gtest_shuffle

# 覆盖率
cmake -B build -DENABLE_COVERAGE=ON
cmake --build build
ctest --test-dir build
lcov --directory . --capture --output-file coverage.info
genhtml coverage.info --output-directory coverage_report
```

---

## 参考资源

- [Google Test Documentation](https://google.github.io/googletest/)
- [Google Mock Documentation](https://google.github.io/googletest/gmock_for_dummies.html)
- [Catch2 Documentation](https://github.com/catchorg/Catch2/blob/devel/docs/Readme.md)
- [lcov Documentation](https://github.com/linux-test-project/lcov)
- [gcovr Documentation](https://gcovr.com/)
