# 项目上下文
<!--
  WHAT: 项目级上下文文件 - 预制的代码库结构和编码规范
  WHY: 解决大型项目首次扫描慢的问题，加速需求分析阶段
  WHEN: 由 /ohspec:init-context 生成，需求分析师自动加载
-->

> 项目: [项目名称]
> 最后更新: [YYYY-MM-DD]

---

## 1. 元信息

### 项目基本信息
```yaml
项目名称: [项目名称]
项目描述: [一句话描述项目功能]
代码库路径: [项目根目录路径]
```

### 技术栈
```yaml
语言:
  - [主要语言] ([版本])
  - [次要语言] ([版本])

框架:
  - [框架1] ([版本]) - [用途]
  - [框架2] ([版本]) - [用途]

关键依赖:
  - [依赖1] ([版本]) - [用途]
  - [依赖2] ([版本]) - [用途]

构建工具:
  - [构建工具] ([版本])

测试框架:
  - [测试框架] ([版本])
```

---

## 2. 业务领域

### 核心领域
<!-- 项目的主要业务领域，需要人工补充 -->
- [领域1]: [描述]
- [领域2]: [描述]

### 子领域
<!-- 细分的业务子领域 -->
| 子领域 | 职责 | 关键概念 |
|-------|------|---------|
| [子领域1] | [职责描述] | [概念1, 概念2] |
| [子领域2] | [职责描述] | [概念1, 概念2] |

### 业务边界
<!-- 明确不属于本项目的范围 -->
- ❌ [不支持的场景1]
- ❌ [不支持的场景2]

---

## 3. 架构概览

### 模块划分
| 模块名 | 路径 | 职责 | 关键接口 |
|-------|------|------|---------|
| [模块1] | src/xxx | [职责描述] | [接口1, 接口2] |
| [模块2] | src/yyy | [职责描述] | [接口1, 接口2] |

### 关键接口
<!-- 最常使用的公共接口 -->
```typescript
// 示例（根据实际语言调整）
interface [接口名] {
  [方法1]([参数]): [返回值]
  [方法2]([参数]): [返回值]
}
```

### 依赖关系
<!-- 模块间依赖关系 -->
```
[模块A] → [模块B] → [模块C]
         ↘ [模块D]
```

### 数据流
<!-- 关键数据流向 -->
```
[数据源] → [处理模块] → [存储/输出]
```

---

## 4. 技术约束

### 性能要求
```yaml
延迟:
  - p50: [X ms]
  - p99: [Y ms]

吞吐量:
  - QPS: [N]
  - TPS: [M]

资源限制:
  - 内存: [X MB/GB]
  - CPU: [核心数]
  - 磁盘: [容量]
```

### 并发模型
- 并发策略: [单线程/多线程/协程/Actor/无锁]
- 线程池配置: [大小、队列长度]
- 锁策略: [悲观锁/乐观锁/读写锁]

### 资源限制
- 最大连接数: [N]
- 超时配置: [连接超时、读写超时]
- 重试策略: [次数、间隔、退避算法]

---

## 5. 编码规范

### 命名约定
```yaml
文件命名: [kebab-case | snake_case | PascalCase]
示例: user-service.ts | user_service.py | UserService.java

变量命名: [camelCase | snake_case]
示例: userName | user_name

常量命名: [UPPER_SNAKE_CASE | camelCase]
示例: MAX_RETRY_COUNT | maxRetryCount

类命名: [PascalCase]
示例: UserService

函数命名: [camelCase | snake_case]
示例: getUserById | get_user_by_id

接口命名: [PascalCase + I前缀 | PascalCase]
示例: IUserService | UserService

类型别名: [PascalCase + Type后缀 | PascalCase]
示例: UserDataType | UserData
```

### 文件组织
```yaml
目录结构: [按功能划分 | 按类型划分]

单文件职责: 每个文件只负责一个功能模块

导入顺序:
  1. 外部依赖（第三方库）
  2. 内部模块（相对路径导入）
  3. 类型定义（.d.ts / types）
  4. 样式文件（如适用）

示例:
  # 外部依赖
  import express from 'express';
  import { Injectable } from '@nestjs/common';

  # 内部模块
  import { UserService } from './user.service';
  import { validateInput } from '../utils/validator';

  # 类型定义
  import type { UserDTO } from './types';
```

