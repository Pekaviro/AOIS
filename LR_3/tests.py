import unittest
from logical_function import LogicalFunction

class TestLogicalFunction(unittest.TestCase):
    def setUp(self):
        """Инициализация тестовых данных"""
        self.vars = ['a', 'b']
        self.expr = "a & b"
        self.lf = LogicalFunction(self.vars, self.expr)
    
    def test_initialization_basic(self):
        """Тест базовой инициализации"""
        lf = LogicalFunction(['a', 'b'], "a & b")
        self.assertEqual(lf.variables, ['a', 'b'])
        self.assertEqual(lf.expression, "a & b")
    
    def test_initialization_sorting(self):
        """Тест сортировки переменных"""
        lf = LogicalFunction(['b', 'a'], "a & b")
        self.assertEqual(lf.variables, ['a', 'b'])
    
    def test_initialization_complex(self):
        """Тест инициализации сложного выражения"""
        lf = LogicalFunction(['a', 'b', 'c'], "(a | b) & !c")
        self.assertEqual(lf.variables, ['a', 'b', 'c'])
        self.assertEqual(lf.expression, "(a | b) & !c")

    def test_truth_table(self):
        """Тест построения таблицы истинности"""
        # Тестируем функцию И (AND)
        lf_and = LogicalFunction(['a', 'b'], "a & b")
        truth_table_and = lf_and._build_truth_table()
        
        # Проверяем количество строк (2^2 = 4)
        self.assertEqual(len(truth_table_and), 4)
        
        # Проверяем конкретные значения
        expected_and = [
            ((0, 0), 0),
            ((0, 1), 0),
            ((1, 0), 0),
            ((1, 1), 1)
        ]
        self.assertEqual(truth_table_and, expected_and)
        
        # Тестируем функцию ИЛИ (OR)
        lf_or = LogicalFunction(['a', 'b'], "a | b")
        truth_table_or = lf_or._build_truth_table()
        
        expected_or = [
            ((0, 0), 0),
            ((0, 1), 1),
            ((1, 0), 1),
            ((1, 1), 1)
        ]
        self.assertEqual(truth_table_or, expected_or)
        
        # Тестируем с одной переменной
        lf_single = LogicalFunction(['a'], "a")
        truth_table_single = lf_single._build_truth_table()
        
        expected_single = [
            ((0,), 0),
            ((1,), 1)
        ]
        self.assertEqual(truth_table_single, expected_single)
    
    def test_evaluate_expression(self):
        """Тест вычисления логического выражения"""
        # Простое И
        lf_and = LogicalFunction(['a', 'b'], "a & b")
        self.assertEqual(lf_and._evaluate_expression({'a': 0, 'b': 0}), 0)
        self.assertEqual(lf_and._evaluate_expression({'a': 0, 'b': 1}), 0)
        self.assertEqual(lf_and._evaluate_expression({'a': 1, 'b': 0}), 0)
        self.assertEqual(lf_and._evaluate_expression({'a': 1, 'b': 1}), 1)

        # Простое ИЛИ
        lf_or = LogicalFunction(['a', 'b'], "a | b")
        self.assertEqual(lf_or._evaluate_expression({'a': 0, 'b': 0}), 0)
        self.assertEqual(lf_or._evaluate_expression({'a': 0, 'b': 1}), 1)
        self.assertEqual(lf_or._evaluate_expression({'a': 1, 'b': 0}), 1)
        self.assertEqual(lf_or._evaluate_expression({'a': 1, 'b': 1}), 1)

        # Отрицание
        lf_not = LogicalFunction(['a'], "!a")
        self.assertEqual(lf_not._evaluate_expression({'a': 0}), 1)
        self.assertEqual(lf_not._evaluate_expression({'a': 1}), 0)

        # Комбинированное выражение
        lf_combined = LogicalFunction(['a', 'b', 'c'], "(a | b) & !c")
        self.assertEqual(lf_combined._evaluate_expression({'a': 1, 'b': 0, 'c': 0}), 1)
        self.assertEqual(lf_combined._evaluate_expression({'a': 1, 'b': 1, 'c': 1}), 0)
    
    def test_get_minterms_maxterms(self):
        """Тест получения минтермов и макстермов"""
        # Создаем тестовый объект один раз в setUp
        self.lf = LogicalFunction(['a', 'b'], "a | b")
        
        # Проверяем минтермы и макстермы для OR
        self.assertEqual(self.lf.minterms, [(0, 1), (1, 0), (1, 1)])
        self.assertEqual(self.lf.maxterms, [(0, 0)])
        
        # Проверяем AND
        self.lf = LogicalFunction(['a', 'b'], "a & b")
        self.assertEqual(self.lf.minterms, [(1, 1)])
        self.assertEqual(self.lf.maxterms, [(0, 0), (0, 1), (1, 0)])
        
        # Проверяем константные функции
        self.lf = LogicalFunction(['a', 'b'], "1")
        self.assertEqual(self.lf.minterms, [(0,0), (0,1), (1,0), (1,1)])
        self.assertEqual(self.lf.maxterms, [])
        
        self.lf = LogicalFunction(['a', 'b'], "0")
        self.assertEqual(self.lf.minterms, [])
        self.assertEqual(self.lf.maxterms, [(0,0), (0,1), (1,0), (1,1)])
        
        # Проверяем отрицание
        self.lf = LogicalFunction(['a'], "!a")
        self.assertEqual(self.lf.minterms, [(0,)])
        self.assertEqual(self.lf.maxterms, [(1,)])
        
        # Проверяем сложное выражение с 3 переменными
        self.lf = LogicalFunction(['a', 'b', 'c'], "a & (b | c)")
        expected_minterms = [
            (1, 0, 1),
            (1, 1, 0), 
            (1, 1, 1)
        ]
        self.assertEqual(self.lf.minterms, expected_minterms)
    
    def test_implicant_to_expression(self):
        """Тест преобразования импликанта в выражение"""
        lf = LogicalFunction(['a', 'b', 'c'], "a & b & c")
        
        # Полный импликант
        self.assertEqual(lf._implicant_to_expression([1, 0, 1]), "a & !b & c")
        
        # Импликант с None (склеенный)
        self.assertEqual(lf._implicant_to_expression([1, None, 0]), "a & !c")
        
        # Все None
        self.assertEqual(lf._implicant_to_expression([None, None, None]), "1")
    
    def test_maxterm_to_expression(self):
        """Тест преобразования макстерма в выражение"""
        lf = LogicalFunction(['a', 'b', 'c'], "a")  # Простое валидное выражение
        
        # Проверяем преобразование макстермов
        self.assertEqual(lf._maxterm_to_expression([0, 1, 0]), "(a | !b | c)")
        self.assertEqual(lf._maxterm_to_expression([1, None, 0]), "(!a | c)")
        self.assertEqual(lf._maxterm_to_expression([None, None, None]), "1")
        self.assertEqual(lf._maxterm_to_expression([]), "1")  # Пустой макстерм
    
    def test_get_prime_implicants(self):
        """Тест нахождения простых импликантов"""
        lf = LogicalFunction(['a', 'b'], "a | b")
        minterms = [(0, 1), (1, 0), (1, 1)]
        primes = lf._get_prime_implicants(minterms)
        
        # Ожидаем два импликанта: (None, 1) и (1, None)
        self.assertEqual(len(primes), 2)
        self.assertIn([None, 1], primes)
        self.assertIn([1, None], primes)
    
    def test_covers(self):
        """Тест проверки покрытия импликантом терма"""
        # Создаем временный объект только для тестирования метода _covers
        # Нам не нужно вычислять выражение, поэтому используем простое валидное
        lf = LogicalFunction(['a', 'b', 'c'], "a")
        
        # Полное совпадение
        self.assertTrue(lf._covers([1, 0, 1], [1, 0, 1]))
        
        # Частичное совпадение (импликант имеет None)
        self.assertTrue(lf._covers([1, None, 0], [1, 1, 0]))
        self.assertTrue(lf._covers([1, None, 0], [1, 0, 0]))
        
        # Не совпадает
        self.assertFalse(lf._covers([1, None, 0], [0, 1, 0]))
        self.assertFalse(lf._covers([1, None, 0], [1, 1, 1]))
    
    def test_minimize_sdnf_calculus(self):
        """Тест минимизации СДНФ расчетным методом"""
        lf = LogicalFunction(['a', 'b'], "a | b")
        result = lf.minimize_sdnf_calculus()
        
        # Разбиваем результат и проверяем наличие всех термов
        terms = result.split(" | ")
        self.assertEqual(len(terms), 2)
        self.assertIn("a", terms)
        self.assertIn("b", terms)
        
        # Тест для более сложного выражения
        lf = LogicalFunction(['a', 'b', 'c'], "(a & !b & !c) | (a & !b & c) | (a & b & c)")
        result = lf.minimize_sdnf_calculus()
        
        terms = result.split(" | ")
        self.assertEqual(len(terms), 2)
        self.assertIn("a & !b", terms)
        self.assertIn("a & c", terms)
    
    def test_minimize_sknf_calculus(self):
        """Тест минимизации СКНФ расчетным методом"""
        lf = LogicalFunction(['a', 'b'], "a & b")
        result = lf.minimize_sknf_calculus()
        
        # Разбиваем результат и проверяем наличие всех термов
        terms = result.split(" & ")
        self.assertEqual(len(terms), 2)
        self.assertIn("(a)", terms)
        self.assertIn("(b)", terms)
        
        # Тест для более сложного выражения
        lf = LogicalFunction(['a', 'b', 'c'], "(a | b | c) & (a | b | !c) & (a | !b | c)")
        result = lf.minimize_sknf_calculus()
        
        terms = result.split(" & ")
        self.assertEqual(len(terms), 2)
        self.assertIn("(a | b)", terms)
        self.assertIn("(a | c)", terms)
    
    def test_minimize_sdnf_table(self):
        """Тест минимизации СДНФ табличным методом"""
        lf = LogicalFunction(['a', 'b'], "a | b")
        result = lf.minimize_sdnf_table()
        
        # Разбиваем результат на части и проверяем их наличие
        parts = result.split(" | ")
        self.assertEqual(len(parts), 2)
        self.assertIn("a", parts)
        self.assertIn("b", parts)

        lf = LogicalFunction(['a', 'b', 'c'], "(a & !b & !c) | (a & !b & c) | (a & b & c)")
        result = lf.minimize_sdnf_table()

        # Проверяем наличие обоих ожидаемых импликантов
        parts = result.split(" | ")
        self.assertEqual(len(parts), 2)
        self.assertIn("a & !b", parts)
        self.assertIn("a & c", parts)
    
    def test_minimize_sknf_table(self):
        """Тест минимизации СКНФ табличным методом"""
        lf = LogicalFunction(['a', 'b'], "a & b")
        result = lf.minimize_sknf_table()
        
        # Разбиваем результат на отдельные импликанты
        implicants = result.split(" & ")
        
        # Проверяем что оба импликанта присутствуют в любом порядке
        self.assertEqual(len(implicants), 2)
        self.assertIn("(a)", implicants)
        self.assertIn("(b)", implicants)

        lf = LogicalFunction(['a', 'b', 'c'], "(a | b | c) & (a | b | !c) & (a | !b | c)")
        result = lf.minimize_sknf_table()

        # Проверяем наличие обоих ожидаемых импликантов
        implicants = result.split(" & ")
        self.assertEqual(len(implicants), 2)
        self.assertIn("(a | b)", implicants)
        self.assertIn("(a | c)", implicants)
    
    def test_karnaugh_map(self):
        """Тест построения карты Карно"""
        lf = LogicalFunction(['a', 'b'], "a | b")
        kmap = lf._build_karnaugh_map()
        expected_kmap = {
            (0, 0): 0,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): 1
        }
        self.assertEqual(kmap, expected_kmap)
    
    def test_minimize_sdnf_kmap(self):
        """Тест минимизации СДНФ с помощью карт Карно"""
        lf = LogicalFunction(['a', 'b'], "a | b")
        result = lf.minimize_sdnf_kmap()
        
        # Разбиваем результат на части и проверяем их наличие
        parts = result.split(" | ")
        self.assertEqual(len(parts), 2)
        self.assertIn("a", parts)
        self.assertIn("b", parts)
        
        # Тест для более сложного выражения
        lf = LogicalFunction(['a', 'b', 'c'], "(a & !b & !c) | (a & !b & c) | (a & b & c)")
        result = lf.minimize_sdnf_kmap()
        
        parts = result.split(" | ")
        self.assertEqual(len(parts), 2)
        self.assertIn("a & !b", parts)
        self.assertIn("a & c", parts)
    
    def test_minimize_sknf_kmap(self):
        """Тест минимизации СКНФ с помощью карт Карно"""
        lf = LogicalFunction(['a', 'b'], "a & b")
        result = lf.minimize_sknf_kmap()
        self.assertEqual(result, "(a) & (b)")
        
        lf = LogicalFunction(['a', 'b', 'c'], "(a | b | c) & (a | b | !c) & (a | !b | c)")
        result = lf.minimize_sknf_kmap()
        self.assertEqual(result, "(a | b) & (a | c)")
    
    def test_invalid_expression(self):
        """Тест обработки неверного выражения"""
        with self.assertRaises(ValueError):
            LogicalFunction(['a', 'b'], "a & invalid")
        
        with self.assertRaises(ValueError):
            LogicalFunction(['a', 'b'], "a &")

    def setUp(self):
        self.vars = ['a', 'b', 'c']
        self.simple_expr = "a & b"
        self.complex_expr = "(a | b) & !c"
    
    def test_empty_expression(self):
        """Тест обработки пустого выражения"""
        with self.assertRaises(ValueError):
            LogicalFunction(self.vars, "")
    
    def test_single_variable(self):
        """Тест работы с одной переменной"""
        lf = LogicalFunction(['a'], "a")
        self.assertEqual(len(lf.truth_table), 2)
        self.assertEqual(lf.minimize_sdnf_calculus(), "a")
        self.assertEqual(lf.minimize_sknf_calculus(), "(a)")
    
    def test_expression_with_spaces(self):
        """Тест обработки выражений с пробелами"""
        lf = LogicalFunction(self.vars, " a  &  ( b | c ) ")
        self.assertEqual(len(lf.truth_table), 8)
    
    def test_karnaugh_map_3vars(self):
        """Тест построения карты Карно для 3 переменных"""
        lf = LogicalFunction(['a', 'b', 'c'], "a & b & c")
        kmap = lf._build_karnaugh_map()
        self.assertEqual(kmap[(1,1,1)], 1)
        self.assertEqual(kmap[(0,0,0)], 0)
    
    def test_karnaugh_map_4vars(self):
        """Тест построения карты Карно для 4 переменных"""
        lf = LogicalFunction(['a', 'b', 'c', 'd'], "a & b & c & d")
        kmap = lf._build_karnaugh_map()
        self.assertEqual(kmap[(1,1,1,1)], 1)
        self.assertEqual(kmap[(0,0,0,0)], 0)
    
    def test_prime_implicants_selection(self):
        """Тест выбора простых импликантов"""
        lf = LogicalFunction(['a', 'b'], "a | b")
        primes = lf._get_prime_implicants(lf.minterms)
        self.assertEqual(len(primes), 2)
    
    def test_essential_primes_selection(self):
        """Тест выбора существенных импликантов"""
        lf = LogicalFunction(['a', 'b', 'c'], "(a & !b & !c) | (a & !b & c) | (a & b & c)")
        primes = lf._get_prime_implicants(lf.minterms)
        essential = lf._select_essential_primes(primes, lf.minterms)
        self.assertEqual(len(essential), 2)
    
    def test_implicant_coverage(self):
        """Тест проверки покрытия импликантом"""
        lf = LogicalFunction(['a', 'b'], "a | b")
        self.assertTrue(lf._covers([1, None], [1, 1]))
        self.assertTrue(lf._covers([None, 1], [0, 1]))
        self.assertFalse(lf._covers([1, None], [0, 1]))
    
    def test_minimize_sknf_kmap_unsupported_vars(self):
        """Тест минимизации СКНФ картами Карно для неподдерживаемого числа переменных"""
        # Для 5 переменных (неподдерживаемый случай)
        lf = LogicalFunction(['a', 'b', 'c', 'd', 'e'], "a | b | c | d | e")
        result = lf.minimize_sknf_kmap()
        
        # Должен либо вернуть константу, либо использовать расчетный метод
        self.assertTrue(result in ["1", "0"] or 
                    "|" in result or "&" in result)  # Проверяем, что это валидное выражение
        
        # Для 6 переменных (крайний случай)
        lf = LogicalFunction(['a', 'b', 'c', 'd', 'e', 'f'], "a & b & c & d & e & f")
        result = lf.minimize_sknf_kmap()
        self.assertTrue(result in ["1", "0"] or 
                    "|" in result or "&" in result)

    def test_minimize_sdnf_kmap_unsupported_vars(self):
        """Тест минимизации СДНФ картами Карно для неподдерживаемого числа переменных"""
        # Для 5 переменных (неподдерживаемый случай)
        lf = LogicalFunction(['a', 'b', 'c', 'd', 'e'], "a & b & c & d & e")
        result = lf.minimize_sdnf_kmap()
        
        # Должен либо вернуть константу, либо использовать расчетный метод
        self.assertTrue(result in ["1", "0"] or 
                    "|" in result or "&" in result)  # Проверяем, что это валидное выражение
        
        # Для 6 переменных (крайний случай)
        lf = LogicalFunction(['a', 'b', 'c', 'd', 'e', 'f'], "a | b | c | d | e | f")
        result = lf.minimize_sdnf_kmap()
        self.assertTrue(result in ["1", "0"] or 
                    "|" in result or "&" in result)
    
    def test_group_to_implicant(self):
        """Тест преобразования группы клеток в импликант"""
        lf = LogicalFunction(['a', 'b', 'c'], "a | b | c")
        group = [(0,0,0), (0,0,1)]
        implicant = lf._group_to_implicant(group)
        self.assertEqual(implicant, (0, 0, None))
    
    def test_is_valid_group(self):
        """Тест проверки валидности группы клеток"""
        lf = LogicalFunction(['a', 'b'], "a | b")
        valid_group = [(0,0), (0,1)]
        invalid_group = [(0,0), (1,1)]
        self.assertTrue(lf._is_valid_group(valid_group))
        self.assertFalse(lf._is_valid_group(invalid_group))
    
    def test_gray_code_generation(self):
        """Тест генерации кода Грея"""
        lf = LogicalFunction(['a'], "a")
        gray = lf._gray_code(3)
        self.assertEqual(len(gray), 8)
        self.assertEqual(gray[0], [0, 0, 0])
        self.assertEqual(gray[1], [0, 0, 1])
        self.assertEqual(gray[-1], [1, 0, 0])

    def test_always_true(self):
        lf = LogicalFunction(['a'], 'a | !a')
        self.assertEqual(lf.minimize_sdnf_calculus(), "1")
        self.assertEqual(lf.minimize_sknf_calculus(), "1") 

    def test_5_variable_kmap(self):
        # Test 5-variable function
        lf = LogicalFunction(['a','b','c','d','e'], 'a & b & c & d & e')
        result = lf.minimize_sdnf_kmap()
        self.assertEqual(result, "a & b & c & d & e")

    def test_kmap_group_validation(self):
        # Test invalid group detection
        lf = LogicalFunction(['a','b'], 'a | b')
        self.assertFalse(lf._is_valid_group([(0,0), (0,1), (1,0)]))  # Not a valid group    


if __name__ == "__main__":
    unittest.main()