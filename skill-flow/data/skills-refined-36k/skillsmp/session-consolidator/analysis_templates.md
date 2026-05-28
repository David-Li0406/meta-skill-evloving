# Analysis Templates and Framework

Этот файл содержит шаблоны для анализа сессии и генерации отчёта консолидации.

**ВАЖНО:** Все генерируемые отчёты должны быть **на русском языке**. При запуске субагента явно указывайте, что выход должен быть на русском.

---

## Pipeline Compliance Checklist

Чек-лист соответствия пайплайну на основе правил из `CLAUDE.md`:

| № | Check | Description | Pass Criteria |
|---|-------|-------------|---------------|
| 1 | **confidence-evaluator used** | Был ли запущен confidence-evaluator перед началом реализации? | First commit shows confidence evaluation or spec was created with high confidence |
| 2 | **Spec file exists** | Существует ли файл спецификации для фичи? | `.ai/specs/{branch-name}.md` exists and is readable |
| 3 | **Spec followed** | Следовала ли implementation этапам из spec? | All completed stages match spec stages |
| 4 | **Line limits respected** | Соблюдён ли лимит ≤250 строк за коммит? | All commits have ≤250 lines changed (additions + deletions) |
| 5 | **Conventional commits** | Использованы ли conventional commits? | All commit messages follow `feat:`, `fix:`, `refactor:`, `test:`, `docs:` pattern |
| 6 | **CHANGELOG updated** | Обновлялся ли CHANGELOG перед каждым коммитом? | CHANGELOG.md has entry for each commit |
| 7 | **Stage tracking** | Отслеживались ли статусы этапов (⬜→🔄→✅)? | Spec file shows proper status progression |
| 8 | **Tests run** | Запускались ли тесты перед коммитом? | Commits after test commits or test evidence in messages |

### Scoring

- **8/8** = Perfect compliance (100%)
- **6-7/8** = Good compliance (75-87%)
- **4-5/8** = Acceptable compliance (50-62%)
- **<4/8** = Poor compliance (<50%) — requires investigation

---

## Ambiguity Categories

Категории неясностей, которые следует выявлять при анализе:

### 1. Requirements Interpretation

**Примеры:**
- Неоднозначная формулировка требования в spec
- Противоречивые требования между разными секциями
- Отсутствующие критерии приёмки

**Что искать:**
- Коммиты с сообщениями "clarify", "update requirement", "fix interpretation"
- Большие переработки после первоначальной реализации
- Множественные коммиты в одном файле для одной задачи

### 2. Architecture Decisions Not in Spec

**Примеры:**
- Новые директории/модули не упомянутые в spec
- Изменения в архитектуре без обновления ARCHITECTURE.md
- Внедрение новых зависимостей без документирования

**Что искать:**
- Новые `import` statements вrequirements/dependencies
- Создание новых модулей не указанных в spec
- Изменения в `pyproject.toml` или `config.py`

### 3. File Path Deviations

**Примеры:**
- Файлы созданы в других директориях чем указано в spec
- Переименование файлов в процессе
- Объединение или разделение файлов

**Что искать:**
- `git mv` operations
- Файлы созданные не в указанных в spec путях
- Множественные файлы там где spec обещал один

### 4. Dependencies Added Without Documentation

**Примеры:**
- Новые пакеты в `pyproject.toml` без упоминания в spec
- Внешние API клиенты не описанные в spec
- Библиотеки для тестирования не указанные изначально

**Что искать:**
- Изменения в `[tool.poetry.dependencies]` или `[project.dependencies]`
- Новые `import` statements для внешних пакетов

### 5. Test Coverage Gaps

**Примеры:**
- Функциональность без тестов
- Тесты покрывающие только happy path
- Отсутствие edge case тестов

**Что искать:**
- Коммиты с кодом но без соответствующих тестовых коммитов
- Отсутствие `test_*.py` для новых модулей

---

## Шаблон выходного отчёта (Analysis Output Template)

