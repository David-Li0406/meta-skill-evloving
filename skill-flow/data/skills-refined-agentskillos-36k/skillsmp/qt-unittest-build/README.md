# Qt Unit Test Build Skill

为 Qt 项目自动生成单元测试框架的技能。

## 设计理念

采用"固定脚本 + 动态AI"架构：
- **固定部分**：stub-ext Mock 工具、测试运行脚本、CMake 工具（硬编码在 Skill 的 resources/ 目录）
- **可变部分**：项目结构分析、Qt 版本检测、依赖识别、CMakeLists.txt 生成（AI 动态完成）

## 架构概览

```
用户请求 → 主 Agent → qt-unittest-build Skill（包含所有资源）
                                       ↓
                                   拷贝依赖和脚本
                                   调用子 Agent
                                       ↓
                          qt-unittest-builder 子 Agent
                                       ↓
                                   分析 + 生成 → 写入文件
```

**组件说明：**
- **qt-unittest-build Skill**：完整功能包，包含：
  - SKILL.md：安装和调度逻辑
  - agent/qt-unittest-builder.md：子 Agent（分析+生成）
  - resources/stub/：stub-ext 完整源码
  - resources/scripts/：固定脚本（run-ut.sh, UnitTestUtils.cmake）
- **qt-unittest-builder Agent**：全栈执行者，负责项目分析、文件生成和写入

## 使用方法

### 基本用法

在 OpenCode 中，直接输入：

```
请为当前项目生成单元测试框架
```

或显式调用：

```
使用 qt-unittest-build 技能
```

### 执行流程

1. **Skill 触发**：qt-unittest-build Skill 接收到请求，指示主 Agent 调用子 Agent
2. **项目分析**：qt-unit-test-executor 子 Agent 分析项目：
   - 读取 CMakeLists.txt 或 .pro 文件
   - 推断项目名称、Qt 版本、C++ 标准
   - 识别第三方依赖
   - 确定源文件模式
   - 询问用户选择测试框架（如果无法自动推断）

3. **文件生成**：子 Agent 基于内置模板生成：
   - 根目录 CMakeLists.txt（修改或新增）
   - tests/CMakeLists.txt
   - tests/test_${PROJECT_NAME}.cpp
   - tests/3rdparty/stub/stub.h
   - tests/3rdparty/stub/stubext.h
   - tests/run-ut.sh
   - tests/README.md

4. **用户确认**：子 Agent 使用 `write` 工具写入文件前会询问用户确认

5. **完成提示**：生成完成后，提供构建和运行命令

### 生成的文件结构

```
project-root/
├── CMakeLists.txt          # 已修改/新增（添加 autotests 子目录）
└── autotests/
    ├── CMakeLists.txt      # 测试配置
    ├── cmake/
    │   └── UnitTestUtils.cmake  # CMake 工具
    ├── 3rdparty/
    │   └── stub/         # Stub-ext 完整源码
    │       ├── stub.h
    │       ├── addr_any.h
    │       ├── addr_pri.h
    │       ├── elfio.hpp
    │       ├── stubext.h
    │       ├── stub-shadow.h
    │       └── stub-shadow.cpp
    ├── run-ut.sh          # 测试运行脚本
    ├── README.md           # 测试文档
    └── [submodules]/      # 测试子目录（按项目结构）
        ├── CMakeLists.txt
        └── test_*.cpp
```

## 支持的测试框架

### Qt Test（默认）

**特点**：
- Qt 官方测试框架
- 与 Qt 生态系统完美集成
- 适合 Qt 项目

**依赖**：
```bash
# Ubuntu/Debian
sudo apt install qtbase5-dev  # Qt5
sudo apt install qt6-base-dev  # Qt6
```

### Google Test

**特点**：
- Google 的测试框架
- 丰富的断言宏
- 适合 C++ 项目

**依赖**：
```bash
# Ubuntu/Debian
sudo apt install libgtest-dev libgmock-dev
```

### Catch2

**特点**：
- 现代、轻量级
- 无需额外测试运行器
- 适合快速原型开发

**依赖**：
```bash
# Ubuntu/Debian
sudo apt install libcatch2-dev
```

