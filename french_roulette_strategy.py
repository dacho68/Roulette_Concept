"""
French Roulette Emulator
Simulates French Roulette with all standard rules including:
- Single zero (0)
- La Partage rule: Even money bets lose only half when 0 hits
- All standard betting options
"""

import random
from enum import Enum
from typing import List, Dict, Tuple, Optional


class BetType(Enum):
    """Types of bets available in French Roulette"""
    # Inside bets
    STRAIGHT = "straight"  # Single number
    SPLIT = "split"  # Two adjacent numbers
    STREET = "street"  # Three numbers in a row
    CORNER = "corner"  # Four numbers
    LINE = "line"  # Six numbers (two streets)
    
    # Outside bets
    RED = "red"
    BLACK = "black"
    EVEN = "even"
    ODD = "odd"
    LOW = "low"  # 1-18
    HIGH = "high"  # 19-36
    DOZEN_1 = "dozen_1"  # 1-12
    DOZEN_2 = "dozen_2"  # 13-24
    DOZEN_3 = "dozen_3"  # 25-36
    COLUMN_1 = "column_1"  # 1,4,7,10...34
    COLUMN_2 = "column_2"  # 2,5,8,11...35
    COLUMN_3 = "column_3"  # 3,6,9,12...36


class FrenchRouletteEmulator:
    """
    Emulator for French Roulette with standard rules.
    Features:
    - Single zero (0-36)
    - La Partage rule for even money bets
    - All standard betting options
    """
    
    # Roulette wheel numbers
    NUMBERS = list(range(0, 37))  # 0-36
    
    # Red numbers in roulette
    RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    
    # Black numbers (all non-red, non-zero numbers)
    BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the roulette emulator.
        
        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        self.history: List[int] = []
        
    def spin(self) -> int:
        """
        Spin the roulette wheel.
        
        Returns:
            The number that came up (0-36)
        """
        result = random.choice(self.NUMBERS)
        self.history.append(result)
        return result
    
    def check_bet(self, bet_type: BetType, bet_numbers: List[int], result: int) -> bool:
        """
        Check if a bet wins.
        
        Args:
            bet_type: Type of bet placed
            bet_numbers: Numbers bet on (for inside bets)
            result: The number that came up
            
        Returns:
            True if the bet wins, False otherwise
        """
        if bet_type == BetType.STRAIGHT:
            return result in bet_numbers
        elif bet_type == BetType.SPLIT:
            return result in bet_numbers
        elif bet_type == BetType.STREET:
            return result in bet_numbers
        elif bet_type == BetType.CORNER:
            return result in bet_numbers
        elif bet_type == BetType.LINE:
            return result in bet_numbers
        elif bet_type == BetType.RED:
            return result in self.RED_NUMBERS
        elif bet_type == BetType.BLACK:
            return result in self.BLACK_NUMBERS
        elif bet_type == BetType.EVEN:
            return result != 0 and result % 2 == 0
        elif bet_type == BetType.ODD:
            return result != 0 and result % 2 == 1
        elif bet_type == BetType.LOW:
            return 1 <= result <= 18
        elif bet_type == BetType.HIGH:
            return 19 <= result <= 36
        elif bet_type == BetType.DOZEN_1:
            return 1 <= result <= 12
        elif bet_type == BetType.DOZEN_2:
            return 13 <= result <= 24
        elif bet_type == BetType.DOZEN_3:
            return 25 <= result <= 36
        elif bet_type == BetType.COLUMN_1:
            return result % 3 == 1 and result != 0
        elif bet_type == BetType.COLUMN_2:
            return result % 3 == 2 and result != 0
        elif bet_type == BetType.COLUMN_3:
            return result % 3 == 0 and result != 0
        return False
    
    def get_payout_multiplier(self, bet_type: BetType) -> float:
        """
        Get the payout multiplier for a bet type.
        
        Args:
            bet_type: Type of bet
            
        Returns:
            Payout multiplier (includes original stake)
        """
        payouts = {
            BetType.STRAIGHT: 36,  # 35:1 + original stake
            BetType.SPLIT: 18,  # 17:1 + original stake
            BetType.STREET: 12,  # 11:1 + original stake
            BetType.CORNER: 9,  # 8:1 + original stake
            BetType.LINE: 6,  # 5:1 + original stake
            BetType.RED: 2,  # 1:1 + original stake
            BetType.BLACK: 2,  # 1:1 + original stake
            BetType.EVEN: 2,  # 1:1 + original stake
            BetType.ODD: 2,  # 1:1 + original stake
            BetType.LOW: 2,  # 1:1 + original stake
            BetType.HIGH: 2,  # 1:1 + original stake
            BetType.DOZEN_1: 3,  # 2:1 + original stake
            BetType.DOZEN_2: 3,  # 2:1 + original stake
            BetType.DOZEN_3: 3,  # 2:1 + original stake
            BetType.COLUMN_1: 3,  # 2:1 + original stake
            BetType.COLUMN_2: 3,  # 2:1 + original stake
            BetType.COLUMN_3: 3,  # 2:1 + original stake
        }
        return payouts[bet_type]
    
    def is_even_money_bet(self, bet_type: BetType) -> bool:
        """
        Check if a bet is an even money bet (affected by La Partage rule).
        
        Args:
            bet_type: Type of bet
            
        Returns:
            True if it's an even money bet
        """
        return bet_type in [BetType.RED, BetType.BLACK, BetType.EVEN, 
                           BetType.ODD, BetType.LOW, BetType.HIGH]
    
    def calculate_payout(self, bet_type: BetType, bet_amount: float, 
                        bet_numbers: List[int], result: int,
                        la_partage: bool = True) -> float:
        """
        Calculate the payout for a bet.
        
        Args:
            bet_type: Type of bet placed
            bet_amount: Amount bet
            bet_numbers: Numbers bet on (for inside bets)
            result: The number that came up
            la_partage: Whether to apply La Partage rule (default True for French Roulette)
            
        Returns:
            Net profit/loss (positive for win, negative for loss)
        """
        # Check for La Partage rule (zero with even money bet)
        if result == 0 and self.is_even_money_bet(bet_type) and la_partage:
            # Return half the bet (lose only half)
            return -bet_amount / 2
        
        # Check if bet wins
        if self.check_bet(bet_type, bet_numbers, result):
            multiplier = self.get_payout_multiplier(bet_type)
            return bet_amount * (multiplier - 1)  # Subtract 1 because we return net profit
        else:
            return -bet_amount
    
    def play_round(self, bets: List[Tuple[BetType, float, List[int]]], 
                   la_partage: bool = True) -> Tuple[int, float]:
        """
        Play a complete round with multiple bets.
        
        Args:
            bets: List of (bet_type, bet_amount, bet_numbers) tuples
            la_partage: Whether to apply La Partage rule
            
        Returns:
            Tuple of (result number, total net profit/loss)
        """
        result = self.spin()
        total_payout = 0
        
        for bet_type, bet_amount, bet_numbers in bets:
            payout = self.calculate_payout(bet_type, bet_amount, bet_numbers, 
                                          result, la_partage)
            total_payout += payout
        
        return result, total_payout
    
    def get_color(self, number: int) -> str:
        """
        Get the color of a number.
        
        Args:
            number: The roulette number
            
        Returns:
            'red', 'black', or 'green' (for 0)
        """
        if number == 0:
            return 'green'
        elif number in self.RED_NUMBERS:
            return 'red'
        else:
            return 'black'
    
    def get_statistics(self) -> Dict:
        """
        Get statistics from spin history.
        
        Returns:
            Dictionary with various statistics
        """
        if not self.history:
            return {"total_spins": 0}
        
        return {
            "total_spins": len(self.history),
            "red_count": sum(1 for n in self.history if n in self.RED_NUMBERS),
            "black_count": sum(1 for n in self.history if n in self.BLACK_NUMBERS),
            "zero_count": sum(1 for n in self.history if n == 0),
            "even_count": sum(1 for n in self.history if n != 0 and n % 2 == 0),
            "odd_count": sum(1 for n in self.history if n != 0 and n % 2 == 1),
            "last_10": self.history[-10:] if len(self.history) >= 10 else self.history,
        }


