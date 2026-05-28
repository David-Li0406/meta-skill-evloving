# AI 助手技能安装目录配置

此文件定义了各个 AI 助手支持的技能安装目录位置。

## Codex (OpenAI)

文档: https://developers.openai.com/codex/skills/

### 支持的作用域

| 作用域 | 目录路径 | 说明 |
|--------|---------|------|
| `global` | `~/.codex/skills` | 用户全局技能 |
| `project` | `$CWD/.codex/skills` | 当前工作目录技能 |
| `project-parent` | `$CWD/../.codex/skills` | 父目录技能（Git 仓库内） |
| `project-root` | `$REPO_ROOT/.codex/skills` | Git 仓库根目录技能 |
| `admin` | `/etc/codex/skills` | 系统级技能 |

**优先级**: `project` > `project-parent` > `project-root` > `global` > `admin` > `system`

## Roo Code

文档: https://docs.roocode.com/features/skills

### 支持的作用域

| 作用域 | 目录路径 | 说明 |
|--------|---------|------|
| `global` | `~/.roo/skills` (macOS/Linux)<br>`%USERPROFILE%\.roo\skills` (Windows) | 用户全局技能 |
| `project` | `.roo/skills` | 项目技能 |
| `global-mode` | `~/.roo/skills-{mode}` | 全局模式特定技能 |
| `project-mode` | `.roo/skills-{mode}` | 项目模式特定技能 |

**优先级**: `project-mode` > `project` > `global-mode` > `global`

**模式示例**: `code`, `architect`, `debug` 等

## Claude Code

文档: https://code.claude.com/docs/en/skills

### 支持的作用域

| 作用域 | 目录路径 | 说明 |
|--------|---------|------|
| `enterprise` | 由企业管理设置决定 | 企业级技能 |
| `global` | `~/.claude/skills` | 用户全局技能 |
| `project` | `.claude/skills` | 项目技能 |
| `plugin` | 由插件提供 | 插件捆绑技能 |

**优先级**: `enterprise` > `global` > `project` > `plugin`

## VS Code Copilot

文档: https://code.visualstudio.com/docs/copilot/customization/agent-skills

### 支持的作用域

| 作用域 | 目录路径 | 说明 |
|--------|---------|------|
| `global` | `~/.copilot/skills` | 用户全局技能（推荐） |
| `global-legacy` | `~/.claude/skills` | 用户全局技能（兼容） |
| `project` | `.github/skills` | 项目技能（推荐） |
| `project-legacy` | `.claude/skills` | 项目技能（兼容） |

**优先级**: `project` > `project-legacy` > `global` > `global-legacy`

## Cursor

文档: https://cursor.com/cn/docs/context/skills

### 支持的作用域

| 作用域 | 目录路径 | 说明 |
|--------|---------|------|
| `global` | `~/.cursor/skills` | 用户全局技能 |
| `project` | `.cursor/skills` | 项目技能 |

**优先级**: `project` > `global`

## KiloCode

文档: https://kilo.ai/docs/agent-behavior/skills

### 支持的作用域

| 作用域 | 目录路径 | 说明 |
|--------|---------|------|
| `global` | `~/.kilocode/skills` (macOS/Linux)<br>`%USERPROFILE%\.kilocode\skills` (Windows) | 用户全局技能 |
| `project` | `.kilocode/skills` | 项目技能 |
| `global-mode` | `~/.kilocode/skills-{mode}` | 全局模式特定技能 |
| `project-mode` | `.kilocode/skills-{mode}` | 项目模式特定技能 |

**优先级**: `project-mode` > `project` > `global-mode` > `global`

**模式示例**: `code`, `architect` 等

## 通用说明

### 路径变量

- `~`: 用户主目录
- `$CWD`: 当前工作目录
- `$REPO_ROOT`: Git 仓库根目录
- `%USERPROFILE%`: Windows 用户目录

### 技能目录结构

所有 AI 助手都遵循相同的技能目录结构：

```
{skills-directory}/
└── {skill-name}/
    ├── SKILL.md          # 必需：技能定义文件
    ├── scripts/          # 可选：脚本文件
    ├── references/       # 可选：参考文档
    └── assets/           # 可选：资源文件
```

### 使用建议

1. **个人技能**: 使用 `global` 作用域
2. **团队共享**: 使用 `project` 作用域并提交到版本控制
3. **特定模式**: 使用 `*-mode` 作用域（如果支持）
4. **系统管理**: 使用 `admin` 作用域（如果支持）
