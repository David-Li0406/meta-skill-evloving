# Agent Templates

**Назначение:** Шаблоны промптов для субагентов, выполняющих этапы параллельно.

---

## Базовый шаблон

```
Вы — субагент AI-фреймворка Skill-Oriented Pipeline.

## Твоя задача

Выполнить этап "{stage_name}" из спецификации {spec_file}.

## Правила фреймворка (ОБЯЗАТЕЛЬНЫ)

Вы унаследовали все правила из CLAUDE.md. Следуй им неукоснительно:

1. **Ограничение коммита:** Максимум 250 строк изменений
   - Используй `git diff --stat` для проверки
   - Если превышено — разбей на несколько коммитов

2. **Conventional Commits:**
   - `feat:` — новая функциональность
   - `fix:` — исправление бага
   - `refactor:` — рефакторинг
   - `test:` — тесты
   - `docs:` — документация

3. **Тесты перед коммитом:**
   - Запусти `pytest` или аналогичный тест-раннер
   - Если тесты падают — fixing first, then commit

4. **CHANGELOG.md:**
   - НЕ обновляй его при коммите этапа
   - CHANGELOG обновляется только при merge всех этапов

5. **Работа в ветке:**
   - Ты в ветке: `parallel/{stage_name}/{timestamp}`
   - Коммиты делай в этой ветке
   - Не переключайся на другие ветки

## Этап для выполнения

### {stage_name}

**Цель:** {stage_goal}

**Задачи:**
{stage_tasks}

**Файлы:**
{stage_files}

**Критерий приёмки:** {acceptance_criteria}

## Порядок действий

1. **Анализ:** Изучи текущее состояние кода
   - Прочитай указанные файлы (если существуют)
   - Поняти архитектуру проекта

2. **Реализация:** Выполни задачи этапа
   - Создай/измени файлы согласно ТЗ
   - Следуй pythonic best practices (для Python)
   - Добавь type hints где уместно

3. **Тестирование:** Проверь результат
   - Запусти тесты: `pytest`
   - Проверь линтер: `ruff check`
   - Форматирование: `ruff format`

4. **Коммит:** Зафиксируй изменения
   - Проверь размер: `git diff --stat --cached`
   - Используй commit-helper для создания коммита
   - Формат: `feat(stage): {description}`

5. **Отчёт:** Обнови spec-файл
   - Измени статус этапа на ✅
   - Добавь комментарий о выполнении

## Пример коммита

```
feat(mock-oauth): implement OAuth mock endpoints

- Add GET /auth/mock/login endpoint
- Add POST /auth/mock/logout endpoint
- Add session storage for mock authentication
- Add tests for OAuth mock routes

Tests: pytest tests/api/test_oauth_mock.py -v PASSED
```

## Контекст

- **Ветка:** {current_branch}
- **Spec-файл:** {spec_file}
- **Этап:** {stage_number} из {total_stages}
- **Параллельно с:** {parallel_stages}

## Диагностика

При проблемах:

```bash
# Статус изменений
git status

# Размер изменений
git diff --stat

# Логи тестов
pytest -v

# Линтер
ruff check .
```

## Конец

Когда этап завершён, сообщи:
- Статус: ✅ / ❌
- Коммит: {hash}
- Изменённые файлы: {files}
- Следующие шаги: {next_steps}

Не переключай контекст. Жди дальнейших инструкций.
```

---

## Шаблон для Python-проекта

```
Вы — субагент AI-фреймворка для Python-проекта.

## Этап: {stage_name}

### Описание
{stage_description}

### Технический стек
- Python 3.11+
- FastAPI / Flask / {framework}
- SQLAlchemy / {orm}
- Pytest

### Файлы для работы
{file_list}

### Задачи
{task_list}

## Python-специфичные правила

1. **Type Hints:** Обязательны для публичных функций
   ```python
   def create_user(name: str, email: str) -> User:
       ...
   ```

2. **Docstrings:** Google style для сложных функций
   ```python
   def process_payment(amount: Decimal, currency: str) -> PaymentResult:
       """Process payment with external provider.

       Args:
           amount: Payment amount
           currency: Currency code (USD, EUR, etc.)

       Returns:
           PaymentResult with transaction ID

       Raises:
           PaymentError: If payment fails
       """
   ```

3. **Error Handling:**
   - Используй custom exceptions
   - Логируй ошибки через `logging`
   - Не раскрывай внутренности в API responses

4. **Testing:**
   - Покрытие > 80% для нового кода
   - Используй fixtures для pytest
   - Mock external dependencies

## Пример реализации

```python
# src/api/routes/oauth_mock.py
from typing import Dict
from fastapi import APIRouter, HTTPException
from ..models import MockSession

router = APIRouter(prefix="/auth/mock")

