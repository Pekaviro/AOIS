import unittest
from itertools import product
from collections import defaultdict

from logical_function import LogicalFunction


class TestLogicalFunction(unittest.TestCase):
    def setUp(self):
        self.vars = ['A', 'B']
        self.truth_table = defaultdict(dict)
        for a, b in product([0, 1], repeat=2):
            self.truth_table['A & B'][(a, b)] = a & b
            self.truth_table['A | B'][(a, b)] = a | b
            self.truth_table['A ^ B'][(a, b)] = a ^ b
            self.truth_table['!A'][(a, b)] = not a

    def test_init_without_truth_table(self):
        """Тест инициализации без таблицы истинности"""
        lf = LogicalFunction(['A', 'B'], 'A & B', {})
        self.assertEqual(lf.variables, ['A', 'B'])
        self.assertEqual(lf.expression, 'A & B')
        self.assertEqual(lf.minterms, [[1, 1]])

    def test_evaluate_expression(self):
        """Тест вычисления логического выражения"""
        lf = LogicalFunction(['A', 'B'], 'A & B', {})
        self.assertEqual(lf._evaluate_expression({'A': 1, 'B': 1}), 1)
        self.assertEqual(lf._evaluate_expression({'A': 1, 'B': 0}), 0)
        self.assertEqual(lf._evaluate_expression({'A': 0, 'B': 1}), 0)
        self.assertEqual(lf._evaluate_expression({'A': 0, 'B': 0}), 0)

    def test_minterm_to_binary(self):
        """Тест преобразования индекса минтерма в бинарное представление"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A', {})
        self.assertEqual(lf._minterm_to_binary(0), [0, 0, 0])
        self.assertEqual(lf._minterm_to_binary(5), [1, 0, 1])  # 5 = 101
        self.assertEqual(lf._minterm_to_binary(7), [1, 1, 1])

    def test_get_minterms(self):
        """Тест получения минтермов"""
        lf = LogicalFunction(['A', 'B'], 'A & B', {})
        self.assertEqual(lf.minterms, [[1, 1]])
        
        lf = LogicalFunction(['A', 'B'], 'A | B', {})
        self.assertEqual(sorted(lf.minterms), sorted([[0, 1], [1, 0], [1, 1]]))

    def test_get_maxterms(self):
        """Тест получения макстермов"""
        lf = LogicalFunction(['A', 'B'], 'A & B', {})
        self.assertEqual(sorted(lf.maxterms), sorted([[0, 0], [0, 1], [1, 0]]))
        
        lf = LogicalFunction(['A', 'B'], 'A | B', {})
        self.assertEqual(lf.maxterms, [[0, 0]])

    def test_implicant_to_expression(self):
        """Тест преобразования импликанта в выражение"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A', {})
        self.assertEqual(lf._implicant_to_expression([1, 0, 1]), "A & !B & C")
        self.assertEqual(lf._implicant_to_expression([1, None, 0]), "A & !C")
        self.assertEqual(lf._implicant_to_expression([None, None, None]), "1")

    def test_glue_terms(self):
        """Тест склеивания терминов"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A', {})
        self.assertEqual(lf._glue_terms((1, 0, 1), (1, 0, 0)), (1, 0, None))
        self.assertEqual(lf._glue_terms((1, 0, 1), (1, 1, 1)), (1, None, 1))
        self.assertIsNone(lf._glue_terms((1, 0, 1), (0, 1, 0)))

    def test_minimize_sdnf_calculus(self):
        """Тест минимизации СДНФ расчетным методом"""
        lf = LogicalFunction(['A', 'B'], 'A & B', {})
        self.assertEqual(lf.minimize_sdnf_calculus(), "A & B")
        
        lf = LogicalFunction(['A', 'B'], 'A | B', {})
        self.assertIn(lf.minimize_sdnf_calculus(), ["A | B", "B | A"])

    def test_minimize_sknf_calculus(self):
        """Тест минимизации СКНФ расчетным методом"""
        lf = LogicalFunction(['A', 'B'], 'A & B', {})
        expected = "(!A | B) & (A | !B) & (A | B)"
        result = lf.minimize_sknf_calculus()
        self.assertIn(result, ["(A) & (B)", "(B) & (A)"])

    def test_minimize_with_kmap_dnf(self):
        """Тест минимизации DNF с помощью карт Карно"""
        lf = LogicalFunction(['A', 'B'], 'A & B', {})
        result = lf.minimize_with_kmap(is_dnf=True)
        self.assertIn(result, ["(A & B)", "(B & A)"])

    def test_minimize_with_kmap_cnf(self):
        """Тест минимизации CNF с помощью карт Карно"""
        lf = LogicalFunction(['A', 'B'], 'A & B', {})
        result = lf.minimize_with_kmap(is_dnf=False)

        self.assertIn(result, ["(A) & (B)", "(B) & (A)"])

    def test_display_kmap(self):
        """Тест отображения карты Карно (проверяем, что не падает)"""
        lf = LogicalFunction(['A', 'B'], 'A & B', {})
        try:
            lf.display_kmap(is_dnf=True)
            lf.display_kmap(is_dnf=False)
        except Exception as e:
            self.fail(f"display_kmap() raised {type(e).__name__} unexpectedly!")



class TestLogicalFunctionExtended(unittest.TestCase):
    def setUp(self):
        self.vars_3 = ['A', 'B', 'C']
        self.truth_table = defaultdict(dict)
        for a, b, c in product([0, 1], repeat=3):
            self.truth_table['A & B & C'][(a, b, c)] = a & b & c
            self.truth_table['A | B | C'][(a, b, c)] = a | b | c

    def test_init_with_truth_table(self):
        """Тест инициализации с таблицей истинности"""
        lf = LogicalFunction(['A', 'B'], 'A & B', self.truth_table)
        self.assertEqual(lf.variables, ['A', 'B'])
        self.assertEqual(lf.expression, 'A & B')
        self.assertEqual(lf.minterms, [[1, 1]])

    def test_maxterm_to_expression(self):
        """Тест преобразования макстерма в выражение"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A', {})
        self.assertEqual(lf._maxterm_to_expression([1, 0, 1]), "(!A | B | !C)")
        self.assertEqual(lf._maxterm_to_expression([1, None, 0]), "(!A | C)")
        self.assertEqual(lf._maxterm_to_expression([None, None, None]), "1")

    def test_get_prime_implicants(self):
        """Тест получения простых импликантов"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A & B & C', {})
        minterms = [[1, 1, 1]]
        primes = lf._get_prime_implicants(minterms)
        self.assertEqual(primes, [[1, 1, 1]])

        lf = LogicalFunction(['A', 'B'], 'A | B', {})
        minterms = [[0, 1], [1, 0], [1, 1]]
        primes = lf._get_prime_implicants(minterms)
        self.assertEqual(len(primes), 2)  # Должно быть 2 импликанта

    def test_select_essential_primes(self):
        """Тест выбора существенных импликантов"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A & B & C', {})
        primes = [[1, 1, None], [None, 1, 1]]
        minterms = [[1, 1, 0], [1, 1, 1], [0, 1, 1]]
        essentials = lf._select_essential_primes(primes, minterms)
        self.assertEqual(len(essentials), 2)

    def test_covers(self):
        """Тест проверки покрытия термина импликантом"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A', {})
        self.assertTrue(lf._covers([1, None, None], [1, 0, 1]))
        self.assertFalse(lf._covers([1, None, None], [0, 0, 1]))
        self.assertTrue(lf._covers([None, None, None], [1, 0, 1]))

    def test_generate_gray_codes(self):
        """Тест генерации кодов Грея"""
        lf = LogicalFunction(['A', 'B'], 'A', {})
        gray_codes = lf._generate_gray_codes(2)
        self.assertEqual(gray_codes, [0, 1, 3, 2])

    def test_convert_to_binary_terms(self):
        """Тест преобразования терминов в бинарное представление"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A', {})
        terms = [5, 3]  # 101 и 011
        binary_terms = lf._convert_to_binary_terms(terms, 3)
        self.assertEqual(binary_terms, [(1, 0, 1), (0, 1, 1)])

    def test_try_merge_implicants(self):
        """Тест попытки объединения импликантов"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A', {})
        merged = lf._try_merge_implicants((1, 0, 1), (1, 0, 0))
        self.assertEqual(merged, (1, 0, '-'))
        self.assertIsNone(lf._try_merge_implicants((1, 0, 1), (0, 1, 0)))

    def test_find_prime_implicants_kmap(self):
        """Тест поиска простых импликантов для карт Карно"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A', {})
        minterms = [(1, 0, 1), (1, 0, 0)]
        primes = lf._find_prime_implicants_kmap(minterms, 3)
        self.assertEqual(primes, {(1, 0, '-')})

    def test_is_covering(self):
        """Тест проверки покрытия минтерма импликантом"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A', {})
        self.assertTrue(lf._is_covering((1, '-', '-'), (1, 0, 1)))
        self.assertFalse(lf._is_covering((1, '-', '-'), (0, 0, 1)))

    def test_select_essential_primes_kmap(self):
        """Тест выбора существенных импликантов для карт Карно"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A', {})
        primes = {(1, '-', '-'), ('-', 1, '-')}
        minterms = [(1, 0, 0), (0, 1, 0)]
        essentials = lf._select_essential_primes_kmap(primes, minterms)
        self.assertEqual(len(essentials), 2)


