"""
Задача 1. Декоратор прав администратора
Вариант 1: роли 'admin', 'user'
"""

import functools
from typing import Any, Callable

# Глобальная переменная с ролью текущего пользователя
user_role = 'user'  # Можно менять на 'admin' для проверки


def role_required(required_role: str) -> Callable:
    """
    Декоратор, проверяющий соответствие роли пользователя требуемой роли.
    
    Args:
        required_role: Роль, которая имеет доступ к функции
    
    Returns:
        Декорированную функцию
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            global user_role
            if user_role == required_role:
                # Если роль совпадает, выполняем функцию
                return func(*args, **kwargs)
            else:
                # Если нет - выводим сообщение о запрете
                print(f"Доступ запрещен! Требуется роль: {required_role}, ваша роль: {user_role}")
                return None
        return wrapper
    return decorator


@role_required('admin')
def secret_resource() -> str:
    """Секретный ресурс, доступный только администраторам."""
    return "Секретные данные: Пароль от сервера - 1234"
    

@role_required('admin')
def delete_database() -> str:
    """Опасная функция, доступная только админам."""
    return "База данных удалена!"


def main():
    """Демонстрация работы декоратора."""
    global user_role
    
    print("ЗАДАЧА 1: Декоратор проверки ролей")
    
    # Тест с ролью user
    print(f"\n[Тест 1] Текущая роль: {user_role}")
    secret_resource()
    delete_database()
    
    # Меняем роль на admin
    print(f"\n[Тест 2] Меняем роль на 'admin'...")
    user_role = 'admin'
    print(f"Текущая роль: {user_role}")
    
    result1 = secret_resource()
    if result1:
        print(f"Результат secret_resource(): {result1}")
    
    result2 = delete_database()
    if result2:
        print(f"Результат delete_database(): {result2}")
    
    print("\n")


if __name__ == "__main__":
    main()