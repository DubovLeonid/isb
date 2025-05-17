from func import *

def calculate_frequencies(text: str) -> dict:
    """
    Вычисляет частоту появления символов в зашифрованном тексте
    :param text: Исходный текст.
    :return: Словарь с частотами символов
    """
    char_count = {}
    total_chars = 0

    for char in text:
        if char in char_count:
            char_count[char] += 1
        else:
            char_count[char] = 1
        total_chars += 1

    frequencies = {}
    for char, count in char_count.items():
        frequencies[char] = count / total_chars

    return frequencies


def create_key(real_freq, ru_freq):
    """
    Создает прямое сопоставление символов по частотам
    :param real_freq: Частоты символов в зашифрованном тексте.
    :param ru_freq: Частоты символов в русском языке.
    :return: Ключ
    """

    real_freq_upper = {k.upper(): v for k, v in real_freq.items()}
    ru_freq_upper = {k.upper(): v for k, v in ru_freq.items()}

    sorted_encrypted = sorted(real_freq_upper.items(), key=lambda x: -x[1])
    sorted_ru = sorted(ru_freq_upper.items(), key=lambda x: -x[1])

    key = {}
    for i in range(min(len(sorted_encrypted), len(sorted_ru))):
        enc_char = sorted_encrypted[i][0]
        ru_char = sorted_ru[i][0]
        key[enc_char] = ru_char

    return key


def create_char_mapping(text: str, key: dict) -> str:
    """
    Дешифрует текст.
    :param text: Зашифрованный текст
    :param key: Ключ
    :return: Дешифрованный текст
    """
    text = text.upper()
    encrypted_text = ""

    for i in text:
        if i in key:
            encrypted_text += key[i]
        else:
            encrypted_text += i

    return encrypted_text

def main():
    try:
        config = load_json("settings.json")
        text = read(config["cod8_txt"])
        freq_ru = load_json(config["freq_ru"])
        real_frequency = calculate_frequencies(text)
        save_json(config["real_frequency"], real_frequency)
        key2 = create_key(real_frequency, freq_ru)
        save_json(config["key2"], key2)

        encrypted_text = create_char_mapping(text, key2)
        save(config["encrypted_text"], encrypted_text)

    except Exception as e:
        print(f"Ошибка в : {e}")
    return 0


if __name__ == "__main__":
    main()