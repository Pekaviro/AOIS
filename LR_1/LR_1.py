from binary_calculator import BinaryCalculator
from binary_converter import BinaryConverter
from decimal_converter import DecimalConverter



def print_choice_of_numeric_format():
    print("Выберите формат чисел:")
    print("1. Целые числа")
    print("2. Дробные числа (положительные)")
    print("3. Выход")

def print_choice_of_operation():
    print("Выберите операцию:")
    print("1. Сложение")
    print("2. Вычитание")
    print("3. Умножение")
    print("4. Деление")
    print("5. Вернуться в главное меню")

def get_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Ошибка: Введите целое число.")

def get_positive_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
            else:
                print("Ошибка: Число должно быть положительным.")
        except ValueError:
            print("Ошибка: Введите число.")

def main():
    while True:
        print_choice_of_numeric_format()
        choice_1 = input()

        if choice_1 == '1':  # Целые числа
            num1 = get_integer_input("Введите первое число: ")
            num2 = get_integer_input("Введите второе число: ")

            converter1 = BinaryConverter(num1)
            converter2 = BinaryConverter(num2)

            print("\nПервое число:")
            print(converter1)

            print("\nВторое число:")
            print(converter2)

            while True:  # Цикл для операций с целыми числами
                print_choice_of_operation()
                choice_2 = input()

                if choice_2 == '1':
                    result = BinaryCalculator.sum_additional_code(converter1.additional_code(), converter2.additional_code())
                    print(f"\nРезультат в дополнительном коде: {result}")
                    print(f"Результат в десятичном формате: {DecimalConverter.additional_code_to_decimal(result)}")
                elif choice_2 == '2':
                    result = BinaryCalculator.subtract_additional_code(converter1.additional_code(), converter2.additional_code())
                    print(f"\nРезультат в дополнительном коде: {result}")
                    print(f"Результат в десятичном формате: {DecimalConverter.additional_code_to_decimal(result)}")
                elif choice_2 == '3': 
                    result = BinaryCalculator.multiply_direct_code(converter1.direct_code(), converter2.direct_code())
                    print(f"\nРезультат в прямом коде: {result}")
                    print(f"Результат в десятичном формате: {DecimalConverter.direct_code_to_decimal_int(result)}")
                elif choice_2 == '4': 
                    result = BinaryCalculator.division_direct_code(converter1.direct_code(), converter2.direct_code())
                    print(f"\nРезультат в прямом коде: {result}")
                    print(f"Результат в десятичном формате: {DecimalConverter.direct_code_to_decimal_float(result)}")
                elif choice_2 == '5':
                    break
                else:
                    print("Ошибка: Неверный выбор.")

        elif choice_1 == '2':  # Дробные числа
            num1 = get_positive_float_input("Введите первое число: ")
            num2 = get_positive_float_input("Введите второе число: ")

            converter1 = BinaryConverter(num1)
            converter2 = BinaryConverter(num2)

            print("\nПервое число:")
            print(converter1)

            print("\nВторое число:")
            print(converter2)

            result = BinaryCalculator.sum_ieee754(converter1.ieee754(), converter2.ieee754())
            print(f"\nРезультат сложения (IEEE754): {result}")
            print(f"Результат в десятичном формате: {DecimalConverter.ieee754_to_decimal(result)}")

        elif choice_1 == '3':  # Выход
            print("Выход из программы.")
            break 

        else:
            print("Ошибка: Неверный выбор.")

if __name__ == "__main__":
    main()
