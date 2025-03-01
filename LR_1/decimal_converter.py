class DecimalConverter:
    @staticmethod
    def reverse_code_to_decimal(binary_str):
        # Проверяем, является ли число отрицательным (первый бит равен 1)
        is_negative = binary_str[0] == '1'
    
        # Если число отрицательное, инвертируем все биты
        if is_negative:
            inverted_bits = ''
            for bit in binary_str:
                inverted_bits += '1' if bit == '0' else '0'
            binary_str = inverted_bits
    
        # Переводим двоичное число в десятичное
        decimal_value = 0
        power = len(binary_str) - 1
        for bit in binary_str:
            decimal_value += int(bit) * (2 ** power)
            power -= 1
    
        # Если число было отрицательным, добавляем знак минус
        if is_negative:
            decimal_value = -decimal_value
    
        return decimal_value


    def additional_code_to_decimal(bin_str):
        n = len(bin_str)
        # Проверяем, является ли число отрицательным
        if bin_str[0] == '1':
            # Переводим в дополнительный код
            inverted_bin = ''.join('1' if b == '0' else '0' for b in bin_str)
        
            # Добавляем 1 к перевернутому числу (это будет дополнительный код)
            carry = 1
            result = ''
            for i in range(n - 1, -1, -1):
                if carry == 0:
                    result = inverted_bin[i] + result
                else:
                    if inverted_bin[i] == '0':
                        result = '1' + result
                        carry = 0
                    else:
                        result = '0' + result

            # Конвертируем результат в десятичное число
            decimal = 0
            for i in range(n):
                decimal += int(result[i]) * (2 ** (n - i - 1))
        
            return -decimal
        else:
            # Конвертируем положительное число в десятичное
            decimal = 0
            for i in range(n):
                decimal += int(bin_str[i]) * (2 ** (n - i - 1))
        
            return decimal


    @staticmethod
    def direct_code_to_decimal_int(binary_str):
        # Определяем знак по старшему биту
        if binary_str[0] == '1':
            sign = -1  # Отрицательное число
        else:
            sign = 1  # Положительное число

        # Преобразуем оставшиеся биты в десятичное число
        decimal_value = 0
        for i, bit in enumerate(binary_str[1:]):  # Игнорируем старший бит (знак)
            if bit == '1':
                decimal_value += 2 ** (len(binary_str) - 2 - i)  # Вес бита

        return sign * decimal_value


    @staticmethod
    def direct_code_to_decimal_float(binary):
        """
        Переводит дробное число из двоичного прямого кода в десятичный формат.
        """
        # Проверяем, есть ли точка в числе
        if '.' not in binary:
            binary += '.'  # Добавляем точку, если её нет

        # Разделяем на знаковый бит, целую и дробную части
        sign_bit = binary[0]
        int_part, frac_part = binary[1:].split('.')

        # Преобразуем целую часть
        int_decimal = 0
        for i, bit in enumerate(int_part):
            if bit == '1':
                int_decimal += 2 ** (len(int_part) - i - 1)

        # Преобразуем дробную часть
        frac_decimal = 0
        for i, bit in enumerate(frac_part):
            if bit == '1':
                frac_decimal += 2 ** -(i + 1)

        # Собираем результат
        decimal = int_decimal + frac_decimal
        if sign_bit == '1':
            decimal = -decimal

        return decimal


    @staticmethod
    def ieee754_to_decimal(binary_str):
        """
        Преобразует 32-битное число в формате IEEE 754 в десятичное.
        """
        # Проверяем длину строки
        if len(binary_str) != 32:
            raise ValueError("Длина двоичной строки должна быть 32 бита")

        # Разделяем биты на знак, экспоненту и мантиссу
        sign_bit = binary_str[0]  # Знаковый бит
        exponent_bits = binary_str[1:9]  # Экспонента
        mantissa_bits = binary_str[9:]   # Мантисса

        # Преобразуем знаковый бит
        sign = -1 if sign_bit == '1' else 1

        # Преобразуем экспоненту
        exponent = int(exponent_bits, 2) - 127  # Вычитаем смещение (bias)

        # Преобразуем мантиссу
        mantissa = 1.0  # Начинаем с неявной ведущей единицы
        for i, bit in enumerate(mantissa_bits):
            mantissa += int(bit) * (2 ** -(i + 1))

        # Вычисляем итоговое значение
        return sign * mantissa * (2 ** exponent)