# Example usage
def demo():
    print("=== French Roulette Emulator Demo ===\n")
    
    # Create emulator instance
    roulette = FrenchRouletteEmulator(seed=42)
    
    # Example 1: Simple single bet
    print("Example 1: Betting $10 on Red")
    result, profit = roulette.play_round([
        (BetType.RED, 10, [])
    ])
    color = roulette.get_color(result)
    print(f"Result: {result} ({color})")
    print(f"Profit/Loss: ${profit:.2f}\n")
    
    # Example 2: Multiple bets in one round
    print("Example 2: Multiple bets")
    print("- $5 on Black")
    print("- $10 on number 17 (straight)")
    print("- $20 on first dozen (1-12)")
    result, profit = roulette.play_round([
        (BetType.BLACK, 5, []),
        (BetType.STRAIGHT, 10, [17]),
        (BetType.DOZEN_1, 20, [])
    ])
    color = roulette.get_color(result)
    print(f"Result: {result} ({color})")
    print(f"Total Profit/Loss: ${profit:.2f}\n")
    
    # Example 3: Demonstrating La Partage rule
    print("Example 3: La Partage Rule (when 0 hits on even money bet)")
    # Force a zero for demonstration
    roulette.history.append(0)
    result = 0
    profit = roulette.calculate_payout(BetType.RED, 100, [], result, la_partage=True)
    print(f"Bet: $100 on Red")
    print(f"Result: 0 (green)")
    print(f"With La Partage: Lose ${-profit:.2f} (only half)")
    profit_without = roulette.calculate_payout(BetType.RED, 100, [], result, la_partage=False)
    print(f"Without La Partage: Lose ${-profit_without:.2f} (full amount)\n")
    
    # Example 4: Strategy simulation
    print("Example 4: Simple Martingale Strategy on Red (10 spins)")
    bankroll = 1000
    base_bet = 10
    current_bet = base_bet
    wins = 0
    losses = 0
    
    print(f"Starting Bankroll: ${bankroll:.2f}\n")
    
    for i in range(10):
        result, profit = roulette.play_round([
            (BetType.RED, current_bet, [])
        ])
        bankroll += profit
        color = roulette.get_color(result)
        
        if profit > 0:
            print(f"Spin {i+1}: {result} ({color}) - Bet: ${current_bet:.2f} - WIN ${profit:.2f} - Bankroll: ${bankroll:.2f}")
            current_bet = base_bet  # Reset to base bet after win
            wins += 1
        else:
            print(f"Spin {i+1}: {result} ({color}) - Bet: ${current_bet:.2f} - LOSS ${profit:.2f} - Bankroll: ${bankroll:.2f}")
            current_bet = min(current_bet * 2, bankroll)  # Double bet, but not more than bankroll
            losses += 1
    
    print(f"\nFinal Bankroll: ${bankroll:.2f}")
    print(f"Net Profit/Loss: ${bankroll - 1000:.2f}")
    print(f"Wins: {wins}, Losses: {losses}\n")
    
    # Example 5: Statistics
    print("Example 5: Spin Statistics")
    stats = roulette.get_statistics()
    print(f"Total Spins: {stats['total_spins']}")
    print(f"Red: {stats['red_count']} ({stats['red_count']/stats['total_spins']*100:.1f}%)")
    print(f"Black: {stats['black_count']} ({stats['black_count']/stats['total_spins']*100:.1f}%)")
    print(f"Zero: {stats['zero_count']} ({stats['zero_count']/stats['total_spins']*100:.1f}%)")
    print(f"Last 10 spins: {stats['last_10']}")

