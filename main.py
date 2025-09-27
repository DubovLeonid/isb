import argparse
from application import Application


def main() -> int:
    """Основная функция с использованием argparse."""
    parser = argparse.ArgumentParser(description="Гибридная криптосистема для шифрования файлов")

    parser.add_argument(
        "--config",
        default="settings.json",
        help="Путь к конфигурационному файлу (по умолчанию: settings.json)")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "--generate-keys",
        action="store_true",
        help="Сгенерировать новые криптографические ключи")

    group.add_argument(
        "--encrypt",
        action="store_true",
        help="Зашифровать файл")

    group.add_argument(
        "--decrypt",
        action="store_true",
        help="Дешифровать файл")

    parser.add_argument(
        "--input",
        help="Путь к входному файлу")

    parser.add_argument(
        "--output",
        help="Путь для сохранения результата (по умолчанию из конфигурации)")

    args = parser.parse_args()

    try:
        app = Application(args.config)

        if args.generate_keys:
            app.generate_keys()

        elif args.encrypt:
            input_file = args.input if args.input else app.config["original_file"]
            output_file = args.output if args.output else app.config["secret_file"]
            app.encrypt_file(input_file, output_file)

        elif args.decrypt:
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
