---
name: parallel-executor
description: Execute independent spec stages in parallel using subagents with real-time incremental apply. Use when spec has multiple stages without file conflicts. Automatically detects dependencies and runs maximum parallel agents.
---

# Parallel Executor Skill

**Назначение:** Выполняет независимые этапы ТЗ параллельно с помощью субагентов.

**Ключевая особенность:** Real-time incremental apply — изменения применяются мгновенно по мере завершения каждого агента, обеспечивая немедленную обратную связь.

---

## Когда использовать

- Пользователь запрашивает: "реализуй ТЗ параллельно", "implement spec in parallel"
- Spec-файл содержит ≥2 этапов
- Этапы не конфликтуют по файлам

---

## Алгоритм работы

### 1. Загрузка спецификации

Определить текущую ветку:
```bash
git branch --show-current
```

Загрузить spec-файл:
```
.ai/specs/{branch-name}.md
```

### 2. Анализ зависимостей

Для каждого этапа спецификации извлечь:
- **Статус** — только ⬜ (не начат) или 🔄 (в работе)
- **Файлы** — секция "Файлы" в этапе

Построить **матрицу конфликтов**:

| Этап A | Этап B | Конфликт? |
|--------|--------|-----------|
| Stage1 | Stage2 | Да, если пересекаются файлы |
| Stage1 | Stage3 | Нет, файлы разные |

**Правило:** Этапы могут выполняться параллельно ↔️ их файлы не пересекаются.

### 3. Топологическая сортировка

Разбить этапы на **уровни параллелизма**:

```
Уровень 0: [Stage1, Stage3]  — могут выполняться параллельно
Уровень 1: [Stage2]           — зависит от Stage1
Уровень 2: [Stage4]           — зависит от Stage2
```

### 4. Запуск параллельных агентов

Для каждого этапа на текущем уровне создать субагента:

```python
# Через Task tool
Task(
    subagent_type="general-purpose",
    prompt=f"""
    Выполни этап {stage_name} из спецификации {spec_file}.

    ## Правила фреймворка
    1. Работай в рамках одного коммита (≤250 строк изменений)
    2. Используй conventional commits: feat:, fix:, refactor:, test:
    3. Запускай тесты перед коммитом
    4. НЕ обновляй CHANGELOG.md (обновляется только при merge)
    5. Все правила из CLAUDE.md обязательны к исполнению

    ## Этап для выполнения
    {stage_content}

    ## Требуемый результат
    1. Реализуй все задачи этапа
    2. Запусти тесты
    3. Создай коммит через commit-helper
    4. Обнови статус этапа в spec на ✅
    """,
    run_in_background=True  # параллельное выполнение
)
```

**Важно:** Передать все агенты в **одном сообщении** для истинного параллелизма:

```
[Task tool для агента 1]
[Task tool для агента 2]
[Task tool для агента 3]
```

### 5. Мониторинг и применение изменений

Сохранить task_id для каждого агента:
```python
task_ids = [agent1.id, agent2.id, agent3.id]
```

#### Режим 1: Real-time Incremental Apply (рекомендуется)

Применять изменения **мгновенно** по мере завершения каждого агента:

```python
import time

pending_tasks = {task_id: stage_name for task_id, stage_name in zip(task_ids, stage_names)}
applied_stages = []

while pending_tasks:
    for task_id in list(pending_tasks.keys()):
        result = TaskOutput(task_id=task_id, block=False)

        if result.get("status") == "completed":
            # Агент завершился — применяем изменения немедленно
            stage_name = pending_tasks[task_id]

            # Извлекаем сгенерированный код из результата
            generated_files = extract_code_from_result(result)

            # Применяем через Write/Edit
            for file_path, content in generated_files.items():
                if content.get("action") == "create":
                    Write(file_path=file_path, content=content["code"])
                elif content.get("action") == "edit":
                    Edit(file_path=file_path, old_string=content["old"], new_string=content["new"])

            applied_stages.append(stage_name)
            del pending_tasks[task_id]

            print(f"✅ {stage_name} применён ({len(applied_stages)}/{len(task_ids)})")

    time.sleep(2)  # Polling interval
```

**Преимущества real-time apply:**
- Мгновенная обратная связь для пользователя
- Раннее обнаружение конфликтов
- Возможность продолжить работу даже если один агент упал
- Пользователь видит прогресс в реальном времени

#### Режим 2: Batch Apply (традиционный)

Ждать завершения всех агентов, затем применять:

```python
all_results = []
for task_id in task_ids:
    result = TaskOutput(task_id=task_id, block=True)
    all_results.append(result)

# Применяем все изменения разом
for result in all_results:
    apply_changes_from_result(result)
```

