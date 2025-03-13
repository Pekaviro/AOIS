import unittest
from logical_expression import TruthTableGenerator, VariableManager, LogicalExpression, ReversePolishNotationConverter


class TestReversePolishNotationConverter(unittest.TestCase):
    def test_simple_expression(self):
        converter = ReversePolishNotationConverter("a & b")
        self.assertEqual(converter.to_reverse_polish_notation(), ['a', 'b', '&'])

    def test_complex_expression(self):
        converter = ReversePolishNotationConverter("(a | b) & !c")
        self.assertEqual(converter.to_reverse_polish_notation(), ['a', 'b', '|', 'c', '!', '&'])

    def test_implication(self):
        converter = ReversePolishNotationConverter("a -> b")
        self.assertEqual(converter.to_reverse_polish_notation(), ['a', 'b', '->'])

    def test_priority(self):
        converter = ReversePolishNotationConverter("a & b | c")
        self.assertEqual(converter.to_reverse_polish_notation(), ['a', 'b', '&', 'c', '|'])


class TestVariableManager(unittest.TestCase):
    def test_extract_variables(self):
        manager = VariableManager("a & b | c")
        manager.extract_variables()
        self.assertEqual(set(manager.variable_map.keys()), {'a', 'b', 'c'})

    def test_initialize_variable_map(self):
        manager = VariableManager("a & b")
        manager.initialize_variable_map()
        self.assertEqual(manager.variable_map, {
            'a': [False, False, True, True],  # 2 переменные, 4 комбинации
            'b': [False, True, False, True]
        })

    def test_count_variables(self):
        manager = VariableManager("a & b | c")
        self.assertEqual(manager.count_variables(), 3)


class TestTruthTableGenerator(unittest.TestCase):
    def setUp(self):
        # Инициализация variable_map
        self.variable_map = {
            'a': [False, False, True, True],  # 2 переменные: a и b
            'b': [False, True, False, True]
        }
        # Обратная польская запись для выражения "a & b"
        self.rpn = ['a', 'b', '&']
        self.generator = TruthTableGenerator(self.variable_map, self.rpn)

    def test_evaluate_expression(self):
        final_result, intermediates = self.generator.evaluate_expression()
        self.assertEqual(final_result, [False, False, False, True])
        self.assertEqual(intermediates, {
            'step_1 (&)': [False, False, False, True]
        })


class TestLogicalExpression(unittest.TestCase):
    def test_generate_truth_table(self):
        expression = LogicalExpression("a & b")
        truth_table = expression.generate_truth_table()
        self.assertEqual(truth_table['a'], [False, False, True, True])
        self.assertEqual(truth_table['b'], [False, True, False, True])
        self.assertEqual(truth_table['a & b'], [False, False, False, True])

    def test_generate_pdnf(self):
        expression = LogicalExpression("a & b")
        pdnf = expression.generate_pdnf()
        self.assertEqual(pdnf.get_expression(), "(a & b)")

    def test_generate_pcnf(self):
        expression = LogicalExpression("a | b")
        pcnf = expression.generate_pcnf()
        self.assertEqual(pcnf.get_expression(), "(a | b)")

    def test_to_numeric_form_pdnf(self):
        expression = LogicalExpression("a & b")
        numeric_form = expression.to_numeric_form_pdnf()
        self.assertEqual(numeric_form, "( 3 ) |")

    def test_to_numeric_form_pcnf(self):
        expression = LogicalExpression("a & b")
        numeric_form = expression.to_numeric_form_pcnf()
        self.assertEqual(numeric_form, "( 0 , 1 , 2 ) &")  # Ожидается три комбинации

    def test_to_index_form(self):
        expression = LogicalExpression("a & b")
        index_form = expression.to_index_form()
        self.assertEqual(index_form, 1) 


if __name__ == '__main__':
    unittest.main()