#include <iostream>
#include <random>
#include <fstream>

int main() {
/**
     * @details
     * 1. Использует генератор случайных чисел (`std::random_device`)
     * 2. Применяет вихрь Мерсенна (`std::mt19937`) для генерации
     * 3. Сохраняет результат в файл
     *
     * @return 0 при успешном выполнении
*/
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(0, 1);
    const int N = 128;

    std::ofstream out("cpp_random_bits.txt");
    for (int i = 0; i < N; ++i) {
        out << dis(gen);
    }
    out.close();
    return 0;
}
