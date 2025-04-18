import re
from logical_function import LogicalFunction
from LR_2.logical_expression import LogicalExpression

def main():
    print("Минимизация логических функций")
    print("Доступные переменные: a, b, c, d, e")
    print("Логические операторы: ! (НЕ), | (ИЛИ), & (И), -> (импликация), ~ (эквивалентность)")
    
    expression = input("\nВведите логическое выражение: ")
    
    logical_expr = LogicalExpression(expression)
    
    variables = sorted(logical_expr.variable_manager.get_variable_map().keys())
    if not variables:
        print("Не найдено переменных в выражении")
        return

    truth_table = logical_expr.generate_truth_table()
    
    
    print("\nМинимизация СДНФ расчетным методом:")
    lf_pdnf = LogicalFunction(variables, expression, truth_table)
    lf_pdnf.minimize_sdnf_calculus()

    print("\nМинимизация СКНФ расчетным методом:")
    lf_pcnf = LogicalFunction(variables, expression, truth_table)
    lf_pcnf.minimize_sknf_calculus()

    print("\nМинимизация СДНФ расчетно-табличным методом:")
    lf_pdnf.minimize_sdnf_table()

    print("\nМинимизация СКНФ расчетно-табличным методом:")
    lf_pcnf.minimize_sknf_table()

    lf_pcnf.display_kmap()

    print("\nМинимизация СДНФ табличным методом (карта Карно):")
    print(f"Минимизированная функция: {lf_pdnf.minimize_with_kmap(is_dnf=True)}")

    print("\nМинимизация СКНФ табличным методом (карта Карно):")
    print(f"Минимизированная функция: {lf_pcnf.minimize_with_kmap(is_dnf=False)}")

if __name__ == "__main__":
    main()
