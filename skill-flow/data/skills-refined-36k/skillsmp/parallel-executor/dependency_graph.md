# Dependency Graph Analysis

**Назначение:** Алгоритм определения параллельности этапов на основе анализа файлов.

---

## Входные данные

```yaml
spec_file: .ai/specs/feature-user-dashboard.md

stages:
  - name: "Mock OAuth"
    status: "⬜"
    files:
      - "src/api/routes/oauth_mock.py"
      - "src/api/dependencies.py"

  - name: "Dashboard Page"
    status: "⬜"
    files:
      - "src/web/dashboard/"
      - "src/templates/dashboard.html"

  - name: "Admin Panel"
    status: "⬜"
    files:
      - "src/api/routes/admin.py"
      - "src/api/dependencies.py"  # ← конфликт с Mock OAuth!
```

---

## Алгоритм

### Шаг 1: Извлечение файлов из этапов

```python
def extract_stage_files(spec_content):
    stages = parse_markdown_stages(spec_content)
    stage_files = {}

    for stage in stages:
        if stage.status in ["⬜", "🔄"]:
            files = []
            for line in stage.files_section:
                # Парсинг строк типа "- `path/to/file.py` (создать/изменить)"
                match = re.match(r'-\s*`([^`]+)`', line)
                if match:
                    files.append(match.group(1))
            stage_files[stage.name] = files

    return stage_files
```

**Результат:**
```python
{
    "Mock OAuth": ["src/api/routes/oauth_mock.py", "src/api/dependencies.py"],
    "Dashboard Page": ["src/web/dashboard/", "src/templates/dashboard.html"],
    "Admin Panel": ["src/api/routes/admin.py", "src/api/dependencies.py"]
}
```

### Шаг 2: Построение матрицы конфликтов

```python
def build_conflict_matrix(stage_files):
    stages = list(stage_files.keys())
    n = len(stages)
    matrix = [[False] * n for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            files_i = set(stage_files[stages[i]])
            files_j = set(stage_files[stages[j]])

            # Конфликт = пересечение файлов непусто
            has_conflict = bool(files_i & files_j)
            matrix[i][j] = has_conflict
            matrix[j][i] = has_conflict  # симметрично

    return matrix, stages
```

**Результат:**
```
              Mock OAuth  Dashboard  Admin Panel
Mock OAuth       [ - ]        [ ✅ ]       [ ❌ ]
Dashboard Page   [ ✅ ]       [ - ]        [ ✅ ]
Admin Panel      [ ❌ ]       [ ✅ ]        [ - ]

✅ = можно параллельно (нет конфликта)
❌ = конфликт (общие файлы)
```

### Шаг 3: Построение графа зависимостей

```python
def build_dependency_graph(conflict_matrix, stages):
    # Узел = этап, Ребро = конфликт (не могут быть параллельны)
    graph = {stage: [] for stage in stages}

    for i in range(len(stages)):
        for j in range(i + 1, len(stages)):
            if conflict_matrix[i][j]:
                # Конфликт → добавляем зависимость
                graph[stages[i]].append(stages[j])
                graph[stages[j]].append(stages[i])

    return graph
```

**Результат:**
```python
{
    "Mock OAuth": ["Admin Panel"],      # конфликт с Admin Panel
    "Dashboard Page": [],               # ни с кем не конфликтует
    "Admin Panel": ["Mock OAuth"]       # конфликт с Mock OAuth
}
```

### Шаг 4: Топологическая сортировка по уровням

```python
def compute_parallel_levels(graph):
    # Используем раскраску графа для определения независимых множеств
    levels = []
    remaining = set(graph.keys())

    while remaining:
        # Найти вершины без зависимостей внутри remaining
        current_level = []
        for stage in remaining:
            dependencies = graph[stage]
            # Проверяем, что все зависимости уже выполнены
            if not any(dep in remaining for dep in dependencies):
                current_level.append(stage)

        if not current_level:
            # Циклическая зависимость - невозможно параллелить
            raise ValueError("Cyclic dependency detected")

        levels.append(current_level)

        # Удаляем выполненные этапы
        for stage in current_level:
            remaining.remove(stage)

    return levels
```

**Результат:**
```python
[
    ["Mock OAuth", "Dashboard Page"],  # Уровень 0 - параллельно
    ["Admin Panel"]                     # Уровень 1 - после Mock OAuth
]
```

### Шаг 5: Визуализация

```
┌─────────────────────────────────────────────────────────┐
│                  УРОВЕНЬ 0 (Parallel)                   │
├───────────────────────┬─────────────────────────────────┤
│   Mock OAuth          │   Dashboard Page                │
│   src/api/routes/     │   src/web/dashboard/            │
│   oauth_mock.py       │   src/templates/dashboard.html  │
│   src/api/            │                                 │
│   dependencies.py     │                                 │
└───────────────────────┴─────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  УРОВЕНЬ 1 (Sequential)                 │
├───────────────────────┬─────────────────────────────────┤
│   Admin Panel          │   (зависит от Mock OAuth)      │
│   src/api/routes/     │   конфликт: dependencies.py     │
│   admin.py            │                                 │
│   src/api/            │                                 │
│   dependencies.py     │                                 │
└───────────────────────┴─────────────────────────────────┘
```

---

## Крайние случаи

### Случай 1: Полная независимость

```yaml
stages:
  - name: "Frontend"
    files: ["src/frontend/"]
  - name: "Backend"
    files: ["src/backend/"]
  - name: "Tests"
    files: ["tests/"]
```

**Результат:** Уровень 0 = ["Frontend", "Backend", "Tests"] → 3 агента параллельно

### Случай 2: Полная зависимость

```yaml
stages:
  - name: "Database"
    files: ["src/db/models.py"]
  - name: "API"
    files: ["src/db/models.py", "src/api/"]
  - name: "Frontend"
    files: ["src/api/", "src/frontend/"]
```

**Результат:**
```
Уровень 0: ["Database"]
Уровень 1: ["API"]       (ждёт Database)
Уровень 2: ["Frontend"]  (ждёт API)
```

### Случай 3: Циклическая зависимость (ошибка)

```yaml
stages:
  - name: "A"
    files: ["shared.py", "a.py"]
  - name: "B"
    files: ["shared.py", "b.py"]
  - name: "C"
    files: ["a.py", "b.py"]  # зависит и от A, и от B
```

**Результат:** Ошибка "Cyclic dependency detected" → выполнить последовательно

---

## Оптимизация

### Эвристика: Размер файлов

Если два этапа конфликтуют, но изменения маленькие:
```python
def can_merge_small_changes(stage1, stage2):
    # Если < 50 строк в сумме → можно выполнить в одном коммите
    return estimate_lines(stage1) + estimate_lines(stage2) < 50
```

### Эвристика: Типы файлов

Некоторые типы файлов безопасны для параллели:
```python
SAFE_PARALLEL_TYPES = {
    ".test.py",     # тесты
    ".spec.ts",     # типы TypeScript
    ".md",          # документация
}

def is_safe_parallel(file1, file2):
    return all(
        any(f.endswith(ext) for ext in SAFE_PARALLEL_TYPES)
        for f in [file1, file2]
    )
```

---

## Интеграция с SKILL.md

```python
# В начале parallel-executor
stage_files = extract_stage_files(spec_content)
conflict_matrix, stages = build_conflict_matrix(stage_files)
graph = build_dependency_graph(conflict_matrix, stages)
levels = compute_parallel_levels(graph)

# Для каждого уровня...
for level in levels:
    launch_parallel_agents(level)
```

---

## Сложность

| Алгоритм                | Сложность   | Комментарий                          |
| ----------------------- | ----------- | ------------------------------------ |
| Извлечение файлов       | O(S × F)    | S = этапов, F = файлов в этапе       |
| Матрица конфликтов      | O(S² × F)   | попарное сравнение                   |
| Топологическая сортировка | O(S + E)   | E = рёбер (конфликтов)               |
| **Итого**               | O(S² × F)   | для S ≤ 10, F ≤ 20 — пренебрежимо   |

---

## Тестирование

```python
# Тест 1: Полная независимость
assert parallel_levels(
    {"A": ["a.py"], "B": ["b.py"], "C": ["c.py"]}
) == [["A", "B", "C"]]

# Тест 2: Полная зависимость
assert parallel_levels(
    {"A": ["shared.py"], "B": ["shared.py", "b.py"]}
) == [["A"], ["B"]]

# Тест 3: Смешанная
assert parallel_levels(
    {"A": ["a.py"], "B": ["b.py"], "C": ["a.py", "b.py"]}
) in [
    [["A", "B"], ["C"]],
    [["B", "A"], ["C"]],
]
```