### 注释规范
```yaml
文档注释: [JSDoc | Docstring | Rustdoc | Javadoc]
位置: 函数/类/接口定义之前

行内注释: [// | # | /* */]
用途: 解释复杂逻辑、非显而易见的设计决策

TODO 标记:
  - TODO: 待完成的功能
  - FIXME: 需要修复的问题
  - NOTE: 重要说明
  - HACK: 临时方案
  - XXX: 需要重构的代码

示例（TypeScript）:
  /**
   * 获取用户信息
   * @param userId 用户 ID
   * @param options 查询选项
   * @returns 用户信息对象
   * @throws UserNotFoundException 用户不存在时抛出
   */
  async getUserById(userId: string, options?: QueryOptions): Promise<User> {
    // TODO: 添加缓存支持
    return this.userRepository.findById(userId);
  }
```

### 代码风格
```yaml
缩进: [2 spaces | 4 spaces | 1 tab]
行宽: [80 | 100 | 120] 字符
括号风格: [K&R | Allman | Stroustrup]
分号: [required | optional]
引号: [single | double]
尾逗号: [always | never | multiline]
```

---

## 6. 测试策略

### 单元测试
```yaml
测试框架: [Jest | Mocha | PyTest | JUnit]
覆盖率要求: [80% | 90%]

测试文件命名: [*.test.ts | *.spec.ts | *_test.py]
测试文件位置: [与源文件同目录 | 独立 test/ 目录]

断言库: [expect | assert | should]

Mock 工具: [sinon | jest.mock | unittest.mock]
```

### 集成测试
```yaml
测试范围: [API 端到端 | 模块集成]
测试环境: [本地 | Docker | 测试服务器]
测试数据: [Mock 数据 | 测试数据库]
```

### 性能测试
```yaml
工具: [k6 | JMeter | Locust]
指标: [延迟 | 吞吐量 | 资源占用]
基准: [p99 < X ms | QPS > Y]
```

---

## 7. 常见模式

### 错误处理
```yaml
策略: [异常捕获 | 错误码 | Result/Option 类型]

示例:
  try {
    const result = await riskyOperation();
    return result;
  } catch (error) {
    logger.error('操作失败', { error, context });
    throw new CustomError('操作失败', { cause: error });
  }
```

### 配置管理
```yaml
配置来源: [环境变量 | 配置文件 | 配置中心]
配置文件格式: [YAML | JSON | TOML | .env]
配置文件路径: [config/ | conf/ | .env]

优先级: 环境变量 > 配置文件 > 默认值
```

### 日志规范
```yaml
日志级别: [DEBUG | INFO | WARN | ERROR | FATAL]
日志格式: [JSON | 文本]

日志内容:
  - 时间戳（ISO 8601）
  - 日志级别
  - 模块名称
  - 消息
  - 上下文（关键字段）
  - 错误堆栈（如适用）

PII 脱敏: 用户 ID、手机号、邮箱等敏感信息需脱敏
```

### 并发控制
```yaml
模式: [互斥锁 | 读写锁 | 信号量 | 无锁队列]
使用场景: [共享资源保护 | 限流 | 任务队列]
```

---

## 8. 关键文件索引

### 配置文件
| 文件路径 | 用途 |
|---------|------|
| config/app.config.ts | 应用配置入口 |
| config/database.config.ts | 数据库配置 |
| .env | 环境变量 |

### 核心模块
| 文件路径 | 职责 | 关键接口 |
|---------|------|---------|
| src/core/engine.ts | 核心引擎 | Engine.start(), Engine.stop() |
| src/utils/helper.ts | 工具函数集 | formatDate(), validateEmail() |

### 接口定义
| 文件路径 | 接口类型 |
|---------|---------|
| src/types/user.d.ts | 用户相关类型定义 |
| src/types/api.d.ts | API 请求/响应类型 |

### 测试文件
| 文件路径 | 测试类型 |
|---------|---------|
| tests/unit/ | 单元测试 |
| tests/integration/ | 集成测试 |
| tests/e2e/ | 端到端测试 |

---

## 9. 依赖关系图

### 外部依赖
```
[项目] → [框架A] → [底层库B]
       → [框架C]
```

### 内部模块依赖
```
[应用层] → [业务逻辑层] → [数据访问层] → [数据库]
         ↘ [工具层]
```

---

## 10. 更新日志

### [YYYY-MM-DD] - 初始化
- 创建项目上下文文件
- 自动扫描代码库结构
- 生成模块划分和关键文件索引

### [YYYY-MM-DD] - 补充业务信息
- 添加核心业务领域说明
- 补充技术约束和性能要求

---

<!--
  维护提示：
  - 当项目结构发生重大变化时，运行 /ohspec:init-context 更新
  - 业务领域信息需要人工维护
  - 建议将此文件纳入版本控制
  - 不要在此文件中包含敏感信息
-->
