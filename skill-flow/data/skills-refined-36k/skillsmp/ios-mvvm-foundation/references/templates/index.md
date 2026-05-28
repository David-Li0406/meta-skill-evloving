# Templates

> Code generation templates cho MVVM components.

---

## 📁 Available Templates

| Template | Description | Use When |
|----------|-------------|----------|
| [mvvm-screen.md](mvvm-screen.md) | Complete screen với ViewModel + View | Tạo feature mới |
| [viewmodel.md](viewmodel.md) | Standalone ViewModel | ViewModel riêng lẻ |
| [repository.md](repository.md) | Repository protocol + implementation | Data access layer |
| [usecase.md](usecase.md) | UseCase protocol + implementation | Domain logic |
| [navigator.md](navigator.md) | Navigation patterns | Navigation setup |
| [theme-manager.md](theme-manager.md) | Theme system setup | Theming |

---

## 🚀 Quick Usage

### Tạo Feature Mới

1. Copy template từ [mvvm-screen.md](mvvm-screen.md)
2. Replace placeholders:
   - `{Feature}` → `Login`, `Profile`, etc.
   - `{featureLower}` → `login`, `profile`, etc.
3. Adjust theo requirements

### Placeholder Convention

| Placeholder | Example | Description |
|-------------|---------|-------------|
| `{Feature}` | `Login` | PascalCase feature name |
| `{featureLower}` | `login` | camelCase feature name |
| `{ENTITY}` | `User` | Domain entity name |
| `{ACTION}` | `Create`, `Fetch` | UseCase action |

---

## 📋 Template Selection Guide

```
What are you building?
    ├── New screen → mvvm-screen.md
    ├── Data access → repository.md
    ├── Business logic → usecase.md
    ├── Navigation → navigator.md
    └── Theming → theme-manager.md
```
