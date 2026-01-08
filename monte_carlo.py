"""
Monte Carlo Simulation for French Roulette Streak Probabilities
Calculates the probability of getting multiple streaks of consecutive reds in 51 spins
"""

import random


def simulate_roulette_spins(num_spins):
    """
    Simulate French roulette spins.
    French roulette: 18 red, 18 black, 1 green (0)
    Returns list of results: 'R' for red, 'B' for black, 'G' for green
    """
    # Probability: 18/37 for red, 18/37 for black, 1/37 for green
    results = []
    for _ in range(num_spins):
        rand = random.randint(1, 37)
        if rand <= 18:
            results.append('R')
        elif rand <= 36:
            results.append('B')
        else:
            results.append('G')
    return results


def count_streaks(spins, streak_length):
    """
    Count the number of non-overlapping streaks of consecutive reds.
    Returns the count of complete streaks found.
    """
    count = 0
    current_streak = 0
    
    for spin in spins:
        if spin == 'R':
            current_streak += 1
            if current_streak == streak_length:
                count += 1
                current_streak = 0  # Reset to count non-overlapping streaks
        else:
            current_streak = 0
    
    return count


def run_simulation(num_simulations, num_spins, streak_length):
    """
    Run Monte Carlo simulation to calculate probabilities.
    
    Args:
        num_simulations: Number of times to simulate
        num_spins: Number of spins per simulation
        streak_length: Length of streak to look for
    
    Returns:
        Dictionary with probability results
    """
    at_least_one = 0
    at_least_two = 0
    at_least_three = 0
    exactly_one = 0
    exactly_two = 0
    exactly_three = 0

    four_or_more = 0
    
    for _ in range(num_simulations):
        spins = simulate_roulette_spins(num_spins)
        streak_count = count_streaks(spins, streak_length)
        
        if streak_count >= 1:
            at_least_one += 1
        if streak_count >= 2:
            at_least_two += 1
        if streak_count >= 3:
            at_least_three += 1

        if streak_count == 1:
            exactly_one += 1
        if streak_count == 2:
            exactly_two += 1
        if streak_count == 3:
            exactly_three += 1
        if streak_count >= 4:
            four_or_more += 1
    
    return {
        'at_least_one': (at_least_one / num_simulations) * 100,
        'at_least_two': (at_least_two / num_simulations) * 100,
        'at_least_three': (at_least_three / num_simulations) * 100,

        'exactly_one': (exactly_one / num_simulations) * 100,
        'exactly_two': (exactly_two / num_simulations) * 100,
        'exactly_three': (exactly_three / num_simulations) * 100,
        'four_or_more': (four_or_more / num_simulations) * 100,
        'zero_streaks': ((num_simulations - at_least_one) / num_simulations) * 100
    }


def test_non_overlapping():
    """Test to verify non-overlapping streak counting."""
    print("\n" + "=" * 70)
    print("TESTING NON-OVERLAPPING STREAK LOGIC:")
    print("=" * 70)
    
    test_cases = [
        (['R', 'R', 'R', 'R', 'R'], 5, 1, "Exactly 5 reds"),
        (['R', 'R', 'R', 'R', 'R', 'R'], 5, 1, "6 reds in a row (NOT 2 streaks)"),
        (['R', 'R', 'R', 'R', 'R', 'B', 'R', 'R', 'R', 'R', 'R'], 5, 2, "Two separate 5-red streaks"),
        (['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'], 5, 2, "10 reds = 2 non-overlapping streaks"),
        (['R', 'R', 'R', 'R'], 5, 0, "Only 4 reds (no complete streak)"),
        (['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'], 5, 3, "15 reds = 3 non-overlapping streaks"),
    ]
    
    all_passed = True
    for spins, streak_len, expected, description in test_cases:
        result = count_streaks(spins, streak_len)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        if result != expected:
            all_passed = False
        print(f"  {status}: {description}")
        print(f"         Input: {''.join(spins)} | Expected: {expected} | Got: {result}")
    
    print(f"\n{'All tests passed!' if all_passed else 'Some tests failed!'}")
    print("=" * 70)


def main():
    """Run the simulation and display results."""
    # First, run tests to verify non-overlapping logic
    test_non_overlapping()
    
    NUM_SIMULATIONS = 30000  # 100 thousand simulations for accuracy
    NUM_SPINS = 100
    STREAK_LENGTH = 7
    
    print("=" * 70)
    print("FRENCH ROULETTE STREAK PROBABILITY SIMULATION")
    print("=" * 70)
    print(f"\nSimulation Parameters:")
    print(f"  - Number of simulations: {NUM_SIMULATIONS:,}")
    print(f"  - Spins per simulation: {NUM_SPINS}")
    print(f"  - Streak length: {STREAK_LENGTH} consecutive reds")
    print(f"  - Probability of red: 18/37 = {18/37:.4f} ({18/37*100:.2f}%)")
    print(f"\nRunning simulation... (this may take a moment)")
    
    results = run_simulation(NUM_SIMULATIONS, NUM_SPINS, STREAK_LENGTH)
    
    print("\n" + "=" * 70)
    print("RESULTS:")
    print("=" * 70)
    print(f"\nProbability of getting streaks of {STREAK_LENGTH} consecutive reds in {NUM_SPINS} spins:")
    print(f"  - Zero streaks:           {results['zero_streaks']:6.2f}%")
    print(f"  - At least ONE streak:    {results['at_least_one']:6.2f}%")
    print(f"  - Exactly one streak:     {results['exactly_one']:6.2f}%")
    print(f"  - At least TWO streaks:   {results['at_least_two']:6.2f}%")
    print(f"  - Exactly two streaks:    {results['exactly_two']:6.2f}%")
    print(f"  - At least THREE streaks: {results['at_least_three']:6.2f}%")
    print(f"  - Exactly three streaks:  {results['exactly_three']:6.2f}%")
    print(f"  - Four or more streaks:   {results['four_or_more']:6.2f}%")
    
    print(f"\n" + "=" * 70)
    print("KEY INSIGHTS:")
    print("=" * 70)
    print(f"  - Single {STREAK_LENGTH}-red streak occurrence: ~{results['at_least_one']:.1f}%")
    print(f"  - TWO {STREAK_LENGTH}-red streaks occurrence:   ~{results['at_least_two']:.2f}%")
    print(f"  - Three {STREAK_LENGTH}-red streaks occurrence:   ~{results['at_least_three']:.2f}%")
    print(f"  - Four or more {STREAK_LENGTH}-red streaks occurrence:   ~{results['four_or_more']:.2f}%")
    print(f"  - Ratio (two streaks/one streak): {results['at_least_two']/results['at_least_one']:.4f}")
    print("\nNote: These are non-overlapping streaks.")
    print("=" * 70)


if __name__ == "__main__":
    main()
