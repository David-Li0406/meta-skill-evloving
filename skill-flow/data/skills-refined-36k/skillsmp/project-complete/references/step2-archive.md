# 步骤2：归档 OpenSpec 提案

## 执行归档

对每个状态为 `accepted` 的提案执行：

```bash
openspec archive {proposal_id} --yes
```

归档顺序：
1. 功能实现提案（按创建顺序）
2. 修复提案（如有）
3. 编译提案

## 归档效果

- `openspec/changes/{proposal_id}/` → `openspec/archive/{proposal_id}/`
- delta 合并到 `openspec/specs/`

## 归档后本地提交

```bash
git add openspec/
git commit -m "chore: 归档提案"
```

**禁止**：`git push`

## 追加项目记录

归档提交后，追加记录到 `Record/record.md`：

```markdown
## YYYY-MM-DD HH:MM 归档完成
commit：{commit_hash}
归档提案数：{数量}
提案列表：{proposal_id_1}, {proposal_id_2}, ...
```

获取 commit hash：
```bash
git log -1 --format="%H"
```

## 更新状态

更新 `Record/state.json` 中每个提案状态为 `archived`。
