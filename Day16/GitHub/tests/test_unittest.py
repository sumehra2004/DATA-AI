import unittest
from app.calculator import divide, sqrt, factorial

class TestSuperCalculator(unittest.TestCase):
    def test_divide(self):
        self.assertEqual(divide(9, 3), 3)

    def test_sqrt(self):
        self.assertEqual(sqrt(16), 4.0)

    def test_factorial(self):
        self.assertEqual(factorial(6), 720)

if __name__ == "__main__":
    unittest.main()
