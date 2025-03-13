from binary_converter import BinaryConverter
from decimal_converter import DecimalConverter

BITS_OF_MANTISSA = 24
BITS_OF_IEEE754 = 32
BITS_OF_EXPONENT = 9


class BinaryCalculator:
    @staticmethod
    def sign_extend(bin_str: str, new_len: int) -> str:
        """Расширяет двоичное число до new_len бит с учетом знака.
        Если число отрицательное (начинается с '1'), добавляются единицы, иначе – добавляются нули.
        """
        if len(bin_str) >= new_len:
            return bin_str
        sign_bit = bin_str[0]
        return sign_bit * (new_len - len(bin_str)) + bin_str

    def add_binaries(bin1, bin2):
        max_len = max(len(bin1), len(bin2))
    
        # Дополняем строки нулями до одинаковой длины
        bin1 = bin1.zfill(max_len)
        bin2 = bin2.zfill(max_len)
    
        carry = 0
        result = []
    
        # Идем с конца строки к началу
        for i in range(max_len - 1, -1, -1):
            bit_a = int(bin1[i])
            bit_b = int(bin2[i])
        
            sum_bits = bit_a + bit_b + carry
            result_bit = sum_bits % 2
            carry = sum_bits // 2
        
            result.insert(0, str(result_bit))
    
        if carry:
            result.insert(0, str(carry))
    
        return ''.join(result)


    @staticmethod
    def sum_additional_code(bin1, bin2):
        max_len = max(len(bin1), len(bin2)) + 1  # Увеличиваем max_len на 1
        bin1 = BinaryCalculator.sign_extend(bin1, max_len)
        bin2 = BinaryCalculator.sign_extend(bin2, max_len)

        result = BinaryCalculator.add_binaries(bin1, bin2)

        # Если результат длиннее max_len, обрезаем лишний бит
        if len(result) > max_len:
            result = result[-max_len:]

        return result


    @staticmethod
    def subtract_additional_code(bin1: str, bin2: str) -> str:
        """Вычитает два двоичных числа в дополнительном коде."""
        # Увеличиваем max_len на 1, чтобы учесть возможный перенос
        max_len = max(len(bin1), len(bin2)) + 1
        bin1 = BinaryCalculator.sign_extend(bin1, max_len)
        bin2 = BinaryCalculator.sign_extend(bin2, max_len)

        # Инвертируем биты bin2
        inverted_bin2 = ''.join('1' if bit == '0' else '0' for bit in bin2)

        # Добавляем 1 к инвертированному bin2 (получаем дополнительный код)
        bin2_twos_complement = BinaryCalculator.sum_additional_code(inverted_bin2, '1'.zfill(max_len))

        # Складываем bin1 и bin2_twos_complement
        result = BinaryCalculator.sum_additional_code(bin1, bin2_twos_complement)

        # Обрезаем результат до max_len
        if len(result) > max_len:
            result = result[-max_len:]

        return result


    @staticmethod
    def multiply_direct_code(bin1: str, bin2: str) -> str:
        """Умножает два двоичных числа в прямом коде."""

        # Определяем знак результата
        sign = '0' if bin1[0] == bin2[0] else '1'

        # Работаем с модулями чисел
        bin1_mod = bin1[1:] if len(bin1) > 1 else bin1
        bin2_mod = bin2[1:] if len(bin2) > 1 else bin2

        # Инициализируем результат нулями
        result = '0'

        # Умножение модулей
        for i in range(len(bin2_mod) - 1, -1, -1):
            if bin2_mod[i] == '1':
                # Сдвигаем bin1_mod на (len(bin2_mod) - 1 - i) позиций влево
                shifted_bin1 = bin1_mod + '0' * (len(bin2_mod) - 1 - i)
                # Складываем result и shifted_bin1
                result = BinaryCalculator.add_binaries(result, shifted_bin1)

        # Добавляем знак к результату
        return sign + result


    @staticmethod
    def division_direct_code(dividend, divisor, precision=5):
        """
        Выполняет деление двух двоичных чисел в прямом коде.
        Возвращает результат с точностью до precision знаков после запятой.
        Удаляет лишние нули перед знаковым битом в целой части.
        """
        # Определяем знак результата
        sign = '0' if dividend[0] == divisor[0] else '1'
    
        # Работаем с абсолютными значениями
        dividend = dividend[1:]  # Убираем знаковый бит
        divisor = divisor[1:]    # Убираем знаковый бит
    
        # Если делитель равен нулю
        if all(bit == '0' for bit in divisor):
            raise ValueError("Деление на ноль невозможно")
    
        # Добавляем нули для дробной части
        dividend += '0' * precision
    
        # Инициализация
        result = ''
        remainder = ''
    
        # Деление в столбик
        for bit in dividend:
            remainder += bit
            if len(remainder) < len(divisor):
                result += '0'
                continue
            if BinaryCalculator.binary_compare(remainder, divisor) >= 0:
                result += '1'
                remainder = BinaryCalculator.subtract_direct_code(remainder, divisor)
            else:
                result += '0'
    
        # Вставляем точку
        result = result[:-precision] + '.' + result[-precision:]
    
        # Удаляем ведущие нули в целой части
        int_part, frac_part = result.split('.')
        int_part = int_part.lstrip('0') or '0'  # Удаляем ведущие нули, оставляя хотя бы один ноль
        result = int_part + '.' + frac_part
    
        # Возвращаем результат с учетом знака
        return sign + result


    @staticmethod
    def binary_compare(bin1, bin2):
        """
        Сравнивает два двоичных числа.
        Возвращает 1, если bin1 > bin2; 0, если bin1 == bin2; -1, если bin1 < bin2.
        """
        if len(bin1) > len(bin2):
            bin2 = bin2.zfill(len(bin1))
        else:
            bin1 = bin1.zfill(len(bin2))
        if bin1 > bin2:
            return 1
        elif bin1 == bin2:
            return 0
        else:
            return -1


    @staticmethod
    def subtract_direct_code(bin1, bin2):
        """
        Вычитает два двоичных числа (bin1 - bin2).
        """
        if len(bin1) > len(bin2):
            bin2 = bin2.zfill(len(bin1))
        else:
            bin1 = bin1.zfill(len(bin2))
        result = []
        borrow = 0
        for i in range(len(bin1) - 1, -1, -1):
            bit_a = int(bin1[i])
            bit_b = int(bin2[i])
            diff = bit_a - bit_b - borrow
            if diff < 0:
                diff += 2
                borrow = 1
            else:
                borrow = 0
            result.append(str(diff))
        return ''.join(reversed(result)).lstrip('0') or '0'


    @staticmethod
    def sum_ieee754(bin1: str, bin2: str) -> str:
        """Складывает два положительных числа в формате IEEE-754 (32 бита)."""
        # Проверка длины входных строк
        if len(bin1) != BITS_OF_IEEE754 or len(bin2) != BITS_OF_IEEE754:
            raise ValueError("Входные строки должны быть длиной 32 бита.")

        # Разбор первого числа
        sign1 = bin1[0]
        exponent1 = bin1[1:BITS_OF_EXPONENT]  # Экспонента (смещенная)
        mantissa1 = '1' + bin1[BITS_OF_EXPONENT:]  # Мантисса (с ведущей единицей)

        # Разбор второго числа
        sign2 = bin2[0]
        exponent2 = bin2[1:BITS_OF_EXPONENT]  # Экспонента (смещенная)
        mantissa2 = '1' + bin2[BITS_OF_EXPONENT:]  # Мантисса (с ведущей единицей)

        # Проверка на положительные числа
        if sign1 != '0' or sign2 != '0':
            raise ValueError("Метод поддерживает только положительные числа.")

        # Преобразование экспонент в целые числа
        exp1 = int(exponent1, 2)
        exp2 = int(exponent2, 2)

        # Выравнивание экспонент
        if exp1 > exp2:
            shift = exp1 - exp2
            mantissa2 = '0' * shift + mantissa2  # Сдвигаем мантиссу второго числа вправо
            mantissa2 = mantissa2[:BITS_OF_MANTISSA]  # Обрезаем до 24 бит
            exp2 = exp1  # Обновляем экспоненту
        elif exp2 > exp1:
            shift = exp2 - exp1
            mantissa1 = '0' * shift + mantissa1  # Сдвигаем мантиссу первого числа вправо
            mantissa1 = mantissa1[:BITS_OF_MANTISSA]  # Обрезаем до 24 бит
            exp1 = exp2  # Обновляем экспоненту

        # Сложение мантисс
        mantissa_sum = BinaryCalculator.add_binaries(mantissa1, mantissa2)

        # Нормализация результата
        if len(mantissa_sum) > BITS_OF_MANTISSA:  # Если произошел перенос
            mantissa_sum = mantissa_sum[:-1]  # Сдвигаем мантиссу вправо
            exp1 += 1  # Увеличиваем экспоненту
        elif len(mantissa_sum) < BITS_OF_MANTISSA:  # Если мантисса слишком короткая
            mantissa_sum += '0' * (BITS_OF_MANTISSA - len(mantissa_sum))  # Дополняем нулями справа

        # Убираем ведущую единицу (она подразумевается)
        mantissa_sum = mantissa_sum[1:BITS_OF_MANTISSA]

        # Преобразуем экспоненту обратно в строку из 8 бит
        exponent1 = f"{exp1:08b}"

        # Объединяем все части
        ieee754 = f'0{exponent1}{mantissa_sum}'
        return ieee754
