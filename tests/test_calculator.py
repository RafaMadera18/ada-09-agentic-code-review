import unittest
from src.calculator import (
    calculate_subtotal,
    apply_discount,
    apply_fixed_discount,
    apply_tax,
    calculate_order_total,
)


class TestCalculator(unittest.TestCase):
    def test_calculate_subtotal_valid(self):
        self.assertEqual(calculate_subtotal([10.5, 20.0, 5.25]), 35.75)
        self.assertEqual(calculate_subtotal([]), 0.0)

    def test_calculate_subtotal_negative(self):
        with self.assertRaises(ValueError):
            calculate_subtotal([10.0, -5.0])

    def test_apply_discount_valid(self):
        self.assertEqual(apply_discount(100.0, 10.0), 90.0)
        self.assertEqual(apply_discount(100.0, 0.0), 100.0)
        self.assertEqual(apply_discount(100.0, 100.0), 0.0)

    def test_apply_discount_invalid(self):
        with self.assertRaises(ValueError):
            apply_discount(100.0, -5.0)
        with self.assertRaises(ValueError):
            apply_discount(100.0, 105.0)
        with self.assertRaises(ValueError):
            apply_discount(-50.0, 10.0)

    def test_apply_tax_valid(self):
        self.assertEqual(apply_tax(100.0, 0.16), 116.0)

    def test_apply_tax_negative_amount(self):
        with self.assertRaises(ValueError):
            apply_tax(-100.0, 0.16)

    def test_apply_tax_negative_rate(self):
        with self.assertRaises(ValueError):
            apply_tax(100.0, -0.16)

    def test_calculate_order_total_discount_then_tax(self):
        self.assertEqual(calculate_order_total([100.0, 50.0], 10.0, 0.16), 156.6)

    def test_calculate_order_total_defaults(self):
        self.assertEqual(calculate_order_total([10.5, 20.0, 5.25]), 35.75)
        self.assertEqual(calculate_order_total([100.0], discount_percent=10.0), 90.0)
        self.assertEqual(calculate_order_total([100.0], tax_rate=0.16), 116.0)

    def test_calculate_order_total_empty(self):
        self.assertEqual(calculate_order_total([]), 0.0)
        self.assertEqual(calculate_order_total([], 10.0, 0.16), 0.0)

    def test_calculate_order_total_full_discount(self):
        self.assertEqual(calculate_order_total([100.0], 100.0, 0.16), 0.0)

    def test_calculate_order_total_negative_price(self):
        with self.assertRaises(ValueError):
            calculate_order_total([10.0, -5.0])

    def test_calculate_order_total_invalid_discount(self):
        with self.assertRaises(ValueError):
            calculate_order_total([100.0], -1.0)
        with self.assertRaises(ValueError):
            calculate_order_total([100.0], 100.5)

    def test_calculate_order_total_negative_tax_rate(self):
        with self.assertRaises(ValueError):
            calculate_order_total([100.0], 0.0, -0.16)

    def test_apply_fixed_discount_valid(self):
        self.assertEqual(apply_fixed_discount(100.0, 15.0), 85.0)
        self.assertEqual(apply_fixed_discount(50.0, 0.0), 50.0)
        self.assertEqual(apply_fixed_discount(20.0, 20.0), 0.0)
        self.assertEqual(apply_fixed_discount(100.0, 15.556), 84.44)

    def test_apply_fixed_discount_negative(self):
        with self.assertRaises(ValueError):
            apply_fixed_discount(100.0, -10.0)
        with self.assertRaises(ValueError):
            apply_fixed_discount(-50.0, 10.0)
        with self.assertRaises(ValueError):
            apply_fixed_discount(-50.0, 0.0)

    def test_apply_fixed_discount_exceeds_amount(self):
        with self.assertRaises(ValueError):
            apply_fixed_discount(50.0, 60.0)

    def test_calculate_order_total_fixed_discount(self):
        # 100 subtotal -> 10% discount = 90 -> fixed discount 10 = 80 -> tax 16% = 92.8
        self.assertEqual(
            calculate_order_total([100.0], discount_percent=10.0, tax_rate=0.16, fixed_discount=10.0),
            92.8,
        )

    def test_calculate_order_total_fixed_discount_only(self):
        # 100 subtotal -> default 0% discount = 100 -> fixed discount 15 = 85 -> default tax 0% = 85.0
        self.assertEqual(calculate_order_total([100.0], fixed_discount=15.0), 85.0)

    def test_calculate_order_total_negative_fixed_discount(self):
        with self.assertRaises(ValueError):
            calculate_order_total([100.0], fixed_discount=-5.0)

    def test_calculate_order_total_fixed_discount_exceeds_balance(self):
        # Subtotal 100, 50% discount leaves 50; fixed discount 60 exceeds remaining balance
        with self.assertRaises(ValueError):
            calculate_order_total([100.0], discount_percent=50.0, fixed_discount=60.0)


if __name__ == "__main__":
    unittest.main()
