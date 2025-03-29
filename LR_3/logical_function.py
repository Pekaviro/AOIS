from itertools import product, combinations
from collections import defaultdict


class LogicalFunction:
    def __init__(self, variables, expression):
        self.variables = sorted(variables)
        self.expression = expression
        self.truth_table = self._build_truth_table()
        self.minterms = self._get_minterms()
        self.maxterms = self._get_maxterms()
    
    def _build_truth_table(self):
        """Построение таблицы истинности для функции"""
        num_vars = len(self.variables)
        truth_table = []
        
        for values in product([0, 1], repeat=num_vars):
            assignment = dict(zip(self.variables, values))
            result = self._evaluate_expression(assignment)
            truth_table.append((values, result))
        
        return truth_table
    
    def _evaluate_expression(self, assignment):
        """Вычисление значения выражения при заданных значениях переменных"""
        # Заменяем переменные на их значения
        expr = self.expression
        for var, val in assignment.items():
            expr = expr.replace(var, str(val))
        
        # Заменяем логические операторы на Python-эквиваленты
        expr = expr.replace('!', ' not ').replace('|', ' or ').replace('&', ' and ')
        
        try:
            return int(eval(expr))
        except:
            raise ValueError("Неверное логическое выражение")
    
    def _get_minterms(self):
        """Получение минтермов (наборов, где функция = 1)"""
        return [values for values, result in self.truth_table if result == 1]
    
    def _get_maxterms(self):
        """Получение макстермов (наборов, где функция = 0)"""
        return [values for values, result in self.truth_table if result == 0]
        
    def _implicant_to_expression(self, implicant):
        terms = []
        for i, var in enumerate(self.variables):
            val = implicant[i]
            if val is None:
                continue  # Пропускаем склеенные переменные
            terms.append(f"!{var}" if val == 0 else var)
        return " & ".join(terms) if terms else "1"   
    
    def _maxterm_to_expression(self, maxterm):
        """Преобразование макстерма в логическое выражение с учетом None"""
        terms = []
        for i, var in enumerate(self.variables):
            if i >= len(maxterm):
                continue
            val = maxterm[i]
            if val is None:
                continue  # Пропускаем склеенные переменные
            terms.append(f"!{var}" if val == 1 else var)
        return "(" + " | ".join(terms) + ")" if terms else "1"
    
    def _get_prime_implicants(self, terms):
        """Нахождение всех простых импликантов для СКНФ"""
        groups = defaultdict(list)
        for term in terms:
            # Группируем по количеству единиц в терме
            groups[sum(term)].append(term)
        
        prime_implicants = set()
        changed = True
        
        while changed:
            changed = False
            new_groups = defaultdict(list)
            used = set()
            
            for k in sorted(groups.keys()):
                if k + 1 in groups:
                    for term1 in groups[k]:
                        for term2 in groups[k + 1]:
                            # Находим позиции, где термы отличаются
                            diff_pos = [i for i in range(len(term1)) if term1[i] != term2[i]]
                            if len(diff_pos) == 1:
                                # Создаем новый терм с None на позиции различия
                                new_term = list(term1)
                                new_term[diff_pos[0]] = None
                                new_term = tuple(new_term)
                                # Группируем по количеству не-None значений
                                new_groups[sum(1 for x in new_term if x is not None)].append(new_term)
                                used.add(tuple(term1))
                                used.add(tuple(term2))
                                changed = True
            
            # Добавляем неиспользованные термы в простые импликанты
            for group in groups.values():
                for term in group:
                    if tuple(term) not in used:
                        prime_implicants.add(tuple(term))
            
            groups = new_groups
        
        # Добавляем все оставшиеся термы из последней итерации
        for group in groups.values():
            for term in group:
                prime_implicants.add(tuple(term))
        
        return [list(imp) for imp in prime_implicants]
    
    def _select_essential_primes(self, prime_implicants, terms):
        """Выбор существенных простых импликантов (метод Петрика)"""
        # Создаем покрытие для каждого терма, используя tuples как ключи
        coverage = {tuple(term): [] for term in terms}  # Convert terms to tuples
        for i, implicant in enumerate(prime_implicants):
            for term in terms:
                if self._covers(implicant, term):
                    coverage[tuple(term)].append(i)  # Convert term to tuple
        
        # Упрощаем покрытие (удаляем доминирующие строки и столбцы)
        essential = set()
        remaining_terms = {tuple(term) for term in terms}  # Store as tuples
        
        # Находим существенные импликанты (которые покрывают хотя бы один терм единственным образом)
        while True:
            changed = False
            
            # Ищем термы, покрытые только одним импликантом
            for term in list(remaining_terms):
                if len(coverage[term]) == 1:
                    imp_index = coverage[term][0]
                    essential.add(imp_index)
                    changed = True
                    
                    # Удаляем все термы, покрытые этим импликантом
                    imp = prime_implicants[imp_index]
                    for t in list(remaining_terms):
                        if self._covers(imp, t):
                            remaining_terms.discard(t)
            
            if not changed:
                break
        
        # Если остались непокрытые термы, выбираем минимальное покрытие
        if remaining_terms:
            # Простой эвристический подход: выбираем импликанты, покрывающие больше всего оставшихся термов
            remaining_imp = [i for i in range(len(prime_implicants)) if i not in essential]
            remaining_imp.sort(key=lambda i: -sum(1 for t in remaining_terms if self._covers(prime_implicants[i], t)))
            
            for i in remaining_imp:
                imp = prime_implicants[i]
                covered = any(self._covers(imp, t) for t in remaining_terms)
                if covered:
                    essential.add(i)
                    remaining_terms = {t for t in remaining_terms if not self._covers(imp, t)}
                    if not remaining_terms:
                        break
        
        return [prime_implicants[i] for i in essential]
    
    def _covers(self, implicant, term):
        """Проверяет, покрывает ли импликант данный терм"""
        for i in range(len(term)):
            if implicant[i] is not None and implicant[i] != term[i]:
                return False
        return True
    
    def minimize_sdnf_calculus(self):
        """Минимизация СДНФ расчетным методом"""
        if not self.minterms:
            print("Результат после склеивания: 0")
            print("Окончательный результат: 0")
            return "0"
        
        # Если функция всегда истинна (все возможные комбинации)
        num_vars = len(self.variables)
        if len(self.minterms) == 2 ** num_vars:
            print("Функция всегда истинна")
            return "1"
        
        prime_implicants = self._get_prime_implicants(self.minterms)
        essential_primes = self._select_essential_primes(prime_implicants, self.minterms)
        
        # Форматируем результат
        simplified = list({self._implicant_to_expression(imp) for imp in prime_implicants})
        print(f"\nРезультат после склеивания: {' | '.join(simplified)}")
        
        final_expr = list({self._implicant_to_expression(imp) for imp in essential_primes})
        print(f"Окончательный результат: {' | '.join(final_expr)}")
        return ' | '.join(final_expr)

    def minimize_sknf_calculus(self):
        if not self.maxterms:
            print("Результат после склеивания: 1")
            print("Окончательный результат: 1")
            return "1"
        
        prime_implicants = self._get_prime_implicants(self.maxterms)
        essential_primes = self._select_essential_primes(prime_implicants, self.maxterms)
        
        # Форматируем результат
        simplified = list({self._maxterm_to_expression(imp) for imp in prime_implicants})
        print(f"\nРезультат после склеивания: {' & '.join(simplified)}")
        
        final_expr = list({self._maxterm_to_expression(imp) for imp in essential_primes})
        print(f"Окончательный результат: {' & '.join(final_expr)}")
        return ' & '.join(final_expr)
   
    def minimize_sdnf_table(self):
        """Минимизация СДНФ расчетно-табличным методом с красивым выводом таблицы"""
        if not self.minterms:
            print("\nРезультат после склеивания: 0")
            print("Окончательный результат: 0")
            return "0"
        
        prime_implicants = self._get_prime_implicants(self.minterms)
        essential_primes = self._select_essential_primes(prime_implicants, self.minterms)
        
        # Форматируем результаты
        simplified = list({self._implicant_to_expression(imp) for imp in prime_implicants})
        final_expr = list({self._implicant_to_expression(imp) for imp in essential_primes})
        
        # Построение таблицы покрытия с выравниванием
        print("\nТаблица:")
        
        # Определяем ширину столбцов
        term_widths = [len("".join(map(str, term))) for term in self.minterms]
        term_width = max(term_widths) + 2 if term_widths else 10
        imp_width = max(len(self._implicant_to_expression(imp)) for imp in prime_implicants) + 2
        
        # Шапка таблицы
        print(f"{'Импликанты':<{imp_width}}", end=" | ")
        for term in self.minterms:
            term_str = "".join(map(str, term)) 
            print(f"{term_str:^{term_width}}", end=" | ")
        print()
        
        # Разделительная линия
        print("-" * (imp_width + 2), end="+")
        print(("-" * (term_width + 2) + "+") * len(self.minterms))
        
        # Тело таблицы
        for imp in prime_implicants:
            imp_str = self._implicant_to_expression(imp)
            print(f"{imp_str:<{imp_width}}", end=" | ")
            for term in self.minterms:
                mark = "X" if self._covers(imp, term) else " "
                print(f"{mark:^{term_width}}", end=" | ")
            print()
        
        # Вывод результатов
        print(f"\nРезультат после склеивания: {' | '.join(simplified)}")
        print(f"Окончательный результат: {' | '.join(final_expr)}")
        return ' | '.join(final_expr)
    
    def minimize_sknf_table(self):
        """Минимизация СКНФ расчетно-табличным методом"""
        if not self.maxterms:
            print("\nРезультат после склеивания: 1")
            print("Окончательный результат: 1")
            return "1"

        # 1. Находим все простые импликанты (без инвертирования!)
        prime_implicants = self._get_prime_implicants(self.maxterms)
        
        # 2. Выбираем существенные импликанты (тоже без инвертирования)
        essential_primes = self._select_essential_primes(prime_implicants, self.maxterms)
        
        # 3. Формируем промежуточный результат
        simplified = list({self._maxterm_to_expression(imp) for imp in prime_implicants})
        print(f"\nРезультат после склеивания: {' & '.join(simplified)}")
        
        # 4. Построение таблицы покрытия
        print("\nТаблица покрытия:")
        
        # Определяем ширину столбцов
        term_widths = [len("".join(map(str, term))) for term in self.maxterms]
        term_width = max(term_widths) + 2 if term_widths else 10
        imp_width = max(len(self._maxterm_to_expression(imp)) for imp in prime_implicants) + 2
        
        # Шапка таблицы
        print(f"{'Импликанты':<{imp_width}}", end=" | ")
        for term in self.maxterms:
            term_str = "".join(map(str, term))
            print(f"{term_str:^{term_width}}", end=" | ")
        print()
        
        # Разделительная линия
        print("-" * (imp_width + 2), end="+")
        print(("-" * (term_width + 2) + "+") * len(self.maxterms))
        
        # Тело таблицы
        for imp in prime_implicants:
            expr = self._maxterm_to_expression(imp)
            print(f"{expr:<{imp_width}}", end=" | ")
            for term in self.maxterms:
                mark = "X" if self._covers(imp, term) else " "
                print(f"{mark:^{term_width}}", end=" | ")
            print()
        
        # Формируем итоговый результат
        final_expr = [self._maxterm_to_expression(imp) for imp in essential_primes]
        final_expr = list(set(final_expr))  # Удаляем дубликаты
        
        print("\nИтоговый результат:")
        if not final_expr:
            print("1")
            return "1"
        
        result = " & ".join(final_expr)
        print(result)
        return result
    
    def minimize_sdnf_kmap(self):
        """Минимизация СДНФ с помощью карт Карно"""
        if len(self.variables) not in [2, 3, 4, 5]:
            print("Карты Карно поддерживают только 2-5 переменных")
            return self.minimize_sdnf_calculus()
        
        kmap = self._build_karnaugh_map()
        print("\nКарта Карно:")
        self._print_karnaugh_map(kmap)
        
        # Находим максимальные покрытия единиц
        prime_implicants = self._find_prime_implicants(kmap, 1)

        # Выбираем минимальное покрытие
        essential_primes = self._select_essential_primes(prime_implicants, self.minterms)
        
        print("\nИтоговый результат:")
        if not essential_primes:
            return "0"
        
        result = " | ".join(self._implicant_to_expression(imp) for imp in essential_primes)
        print(result)
        return result
    
    def minimize_sknf_kmap(self):
        """Минимизация СКНФ с помощью карт Карно (исправленная версия)"""
        if len(self.variables) not in [2, 3, 4]:
            print("Карты Карно поддерживают только 2-4 переменных. Используется расчетный метод.")
            return self.minimize_sknf_calculus()  # Автоматически переключаемся на расчетный метод
        
        kmap = self._build_karnaugh_map()
        print("\nКарта Карно:")
        self._print_karnaugh_map(kmap)
        
        # Находим все максимальные импликанты для нулей
        prime_implicants = self._find_prime_implicants(kmap, 0)
        
        # Выбираем минимальное покрытие
        essential_primes = self._select_essential_primes(prime_implicants, self.maxterms)
        
        # Формируем результат
        if not essential_primes:
            return "1"
        
        result = " & ".join([self._maxterm_to_expression(imp) for imp in essential_primes])
        print("\nИтоговый результат:", result)
        return result

    def _find_prime_implicants(self, kmap, target):
        """Находит все простые импликанты для карты Карно"""
        size = len(self.variables)
        all_zeros = [k for k, v in kmap.items() if v == target]
        prime_implicants = []
        
        # Генерируем все возможные комбинации размеров групп
        for group_size in [4, 2, 1]:  # Для 4 переменных: 4, 2, 1
            for cells in combinations(all_zeros, group_size):
                if self._is_valid_group(cells):
                    imp = self._group_to_implicant(cells)
                    if imp not in prime_implicants:
                        prime_implicants.append(imp)
        
        # Удаляем дубликаты и подмножества
        prime_implicants = [imp for imp in prime_implicants 
                          if not any(self._covers(other, imp) for other in prime_implicants if other != imp)]
        return prime_implicants

    def _group_to_implicant(self, cells):
        """Преобразует группу клеток в импликант"""
        imp = [None] * len(self.variables)
        for i in range(len(self.variables)):
            values = set([cell[i] for cell in cells])
            if len(values) == 1:
                imp[i] = values.pop()
            else:
                imp[i] = None
        return tuple(imp)

    def _is_valid_group(self, cells):
        """Проверяет, образуют ли клетки допустимую группу в карте Карно"""
        num_vars = len(self.variables)
        if not cells:
            return False

        # Определяем фиксированные и нефиксированные переменные
        fixed = {}
        non_fixed = []
        
        for i in range(num_vars):
            values = {cell[i] for cell in cells}
            if len(values) == 1:
                fixed[i] = values.pop()
            else:
                non_fixed.append(i)
        
        # Проверяем соответствие размера группы
        expected_size = 2 ** len(non_fixed)
        if len(cells) != expected_size:
            return False
        
        # Генерируем все возможные комбинации для нефиксированных переменных
        from itertools import product
        required_combinations = product([0, 1], repeat=len(non_fixed))
        
        # Проверяем наличие всех комбинаций в группе
        for combo in required_combinations:
            # Собираем полный кортеж
            cell = list(cells[0])
            for idx in fixed:
                cell[idx] = fixed[idx]
            for i, var_idx in enumerate(non_fixed):
                cell[var_idx] = combo[i]
            
            if tuple(cell) not in cells:
                return False
        
        return True
    
    def _build_karnaugh_map(self):
        """Построение карты Карно"""
        num_vars = len(self.variables)
        kmap = {}
        
        # Генерируем все возможные комбинации переменных в порядке Грея
        gray_order = self._gray_code(num_vars)
        
        for values, result in self.truth_table:
            key = tuple(values)
            kmap[key] = result
        
        return kmap
    
    def _gray_code(self, n):
        """Генерация кода Грея для n битов"""
        if n == 0:
            return [[]]
        lower = self._gray_code(n - 1)
        return [[0] + x for x in lower] + [[1] + x for x in reversed(lower)]
    
    def _print_karnaugh_map(self, kmap):
        """Печать карты Карно"""
        num_vars = len(self.variables)
        
        if num_vars == 2:
            print("   b 0   1")
            print("a")
            print(f"0   {kmap[(0,0)]}   {kmap[(0,1)]}")
            print(f"1   {kmap[(1,0)]}   {kmap[(1,1)]}")
        
        elif num_vars == 3:
            print("  bc")
            print("a 00 01 11 10")
            print(f"0 {kmap[(0,0,0)]}  {kmap[(0,0,1)]}  {kmap[(0,1,1)]}  {kmap[(0,1,0)]}")
            print(f"1 {kmap[(1,0,0)]}  {kmap[(1,0,1)]}  {kmap[(1,1,1)]}  {kmap[(1,1,0)]}")
        
        elif num_vars == 4:
            print("   cd")
            print("ab 00 01 11 10")
            print(f"00 {kmap[(0,0,0,0)]}  {kmap[(0,0,0,1)]}  {kmap[(0,0,1,1)]}  {kmap[(0,0,1,0)]}")
            print(f"01 {kmap[(0,1,0,0)]}  {kmap[(0,1,0,1)]}  {kmap[(0,1,1,1)]}  {kmap[(0,1,1,0)]}")
            print(f"11 {kmap[(1,1,0,0)]}  {kmap[(1,1,0,1)]}  {kmap[(1,1,1,1)]}  {kmap[(1,1,1,0)]}")
            print(f"10 {kmap[(1,0,0,0)]}  {kmap[(1,0,0,1)]}  {kmap[(1,0,1,1)]}  {kmap[(1,0,1,0)]}")
        
        elif num_vars == 5:
            # Для 5 переменных карта будет 4x8
            print("Карта Карно для 5 переменных слишком большая для консоли")
            print("Вот сокращенный вариант:")
            for a in [0, 1]:
                print(f"\na={a}")
                print("  cde")
                print("b 000 001 011 010 110 111 101 100")
                for b in [0, 1]:
                    line = f"{b} "
                    for c, d, e in [(0,0,0), (0,0,1), (0,1,1), (0,1,0), (1,1,0), (1,1,1), (1,0,1), (1,0,0)]:
                        line += f" {kmap[(a,b,c,d,e)]}"
                    print(line)
    
    def _find_kmap_implicants(self, kmap, target):
        """Нахождение максимальных покрытий в карте Карно"""
        num_vars = len(self.variables)
        implicants = []
        
        # Для всех возможных размеров прямоугольников (начиная с наибольших)
        for size in range(num_vars, 0, -1):
            # Генерируем все возможные комбинации переменных для размера size
            for vars_to_keep in combinations(range(num_vars), num_vars - size):
                vars_to_change = [i for i in range(num_vars) if i not in vars_to_keep]
                
                # Проверяем все возможные фиксированные значения для оставшихся переменных
                for fixed_values in product([0, 1], repeat=num_vars - size):
                    # Создаем шаблон импликанта
                    imp = [None] * num_vars
                    for i, var in enumerate(vars_to_keep):
                        imp[var] = fixed_values[i]
                    
                    # Проверяем, все ли соответствующие клетки содержат target
                    valid = True
                    for changing_values in product([0, 1], repeat=size):
                        full_values = list(imp)
                        for i, var in enumerate(vars_to_change):
                            full_values[var] = changing_values[i]
                        
                        if kmap[tuple(full_values)] != target:
                            valid = False
                            break
                    
                    if valid:
                        # Проверяем, не покрыт ли этот импликант уже существующими
                        covered = False
                        for existing in implicants:
                            if self._kmap_imp_covered(existing, imp):
                                covered = True
                                break
                        
                        if not covered:
                            implicants.append(tuple(imp))
        
        return implicants
    
    def _kmap_imp_covered(self, imp1, imp2):
        """Проверяет, покрывает ли imp1 imp2 (imp2 более специфичный)"""
        for i in range(len(imp1)):
            if imp1[i] is not None and imp1[i] != imp2[i]:
                return False
        return True