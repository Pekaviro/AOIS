from binary_converter import BinaryConverter
from decimal_converter import DecimalConverter

import unittest

class TestBinaryConverter(unittest.TestCase):

    def test_to_binary(self):
        self.assertEqual(BinaryConverter.to_binary(0), '0')
        self.assertEqual(BinaryConverter.to_binary(5), '101')
        self.assertEqual(BinaryConverter.to_binary(10), '1010')

    def test_frac_to_binary(self):
        self.assertEqual(BinaryConverter.frac_to_binary(0.5), '1')
        self.assertEqual(BinaryConverter.frac_to_binary(0.25), '01')
        self.assertEqual(BinaryConverter.frac_to_binary(0.75), '11')

    def test_direct_code(self):
        bc = BinaryConverter(5)
        self.assertEqual(bc.direct_code(), '0101')
        
        bc = BinaryConverter(-5)
        self.assertEqual(bc.direct_code(), '1101')
        
        bc = BinaryConverter(2.75)
        self.assertEqual(bc.direct_code(), '010.11')

    def test_reverse_code(self):
        bc = BinaryConverter(5)
        self.assertEqual(bc.reverse_code(), '0101')
        
        bc = BinaryConverter(-5)
        self.assertEqual(bc.reverse_code(), '1010')
        
        bc = BinaryConverter(2.75)
        self.assertEqual(bc.reverse_code(), '010.11')

    def test_additional_code(self):
        bc = BinaryConverter(5)
        self.assertEqual(bc.additional_code(), '0101')
        
        bc = BinaryConverter(-5)
        self.assertEqual(bc.additional_code(), '1011')
        
        bc = BinaryConverter(2.75)
        self.assertEqual(bc.additional_code(), '010.11')

    def test_ieee754(self):
        bc = BinaryConverter(5.5)
        self.assertEqual(bc.ieee754(), '01000000101100000000000000000000')


class TestDecimalConverter(unittest.TestCase):

    def test_reverse_code_to_decimal(self):
        self.assertEqual(DecimalConverter.reverse_code_to_decimal('0001'), 1)
        self.assertEqual(DecimalConverter.reverse_code_to_decimal('1110'), -1)
        self.assertEqual(DecimalConverter.reverse_code_to_decimal('0101'), 5)
        self.assertEqual(DecimalConverter.reverse_code_to_decimal('1010'), -5)

    def test_additional_code_to_decimal(self):
        self.assertEqual(DecimalConverter.additional_code_to_decimal('0001'), 1)
        self.assertEqual(DecimalConverter.additional_code_to_decimal('1111'), -1)
        self.assertEqual(DecimalConverter.additional_code_to_decimal('0101'), 5)
        self.assertEqual(DecimalConverter.additional_code_to_decimal('1011'), -5)

    def test_direct_code_to_decimal_int(self):
        self.assertEqual(DecimalConverter.direct_code_to_decimal_int('0001'), 1)
        self.assertEqual(DecimalConverter.direct_code_to_decimal_int('1001'), -1)
        self.assertEqual(DecimalConverter.direct_code_to_decimal_int('0101'), 5)
        self.assertEqual(DecimalConverter.direct_code_to_decimal_int('1101'), -5)

    def test_direct_code_to_decimal_float(self):
        self.assertEqual(DecimalConverter.direct_code_to_decimal_float('0001.1'), 1.5)
        self.assertEqual(DecimalConverter.direct_code_to_decimal_float('1001.1'), -1.5)
        self.assertEqual(DecimalConverter.direct_code_to_decimal_float('0101.101'), 5.625)
        self.assertEqual(DecimalConverter.direct_code_to_decimal_float('1101.101'), -5.625)

    def test_ieee754_to_decimal(self):
        self.assertEqual(DecimalConverter.ieee754_to_decimal('01000000101100000000000000000000'), 5.5)
        self.assertEqual(DecimalConverter.ieee754_to_decimal('11000000101100000000000000000000'), -5.5)
        self.assertEqual(DecimalConverter.ieee754_to_decimal('00111111100000000000000000000000'), 1.0)
        self.assertEqual(DecimalConverter.ieee754_to_decimal('10111111100000000000000000000000'), -1.0)



if __name__ == '__main__':
    unittest.main()
