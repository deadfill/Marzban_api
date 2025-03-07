#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Пример использования API для работы с Telegram-пользователями в Marzban.
"""

import asyncio
import os
from marzban import MarzbanAPI, TelegramUserCreate, TelegramUserUpdate

# Загрузка переменных окружения (можно использовать python-dotenv)
MARZBAN_URL = os.getenv("MARZBAN_URL", "http://localhost:8000")
MARZBAN_USERNAME = os.getenv("MARZBAN_USERNAME", "admin")
MARZBAN_PASSWORD = os.getenv("MARZBAN_PASSWORD", "admin")


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
        # Получение списка всех пользователей Telegram
        print("Получение списка всех пользователей Telegram:")
        telegram_users = await api.get_telegram_users()
        for user in telegram_users:
            print(f"- ID: {user.id}, Telegram ID: {user.telegram_id}, Username: {user.username}")
        
        if telegram_users:
            # Получение информации о первом пользователе Telegram
            first_user_id = telegram_users[0].telegram_id
            print(f"\nПолучение информации о пользователе Telegram (ID: {first_user_id}):")
            user = await api.get_telegram_user(first_user_id)
            print(f"- ID: {user.id}, Telegram ID: {user.telegram_id}, Username: {user.username}")
            
            # Получение пользователей Marzban, связанных с пользователем Telegram
            print(f"\nПолучение пользователей Marzban, связанных с пользователем Telegram (ID: {first_user_id}):")
            marzban_users = await api.get_users_by_telegram_id(first_user_id)
            for m_user in marzban_users:
                print(f"- Username: {m_user.username}, Status: {m_user.status}")
                
            # Обновление данных пользователя Telegram
            print(f"\nОбновление данных пользователя Telegram (ID: {first_user_id}):")
            update_data = TelegramUserUpdate(
                test_period=14  # Изменяем тестовый период
            )
            updated_user = await api.update_telegram_user(first_user_id, update_data)
            print(f"- Обновлено: ID: {updated_user.id}, Test Period: {updated_user.test_period}")
            
        # Создание нового пользователя Telegram (закомментировано, чтобы не создавать реального пользователя)
        """
        # Получение пользователя Marzban для привязки
        users = await api.get_users(offset=0, limit=1)
        if users:
            marzban_user_id = users[0].id
            
            print("\nСоздание нового пользователя Telegram:")
            new_user_data = TelegramUserCreate(
                telegram_id=123456789,  # ID вашего пользователя в Telegram
                username="testuser",
                test_period=7,
                user_id=marzban_user_id
            )
            new_user = await api.create_telegram_user(new_user_data)
            print(f"- Создан: ID: {new_user.id}, Telegram ID: {new_user.telegram_id}, Username: {new_user.username}")
            
            # Удаление созданного пользователя
            print(f"\nУдаление пользователя Telegram (ID: {new_user.telegram_id}):")
            result = await api.delete_telegram_user(new_user.telegram_id)
            print(f"- Удалено: {result}")
        """
        
    except Exception as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 