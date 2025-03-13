from logical_expression import LogicalExpression

def print_menu():
    """Выводит меню на экран."""
    print("\nМеню:")
    print("1. Таблица истинности.")
    print("2. СДНФ и СКНФ.")
    print("3. СДНФ и СКНФ в числовой форме.")
    print("4. Индексная форма функции.")
    print("5. Выход.")

def main():
    expression_str = input("Введите логическое выражение (любые названия для переменных, знаки операций: &, |, ~, ->, !): ")
    
    try:
        expression = LogicalExpression(expression_str)
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    while True:
        print_menu()
        choose = input("Сделайте выбор: ")

        if choose == "1":
            expression.print_truth_table()
        elif choose == "2":
            pdnf = expression.generate_pdnf()
            pcnf = expression.generate_pcnf()
            print("\nСДНФ:", pdnf.get_expression())
            print("СКНФ:", pcnf.get_expression())
        elif choose == "3":
            numeric_form_pdnf = expression.to_numeric_form_pdnf()
            numeric_form_pcnf = expression.to_numeric_form_pcnf()
            print("\nСДНФ в числовой форме:", numeric_form_pdnf)
            print("СКНФ в числовой форме:", numeric_form_pcnf)
        elif choose == "4":
            index_form = expression.to_index_form()
            print("\nФункция в индексной форме:", index_form)
        elif choose == "5":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите от 1 до 5.")

if __name__ == "__main__":
    main()