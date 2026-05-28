---
name: js-safe-dom
description: Написання безпечного, продуктивного JavaScript коду для маніпуляцій з DOM. Використовуй для інтерактивності.
version: 1.0.0
---

# Безпечні маніпуляції DOM

## Правила

1. **Селектори**: Використовуй `document.getElementById` для ID (швидкодія) та `querySelector` для класів.
2. **Модифікація контенту**:
   - **ЗАБОРОНЕНО**: `innerHTML` при вставці даних користувача (ризик XSS).
   - **РЕКОМЕНДОВАНО**: `textContent` для тексту, `classList` для стилів.
   - Для створення складних структур використовуй `document.createElement` та `appendChild` або шаблони `<template>`.
3. **Події**:
   - Використовуй іменовані функції для обробників подій, щоб мати можливість їх видалити (`removeEventListener`).
   - Застосовуй делегування подій (Event Delegation) для списків та динамічних елементів.

## Доступність (WCAG 2.2)

1. **Dragging Movements (2.5.7)**: Якщо ти імплементуєш Drag-and-Drop (наприклад, сортування списку), ти ОБОВ'ЯЗКОВО повинен додати кнопки "Вгору"/"Вниз" або контекстне меню для зміни порядку без перетягування (single pointer alternative).

## Шаблон безпечного слухача

```javascript
const btn = document.getElementById("action-btn");
if (btn) {
  btn.addEventListener("click", handleClick);
}

function handleClick(event) {
  // логіка
}
```
