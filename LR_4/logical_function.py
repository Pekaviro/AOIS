from itertools import product, combinations
from collections import defaultdict
from typing import List


class LogicalFunction:
    def __init__(self, variables, expression, truth_table):
        self.variables = variables
        self.expression = expression
        self.truth_table = truth_table
        self.minterms = self._get_minterms()
        self.maxterms = self._get_maxterms()
    
    def _evaluate_expression(self, assignment):
        """Вычисление значения выражения при заданных значениях переменных"""
        expr = self.expression
        for var, val in assignment.items():
            expr = expr.replace(var, str(val))
        
        expr = expr.replace('!', ' not ').replace('|', ' or ').replace('&', ' and ')
        
        try:
            return int(eval(expr))
        except:
            raise ValueError("Неверное логическое выражение")
    
    def _get_minterms(self) -> List[List[int]]:
        """Возвращает список бинарных представлений минтермов."""
        truth_values = self.truth_table.get(self.expression, None)
        if truth_values is None:
            truth_values = []
            for assignment in product([0, 1], repeat=len(self.variables)):
                assignment_dict = dict(zip(self.variables, assignment))
                truth_values.append(self._evaluate_expression(assignment_dict))
        
        return [self._minterm_to_binary(i) for i, val in enumerate(truth_values) if val]

    def _get_maxterms(self) -> List[List[int]]:
        """Возвращает список бинарных представлений макстермов."""
        truth_values = self.truth_table.get(self.expression, None)
        if truth_values is None:
            truth_values = []
            for assignment in product([0, 1], repeat=len(self.variables)):
                assignment_dict = dict(zip(self.variables, assignment))
                truth_values.append(self._evaluate_expression(assignment_dict))
        
        return [self._minterm_to_binary(i) for i, val in enumerate(truth_values) if not val]

    def _minterm_to_binary(self, minterm_index: int) -> List[int]:
        """Представляет минтермы в бинарном коде"""
        binary = []
        for i in range(len(self.variables)):
            binary.append((minterm_index >> (len(self.variables) - i - 1)) & 1)
        return binary    
        
    def _implicant_to_expression(self, implicant):
        terms = []
        for i, var in enumerate(self.variables):
            val = implicant[i]
            if val is None:
                continue
            terms.append(f"!{var}" if val == 0 else var)
        return " & ".join(terms) if terms else "1"   
    
    def _maxterm_to_expression(self, maxterm):
        terms = []
        for i, var in enumerate(self.variables):
            if i >= len(maxterm):
                continue
            val = maxterm[i]
            if val is None:
                continue
            terms.append(f"!{var}" if val == 1 else var)
        return "(" + " | ".join(terms) + ")" if terms else "1"

    def _glue_terms(self, term1, term2):
        diff = 0
        glued = []
        for v1, v2 in zip(term1, term2):
            if v1 == v2:
                glued.append(v1)
            elif v1 is None or v2 is None:
                return None
            else:
                diff += 1
                glued.append(None)
        
        return tuple(glued) if diff == 1 else None   

    def _get_prime_implicants(self, terms):
        current_implicants = {tuple(term) for term in terms}
        prime_implicants = set()
        
        changed = True
        while changed:
            changed = False
            new_implicants = set()
            used = set()
            
            for imp1 in current_implicants:
                for imp2 in current_implicants:
                    if imp1 != imp2:
                        glued = self._glue_terms(imp1, imp2)
                        if glued is not None:
                            new_implicants.add(glued)
                            used.add(imp1)
                            used.add(imp2)
                            changed = True
            
            for imp in current_implicants:
                if imp not in used:
                    prime_implicants.add(imp)
            
            current_implicants = new_implicants
        
        return [list(imp) for imp in prime_implicants]
    
    def _select_essential_primes(self, prime_implicants, terms):
        coverage = {tuple(term): [] for term in terms}
        for i, implicant in enumerate(prime_implicants):
            for term in terms:
                if self._covers(implicant, term):
                    coverage[tuple(term)].append(i)
        
        essential = set()
        remaining_terms = {tuple(term) for term in terms}
        
        while True:
            changed = False
            
            for term in list(remaining_terms):
                if len(coverage[term]) == 1:
                    imp_index = coverage[term][0]
                    essential.add(imp_index)
                    changed = True
                    
                    for t in list(remaining_terms):
                        if self._covers(prime_implicants[imp_index], t):
                            remaining_terms.discard(t)
            
            if not changed:
                break
        
        if remaining_terms:
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
        for i in range(len(term)):
            if implicant[i] is not None and implicant[i] != term[i]:
                return False
        return True
    
    def _generate_gray_codes(self, num_bits):
        """Генерирует коды Грея заданной длины."""
        return [num ^ (num >> 1) for num in range(1 << num_bits)]
    
    def _convert_to_binary_terms(self, terms, variable_count):
        """Преобразует список терминов в их бинарное представление."""
        return [tuple((term >> bit) & 1 for bit in reversed(range(variable_count))) for term in terms]
    
    def _try_merge_implicants(self, implicant1, implicant2):
        """Пытается объединить два импликанта."""
        difference_count = 0
        merged = []
        for bit1, bit2 in zip(implicant1, implicant2):
            if bit1 != bit2:
                difference_count += 1
                merged.append('-')
            else:
                merged.append(bit1)
            if difference_count > 1:
                return None
        return tuple(merged) if difference_count == 1 else None
    
    def _find_prime_implicants_kmap(self, minterms, variable_count):
        """Находит все простые импликанты для карт Карно."""
        groups = defaultdict(list)
        for term in minterms:
            groups[term.count(1)].append(term)
        
        prime_implicants = set()
        unchecked = set(minterms)
        
        while groups:
            new_groups = defaultdict(list)
            used = set()
            
            for group_index in sorted(groups):
                for current_term in groups[group_index]:
                    for next_term in groups.get(group_index + 1, []):
                        merged = self._try_merge_implicants(current_term, next_term)
                        if merged:
                            used.add(current_term)
                            used.add(next_term)
                            new_groups[merged.count(1)].append(merged)
            
            prime_implicants.update(unchecked - used)
            unchecked = set()
            for term_list in new_groups.values():
                unchecked.update(term_list)
            
            groups = defaultdict(list)
            for term in unchecked:
                groups[term.count(1)].append(term)
        
        return prime_implicants
    
    def _is_covering(self, implicant, minterm):
        """Проверяет, покрывает ли импликант данный минтерм."""
        return all(imp_bit == '-' or imp_bit == min_bit for imp_bit, min_bit in zip(implicant, minterm))
    
    def _select_essential_primes_kmap(self, prime_implicants, minterms):
        """Выбирает существенные импликанты для карт Карно."""
        coverage_table = {pi: [mt for mt in minterms if self._is_covering(pi, mt)] for pi in prime_implicants}
        essential_primes = set()
        covered_minterms = set()
        
        for minterm in minterms:
            covering = [pi for pi in prime_implicants if self._is_covering(pi, minterm)]
            if len(covering) == 1:
                essential_primes.add(covering[0])
        
        for implicant in essential_primes:
            covered_minterms.update(coverage_table[implicant])
        
        remaining_minterms = set(minterms) - covered_minterms
        while remaining_minterms:
            best_implicant = max(
                coverage_table.items(),
                key=lambda item: len(set(item[1]) & remaining_minterms))
            essential_primes.add(best_implicant[0])
            remaining_minterms -= set(best_implicant[1])
        
        return essential_primes
    
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

        # Находим все простые импликанты
        prime_implicants = self._get_prime_implicants(self.maxterms)
        
        # Выбираем существенные импликанты
        essential_primes = self._select_essential_primes(prime_implicants, self.maxterms)
        
        # Формируем промежуточный результат
        simplified = list({self._maxterm_to_expression(imp) for imp in prime_implicants})
        print(f"\nРезультат после склеивания: {' & '.join(simplified)}")
        
        # Построение таблицы покрытия
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
        
        final_expr = [self._maxterm_to_expression(imp) for imp in essential_primes]
        final_expr = list(set(final_expr)) 
        
        print("\nИтоговый результат:")
        if not final_expr:
            print("1")
            return "1"
        
        result = " & ".join(final_expr)
        print(result)
        return result
     
    def minimize_with_kmap(self, is_dnf=True):
        """Минимизация с использованием карт Карно."""
        terms = [int(''.join(map(str, term)), 2) for term in (self.minterms if is_dnf else self.maxterms)]
        variable_count = len(self.variables)
        
        binary_terms = self._convert_to_binary_terms(terms, variable_count)
        prime_implicants = self._find_prime_implicants_kmap(binary_terms, variable_count)
        essential_primes = self._select_essential_primes_kmap(prime_implicants, binary_terms)
        
        operator = ' & ' if is_dnf else ' | '
        result_terms = []
        
        for implicant in essential_primes:
            components = []
            for var_name, bit in zip(self.variables, implicant):
                if bit == '-':
                    continue
                if is_dnf:
                    components.append(var_name if bit else f"!{var_name}")
                else:
                    components.append(f"!{var_name}" if bit else var_name)
            
            term = "(" + operator.join(components) + ")" if components else "1"
            result_terms.append(term)
        
        main_operator = ' | ' if is_dnf else ' & '
        return main_operator.join(result_terms) if result_terms else ("0" if is_dnf else "1")

    def display_kmap(self, is_dnf=True):
        """Отображает карту Карно для заданных терминов."""
        terms = self.minterms if is_dnf else self.maxterms
        variable_count = len(self.variables)
        row_bits = variable_count // 2
        col_bits = variable_count - row_bits
        
        row_gray = self._generate_gray_codes(row_bits)
        col_gray = self._generate_gray_codes(col_bits)
        
        term_set = set(int(''.join(map(str, term)), 2) for term in terms)
        row_vars = "".join(self.variables[:row_bits])
        col_vars = "".join(self.variables[row_bits:])
        
        # Ширина столбцов
        col_width = col_bits + 2 
        header_width = len(f"{row_vars} \\ {col_vars}")
        
        print(f"\nКарта Карно:")

        header_line1 = f"{row_vars} \\ {col_vars}"
        print(f"{header_line1:{header_width}}", end=" | ")
        for code in col_gray:
            print(f" {code:0{col_bits}b} ", end="|")
        print()

        print("-" * ((col_bits + 3) * (len(col_gray) + 1) + len(header_line1) + 1))
        
        # Тело таблицы
        for row_code in row_gray:
            row_str = f"{row_code:0{row_bits}b}"
            # Выравнивание строки с переменными
            print(f"{row_str:{header_width}}", end=" | ")
            for col_code in col_gray:
                full_code = row_str + f"{col_code:0{col_bits}b}"
                index = int(full_code, 2)
                value = 1 if is_dnf else 0
                cell_value = str(value) if index in term_set else str(1 - value)
                # Выравнивание значения по центру столбца
                print(f" {cell_value:^{col_bits}} ", end="|")
            print()        
