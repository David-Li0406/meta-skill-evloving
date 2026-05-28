---
name: session-consolidator
description: Analyze completed parallel-executor session in fresh context and generate consolidation report. Use after all parallel stages complete. Spawns isolated subagent to analyze session history and create archive document.
---

# Session Consolidator Skill

**Назначение:** Анализирует завершённую сессию параллельного выполнения в чистом контексте и создаёт отчёт о консолидации в архиве.

**Ключевая особенность:** Запускает субагента в изолированном контексте (fresh context) для объективного анализа выполнения пайплайна.

---

## Когда использовать

- **Auto-triggered** после завершения всех этапов `parallel-executor` (основной триггер)
- Все этапы спецификации имеют статус ✅
- Пользователь явно запрашивает: "analyze session", "consolidate session"

---

## Алгоритм работы

### 1. Определение текущей ветки

```bash
git branch --show-current
```

Результат: `feature/{branch-name}` или `bugfix/{branch-name}`

### 2. Поиск spec-файла

Формат пути: `.ai/specs/{branch-name}.md`

Примеры:
- `feature/user-auth` → `.ai/specs/feature-user-auth.md`
- `bugfix/123-fix` → `.ai/specs/bugfix-123-fix.md`

Если файл не найден:
```
❌ Spec-файл не найден: .ai/specs/{branch-name}.md

Невозможно выполнить консолидацию без спецификации.
```
**STOP** — завершение работы.

### 3. Сбор истории сессии

Извлечь из репозитория:

**Данные из spec-файла:**
- Название фичи
- Все этапы с их статусами
- Таблица истории изменений
- Даты создания и завершения

**Git история:**
```bash
# Коммиты текущей ветки
git log {branch-name} --oneline --no-merges

# Статистика изменений
git log --stat {branch-name}

# Первый и последний коммит
git log --reverse {branch-name} | head -1
git log {branch-name} | head -1
```

**Framework правила:**
- Извлечь релевантные секции из `CLAUDE.md`
- Чек-лист соответствия пайплайну

### 4. Подготовка сжатой сессии

Создать структурированный дата-пакет для субагента:

```yaml
session_data:
  branch: {branch-name}
  spec_file: .ai/specs/{branch-name}.md
  start_date: {date of first commit}
  end_date: {date of last commit}
  stages:
    - name: {stage-1}
      status: ✅
      commits: [hash1, hash2]
      files: [file1.py, file2.py]
    - name: {stage-2}
      status: ✅
      commits: [hash3]
      files: [file3.py]
  git_history:
    total_commits: {count}
    files_changed: {count}
    insertions: {count}
    deletions: {count}
  framework_rules:
    - confidence-evaluator required
    - spec file required
    - max 250 lines per stage
    - conventional commits
    - changelog update
```

**ВАЖНО:** Не передавать полную историю переписки — только структурированные данные!

### 5. Запуск субагента в чистом контексте

```python
Task(
    subagent_type="general-purpose",
    prompt=f"""
    # Session Analysis in FRESH CONTEXT

    You are analyzing a completed development session. This is your ONLY input — you have NO access to previous conversations.

    **ВАЖНО:** Генерируй отчёт **на русском языке**. Все секции (Executive Summary, Ambiguities, Decisions, Lessons Learned и т.д.) должны быть на русском.

    ## Session Data

    {condensed_session_data}

    ## Your Task

    1. **Analyze pipeline compliance** using the framework checklist
    2. **Identify ambiguities** encountered during implementation
    3. **Document decisions** made and their rationale
    4. **Generate report** in **RUSSIAN** using the template below

    ## Pipeline Compliance Checklist

    Derived from CLAUDE.md framework:
    - [ ] confidence-evaluator run before implementation?
    - [ ] Spec file exists and was followed?
    - [ ] Each stage ≤250 lines?
    - [ ] Tests run before each commit?
    - [ ] Conventional commits used (feat:, fix:, etc.)?
    - [ ] CHANGELOG updated before each commit?
    - [ ] Stage statuses properly tracked (⬜→🔄→✅)?

    ## Ambiguity Categories

    Look for:
    - Requirements interpretation issues
    - Architecture decisions not in spec
    - File path deviations from plan
    - Dependencies added without documentation
    - Unclear requirements resolved mid-implementation

    ## Output Template

    {session_summary_template}

    ---

    Remember: You are in FRESH CONTEXT. Analyze ONLY the data provided above.
    """,
    # NOT run_in_background — wait for completion to get the report
)
```

### 6. Получение отчёта

Дождаться завершения субагента и извлечь сгенерированный markdown-отчёт.

### 7. Запись в архив

Путь: `.ai/specs/archive/{branch-name}-session-summary.md`

Если файл существует — **перезаписать** (overwrite_existing: true)

```bash
# Создать директорию archive если не существует
mkdir -p .ai/specs/archive

# Записать отчёт
cat > .ai/specs/archive/{branch-name}-session-summary.md <<'EOF'
{generated_report_content}
EOF
```

