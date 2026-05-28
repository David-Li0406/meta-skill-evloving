# 变异测试配置模板

各语言变异测试工具配置指南。

## 语言支持概览

| 语言 | 工具 | 成熟度 | 推荐指数 |
|------|------|--------|----------|
| JavaScript/TypeScript | **Stryker** | 高 | ⭐⭐⭐⭐⭐ |
| Python | **mutmut** | 高 | ⭐⭐⭐⭐⭐ |
| Java | **PIT** | 高 | ⭐⭐⭐⭐⭐ |
| C# (.NET) | **Stryker.NET** | 高 | ⭐⭐⭐⭐ |
| C/C++ | **Mull** | 中 | ⭐⭐⭐⭐ |
| Swift | **Muter** | 中 | ⭐⭐⭐⭐ |
| Go | **go-mutesting** | 中 | ⭐⭐⭐ |
| Rust | **cargo-mutants** | 中 | ⭐⭐⭐ |

---

## JavaScript/TypeScript (Stryker)

### 安装

```bash
# npm
npm install --save-dev @stryker-mutator/core @stryker-mutator/jest-runner

# Vitest 用户
npm install --save-dev @stryker-mutator/core @stryker-mutator/vitest-runner

# yarn
yarn add -D @stryker-mutator/core @stryker-mutator/jest-runner

# pnpm
pnpm add -D @stryker-mutator/core @stryker-mutator/jest-runner
```

### 配置文件

```javascript
// stryker.conf.js
module.exports = {
  // 要变异的文件
  mutate: [
    'src/**/*.ts',
    'src/**/*.tsx',
    '!src/**/*.test.ts',
    '!src/**/*.spec.ts',
    '!src/**/__tests__/**',
    '!src/**/*.d.ts',
  ],

  // 测试运行器 (jest | vitest | mocha | karma)
  testRunner: 'jest',
  jest: {
    configFile: 'jest.config.js',
  },

  // 报告器
  reporters: ['html', 'clear-text', 'progress', 'dashboard'],

  // 覆盖率分析模式
  coverageAnalysis: 'perTest',

  // 阈值设置
  thresholds: {
    high: 80,    // 高于此分数显示为绿色
    low: 60,     // 低于此分数显示为红色
    break: 50,   // 低于此分数构建失败
  },

  // 超时设置
  timeoutMS: 10000,
  timeoutFactor: 1.5,

  // 并发数
  concurrency: 4,

  // 增量模式
  incremental: true,
  incrementalFile: '.stryker-incremental.json',
};
```

### 运行命令

```bash
# 完整运行
npx stryker run

# 只对指定文件运行
npx stryker run --mutate "src/services/**/*.ts"

# 增量模式
npx stryker run --incremental

# 查看报告
open reports/mutation/html/index.html
```

---

## Python (mutmut)

### 安装

```bash
pip install mutmut
```

### 配置文件

```ini
# setup.cfg
[mutmut]
paths_to_mutate=src/
tests_dir=tests/
runner=pytest
```

或使用 `pyproject.toml`:

```toml
[tool.mutmut]
paths_to_mutate = "src/"
tests_dir = "tests/"
runner = "pytest"
```

### 运行命令

```bash
# 运行变异测试
mutmut run

# 查看结果摘要
mutmut results

# 查看详细 HTML 报告
mutmut html
open html/index.html

# 只对指定文件运行
mutmut run --paths-to-mutate=src/services/

# 查看存活的变异体
mutmut show <id>
```

---

## Java (PIT / pitest)

### Maven 配置

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <version>1.15.0</version>
    <dependencies>
        <!-- JUnit 5 支持 -->
        <dependency>
            <groupId>org.pitest</groupId>
            <artifactId>pitest-junit5-plugin</artifactId>
            <version>1.2.1</version>
        </dependency>
    </dependencies>
    <configuration>
        <!-- 目标类 -->
        <targetClasses>
            <param>com.example.service.*</param>
            <param>com.example.domain.*</param>
        </targetClasses>
        <!-- 目标测试 -->
        <targetTests>
            <param>com.example.*Test</param>
        </targetTests>
        <!-- 阈值 -->
        <mutationThreshold>80</mutationThreshold>
        <coverageThreshold>80</coverageThreshold>
        <!-- 输出格式 -->
        <outputFormats>
            <outputFormat>HTML</outputFormat>
            <outputFormat>XML</outputFormat>
        </outputFormats>
        <!-- 变异器 -->
        <mutators>
            <mutator>DEFAULTS</mutator>
        </mutators>
        <!-- 排除 -->
        <excludedClasses>
            <param>*Config</param>
            <param>*Application</param>
        </excludedClasses>
    </configuration>
</plugin>
```

### Gradle 配置

```groovy
// build.gradle
plugins {
    id 'info.solidsoft.pitest' version '1.15.0'
}