ADJUSTMENT_TABLE = [
    # min, max, adjustment
    (0.20, 0.90, 0.10),
    (1.00, 1.80, 0.20),    
    (2.00, 3.60, 0.40),
    (4.00, 7.20, 0.80),
    (8.00, 12.80, 1.20),
    (14.00, 20.00, 2.00),
]

BET_ZERO_TABLE = [
    # min, max, adjustment
    (3.50, 0.10),
    (7.00, 0.20),
    (10.50, 0.30),
    (14.30, 0.40),
    (18.00, 0.50),
]

def get_next_bet_adjustment(current_bet: float) -> float:
    """Adjust bet downwards on win, not going below min_bet."""
    for min_bet, max_bet, adjustment in ADJUSTMENT_TABLE:
        if min_bet <= current_bet <= max_bet:
            return adjustment
    raise ValueError(f"Current bet {current_bet} out of adjustment table range.")

def get_bet_increase(current_bet: float) -> float:
    new_bet = current_bet + get_next_bet_adjustment(current_bet)
    return round(new_bet, 2)

def get_bet_decrease(current_bet: float) -> float:

    prev_adjustment = 0.0
    for i , (min_bet, max_bet, adjustment) in enumerate(ADJUSTMENT_TABLE):
        if min_bet == current_bet:
            prev_adjustment = ADJUSTMENT_TABLE[i-1][2] if i > 0 else adjustment
        elif min_bet < current_bet <= max_bet:
            prev_adjustment = ADJUSTMENT_TABLE[i][2]
            
    if prev_adjustment == 0.0:
        raise ValueError(f"Current bet {current_bet} out of adjustment table range.")
    
    new_bet = current_bet - prev_adjustment
    return round(new_bet, 2)

