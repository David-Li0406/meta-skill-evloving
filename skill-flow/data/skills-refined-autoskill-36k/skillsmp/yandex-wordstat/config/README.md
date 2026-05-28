# Получение токена Yandex Wordstat API

Wordstat API бесплатный с июня 2025. Лимиты: 1000 запросов/день, 10 запросов/сек.

## Шаг 1: Запросите доступ к API

1. Перейдите на https://yandex.ru/support2/wordstat/ru/content/api-wordstat
2. Прочитайте инструкцию
3. **Внизу страницы заполните и отправьте форму** для разблокировки API
4. Дождитесь одобрения (обычно в течение дня)

## Шаг 2: Получите OAuth токен

После одобрения доступа откройте в браузере:

```
https://oauth.yandex.ru/authorize?response_type=token&client_id=ВАШ_CLIENT_ID
```

Замените `ВАШ_CLIENT_ID` на ID вашего приложения.

После авторизации токен будет в URL:
```
https://oauth.yandex.ru/#access_token=ВАШТОКЕН&token_type=bearer&expires_in=31536000
```

Скопируйте значение `access_token`.

## Шаг 3: Настройте токен

Создайте файл `.env` в папке `config/`:

```bash
cp config/.env.example config/.env
```

Вставьте токен:

```
YANDEX_WORDSTAT_TOKEN=ваш_токен_здесь
```

## Проверка

```bash
bash scripts/quota.sh
```

Должно показать "Wordstat API: OK".

## Частые проблемы

### "Authorization error" (код 53)
- Не отправили форму на странице Wordstat → отправьте и дождитесь одобрения
- Токен устарел → получите новый
- Токен от другого приложения → используйте правильный client_id

### Методы недоступны
- Доступ к API ещё не одобрен → дождитесь письма от Яндекса

## Лимиты

- **10 запросов в секунду**
- **1000 запросов в день**

## Срок жизни токена

Токен действует **1 год**. После истечения получите новый по той же ссылке.

## Документация

- Wordstat API: https://yandex.ru/support2/wordstat/ru/content/api-wordstat
- Структура API: https://yandex.ru/support2/wordstat/ru/content/api-structure
- Операторы: https://yandex.ru/support/direct/keywords/symbols-and-operators.html