pitest {
    targetClasses = ['com.example.service.*', 'com.example.domain.*']
    targetTests = ['com.example.*Test']
    mutationThreshold = 80
    coverageThreshold = 80
    outputFormats = ['HTML', 'XML']
    timestampedReports = false
    junit5PluginVersion = '1.2.1'
}
```

### 运行命令

```bash
# Maven
mvn org.pitest:pitest-maven:mutationCoverage

# Gradle
./gradlew pitest

# 查看报告
open target/pit-reports/index.html
```

---

## C# / .NET (Stryker.NET)

### 安装

```bash
# 全局安装
dotnet tool install -g dotnet-stryker

# 项目安装
dotnet tool install dotnet-stryker
```

### 配置文件

```json
// stryker-config.json
{
  "stryker-config": {
    "project": "YourProject.csproj",
    "test-project": "YourProject.Tests.csproj",
    "mutate": [
      "**/*.cs",
      "!**/*Config.cs",
      "!**/Program.cs"
    ],
    "reporters": ["html", "progress", "dashboard"],
    "thresholds": {
      "high": 80,
      "low": 60,
      "break": 50
    },
    "concurrency": 4,
    "log-level": "info"
  }
}
```

### 运行命令

```bash
# 在测试项目目录运行
cd YourProject.Tests
dotnet stryker

# 使用配置文件
dotnet stryker -c stryker-config.json

# 查看报告
open StrykerOutput/reports/mutation-report.html
```

---

## C/C++ (Mull)

### 安装

```bash
# Ubuntu/Debian
sudo apt-get install mull

# macOS (Homebrew)
brew install mull-project/mull/mull-runner

# 从源码构建
git clone https://github.com/mull-project/mull.git
cd mull
mkdir build && cd build
cmake -G Ninja ..
ninja mull-runner
```

### 配置文件

```yaml
# mull.yml
mutators:
  # 算术运算符
  - cxx_add_to_sub        # + → -
  - cxx_sub_to_add        # - → +
  - cxx_mul_to_div        # * → /
  - cxx_div_to_mul        # / → *

  # 关系运算符
  - cxx_lt_to_le          # < → <=
  - cxx_le_to_lt          # <= → <
  - cxx_gt_to_ge          # > → >=
  - cxx_ge_to_gt          # >= → >

  # 相等运算符
  - cxx_eq_to_ne          # == → !=
  - cxx_ne_to_eq          # != → ==

  # 逻辑运算符
  - cxx_and_to_or         # && → ||
  - cxx_or_to_and         # || → &&

  # 移除语句
  - negate_mutator        # 条件取反
  - remove_void_call      # 删除 void 函数调用

# 排除路径
excludePaths:
  - ".*test.*"
  - ".*third_party.*"
  - ".*vendor.*"

# 超时
timeout: 10000
```

### 运行命令

```bash
# 基本用法（需要先用 clang 编译）
clang -fembed-bitcode -g -O0 main.c -o main
mull-runner ./main

# 使用配置文件
mull-runner --config mull.yml ./main

# CMake 项目集成
cmake -DCMAKE_C_FLAGS="-fembed-bitcode -g" \
      -DCMAKE_CXX_FLAGS="-fembed-bitcode -g" ..
make
mull-runner ./your_test_binary

# 生成报告
mull-runner --report-dir=./mull-report ./main
```

### CMake 集成

```cmake
# CMakeLists.txt
option(ENABLE_MULL "Enable Mull mutation testing" OFF)

if(ENABLE_MULL)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fembed-bitcode -g -O0")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fembed-bitcode -g -O0")
endif()
```

### 其他 C/C++ 工具

| 工具 | 特点 | 链接 |
|------|------|------|
| **Mull** | 基于 LLVM，最活跃 | [GitHub](https://github.com/mull-project/mull) |
| **Sentinel** | 支持 HTML/XML 报告 | [GitHub](https://github.com/shift-left-test/sentinel) |
| **MuCPP** | 支持 C++ 类变异 | [官网](https://ucase.uca.es/mucpp/) |
| **mutate_cpp** | Web 界面 | [GitHub](https://github.com/nlohmann/mutate_cpp) |

### 注意事项

```
C/C++ 变异测试注意:
- 需要使用 Clang 编译（GCC 不支持 -fembed-bitcode）
- 必须使用 -g（调试信息）和 -O0（无优化）
- 大型项目编译和测试时间较长
- 建议只对核心模块运行
```

---

## Swift (Muter)

### 安装

```bash
# Homebrew
brew install muter-mutation-testing/muter/muter

# Mint
mint install muter-mutation-testing/muter

# 从源码构建
git clone https://github.com/muter-mutation-testing/muter.git
cd muter
make install
```

### 配置文件

```yaml
# muter.conf.yml
xcodeproj: YourProject.xcodeproj
testSuiteTimeout: 300  # 秒

# 可选：指定 scheme
# scheme: YourScheme

# 可选：排除文件
exclude:
  - "**/*Tests*"
  - "**/*Mock*"
  - "**/AppDelegate.swift"