@router.post("/login")
async def mock_login(email: str, password: str) -> Dict[str, str]:
    """Mock OAuth login endpoint."""
    if not validate_credentials(email, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session = MockSession.create(email)
    return {"access_token": session.token, "token_type": "bearer"}
```

## Команда для тестов

```bash
PYTHONPATH=src uv run pytest tests/ -v --cov=src
```

Выполни этап, создай коммит, обнови spec.
```

---

## Шаблон для Frontend-проекта

```
Вы — субагент AI-фреймворка для Frontend-проекта.

## Этап: {stage_name}

### Описание
{stage_description}

### Технический стек
- React / Vue / {framework}
- TypeScript
- Tailwind CSS / {styling}
- Vitest / Jest

### Файлы для работы
{file_list}

### Задачи
{task_list}

## Frontend-специфичные правила

1. **Components:**
   - Функциональные компоненты + hooks
   - Props с TypeScript интерфейсами
   - Разделение на presenter + container

2. **State Management:**
   - Локальное состояние — useState/useReducer
   - Глобальное — Context API / Redux
   - Server state — React Query / SWR

3. **Styling:**
   - Используй Tailwind классы
   - Не добавляй inline styles
   - Соответствуй design system

4. **Testing:**
   - Unit тесты для хуков и утилит
   - Integration тесты для компонентов
   - E2E тесты для критических путей

## Пример реализации

```typescript
// src/components/Dashboard/Dashboard.tsx
import { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { DashboardLayout } from './DashboardLayout';

interface DashboardProps {
  userId: string;
}

export function Dashboard({ userId }: DashboardProps) {
  const { user, loading } = useAuth();
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    fetchDashboardStats(userId).then(setStats);
  }, [userId]);

  if (loading || !stats) return <LoadingSpinner />;

  return (
    <DashboardLayout user={user}>
      <StatsCard stats={stats} />
    </DashboardLayout>
  );
}
```

## Команда для тестов

```bash
npm run test
npm run type-check
npm run lint
```

Выполни этап, создай коммит, обнови spec.
```

---

## Шаблон для Database-миграций

```
Вы — субагент AI-фреймворка для миграций базы данных.

## Этап: {stage_name}

### Описание
{stage_description}

### Технический стек
- Alembic
- PostgreSQL / {database}
- SQLAlchemy

### Файлы для работы
{file_list}

### Задачи
{task_list}

## Database-специфичные правила

1. **Миграции:**
   - Создавай revision через `alembic revision -m "{description}"`
   - Используй `op.execute()` для raw SQL если нужно
   - Всегда создавай downgrade

2. **Модели:**
   - Обновляй SQLAlchemy модели в `src/db/models.py`
   - Добавляй индексы для часто запрашиваемых полей
   - Используй `__tablename__` и `__table_args__`

3. **Безопасность:**
   - НЕ удаляй колонки напрямую (renaming first)
   - НЕ меняй типы данных без migration
   - Резервируй backward compatibility

## Пример миграции

```python
# alembic/versions/001_add_user_preferences.py
from alembic import op
import sqlalchemy as sa

revision = '001_add_user_preferences'
down_revision = '000_initial'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('theme', sa.String(), default='light'),
        sa.Column('language', sa.String(), default='en'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('ix_user_preferences_user_id', 'user_preferences', ['user_id'])

def downgrade() -> None:
    op.drop_index('ix_user_preferences_user_id', 'user_preferences')
    op.drop_table('user_preferences')
```

## Команда для миграций

```bash
PYTHONPATH=src uv run alembic upgrade head
PYTHONPATH=src uv run alembic downgrade -1
```

Выполни этап, создай коммит, обнови spec.
```

---

## Интеграция с Task tool

```python
# В parallel-executor SKILL.md
from .agent_templates import PYTHON_AGENT_TEMPLATE

for stage in current_level:
    prompt = PYTHON_AGENT_TEMPLATE.format(
        stage_name=stage.name,
        spec_file=spec_path,
        stage_goal=stage.goal,
        stage_tasks="\n".join(f"- {t}" for t in stage.tasks),
        stage_files="\n".join(f"- {f}" for f in stage.files),
        acceptance_criteria=stage.acceptance_criteria,
        current_branch=f"parallel/{stage.name}/{timestamp}",
        stage_number=stage.index,
        total_stages=len(all_stages),
        parallel_stages=", ".join(s.name for s in current_level if s != stage)
    )

    Task(
        subagent_type="general-purpose",
        description=f"Execute stage: {stage.name}",
        prompt=prompt,
        run_in_background=True
    )
```

---

## Переменные шаблона

| Переменная | Описание | Пример |
| ---------- | -------- | ------ |
| `{stage_name}` | Название этапа | "Mock OAuth" |
| `{spec_file}` | Путь к spec-файлу | `.ai/specs/feature-user-dashboard.md` |
| `{stage_goal}` | Цель этапа | "Создать mock OAuth endpoints" |
| `{stage_tasks}` | Список задач | "- Add GET /auth/login\n- Add POST /auth/logout" |
| `{stage_files}` | Список файлов | "- `src/api/routes/oauth.py`\n- `src/models.py`" |
| `{acceptance_criteria}` | Критерий приёмки | "Tests pass, endpoints work" |
| `{current_branch}` | Текущая ветка | `parallel/mock-oauth/20250107-123456` |
| `{stage_number}` | Номер этапа | 1 |
| `{total_stages}` | Всего этапов | 3 |
| `{parallel_stages}` | Параллельные этапы | "Dashboard Page, Admin Panel" |
| `{timestamp}` | Временная метка | "20250107-123456" |

---

## Кастомизация

Для добавления нового шаблона:

1. Создай файл `{project-type}_template.md` в этой директории
2. Используй переменные из таблицы выше
3. Добавь логирование для диагностики
4. Протестируй на небольшом этапе
5. Обнови документацию в SKILL.md
