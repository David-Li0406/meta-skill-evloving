---
name: session-loader
description: Load feature specification and determine next task at session start. Use when user asks to "implement spec", "continue work", or "реализуй ТЗ". Finds spec file matching current branch and extracts next atomic task.
---

# Session Loader Skill

You load the feature specification and prepare the next implementation task at the start of each session.

## When to Use This Skill

- User asks to "implement spec" or "реализуй ТЗ"
- User asks to "continue work" or "продолжи работу"
- Starting a new session after `/clear`
- User references a feature spec file

## Workflow

### Step 1: Identify Current Branch

```bash
git branch --show-current
```

If on `master` or `main`:
```
⚠️ Вы находитесь в защищённой ветке: {branch}

Для реализации фичи:
1. Запустите /plan для создания ТЗ и ветки
2. Или переключитесь на существующую feature-ветку:
   git checkout feature/{name}
```
**STOP** — do not proceed.

### Step 2: Find Spec File

Convert branch name to spec path:
```
{branch-name} → .ai/specs/{branch-name}.md
```

Examples:
- `feature/user-auth` → `.ai/specs/feature-user-auth.md`
- `bugfix/123-fix` → `.ai/specs/bugfix-123-fix.md`

Check if file exists:
```bash
test -f .ai/specs/{branch-name}.md && echo "EXISTS" || echo "NOT FOUND"
```

If NOT FOUND:
```
❌ ТЗ не найдено для ветки: {branch}

Ожидаемый файл: .ai/specs/{branch-name}.md

Действия:
1. Запустите /plan для создания ТЗ
2. Или создайте файл вручную
```
**STOP** — do not proceed.

### Step 3: Load and Parse Spec

Read the spec file and extract:
1. **Feature name** — from title
2. **Current status** — 🟡 В работе / ✅ Завершён
3. **All stages** — with their statuses
4. **Next incomplete stage** — first with ⬜ or 🔄

### Step 4: Determine Next Task

Find the first stage that is:
- ⬜ Не начат, OR
- 🔄 В работе (resume)

If all stages are ✅:
```
✅ Все этапы завершены!

Фича готова к мержу.
Запустите: "merge в main" или используйте merge-helper
```
**STOP** — feature complete.

### Step 5: Present Task to User

Output the session context:

```
📋 Загружено ТЗ: .ai/specs/{branch-name}.md
🌿 Ветка: {branch-name}

═══════════════════════════════════════════════════
📌 ТЕКУЩИЙ ЭТАП: {stage_number}. {stage_name}
═══════════════════════════════════════════════════

**Цель:** {stage_goal}

**Задачи:**
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

**Файлы:**
- `path/to/file1.py` (создать)
- `path/to/file2.py` (изменить)

**Критерий приёмки:** {acceptance_criteria}

═══════════════════════════════════════════════════

📊 Прогресс: {completed}/{total} этапов
[████████░░░░░░░░] {percent}%

Готов к реализации. Подтвердите начало работы.
```

### Step 6: Update Stage Status

When user confirms, update spec file:
- Change stage status: ⬜ → 🔄
- Add timestamp to history table

### Step 7: Execute Task

Implement the stage tasks:
1. Create/modify files as specified
2. Follow project conventions
3. Write tests if required
4. Keep changes ≤250 lines

### Step 8: After Implementation

When stage is complete:
1. Run tests: `uv run pytest`
2. Use **commit-helper** for commit
3. Update spec file:
   - Change stage status: 🔄 → ✅
   - Check off completed tasks
   - Add commit hash to history

## Spec File Updates

### Marking Stage In-Progress

```markdown
### Этап 2: Service Layer (~150 строк)
**Статус:** 🔄 В работе  ← Changed from ⬜
```

### Marking Stage Complete

```markdown
### Этап 2: Service Layer (~150 строк)
**Статус:** ✅ Завершён  ← Changed from 🔄

**Задачи:**
- [x] Task 1  ← Checked
- [x] Task 2  ← Checked
```

### History Entry

```markdown
## История изменений

| Дата       | Этап | Коммит  | Описание                  |
| ---------- | ---- | ------- | ------------------------- |
| 2026-01-07 | 2    | abc1234 | Service layer implemented | ← New row |
| 2026-01-06 | 1    | def5678 | Models and schemas        |
| 2026-01-06 | -    | -       | ТЗ создано                |
```

## Error Handling

### Branch Mismatch

If spec branch doesn't match current branch:
```
⚠️ Несоответствие веток

Текущая ветка: feature/other-feature
ТЗ ветка: feature/user-auth

Переключитесь на нужную ветку:
git checkout feature/user-auth
```

### Spec Corruption

If spec file is malformed:
```
⚠️ Ошибка парсинга ТЗ

Файл .ai/specs/{branch}.md повреждён или имеет неверный формат.

Проверьте структуру файла или создайте новый через /plan
```

## References

See [commit-helper](../commit-helper/SKILL.md) for commit workflow.
See [plan-mode](../plan-mode/SKILL.md) for spec creation.
