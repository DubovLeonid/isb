from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.backends import default_backend
from key_manager import KeyManager


class CryptoService:
    """Класс для криптографических операций."""

    @staticmethod
    def encrypt_symmetric_key(public_key, symmetric_key: bytes) -> bytes:
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
    def decrypt_symmetric_key(private_key, encrypted_key: bytes) -> bytes:
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