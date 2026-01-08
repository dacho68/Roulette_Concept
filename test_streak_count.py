"""
Unit tests for get_number_of_streak_color method in FrenchRouletteEmulator
"""

import unittest
from french_roulette_strategy import FrenchRouletteEmulator


class TestGetNumberOfStreakColor(unittest.TestCase):
    """Test cases for the get_number_of_streak_color method"""
    
    def setUp(self):
        """Set up a new roulette emulator for each test"""
        self.roulette = FrenchRouletteEmulator(seed=42)
    
    def test_empty_history(self):
        """Test with no spins in history"""
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 0)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 0)
    
    def test_single_red_spin(self):
        """Test with a single red number in history"""
        self.roulette.history = [1]  # 1 is red
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 1)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 0)
    
    def test_single_black_spin(self):
        """Test with a single black number in history"""
        self.roulette.history = [2]  # 2 is black
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 0)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 1)
    
    def test_single_zero_spin(self):
        """Test with zero in history (should return 0 for both colors)"""
        self.roulette.history = [0]
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 0)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 0)
    
    def test_consecutive_red_streak(self):
        """Test with multiple consecutive red numbers"""
        self.roulette.history = [1, 3, 5, 7, 9]  # All red numbers
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 5)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 0)
    
    def test_consecutive_black_streak(self):
        """Test with multiple consecutive black numbers"""
        self.roulette.history = [2, 4, 6, 8, 10]  # All black numbers
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 0)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 5)
    
    def test_streak_broken_by_opposite_color(self):
        """Test streak counting stops at opposite color"""
        self.roulette.history = [2, 4, 6, 1, 3, 5]  # Black, black, black, red, red, red
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 3)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 0)
    
    def test_streak_broken_by_zero(self):
        """Test streak counting stops at zero"""
        self.roulette.history = [1, 3, 5, 0, 7, 9]  # Red, red, red, zero, red, red
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 2)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 0)
    
    def test_no_streak_at_end(self):
        """Test when last spin is not the requested color"""
        self.roulette.history = [1, 3, 5, 2]  # Red, red, red, black
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 0)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 1)
    
    def test_alternating_colors(self):
        """Test with alternating red and black"""
        self.roulette.history = [1, 2, 3, 4, 5, 6, 7]  # Red, black, red, black, red, black, red
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 1)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 0)
    
    def test_long_streak_after_mixed_history(self):
        """Test long streak at the end of mixed history"""
        self.roulette.history = [1, 2, 0, 4, 6, 8, 10, 11, 13, 15]  # Mixed, then 7 blacks at end
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 7)
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 0)
    
    def test_zero_ends_streak(self):
        """Test that zero at the end returns 0"""
        self.roulette.history = [1, 3, 5, 7, 9, 0]  # Five reds, then zero
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 0)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 0)
    
    def test_specific_red_numbers(self):
        """Test with specific red numbers from the RED_NUMBERS set"""
        # Red numbers: 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
        self.roulette.history = [36, 32, 30, 27]  # All red
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 4)
    
    def test_specific_black_numbers(self):
        """Test with specific black numbers from the BLACK_NUMBERS set"""
        # Black numbers: 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35
        self.roulette.history = [35, 33, 31, 29]  # All black
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 4)
    
    def test_streak_with_multiple_zeros(self):
        """Test streak calculation with zeros in history"""
        self.roulette.history = [0, 0, 1, 3, 5]  # Two zeros, then three reds
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 3)
        self.assertEqual(self.roulette.get_number_of_streak_color('black'), 0)
    
    def test_very_long_streak(self):
        """Test with a very long streak (edge case)"""
        # Create a streak of 20 red numbers
        red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36, 1, 3]
        self.roulette.history = red_numbers
        self.assertEqual(self.roulette.get_number_of_streak_color('red'), 20)


if __name__ == '__main__':
    unittest.main()
