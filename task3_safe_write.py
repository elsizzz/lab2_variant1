"""
Задача 3. Контекстный менеджер safe_write
Вариант 1: Работа с текстовыми файлами (стихи, песни)
"""

import os
from typing import Optional, TextIO


class safe_write:
    """
    Контекстный менеджер для безопасной записи в файл с возможностью отката при ошибке.
    
    Пример использования:
        with safe_write('poem.txt') as file:
            file.write('Строка текста...')
    """
    
    def __init__(self, filename: str):
        """
        Инициализация контекстного менеджера.
        
        Args:
            filename: Имя файла для записи
        """
        self.filename = filename
        self.file: Optional[TextIO] = None
        self.content_before_write: Optional[str] = None

    def __enter__(self) -> TextIO:
        """
        Вход в контекстный менеджер.
        Сохраняем предыдущее содержимое файла (если оно есть) и открываем файл для записи.
        
        Returns:
            Открытый файловый объект для записи
        """
        # Сохраняем старое содержимое, если файл существует
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.content_before_write = f.read()
        except FileNotFoundError:
            self.content_before_write = None

        # Открываем файл для записи
        self.file = open(self.filename, 'w', encoding='utf-8')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Выход из контекстного менеджера.
        Если было исключение - откатываем изменения и выводим сообщение.
        
        Returns:
            True - подавляем исключение
        """
        # Закрываем файл
        if self.file:
            self.file.close()

        # Если произошло исключение
        if exc_type is not None:
            print(f"Во время записи в файл было возбуждено исключение {exc_type.__name__}")

            # Восстанавливаем старое содержимое
            if self.content_before_write is not None:
                with open(self.filename, 'w', encoding='utf-8') as f:
                    f.write(self.content_before_write)
                print(f"Файл '{self.filename}' восстановлен в исходное состояние")
            else:
                # Если файла не было, удаляем созданный
                try:
                    os.remove(self.filename)
                    print(f"Созданный файл '{self.filename}' удален")
                except FileNotFoundError:
                    pass

        # Подавляем исключение
        return True


def main():
    """Демонстрация работы контекстного менеджера safe_write."""
    print("ЗАДАЧА 3: Контекстный менеджер safe_write")
    
    # Пример 1: Успешная запись
    print("\n[Пример 1] Успешная запись в файл:")
    
    poem = """Белеет парус одинокой
В тумане моря голубом!..
Что ищет он в стране далекой?
Что кинул он в краю родном?.."""
    
    with safe_write('poem.txt') as file:
        file.write(poem)
    
    # Проверяем содержимое
    with open('poem.txt', 'r', encoding='utf-8') as file:
        print("\nСодержимое файла 'poem.txt':")
        print(file.read())
    
    # Пример 2: Запись с ошибкой
    print("\n[Пример 2] Запись с исключением:")
    
    # Сначала запишем начальные данные
    with safe_write('song.txt') as file:
        file.write("Катюша\nВыходила на берег Катюша\n")
    
    print("Пытаемся записать новые данные с ошибкой...")
    
    # Пытаемся записать новые данные, но вызываем исключение
    try:
        with safe_write('song.txt') as file:
            file.write("Новые строки песни...\n")
            file.write("Еще одна строка...\n")
            # Искусственно вызываем исключение
            raise ValueError("Ошибка при записи!")
    except ValueError:
        # safe_write подавляет исключение, так что мы сюда не попадем
        pass
    
    # Проверяем, что файл остался неизменным
    with open('song.txt', 'r', encoding='utf-8') as file:
        print("\nСодержимое файла 'song.txt' после ошибки:")
        print(file.read())
    
    # Пример 3: Запись в новый файл с ошибкой
    print("\n[Пример 3] Запись в новый файл с ошибкой:")
    
    with safe_write('new_file.txt') as file:
        file.write("Этот текст не должен сохраниться...\n")
        # Вызываем исключение
        raise TypeError("Ошибка типа данных!")
    
    # Проверяем, что файл не создался
    if not os.path.exists('new_file.txt'):
        print("Файл 'new_file.txt' не был создан (правильно!)")
    else:
        print(" Ошибка: файл создался, хотя не должен был")
    
    print("\n")


if __name__ == "__main__":
    main()