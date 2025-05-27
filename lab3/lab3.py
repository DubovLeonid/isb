import os
import json
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


def load_config(config_path: str = "settings.json") -> dict:
    """Загружает конфигурацию приложения из JSON-файла.
    Args:config_path (str, optional): Путь к файлу конфигурации. По умолчанию "settings.json".
    Returns:dict: Словарь с параметрами конфигурации."""

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise SystemExit(f"Ошибка загрузки конфигурации: {str(e)}")


def generate_keys(symmetric_key_path: str, public_key_path: str, private_key_path: str) -> None:
    """Генерирует и сохраняет криптографические ключи для гибридной системы.
       Args:symmetric_key_path (str): Путь для сохранения зашифрованного симметричного ключа
            public_key_path (str): Путь для сохранения публичного RSA-ключа
            private_key_path (str): Путь для сохранения приватного RSA-ключа"""

    try:
        symmetric_key = os.urandom(16)
        iv = os.urandom(16)

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        with open(public_key_path, "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        with open(private_key_path, "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        encrypted_key = public_key.encrypt(
            symmetric_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        with open(symmetric_key_path, "wb") as f:
            f.write(iv + encrypted_key)

        print(" Ключи успешно сгенерированы и сохранены")

    except IOError as e:
        raise SystemExit(f"Ошибка записи ключей: {str(e)}")
    except Exception as e:
        raise SystemExit(f"Ошибка генерации ключей: {str(e)}")


def read_secret_file(path: str) -> str:
    """Считывает секретный текст из указанного файла.
        Args:path (str): Путь к файлу с секретным текстом
    Returns:str: Содержимое файла"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except IOError as e:
        raise SystemExit(f"Ошибка чтения секретного файла: {str(e)}")


def encrypt_file(input_path: str, private_key_path: str, enc_sym_key_path: str, output_path: str) -> None:
    """Шифрует файл с использованием гибридной криптосистемы.
         Args:input_path (str): Путь к исходному файлу
            private_key_path (str): Путь к файлу приватного RSA-ключа
            enc_sym_key_path (str): Путь к файлу с зашифрованным симметричным ключом
            output_path (str): Путь для сохранения зашифрованного файла"""\

    try:
        with open(enc_sym_key_path, "rb") as f:
            data = f.read()
            iv, encrypted_key = data[:16], data[16:]

        with open(private_key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )

        symmetric_key = private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        with open(input_path, "rb") as f:
            plaintext = f.read()

        padder = padding.ANSIX923(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        cipher = Cipher(
            algorithms.SM4(symmetric_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        with open(output_path, "wb") as f:
            f.write(ciphertext)

        print(f"[+] Файл '{input_path}' успешно зашифрован в '{output_path}'")

    except (IOError, ValueError) as e:
        raise SystemExit(f"Ошибка шифрования: {str(e)}")


def decrypt_file(input_path: str, private_key_path: str, enc_sym_key_path: str, output_path: str) -> None:
    """Дешифрует файл с использованием гибридной криптосистемы.
         Args:input_path (str): Путь к зашифрованному файлу
            private_key_path (str): Путь к файлу приватного RSA-ключа
            enc_sym_key_path (str): Путь к файлу с зашифрованным симметричным ключом
            output_path (str): Путь для сохранения расшифрованного файла"""

    try:
        with open(enc_sym_key_path, "rb") as f:
            data = f.read()
            iv, encrypted_key = data[:16], data[16:]

        with open(private_key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None,
                backend=default_backend()
            )

        symmetric_key = private_key.decrypt(
            encrypted_key,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        with open(input_path, "rb") as f:
            ciphertext = f.read()

        cipher = Cipher(
            algorithms.SM4(symmetric_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.ANSIX923(128).unpadder()
        plaintext = unpadder.update(decrypted_padded) + unpadder.finalize()

        with open(output_path, "wb") as f:
            f.write(plaintext)

        print(f" Файл '{input_path}' успешно расшифрован в '{output_path}'")

    except (IOError, ValueError) as e:
        raise SystemExit(f"Ошибка дешифрования: {str(e)}")


def main() -> None:
    """Выполняет полный цикл работы гибридной криптосистемы."""
    try:
        config = load_config()
        secret_text = read_secret_file(config["secret_file"])

        try:
            with open(config["original_file"], "w", encoding="utf-8") as f:
                f.write(secret_text)
            print(f" Создан исходный файл '{config['original_file']}'")
        except IOError as e:
            raise SystemExit(f"Ошибка создания файла: {str(e)}")

        generate_keys(
            config["symmetric_key"],
            config["public_key"],
            config["private_key"]
        )

        encrypt_file(
            config["original_file"],
            config["private_key"],
            config["symmetric_key"],
            config["encrypted_file"]
        )

        decrypt_file(
            config["encrypted_file"],
            config["private_key"],
            config["symmetric_key"],
            config["decrypted_file"]
        )

        print("\nРезультаты работы:")
        file_stats = [
            (config["original_file"], "Исходный файл"),
            (config["encrypted_file"], "Зашифрованный файл"),
            (config["decrypted_file"], "Расшифрованный файл")
        ]

        for path, name in file_stats:
            try:
                size = os.path.getsize(path)
                print(f"{name}: {size} байт")
            except FileNotFoundError:
                print(f"{name}: файл не найден")

        try:
            with open(config["original_file"], "r", encoding="utf-8") as f1, \
                    open(config["decrypted_file"], "r", encoding="utf-8") as f2:
                match = f1.read() == f2.read()
                print("\nСовпадение содержимого:", match)
        except IOError:
            print("\nОшибка сравнения файлов: один из файлов не найден")

    except KeyboardInterrupt:
        print("\nРабота прервана пользователем")
    except Exception as e:
        print(f"\nКритическая ошибка: {str(e)}")


if __name__ == "__main__":
    main()