### 6. Сбор результатов

**Возможные исходы:**
- ✅ Все этапы успешно — перейти к следующему уровню
- ⚠️ Частичный успех — зафиксировать ошибки, предложить повтор
- ❌ Конфликт при merge — использовать git-merge стратегию

### 7. Обработка конфликтов

Если агенты изменили одни и те же файлы:

```bash
# Попытка авто-merge
git merge agent1-branch --no-edit

# Если конфликт — уведомить пользователя
echo "Обнаружен конфликт в {файл}"
echo "Агент 1: {изменения}"
echo "Агент 2: {изменения}"
echo "Требуется ручное разрешение"
```

### 8. Переход к следующему уровню

Повторить шаги 4-7 для следующего уровня параллелизма.

---

## Пример сценария

**Spec:** `feature-user-dashboard.md`

**Этапы:**
1. Mock OAuth (файлы: `src/api/routes/oauth_mock.py`)
2. Dashboard Page (файлы: `src/web/dashboard/`, `src/templates/dashboard.html`)
3. Admin Panel (файлы: `src/api/routes/admin.py`)

**Анализ:**
- Этап 1 и Этап 2: ✅ параллельно (разные файлы)
- Этап 1 и Этап 3: ✅ параллельно (разные файлы)
- Этап 2 и Этап 3: ✅ параллельно (разные файлы)

**Результат:** Все 3 этапа на Уровне 0 → запустить 3 агента параллельно

---

## Ограничения

- **Максимум 3 агента** одновременно (настраивается в `ai-settings.json`)
- **Sandbox ограничения:** Субагенты не могут напрямую писать файлы (Write/Edit) из-за безопасности
  - **Workaround:** Агенты возвращают код как текст, главный агент применяет через Write/Edit
  - Real-time apply работает благодаря главному агенту, который применяет изменения мгновенно
- Каждый агент работает в своей ветке: `parallel/{stage-name}/{timestamp}`
- Каждый агент создаёт независимый коммит
- CHANGELOG обновляется только при merge всех этапов

---

## Конфигурация

`.ai/ai-settings.json`:
```json
{
  "parallel": {
    "enabled": true,
    "min_parallel_stages": 2,
    "max_concurrent_agents": 3,
    "conflict_resolution": "git-merge",
    "commit_strategy": "independent",
    "apply_mode": "realtime"
  }
}
```

**Параметр `apply_mode`:**
- `"realtime"` — применять изменения мгновенно по мере завершения агентов (рекомендуется)
- `"batch"` — применять все изменения после завершения всех агентов

---

## Коды возврата

| Код | Значение           | Действие                        |
| --- | ------------------ | ------------------------------- |
| 0   | Успех              | Следующий уровень               |
| 1   | Частичный успех    | Повторить неудачные этапы       |
| 2   | Конфликт merge     | Запросить разрешение у пользователя |
| 3   | Ошибка агента      | Логи + предложение альтернативы  |

---

## Интеграция с другими skills

- **session-loader:** Загружает spec перед параллельным выполнением
- **commit-helper:** Вызывается каждым агентом для коммита
- **merge-helper:** Финальный merge всех параллельных веток

---

## Диагностика

При ошибках проверить:
```bash
# Статус всех параллельных веток
git branch | grep parallel

# Конфликты в текущей ветке
git status

# Логи агентов
ls -la .claude/logs/parallel/
```

---

## Post-Execution Consolidation (Auto-Triggered)

После завершения всех этапов автоматически запускается консолидация сессии:

```python
# В конце parallel-executor, после завершения всех этапов
if all_stages_complete():
    Skill(skill="session-consolidator")
```

### Что делает session-consolidator

1. **Запускает субагента в чистом контексте** — анализ происходит без влияния истории текущей сессии
2. **Собирает историю сессии** — spec, git log, изменения файлов
3. **Анализирует соответствие пайплайну** — проверка выполнения правил из CLAUDE.md
4. **Выявляет неясности** — документы ambiguities и решения
5. **Создаёт отчёт** — `.ai/specs/archive/{branch-name}-session-summary.md`

### Результат консолидации

```
✅ Session consolidation complete

📄 Report: .ai/specs/archive/{branch-name}-session-summary.md
🌿 Branch: {branch-name}
📊 Compliance Score: {X}/10
```

### Конфигурация

Авто-запуск контролируется настройкой в `.ai/ai-settings.json`:

```json
{
  "framework": {
    "session_consolidation": {
      "enabled": true,
      "auto_trigger_after_parallel": true
    }
  }
}
```

Если нужно отключить авто-запуск, установите `auto_trigger_after_parallel: false`.
