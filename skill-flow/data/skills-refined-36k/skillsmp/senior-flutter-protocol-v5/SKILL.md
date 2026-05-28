---
name: senior-flutter-protocol-v5
description: Enterprise-level rules for Melos/Mason project structure (Core, Common, Package)
---

# 🛡 Senior Flutter Engineering Protocol (V5 Enterprise)

## 0. Project Context & Awareness (MANDATORY)
Перед генерацией кода агент ОБЯЗАН просканировать структуру проекта:
- **Core Library (`lib/core/`):**
    - `error/` — используй для моделей Failure.
    - `router/` — используй для навигации.
    - `di/` — используй для инъекции зависимостей.
    - `theme/`, `constants/`, `extensions/` — используй для UI и стилизации.
- **Common Components (`lib/common/`):** Сначала ищи готовые виджеты здесь (dialogs, timer, food_card). ❌ Запрещено дублировать существующие компоненты.
- **Packages:** Проект использует Melos. Изменения в `package/rest_client` или `storage` должны быть изолированы.
- **Automation:** Проверь `mason.yaml` и `Makefile` перед созданием новых модулей.

## 1. Architecture (HARD RULES)
- **Dependency Flow:** `Presentation → Domain ← Data`. (Strict)
- **Layer Isolation:**
    - ❌ `flutter/*`, `dio` или сторонние SDK внутри `domain`.
    - ❌ `BuildContext` внутри Cubit/Bloc/Repository/Service.
    - ✅ **Domain = Pure Dart.** Бизнес-логика только в UseCase или Cubit.
- **Contract-First:** Репозитории в Domain — это интерфейсы (`abstract class`). Реализация — в Data.

## 2. State Management (Bloc/Cubit)
- **Single Source of Truth:** Весь стейт хранится ТОЛЬКО в классе `State`.
- **Immutability:** Все State: `sealed`, `final`, immutable. Обновление только через `copyWith`.
- ❌ **No Hidden State:** Запрещены `late` переменные и приватные поля внутри Cubit/Bloc.
- **State Design:** Состояние должно быть явным (Initial, Loading, Success, Failure).

## 3. UI & Performance (Custom Kit)
- **UI Kit First:** ❌ Запрещено использовать базовые виджеты (ElevatedButton и т.д.), если есть проектные аналоги в `common/` или `core/`.
- **Decomposition:** `build()` > 40 строк → Extract to `const StatelessWidget`.
- ❌ **No Logic in UI:** В `build()` и `onPressed` запрещены вычисления и условия (`if/else`).
- ✅ **Intent Pattern:** `onPressed` только уведомляет логику: `cubit.onAction()`.

## 4. Side Effects & Navigation
- **Navigation:** Только через `lib/core/router/`. Логика не знает о маршрутах.
- **Side Effects:** Snackbar, Dialog, Toast — это **Effect**. Cubit эмитит `Effect`, UI слушает через `BlocListener`.

## 5. Error Handling & Data Flow
- **Data Layer:** `try-catch` (Dio/Storage) → маппинг в Failure из `lib