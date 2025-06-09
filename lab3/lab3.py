import os
import json
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from typing import Tuple, Optional

import os
import json
from typing import Tuple, Optional
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class KeyManager:
    """Класс для управления криптографическими ключами."""

    @staticmethod
    def generate_symmetric_key() -> bytes:
        """Генерирует симметричный ключ.

        :return: Сгенерированный симметричный ключ длиной 16 байт
        """
        return os.urandom(16)

    @staticmethod
    def generate_iv() -> bytes:
        """Генерирует вектор инициализации.

        :return: Сгенерированный вектор инициализации длиной 16 байт
        """
        return os.urandom(16)

    @staticmethod
    def generate_key_pair() -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
        """Генерирует пару RSA ключей.

        :return: Кортеж (приватный ключ, публичный ключ)
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        return private_key, private_key.public_key()

    @staticmethod
    def save_public_key(public_key: rsa.RSAPublicKey, path: str) -> None:
        """Сохраняет публичный ключ в файл.

        :param public_key: Публичный ключ для сохранения
        :param path: Путь к файлу для сохранения
        """
        with open(path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    @staticmethod
    def save_private_key(private_key: rsa.RSAPrivateKey, path: str) -> None:
        """Сохраняет приватный ключ в файл.

        :param private_key: Приватный ключ для сохранения
        :param path: Путь к файлу для сохранения
        """
        with open(path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

    @staticmethod
    def load_private_key(path: str) -> rsa.RSAPrivateKey:
        """Загружает приватный ключ из файла.

        :param path: Путь к файлу с приватным ключом
        :return: Загруженный приватный ключ
        :raises ValueError: Если файл поврежден или ключ невалиден
        """
        with open(path, "rb") as f:
            return serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )


class FileManager:
    """Класс для работы с файлами."""

    @staticmethod
    def load_config(config_path: str = "settings.json") -> dict:
        """Загружает конфигурацию из JSON-файла.

        :param config_path: Путь к конфигурационному файлу, по умолчанию "settings.json"
        :return: Словарь с загруженной конфигурацией
        :raises SystemExit: Если файл не найден или содержит невалидный JSON
        """
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise SystemExit(f"Ошибка загрузки конфигурации: {str(e)}")

    @staticmethod
    def read_file(path: str, binary: bool = False) -> bytes | str:
        """Читает содержимое файла.

        :param path: Путь к файлу
        :param binary: Флаг бинарного режима чтения, по умолчанию False
        :return: Содержимое файла (байты или строка)
        """
        mode = "rb" if binary else "r"
        with open(path, mode, encoding="utf-8" if not binary else None) as f:
            return f.read()

    @staticmethod
    def write_file(path: str, data: bytes | str, binary: bool = False) -> None:
        """Записывает данные в файл.

        :param path: Путь к файлу
        :param data: Данные для записи
        :param binary: Флаг бинарного режима записи, по умолчанию False
        """
        mode = "wb" if binary else "w"
        with open(path, mode, encoding="utf-8" if not binary else None) as f:
            f.write(data)


class CryptoService:
    """Класс для криптографических операций."""

    @staticmethod
    def encrypt_symmetric_key(public_key: rsa.RSAPublicKey, symmetric_key: bytes) -> bytes:
        """Шифрует симметричный ключ с помощью RSA.

        :param public_key: Публичный RSA-ключ
        :param symmetric_key: Симметричный ключ для шифрования
        :return: Зашифрованный симметричный ключ
        """
        return public_key.encrypt(
            symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def decrypt_symmetric_key(private_key: rsa.RSAPrivateKey, encrypted_key: bytes) -> bytes:
        """Дешифрует симметричный ключ с помощью RSA.

        :param private_key: Приватный RSA-ключ
        :param encrypted_key: Зашифрованный симметричный ключ
        :return: Расшифрованный симметричный ключ
        """
        return private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    @staticmethod
    def encrypt_data(data: bytes, key: bytes, iv: bytes) -> bytes:
        """Шифрует данные с помощью SM4.

        :param data: Данные для шифрования
        :param key: Симметричный ключ
        :param iv: Вектор инициализации
        :return: Зашифрованные данные
        """
        padder = padding.ANSIX923(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        cipher = Cipher(
            algorithms.SM4(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        return encryptor.update(padded_data) + encryptor.finalize()

    @staticmethod
    def decrypt_data(data: bytes, key: bytes, iv: bytes) -> bytes:
        """Дешифрует данные с помощью SM4.

        :param data: Зашифрованные данные
        :param key: Симметричный ключ
        :param iv: Вектор инициализации
        :return: Расшифрованные данные
        """
        cipher = Cipher(
            algorithms.SM4(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(data) + decryptor.finalize()

        unpadder = padding.ANSIX923(128).unpadder()
        return unpadder.update(decrypted_padded) + unpadder.finalize()


class Application:
    """Основной класс приложения."""

    def __init__(self):
        """Инициализирует приложение, загружая конфигурацию."""
        self.config = FileManager.load_config()

    def generate_keys(self) -> None:
        """Генерирует и сохраняет все необходимые ключи.

        Создает:
        - Симметричный ключ
        - Вектор инициализации
        - Пару RSA ключей (публичный и приватный)
        """
        symmetric_key = KeyManager.generate_symmetric_key()
        iv = KeyManager.generate_iv()
        private_key, public_key = KeyManager.generate_key_pair()

        KeyManager.save_public_key(public_key, self.config["public_key"])
        KeyManager.save_private_key(private_key, self.config["private_key"])

        encrypted_key = CryptoService.encrypt_symmetric_key(public_key, symmetric_key)
        FileManager.write_file(self.config["symmetric_key"], iv + encrypted_key, binary=True)

        print("Ключи успешно сгенерированы и сохранены")

    def encrypt_file(self, input_path: str, output_path: str) -> None:
        """Шифрует указанный файл.

        :param input_path: Путь к исходному файлу
        :param output_path: Путь для сохранения зашифрованного файла
        """
        data = FileManager.read_file(input_path, binary=True)
        sym_key_data = FileManager.read_file(self.config["symmetric_key"], binary=True)

        iv, encrypted_key = sym_key_data[:16], sym_key_data[16:]
        private_key = KeyManager.load_private_key(self.config["private_key"])
        symmetric_key = CryptoService.decrypt_symmetric_key(private_key, encrypted_key)

        ciphertext = CryptoService.encrypt_data(data, symmetric_key, iv)
        FileManager.write_file(output_path, ciphertext, binary=True)

        print(f"Файл '{input_path}' успешно зашифрован в '{output_path}'")

    def decrypt_file(self, input_path: str, output_path: str) -> None:
        """Дешифрует указанный файл.

        :param input_path: Путь к зашифрованному файлу
        :param output_path: Путь для сохранения расшифрованного файла
        """
        ciphertext = FileManager.read_file(input_path, binary=True)
        sym_key_data = FileManager.read_file(self.config["symmetric_key"], binary=True)

        iv, encrypted_key = sym_key_data[:16], sym_key_data[16:]
        private_key = KeyManager.load_private_key(self.config["private_key"])
        symmetric_key = CryptoService.decrypt_symmetric_key(private_key, encrypted_key)

        plaintext = CryptoService.decrypt_data(ciphertext, symmetric_key, iv)
        FileManager.write_file(output_path, plaintext, binary=True)

        print(f"Файл '{input_path}' успешно расшифрован в '{output_path}'")

    def run(self) -> None:
        """Запускает главный цикл приложения с меню управления."""
        print("Гибридная криптосистема")

        while True:
            print("\nМеню:")
            print("1. Сгенерировать новые ключи")
            print("2. Зашифровать файл")
            print("3. Дешифровать файл")
            print("4. Выход")

            choice = input("Выберите действие: ").strip()

            match choice:
                case "1":
                    self.generate_keys()
                case "2":
                    try:
                        input_file = self.config["original_file"]
                        output_file = self.config["secret_file"]
                        self.encrypt_file(input_file, output_file)
                    except KeyError:
                        print("Ошибка: Не найдены пути в конфигурации")
                    except Exception as e:
                        print(f"Ошибка шифрования: {str(e)}")
                case "3":
                    try:
                        input_file = self.config["secret_file"]
                        output_file = self.config["decrypted_file"]
                        self.decrypt_file(input_file, output_file)
                    except KeyError:
                        print("Ошибка: Не найдены пути в конфигурации")
                    except Exception as e:
                        print(f"Ошибка дешифрования: {str(e)}")
                case "4":
                    print("Выход из программы")
                    break
                case _:
                    print("Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        print("\nРабота прервана пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {str(e)}")
