# 文件引用规范（problem-solution-dialogue）

当 `skills/problem-solution-dialogue/SKILL.md` 需要引用同技能目录下的其他文件时，遵循：

1) 使用相对路径（从技能根目录开始）

- 正例：`context-clarifier.md`、`references/xxx.md`、`scripts/xxx.py`
- 反例：绝对路径、跨目录引用到其他技能

2) 引用深度保持一层（从 `SKILL.md` 出发最多 1 层）

- 允许：`SKILL.md -> context-clarifier.md`
- 允许：`SKILL.md -> references/xxx.md`
- 避免：`SKILL.md -> a.md -> references/b.md`（深链）

3) 让 `SKILL.md` 保持“可扫描”，把细节放到被引用文件

- `SKILL.md`：规则/阶段门/最小必要结构
- 被引用文件：模板、提示语、详细说明

4) 修改后运行抽取/校验脚本

在技能根目录下执行：

```bash
python3 scripts/extract.py
```

