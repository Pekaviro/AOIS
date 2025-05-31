import random

from word import Word


class Matrix:
    def __init__(self):
        self.words = [Word(''.join(random.choice('01') for _ in range(16))) for _ in range(16)]
        self.update_diagonal_matrix()

    def update_diagonal_matrix(self):
        self.matrix = [['0']*16 for _ in range(16)]
        for word_idx in range(16):
            for bit_idx in range(16):
                row = (word_idx + bit_idx) % 16
                col = word_idx
                self.matrix[row][col] = self.words[word_idx].bits[bit_idx]

    def apply_logical_function(self, func, col1, col2, target_col):
        # Получаем слова для операции
        word1 = self.words[col1]
        word2 = self.words[col2]
        target_word = self.words[target_col]
        
        print("\n--- Логическая операция ---")
        print(f"Функция: {func}")
        print(f"Слово {col1}: {word1.bits} (V={word1.get_v()}, A={word1.get_a()}, B={word1.get_b()}, S={word1.get_s()})")
        print(f"Слово {col2}: {word2.bits} (V={word2.get_v()}, A={word2.get_a()}, B={word2.get_b()}, S={word2.get_s()})")
        print(f"Целевое слово до операции (слово {target_col}): {target_word.bits}")
        
        # Применяем операцию к каждому биту
        result_bits = []
        for i, (bit1, bit2) in enumerate(zip(word1.bits, word2.bits)):
            res = '0'
            if func == 'f7':  # ИЛИ
                res = '1' if bit1 == '1' or bit2 == '1' else '0'
            elif func == 'f8':  # Пирса (ИЛИ-НЕ)
                res = '0' if (bit1 == '1' or bit2 == '1') else '1'
            elif func == 'f2':  # Запрет первого аргумента
                res = '1' if (bit1 == '1' and bit2 == '0') else '0'
            elif func == 'f13':  # Импликация
                res = '1' if (bit1 == '0' or bit2 == '1') else '0'
            result_bits.append(res)
        
        # Формируем результат
        result = ''.join(result_bits)
        print(f"\nРезультат операции: {result}")
        
        # Записываем результат
        target_word.bits = result
        print(f"Целевое слово после операции (слово {target_col}): {target_word.bits}")
        
        # Обновляем матрицу
        self.update_diagonal_matrix()
        print("Матрица обновлена")  

    def search_interval(self, lower_bin, upper_bin):
        """Ищет 16-битные слова в интервале [lower_bin, upper_bin]"""
        # Конвертируем границы в 16-битные строки
        if isinstance(lower_bin, int):
            lower_bin = f"{lower_bin:016b}"
        if isinstance(upper_bin, int):
            upper_bin = f"{upper_bin:016b}"

        if len(lower_bin) != 16 or len(upper_bin) != 16:
            raise ValueError("Границы должны быть 16-битными строками или числами (0-65535)")

        flags = [1] * len(self.words)  # Изначально все флаги = 1
        lower_val = int(lower_bin, 2)
        upper_val = int(upper_bin, 2)

        print("\nНачало поиска. Все флаги установлены в 1.")
        print(f"Интервал: [{lower_bin} ({lower_val}), {upper_bin} ({upper_val})]")

        for i, word in enumerate(self.words):
            word_val = int(word.bits, 2)
            if word_val >= upper_val:
                flags[i] = 0

        for i, word in enumerate(self.words):
            word_val = int(word.bits, 2)
            if word_val <= lower_val:
                flags[i] = 0

        results = [i for i, flag in enumerate(flags) if flag == 1]
        
        print("\nРезультат:")
        for i in results:
            word_val = int(self.words[i].bits, 2)
            print(f"Слово {i}: {self.words[i].bits} ({word_val})")
        print(f"Найдено слов: {len(results)}")

        return results

    def arithmetic_operation(self, v_key):
        # Преобразуем v_key в 3-битную строку
        if isinstance(v_key, int):
            target_v = f"{v_key:03b}"
        else:
            target_v = v_key.zfill(3)[-3:] 
        
        print(f"\nИщем слова с V = {target_v}")  
        
        for word in self.words:
            if word.get_v() == target_v:
                a = word.get_value('a')
                b = word.get_value('b')
                s = a + b
                s_bits = f"{s & 0b11111:05b}"  # Обрезаем до 5 бит
                print(f"Слово до: {word.bits} | A={a}, B={b}, S={word.get_s()}") 
                word.set_s(s_bits)
                print(f"Слово после: {word.bits} | Новое S={s_bits}")
        
        self.update_diagonal_matrix()       

    def print_matrix(self):
        print("\nТекущее состояние матрицы:")
        for row in self.matrix:
            print(" ".join(row))
