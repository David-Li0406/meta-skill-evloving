#!/usr/bin/env python3
"""
Web scraping через scrape.do API
Использует токен из локального файла config/token.txt или переменной окружения SCRAPEDO_TOKEN
"""

import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from typing import Optional
from pathlib import Path


def get_token() -> Optional[str]:
    """
    Получает токен Scrape.do из различных источников.
    
    Приоритет:
    1. Локальный файл config/token.txt в директории skill'а
    2. Переменная окружения SCRAPEDO_TOKEN
    3. Файл .env в директории skill'а
    
    Returns:
        Токен или None если не найден
    """
    # Определяем путь к директории скрипта
    script_dir = Path(__file__).parent.parent  # Поднимаемся на уровень skill'а
    
    # Вариант 1: config/token.txt
    token_file = script_dir / 'config' / 'token.txt'
    if token_file.exists():
        try:
            token = token_file.read_text().strip()
            if token:
                return token
        except Exception:
            pass
    
    # Вариант 2: Переменная окружения SCRAPEDO_TOKEN
    token = os.environ.get('SCRAPEDO_TOKEN')
    if token:
        return token
    
    # Вариант 3: .env файл
    env_file = script_dir / '.env'
    if env_file.exists():
        try:
            for line in env_file.read_text().splitlines():
                if line.startswith('SCRAPEDO_TOKEN='):
                    token = line.split('=', 1)[1].strip().strip('"').strip("'")
                    if token:
                        return token
        except Exception:
            pass
    
    return None


def extract_text_from_html(html: str) -> str:
    """
    Извлекает текстовое содержимое из HTML.
    
    Args:
        html: HTML строка
        
    Returns:
        Извлеченный текст
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # Удаляем скрипты и стили
    for element in soup(['script', 'style', 'noscript']):
        element.decompose()
    
    # Получаем текст
    text = soup.get_text(separator='\n', strip=True)
    
    # Убираем избыточные пробелы и пустые строки
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    
    return '\n'.join(lines)


def fetch_via_scrapedo(url: str, token: Optional[str] = None) -> dict:
    """
    Делает запрос к Scrape.do API для скрапинга сайта.
    
    Args:
        url: URL для скрапинга
        token: Токен Scrape.do (если не передан, берется автоматически)
        
    Returns:
        Словарь с результатом:
        - success: bool - успешность операции
        - content: str - извлеченный контент или ошибка
        - html: str - оригинальный HTML (если успешно)
    """
    # Получаем токен
    if token is None:
        token = get_token()
    
    if not token:
        script_dir = Path(__file__).parent.parent
        return {
            'success': False,
            'content': f'Ошибка: Не найден токен Scrape.do. Создайте файл {script_dir}/config/token.txt с вашим токеном или установите переменную окружения SCRAPEDO_TOKEN'
        }
    
    # Формируем запрос (requests сам кодирует параметры)
    base_api = 'http://api.scrape.do'
    params = {
        'token': token,
        'url': url
    }
    
    try:
        # Делаем запрос
        response = requests.get(
            base_api,
            params=params,
            timeout=30,
            headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                'Accept-Encoding': 'gzip, deflate',
            }
        )
        
        # Обрабатываем ошибки API
        if response.status_code == 401:
            return {
                'success': False,
                'content': 'Ошибка: Неверный токен Scrape.do или сервис заблокирован'
            }
        
        if response.status_code == 429:
            return {
                'success': False,
                'content': 'Ошибка: Превышен лимит запросов Scrape.do'
            }
        
        # Проверяем статус
        response.raise_for_status()
        
        # Извлекаем HTML
        html_content = response.text
        
        # Извлекаем текст
        text_content = extract_text_from_html(html_content)
        
        return {
            'success': True,
            'content': text_content,
            'html': html_content
        }
        
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'content': f'Ошибка: Таймаут при запросе к {url}'
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'content': f'Ошибка при запросе: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'content': f'Неожиданная ошибка: {str(e)}'
        }


def main():
    """CLI интерфейс для скрипта"""
    parser = argparse.ArgumentParser(
        description='Скрапинг веб-страниц через Scrape.do API'
    )
    parser.add_argument('url', help='URL для скрапинга')
    parser.add_argument(
        '--html',
        action='store_true',
        help='Вернуть HTML вместо извлеченного текста'
    )
    parser.add_argument(
        '--token',
        help='Токен Scrape.do (по умолчанию из GLOBAL_SYSTEM_SCRAPEDO_TOKEN)'
    )
    
    args = parser.parse_args()
    
    # Выполняем скрапинг
    result = fetch_via_scrapedo(args.url, args.token)
    
    if not result['success']:
        print(result['content'], file=sys.stderr)
        sys.exit(1)
    
    # Выводим результат
    if args.html and 'html' in result:
        print(result['html'])
    else:
        print(result['content'])


if __name__ == '__main__':
    main()
