import unittest
from calc import add, subtract, multiply, devide

class Calc_test(unittest.TestCase):
    def test_add(self):
        result = add(6, 3)
        self.assertEqual(result, 9)

    def test_subtract(self):
        result = subtract(6, 3)
        self.assertEqual(result, 3)

    def test_multiply(self):
        result = multiply(6, 3)
        self.assertEqual(result, 18)

    def test_devide(self):
        result = devide(6, 3)
        self.assertEqual(result, 2)

'''Without "if __name__==__main__ " we run the module as below:'''
# python3 -m unittest test_calc.py

# Otherwise we specify the following to run the module
if __name__== '__main__':
    unittest.main()