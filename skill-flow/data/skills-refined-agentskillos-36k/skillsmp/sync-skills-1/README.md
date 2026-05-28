# sync-skills

自动将 skills 从多种来源同步到所有已安装的 AI 编码工具目录。

## 功能特点

- 🔍 **自动检测源类型**：本地文件夹、GitHub 仓库、skillsmp.com 页面
- 🎯 **智能同步**：只同步到已存在的目标目录
- 🔄 **自动覆盖**：同步时会覆盖已存在的 skill
- 🧹 **自动清理**：使用临时文件后自动清理

## 支持的目标目录

| 工具 | 项目级 | 用户级 |
|------|--------|--------|
| Claude Code | `.claude/skills` | `~/.claude/skills` |
| GitHub Copilot | `.github/skills` | `~/.copilot/skills` |
| Google Antigravity | `.agent/skills` | `~/.gemini/antigravity/skills` |
| Cursor | `.cursor/skills` | `~/.cursor/skills` |
| OpenCode | `.opencode/skill` | `~/.config/opencode/skill` |
| OpenAI Codex | `.codex/skills` | `~/.codex/skills` |
| Gemini CLI | `.gemini/skills` | `~/.gemini/skills` |
| Windsurf | `.windsurf/skills` | `~/.codeium/windsurf/skills` |
| Qwen Code | `.qwen/skills` | `~/.qwen/skills` |
| Qoder | `.qoder/skills` | `~/.qoder/skills` |

## 使用方法

### 基本用法

```bash
./sync-skill.sh <源地址>
```

### 示例

**本地文件夹：**
```bash
./sync-skill.sh /Users/user/skills/my-skill
```

**GitHub 仓库：**
```bash
./sync-skill.sh https://github.com/user/skill-repo
```

**skillsmp.com 页面：**
```bash
./sync-skill.sh https://skillsmp.com/skills/skill-name
```

## 输出示例

```
🔍 Detected source type: local

📁 Syncing local folder: /Users/user/skills/my-skill

🎯 Target directories:
  ➕ Creating: /Users/user/.claude/skills/my-skill
  📝 Overwriting: /Users/user/.gemini/antigravity/skills/my-skill

✅ Synced to 2 target directory(s)
```

## 注意事项

1. **覆盖策略**：如果目标目录已存在同名 skill，将直接覆盖，不会提示确认
2. **目录检查**：只同步到已存在的目标目录，不存在的目录会跳过
3. **临时文件**：GitHub 和 skillsmp.com 同步会使用临时文件，完成后自动清理
4. **权限要求**：脚本需要有执行权限（`chmod +x sync-skill.sh`）

## 故障排除

**问题：权限被拒绝**
```bash
chmod +x sync-skill.sh
```

**问题：没有目标目录**
脚本会显示 "No target directories exist"，确保至少安装了一个 AI 编码工具。

**问题：GitHub 克隆失败**
检查网络连接和仓库 URL 是否正确。

## 在 AI 助手中使用

当用户要求同步 skill 时，运行脚本：

```bash
# 用户说："帮我同步 /path/to/my-skill 这个 skill"
./sync-skill.sh /path/to/my-skill

# 用户说："同步这个 GitHub 仓库：https://github.com/user/skill"
./sync-skill.sh https://github.com/user/skill
```
