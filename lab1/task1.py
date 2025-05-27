from func import *

def caesar(text: str, alph: str, key: int) -> str:
    """
    Шифрует текст с помощью шифра Цезаря.

    :param text: Исходный текст для шифрования.
    :param alph: Алфавит (символы должны быть уникальными).
    :param key: Числовой сдвиг для шифра.
    :return: Зашифрованная строка или сообщение об ошибке.
    """
    try:
        alph_lower = alph.lower()
        if len(set(alph_lower)) != len(alph):
            raise ValueError("Алфавит содержит повторяющиеся символы")
        
        char_to_index = {char: idx for idx, char in enumerate(alph_lower)}
        alpha_len = len(alph_lower)
        encrypted_chars = []

        for char in text:
            lower_char = char.lower()
            if lower_char in char_to_index:
                original_idx = char_to_index[lower_char]
                new_idx = (original_idx + key) % alpha_len
                new_char = alph_lower[new_idx]
                encrypted_chars.append(new_char.upper() if char.isupper() else new_char)
            else:
                encrypted_chars.append(char)

        return ''.join(encrypted_chars)

    except ValueError as ve:
        return f"Ошибка валидации: {ve}"
    except Exception as e:
        return f"Неизвестная ошибка: {e}"

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
