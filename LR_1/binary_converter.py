PLUS_TO_EXPONENT = 127
BITS_OF_MANTISSA = 23


class BinaryConverter:
    def __init__(self, number):
        self.number = number


    @staticmethod
    def to_binary(num: int) -> str:
        """Переводит целую часть числа в двоичный формат (без знака)."""
        if num == 0:
            return "0"  # Особый случай для числа 0

        binary = ""
        while num > 0:
            binary = str(num % 2) + binary  # Добавляем остаток в начало строки
            num = num // 2  # Делим число на 2
        return binary


    @staticmethod
    def frac_to_binary(frac: float, precision: int = 10) -> str:
        """Переводит дробную часть числа в двоичный формат."""
        binary = ""
        while frac and len(binary) < precision:
            frac *= 2
            bit = int(frac)
            binary += str(bit)
            frac -= bit
        return binary


    def direct_code(self) -> str:
        """Возвращает прямой код числа (включая дробную часть, если она есть)."""
        # Разделяем число на целую и дробную части
        int_part = int(abs(self.number))
        frac_part = abs(self.number) - int_part

        # Преобразуем целую часть
        int_binary = self.to_binary(int_part)

        # Преобразуем дробную часть, если она есть
        if frac_part != 0:
            frac_binary = self.frac_to_binary(frac_part)
            binary = int_binary + '.' + frac_binary
        else:
            binary = int_binary

        # Добавляем знаковый бит
        if self.number >= 0:
            return '0' + binary
        else:
            return '1' + binary


    def reverse_code(self) -> str:
        """Возвращает обратный код числа (включая дробную часть)."""
        direct = self.direct_code()
        if self.number >= 0:
            return direct
        else:
            # Инвертируем все биты, кроме знакового
            reversed_bits = '1'
            for bit in direct[1:]:  # Пропускаем знаковый бит
                if bit == '0':
                    reversed_bits += '1'
                elif bit == '1':
                    reversed_bits += '0'
                else:
                    reversed_bits += '.'  # Сохраняем точку
            return reversed_bits


    def additional_code(self) -> str:
        """Возвращает дополнительный код числа (включая дробную часть)."""
        reverse = self.reverse_code()
        if self.number >= 0:
            return reverse
        else:
            # Разделяем на целую и дробную части
            reverse_list = reverse.split('.')
            int_part = reverse_list[0]  # Целая часть всегда есть

            # Если есть дробная часть, обрабатываем её
            if len(reverse_list) > 1:
                frac_part = reverse_list[1]
                # Добавляем 1 к дробной части
                frac_list = list(frac_part)
                carry = 1
                for i in range(len(frac_list) - 1, -1, -1):
                    if frac_list[i] == '0' and carry == 1:
                        frac_list[i] = '1'
                        carry = 0
                    elif frac_list[i] == '1' and carry == 1:
                        frac_list[i] = '0'
                frac_part = ''.join(frac_list)
                return int_part + '.' + frac_part
            else:
                # Если дробной части нет, добавляем 1 к целой части
                int_list = list(int_part)
                carry = 1
                for i in range(len(int_list) - 1, -1, -1):
                    if int_list[i] == '0' and carry == 1:
                        int_list[i] = '1'
                        carry = 0
                    elif int_list[i] == '1' and carry == 1:
                        int_list[i] = '0'
                int_part = ''.join(int_list)
                return int_part



    def ieee754(self):
        # Получаем знак числа
        if self.number>= 0:
            sign_bit = 0 
        else: 
            raise ValueError("Метод поддерживает только положительные числа.")

        num = abs(self.number)
    
        # Преобразуем целую часть и десятичную часть в двоичную форму
        int_part = int(num)
        frac_part = num - int_part
    
        int_bin = BinaryConverter.to_binary(int_part)
    
        frac_bin = BinaryConverter.frac_to_binary(frac_part)
    
        # Объединяем целую и дробную часть
        binary = int_bin + "." + frac_bin
    
        # Преобразуем двоичное число в научную запись с основанием 2
        dot_index = binary.index(".")
        first_one_index = binary.index("1")
    
        exponent = dot_index - first_one_index - 1
        mantissa = binary[first_one_index+1:dot_index] + binary[dot_index+1:]
    
        # Получаем показатель степени в двоичной форме
        exponent += PLUS_TO_EXPONENT

        exponent_bin = BinaryConverter.to_binary(exponent).rjust(8, '0')
    
        # Получаем мантиссу
        mantissa = mantissa[:BITS_OF_MANTISSA]
    
        # Компилируем итоговое число
        ieee754 = f"{sign_bit}{exponent_bin}{mantissa.ljust(BITS_OF_MANTISSA, '0')}"
    
        return ieee754



    def __str__(self):
        return (f"Число введено: {self.number}\n"
                f"Прямой код: {self.direct_code()}\n"
                f"Обратный код: {self.reverse_code()}\n"
                f"Дополнительный код: {self.additional_code()}")


# Пример использования
if __name__ == "__main__":
    num1 = float(input("Введите первое число: "))
    num2 = float(input("Введите второе число: "))

    converter1 = BinaryConverter(num1)
    converter2 = BinaryConverter(num2)

    print("\nПервое число:")
    print(converter1)

    print("\nВторое число:")
    print(converter2)

    print(f"\nРезультат в стандарте: {converter1.ieee754(), converter2.ieee754()}")