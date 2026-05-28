# Примеры локализации

## Простые строки

### Добавление новой строки

```xml
<!-- res/values/strings.xml -->
<string name="welcome">Добро пожаловать в Days Counter</string>

<!-- res/values-en/strings.xml -->
<string name="welcome">Welcome to Days Counter</string>
```

### Использование в коде

```kotlin
// В Activity/Fragment
val welcomeText = getString(R.string.welcome)
textView.text = welcomeText

// В XML
<TextView
    android:layout_width="wrap_content"
    android:layout_height="wrap_content"
    android:text="@string/welcome" />
```

## Множественное число (Plurals)

### Пример для "день/дня/дней"

```xml
<!-- res/values/strings.xml -->
<plurals name="days_count">
    <item quantity="one">%d день</item>
    <item quantity="few">%d дня</item>
    <item quantity="many">%d дней</item>
    <item quantity="other">%d дней</item>
</plurals>

<!-- res/values-en/strings.xml -->
<plurals name="days_count">
    <item quantity="one">%d day</item>
    <item quantity="other">%d days</item>
</plurals>
```

### Использование в коде

```kotlin
// Пример 1: Прямое использование
val days = 5
val text = resources.getQuantityString(R.plurals.days_count, days, days)
// Результат: "5 дней" (ru) или "5 days" (en)

// Пример 2: В функции форматирования
fun formatDaysCount(days: Int): String {
    return resources.getQuantityString(R.plurals.days_count, days, days)
}

// Пример 3: В ViewModel (через ResourceProvider)
class DaysFormatter(private val resourceProvider: ResourceProvider) {
    fun formatDays(days: Int): String {
        return resourceProvider.getQuantityString(R.plurals.days_count, days, days)
    }
}
```

## Форматирование строк

### Одно значение

```xml
<!-- res/values/strings.xml -->
<string name="days_from_date">%s дней с %s</string>

<!-- res/values-en/strings.xml -->
<string name="days_from_date">%s days from %s</string>
```

```kotlin
val days = "42"
val date = "2024-01-01"
val text = getString(R.string.days_from_date, days, date)
// Результат: "42 дня с 2024-01-01"
```

### Несколько значений разного типа

```xml
<!-- res/values/strings.xml -->
<string name="item_summary">%1$s (%2$d дней, цвет: %3$s)</string>

<!-- res/values-en/strings.xml -->
<string name="item_summary">%1$s (%2$d days, color: %3$s)</string>
```

```kotlin
val title = "Мой день"
val days = 42
val color = "#FFFF00"
val text = getString(R.string.item_summary, title, days, color)
// Результат: "Мой день (42 дня, цвет: #FFFF00)"
```

## Форматирование дат

### Локализованное форматирование

```kotlin
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.time.format.FormatStyle

val date = LocalDate.now()
val formatter = DateTimeFormatter.ofLocalizedDate(FormatStyle.MEDIUM)
val formattedDate = date.format(formatter)
// Результат: "15 янв. 2024 г." (ru) или "Jan 15, 2024" (en)

// Стиль LONG: "15 января 2024 г." (ru) или "January 15, 2024" (en)
// Стиль SHORT: "15.01.2024" (ru) или "1/15/24" (en)
```

### Кастомное форматирование

```kotlin
val date = LocalDate.now()
val formatter = DateTimeFormatter.ofPattern("dd MMMM yyyy")
val formattedDate = date.format(formatter)
// Результат: "15 января 2024"
```

## Организация ресурсов с префиксами

### Пример группировки

```xml
<!-- Общие строки -->
<string name="common_ok">ОК</string>
<string name="common_cancel">Отмена</string>
<string name="common_save">Сохранить</string>
<string name="common_delete">Удалить</string>
<string name="common_edit">Редактировать</string>
<string name="common_back">Назад</string>
<string name="common_error">Ошибка</string>

<!-- Строки для экрана списка -->
<string name="list_title">Счетчики</string>
<string name="list_empty">Нет счетчиков. Нажмите + чтобы добавить.</string>
<string name="list_search">Поиск</string>

<!-- Строки для экрана деталей -->
<string name="detail_title">Детали</string>
<string name="detail_days">Дней прошло</string>
<string name="detail_today">Сегодня</string>

<!-- Строки для экрана создания/редактирования -->
<string name="create_title">Новый счетчик</string>
<string name="edit_title">Редактировать счетчик</string>
<string name="edit_title_hint">Название</string>
<string name="edit_details_hint">Описание</string>
<string name="edit_date_hint">Дата</string>

<!-- Строки для настроек -->
<string name="settings_title">Настройки</string>
<string name="settings_theme">Тема оформления</string>
<string name="settings_icon">Иконка приложения</string>
<string name="settings_backup">Резервное копирование</string>
```

