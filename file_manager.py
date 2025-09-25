import json
from typing import Union


class FileManager:
    """Класс для работы с файлами."""

    @staticmethod
    def read_file(path: str, binary: bool = False) -> Union[bytes, str]:
        """Читает содержимое файла.

        :param path: Путь к файлу
        :param binary: Флаг бинарного режима чтения, по умолчанию False
        :return: Содержимое файла (байты или строка)
        """
        mode = "rb" if binary else "r"
        encoding = None if binary else "utf-8"
        try:
            with open(path, mode, encoding=encoding) as f:
                return f.read()
        except FileNotFoundError as e:
            raise SystemExit(f"Файл не найден: {path}")

    @staticmethod
    def load_config(config_path: str = "settings.json") -> dict:
        """Загружает конфигурацию из JSON-файла.

        :param config_path: Путь к конфигурационному файлу, по умолчанию "settings.json"
        :return: Словарь с загруженной конфигурацией
        :raises SystemExit: Если файл не найден или содержит невалидный JSON
        """
        content = FileManager.read_file(config_path, binary=False)
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise SystemExit(f"Ошибка парсинга JSON в файле {config_path}: {str(e)}")

    @staticmethod
    def write_file(path: str, data: Union[bytes, str], binary: bool = False) -> None:
        """Записывает данные в файл.

        :param path: Путь к файлу
        :param data: Данные для записи
        :param binary: Флаг бинарного режима записи, по умолчанию False
        """
        mode = "wb" if binary else "w"
        encoding = None if binary else "utf-8"
        with open(path, mode, encoding=encoding) as f:
            f.write(data)