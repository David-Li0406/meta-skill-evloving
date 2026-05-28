# 编程助手 Skill - 使用指南


## 概述

这是一个专业的编程助手skill，基于ZhiSi Architect方法论，支持全栈开发和架构设计。该skill集成了Context7、sequential-thinking等MCP工具，能够在 **OpenCode**、**Claude Code** 和 **Cursor** 中使用。

## 核心特性

### 全栈开发支持
- **前端**: React, Vue, Angular, TypeScript
- **后端**: Golang, Python, Node.js, Java
- **数据库**: PostgreSQL, MySQL, MongoDB, Redis
- **云服务**:
  - **私有云**: Docker, Docker Compose, Kubernetes
  - **公有云/混合云**: 腾讯云、阿里云、华为云为主，AWS/Azure/Google Cloud为补充
- **DevOps**:
  - **CI/CD**: 适配私有云和公有云/混合云两类场景

### MCP工具集成
- **Context7**: 获取最新文档和代码示例
- **sequential-thinking**: 深度分析和问题拆解

## 快速开始

### 一键安装（推荐）

```bash
# 完整安装（OpenCode + Claude Code + Cursor + MCP）
./install.sh --all --with-mcp
```

这将自动：
1. ✅ 安装到 OpenCode（全局 skill）
2. ✅ 安装到 Claude Code（全局 skill）
3. ✅ 安装到 Cursor（全局规则）
4. ✅ 配置 MCP 服务器（context7, sequential-thinking）
5. ✅ 验证安装结果

**完成后重启相应的 IDE/CLI 即可使用！**

### OpenCode 用户

```bash
./install.sh --opencode --with-mcp
```

安装到: `~/.config/opencode/skill/programming-assistant/SKILL.md`

### Claude Code 用户

```bash
./install.sh --claude-code
```

安装到: `~/.claude/skills/programming-assistant/SKILL.md`

### Cursor 用户

```bash
./install.sh --cursor --with-mcp
```

安装到: `~/.cursor/rules/programming-assistant.md`

### 详细文档

