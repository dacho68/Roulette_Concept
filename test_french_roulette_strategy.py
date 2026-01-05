"""
Unit tests for French Roulette Strategy functions
"""

import unittest
from french_roulette_strategy import (
    get_next_bet_adjustment,
    get_bet_increase,
    get_bet_decrease,
    ADJUSTMENT_TABLE
)


class TestGetNextBetAdjustment(unittest.TestCase):
    """Test cases for get_next_bet_adjustment function"""
    
    def test_first_range_min_boundary(self):
        """Test minimum boundary of first range (0.20-0.90)"""
        result = get_next_bet_adjustment(0.20)
        self.assertEqual(result, 0.10)
    
    def test_first_range_max_boundary(self):
        """Test maximum boundary of first range (0.20-0.90)"""
        result = get_next_bet_adjustment(0.90)
        self.assertEqual(result, 0.10)
    
    def test_first_range_middle(self):
        """Test middle value of first range (0.20-0.90)"""
        result = get_next_bet_adjustment(0.50)
        self.assertEqual(result, 0.10)
    
    def test_second_range_min_boundary(self):
        """Test minimum boundary of second range (1.00-1.80)"""
        result = get_next_bet_adjustment(1.00)
        self.assertEqual(result, 0.20)
    
    def test_second_range_max_boundary(self):
        """Test maximum boundary of second range (1.00-1.80)"""
        result = get_next_bet_adjustment(1.80)
        self.assertEqual(result, 0.20)
    
    def test_second_range_middle(self):
        """Test middle value of second range (1.00-1.80)"""
        result = get_next_bet_adjustment(1.40)
        self.assertEqual(result, 0.20)
    
    def test_third_range_min_boundary(self):
        """Test minimum boundary of third range (2.00-3.60)"""
        result = get_next_bet_adjustment(2.00)
        self.assertEqual(result, 0.40)
    
    def test_third_range_max_boundary(self):
        """Test maximum boundary of third range (2.00-3.60)"""
        result = get_next_bet_adjustment(3.60)
        self.assertEqual(result, 0.40)
    
    def test_third_range_middle(self):
        """Test middle value of third range (2.00-3.60)"""
        result = get_next_bet_adjustment(2.80)
        self.assertEqual(result, 0.40)
    
    def test_fourth_range_min_boundary(self):
        """Test minimum boundary of fourth range (4.00-7.20)"""
        result = get_next_bet_adjustment(4.00)
        self.assertEqual(result, 0.80)
    
    def test_fourth_range_max_boundary(self):
        """Test maximum boundary of fourth range (4.00-7.20)"""
        result = get_next_bet_adjustment(7.20)
        self.assertEqual(result, 0.80)
    
    def test_fourth_range_middle(self):
        """Test middle value of fourth range (4.00-7.20)"""
        result = get_next_bet_adjustment(5.60)
        self.assertEqual(result, 0.80)
    
    def test_fifth_range_min_boundary(self):
        """Test minimum boundary of fifth range (8.00-12.80)"""
        result = get_next_bet_adjustment(8.00)
        self.assertEqual(result, 1.20)
    
    def test_fifth_range_max_boundary(self):
        """Test maximum boundary of fifth range (8.00-12.80)"""
        result = get_next_bet_adjustment(12.80)
        self.assertEqual(result, 1.20)
    
    def test_fifth_range_middle(self):
        """Test middle value of fifth range (8.00-12.80)"""
        result = get_next_bet_adjustment(10.40)
        self.assertEqual(result, 1.20)
    
    def test_sixth_range_min_boundary(self):
        """Test minimum boundary of sixth range (14.00-20.00)"""
        result = get_next_bet_adjustment(14.00)
        self.assertEqual(result, 2.00)
    
    def test_sixth_range_max_boundary(self):
        """Test maximum boundary of sixth range (14.00-20.00)"""
        result = get_next_bet_adjustment(20.00)
        self.assertEqual(result, 2.00)
    
    def test_sixth_range_middle(self):
        """Test middle value of sixth range (14.00-20.00)"""
        result = get_next_bet_adjustment(17.00)
        self.assertEqual(result, 2.00)
    
    def test_below_min_range(self):
        """Test bet below minimum range should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            get_next_bet_adjustment(0.10)
        self.assertIn("out of adjustment table range", str(context.exception))
    
    def test_above_max_range(self):
        """Test bet above maximum range should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            get_next_bet_adjustment(25.00)
        self.assertIn("out of adjustment table range", str(context.exception))
    
    def test_gap_between_first_and_second_range(self):
        """Test bet in gap between first and second range (0.95)"""
        with self.assertRaises(ValueError) as context:
            get_next_bet_adjustment(0.95)
        self.assertIn("out of adjustment table range", str(context.exception))
    
    def test_gap_between_second_and_third_range(self):
        """Test bet in gap between second and third range (1.90)"""
        with self.assertRaises(ValueError) as context:
            get_next_bet_adjustment(1.90)
        self.assertIn("out of adjustment table range", str(context.exception))
    
    def test_gap_between_fifth_and_sixth_range(self):
        """Test bet in gap between fifth and sixth range (13.00)"""
        with self.assertRaises(ValueError) as context:
            get_next_bet_adjustment(13.00)
        self.assertIn("out of adjustment table range", str(context.exception))


