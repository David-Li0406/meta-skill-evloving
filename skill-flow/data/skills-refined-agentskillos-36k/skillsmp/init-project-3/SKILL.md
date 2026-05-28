---
name: init-project
description: 初始化项目上下文。两步流程：codex exec 生成基础框架 + AI 润色补充。触发词：初始化项目、init、初始化上下文。
---

# Init Project Skill

当用户说"初始化项目"时，执行**两步流程**生成高质量的 `.cunzhi-memory/context.md`。

## ⚠️ 推荐流程：codex exec + AI 润色

### 第一步：codex exec 生成基础框架

```bash
# 1. 确保 .cunzhi-memory 目录存在
mkdir -p {项目路径}/.cunzhi-memory

# 2. 使用 codex exec 自动分析并生成基础框架
codex exec "Analyze this project and create a context.md file. Include:
1) Project overview (from README or config files)
2) Tech stack with versions (from package.json/Cargo.toml)
3) Key directories with descriptions
4) Common commands (from package.json scripts)
5) Code conventions (from lint/format configs)
6) Architecture overview

Write the result to {项目路径}/.cunzhi-memory/context.md in Chinese."
```

### 第二步：AI 读取并润色

AI 读取 codex exec 生成的内容，补充以下细节：

1. **项目特色描述**：用生动的语言描述项目用途（如"AI 对话早泄终结者"）
2. **精确版本号**：从配置文件读取具体版本（如 Rust 1.75、Vue 3.5）
3. **目录结构注释**：为每个目录添加详细说明
4. **当前进度**：从 sessions.md 或 notes.md 提取最近进度
5. **架构细节**：补充前后端交互、端口约定等

### 自动生效

生成完成后，下次对话会**自动加载** context.md 到上下文，无需手动确认。

---

## 备选方式：AI 完全手动分析

如果 codex exec 不可用，AI 可以手动执行以下步骤：

1. **分析项目结构**
   - 读取 `package.json`、`Cargo.toml`、`pyproject.toml` 等配置文件
   - 扫描目录结构，识别关键目录（src、bin、tests 等）
   - 识别框架和库（Vue、React、Tauri、Express 等）

2. **分析代码风格**
   - 检查 `.eslintrc`、`.prettierrc`、`rustfmt.toml` 等配置
   - 识别缩进风格、命名规范
   - 检查是否有 TypeScript、类型注解等

3. **生成详细上下文**
   - 项目描述（从 README 或配置文件提取）
   - 技术栈（具体版本号）
   - 常用命令（从 scripts 提取，附带说明）
   - 目录结构（带注释说明每个目录用途）
   - 代码规范（具体规则，不是空话）
   - 架构说明（前后端分离、微服务等）

4. **写入 context.md**
   - 将生成的内容写入 `.cunzhi-memory/context.md`
   - 调用 `zhi` 让用户确认

## 输出格式示例

```markdown
# {项目名} 项目上下文

{项目描述，从 README 或 package.json 提取}

## 技术栈

- **后端**: Rust 1.75 + Tauri 2.0
- **前端**: Vue 3.4 + Vite 5.0 + TypeScript
- **样式**: UnoCSS + Tailwind 兼容语法
- **状态管理**: Pinia
- **构建工具**: pnpm + cargo

## 常用命令

| 命令 | 说明 |
|------|------|
| `pnpm dev` | 启动开发服务器（Vite + Tauri） |
| `pnpm build` | 构建生产版本 |
| `cargo test` | 运行 Rust 单元测试 |

## 目录结构

```
项目名/
├── src/
│   ├── frontend/     # Vue 前端代码
│   │   ├── components/  # 可复用组件
│   │   └── views/       # 页面视图
│   └── rust/         # Rust 后端代码
│       ├── app/      # 应用逻辑
│       └── mcp/      # MCP 工具实现
├── bin/              # Python 脚本
└── .cunzhi-memory/   # 项目记忆
```

## 代码规范

- **命名**: 
  - Rust: snake_case 函数/变量，PascalCase 类型
  - TypeScript: camelCase 函数/变量，PascalCase 组件
- **缩进**: 4 空格（Rust），2 空格（前端）
- **提交**: `feat:`, `fix:`, `docs:`, `refactor:` 前缀

## 架构说明

Tauri 桌面应用，前后端分离：
- 前端通过 Tauri IPC 调用后端命令
- 后端提供 MCP 工具供 AI 调用
- 支持多端口并行运行

## 当前进度

{从 sessions.md 或 notes.md 提取最近进度}
```

## 注意事项

- 不要生成空洞的描述，要具体
- 版本号要从配置文件读取
- 目录结构要带注释说明用途
- 代码规范要具体到命名、缩进等细节
