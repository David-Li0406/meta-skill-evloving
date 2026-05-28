# /ohspec:init-context - 项目上下文初始化

## 命令说明
生成项目上下文文件，解决大型项目首次扫描慢的问题。通过预制项目结构、关键模块和编码规范，加速后续需求分析阶段。

## 使用方式
```bash
/ohspec:init-context
```

## 工作流程

### 步骤1：扫描代码库结构
使用代码扫描工具收集项目信息：

**1.1 识别项目元信息**
```bash
# 项目名称（从 package.json、pom.xml、Cargo.toml 等）
# 技术栈（语言、框架、主要依赖）
# 版本信息
```

**1.2 扫描目录结构**
使用 Glob 工具扫描关键目录：
- 源代码目录（src/、lib/、app/ 等）
- 测试目录（test/、tests/、__tests__/ 等）
- 配置目录（config/、conf/、configs/ 等）
- 文档目录（docs/、doc/、documentation/ 等）

**1.3 识别关键模块**
使用 Grep 工具搜索：
- 主要类/接口定义（class、interface、struct、trait 等）
- 主要函数/方法（public、export、def 等）
- API 端点（@RestController、@app.route、express.Router 等）
- 配置入口（config、settings、environment 等）

**1.4 分析依赖关系**
读取依赖配置文件：
- package.json / package-lock.json（Node.js）
- pom.xml / build.gradle（Java）
- requirements.txt / Pipfile（Python）
- Cargo.toml（Rust）
- go.mod（Go）

### 步骤2：生成初始上下文文件
使用 templates/project-context.md 模板生成 `.claude/project-context.md`：

**2.1 填充元信息章节**
```yaml
元信息:
  项目名称: [从配置文件提取]
  技术栈:
    语言: [主要编程语言]
    框架: [主要框架列表]
    依赖: [关键依赖列表]
  最后更新: [YYYY-MM-DD]
```

**2.2 填充架构概览章节**
基于扫描结果生成模块列表：
```markdown
## 架构概览

### 模块划分
| 模块名 | 路径 | 职责 | 关键接口 |
|-------|------|------|---------|
| [模块1] | src/xxx | [职责描述] | [接口列表] |
| [模块2] | src/yyy | [职责描述] | [接口列表] |
```

**2.3 填充关键文件索引**
列出最常访问的文件（基于文件大小、修改频率、依赖关系）：
```markdown
## 关键文件索引

### 配置文件
- config/app.config.ts - 应用配置入口
- config/database.config.ts - 数据库配置

### 核心模块
- src/core/engine.ts - 核心引擎
- src/utils/helper.ts - 工具函数集
```

### 步骤3：智能推断编码规范
通过分析现有代码推断项目约定：

**3.1 命名约定**
- 文件命名：kebab-case / snake_case / PascalCase
- 变量命名：camelCase / snake_case
- 常量命名：UPPER_SNAKE_CASE / camelCase
- 类命名：PascalCase
- 函数命名：camelCase / snake_case

**3.2 文件组织**
- 单一职责：每个文件/模块只负责一个功能
- 目录结构：按功能划分 / 按类型划分
- 导入顺序：外部依赖 → 内部模块 → 类型定义 → 样式

**3.3 注释规范**
- 文档注释：JSDoc / Docstring / Rustdoc
- 行内注释：// / # / /* */
- TODO 标记：TODO / FIXME / NOTE

### 步骤4：用户审查和补充
将生成的 project-context.md 展示给用户：

```markdown
项目上下文文件已生成：`.claude/project-context.md`

请审查以下内容：

## 已自动识别
✅ 项目元信息（名称、技术栈）
✅ 模块划分（X 个模块）
✅ 关键文件索引（Y 个文件）
✅ 编码规范（命名约定、文件组织）

## 需要补充（可选）
- [ ] 业务领域说明（核心领域、子领域）
- [ ] 技术约束（性能要求、并发模型）
- [ ] 测试策略（单元测试、集成测试）
- [ ] 常见模式（错误处理、配置管理）

你可以直接编辑 `.claude/project-context.md` 补充业务相关信息。
```

### 步骤5：更新配置状态
在 config.yaml 中标记上下文已初始化：
```yaml
project_context:
  enabled: true
  initialized: true
  last_update: [YYYY-MM-DD]
```

## 输出物
- `.claude/project-context.md` - 项目上下文文件

## 后续使用
需求分析师在启动时会自动读取此文件（参见 analyst.md 阶段0）：
1. 跳过重复的代码结构扫描
2. 直接加载模块信息和编码规范
3. 仅扫描与需求相关的特定模块

## 更新机制
当项目结构发生重大变化时，重新运行 `/ohspec:init-context` 更新上下文文件。

触发更新的情况：
- 新增/删除主要模块
- 技术栈升级（框架版本、依赖变更）
- 架构重构（模块职责调整）
- 编码规范变更

## 注意事项
- 初次生成可能需要 1-2 分钟（取决于项目大小）
- 生成的上下文文件可编辑，建议纳入版本控制
- 不要在上下文文件中包含敏感信息（密钥、密码等）
- 业务领域信息需要人工补充，AI 无法自动推断