```markdown
# Отчёт о консолидации сессии: {feature-name}

> **Создан:** {YYYY-MM-DD HH:MM}
> **Ветка:** {branch-name}
> **Spec:** `.ai/specs/{branch-name}.md`
> **Длительность:** {start-date} → {end-date} ({days} дней)

---

## Краткое содержание (Executive Summary)

{2-3 предложения о выполненной работе в этой сессии}

**Оценка соответствия:** {X}/10 — {прилагательное}

---

## Анализ соответствия пайплайну (Pipeline Compliance Analysis)

### Оценка соответствия: {X}/10

| Проверка | Статус | Заметки |
|----------|--------|---------|
| Использован confidence-evaluator | ✅/❌ | {краткое объяснение} |
| Spec-файл существует | ✅/❌ | {путь или причина отсутствия} |
| Spec выполнен | ✅/❌ | {процент выполненных этапов по плану} |
| Лимиты строк соблюдены | ✅/❌ | {максимум строк в коммите, нарушения} |
| Использованы conventional commits | ✅/❌ | {количество не соответствующих коммитов} |
| CHANGELOG обновлён | ✅/❌ | {количество записей на коммит} |
| Отслеживание этапов | ✅/❌ | {проверка прогресса статусов} |
| Тесты запущены перед коммитами | ✅/❌ | {доказательства тестов} |

### Отклонения от фреймворка

{Если есть отклонения, перечислить их с подробным объяснением}

**Отклонение #{N}: {Заголовок}**
- **Что произошло:** {описание}
- **Влияние:** {низкое/среднее/высокое}
- **Рекомендация:** {как предотвратить в будущем}

{Если нет отклонений:}
✅ Значительных отклонений от фреймворка не обнаружено.

---

## Выявленные неясности (Ambiguities Encountered)

{Список неясностей, обнаруженных при анализе в хронологическом порядке}

### {Название категории}: {Краткий заголовок}

**Неясность:**
{Описание нечёткого требования или ситуации}

**Как было решено:**
{Объяснение принятого решения}

**Обоснование:**
{Почему этот подход был выбран вместо альтернатив}

**Доказательства:**
{Хеши коммитов, пути к файлам или другие индикаторы}

{Если нет неясностей:}
✅ Значительных неясностей в ходе реализации не выявлено.

---

## Принятые решения (Decisions Made)

{Документирование ключевых архитектурных и реализационных решений}

### {Область решения}: {Краткий заголовок}

**Решение:**
{Что было решено}

**Рассмотренные альтернативы:**
- Альтернатива 1: {описание}
- Альтернатива 2: {описание}

**Обоснование:**
{Почему этот вариант был выбран}

**Влияние:**
{Эффект на кодовую базу, производительность, поддерживаемость}

{Если нет значимых решений:}
Все решения по реализации были указаны в исходном spec.

---

## Сводка выполнения этапов (Stage Execution Summary)

| Этап | Статус | Коммиты | Строк изменено | Длительность | Заметки |
|------|--------|---------|---------------|--------------|---------|
| {название этапа-1} | ✅ | {hash1, hash2} | {+123, -45} | {дней} | {краткие заметки} |
| {название этапа-2} | ✅ | {hash3} | {+67, -12} | {дней} | {краткие заметки} |
| {название этапа-3} | ✅ | {hash4, hash5, hash6} | {+234, -89} | {дней} | {краткие заметки} |

**Всего изменений:**
- Коммитов: {total_count}
- Файлов изменено: {total_files}
- Строк добавлено: {+total_additions}
- Строк удалено: {-total_deletions}
- Чистое изменение: {net_change}

---

## Статистика Git

```bash
# Информация о ветке
Ветка: {branch-name}
Базовая ветка: {main/master}
Коммитов в ветке: {count}

# Первый коммит
{first_commit_hash} - {first_commit_date} - {first_commit_message}

# Последний коммит
{last_commit_hash} - {last_commit_date} - {last_commit_message}

# Изменённые файлы по типу
Python: {count} файлов
Markdown: {count} файлов
Config: {count} файлов
Tests: {count} файлов
```

---

## Уроки на будущее (Lessons Learned)

### Что прошло хорошо

{2-3 пункта о положительных аспектах}

- {пример: "Чёткая структура spec позволила параллельное выполнение"}
- {пример: "Ограничение в 250 строк удерживало изменения сфокусированными"}

### Области для улучшения

{2-3 пункта о том, что можно улучшить}

- {пример: "Spec мог иметь более детальные критерии приёмки"}
- {пример: "Некоторые этапы превысили 250 строк из-за сложности"}

---

## Рекомендации для будущих сессий

1. **{Область}:** {конкретная рекомендация с обоснованием}
2. **{Область}:** {конкретная рекомендация с обоснованием}
3. **{Область}:** {конкретная рекомендация с обоснованием}

---

## Метаданные архива

- **Spec-файл:** `.ai/specs/{branch-name}.md`
- **Сводка сессии:** `.ai/specs/archive/{branch-name}-session-summary.md`
- **Ветка фичи:** {branch-name}
- **Первый коммит:** {first_commit_hash}
- **Финальный коммит:** {last_commit_hash}
- **Общая длительность:** {days} дней
- **Всего изменений:** {files} файлов изменено, {insertions} добавлений(+), {deletions} удалений(-)

---

*Отчёт сгенерирован автоматически навыком session-consolidator в чистом контексте*
```

