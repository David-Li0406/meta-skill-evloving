---
name: deepwiki
description: "DeepWiki CLI - GitHub 仓库文档查询工具。用法: dw rws -r \"owner/repo\" | dw rwc -r \"owner/repo\" -t \"topic\" | dw aq -r \"owner/repo\" -q \"question\""
---

# DeepWiki Skill

GitHub 仓库文档查询工具，通过 DeepWiki API 获取结构、内容和问答。

## 快速使用

```bash
# 查看文档结构
dw rws -r "owner/repo"

# 查看特定内容
dw rwc -r "owner/repo" -t "topic"

# 提问
dw aq -r "owner/repo" -q "your question"

# 查看共享结果
dw vs -u "uuid"
```

## 安装

```bash
npm install -g deepwiki-cli
```

## 命令

| 命令 | 别名 | 说明 |
|------|------|------|
| `read_wiki_structure` | `rws`, `str` | 获取文档结构 |
| `read_wiki_contents` | `rwc`, `cont` | 读取文档内容 |
| `ask_question` | `aq`, `ask` | 提问 |
| `view_share` | `vs` | 查看共享查询 |

## 参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `--repoName` | `-r` | 仓库名 (owner/repo) |
| `--topic` | `-t` | 文档主题 |
| `--question` | `-q` | 问题 |
| `--uuid` | `-u` | 查询 UUID |
| `--format` | `-f` | 格式 (brief\|full\|json) |
| `--lang` | `-l` | 语言 (en\|zh) |

## 本地使用

```bash
cd ~/.pi/agent/skills/deepwiki
node dw.js <command> [options]
```

## 链接

- GitHub: https://github.com/Dwsy/deepwiki-skills
- npm: https://www.npmjs.com/package/deepwiki-cli