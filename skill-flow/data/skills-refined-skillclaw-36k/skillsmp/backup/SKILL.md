---
name: backup
description: Правила работы с резервной копией в приложении
---

# When to Use

- Используй этот навык, когда работаешь с экспортом данных приложения в JSON-файл
- Используй этот навык, когда работаешь с импортом данных из JSON-файла
- Используй этот навык, когда тестируешь резервное копирование (BackupItemTest.kt)
- Используй этот навык, когда реализуешь конвертацию типов (цветов, DisplayOption)
- Используй этот навык, когда работаешь с кроссплатформенной совместимостью (iOS/Android)
- Используй этот навык, когда обрабатываешь ошибки при экспорте/импорте данных
- Этот навык полезен, когда нужно понять формат JSON для обмена данными между устройствами

# Резервное копирование

## Формат JSON

Совместим с iOS-приложением:

```json
[
  {
    "title": "Название события",
    "details": "Описание события",
    "timestamp": 1234567890000,
    "colorTag": "#FFFF00",
    "displayOption": "day"
  }
]
```

## Реализация

**Use Cases:**

- `ExportBackupUseCase`: экспорт в JSON через FilePicker
- `ImportBackupUseCase`: импорт из JSON через FilePicker с предотвращением дубликатов
- `BackupItem`: DTO с kotlinx.serialization

**Конвертация типов:**

- **Цвета:** ARGB (Int) ↔ hex-строка (#RRGGBB), альфа-канал всегда 0xFF
- **Display Option:** enum ↔ camelCase строки (`day`, `monthDay`, `yearMonthDay`)

## Правила

**Экспорт:**

- JSON с prettyPrint через kotlinx.serialization
- Обработка ошибок (IOException, SerializationException, BackupException)

**Импорт:**

- Валидация JSON с игнорированием неизвестных полей
- Проверка дубликатов по title/details/timestamp/displayOption (БЕЗ colorTag)
- Обработка ошибок (FileNotFoundException, IOException, SerializationException, SQLException, BackupException)

**Совместимость с iOS:**

- Цвета из iOS (Data) не поддерживаются → null при импорте
- Кроссплатформенный обмен цветами не работает

## Тестирование

Unit-тесты: `app/src/test/java/com/dayscounter/domain/usecase/BackupItemTest.kt`
