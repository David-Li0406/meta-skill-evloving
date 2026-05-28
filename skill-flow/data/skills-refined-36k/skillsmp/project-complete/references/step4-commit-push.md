# 步骤4：项目完成提交与推送

## Git 禁止项

- AI 署名（Co-Authored-By、Signed-off-by）
- `git push --force`
- `git commit --amend` 修改他人提交
- `git reset --hard` 到远程提交
- 提交 `.env`、密钥文件

## 提交前检查

```bash
git status
```

确认没有敏感信息。

## 执行最终提交（如有未提交变更）

```bash
git add Record/{plan_version}-changelog.md
git commit -m "docs: {plan_version} 变更日志"
```

## 推送到远程仓库

```bash
git push
```

**注意**：这是整个流程中唯一允许 `git push` 的时机。

## 追加项目记录

推送成功后，追加记录到 `Record/record.md`：

```markdown
## YYYY-MM-DD HH:MM 推送远程
commit：{commit_hash}
分支：{branch_name}
远程：{remote_name}
```

获取信息：
```bash
git log -1 --format="%H"
git branch --show-current
git remote -v | head -1 | awk '{print $1}'
```

## Record 目录处理

根据用户偏好：
- 要求提交：单独提交后一起推送
- 不要求：添加到 .gitignore
