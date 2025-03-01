from binary_calculator import BinaryCalculator
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



class TestBinaryCalculator(unittest.TestCase):

    def test_sign_extend(self):
        self.assertEqual(BinaryCalculator.sign_extend('1', 4), '1111')
        self.assertEqual(BinaryCalculator.sign_extend('0', 4), '0000')
        self.assertEqual(BinaryCalculator.sign_extend('101', 6), '111101')
        self.assertEqual(BinaryCalculator.sign_extend('001', 6), '000001')

    def test_add_binaries(self):
        self.assertEqual(BinaryCalculator.add_binaries('101', '11'), '1000')
        self.assertEqual(BinaryCalculator.add_binaries('110', '110'), '1100')
        self.assertEqual(BinaryCalculator.add_binaries('1010', '1010'), '10100')

    def test_sum_additional_code(self):
        self.assertEqual(BinaryCalculator.sum_additional_code('101', '11'), '1000')
        self.assertEqual(BinaryCalculator.sum_additional_code('110', '110'), '1100')
        self.assertEqual(BinaryCalculator.sum_additional_code('1010', '1010'), '10100')

    def test_subtract_additional_code(self):
        self.assertEqual(BinaryCalculator.subtract_additional_code('1010', '10'), '1000')
        self.assertEqual(BinaryCalculator.subtract_additional_code('1100', '110'), '110')
        self.assertEqual(BinaryCalculator.subtract_additional_code('1001', '1'), '1000')

    def test_multiply_direct_code(self):
        self.assertEqual(BinaryCalculator.multiply_direct_code('010', '011'), '00110')
        self.assertEqual(BinaryCalculator.multiply_direct_code('110', '010'), '11000')
        self.assertEqual(BinaryCalculator.multiply_direct_code('001', '100'), '0100')

    def test_division_direct_code(self):
        self.assertEqual(BinaryCalculator.division_direct_code('010', '001'), '010.00000')
        self.assertEqual(BinaryCalculator.division_direct_code('0110', '0010'), '0011.00000')
        self.assertEqual(BinaryCalculator.division_direct_code('0100', '0100'), '01.00000')

    def test_binary_compare(self):
        self.assertEqual(BinaryCalculator.binary_compare('101', '100'), 1)
        self.assertEqual(BinaryCalculator.binary_compare('101', '101'), 0)
        self.assertEqual(BinaryCalculator.binary_compare('100', '101'), -1)

    def test_subtract_direct_code(self):
        self.assertEqual(BinaryCalculator.subtract_direct_code('1010', '10'), '1000')
        self.assertEqual(BinaryCalculator.subtract_direct_code('1100', '110'), '110')
        self.assertEqual(BinaryCalculator.subtract_direct_code('1001', '1'), '1000')

    def test_sum_ieee754(self):
        self.assertEqual(BinaryCalculator.sum_ieee754('01000000101100000000000000000000', '01000000101100000000000000000000'), '01000001001100000000000000000000')
        self.assertEqual(BinaryCalculator.sum_ieee754('00111111100000000000000000000000', '00111111100000000000000000000000'), '01000000000000000000000000000000')
        self.assertEqual(BinaryCalculator.sum_ieee754('01000000000000000000000000000000', '01000000000000000000000000000000'), '01000000100000000000000000000000')


if __name__ == '__main__':
    unittest.main()