## 运行测试

### 使用测试运行脚本（推荐）

```bash
cd autotests
./run-ut.sh
```

### 手动构建和运行

```bash
mkdir build && cd build
cmake .. -DBUILD_TESTS=ON
cmake --build .
ctest --output-on-failure
```

## Stub-Ext Mock 工具

本技能包含 stub-ext 的完整源码（非精简版），支持：
- x86_64、ARM、AArch64 等多平台
- 函数 mock（普通函数）
- 虚函数 mock（VADDR 宏）
- 重载函数 mock（static_cast）
- UI 方法 mock（QWidget::show, QDialog::exec）

### 源码位置

stub-ext 源码来自 `resources/stub/`，包含：
- stub.h, addr_any.h, addr_pri.h, elfio.hpp（cpp-stub）
- stubext.h, stub-shadow.h, stub-shadow.cpp（stub-ext）

### 基本用法

### 使用示例

```cpp
#include "stubext.h"

// 原始函数
int calculateSum(int a, int b) {
    return a + b;
}

// 在测试中 mock
void mockSum(int& result, int a, int b) {
    result = 42; // 固定返回值
}

stub_ext::StubExt stub;
stub.set_lamda(calculateSum, mockSum);
```

## 与旧版本（qt-cpp-unittest-framework）的对比

| 特性 | qt-cpp-unittest-framework (v5.0.0) | qt-unittest-build (新) |
|------|-----------------------------------|----------------------|
| **架构** | 多脚本 + 占位符模式 | Skill + 子 Agent（扁平化）|
| **AI 调用** | 用户手动调用 AI | 子 Agent 自动调用 |
| **文件生成** | 模板 → 手动替换 → 最终文件 | 直接分析 → 直接生成 |
| **用户交互** | 5-6步手动流程 | 1句话，全自动 |
| **维护复杂度** | 多文件同步更新 | 只改 Agent 提示词 |
| **占位符** | 需要手动替换 | 无占位符 |

## 优势

1. **符合直觉**：用户说"生成测试"，系统直接找"测试专家"（子 Agent）
2. **维护简单**：所有逻辑在一个 Agent 文件，改模板只需改提示词
3. **灵活性高**：子 Agent 可以灵活决策：覆盖 vs 修改
4. **无技术债**：不需要管理 AI API 密钥、JSON 解析、占位符替换逻辑

## 注意事项

1. **CMake 版本**：需要 CMake 3.16+
2. **构建目录**：建议使用独立的构建目录（如 `build/` 或 `build-tests/`）
3. **第三方依赖**：确保项目所需的第三方库已正确安装和配置
4. **权限问题**：测试运行脚本需要执行权限（会自动设置）

## 故障排查

### CMake 配置失败

检查：
- CMake 版本（需要 3.16+）
- Qt 版本（Qt5 或 Qt6）
- 测试框架是否正确安装
- 编译器是否支持所需的 C++ 标准

### 测试运行失败

检查：
- 测试代码是否正确
- Mock 设置是否正确
- 依赖库是否正确链接

### Stub-Ext 不工作

检查：
- 函数签名是否匹配
- 是否使用正确的宏（`ADDR` 或 `VADDR`）
- 是否在测试结束后重置 stub

## 进阶使用

### 添加更多测试文件

1. 创建新的测试文件 `tests/test_feature.cpp`
2. 在 `tests/CMakeLists.txt` 中添加到测试目标

### 自定义测试框架

如果需要使用其他测试框架，可以在子 Agent 中添加对应的模板。

### 模块化测试

对于大型项目，可以为每个模块创建独立的测试子目录：
```
tests/
├── core/
│   └── CMakeLists.txt
├── ui/
│   └── CMakeLists.txt
└── main/
    └── CMakeLists.txt
```

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 相关资源

- **Qt Test 文档**：https://doc.qt.io/qt-6/qtest-overview.html
- **Google Test 文档**：https://google.github.io/googletest/
- **Catch2 文档**：https://github.com/catchorg/Catch2
- **Stub-Ext 源码**：https://github.com/manfredlohw/cpp-stub