### 8. Подтверждение пользователю

```
✅ Session consolidation complete

📄 Report: .ai/specs/archive/{branch-name}-session-summary.md
🌿 Branch: {branch-name}
📊 Compliance Score: {X}/10

Generated in fresh context by isolated subagent.
```

---

## Шаблон отчёта (для ссылки)

```markdown
# Отчёт о консолидации сессии: {feature-name}

> **Создан:** {timestamp}
> **Ветка:** {branch-name}
> **Spec:** `.ai/specs/{branch-name}.md`
> **Длительность:** {start-date} → {end-date}

---

## Краткое содержание (Executive Summary)

{Краткий обзор выполненной работы}

---

## Анализ соответствия пайплайну (Pipeline Compliance Analysis)

### Оценка соответствия: {X}/10

| Проверка | Статус | Заметки |
|----------|--------|---------|
| Использован confidence-evaluator | ✅/❌ | {notes} |
| Spec выполнен | ✅/❌ | {notes} |
| Лимиты строк соблюдены | ✅/❌ | {notes} |
| Тесты запущены перед коммитами | ✅/❌ | {notes} |
| Использованы conventional commits | ✅/❌ | {notes} |
| CHANGELOG обновлён | ✅/❌ | {notes} |
| Отслеживание этапов | ✅/❌ | {notes} |

### Отклонения от фреймворка

{Список отклонений с объяснениями}

---

## Выявленные неясности (Ambiguities Encountered)

### {Категория}

**Неясность:** {description}
**Решение:** {how it was resolved}
**Обоснование:** {why this approach was chosen}

---

## Принятые решения (Decisions Made)

### {Область решения}

**Решение:** {what was decided}
**Рассмотренные альтернативы:** {other options}
**Обоснование:** {why this was chosen}

---

## Сводка выполнения этапов (Stage Execution Summary)

| Этап | Статус | Коммиты | Строк изменено | Заметки |
|------|--------|---------|----------------|---------|
| {stage-1} | ✅ | {hash} | {count} | {notes} |
| {stage-2} | ✅ | {hash} | {count} | {notes} |

---

## Уроки на будущее (Lessons Learned)

{Что прошло хорошо, что можно улучшить}

---

## Рекомендации для будущих сессий

1. {recommendation-1}
2. {recommendation-2}

---

## Метаданные архива

- **Spec-файл:** `.ai/specs/{branch-name}.md`
- **Сводка сессии:** `.ai/specs/archive/{branch-name}-session-summary.md`
- **Финальный коммит:** {commit-hash}
- **Всего изменений:** {files changed}, {insertions}, {deletions}
```

---

## Интеграция с parallel-executor

После завершения всех этапов `parallel-executor` автоматически запускается `session-consolidator`:

```python
# В конце parallel-executor, после всех этапов
if all_stages_complete():
    Skill(skill="session-consolidator")
```

---

## Конфигурация

`.ai/ai-settings.json`:

```json
{
  "framework": {
    "session_consolidation": {
      "enabled": true,
      "auto_trigger_after_parallel": true,
      "output_directory": ".ai/specs/archive",
      "output_filename_pattern": "{branch-name}-session-summary.md",
      "include_git_history": true,
      "overwrite_existing": true,
      "analysis_focus": "pipeline_compliance_only"
    }
  }
}
```

**Параметры:**
- `enabled` — включён ли skill
- `auto_trigger_after_parallel` — авто-запуск после parallel-executor
- `overwrite_existing` — перезаписывать существующий отчёт
- `analysis_focus` — "pipeline_compliance_only" (без тестов)

---

## Диагностика

При ошибках проверить:
```bash
# Существование spec-файла
test -f .ai/specs/{branch-name}.md

# Доступность archive директории
test -d .ai/specs/archive

# Git лог для ветки
git log {branch-name}
```

---

## Fresh Context Guarantee

Для обеспечения чистого контекста:

1. **НЕ передавать** историю переписки родительской сессии
2. Передавать только структурированные данные (spec, git log, framework excerpts)
3. Явно указать субагенту, что это новый контекст
4. Субагент не имеет доступа к tool results родительской сессии

Это обеспечивает объективность анализа — субагент видит только факты, а не эмоциональный контекст выполнения.

---

## Related Skills

- **parallel-executor** — запускает этот skill по завершении
- **session-loader** — загружает spec перед консолидацией
- **merge-helper** — использует отчёт при финальном merge

---

## Output Example

```
✅ Session consolidation complete

📄 Report: .ai/specs/archive/feature-user-auth-session-summary.md
🌿 Branch: feature/user-auth
📊 Compliance Score: 9/10

⚠️ 1 deviation found: Stage 2 exceeded 250 lines limit
💡 3 ambiguities documented
📋 5 decisions recorded
```