class TestLogicalFunctionEdgeCases(unittest.TestCase):

    def test_single_variable_function(self):
        """Тест функции с одной переменной"""
        lf = LogicalFunction(['A'], 'A', {})
        self.assertEqual(lf.minimize_sdnf_calculus(), "A")
        self.assertEqual(lf.minimize_sknf_calculus(), "(A)")

    def test_complex_kmap_minimization(self):
        """Тест сложной минимизации с картами Карно для 3 переменных"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A & (B | C)', {})
        dnf_result = lf.minimize_with_kmap(is_dnf=True)
        cnf_result = lf.minimize_with_kmap(is_dnf=False)
        self.assertTrue(len(dnf_result) > 0)
        self.assertTrue(len(cnf_result) > 0)

    def test_minimize_sdnf_table_complex(self):
        """Тест табличной минимизации СДНФ для сложной функции"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A & (B | C)', {})
        result = lf.minimize_sdnf_table()
        self.assertTrue(len(result) > 0)

    def test_minimize_sknf_table_complex(self):
        """Тест табличной минимизации СКНФ для сложной функции"""
        lf = LogicalFunction(['A', 'B', 'C'], 'A & (B | C)', {})
        result = lf.minimize_sknf_table()
        self.assertTrue(len(result) > 0)

    def test_all_true_function(self):
        """Тест функции, которая всегда истинна (все минтермы)"""
        lf = LogicalFunction(['A', 'B'], 'A | !A', {})
        self.assertEqual(lf.minimize_sdnf_calculus(), "1")
        self.assertEqual(lf.minimize_sknf_calculus(), "1")
        self.assertEqual(lf.minimize_with_kmap(is_dnf=True), "1")
        self.assertEqual(lf.minimize_with_kmap(is_dnf=False), "1")

    def test_expression_with_spaces(self):
        """Тест выражения с пробелами"""
        lf = LogicalFunction(['A', 'B'], ' A  &  B ', {})
        self.assertEqual(lf._evaluate_expression({'A': 1, 'B': 1}), 1)
        self.assertEqual(lf.minimize_sdnf_calculus(), "A & B")

    def test_multiple_variables(self):
        """Тест с большим количеством переменных (4)"""
        lf = LogicalFunction(['A', 'B', 'C', 'D'], 'A & B & (C | D)', {})
        try:
            lf.display_kmap(is_dnf=True)
            result = lf.minimize_sdnf_calculus()
            self.assertTrue(len(result) > 0)
        except Exception as e:
            self.fail(f"Failed with 4 variables: {type(e).__name__}")

    def test_maxterm_to_expression_empty(self):
        """Тест пустого макстерма"""
        lf = LogicalFunction(['A', 'B'], 'A & B', {})
        self.assertEqual(lf._maxterm_to_expression([None, None]), "1")

if __name__ == '__main__':
    unittest.main()