---

## Структура промпта субагента (Subagent Prompt Structure)

Шаблон промпта для запуска субагента в чистом контексте:

```python
condensed_prompt = f"""
# Запрос на анализ сессии (Session Analysis Request)

You are a session analyzer operating in **FRESH CONTEXT**. This means:
- You have NO access to previous conversation history
- You must base your analysis ONLY on the structured data below
- You cannot ask follow-up questions about the implementation

**ВАЖНО:** Генерируй отчёт **на русском языке**. Все секции должны быть на русском.

## Пакет данных сессии (Session Data Package)

```yaml
session_metadata:
  branch: "{branch_name}"
  spec_file: ".ai/specs/{spec_filename}"
  analysis_date: "{current_date}"
  duration: "{start_date} → {end_date}"

spec_content: |
  {FULL_SPEC_FILE_CONTENT}

git_history: |
  {GIT_LOG_OUTPUT}

git_statistics:
  total_commits: {count}
  files_changed: {count}
  insertions: {count}
  deletions: {count}

commits_detail:
  - hash: "{hash1}"
    message: "{commit_msg}"
    author: "{author}"
    date: "{date}"
    files: [file1.py, file2.py]
    stats: "{{'+123', '-45'}}"

framework_rules:
  max_lines_per_commit: 250
  commit_convention: "conventional"
  changelog_policy: "before_each_commit"
  stage_tracking: true
```

## Ваша задача анализа (Your Analysis Task)

Используя ТОЛЬКО данные выше:

1. **Рассчитать оценку соответствия (Compliance Score)** (0-10) по чек-листу:
   - Использован ли confidence-evaluator?
   - Существует ли spec-файл и был ли он выполнен?
   - Каждый этап ≤250 строк?
   - Использованы ли conventional commits?
   - CHANGELOG обновлён?
   - Отслеживание этапов правильное?

2. **Выявить неясности (Identify Ambiguities)** по:
   - Проблемам интерпретации требований
   - Архитектурным решениям не в spec
   - Отклонениям путей файлов
   - Недокументированным зависимостям
   - Пробелам в покрытии тестами

3. **Документировать решения (Document Decisions)** принятые в процессе:
   - Архитектурного выбора
   - Подходов реализации
   - Выбора зависимостей

4. **Сгенерировать отчёт на русском языке (Generate Report in Russian)** используя шаблон ниже:

{SESSION_SUMMARY_TEMPLATE}

## Важные напоминания (Important Reminders)

- Вы в ЧИСТОМ КОНТЕКСТЕ (FRESH CONTEXT) — не ссылайтесь на какие-либо разговоры
- Базируйте анализ ТОЛЬКО на предоставленных структурированных данных
- Будьте объективны и фактичны
- Если данных недостаточно, укажите "Недостаточно данных для определения"
- Не делайте предположений за пределами того, что показывают данные

Начните свой анализ сейчас.
"""
```

---

## File Change Categories

Для анализа изменения файлов:

| Category | Pattern | Description |
|----------|---------|-------------|
| Core Logic | `src/**/*.py` | Основной код приложения |
| Tests | `tests/**/*.py` | Тестовые файлы |
| Config | `*.toml`, `*.json`, `.env*` | Конфигурация |
| Docs | `*.md`, `*.txt` | Документация |
| Specs | `.ai/**/*.md` | Спецификации фич |
| Skills | `.claude/**/*.md` | Skill определения |
| Templates | `templates/**/*` | HTML/UI шаблоны |
| Static | `static/**/*` | CSS, JS, assets |

---

## Commit Message Pattern Matching

Для проверки conventional commits:

```python
import re

CONVENTIONAL_COMMIT_PATTERN = r'^(feat|fix|refactor|test|docs|chore|style|perf)(\(.+\))?\!?:\s.+'

def check_conventional_commit(message: str) -> bool:
    """Check if commit message follows conventional commit format."""
    return bool(re.match(CONVENTIONAL_COMMIT_PATTERN, message))
```

**Valid examples:**
- `feat(auth): add JWT token validation`
- `fix: correct timezone handling in scheduler`
- `refactor(user): simplify password hashing`
- `test: add integration tests for API`
- `docs: update README with new features`

**Invalid examples:**
- `update code`
- `fixed bug`
- `Add new feature`
- `wip`
- `update`