class TestGetBetIncrease(unittest.TestCase):
    """Test cases for get_bet_increase function"""
    
    def test_increase_from_first_range(self):
        """Test bet increase from first range"""
        result = get_bet_increase(0.50)
        self.assertEqual(result, 0.60)  # 0.50 + 0.10
    
    def test_increase_from_second_range(self):
        """Test bet increase from second range"""
        result = get_bet_increase(1.40)
        self.assertEqual(result, 1.60)  # 1.40 + 0.20
    
    def test_increase_from_third_range(self):
        """Test bet increase from third range"""
        result = get_bet_increase(2.80)
        self.assertEqual(result, 3.20)  # 2.80 + 0.40
    
    def test_increase_from_fourth_range(self):
        """Test bet increase from fourth range"""
        result = get_bet_increase(5.60)
        self.assertEqual(result, 6.40)  # 5.60 + 0.80
    
    def test_increase_from_fifth_range(self):
        """Test bet increase from fifth range"""
        result = get_bet_increase(10.40)
        self.assertEqual(result, 11.60)  # 10.40 + 1.20
    
    def test_increase_from_sixth_range(self):
        """Test bet increase from sixth range"""
        result = get_bet_increase(17.00)
        self.assertEqual(result, 19.00)  # 17.00 + 2.00
    
    def test_increase_rounding(self):
        """Test that increase result is properly rounded"""
        result = get_bet_increase(0.25)
        self.assertEqual(result, 0.35)  # Should be rounded to 2 decimals


