from key_manager import KeyManager
from file_manager import FileManager
from crypto_service import CryptoService


class Application:
    """Основной класс приложения."""

    def __init__(self, config_path: str = "settings.json"):
        """Инициализирует приложение, загружая конфигурацию."""
        self.config = FileManager.load_config(config_path)

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