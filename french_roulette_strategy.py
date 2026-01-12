"""
French Roulette Emulator
Simulates French Roulette with all standard rules including:
- Single zero (0)
- La Partage rule: Even money bets lose only half when 0 hits
- All standard betting options
"""

import random
import logging
from enum import Enum
from typing import List, Dict, Tuple, Optional
import requests

import time

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create console handler
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Create file handler
    file_handler = logging.FileHandler('roulette_simulation.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

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
    GREEN = "green"  # Single zero (0)


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
    
    def __init__(self, seed: Optional[int] = None, random_numbers: Optional[List[int]] = None):
        """
        Initialize the roulette emulator.
        
        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
        self.history: List[int] = []
        self.red_count =  0
        self.black_count = 0
        self.zero_count = 0
        self.random_numbers = random_numbers if random_numbers is not None else []
        self.random_index = 0
        self.spin_count = 1


    def get_spin_count(self) -> int:
        """
        Get the total number of spins played.
        
        Returns:
            Total spins count
        """
        return self.spin_count          

    def spin(self) -> int:
        """
        Spin the roulette wheel.
        
        Returns:
            The number that came up (0-36)
        """

        if self.random_numbers is not None and len(self.random_numbers) > 0:
            self.random_index   = self.spin_count % len(self.random_numbers)
            random_number = self.random_numbers[self.random_index]            
            result = random_number
        else:
            result = random.choice(self.NUMBERS)
    
        self.history.append(result)
        self.spin_count += 1
        return result

    def get_last_result(self) -> Optional[int]:
        """
        Get the last spin result.
        
        Returns:
            The last number that came up, or None if no spins yet
        """
        if not self.history:
            return None
        return self.history[-1]         
    
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
        if  result in self.RED_NUMBERS:
            self.red_count += 1
        elif result in self.BLACK_NUMBERS:
            self.black_count += 1
        else:
            self.zero_count += 1

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
            RED, BLACK, or 'green' (for 0)
        """
        if number == 0:
            return BetType.GREEN
        elif number in self.RED_NUMBERS:
            return BetType.RED
        else:
            return BetType.BLACK
    def get_number_of_streak_color(self, color: str) -> int:
        """
        Get the number of consecutive spins of a given color.
        
        Args:
            color: RED or BLACK
            
        Returns:
            Number of consecutive spins of the specified color
        """
        count = 0
        for number in reversed(self.history):
            if (color == BetType.RED and number in self.RED_NUMBERS) or \
               (color == BetType.BLACK and number in self.BLACK_NUMBERS):
                count += 1
            else:
                break
        return count

    def get_odds_streak_color(self, k:int) -> float:
        """
        odds = (1/2)^(k +1)
        Get the odds of getting a streak of k consecutive spins of a given color.   
        """
        odds = (18/37) ** (k + 1)
        return odds

    def get_black_red_ratio(self) -> float:
        """
        Get the ratio of black to red spins.
        
        Returns:
            Ratio of black spins to red spins
        """
        if self.red_count == 0:
            return float('inf')  # Avoid division by zero
        return self.black_count / self.red_count
    
    def get_red_black_ratio(self) -> float:
        """
        Get the ratio of red to black spins.
        
        Returns:
            Ratio of red spins to black spins
        """
        if self.black_count == 0:
            return float('inf')  # Avoid division by zero
        return self.red_count / self.black_count
        
    def get_red_count(self) -> int: 
        """
        Get the count of red spins.
        
        Returns:
            Count of red spins
        """
        return self.red_count
    
    def get_black_count(self) -> int:
        """
        Get the count of black spins.
        
        Returns:
            Count of black spins
        """
        return self.black_count

    def get_zero_count(self) -> int:
        """
        Get the count of zero spins.
        
        Returns:
            Count of zero spins
        """
        return self.zero_count
    

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
    logger.info("=== French Roulette Emulator Demo ===\n")
    
    # Create emulator instance
    import time
    current_sec = int(time.time())  # Get current time in microseconds
    roulette = FrenchRouletteEmulator(seed=current_sec)
    
    # Example 1: Simple single bet
    logger.info("Example 1: Betting $10 on Red")
    result, profit = roulette.play_round([
        (BetType.RED, 10, [])
    ])
    color = roulette.get_color(result)
    logger.info(f"Result: {result} ({color})")
    logger.info(f"Profit/Loss: ${profit:.2f}\n")
    
    # Example 2: Multiple bets in one round
    logger.info("Example 2: Multiple bets")
    logger.info("- $5 on Black")
    logger.info("- $10 on number 17 (straight)")
    logger.info("- $20 on first dozen (1-12)")
    result, profit = roulette.play_round([
        (BetType.BLACK, 5, []),
        (BetType.STRAIGHT, 10, [17]),
        (BetType.DOZEN_1, 20, [])
    ])
    color = roulette.get_color(result)
    logger.info(f"Result: {result} ({color})")
    logger.info(f"Total Profit/Loss: ${profit:.2f}\n")
    
    # Example 3: Demonstrating La Partage rule
    logger.info("Example 3: La Partage Rule (when 0 hits on even money bet)")
    # Force a zero for demonstration
    roulette.history.append(0)
    result = 0
    profit = roulette.calculate_payout(BetType.RED, 100, [], result, la_partage=True)
    logger.info(f"Bet: $100 on Red")
    logger.info(f"Result: 0 (green)")
    logger.info(f"With La Partage: Lose ${-profit:.2f} (only half)")
    profit_without = roulette.calculate_payout(BetType.RED, 100, [], result, la_partage=False)
    logger.info(f"Without La Partage: Lose ${-profit_without:.2f} (full amount)\n")
    
    # Example 4: Strategy simulation
    logger.info("Example 4: Simple Martingale Strategy on Red (10 spins)")
    bankroll = 1000
    base_bet = 10
    current_bet = base_bet
    wins = 0
    losses = 0
    
    logger.info(f"Starting Bankroll: ${bankroll:.2f}\n")
    
    for i in range(10):
        result, profit = roulette.play_round([
            (BetType.RED, current_bet, [])
        ])
        bankroll += profit
        color = roulette.get_color(result)
        
        if profit > 0:
            logger.info(f"Spin {i+1}: {result} ({color}) - Bet: ${current_bet:.2f} - WIN ${profit:.2f} - Bankroll: ${bankroll:.2f}")
            current_bet = base_bet  # Reset to base bet after win
            wins += 1
        else:
            logger.info(f"Spin {i+1}: {result} ({color}) - Bet: ${current_bet:.2f} - LOSS ${profit:.2f} - Bankroll: ${bankroll:.2f}")
            current_bet = min(current_bet * 2, bankroll)  # Double bet, but not more than bankroll
            losses += 1
    
    logger.info(f"\nFinal Bankroll: ${bankroll:.2f}")
    logger.info(f"Net Profit/Loss: ${bankroll - 1000:.2f}")
    logger.info(f"Wins: {wins}, Losses: {losses}\n")
    
    # Example 5: Statistics
    logger.info("Example 5: Spin Statistics")
    stats = roulette.get_statistics()
    logger.info(f"Total Spins: {stats['total_spins']}")
    logger.info(f"Red: {stats['red_count']} ({stats['red_count']/stats['total_spins']*100:.1f}%)")
    logger.info(f"Black: {stats['black_count']} ({stats['black_count']/stats['total_spins']*100:.1f}%)")
    logger.info(f"Zero: {stats['zero_count']} ({stats['zero_count']/stats['total_spins']*100:.1f}%)")
    logger.info(f"Last 10 spins: {stats['last_10']}")



ADJUSTMENT_TABLE = [
    # min, max, adjustment
    (0.20, 0.90, 0.10),
    (1.00, 1.80, 0.20),    
    (2.00, 3.60, 0.40),
    (4.00, 7.20, 0.80),
    (8.00, 12.80, 1.20),
    (14.00, 22.00, 2.00),
    (24.00, 44.00, 4.00),]

# ADJUSTMENT_TABLE = [
#     # min, max, adjustment
#     (0.20, 3.80, 0.20),
#     (4.00, 7.60, 0.40),
#     (8.00, 12.50, 0.50),
#     ]

BET_ZERO_TABLE = [
    # bet, bet on zero
    (0.10, 0.10),
    (3.50, 0.10),
    (7.00, 0.20),
    (10.50, 0.30),
    (14.30, 0.40),
    (18.00, 0.50),
]

def get_zero_bet(current_bet: float) -> float:
    """Determine the bet amount for zero based on current bet."""
    for bet, bet_on_zero in BET_ZERO_TABLE:
        if current_bet <= bet:
            return bet_on_zero
    raise ValueError(f"Current bet {current_bet} out of zero bet table range.")

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

def print_spin_status(sim_num: int, spin_count: int, bankroll: float, current_bet: float, win_count: int, loss_count: int, red_count: int, black_count: int, last_result: Optional[int] = None, prev_bet: float = 0.0) -> None:
    """
    Print the current status of a simulation spin.
    
    Args:
        spin_count: Current spin number
        bankroll: Current bankroll amount
        current_bet: Current bet amount
        red_count: Count of red spins
        black_count: Count of black spins
        last_result: The last spin result number
        prev_bet: The previous bet amount
    """
    last_result_str = f" | Last: {last_result}" if last_result is not None else ""
    prev_bet_str = f" | Prev Bet: ${prev_bet:5.2f}" if prev_bet > 0 else ""
    logger.info(f"Sim {sim_num} | Spin #{spin_count:3d} | Wins: {win_count:3d} | Losses: {loss_count:3d} | Red: {red_count:3d} | Black: {black_count:3d}{last_result_str}{prev_bet_str} | Bankroll: ${bankroll:8.2f} | Current Bet: ${current_bet:5.2f}")


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

    NUM_SIMULATIONS =  10
    SPINS_PER_SIMULATION = 120
    STARTING_BANKROLL = 1000.00
    STARTING_BET = 1.20
    BET_ADJUSTMENT = 0.20
    MIN_BET = 0.20
    MAX_BET = 8.00
    SWITCH_RATIO = 1.5

    sim_switch_track = []
    sim_win_track = []

    
    # Track results
    results = []
    bankruptcies = 0
    max_bet_reached = 0
    min_bet_reached = 0
    completed_all_spins = 0

    def get_random_numbers() -> List[int]:
        url="https://www.random.org/integers/?num=201&min=0&max=36&col=10&base=10&format=plain&rnd=new"
        resp = requests.get(url)
        text = resp.text   
        numbers = []
        for line in text.strip().split('\n'):
            numbers.extend([int(num) for num in line.split()])
        return numbers


    def get_first_bets(color) -> List[Tuple[BetType, float, List[int]]]:
        if color ==  BetType.BLACK:
            bets = [
                (BetType.BLACK, STARTING_BET, [])
            ]
        else:
            bets = [
                (BetType.RED, STARTING_BET, [])
            ] 
        return bets
    
    def get_next_color_bet(spins:int, new_bet_tuple: Tuple[BetType, float, List[int]], roulette: FrenchRouletteEmulator) -> Tuple[BetType, float, List[int]]:
        c_bet_color = new_bet_tuple[0]
        if c_bet_color == BetType.RED: # red is over shooting
            if spins >= 12 and roulette.get_red_black_ratio() >= SWITCH_RATIO:
                new_bet_tuple = (BetType.BLACK, new_bet_tuple[1], []) 
                logger.info(f"Sim {sim_num} Switching bet to BLACK due to Red dominance at spin {spins}.")
                sim_switch_track.append(sim_num + 1)
                return  new_bet_tuple

        if c_bet_color == BetType.BLACK: # black is over shooting
            if spins >= 12 and roulette.get_black_red_ratio() >= SWITCH_RATIO:
                new_bet_tuple = (BetType.RED, new_bet_tuple[1], []) 
                logger.info(f"Sim {sim_num} Switching bet to RED due to Black dominance at spin {spins}.")
                sim_switch_track.append(sim_num + 1)
                return  new_bet_tuple
            
        return new_bet_tuple

    def min_bet_reached_switch_color(spins:int, bet_color, bet_amount) -> Tuple[BetType, float, List[int]] | None:

        if bet_color == BetType.RED: # red is over shooting
            if spins < 12 :
                new_bet_tuple = (BetType.BLACK, bet_amount, []) 
                logger.info(f"Sim {sim_num} Switching bet to BLACK at spin {spins}. Reached Min too fast")
                sim_switch_track.append(sim_num + 1)
                return  new_bet_tuple

        if bet_color == BetType.BLACK: # black is over shooting
            if spins < 12 :
                new_bet_tuple = (BetType.RED, bet_amount, []) 
                logger.info(f"Sim {sim_num} Switching bet to RED at spin {spins}. Reached Min too fast")
                sim_switch_track.append(sim_num + 1)
                return  new_bet_tuple

        return None

    logger.info("=== Roulette Betting Strategy Simulation ===")
    logger.info(f"Running {NUM_SIMULATIONS} simulations...")
    logger.info(f"Parameters:")
    logger.info(f"  - Spins per simulation: {SPINS_PER_SIMULATION}")
    logger.info(f"  - Starting bankroll: ${STARTING_BANKROLL:.2f}")
    logger.info(f"  - Starting bet: ${STARTING_BET:.2f}")
    logger.info(f"  - Bet adjustment: ${BET_ADJUSTMENT:.2f}")
    logger.info(f"  - Bet limits: ${MIN_BET:.2f} - ${MAX_BET:.2f}")

    using_random_org = False



    for sim_num in range(NUM_SIMULATIONS):
        import time
        current_sec = int(time.time())  # Get current time in microseconds
        if using_random_org:
            random_numbers = get_random_numbers()
        else:
            random_numbers = [random.randint(0,36) for _ in range(1001)]


        time.sleep(2)  # To avoid hitting the API rate limit

        roulette = FrenchRouletteEmulator(seed=current_sec)

        bankroll = STARTING_BANKROLL
        current_bet_amount = STARTING_BET
        spins_completed = 0
        stop_reason = None
        first_time = True
        win_count = 0
        loss_count = 0
        
        color = roulette.get_color(random_numbers[0])
        bets = get_first_bets(color)  
        logger.info(f"Sim {sim_num} - First Betting on: {bets[0][0].name}")
     
        spin = 0
        while stop_reason is None:
            # Check if we have enough money to bet
            if bankroll < current_bet_amount:
                stop_reason = "bankruptcy"
                bankruptcies += 1
                break
            
            if spin >= SPINS_PER_SIMULATION and bankroll - STARTING_BANKROLL > 6.00:
                stop_reason = "end_stop_profit"
                break

            if spin >= SPINS_PER_SIMULATION and win_count > loss_count :
                stop_reason = "ext_stop_profit"
                break

            red_count = roulette.get_red_count()
            black_count = roulette.get_black_count()
            if spin >= 12 and red_count == black_count and bankroll > STARTING_BANKROLL:
                logger.info(f"Spin {spin}: Equal win and loss count stop playing - profit {bankroll - STARTING_BANKROLL:.2f}.")
                stop_reason = "equal_red_black_stop"
                break
            
            # Play round

            result, profit = roulette.play_round(bets)

            bankroll += profit
            spins_completed += 1
            
            # Adjust bet based on win/loss
            prev_bet_amount = current_bet_amount
            if profit > 0:  # Won
                new_bet_amount = get_bet_decrease(current_bet_amount)
                current_bet_amount = round(new_bet_amount, 2)
                win_count += 1
                if first_time == False:
                    logger.info("Win on spin {}: Result {}, Profit ${:.2f}, New Bet ${:.2f}, Bankroll ${:.2f}".format(
                        spin + 1, result, profit, current_bet_amount, bankroll))
                # Check if bet reached minimum
                if current_bet_amount <= MIN_BET:
                    new_bets = min_bet_reached_switch_color(spin, bets[0][0] ,STARTING_BET)
                    if new_bets is None:
                        stop_reason = "min_bet"
                        min_bet_reached += 1
                        break
                    else:
                        new_bet_amount = STARTING_BET
                        bets = [new_bets]

            else:  # Lost (includes La Partage on zero)
                new_bet_amount = get_bet_increase(current_bet_amount)
                current_bet_amount = round(new_bet_amount, 2)
                loss_count += 1
                # Check if bet reached maximum
                if current_bet_amount >= MAX_BET : #and  (loss_count/(win_count +1) ) < 1.2:
                    current_bet_amount = MAX_BET
                    stop_reason = "max_bet"
                    max_bet_reached += 1
                    break
            spin += 1
            print_spin_status(sim_num, spins_completed, bankroll, current_bet_amount, win_count, loss_count, roulette.get_red_count(), roulette.get_black_count(), roulette.get_last_result(), prev_bet_amount)    
            first_time = False
            if first_time == False:
                current_bet_amount = round(new_bet_amount, 2)
                bets = [get_next_color_bet(spin, (bets[0][0],new_bet_amount, [])  , roulette)]
            #end of spins loop

        # Check if completed all spins
        if stop_reason is None:
            stop_reason = "completed"
            completed_all_spins += 1

    
        profit_loss = bankroll - STARTING_BANKROLL

        if profit_loss > 0:
            sim_win_track.append(sim_num + 1)

        import pandas as pd
        #print_spin_status(spins_completed, bankroll, current_bet)
        results.append({
            'simulation': sim_num + 1,
            'final_bankroll': bankroll,
            'profit_loss': profit_loss,
            'spins_completed': spins_completed,
            'stop_reason': stop_reason,
            'win_count': win_count,
            'loss_count': loss_count
        })
        print_spin_status(sim_num, spins_completed, bankroll, current_bet_amount,
                           win_count, loss_count, roulette.get_red_count(), roulette.get_black_count(), roulette.get_last_result(), current_bet_amount)
        # Print progress every 100 simulations
        if (sim_num + 1) % 100 == 0:
            logger.info(f"Completed {sim_num + 1}/{NUM_SIMULATIONS} simulations...")
        logger.info(f"======> {stop_reason}")
        # end of simulation loop
        if roulette.history is not None:
            result2 = ",".join(str(n) for n in roulette.history)
            logger.info(f"history: {result2}")
        logger.info("-" * 120)

    sim_switch_track = list(set(sim_switch_track))
    sim_switch_track.sort()

    logger.info("\n=== Simulation Results ===\n")
    
    # Print switch and win ratios
    logger.info(f"Simulations that switched bets: {len(sim_switch_track)} ({len(sim_switch_track)/NUM_SIMULATIONS*100:.1f}%)")
    logger.info(f"Simulations that won: {len(sim_win_track)} ({len(sim_win_track)/NUM_SIMULATIONS*100:.1f}%)")
    
    # Calculate overlap between switch and win
    switch_and_win = len(set(sim_switch_track) & set(sim_win_track))
    logger.info(f"Simulations that both switched and won: {switch_and_win}")
    if len(sim_switch_track) > 0:
        logger.info(f"  - Of simulations that switched, {switch_and_win/len(sim_switch_track)*100:.1f}% won")
    if len(sim_win_track) > 0:
        logger.info(f"  - Of simulations that won, {switch_and_win/len(sim_win_track)*100:.1f}% had switched")
    logger.info("")

    # Calculate statistics

    profit_losses = [r['profit_loss'] for r in results]

    df = pd.DataFrame([{
        'final_bankroll': r['final_bankroll'],
        'profit_loss': r['profit_loss'],
        'spins_completed': r['spins_completed'],
        'win_count': r['win_count'],
        'loss_count': r['loss_count']
    } for r in results])
    
    logger.info(df.describe())
    logger.info("")
 
    logger.info(f"Win Count - Median: {df['win_count'].median()}, Mean: {df['win_count'].mean():.2f}")
    logger.info("")
    
    winning_simulations = sum(1 for p in profit_losses if p > 0)
    losing_simulations = sum(1 for p in profit_losses if p < 0)
    breakeven_simulations = sum(1 for p in profit_losses if p == 0)
    
    max_profit = max(profit_losses)
    max_loss = min(profit_losses)
    
    best_sim = results[profit_losses.index(max_profit)]
    worst_sim = results[profit_losses.index(max_loss)]
    
    # Print summary statistics
    logger.info(f"Average Final Bankroll: ${df['final_bankroll'].mean():.2f}")
    logger.info(f"Average Profit/Loss: ${df['profit_loss'].mean():.2f}")
    logger.info(f"Average Spins Completed: {df['spins_completed'].mean():.1f}")
    logger.info("")
    
    logger.info(f"Winning Simulations: {winning_simulations} ({winning_simulations/NUM_SIMULATIONS*100:.1f}%)")
    logger.info(f"Losing Simulations: {losing_simulations} ({losing_simulations/NUM_SIMULATIONS*100:.1f}%)")
    logger.info(f"Break-even Simulations: {breakeven_simulations} ({breakeven_simulations/NUM_SIMULATIONS*100:.1f}%)")
    logger.info("")
    
    logger.info(f"Best Result: ${max_profit:.2f} (Simulation #{best_sim['simulation']}, {best_sim['spins_completed']} spins)")
    logger.info(f"Worst Result: ${max_loss:.2f} (Simulation #{worst_sim['simulation']}, {worst_sim['spins_completed']} spins)")
    logger.info("")
    
    logger.info("Stop Reasons:")
    logger.info(f"  - Completed all {SPINS_PER_SIMULATION} spins: {completed_all_spins} ({completed_all_spins/NUM_SIMULATIONS*100:.1f}%)")
    logger.info(f"  - Reached minimum bet (${MIN_BET}): {min_bet_reached} ({min_bet_reached/NUM_SIMULATIONS*100:.1f}%)")
    logger.info(f"  - Reached maximum bet (${MAX_BET}): {max_bet_reached} ({max_bet_reached/NUM_SIMULATIONS*100:.1f}%)")
    logger.info(f"  - Bankruptcy (insufficient funds): {bankruptcies} ({bankruptcies/NUM_SIMULATIONS*100:.1f}%)")
    logger.info("")
    
    # Profit/Loss Distribution
    logger.info("Profit/Loss Distribution:")
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
            
            message = f"  {label:20s}: {count:4d} ({percentage:5.1f}%)"
            print(f"{message} {bar}")
            logger.info(message)

    
    stats = roulette.get_statistics()
    logger.info(f"Zero count: {stats['zero_count']}")
    return results


if __name__ == "__main__":
    run_simulation()