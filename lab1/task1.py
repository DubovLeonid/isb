from func import *

def caesar(text: str, alph: str, key: int) -> str:
    """
        Шифрует текст с помощью шифра Цезаря.

        :param text: Исходный текст для шифрования.
        :param alph: Алфавит, используемый для шифрования.
        :param key: Числовой сдвиг для шифра.
        :return: Зашифрованная строка.
    """
    try:
        enctext = ""
        for char in text:
            match char:
                case c if c in alph:
                    new_index = (alph.index(c) + key) % len(alph)
                    enctext += alph[new_index]
                case c if c.lower() in alph:
                    new_index = (alph.index(c.lower()) + key) % len(alph)
                    enctext += alph[new_index].upper()
                case _:
                    enctext += char
        return enctext
    except Exception as e:
        return f"Ошибка: {e}"

def decrypt_caesar(text: str, alph: str, key: int) -> str:
    """
        Дешифрует текст, зашифрованный шифром Цезаря.
    """
    return caesar(text, alph, -key)

def main() -> None:
    """
        Главная функция программы.

        Читает исходный текст и ключ из файлов, проверяет корректность ключа,
        выполняет шифрование методом Цезаря и сохраняет результат.

        :return: None
    """
    settings = load_json("./settings.json")

    alph_ = settings.get("ALPH", "")
    text_ = settings.get("TEXT", "")
    enctext_ = settings.get("ENCTEXT", "")
    key_ = load_json(settings.get("KEY", "")).get("KEY")
    try:
        text = read(text_)
        match str(key_).isdigit():
            case False:
                print("Ошибка: Ключ должен быть числом.")
                return
            case True:
                key = int(key_)
                enctext = caesar(text, alph_, key)
                dectext = decrypt_caesar(enctext, alph_, key)
                print("Исходный текст:")
                print(text)
                print("\n")
                match bool(enctext):
                    case True:
                        print("Зашифрованный текст:")
                        print(enctext)
                        save(enctext_, enctext)
                        print("\nУспешно сохранено:", enctext_)
                        print("\nРасшифрованный текст:")
                        print(dectext)
                    case False:
                        print("\nОшибка при шифровании.")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()