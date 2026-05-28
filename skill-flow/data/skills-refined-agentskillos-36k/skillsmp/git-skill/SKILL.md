---
name: git-skill
description: 用户说使用 git 时调用，git add,git commit, git push 自动化
---

## instructions
当用户要求进行 Git 相关操作时，请遵循以下规则：
1. 仅在用户明确要求进行 Git 操作时使用此技能。
2. 支持的操作包括：git add、git commit、git push。
3. 在执行任何操作前，务必确认用户的意图。
4. 在执行 git commit 时，由你根据上下文生成合适的提交信息，确保其简洁且描述性强。
5. 在执行 git push 前，确保本地分支与远程分支同步，避免冲突。

## usage examples
1. 添加变更（git add）
目的：将工作区的修改暂存到索引区。
最优操作：
使用 git add <文件名> 精确添加特定文件，避免使用 git add . 误加无关文件。
交互式暂存：git add -p 可逐块审查变更，适合部分提交。
始终通过 git status 验证暂存内容。

2. 提交变更（git commit）
目的：将暂存区的变更记录到本地仓库。
最优操作：
提交信息规范：采用清晰格式（如 类型: 描述），例如 fix: 修复登录逻辑错误。
频繁提交：小单元提交便于回溯，避免大规模一次性提交。
命令选择：git commit -m "消息" 快速提交，或 git commit 编写详细说明。

3. 推送到远程（git push）
目的：将本地提交同步到远程仓库（如 GitHub）。
最优操作：
先拉取后推送：执行 git pull 合并远程更新，防止冲突。
指定分支：git push origin <分支名> 确保目标准确。
定期推送：减少合并复杂度，结合代码审查流程。
