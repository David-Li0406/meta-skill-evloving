# 步骤2：初始化 OpenSpec 和 Git

## 2.1 初始化 Git 仓库

如果项目尚未初始化 git：

```bash
git init
```

## 2.2 初始化 OpenSpec

```bash
openspec init --tools none
```

执行效果：
- 创建 `openspec/specs/`
- 创建 `openspec/changes/`
- 创建 `openspec/changes/archive/`

## 2.3 初始化后清理

```bash
rm -f AGENTS.md
```

## 2.4 初始提交

```bash
git add openspec/
git add .gitignore
git commit -m "chore: 初始化 OpenSpec 项目结构"
```

**禁止**：`git push`
