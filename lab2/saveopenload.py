import json


def read(filename: str) -> str:
    """
    Читает текстовый файл и возвращает его содержимое.
    :param filename: Путь к файлу для чтения
    :return: Содержимое файла в виде строки или None при ошибке
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
    except Exception as e:
        print(f"Файл {e} не может быть открыт")


def save(filename: str, content: str) -> None:
    """
    Записывает текст в файл.
    :param filename: Путь к файлу для записи
    :param content: Текст для записи в файл
    :return:
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Файд {e} не может быть создан")


def load_json(filename: str) -> dict:
    """
    Загружает JSON-файл.
    :param filename: Путь к JSON-файлу
    :return: Словарь с данными или None при ошибке
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файд {filename} не найден")
    except Exception as e:
        print(f"Файд {e} не может быть открыт")


def save_json(filename: str, data: dict) -> None:
    """
    Сохраняет данные в JSON-файл.
    :param filename: Путь к файлу для сохранения
    :param data: Данные для сохранения
    :return:
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Файд {e} не может быть создан")