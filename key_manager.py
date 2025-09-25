import os
from typing import Tuple
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
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