- **快速开始**: [QUICK-START.md](QUICK-START.md)
- **Skill 详细说明**: [SKILL.md](SKILL.md)
- **MCP 安装详解**: [MCP-INSTALL.md](MCP-INSTALL.md)
- **OpenCode 配置**: [OpenCode Skills 官方文档](https://opencode.ai/docs/skills/)
- **OpenCode MCP 文档**: [OpenCode MCP 服务器文档](https://opencode.ai/docs/mcp-servers/)
- **Claude Code 配置**: [Claude Code Skills 官方文档](https://docs.anthropic.com/en/docs/claude-code/skills)


## 工作流程

### 项目初始化
```
输入: 新项目需求
流程:
  1. 读取项目根目录的 SOLUTION.md 和 TASK.md（如果存在）
  2. 如果文件不存在：
     - 使用 sequential-thinking MCP 分析需求
     - 生成 SOLUTION.md 架构文档
     - 将 SOLUTION.md 拆解成 TASK.md 任务列表（包含实现步骤、技术选型、代码片段）
  3. 将 TASK.md 转化为 feature_list.json（只包含任务基本信息和状态）
  4. 理解架构设计和技术选型
  5. 检查 README.md，不存在则创建
  6. 创建 progress.txt
  7. 初始化 git 仓库
输出: 项目初始化完成，准备开发
```

### 需求分析
```
输入: 用户功能需求
流程:
  1. 深入理解需求，从用户角度思考
  2. 使用 sequential-thinking 分析需求完整性
  3. 识别缺失需求或缺口，与用户讨论完善
  4. 选择最简单的解决方案，避免过度工程化
输出: 需求确认和技术方案
```

### 代码实现
```
输入: 确认的需求和方案
流程:
  1. 按 TASK.md 顺序执行任务
  2. 每次只完成一个任务
  3. 使用 Context7 查询最新文档和示例
  4. 编写符合规范的代码（精确、模块化、可测试）
  5. 运行测试验证功能
  6. 确认不破坏现有功能
输出: 可测试的代码单元
```
### 问题解决
```
输入: 用户反馈的问题或错误
流程:
  1. 彻底审查相关代码
  2. 使用 sequential-thinking 深度分析
  3. 使用 Context7 查询相关文档和最佳实践
  4. 提出多个解决方案，使用决策树评估
  5. 选择最优方案并实施
  6. 最小化修改，确保不破坏现有功能
  7. 测试验证修复效果
输出: 问题解决和修复代码
```

## 使用示例

### 示例1: 新项目初始化

**用户输入**:
```
帮我开发一个电商系统，功能包括：
- 商品浏览和搜索
- 购物车和订单管理
- 用户注册和登录
- 支付集成

前端使用Vue.js，后端使用Golang 1.22+，数据库使用PostgreSQL。
```

**助手会自动**:
1. 检查 SOLUTION.md 和 TASK.md 是否存在
2. 如果不存在：
   - 使用 sequential-thinking MCP 分析需求
   - 生成 SOLUTION.md 架构文档
   - 将 SOLUTION.md 拆解成 TASK.md 任务列表
3. 创建 progress.txt 和 feature_list.json
4. 创建项目目录结构
5. 初始化配置文件
6. 初始化 git 仓库并首次提交

### 示例2: 功能实现

**用户输入**:
```
实现用户登录功能
```

**助手会自动**:
1. 读取 SOLUTION.md 和 TASK.md
2. 使用 Context7 查询JWT最佳实践
3. 设计登录API接口
4. 实现后端认证逻辑
5. 实现前端登录组件
6. 编写测试用例
7. 运行测试验证

### 示例3: 问题修复

**用户输入**:
```
登录后session过期太快，怎么调整？
```

**助手会自动**:
1. 审查认证相关代码
2. 使用 sequential-thinking 分析原因
3. 使用 Context7 查询session配置最佳实践
4. 提出调整session过期时间的方案
5. 实施修改
6. 测试验证效果

## 代码规范

### 必须遵守
1. 用最少的代码完成任务
2. 代码必须精确、模块化、可测试
3. 始终考虑安全性
4. 优化代码性能
5. 每完成一个任务就进行测试

### 代码风格
- 不使用emoji
- 减少代码注释，仅必要时编写
- 遵循现有代码库的规范和风格
- 保持代码清晰性和可维护性

### 文档规范
- 减少文档数量
- 仅保留主要文档：README.md, SOLUTION.md, TASK.md, DEPLOYMENT.md
- 使用简体中文编写文档
- 技术术语保持英文原样

## 响应规则

### 语言规则
- **必须使用简体中文回复**（最高优先级）
- 技术术语使用英文原样（API, React, Vue 等）
- 产品名称、品牌名使用英文原样
- 代码片段、命令使用英文原样

### 沟通风格
- **简洁直接**: 不废话，直接开始工作
- **无奉承**: 不使用"好问题"、"太棒了"等
- **无状态汇报**: 不说"我正在..."、"让我开始..."
- **使用todo**: 用todo工具跟踪进度，不要口头汇报
- **匹配用户**: 用户简洁则简洁，需要细节则提供细节

## 工具使用优先级

```
1. 需求分析
   ↓ sequential-thinking (深度分析)

2. 技术调研
   ↓ Context7 (文档查询)
   ↓ grep/Grep (代码搜索)

3. 代码实现
   ↓ Read/Write/Edit (文件操作)
   ↓ lsp_* (LSP工具)
   ↓ Bash (命令执行)

4. 测试验证
   ↓ Bash (运行测试)
   ↓ lsp_diagnostics (代码检查)

5. 用户交互
   ↓ todoread (获取反馈)
   ↓ todowrite (进度跟踪)
```

## 质量保证

### 代码质量
- 使用 LSP 工具进行代码检查
- 运行构建命令确保编译通过
- 执行测试用例验证功能
- 检查类型错误和警告

### 测试策略
- 编写单元测试覆盖核心逻辑
- 编写集成测试验证模块交互
- 每完成一个任务立即测试
- 确保测试通过后再继续下一个任务

### 安全检查
- 验证用户输入
- 防止SQL注入、XSS等常见漏洞
- 使用HTTPS和加密传输
- 遵循最小权限原则

## 最佳实践

1. **理解优于实施**: 先彻底理解需求，再动手实现
2. **测试驱动**: 每完成一个单元立即测试
3. **最小修改**: 每次改动尽可能小，降低风险
4. **持续反馈**: 与用户保持沟通，及时调整方向
5. **文档同步**: 代码和文档保持同步更新
6. **安全第一**: 始终考虑安全性和数据保护
7. **性能优化**: 在保证功能的前提下优化性能

## 故障恢复

### 修复失败时的处理
1. 修复根本原因，而非症状
2. 每次修复后重新验证
3. 不进行随机调试（shotgun debugging）

### 连续失败处理（3次以上）
1. 停止所有编辑
2. 回滚到最后已知的工作状态
3. 记录所有尝试和失败原因
4. 向用户报告问题，寻求指导

## 版本历史

### v1.3.0 (2025-01-16)
- 添加自动 MCP 配置功能
- 支持 OpenCode 的 MCP 配置（~/.config/opencode/opencode.json）
- 支持 Cursor 的 MCP 配置（~/.cursor/mcp.json）
- 智能合并配置,不覆盖现有配置
- 自动备份原配置文件
- 添加 MCP 配置验证功能
- 创建详细的 MCP 安装文档（MCP-INSTALL.md）
- 修正安装脚本参数为 --with-mcp

### v1.2.1 (2025-01-16)
- 修复OpenCode skill未生效问题 - triggers字段已在metadata中
- 添加command目录复制到OpenCode和Claude Code安装路径
- 为Cursor创建兼容版本 - 移除YAML frontmatter
- 添加MCP工具检查和降级机制 - 未安装时跳过MCP配置
- 修复install.sh安装逻辑

### v1.2.0 (2025-01-15)
- 统一版本号管理，创建 VERSION 文件作为单一版本源
- 优化文档结构，明确各文档职责
- 创建 MCP-SERVERS.md 统一 MCP 配置文档
- 创建 DOCS-STRUCTURE.md 说明文档结构
- 修复版本不一致问题
- 改进 MCP 配置管理

### v1.1.0 (2025-01-13)
- 添加 Claude Code 支持
- 添加渐进式工作流程
- 双代理策略（初始化代理 + 编码代理）
- 三大关键文件（progress.txt, feature_list.json, git history）
- 黄金法则（干净状态）
- 修复 OpenCode 安装路径（统一使用 `~/.config/opencode/skill/`）
- 修复 Cursor 安装路径（使用正确的 `~/.cursor/rules/` 路径）
- 统一 install.sh 和 uninstall.sh 的路径定义
- 自动检测 OpenCode、Claude Code、Cursor 安装

### v1.0.0 (2025-01-13)
- 初始版本发布
- 基于ZhiSi Architect方法论
- 集成Context7、sequential-thinking、mcp-feedback-enhanced MCP服务器
- 支持OpenCode和Cursor平台

## 贡献

欢迎提出改进建议和问题反馈！

## 许可

本skill基于ZhiSi Architect方法论创建，可自由使用和修改。

---