```

### 运行命令

```bash
# 初始化配置（首次使用）
muter init

# 运行变异测试
muter run

# 查看帮助
muter --help
```

### 支持的变异操作

| 变异器 | 说明 |
|--------|------|
| `RelationalOperatorReplacement` | `==` ↔ `!=`, `<` ↔ `>=` 等 |
| `RemoveSideEffects` | 删除函数调用 |
| `ChangeLogicalConnector` | `&&` ↔ `\|\|` |
| `SwapTernary` | 交换三元表达式分支 |

### 平台支持

- macOS 10.15+（必需）
- 支持 iOS、macOS、tvOS、watchOS 项目
- 需要 Xcode 和 xcodebuild

### 注意事项

```
Swift 变异测试注意:
- 仅支持 macOS 运行（需要 xcodebuild）
- 大型项目运行时间较长
- 建议在 CI 的 macOS runner 上运行
- Swift 5.9+ 兼容性更好
```

---

## Go (go-mutesting)

### 安装

```bash
go install github.com/zimmski/go-mutesting/cmd/go-mutesting@latest
```

### 运行命令

```bash
# 对包运行变异测试
go-mutesting ./...

# 对指定包运行
go-mutesting ./pkg/service/...

# 详细输出
go-mutesting -v ./...

# 使用自定义测试命令
go-mutesting --exec "go test -v" ./...
```

### 配置示例

```bash
# 排除测试文件
go-mutesting --blacklist "_test.go" ./...

# 只运行特定变异器
go-mutesting --mutator "expression/remove" ./...
```

### 注意事项

```
Go 变异测试局限性:
- 工具成熟度相对较低
- 大型项目运行较慢
- 建议只对核心模块运行
```

---

## Rust (cargo-mutants)

### 安装

```bash
cargo install cargo-mutants
```

### 运行命令

```bash
# 运行变异测试
cargo mutants

# 只对指定模块运行
cargo mutants --file src/lib.rs

# 使用多线程
cargo mutants --jobs 4

# 查看详细输出
cargo mutants -v

# 排除特定函数
cargo mutants --exclude "test_*"
```

### 配置文件

```toml
# .cargo/mutants.toml
[mutants]
# 排除文件
exclude_globs = [
    "**/tests/**",
    "**/benches/**",
]

# 排除函数
exclude_re = [
    "^test_",
    "^bench_",
]

# 超时（秒）
timeout = 300

# 并行作业数
jobs = 4
```

### 注意事项

```
Rust 变异测试注意:
- 编译时间较长，建议增量运行
- 泛型代码变异效果较差
- 建议配合 cargo test --release
```

---

## CI 集成

### GitHub Actions (多语言)

```yaml
# .github/workflows/mutation-test.yml
name: Mutation Testing

on:
  pull_request:
    branches: [main]

jobs:
  # JavaScript/TypeScript
  mutation-js:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci
      - run: npx stryker run
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: mutation-report-js
          path: reports/mutation/

  # Python
  mutation-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt mutmut
      - run: mutmut run --CI
      - run: mutmut html
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: mutation-report-python
          path: html/

  # Java
  mutation-java:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      - run: mvn org.pitest:pitest-maven:mutationCoverage
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: mutation-report-java
          path: target/pit-reports/

  # Go
  mutation-go:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version: '1.21'
      - run: go install github.com/zimmski/go-mutesting/cmd/go-mutesting@latest
      - run: go-mutesting ./...

  # Swift (需要 macOS runner)
  mutation-swift:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install Muter
        run: brew install muter-mutation-testing/muter/muter
      - name: Run Mutation Tests
        run: muter run
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: mutation-report-swift
          path: muter_logs/
```

---

## 分数解读

| 分数范围 | 评价 | 建议 |
|----------|------|------|
| ≥ 80% | 优秀 | 测试质量高，保持现状 |
| 60-80% | 良好 | 建议补充关键路径测试 |
| 40-60% | 一般 | 需要审查断言质量 |
| < 40% | 较差 | 测试可能形同虚设，需重构 |

---

## 常见问题

### 变异测试太慢？

1. **使用增量模式** - 只测试改动的代码
2. **减少并发** - 避免资源竞争
3. **排除非核心代码** - 配置、工具类等
4. **只在 PR 时运行** - 不要每次提交都跑
5. **分模块运行** - 拆分为多个 CI 任务

### 某些变异不合理？

```javascript
// JS: 注释排除
// Stryker disable next-line all
const DEBUG = true;
```

```java
// Java: 注解排除
@Generated  // PIT 自动跳过
public class Config {}
```

```python
# Python: pragma 排除
x = 1  # pragma: no mutate
```

### 如何选择工具？

| 场景 | 推荐 |
|------|------|
| 新项目 | 选择语言对应的首选工具 |
| CI 时间紧张 | 只对核心模块运行 |
| 大型单体项目 | 分模块、增量运行 |
| 微服务 | 每个服务独立配置 |