## Локализованные сообщения об ошибках

### Сетевые ошибки (не применимо в JetpackDays, но для примера)

```xml
<string name="error_network">Ошибка сети. Проверьте подключение к интернету.</string>
<string name="error_timeout">Время ожидания истекло. Попробуйте еще раз.</string>
```

### Ошибки импорта/экспорта

```xml
<!-- Ошибки экспорта -->
<string name="error_export_failed">Не удалось экспортировать данные</string>
<string name="error_export_permission">Нет разрешения на запись файлов</string>

<!-- Ошибки импорта -->
<string name="error_import_failed">Не удалось импортировать данные</string>
<string name="error_invalid_format">Неверный формат файла</string>
<string name="error_duplicate_item">Элемент с таким названием уже существует</string>
```

### Ошибки валидации

```xml
<string name="error_empty_title">Название не может быть пустым</string>
<string name="error_invalid_date">Неверная дата</string>
<string name="error_title_too_long">Название слишком длинное</string>
```

### Использование в коде

```kotlin
fun exportBackup(uri: Uri) {
    try {
        val jsonData = exportBackupUseCase()
        contentResolver.openOutputStream(uri)?.use { outputStream ->
            outputStream.write(jsonData.toByteArray())
        }
        Log.i(TAG, "Резервная копия создана успешно")
    } catch (e: IOException) {
        Log.e(TAG, "Ошибка экспорта данных: ${e.message}")
        _uiState.value = BackupUiState.Error(
            message = getString(R.string.error_export_failed)
        )
    }
}

fun importBackup(uri: Uri) {
    try {
        val jsonData = contentResolver.openInputStream(uri)?.use { inputStream ->
            inputStream.bufferedReader().readText()
        } ?: throw IOException("Не удалось прочитать файл")

        importBackupUseCase(jsonData)
        Log.i(TAG, "Импорт данных завершен успешно")
    } catch (e: SerializationException) {
        Log.e(TAG, "Ошибка десериализации: ${e.message}")
        _uiState.value = BackupUiState.Error(
            message = getString(R.string.error_invalid_format)
        )
    } catch (e: SQLException) {
        Log.e(TAG, "Ошибка базы данных: ${e.message}")
        _uiState.value = BackupUiState.Error(
            message = getString(R.string.error_import_failed)
        )
    }
}
```

## Логирование

**Важно:** Все логи пишутся на русском языке

```kotlin
// Правильно
Log.e(TAG, "Ошибка загрузки данных: ${error.message}")
Log.i(TAG, "Загружено $count элементов")
Log.d(TAG, "Начинаем экспорт данных")

// Неправильно
Log.e(TAG, "Error loading data: ${error.message}")
Log.i(TAG, "Loaded $count items")
Log.d(TAG, "Starting data export")
```

## Работа с ResourceProvider в проекте JetpackDays

В JetpackDays используется `ResourceProvider` для доступа к строковым ресурсам:

```kotlin
class DaysFormatter(
    private val resourceProvider: ResourceProvider
) {
    fun formatDaysText(daysDifference: DaysDifference): String {
        val days = daysDifference.days

        return when {
            days == 0L -> resourceProvider.getString(R.string.today)
            days == 1L -> resourceProvider.getString(R.string.yesterday)
            days == -1L -> resourceProvider.getString(R.string.tomorrow)
            days > 0 -> resourceProvider.getQuantityString(
                R.plurals.days_ago,
                days.toInt(),
                days
            )
            else -> resourceProvider.getQuantityString(
                R.plurals.days_until,
                abs(days).toInt(),
                abs(days)
            )
        }
    }
}
```

## Чек-лист проверки

Перед коммитом изменений в локализации:

- [ ] Добавлены строки в оба файла (ru и en)
- [ ] Имена строк уникальны
- [ ] Имена строк соответствуют конвенции (lowercase_with_underscores)
- [ ] Использованы префиксы для группировки
- [ ] Plurals определены корректно для обоих языков
- [ ] Параметры форматирования совпадают по количеству и типу
- [ ] Логи на русском языке
- [ ] Проверено на обоих языках устройства (если возможно)