def print_spin_status(spin_count: int, bankroll: float, current_bet: float) -> None:
    """
    Print the current status of a simulation spin.
    
    Args:
        spin_count: Current spin number
        bankroll: Current bankroll amount
        current_bet: Current bet amount
    """
    print(f"Spin #{spin_count:3d} | Bankroll: ${bankroll:8.2f} | Current Bet: ${current_bet:5.2f}")

def run_simulation():
    """
    Run 1000 simulations with the specified betting strategy:
    - 100 spins per simulation
    - Starting bankroll: $1000
    - Starting bet: $2.00
    - Bet on Red
    - If lost: increase bet by $0.20
    - If won: decrease bet by $0.20
    - Stop if bet reaches $0.20 or $6.00
    """

    NUM_SIMULATIONS =  1000
    SPINS_PER_SIMULATION = 100
    STARTING_BANKROLL = 1000.00
    STARTING_BET = 1.00
    BET_ADJUSTMENT = 0.20
    MIN_BET = 0.20
    MAX_BET = 20.00
    
    
    # Track results
    results = []
    bankruptcies = 0
    max_bet_reached = 0
    min_bet_reached = 0
    completed_all_spins = 0
    
    print("=== Roulette Betting Strategy Simulation ===")
    print(f"Running {NUM_SIMULATIONS} simulations...")
    print(f"Parameters:")
    print(f"  - Spins per simulation: {SPINS_PER_SIMULATION}")
    print(f"  - Starting bankroll: ${STARTING_BANKROLL:.2f}")
    print(f"  - Starting bet: ${STARTING_BET:.2f}")
    print(f"  - Bet adjustment: ${BET_ADJUSTMENT:.2f}")
    print(f"  - Bet limits: ${MIN_BET:.2f} - ${MAX_BET:.2f}")
    print(f"  - Betting on: Red")
    print()
    
    for sim_num in range(NUM_SIMULATIONS):
        roulette = FrenchRouletteEmulator()
        bankroll = STARTING_BANKROLL
        current_bet = STARTING_BET
        spins_completed = 0
        stop_reason = None
        
        for spin in range(SPINS_PER_SIMULATION):
            # Check if we have enough money to bet
            if bankroll < current_bet:
                stop_reason = "bankruptcy"
                bankruptcies += 1
                break
            
            # Place bet on Red
            result, profit = roulette.play_round([
                (BetType.RED, current_bet, [])
            ])
            
            bankroll += profit
            spins_completed += 1
            
            # Adjust bet based on win/loss
            if profit > 0:  # Won
                new_bet = get_bet_decrease(current_bet)
                current_bet = round(new_bet, 2)
                
                # Check if bet reached minimum
                if current_bet <= MIN_BET:
                    current_bet = MIN_BET
                    stop_reason = "min_bet"
                    min_bet_reached += 1
                    break
            else:  # Lost (includes La Partage on zero)
                new_bet = get_bet_increase(current_bet)
                current_bet = round(new_bet, 2)
                
                # Check if bet reached maximum
                if current_bet >= MAX_BET:
                    current_bet = MAX_BET
                    stop_reason = "max_bet"
                    max_bet_reached += 1
                    break
        
        # Check if completed all spins
        if stop_reason is None:
            stop_reason = "completed"
            completed_all_spins += 1
        
        print_spin_status(spins_completed, bankroll, current_bet)
        results.append({
            'simulation': sim_num + 1,
            'final_bankroll': bankroll,
            'profit_loss': bankroll - STARTING_BANKROLL,
            'spins_completed': spins_completed,
            'stop_reason': stop_reason
        })
        
        # Print progress every 100 simulations
        if (sim_num + 1) % 100 == 0:
            print(f"Completed {sim_num + 1}/{NUM_SIMULATIONS} simulations...")
    
    print("\n=== Simulation Results ===\n")
    
    # Calculate statistics
    final_bankrolls = [r['final_bankroll'] for r in results]
    profit_losses = [r['profit_loss'] for r in results]
    spins_completed_list = [r['spins_completed'] for r in results]
    
    avg_final_bankroll = sum(final_bankrolls) / len(final_bankrolls)
    avg_profit_loss = sum(profit_losses) / len(profit_losses)
    avg_spins = sum(spins_completed_list) / len(spins_completed_list)
    
    winning_simulations = sum(1 for p in profit_losses if p > 0)
    losing_simulations = sum(1 for p in profit_losses if p < 0)
    breakeven_simulations = sum(1 for p in profit_losses if p == 0)
    
    max_profit = max(profit_losses)
    max_loss = min(profit_losses)
    
    best_sim = results[profit_losses.index(max_profit)]
    worst_sim = results[profit_losses.index(max_loss)]
    
    # Print summary statistics
    print(f"Average Final Bankroll: ${avg_final_bankroll:.2f}")
    print(f"Average Profit/Loss: ${avg_profit_loss:.2f}")
    print(f"Average Spins Completed: {avg_spins:.1f}")
    print()
    
    print(f"Winning Simulations: {winning_simulations} ({winning_simulations/NUM_SIMULATIONS*100:.1f}%)")
    print(f"Losing Simulations: {losing_simulations} ({losing_simulations/NUM_SIMULATIONS*100:.1f}%)")
    print(f"Break-even Simulations: {breakeven_simulations} ({breakeven_simulations/NUM_SIMULATIONS*100:.1f}%)")
    print()
    
    print(f"Best Result: ${max_profit:.2f} (Simulation #{best_sim['simulation']}, {best_sim['spins_completed']} spins)")
    print(f"Worst Result: ${max_loss:.2f} (Simulation #{worst_sim['simulation']}, {worst_sim['spins_completed']} spins)")
    print()
    
    print("Stop Reasons:")
    print(f"  - Completed all {SPINS_PER_SIMULATION} spins: {completed_all_spins} ({completed_all_spins/NUM_SIMULATIONS*100:.1f}%)")
    print(f"  - Reached minimum bet (${MIN_BET}): {min_bet_reached} ({min_bet_reached/NUM_SIMULATIONS*100:.1f}%)")
    print(f"  - Reached maximum bet (${MAX_BET}): {max_bet_reached} ({max_bet_reached/NUM_SIMULATIONS*100:.1f}%)")
    print(f"  - Bankruptcy (insufficient funds): {bankruptcies} ({bankruptcies/NUM_SIMULATIONS*100:.1f}%)")
    print()
    
    # Profit/Loss Distribution
    print("Profit/Loss Distribution:")
    ranges = [
        (-float('inf'), -500, "< -$500"),
        (-500, -200, "-$500 to -$200"),
        (-200, -100, "-$200 to -$100"),
        (-100, 0, "-$100 to $0"),
        (0, 100, "$0 to $100"),
        (100, 200, "$100 to $200"),
        (200, 500, "$200 to $500"),
        (500, float('inf'), "> $500")
    ]
    
    for low, high, label in ranges:
        count = sum(1 for p in profit_losses if low <= p < high)
        if count > 0:
            percentage = count / NUM_SIMULATIONS * 100
            bar = '█' * int(percentage / 2)
            print(f"  {label:20s}: {count:4d} ({percentage:5.1f}%) {bar}")
    
    return results


if __name__ == "__main__":
    run_simulation()