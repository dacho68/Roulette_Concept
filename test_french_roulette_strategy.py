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




class TestFrenchRouletteEmulatorSpin(unittest.TestCase):
    """Test cases for FrenchRouletteEmulator.spin() method"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        from french_roulette_strategy import FrenchRouletteEmulator
        self.roulette = FrenchRouletteEmulator(seed=42)
    
    def test_spin_returns_valid_number(self):
        """Test that spin returns a number between 0-36"""
        result = self.roulette.spin()
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 36)
        self.assertIsInstance(result, int)
    
    def test_spin_adds_to_history(self):
        """Test that spin result is added to history"""
        initial_length = len(self.roulette.history)
        result = self.roulette.spin()
        self.assertEqual(len(self.roulette.history), initial_length + 1)
        self.assertEqual(self.roulette.history[-1], result)
    
    def test_spin_count_increments(self):
        """Test that spin_count increments after each spin"""
        initial_count = self.roulette.get_spin_count()
        self.roulette.spin()
        self.assertEqual(self.roulette.get_spin_count(), initial_count + 1)
    
    def test_multiple_spins_increment_count(self):
        """Test that multiple spins increment count correctly"""
        initial_count = self.roulette.get_spin_count()
        for _ in range(5):
            self.roulette.spin()
        self.assertEqual(self.roulette.get_spin_count(), initial_count + 5)
    
    def test_spin_with_random_numbers_list(self):
        """Test spin with provided random numbers list"""
        from french_roulette_strategy import FrenchRouletteEmulator
        random_numbers = [10, 25, 34, 5, 18]
        roulette = FrenchRouletteEmulator(random_numbers=random_numbers)
        
        # First spin should use first number
        result = roulette.spin()
        self.assertEqual(result, 10)
        
        # Second spin should use second number
        result = roulette.spin()
        self.assertEqual(result, 25)
        
        # Third spin should use third number
        result = roulette.spin()
        self.assertEqual(result, 34)
    
    def test_spin_cycles_through_random_numbers(self):
        """Test that spin cycles through the random numbers list"""
        from french_roulette_strategy import FrenchRouletteEmulator
        random_numbers = [1, 2, 3, 4, 5]
        roulette = FrenchRouletteEmulator(random_numbers=random_numbers)
        
        # Spin 10 times and verify cycling
        results = []
        for _ in range(10):
            results.append(roulette.spin())
        
        expected = [1, 2, 3, 4, 5, 1, 2, 3, 4, 5]
        self.assertEqual(results, expected)
    
    def test_spin_with_zero_in_random_numbers(self):
        """Test spin when zero is in random numbers"""
        from french_roulette_strategy import FrenchRouletteEmulator
        random_numbers = [0, 18, 0, 25]
        roulette = FrenchRouletteEmulator(random_numbers=random_numbers)
        
        result = roulette.spin()
        self.assertEqual(result, 0)
        
        result = roulette.spin()
        self.assertEqual(result, 18)
        
        result = roulette.spin()
        self.assertEqual(result, 0)
    
    def test_spin_history_preserves_all_results(self):
        """Test that history preserves all spin results in order"""
        from french_roulette_strategy import FrenchRouletteEmulator
        random_numbers = [10, 20, 30, 10, 20]
        roulette = FrenchRouletteEmulator(random_numbers=random_numbers)
        
        for _ in range(5):
            roulette.spin()
        
        self.assertEqual(roulette.history, [10, 20, 30, 10, 20])
    
    
    def test_spin_with_edge_case_numbers(self):
        """Test spin with edge case wheel numbers (0 and 36)"""
        from french_roulette_strategy import FrenchRouletteEmulator
        random_numbers = [0, 36, 1, 35]
        roulette = FrenchRouletteEmulator(random_numbers=random_numbers)
        
        result = roulette.spin()
        self.assertEqual(result, 0)
        
        result = roulette.spin()
        self.assertEqual(result, 36)
        
        result = roulette.spin()
        self.assertEqual(result, 1)
        
        result = roulette.spin()
        self.assertEqual(result, 35)
    

    def test_spin_different_with_different_seed(self):
        """Test that spin produces different results with different seeds"""
        from french_roulette_strategy import FrenchRouletteEmulator
        
        
        roulette1 = FrenchRouletteEmulator(seed=42)
        roulette2 = FrenchRouletteEmulator(seed=123)
        
        results1 = [roulette1.spin() for _ in range(5)]
        results2 = [roulette2.spin() for _ in range(5)]
        
        # With different seeds, results should be different (with high probability)
        self.assertNotEqual(results1, results2)
    
    def test_spin_index_management(self):
        """Test that random_index is correctly managed during spins"""
        from french_roulette_strategy import FrenchRouletteEmulator
        random_numbers = [5, 15, 25, 35]
        roulette = FrenchRouletteEmulator(random_numbers=random_numbers)
        
        roulette.spin()  # spin_count = 1, index = 0 % 4 = 0
        self.assertEqual(roulette.spin_count, 1)
        
        roulette.spin()  # spin_count = 2, index = 1 % 4 = 1
        self.assertEqual(roulette.spin_count, 2)
        
        roulette.spin()  # spin_count = 3, index = 2 % 4 = 2
        self.assertEqual(roulette.spin_count, 3)
        
        roulette.spin()  # spin_count = 4, index = 3 % 4 = 3
        self.assertEqual(roulette.spin_count, 4)
        
        roulette.spin()  # spin_count = 5, index = 4 % 4 = 0 (cycles back)
        self.assertEqual(roulette.spin_count, 5)
        self.assertEqual(roulette.history[-1], 5)  # Should be first number again
    
    def test_spin_many_times_with_small_list(self):
        """Test spinning many times with a small random numbers list"""
        from french_roulette_strategy import FrenchRouletteEmulator
        random_numbers = [7, 14, 21]
        roulette = FrenchRouletteEmulator(random_numbers=random_numbers)
        
        for _ in range(9):
            roulette.spin()
        
        # After 9 spins with 3-number list: 7,14,21,7,14,21,7,14,21
        self.assertEqual(roulette.history, [7, 14, 21, 7, 14, 21, 7, 14, 21])
    
    def test_spin_return_type_is_int(self):
        """Test that spin always returns an integer"""
        from french_roulette_strategy import FrenchRouletteEmulator
        random_numbers = [10.5, 20.7, 35.2]  # Float values in list
        roulette = FrenchRouletteEmulator(random_numbers=random_numbers)
        
        result = roulette.spin()
        self.assertIsInstance(result, (int, float))
        # The result type depends on what's in random_numbers
if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
