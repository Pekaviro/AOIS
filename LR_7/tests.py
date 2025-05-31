import unittest
from unittest.mock import patch
from matrix import Matrix
from word import Word

class TestWord(unittest.TestCase):
    def setUp(self):
        self.word = Word('1101001011110010')

    def test_init_valid(self):
        word = Word('0' * 16)
        self.assertEqual(word.bits, '0' * 16)

    def test_init_invalid(self):
        with self.assertRaises(ValueError):
            Word('01')

    def test_get_v(self):
        self.assertEqual(self.word.get_v(), '110')

    def test_get_a(self):
        self.assertEqual(self.word.get_a(), '1001')

    def test_get_b(self):
        self.assertEqual(self.word.get_b(), '0111')

    def test_get_s(self):
        self.assertEqual(self.word.get_s(), '10010')

    def test_set_s_valid(self):
        self.word.set_s('11111')
        self.assertEqual(self.word.get_s(), '11111')
        self.assertEqual(self.word.bits, '1101001011111111')

    def test_set_s_invalid(self):
        with self.assertRaises(ValueError):
            self.word.set_s('111')

    def test_get_value_v(self):
        self.assertEqual(self.word.get_value('v'), 6)

    def test_get_value_a(self):
        self.assertEqual(self.word.get_value('a'), 9)

    def test_get_value_b(self):
        self.assertEqual(self.word.get_value('b'), 7)

    def test_get_value_s(self):
        self.assertEqual(self.word.get_value('s'), 18)

    def test_get_value_invalid(self):
        with self.assertRaises(ValueError):
            self.word.get_value('x')

    def test_repr(self):
        expected = "V: 110 (6) | A: 1001 (9) | B: 0111 (7) | S: 10010 (18)"
        self.assertEqual(repr(self.word), expected)


class TestMatrix(unittest.TestCase):
    def setUp(self):
        self.matrix = Matrix()

    def test_init(self):
        self.assertEqual(len(self.matrix.words), 16)
        for word in self.matrix.words:
            self.assertEqual(len(word.bits), 16)
        self.assertEqual(len(self.matrix.matrix), 16)
        for row in self.matrix.matrix:
            self.assertEqual(len(row), 16)

    def test_update_diagonal_matrix(self):
        self.matrix.words = [Word('0'*16) for _ in range(16)]
        self.matrix.words[0].bits = '1' + '0'*15
        self.matrix.update_diagonal_matrix()
        
        for i in range(16):
            self.assertEqual(self.matrix.matrix[i][0], '1' if i == 0 else '0')

    def test_apply_logical_function_f7_or(self):
        self.matrix.words[0].bits = '0101010101010101'
        self.matrix.words[1].bits = '0011001100110011'
        
        self.matrix.apply_logical_function('f7', 0, 1, 2)
        
        expected = '0111011101110111'
        self.assertEqual(self.matrix.words[2].bits, expected)

    def test_apply_logical_function_f8_nor(self):
        self.matrix.words[0].bits = '0101010101010101'
        self.matrix.words[1].bits = '0011001100110011'
        
        self.matrix.apply_logical_function('f8', 0, 1, 2)

        expected = '1000100010001000'
        self.assertEqual(self.matrix.words[2].bits, expected)

    def test_apply_logical_function_f2_inhibit(self):
        self.matrix.words[0].bits = '0101010101010101'
        self.matrix.words[1].bits = '0011001100110011'
        
        self.matrix.apply_logical_function('f2', 0, 1, 2)
        
        expected = '0100010001000100'
        self.assertEqual(self.matrix.words[2].bits, expected)

    def test_apply_logical_function_f13_implication(self):
        self.matrix.words[0].bits = '0101010101010101'
        self.matrix.words[1].bits = '0011001100110011'
        
        self.matrix.apply_logical_function('f13', 0, 1, 2)
        
        expected = '1011101110111011'
        self.assertEqual(self.matrix.words[2].bits, expected)

    def test_search_interval_string_bounds(self):
        self.matrix.words[0].bits = '0000000000000000'  # 0
        self.matrix.words[1].bits = '0000000000001111'  # 15
        self.matrix.words[2].bits = '0000000011111111'  # 255
        self.matrix.words[3].bits = '1111111111111111'  # 65535
        
        results = self.matrix.search_interval('0000000000000001', '0000000011111110')
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], 1)

    def test_search_interval_int_bounds(self):
        self.matrix.words[0].bits = '0000000000000000'  # 0
        self.matrix.words[1].bits = '0000000000001111'  # 15
        self.matrix.words[2].bits = '0000000011111111'  # 255
        self.matrix.words[3].bits = '1111111111111111'  # 65535
        
        results = self.matrix.search_interval(1, 254)
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], 1)

    def test_search_interval_invalid_bounds(self):
        with self.assertRaises(ValueError):
            self.matrix.search_interval('01', '10')

    def test_arithmetic_operation_int_key(self):
        # V=5 (101)
        self.matrix.words[0].bits = '1010101010101010'
        result = self.matrix.arithmetic_operation(5)
        
        # A=5, B=5, S=10
        self.assertEqual(self.matrix.words[0].bits[11:16], '01010')

    def test_arithmetic_operation_string_key(self):
        # V=3 (011)
        self.matrix.words[0].bits = '0110101010101010'
        result = self.matrix.arithmetic_operation('11')
        
        # A=5, B=5, S=10
        self.assertEqual(self.matrix.words[0].bits[11:16], '01010')

    def test_arithmetic_operation_no_match(self):
        original_bits = self.matrix.words[0].bits
        result = self.matrix.arithmetic_operation(0)
        self.assertEqual(self.matrix.words[0].bits, original_bits)

    @patch('builtins.print')
    def test_print_matrix(self, mock_print):
        self.matrix.print_matrix()
        self.assertTrue(mock_print.called)

if __name__ == '__main__':
    unittest.main()