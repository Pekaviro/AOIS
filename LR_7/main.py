from matrix import Matrix

def main():
    matrix = Matrix()
    
    while True:
        print("\nМеню:")
        print("1. Вывести таблицу")
        print("2. Применить логическую функцию")
        print("3. Поиск в интервале")
        print("4. Арифметическая операция")
        print("5. Выход")
        
        choice = input("Выберите действие: ")
        
        if choice == '1':
            matrix.print_matrix()
        
        elif choice == '2':
            try:
                func = input("Введите функцию (f2, f7, f8, f13): ").strip()
                col1 = int(input("Номер первого столбца (0-15): "))
                col2 = int(input("Номер второго столбца (0-15): "))
                target_col = int(input("Целевой столбец (0-15): "))
                if not (0 <= col1 <=15 and 0 <= col2 <=15 and 0 <= target_col <=15):
                    raise ValueError
                matrix.apply_logical_function(func, col1, col2, target_col)
                print("Операция выполнена")
            except Exception as e:
                print(f"Ошибка: {e}")
        
        elif choice == '3':
            try:
                lower = int(input("Нижняя граница(можно десятичным числом): "))
                upper = int(input("Верхняя граница(можно десятичным числом): "))
                results = matrix.search_interval(lower, upper)
                print(f"Найденные индексы: {results}")
            except Exception as e:
                print(f"Ошибка: {e}")
        
        elif choice == '4':
            try:
                v_input = input("Ключ V (3 бита как двоичная строка или число 0-7): ").strip()
                
                # Проверяем, является ли ввод двоичной строкой (например, '100')
                if all(c in '01' for c in v_input):
                    if len(v_input) != 3:
                        raise ValueError("Двоичная строка должна быть ровно 3 бита (например, '100')")
                    v_key = v_input  # Сохраняем как строку '100'
                
                # Если ввод — десятичное число (0-7)
                elif v_input.isdigit():
                    v_key = int(v_input)
                    if v_key < 0 or v_key > 7:
                        raise ValueError("Число должно быть от 0 до 7")
                
                # Некорректный ввод (например, '102', 'abc')
                else:
                    raise ValueError("Введите 3-битную двоичную строку (например, '100') или число 0-7")
                
                matrix.arithmetic_operation(v_key)
                print("Операция выполнена")
            
            except Exception as e:
                print(f"Ошибка: {e}")
        
        elif choice == '5':
            print("Выход")
            break
        
        else:
            print("Неверный ввод")

if __name__ == "__main__":
    main()