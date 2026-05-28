---
name: settle
description: 问题沉淀流程。触发词：沉淀、三件套、settle。
---

# /settle

沉淀三件套的内部循环命令。确保每次沉淀都自动同步到 GitHub。

## 使用场景

- 解决 Bug 后记录经验
- 完成功能后沉淀模式
- 任何需要写入 `.cunzhi-knowledge/` 的场景

## 执行步骤（CRITICAL）

1. **调用 zhi** 询问要沉淀的类型：
   - problems（P-YYYY-NNN）
   - patterns（PAT-YYYY-NNN）
   - regressions（R-YYYY-NNN）

2. **准备内容** 按对应格式整理

3. **调用 ji(沉淀)** 写入（自动 git push）
   - `ji(action=沉淀, category=problems, content=...)`
   - `ji(action=沉淀, category=regressions, content=...)`
   - `ji(action=沉淀, category=patterns, content=...)`

4. **确认同步结果**
   - 看到 "🚀 已自动推送到 GitHub" → 成功
   - 看到 "⚠️ Git 同步失败" → 需要手动处理

## 禁止事项

- ❌ 使用 `edit` 工具直接编辑 `.cunzhi-knowledge/*.md`
- ❌ 跳过 regressions.md
- ❌ 不等 git push 完成就说"沉淀完成"

## 三件套顺序

```
problems.md → regressions.md → patterns.md
     ↓                ↓              ↓
  P-YYYY-NNN      R-YYYY-NNN    PAT-YYYY-NNN
```

**P-ID 与 R-ID 必须一一对应**

## 三件套完成后自动触发 Codex 审查

**三件套全部完成后，AI 自动执行以下步骤**：

1. **查找空闲端口**：检查 5313-5320 范围内的空闲端口
2. **启动后台审查**：
   ```bash
   (codex exec "审查最近提交..." > ~/.cunzhi/{端口}/codex_result.txt && \
    cat > ~/.cunzhi/{端口}/output.md <<'MD'
   ## Codex 审查完成
   $(cat ~/.cunzhi/{端口}/codex_result.txt)
   MD
    python3 /Users/apple/cunzhi/bin/cunzhi.py {端口} --workspace {项目路径}) &
   ```
3. **继续当前对话**：不等待审查完成
4. **用户收到通知**：审查完成后通过 iterate 弹窗呈现结果

## 示例输出

```
✅ 已沉淀到 .cunzhi-knowledge/problems.md
🚀 已自动推送到 GitHub

✅ 已沉淀到 .cunzhi-knowledge/regressions.md
🚀 已自动推送到 GitHub

✅ 已沉淀到 .cunzhi-knowledge/patterns.md
🚀 已自动推送到 GitHub

✓ 三件套沉淀完成，已同步到 GitHub

是否需要调用 Codex Skill 进行审查？
- 是：启动 Codex 后台审查
- 否：跳过审查
```
