#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пример связывания пользователя Marzban с Telegram-пользователем.
"""

import asyncio
import os
from marzban import MarzbanAPI, TelegramUserUpdate

# Загрузка переменных окружения (можно использовать python-dotenv)
MARZBAN_URL = os.getenv("MARZBAN_URL", "http://localhost:8000")
MARZBAN_USERNAME = os.getenv("MARZBAN_USERNAME", "admin")
MARZBAN_PASSWORD = os.getenv("MARZBAN_PASSWORD", "admin")

# ID пользователя Marzban (замените на реальный ID)
MARZBAN_USER_ID = 1

# ID пользователя в Telegram (замените на реальный ID)
TELEGRAM_USER_ID = 123456789

# Имя пользователя в Telegram (опционально)
TELEGRAM_USERNAME = "user_example"


async def main():
    # Инициализация API клиента
    api = MarzbanAPI(
        base_url=MARZBAN_URL,
        timeout=10.0,
        verify=False,  # Установите True в продакшн окружении
    )
    
    # Получение токена доступа
    await api.get_token(
        username=MARZBAN_USERNAME,
        password=MARZBAN_PASSWORD
    )
    
    try:
        print(f"Связывание пользователя Marzban (ID: {MARZBAN_USER_ID}) с пользователем Telegram (ID: {TELEGRAM_USER_ID}):")
        
        # Дополнительная информация для пользователя Telegram (опционально)
        telegram_data = TelegramUserUpdate(
            username=TELEGRAM_USERNAME,
            test_period=7  # Тестовый период в днях
        )
        
        # Связывание пользователя
        linked_user = await api.link_user_to_telegram(
            user_id=MARZBAN_USER_ID,
            telegram_id=TELEGRAM_USER_ID,
            telegram_data=telegram_data
        )
        
        print(f"Пользователь успешно связан!")
        print(f"- ID: {linked_user.id}")
        print(f"- Telegram ID: {linked_user.telegram_id}")
        print(f"- Username: {linked_user.username}")
        print(f"- User ID: {linked_user.user_id}")
        print(f"- Test Period: {linked_user.test_period}")
        print(f"- Created At: {linked_user.created_at}")
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 