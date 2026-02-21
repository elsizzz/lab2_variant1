"""
Задача 2. Декоратор кэширования
Вариант 1: База данных postgreSQL
"""

import functools
from typing import Any, Callable, Dict, Tuple


def cache(db: str):
    """
    Декоратор для кэширования результатов функции с ограничением по количеству использований.
    
    Args:
        db: Название базы данных
    
    Returns:
        Декорированную функцию
    """
    def decorator(func: Callable) -> Callable:
        # Хранилище для кэша: {аргумент: (закэшированный_результат, оставшиеся_использования)}
        cache_storage: Dict[str, Tuple[Any, int]] = {}

        @functools.wraps(func)
        def wrapper(thing: str, **kwargs) -> str:
            # Извлекаем expiration из kwargs, если его нет - используем значение по умолчанию
            expiration = kwargs.get('expiration', 5)

            # Проверяем, есть ли элемент в кэше
            if thing in cache_storage:
                cached_value, remaining = cache_storage[thing]
                
                # Если еще остались попытки
                if remaining > 0:
                    # Уменьшаем счетчик
                    cache_storage[thing] = (cached_value, remaining - 1)
                    return f"Info about: {thing} cached in {db}, expire={remaining - 1}"
                else:
                    # Кэш истек, удаляем запись
                    del cache_storage[thing]
                    # Рекурсивно запрашиваем новые данные
                    return wrapper(thing, **kwargs)
            else:
                # Данных нет в кэше - запрашиваем актуальные данные
                fresh_result = func(thing)
                # Сохраняем в кэш, если expiration > 0
                if expiration > 0:
                    cache_storage[thing] = (fresh_result, expiration)
                return f"Info about: {thing} from {db}, now cached with expire={expiration}"
        
        return wrapper
    return decorator


# Исходная функция, информацию из которой мы будем кэшировать
def get_info(thing: str) -> str:
    """Симуляция получения данных из БД."""
    # В реальном проекте здесь был бы запрос к базе данных
    data = {
        'bike_store': 'Горный велосипед, цена: $500',
        'users': 'Всего пользователей: 1500',
        'products': 'Товаров в наличии: 45',
        'orders': 'Заказов сегодня: 23'
    }
    return data.get(thing, f"Информация о '{thing}' не найдена")


# Декорируем функцию для работы с postgreSQL
@cache(db='postgresql')
def get_info_cached(thing: str, **kwargs) -> str:
    """Обертка для get_info с кэшированием."""
    return get_info(thing)


def demonstrate_cache(thing: str, expire: int, times: int):
    """
    Демонстрирует работу кэша для заданного предмета.
    
    Args:
        thing: Предмет для поиска
        expire: Время жизни кэша
        times: Количество вызовов
    """
    print(f"\n--- Демонстрация для '{thing}' с expire={expire} ---")
    for i in range(times):
        result = get_info_cached(thing, expiration=expire)
        print(result)


def main():
    """Демонстрация работы декоратора кэширования."""
    print("ЗАДАЧА 2: Декоратор кэширования (postgreSQL)")
    
    # Пример 1: bike_store с expire=5
    demonstrate_cache('bike_store', 5, 8)  # Вызовем 8 раз, чтобы увидеть обновление
    
    print("\n")
    
    # Пример 2: users с expire=5
    demonstrate_cache('users', 5, 8)
    
    print("\n")
    
    # Пример 3: products с разным expire
    demonstrate_cache('products', 3, 5)
    
    print("\n")


if __name__ == "__main__":
    main()