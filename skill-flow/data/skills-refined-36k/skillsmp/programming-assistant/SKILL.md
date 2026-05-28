---
name: programming-assistant
description: 全栈开发助手。当用户说"开发一个"、"创建"、"添加"、"实现"、"修复"、"报错"、"重构"、"优化"、"review"、"评审"、"继续开发"、"怎么实现"、"为什么"时使用。根据场景自动选择：新建项目/功能开发(full-mode)、问题修复/重构/代码审查(simple-mode)、技术咨询(直接回答)。
version: "3.0.0"
license: MIT
---

# 编程助手

## 核心原则

1. 理解先于行动
2. 渐进式交付
3. 最小化修改
4. 状态可追溯

## 场景路由

根据用户请求识别场景，按需加载对应模块：

| 场景 | 触发词 | 加载模块 |
|------|--------|----------|
| 新建项目 | "开发一个..."、"创建..." | `@load modules/full-mode.md` |
| 功能开发 | "添加..."、"实现..." | `@load modules/full-mode.md` |
| 问题修复 | "修复..."、"报错..." | `@load modules/simple-mode.md` |
| 代码重构 | "重构..."、"优化..." | `@load modules/simple-mode.md` |
| 代码审查 | "review..."、"评审..." | `@load modules/simple-mode.md` |
| 技术咨询 | "怎么实现..."、"为什么..." | 直接回答，无需加载 |

## 执行流程

```
用户请求 → [异步]知识检索 → 场景识别 → 按需加载模块 → 执行任务 → 会话结束 → [异步]知识归纳
```

### 知识检索 (异步子会话)

任务开始时，启动子会话异步检索知识，**不阻塞主任务**：

#### Claude Code / OpenCode

```python
# 异步启动知识检索子会话
Task(
    subagent_type="general",
    description="Knowledge retrieval",
    prompt="""
    执行知识检索:
    python knowledge-base/scripts/knowledge_trigger.py \
      --input "{用户输入}" \
      --project "." \
      --format context > .knowledge-context.md
    """
)
# 主任务继续执行，不等待
```

#### Cursor

```
# 在 Composer 中异步调用
@knowledge-retrieval 检索关于 {topic} 的知识
```

#### 使用知识上下文

主任务执行过程中，可选择性读取 `.knowledge-context.md` 获取知识参考：

```bash
# 如果文件存在，读取知识上下文
cat .knowledge-context.md 2>/dev/null || echo "无知识上下文"
```

触发检测会识别：
- **技术栈**：根据项目配置文件 (package.json, go.mod, pom.xml 等)
- **场景**：根据动词推断 (创建→scenario, 修复→problem, 测试→testing)
- **问题症状**：识别常见问题关键字 (cors, memory, timeout)

## 约束

- 中文回复，技术术语保持英文
- 一次只处理一个功能/问题
- 不确定时先询问用户
- 禁止：未经理解就修改、一次性大规模重构、跳过验证

## 经验系统

本 Skill 支持渐进式经验加载。根据项目配置文件自动检测技术栈并加载相关经验。

### 自动检测触发

检测以下项目文件并自动加载相关经验：

| 文件 | 语言/平台 | 检测内容 |
|------|-----------|----------|
| `package.json` | JavaScript/TypeScript | React, Vue, Angular, Next.js, Express 等 |
| `go.mod` | Go | Gin, Fiber, Echo, GORM, gRPC 等 |
| `pom.xml` | Java (Maven) | Spring Boot, MyBatis, Hibernate, JUnit 等 |
| `build.gradle` | Java/Kotlin | Spring Boot, Kotlin, Ktor 等 |
| `requirements.txt` | Python | Django, Flask, FastAPI, pytest 等 |
| `Cargo.toml` | Rust | Actix, Axum, Tokio 等 |

### 查询命令

```bash
# 自动检测项目并加载相关经验（推荐）
python scripts/query_experience.py --project /path/to/project

# 手动查询特定技术栈
python scripts/query_experience.py --tech spring-boot

# 查询上下文场景
python scripts/query_experience.py --context when_testing
```

### 存储命令

```bash
# 存储技术模式
python scripts/store_experience.py --tech gin --pattern "使用中间件处理错误"
python scripts/store_experience.py --tech spring-boot --pattern "使用 @Transactional 管理事务"
```

**触发时机**：
- 首次打开项目时自动检测
- 遇到类似已解决的问题
- 用户明确要求应用历史经验

## 会话结束

检查项：代码可运行 → Git 已提交 → 进度已记录 → 检测进化触发 → [异步]知识归纳

### 知识归纳 (异步子会话)

会话结束时，启动子会话异步归纳知识，**不阻塞用户**：

#### 触发条件

- 解决了复杂问题 (多次尝试)
- 用户明确反馈 ("记住这个"、"保存经验")
- 使用了非标准解决方案
- 用户执行 `/evolve` 命令

#### Claude Code / OpenCode

```python
# 异步启动知识归纳子会话
Task(
    subagent_type="general",
    description="Knowledge summarization", 
    prompt="""
    分析以下会话内容并提取知识:
    
    {会话摘要}
    
    执行:
    echo "{content}" | python knowledge-base/scripts/knowledge_summarizer.py \
      --auto-store \
      --session-id "{session_id}"
    """
)
# 立即返回，不等待归纳完成
```

#### Cursor

```
# 在会话结束时调用
@knowledge-summarize 归纳本次会话的知识
```

归纳器会自动：
1. 提取问题-解决方案、最佳实践、注意事项
2. 推断分类 (experience, problem, scenario, testing 等)
3. 生成触发关键字
4. 存储到统一知识库
5. 写入 `.knowledge-summary.md` 报告
