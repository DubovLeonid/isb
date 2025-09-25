
import argparse
from application import Application


def main() -> int:
    """Основная функция с использованием argparse."""
    parser = argparse.ArgumentParser(description="Гибридная криптосистема для шифрования файлов")

    parser.add_argument(
        "--config",
        default="settings.json",
        help="Путь к конфигурационному файлу (по умолчанию: settings.json)"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Доступные команды",
        required=True
    )

    generate_parser = subparsers.add_parser(
        "generate-keys",
        help="Сгенерировать новые криптографические ключи"
    )

    encrypt_parser = subparsers.add_parser(
        "encrypt",
        help="Зашифровать файл"
    )

    encrypt_parser.add_argument(
        "--input",
        help="Путь к исходному файлу для шифрования"
    )

    encrypt_parser.add_argument(
        "--output",
        help="Путь для сохранения зашифрованного файла (по умолчанию из конфигурации)"
    )

    decrypt_parser = subparsers.add_parser(
        "decrypt",
        help="Дешифровать файл"
    )

    decrypt_parser.add_argument(
        "--input",
        help="Путь к зашифрованному файлу"
    )

    decrypt_parser.add_argument(
        "--output",
        help="Путь для сохранения расшифрованного файла (по умолчанию из конфигурации)"
    )

    args = parser.parse_args()

    try:
        app = Application(args.config)

        if args.command == "generate-keys":
            app.generate_keys()

        elif args.command == "encrypt":
            input_file = args.input if args.input else app.config["original_file"]
            output_file = args.output if args.output else app.config["secret_file"]
            app.encrypt_file(input_file, output_file)

        elif args.command == "decrypt":
            input_file = args.input if args.input else app.config["secret_file"]
            output_file = args.output if args.output else app.config["decrypted_file"]
            app.decrypt_file(input_file, output_file)

    except KeyError as e:
        print(f"Ошибка конфигурации: отсутствует ключ {e}")
        return 1
    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return 1

    print("Операция завершена успешно")
    return 0


if __name__ == "__main__":
    exit(main())