class TestGetBetDecrease(unittest.TestCase):
    """Test cases for get_bet_decrease function"""
    
    def test_decrease_from_first_range(self):
        """Test bet decrease from first range (uses current range adjustment)"""
        result = get_bet_decrease(0.50)
        self.assertEqual(result, 0.40)  # 0.50 - 0.10
    
    def test_decrease_from_first_range_min(self):
        """Test bet decrease from first range minimum boundary (special case: uses own adjustment)"""
        result = get_bet_decrease(0.20)
        self.assertEqual(result, 0.10)  # 0.20 - 0.10
    
    def test_decrease_from_first_range_max(self):
        """Test bet decrease from first range maximum boundary"""
        result = get_bet_decrease(0.90)
        self.assertEqual(result, 0.80)  # 0.90 - 0.10
    
    def test_decrease_from_second_range(self):
        """Test bet decrease from second range (uses current range adjustment)"""
        result = get_bet_decrease(1.40)
        self.assertEqual(result, 1.20)  # 1.40 - 0.20 (current range adjustment)
    
    def test_decrease_from_second_range_min(self):
        """Test bet decrease from second range minimum boundary (uses prev range adjustment)"""
        result = get_bet_decrease(1.00)
        self.assertEqual(result, 0.90)  # 1.00 - 0.10 (prev adjustment)
    
    def test_decrease_from_second_range_max(self):
        """Test bet decrease from second range maximum boundary"""
        result = get_bet_decrease(1.80)
        self.assertEqual(result, 1.60)  # 1.80 - 0.20 (current range adjustment)
    
    def test_decrease_from_third_range(self):
        """Test bet decrease from third range (uses current range adjustment)"""
        result = get_bet_decrease(2.80)
        self.assertEqual(result, 2.40)  # 2.80 - 0.40 (current range adjustment)
    
    def test_decrease_from_third_range_min(self):
        """Test bet decrease from third range minimum boundary (uses prev range adjustment)"""
        result = get_bet_decrease(2.00)
        self.assertEqual(result, 1.80)  # 2.00 - 0.20 (prev adjustment)
    
    def test_decrease_from_third_range_max(self):
        """Test bet decrease from third range maximum boundary"""
        result = get_bet_decrease(3.60)
        self.assertEqual(result, 3.20)  # 3.60 - 0.40 (current range adjustment)
    
    def test_decrease_from_fourth_range(self):
        """Test bet decrease from fourth range (uses current range adjustment)"""
        result = get_bet_decrease(5.60)
        self.assertEqual(result, 4.80)  # 5.60 - 0.80 (current range adjustment)
    
    def test_decrease_from_fourth_range_min(self):
        """Test bet decrease from fourth range minimum boundary (uses prev range adjustment)"""
        result = get_bet_decrease(4.00)
        self.assertEqual(result, 3.60)  # 4.00 - 0.40 (prev adjustment)
    
    def test_decrease_from_fourth_range_max(self):
        """Test bet decrease from fourth range maximum boundary"""
        result = get_bet_decrease(7.20)
        self.assertEqual(result, 6.40)  # 7.20 - 0.80 (current range adjustment)
    
    def test_decrease_from_fifth_range(self):
        """Test bet decrease from fifth range (uses current range adjustment)"""
        result = get_bet_decrease(10.40)
        self.assertEqual(result, 9.20)  # 10.40 - 1.20 (current range adjustment)
    
    def test_decrease_from_fifth_range_min(self):
        """Test bet decrease from fifth range minimum boundary (uses prev range adjustment)"""
        result = get_bet_decrease(8.00)
        self.assertEqual(result, 7.20)  # 8.00 - 0.80 (prev adjustment)
    
    def test_decrease_from_fifth_range_max(self):
        """Test bet decrease from fifth range maximum boundary"""
        result = get_bet_decrease(12.80)
        self.assertEqual(result, 11.60)  # 12.80 - 1.20 (current range adjustment)
    
    def test_decrease_from_sixth_range(self):
        """Test bet decrease from sixth range (uses current range adjustment)"""
        result = get_bet_decrease(17.00)
        self.assertEqual(result, 15.00)  # 17.00 - 2.00 (current range adjustment)
    
    def test_decrease_from_sixth_range_min(self):
        """Test bet decrease from sixth range minimum boundary (uses prev range adjustment)"""
        result = get_bet_decrease(14.00)
        self.assertEqual(result, 12.80)  # 14.00 - 1.20 (prev adjustment)
    
    def test_decrease_from_sixth_range_max(self):
        """Test bet decrease from sixth range maximum boundary"""
        result = get_bet_decrease(20.00)
        self.assertEqual(result, 18.00)  # 20.00 - 2.00 (current range adjustment)
    
    def test_decrease_rounding(self):
        """Test that decrease result is properly rounded"""
        result = get_bet_decrease(0.35)
        self.assertEqual(result, 0.25)  # 0.35 - 0.10, properly rounded to 2 decimals
    
    def test_decrease_with_precision(self):
        """Test decrease with floating point precision"""
        result = get_bet_decrease(1.23)
        self.assertEqual(result, 1.03)  # 1.23 - 0.20 (current range adjustment)
    
    def test_decrease_below_min_range(self):
        """Test bet decrease with value below minimum range should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            get_bet_decrease(0.10)
        self.assertIn("out of adjustment table range", str(context.exception))
    
    def test_decrease_above_max_range(self):
        """Test bet decrease with value above maximum range should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            get_bet_decrease(25.00)
        self.assertIn("out of adjustment table range", str(context.exception))
    
    def test_decrease_in_gap_between_ranges(self):
        """Test bet decrease with value in gap between ranges should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            get_bet_decrease(0.95)  # Gap between first (0.20-0.90) and second (1.00-1.80)
        self.assertIn("out of adjustment table range", str(context.exception))
    
    def test_decrease_in_another_gap(self):
        """Test bet decrease with value in another gap between ranges"""
        with self.assertRaises(ValueError) as context:
            get_bet_decrease(13.00)  # Gap between fifth (8.00-12.80) and sixth (14.00-20.00)
        self.assertIn("out of adjustment table range", str(context.exception))
    
    def test_decrease_negative_value(self):
        """Test bet decrease with negative value should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            get_bet_decrease(-5.00)
        self.assertIn("out of adjustment table range", str(context.exception))
    
    def test_decrease_zero_value(self):
        """Test bet decrease with zero value should raise ValueError"""
        with self.assertRaises(ValueError) as context:
            get_bet_decrease(0.00)
        self.assertIn("out of adjustment table range", str(context.exception))


class TestAdjustmentTableConsistency(unittest.TestCase):
    """Test cases for ADJUSTMENT_TABLE consistency"""
    
    def test_table_has_six_ranges(self):
        """Test that adjustment table has 6 ranges"""
        self.assertEqual(len(ADJUSTMENT_TABLE), 6)
    
    def test_all_ranges_have_three_values(self):
        """Test that all ranges have min, max, and adjustment values"""
        for range_tuple in ADJUSTMENT_TABLE:
            self.assertEqual(len(range_tuple), 3)
    
    def test_adjustments_increase_with_bet_size(self):
        """Test that adjustments generally increase as bet ranges increase"""
        adjustments = [adj for _, _, adj in ADJUSTMENT_TABLE]
        # Check that adjustments are non-decreasing
        for i in range(len(adjustments) - 1):
            self.assertLessEqual(adjustments[i], adjustments[i + 1])
    
    def test_ranges_min_less_than_max(self):
        """Test that all ranges have min < max"""
        for min_bet, max_bet, _ in ADJUSTMENT_TABLE:
            self.assertLess(min_bet, max_bet)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
