import re
from logical_function import LogicalFunction


def main():
    print("Минимизация логических функций")
    print("Доступные переменные: a, b, c, d, e")
    print("Логические операторы: ! (НЕ), | (ИЛИ), & (И)")
    
    while True:  # Главный цикл программы
        # Выбор типа формы
        while True:
            print("\nВыберите тип логической формы:")
            print("1. СДНФ (Совершенная дизъюнктивная нормальная форма)")
            print("2. СКНФ (Совершенная конъюнктивная нормальная форма)")
            print("0. Выход из программы")
            
            form_choice = input("Ваш выбор: ")
            
            if form_choice == '0':
                return  # Выход из программы
            elif form_choice in ('1', '2'):
                break
            else:
                print("Неверный выбор, попробуйте снова")
        
        # Ввод формулы
        expression = input("\nВведите логическое выражение: ")
        
        # Извлекаем переменные из выражения
        variables = sorted(set(re.findall(r'\b[a-e]\b', expression)))
        if not variables:
            print("Не найдено переменных в выражении")
            continue  # Возвращаемся к выбору формы
        
        print(f"\nИспользуемые переменные: {', '.join(variables)}")
        
        try:
            lf = LogicalFunction(variables, expression)
        except ValueError as e:
            print(f"Ошибка: {e}")
            continue  # Возвращаемся к выбору формы
        
        # Выбор метода минимизации
        while True:
            print("\nВыберите метод минимизации:")
            print("1. Расчетный метод")
            print("2. Расчетно-табличный метод")
            print("3. Табличный метод (карта Карно)")
            print("0. Вернуться к выбору формы")
            
            method_choice = input("Ваш выбор: ")
            
            if method_choice == '0':
                break  # Выходим из цикла методов, возвращаемся к выбору формы
            elif form_choice == '1' and method_choice == '1':
                print("\nМинимизация СДНФ расчетным методом:")
                lf.minimize_sdnf_calculus()
            elif form_choice == '1' and method_choice == '2':
                print("\nМинимизация СДНФ расчетно-табличным методом:")
                lf.minimize_sdnf_table()
            elif form_choice == '1' and method_choice == '3':
                print("\nМинимизация СДНФ табличным методом (карта Карно):")
                lf.minimize_sdnf_kmap()
            elif form_choice == '2' and method_choice == '1':
                print("\nМинимизация СКНФ расчетным методом:")
                lf.minimize_sknf_calculus()
            elif form_choice == '2' and method_choice == '2':
                print("\nМинимизация СКНФ расчетно-табличным методом:")
                lf.minimize_sknf_table()
            elif form_choice == '2' and method_choice == '3':
                print("\nМинимизация СКНФ табличным методом (карта Карно):")
                lf.minimize_sknf_kmap()
            else:
                print("Неверный выбор, попробуйте снова")


if __name__ == "__main__":
    main()
